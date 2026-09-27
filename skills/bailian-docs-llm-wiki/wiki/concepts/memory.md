# 记忆管理

记忆管理是百炼平台提供的统一长期状态维护机制，用于在多轮对话、跨会话及托管式 Agent 运行中，结构化地持久化、检索和注入用户相关事实与画像信息，使大模型具备持续理解上下文与用户意图的能力。它不依赖特定模型，而是由平台级服务抽象实现，支持自动提取、语义召回与策略化生命周期控制。

## 在百炼平台的不同场景中，这个概念如何使用

- **记忆库（Memory Library）场景**：面向通用智能体应用，以 `user_id` 为隔离单元，提供开箱即用的“默认记忆库”。通过 `POST /add` 写入对话上下文，系统自动提取**事实记忆**（事件性、临时性信息）和**用户画像**（结构化、稳定性属性）；调用 `POST /memory_nodes/search` 检索并注入 Prompt。适用于个性化助手、推荐引擎等需长期状态延续的业务。

- **长期记忆（Long Term Memory, LTM）新架构场景**：面向高可控性需求，需显式启用 `long_term_memory: true` 并定义 `memory_schema`（JSON Schema）。支持按 `memory_type`（`fragment` 或 `profile`）写入，通过 `memory_context` 声明自动注入，或调用 `/v1/memory/fragments` 等 REST 接口直接操作。仅限 `qwen-max`、`qwen-plus` 等标注为 `ltm-enabled` 的模型，适合对 schema、TTL、命名空间有精细要求的生产级 Agent。

- **托管式 Agent（Managed Agents）场景**：记忆管理作为运行时隐式能力嵌入。Agent 自动基于 `session_id` 隔离短期上下文，并可**主动集成记忆库或 LTM**：在 Agent 工作流中调用 `AddMemory`/`SearchMemory` 工具，或在 `input` 中透传 `user_id` 触发记忆召回。此时记忆管理承担“跨会话状态桥接”角色，弥补单次会话上下文窗口（≤32768 token）的局限。

- **应用调用（Application Call）与 LLM 应用场景**：记忆管理通过 `user_id` 参数与应用层解耦。当调用 `/apps/{app_id}/call` 时，若传入 `user_id` 且该应用已配置记忆能力（如启用了记忆插件或绑定了记忆库），平台将在推理前自动执行记忆检索，并将结果拼接至系统提示词。无需修改应用逻辑，即可为低代码/工作流类应用赋予长期记忆。

> ⚠️ 注意：旧版 `short_term_memory` 与新版 `long_term_memory` 完全隔离；记忆库（Memory Library）与 LTM 新架构接口不兼容，迁移需重写规则与调用逻辑。

## 关键参数和配置

| 参数 | 所属场景 | 说明 | 典型取值/默认值 |
|------|----------|------|----------------|
| `user_id` | 记忆库、Application Call | 记忆实体作用域标识，强制用于跨会话隔离 | 字符串（必填） |
| `memory_type` | LTM 新架构 | 指定操作类型 | `"fragment"`（事实记忆）、`"profile"`（用户画像） |
| `ttl_seconds` | LTM 新架构 | 记忆存活时间（秒） | `0`（永不过期）、`86400`（1天）、`31536000`（1年，默认） |
| `namespace` | LTM 新架构 | 记忆逻辑分组，用于多租户/多环境隔离 | 字符串（默认为 `app_id`） |
| `plan_version` | 记忆库 | 控制提取与检索策略强度 | `"Pro"`（默认，支持相似度阈值）、`"Lite"`（轻量版） |
| `top_k` | 记忆库、LTM | 检索返回最大条数 | `1–100`，默认 `10`（平衡效果与 [Token](token.md) 开销） |
| `min_score` | 记忆库（Pro 版） | 相似度过滤阈值 | `0.5–0.7`（推荐），`0.3`（默认） |
| `auto_extract` | LTM 新架构 | 是否启用模型自动提取事实 | `true`（需配合 fragment schema） |

> ✅ 最佳实践：高频检索场景优先选 `Lite` 版本降低费用；对查准率敏感的业务（如医疗提醒、金融偏好）务必设 `min_score ≥ 0.6`；`user_id` 应与业务主键对齐（如 `uid_123456`），避免使用会话 ID 或临时 token。

## 面向开发者，简洁实用

- **快速验证**：无需创建记忆库，直接调用 `POST /add`（记忆库）或 `/v1/memory/fragments`（LTM）写入测试数据，再用 `SearchMemory` 或 `/v1/memory/debug` 查看是否生效。
- **调试技巧**：在控制台「记忆库详情页」→「记忆检索」标签页，粘贴当前 `messages` 内容模拟召回；LTM 场景下务必检查 `/v1/memory/debug` 返回的实际加载记忆快照，避免依赖隐式注入。
- **成本控制**：`SearchMemory` Pro 版 ¥0.001/次，Lite 版 ¥0.00002/次；事实记忆存储 ¥0.002/万条/小时。高频场景建议：
  - 用 `filter` 参数缩小检索范围（如 `{"key": "user_email"}`）；
  - 对非关键记忆设 `ttl_seconds = 86400`（1天）自动清理；
  - 用户画像优先复用模板，避免重复提取。
- **错误处理**：HTTP `429` 表示限流（记忆库全局 ≤3000 QPM），需实现指数退避；`200 OK` 不代表记忆立即可查（LTM 写入异步），关键路径应加 `GET /profiles/{id}` 或 `SearchMemory` 重试逻辑（建议 3 秒后查）。
- **迁移提示**：从记忆库迁移到 LTM 新架构时，需重写 schema（JSON Schema 格式）、替换 API 路径（`/v1/memory/...`）、并确认模型版本兼容性（仅 `qwen-max`/`qwen-plus` 支持）。

## 关联主题页

- [memory library overview](../guides/memory-library-overview.md)
- [long term memory new](../api/long-term-memory-new.md)
- [managed agents](../guides/managed-agents.md)
- [application call](../api/application-call.md)
- [llm application](../guides/llm-application.md)


