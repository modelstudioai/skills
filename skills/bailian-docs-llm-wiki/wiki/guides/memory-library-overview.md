# memory library [overview](overview.md)

记忆库是百炼平台为大模型提供的跨会话[长期记忆](../concepts/memory.md)服务，通过自动从对话中提取关键信息并持久化存储，解决大模型上下文窗口限制导致的“每次对话从零开始”问题。它支持两种核心记忆类型：动态的**事实记忆**（如事件、提醒）和结构化的**用户画像**（如年龄、职业），并在后续对话中基于语义检索相关记忆，注入 Prompt 实现个性化、连贯的交互。所有能力均通过开放 API 提供，可无缝集成至 Agent 或工作流应用。

## 支持的模型/功能

- **事实记忆**：自动从 `messages` 对话流中提取关键事件（如“每天上午9点提醒我喝水”），支持配置过期时间（7/30/180天或永不过期）和抽取策略版本（Pro/Lite）。详见[配置记忆规则](../../raw/application-user-guide/memory-library-overview/create-memory/configure-rules.md)。
- **用户画像**：基于预定义模板（`profile_schema`）提取结构化属性（如年龄、爱好、职业），需显式传入 `profile_schema_id` 才触发抽取，提取结果异步生成，首次查询可能为空，建议按业务重试。完整流程见[使用用户画像](../../raw/application-user-guide/memory-library-overview/create-memory/user-profile.md)。
- **多模态与技能记忆**：当前文档未覆盖多模态记忆细节，但计费说明明确区分了“事实记忆多模态 Pro”和“技能记忆 Pro”等独立计费项，表明底层支持扩展类型 [计费说明](../../raw/application-user-guide/memory-library-overview/integration-overview/billing.md)。

> **注意**：文档 15 中 OpenClaw 插件的 `memory_store` 工具允许直接写入原始内容（绕过自动抽取），而文档 2 和 4 的 `AddMemory` 接口默认仅支持自动抽取。二者功能定位不同：前者用于用户主动指令（如“记住我的服务器IP”），后者用于被动提炼对话。开发者应根据场景选择。

## 关键参数

| 参数 | 说明 | 默认值 | 注意事项 |
|------|------|--------|----------|
| `user_id` | 记忆实体 ID，实现用户级隔离 | 必填 | 不同 `user_id` 的记忆完全隔离；OpenClaw 插件强制要求配置此参数 |
| `plan_version` | 控制 Add/Search 调用的策略版本 | `Pro` | `Add` 的版本由记忆规则配置决定；`Search` 的版本由请求参数独立控制，不传即 `Pro`。详见[核心概念](../../raw/application-user-guide/memory-library-overview/overview/concepts.md) |
| `top_k` | 检索最大返回条数 | `10`（API） / `5`（OpenClaw 插件） | 取值范围 1–100；过高可能引入噪声，建议按需设置 |
| `min_score` | 相似度阈值（0.0–1.0） | `0.3`（API） / `0`（OpenClaw 插件） | 建议设为 `0.5–0.7` 平衡召回率与精度；低于阈值的记忆被过滤 |
| `meta_data` | 自定义元数据字段 | 可选 | 强烈建议用于分类管理（如 `{"category": "health"}`），便于后续精确检索 |

## 使用方式

1. **快速验证**：使用默认记忆库，3 步完成闭环——调用 `AddMemory` 写入对话 → 在控制台**记忆详情**页按 `user_id` 查看 → 调用 `SearchMemory` 检索 [快速开始](../../raw/application-user-guide/memory-library-overview/overview/quickstart.md)。
2. **自定义规则**：创建新记忆库后，在**记忆规则**标签页配置事实记忆（指定指令、过期时间）和用户画像（定义字段、初始值），每个库最多 50+50 条规则 [配置记忆规则](../../raw/application-user-guide/memory-library-overview/create-memory/configure-rules.md)。
3. **集成路径**：
   - **Agent Harness**：在百炼智能体控制台直接绑定记忆库，零代码启用跨会话记忆；
   - **插件模式**：如 OpenClaw 插件，通过 `autoCapture`/`autoRecall` 钩子自动完成记忆生命周期管理，同时暴露 `memory_search` 等工具供 Agent 主动调用 [集成方式概览](../../raw/application-user-guide/memory-library-overview/integration-overview.md)。

## 限制和注意事项

- **限流**：全部接口总计 ≤ 3000 QPM（账号级）；`AddMemory` ≤ 120 QPM；`SearchMemory` ≤ 300 QPM。超限返回 HTTP `429`，需实现退避重试 [限流说明](../../raw/application-user-guide/memory-library-overview/integration-overview/limits.md)。
- **商业化时间点**：记忆库将于 **2026 年 8 月 20 日 10:00（北京时间）** 正式计费，此前为免费体验期。所有文档均强调此时间点，信息一致。
- **默认记忆库**：每个账号自带且**不可删除**，但可编辑名称、描述及规则；其预置的“默认项目”规则可修改，不可删除 [创建与删除记忆库](../../raw/application-user-guide/memory-library-overview/create-memory.md)。
- **存储有效期**：事实记忆与用户画像本身无全局失效日期，仅受创建时配置的“记忆过期时间”约束；10,000 条免费存储额度长期有效，无时效限制 [常见问题](../../raw/application-user-guide/memory-library-overview/integration-overview/faq.md)。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)
- [记忆库概览](../../raw/application-user-guide/memory-library-overview/overview.md)
- [快速开始](../../raw/application-user-guide/memory-library-overview/overview/quickstart.md)
- [核心概念](../../raw/application-user-guide/memory-library-overview/overview/concepts.md)
- [创建与删除记忆库](../../raw/application-user-guide/memory-library-overview/create-memory.md)
- [使用用户画像](../../raw/application-user-guide/memory-library-overview/create-memory/user-profile.md)
- [配置记忆规则](../../raw/application-user-guide/memory-library-overview/create-memory/configure-rules.md)
- [集成方式概览](../../raw/application-user-guide/memory-library-overview/integration-overview.md)
- [管理记忆](../../raw/application-user-guide/memory-library-overview/create-memory/manage-memory.md)
- [计费说明](../../raw/application-user-guide/memory-library-overview/integration-overview/billing.md)
- [限流说明](../../raw/application-user-guide/memory-library-overview/integration-overview/limits.md)
- [常见问题](../../raw/application-user-guide/memory-library-overview/integration-overview/faq.md)
- [最佳实践](../../raw/application-user-guide/memory-library-overview/best-practices.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/best-practices/modelstudio-memory-for-openclaw.md)


