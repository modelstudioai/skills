# bailian-model-recommend

> [中文版 / Chinese →](README.zh.md)

Model selection & recommendation skill for **Alibaba Cloud Model Studio (Bailian)** — analyzes your AI scenario and recommends the best-fit models from the Bailian model marketplace, complete with trade-off comparisons and ready-to-use code samples.

## What it does

Tell your agent what you want to build, and this skill will:

1. **Understand your requirements** — extract modality, capability, budget, and quality preferences from your description
2. **Filter candidates** — search the full Bailian model catalog by modality, capability, context window, and semantic relevance
3. **Recommend 3 models** — best fit, runner-up, and an alternative perspective, each with clear trade-off explanations
4. **Provide code samples** — OpenAI-compatible Python SDK and cURL examples for each recommendation

## When to use

**Explicit model selection:**
- "Recommend a model for X"
- "Which model should I use for Y?"
- "Compare model A vs model B"

**Implicit model selection (you describe a goal, the skill picks the model):**
- "I want to build a customer service chatbot"
- "Help me implement image generation"
- "What AI solution fits my summarization use case?"

**Technical selection:**
- "Which model is best for low-cost / high-throughput / high-accuracy scenarios?"
- "Model A vs Model B — which is better for task Y?"

**Not for this skill:**
- You already know which model to use and just need the API call → use `bailian-cli` directly
- Pure parameter / pricing lookup → use `bailian-docs-llm-wiki`

## Example

```
I want to build a multilingual customer service bot that handles
Chinese + English, needs to support function calling, and I want
to keep costs low.
```

The skill will recommend 3 models with reasoning like:

| # | Strategy | Example rationale |
|---|----------|-------------------|
| **1 — Best fit** | Cost-effective with function calling | "Supports both languages, native tool use, lowest per-token cost in its tier" |
| **2 — Runner-up** | Higher capability, moderate cost | "Stronger reasoning for complex queries, 2× cost but handles edge cases better" |
| **3 — Alternative** | Different trade-off angle | "Open-source option with self-hosting flexibility, no per-call charge at scale" |

Each recommendation includes model name, ID, key specs (context window, pricing), and copy-paste code samples.

## Prerequisites

- [`bailian-docs-llm-wiki`](../bailian-docs-llm-wiki/) skill installed (provides the model data catalog)
  - Auto-installed if missing: `npx skills add modelstudioai/skills --skill bailian-docs-llm-wiki -y`

## How it works under the hood

Deterministic pipeline (ported from the `bl advisor recommend` engine in
bailian-cli): scene presets, recall, scoring, ranking, slot assignment and code
sample extraction all run in `scripts/recommend.mjs` — no LLM involved in those
decisions. The LLM only writes the final recommendation reasons.

```
User request
  → one command: scripts/recommend.mjs --scene code --exclude qwen
      scene preset → intent (modality, capabilities, scenes, budget, targets)
      → snapshot dedup → excludes → hard filter (modality + capability, capability never dropped)
      → notSuitableFor exclusion → formula scoring → tier/price/provider ordering
      → family fairness cap → slot assignment (primary / runner-up / exploration)
      → embed specs + code samples + endpoint notes + warnings
  → LLM: write recommendation reasons grounded in that single JSON output
  → Output natural-language recommendation with specs + code
```

The candidate list is never added to, removed from, or reordered by the LLM.
All recommendations are grounded in the actual model catalog data — the skill never recommends from memory.

Lower-level entries stay available: `scripts/recall-rank.mjs` for a hand-written
intent JSON (pipeline scenarios, `--with-samples` to embed code) and
`scripts/get-samples.mjs` when the user already picked a model and only wants code.

## License

Apache-2.0
