# 长期记忆

长期记忆（Long Term Memory）是百炼平台提供的结构化、持久化记忆管理服务，用于跨会话、跨用户地存储和检索事实性信息、可复用技能及用户画像等高价值语义知识。它不是简单的键值存储，而是具备语义理解、异步抽取、类型化建模与向量检索能力的智能记忆中枢。

## 在百炼平台的不同场景中，这个概念如何使用

长期记忆在百炼平台中以**两种互补形态**存在，服务于不同架构层级的智能体应用：

- **面向开发者 API 层（推荐新版本）**：通过 `long-term-memory-new` 接口族（如 `/add-async`、`/memory_nodes/search`）直接管理结构化记忆节点。适用于需精细控制抽取逻辑、多项目隔离、或构建自定义记忆增强型 Agent 的场景。支持三类原生记忆类型：
  - `observation`：从对话消息中抽取的用户意图、日程、偏好等事实；
  - `skill`：从工具调用或结构化指令中提取的带元数据（`skill_name`、`skill_description`、`skill_tags`）的可复用流程；
  - `user_profile`：基于预定义 schema 异步提取的用户属性（如“职级”“常用设备”“决策风格”），需配合 `profile_schemas` 管理。

- **面向低代码/托管运行时层**：  
  - 在 **Flow Agent 应用** 中，通过 `memoryId` 将预建的记忆库注入智能体调用上下文，使 Agent 在推理时自动引用其中内容；  
  - 在 **Managed Agents（托管智能体）** 中，作为 `resources` 类型挂载至会话（`"type": "memory", "memory_id": "..."`），供沙箱内 Agent 跨步骤持续读写；  
  - 在 **Agent Context 机制** 中，当 `context.type = "memory"` 时，平台将自动注入匹配 `session_id` 和 `user_id` 的近期记忆片段（含 `role`、`content`、`timestamp`），实现轻量级上下文增强。

> ⚠️ 注意：`long-term-memory-new`（新）与 `flow-agent-api` 中的旧版长期记忆接口**不互通**，数据隔离、鉴权方式、参数体系均不同。新项目请统一使用 `long-term-memory-new`；旧版仅限存量 Flow Agent 应用维护。

## 关键参数和配置

| 参数 | 说明 | 必填 | 备注 |
|------|------|------|------|
| `user_id` | 子用户唯一标识，用于严格隔离用户级记忆 | 是 | 所有写入/检索操作强制要求，不可为空或占位符 |
| `memory_library_id` | 记忆库 ID | 否 | 不传则使用默认库；建议显式指定以提升 `ListMemory` 等接口性能 |
| `project_id` / `project_ids` | 项目 ID（最多 5 个） | 否 | 用于二级业务隔离；决定抽取 `observation` 或 `skill`；与 `custom_content` 互斥 |
| `profile_schema` | 用户画像模板 ID | 否（仅画像抽取必需） | 必须与 `messages` 同时传入，否则画像任务静默失败 |
| `plan_version` | 计费计划：`pro`（默认）或 `lite` | 否 | 影响 `SearchMemory` 的 `min_score` 过滤能力（仅 `pro` 生效）及抽取模型质量 |
| `min_score` | 检索最小相似度阈值 | 否（默认 `0.3`） | 仅 `plan_version=pro` 时生效；低于该值的结果被过滤，不返回 |

## 面向开发者，简洁实用

- ✅ **首选异步写入**：用 `POST /add-async` 提交任务，轮询 `GET /events/{event_id}` 获取结果。同步 `/add` 仅适用于极简短文本，且 `intelligent` 模式下易超时。
- ✅ **检索即用**：`POST /memory_nodes/search` 支持 `top_k`、`memory_types: ["observation","skill"]`、`filter`（JSONPath 表达式）等精准筛选，返回已向量化的内容与元数据。
- ✅ **画像闭环**：先 `POST /profile_schemas` 创建模板 → 写入时传 `profile_schema` 触发抽取 → 查询用 `GET /profile_schemas/{id}/user_profile?user_id=...`。
- ✅ **环境准备**：设置 `DASHSCOPE_API_KEY`，并用业务空间专属域名（`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory`）调用，`{WorkspaceId}` 从控制台复制。
- ❌ **避坑提示**：
  - `extract_mode=profile_only` 必须同时传 `profile_schema` 和 `messages`，缺一不可；
  - `context.type="memory"` 注入时，`context.content` 必须是符合 memory-library 结构的 JSON 对象（非字符串）；
  - 新版长期记忆**不支持** `flow-agent-api` 的 `CreateMemory` 流程，勿混用 `memoryId` 与 `memory_library_id`。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [agent context](../guides/agent-context.md)
- [flow agent api](../api/flow-agent-api.md)
- [llm application](../guides/llm-application.md)
- [agent development](../guides/agent-development.md)


