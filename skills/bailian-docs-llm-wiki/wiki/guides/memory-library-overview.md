# memory library overview

记忆库（Memory Library）是百炼平台提供的长期记忆管理能力，用于在多轮对话中持久化存储和检索用户/应用相关的上下文信息。它支持结构化与非结构化数据的混合存储，并通过向量检索与关键词匹配双路召回提升检索精度。该能力面向 LLM 应用开发者，需配合百炼 SDK 或 REST API 集成使用。

## 支持的模型/功能

- 当前仅支持接入百炼平台托管的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 等 Qwen 系列模型（[记忆库](../../raw/application-user-guide/memory-library-overview.md)）；其他自定义模型暂不支持原生记忆库调用。
- 提供两类核心功能：**长期记忆写入（`upsert`）** 与 **上下文增强式检索（`retrieve`）**，后者可在推理请求中自动注入相关记忆片段。
- 支持按 `user_id`、`session_id`、`tag` 多维元数据过滤，且允许为每条记忆设置 TTL（时间生存期）。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `memory_id` | string | 否 | 记忆唯一 ID，未提供时由系统自动生成；重复 ID 将触发覆盖写入 |
| `content` | string | 是 | 原始文本内容（最大 8192 字符），将被自动切片并嵌入 |
| `embedding_model` | string | 否 | 指定嵌入模型，默认为 `text-embedding-v1`；注意该参数仅影响当前写入，不影响已有记忆的向量表示（[长期记忆 API](../../raw/application-user-guide/memory-library-overview.md)） |
| `ttl_seconds` | integer | 否 | 过期时间（秒），0 表示永不过期；超过 TTL 的记忆在检索时不可见 |

> **注意**：`embedding_model` 参数在 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview.md) 文档中被错误标注为“全局生效”，实际作用域仅限单次 `upsert` 请求，此为文档过时描述。

## 使用方式

1. **初始化**：调用 `InitMemoryClient()`（Python SDK）或配置 `X-Api-Key` 与 `X-Region` 请求头（REST）；
2. **写入记忆**：调用 `client.upsert(...)`，传入 `content`、`user_id` 及可选元数据；
3. **检索增强**：在 `ChatCompletion` 请求的 `messages` 外层添加 `memory_config` 字段，指定 `user_id` 与 `top_k`（默认 3）：
   ```json
   "memory_config": { "user_id": "u_123", "top_k": 5 }
   ```
   系统将自动检索并拼接至 system [prompt](prompt.md) 前置上下文。

## 限制和注意事项

- 单账户默认配额：100 万条记忆条目，总向量索引容量上限 10 GB；
- `content` 中若含控制字符（如 `\x00`）、超长 URL 或 Base64 编码块，可能导致嵌入异常，建议预清洗；
- 检索结果按混合相关性排序（向量相似度 × 权重 + 关键词匹配分），但不保证严格单调；如需确定性排序，应启用 `rerank: true` 并接受约 200ms 额外延迟（[记忆库](../../raw/application-user-guide/memory-library-overview.md)）。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview.md)


