---
name: bailian-rl-deploy
description: End-to-end reinforcement-learning training and deployment on Alibaba Cloud Bailian / DashScope with the `bl` CLI — authorize → sandbox runtime → data & Rollout/Reward code → submit RL job → monitor → publish checkpoint → deploy & invoke. Covers bl finetune rl authorize / run / watch / logs / get / list / cancel / delete, bl finetune runtime prepare / doctor / clean, and post-training checkpoints / export / deploy. Activate whenever the user wants "reinforcement learning", "RL training", "GRPO/GSPO", "AgenticRL", "reward function", "rollout function", "math-reasoning training", "agent tool-calling training", "MTU training units", "rl run", or "submit an RL job" on Bailian / DashScope — even without saying "use bl"; do not hand-assemble commands or make the user write submit_job.py. Underspecified requests must go through the Step 0 intake (ask the user for model / data / Rollout-Reward code / billing / deploy intent) before any action — never answer a training request with doc summaries or code samples. Not for SFT / DPO / CPT / LoRA supervised fine-tuning or OPD distillation (pg_opd / teacher_model) — those go to bailian-finetune; training on other platforms, plain Q&A / coding / model selection do not trigger this skill.
---

# Bailian RL training → deployment loop (`bl finetune rl`)

Submit, monitor, and deploy your first RL training job with the Bailian CLI `bl`. RL drives the model to explore optimal policies through a generate (Rollout) → score (Reward) → optimize loop — no ground-truth labels required. Well suited to math reasoning, agent tool calling, and code generation.

```
0. Intake (mandatory)   inputs missing? ask the user first — model / data / functions / billing / deploy
1. Auth & environment   bl auth status → bl finetune rl authorize → runtime prepare → runtime doctor
2. Data & code          JSONL (messages + rollout_extra) + Rollout/Reward function package (official demo available)
3. Submit               bl finetune rl run --dry-run preview → user confirms → --yes submit (optionally --watch)
4. Monitor              bl finetune rl watch / logs / get + console Metrics tab (critic/rewards/mean)
5. Publish & deploy     last checkpoint auto-published → bl deploy text create → invoke via bl text chat
```

> **Read the shared protocol before executing** [`../bailian-protocol/SKILL.md`](../bailian-protocol/SKILL.md): version pre-flight, call attribution, auth, error reporting. If the protocol file is missing, stop running `bl` and prompt `bl skill init`. Command details are authoritative in `bl <command> --help` and skill `bailian-finetune`'s `reference/finetune.md` — **do not guess flags**.

