# agent context

agent context 是百炼平台中用于定义 Agent 运行时环境与外部信息输入能力的核心机制，它决定了 Agent 能够感知和利用哪些上下文数据（如知识库、历史记忆、外部系统连接等）。该机制通过结构化配置将多源上下文注入 LLM 的 prompt 或推理流程，从而提升任务执行的准确性与连贯性。其设计遵循模块化原则，各组件可独立启用或组合使用。

## 支持的模型/功能

agent context 当前支持所有百炼平台已上线的 Agent 类模型（包括 `qwen-plus-agent`、`qwen-max-agent` 及后续发布的 `-agent` 后缀模型），不兼容非 Agent 专用模型（如 `qwen-turbo` 或 `qwen-max` 基础版）。核心功能模块包括：  
- **RAG 检索增强**：对接知识库实现动态片段注入，详见 [Agent 上下文](../../raw/application-user-guide/agent-context.md)；  
- **Memory 管理**：支持会话级短期记忆与用户级[长期记忆](../concepts/long-term-memory.md)，由 [Memory](../../raw/application-user-guide/agent-context/memory-library-overview.md) 文档定义接口规范；  
- **Connector 集成**：提供标准协议接入第三方系统（如 CRM、数据库、API 网关），其能力边界在 [Connector](../../raw/application-user-guide/agent-context/overview.md) 中明确说明。

> **注意**：`qwen-plus-agent` 在 v2.3.0 版本起才完整支持 ParseX 解析器上下文注入，旧版 SDK 若未升级可能忽略 `parsex_config` 参数 —— 请以 [ParseX](../../raw/application-user-guide/agent-context/getting-started-overview.md) 的版本兼容性表格为准。

## 关键参数

在创建或更新 Agent 时，需通过 `context_config` 字段声明上下文能力，主要参数如下：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `knowledge_base_ids` | string[] | 否 | 关联的知识库 ID 列表，启用 RAG；单次最多 5 个 |
| `memory_type` | `"session"` \| `"user"` \| `"none"` | 否 | 默认 `"session"`；设为 `"user"` 时需配合 `user_id` 字段 |
| `connectors` | object[] | 否 | 每项含 `id`（connector ID）、`config`（运行时参数） |
| `parsex_config` | object | 否 | 启用 ParseX 结构化解析，详见 [ParseX](../../raw/application-user-guide/agent-context/getting-started-overview.md) |

## 使用方式

1. 在控制台「Agent 配置 → 上下文设置」中勾选所需模块并填写参数；  
2. 或通过 OpenAPI `POST /v1/agents` 请求体中传入 `context_config` 对象（格式同上表）；  
3. 调用时若需覆盖默认上下文（如指定临时知识库），可在 `/v1/agents/{id}/chat` 的 `context_override` 字段中传入子集配置 —— 此覆盖仅作用于单次请求，不影响 Agent 全局配置。

## 限制和注意事项

- 单次请求注入的上下文总 token 数（含 RAG 片段 + Memory 内容 + Connector 返回）不得超过所选模型最大 context length 的 80%，超出部分将被自动截断；  
- Memory 的 `user` 模式要求调用方必须在请求 header 中携带 `X-User-ID`，否则降级为 `session` 模式；  
- Connector 返回内容若含敏感字段（如 `password`、`token`），需在 connector 配置中显式声明 `redact_fields`，否则可能泄露 —— 该规则在 [Connector](../../raw/application-user-guide/agent-context/overview.md) 中强制要求；  
- RAG 检索结果默认按相关性排序，但不支持自定义排序逻辑或分页，如需高级检索能力，请参考 [Agent 上下文](../../raw/application-user-guide/agent-context.md) 中的扩展方案说明。

## 来源文档

- [Agent 上下文](../../raw/application-user-guide/agent-context.md)


