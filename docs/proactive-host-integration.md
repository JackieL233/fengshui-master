# Portable Proactive Host Integration

This is a host-neutral recipe for opt-in FengShui Master check-ins. It does
not claim that any scheduler, notification provider, webhook, or product API
is configured or tested.

## Runtime Boundary

The runtime module is a planner and receipt-state helper:

- plan_checkin(job, now=None) returns a decision.
- acknowledge_delivery(job, decision, receipt, sent_at, now=None) returns only
  the next state dictionary.
- The functions calculate and validate without mutating the input job, using
  network, or writing files. now=None uses the live UTC clock, so pass an
  aware datetime for deterministic tests.
- The CLI reads its JSON paths and prints JSON to stdout. It does not save the
  returned state:

~~~bash
python fengshui-master/scripts/proactive_checkin.py plan JOB.json [--now ISO]
python fengshui-master/scripts/proactive_checkin.py ack JOB.json DECISION.json --receipt ID --sent-at ISO [--now ISO]
~~~

--now fixes evaluation time only. It does not schedule, authorize, send, or
persist a notification. The host owns data retrieval, agent assessment,
consent, scheduling, locking, transport, reconciliation, and atomic storage.

## Required Job Contract

version: 1 is required. The required top-level objects are subscription,
event, and state.

subscription requires:

~~~text
id
status: active | paused | revoked
consent: {granted, recorded_at, source_ref, scope_hash}
domains: nonempty list
triggers: context_changed | review_due | calendar
channel, recipient, timezone (IANA), language (en | zh-CN)
expires_at, quiet_hours (null or {start, end}), max_per_day
min_interval_minutes, max_evidence_age_hours
~~~

max_per_day is 1..20, min_interval_minutes is 0..10080, and
max_evidence_age_hours is 1..8760. quiet_hours.start and .end are unequal
HH:MM values and may cross midnight. channel is a delivery field, not a
trigger.

consent.recorded_at, subscription.expires_at, and every event, receipt,
decision, and CLI timestamp are full RFC3339 date-times with a T, seconds,
and a timezone offset or Z, for example
2026-09-29T09:00:00+08:00. Fractional seconds support at most six digits;
greater precision is rejected, not rounded. due_at is required for review_due and calendar; it
is an aware full date-time, not a date-only value, and must be before event
expiry.

consent.scope_hash is a lowercase 64-character SHA-256 digest. The helper
below hashes every current SUBSCRIPTION_FIELDS member except status and consent:

The domains and triggers lists are sorted before hashing, so merely reordering
the same memberships does not invalidate approval.

~~~python
from proactive_checkin import consent_scope_fingerprint

approved_hash = consent_scope_fingerprint(subscription)
~~~

This is configuration binding, not cryptographic proof of user consent. The
host must obtain actual permission. If a user changes channel, recipient,
domains, triggers, cadence, quiet hours, timezone, expiry, language, or the
evidence-age limit, do not auto-reseal the old consent. Obtain fresh approval
and then store the newly computed hash. Status-only pause/revoke changes are
still delivery gates even though status is excluded from the hash.

event requires key, trigger, domain, observed_at, expires_at, changed,
risk_level, basis, evidence_refs, assessment, next_step, check_signal, and
action_type. Optional fields are favorable, friction, symbolic_note,
native_basis, and due_at.

- risk_level is low, medium, or high; basis is observed, inferred, calculated,
  or reminder.
- evidence_refs is a nonempty list of strings used for provenance; it is not
  permission to copy evidence into the delivery ledger.
- action_type is reversible_preparation, reflection, or professional_support.
  It is not an execution command.
- native_basis is required for high risk and for finance, wellbeing,
  legal_adjacent, health, medical, and safety domains.
- The agent must not assert deterministic health/fate outcomes or hidden
  events. The runtime cannot semantically validate arbitrary model prose.

state contains only the fields below. Its revision must be at least the number
of append-only delivery rows; runtime validation enforces this cross-field rule:

~~~json
{
  "subscription_id": "...",
  "revision": 0,
  "deliveries": [
    {
      "fingerprint": "64 lowercase SHA-256 hex characters",
      "delivery_id": "fsm-<fingerprint>",
      "receipt_id": "provider receipt",
      "sent_at": "2026-09-29T09:30:00+08:00"
    }
  ]
}
~~~

revision is nonnegative and capped at 10**12. The delivery list is
append-only; do not rewrite or reorder existing rows.

