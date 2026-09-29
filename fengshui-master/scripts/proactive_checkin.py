#!/usr/bin/env python3
"""Plan opt-in follow-ups and acknowledge receipts; never schedule or send them."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from datetime import datetime, time, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


TRIGGERS = {"context_changed", "review_due", "calendar"}
HIGH_RISK_DOMAINS = {"finance", "wellbeing", "legal_adjacent", "health", "medical", "safety"}
ACTION_TYPES = {"reversible_preparation", "reflection", "professional_support"}
EVENT_FIELDS = {
    "key", "trigger", "domain", "observed_at", "expires_at", "changed",
    "risk_level", "basis", "evidence_refs", "assessment", "next_step",
    "check_signal", "action_type",
}
EVENT_OPTIONAL = {"favorable", "friction", "symbolic_note", "native_basis", "due_at"}
SUBSCRIPTION_FIELDS = {
    "id", "status", "consent", "domains", "triggers", "channel", "recipient",
    "timezone", "language", "expires_at", "quiet_hours", "max_per_day",
    "min_interval_minutes",
    "max_evidence_age_hours",
}


def object_fields(value: Any, required: set[str], optional: set[str], label: str) -> dict:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    if required - value.keys():
        raise ValueError(f"{label} missing fields: {', '.join(sorted(required - value.keys()))}")
    if value.keys() - required - optional:
        raise ValueError(f"{label} has unsupported fields")
    return value


def text_field(value: Any, label: str, maximum: int = 1000) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > maximum:
        raise ValueError(f"{label} must be a nonblank string of at most {maximum} characters")
    return value


def integer_field(value: Any, label: str, minimum: int, maximum: int) -> int:
    if type(value) is not int or not minimum <= value <= maximum:
        raise ValueError(f"{label} must be an integer between {minimum} and {maximum}")
    return value


def choice(value: Any, allowed: set[str], label: str) -> None:
    if not isinstance(value, str) or value not in allowed:
        raise ValueError(f"{label} must be one of {', '.join(sorted(allowed))}")


def string_list(value: Any, label: str, maximum: int = 30) -> None:
    if not isinstance(value, list) or not 1 <= len(value) <= maximum:
        raise ValueError(f"{label} must be a nonempty list of at most {maximum} strings")
    for item in value:
        text_field(item, label, 300)
    if len(set(value)) != len(value):
        raise ValueError(f"{label} contains duplicates")


def parse_timestamp(value: Any, label: str = "timestamp") -> datetime:
    if not isinstance(value, str) or not re.fullmatch(
        r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}"
        r"(?:\.[0-9]{1,6})?(?:Z|[+-](?:[01][0-9]|2[0-3]):[0-5][0-9])", value
    ):
        raise ValueError(f"{label} must be an ISO timestamp with timezone offset")
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return result.astimezone(timezone.utc)
    except (ValueError, OverflowError) as exc:
        raise ValueError(f"{label} must be an ISO timestamp with timezone offset") from exc


def clock_value(value: datetime | None) -> datetime:
    result = value if value is not None else datetime.now(timezone.utc)
    if not isinstance(result, datetime) or result.tzinfo is None or result.utcoffset() is None:
        raise ValueError("now must be a timezone-aware datetime")
    return result.astimezone(timezone.utc)


def wall_time(value: Any) -> time:
    if not isinstance(value, str) or not re.fullmatch(r"(?:[01][0-9]|2[0-3]):[0-5][0-9]", value):
        raise ValueError("quiet_hours must use HH:MM")
    return time.fromisoformat(value)


def validate_job(job: Any) -> ZoneInfo:
    object_fields(job, {"version", "subscription", "event", "state"}, set(), "job")
    if type(job["version"]) is not int or job["version"] != 1:
        raise ValueError("job.version must be 1")
    sub = object_fields(job["subscription"], SUBSCRIPTION_FIELDS, set(), "subscription")
    for field in ["id", "channel", "recipient", "timezone"]:
        text_field(sub[field], f"subscription.{field}", 300)
    choice(sub["status"], {"active", "paused", "revoked"}, "subscription.status")
    choice(sub["language"], {"en", "zh-CN"}, "subscription.language")
    consent = object_fields(sub["consent"], {"granted", "recorded_at", "source_ref", "scope_hash"}, set(), "consent")
    if type(consent["granted"]) is not bool:
        raise ValueError("consent.granted must be boolean")
    text_field(consent["source_ref"], "consent.source_ref", 300)
    if not isinstance(consent["scope_hash"], str) or not re.fullmatch(r"[0-9a-f]{64}", consent["scope_hash"]):
        raise ValueError("consent.scope_hash must be a SHA256 hex digest of the approved scope")
    consent_at = parse_timestamp(consent["recorded_at"], "consent.recorded_at")
    expiry = parse_timestamp(sub["expires_at"], "subscription.expires_at")
    if expiry <= consent_at:
        raise ValueError("subscription expiry must be after consent.recorded_at")
    string_list(sub["domains"], "subscription.domains")
    string_list(sub["triggers"], "subscription.triggers", 3)
    for trigger in sub["triggers"]:
        choice(trigger, TRIGGERS, "subscription.triggers")
    integer_field(sub["max_per_day"], "max_per_day", 1, 20)
    integer_field(sub["min_interval_minutes"], "min_interval_minutes", 0, 10080)
    integer_field(sub["max_evidence_age_hours"], "max_evidence_age_hours", 1, 8760)
    if sub["quiet_hours"] is not None:
        quiet = object_fields(sub["quiet_hours"], {"start", "end"}, set(), "quiet_hours")
        if wall_time(quiet["start"]) == wall_time(quiet["end"]):
            raise ValueError("quiet_hours start and end must differ; use null to disable")
    try:
        zone = ZoneInfo(sub["timezone"])
    except (ZoneInfoNotFoundError, ValueError) as exc:
        raise ValueError("subscription timezone is unknown or IANA data unavailable; install tzdata") from exc

    event = object_fields(job["event"], EVENT_FIELDS, EVENT_OPTIONAL, "event")
    for field in ["key", "domain"]:
        text_field(event[field], f"event.{field}", 300)
    for field in ["assessment", "next_step", "check_signal", "favorable", "friction", "symbolic_note", "native_basis"]:
        if field in event:
            text_field(event[field], f"event.{field}")
    choice(event["trigger"], TRIGGERS, "event.trigger")
    choice(event["risk_level"], {"low", "medium", "high"}, "event.risk_level")
    choice(event["basis"], {"observed", "inferred", "calculated", "reminder"}, "event.basis")
    choice(event["action_type"], ACTION_TYPES, "event.action_type")
    if type(event["changed"]) is not bool:
        raise ValueError("event.changed must be boolean")
    string_list(event["evidence_refs"], "event.evidence_refs")
    observed = parse_timestamp(event["observed_at"], "event.observed_at")
    event_expiry = parse_timestamp(event["expires_at"], "event.expires_at")
    if event_expiry <= observed:
        raise ValueError("event expiry must be after observed_at")
    if event["trigger"] in {"review_due", "calendar"} and "due_at" not in event:
        raise ValueError("event.due_at is required for review_due and calendar")
    if "due_at" in event and parse_timestamp(event["due_at"], "event.due_at") >= event_expiry:
        raise ValueError("event.due_at must be before event expiry")
    if (event["risk_level"] == "high" or event["domain"] in HIGH_RISK_DOMAINS) and "native_basis" not in event:
        raise ValueError("high-stakes event requires native_basis; symbolism is not decision evidence")

    state = object_fields(job["state"], {"subscription_id", "revision", "deliveries"}, set(), "state")
    if state["subscription_id"] != sub["id"]:
        raise ValueError("state.subscription_id does not match subscription")
    integer_field(state["revision"], "state.revision", 0, 10**12)
    deliveries = state["deliveries"]
    if not isinstance(deliveries, list) or len(deliveries) > 10000:
        raise ValueError("state.deliveries must be a list of at most 10000 receipts")
    if state["revision"] < len(deliveries):
        raise ValueError("state.revision must cover every append-only delivery receipt")
    fingerprints: set[str] = set()
    receipts: set[str] = set()
    for row in deliveries:
        object_fields(row, {"fingerprint", "delivery_id", "receipt_id", "sent_at"}, set(), "delivery")
        fingerprint = text_field(row["fingerprint"], "delivery.fingerprint", 64)
        if not re.fullmatch(r"[0-9a-f]{64}", fingerprint):
            raise ValueError("delivery.fingerprint must be a SHA256 hex digest")
        if row["delivery_id"] != f"fsm-{fingerprint}":
            raise ValueError("delivery_id does not match fingerprint")
        text_field(row["receipt_id"], "delivery.receipt_id", 300)
        parse_timestamp(row["sent_at"], "delivery.sent_at")
        if fingerprint in fingerprints or row["receipt_id"] in receipts:
            raise ValueError("state contains duplicate delivery fingerprints or receipts")
        fingerprints.add(fingerprint)
        receipts.add(row["receipt_id"])
    return zone


def event_fingerprint(job: dict) -> str:
    event = job["event"]
    # Refresh timestamps and retrieval references alone must not create a new alert.
    fields = {key: value for key, value in event.items()
              if key not in {"observed_at", "expires_at", "evidence_refs", "due_at", "changed"}}
    sub = job["subscription"]
    payload = {"subscription": sub["id"], "recipient": sub["recipient"],
               "channel": sub["channel"], "event": fields}
    return hashlib.sha256(json.dumps(payload, ensure_ascii=True, sort_keys=True,
                                     separators=(",", ":")).encode("utf-8")).hexdigest()


def consent_scope_fingerprint(subscription: dict) -> str:
    """Bind the approved configuration; this checksum is not proof of consent."""
    scope = {key: subscription[key] for key in sorted(SUBSCRIPTION_FIELDS - {"status", "consent"})}
    for key in ("domains", "triggers"):
        scope[key] = sorted(scope[key])
    return hashlib.sha256(json.dumps(scope, ensure_ascii=True, sort_keys=True,
                                     separators=(",", ":")).encode("utf-8")).hexdigest()


def render_message(job: dict) -> dict[str, str]:
    event, sub = job["event"], job["subscription"]
    chinese = sub["language"] == "zh-CN"
    titles = {
        "context_changed": "风水复盘：有新依据" if chinese else "Feng shui review: new evidence",
        "review_due": "风水复盘提醒" if chinese else "Feng shui review reminder",
        "calendar": "风水时令复盘" if chinese else "Feng shui calendar reflection",
    }
    labels = {
        "assessment": "暂定判断" if chinese else "Provisional assessment",
        "favorable": "有利条件" if chinese else "Favorable conditions",
        "friction": "待核验阻力" if chinese else "Friction to check",
        "next_step": "下一步" if chinese else "Next step",
        "check_signal": "核验信号" if chinese else "Check signal",
        "symbolic_note": "象义说明" if chinese else "Symbolic lens",
        "native_basis": "现实依据" if chinese else "Native-domain basis",
    }
    lines = []
    if event["trigger"] == "review_due":
        lines.append("这是你预约的复盘，不表示运势已改变。" if chinese else
                     "This is your requested review, not evidence that your fortune changed.")
    elif event["trigger"] == "calendar":
        lines.append("时令变化仅作复盘线索，不预示吉凶。" if chinese else
                     "Calendar timing is a reflection cue, not a forecast of good or bad luck.")
    if "native_basis" in event:
        lines.append(f"{labels['native_basis']}: {event['native_basis']}")
    for field in ["assessment", "favorable", "friction", "next_step", "check_signal", "symbolic_note"]:
        if field in event:
            lines.append(f"{labels[field]}: {event[field]}")
    basis_labels = {"observed": "观察", "inferred": "条件推断", "calculated": "计算", "reminder": "提醒"}
    basis = basis_labels[event["basis"]] if chinese else event["basis"]
    lines.append(("依据类型: " if chinese else "Basis type: ") + basis)
    lines.append(("资料时间: " if chinese else "Evidence as of: ") + event["observed_at"])
    lines.append(("来源: " if chinese else "Sources: ") + ", ".join(event["evidence_refs"]))
    if event["domain"] == "finance":
        lines.append("仅作复盘辅助，不是投资建议或买卖指令。" if chinese else
                     "For review only, not financial advice or a trading instruction.")
    elif event["domain"] in {"wellbeing", "health", "medical"}:
        lines.append("不作诊断或治疗建议，健康疑虑请咨询合格专业人员。" if chinese else
                     "Not a diagnosis or treatment recommendation; consult qualified care for health concerns.")
    elif event["domain"] == "legal_adjacent":
        lines.append("不替代法律意见，实际期限和程序优先。" if chinese else
                     "Not legal advice; actual deadlines and procedures take priority.")
    lines.append("可随时要求暂停或取消。" if chinese else "You can ask to pause or unsubscribe at any time.")
    return {"title": titles[event["trigger"]], "body": "\n".join(lines), "language": sub["language"]}


def plan_checkin(job: dict, now: datetime | None = None) -> dict:
    zone = validate_job(job)
    current = clock_value(now)
    sub, event, state = job["subscription"], job["event"], job["state"]
    result = {"version": 1, "subscription_id": sub["id"], "status": "suppressed",
              "reason": "", "evaluated_at": current.isoformat()}

    def suppress(reason: str) -> dict:
        return {**result, "reason": reason}

    if sub["status"] != "active":
        return suppress(f"subscription_{sub['status']}")
    if not sub["consent"]["granted"]:
        return suppress("consent_required")
    if sub["consent"]["scope_hash"] != consent_scope_fingerprint(sub):
        return suppress("consent_scope_changed")
    if parse_timestamp(sub["consent"]["recorded_at"]) > current:
        return suppress("consent_not_effective")
    if parse_timestamp(sub["expires_at"]) <= current:
        return suppress("subscription_expired")
    if event["domain"] not in sub["domains"]:
        return suppress("out_of_scope")
    if event["trigger"] not in sub["triggers"]:
        return suppress("trigger_not_enabled")
    if parse_timestamp(event["observed_at"]) > current:
        return suppress("future_event")
    if parse_timestamp(event["expires_at"]) <= current:
        return suppress("stale_event")
    if current - parse_timestamp(event["observed_at"]) > timedelta(hours=sub["max_evidence_age_hours"]):
        return suppress("stale_evidence")
    if event["trigger"] == "context_changed" and not event["changed"]:
        return suppress("no_material_change")
    if "due_at" in event and parse_timestamp(event["due_at"]) > current:
        return suppress("not_due")
    local = current.astimezone(zone)
    quiet = sub["quiet_hours"]
    if quiet is not None:
        start, end = wall_time(quiet["start"]), wall_time(quiet["end"])
        wall = local.time().replace(tzinfo=None)
        is_quiet = start <= wall < end if start < end else wall >= start or wall < end
        if is_quiet:
            return suppress("quiet_hours")
    fingerprint = event_fingerprint(job)
    sent_times = [parse_timestamp(row["sent_at"]) for row in state["deliveries"]]
    if any(sent > current for sent in sent_times):
        raise ValueError("state contains a future delivery receipt")
    if any(row["fingerprint"] == fingerprint for row in state["deliveries"]):
        return suppress("already_delivered")
    if sum(sent.astimezone(zone).date() == local.date() for sent in sent_times) >= sub["max_per_day"]:
        return suppress("daily_limit")
    if sent_times and current - max(sent_times) < timedelta(minutes=sub["min_interval_minutes"]):
        return suppress("cooldown")
    if len(state["deliveries"]) >= 10000:
        return suppress("ledger_full")
    if state["revision"] >= 10**12:
        return suppress("revision_exhausted")
    expiry = min(parse_timestamp(event["expires_at"]), parse_timestamp(sub["expires_at"]))
    valid_until = current + min(timedelta(minutes=5), expiry - current)
    return {**result, "status": "ready", "reason": "eligible",
            "fingerprint": fingerprint, "delivery_id": f"fsm-{fingerprint}",
            "planned_at": current.isoformat(), "valid_until": valid_until.isoformat(),
            "event_expires_at": parse_timestamp(event["expires_at"]).isoformat(),
            "subscription_expires_at": parse_timestamp(sub["expires_at"]).isoformat(),
            "consent_scope": sub["consent"]["scope_hash"],
            "state_revision": state["revision"], "recipient": sub["recipient"],
            "channel": sub["channel"], "message": render_message(job)}


def acknowledge_delivery(job: dict, decision: dict, receipt: str, sent_at: datetime,
                         now: datetime | None = None) -> dict:
    validate_job(job)
    current = clock_value(now)
    if sent_at is None:
        raise ValueError("sent_at is required for a confirmed delivery")
    sent = clock_value(sent_at)
    text_field(receipt, "receipt", 300)
    if not isinstance(decision, dict) or decision.get("status") != "ready":
        raise ValueError("only a ready decision can be acknowledged")
    if sent > current:
        raise ValueError("sent_at cannot be in the future")
    fingerprint = event_fingerprint(job)
    if decision.get("fingerprint") != fingerprint or decision.get("delivery_id") != f"fsm-{fingerprint}":
        raise ValueError("decision does not match current subscription target and event")
    state = job["state"]
    for index, row in enumerate(state["deliveries"]):
        if row["fingerprint"] == fingerprint:
            if row["receipt_id"] == receipt and parse_timestamp(row["sent_at"]) == sent:
                # Reconstruct the append-only pre-delivery ledger before accepting a retry.
                original = copy.deepcopy(job)
                original["state"]["deliveries"] = original["state"]["deliveries"][:index]
                original["state"]["revision"] -= len(state["deliveries"]) - index
                acknowledge_delivery(original, decision, receipt, sent, current)
                return copy.deepcopy(state)
            raise ValueError("delivery already acknowledged with a different receipt or time")
        if row["receipt_id"] == receipt:
            raise ValueError("receipt already belongs to another delivery")
    planned = parse_timestamp(decision.get("planned_at"), "decision.planned_at")
    expiry = parse_timestamp(decision.get("valid_until"), "decision.valid_until")
    if not planned <= sent < expiry:
        raise ValueError("sent_at must be inside the decision validity window")
    if decision != plan_checkin(job, planned):
        raise ValueError("decision or state changed; re-plan before dispatch")
    if plan_checkin(job, sent)["status"] != "ready":
        raise ValueError("delivery was no longer eligible at sent_at")
    if len(state["deliveries"]) >= 10000:
        raise ValueError("receipt ledger is full; do not dispatch until the host migrates it safely")
    updated = copy.deepcopy(state)
    updated["revision"] += 1
    updated["deliveries"].append({"fingerprint": fingerprint, "delivery_id": decision["delivery_id"],
                                  "receipt_id": receipt, "sent_at": sent.isoformat()})
    return updated


def read_json(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    plan = commands.add_parser("plan", help="Output a decision; do not send or change state.")
    plan.add_argument("job")
    plan.add_argument("--now", help="Aware ISO timestamp for reproducible tests; normally use the live clock.")
    ack = commands.add_parser("ack", help="Output next state only after confirmed provider delivery.")
    ack.add_argument("job")
    ack.add_argument("decision")
    ack.add_argument("--receipt", required=True)
    ack.add_argument("--sent-at", required=True)
    ack.add_argument("--now")
    args = parser.parse_args()
    try:
        job = read_json(args.job)
        now = parse_timestamp(args.now, "now") if args.now else None
        if args.command == "plan":
            result = plan_checkin(job, now)
        else:
            result = acknowledge_delivery(job, read_json(args.decision), args.receipt,
                                          parse_timestamp(args.sent_at, "sent_at"), now)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError, TypeError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
