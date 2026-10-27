#!/usr/bin/env node
// recall-rank.mjs — 确定性召回+打分+排序+席位分配
//
// 移植自 bailian-cli `packages/core/src/advisor/engine/`（recall/hard-filter、
// score formula、rank、fairness），供 bailian-model-recommend skill 使用。
// 确定性逻辑不依赖 LLM：LLM 只负责把用户需求转成 intent JSON 传给本脚本，
// 以及在最后为入围模型撰写推荐理由。
//
// 用法：
//   node scripts/recall-rank.mjs <intent.json> [--top 3] [--data <wiki-models-dir>]
//   cat intent.json | node scripts/recall-rank.mjs -     # stdin
//
// intent.json 结构见 references/requirement-schema.md。输出 JSON：
//   { candidates: [{ rank, slot, model, name, provider, family, tier,
//     finalScore, specs: {...}, matchedScenes }], poolSize, gate }

import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";

// ---- CLI 参数 ----

const args = process.argv.slice(2);
const intentArg = args[0];
const flagValue = (name) => {
  const idx = args.indexOf(`--${name}`);
  return idx >= 0 ? args[idx + 1] : undefined;
};
const topN = Number.parseInt(flagValue("top") ?? "3", 10);
const wikiDirDefault =
  process.env.BAILIAN_CONFIG_DIR
    ? join(process.env.BAILIAN_CONFIG_DIR, "skills", "bailian-docs-llm-wiki", "models")
    : join(homedir(), ".bailian", "skills", "bailian-docs-llm-wiki", "models");
const dataDir = flagValue("data") ?? wikiDirDefault;

if (!intentArg || !topN) {
  process.stderr.write(
    "用法: node scripts/recall-rank.mjs <intent.json> [--top 3] [--data <wiki-models-dir>]\n" +
      "  intent.json 结构见 references/requirement-schema.md；传 - 从 stdin 读\n",
  );
  process.exit(2);
}

const intent = JSON.parse(intentArg === "-" ? readFileSync(0, "utf-8") : readFileSync(intentArg, "utf-8"));

const modelsPath = join(dataDir, "models.jsonl");
if (!existsSync(modelsPath)) {
  process.stderr.write(`找不到模型目录数据: ${modelsPath}\n请先安装 bailian-docs-llm-wiki skill。\n`);
  process.exit(1);
}

// ---- 数据加载（快照去重，兼容 YYYY-MM-DD 与 MMDD 两种快照后缀）----

const SNAPSHOT_DATE_RE = /(-\d{4}-\d{2}-\d{2}|-\d{4})$/;

function readJsonl(filePath) {
  const records = [];
  for (const line of readFileSync(filePath, "utf-8").split("\n")) {
    if (!line.trim()) continue;
    try {
      records.push(JSON.parse(line));
    } catch {
      // 跳过坏行
    }
  }
  return records;
}

const rawModels = readJsonl(modelsPath);
const mainModels = new Set(rawModels.map(({ model }) => model));
const allModels = rawModels.filter(({ model }) => {
  const base = model.replace(SNAPSHOT_DATE_RE, "");
  return base === model || !mainModels.has(base);
});

// ---- 确定性过滤链（hard-filter.ts 移植）----

const isAvailable = (model) => !model.offlineInfo;

const firstPrice = (model) => {
  const raw = model.prices?.[0]?.price;
  const num = raw ? Number.parseFloat(raw) : Number.NaN;
  return Number.isFinite(num) ? num : Number.POSITIVE_INFINITY;
};

function matchesModalityCap(model, inputModality, outputModality, requiredCapabilities) {
  const modelIn = model.inferenceMetadata?.request_modality ?? [];
  const modelOut = model.inferenceMetadata?.response_modality ?? [];
  if (inputModality.length > 0 && modelIn.length > 0 && !inputModality.some((mod) => modelIn.includes(mod))) return false;
  if (outputModality.length > 0 && modelOut.length > 0 && !outputModality.some((mod) => modelOut.includes(mod))) return false;
  if (requiredCapabilities.length > 0 && !requiredCapabilities.some((cap) => model.capabilities.includes(cap))) return false;
  return true;
}

