# agent context

agent context 是百炼平台中用于定义 Agent 运行时环境与外部信息输入的关键机制，它决定了 Agent 在执行任务过程中可访问的知识、历史记忆、数据源及解析能力。通过合理配置上下文，开发者可显著提升 Agent 的准确性、连贯性与领域适应性。其设计遵循模块化原则，各组件（如 RAG、Memory、Connector）可独立启用或组合使用。

## 支持的模型/功能

agent context 本身不依赖特定大模型，但需与支持 `tool calling` 和 `context injection` 能力的模型协同工作，当前已验证兼容的模型包括：Qwen-Max、Qwen-Plus、Qwen-Turbo 及部分第三方接入模型（需开启 `enable_context` 标志）。核心功能模块包括：
- **RAG**：支持从知识库动态检索并注入上下文片段，详见 [Agent 上下文](../../raw/application-user-guide/agent-context.md)；
- **Memory**：提供短期对话记忆（session-level）与长期用户画像记忆（user-level），其能力边界在 [Memory](../../raw/application-user-guide/agent-context/memory-library-overview.md) 中明确定义；
- **Connector**：用于对接外部系统（如 CRM、数据库），其协议适配与认证方式参考 [Connector](../../raw/application-user-guide/agent-context/overview.md)；
- **ParseX**：专用于非结构化文档（PDF/Word/Excel）的内容提取与语义切分，是 RAG 前置必备环节，用法见 [ParseX](../../raw/application-user-guide/agent-context/getting-started-overview.md)。

> **注意**：部分旧版 SDK 示例中将 `memory` 配置为布尔开关（`true/false`），但自 v2.3.0 起已改为对象结构（含 `type`, `ttl`, `max_length` 字段），请以 [Agent 上下文](../../raw/application-user-guide/agent-context.md) 中的 Schema 定义为准。

## 关键参数

在创建或更新 Agent 时，通过 `context` 字段传入 JSON 对象，主要参数如下：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `rag` | object | 否 | 启用 RAG 时必填，含 `knowledge_base_id`、`top_k`（默认 3）、`score_threshold`（默认 0.3）等字段 |
| `memory` | object | 否 | 启用 Memory 时必填，必须指定 `type: "session"` 或 `"user"`，且 `ttl` 单位为秒（最小 60） |
| `connector` | array | 否 | 元素为 connector ID 字符串，最多支持 5 个；ID 需已在平台预注册 |
| `parsex` | object | 否 | 仅当输入含文件 URL 时需配置，含 `mode: "auto"` / `"strict"` 及 `timeout_ms`（默认 30000） |

## 使用方式

1. 在控制台「Agent 编排」页面，点击「上下文配置」标签页，勾选所需模块并填写参数；
2. 或通过 OpenAPI 创建 Agent 时，在请求体中嵌入 `context` 字段（示例见 [Agent 上下文](../../raw/application-user-guide/agent-context.md)）；
3. 若使用 SDK，调用 `Agent.create()` 时传入 `context` 参数对象（Python SDK v2.4+ 已内置校验逻辑）；
4. RAG 与 ParseX 的协同流程：用户上传文件 → ParseX 自动触发解析 → 结果存入临时索引 → RAG 查询该索引，全过程无需手动干预。

## 限制和注意事项

- 单次请求注入的上下文总 token 数（含 RAG 片段 + Memory 摘要 + Connector 返回内容）不得超过所选模型的 `max_context_length`，超出部分将被截断且**不报错**；
- Memory 的 `user` 类型需配合用户唯一标识（`user_id`）传入，否则降级为 `session` 模式；
- Connector 返回数据若含敏感字段（如 `password`, `token`），平台**不会自动脱敏**，需在 Connector 配置中显式声明 `sensitive_fields`；
- RAG 检索结果默认按相关性排序，但若 `score_threshold` 设为 `0`，可能返回低质噪声片段，建议不低于 `0.2` —— 此行为差异已在 [Agent 上下文](../../raw/application-user-guide/agent-context.md) 的“最佳实践”章节强调。

## 来源文档

- [Agent 上下文](../../raw/application-user-guide/agent-context.md)


