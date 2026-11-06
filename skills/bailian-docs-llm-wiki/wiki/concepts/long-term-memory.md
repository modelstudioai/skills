# 长期记忆

长期记忆（Long Term Memory）是百炼平台提供的结构化、可检索、带生命周期管理的记忆服务，用于持久化存储跨会话的用户事实（如偏好、日程）、技能流程（如会议纪要模板）及结构化用户画像，支撑智能体具备持续学习与个性化服务能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **Agent 运行时上下文（`agent context`）**：作为 `context_sources` 中的 `memory` 源之一，长期记忆在每次 Agent 调用时自动注入相关记忆片段（如用户历史偏好），与 RAG、Connector 等协同增强 LLM 推理依据；需通过 `user_id` 显式隔离，确保跨会话状态一致性。
  
- **Flow Agent API（旧版）**：提供 `Memory` 和 `MemoryNode` 两级抽象的 CRUD 接口（如 `/memories/{id}`），但该能力已被明确标记为**遗留方案（legacy）**，不支持用户画像、多模态抽取与智能过滤，新项目应避免采用。

- **新版长期记忆服务（`long term memory new`）**：当前主推实现，通过 RESTful API 或 `agentscope-runtime` SDK 提供统一入口。核心使用路径包括：
  - **写入**：调用 `/add-async`（推荐）或 `/add`，按 `project_id` 绑定抽取规则，指定 `memory_types`（`observation`/`skill`）或 `profile_schema` 触发画像抽取；
  - **检索**：调用 `/memory_nodes/search`，基于语义相似度召回，并支持 `top_k` 与 `min_score`（仅 `pro` 计划）控制精度；
  - **管理**：通过 `/memory_nodes/{id}` 进行单条更新/删除，或 `/profile_schemas/{id}/user_profile?user_id=xxx` 获取结构化画像。

- **Agent 治理（`agent governance`）**：长期记忆的读写操作自动纳入全链路 Trace，可观测性模块可追踪每次记忆检索的耗时、命中率、[Token](token.md) 开销及内容安全检测结果，用于性能分析与合规审计。

## 关键参数和配置

| 参数 | 说明 | 必填 | 默认值 | 注意事项 |
|------|------|------|--------|----------|
| `user_id` | 子用户唯一标识，用于记忆隔离与检索范围控制 | ✅ | — | 必须全局一致，建议与业务系统用户 ID 对齐 |
| `project_id` / `project_ids` | 指定记忆抽取所用的项目规则（决定 `memory_type`、schema、模型等） | ⚠️（二选一） | — | 与 `custom_content` 互斥；生产环境推荐传数组以支持多规则联合抽取 |
| `memory_types` | 检索时限定返回的记忆类型，支持 `["observation", "skill"]` | ❌ | `["observation"]` | `skill` 类型需显式声明才可召回 |
| `plan_version` | 计费计划版本，影响功能可用性 | ❌ | `"pro"` | `"pro"` 支持 `min_score` 过滤；`"lite"` 仅基础检索 |
| `top_k` | 检索最大返回条数 | ❌ | `10` | 建议设为 `3–5` 平衡精度与延迟 |
| `min_score` | 语义相似度最低阈值（仅 `pro` 生效） | ❌ | `0.3` | 值域 `[0.0, 1.0]`，低于此值的结果被过滤 |
| `extract_mode` | 抽取模式，`"profile_only"` 表示跳过事实/技能抽取，仅处理画像 | ❌ | — | 仅当同时传 `profile_schema` 和 `messages` 时有效 |

> **配置提示**：  
> - 同步写入（`/add`）适用于简单、低延迟场景；**生产环境务必使用异步写入（`/add-async`）**，避免 `intelligent` 模式超时；  
> - 多模态支持需在项目配置中启用，且 `messages` 中含 `image_url` 才参与抽取；  
> - 用户画像需先创建 `profile_schema`，再在写入时传入其 ID，最后通过独立接口获取结构化结果。

## 面向开发者，简洁实用

- ✅ **快速上手**：设置 `MEMORY_SERVICE_ENDPOINT` 和 `DASHSCOPE_API_KEY` 后，一行代码即可异步写入：
  ```python
  from agentscope.runtime import Runtime
  rt = Runtime()
  event = rt.memory.add_async(
      user_id="user_001",
      project_ids=["proj_skill_summary"],
      messages=[{"role": "user", "content": "请整理上周会议纪要"}]
  )
  result = event.wait()  # 阻塞等待或轮询
  ```

- ✅ **检索即用**：无需预建索引，直接语义搜索：
  ```python
  nodes = rt.memory.search(
      user_id="user_001",
      messages=[{"role": "user", "content": "我上次说喜欢什么咖啡？"}],
      memory_types=["observation"],
      top_k=3,
      min_score=0.45  # pro 计划专属
  )
  ```

- ⚠️ **避坑指南**：
  - 不要混用新旧记忆接口：`flow-agent-api` 的 `/memories` 已弃用，新项目禁止接入；
  - `user_id` 是记忆隔离的唯一依据，切勿使用临时 ID 或 session ID；
  - 异步写入后必须检查 `event.status == "succeeded"`，失败时查看 `event.error`；
  - `min_score` 仅对 `plan_version="pro"` 生效，`lite` 计划下传入无效。

- 📈 **可观测性集成**：所有长期记忆操作自动上报至 Agent Governance 的 Trace 系统，可在控制台「应用观测」中按 `memory_operation` 标签筛选，分析平均延迟、失败率与内容安全拦截情况。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [flow agent api](../api/flow-agent-api.md)
- [agent context](../guides/agent-context.md)
- [agent governance](../guides/agent-governance.md)