Do not put DOB, birth time, birth location, sex, raw context, evidence
contents, message prose, provider secrets, or real user data in this delivery
ledger. Any exact job/outbox snapshot is a separate protected,
retention-approved record, not the ledger.

## Plan and Gate

Every decision includes version, subscription_id, status, reason, and
evaluated_at. A ready decision has reason eligible plus fingerprint,
delivery_id, planned_at, valid_until (no more than five minutes),
event_expires_at, subscription_expires_at, consent_scope, state_revision,
recipient, channel, and
message: {title, body, language}. delivery_id is exactly
fsm-<fingerprint>; use it unchanged as the provider idempotency key.

Suppression reasons are:

~~~text
consent_required, consent_scope_changed, subscription_paused,
subscription_revoked, subscription_expired, consent_not_effective,
out_of_scope, trigger_not_enabled, no_material_change, not_due,
stale_event, future_event, stale_evidence, quiet_hours, already_delivered,
daily_limit, cooldown, ledger_full, revision_exhausted
~~~

The gate checks the scope hash, active status, effective consent, subscription
and event expiry, domain/trigger, evidence age, changed/due status, timezone
quiet hours, daily limit, cooldown, content fingerprint, and ledger capacity.
Timing is lower-inclusive and expiry-exclusive. stale_evidence is independent
of event expiry: suppress when now - observed_at exceeds
max_evidence_age_hours. At 10,000 delivery rows, suppress as ledger_full
before transport; acknowledgment also refuses a full ledger. At revision
10**12, suppress as revision_exhausted before transport.

### Content-based dedupe

This is deterministic content hashing, not semantic-NLP similarity. The
fingerprint includes the subscription id, recipient/channel target, and
semantic event fields such as stable key, trigger, domain, and assessment. It
does not hash the entire subscription scope. The implementation excludes
observed_at, expires_at, evidence_refs, due_at, and changed. Scope changes are
bound separately by consent_scope.

Use one stable event.key for one occurrence while polling. Do not generate a
random key on every poll. Create a new stable occurrence key only when the
event itself materially changes. Treat the returned fingerprint as opaque and
do not reimplement the hash.

context_changed with changed false suppresses as no_material_change. An
explicitly opted-in review_due or calendar event may notify unchanged context;
a calendar message is a reflection cue, not a fortune-change claim.

## Host Lifecycle

The scheduler can be cron, a heartbeat, or a queue/job runner. All must use a
per-subscription singleflight lock across
read -> plan -> send -> ack -> atomic save.

~~~text
run_one(subscription_id):
  acquire lock("proactive:" + subscription_id)
  try:
    stored = store.read_consistent(subscription_id)

    # Reconcile an existing attempt before any fetch, assessment, or new send.
    pending = store.find_pending_outbox(subscription_id)
    if pending is not None:
      receipt = provider.reconcile(pending.delivery_id)
      if receipt is None: return
      recovered_state = acknowledge_delivery(
        pending.job_snapshot, pending.decision_snapshot,
        receipt.id, receipt.sent_at, now=clock.now()
      )
      store.atomic_confirm_outbox_and_append_delivery(
        pending, recovered_state, receipt,
        expected_revision=pending.job_snapshot.state.revision
      )
      return

    # Do not fetch user data for an inactive or unapproved subscription.
    preflight_now = clock.now()
    if stored.subscription.status != "active": return
    if not stored.subscription.consent.granted: return
    if not consent_effective(stored, preflight_now): return
    if not scope_hash_matches(stored): return
    if stored.subscription.expires_at <= preflight_now: return

    fresh = permitted_data_source.fetch(stored.subscription)
    reviewed_event = agent.assess(stored.subscription, fresh, clock.now())

    candidate = copy(stored)
    candidate.event = reviewed_event
    first = plan_checkin(candidate, now=clock.now())
    if first.status != "ready": record_suppression(first.reason); return

    # Re-read the complete latest subscription and state. Keep the same event.
    latest = store.read_consistent(subscription_id)
    latest.event = copy(reviewed_event)
    final_now = clock.now()
    decision = plan_checkin(latest, now=final_now)
    if decision.status != "ready": return

    outbox = {
      subscription_id, delivery_id: decision.delivery_id,
      job_snapshot: deep_copy(latest),
      decision_snapshot: deep_copy(decision), status: "pending"
    }
    store.atomic_insert_protected_outbox(outbox)  # BEFORE provider call

    provider_result = provider.send_private(
      decision.channel, decision.recipient, decision.message,
      idempotency_key=decision.delivery_id
    )
    receipt = provider.confirm_or_reconcile(provider_result)
    if receipt is None: return  # leave pending; reconcile before any later send
    next_state = acknowledge_delivery(
      outbox.job_snapshot, outbox.decision_snapshot,
      receipt.id, receipt.sent_at, now=clock.now()
    )
    store.atomic_confirm_outbox_and_append_delivery(
      outbox, next_state, receipt,
      expected_revision=outbox.job_snapshot.state.revision
    )
  finally:
    release lock
