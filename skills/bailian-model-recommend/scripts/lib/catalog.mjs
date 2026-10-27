// catalog.mjs — 模型目录数据层：定位数据目录、加载 models.jsonl、场景词表、
// 调用示例提取。recall-rank.mjs / get-samples.mjs / recommend.mjs 共用，
// 保证三者读到的目录数据完全一致。
//
// 纯 I/O + 纯函数，不做任何排序决策（决策在 engine.mjs）。

import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";

/** 日期快照版本后缀：`-YYYY-MM-DD` 或 `-MMDD`。 */
export const SNAPSHOT_DATE_RE = /(-\d{4}-\d{2}-\d{2}|-\d{4})$/;

/** 示例 base_url 里的 Workspace ID 占位符（两种历史写法都要认）。 */
export const ENDPOINT_PLACEHOLDER_RE = /\[workspace-id\]|\{WorkspaceId\}/i;

const INSTALL_HINT =
  "请先安装 bailian-docs-llm-wiki skill：npx skills add modelstudioai/skills --skill bailian-docs-llm-wiki -y";

/** 解析模型数据目录：显式 --data > BAILIAN_CONFIG_DIR > ~/.bailian。 */
export function resolveDataDir(override) {
  if (override) return override;
  return process.env.BAILIAN_CONFIG_DIR
    ? join(process.env.BAILIAN_CONFIG_DIR, "skills", "bailian-docs-llm-wiki", "models")
    : join(homedir(), ".bailian", "skills", "bailian-docs-llm-wiki", "models");
}

