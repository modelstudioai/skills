# bailian-rl-deploy

> [中文版 / Chinese →](README.zh.md)

End-to-end **RL train → monitor → publish → deploy → call** skill for **Alibaba Cloud Model Studio (Bailian)** — drives the full reinforcement-learning loop with the Bailian CLI (`bl`): authorization probe → managed sandbox runtime → data & Rollout/Reward code → submit RL job (`bl finetune rl run`) → watch training → auto-published checkpoint → create inference deployment → hand off a callable example. RL optimizes the model through a generate (Rollout) → score (Reward) → optimize loop — no ground-truth labels required.

## What it does

Tell your agent "train a reasoning model with RL on Bailian" or "submit an AgenticRL job," and this skill will:

1. **Intake & gates** — if the request lacks inputs, ask the user first (base model / training data / Rollout-Reward code / MTU billing / deploy intent, with official-demo defaults offered as a one-shot option); then verify the CLI has the `rl` command group, check auth (`bl auth status`), probe RL enablement (`bl finetune rl authorize`), and prepare + health-check the managed sandbox runtime (`bl finetune runtime prepare` / `doctor`)
2. **Prepare data & code** — JSONL (`messages` + `rollout_extra`) plus a Rollout/Reward function package; the official math-agent demo works out of the box
3. **Submit with a billing gate** — `bl finetune rl run --dry-run` (zero network, zero billing) → disclose MTU spec × count × cost → user confirms → `--yes`
4. **Monitor** — `bl finetune rl watch / logs / get` plus the console Metrics tab (`critic/rewards/mean`); on FAILED, read logs before touching anything
5. **Publish & deploy** — the last checkpoint auto-publishes to "My Models"; `bl deploy text create` turns it into a callable service, invoked via `bl text chat --model <deployed_model>`

## When to use

**Explicit RL training:**
- "Train a model with reinforcement learning on Bailian"
- "Submit a GRPO/GSPO RL job"
- "Run AgenticRL training with my reward function"
- "Train math reasoning / agent tool-calling with RL"

**Implicit (describe a goal, the skill runs the loop):**
- "I want my model to get better at multi-step tool use through trial and error"
- "Optimize my agent's policy with a custom reward — no labeled answers"
- "Use the official demo to try my first RL training run"

**Not for this skill (reverse-trigger routing):**
- SFT / DPO / CPT / LoRA supervised fine-tuning, audio/image/video fine-tuning → `bailian-finetune` (CLI registry, `bl skill init`)
- OPD distillation (`pg_opd`, `teacher_model`) → `bailian-finetune` (`bl finetune opd *`)
- Just want to try a model / one-off chat → `bailian-cli`: `bl text chat`
- Don't know which base model to pick → `bailian-model-recommend`
- Training quota / usage questions → `bailian-cli`: `bl quota` / `bl usage`

## Safety guardrails

RL jobs provision **dedicated MTU (Model Training Unit) resources — billing starts at creation**, and there is no per-token billing option:

1. **dry-run → confirm → `--yes`** — `rl run` / `cancel` / `delete` / `authorize --authorize` / `runtime clean` are all high-risk writes. Preview with `--dry-run` first, disclose spec × count × estimated duration and the cost magnitude, and only add `--yes` after explicit user confirmation. Exit code 7 / `requires_confirmation` is normal control flow — stop and ask, never auto-approve.
2. **Cost transparency** — type-IV MTU4 postpaid is CNY 41.00/hour/instance; the official qwen3.5-9b demo needs 24 × MTU4 ≈ **CNY 984/hour**. Prepaid requires an `--instance-id` from your account manager.
3. **Capacity formula** — `--mtu-count` must equal `nnodes_rollout × n_gpus_rollout + nnodes_training × n_gpus_training`; tune parallelism hyperparameters and capacity in lockstep.
4. **Waiting ≠ canceling** — a `--watch` timeout (or Ctrl-C) only stops waiting; the cloud job keeps running and billing. Only an explicit `rl cancel` (with confirmation) stops it.
5. **Platform & access gates** — the sandbox is macOS/Linux only (Windows fails closed); RL training requires account-manager whitelist enablement. The CLI **never creates service-linked roles** — a missing required role stops the flow and guides the user to console one-click authorization, then re-probes; advisory items (telemetry SLR / AppTrace / SLS activation) do not block.

## Prerequisites

- `bl` (bailian-cli) with the `rl` command group (`bl finetune rl run --help` must work; older CLIs need `bl update`)
- Authenticated: `bl auth status`, or `bl auth login --api-key sk-...`
- macOS or Linux; RL training whitelist enabled for your account
- **No local Python / dashscope install needed** — the CLI ships a reviewed managed runtime (pinned CPython + dashscope baseline), downloaded, verified, and cached automatically
- **Outbound network access** for runtime download and job submission. Agent host sandboxes (e.g. Codex default `workspace-write`) block network by default: `runtime doctor` reports this as the advisory `host-network-reachability` check — enable network for the agent or run prepare / submission in a regular terminal; `HTTPS_PROXY` / `HTTP_PROXY` (upper- or lowercase) are honored

## Example

```
Use the official agentic-rl demo to run my first RL training on Bailian:
qwen3.5-9b, GSPO, minimal calc data, MTU4 postpaid.
Preview the cost first, then submit after I confirm, and deploy the
result so I can call it.
```

The skill walks the five-step pipeline:

```
authorize → runtime prepare/doctor → data & functions → rl run (dry-run → confirm → --yes)
  → rl watch/logs (critic/rewards/mean) → checkpoint auto-publish → deploy text create → text chat
```

It captures the right IDs at each step (`job_id` → published model → `deployed_model`) and steers around the common pitfalls (calling the fine-tuned model by its `qwen3.5-9b-ft-...` name returns 404 — inference must use the `deployed_model` from the deploy response).

## How it works under the hood

```
User request
  → Version/platform/auth gates + rl authorize probe (Console auth)
  → runtime prepare (managed CPython + dashscope, integrity-verified) + doctor self-checks
  → Data JSONL + Rollout/Reward package (--requirements uploaded to FC only, never installed locally)
  → rl run --dry-run (zero-network spec preview) → user confirmation → --yes submit
  → rl watch --follow / logs / get (host-direct, no sandbox needed for queries)
  → Last checkpoint auto-published → deploy text create → bl text chat --model <deployed_model>
```

The skill encodes the orchestration plus field-verified gotchas: the 11 required GSPO hyperparameters for qwen3.5-9b (the server rejects an empty `hyper_parameters`), absolute-path rules for `--code-dir` / data files vs the code-dir-relative `--requirements`, reward metric names must match `--reward-metric` keys verbatim, sandbox task dirs are destroyed per call, and server errors pass through untranslated.

## License

Apache-2.0