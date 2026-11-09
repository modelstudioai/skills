# agent context

`agent context` 是百炼平台中用于为 Agent 提供运行时上下文信息的核心机制，它决定了 Agent 在执行任务时可访问的知识、历史记忆、外部数据源及结构化解析能力。该机制通过统一的上下文注入框架，将 RAG 检索结果、[长期记忆](../concepts/long-term-memory.md)、Connector 接入的实时数据以及 ParseX 解析的文档内容动态组装为模型输入。其设计目标是提升 Agent 的事实准确性、状态一致性与多步推理可靠性。

## 支持的模型与功能

- **支持模型**：当前仅 `qwen-plus` 和 `qwen-max` 支持完整的 `agent context` 注入；`qwen-turbo` 仅支持基础 memory 注入，不支持 RAG 或 Connector 上下文（详见 [Agent 上下文](../../raw/application-user-guide/agent-context.md)）。
- **核心功能模块**：
  - **RAG 上下文**：从知识库检索相关片段，经重排序后注入（依赖 [RAG](../../raw/application-user-guide/knowledge-base.md) 配置）；
  - **Memory 上下文**：加载用户级或会话级[长期记忆](../concepts/long-term-memory.md)（参见 [Memory](../../raw/application-user-guide/agent-context/memory-library-overview.md)）；
  - **Connector 上下文**：调用预注册的外部系统（如 CRM、数据库）实时获取数据；
  - **ParseX 上下文**：对上传文档进行结构化解析（如表格提取、段落语义切分），输出标准化 JSON 片段。

> **注意**：原始文档中 `[ParseX](raw/application-user-guide/agent-context/getting-started-overview.md)` 的路径指向入门概览页，但实际 ParseX 上下文注入需在 `agent` 配置中显式启用 `parsex: true` 并指定 `parsex_id`，该细节在 [Agent 上下文](../../raw/application-user-guide/agent-context.md) 中未明确说明，应以控制台配置面板为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `context_type` | string | 是 | 取值为 `"rag"`、`"memory"`、`"connector"` 或 `"parsex"`；支持组合，如 `["rag", "memory"]` |
| `rag_config.kb_ids` | string[] | 条件必填 | 当 `context_type` 含 `"rag"` 时必需，指定知识库 ID 列表 |
| `memory_config.scope` | string | 条件必填 | 当 `context_type` 含 `"memory"` 时必需，取值 `"user"` 或 `"session"` |
| `connector_config.connector_id` | string | 条件必填 | 当 `context_type` 含 `"connector"` 时必需 |
| `parsex_config.parsex_id` | string | 条件必填 | 当 `context_type` 含 `"parsex"` 时必需 |

## 使用方式

1. 在 Agent 创建或更新时，在 `context` 字段中声明所需上下文类型及对应配置；
2. 确保所引用的 `kb_ids`、`connector_id`、`parsex_id` 已在平台中成功创建并处于 `active` 状态；
3. 调用 Agent 时无需额外传参——上下文由平台在推理前自动组装并注入 `system_prompt` 末尾（格式为 `<context>...</context>`）；
4. 开发者可通过调试日志中的 `context_summary` 字段查看实际注入的上下文摘要（需开启 `debug: true`）。

## 限制和注意事项

- 单次请求总上下文 token 数上限为 8192（含模型自身 system prompt），超限将触发截断，优先保留 RAG > Memory > Connector > ParseX；
- RAG 与 ParseX 上下文不支持跨知识库/文档的联合语义检索，必须显式指定来源；
- Memory 上下文默认按 `user_id` 隔离，若需跨用户共享（如客服坐席全局记忆），须手动配置 `scope: "global"`（该能力在 [Memory](../../raw/application-user-guide/agent-context/memory-library-overview.md) 中未提及，属新增特性）；
- Connector 上下文调用失败时，Agent 不中断执行，但对应字段注入空字符串，建议在 `post_process` 中校验关键字段存在性。

## 来源文档

- [Agent 上下文](../../raw/application-user-guide/agent-context.md)


