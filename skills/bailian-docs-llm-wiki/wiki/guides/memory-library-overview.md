# memory library [overview](overview.md)

记忆库是百炼平台为大模型提供的跨会话[长期记忆](../concepts/memory.md)服务，通过自动从对话中提取关键信息并持久化存储，解决大模型上下文窗口限制导致的会话状态丢失问题。它支持两种核心记忆类型——动态的**事实记忆**与结构化的**用户画像**，并在后续对话中基于语义检索相关记忆、注入 Prompt，实现个性化、连贯的智能体交互。所有能力均通过标准化 API 开放，可无缝集成至 Agent Harness 或工作流插件。

## 支持的模型/功能

- **事实记忆**：自动从对话消息（`messages`）中提取事件性信息（如“每天上午9点提醒我喝水”），适用于动态、时效性强的用户指令或行为记录。  
- **用户画像**：基于预定义模板（`profile_schema`）提取结构化属性（如年龄、职业、爱好），适用于需长期稳定维护的用户固有特征。两者可并存使用，互不干扰。  
- **多模态与技能记忆**：除文本外，还支持多模态内容（图像/音频等）及技能型记忆（如工具调用偏好），详见[长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。  
- **集成路径**：提供 **Agent Harness**（控制台一键配置，面向百炼原生智能体）和 **插件**（如 OpenClaw 插件，面向工作流应用）两种接入方式，参见[集成方式概览](../../raw/application-user-guide/memory-library-overview/integration-overview.md)。

> **注意**：文档 13 明确指出“与之前的[长期记忆](../concepts/memory.md)功能相比，记忆库是全面升级版”，而文档 2 和文档 3 均将本服务称为“[长期记忆](../concepts/memory.md) API”或“记忆库”，术语已统一。但需注意：旧版“长期记忆”功能已下线，当前所有文档均指向本记忆库服务，无并存旧版本。

## 关键参数

| 参数 | 说明 | 取值/范围 | 备注 |
|------|------|-----------|------|
| `user_id` | 记忆实体唯一标识，用于隔离不同用户数据 | 字符串 | 必填；所有读写操作均以此为维度隔离 |
| `plan_version` | 控制 Pro/Lite 策略版本 | `"Pro"` / `"Lite"` | **Add 调用**由记忆规则配置决定；**Search 调用**由请求参数独立控制，默认 `"Pro"`；详见[核心概念](../../raw/application-user-guide/memory-library-overview/overview/concepts.md) |
| `top_k` | 检索返回的最大记忆条数 | 1–100 | 默认值未显式声明，但控制台建议设为 5–10，API 示例中常用 `10` |
| `min_score` | 相似度阈值（过滤低相关性结果） | `0.0`–`1.0` | 文档 1 和文档 10 均建议 `0.5`–`0.7`；文档 1 中 `SearchMemory` 示例默认 `0.3`，属保守值，实际推荐提高以减少噪声 |
| `memory_library_id` / `project_id` | 指定记忆库或具体规则 ID | 字符串 | 非必填；不传时自动使用默认记忆库及默认规则 |

## 使用方式

1. **开通与准备**：首次使用需在[百炼控制台记忆库页面](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list)点击**立即开通**，并获取 `DASHSCOPE_API_KEY`。  
2. **写入记忆**：调用 `POST /api/v2/apps/memory/add`，传入 `user_id` 和 `messages` 数组。若需提取用户画像，必须同时传入 `profile_schema` ID。示例见[快速开始](../../raw/application-user-guide/memory-library-overview/overview/quickstart.md)。  
3. **检索记忆**：调用 `POST /api/v2/apps/memory/memory_nodes/search`，传入 `user_id` 和当前 `messages`，系统将语义匹配历史记忆并返回 `memory_nodes` 列表。  
4. **管理记忆**：支持 `GET /memory_nodes`（列表）、`PATCH /memory_nodes/{id}`（更新）、`DELETE /memory_nodes/{id}`（删除）等完整 CRUD 操作，参见[管理记忆](../../raw/application-user-guide/memory-library-overview/create-memory/manage-memory.md)。  

## 限制和注意事项

- **限流**：全部接口总计 ≤ 3000 QPM（阿里云账号级别）；`AddMemory` ≤ 120 QPM；`SearchMemory` ≤ 300 QPM。超限返回 HTTP `429`，需实现退避重试。  
- **计费**：2026 年 8 月 20 日起正式商业化，Add/Search 调用按 Pro/Lite 版本计费（Pro 含 Rerank，Lite 不含），存储按小时计费。免费额度（1500 次 Add + 5000 次 Search）有效期为商业化起 3 个月。详情见[计费说明](../../raw/application-user-guide/memory-library-overview/integration-overview/billing.md)。  
- **异步行为**：用户画像提取为异步过程，调用 `AddMemory` 后需等待数秒再调用 `GetUserProfile`，否则可能返回空值。  
- **默认记忆库**：每个账号自带一个不可删除的默认记忆库，已预置一条有效期 180 天的“默认项目”规则，可编辑但不可删。  
- **相似度阈值实践**：文档 10 明确提示“相似度过高可能漏召，过低可能引入噪声”，结合文档 4 和文档 10 的建议，生产环境应优先尝试 `min_score=0.6` 并根据召回质量微调。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)
- [记忆库概览](../../raw/application-user-guide/memory-library-overview/overview.md)
- [核心概念](../../raw/application-user-guide/memory-library-overview/overview/concepts.md)
- [快速开始](../../raw/application-user-guide/memory-library-overview/overview/quickstart.md)
- [创建与删除记忆库](../../raw/application-user-guide/memory-library-overview/create-memory.md)
- [配置记忆规则](../../raw/application-user-guide/memory-library-overview/create-memory/configure-rules.md)
- [集成方式概览](../../raw/application-user-guide/memory-library-overview/integration-overview.md)
- [使用用户画像](../../raw/application-user-guide/memory-library-overview/create-memory/user-profile.md)
- [管理记忆](../../raw/application-user-guide/memory-library-overview/create-memory/manage-memory.md)
- [计费说明](../../raw/application-user-guide/memory-library-overview/integration-overview/billing.md)
- [限流说明](../../raw/application-user-guide/memory-library-overview/integration-overview/limits.md)
- [常见问题](../../raw/application-user-guide/memory-library-overview/integration-overview/faq.md)
- [最佳实践](../../raw/application-user-guide/memory-library-overview/best-practices.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/best-practices/modelstudio-memory-for-openclaw.md)