const matchesIntentHard = (model) =>
  matchesModalityCap(model, intent.inputModality ?? [], intent.outputModality ?? [], intent.requiredCapabilities ?? []);

/** 能力约束永不静默丢弃：硬门不足时先去模态保能力，仅当无任何模型匹配能力才回全池。 */
function filterWithFallback(pool) {
  const filtered = pool.filter(matchesIntentHard);
  if (filtered.length >= 5) return filtered;
  if ((intent.requiredCapabilities ?? []).length > 0) {
    const capOnly = pool.filter((model) => intent.requiredCapabilities.some((cap) => model.capabilities.includes(cap)));
    if (capOnly.length > 0) return capOnly;
  }
  return pool;
}

/** notSuitableFor 与用户场景/任务信号的关键词排除。 */
function applyDisqualification(pool) {
  const signals = [...(intent.matchedScenes ?? []), ...(intent.scenarioHints ?? [])].filter(Boolean);
  if (signals.length === 0) return pool;
  return pool.filter((model) => {
    const negatives = model.profile?.notSuitableFor;
    if (!negatives?.length) return true;
    return !negatives.some((neg) => signals.some((sig) => neg.includes(sig)));
  });
}

// ---- 用户点名模型（target-match，forced 语义）----

function resolveTargetedModels(pool, targets) {
  if (!targets?.length) return [];
  const normalized = targets.map((t) => t.toLowerCase());
  return pool.filter((model) => {
    const id = model.model.toLowerCase();
    const family = (model.family ?? "").toLowerCase();
    return normalized.some((t) => id === t || id.includes(t) || family === t || family.includes(t));
  });
}

// ---- 公式打分（score/index.ts formulaScore 移植）----

const CONTEXT_THRESHOLDS = { standard: 0, large: 32000, "extra-large": 128000 };
const WEIGHT_PRESETS = {
  match: { scene: 0.4, tier: 0.2, price: 0.2, context: 0.2 },
  optimize: { scene: 0.1, tier: 0.1, price: 0.6, context: 0.2 },
  evaluate: { scene: 0.5, tier: 0.2, price: 0.1, context: 0.2 },
  differentiate: { scene: 0.3, tier: 0.3, price: 0.2, context: 0.2 },
};
const PURE_DIMENSION_WEIGHTS = {
  price: { scene: 0, tier: 0, price: 1, context: 0 },
  context: { scene: 0, tier: 0, price: 0, context: 1 },
  quality: { scene: 0.2, tier: 0.8, price: 0, context: 0 },
  speed: { scene: 0.2, tier: 0, price: 0.4, context: 0.4 },
};

function resolveWeights() {
  const userIntent = intent.userIntent ?? "match";
  if (userIntent === "optimize" && intent.optimizeDimension) {
    return PURE_DIMENSION_WEIGHTS[intent.optimizeDimension] ?? WEIGHT_PRESETS.optimize;
  }
  return WEIGHT_PRESETS[userIntent] ?? WEIGHT_PRESETS.match;
}

function sceneMatchScore(model) {
  const scenes = intent.matchedScenes ?? [];
  if (scenes.length === 0) return 1;
  return scenes.some((scene) => (model.profile?.scenes ?? []).includes(scene)) ? 1 : 0;
}

function tierAlignScore(model) {
  const tier = model.profile?.familyTier;
  if (!tier) return 1;
  if (intent.qualityPreference === "flagship") return tier === "flagship" ? 1 : 0.5;
  if (intent.qualityPreference === "cost-optimized") return tier === "lightweight" ? 1 : 0.5;
  return 1;
}

