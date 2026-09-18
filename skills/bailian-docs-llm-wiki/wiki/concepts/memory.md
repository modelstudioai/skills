# 长期记忆

长期记忆（Long Term Memory）是百炼平台提供的结构化、跨会话的记忆管理能力，用于持久化存储用户关键信息，并在后续对话中通过语义检索自动召回，突破大模型单次上下文窗口限制，实现智能体对用户偏好、历史行为与结构化属性的持续理解。

## 在百炼平台的不同场景中，这个概念如何使用

- **Agent Harness（智能体控制台）**：零代码启用，配置记忆规则后，系统自动从每轮对话中提取事实记忆（如“用户需每日9点喝水提醒”）和用户画像（如年龄、职业），无需修改 Agent 逻辑；检索结果需手动注入 Prompt 才能被模型感知。  
- **Managed Agents（托管式智能体）**：通过 `memory_store_id` 显式绑定记忆库实例，支持会话级与用户级双维度记忆隔离；Agent 执行中触发的 `memory_updated` 等事件可通过 Webhook 实时捕获，便于构建记忆驱动的状态机。  
- **OpenClaw 工作流**：以插件形式集成，提供 `memory_search` 和 `memory_store` 工具，支持在任意节点调用——例如在决策前检索历史反馈，在任务完成后写入执行结果，实现工作流级别的记忆闭环。  
- **Agenteval 观测与评测**：长期记忆的读写操作（`AddMemory`/`SearchMemory`）作为标准 Span 节点被全链路追踪，可用于分析记忆召回率、噪声引入率等质量指标；真实记忆交互数据可直接沉淀为评测样本，验证个性化效果。  
- **自定义应用（API 直接调用）**：面向开发者提供统一 RESTful 接口（`/add`, `/memory_nodes/search`, `/profile_schemas/{id}/user_profile`），支持细粒度控制写入内容、检索策略与画像模板，适用于需要完全自主编排记忆逻辑的高阶场景。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 | 推荐值 |
|------|------|------|------|--------|
| `user_id` | string | 是 | 用户唯一标识，所有读写操作均以此为隔离维度；最大 64 字符 | 使用业务侧稳定 ID（如用户 UUID） |
| `profile_schema` | string | 否（画像必需） | 用户画像模板 ID；**不传则仅生成事实记忆，不触发画像提取** | 创建模板后获取的有效 ID |
| `top_k` | number | 否 | 单次检索返回的最大记忆条数 | `5–10`（平衡精度与 token 开销） |
| `min_score` | number | 否 | 相似度阈值（0.0–1.0），低于此值的记忆将被过滤 | `0.5–0.7`（避免噪声，防止漏召） |
| `plan_version` | string | 否 | `"Pro"`（启用 Rerank，质量高）或 `"Lite"`（跳过 Rerank，成本低）；大小写不敏感 | 检索默认 `Pro`；高频调用可设 `Lite` |
| `messages` / `custom_content` | array / string | 是（互斥） | 对话消息列表（最多 50 条）或自定义文本（≤512 字符） | 优先传 `messages`，确保上下文完整性 |

> ⚠️ 注意：`AddMemory` 的 `plan_version` 由所引用的 `profile_schema` 模板决定（创建时指定），而非请求参数；`SearchMemory` 的 `plan_version` 则由请求显式传入，两者策略解耦。

## 面向开发者，简洁实用

- **快速上手**：开通记忆库 → 控制台创建默认项目 → 调用 `POST /add` 写入带 `user_id` 的对话 → 调用 `POST /memory_nodes/search` 检索 → 将结果拼入 Prompt。  
- **必做校验**：每次 `AddMemory` 后，若需立即使用画像，须等待约 3 秒再调用 `GET /profile_schemas/{schema_id}/user_profile?user_id=xxx`（异步提取）。  
- **调试技巧**：在控制台【记忆检索】页交互式调整 `min_score` 和 `top_k`，开启“查询改写”和“Rerank 可视化”优化召回效果。  
- **生产注意**：  
  - 所有 API 为阿里云账号级限流（总计 ≤3000 QPM，`Add` ≤120 QPM，`Search` ≤300 QPM），超限返回 `429`，需实现指数退避重试；  
  - 记忆默认长期有效，无自动过期；删除操作（`DeleteMemory`/`DeleteProfileSchema`）不可恢复；  
  - 商业化后，`Add`/`Search` 调用按 Pro/Lite 版本计费，存储按万条/小时计费，免费额度 3 个月内有效。

## 关联主题页

- [memory library overview](../guides/memory-library-overview.md)
- [long term memory new](../api/long-term-memory-new.md)
- [managed agents](../guides/managed-agents.md)
- [managed agents api](../api/managed-agents-api.md)
- [agenteval](../guides/agenteval.md)


