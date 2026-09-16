# long term memory new

[长期记忆](../concepts/long-term-memory.md)（新）是百炼平台提供的持久化对话状态管理能力，支持在多轮对话中跨会话保留用户偏好、历史交互、上下文摘要等结构化信息。该能力通过独立的存储服务与推理模型解耦，开发者可自主控制写入、检索与生命周期策略。其设计目标是替代旧版 `session_state` 的临时性局限，适用于客服助手、个性化推荐、多步骤任务型对话等场景。

## 支持的模型/功能

- 当前仅对调用 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 模型的 `chat` 接口生效（需显式启用 `long_term_memory: true`）；其他模型（如 `qwen-vl`、`qwen-audio`）暂不支持。
- 支持两种核心操作：**自动记忆写入**（基于系统提示中的 `memory_schema` 定义字段）和**按需检索**（通过 `retrieve_memory` 参数触发语义召回）。
- 不支持在 `completion` 或 `function_calling` 模式下使用。详见 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `long_term_memory` | boolean | 否（默认 `false`） | 启用[长期记忆](../concepts/long-term-memory.md)功能开关 |
| `memory_schema` | object | 否 | 定义需提取并持久化的字段结构，如 `{ "user_preference": "string", "order_id": "number" }`；字段名将作为后续检索的 key |
| `retrieve_memory` | object | 否 | 控制检索行为，含 `top_k`（默认 3）、`filter`（KV 过滤条件）等子字段 |

> **注意**：`memory_schema` 中字段类型声明（如 `"string"`）仅用于校验，不参与向量化；实际存储为 JSON 字符串。该行为与 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 中“数据序列化”章节一致，但与旧版文档中提及的“类型映射到向量字段”描述矛盾——后者已过时，请以本页及 [长期记忆（新）API 参考](../../raw/application-api-reference/long-term-memory-new/long-term-memory-api-reference.md) 为准。

## 使用方式

1. 在请求 `chat` 接口的 `messages` 外层传入 `long_term_memory: true`；
2. （可选）在 `system` 消息中定义 `memory_schema`，例如：
   ```json
   { "role": "system", "content": "请从对话中提取：用户所在城市（city）、偏好的语言（language）。schema: {\"city\":\"string\",\"language\":\"string\"}" }
   ```
3. （可选）在后续请求中添加 `retrieve_memory: { "top_k": 5, "filter": { "city": "杭州" } }` 触发定向召回；
4. 所有写入/检索均基于 `user_id` 隔离，无需额外指定 namespace。

## 限制和注意事项

- 单个 `user_id` 下最多存储 1000 条记忆记录，超出后按 LRU 策略自动淘汰；
- `memory_schema` 最多支持 10 个字段，单字段值长度上限 2048 字符；
- 检索结果以 `retrieved_memory` 字段返回于响应体顶层，**不会自动注入 `messages`**，需开发者手动拼接至 [prompt](../guides/prompt.md)；
- 写入延迟约 200–500ms，高并发场景建议异步调用或降级为本地缓存；
- 该能力依赖平台统一记忆服务，若服务不可用，请求将降级为 `long_term_memory: false` 并记录告警日志。

## 来源文档

- [长期记忆](../../raw/application-api-reference/long-term-memory-new.md)


