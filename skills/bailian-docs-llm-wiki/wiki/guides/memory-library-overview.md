# memory library [overview](overview.md)

记忆库是百炼平台为大模型提供的跨会话[长期记忆](../concepts/memory.md)服务，通过自动从对话中提取关键信息并持久化存储为事实记忆与用户画像，在后续对话中基于语义检索并注入上下文，从而突破上下文窗口限制，实现个性化、连贯的智能体交互。它以 API 为核心交付形态，支持灵活集成与多应用共享，适用于需持续理解用户偏好与历史行为的生产场景。

## 支持的模型/功能

- **两类核心记忆类型**：  
  - **事实记忆**：自动从对话中提取动态事件信息（如“用户每天上午9点需要喝水提醒”），适用于临时性、时效性任务；  
  - **用户画像**：基于预定义模板提取结构化用户属性（如年龄、职业、爱好），适用于固定、长期稳定的用户特征。二者可独立使用或协同增强上下文理解。  
- **完整生命周期能力**：覆盖记忆写入（`AddMemory`/`AddMemoryAsync`）、语义检索（`SearchMemory`）、列表查询（`ListMemory`）、详情获取（`GetMemoryNode`）、更新（`UpdateMemory`）与删除（`DeleteMemory`）；用户画像支持模板管理（`CreateProfileSchema`）、异步提取与同步获取（`GetUserProfile`）[长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。  
- **两种集成路径**：支持通过 **Agent Harness**（控制台零代码配置）快速接入百炼智能体，或通过 **插件方式**（如 `modelstudio-memory-for-openclaw`）为工作流注入记忆能力 [集成方式概览](../../raw/application-user-guide/memory-library-overview/integration-overview.md)。

## 关键参数

- `user_id`：记忆实体唯一标识符，用于隔离不同用户的记忆空间，所有读写操作均以此为维度进行数据隔离。  
- `plan_version`：控制 Pro/Lite 策略版本的核心参数：  
  - **Add 调用**的版本由记忆规则中配置的 `plan_version` 决定（创建/更新规则时指定）；  
  - **Search 调用**的版本由请求体中的 `plan_version` 字段独立控制（不传默认 `Pro`）；  
  > **注意**：文档 5 与文档 11 均明确说明 `plan_version` 对 Add/Search 的控制逻辑分离，但文档 4 的 cURL 示例中 `SearchMemory` 请求误写为 `"plan_version": "Lite"`（小写），而实际 API 仅接受 `Pro` 或 `Lite`（首字母大写）。请严格按 [计费说明](../../raw/application-user-guide/memory-library-overview/integration-overview/billing.md) 中的枚举值使用，避免调用失败。  
- `top_k`：控制最大召回数量（1–100），默认值未显式声明，建议显式设置以保障结果可控性；  
- `min_score`：相似度阈值（0.0–1.0），Pro 版本生效，默认 `0.3`；推荐业务侧设为 `0.5–0.7` 以平衡查全率与查准率 [管理记忆](../../raw/application-user-guide/memory-library-overview/create-memory/manage-memory.md)；  
- `profile_schema`：调用 `AddMemory` 时传入画像模板 ID，方可触发用户画像字段提取；不传则仅处理事实记忆。

## 使用方式

1. **开通与准备**：进入[百炼控制台记忆库页面](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list)点击**立即开通**，并确保已获取有效 `DASHSCOPE_API_KEY`；  
2. **写入记忆**：调用 `AddMemory`，传入 `user_id` 与对话 `messages` 数组（含 user/assistant 角色），系统自动提取事实记忆；若需提取画像，须同时传入 `profile_schema`；  
3. **检索记忆**：调用 `SearchMemory`，传入 `user_id` 与当前 `messages`（代表用户最新意图），系统返回语义相关记忆节点；检索结果需由业务方主动注入 Prompt；  
4. **控制台调试**：在记忆库详情页的**记忆检索**标签页可实时调试参数效果，支持开启“意图判别召回”“改写”“排序”等优化开关；  
5. **进阶配置**：通过创建自定义记忆库并配置规则（最多 50 条事实记忆规则 + 50 条用户画像规则），可精细化控制抽取指令、过期时间（7/30/180 天或永不过期）及策略版本 [配置记忆规则](../../raw/application-user-guide/memory-library-overview/create-memory/configure-rules.md)。

## 限制和注意事项

- **限流约束**：全部接口总计 ≤ 3000 QPM（阿里云账号级别）；其中 `AddMemory` ≤ 120 QPM，`SearchMemory` ≤ 300 QPM；超限返回 HTTP `429`，需实现退避重试 [限流说明](../../raw/application-user-guide/memory-library-overview/integration-overview/limits.md)；  
- **商业化时间点**：记忆库将于 **2026 年 8 月 20 日 10:00（北京时间）** 正式开始计费，Add/Search 调用区分 Pro/Lite 版本，免费额度自商业化日起 3 个月内有效 [计费说明](../../raw/application-user-guide/memory-library-overview/integration-overview/billing.md)；  
- **默认记忆库不可删除**：每个账号自带一个默认记忆库，仅可编辑名称、描述及规则，不可删除；新建记忆库可自由增删；  
- **画像提取为异步过程**：调用 `AddMemory` 后，用户画像字段可能延迟数秒才就绪，首次 `GetUserProfile` 可能返回空值，需按业务逻辑重试；  
- **存储成本按小时计费**：记忆存储费用为 ¥0.002/万条/小时（约 ¥1.44/万条/月），长期有效，无有效期限制；  
- **Rerank 模型依赖**：Pro 版本的 `SearchMemory` 依赖 `gte-rerank-v2` 模型进行重排序，该模型为当前唯一支持排序的模型，不可替换。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)
- [记忆库概览](../../raw/application-user-guide/memory-library-overview/overview.md)
- [快速开始](../../raw/application-user-guide/memory-library-overview/overview/quickstart.md)
- [核心概念](../../raw/application-user-guide/memory-library-overview/overview/concepts.md)
- [创建与删除记忆库](../../raw/application-user-guide/memory-library-overview/create-memory.md)
- [配置记忆规则](../../raw/application-user-guide/memory-library-overview/create-memory/configure-rules.md)
- [使用用户画像](../../raw/application-user-guide/memory-library-overview/create-memory/user-profile.md)
- [管理记忆](../../raw/application-user-guide/memory-library-overview/create-memory/manage-memory.md)
- [集成方式概览](../../raw/application-user-guide/memory-library-overview/integration-overview.md)
- [计费说明](../../raw/application-user-guide/memory-library-overview/integration-overview/billing.md)
- [限流说明](../../raw/application-user-guide/memory-library-overview/integration-overview/limits.md)
- [常见问题](../../raw/application-user-guide/memory-library-overview/integration-overview/faq.md)
- [最佳实践](../../raw/application-user-guide/memory-library-overview/best-practices.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/best-practices/modelstudio-memory-for-openclaw.md)


