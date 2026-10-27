#!/usr/bin/env node
// recall-rank.mjs — 确定性召回+打分+排序+席位分配（CLI 壳）
//
// 引擎在 lib/engine.mjs（移植自 bailian-cli `packages/core/src/advisor/engine/`），
// 数据层在 lib/catalog.mjs。LLM 只负责把用户需求转成 intent JSON 传进来，
// 以及在拿到输出后撰写推荐理由——排序与筛选全程无 LLM 参与。
//
// 用法：
//   node scripts/recall-rank.mjs <intent.json> [--top 3] [--with-samples] [--data <wiki-models-dir>]
//   cat intent.json | node scripts/recall-rank.mjs -                 # stdin
//
// intent.json 结构见 references/requirement-schema.md。输出 JSON：
//   { gate, poolSize, warnings[], endpointNote?, candidates[] }
//   candidates[] 含 rank/slot/model/name/provider/family/familyName/tier/
//   finalScore/matchedScenes/oneLinePositioning/capabilities/callModes/
//   notSuitableFor/pipelineRole/docUrl/specs，--with-samples 时再附 samples。
//
// 常规路径请优先用 scripts/recommend.mjs（一次调用即含 samples 与场景预设）。

import { readFileSync } from "node:fs";
import { endpointNoteFor, loadCatalog, loadSamples, resolveDataDir, sceneSuggestions } from "./lib/catalog.mjs";
import { recallRank } from "./lib/engine.mjs";

const args = process.argv.slice(2);
const intentArg = args[0];
const flagValue = (name) => {
  const idx = args.indexOf(`--${name}`);
  return idx >= 0 ? args[idx + 1] : undefined;
};
const hasFlag = (name) => args.includes(`--${name}`);
const topN = Number.parseInt(flagValue("top") ?? "3", 10);
const withSamples = hasFlag("with-samples");
const dataDir = resolveDataDir(flagValue("data"));

if (!intentArg || !topN) {
  process.stderr.write(
    "用法: node scripts/recall-rank.mjs <intent.json|-> [--top 3] [--with-samples] [--data <wiki-models-dir>]\n" +
      "  intent.json 结构见 references/requirement-schema.md；传 - 从 stdin 读\n" +
      "  常规路径建议改用 node scripts/recommend.mjs --scene <预设>\n",
  );
  process.exit(2);
}

const intent = JSON.parse(intentArg === "-" ? readFileSync(0, "utf-8") : readFileSync(intentArg, "utf-8"));

let catalog;
try {
  catalog = loadCatalog(dataDir);
} catch (error) {
  process.stderr.write(`${error.message}\n`);
  process.exit(1);
}

const { gate, poolSize, candidates, warnings } = recallRank({
  intent,
  models: catalog.models,
  topN,
  suggestScenes: sceneSuggestions,
});

const output = { gate, poolSize, warnings };

if (withSamples && candidates.length > 0) {
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
