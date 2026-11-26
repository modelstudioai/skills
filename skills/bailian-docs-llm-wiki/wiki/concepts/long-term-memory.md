# 长期记忆

长期记忆（Long Term Memory）是百炼平台提供的**结构化、用户隔离、跨会话持久化**的记忆管理服务，用于存储和检索与用户相关的事实性信息（observation）、技能型知识（skill）及结构化用户画像（profile）。它独立于单次对话生命周期，支持按 `user_id` + `project_id` 多维隔离，并通过统一抽取模型与语义重排能力保障记忆质量。

## 在百炼平台的不同场景中，这个概念如何使用

- **Managed Agents**：在创建 Agent 时通过 `memory_store_id` 显式绑定一个长期记忆库；该库自动为每个 `session_id` 关联的 `user_id` 提供上下文注入，无需开发者手动读写。Agent 运行时自动触发记忆检索（如回答“我上次提过什么？”），并可配置是否将新对话片段写入长期记忆。
  
- **Flow Agent / Sandbox Agent**：不直接集成长期记忆服务，但可通过 `agent context` 的 `memory: { type: "long" }` 声明启用——此时平台自动注入当前用户的长期记忆片段（基于最近交互的语义相关性 Top-K 检索），作为 LLM 输入的一部分。写入需调用独立的 Long Term Memory API。

- **独立记忆服务（API/SDK）**：面向高控制需求场景，提供完整的 CRUD 能力：
  - `AddMemoryAsync`：异步写入原始消息流，触发事实/技能/画像三类抽取（由 `project_id` 或 `profile_schema` 决定）；
  - `SearchMemory`：基于自然语言查询语义检索，支持 `pro`（启用 Rerank）与 `lite`（基础向量检索）两种精度/成本模式；
  - `GetUserProfile`：按 schema 获取结构化用户画像，适用于个性化推荐、身份识别等闭环业务。

- **Agent Governance**：长期记忆的读写行为被纳入安全治理范畴——内容检测（如敏感信息、PPI）默认开启；所有写入操作在可观测性 Trace 中标记为 `memory.write` 事件，支持审计与告警。

> ⚠️ 注意：`Flow Agent API` 中提到的“长期记忆（旧）”（`/memories` 接口）属于历史组件，已停止维护；新项目**必须使用 `long-term-memory-new` 服务**（即本文档所述能力）。

## 关键参数和配置

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `user_id` | Query / Body | string | 是 | **强制字段**，用于用户级数据隔离与权限校验；缺失则拒绝请求。 |
| `project_id` 或 `project_ids` | Body | string / array[string] | 否 | 项目级二级隔离；`project_ids` 最多 5 个，与 `custom_content` 模式互斥。 |
| `memory_library_id` | Query / Body | string | 否 | 指定记忆库；不传则使用业务空间默认库（影响配额归属与物理分区）。 |
| `profile_schema` | Body | string | 否 | 用户画像模板 ID；传入后触发画像抽取，需配合 `messages` 使用（`extract_mode=profile_only` 时除外）。 |
| `plan_version` | Body | string | 否 | 计费策略版本，取值 `pro`（启用 Rerank）或 `lite`（基础检索）；`SearchMemory` 默认 `pro`。 |
| `extract_mode` | Body | string | 否 | 仅 `profile_only` 有效（此时必须同时传 `profile_schema` 和 `messages`）。 |

- **Managed Agent 绑定配置**：在 `POST /v1/agents` 请求体中指定：
  ```json
  {
    "model": "qwen-max",
    "skills": ["skl-xxx"],
    "memory_store_id": "ms-yyy"  // 必须为已创建的长期记忆库 ID
  }
  ```
- **Agent Context 启用（Flow/Sandbox）**：在 YAML 或 `context_override` 中声明：
  ```yaml
  memory:
    type: "long"
    ttl_seconds: 2592000  # 可选，单位秒（30天），默认永久
  ```

## 面向开发者，简洁实用

- ✅ **首选异步写入**：生产环境务必使用 `AddMemoryAsync`，避免同步接口超时风险；轮询 `event_id` 获取结果。
- ✅ **搜索即用即查**：`SearchMemory` 不需要预建索引，传入自然语言问题（如“我订过哪些酒店？”）即可返回相关记忆片段。
- ✅ **用户 ID 是生命线**：所有读写必须带 `user_id`；若业务无天然用户标识，需自行生成稳定 ID（如哈希手机号）。
- ❌ **不支持运行时切换记忆库**：Managed Agent 创建后，`memory_store_id` 不可修改；需重建 Agent。
- ❌ **不支持跨用户共享记忆**：`user_id` 隔离严格，无“全局记忆”概念；共享需业务层聚合。
- 📌 **调试建议**：在 Agent Governance 的 Trace 中查看 `memory.search` 和 `memory.write` 事件耗时与返回条数，快速定位检索效果问题。

## 关联主题页

- [managed agents api](../api/managed-agents-api.md)
- [long term memory new](../api/long-term-memory-new.md)
- [agent development](../guides/agent-development.md)
- [flow agent api](../api/flow-agent-api.md)
- [agent governance](../guides/agent-governance.md)
- [agent context](../guides/agent-context.md)


