# Consent-Based Proactive Follow-up Protocol / 经同意的主动跟进与推送协议

Use this protocol when FengShui Master may continue a topic in the current turn, offer a scheduled review, or send a material-evidence notification. Pair it with [proactive-reading-protocol.md](proactive-reading-protocol.md) for the reading itself. This document governs consent, freshness, planning, delivery, privacy, and stop behavior; it does not turn the skill into a passive daemon.

## Non-Negotiable Boundary

- A model can answer in the current session, but a subscription, reminder, or push is an external action. It requires explicit opt-in for the requested scope.
- Before accepting or executing a subscription, the host must tool-confirm that a real scheduler and a real delivery channel are available, addressable, and able to return a send or cancellation receipt. If that confirmation is unavailable, provide a plan or ask for the missing capability; never claim that the skill will run or notify autonomously.
- A clearly worded request for a subscription authorizes only the named topic, trigger/cadence, destination, and time bounds. It does not authorize adjacent domains, extra recipients, broader evidence access, or a different channel.
- Installing, editing, or reading this skill is not user consent for a subscription. Do not create an actual automation, subscription, schedule, or delivery without the user's separate opt-in and a host-confirmed capability.

## Runtime Boundary and Host Contract

For an installed skill, resolve `scripts/proactive_checkin.py` relative to the skill root. In this repository checkout the path is `fengshui-master/scripts/proactive_checkin.py`. Its commands are pure JSON planner/ack operations and do not perform scheduler, network, or file writes:

```text
python <skill-root>/scripts/proactive_checkin.py plan JOB.json [--now ISO]
python <skill-root>/scripts/proactive_checkin.py ack JOB.json DECISION.json --receipt ID --sent-at ISO [--now ISO]
```

In a repository checkout, `<skill-root>` is `fengshui-master`; the equivalent commands use `python fengshui-master/scripts/proactive_checkin.py ...`. An installed host should still resolve the script from its installed skill root rather than requiring repository-root files.

`JOB.json` contains the subscription, event, and state. Root-level `examples/proactive-checkin-job.json` and `docs/` are optional full-repository aids, not runtime dependencies for an installed skill folder. When present, the example is a fictional demonstration job; obtain its exact rendered decision by running the CLI. Use optional full-repository host-integration documentation for the public API and complete field contract rather than duplicating the job fields here.

The subscription contract requires `max_evidence_age_hours` as an integer from 1 through 8760. This freshness limit is independent of event expiry: an event can still be inside its own expiry window and be suppressed as `stale_evidence` when the observed evidence is too old.

Consent also requires a lowercase 64-character SHA-256 `scope_hash`. The runtime helper `consent_scope_fingerprint(subscription)` hashes all current `SUBSCRIPTION_FIELDS` except `status` and `consent`, including the delivery target, topics/domains, triggers/cadence, timezone, expiry, quiet hours, quotas, and the evidence-age limit. This is a configuration binding, not cryptographic proof of user consent; the host still obtains actual permission through its consent flow.

All JSON and CLI timestamps, especially `due_at`, must be full aware RFC3339 date-times with a `T`, seconds, and a timezone offset (or `Z`), and `due_at` must precede event expiry. Fractional seconds support at most six digits. A date-only value or local wall-clock value is invalid. Domain and trigger list order is normalized before scope hashing; only membership changes affect those fields.

The planner status is only `ready` or `suppressed`, with a `reason` and the contract fields for that result. It does not return `send`, `quiet`, `consent-question`, or `blocked` statuses; an agent may ask or explain outside the planner. The host still owns the durable lock, atomic store, scheduler, provider authentication, protected outbox, and idempotent channel operation. A ready plan is not a send.

## Three Modes

Choose exactly one mode for each proactive action. Keep the mode visible in the job/decision path and, where useful, in the user-facing wording.

### 1. In-session initiative / 会话内主动判断

Use when the user is present and has asked for a reading, decision aid, or follow-up. No extra consent is needed to answer the current request. After the urgent reality check, give the bounded current posture, favorable factors, possible friction, one reversible action, and a check signal from the known facts. Do not imply that anything was saved, scheduled, monitored, or sent outside the current response.

Offer at most one scoped subscription in a turn, and only when a concrete review point or evidence change would genuinely help the user's stated goal. Do not offer one on every turn, after a recent decline, or merely because the topic sounds ongoing. The answer comes first; a subscription offer is optional and separate from consent to receive the answer.