function priceFitScore(model, pool) {
  const prices = pool.map((m) => firstPrice(m)).filter((p) => Number.isFinite(p));
  if (prices.length < 2) return 1;
  const min = Math.min(...prices);
  const max = Math.max(...prices);
  if (max === min) return 1;
  const price = firstPrice(model);
  const cheapness = Number.isFinite(price) ? 1 - (price - min) / (max - min) : 0.5;
  if (intent.budget === "low") return cheapness;
  if (intent.budget === "high") return 1 - cheapness * 0.5;
  return 0.5 + cheapness * 0.5;
}

function contextFitScore(model) {
  const threshold = CONTEXT_THRESHOLDS[intent.contextNeed] ?? 0;
  if (threshold === 0) return 1;
  const cw = model.contextWindow ?? 0;
  if (cw === 0) return 1;
  return cw >= threshold ? 1 : cw / threshold;
}

function formulaScore(pool) {
  const weights = resolveWeights();
  return pool.map((model) => ({
    model,
    score:
      weights.scene * sceneMatchScore(model) +
      weights.tier * tierAlignScore(model) +
      weights.price * priceFitScore(model, pool) +
      weights.context * contextFitScore(model),
  }));
}

// ---- 排序（recall/index.ts byTierThenPrice 移植）----

const TIER_ORDER = { flagship: 0, balanced: 1, lightweight: 2 };
const ALIBABA_PROVIDERS = new Set(["qwen", "qwen-domain-model", "wan"]);
const generationOf = (model) => {
  const match = model.model.match(/(\d+(?:\.\d+)?)/);
  return match ? Number.parseFloat(match[1]) : Number.NEGATIVE_INFINITY;
};

function byTierThenPrice(left, right) {
  const preferCheap = intent.budget === "low" || intent.qualityPreference === "cost-optimized";
  const tierA = TIER_ORDER[left.profile?.familyTier ?? ""] ?? 1.5;
  const tierB = TIER_ORDER[right.profile?.familyTier ?? ""] ?? 1.5;
  const tierDiff = preferCheap ? tierB - tierA : tierA - tierB;
  if (tierDiff !== 0) return tierDiff;
  const aliA = ALIBABA_PROVIDERS.has(left.provider) ? 0 : 1;
  const aliB = ALIBABA_PROVIDERS.has(right.provider) ? 0 : 1;
  if (aliA !== aliB) return aliA - aliB;
  const priceL = firstPrice(left);
  const priceR = firstPrice(right);
  const unknownL = !Number.isFinite(priceL);
  const unknownR = !Number.isFinite(priceR);
  if (unknownL !== unknownR) return unknownL ? 1 : -1;
  if (!unknownL) {
    const priceDiff = preferCheap ? priceL - priceR : priceR - priceL;
    if (priceDiff !== 0) return priceDiff;
  }
  return generationOf(right) - generationOf(left);
}

// ---- fairness（family 软上限 + 探索位）----

function applyFairness(ordered) {
  if (ordered.length <= 1) return ordered;
  const familyCounts = new Map();
  const kept = [];
  const overflow = [];
  for (const cand of ordered) {
    const family = cand.model.family;
    if (!family) {
      kept.push(cand);
      continue;
    }
    const count = familyCounts.get(family) ?? 0;
    if (count < 2) {
      kept.push(cand);
      familyCounts.set(family, count + 1);
    } else {
      overflow.push(cand);
    }
  }
  const result = [...kept, ...overflow];
  const visible = result.slice(0, topN);
  const families = new Set(visible.map((c) => c.model.family).filter(Boolean));
  if (topN >= 3 && families.size === 1 && result.length > topN) {
    const firstFamily = visible[0].model.family;
    const altIdx = result.findIndex((cand, index) => index >= topN && cand.model.family !== firstFamily);
    if (altIdx >= 0) {
      const [alternative] = result.splice(altIdx, 1);
      result.splice(topN - 1, 0, alternative);
    }
  }
  return result;
}

