# memory library overview

记忆库（Memory Library）是百炼平台提供的长期记忆管理能力，用于在多轮对话中持久化存储和检索用户/应用相关的上下文信息。它支持结构化与非结构化数据的混合存储，并通过向量检索与关键词匹配双路召回提升检索精度。该能力面向 LLM 应用开发者，需配合百炼 SDK 或 REST API 集成使用。

## 支持的模型/功能

- 当前仅支持接入百炼平台托管的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 等 Qwen 系列模型（[记忆库](../../raw/application-user-guide/memory-library-overview.md)）；其他自定义模型暂不支持原生记忆库调用。
- 提供两类核心功能：**长期记忆写入（`upsert`）** 与 **上下文增强式检索（`retrieve`）**，后者可在推理请求中自动注入相关记忆片段。
- 支持按 `user_id`、`session_id`、`tag` 多维元数据过滤，且允许为每条记忆设置 TTL（Time-To-Live），实现自动过期清理。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `memory_id` | string | 否 | 唯一标识符，未提供时由系统自动生成；重复 ID 视为更新操作 |
| `content` | string | 是 | 记忆正文，最大长度 8192 字符；超长内容将被截断（[长期记忆 API](../../raw/application-user-guide/memory-library-overview.md)） |
| `embedding_model` | string | 否 | 指定嵌入模型，默认为 `text-embedding-v3`；若显式指定不兼容模型（如 `text-embedding-ada-002`），请求将失败 |
| `ttl_seconds` | integer | 否 | 过期时间（秒），范围 `60`–`31536000`（1年），设为 `0` 表示永不过期 |

> **注意**：原始文档 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview.md) 中提及“支持任意 HuggingFace 模型作为 embedding backend”，该描述已过时；当前仅支持平台预置的 embedding 模型，自定义 embedding 模型接入尚未开放。

## 使用方式

1. **初始化**：调用 `MemoryClient`（Python SDK）或 `POST /v1/memories`（REST API），需携带 `Authorization: Bearer <api_key>`；
2. **写入记忆**：调用 `client.upsert()`，传入 `content`、可选 `metadata` 及 `ttl_seconds`；
3. **检索增强**：在 `ChatCompletion` 请求的 `extra_parameters.memory` 字段中启用 `enable: true`，并指定 `top_k`（默认 3）与 `filter` 条件；
4. 所有操作均需在百炼控制台开通「记忆库」配额并绑定应用（[记忆库](../../raw/application-user-guide/memory-library-overview.md)）。

## 限制和注意事项

- 单次 `upsert` 最大请求数：100 条；单条 `content` 超过 8192 字符将被静默截断；
- 免费版应用默认配额为 10 万条记忆条目，超出后写入失败并返回 `429 Too Many Requests`；
- 检索结果不保证实时一致性：写入后最多 2 秒内可被检索到，高并发场景下可能存在短暂延迟；
- 不支持跨项目（project_id）共享记忆库实例，每个应用必须独立管理其记忆空间。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview.md)