**Call attribution** (wrap every agent-initiated `bl` command; inline samples below are for one-off runs — when copying into reusable scripts, use the protocol's script template):

```bash
BAILIAN_CALLER_TYPE=agent BAILIAN_CALLER_NAME=qoder BAILIAN_SKILL_NAME=bailian-rl-deploy BAILIAN_SKILL_VERSION=1.0.0 bl finetune rl authorize
```

## Step 0: Intake — clarify missing inputs before acting (mandatory)

A submission needs five decisions. When the trigger message does not supply them, **stop and ask the user** — one compact round of questions with recommended defaults. Do not read official docs, do not generate code samples, and do not run any `bl` write command before the intake is settled:

| # | Input | Ask | Default to offer |
|---|---|---|---|
| 1 | Base model | Which model to train? | `qwen3.5-9b` (field-verified) |
| 2 | Training data | Own JSONL path(s), or the official demo data? | demo `calc_train_min.jsonl` + `calc_validation_min.jsonl` |
| 3 | Rollout/Reward code | Own function package path, or the official demo? | demo `agentic-rl-example` (math-calculation agent) |
| 4 | Billing | MTU spec × count; postpaid or prepaid? | `MTU4 × 24`, `mtu_postpaid` ≈ CNY 984/hour — disclose the cost |
| 5 | After training | Deploy automatically and hand off a call example? | yes |

- **One-shot escape hatch**: offer "use the official demo with the verified defaults" — accepting it settles all five inputs at once; the user then only confirms the disclosed cost at the Step 3 gate.
- Only after all five are settled (answered or explicitly defaulted) proceed to the version/platform gates and Step 1. The Step 3 dry-run → confirm → `--yes` billing gate still applies on top — intake does not replace it.
- **The deliverable is a submitted `bl` job, not documentation or code.** Never respond to a training request with a hand-written SDK script (`submit_job.py` etc.), a doc summary, or generic code examples. If the user explicitly wants learning material / SDK sample code instead of running a job, that is out of scope — point to the official docs and stop.
- Inputs already given in the trigger message are not re-asked; only the missing ones are.

## Version & platform gates (start of the action flow)

1. **CLI version**: proceed only if `bl finetune rl run --help` prints normally. The RL command group is recent — older CLIs lack it; upgrade with `bl update` first. During development you can use the repo entry `pnpm -s bl` (note its cwd is pinned to `packages/cli`; see the path rules below).
2. **Platform**: the RL sandbox supports **macOS / Linux** only; Windows fails closed with "Not supported on Windows yet." — do not try to bypass it. OPD has no such restriction (but OPD is out of scope for this skill).
3. **Auth**: `bl auth status`; if unauthenticated, `bl auth login --api-key sk-...` first. The `bl` path does **not** require a local Python / dashscope SDK install — the CLI ships a reviewed managed runtime (pinned CPython + dashscope baseline) that is downloaded, verified, and cached automatically. The `pip install dashscope` instructions in official docs apply only to the hand-written SDK-script path.
4. **Access whitelist**: RL training must be enabled by your **account manager**. If the authorize probe reports `REQUIRES_USER_ACTION` / missing whitelist, hand the enablement guidance back to the user; do not retry in a loop.

## Write-operation guardrails (read before submitting)

- **RL supports MTU (Model Training Unit) billing only — no per-token billing.** These are dedicated training resources; **billing starts at creation**:
  | Billing | `--charge-type` | Unit price (type-IV MTU4) | Notes |
  |---|---|---|---|
  | Postpaid | `mtu_postpaid` | CNY 41.00/hour/instance (1-minute granularity) | Provisioned directly at job creation; no pre-purchase |
  | Prepaid | `mtu_prepaid` | CNY 19,914.00/month/instance | Requires `--instance-id` (get it from your account manager); early unsubscribe billed at 1.2× the hourly rate |

  The official demo (qwen3.5-9b) needs at least 24 × MTU4 ≈ **CNY 984/hour** (postpaid). Before submitting you **must** explicitly state spec × count × estimated duration and the cost magnitude to the user, and get confirmation.
- **`mtu_capacity` hard formula**: `--mtu-count` must strictly equal `nnodes_rollout × n_gpus_rollout + nnodes_training × n_gpus_training` (all four live in `hyper_parameters`; defaults differ per model). When tuning parallelism hyperparameters, update `--mtu-count` in lockstep. Recommended starting points: qwen3.5-9b → 24; qwen3.6-flash-2026-04-16 / qwen3.5-flash-2026-02-23 / qwen3.6-35b-a3b (MoE) → 40.
- **dry-run → user confirmation → `--yes`**: `rl run` / `rl cancel` / `rl delete` / `rl authorize --authorize` / `runtime clean` are all `risk: high`. Preview with `--dry-run` first (rl run's dry-run is zero-network, zero-billing), then hand the preview and cost back to the user; **never add `--yes` automatically**. On exit code 7 / `requires_confirmation`, stop and ask for confirmation — that is normal control flow, not a bug; re-confirm whenever the target or scope changes.
- **A `--watch` timeout only stops waiting — it never cancels the cloud job** (same for `--wait-timeout` / `--poll-timeout`). The job keeps billing; only an explicit `rl cancel` stops it.

## Step 1: Authorization & sandbox runtime

```bash
bl finetune rl authorize                        # read-only probe (Console auth); per-item READY/MISSING/UNKNOWN/REQUIRES_USER_ACTION
bl finetune rl authorize --authorize --yes      # enable RL business mode only after user confirmation AND prerequisites READY (never creates roles, never enables OPD)
bl finetune runtime prepare                     # first-time download & verification of the managed runtime (local only, no cloud resources)
bl finetune runtime doctor                      # read-only health check: credential deny-read / home redirect / SDK import / host network reachability (advisory) etc.; non-zero exit on failure
```

**The CLI never creates service-linked roles (SLR).** Role authorization is an account-level grant that only the user can perform in the console. The probe reports six checks:

| Check | Required? | Not READY means | Agent action |
|---|---|---|---|
| `whitelist` | yes | RL admission not granted (`REQUIRES_USER_ACTION`) | Hand back to user: enablement via account manager; do not retry in a loop |
| `finetune-slr` | yes | Fine-tuning SLR missing (covers FC **and** SLS roles) → `REQUIRES_USER_ACTION`, **blocks enablement** | Stop; guide the user to console one-click authorization per the doc below; re-run the probe after the user confirms completion |
| `telemetry-slr` | no (advisory) | Xtrace telemetry SLR missing → `REQUIRES_USER_ACTION` | Same console guidance; does **not** block `ok` or submission |
| `apptrace-service` | no (advisory) | AppTrace not activated (console purchase page) | Manual console step; advisory only |
| `sls-service` | no (advisory) | **Static** manual reminder, always `REQUIRES_USER_ACTION` — the CLI never probes or opens SLS | Tell the user SLS activation is a separate manual console step; its SLR is already covered by `finetune-slr`. Not an error — do not try to clear it via CLI |
| `business-enabled` | yes | RL training mode not enabled | `--authorize --yes` enables it **only when** `whitelist` + `finetune-slr` are already READY |

- **Stop-and-guide rule**: any required `REQUIRES_USER_ACTION` → stop the flow, give the user the console authorization guidance (model-tuning page one-click authorization; doc: https://docs.bailian.console.aliyun.com/zh/model-studio/rl-training-overview#%E7%8E%AF%E5%A2%83%E5%87%86%E5%A4%87 ), wait for the user to complete it, then re-run `bl finetune rl authorize` to verify. Never attempt role creation through any CLI/API path, and never treat advisory items as blockers.
- `--authorize` only flips business enablement; with missing prerequisites it does nothing — roles must be authorized manually first. `ok: true` requires every **required** check READY; advisory degradation does not fail the report.
- Query failures are always `UNKNOWN` — never assume enabled.
- Mirror switches for stuck downloads (integrity verification is never skipped): `BAILIAN_RL_PYTHON_MIRROR` (custom CPython mirror prefix; built-in npmmirror fallback); `BAILIAN_RL_PIP_INDEX_URL` (PyPI mirror, e.g. `https://pypi.tuna.tsinghua.edu.cn/simple/`). If a mirror lags behind PyPI, pip fails closed with `No matching distribution found for X==ver` — switch to a fresher mirror or back to default PyPI.
- For development, `BAILIAN_RL_RUNTIME` can point at a local dashscope Python directory to skip release verification (integration debugging only).
- **Agent host sandboxes may block outbound network** (e.g. Codex's default `workspace-write` disables network and restricts writes to the workspace): `runtime prepare` downloads and `rl run` submission then fail with connect-level `EPERM` / `EACCES` / `ENETUNREACH` — switching mirrors does not help. `runtime doctor` probes host reachability (API / CPython download / PyPI) as the advisory `host-network-reachability` check: on `degraded`, stop and either (a) enable network access for the agent (Codex: `sandbox_workspace_write.network_access = true`), or (b) run `runtime prepare` and the submission in a regular terminal. The CLI honors `HTTPS_PROXY` / `HTTP_PROXY` (upper- or lowercase) when an egress proxy is available. Provisioning is one-time — a READY runtime is reused across runs, so preparing once in a regular terminal unblocks later agent runs; submission itself always needs network.

## Step 2: Prepare data & code

**Fastest path — the official demo** (math-calculation agent, minimum 24 × MTU4):
download [agentic-rl-example.zip](https://g-adoc.alcasset.com/media/maas_docs/sfm/zh/files/6a4b3c2d1e0f90c0.zip); key structure after extraction:

```
agentic-rl-example/
├── job.yaml                  ← YAML submission config (feed directly to bl finetune rl run --config-file)
├── data/calc_train_min.jsonl / calc_validation_min.jsonl   ← minimal data (recommended for the first run)
├── functions/rollout/rollout.py      ← Rollout: LangGraph + MCP calculator tool
├── functions/reward/reward.py        ← Reward: scores against the reference answer
└── requirements.txt          ← function business dependencies (only packaged & uploaded to FC; never installed into the local sandbox)
```

**Data format** (JSONL, one object per line):

```json
{"messages": [{"content": "Output the answer when you are ready. The answer should be surrounded by three sharps (`###`), in the form of ### ANSWER: <answer> ###. 6.6 minus x (3/2) times equals 5.6.", "role": "user"}], "rollout_extra": {"solution": "2/3"}}
```

- `messages`: the user question in ChatML format; `rollout_extra`: reference answer / business data, passed through to Rollout's `RolloutInput.rollout_extra` and Reward's `RewardInput.agent_output.rollout_extra`. Keys are user-defined (not limited to `solution`).
- Volume: tens to hundreds of rows suffice to validate the pipeline, but the count **must exceed batch_size**; larger is steadier for real training.
- Upload package limit 200 MB; use `--exclude <glob>` (repeatable) to strip `.git` / `data` / `__pycache__` etc. (maps to the SDK's `FC_ZIP_EXCLUDE_PATTERNS`); `--include <glob>` for the inverse selection.
- Custom Rollout / Reward development → official guide https://docs.bailian.console.aliyun.com/zh/model-studio/rl-function-development-guide . **Metric names returned by the Reward function must match the `--reward-metric` keys verbatim** (e.g. a function returning `{"accuracy":…, "format":…}` pairs with `--reward-metric reward-1.accuracy=0.7`); mismatches silently drop weights.

## Step 3: Submit the training job

**Preview the spec with dry-run first (zero network, zero billing); the user adds `--yes` after confirming:**

```bash
bl finetune rl run \
  --model qwen3.5-9b \
  --train-file /abs/path/data/calc_train_min.jsonl \
  --validation-file /abs/path/data/calc_validation_min.jsonl \
  --code-dir /abs/path/agentic-rl-example \
  --requirements requirements.txt \
  --rollout functions.rollout.rollout.CalcXRolloutProcessor \
  --reward reward-1=functions.reward.reward.DemoRewardProcessor \
  --reward-metric reward-1.accuracy=0.7 --reward-metric reward-1.format=0.3 \
  --hp algorithm=gspo --hp batch_size=64 --hp eval_steps=1 --hp kl_loss_coef=0.002 \
  --hp learning_rate=2e-6 --hp lr_scheduler_type=linear --hp max_length=8192 \
  --hp n_epochs=1 --hp n_rollouts=8 --hp ppo_mini_batch_size=8 --hp save_strategy=epoch \
  --charge-type mtu_postpaid --mtu-spec MTU4 --mtu-count 24 \
  --dry-run
```

- The 11 `--hp` entries above are the **field-verified required starting set for qwen3.5-9b (non-MoE) GSPO** — the server enforces required hyperparameters (an empty `hyper_parameters` is rejected with 400, e.g. `n_epochs is required.`). **Do not assume the platform fills defaults and omit the whole set.** MoE models (qwen3.6-35b-a3b etc.) have different required sets and defaults — check https://docs.bailian.console.aliyun.com/zh/model-studio/rl-training-config-monitoring ; do not copy blindly.
- **Path rules**: `--code-dir` / `--train-file` / `--validation-file` resolve against the **CLI process cwd** — when running across directories (especially `pnpm -s bl`, whose cwd is pinned to `packages/cli`), always use **absolute paths**. The single exception: `--requirements` must stay **relative to code-dir** (the SDK does `join(zipdir, requirements_path)` internally).
- `--rollout <classpath>` with a bare classpath defaults the function name to `rollout-1`; `--reward` requires explicit `name=classpath`. Optional function tuning: `--function-timeout name=seconds`, `--function-runtime name.field=value` (cpu/memory_size/concurrency etc.), `--reward-weight name=value`, `--function-env name.KEY=value`; all can be omitted on the first run.
- **YAML-equivalent path**: if the demo ships `job.yaml`, run `bl finetune rl run --config-file /abs/path/job.yaml --dry-run` directly; explicit flags override same-named YAML fields, and `--clear-functions` empties the YAML functions section. Both submission styles produce an equivalent spec — pick one.
- Reuse uploaded data: `--train-file-id <id>` / `--validation-file-id <id>` (obtained via `bl dataset upload`).
- If the runtime has never been prepared, add `--install-runtime` to allow in-place installation; otherwise run Step 1's `runtime prepare` first.
- On successful submission, record the `job_id` (form `ft-xxx`). Add `--watch` to block-poll until a terminal state (`--wait-timeout <seconds>` only stops waiting, never cancels the job).

## Step 4: Monitor training

```bash
bl finetune rl watch --job-id ft-xxx                          # single non-blocking probe
bl finetune rl watch --job-id ft-xxx --follow --interval 10   # poll to terminal state (non-zero exit on FAILED/CANCELED)
bl finetune rl logs --job-id ft-xxx --offset 0 --lines 100    # training logs
bl finetune rl get --job-id ft-xxx                            # job details
bl finetune rl list --page 1 --size 20                        # job history
```

- Training typically takes tens of minutes to hours. Watch `critic/rewards/mean` on the console **Metrics** tab: a steady rise means it is learning; if it plateaus or drops, stop and investigate — do not burn MTU idly.
- **On FAILED, read the logs first**: pull the tail errors with `rl logs`; configuration/dependency errors are usually obvious. Note the CLI-side logs cover the orchestration layer only — training-engine / in-function errors do not land in the CLI; use the console job-details **Logs** tab, or ask the platform for backend logs with the job_id / request_id.
- Console details page has five tabs: Details / Trajectories (agent behavior replay + three-dimensional reward analysis) / Metrics (13 chart groups) / Logs / Artifacts (checkpoints).
- Four starter practices: validate the pipeline on minimal data before switching to full data; do not touch hyperparameters on the first run — when tuning, change one variable at a time and run at least `eval_steps × 3` steps before judging; watch one core metric; read logs first on failure.
- Stop-loss: when a confirmed misconfiguration requires aborting, `bl finetune rl cancel --job-id ft-xxx --dry-run` → user confirmation → `--yes` (cancel is destructive; progress may be lost).

## Step 5: Publish & deploy the model

After SUCCEEDED, **the last checkpoint is auto-published to "My Models"** — manual export is usually unnecessary:

```bash
bl finetune checkpoints --job-id ft-xxx        # checkpoint list & publication status
# Only needed to publish an intermediate checkpoint (also doable on the console Artifacts tab):
bl finetune export --job-id ft-xxx --checkpoint <ckpt-name> --model-name my-rl-model

bl deploy models --source custom               # confirm deployable models & plans
bl deploy list --status RUNNING                # reuse check: do not create another billed instance if the same model is already RUNNING
bl deploy text create --model-name <published-model-name> --display-name my-rl-svc --dry-run
# --yes after user confirmation; record output.deployed_model from the response
bl text chat --model <deployed_model> --message "6.6 minus x (3/2) times equals 5.6, solve x."
```

- **Inference `--model` must use `deployed_model` from the deploy response**, not the name passed to `deploy create --model-name` — the wrong one 404s with `Model not exist`.
- Invoking immediately after the deployment reaches RUNNING may briefly 404 (server-side state propagation delay); wait a dozen seconds and retry. On persistent 404, first check whether the model name is wrong.
- Deployment plans / billing / pause-delete operations are covered by skill `bailian-finetune` and `bl deploy --help`; this skill does not duplicate them.

## Wrap-up & cleanup

- Delete a job record: `bl finetune rl delete --job-id ft-xxx` (destructive; dry-run → user `--yes`).
- Sandbox artifacts: task directories are destroyed automatically when the call ends (same policy for success/failure/timeout). For crash orphans and superseded runtime versions, preview the remove/keep plan with `bl finetune runtime clean --dry-run` → user confirmation → `--yes` (`--ttl-hours` adjusts the orphan threshold, default 24h). The current baseline runtime, the `BAILIAN_RL_RUNTIME` directory, and the download cache are never touched.
- Idle-billing reminder: training fees stop once the RL job reaches a terminal state, but **deployment instances** (especially mu/ptu) bill while idle — clean up with `bl deploy pause` / `delete` when unused.

## Common pitfalls (field-verified)

- **SLR `REQUIRES_USER_ACTION` is a stop-and-guide signal**: the CLI cannot create service-linked roles — guide the user to console authorization, then re-probe; `sls-service` is a static advisory that is always present, never a failure to retry. `--authorize` with missing role prerequisites silently does nothing.
- **Connect-level `EPERM` / `ENETUNREACH` inside an agent ≠ regional network issue**: do not loop on mirrors or retries. Read `runtime doctor`'s `host-network-reachability` detail, then enable network access in the agent settings or move prepare / submission to a regular terminal (`HTTPS_PROXY` is honored when set).
- **Answering with docs + code instead of intake**: a triggered training request with missing inputs must produce clarifying questions (Step 0), not a doc-reading spree followed by SDK code samples. Official docs are for resolving a specific blocker mid-flow, never the default first action.
- **These commands/flags do not exist**: no `bl finetune rl jobs` subgroup; `rl run` has no top-level `--timeout` (use `--wait-timeout`); YAML input is `--config-file`, not `--config` (the latter is the global profile flag); `--yes` is runtime-injected — do not invent confirmation flags.
- **Hyperparameters cannot be omitted wholesale**: SDK type annotations of Optional=None are pass-through only; required constraints live in the server-side validation layer. The only evidence for whether something can be omitted is dry-run + real submission responses, not source annotations.
- **`--requirements` lists function business dependencies**: they are only read/packaged/uploaded to the FC container and never enter the local sandbox install step. The local SDK version is fixed by the managed runtime baseline; `FC_PYPI_LIB` is derived and injected automatically by the CLI, invisible to the user — do not export it manually, and do not pip install dashscope on the host for RL.
- **Function registration failure ≠ training failure**: `[2052] Registration failed` happens before the training job is created (no billed training in principle); check `rl list` for FAILED records first. For sandbox write-permission / path errors, check cwd and the absolute-path rules first.
- **Reward metric-name mismatch is a silent error**: `--reward-metric` keys must equal the metric names the Reward function actually returns, verbatim.
- **watch/logs/get/cancel/delete go host-direct** and need no sandbox runtime; only `rl run` goes through the sandbox. An unprepared runtime does not affect query commands.
- **Server errors pass through verbatim**: the CLI does not translate server error codes; a 403 `Workspace.AccessDenied` is an account/workspace configuration issue — verify `--workspace-id` and API key ownership instead of mutating the command and retrying.

## Out of scope

These intents do not belong to this skill; here are the correct entry points to avoid misrouting:

| User intent | Correct entry |
|---|---|
| SFT / DPO / CPT / LoRA supervised fine-tuning; audio/image/video fine-tuning | skill `bailian-finetune` (`bl finetune text\|audio\|image create`) |
| OPD distillation (`pg_opd`, teacher_model, pure model distillation) | skill `bailian-finetune` (`bl finetune opd *`, host-direct, no sandbox) |
| Training jobs on non-Bailian platforms | Not this skill — use that platform's own tooling |
| Just trying a model / one-off chat | `bl text chat` (skill `bailian-cli`) |
| Model selection / recommendation | `bl advisor recommend` |
| Training quota / usage | `bl quota` / `bl usage` (skill `bailian-cli`) |

## references

- [bailian-protocol](../bailian-protocol/SKILL.md) — shared protocol (consent / version pre-flight / auth / attribution / error reporting); read before executing
- skill `bailian-finetune`'s `reference/finetune.md` — authoritative flag tables for `rl *` / `runtime *` (generated); Read it if installed, otherwise prompt `bl skill init`
- Official docs: [RL training overview](https://docs.bailian.console.aliyun.com/zh/model-studio/rl-training-overview) · [RL function development guide](https://docs.bailian.console.aliyun.com/zh/model-studio/rl-function-development-guide) · [RL training configuration & monitoring](https://docs.bailian.console.aliyun.com/zh/model-studio/rl-training-config-monitoring) · [Observability configuration](https://docs.bailian.console.aliyun.com/zh/model-studio/observable-configuration-for-reinforcement-learning) · [Model Training Unit](https://docs.bailian.console.aliyun.com/zh/model-studio/model-training-unit)