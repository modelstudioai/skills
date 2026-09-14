# memory library overview

记忆库（Memory Library）是百炼平台提供的长期记忆管理能力，用于在多轮对话中持久化存储和检索用户或应用相关的上下文信息。它支持结构化与非结构化数据的混合存储，并通过向量检索与关键词匹配实现高效召回。该能力面向 LLM 应用开发者，需配合百炼 SDK 或 REST API 集成使用。

## 支持的模型/功能

- 当前仅支持接入百炼平台托管的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 等 Qwen 系列模型（详见 [记忆库](../../raw/application-user-guide/memory-library-overview.md)）；其他自定义模型暂不支持原生记忆库调用。
- 提供两类核心功能：**长期记忆写入（upsert）** 与 **上下文增强式检索（retrieve with context）**，后者可在调用大模型时自动注入相关记忆片段。
- 支持按 `user_id`、`session_id`、`tag` 多维过滤，但不支持跨 `app_id` 共享记忆（[长期记忆 API](../../raw/application-user-guide/memory-library-overview.md) 中明确限定作用域为单应用实例）。

## 关键参数

- `memory_id`：必填，由系统生成或用户指定的唯一标识，长度 ≤ 64 字符，仅支持字母、数字、下划线、短横线。
- `content`：必填，文本内容（最大 8192 字符），将被自动切片并嵌入；若含 JSON 结构，建议先序列化为字符串。
- `metadata`：选填，键值对字典（最大 10 对，每 key ≤ 32 字符，value ≤ 256 字符），用于后续过滤，**不参与向量化**。
- `ttl_seconds`：选填，过期时间（默认 30 天，最小 300 秒，最大 365 天），超时后自动清理。

## 使用方式

1. 初始化：通过 `BailianClient` 实例调用 `memory.create()` 创建记忆库实例（需传入 `app_id`）；
2. 写入：调用 `memory.upsert()` 批量插入或更新记忆条目；
3. 检索：在 `chat.completions.create()` 的 `extra_parameters` 中设置 `"enable_memory": true`，系统将自动基于当前 `user_id` 和对话历史检索并注入 Top-K 相关记忆（K 默认为 3，不可配置）；
4. 显式检索（调试用）：调用 `memory.retrieve()`，传入 `query` 和可选 `filter` 参数，返回带 score 的记忆列表。

> **注意**：[为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview.md) 文档中描述的 `plugin_config` 方式已废弃，当前所有 OpenClaw 应用必须统一通过 `extra_parameters.enable_memory` 控制，否则无法生效。

## 限制和注意事项

- 单次 `upsert` 最多提交 100 条记录；单个记忆库总容量上限为 100 万条（硬限制，超限写入将返回 `400 Bad Request`）；
- 检索延迟受记忆总量影响，当条目数 > 10 万时，P95 响应时间可能超过 800ms，建议按业务维度拆分多个记忆库；
- 记忆内容不经过模型侧微调或重排序，检索结果按向量相似度降序排列，**不支持 BM25 或混合打分**；
- 所有操作均需 `app_id` 授权，且仅限创建者账号或具有 `BailianFullAccess` 权限的 RAM 角色调用（参见 [记忆库](../../raw/application-user-guide/memory-library-overview.md) 权限说明）。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview.md)


