# agent context

agent context 是 Agent 运行时所依赖的动态上下文环境，用于支撑其感知、推理与执行能力。它由知识库（RAG）、记忆（Memory）、外部连接器（Connector）及结构化解析组件（ParseX）共同构成，决定了 Agent 在每次调用中可访问的信息边界与行为依据。该机制是实现状态感知型、多轮协作式智能体的核心基础设施。

## 支持的模型与功能

当前 agent context 仅在百炼平台的 `qwen-agent-2.5` 及后续支持 Agent 模式的模型中生效；基础大语言模型（如 `qwen-max`、`qwen-plus`）默认不启用 context 管理逻辑，需显式配置 `agent_mode: true` 才能激活相关上下文注入能力。其核心功能包括：基于 RAG 的实时知识检索、跨会话 Memory 持久化、第三方系统 Connector 接入，以及 ParseX 驱动的非结构化内容解析——这些能力均在 [Agent 上下文](../../raw/application-user-guide/agent-context.md) 中统一定义。

## 关键参数

- `context_config`: JSON 对象，用于声明启用的上下文模块及其配置  
  - `knowledge_base_ids`: 字符串数组，指定关联的知识库 ID（对应 [RAG](../../raw/application-user-guide/agent-context/knowledge-base.md)）  
  - `memory_library_id`: 字符串，指定记忆库 ID（对应 [Memory](../../raw/application-user-guide/agent-context/memory-library-overview.md)）  
  - `connectors`: 对象数组，每个含 `type` 和 `config` 字段（对应 [Connector](../../raw/application-user-guide/agent-context/overview.md)）  
  - `parsex_enabled`: 布尔值，启用后自动对输入文档调用 ParseX 解析（对应 [ParseX](../../raw/application-user-guide/agent-context/getting-started-overview.md)）

> **注意**：`context_config` 中若同时指定 `memory_library_id` 和 `session_id`，但未在请求头中携带有效的 `X-Bailian-Session-ID`，将导致 Memory 初始化失败——此行为与 [Memory](../../raw/application-user-guide/agent-context/memory-library-overview.md) 文档中“会话绑定为可选”的旧描述存在矛盾，以当前 API 实现为准。

## 使用方式

1. 在创建 Agent 应用或调用 `/v1/agents/{id}/chat` 接口时，于请求体中传入 `context_config`；  
2. 确保所引用的 `knowledge_base_ids`、`memory_library_id` 已在控制台完成授权与发布；  
3. 若启用 ParseX，上传文件需符合 [ParseX](../../raw/application-user-guide/agent-context/getting-started-overview.md) 支持的格式（PDF/DOCX/PPTX/TXT/CSV），且单文件 ≤ 50MB；  
4. Connector 调用前需在控制台完成 OAuth 或 API Key 配置，否则请求将被拒绝。

## 限制和注意事项

- 单次请求中 `context_config` 总大小不得超过 16KB（JSON 序列化后）；  
- Memory 当前仅支持 LRU 缓存策略，最大会话数为 10,000，超出后自动淘汰最久未访问项；  
- RAG 检索结果默认截断为 top-3 片段，不可通过 `context_config` 调整，需改用自定义检索插件；  
- 所有上下文模块均不支持嵌套调用（例如在 Connector 返回内容中再触发 RAG）；  
- 请务必参考 [Agent 上下文](../../raw/application-user-guide/agent-context.md) 的最新版本确认各模块兼容性矩阵，避免因模型升级导致 context 配置失效。

## 来源文档

- [Agent 上下文](../../raw/application-user-guide/agent-context.md)