### 2. Opt-in scheduled review / 主动选择的定期复盘

Use only after the user explicitly opts in to a review cadence or a specific future review. A scheduled review asks the host to run the same bounded evidence-and-action check at the agreed time. It is a reminder or review opportunity, not permission to invent a new change. If no new evidence is available, say that the evidence is unchanged or insufficient and do not send unless the user explicitly scheduled the review.

The review may include an opted-in calendar, moon-phase, or seasonal context, but label it as calculated symbolic timing or a reflective prompt. A date, moon, or seasonal change is never proof that luck changed, that an omen occurred, or that a bad outcome is approaching.

### 3. Material evidence-change notification / 重大证据变化通知

Use only after explicit opt-in to a named topic and trigger. Send only when new, dated, allowed evidence materially changes the provisional posture, favorable/friction assessment, one action, or check signal, and the planner gate passes. No new evidence, stale evidence, a mere calendar/moon/season change, or a cosmetic wording change is a notification ground; the planner must remain `suppressed` with an applicable reason. Do not send a generic "just checking in" ping.

## When and How to Offer a Subscription

Offer one only when all of these are true:

1. The current request has a bounded topic and a useful observable check signal.
2. A future review or material change could alter the next action or reduce avoidable uncertainty.
3. The user has not just declined, paused, or revoked a related subscription.
4. The host can confirm a scheduler and private delivery destination before setup.

Use a narrow, non-leading offer after the useful in-session answer, for example:

> Your current check signal is desk interruptions over the next week. A weekly private review of that workspace topic could be useful. Would you like to opt in? I would need only the cadence/timezone and private destination; no unrelated topics would be included.

Do not phrase an offer as if a schedule already exists. Do not use fear, urgency, "bad luck" language, or a generic calendar ping to manufacture consent.

## Consent Intake: Reuse First, Ask at Most Three

Treat the current conversation and confirmed host settings as working context. Reuse facts, topic, language, timezone, destination, quiet hours, expiry, and prior stop/refusal decisions already supplied. Never ask again for a field the user supplied or explicitly refused. An explicit refusal remains a refusal; it is not a cue to infer a value.

Before activation, resolve the missing fields below. Group them into no more than three concise questions; zero questions is valid when every required field is already known and the user has clearly opted in.

| Required field | Capture | Safe rule |
| --- | --- | --- |
| Topic and scope | One native domain or artifact, the exact facts/evidence allowed, and excluded adjacent topics | Do not broaden from "my desk" to home, health, relationships, or money without explicit scope. |
| Cadence or trigger | A schedule for `review_due`, or a material-change predicate for `context_changed` | A trigger must describe an observable evidence change, not "when luck shifts." `calendar` is a separate opt-in reflective trigger. |
| Timezone | IANA timezone or a host-confirmed timezone with an as-of timestamp | Never infer a residence or silently use a different timezone. |
| Private destination | A user-approved private channel/address and its provider identity | Do not send to a public feed, shared lock screen, or unconfirmed recipient. |
| Quiet hours | Start/end and timezone, plus any no-send days if relevant | Quiet hours suppress sends; they do not justify a queued burst later. |
| Expiry and stop preference | End date, review count, or explicit stop/pause/unsubscribe rule | If absent, ask; do not create an indefinite subscription by default. |

Suggested maximum-three intake:

1. **Scope:** "What exact topic/evidence should I review, and is this a scheduled review or a notification only when that evidence materially changes?"
2. **Timing:** "What cadence or change trigger should apply, and which timezone should govern it?"
3. **Delivery and end:** "Which private destination is approved, what quiet hours should I honor, and when should it expire or stop?"

If the user clearly requests "subscribe me to X every Friday in my private channel until June," that authorizes only that stated scope. Ask only for missing destination, timezone, or quiet/stop details, and do not ask for unrelated birth data, financial records, health details, or a broader reading.

When a user approves a changed scope, the host may compute and store a new `scope_hash` with that approval. Do not auto-reseal an old consent record after changing the channel, recipient, topics/domains, triggers or cadence, quiet hours, timezone, expiry, quotas, evidence-age limit, or any other hashed field. The planner must suppress the changed configuration as `consent_scope_changed` until the host obtains fresh approval. Status-only pause/revoke transitions do not change the hash, but they still block delivery.

## Evidence-to-Message Lifecycle

