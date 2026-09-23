# memory library [overview](overview.md)

记忆库是为大模型提供跨会话[长期记忆](../concepts/memory.md)的 API 服务，通过自动从对话中提取关键信息并持久化存储为**事实记忆**（动态事件）和**用户画像**（结构化属性），在后续对话中基于语义检索相关记忆并注入上下文，解决大模型上下文窗口限制导致的“每次对话从零开始”问题。它支持多应用共享、细粒度规则配置与策略版本控制，适用于个性化智能体、工作流增强等场景。

## 支持的模型/功能

- **两类核心记忆类型**：  
  - **事实记忆**：自动从对话中提取的关键事件（如“用户每天上午9点需要喝水提醒”），适用于动态、时效性信息；  
  - **用户画像**：基于预定义模板提取的结构化用户属性（如年龄、职业、爱好），适用于固定、长期稳定的用户特征。二者可并存使用，互为补充。  
- **完整生命周期管理**：支持记忆的写入（`AddMemory`）、异步抽取（`AddMemoryAsync`）、语义检索（`SearchMemory`）、分页查询（`ListMemory`）、更新（`UpdateMemory`）、删除（`DeleteMemory`）及导出（`GetSkillExport`）；  
- **用户画像全链路支持**：提供 `CreateProfileSchema`、`GetUserProfile` 等接口，支持模板创建、对话中自动提取、异步获取结构化画像；  
- **集成路径灵活**：既可通过 **Agent Harness** 在百炼智能体中零代码启用，也支持以 **插件** 形式嵌入 OpenClaw 等工作流系统，实现自动捕获（`autoCapture`）与自动召回（`autoRecall`）[为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/best-practices/modelstudio-memory-for-openclaw.md)。

## 关键参数

- `user_id`：记忆实体 ID，用于跨会话、跨请求的记忆隔离，是所有读写操作的必需维度；  
- `plan_version`：控制 Pro/Lite 策略版本，**Add 调用**由记忆规则配置决定，**Search 调用**由请求参数独立控制（不传默认 `Pro`）；  
- `top_k`：检索最大召回数量（1–100），默认值未显式声明，但控制台调试建议设为 5–10；  
- `min_score`：相似度阈值（0.0–1.0），仅 Pro 版本生效，默认 `0.3`，推荐业务侧设为 `0.5–0.7` 以平衡查全率与查准率 [管理记忆](../../raw/application-user-guide/memory-library-overview/create-memory/manage-memory.md)；  
- `profile_schema`：调用 `AddMemory` 时传入的画像模板 ID，缺失则不触发画像提取；  
- `memoryLibraryId` / `projectId`：插件配置中可选参数，用于指定自定义记忆库或规则，不传则自动选用默认记忆库及默认规则 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/best-practices/modelstudio-memory-for-openclaw.md)。

> **注意**：文档 16 中提出的“记忆片段（MemoryNode）”与“记忆变量”概念，与文档 1–7 定义的“事实记忆”和“用户画像”存在术语不一致。前者属旧版[长期记忆](../concepts/memory.md)功能表述，后者为当前记忆库统一架构下的标准术语。实际开发应以 [核心概念](../../raw/application-user-guide/memory-library-overview/memory/concepts.md) 中定义的“事实记忆”和“用户画像”为准，避免混淆。

## 使用方式

1. **开通与准备**：进入百炼控制台记忆库页面开通服务，获取 `DASHSCOPE_API_KEY`；  
2. **写入记忆**：调用 `AddMemory`，传入 `user_id` 和对话 `messages`，系统自动提取事实记忆；若需画像，须同时传入 `profile_schema`；  
3. **检索记忆**：调用 `SearchMemory`，传入 `user_id` 和当前 `messages`，结果可直接注入 Prompt；  
4. **查看与调试**：在控制台**记忆详情**标签页按 `user_id` 查看记忆内容，在**记忆检索**标签页调整 `min_score`、`top_k` 等参数优化效果；  
5. **高级管理**：通过 `ListMemory` 分页查询、`UpdateMemory` 修改内容、`DeleteMemory` 清理过期记忆；用户画像需先 `CreateProfileSchema` 再 `GetUserProfile` 获取。

## 限制和注意事项

- **限流**：全部 API 接口总计 ≤ 3000 QPM（阿里云账号级别）；`AddMemory` ≤ 120 QPM；`SearchMemory` ≤ 300 QPM [限流说明](../../raw/application-user-guide/memory-library-overview/integration-overview/limits.md)；  
- **商业化时间点**：记忆库将于 **2026 年 8 月 20 日 10:00（北京时间）** 正式计费，此前为免费试用期；  
- **免费额度**：商业化后赠送 1,500 次 Add（含 6 类规格）、5,000 次 Search（Pro/Lite 各 2,500 次）及 10,000 条长期存储，均自生效日起 3 个月内有效；  
- **默认记忆库不可删除**：每个账号自带一个默认记忆库，仅可编辑名称、描述及规则，不可删除；  
- **异步行为需重试**：用户画像提取为异步过程，首次 `GetUserProfile` 可能返回空值，需按业务逻辑实现重试 [使用用户画像](../../raw/application-user-guide/memory-library-overview/create-memory/user-profile.md)；  
- **策略版本切换影响范围**：修改记忆规则的 `plan_version` 后，**仅新写入的记忆**遵循新策略，已写入记忆的存储与检索行为不受影响。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)
- [快速开始](../../raw/application-user-guide/memory-library-overview/memory/quickstart.md)
- [核心概念](../../raw/application-user-guide/memory-library-overview/memory/concepts.md)
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
- [记忆库概览](../../raw/application-user-guide/memory-library-overview/memory.md)
- [长期记忆](../../raw/application-user-guide/memory-library-overview/memory/long-term-memory.md)


