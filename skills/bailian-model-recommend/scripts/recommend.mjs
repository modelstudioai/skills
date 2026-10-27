#!/usr/bin/env node
// recommend.mjs — 一键推荐入口：场景预设 → intent → 召回排序 → 内嵌调用示例
//
// 常规路径只需要这一个命令（含示例代码、规格、负面清单、端点提示），
// 拿到输出后直接撰写推荐理由即可，不必再调 recall-rank.mjs / get-samples.mjs。
//
// 用法：
//   node scripts/recommend.mjs --scene code [--exclude qwen] [--top 3] [偏好 flag]
//   node scripts/recommend.mjs --intent intent.json     # 复杂/pipeline 需求走自由 intent
//   node scripts/recommend.mjs --list-scenes            # 列出场景预设与目录场景词
//
// flag：
//   --scene <预设key|场景词>[,...]  可重复或逗号分隔；预设见 SCENE_PRESETS，
//                                   也可直接传目录里的场景词（约束由数据反推）
//   --exclude <needle>[,...]        排除：子串匹配 model id / family / provider / familyName
//   --only <needle>[,...]           限定在某个家族/厂商内选（scoped）
//   --compare <a,b>                 对比点名模型（comparison，保持给定顺序）
//   --alternative-to <model>[,...]  要指定模型的替代品（alternative）
//   --budget low|medium|high        默认 medium
//   --quality flagship|balanced|cost-optimized   默认 balanced
//   --context standard|large|extra-large         默认 standard
//   --optimize price|context|quality|speed       按某维度优化（会改写打分权重）
//   --top <n>                       默认 3
//   --no-samples                    不内嵌示例代码（省 token）
//   --data <wiki-models-dir>
//
// 输出 JSON：{ scene, intent, gate, poolSize, warnings[], endpointNote?, candidates[] }

import { readFileSync } from "node:fs";
import {
  deriveSceneConstraint,
  endpointNoteFor,
  loadCatalog,
  loadSamples,
  resolveDataDir,
  sceneSuggestions,
  sceneVocabulary,
} from "./lib/catalog.mjs";
import { recallRank } from "./lib/engine.mjs";

/**
 * 场景预设：key → 场景词 + 模态 + 能力约束。
 * 约束值全部取自目录实际数据（`profile.scenes` / `inferenceMetadata.*_modality` /
 * `capabilities` 的观测取值），不要凭记忆新增；新增预设前先用
 * `--list-scenes` 或 wiki 数据核对该场景下的真实模态与能力分布。
 */
const SCENE_PRESETS = {
  code: { scenes: ["代码生成"], input: ["Text"], output: ["Text"], caps: ["TG"] },
  agent: { scenes: ["Agent编排", "意图识别"], input: ["Text"], output: ["Text"], caps: ["TG"] },
  chat: { scenes: ["客服对话", "知识问答"], input: ["Text"], output: ["Text"], caps: ["TG"] },
  research: { scenes: ["深度研究", "数学推理"], input: ["Text"], output: ["Text"], caps: ["Reasoning", "TG"] },
  writing: { scenes: ["创意写作", "角色扮演"], input: ["Text"], output: ["Text"], caps: ["TG"] },
  translate: { scenes: ["翻译"], input: ["Text"], output: ["Text"], caps: ["TR", "TG"] },
  doc: { scenes: ["文档理解", "OCR文字识别"], input: ["Image", "Text"], output: ["Text"], caps: ["VU"] },
  analytics: { scenes: ["数据分析"], input: ["Text", "Image"], output: ["Text"], caps: ["TG", "VU"] },
  education: { scenes: ["教育辅导"], input: ["Text", "Image"], output: ["Text"], caps: ["TG", "VU"] },
  sentiment: { scenes: ["情感分析"], input: ["Text", "Audio"], output: ["Text"], caps: ["TG"] },
  rag: { scenes: ["向量检索", "语义重排"], input: ["Text"], output: ["Text"], caps: ["ME", "TR"] },
  image: { scenes: ["图像生成"], input: ["Text", "Image"], output: ["Image"], caps: ["IG"] },
  "image-edit": { scenes: ["图像编辑", "图像修复"], input: ["Image", "Text"], output: ["Image"], caps: ["IG"] },
  portrait: { scenes: ["人脸人像", "虚拟试穿"], input: ["Image", "Text"], output: ["Image"], caps: ["IG"] },
  marketing: { scenes: ["电商营销"], input: ["Text", "Image"], output: ["Text", "Image", "Video"], caps: ["TG", "IG"] },
  video: { scenes: ["视频生成"], input: ["Text", "Image"], output: ["Video"], caps: ["VG", "World-Model"] },
  "video-edit": { scenes: ["视频编辑"], input: ["Video", "Image"], output: ["Video"], caps: ["VG"] },
  "3d": { scenes: ["3D生成"], input: ["Text", "Image"], output: ["3D-Generation", "Video"], caps: ["3D-generation", "World-Model"] },
  tts: { scenes: ["语音合成", "有声书", "播客"], input: ["Text"], output: ["Audio"], caps: ["TTS"] },
  asr: { scenes: ["语音识别"], input: ["Audio"], output: ["Text"], caps: ["ASR", "Realtime-ASR"] },
  music: { scenes: ["音乐生成"], input: ["Text", "Audio"], output: ["Audio"], caps: ["TTS"] },
  realtime: {
    scenes: ["实时对话", "数字人"],
    input: ["Audio", "Text"],
    output: ["Audio", "Text"],
    caps: ["Realtime-Omni", "Realtime-Chatting", "Realtime-Text-to-Speech", "Realtime-ASR", "Realtime-Audio-Translate"],
  },
  omni: {
    scenes: ["实时对话", "Agent编排"],
    input: ["Text", "Image", "Audio", "Video"],
    output: ["Text", "Audio"],
    caps: ["Multimodal-Omni", "Realtime-Omni"],
  },
};