Every scheduled-review or material-change attempt follows this sequence. Planning is not sending.

### 1. Gather allowed sources

Use only sources allowed by the consent scope and host capabilities:

- facts, corrections, artifacts, and signals supplied in the current conversation;
- user-authorized private records or integrations, only for the named topic;
- host-confirmed clock, timezone, calendar, or deterministic FengShui Master helper outputs, with method and inputs;
- user-named or otherwise permitted source material with a retrievable source reference.

Do not use inferred private events, cold-reading guesses, an unconfirmed integration, a generic horoscope, or a calendar/moon/season transition as evidence of a life event or changed fortune. A symbolic mapping remains an interpretive lens.

### 2. Attach dated evidence

For each material item, retain in the plan an opaque reference, status, observed/calculated time, source, timezone, freshness, and scope. Use the existing statuses `observed`, `calculated`, `inferred`, `unknown`, and `recommended`; never promote an inference to an observation.

When a user corrects a fact, the latest value supersedes it. Retract dependent posture, actions, and triggers, then recompute only affected outputs. Keep unrelated conclusions. When the user refuses a field, mark it unavailable and do not re-request it. Conflicting, stale, or missing evidence is uncertainty, not a reason to fill the gap with prediction.

### 3. Build the provisional check

The plan must contain a compact, bounded packet:

- **Current posture:** one conditional statement tied to the topic and as-of time.
- **Favorable:** one or more supported factors, if any.
- **Friction:** a conditional, ordinary manifestation, never a hidden event.
- **One action:** one low-risk, reversible action useful even if the symbolic interpretation is wrong.
- **Check signal:** an observable measure or observation that can confirm or weaken the posture.

Include evidence references, confidence, assumptions, and falsifiers. For high-stakes domains, the packet may orient the user to evidence and qualified professionals but must not give execution advice such as a buy/sell order, treatment decision, legal filing, or safety-critical intervention.

### 4. Apply the planner gate

Host preflight comes first. The host/agent must verify explicit scope and opt-in, actual scheduler and delivery capability, private destination, permitted-source access, materiality and truthfulness of the grounded event, privacy of rendered text, and high-stakes safety. The runtime cannot enforce those semantic or host capabilities; if any is unavailable, do not call it as permission to send.

After host preflight, the runtime applies deterministic checks and returns only a `ready` or `suppressed` decision with a reason. Agent consent questions and explanatory copy are outside the planner:

- subscription status is active, consent is granted/effective, and `scope_hash` matches;
- the event domain and trigger are enabled;
- event timestamps are not future, event/subscription expiry has not passed, and evidence freshness is checked against `subscription.max_evidence_age_hours` separately from `event.expires_at`;
- `context_changed` has a material `changed` flag, while `review_due`/`calendar` satisfy their due-time requirements;
- quiet hours, duplicate fingerprint, daily quota, cooldown, full ledger, and revision exhaustion are enforced;
- the ready decision carries the bounded message and delivery/idempotency fields only after those checks pass.

When a ready decision is returned, it carries `consent_scope` equal to the approved `subscription.consent.scope_hash`, plus `event_expires_at` and `subscription_expires_at`. The host must verify those bounds and the consent binding again immediately before transport; a plan is invalid if the current subscription, approval, or expiry context changed.

For `review_due`, create a fresh reminder event at the scheduled time. It may report unchanged context, but must label the underlying evidence as older and include its as-of time; a reminder event does not bypass the `max_evidence_age_hours` check or turn stale evidence into fresh evidence. For `context_changed`, no material evidence change is suppressed. `calendar` is separate and may pass only as an opted-in reflective prompt; calendar, moon, or seasonal context cannot by itself establish a material change.

### 5. Host send and receipt acknowledgment

The runtime commands above output JSON only. They do not call a scheduler, mutate a subscription, send a channel message, or write a receipt file. The host owns the durable lock, atomic schedule/state store, protected outbox, provider authentication, and idempotent channel operation.

The host sequence is:

