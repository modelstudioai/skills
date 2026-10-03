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
| `user_id` | 记忆实体 ID，实现用户级隔离 | 必填 | 不同 `user_id` 的记忆完全隔离；OpenClaw 插件强制要求此字段 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/best-practices/modelstudio-memory-for-openclaw.md) |
| `plan_version` | 控制 Pro/Lite 策略版本 | `Pro` | **Add 调用**由记忆规则配置决定；**Search 调用**由请求参数独立控制，不传即 `Pro`。Lite 版关闭 Rerank，成本更低但检索质量略低 [核心概念](../../raw/application-user-guide/memory-library-overview/overview/concepts.md) |
| `top_k` | 检索最大返回条数 | `10`（API） / `5`（OpenClaw 插件） | 取值范围 1–100；过高易引入噪声，过低可能漏召 |
| `min_score` | 相似度阈值（0.0–1.0） | `0.3`（API） / `0`（OpenClaw 插件） | 建议设为 `0.5–0.7` 平衡精度与召回率；低于阈值的记忆被过滤 [管理记忆](../../raw/application-user-guide/memory-library-overview/create-memory/manage-memory.md) |
| `meta_data` | 自定义元数据 | 可选 | 强烈建议用于分类管理（如 `{"source": "chat", "priority": "high"}`），提升后续精确检索能力 [管理记忆](../../raw/application-user-guide/memory-library-overview/create-memory/manage-memory.md) |

## 使用方式

1. **快速接入**：开通服务后，使用默认记忆库 + `DASHSCOPE_API_KEY`，3 步完成闭环：  
   - 写入：调用 `POST /add` 传入 `messages` 和 `user_id`；  
   - 查看：控制台输入 `user_id` 查看提取结果，或调用 `GET /memory_nodes` 分页列表；  
   - 检索：调用 `POST /memory_nodes/search` 传入当前 `messages` 触发语义召回。示例见[快速开始](../../raw/application-user-guide/memory-library-overview/overview/quickstart.md)。  
2. **自定义规则**：创建新记忆库后，在控制台配置最多 50 条事实记忆规则和 50 条用户画像规则，定义抽取指令、过期时间及策略版本 [配置记忆规则](../../raw/application-user-guide/memory-library-overview/create-memory/configure-rules.md)。  
3. **集成路径**：  
   - **Agent Harness**：在百炼智能体控制台直接绑定记忆库，零代码启用跨会话记忆；  
   - **插件模式**：如 OpenClaw，通过生命周期钩子（`before_agent_start`/`agent_end`）自动捕获与召回，同时暴露 `memory_search`、`memory_store` 等工具供 Agent 主动调用 [集成方式概览](../../raw/application-user-guide/memory-library-overview/integration-overview.md)。

## 限制和注意事项

- **限流**：阿里云账号级别全局限流——全部接口合计 ≤ 3000 QPM；`/add` 接口 ≤ 120 QPM；`/memory_nodes/search` 接口 ≤ 300 QPM。超限返回 HTTP `429`，需实现退避重试 [限流说明](../../raw/application-user-guide/memory-library-overview/integration-overview/limits.md)。  
- **商业化时间点**：记忆库将于 **2026 年 8 月 20 日 10:00（北京时间）** 正式计费，Add/Search 调用区分 Pro/Lite 版本定价，免费额度（1500次Add+5000次Search）自该日起 3 个月内有效 [计费说明](../../raw/application-user-guide/memory-library-overview/integration-overview/billing.md)。  
- **默认记忆库不可删除**：每个账号自带一个默认记忆库，仅可编辑名称、描述及规则，不可删除；其预置的“默认项目”规则有效期为 180 天，可修改但不可删除 [创建与删除记忆库](../../raw/application-user-guide/memory-library-overview/create-memory.md)。  
- **Rerank 依赖**：`min_score` 仅对 Pro 版本生效；Lite 版本因关闭 Rerank，实际相似度分数可能偏低，此时 `min_score` 过滤效果有限，建议优先用 `top_k` 控制召回量。

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