const BUDGETS = new Set(["low", "medium", "high"]);
const QUALITIES = new Set(["flagship", "balanced", "cost-optimized"]);
const CONTEXT_NEEDS = new Set(["standard", "large", "extra-large"]);
const OPTIMIZE_DIMENSIONS = new Set(["price", "context", "quality", "speed"]);

// ---- CLI 参数 ----

const args = process.argv.slice(2);
const listAll = (name) => {
  const values = [];
  for (let index = 0; index < args.length; index += 1) {
    if (args[index] !== `--${name}`) continue;
    const raw = args[index + 1];
    if (raw === undefined) continue;
    values.push(...raw.split(",").map((part) => part.trim()).filter(Boolean));
    index += 1;
  }
  return values;
};
const flagValue = (name) => {
  const idx = args.indexOf(`--${name}`);
  return idx >= 0 ? args[idx + 1] : undefined;
};
const hasFlag = (name) => args.includes(`--${name}`);

const dataDir = resolveDataDir(flagValue("data"));

let catalog;
try {
  catalog = loadCatalog(dataDir);
} catch (error) {
  process.stderr.write(`${error.message}\n`);
  process.exit(1);
}

const vocabulary = sceneVocabulary(catalog.models);

if (hasFlag("list-scenes")) {
  process.stdout.write(
    JSON.stringify(
      {
        presets: Object.fromEntries(
          Object.entries(SCENE_PRESETS).map(([key, preset]) => [
            key,
            { scenes: preset.scenes, inputModality: preset.input, outputModality: preset.output, requiredCapabilities: preset.caps },
          ]),
        ),
        catalogScenes: vocabulary,
        note: "--scene 也可以直接传 catalogScenes 里的任意场景词，模态/能力约束由数据反推（多数票）。",
      },
      null,
      2,
    ) + "\n",
  );
  process.exit(0);
}

const USAGE =
  "用法: node scripts/recommend.mjs --scene <预设|场景词>[,...] [--exclude qwen] [--top 3]\n" +
  "      node scripts/recommend.mjs --intent <intent.json|->\n" +
  "      node scripts/recommend.mjs --list-scenes\n";

// ---- intent 构建 ----

let intent;
let sceneLabel;