1. Acquire the durable per-subscription lock before reading the job or planning.
2. Read a consistent current job, verify active consent/scope/status and expiry, and inspect or reconcile any pending outbox before gathering sources. An unresolved pending send blocks new source gathering and later sends for that subscription.
3. Gather only permitted fresh context, create the reviewed event, and call `plan`.
4. If the planner returns `status: suppressed`, stop and expose its `reason` to the host/agent; do not send.
5. While still holding the lock, read the current subscription and state again, attach the same reviewed event to that current job, and re-plan immediately before transport. If scope, state, consent, quiet hours, expiry, freshness, or any other gate changed, discard the earlier decision and do not send.
6. For the second `ready` decision, atomically persist a protected outbox record containing the exact current job snapshot, exact decision, and `delivery_id` before calling the provider. The outbox is an in-flight control record, not a sent receipt or permission to widen scope.
7. Call the confirmed private provider with that exact `delivery_id`. If the result is uncertain, mark the protected outbox unresolved and do not call `ack` or dispatch another send.
8. After the provider confirms the original send, call `ack` once for that confirmed delivery using the protected original job/decision snapshot and the provider's receipt ID and `sent_at`. A crash-recovery retry may submit that identical acknowledgment again; the runtime must validate the same snapshot and append-only prefix and return the existing state. Do not acknowledge an altered snapshot or a new receipt.
9. Atomically merge the returned append-only state with a revision-checked current job and close the outbox under the same lock. Preserve the latest consent and subscription status, including a newer pause or revoke; never overwrite them with stale snapshot fields. The delivery ledger records only the minimal confirmed receipt.

An uncertain provider result blocks later sends for that subscription until the same `delivery_id` is reconciled. If the original request was accepted before a revoke and later reconciles to a confirmed receipt, record that receipt with the protected original snapshot; this does not re-enable, re-seal, or resume the revoked scope. Revocation cannot recall an in-flight provider request, so never imply that it can. A failed or confirmed-not-sent attempt may close without `ack` after reconciliation. For the job/decision field contract, use the optional full-repository host documentation rather than creating a second schema in this reference.

The delivery ledger is capped at 10,000 receipt rows. The planner must suppress as `ledger_full` before transport, and `ack` must reject a full ledger. If the revision is `10**12`, the planner must suppress as `revision_exhausted` before transport. The host must migrate or compact safely before another send; it must not wrap the revision or dispatch from a stale or over-capacity snapshot. `ack` validates the original event/subscription snapshot and exact ready decision again. A repeated acknowledgment for the same confirmed receipt revalidates the original snapshot against the append-only pre-delivery ledger before returning the existing state; a different receipt or altered snapshot is an error. Never rewrite or delete earlier ledger rows.

## Pause, Stop, Unsubscribe, and Expiry

- A user saying **pause**, **stop**, **unsubscribe**, **不要再发**, or equivalent revokes send permission for the matching scope immediately. The planner must return `status: suppressed` with the applicable subscription reason from the next evaluation, even if host cancellation is still pending.
- The host must cancel the durable schedule and return a cancellation receipt. Report `cancel_requested` and `cancelled_confirmed` separately; do not say a schedule is stopped until the host confirms cancellation, but do not send while confirmation is pending.
- Expiry, quiet hours, provider failure, missing consent, or an uncertain send also suppresses a send; an uncertain send blocks later sends until reconciled. Do not queue a catch-up burst after quiet hours or expiry.
- Resume requires an explicit user request. A changed topic, trigger, destination, or duration requires fresh consent; never silently revive a revoked scope.

## Privacy, Freshness, and High-Stakes Boundaries

- Keep state privacy-minimal. The runtime records only a provider-confirmed sent receipt with opaque identifiers and minimal delivery metadata. The host may retain only the schedule, cancellation, lock, and deduplication fields needed to operate it; do not persist full private evidence or message bodies unless the host's consented product contract requires it.
- Make title and lock-screen text non-sensitive. Suppress routine financial amounts, medical details, diagnoses/symptoms, named people, relationship allegations, account identifiers, and other private person-specific details. Put the bounded basis in the approved private destination after opening.
- Freshness is part of evidence: a fresh `review_due` reminder may label older evidence and say "no material update," but the runtime still applies `max_evidence_age_hours`; `stale_evidence` suppresses the plan rather than bypassing the freshness gate. State the as-of time and timezone.
- A user correction, refusal, uncertainty, or source withdrawal changes the next plan before any send. Do not use a stale draft or a cached inference to keep a notification alive.
- Feng shui, moon phases, solar terms, and seasons may support an opt-in reflective prompt. They are not proof of changed luck, a bad omen, causation, or a forecast of health, money, relationship, legal, or safety outcomes.
- Never send high-stakes execution advice. Point to the relevant evidence, reversible preparation, and qualified professional help when needed.

