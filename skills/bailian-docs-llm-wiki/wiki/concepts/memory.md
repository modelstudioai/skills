# 长期记忆

长期记忆（Long Term Memory, LTM）是百炼平台提供的**跨会话、结构化、语义可检索的用户状态持久化能力**，用于突破大模型上下文窗口限制，在多轮对话、智能体执行、工作流编排等场景中持续维护事实性知识、动态偏好与静态画像，实现真正具备上下文连续性的 AI 应用。

## 在百炼平台的不同场景中，这个概念如何使用

长期记忆不是单一组件，而是贯穿多个平台能力的统一抽象，其接入方式和语义侧重因场景而异：

- **智能体（Agent）应用**：  
  - *原生集成*：在 Agent 2.0 或旧版智能体中，通过控制台开启「长期记忆」开关并绑定记忆库，或调用 API 时传入 `memory_id` 参数，即可自动完成记忆提取（事实/画像）、存储与检索；模型（如 `qwen-max`、`qwen3.8-max`）会在推理前自动召回相关记忆并注入 Prompt。  
  - *托管运行时（Managed Agents）*：在 Session 创建时，通过 `resources` 字段挂载记忆库（路径为 `/mnt/memory/<名称>`），智能体沙箱内可直接读写该路径下的结构化记忆节点，实现工具链与记忆的深度协同。

- **工作流（Workflow）应用**：  
  - 通过内置 `memory_search` 和 `memory_store` 工具节点调用，支持在任意流程节点中显式触发记忆检索或写入；也可结合条件判断节点，基于记忆内容（如 `user.preferred_language == "zh"`）动态路由分支。

- **API 直接集成（Application Call / LTM API）**：  
  - 使用 `/v1/memory/query` 与 `/v1/memory/upsert` 接口手动管理记忆，适用于自建 SDK、OpenClaw 工作流插件（`@modelstudio/modelstudio-memory-for-openclaw`）或高代码应用；支持按 `namespace` + `user_id` 精确隔离业务域。

- **记忆库（Memory Library）服务层**：  
  - 作为底层基础设施，提供统一的规则引擎（事实提取规则、画像模板 Schema）、向量索引、权限隔离（`user_id` 维度）与计费策略（Pro/Lite 版本），所有上层能力均构建于其之上。

> ✅ 关键共识：无论何种接入方式，**`user_id` 是记忆隔离的强制维度**；不同 `user_id` 的记忆完全不可见；同一 `user_id` 下，事实记忆与用户画像可共存且独立管理。

## 关键参数和配置

| 参数名 | 说明 | 典型取值 | 注意事项 |
|--------|------|----------|----------|
| `user_id` | **必填**，记忆归属标识 | `"u_123456"` | 所有 API（`AddMemory`/`SearchMemory`/`upsert`/`query`）均需携带；建议与业务用户 ID 对齐，避免使用会话 ID 等临时标识 |
| `memory_type` | 记忆类型标识 | `"fragment"`（事实）或 `"profile"`（画像） | 决定数据结构、TTL 默认值及校验逻辑；`profile` 支持字段类型定义（如 `age: integer`） |
| `namespace` | **推荐必填**，业务域隔离标识 | `"customer_service"`, `"personal_assistant"` | 与 `user_id` 共同构成三级隔离（`app_id` + `namespace` + `user_id`）；命名空间拼写错误将导致静默失败 |
| `ttl_seconds` | 记忆存活时间（秒） | `0`（永不过期）、`604800`（7天）、`2592000`（30天） | `fragment` 默认 7 天，`profile` 默认 30 天；生产环境建议显式设置，避免依赖默认值 |
| `top_k` | 检索返回最大条数 | `3`–`10` | 过高易引入噪声；API 默认 `10`，插件默认 `5`；优先设低值，按需调优 |
| `min_score` / `minScore` | 相似度阈值（过滤低相关结果） | `0.5`–`0.7` | API 单位为 `0.0–1.0`，插件单位为 `0–100`（整数）；建议从 `0.6` 起调 |
| `memory_library_id` / `memory_id` | 目标记忆库唯一标识 | `"ml-abc123..."` | 控制台记忆库卡片页可复制；未指定则使用默认库（生产环境不推荐） |
| `profile_schema` | 用户画像模板 ID | `"ps-xyz789..."` | 仅 `AddMemory` 写入画像时必需；需先调用 `CreateProfileSchema` 创建 |

> ⚠️ 重要提醒：  
> - **`projectId` 不可删除**：默认项目规则虽可编辑但不可删除，插件若未显式传入 `projectId` 将 fallback 至该规则——生产环境务必显式指定稳定 ID。  
> - **强一致性不保证**：写入后最多 2 秒内可被检索到，高并发下存在短暂延迟，勿用于强事务场景。  
> - **跨 app_id 隔离**：即使 `namespace` 和 `user_id` 相同，不同 `app_id` 的记忆完全不可见。

## 面向开发者，简洁实用

- **快速验证三步走**：  
  1. `POST /v1/memory/upsert` 写入一条 `fragment`（带 `user_id` + `namespace`）；  
  2. `GET /v1/memory/query?user_id=u_123&namespace=xxx&limit=1` 验证可见性；  
  3. 在智能体或工作流中启用记忆，观察是否自动召回。

- **生产部署四原则**：  
  ✅ 显式传入 `user_id`、`namespace`、`memory_library_id`；  
  ✅ `top_k` 设为 `3–5`，`min_score` 设为 `0.6`；  
  ✅ 画像使用前先 `CreateProfileSchema`，事实提取配置规则而非硬编码；  
  ✅ 高吞吐场景用 `AddMemoryAsync` + 轮询，避免阻塞。

- **避坑指南**：  
  ❌ 不要用会话 ID 作为 `user_id`；  
  ❌ 不要省略 `namespace` 导致跨业务污染；  
  ❌ 不要依赖默认 `projectId` 或 `memory_library_id`；  
  ❌ 不要在 `upsert` 中一次提交超 50 条记忆（限流）；  
  ❌ 不要对 `profile` 字段名使用特殊字符或超长字符串（≤64 字符）。

## 关联主题页

- [memory library overview](../guides/memory-library-overview.md)
- [long term memory new](../api/long-term-memory-new.md)
- [managed agents](../guides/managed-agents.md)
- [application call](../api/application-call.md)
- [llm application](../guides/llm-application.md)


