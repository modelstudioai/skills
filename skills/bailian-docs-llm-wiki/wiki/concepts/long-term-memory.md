# 长期记忆

长期记忆（Long Term Memory）是百炼平台提供的结构化、可编程的记忆管理服务，用于持久化存储和语义化检索用户级事实信息（如偏好、习惯）、可复用技能（如操作流程），以及基于模板的用户画像属性。它不是简单的键值缓存，而是融合了对话理解、自动抽取、多项目隔离与向量语义搜索能力的智能记忆中枢。

## 在百炼平台的不同场景中，这个概念如何使用

- **Agent 运行时上下文注入**：在 Managed Agent 或 Flow Agent 中启用 `enable_memory: true` 后，平台会自动从长期记忆服务中检索与当前 `user_id`（或 `session_id`）匹配的 `observation` 和 `skill` 类型记忆，并以 `<context>...</context>` 格式注入模型输入，提升响应的事实准确性与个性化水平。支持 `scope: "user"`（默认）或 `"session"` 级别隔离。

- **自主记忆管理（API 驱动）**：通过 `long-term-memory-new` API，开发者可主动写入、检索、更新记忆节点：
  - 使用 `POST /add-async` 提交对话消息，由系统自动抽取 `observation`（如“用户不吃香菜”）和显式注册的 `skill`（如“生成周报”）；
  - 使用 `POST /memory_nodes/search` 按语义查询记忆（例如：“用户最近提过哪些健康目标？”），支持 `min_score` 过滤与类型筛选；
  - 结合 `profile_schema` 模板异步构建结构化用户画像（如年龄、职业、兴趣标签），再通过 `GET /profile_schemas/{id}/user_profile` 获取字段值。

- **与旧版记忆机制的区别**：`flow-agent-api` 中的“长期记忆（旧）”仅提供基础 CRUD 的 `Memory`/`MemoryNode` 资源，不支持自动抽取、用户画像、语义搜索或 `skill` 类型，且需 AccessKey 签名鉴权。**新项目必须使用 `long-term-memory-new` 接口**，旧接口已标记为弃用，不推荐集成。

- **多模态与扩展性**：当 `messages` 中包含 `image_url` 且项目已开通多模态能力时，图像内容可参与记忆抽取；所有记忆按 `project_id` 逻辑分组，支持单用户跨多个业务场景（如电商+客服）的数据隔离与联合检索。

## 关键参数和配置

| 参数 | 说明 | 是否必填 | 备注 |
|------|------|----------|------|
| `user_id` | 用户唯一标识，用于记忆归属与隔离 | 是 | 所有写入/检索接口均需提供 |
| `project_ids` | 记忆所属的业务项目 ID 列表（最多 5 个） | 否 | 与 `project_id` 互斥；影响检索范围，建议明确指定 |
| `memory_types` | 检索时过滤记忆类型 | 否 | 默认 `["observation"]`；可设为 `["observation", "skill"]` |
| `plan_version` | 检索计费策略 | 否 | `"pro"`（支持 `min_score`、Rerank）或 `"lite"`（基础向量检索），默认 `"pro"` |
| `min_score` | `plan_version=pro` 时生效，过滤低相关性结果 | 否 | 默认 `0.3`，建议生产环境设为 `0.5–0.7` |
| `profile_schema` | 用户画像模板 ID | 否（仅画像场景需） | 需先调用 `/profile_schemas` 创建，传入后触发异步抽取 |

> ✅ **开发提示**：  
> - 优先使用 **异步写入**（`/add-async` + 轮询 `/events/{event_id}`），同步接口在 `intelligent` 模式下易超时；  
> - 设置 `MEMORY_SERVICE_ENDPOINT` 为业务空间专属域名（格式：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/memory`），末尾**不可带 `/`**；  
> - SDK 推荐 `agentscope-runtime` 中的 `AddMemoryAsync`、`SearchMemory`、`GetUserProfile` 工具类，避免手动构造请求。

## 注意事项（面向开发者）

- **限流**：账号级总限流 3000 QPM；`add-async` 接口限 120 QPM，`search` 接口限 300 QPM。超时返回 HTTP 429，需实现指数退避重试（建议初始延迟 1s，倍增至 4s）。
- **计费时间点**：长期记忆服务将于 **2026 年 8 月 20 日 10:00（北京时间）起正式商业化计费**，按 `pro`/`lite` 版本区分调用费用。
- **安全与隔离**：记忆严格按 `user_id` + `project_ids` 双维度隔离；不支持跨用户共享，如需全局记忆（如客服坐席知识），须通过业务层聚合实现。
- **调试建议**：开启 Agent 的 `debug: true`，查看日志中 `context_summary` 字段确认记忆是否成功注入及内容摘要。

## 关联主题页

- [long term memory new](../api/long-term-memory-new.md)
- [agent context](../guides/agent-context.md)
- [flow agent api](../api/flow-agent-api.md)
- [get started with agents](../guides/get-started-with-agents.md)
- [agent development](../guides/agent-development.md)