// ---- 主流程：召回 → 打分 → 排序 → fairness → 席位 ----

const pref = intent.modelPreference ?? { mode: "unconstrained" };
let pool = allModels.filter(isAvailable);

// excludes 统一过滤（匹配 model id / family / provider）
for (const excluded of pref.excludes ?? []) {
  const needle = excluded.toLowerCase();
  pool = pool.filter((model) => {
    const id = model.model.toLowerCase();
    const family = (model.family ?? "").toLowerCase();
    const provider = (model.provider ?? "").toLowerCase();
    const familyName = (model.familyName ?? "").toLowerCase();
    return !id.includes(needle) && !family.includes(needle) && !provider.includes(needle) && !familyName.includes(needle);
  });
}

let gate = "structured";
let scored;

if (pref.mode === "comparison" || pref.mode === "alternative") {
  // 用户点名模型（comparison：只返回点名集；alternative：点名+补齐）
  const forced = resolveTargetedModels(pool, pref.targets ?? []);
  if (pref.mode === "comparison" && forced.length > 0) {
    // 点名集保持用户顺序（forced-order 语义），不做 fairness 重排
    const order = (pref.targets ?? []).map((t) => t.toLowerCase());
    const sortedForced = [...forced].sort(
      (left, right) =>
        order.findIndex((t) => left.model.toLowerCase().includes(t) || (left.family ?? "").toLowerCase().includes(t)) -
        order.findIndex((t) => right.model.toLowerCase().includes(t) || (right.family ?? "").toLowerCase().includes(t)),
    );
    scored = formulaScore(sortedForced).map((cand, idx) => ({ ...cand, score: cand.score, forcedIdx: idx }));
    gate = "forced-comparison";
  } else if (forced.length > 0) {
    const seen = new Set(forced.map((m) => m.model));
    const fillCount = Math.max(0, Math.max(topN, 5) - forced.length);
    const fill = filterWithFallback(pool.filter((m) => !seen.has(m.model)))
      .sort(byTierThenPrice)
      .slice(0, fillCount);
    scored = [...formulaScore(forced), ...formulaScore(fill)];
    gate = "forced-alternative";
  } else {
    scored = formulaScore(applyDisqualification(filterWithFallback(pool)));
  }
} else {
  // structured：硬门 + 场景优先排序 + tier 配额多样性（top-K 池）
  const gated = filterWithFallback(pool);
  const scene = (intent.matchedScenes ?? [])[0];
  const sorted = [...gated].sort((left, right) => {
    if (scene) {
      const leftHit = left.profile?.scenes?.includes(scene) ? 0 : 1;
      const rightHit = right.profile?.scenes?.includes(scene) ? 0 : 1;
      if (leftHit !== rightHit) return leftHit - rightHit;
    }
    return byTierThenPrice(left, right);
  });
  const byTier = new Map();
  for (const model of sorted) {
    const tier = model.profile?.familyTier ?? "unknown";
    const list = byTier.get(tier) ?? [];
    list.push(model);
    byTier.set(tier, list);
  }
  const picked = [];
  const perTier = Math.ceil(20 / Math.max(byTier.size, 1));
  for (const [, group] of byTier) picked.push(...group.slice(0, perTier));
  if (picked.length < 20) {
    const pickedIds = new Set(picked.map((m) => m.model));
    for (const model of sorted) {
      if (picked.length >= 20) break;
      if (!pickedIds.has(model.model)) picked.push(model);
    }
  }
  const kept = new Set(applyDisqualification(picked).map((m) => m.model));
  const finalPool = picked.filter((m) => kept.has(m.model));
  scored = formulaScore(finalPool.length > 0 ? finalPool : picked);
  gate = "structured";
}

