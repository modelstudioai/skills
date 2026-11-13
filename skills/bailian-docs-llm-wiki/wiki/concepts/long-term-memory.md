# 长期记忆

长期记忆（Long Term Memory）是百炼平台提供的结构化、用户级记忆管理服务，支持开发者以编程方式持久化存储、智能抽取、精准检索和生命周期管理业务相关的事实、技能与用户画像信息。所有数据按 `user_id` 隔离，并可结合 `project_id` 进行二级分组，适用于构建具备持续认知能力的生产级 AI 应用。

## 在百炼平台的不同场景中，这个概念如何使用

- **Agent 开发（Agent Context）**：在 Agent 的 `context_config` 中设置 `memory_type: "user"`，即可自动将用户级长期记忆注入推理上下文；调用时需在请求 Header 中携带 `X-User-ID`，否则降级为会话级短期记忆。该机制与 RAG、Connector 等上下文模块正交协同，共同增强 LLM 的环境感知能力。

- **Managed Agent / Sandbox / Flow Agent**：可通过 API 主动写入或检索记忆节点（如记录用户偏好、会议纪要流程、出差计划等），不依赖 Agent 自动触发；Sandbox Agent 可在 Python 代码中调用 Long Term Memory API 实现复杂记忆编排（例如：多轮对话后批量更新画像 + 触发技能同步）。

- **独立记忆服务（API 直接调用）**：面向需要精细控制记忆生命周期的场景，提供完整 CRUD 接口：
  - 同步写入（`/add`）：适用于低延迟事实记忆（`observation`）录入；
  - 异步写入（`/add-async`）：推荐用于高精度技能抽取（`skill`）或用户画像联合生成；
  - 检索（`/search`）：支持按类型（`observation`/`skill`）、相关性（`min_score`）、项目分组（`project_ids`）等多维过滤；
  - 用户画像管理：通过预定义 `profile_schema` 驱动结构化抽取，结果严格遵循模板字段。

> ⚠️ 注意：长期记忆与 Managed Agent 中的 `memory_store_id`（会话级内存）属不同抽象层——前者跨会话、跨 Agent、用户全局可见；后者仅限单次 Session 生命周期内临时缓存，不可跨请求复用。

## 关键参数和配置

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `user_id` | Query / Body | string | ✅ | 用户唯一标识，所有读写操作均以此隔离数据；必须与 Agent 调用时的 `X-User-ID` 一致。 |
| `memory_types` | Body (Search) | string[] | ❌ | 默认 `["observation"]`；查技能需显式传 `["skill"]` 或 `["observation", "skill"]`。 |
| `project_ids` | Body (Add/Search) | string[] | ❌ | 最多 5 个，用于按 Agent、Session、任务流等逻辑分组；与 `project_id` 互斥。 |
| `profile_schema` | Body (Add) | string | ❌ | 画像模板 ID；传入后自动触发用户画像抽取（需配合 `messages` 内容）。 |
| `extract_mode` | Body (Add) | `"efficient"` \| `"intelligent"` | ❌ | 默认 `"efficient"`；`"intelligent"` 模式必须搭配 `/add-async` 使用。 |
| `min_score` | Body (Search) | number | ❌ | 默认 `0.3`；仅当 `plan_version="pro"` 时生效，用于过滤低置信度结果。 |
| `top_k` | Body (Search) | integer | ❌ | 默认 `5`，最大 `50`；控制返回记忆节点数量。 |

- **认证要求**：需配置 `DASHSCOPE_API_KEY` 和 `MEMORY_SERVICE_ENDPOINT`（格式：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory`）。
- **多模态支持**：若项目已开通多模态能力，`messages[].content` 中的 `image_url` 将参与记忆抽取；否则图片被忽略。
- **画像模板驱动**：字段完全由开发者通过 `CreateProfileSchema` 定义（如 `age`, `preferred_language`），抽取结果 100% 结构化，无自由文本。

## 面向开发者，简洁实用

- ✅ **首选异步写入**：对含技能或画像的记忆，一律使用 `/add-async` + 轮询 `/events/{event_id}`，避免超时失败。
- ✅ **检索前先指定类型**：`/search` 默认不返回 `skill`，务必显式传 `memory_types: ["skill"]`。
- ✅ **画像抽取 = 模板 + 内容 + `profile_schema`**：三者缺一不可；`extract_scene` 等高级配置仅在模板创建时设定，调用 `AddMemory` 时无需重复传。
- ❌ **不要混用 `memory_store_id` 和长期记忆**：前者是 Managed Agent 的会话缓存，后者是独立服务，二者数据不互通、不共享。
- 📌 **计费提示**：长期记忆服务自 2026 年 8 月 20 日起正式商业化，建议在开发阶段通过控制台配额监控用量。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [agent development](../guides/agent-development.md)
- [agent context](../guides/agent-context.md)
- [managed agents api](../api/managed-agents-api.md)


