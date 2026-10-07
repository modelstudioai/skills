# memory library [overview](overview.md)

记忆库是为大模型提供跨会话[长期记忆](../concepts/memory.md)的 API 服务，通过自动从对话中提取关键信息并持久化存储为**事实记忆**和**用户画像**，在后续对话中基于语义检索相关记忆并注入上下文，从而突破上下文窗口限制，实现个性化、连贯的智能体交互。它以 `user_id` 为隔离维度，支持多应用共享同一记忆库，并提供完整的开放接口与控制台管理能力。

## 支持的模型/功能

- **两类核心记忆类型**：
  - **事实记忆**：自动从对话中提取动态事件信息（如“每天上午9点提醒我喝水”），适用于临时性、时效性信息。
  - **用户画像**：基于预定义模板提取结构化用户属性（如年龄、职业、爱好），适用于固定、长期稳定的用户特征。两者可并行使用，互不干扰。
- **策略版本支持**：Add 和 Search 操作均支持 `Pro`（开启 Rerank，检索质量更高）与 `Lite`（关闭 Rerank，成本更低）两个策略版本，按需选择。详见[计费说明](raw/application-user-guide/memory-library-overview/integration-overview/billing.md)。
- **集成路径**：支持两种主流接入方式——面向百炼智能体的 **Agent Harness**（零代码配置）和面向工作流的 **插件模式**（如 OpenClaw 插件），参见[集成方式概览](raw/application-user-guide/memory-library-overview/integration-overview.md)。

> **注意**：文档 6 与文档 11 均指出 `plan_version` 默认为 `Pro`，但文档 7 的配置界面说明中称“不传默认 Pro”，而文档 11 明确补充“商业化前已存在的规则，`plan_version` 默认为 Pro”。该表述一致，无矛盾；但需注意：**Search 接口的 `plan_version` 由请求参数独立控制，与规则配置无关**，此关键行为在文档 6 和文档 11 中均有强调，而文档 3 的 cURL 示例中误写为 `"plan_version": "Lite"`（应为 `"pro"` 或 `"Pro"`，大小写敏感），实际调用以文档 11 的规范为准。

## 关键参数

| 参数 | 说明 | 取值/范围 | 备注 |
|------|------|-----------|------|
| `user_id` | 记忆实体唯一标识，用于跨会话隔离 | 字符串 | 必填；所有读写操作均以此为作用域 |
| `plan_version` | 控制策略版本 | `"Pro"` / `"Lite"` | Add 调用由记忆规则配置决定；Search 调用由请求参数决定，**不传时默认 `"Pro"`** |
| `top_k` | 检索返回的最大记忆条数 | `1–100` | 默认值未统一（文档 3 示例为 `10`，文档 9 控制台建议为 `10`，文档 14 插件默认为 `5`） |
| `min_score` | 相似度阈值，过滤低相关性结果 | `0.0–1.0` | 文档 6 建议 `0.5–0.7`；文档 9 控制台说明中称“相似度过高可能漏召”，文档 1 的 API 描述中 `min_score` 仅对 Pro 版本生效 |
| `memory_library_id` | 指定目标记忆库 ID | 字符串 | 非必填；不传时使用默认记忆库（文档 1、文档 14） |

## 使用方式

1. **快速上手（3 步）**：  
   - **写入**：调用 `AddMemory`，传入 `messages` 和 `user_id`，系统自动提取事实记忆或画像（需指定 `profile_schema`）；  
   - **查看**：通过控制台[记忆详情](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list)页按 `user_id` 查询，或调用 `ListMemory`；  
   - **检索**：调用 `SearchMemory`，传入当前对话 `messages` 和 `user_id`，获取语义相关记忆片段。完整流程见[快速开始](raw/application-user-guide/memory-library-overview/overview/quickstart.md)。

2. **高级配置**：  
   - 创建自定义记忆库（非必需，但推荐用于业务隔离），并在其下配置最多 50 条事实记忆规则和 50 条用户画像规则；  
   - 用户画像需先调用 `CreateProfileSchema` 创建模板，再在 `AddMemory` 中传入 `profile_schema` 才能触发结构化抽取；  
   - 插件方式（如 OpenClaw）支持全自动捕获（`autoCapture`）与召回（`autoRecall`），无需手动调用 API。

## 限制和注意事项

- **限流**：全部接口总计 ≤ 3000 QPM（账号级）；`AddMemory` ≤ 120 QPM；`SearchMemory` ≤ 300 QPM。超限返回 HTTP `429`，需实现退避重试 [限流说明](raw/application-user-guide/memory-library-overview/integration-overview/limits.md)。
- **默认记忆库**：每个账号自带一个，**不可删除**，但可编辑名称、描述及规则；已预置一条有效期 180 天的“默认项目”事实记忆规则。
- **计费与生命周期**：商业化将于 **2026 年 8 月 20 日 10:00（北京时间）** 启动，届时 Add/Search 调用按 Pro/Lite 版本计费，存储按小时计费；免费额度（1500 次 Add + 5000 次 Search）自商业化日起 3 个月内有效 [计费说明](raw/application-user-guide/memory-library-overview/integration-overview/billing.md)。
- **异步行为**：用户画像提取为异步过程，首次 `GetUserProfile` 可能返回空值，需按业务逻辑重试（文档 10 明确提示）。
- **元数据建议**：推荐使用 `meta_data` 字段对记忆分类，便于后续精确过滤与管理（文档 9）。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)
- [快速开始](../../raw/application-user-guide/memory-library-overview/overview/quickstart.md)
- [记忆库概览](../../raw/application-user-guide/memory-library-overview/overview.md)
- [创建与删除记忆库](../../raw/application-user-guide/memory-library-overview/create-memory.md)
- [核心概念](../../raw/application-user-guide/memory-library-overview/overview/concepts.md)
- [配置记忆规则](../../raw/application-user-guide/memory-library-overview/create-memory/configure-rules.md)
- [集成方式概览](../../raw/application-user-guide/memory-library-overview/integration-overview.md)
- [管理记忆](../../raw/application-user-guide/memory-library-overview/create-memory/manage-memory.md)
- [使用用户画像](../../raw/application-user-guide/memory-library-overview/create-memory/user-profile.md)
- [计费说明](../../raw/application-user-guide/memory-library-overview/integration-overview/billing.md)
- [限流说明](../../raw/application-user-guide/memory-library-overview/integration-overview/limits.md)
- [常见问题](../../raw/application-user-guide/memory-library-overview/integration-overview/faq.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/best-practices/modelstudio-memory-for-openclaw.md)
- [最佳实践](../../raw/application-user-guide/memory-library-overview/best-practices.md)


