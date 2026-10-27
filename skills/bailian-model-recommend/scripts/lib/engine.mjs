// engine.mjs — 确定性召回 + 打分 + 排序 + fairness + 席位分配。
//
// 移植自 bailian-cli `packages/core/src/advisor/engine/`（recall/hard-filter、
// score formula、rank、fairness）。纯函数：入参只有 intent / models / topN，
// 不读盘、不写盘、不调 LLM。CLI 层（recall-rank.mjs / recommend.mjs）负责 I/O。
//
// 输出结构与 SKILL.md「脚本输出」一节保持一致；候选字段为理由撰写做了富化
// （oneLinePositioning / notSuitableFor / capabilities / callModes / pipelineRole），
// 目的是让 LLM 不必回读 models.jsonl。

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

// ---- 公式打分常量（score/index.ts 移植）----

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

// ---- 排序常量（recall/index.ts byTierThenPrice 移植）----

const TIER_ORDER = { flagship: 0, balanced: 1, lightweight: 2 };
const ALIBABA_PROVIDERS = new Set(["qwen", "qwen-domain-model", "wan"]);
const generationOf = (model) => {
  const match = model.model.match(/(\d+(?:\.\d+)?)/);
  return match ? Number.parseFloat(match[1]) : Number.NEGATIVE_INFINITY;
};

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

const SLOTS = ["primary", "runner-up", "exploration"];

// ---- intent 字段名校验 ----
// 写错的键会被 `?? []` 静默忽略：模态过滤失效 → 排序退化成"旗舰/贵的优先"，
// 且不报错。目录里模型侧的模态字段叫 inferenceMetadata.request_modality，
// 所以调用方（尤其手写 intent 的 LLM）很容易误写成 requestModality。
// 无歧义的别名直接归一化并如实回报；其余未知键只警告，不猜测语义。

const KNOWN_INTENT_KEYS = [
  "complexity",
  "inputModality",
  "outputModality",
  "requiredCapabilities",
  "requiredFeatures",
  "matchedScenes",
  "scenarioHints",
  "budget",
  "contextNeed",
  "qualityPreference",
  "userIntent",
  "optimizeDimension",
  "modelPreference",
  "segments",
];

const INTENT_KEY_ALIASES = {
  requestModality: "inputModality",
  responseModality: "outputModality",
  request_modality: "inputModality",
  response_modality: "outputModality",
  input_modality: "inputModality",
  output_modality: "outputModality",
};

function normalizeIntentKeys(rawIntent) {
  const intent = { ...(rawIntent ?? {}) };
  const warnings = [];
  const renamed = [];
  const unknownKeys = [];

  for (const key of Object.keys(intent)) {
    if (KNOWN_INTENT_KEYS.includes(key)) continue;
    const canonical = INTENT_KEY_ALIASES[key];
    if (canonical) {
      if (intent[canonical] === undefined) intent[canonical] = intent[key];
      delete intent[key];
      renamed.push(`${key} → ${canonical}`);
    } else {
      unknownKeys.push(key);
    }
  }

  if (renamed.length > 0) {
    warnings.push({
      code: "intent-key-normalized",
      message:
        `intent 字段名 ${renamed.join("、")} 已自动归一化（目录里 request_modality 是模型侧字段，intent 侧用 inputModality/outputModality）。`,
      renamed,
    });
  }
  if (unknownKeys.length > 0) {
    warnings.push({
      code: "unknown-intent-keys",
      message:
        `intent 含未识别字段 ${JSON.stringify(unknownKeys)}，引擎已忽略（不参与过滤与打分）。` +
        `可用字段：${KNOWN_INTENT_KEYS.join(" / ")}。`,
      unknownKeys,
      knownKeys: KNOWN_INTENT_KEYS,
    });
  }
  return { intent, warnings };
}

/**
 * @param {object} params
 * @param {object} params.intent      需求提取 JSON（结构见 references/requirement-schema.md）
 * @param {object[]} params.models    已做快照去重的目录数据（catalog.loadCatalog().models）
 * @param {number} params.topN        输出候选数（默认 3）
 * @param {(scene:string, models:object[])=>string[]} [params.suggestScenes] 场景词纠错建议（可选注入，避免 engine 依赖 catalog）
 * @returns {{gate:string, poolSize:number, candidates:object[], warnings:object[], intent:object}} intent 为字段名归一化后的版本
 */