~~~

The final re-plan uses the complete latest subscription and state, not just the
consent object, and uses a fresh clock immediately before the outbox is
written. It catches pause/revoke, consent_scope_changed,
recipient/topic/cadence changes, state revisions, quiet hours, quotas, and
stale evidence. The reviewed_event remains the agent-reviewed event;
re-reading the job must not replace it with stale stored event data.

Once the provider call has begun, a later revocation cannot recall that
request. Record the provider's actual result and prevent future sends; never
claim that a notification was withdrawn after dispatch began.

## Durable Outbox and Recovery

Persist the exact final job_snapshot, exact decision_snapshot,
subscription_id, delivery_id, and pending status atomically before the
provider call. Protect the outbox with access control/encryption and a
retention policy; minimize surrounding metadata and delete it only after
reconciliation permits. Do not expose this snapshot to the provider by
default.

If the process crashes or the provider times out, the pending outbox blocks
any later send for that subscription. Reconcile the same delivery_id by
provider lookup or callback before any later send. Never retry with a new
random idempotency key. If the provider cannot deduplicate or reconcile,
leave the attempt ambiguous and stop sending for that subscription.

When reconciliation confirms delivery, call acknowledge_delivery with the
original outbox job and decision snapshots, including the original event and
subscription, and the original receipt/time. Do this even if the current
subscription has since been revoked. The idempotent retry path must validate
that original snapshot and reconstruct only the append-only pre-delivery
ledger; it must not acknowledge against a newly reconstructed current job or
rewrite prior rows. Merge the returned delivery row into current state under a
revision-checked transaction, preserving the current revoked/paused status and
consent; never re-enable the subscription. A matching receipt is idempotent; a
conflicting receipt or snapshot is an error.

The normal confirmation and recovery paths use one revision-checked
transaction to mark the outbox confirmed and append exactly one ledger row.
Do not blind-replace state and then mark the outbox in a separate write. If a
transaction already contains the same confirmed receipt, return the existing
state idempotently; otherwise reject a revision or receipt conflict.

## Provider and Fallback Recipes

A notification tool or webhook connector needs private routing,
authentication, a stable receipt, provider idempotency keyed by delivery_id,
and a documented accepted/delivered/failed/ambiguous status. Pass only channel,
recipient, the rendered message, and delivery_id; do not pass the full job or
raw evidence. An accepted-for-processing response is not delivery
confirmation. No provider API is assumed here.

Without a scheduler or private transport, use an interactive chat-only
fallback: fetch permitted context when the user asks, run the same grounded
assessment, and show the message in that active conversation. Do not promise a
future reminder or record an external delivery without a provider receipt.
Only offer periodic or changes-only opt-in when the host can actually schedule,
revoke, send, reconcile, and save it.

## Runnable In-Memory Fake Sender

Run this from the repository root after the runtime and sample exist. It loads
the authoritative sample instead of duplicating it, models the outbox in
memory, and asserts that the outbox is present before the fake send:

~~~python
from copy import deepcopy
from datetime import datetime
import json
from pathlib import Path
import sys
from threading import Lock

sys.path.insert(0, "fengshui-master/scripts")
from proactive_checkin import acknowledge_delivery, plan_checkin

NOW = datetime.fromisoformat("2026-09-29T09:30:00+08:00")
job = json.loads(Path("examples/proactive-checkin-job.json").read_text(encoding="utf-8"))
reviewed_event = deepcopy(job["event"])
outbox = []

class FakeSender:
    def __init__(self):
        self.calls = []

    def send_private(self, decision):
        assert outbox[-1]["delivery_id"] == decision["delivery_id"]
        self.calls.append(decision["delivery_id"])
        return {"receipt_id": "fake-receipt-001", "sent_at": NOW}

