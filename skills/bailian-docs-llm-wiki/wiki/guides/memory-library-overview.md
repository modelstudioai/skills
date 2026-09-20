# memory library [overview](../api/overview.md)

记忆库是为大模型提供跨会话[长期记忆](../concepts/long-term-memory.md)的核心服务，通过自动从对话中提取关键信息并持久化存储为事实记忆与用户画像，在后续交互中基于语义检索并注入上下文，从而突破上下文窗口限制，实现个性化、连贯的智能体体验。它以 `user_id` 为隔离维度，支持多应用共享与细粒度业务隔离，所有能力均通过标准化 API 暴露，可无缝集成至 Agent 或工作流系统。

## 支持的模型/功能

记忆库提供两类核心记忆能力：
- **事实记忆**：自动从对话消息中提取动态事件信息（如“每天上午9点提醒我喝水”），适用于偏好变更、临时任务等场景。提取行为由配置的**事实记忆规则**驱动，支持自定义指令、自动更新开关和过期策略。
- **用户画像**：基于预定义模板（如年龄、职业、爱好）结构化提取并持久化用户固有属性，适用于需稳定引用的用户特征管理。需先调用 `CreateProfileSchema` 创建模板，再在 `AddMemory` 中传入 `profile_schema` 参数触发提取。

> **注意**：文档 4（`raw/application-user-guide/memory-library-overview/memory/long-term-memory.md`）中提出的“记忆片段（MemoryNode）”与“记忆变量”概念，与当前统一术语体系存在不一致——后者已被明确重构为“事实记忆”与“用户画像”两种标准类型，该文档描述的旧模型已过时，应以[核心概念](../../raw/application-user-guide/memory-library-overview/memory/concepts.md)为准。

记忆库还支持完整的生命周期管理：写入（`AddMemory`）、语义检索（`SearchMemory`）、分页查询（`ListMemory`）、更新（`UpdateMemory`）、删除（`DeleteMemory`）及用户画像全链路操作（`CreateProfileSchema` / `GetUserProfile` 等）。所有接口均通过 DashScope 网关提供，服务地址为 `https://dashscope.aliyuncs.com/api/v2/apps/memory/`，详见[长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。

## 关键参数

- **`user_id`**：记忆实体唯一标识，是存储与检索的隔离维度，不同 `user_id` 的记忆完全独立。
- **`plan_version`**：控制 Pro/Lite 策略版本的核心参数。`Add` 调用的版本由对应记忆规则的 `plan_version` 决定；`Search` 调用的版本由请求参数独立指定（不传默认 `Pro`）。Pro 版本启用 Rerank 重排序，质量更高；Lite 版本跳过 Rerank，成本更低。
- **`min_score`**（相似度阈值）：取值范围 `0.0–1.0`，用于过滤低相关性结果，建议设为 `0.5–0.7`。
- **`top_k`**：单次检索返回的最大记忆条数，范围 `1–100`。
- **`meta_data`**：可选元数据字段，推荐用于分类标记（如 `{"category": "health_reminder"}`），提升后续精确检索能力。

## 使用方式

1. **快速验证**：使用默认记忆库，3 步完成端到端流程——调用 `AddMemory` 写入对话消息，通过控制台或 `ListMemory` 查看提取结果，再用 `SearchMemory` 检索验证效果。详细示例见[快速开始](../../raw/application-user-guide/memory-library-overview/memory/quickstart.md)。
2. **自定义配置**：在控制台创建新记忆库后，进入**记忆规则**标签页配置最多 50 条事实记忆规则与 50 条用户画像规则，包括规则指令、过期时间、`plan_version` 等。参见[配置记忆规则](../../raw/application-user-guide/memory-library-overview/create-memory/configure-rules.md)。
3. **集成路径**：  
   - **Agent Harness**：直接在百炼智能体控制台启用，零代码接入；  
   - **插件模式**：为 OpenClaw 等工作流框架安装 `@modelstudio/modelstudio-memory-for-openclaw` 插件，自动挂载 `before_agent_start`/`agent_end` 钩子实现记忆捕获与召回，详见[为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/best-practices/modelstudio-memory-for-openclaw.md)。

## 限制和注意事项

- **限流**：全部 API 接口总计不超过 3000 QPM（阿里云账号级别）；其中 `AddMemory` 限 120 QPM，`SearchMemory` 限 300 QPM。超限返回 HTTP `429`，需实现退避重试。
- **计费**：商业化将于 **2026 年 8 月 20 日 10:00（北京时间）** 启动，Add/Search 操作按 `plan_version` 分档计费，存储按小时计费。免费额度（1500 次 Add + 5000 次 Search）有效期为商业化生效日起 3 个月，逾期作废。
- **异步延迟**：用户画像提取为异步过程，`AddMemory` 调用后需等待约 3 秒再调用 `GetUserProfile` 获取结果。
- **默认记忆库**：每个账号自带且不可删除，但可编辑名称、描述及规则；其预置的“默认项目”规则可修改，不可删除。
- **策略版本切换**：更新记忆规则的 `plan_version` 后，**仅新写入的记忆**遵循新策略，历史记忆不受影响。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)
- [记忆库概览](../../raw/application-user-guide/memory-library-overview/memory.md)
- [长期记忆](../../raw/application-user-guide/memory-library-overview/memory/long-term-memory.md)
- [快速开始](../../raw/application-user-guide/memory-library-overview/memory/quickstart.md)
- [创建与删除记忆库](../../raw/application-user-guide/memory-library-overview/create-memory.md)
- [使用用户画像](../../raw/application-user-guide/memory-library-overview/create-memory/user-profile.md)
- [管理记忆](../../raw/application-user-guide/memory-library-overview/create-memory/manage-memory.md)
- [集成方式概览](../../raw/application-user-guide/memory-library-overview/overview.md)
- [计费说明](../../raw/application-user-guide/memory-library-overview/overview/billing.md)
- [限流说明](../../raw/application-user-guide/memory-library-overview/overview/limits.md)
- [常见问题](../../raw/application-user-guide/memory-library-overview/overview/faq.md)
- [最佳实践](../../raw/application-user-guide/memory-library-overview/best-practices.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/best-practices/modelstudio-memory-for-openclaw.md)
- [配置记忆规则](../../raw/application-user-guide/memory-library-overview/create-memory/configure-rules.md)
- [核心概念](../../raw/application-user-guide/memory-library-overview/memory/concepts.md)