export function recallRank({ intent: rawIntent, models, topN = 3, suggestScenes }) {
  const { intent, warnings: intentWarnings } = normalizeIntentKeys(rawIntent);
  const allModels = models;

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

  // ---- 公式打分 ----

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

  // ---- 排序 ----

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

  const warnings = [...intentWarnings];
  const pref = intent.modelPreference ?? { mode: "unconstrained" };
  let pool = allModels.filter(isAvailable);

  // excludes 统一过滤：子串匹配 model id / family / provider / familyName
  // （所以 "qwen" 会连带排除 provider=qwen-domain-model 与 id 含 qwen 的模型）
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

  // 场景词校验：填了但目录里没人认领 → 回报可用词表，而不是静默按 0 分排
  const requestedScenes = intent.matchedScenes ?? [];
  if (requestedScenes.length > 0) {
    const sceneHit = pool.some((model) => (model.profile?.scenes ?? []).some((scene) => requestedScenes.includes(scene)));
    if (!sceneHit) {
      const vocabulary = sceneVocabularyOf(pool);
      const poolLabel = (pref.excludes ?? []).length > 0 ? `已应用 excludes 后的 ${pool.length} 个模型` : `${pool.length} 个可用模型`;
      warnings.push({
        code: "scene-no-match",
        message:
          `matchedScenes ${JSON.stringify(requestedScenes)} 在当前目录（${poolLabel}）中无任何匹配，` +
          "场景维度会全部按 0 分计算，排序结果不可信。请改用 availableScenes 中的词重跑。",
        requestedScenes,
        availableScenes: vocabulary,
        suggestions: suggestScenes ? suggestScenes(requestedScenes, vocabulary) : [],
      });
    }
  }

  // 能力/模态词校验：填了目录里不存在的代码 → 硬门形同虚设。
  // 尤其能力：无任何模型匹配时 filterWithFallback 会回退全池，模态约束一起失效，
  // 排序悄悄退化成"旗舰/贵的优先"。必须显式回报，不能静默。
  const requestedCapabilities = intent.requiredCapabilities ?? [];
  if (requestedCapabilities.length > 0) {
    const catalogCapabilities = new Set(pool.flatMap((model) => model.capabilities ?? []));
    const unknownCapabilities = requestedCapabilities.filter((capability) => !catalogCapabilities.has(capability));
    if (unknownCapabilities.length > 0) {
      warnings.push({
        code: "capability-no-match",
        message:
          `requiredCapabilities ${JSON.stringify(unknownCapabilities)} 在目录中不存在（能力代码是 TG/VU/IG 这类缩写，` +
          "不是 Text-Generation 这类全称）。无任何模型匹配能力时会回退全池、模态约束一并失效，排序不可信。" +
          "请改用 availableCapabilities 里的代码重跑。",
        unknownCapabilities,
        availableCapabilities: [...catalogCapabilities].sort(),
      });
    }
  }

  const requestedInput = intent.inputModality ?? [];
  const requestedOutput = intent.outputModality ?? [];
  if (requestedInput.length > 0 || requestedOutput.length > 0) {
    const catalogInput = new Set(pool.flatMap((model) => model.inferenceMetadata?.request_modality ?? []));
    const catalogOutput = new Set(pool.flatMap((model) => model.inferenceMetadata?.response_modality ?? []));
    const unknownInput = requestedInput.filter((modality) => !catalogInput.has(modality));
    const unknownOutput = requestedOutput.filter((modality) => !catalogOutput.has(modality));
    if (unknownInput.length > 0 || unknownOutput.length > 0) {
      warnings.push({
        code: "modality-no-match",
        message:
          `模态取值 ${JSON.stringify([...unknownInput, ...unknownOutput])} 在目录中不存在（大小写敏感，如 Text 不是 text）。` +
          "该侧模态约束不会生效，排序不可信。请改用 available* 里的取值重跑。",
        unknownInputModality: unknownInput,
        unknownOutputModality: unknownOutput,
        availableInputModality: [...catalogInput].sort(),
        availableOutputModality: [...catalogOutput].sort(),
      });
    }
  }

  // pipeline 校验：约束只写在 segments 里 → 顶层为空 → 硬过滤形同虚设。
  // 这是最隐蔽的一种失效：零报错、输出看着正常，但选出的模型不属于任何一段。
  const segments = intent.segments ?? [];
  const hasTopLevelConstraint =
    (intent.inputModality ?? []).length > 0 ||
    (intent.outputModality ?? []).length > 0 ||
    (intent.requiredCapabilities ?? []).length > 0;
  if (segments.length > 1 && !hasTopLevelConstraint) {
    warnings.push({
      code: "pipeline-not-ranked",
      message:
        `intent 是 ${segments.length} 段的 pipeline，但模态/能力只写在 segments 里、顶层为空。` +
        "segments 不参与排序，此时硬过滤完全不生效，只剩场景词打分，选不出任何一段的模型。" +
        '请把每段的约束提到顶层各跑一次（见 SKILL.md「pipeline：每段各跑一次，但合并进一条命令」）。',
      segmentSteps: segments.map((segment) => segment?.step ?? null),
    });
  }

  let gate = "structured";
  let scored;

  if (pref.mode === "comparison" || pref.mode === "alternative") {
    // 用户点名模型（comparison：只返回点名集；alternative：点名+补齐）
    const forced = resolveTargetedModels(pool, pref.targets ?? []);
    const matchedIds = forced.map((model) => model.model.toLowerCase());
    const missingTargets = (pref.targets ?? []).filter(
      (target) => !matchedIds.some((id) => id.includes(target.toLowerCase())),
    );
    if (missingTargets.length > 0) {
      warnings.push({
        code: "target-not-found",
        message: `点名模型 ${JSON.stringify(missingTargets)} 在目录中不存在（或已被 excludes 排除），请如实告知用户。`,
        targets: missingTargets,
      });
    }
    if (pref.mode === "comparison" && forced.length > 0) {
      // 点名集保持用户顺序（forced-order 语义），不做 fairness 重排。
      // target 是子串匹配，一个 target 可能命中多个版本；按 target 分组后轮转排布，
      // 组内精确命中（model id 或 family 全等）优先、其余按分数降序，
      // 保证每个点名模型都先以用户点名的那个版本出现，不会被变体挤出 topN。
      const order = (pref.targets ?? []).map((t) => t.toLowerCase());
      const targetIndexOf = (model) =>
        order.findIndex(
          (t) => model.model.toLowerCase().includes(t) || (model.family ?? "").toLowerCase().includes(t),
        );
      const scoredForced = formulaScore(forced);
      const isExactTarget = (model) => {
        const id = model.model.toLowerCase();
        const family = (model.family ?? "").toLowerCase();
        return order.some((target) => id === target || family === target) ? 0 : 1;
      };
      const bucketsByTarget = new Map();
      for (const cand of scoredForced) {
        const targetIndex = targetIndexOf(cand.model);
        const bucket = bucketsByTarget.get(targetIndex) ?? [];
        bucket.push(cand);
        bucketsByTarget.set(targetIndex, bucket);
      }
      const buckets = [...bucketsByTarget.entries()]
        .sort((left, right) => left[0] - right[0])
        .map(([, bucket]) =>
          bucket.sort(
            (left, right) => isExactTarget(left.model) - isExactTarget(right.model) || right.score - left.score,
          ),
        );
      const interleaved = [];
      for (let round = 0; ; round += 1) {
        const pickedThisRound = buckets.map((bucket) => bucket[round]).filter(Boolean);
        if (pickedThisRound.length === 0) break;
        interleaved.push(...pickedThisRound);
      }
      scored = interleaved.map((cand, idx) => ({ ...cand, forcedIdx: idx }));
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
    // scoped：限定在用户点名的家族/厂商内选（此前 targets 在 structured 路径被静默忽略）
    if (pref.mode === "scoped" && (pref.targets ?? []).length > 0) {
      const scopedPool = resolveTargetedModels(pool, pref.targets);
      if (scopedPool.length > 0) {
        pool = scopedPool;
      } else {
        warnings.push({
          code: "target-not-found",
          message:
            `scoped 点名 ${JSON.stringify(pref.targets)} 在目录中不存在（或已被 excludes 排除），` +
            "已回退到全池排序，请如实告知用户。",
          targets: pref.targets,
        });
      }
    }
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

  const candidates = ranked.map(({ model, rank, slot, score }) => ({
    rank,
    slot,
    model: model.model,
    name: model.name,
    provider: model.provider,
    family: model.family,
    familyName: model.familyName,
    tier: model.profile?.familyTier ?? "unknown",
    finalScore: Math.round(score * 1000) / 1000,
    matchedScenes: requestedScenes.filter((scene) => (model.profile?.scenes ?? []).includes(scene)),
    // 以下为理由撰写富化字段：有了它们就不必回读 models.jsonl
    oneLinePositioning: model.profile?.oneLinePositioning,
    capabilities: model.capabilities ?? [],
    callModes: model.profile?.callModes ?? [],
    notSuitableFor: model.profile?.notSuitableFor ?? [],
    pipelineRole: model.profile?.pipelineRole ?? [],
    docUrl: model.docUrl,
    specs: buildSpecs(model),
  }));

  if (candidates.length === 0) {
    warnings.push({
      code: "empty-candidates",
      message:
        "候选为空。优先检查 inputModality/outputModality/requiredCapabilities 是否填错（模态词大小写敏感，" +
        "取值见 SKILL.md 模态表）；确认无误再告知用户无匹配。",
    });
  }

  return { gate, poolSize: ordered.length, candidates, warnings, intent };
}

/** 场景词全集（engine 内部用，避免依赖 catalog.mjs）。 */
function sceneVocabularyOf(models) {
  const scenes = new Set();
  for (const model of models) {
    for (const scene of model.profile?.scenes ?? []) scenes.add(scene);
  }
  return [...scenes].sort();
}
