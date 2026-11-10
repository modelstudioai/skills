# agent context

`agent context` 是百炼平台中用于增强 Agent 推理能力的核心机制，通过动态注入外部信息（如知识库、历史记忆、连接器数据等）来扩展模型的上下文感知范围。它不改变模型本身，而是控制 LLM 输入前的上下文拼接逻辑与生命周期管理。该机制深度集成于百炼 Agent 框架，支持运行时按需加载与过滤。

## 支持的模型/功能

- **模型兼容性**：所有百炼平台支持的 Agent 模型（包括 `qwen-max`、`qwen-plus`、`qwen-turbo` 及自定义微调模型）均原生支持 `agent context`，无需额外适配。
- **核心功能模块**：
  - RAG：从知识库检索相关片段并注入上下文，详见 [Agent 上下文 (raw/application-user-guide/agent-context.md)](../../raw/application-user-guide/agent-context.md)；
  - Memory：维护会话级或用户级[长期记忆](../concepts/long-term-memory.md)，支持向量检索与 TTL 管理；
  - Connector：对接第三方系统（如 CRM、数据库），实时拉取结构化数据并转换为上下文文本；
  - ParseX：对上传文件（PDF/Word/Excel 等）进行解析与分块，生成可检索的上下文源。

## 关键参数

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `context_sources` | array of object | `[]` | 指定上下文来源列表，每个对象含 `type`（`rag`/`memory`/`connector`/`parsex`）、`id`（资源 ID）和可选 `filter`（如 `{"user_id": "{{user_id}}"}`） |
| `max_context_tokens` | integer | `2048` | 向 LLM 实际注入的上下文最大 token 数（含 prompt），超出部分按相关性截断 |
| `context_ttl_seconds` | integer | `3600` | 内存类上下文（如 `memory`）的缓存有效期，仅对启用缓存的场景生效 |

> **注意**：`max_context_tokens` 的实际生效值受所选模型最大上下文长度限制；例如 `qwen-turbo` 最大输入为 8192 tokens，但若设置 `max_context_tokens: 10000`，将被静默截断为 8192 —— 此行为在 [Agent 上下文 (raw/application-user-guide/agent-context.md)](../../raw/application-user-guide/agent-context.md) 中未明确说明，需以模型规格文档为准。

## 使用方式

1. 在 Agent 配置 YAML 或 API 请求体中声明 `context_sources`，例如：

```yaml
context_sources:
  - type: rag
    id: kb_abc123
    filter: { tags: ["public"] }
  - type: memory
    id: user_mem
    filter: { user_id: "{{user_id}}" }
```

2. 调用 `/v1/agents/{agent_id}/chat` 时传入运行时变量（如 `user_id`），系统自动解析 `filter` 并加载对应上下文；
3. 上下文内容经标准化清洗（去重、去噪、格式归一）后，与 system prompt 和用户消息拼接，送入模型推理流程。

完整配置示例与字段约束请参考 [Agent 上下文 (raw/application-user-guide/agent-context.md)](../../raw/application-user-guide/agent-context.md)。

## 限制和注意事项

- 单次请求最多支持 5 个 `context_sources`，超限将返回 `400 Bad Request`；
- `connector` 类型上下文需提前在控制台完成认证与字段映射配置，否则加载失败且无 fallback；
- `parsex` 上下文仅在首次调用时触发解析，后续请求复用已索引结果；若原始文件更新，需手动触发 `reindex`；
- 所有上下文内容在进入模型前均经过敏感词过滤与长度截断，**不保证原始格式保留**（如表格结构、代码缩进可能丢失）。

## 来源文档

- [Agent 上下文](../../raw/application-user-guide/agent-context.md)


