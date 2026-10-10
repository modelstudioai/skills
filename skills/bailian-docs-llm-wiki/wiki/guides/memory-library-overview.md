# memory library [overview](overview.md)

记忆库是百炼平台为大模型提供的跨会话长期记忆服务，通过自动从对话中提取关键信息并持久化存储，解决大模型上下文窗口限制导致的“每次对话从零开始”问题。它支持两种核心记忆类型——动态的**事实记忆**和结构化的**用户画像**，并在后续对话中基于语义检索相关记忆、注入 Prompt，实现个性化、连贯的智能体交互。所有能力均通过标准化 REST API 暴露，可无缝集成至 Agent Harness 或工作流插件。

## 支持的模型/功能

- **事实记忆**：自动从 `messages` 对话流中提取事件性信息（如“每天上午9点提醒喝水”），支持按规则指令抽取、自动更新与过期管理。  
- **用户画像**：基于预定义模板（`profile_schema`）提取结构化属性（如年龄、职业、爱好），需显式传入 `profile_schema_id` 触发抽取。  
- **双策略版本支持**：Add 和 Search 接口均支持 `Pro`（开启 Rerank，质量高）与 `Lite`（关闭 Rerank，成本低）两种策略版本，适用于不同精度与成本诉求场景 [计费说明](../../raw/application-user-guide/memory-library-overview/integration-overview/billing.md)。  
- **集成路径**：提供 **Agent Harness**（控制台一键配置，面向百炼原生智能体）和 **插件**（如 OpenClaw 插件，面向工作流应用）两种接入方式 [集成方式概览](../../raw/application-user-guide/memory-library-overview/integration-overview.md)。  
> **注意**：文档 15 中 OpenClaw 插件的 `minScore` 参数单位为 `0–100`（整数），而其他所有 API 文档（如文档 4、8）明确要求 `min_score` 为 `0.0–1.0`（浮点数）。实际调用应以 API 参考文档为准，使用 `0.0–1.0` 范围。

## 关键参数

| 参数 | 说明 | 默认值 | 注意事项 |
|------|------|--------|----------|
| `user_id` | 记忆实体 ID，用于跨会话隔离与检索 | 必填 | 是所有读写操作的必需维度，不同 `user_id` 完全隔离 |
| `plan_version` | 控制 Add/Search 的策略版本 | `Pro` | Add 的版本由记忆规则配置决定；Search 的版本由请求参数独立控制，与规则无关 [核心概念](../../raw/application-user-guide/memory-library-overview/overview/concepts.md) |
| `top_k` | 检索最大召回条数 | `10`（API） / `5`（OpenClaw 插件） | 取值范围 `1–100`，过高可能引入噪声 |
| `min_score` | 相似度阈值（过滤低相关性结果） | `0.3`（API） / `0`（OpenClaw 插件） | 建议 `0.5–0.7`；`0.0` 表示不过滤，`1.0` 表示仅返回完全匹配项 |
| `profile_schema` | 用户画像模板 ID | 选填 | 仅当需触发画像抽取时必传；不传则仅处理事实记忆 |

## 使用方式

1. **快速验证**：使用默认记忆库，三步完成闭环：  
   - 调用 `POST /add` 写入对话（含 `user_id` 和 `messages`）；  
   - 调用 `GET /memory_nodes?user_id=xxx` 列出记忆；  
   - 调用 `POST /memory_nodes/search` 检索（传入 `user_id` 和当前 `messages`）[快速开始](../../raw/application-user-guide/memory-library-overview/overview/quickstart.md)。  
2. **自定义规则**：在控制台创建新记忆库 → 配置事实记忆规则（设定有效期、`plan_version`）或用户画像规则（定义字段名/描述/初始值）→ 在 `AddMemory` 请求中指定 `profile_schema` 即可启用画像抽取。  
3. **生产集成**：  
   - 百炼智能体：直接在 Agent 配置页绑定记忆库；  
   - 工作流/外部系统：调用长期记忆 API（服务地址 `https://dashscope.aliyuncs.com/api/v2/apps/memory/`），使用 `DASHSCOPE_API_KEY` 鉴权 [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。

## 限制和注意事项

- **限流**：API 为阿里云账号级别限流——全部接口合计 ≤ 3000 QPM；`/add` ≤ 120 QPM；`/memory_nodes/search` ≤ 300 QPM。超限返回 `429`，需实现退避重试 [限流说明](../../raw/application-user-guide/memory-library-overview/integration-overview/limits.md)。  
- **默认记忆库**：每个账号自带一个，不可删除，但可编辑名称、描述及规则；已预置一条“默认项目”事实记忆规则（有效期 180 天）[创建与删除记忆库](../../raw/application-user-guide/memory-library-overview/create-memory.md)。  
- **商业化时间点**：记忆库将于 **2026 年 8 月 20 日 10:00（北京时间）** 正式计费，此前为免费体验期 [记忆库概览](../../raw/application-user-guide/memory-library-overview/overview.md)。  
- **异步行为**：用户画像提取为异步过程，`AddMemory` 返回后需等待数秒再调用 `GetUserProfile` 查询结果；事实记忆写入后可立即检索。  
- **存储有效期**：未配置过期时间的记忆永久保留；已配置的按规则设置（如 7/30/180 天）自动清理。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [记忆库概览](../../raw/application-user-guide/memory-library-overview/overview.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)
- [快速开始](../../raw/application-user-guide/memory-library-overview/overview/quickstart.md)
- [核心概念](../../raw/application-user-guide/memory-library-overview/overview/concepts.md)
- [配置记忆规则](../../raw/application-user-guide/memory-library-overview/create-memory/configure-rules.md)
- [创建与删除记忆库](../../raw/application-user-guide/memory-library-overview/create-memory.md)
- [管理记忆](../../raw/application-user-guide/memory-library-overview/create-memory/manage-memory.md)
- [使用用户画像](../../raw/application-user-guide/memory-library-overview/create-memory/user-profile.md)
- [集成方式概览](../../raw/application-user-guide/memory-library-overview/integration-overview.md)
- [计费说明](../../raw/application-user-guide/memory-library-overview/integration-overview/billing.md)
- [限流说明](../../raw/application-user-guide/memory-library-overview/integration-overview/limits.md)
- [最佳实践](../../raw/application-user-guide/memory-library-overview/best-practices.md)
- [常见问题](../../raw/application-user-guide/memory-library-overview/integration-overview/faq.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/best-practices/modelstudio-memory-for-openclaw.md)


