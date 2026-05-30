# 数据来源

所有模型信息来自 `bailian-docs-llm-wiki` skill 的 `models/` 目录。

## 文件说明

| 文件 | 用途 |
| --- | --- |
| `models/models.jsonl` | 主数据源，每行一个模型 |
| `models/families.jsonl` | 家族信息，用于去重 |
| `models/groups/<slug>.json` | 模型详情，含 samples（API 调用示例代码） |

## models.jsonl 字段

每行 JSON 包含：

- `model` — 模型 API 调用名（如 `qwen-plus`）
- `family` — 所属家族 slug
- `capabilities` — 能力代码数组（如 `["TG", "VU"]`）
- `features` — 特性数组（如 `["function-calling", "web-search"]`）
- `contextWindow` — 上下文窗口（tokens）
- `prices` — 定价数组，含 input_token / output_token 等类型
- `qpmInfo` — QPM 限流信息
- `detailPath` — 指向 group 详情文件的路径

## families.jsonl 字段

每行 JSON 包含：

- `slug` — 家族标识（与 models.jsonl 的 family 字段 join）
- `name` — 家族中文名
- `primaryCapability` — 主能力
- `capabilities` — 家族下所有 item 能力的并集
- `itemCount` — 家族下模型数量
- `maxContextWindow` — 家族最大上下文窗口

## groups/<slug>.json 字段

单个家族完整明细：

- `name` — 家族名称
- `description` — 家族描述
- `items[]` — 家族下所有模型版本，每个 item 含：
  - `model` — API 调用名
  - `contextWindow` / `maxInputTokens` / `maxOutputTokens`
  - `capabilities` / `features`
  - `prices` / `qpmInfo`
  - `samples` — 调用示例代码（详见 [samples-format.md](samples-format.md)）
  - `predictConfig` — 模型调用入参定义（temperature / top_p 等）