sender = FakeSender()
with Lock():
    candidate = deepcopy(job)
    candidate["event"] = deepcopy(reviewed_event)
    assert plan_checkin(candidate, now=NOW)["status"] == "ready"

    latest = deepcopy(job)  # real host re-reads complete subscription + state
    latest["event"] = deepcopy(reviewed_event)  # preserve reviewed event
    decision = plan_checkin(latest, now=NOW)  # real host uses fresh clock.now()
    assert decision["status"] == "ready"
    assert {"event_expires_at", "subscription_expires_at"} <= decision.keys()
    outbox.append({
        "subscription_id": latest["subscription"]["id"],
        "delivery_id": decision["delivery_id"],
        "job_snapshot": deepcopy(latest),
        "decision_snapshot": deepcopy(decision),
        "status": "pending",
    })
    result = sender.send_private(decision)
    job["state"] = acknowledge_delivery(
        outbox[0]["job_snapshot"], outbox[0]["decision_snapshot"],
        result["receipt_id"], result["sent_at"], now=NOW,
    )
    outbox[0]["receipt_id"] = result["receipt_id"]
    outbox[0]["status"] = "confirmed"

assert len(sender.calls) == 1
assert plan_checkin(job, now=NOW)["reason"] == "already_delivered"
assert outbox[0]["status"] == "confirmed"
print({"delivery_id": sender.calls[0], "revision": job["state"]["revision"]})
~~~

This is an in-memory local wiring check only. It makes no network request and
does not prove live push, scheduler delivery, webhook behavior, or crash
recovery.

## Agent Wakeup Prompt

Use one of these self-contained prompts after the host supplies only permitted
fresh context and the selected opt-in mode.

### English

~~~text
You are the grounded FengShui Master check-in agent. This is an opt-in
assessment, not a hidden-fact detector, fortune guarantee, or professional
service. Read only permitted fresh context. State the user's bounded current
posture and one low-risk actionable change to make or verify next. Label
material points observed, calculated, inferred, unknown, or recommended. Keep
symbolic language conditional and tied to evidence. Never invent hidden events,
deterministic health/fate outcomes, or execution commands. For finance,
wellbeing, legal-adjacent, health, medical, or safety topics, state the native
real-world basis and suggest professional support when warranted.

Return an event with a stable key for this occurrence, trigger, domain, aware
observed_at/expires_at, changed, risk_level, basis, nonempty evidence_refs,
assessment, next_step, check_signal, and action_type; include native_basis
when required. The user must separately opt into periodic review_due/calendar
check-ins, changes-only context_changed check-ins, or neither. Do not schedule
or send without consent. Reuse the same key while the occurrence is unchanged;
do not make a random key per poll. A calendar check is reflection, not a claim
that fortune changed. Respect language, timezone, quiet hours, and expiry.
~~~

### 中文

~~~text
你是有证据约束的 FengShui Master 主动检查代理。这是用户明确选择后的评估，
不是探测隐秘事实、保证运势或替代专业服务。只读取允许的最新上下文，说明用户
当前有边界的态势，并给出一个低风险、可执行或可核验的下一步。对重要内容标记
为 observed、calculated、inferred、unknown 或 recommended。象征性语言必须有条件
并绑定证据。不得编造隐秘事件，不得作确定性的健康或命运结论，不得输出执行命令。
涉及金融、身心健康、法律相关、health、medical 或 safety 时，说明现实依据，必要时
建议寻求专业人士帮助。

输出包含本次发生的稳定 key、trigger、domain、带时区的 observed_at/expires_at、
changed、risk_level、basis、非空 evidence_refs、assessment、next_step、check_signal
和 action_type；必要时加入 native_basis。用户必须单独选择周期性复盘
（review_due/calendar）、仅在上下文发生变化时检查（context_changed）或不启用。
没有 consent 不得安排或发送。同一事件未变化时复用 key，不要每次轮询随机生成 key。
日历检查是反思提示，不是运势改变的断言。遵守语言、时区、免打扰时间和有效期。
~~~

## Acceptance Checks

- Verify every suppression reason, including consent_scope_changed,
  stale_evidence, and ledger_full.
- Test pause/revoke and all scope changes with the full latest re-plan; do not
  compare only the consent object or discard the reviewed event.
- Test outbox persistence before provider invocation, provider idempotency,
  ambiguous reconciliation before later sends, and post-dispatch no-recall.
- Confirm the delivery ledger contains no DOB or other private source data.
- The fake sender remains local and in-memory; no live external push is
  claimed.
