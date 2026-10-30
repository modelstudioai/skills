# 长期记忆

长期记忆（Long Term Memory）是百炼平台提供的结构化、跨会话、可检索的持久化记忆服务，用于存储和管理用户事实性信息（如偏好、日程）、技能知识（如工具调用流程）及结构化用户画像。它独立于单次对话生命周期，支持按用户、项目维度隔离，并通过语义向量检索实现高相关性召回。

## 在百炼平台的不同场景中，这个概念如何使用

- **Agent 上下文（`context.memory`）中**：作为 `agent context` 的一个可选模块，提供轻量级、自动化的会话状态缓存能力。当启用 `context.memory` 且配置 `auto_memory_summary: true` 时，系统会在非流式调用中自动将本轮 RAG 结果或关键对话摘要写入长期记忆；读取则在每次 Agent 调用时按 `user_id` 和 `project_id` 注入上下文，增强响应连贯性与个性化。

- **长期记忆新 API（`/api/v2/apps/memory/`）中**：作为独立的 PaaS 服务，面向开发者提供完整的 CRUD + 检索能力。支持同步/异步写入（推荐 `AddMemoryAsync`）、多模态内容解析、`observation`/`skill`/`user_profile` 三类记忆节点建模，以及基于语义相似度的 `SearchMemory`。适用于需精细控制记忆生命周期、支持画像建模或对接复杂业务逻辑的场景。

- **Flow Agent API（旧版记忆接口）中**：提供基础的 `CreateMemory`/`GetMemory` 等 OpenAPI 接口，但文档明确标注为“长期记忆（旧）”，功能受限（如无语义检索、无画像支持、无 TTL 控制），**不建议新项目采用**，仅用于存量应用兼容。

- **Agent 开发范式中**：在 Managed Agent 和 Flow Agent 中，长期记忆通过 `context.memory` 自动集成；在 Sandbox 沙箱中，开发者可直接调用长期记忆新 API（需自行处理鉴权与重试），实现自定义记忆策略（如条件写入、多源融合、事件驱动更新）。

## 关键参数和配置

| 参数 | 作用域 | 类型 | 说明 |
|------|--------|------|------|
| `context.memory.read_only` | Agent Context | boolean | `true`：仅读取已有记忆，禁止写入；`false`（默认）：允许自动摘要写入（需配合 `auto_memory_summary`） |
| `context.memory.ttl_seconds` | Agent Context | integer | 记忆项过期时间（秒），最小值 60；超时后自动清理，避免陈旧信息干扰 |
| `user_id` | 长期记忆新 API | string | **必填**，用于用户级隔离，是所有写入/检索操作的主键 |
| `project_id` 或 `project_ids` | 长期记忆新 API | string / string[] | 二级隔离键，常用于按 Agent 实例、会话 ID 或业务场景分组；与 `custom_content` 互斥 |
| `memory_types` | `SearchMemory` 请求体 | string[] | 指定检索类型，支持 `["observation", "skill"]`；默认仅查 `["observation"]` |
| `profile_schema` | `AddMemory*` 请求体 | string | 画像模板 ID；传入后触发用户画像字段抽取（如年龄、兴趣标签等） |
| `plan_version` | `SearchMemory` / 画像 API | string | `"pro"`（支持 `min_score` 过滤、高级抽取）或 `"lite"`（基础能力）；大小写不敏感 |

> ⚠️ 注意：  
> - 所有长期记忆新 API 必须通过 `Authorization: Bearer $DASHSCOPE_API_KEY` 鉴权，且 Key 需归属目标业务空间；  
> - Agent Context 中的 `context.memory` 仅在 `qwen-plus`/`qwen-max`/`qwen-turbo` 等 Qwen 系列模型上完整生效；  
> - 单次请求总 context 大小（含 memory 注入内容）不得超过 128 KB。

## 面向开发者，简洁实用

- ✅ **新项目首选**：使用长期记忆新 API（`/add-async` + `/memory_nodes/search`），搭配 `profile_schema` 构建用户画像闭环；  
- ✅ **快速集成 Agent**：在 `/v1/agents/{id}/chat` 请求中启用 `context.memory`，设置 `read_only: false` 和合理 `ttl_seconds`，开启 `auto_memory_summary` 实现零代码记忆沉淀；  
- ❌ **避免使用**：Flow Agent API 中的旧版 `/memories` 接口（已标记为“旧”，无语义检索与画像能力）；  
- 📦 **SDK 提示**：Python 开发者优先使用 `agentscope-runtime>=0.4.0`，内置 `LongTermMemoryClient` 封装了异步写入、轮询与检索全流程；  
- 🔍 **调试技巧**：检索前先用 `GET /memory_nodes?user_id=xxx` 查看原始记忆列表，确认数据已成功写入再调 `SearchMemory`。

## 关联主题页

- [agent context](../guides/agent-context.md)
- [long term memory new](../api/long-term-memory-new.md)
- [flow agent api](../api/flow-agent-api.md)
- [agent development](../guides/agent-development.md)


