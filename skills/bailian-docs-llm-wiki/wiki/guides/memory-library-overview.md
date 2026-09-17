# memory library [overview](overview.md)

记忆库是百炼平台为大模型提供的跨会话长期记忆服务，通过自动从对话中提取关键信息并持久化存储为事实记忆与用户画像，在后续对话中基于语义检索相关记忆并注入上下文，使智能体持续理解用户偏好和历史行为。它以 `user_id` 为隔离维度，支持多应用共享、规则驱动的自动化[记忆管理](../concepts/memory.md)，并提供完整的开放 API 与控制台可视化操作能力。

## 支持的模型/功能

记忆库不依赖特定大模型，而是作为独立的记忆中间件，通过向量化与语义检索技术实现跨模型通用能力。其核心功能包括：

- **事实记忆**：自动从对话消息中提取动态事件信息（如“每天上午9点提醒我喝水”），适用于临时性、变化中的用户意图或任务；
- **用户画像**：基于预定义模板（`profile_schema`）结构化提取固定属性（如年龄、职业、爱好），支持字段级描述引导与初始值配置；
- **双模式[记忆管理](../concepts/memory.md)**：既可通过控制台配置记忆规则实现全自动提取（[记忆库概览](../../raw/application-user-guide/memory-library-overview/memory.md)），也可通过[插件](../concepts/plugin.md)方式在 OpenClaw 等工作流中启用 `autoCapture`/`autoRecall` 生命周期钩子实现零代码集成（[为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/best-practices/modelstudio-memory-for-openclaw.md)）。

> **注意**：文档 4（`long-term-memory.md`）中提出的“记忆片段（MemoryNode）”与“记忆变量”概念，与当前统一术语体系存在不一致——后者已被“事实记忆”和“用户画像”取代。所有新开发应以 [核心概念](../../raw/application-user-guide/memory-library-overview/memory/concepts.md) 中定义的两类记忆为准，避免使用已废弃的“记忆变量”表述。

## 关键参数

| 参数 | 说明 | 取值/范围 | 默认值 | 备注 |
|------|------|-----------|--------|------|
| `user_id` | 记忆实体唯一标识，用于跨会话隔离 | 字符串 | — | 必填，所有接口均需传入 |
| `plan_version` | 控制 Add/Search 调用策略版本 | `"Pro"` 或 `"Lite"` | `"Pro"` | `Add` 版本由记忆规则配置决定；`Search` 版本由请求参数独立控制（详见[计费说明](../../raw/application-user-guide/memory-library-overview/overview/billing.md)） |
| `min_score` | 相似度阈值，过滤低相关性结果 | `0.0–1.0` | `0.3`（API）、`0.5–0.7`（控制台建议） | 建议调试时设为 `0.5–0.7`，过低易引入噪声，过高可能漏召 |
| `top_k` | 单次检索返回的最大记忆条数 | `1–100` | `10`（API 示例）、`5`（OpenClaw [插件](../concepts/plugin.md)默认） | — |
| `memory_library_id` | 指定目标记忆库 ID | 字符串 | 默认记忆库 | 非必填，不传则使用账号默认记忆库 |
| `profile_schema` | 用户画像模板 ID | 字符串 | — | 仅当需触发画像提取时必填；未传则仅生成事实记忆 |

## 使用方式

### 1. 快速验证（3 步）
- **写入**：调用 `AddMemory` 接口传入 `messages` 和 `user_id`，系统自动提取事实记忆（[快速开始](../../raw/application-user-guide/memory-library-overview/memory/quickstart.md)）；
- **查看**：在控制台「记忆详情」页输入 `user_id` 查看提取结果，或调用 `ListMemory` API；
- **检索**：调用 `SearchMemory` 接口传入查询语句，或在控制台「记忆检索」页调试参数。

### 2. 生产就绪配置
- **创建自定义记忆库**：用于业务隔离（如区分电商/客服场景），支持最多 50 条事实记忆规则 + 50 条用户画像规则（[创建与删除记忆库](../../raw/application-user-guide/memory-library-overview/create-memory.md)）；
- **配置记忆规则**：在事实记忆规则中设置 `plan_version`、过期时间（7/30/180天/永不过期）；在用户画像规则中定义字段名、描述及初始值（[配置记忆规则](../../raw/application-user-guide/memory-library-overview/create-memory/configure-rules.md)）；
- **集成到工作流**：通过 Agent Harness（百炼智能体原生集成）或[插件](../concepts/plugin.md)（如 OpenClaw）方式接入，后者支持自动捕获与召回（[集成方式概览](../../raw/application-user-guide/memory-library-overview/overview.md)）。

## 限制和注意事项

- **限流**：阿里云账号级别总限流 3000 QPM；其中 `AddMemory` 接口限 120 QPM，`SearchMemory` 接口限 300 QPM（[限流说明](../../raw/application-user-guide/memory-library-overview/overview/limits.md)）。超限返回 HTTP `429`，需实现退避重试。
- **计费生效时间**：商业化计费将于 **2026 年 8 月 20 日 10:00（北京时间）** 正式启动，此前为免费试用期（[计费说明](../../raw/application-user-guide/memory-library-overview/overview/billing.md)）。
- **异步延迟**：用户画像提取为异步过程，调用 `AddMemory` 后需等待约 3 秒再调用 `GetUserProfile` 获取结果（[使用用户画像](../../raw/application-user-guide/memory-library-overview/create-memory/user-profile.md)）。
- **默认记忆库不可删除**：仅可编辑名称、描述及规则；自定义记忆库删除后数据不可恢复（[创建与删除记忆库](../../raw/application-user-guide/memory-library-overview/create-memory.md)）。
- **存储有效期**：事实记忆与用户画像本身无全局失效时间，但每条记忆规则可单独配置过期时间；免费存储额度为 10,000 条，长期有效（[常见问题](../../raw/application-user-guide/memory-library-overview/overview/faq.md)）。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)
- [记忆库概览](../../raw/application-user-guide/memory-library-overview/memory.md)
- [长期记忆](../../raw/application-user-guide/memory-library-overview/memory/long-term-memory.md)
- [快速开始](../../raw/application-user-guide/memory-library-overview/memory/quickstart.md)
- [核心概念](../../raw/application-user-guide/memory-library-overview/memory/concepts.md)
- [创建与删除记忆库](../../raw/application-user-guide/memory-library-overview/create-memory.md)
- [配置记忆规则](../../raw/application-user-guide/memory-library-overview/create-memory/configure-rules.md)
- [使用用户画像](../../raw/application-user-guide/memory-library-overview/create-memory/user-profile.md)
- [管理记忆](../../raw/application-user-guide/memory-library-overview/create-memory/manage-memory.md)
- [集成方式概览](../../raw/application-user-guide/memory-library-overview/overview.md)
- [计费说明](../../raw/application-user-guide/memory-library-overview/overview/billing.md)
- [限流说明](../../raw/application-user-guide/memory-library-overview/overview/limits.md)
- [常见问题](../../raw/application-user-guide/memory-library-overview/overview/faq.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/best-practices/modelstudio-memory-for-openclaw.md)
- [最佳实践](../../raw/application-user-guide/memory-library-overview/best-practices.md)


