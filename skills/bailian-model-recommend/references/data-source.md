# 数据来源

所有模型信息来自 `bailian-docs-llm-wiki` skill 的 `models/` 目录。

定位顺序：`--data <dir>` > `$BAILIAN_CONFIG_DIR/skills/bailian-docs-llm-wiki/models` > `~/.bailian/skills/bailian-docs-llm-wiki/models`。
数据缺失时脚本以退出码 1 报错并打印安装命令。

## 文件说明

| 文件 | 用途 | 谁读 |
| --- | --- | --- |
| `models/models.jsonl` | 主数据源，每行一个模型 | engine + samples |
| `models/families.jsonl` | 家族信息 | 当前脚本未读（家族维度用 models.jsonl 的 family/familyName） |
| `models/groups/<slug>.json` | 模型详情，含 description（语义匹配）与 samples（调用示例） | 仅取 samples 时按需读 |

脚本会先做**快照去重**：模型名带 `-YYYY-MM-DD` / `-MMDD` 后缀且主版本存在时，丢弃快照版本。

## models.jsonl 字段

顶层：

- `model` — 模型 API 调用名（如 `glm-5.3`）
- `name` / `familyName` — 展示名 / 家族中文名（`excludes` 会匹配 familyName）
- `family` — 所属家族 slug
- `provider` — 厂商（`qwen` / `qwen-domain-model` / `wan` 为阿里系，同档排序时优先）
- `capabilities` — 能力代码数组（枚举见 [capability-codes.md](capability-codes.md)）
- `features` — 特性数组
- `contextWindow` / `maxInputTokens` / `maxOutputTokens`
- `inferenceMetadata.request_modality` / `response_modality` — 模态（硬过滤依据）
- `prices` — 定价数组（type: input_token / output_token / input_token_cache / …）
- `qpmInfo` — QPM 限流信息
- `docUrl` — 官方文档链接
- `detailPath` — 指向 group 详情文件
- `offlineInfo` — 存在即视为下线，直接排除

`profile`（wiki 合成层产出，推荐理由的主要素材）：

- `familyTier` — `flagship` / `balanced` / `lightweight`（档位排序与席位分配依据）
- `scenes` — 适用场景词（场景维度打分依据）
- `oneLinePositioning` — 一句话定位（写理由时最直接可用的素材）
- `notSuitableFor` — 不适用场景（参与负面排除，也是写 tradeoff 的依据）
- `callModes` — `sync` / `streaming` / `async` / `realtime`（决定示例形态）
- `pipelineRole` — `[{ from, to, role }]`，pipeline 场景里的角色与模态衔接
- `styleKeywords` / `familyComparison` / `profileCompleteness` — 辅助字段，脚本未透出

以上 `profile.*` 字段中，`familyTier` / `scenes` / `oneLinePositioning` / `notSuitableFor` /
`callModes` / `pipelineRole` 已由脚本直接透出到候选里，**写理由时不要回读 models.jsonl**。

## families.jsonl 字段

- `slug` — 家族标识（与 models.jsonl 的 family 字段 join）
- `name` — 家族中文名
- `primaryCapability` — 主能力
- `capabilities` — 家族下所有 item 能力的并集
- `itemCount` / `maxContextWindow`

## groups/<slug>.json 字段

单个家族完整明细：

- `name` / `description` — 家族名称与描述（含整体定位、适用领域）
- `items[]` — 家族下所有模型版本，每个 item 含：
  - `model` / `description` / `docUrl`
  - `contextWindow` / `maxInputTokens` / `maxOutputTokens`
  - `capabilities` / `features` / `prices` / `qpmInfo`
  - `samples` — 调用示例代码（详见 [samples-format.md](samples-format.md)）
  - `predictConfig` — 模型调用入参定义（temperature / top_p 等）
  - `inferenceMetadata` / `priceTimeBands` / `builtInToolMultiPrices` 等计费与推理细节
