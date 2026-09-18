# memory library [overview](overview.md)

记忆库是百炼平台为大模型提供的跨会话[长期记忆](../concepts/memory.md)服务，通过自动从对话中提取关键信息并持久化存储，解决大模型上下文窗口限制导致的“每次对话都从零开始”问题。它支持事实记忆（动态事件）和用户画像（结构化属性）两类内容，并基于语义检索将相关记忆注入后续对话上下文，使智能体具备持续理解用户偏好与历史的能力。该服务以 API 为核心，同时支持控制台配置与插件集成。

## 支持的模型/功能

- **两类核心记忆类型**：  
  - **事实记忆**：自动从对话中提取的关键事件信息（如“用户每天上午9点需要喝水提醒”），适用于动态、时效性强的信息；  
  - **用户画像**：基于预定义模板提取的结构化用户属性（如年龄、职业、爱好），适用于相对稳定的固定属性。二者可并存使用，协同构建完整用户认知。  
- **两种集成路径**：  
  - **Agent Harness**：直接在百炼智能体控制台启用，零代码配置，适合快速接入；  
  - **插件模式**：为 OpenClaw 等工作流应用提供 `memory_search`、`memory_store` 等工具接口，支持自动捕获（`autoCapture`）与自动召回（`autoRecall`）[为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/best-practices/modelstudio-memory-for-openclaw.md)。  
- **统一 API 能力**：覆盖记忆全生命周期操作，包括写入（`AddMemory`）、语义检索（`SearchMemory`）、分页列表（`ListMemory`）、更新（`UpdateMemory`）、删除（`DeleteMemory`），以及用户画像模板管理（`CreateProfileSchema`）与画像获取（`GetUserProfile`）[长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。

## 关键参数

- **`user_id`**：记忆实体唯一标识符，用于实现用户级隔离。不同 `user_id` 的记忆完全独立，是所有读写操作的必传维度。  
- **`plan_version`**：控制 Pro/Lite 策略版本，影响计费与质量：  
  - **Pro**：开启 Rerank 重排序，检索质量更高，适用于对回答准确性要求高的场景；  
  - **Lite**：跳过 Rerank，成本更低，适用于高频调用、成本敏感场景。  
  > **注意**：`Add` 调用的 `plan_version` 由记忆规则配置决定（创建时指定），而 `Search` 调用的 `plan_version` 由请求参数独立控制，不传时默认 `Pro`；两者策略解耦，但文档 11 与文档 5 对 `Search` 默认行为的描述一致，无矛盾。  
- **`min_score`（相似度阈值）**：取值范围 `0.0–1.0`，用于过滤低相关性记忆，推荐设置为 `0.5–0.7`。过低易引入噪声，过高可能漏召相关记忆 [管理记忆](../../raw/application-user-guide/memory-library-overview/create-memory/manage-memory.md)。  
- **`top_k`**：单次检索返回的最大记忆条数，范围 `1–100`，需按业务精度需求权衡。  
- **`profile_schema`**：用户画像模板 ID，调用 `AddMemory` 时必须显式传入才能触发画像字段提取；未传则仅生成事实记忆。

## 使用方式

1. **开通与准备**：首次使用需在[百炼控制台记忆库页面](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list)点击**立即开通**，并获取 `DASHSCOPE_API_KEY`。  
2. **写入记忆**：调用 `AddMemory` 接口，传入 `user_id` 和对话消息数组（`messages`）。系统自动提取事实记忆；若需提取画像，须额外传入 `profile_schema`。  
3. **检索记忆**：调用 `SearchMemory` 接口，传入 `user_id` 和当前用户提问（`messages`），可选配 `top_k`、`min_score`、`plan_version` 等参数。检索结果需手动注入 Prompt 才能被大模型使用。  
4. **查看与调试**：在控制台**记忆详情**标签页按 `user_id` 查看已写入的记忆；在**记忆检索**标签页交互式调试，调整相似度阈值、开启改写/排序等优化召回效果。  
5. **高级操作**：通过 `ListMemory` 分页查询、`UpdateMemory` 修改内容、`DeleteMemory` 删除指定记忆；用户画像需先 `CreateProfileSchema` 创建模板，再 `GetUserProfile` 获取结构化结果。

## 限制和注意事项

- **商业化与计费**：记忆库将于 **2026 年 8 月 20 日 10:00（北京时间）** 正式开始商业化计费，Add/Search 调用区分 Pro/Lite 版本，存储按万条/小时计费 [计费说明](../../raw/application-user-guide/memory-library-overview/overview/billing.md)。  
- **限流约束**：API 为阿里云账号级别限流——全部接口总计 ≤3000 QPM，其中 `AddMemory` ≤120 QPM，`SearchMemory` ≤300 QPM；超限返回 HTTP `429`，需实现退避重试。  
- **默认记忆库不可删除**：每个账号自带一个默认记忆库，无法删除，但可编辑名称、描述及规则；其预置的“默认项目”规则有效期默认 180 天，可修改。  
- **异步处理延迟**：用户画像提取为异步过程，调用 `AddMemory` 后需等待约 3 秒再调用 `GetUserProfile` 才能获取结果 [使用用户画像](../../raw/application-user-guide/memory-library-overview/create-memory/user-profile.md)。  
- **免费额度有效期**：商业化后赠送的 Add/Search 免费额度自生效日起 **3 个月内有效**，逾期未用自动作废；10,000 条免费存储长期有效。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
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
- [常见问题](../../raw/application-user-guide/memory-library-overview/overview/faq.md)
- [最佳实践](../../raw/application-user-guide/memory-library-overview/best-practices.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/best-practices/modelstudio-memory-for-openclaw.md)
- [限流说明](../../raw/application-user-guide/memory-library-overview/overview/limits.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)


