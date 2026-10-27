#!/usr/bin/env node
// get-samples.mjs — 从 groups/<slug>.json 提取指定模型的调用示例代码
//
// 用法：
//   node scripts/get-samples.mjs <model-id> [<model-id>...] [--data <wiki-models-dir>]
//
// 输出 JSON（stdout）：{ "<model-id>": { "source": "openai|dashscope|fallback",
//   "python": "...", "curl": "...", "docUrl": "..." } }
// 优先 samples.openai，其次 samples.dashscope；两者皆无时基于 OpenAI 兼容端点
// 构造最简示例（source=fallback）。
//
// 若示例 base_url 含 Workspace ID 占位符，会在 stderr 打印一条替换提示
// （stdout 结构保持不变，便于脚本消费）。
//
// 推荐流程里通常不需要单独调用本脚本：recommend.mjs / recall-rank.mjs
// --with-samples 已经把示例内嵌进候选。本脚本用于「用户已确定模型，只要代码」。

import { endpointNoteFor, loadCatalog, loadSamples, resolveDataDir } from "./lib/catalog.mjs";

const args = process.argv.slice(2);
const dataDirFlagIndex = args.indexOf("--data");
const dataDirOverride = dataDirFlagIndex >= 0 ? args[dataDirFlagIndex + 1] : undefined;
const skipIndexes = new Set(dataDirFlagIndex >= 0 ? [dataDirFlagIndex, dataDirFlagIndex + 1] : []);
const modelIds = args.filter((arg, idx) => !skipIndexes.has(idx) && !arg.startsWith("--"));

if (modelIds.length === 0) {
  process.stderr.write("用法: node scripts/get-samples.mjs <model-id> [<model-id>...] [--data <wiki-models-dir>]\n");
  process.exit(2);
}

const dataDir = resolveDataDir(dataDirOverride);

let catalog;
try {
  catalog = loadCatalog(dataDir);
} catch (error) {
  process.stderr.write(`${error.message}\n`);
  process.exit(1);
}

const samples = loadSamples({ dataDir: catalog.dataDir, models: catalog.models, modelIds });
process.stdout.write(JSON.stringify(samples, null, 2) + "\n");

const endpointNote = endpointNoteFor(samples);
if (endpointNote) process.stderr.write(`[note] ${endpointNote}\n`);
