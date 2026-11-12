# 长期记忆

长期记忆（Long Term Memory, LTM）是百炼平台提供的**结构化、可检索、跨会话持久化**的记忆管理服务，用于存储和复用用户事实、技能知识与画像信息，支撑智能体在多轮交互中保持上下文连贯性与个性化能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **Agent 场景（Managed / Flow / Sandbox）**：通过 `enable_memory=true` 参数启用后，Agent 在每次运行时自动将关键对话片段、工具调用结果或用户显式声明的信息（如“我叫李明，住在杭州”）写入长期记忆库；后续请求中，Agent 可基于当前 query 语义检索相关记忆节点，并注入 prompt 上下文，实现“记住用户偏好”“延续上一次任务”等行为。  
- **独立记忆服务（LTM New API）**：作为独立能力开放 RESTful 接口，支持开发者细粒度控制记忆生命周期——可按 `user_id` + `project_id` 多维隔离写入 `observation`（事实）、`skill`（可复用能力封装）或触发用户画像抽取；适用于构建个性化推荐引擎、客服知识沉淀系统或 Agent 能力中心。  
- **Flow Agent 工作流**：虽文档中标注为“长期记忆（旧）”，但历史 Flow Agent 仍可通过 `CreateMemoryNode` 等接口手动注入结构化记忆片段，并在节点中通过变量引用（如 `{{memory.node_123.content}}`）显式调用，属于低代码模式下的轻量级记忆集成方式；**新项目应优先采用 LTM New 架构**。  
- **RAG 协同增强**：长期记忆不替代 RAG，而是互补——RAG 检索外部知识库，LTM 存储用户专属状态；二者可同时启用（`enable_rag=true` & `enable_memory=true`），由 Agent 统一融合决策。

## 关键参数和配置

| 参数 | 作用 | 是否必需 | 说明 |
|------|------|----------|------|
| `user_id` | 用户级隔离标识 | 是 | 所有 LTM 写/读操作必须指定，确保跨用户数据隔离 |
| `project_id` 或 `project_ids` | 项目级规则隔离 | 否（但推荐） | 决定记忆抽取逻辑（如仅对 `project_id="customer_service"` 的输入提取 `observation`）；`project_ids` 最多支持 5 个 |
| `memory_library_id` | 记忆库分组标识 | 否 | 不传则使用默认库；可用于按业务域划分（如 `"sales"` / `"hr"` 库） |
| `profile_schema` | 用户画像模板 ID | 仅画像场景必需 | 写入时携带该字段，才触发画像属性抽取；需先调用 `CreateProfileSchema` 创建模板 |
| `memory_types`（Search） | 检索目标类型 | 否（默认 `["observation"]`） | 显式传 `["skill"]` 或 `["observation","skill"]` 才能命中技能记忆 |
| `plan_version`（Search） | 计费版本控制 | 否（默认 `pro`） | `pro` 支持 `min_score` 过滤，`lite` 版本忽略该参数 |
| `enable_memory`（Agent API） | 启用开关 | 否（默认 `false`） | 在 `POST /v1/agents/{agent_id}/run` 请求体中设置，开启后 Agent 自动管理记忆 |

> ⚠️ 注意：同步写入（`/add`）仅适合纯文本、低延迟场景；生产环境**强烈推荐异步写入（`/add-async`）**，避免因抽取超时导致请求失败。

## 面向开发者，简洁实用

- ✅ **快速起步**：只需 `user_id` + `messages`（或 `custom_content`），调用 `/add-async` 即可写入记忆；后续用 `/memory_nodes/search` 传相同 `messages` 即可语义检索。  
- ✅ **技能复用**：将常用逻辑封装为 `skill` 类型记忆（含 `skill_name`/`skill_description`/`skill_tags`），再通过 `SearchMemory` 检索后动态注入 Agent 工具描述，实现“技能发现”与“零代码插件化”。  
- ✅ **画像驱动**：创建画像模板 → 写入带 `profile_schema` 的记忆 → 调用 `GetUserProfile` 获取结构化属性（如 `{"age": 28, "preferred_language": "zh"}`），直接用于 prompt 拼接或路由决策。  
- ❌ **避免踩坑**：  
  - 不要混用旧版 Flow Agent 的 `CreateMemory` 和新版 LTM API；二者数据不互通；  
  - `session_id` 仅控制 Agent 会话内短期上下文（1 小时失效），**不等于长期记忆**；LTM 数据永久保留（除非主动删除）；  
  - 图片等多模态内容需项目已开通多模态权限，否则 `image_url` 字段被静默忽略。

## 关联主题页

- [get started with agents](../guides/get-started-with-agents.md)
- [long term memory new](../api/long-term-memory-new.md)
- [agent development](../guides/agent-development.md)
- [flow agent api](../api/flow-agent-api.md)