const intentSource = flagValue("intent");
if (intentSource) {
  intent = JSON.parse(intentSource === "-" ? readFileSync(0, "utf-8") : readFileSync(intentSource, "utf-8"));
  sceneLabel = intentSource === "-" ? "stdin" : intentSource;
} else {
  const excludes = listAll("exclude");
  const onlyTargets = listAll("only");
  const compareTargets = listAll("compare");
  const alternativeTargets = listAll("alternative-to");
  const sceneTokens = listAll("scene");
  const hasNamedTarget = compareTargets.length + alternativeTargets.length + onlyTargets.length > 0;

  if (sceneTokens.length === 0 && !hasNamedTarget) {
    process.stderr.write(
      `${USAGE}\n缺少 --scene（点名模型可只用 --compare / --alternative-to / --only；复杂需求改用 --intent）。\n` +
        `可用预设: ${Object.keys(SCENE_PRESETS).join(", ")}\n目录场景词: ${vocabulary.join("、")}\n`,
    );
    process.exit(2);
  }

  const merged = { scenes: [], input: [], output: [], caps: [] };
  const derived = [];
  for (const token of sceneTokens) {
    const preset = SCENE_PRESETS[token];
    if (preset) {
      merged.scenes.push(...preset.scenes);
      merged.input.push(...preset.input);
      merged.output.push(...preset.output);
      merged.caps.push(...preset.caps);
      continue;
    }
    if (vocabulary.includes(token)) {
      const constraint = deriveSceneConstraint(token, catalog.models);
      merged.scenes.push(...constraint.matchedScenes);
      merged.input.push(...constraint.inputModality);
      merged.output.push(...constraint.outputModality);
      merged.caps.push(...constraint.requiredCapabilities);
      derived.push(token);
      continue;
    }
    const suggestions = sceneSuggestions([token], vocabulary);
    process.stderr.write(
      `未知场景: ${token}\n可用预设: ${Object.keys(SCENE_PRESETS).join(", ")}\n` +
        `目录场景词: ${vocabulary.join("、")}\n` +
        (suggestions.length > 0 ? `最近似: ${suggestions.join("、")}\n` : ""),
    );
    process.exit(2);
  }

  const budget = flagValue("budget") ?? "medium";
  const quality = flagValue("quality") ?? "balanced";
  const contextNeed = flagValue("context") ?? "standard";
  const optimizeDimension = flagValue("optimize");
  for (const [flagName, value, allowed] of [
    ["budget", budget, BUDGETS],
    ["quality", quality, QUALITIES],
    ["context", contextNeed, CONTEXT_NEEDS],
  ]) {
    if (!allowed.has(value)) {
      process.stderr.write(`--${flagName} 取值非法: ${value}（可用: ${[...allowed].join(" | ")}）\n`);
      process.exit(2);
    }
  }
  if (optimizeDimension !== undefined && !OPTIMIZE_DIMENSIONS.has(optimizeDimension)) {
    process.stderr.write(`--optimize 取值非法: ${optimizeDimension}（可用: ${[...OPTIMIZE_DIMENSIONS].join(" | ")}）\n`);
    process.exit(2);
  }

  let modelPreference = { mode: "unconstrained" };
  if (compareTargets.length > 0) modelPreference = { mode: "comparison", targets: compareTargets };
  else if (alternativeTargets.length > 0) modelPreference = { mode: "alternative", targets: alternativeTargets };
  else if (onlyTargets.length > 0) modelPreference = { mode: "scoped", targets: onlyTargets };
  if (excludes.length > 0) modelPreference = { ...modelPreference, excludes };

  intent = {
    complexity: "single",
    inputModality: [...new Set(merged.input)],
    outputModality: [...new Set(merged.output)],
    requiredCapabilities: [...new Set(merged.caps)],
    requiredFeatures: [],
    matchedScenes: [...new Set(merged.scenes)],
    budget,
    contextNeed,
    qualityPreference: quality,
    userIntent: optimizeDimension ? "optimize" : "match",
    ...(optimizeDimension ? { optimizeDimension } : {}),
    modelPreference,
  };
  sceneLabel =
    sceneTokens.length > 0
      ? sceneTokens.join(",") + (derived.length > 0 ? `（${derived.join("/")} 由数据反推约束）` : "")
      : `点名模型（${modelPreference.mode}）`;
}

const topN = Number.parseInt(flagValue("top") ?? "3", 10);
if (!topN) {
  process.stderr.write(USAGE);
  process.exit(2);
}

// ---- 召回 + 排序 + 示例 ----

const { gate, poolSize, candidates, warnings, intent: resolvedIntent } = recallRank({
  intent,
  models: catalog.models,
  topN,
  suggestScenes: sceneSuggestions,
});

const output = { scene: sceneLabel, intent: resolvedIntent, gate, poolSize, warnings };

if (!hasFlag("no-samples") && candidates.length > 0) {
  const samplesById = loadSamples({
    dataDir: catalog.dataDir,
    models: catalog.models,
    modelIds: candidates.map((candidate) => candidate.model),
  });
  for (const candidate of candidates) candidate.samples = samplesById[candidate.model];
  const endpointNote = endpointNoteFor(samplesById);
  if (endpointNote) output.endpointNote = endpointNote;
}

output.candidates = candidates;
process.stdout.write(JSON.stringify(output, null, 2) + "\n");

for (const warning of warnings) process.stderr.write(`[warn] ${warning.code}: ${warning.message}\n`);
