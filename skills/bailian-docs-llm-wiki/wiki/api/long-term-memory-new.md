# long term memory new

[长期记忆](../concepts/long-term-memory.md)（新）是百炼平台提供的持久化对话状态管理能力，支持在多轮会话中跨请求保留用户上下文、实体信息与自定义元数据。它通过独立的内存服务与推理模型解耦，适用于客服对话、个性化推荐、多步骤任务等需状态延续的场景。该能力基于向量检索与结构化存储混合架构实现，开发者可通过 API 显式读写。

## 支持的模型/功能

- 当前仅支持 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三款 Qwen 系列模型接入[长期记忆](../concepts/long-term-memory.md)（新）；其他模型调用时将忽略 `memory_id` 参数，[原文标题](../../raw/application-api-reference/long-term-memory-new.md) 明确标注“不兼容模型将退化为无状态调用”。
- 支持两类核心操作：`write_memory`（写入带 embedding 的文本块及可选 metadata）和 `retrieve_memory`（按 query 向量相似度 + metadata 过滤召回），详见 [原文标题](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。
- 不支持直接修改或删除单条记忆项，仅能通过 `clear_memory` 清空整个 `memory_id` 下全部内容。

## 关键参数

- `memory_id`（必填，string）：用户级唯一标识，建议使用业务侧 UID 或 session ID 哈希值，长度限制 1–64 字符，仅支持字母、数字、下划线、短横线。
- `query`（`retrieve_memory` 时必填）：用于向量检索的自然语言查询句，长度 ≤ 512 字符；系统自动调用内置 embedding 模型生成向量，**不可指定外部 embedding**。
- `top_k`（可选，默认 3，范围 1–10）：返回最相关记忆条目数；> **注意**：[原文标题](../../raw/application-api-reference/long-term-memory-new.md) 中示例误写为默认值 5，实际以 API 接口响应为准（v20240701+ 版本已修正为 3）。

## 使用方式

1. 初始化：首次调用 `write_memory` 时自动创建 `memory_id` 对应的内存空间；
2. 写入：POST `/v1/memory/write`，Body 包含 `memory_id`、`content`（string）、`metadata`（object，键值对，总大小 ≤ 4KB）；
3. 检索：POST `/v1/memory/retrieve`，Body 包含 `memory_id`、`query`、`top_k`、`filter`（JSON object，支持 `eq`/`in`/`contains` 操作符）；
4. 清空：POST `/v1/memory/clear`，仅需 `memory_id`。

## 限制和注意事项

- 单个 `memory_id` 下最多存储 10,000 条记忆项，单条 `content` 长度上限 8,192 字符；
- 写入延迟通常 < 300ms，但高并发写入（> 50 QPS）可能导致 503 错误，建议业务层添加重试（指数退避）；
- `metadata` 中的字段名不能以 `_` 开头（系统保留字段如 `_created_at` 由服务端注入，不可覆盖）；
- > **注意**：文档 `raw/application-api-reference/long-term-memory-new.md` 提到“支持 TTL 自动过期”，但当前生产环境（v20240701）尚未开放该配置项，实际所有记忆永久保留，直至显式调用 `clear_memory`。

## 来源文档

- [长期记忆](../../raw/application-api-reference/long-term-memory-new.md)