// 排序：分数降序，同分价格升序（便宜优先）
let ordered = [...scored].sort((left, right) => {
  // forced 候选（点名模型）锁在点名顺序，不参与按分重排
  const forcedL = left.forcedIdx !== undefined;
  const forcedR = right.forcedIdx !== undefined;
  if (forcedL && forcedR) return left.forcedIdx - right.forcedIdx;
  if (forcedL !== forcedR) return forcedL ? -1 : 1;
  const diff = right.score - left.score;
  if (Math.abs(diff) > 1e-9) return diff;
  return firstPrice(left.model) - firstPrice(right.model);
});
ordered = gate === "forced-comparison" ? ordered : applyFairness(ordered);

// ---- 席位分配（rank/index.ts assignTierSlots 移植）----

const SLOTS = ["primary", "runner-up", "exploration"];
const assignSlots = (candidates) =>
  candidates.slice(0, topN).map((cand, idx) => ({ ...cand, rank: idx + 1, slot: SLOTS[Math.min(idx, SLOTS.length - 1)] }));

function assignTierSlots(candidates) {
  if (topN < 3 || candidates.length < 3) return assignSlots(candidates);
  const picked = [];
  const used = new Set();
  const backfill = () => {
    for (const cand of candidates) {
      if (picked.length >= 3) break;
      if (used.has(cand.model.model)) continue;
      picked.push(cand);
      used.add(cand.model.model);
    }
  };
  if (intent.budget === "low" || intent.qualityPreference === "cost-optimized") {
    const groups = new Map();
    for (const cand of candidates) {
      const tier = cand.model.profile?.familyTier ?? "unknown";
      const list = groups.get(tier) ?? [];
      list.push(cand);
      groups.set(tier, list);
    }
    for (const tier of ["lightweight", "balanced", "flagship"]) {
      const cand = groups.get(tier)?.[0];
      if (cand && !used.has(cand.model.model)) {
        picked.push(cand);
        used.add(cand.model.model);
      }
      if (picked.length >= 3) break;
    }
    backfill();
    return assignSlots(picked);
  }
  const providers = new Set();
  for (const cand of candidates) {
    if (picked.length >= 3) break;
    if (cand.model.profile?.familyTier !== "flagship") continue;
    if (providers.has(cand.model.provider)) continue;
    providers.add(cand.model.provider);
    picked.push(cand);
    used.add(cand.model.model);
  }
  backfill();
  return assignSlots(picked);
}

const forcedGate = gate.startsWith("forced");
const ranked = forcedGate ? assignSlots(ordered) : assignTierSlots(ordered);

// ---- specs 透出（specs.ts buildModelSpecs 移植）----

const PRICE_TYPE_LABEL = {
  input_token: "输入",
  output_token: "输出",
  input_token_cache: "缓存输入",
  input_token_cache_creation_5m: "缓存写入",
  input_token_cache_read: "缓存读取",
  input_token_batch: "批量输入",
  output_token_batch: "批量输出",
};

function buildSpecs(model) {
  const pricing = [];
  for (const entry of model.prices ?? []) {
    if (pricing.length >= 3) break;
    const label = PRICE_TYPE_LABEL[entry.type] ?? entry.type;
    pricing.push(`${label} ${entry.price} / ${entry.unit}`);
  }
  return {
    pricing,
    contextWindow: model.contextWindow,
    maxInputTokens: model.maxInputTokens,
    maxOutputTokens: model.maxOutputTokens,
    features: model.features ?? [],
  };
}

const output = {
  gate,
  poolSize: ordered.length,
  candidates: ranked.map(({ model, rank, slot, score }) => ({
    rank,
    slot,
    model: model.model,
    name: model.name,
    provider: model.provider,
    family: model.family,
    tier: model.profile?.familyTier ?? "unknown",
    finalScore: Math.round(score * 1000) / 1000,
    matchedScenes: (intent.matchedScenes ?? []).filter((scene) =>
      (model.profile?.scenes ?? []).includes(scene),
    ),
    specs: buildSpecs(model),
  })),
};

process.stdout.write(JSON.stringify(output, null, 2) + "\n");