export function readJsonl(filePath) {
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

/**
 * 加载目录数据并做快照去重（保留主版本；主版本缺失时才保留日期快照）。
 * 数据缺失时抛 CATALOG_MISSING，由 CLI 层转成退出码。
 */
export function loadCatalog(dataDir) {
  const modelsPath = join(dataDir, "models.jsonl");
  if (!existsSync(modelsPath)) {
    const error = new Error(`找不到模型目录数据: ${modelsPath}\n${INSTALL_HINT}`);
    error.code = "CATALOG_MISSING";
    throw error;
  }
  const rawModels = readJsonl(modelsPath);
  const mainModels = new Set(rawModels.map(({ model }) => model));
  const models = rawModels.filter(({ model }) => {
    const base = model.replace(SNAPSHOT_DATE_RE, "");
    return base === model || !mainModels.has(base);
  });
  return { dataDir, modelsPath, models };
}

/** 目录里实际存在的场景词全集（`profile.scenes`），已排序去重。 */
export function sceneVocabulary(models) {
  const scenes = new Set();
  for (const model of models) {
    for (const scene of model.profile?.scenes ?? []) scenes.add(scene);
  }
  return [...scenes].sort();
}

/**
 * 为写错/过期的场景词给出最近似的候选：双向子串包含优先，其次按共同汉字数排序。
 * 只用于报错提示，不参与任何打分。
 */
export function sceneSuggestions(requestedScenes, vocabulary, limit = 6) {
  const sharedCharacters = (left, right) => {
    const rightChars = new Set(right);
    return [...left].filter((char) => rightChars.has(char)).length;
  };
  const scored = vocabulary.map((scene) => {
    let score = 0;
    for (const requested of requestedScenes) {
      if (scene.includes(requested) || requested.includes(scene)) score += 10;
      score += sharedCharacters(requested, scene);
    }
    return { scene, score };
  });
  return scored
    .filter((entry) => entry.score > 0)
    .sort((left, right) => right.score - left.score || left.scene.localeCompare(right.scene, "zh-Hans-CN"))
    .slice(0, limit)
    .map((entry) => entry.scene);
}

const majorityVote = (values) => {
  const counts = new Map();
  for (const value of values) counts.set(value, (counts.get(value) ?? 0) + 1);
  return [...counts.entries()].sort(
    (left, right) => right[1] - left[1] || left[0].localeCompare(right[0]),
  );
};

/**
 * 从数据反推某个场景词的模态/能力约束（多数票），供 `--scene <场景词>` 直传时使用。
 * 目的是不让场景→约束的映射写死在代码里：目录漂移时约束自动跟随。
 * - 模态取出现次数最多的一个（并列取字典序首个，保证确定性）
 * - 能力取出现率 >= 50% 的（至少保留一个最高频能力，避免空约束退化成全池）
 */
export function deriveSceneConstraint(scene, models) {
  const matched = models.filter((model) => (model.profile?.scenes ?? []).includes(scene));
  if (matched.length === 0) return null;
  const inputVotes = majorityVote(matched.flatMap((model) => model.inferenceMetadata?.request_modality ?? []));
  const outputVotes = majorityVote(matched.flatMap((model) => model.inferenceMetadata?.response_modality ?? []));
  const capabilityVotes = majorityVote(matched.flatMap((model) => model.capabilities ?? []));
  const threshold = matched.length / 2;
  const capabilities = capabilityVotes.filter(([, count]) => count >= threshold).map(([capability]) => capability);
  return {
    matchedScenes: [scene],
    inputModality: inputVotes.length > 0 ? [inputVotes[0][0]] : [],
    outputModality: outputVotes.length > 0 ? [outputVotes[0][0]] : [],
    requiredCapabilities: capabilities.length > 0 ? capabilities : capabilityVotes.slice(0, 1).map(([capability]) => capability),
  };
}

// ---- 调用示例（原 get-samples.mjs 逻辑，抽出共用）----

const FALLBACK_SAMPLE = {
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

function structuredFallback(modelId) {
  return {
    source: "fallback",
    python: FALLBACK_SAMPLE.python.replace("<MODEL>", modelId).replace("from openai import OpenAI", "import os\nfrom openai import OpenAI"),
    curl: FALLBACK_SAMPLE.curl.replaceAll("<MODEL>", modelId),
  };
}

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
  const variant = group[preferred ?? keys[0]];
  return typeof variant === "string" ? { text: variant } : variant;
}

/**
 * 提取一批模型的调用示例。优先 samples.openai，其次 samples.dashscope，
 * 都没有时构造最简 OpenAI 兼容示例（source=fallback）。
 */
export function loadSamples({ dataDir, models, modelIds }) {
  const detailOf = new Map();
  for (const model of models) {
    if (model.model && model.detailPath) detailOf.set(model.model, model.detailPath);
  }

  const result = {};
  for (const modelId of modelIds) {
    const detailPath = detailOf.get(modelId);
    let entry = structuredFallback(modelId);
    if (detailPath) {
      const groupPath = join(dataDir, String(detailPath).replace(/^.*models\//, ""));
      const fallbackPath = join(dataDir, "groups", `${modelId.replace(/-\d{4}-\d{2}-\d{2}$/, "")}.json`);
      const groupFile = existsSync(groupPath) ? groupPath : fallbackPath;
      if (existsSync(groupFile)) {
        try {
          const group = JSON.parse(readFileSync(groupFile, "utf-8"));
          const item = (group.items ?? []).find((candidate) => candidate.model === modelId) ?? (group.items ?? [])[0];
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
    if (!entry.docUrl) {
      const catalogDocUrl = models.find((model) => model.model === modelId)?.docUrl;
      if (catalogDocUrl) entry.docUrl = catalogDocUrl;
    }
    result[modelId] = entry;
  }
  return result;
}

/**
 * 示例里的 base_url 含 Workspace ID 占位符时，给出必须替换的标准提示。
 * 依据：wiki/guides/use-chat-client-or-development-tool.md —— 按量计费 URL 中
 * `{WorkspaceId}` 需替换为真实 ID，且必须与 API Key、地域严格匹配。
 */
export function endpointNoteFor(samplesById) {
  const hasPlaceholder = Object.values(samplesById).some((sample) =>
    ENDPOINT_PLACEHOLDER_RE.test(`${sample.python ?? ""}\n${sample.curl ?? ""}`),
  );
  if (!hasPlaceholder) return undefined;
  return (
    "示例 base_url 含 [workspace-id] 占位符（按量计费端点）：必须替换为真实 Workspace ID，" +
    "并与 API Key、地域严格匹配；获取方式见 https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain"
  );
}
