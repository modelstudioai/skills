# memory library [overview](overview.md)

记忆库是百炼平台为大模型提供的跨会话长期记忆服务，通过自动从对话中提取关键信息并持久化存储为事实记忆与用户画像，在后续对话中基于语义检索相关记忆并注入上下文，使智能体具备持续理解用户偏好和历史行为的能力。它以 `user_id` 为隔离维度，支持多应用共享、规则可配置、API 全开放，适用于个性化推荐、场景化助手等需要状态延续的智能体应用。

## 支持的模型/功能

记忆库不依赖特定大模型，所有能力由百炼统一后端服务实现，与前端调用的模型解耦。核心功能包括：

- **事实记忆**：自动从对话中提取动态事件信息（如“用户每天上午9点需要喝水提醒”），支持按规则配置抽取指令、过期时间（7天/30天/180天/永不过期）和策略版本（Pro/Lite）；  
- **用户画像**：基于预定义模板提取结构化用户属性（如年龄、职业、爱好），字段支持初始值、描述引导及独立策略版本控制；  
- **混合使用**：事实记忆记录临时性、事件性信息，用户画像承载稳定性、结构性属性，二者可共存于同一记忆实体，协同增强上下文质量；  
- **插件集成**：除直接 API 调用外，支持通过 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/best-practices/modelstudio-memory-for-openclaw.md) 等方式无缝嵌入工作流或 Agent Harness，实现自动捕获（`autoCapture`）与自动召回（`autoRecall`）。

> **注意**：文档 3 中提出的“记忆片段（MemoryNode）”与“记忆变量”概念，与文档 1/4/10 定义的“事实记忆”和“用户画像”存在术语不一致。当前统一采用 **事实记忆**（对应 MemoryNode）和 **用户画像**（对应 Profile Schema）作为标准术语，[核心概念](../../raw/application-user-guide/memory-library-overview/memory/concepts.md) 文档已明确此定义，开发应以此为准。

## 关键参数

| 参数 | 说明 | 取值范围/默认值 | 备注 |
|------|------|------------------|------|
| `user_id` | 记忆实体唯一标识，用于跨会话隔离 | 字符串 | 必填，所有读写操作均以此为作用域 |
| `plan_version` | 控制 Add/Search 的策略版本 | `"Pro"`（默认）、`"Lite"` | Add 版本由记忆规则 `plan_version` 决定；Search 版本由请求参数独立控制，详见[计费说明](../../raw/application-user-guide/memory-library-overview/integration-overview/billing.md) |
| `top_k` | 检索最大返回条数 | 1–100，默认 10 | 控制召回规模，影响 [Token](../concepts/token.md) 开销与响应延迟 |
| `min_score` | 相似度阈值（Pro 版生效） | 0.0–1.0，默认 0.3 | 建议设为 `0.5–0.7` 平衡查全率与查准率；Lite 版忽略该参数 |
| `messages` | 对话上下文输入 | 数组，含 `role` 和 `content` | Add 接口用于提取记忆；Search 接口用于生成查询向量 |

## 使用方式

### 1. 快速启动（默认记忆库）
无需创建，开箱即用：
- **写入**：调用 `POST /add`，传入 `user_id` 和 `messages`（见[快速开始](../../raw/application-user-guide/memory-library-overview/memory/quickstart.md)）；
- **检索**：调用 `POST /memory_nodes/search`，传入 `user_id` 和当前 `messages`，结果可直接拼接至 Prompt；
- **查看/调试**：在控制台[记忆库详情页](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list)的“记忆详情”与“记忆检索”标签页操作。

### 2. 自定义记忆库与规则
- 创建新记忆库：控制台点击“创建记忆库”，填写名称与描述；
- 配置规则：在记忆库详情页 → “记忆规则”标签页，分别添加最多 50 条事实记忆规则与 50 条用户画像规则；
- 用户画像需先调用 `CreateProfileSchema` 创建模板，再在 `AddMemory` 中通过 `profile_schema` 参数指定模板 ID，系统自动提取结构化属性（参见[使用用户画像](../../raw/application-user-guide/memory-library-overview/create-memory/user-profile.md)）。

### 3. SDK 与 CLI
- Python：安装 `agentscope-runtime`，使用 `AddMemory`、`SearchMemory`、`ListMemory` 等工具类；
- CLI：OpenClaw 插件提供 `openclaw modelstudio-memory search` 等命令，支持本地调试。

## 限制和注意事项

- **限流**：全部接口总计 ≤3000 QPM（阿里云账号级别）；`AddMemory` ≤120 QPM；`SearchMemory` ≤300 QPM。超限返回 HTTP `429`，需实现退避重试（见[限流说明](../../raw/application-user-guide/memory-library-overview/integration-overview/limits.md)）；
- **商业化时间点**：记忆库将于 **2026 年 8 月 20 日 10:00（北京时间）** 正式计费，此前为免费试用期；
- **默认记忆库不可删除**：仅可编辑名称、描述及规则，其预置的“默认项目”规则可修改但不可删除；
- **异步行为**：用户画像提取为异步过程，首次 `GetUserProfile` 可能返回空值，需按业务逻辑重试（如等待 3 秒后查询）；
- **存储成本**：记忆存储按 `¥0.002/万条/小时` 计费，长期有效；检索与写入费用因 Pro/Lite 版本差异显著（如 Search Lite 为 ¥0.00002/次，Pro 为 ¥0.001/次），高频场景务必评估成本。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)
- [长期记忆](../../raw/application-user-guide/memory-library-overview/memory/long-term-memory.md)
- [核心概念](../../raw/application-user-guide/memory-library-overview/memory/concepts.md)
- [创建与删除记忆库](../../raw/application-user-guide/memory-library-overview/create-memory.md)
- [配置记忆规则](../../raw/application-user-guide/memory-library-overview/create-memory/configure-rules.md)
- [使用用户画像](../../raw/application-user-guide/memory-library-overview/create-memory/user-profile.md)
- [管理记忆](../../raw/application-user-guide/memory-library-overview/create-memory/manage-memory.md)
- [集成方式概览](../../raw/application-user-guide/memory-library-overview/integration-overview.md)
- [记忆库概览](../../raw/application-user-guide/memory-library-overview/memory.md)
- [限流说明](../../raw/application-user-guide/memory-library-overview/integration-overview/limits.md)
- [常见问题](../../raw/application-user-guide/memory-library-overview/integration-overview/faq.md)
- [最佳实践](../../raw/application-user-guide/memory-library-overview/best-practices.md)
- [快速开始](../../raw/application-user-guide/memory-library-overview/memory/quickstart.md)
- [计费说明](../../raw/application-user-guide/memory-library-overview/integration-overview/billing.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/best-practices/modelstudio-memory-for-openclaw.md)


