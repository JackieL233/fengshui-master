"""Runtime regression tests for the opt-in proactive check-in contract."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import re
import socket
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = Path(
    os.environ.get(
        "FENGSHUI_CHECKIN_SCRIPT",
        ROOT / "fengshui-master" / "scripts" / "proactive_checkin.py",
    )
)
_RUNTIME = None

UTC = timezone.utc
SAMPLE_NOW = datetime.fromisoformat("2026-09-29T10:00:00+08:00")


def runtime():
    """Load the runtime lazily so manual runs can replace SCRIPT and ROOT."""
    global _RUNTIME
    if _RUNTIME is None:
        spec = importlib.util.spec_from_file_location("proactive_checkin", SCRIPT)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"cannot load runtime from {SCRIPT}")
        _RUNTIME = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_RUNTIME)
    return _RUNTIME


def sample_job() -> dict:
    return json.loads(
        (ROOT / "examples" / "proactive-checkin-job.json").read_text(encoding="utf-8")
    )


def reseal(job: dict) -> None:
    """Model an explicitly approved scope update in a test fixture."""
    subscription = job["subscription"]
    subscription["consent"]["scope_hash"] = runtime().consent_scope_fingerprint(subscription)


def timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def utc(value: datetime) -> datetime:
    return value.astimezone(UTC)


def set_event_window(job: dict, observed: datetime, expires: datetime) -> None:
    job["event"]["observed_at"] = observed.isoformat()
    job["event"]["expires_at"] = expires.isoformat()


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


class ProactiveCheckinTestCase(unittest.TestCase):
    def plan(self, job: dict, now: datetime = SAMPLE_NOW) -> dict:
        return runtime().plan_checkin(job, now)

    def assert_suppressed(self, job: dict, reason: str, now: datetime = SAMPLE_NOW) -> dict:
        decision = self.plan(job, now)
        self.assertEqual(decision["status"], "suppressed")
        self.assertEqual(decision["reason"], reason)
        return decision

    def assert_invalid(self, job: dict, now: datetime = SAMPLE_NOW) -> None:
        with self.assertRaises(ValueError):
            self.plan(job, now)

    def ready_and_ack(
        self,
        job: dict,
        now: datetime = SAMPLE_NOW,
        receipt: str = "provider-receipt-1",
        sent_at: datetime | None = None,
    ) -> tuple[dict, dict, datetime]:
        decision = self.plan(job, now)
        self.assertEqual(decision["status"], "ready")
        sent = sent_at or now
        state = runtime().acknowledge_delivery(job, decision, receipt, sent, sent)
        return decision, state, sent


class PlanContractTests(ProactiveCheckinTestCase):
    def test_authoritative_example_has_ready_contract_and_bounded_window(self):
        job = sample_job()
        before = copy.deepcopy(job)

        decision = self.plan(job)

        self.assertEqual(decision["status"], "ready")
        self.assertEqual(decision["subscription_id"], job["subscription"]["id"])
        self.assertEqual(decision["state_revision"], job["state"]["revision"])
        self.assertEqual(decision["recipient"], job["subscription"]["recipient"])
        self.assertEqual(decision["channel"], job["subscription"]["channel"])
        self.assertRegex(decision["fingerprint"], r"^[0-9a-f]{64}$")
        self.assertEqual(
            decision["delivery_id"], f"fsm-{decision['fingerprint']}"
        )

        planned_at = timestamp(decision["planned_at"])
        valid_until = timestamp(decision["valid_until"])
        self.assertEqual(planned_at, utc(SAMPLE_NOW))
        self.assertGreater(valid_until, planned_at)
        self.assertLessEqual(valid_until - planned_at, timedelta(minutes=5))
        self.assertIn("event_expires_at", decision)
        self.assertIn("subscription_expires_at", decision)
        self.assertEqual(
            timestamp(decision["event_expires_at"]),
            timestamp(job["event"]["expires_at"]).astimezone(UTC),
        )
        self.assertEqual(
            timestamp(decision["subscription_expires_at"]),
            timestamp(job["subscription"]["expires_at"]).astimezone(UTC),
        )
        self.assertEqual(
            decision["consent_scope"], job["subscription"]["consent"]["scope_hash"]
        )

        self.assertEqual(set(decision["message"]), {"title", "body", "language"})
        self.assertTrue(decision["message"]["title"].strip())
        self.assertTrue(decision["message"]["body"].strip())
        self.assertEqual(decision["message"]["language"], job["subscription"]["language"])
        self.assertIn(job["event"]["assessment"], decision["message"]["body"])
        self.assertIn(job["event"]["next_step"], decision["message"]["body"])
        self.assertEqual(job, before)

    def test_plan_is_pure_and_does_not_persist_a_delivery(self):
        job = sample_job()
        before = copy.deepcopy(job)

        decision = self.plan(job)

        self.assertEqual(decision["status"], "ready")
        self.assertEqual(job, before)
        self.assertEqual(job["state"], {"subscription_id": "demo-career-review", "revision": 0, "deliveries": []})

    def test_consent_pause_revocation_and_expiry_suppress(self):
        cases = {
            "consent_required": lambda job: job["subscription"]["consent"].update(granted=False),
            "subscription_paused": lambda job: job["subscription"].update(status="paused"),
            "subscription_revoked": lambda job: job["subscription"].update(status="revoked"),
            "subscription_expired": lambda job: job["subscription"].update(
                expires_at="2026-09-29T10:00:00+08:00"
            ),
            "consent_not_effective": lambda job: job["subscription"]["consent"].update(
                recorded_at="2026-09-29T11:00:00+08:00"
            ),
        }
        for reason, mutate in cases.items():
            with self.subTest(reason=reason):
                job = sample_job()
                mutate(job)
                reseal(job)
                self.assert_suppressed(job, reason)

    def test_scope_trigger_and_material_change_policy(self):
        job = sample_job()
        job["event"]["domain"] = "learning"
        self.assert_suppressed(job, "out_of_scope")

        job = sample_job()
        job["event"].update(
            trigger="calendar",
            changed=False,
            due_at="2026-09-29T09:30:00+08:00",
        )
        self.assert_suppressed(job, "trigger_not_enabled")

        job = sample_job()
        job["event"]["changed"] = False
        self.assert_suppressed(job, "no_material_change")

    def test_explicit_review_and_calendar_due_events_notify_when_unchanged(self):
        for trigger in ("review_due", "calendar"):
            with self.subTest(trigger=trigger):
                job = sample_job()
                job["subscription"]["triggers"] = [trigger]
                job["event"].update(
                    key=f"{trigger}-same-context",
                    trigger=trigger,
                    changed=False,
                    due_at="2026-09-29T09:30:00+08:00",
                )
                reseal(job)
                decision = self.plan(job)

                self.assertEqual(decision["status"], "ready")
                body = decision["message"]["body"]
                self.assertIn(job["event"]["assessment"], body)
                if trigger == "review_due":
                    self.assertEqual(decision["message"]["title"], "Feng shui review reminder")
                    self.assertIn("not evidence that your fortune changed", body)
                else:
                    self.assertEqual(decision["message"]["title"], "Feng shui calendar reflection")
                    self.assertIn("not a forecast of good or bad luck", body)

    def test_review_and_calendar_require_due_at_and_respect_due_boundary(self):
        for trigger in ("review_due", "calendar"):
            with self.subTest(trigger=trigger):
                missing = sample_job()
                missing["subscription"]["triggers"] = [trigger]
                missing["event"].update(trigger=trigger, changed=False)
                reseal(missing)
                self.assert_invalid(missing)

                malformed = sample_job()
                malformed["subscription"]["triggers"] = [trigger]
                malformed["event"].update(
                    trigger=trigger,
                    changed=False,
                    due_at="2026-09-29T10:00+08:00",
                )
                reseal(malformed)
                self.assert_invalid(malformed)

                future = sample_job()
                future["subscription"]["triggers"] = [trigger]
                future["event"].update(
                    trigger=trigger,
                    changed=False,
                    due_at="2026-09-29T10:00:01+08:00",
                )
                reseal(future)
                self.assert_suppressed(future, "not_due")

                due = copy.deepcopy(future)
                due["event"]["due_at"] = "2026-09-29T10:00:00+08:00"
                self.assertEqual(self.plan(due)["status"], "ready")

    def test_event_observed_is_lower_inclusive_and_expiry_is_upper_exclusive(self):
        observed_now = sample_job()
        set_event_window(
            observed_now,
            SAMPLE_NOW,
            SAMPLE_NOW + timedelta(hours=1),
        )
        self.assertEqual(self.plan(observed_now)["status"], "ready")

        stale = sample_job()
        set_event_window(
            stale,
            SAMPLE_NOW - timedelta(hours=1),
            SAMPLE_NOW,
        )
        self.assert_suppressed(stale, "stale_event")

        future = sample_job()
        set_event_window(
            future,
            SAMPLE_NOW + timedelta(seconds=1),
            SAMPLE_NOW + timedelta(hours=1),
        )
        self.assert_suppressed(future, "future_event")

    def test_quiet_hours_cover_same_day_overnight_and_local_timezone(self):
        same_day_cases = [
            ("2026-09-29T10:00:00+08:00", "quiet_hours"),
            ("2026-09-29T17:00:00+08:00", "eligible"),
        ]
        for value, expected in same_day_cases:
            with self.subTest(kind="same-day", value=value):
                job = sample_job()
                job["subscription"]["quiet_hours"] = {"start": "09:00", "end": "17:00"}
                reseal(job)
                decision = self.plan(job, timestamp(value))
                self.assertEqual(decision["reason"], expected)

        overnight_cases = [
            ("2026-09-29T23:00:00+08:00", "quiet_hours"),
            ("2026-09-30T07:59:59+08:00", "quiet_hours"),
            ("2026-09-30T08:00:00+08:00", "eligible"),
        ]
        for value, expected in overnight_cases:
            with self.subTest(kind="overnight", value=value):
                job = sample_job()
                reseal(job)
                decision = self.plan(job, timestamp(value))
                self.assertEqual(decision["reason"], expected)

        utc_now = datetime.fromisoformat("2026-09-29T14:30:00+00:00")
        job = sample_job()
        self.assert_suppressed(job, "quiet_hours", utc_now)

    def test_daily_limit_uses_subscription_local_date_across_dst(self):
        job = sample_job()
        job["subscription"].update(
            timezone="America/New_York",
            quiet_hours=None,
            max_per_day=1,
            min_interval_minutes=0,
        )
        reseal(job)
        set_event_window(
            job,
            datetime.fromisoformat("2026-10-31T12:00:00-04:00"),
            datetime.fromisoformat("2026-11-03T12:00:00-05:00"),
        )
        first_now = datetime.fromisoformat("2026-11-01T04:30:00+00:00")
        _, state, _ = self.ready_and_ack(job, first_now, sent_at=first_now)
        job["state"] = state
        job["event"]["assessment"] = "A distinct follow-up assessment."

        same_local_day = datetime.fromisoformat("2026-11-02T04:30:00+00:00")
        self.assert_suppressed(job, "daily_limit", same_local_day)

        next_local_day = datetime.fromisoformat("2026-11-02T05:00:00+00:00")
        self.assertEqual(self.plan(job, next_local_day)["status"], "ready")

    def test_cooldown_is_enforced_at_and_before_the_interval(self):
        job = sample_job()
        job["subscription"].update(quiet_hours=None, max_per_day=20, min_interval_minutes=60)
        reseal(job)
        _, state, _ = self.ready_and_ack(job, SAMPLE_NOW, sent_at=SAMPLE_NOW)
        job["state"] = state
        job["event"]["assessment"] = "A distinct assessment after the first receipt."

        self.assert_suppressed(job, "cooldown", SAMPLE_NOW + timedelta(minutes=59, seconds=59))
        self.assertEqual(
            self.plan(job, SAMPLE_NOW + timedelta(minutes=60))["status"],
            "ready",
        )

    def test_fingerprint_ignores_refresh_metadata_but_tracks_content_target_and_fields(self):
        original = sample_job()
        first = self.plan(original)["fingerprint"]

        refreshed = copy.deepcopy(original)
        refreshed["event"].update(
            observed_at="2026-09-29T09:30:00+08:00",
            expires_at="2026-09-30T10:30:00+08:00",
            evidence_refs=["demo:refreshed-retrieval"],
        )
        self.assertEqual(self.plan(refreshed)["fingerprint"], first)

        changed = copy.deepcopy(original)
        changed["event"]["assessment"] = "The content-based assessment has materially changed."
        self.assertNotEqual(self.plan(changed)["fingerprint"], first)

        target = copy.deepcopy(original)
        target["subscription"]["id"] = "another-subscription"
        target["state"]["subscription_id"] = "another-subscription"
        reseal(target)
        self.assertNotEqual(self.plan(target)["fingerprint"], first)

    def test_identical_event_with_refreshed_timestamps_is_already_delivered(self):
        job = sample_job()
        decision, state, _ = self.ready_and_ack(job)
        job["state"] = state
        job["event"].update(
            observed_at="2026-09-29T09:30:00+08:00",
            expires_at="2026-09-30T10:30:00+08:00",
            evidence_refs=["demo:another-retrieval"],
        )

        second = self.plan(job, SAMPLE_NOW + timedelta(minutes=1))

        self.assertEqual(second["status"], "suppressed")
        self.assertEqual(second["reason"], "already_delivered")
        self.assertEqual(decision["fingerprint"], state["deliveries"][0]["fingerprint"])

    def test_changed_content_can_notify_after_daily_quota_window(self):
        job = sample_job()
        job["subscription"].update(quiet_hours=None, max_per_day=1, min_interval_minutes=0)
        reseal(job)
        _, state, _ = self.ready_and_ack(job)
        job["state"] = state
        set_event_window(
            job,
            datetime.fromisoformat("2026-09-29T09:00:00+08:00"),
            datetime.fromisoformat("2026-10-01T09:00:00+08:00"),
        )
        job["event"].update(
            assessment="A materially changed assessment should be eligible.",
            next_step="Take a different reversible next step.",
        )

        decision = self.plan(job, datetime.fromisoformat("2026-09-30T10:00:00+08:00"))

        self.assertEqual(decision["status"], "ready")
        self.assertNotEqual(decision["fingerprint"], state["deliveries"][0]["fingerprint"])

    def test_timezone_unavailable_is_a_clean_validation_error(self):
        job = sample_job()
        job["subscription"]["timezone"] = "Mars/Olympus"
        reseal(job)
        with self.assertRaisesRegex(ValueError, "timezone"):
            self.plan(job)

    def test_consent_scope_hash_binds_every_non_status_subscription_field(self):
        subscription = sample_job()["subscription"]
        original = runtime().consent_scope_fingerprint(subscription)
        mutations = {
            "id": "another-subscription",
            "domains": ["career", "learning"],
            "triggers": ["calendar"],
            "channel": "email",
            "recipient": "another-recipient",
            "timezone": "UTC",
            "language": "zh-CN",
            "expires_at": "2027-01-01T00:00:00+08:00",
            "quiet_hours": None,
            "max_per_day": 2,
            "min_interval_minutes": 1,
            "max_evidence_age_hours": 169,
        }
        for field, value in mutations.items():
            with self.subTest(field=field):
                changed = copy.deepcopy(subscription)
                changed[field] = value
                self.assertNotEqual(
                    runtime().consent_scope_fingerprint(changed), original
                )

        status_only = copy.deepcopy(subscription)
        status_only["status"] = "paused"
        self.assertEqual(runtime().consent_scope_fingerprint(status_only), original)

        consent_only = copy.deepcopy(subscription)
        consent_only["consent"]["source_ref"] = "new-user-approval"
        self.assertEqual(runtime().consent_scope_fingerprint(consent_only), original)

    def test_scope_change_requires_explicit_reseal_and_ready_echoes_hash(self):
        job = sample_job()
        old_hash = job["subscription"]["consent"]["scope_hash"]
        job["subscription"]["recipient"] = "new-private-thread"

        suppressed = self.plan(job)

        self.assertEqual(suppressed["status"], "suppressed")
        self.assertEqual(suppressed["reason"], "consent_scope_changed")
        self.assertEqual(job["subscription"]["consent"]["scope_hash"], old_hash)

        reseal(job)
        decision = self.plan(job)
        self.assertEqual(decision["status"], "ready")
        self.assertEqual(
            decision["consent_scope"], job["subscription"]["consent"]["scope_hash"]
        )

    def test_set_like_scope_reordering_does_not_require_new_consent(self):
        job = sample_job()
        job["subscription"]["domains"] = ["career", "learning"]
        reseal(job)
        before = copy.deepcopy(job)
        job["subscription"]["domains"].reverse()
        job["subscription"]["triggers"].reverse()
        self.assertEqual(self.plan(job)["status"], "ready")
        self.assertEqual(job["subscription"]["consent"], before["subscription"]["consent"])

    def test_stale_evidence_is_independent_of_event_expiry(self):
        job = sample_job()
        job["event"].update(
            observed_at="2026-09-29T09:00:00+08:00",
            expires_at="2026-10-10T09:00:00+08:00",
        )
        exact_age = self.plan(job, datetime.fromisoformat("2026-10-06T09:00:00+08:00"))
        self.assertEqual(exact_age["status"], "ready")

        stale = self.plan(job, datetime.fromisoformat("2026-10-06T09:00:01+08:00"))
        self.assertEqual(stale["status"], "suppressed")
        self.assertEqual(stale["reason"], "stale_evidence")

    def test_evidence_age_is_a_strict_non_boolean_bounded_integer(self):
        for value in [True, False, 0, 8761, -1, 1.0, "168"]:
            with self.subTest(value=value):
                job = sample_job()
                job["subscription"]["max_evidence_age_hours"] = value
                reseal(job)
                self.assert_invalid(job)

        job = sample_job()
        job["subscription"]["max_evidence_age_hours"] = 1
        reseal(job)
        self.assertEqual(self.plan(job)["status"], "ready")

        job = sample_job()
        job["subscription"]["max_evidence_age_hours"] = 8760
        reseal(job)
        self.assertEqual(self.plan(job)["status"], "ready")

        missing = sample_job()
        missing["subscription"].pop("max_evidence_age_hours")
        self.assert_invalid(missing)

    def test_consent_scope_hash_is_required_lowercase_sha256(self):
        for value in [None, True, "", "a" * 63, "A" * 64, "g" * 64]:
            with self.subTest(value=value):
                job = sample_job()
                job["subscription"]["consent"]["scope_hash"] = value
                self.assert_invalid(job)

        missing = sample_job()
        missing["subscription"]["consent"].pop("scope_hash")
        self.assert_invalid(missing)

    def test_ledger_full_suppresses_before_a_new_send(self):
        job = sample_job()
        job["subscription"].update(
            quiet_hours=None,
            max_per_day=20,
            min_interval_minutes=0,
        )
        reseal(job)
        deliveries = []
        for index in range(10000):
            fingerprint = hashlib.sha256(f"ledger-entry-{index}".encode()).hexdigest()
            sent_at = SAMPLE_NOW - timedelta(days=1 + index // 20, minutes=index % 20)
            deliveries.append(
                {
                    "fingerprint": fingerprint,
                    "delivery_id": f"fsm-{fingerprint}",
                    "receipt_id": f"receipt-{index}",
                    "sent_at": sent_at.isoformat(),
                }
            )
        job["state"] = {
            "subscription_id": job["subscription"]["id"],
            "revision": 10000,
            "deliveries": deliveries,
        }

        decision = self.plan(job)

        self.assertEqual(decision["status"], "suppressed")
        self.assertEqual(decision["reason"], "ledger_full")

    def test_revision_exhaustion_suppresses_before_a_new_send(self):
        job = sample_job()
        job["state"]["revision"] = 10**12

        decision = self.plan(job)

        self.assertEqual(decision["status"], "suppressed")
        self.assertEqual(decision["reason"], "revision_exhausted")
        self.assertNotIn("fingerprint", decision)
        self.assertNotIn("delivery_id", decision)
        self.assertEqual(job["state"]["revision"], 10**12)


class ValidationTests(ProactiveCheckinTestCase):
    def test_rfc3339_offsets_reject_normalization_and_utc_overflow(self):
        for value in [
            "2026-09-29T10:00:00+00:99",
            "2026-09-29T10:00:00-01:60",
            "2026-09-29T10:00:00+24:00",
            "0001-01-01T00:00:00+01:00",
            "9999-12-31T23:59:59-01:00",
            "2026-09-29T10:00:00.0000009Z",
        ]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                runtime().parse_timestamp(value)

    def test_ready_window_at_last_supported_year_does_not_overflow(self):
        job = sample_job()
        job["subscription"].update(
            timezone="UTC", quiet_hours=None, expires_at="9999-12-31T23:59:59Z"
        )
        job["event"].update(
            observed_at="9999-12-31T23:58:00Z", expires_at="9999-12-31T23:59:59Z"
        )
        reseal(job)
        decision = self.plan(job, timestamp("9999-12-31T23:59:00Z"))
        self.assertEqual(decision["status"], "ready")
        self.assertEqual(timestamp(decision["valid_until"]), timestamp(job["event"]["expires_at"]))

    def test_bool_is_not_accepted_as_an_integer(self):
        for path in [
            ("subscription", "max_per_day", True),
            ("subscription", "min_interval_minutes", False),
            ("state", "revision", True),
        ]:
            with self.subTest(path=path[:2]):
                job = sample_job()
                job[path[0]][path[1]] = path[2]
                reseal(job)
                self.assert_invalid(job)

    def test_bool_is_not_accepted_for_boolean_fields(self):
        job = sample_job()
        job["event"]["changed"] = 1
        self.assert_invalid(job)

        job = sample_job()
        job["subscription"]["consent"]["granted"] = 1
        self.assert_invalid(job)

    def test_malformed_event_and_state_types_are_rejected(self):
        cases = []

        job = sample_job()
        job["event"]["evidence_refs"] = []
        cases.append(("empty evidence", job))

        job = sample_job()
        job["event"]["evidence_refs"] = ["ok", 2]
        cases.append(("non-string evidence", job))

        job = sample_job()
        job["event"]["observed_at"] = "2026-09-29T09:00:00"
        cases.append(("naive event timestamp", job))

        job = sample_job()
        job["subscription"]["quiet_hours"] = {"start": "08:00", "end": "08:00"}
        reseal(job)
        cases.append(("equal quiet bounds", job))

        job = sample_job()
        job["subscription"]["quiet_hours"] = {"start": "8:00", "end": "09:00"}
        reseal(job)
        cases.append(("malformed quiet bound", job))

        job = sample_job()
        job["event"]["expires_at"] = job["event"]["observed_at"]
        cases.append(("non-positive event window", job))

        for label, invalid in cases:
            with self.subTest(label=label):
                self.assert_invalid(invalid)

    def test_high_risk_and_high_stakes_domains_require_native_basis(self):
        high_risk = sample_job()
        high_risk["event"]["risk_level"] = "high"
        self.assert_invalid(high_risk)

        finance = sample_job()
        finance["subscription"]["domains"] = ["finance"]
        finance["event"]["domain"] = "finance"
        finance["event"]["risk_level"] = "low"
        reseal(finance)
        self.assert_invalid(finance)

        complete = copy.deepcopy(finance)
        complete["event"]["native_basis"] = "User-provided budget and verified expense records."
        reseal(complete)
        self.assertEqual(self.plan(complete)["status"], "ready")

    def test_wrong_state_ledger_is_rejected(self):
        job = sample_job()
        job["state"]["subscription_id"] = "different-subscription"
        self.assert_invalid(job)

        job = sample_job()
        job["state"]["revision"] = 1
        job["state"]["deliveries"] = [
            {
                "fingerprint": "a" * 64,
                "delivery_id": "wrong-delivery-id",
                "receipt_id": "receipt-1",
                "sent_at": "2026-09-29T10:00:00+08:00",
            }
        ]
        self.assert_invalid(job)

    def test_revision_cannot_be_lower_than_append_only_receipt_count(self):
        job = sample_job()
        _, state, _ = self.ready_and_ack(job)
        job["state"] = state
        job["state"]["revision"] = 0
        with self.assertRaisesRegex(ValueError, "revision"):
            self.plan(job)


class SideEffectTests(ProactiveCheckinTestCase):
    def test_plan_performs_no_network_or_filesystem_write(self):
        job = sample_job()
        with tempfile.TemporaryDirectory() as directory:
            before = sorted(Path(directory).iterdir())
            with mock.patch("socket.socket", side_effect=AssertionError("network access")):
                with mock.patch.object(socket, "create_connection", side_effect=AssertionError("network access")):
                    with mock.patch("urllib.request.urlopen", side_effect=AssertionError("network access")):
                        decision = self.plan(job)
            after = sorted(Path(directory).iterdir())

        self.assertEqual(decision["status"], "ready")
        self.assertEqual(before, after)
        self.assertEqual(job["state"]["deliveries"], [])


class AcknowledgeDeliveryTests(ProactiveCheckinTestCase):
    def test_acknowledgement_requires_ready_decision_and_nonempty_receipt(self):
        job = sample_job()
        decision = self.plan(job)
        self.assertEqual(decision["status"], "ready")

        suppressed = copy.deepcopy(job)
        suppressed["subscription"]["status"] = "paused"
        suppressed_decision = self.plan(suppressed)
        with self.assertRaisesRegex(ValueError, "ready"):
            runtime().acknowledge_delivery(
                suppressed,
                suppressed_decision,
                "provider-receipt",
                SAMPLE_NOW,
                SAMPLE_NOW,
            )

        for receipt in ["", "   ", None, 7]:
            with self.subTest(receipt=receipt):
                with self.assertRaises(ValueError):
                    runtime().acknowledge_delivery(
                        job,
                        decision,
                        receipt,
                        SAMPLE_NOW,
                        SAMPLE_NOW,
                    )

        for sent_at in [None, datetime.fromisoformat("2026-09-29T10:00:00")]:
            with self.subTest(sent_at=sent_at):
                with self.assertRaises(ValueError):
                    runtime().acknowledge_delivery(
                        job,
                        decision,
                        "provider-receipt",
                        sent_at,
                        SAMPLE_NOW,
                    )

    def test_ack_returns_new_state_only_after_confirmed_delivery(self):
        job = sample_job()
        before = copy.deepcopy(job)
        decision = self.plan(job)
        sent_at = SAMPLE_NOW + timedelta(minutes=1)

        state = runtime().acknowledge_delivery(
            job, decision, "provider-receipt-1", sent_at, sent_at
        )

        self.assertEqual(state["subscription_id"], job["subscription"]["id"])
        self.assertEqual(state["revision"], 1)
        self.assertEqual(len(state["deliveries"]), 1)
        delivery = state["deliveries"][0]
        self.assertEqual(delivery["fingerprint"], decision["fingerprint"])
        self.assertEqual(delivery["delivery_id"], decision["delivery_id"])
        self.assertEqual(delivery["receipt_id"], "provider-receipt-1")
        self.assertEqual(timestamp(delivery["sent_at"]), utc(sent_at))
        self.assertEqual(job, before)

    def test_ack_requires_sent_at_inside_window_and_not_in_the_future(self):
        job = sample_job()
        decision = self.plan(job)
        planned = timestamp(decision["planned_at"])
        valid_until = timestamp(decision["valid_until"])

        cases = [
            (valid_until, valid_until),
            (planned + timedelta(minutes=6), planned + timedelta(minutes=6)),
            (planned + timedelta(minutes=1), planned),
        ]
        for sent_at, now in cases:
            with self.subTest(sent_at=sent_at, now=now):
                with self.assertRaises(ValueError):
                    runtime().acknowledge_delivery(
                        job,
                        decision,
                        "provider-receipt",
                        sent_at,
                        now,
                    )

    def test_ack_rechecks_consent_and_policy_at_send_time(self):
        cases = []

        job = sample_job()
        decision = self.plan(job)
        job["subscription"]["consent"]["granted"] = False
        cases.append((job, decision))

        job = sample_job()
        decision = self.plan(job)
        job["subscription"]["status"] = "paused"
        cases.append((job, decision))

        job = sample_job()
        decision = self.plan(job)
        job["subscription"]["quiet_hours"] = {"start": "09:00", "end": "17:00"}
        reseal(job)
        cases.append((job, decision))

        for index, (changed_job, decision) in enumerate(cases):
            with self.subTest(case=index):
                with self.assertRaises(ValueError):
                    runtime().acknowledge_delivery(
                        changed_job,
                        decision,
                        f"receipt-{index}",
                        SAMPLE_NOW,
                        SAMPLE_NOW,
                    )

    def test_ack_rejects_stale_plan_after_event_or_state_changes(self):
        job = sample_job()
        decision = self.plan(job)
        job["event"]["assessment"] = "Changed after planning."
        with self.assertRaisesRegex(ValueError, "decision|state"):
            runtime().acknowledge_delivery(
                job,
                decision,
                "receipt-event-stale",
                SAMPLE_NOW,
                SAMPLE_NOW,
            )

        job = sample_job()
        decision = self.plan(job)
        job["state"]["revision"] = 1
        with self.assertRaisesRegex(ValueError, "decision|state"):
            runtime().acknowledge_delivery(
                job,
                decision,
                "receipt-state-stale",
                SAMPLE_NOW,
                SAMPLE_NOW,
            )

    def test_matching_duplicate_receipt_is_idempotent(self):
        job = sample_job()
        decision, state, sent_at = self.ready_and_ack(job)
        job["state"] = state

        retry = runtime().acknowledge_delivery(
            job, decision, "provider-receipt-1", sent_at, sent_at
        )

        self.assertEqual(retry, state)
        self.assertEqual(retry["revision"], 1)
        self.assertEqual(len(retry["deliveries"]), 1)

    def test_old_receipt_retry_after_later_delivery_is_unchanged_and_mutation_rejected(self):
        base = sample_job()
        base["subscription"].update(
            quiet_hours=None,
            max_per_day=20,
            min_interval_minutes=0,
        )
        reseal(base)

        first_job = copy.deepcopy(base)
        first_decision, first_state, first_sent_at = self.ready_and_ack(
            first_job,
            SAMPLE_NOW,
            receipt="provider-receipt-1",
            sent_at=SAMPLE_NOW,
        )

        later_job = copy.deepcopy(base)
        later_job["state"] = first_state
        later_job["event"].update(
            assessment="A later content update is a distinct delivery.",
            next_step="Review the later content before taking the next reversible step.",
        )
        later_now = SAMPLE_NOW + timedelta(minutes=1)
        later_decision = self.plan(later_job, later_now)
        self.assertEqual(later_decision["status"], "ready")
        later_state = runtime().acknowledge_delivery(
            later_job,
            later_decision,
            "provider-receipt-2",
            later_now,
            later_now,
        )
        self.assertEqual(later_state["revision"], 2)

        first_job["state"] = later_state
        retry = runtime().acknowledge_delivery(
            first_job,
            first_decision,
            "provider-receipt-1",
            first_sent_at,
            later_now,
        )

        self.assertEqual(retry, later_state)
        self.assertEqual(first_job["state"], later_state)

        mutated = copy.deepcopy(first_decision)
        mutated["message"]["body"] += " Mutated original decision."
        with self.assertRaises(ValueError):
            runtime().acknowledge_delivery(
                first_job,
                mutated,
                "provider-receipt-1",
                first_sent_at,
                later_now,
            )

    def test_conflicting_receipt_time_decision_and_ledger_are_rejected(self):
        job = sample_job()
        decision, state, sent_at = self.ready_and_ack(job)
        job["state"] = state

        with self.assertRaisesRegex(ValueError, "receipt|acknowledged"):
            runtime().acknowledge_delivery(job, decision, "different-receipt", sent_at, sent_at)
        with self.assertRaisesRegex(ValueError, "receipt|acknowledged"):
            runtime().acknowledge_delivery(
                job,
                decision,
                "provider-receipt-1",
                sent_at + timedelta(seconds=1),
                sent_at + timedelta(seconds=1),
            )

        conflicting_decision = copy.deepcopy(decision)
        conflicting_decision["message"]["body"] += " Mutated payload."
        with self.assertRaises(ValueError):
            runtime().acknowledge_delivery(
                job, conflicting_decision, "provider-receipt-1", sent_at, sent_at
            )

        wrong_ledger = copy.deepcopy(job)
        wrong_ledger["state"]["subscription_id"] = "not-the-subscription"
        with self.assertRaises(ValueError):
            runtime().acknowledge_delivery(
                wrong_ledger, decision, "provider-receipt-1", sent_at, sent_at
            )

    def test_fake_sender_ack_then_second_poll_is_quiet(self):
        job = sample_job()
        decision = self.plan(job)
        state = runtime().acknowledge_delivery(
            job,
            decision,
            "provider-receipt-1",
            SAMPLE_NOW,
            SAMPLE_NOW,
        )
        job["state"] = state

        second = self.plan(job, SAMPLE_NOW + timedelta(minutes=1))

        self.assertEqual(second["status"], "suppressed")
        self.assertEqual(second["reason"], "already_delivered")
        self.assertEqual(job["state"], state)


class CliTests(ProactiveCheckinTestCase):
    def test_plan_cli_emits_only_json(self):
        sample = ROOT / "examples" / "proactive-checkin-job.json"
        result = run_cli(
            "plan",
            str(sample),
            "--now",
            "2026-09-29T10:00:00+08:00",
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        parsed = json.loads(result.stdout)
        self.assertEqual(parsed["status"], "ready")
        self.assertEqual(result.stdout.lstrip()[:1], "{")

    def test_ack_cli_emits_updated_state_json_without_persistence(self):
        job = sample_job()
        decision = self.plan(job)
        with tempfile.TemporaryDirectory() as directory:
            directory_path = Path(directory)
            job_path = directory_path / "job.json"
            decision_path = directory_path / "decision.json"
            job_path.write_text(json.dumps(job), encoding="utf-8")
            decision_path.write_text(json.dumps(decision), encoding="utf-8")
            before = sorted(path.name for path in directory_path.iterdir())

            result = run_cli(
                "ack",
                str(job_path),
                str(decision_path),
                "--receipt",
                "provider-receipt-1",
                "--sent-at",
                "2026-09-29T10:01:00+08:00",
                "--now",
                "2026-09-29T10:01:00+08:00",
            )

            after = sorted(path.name for path in directory_path.iterdir())

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        state = json.loads(result.stdout)
        self.assertEqual(state["revision"], 1)
        self.assertEqual(state["deliveries"][0]["receipt_id"], "provider-receipt-1")
        self.assertEqual(before, after)

    def test_cli_errors_are_clean_and_do_not_write_stdout(self):
        sample = ROOT / "examples" / "proactive-checkin-job.json"
        result = run_cli("plan", str(sample), "--now", "not-an-iso-timestamp")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("error", result.stderr.casefold())
        self.assertNotIn("traceback", result.stderr.casefold())

        with tempfile.TemporaryDirectory() as directory:
            malformed = Path(directory) / "malformed.json"
            malformed.write_text("{not json", encoding="utf-8")
            result = run_cli("plan", str(malformed), "--now", "2026-09-29T10:00:00+08:00")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("error", result.stderr.casefold())
        self.assertNotIn("traceback", result.stderr.casefold())


if __name__ == "__main__":
    unittest.main()
