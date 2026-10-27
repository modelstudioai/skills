#!/usr/bin/env node
// get-samples.mjs — 从 groups/<slug>.json 提取指定模型的调用示例代码
//
// 用法：
//   node scripts/get-samples.mjs <model-id> [<model-id>...] [--data <wiki-models-dir>]
//
// 输出 JSON：{ "<model-id>": { "source": "openai|dashscope|fallback",
//   "python": "...", "curl": "...", "docUrl": "..." } }
// 优先 samples.openai，其次 samples.dashscope；两者皆无时基于 OpenAI
// 兼容端点构造最简示例（fallback）。

import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";

const args = process.argv.slice(2);
const dataDirOverrideIndex = args.indexOf("--data");
const dataDir = dataDirOverrideIndex >= 0 ? args[dataDirOverrideIndex + 1] : undefined;
const skipAfter = new Set(dataDirOverrideIndex >= 0 ? [dataDirOverrideIndex, dataDirOverrideIndex + 1] : []);
const modelIds = args.filter((arg, idx) => !skipAfter.has(idx) && !arg.startsWith("--"));

if (modelIds.length === 0) {
  process.stderr.write("用法: node scripts/get-samples.mjs <model-id> [<model-id>...] [--data <wiki-models-dir>]\n");
  process.exit(2);
}

const wikiDir =
  dataDir ??
  (process.env.BAILIAN_CONFIG_DIR
    ? join(process.env.BAILIAN_CONFIG_DIR, "skills", "bailian-docs-llm-wiki", "models")
    : join(homedir(), ".bailian", "skills", "bailian-docs-llm-wiki", "models"));
const modelsPath = join(wikiDir, "models.jsonl");
if (!existsSync(modelsPath)) {
  process.stderr.write(`找不到模型目录数据: ${modelsPath}\n请先安装 bailian-docs-llm-wiki skill。\n`);
  process.exit(1);
}

// model-id → detailPath（去掉可能的前导路径，取文件名 slug）
const detailOf = new Map();
for (const line of readFileSync(modelsPath, "utf-8").split("\n")) {
  if (!line.trim()) continue;
  try {
    const record = JSON.parse(line);
    if (record.model && record.detailPath) {
      detailOf.set(record.model, record.detailPath);
    }
  } catch {
    // 跳过坏行
  }
}

const FALLBACK = {
  python: `from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="<MODEL>",
    messages=[{"role": "user", "content": "你好"}],
)`,
  curl: `curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \\
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{"model": "<MODEL>", "messages": [{"role": "user", "content": "你好"}]}'`,
};

function pickSampleGroup(samples) {
  if (!samples) return null;
  if (samples.openai) return { source: "openai", group: samples.openai };
  if (samples.dashscope) return { source: "dashscope", group: samples.dashscope };
  return null;
}

function pickVariant(group) {
  // 优先 completionsAPI / default，其次任意子键
  const keys = Object.keys(group);
  const preferred = keys.find((key) => key === "completionsAPI" || key === "default");
  const chosen = preferred ?? keys[0];
  const variant = group[chosen];
  return typeof variant === "string" ? { text: variant } : variant;
}

const result = {};
for (const modelId of modelIds) {
  const detailPath = detailOf.get(modelId);
  let entry = structuredFallback(modelId);
  if (detailPath) {
    const groupPath = join(wikiDir, String(detailPath).replace(/^.*models\//, ""));
    const groupFile = existsSync(groupPath) ? groupPath : join(wikiDir, "groups", `${modelId.replace(/-\d{4}-\d{2}-\d{2}$/, "")}.json`);
    if (existsSync(groupFile)) {
      try {
        const group = JSON.parse(readFileSync(groupFile, "utf-8"));
        const item = (group.items ?? []).find((entry) => entry.model === modelId) ?? (group.items ?? [])[0];
        const picked = pickSampleGroup(item?.samples);
        if (picked) {
          const variant = pickVariant(picked.group);
          entry = {
            source: picked.source,
            python: variant?.python,
            curl: variant?.curl,
            docUrl: variant?.docUrl ?? item?.docUrl,
          };
        }
      } catch {
        // 解析失败走 fallback
      }
    }
  }
  result[modelId] = entry;
}

function structuredFallback(modelId) {
  return {
    python: FALLBACK.python.replace("<MODEL>", modelId).replace("from openai import OpenAI", "import os\nfrom openai import OpenAI"),
    curl: FALLBACK.curl.replaceAll("<MODEL>", modelId),
  };
}

process.stdout.write(JSON.stringify(result, null, 2) + "\n");
