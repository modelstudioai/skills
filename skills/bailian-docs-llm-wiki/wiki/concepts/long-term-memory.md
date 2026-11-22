# 长期记忆

长期记忆（Long Term Memory）是百炼平台提供的结构化、可检索、生命周期可控的用户级持久化记忆服务，用于跨会话、跨任务地存储和复用事实性信息（如用户事件）、结构化画像（如偏好与身份属性）及可复用技能（如流程模板）。它独立于单次对话上下文，通过语义向量+结构化索引混合架构实现高精度召回与业务语义对齐。

## 在百炼平台的不同场景中，这个概念如何使用

- **Managed Agents**：作为 `Memory Store` 的核心能力，默认启用（`enable_memory=true`），在每次 `/session/{session_id}/chat` 调用后自动将关键对话片段写入长期记忆（类型由 `project_id` 规则或显式配置决定），并在后续请求中按需检索注入上下文。  
- **Agent Context 配置**：当 `context.memory.type = "user"` 时，底层即调用长期记忆服务，基于传入的 `user_id` 检索并注入该用户的 `observation` 和 `skill` 类型记忆；`user_profile` 则通过预定义 schema 自动填充结构化字段。  
- **独立 API 调用**：开发者可通过 `long-term-memory-new` RESTful 接口（如 `/add-async`、`/memory_nodes/search`）直接管理记忆，适用于需精细控制抽取逻辑、多项目协同或与外部系统集成的场景（如 CRM 同步用户画像）。  
- **Sandbox Agent / Flow Agent**：虽不自动写入，但可通过 `agentscope-runtime` SDK 显式调用 `LongTermMemoryClient` 进行读写，实现自定义记忆策略（例如仅在满足业务规则时保存会议纪要为 `skill`）。  
- **Agent Governance 安全体系**：所有写入长期记忆的内容均经过默认内容安全检测（“量·挡·记”闭环中的“记”环节），敏感信息（如身份证号、手机号）会被自动识别、脱敏并记录审计日志。

## 关键参数和配置

| 参数 | 位置 | 类型 | 说明 | 是否必填 |
|------|------|------|------|----------|
| `user_id` | Query 或 Body | string | 用户唯一标识，用于隔离不同用户的记忆空间 | ✅ |
| `project_id` 或 `project_ids` | Body | string / array | 决定记忆类型（`observation`/`skill`）及抽取规则；多项目时触发联合抽取 | ✅（写入） |
| `profile_schema` | Body | string | 启用用户画像抽取时必需；值为已创建的 schema ID 或内联 JSON Schema | ❌（仅画像场景） |
| `extract_mode` | Body | string | 可选 `"profile_only"`（仅抽画像）、`"full"`（默认，全类型） | ❌（默认 `"full"`） |
| `messages` | Body | array | 触发智能抽取的原始对话消息（推荐）；与 `custom_content` 二选一 | ⚠️（二者必选其一） |
| `custom_content` | Body | string | 直接存为原始文本（跳过抽取），适合已结构化内容 | ⚠️（二者必选其一） |
| `memory_types` | `/search` Body | array | 检索时指定类型，如 `["observation", "skill"]`；默认仅 `["observation"]` | ❌（默认 `["observation"]`） |
| `top_k` | `/search` Body | integer | 最大召回数量，默认 `10` | ❌ |
| `min_score` | `/search` Body | number | 仅 `pro` 计划生效，过滤低置信度结果，默认 `0.3` | ❌ |

> 💡 提示：生产环境强烈推荐使用异步接口 `/add-async`（而非 `/add`）写入含技能或画像的记忆，避免同步超时；同步接口仅适用于轻量、实时摘要类场景。

## 面向开发者，简洁实用

- **快速开始**：设置 `MEMORY_SERVICE_ENDPOINT="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory"` 和 `DASHSCOPE_API_KEY`，即可调用 SDK 或 cURL。
- **SDK 推荐**：使用 `agentscope-runtime>=0.4.0`，一行代码初始化：
  ```python
  from agentscope.runtime import LongTermMemoryClient
  client = LongTermMemoryClient(workspace_id="your-workspace-id", api_key="sk-xxx")
  ```
- **写入示例（异步）**：
  ```python
  event_id = client.add_async(
      user_id="u123",
      project_id="proj-abc",
      messages=[{"role": "user", "content": "我下周二要飞上海，帮我订酒店"}]
  )
  # 轮询 event_id 获取结果
  ```
- **检索示例**：
  ```python
  results = client.search(
      user_id="u123",
      messages=["帮我查一下之前的会议安排"],
      memory_types=["observation", "skill"],
      top_k=5
  )
  ```
- **用户画像工作流**：先调用 `client.create_profile_schema(...)` 定义字段（如 `{"age": "integer", "interests": "array"}`），再在 `add_async` 中传 `profile_schema="schema-xyz"`，最后用 `client.get_user_profile(user_id="u123", schema_id="schema-xyz")` 获取结构化结果。
- **注意边界**：单条记忆最大 8KB（超长截断不报错）；`pro` 计划支持 Rerank 和 `min_score`，`lite` 计划仅基础向量召回；所有操作均按 `WorkspaceId` 隔离，跨空间需切换 endpoint。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [managed agents api](../api/managed-agents-api.md)
- [agent development](../guides/agent-development.md)
- [agent governance](../guides/agent-governance.md)
- [agent context](../guides/agent-context.md)