## Notification Shape and Bilingual Examples

When a message is justified, make the judgment visible without overstating it: name the topic and as-of date, state the bounded posture, give one action, and name the check signal. Keep the lock-screen version generic and open the private destination for detail. Use the user's language.

### English: scheduled review with no invented change

All examples in this section are fictional; dates, facts, destinations, and outcomes are illustrative only.

**Lock-screen:**

> Workspace review due: no material change is confirmed. Open for the dated basis, one low-risk action, and the next check signal.

**Private message:**

> **Scheduled review, as of 29 Sep 2026 (Asia/Shanghai).** Older evidence, last observed 26 Sep, supports a modest workspace-flow test, but there is no new evidence that luck or the posture changed. Favorable: the entry area is clearer. Friction: interruption frequency is still unknown. One action: observe three workdays and count avoidable interruptions. Check signal: interruption count. This is a practical and symbolic review, not a prediction.

### 中文：没有新增证据时的定期复盘

**锁屏文字：**

> 工作空间复盘：目前未确认有重大变化。打开查看有日期依据、一个低风险行动和下一项观察信号。

**私密消息：**

> **定期复盘，依据截至 2026 年 9 月 29 日（Asia/Shanghai）。** 较早证据（最近观察于 2026 年 9 月 26 日）支持做一个小范围的空间流动测试，但没有新证据表明运势或当前态势发生变化。有利点：入口区域更清楚。可能阻力：干扰频率仍未知。一个行动：观察三个工作日并记录可避免的干扰次数。检查信号：干扰次数。这是务实与象义结合的复盘，不是预测。

### English: material evidence change

**Lock-screen:**

> Private workspace update: new dated evidence changes the current posture. Open for the one action and confirmation signal.

**Private message:**

> **Material evidence change, as of 29 Sep 2026.** New user-provided evidence shows the entry obstruction was cleared. Current posture: favorable for a small flow test, with moderate confidence. Friction: whether focus improves is not yet confirmed. One action: observe for three workdays. Check signal: avoidable interruptions per day. The evidence changes the practical assessment; it does not prove a change in luck.

### 中文：重大证据变化通知

**锁屏文字：**

> 私密空间更新：新的、有日期的证据改变了当前态势。打开查看一个行动和确认信号。

**私密消息：**

> **重大证据变化，依据截至 2026 年 9 月 29 日。** 用户新提供的证据显示入口阻挡已经清除。当前态势：适合做小范围的流动测试，置信度中等。可能阻力：专注是否改善尚未确认。一个行动：观察三个工作日。检查信号：每天可避免的干扰次数。变化来自现实证据对判断的影响，不等于证明运势发生变化。

### English and Chinese: opted-in reflective timing prompt

> **Reflective timing prompt / 反思性择时提示:** The solar term changed, so you may review light, air, and routine if that is within your subscription. This is calculated seasonal context, not evidence of changed luck or a bad omen. / 节气发生变化；如果这在你的订阅范围内，可以复查采光、通风与日常节律。这是计算出的季节性背景，不是运势改变或坏兆头的证据。

## Compact Implementer Checklist

Before enabling any push path, verify:

- one of the three modes is selected;
- the answer or offer is scoped and useful, with no spammy repeated subscription offer;
- scheduled/evidence-change consent and all six intake fields are resolved or the missing fields are asked in at most three concise questions;
- allowed, dated evidence produces the current posture, favorable, friction, one action, and check signal;
- no `context_changed` trigger fires from silence, a stale source, or calendar/moon/season context alone;
- the planner returns JSON with only `ready`/`suppressed` status and does not send or mutate state;
- a ready decision includes `consent_scope`, `event_expires_at`, and `subscription_expires_at`; revision `10**12` returns `revision_exhausted` suppression;
- the host confirms scheduler, private destination, durable lock, atomic store, idempotent channel, and receipt path;
- only a confirmed receipt is recorded; uncertain sends block later sends until the original `delivery_id` is reconciled;
- normal acknowledgment is once per confirmed send, with only an identical crash-recovery retry allowed; snapshot validation and append-only ledger preservation remain required;
- pause/stop/unsubscribe/expiry blocks sends immediately and host cancellation is confirmed;
- lock-screen text is privacy-minimal and the message contains no deterministic prediction or high-stakes execution advice.
