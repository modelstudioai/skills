# 长期记忆

长期记忆（Long Term Memory, LTM）是百炼平台提供的结构化用户状态持久化能力，用于跨会话、跨请求地保存和语义化检索用户偏好、行为特征、历史交互等关键上下文。它不是简单的键值存储，而是融合向量索引与结构化字段的双模态记忆系统，支持低延迟、高精度的自动召回与上下文注入。

## 在百炼平台的不同场景中如何使用

- **智能体（Agent）应用**：通过 `memory_id` 参数显式关联用户/会话，在调用时启用 `long_term_memory.enable: true`，平台将自动检索匹配的记忆片段（Fragments）或用户画像（Profiles），并注入 system [prompt](../guides/prompt.md)。适用于个性化推荐、连续对话状态保持、用户意图建模等场景。
- **Agent Context 上下文注入**：在 Agent 配置 YAML 的 `context_sources` 中声明 `type: memory`，指定 `scope: user` 或 `scope: session`，系统会在每次推理前动态加载对应范围的记忆内容，并与其他上下文（如 RAG、Connector 数据）按优先级合并后注入 [prompt](../guides/prompt.md)。
- **Application Call API 调用**：在 DashScope 或 Responses 协议的请求体中传入 `memory_id`（字符串），并确保应用已开启长期记忆开关；若未配置或模型不支持，该参数将被静默忽略。
- **Flow Agent 流程编排**：虽不直接暴露记忆操作节点，但可通过流程中嵌入的 Agent 调用节点间接使用长期记忆能力（需 Agent 子节点已启用 LTM）；旧版 Flow 内置记忆接口已废弃，必须依赖新版 LTM API。
- **开发者直连 API**：通过 REST 接口独立管理记忆：  
  - 写入片段：`POST /v1/applications/{app_id}/memories/fragments`  
  - 更新画像：`PUT /v1/applications/{app_id}/memories/profiles/{memory_id}`  
  - 查询/删除：`GET /v1/applications/{app_id}/memories/{memory_id}` / `DELETE /v1/applications/{app_id}/memories/{memory_id}`  
  所有操作均需应用级鉴权与配额控制。

## 关键参数和配置

| 参数名 | 类型 | 是否必填 | 说明 |
|--------|------|----------|------|
| `memory_id` | string | 是 | 全局唯一标识符（强烈建议使用 UUID v4），用于关联同一用户或会话的所有记忆条目；在 API 调用、Agent 配置、Context 源中统一使用。 |
| `ttl_seconds` | integer | 否 | 记忆存活时间（秒），默认 `2592000`（30 天），最小值 `3600`（1 小时）；设为 `0` 表示永不过期（生产环境不推荐）。 |
| `embedding_model` | string | 否 | 指定用于向量化记忆片段的嵌入模型，默认 `text-embedding-v3`；必须与主推理模型使用的 embedding 模型一致，否则影响语义召回准确率。 |
| `profile_schema` | JSON Schema | 仅 Profile 场景必填 | 定义用户画像字段结构（如 `user_age: integer`, `preferred_language: string`），含类型、约束与校验规则；schema 变更不自动迁移历史数据。 |
| `enable_long_term_memory` | boolean | 应用配置中必填 | 在应用 YAML 或控制台配置中显式设置为 `true`，否则所有记忆功能均不可用。 |

> ⚠️ 注意：  
> - 单次推理最多注入 **5 条记忆片段** 或 **1 个完整用户画像**，超出部分被截断；  
> - 单条记忆总大小（含 `content` + `metadata`）不得超过 **8 KB**；  
> - 用户画像字段名禁止以 `__` 开头，且不可与系统字段（如 `created_at`, `updated_at`）同名；  
> - 所有记忆操作受应用级 QPS 与配额限制，超限返回 `429 Too Many Requests`。

## 面向开发者：快速上手要点

- ✅ **启用前提**：确保应用已开启 `long_term_memory.enabled = true`，且选用 `qwen-max`、`qwen-plus` 或 `qwen-turbo`（v20240815+）模型；其他模型调用将静默跳过记忆注入。  
- ✅ **写入即用**：先调用 `/memories/fragments` 或 `/memories/profiles/{id}` 写入数据，后续请求只需带 `memory_id` 即可触发自动召回。  
- ✅ **混合使用推荐**：对非结构化事件（如“用户昨天问过天气”）用 Fragments；对稳定属性（如“用户年龄=28，语言=zh”）用 Profiles，二者可共存于同一 `memory_id` 下。  
- ✅ **调试技巧**：在 `application call` 请求中添加 `"debug": {"return_memory_context": true}`（如支持），可在响应中查看实际注入的记忆内容与元数据。  
- ❌ **避免踩坑**：不要在 `messages` 中手动拼接记忆文本——这会绕过语义检索，丧失长期记忆的核心价值；所有注入应交由平台自动完成。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [application call](../api/application-call.md)
- [agent context](../guides/agent-context.md)
- [get started with agents](../guides/get-started-with-agents.md)
- [flow agent api](../api/flow-agent-api.md)


