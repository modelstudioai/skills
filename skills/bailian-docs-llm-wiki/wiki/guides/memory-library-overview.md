# memory library [overview](overview.md)

记忆库是百炼平台为大模型提供的跨会话[长期记忆](../concepts/memory.md)服务，通过自动从对话中提取关键信息并持久化存储，解决大模型上下文窗口限制导致的“每次对话从零开始”问题。它支持两种核心记忆类型：动态的**事实记忆**（如事件、任务）和结构化的**用户画像**（如年龄、职业），并在后续对话中基于语义检索相关记忆注入 Prompt，实现个性化、连贯的智能体交互。该服务以开放 API 形式提供，可集成至任意应用或工作流。

## 支持的模型/功能

- **两类记忆能力**：  
  - **事实记忆**：自动从 `messages` 中提取关键事件（如“每天上午9点提醒我喝水”），适用于动态、时效性信息；  
  - **用户画像**：基于预定义模板（`profile_schema`）提取结构化属性（如“年龄=28，爱好=足球”），适用于固定用户属性。二者可同时启用，互不干扰。  
- **双策略版本支持**：Add 和 Search 操作均支持 `Pro`（开启 Rerank，高精度）与 `Lite`（关闭 Rerank，低成本）两个策略版本，按需选择以平衡效果与成本 [计费说明](../../raw/application-user-guide/memory-library-overview/integration-overview/billing.md)。  
- **集成路径**：支持 **Agent Harness**（百炼智能体一键配置）与 **插件**（如 OpenClaw 工作流）两种方式，后者通过生命周期钩子（`before_agent_start`/`agent_end`）实现全自动捕获与召回 [集成方式概览](../../raw/application-user-guide/memory-library-overview/integration-overview.md)。  
- **多模态扩展**：除文本外，还支持事实记忆多模态（Pro 专属）及技能记忆等高级类型，详见 [计费说明](../../raw/application-user-guide/memory-library-overview/integration-overview/billing.md)。

> **注意**：文档 13 明确指出“生成的事实记忆与用户画像暂无失效日期（除非在创建记忆库时配置了记忆过期时间）”，但文档 1 和文档 6 均强调默认记忆规则“默认有效期 180 天”。此处以控制台实际配置为准——**记忆过期时间由每条记忆规则独立设置，未显式配置则永不过期**；默认规则的 180 天仅为初始值，非全局强制策略。

## 关键参数

| 参数 | 说明 | 默认值 | 注意事项 |
|------|------|--------|----------|
| `user_id` | 记忆实体 ID，用于隔离不同用户数据 | 必填 | 是所有读写操作的必需维度，不同 `user_id` 完全隔离 |
| `plan_version` | 控制策略版本（`Pro`/`Lite`） | `Pro` | **Add 调用**由记忆规则的 `plan_version` 决定；**Search 调用**由请求参数独立控制，两者解耦 [核心概念](../../raw/application-user-guide/memory-library-overview/overview/concepts.md) |
| `top_k` | 检索最大返回条数 | `10`（API） / `5`（OpenClaw 插件） | 取值范围 1–100；过高易引入噪声，过低可能漏召 |
| `min_score` | 相似度阈值（0.0–1.0） | `0.3`（API） / `0`（插件） | 建议设为 `0.5–0.7` 平衡准确率与召回率；仅 `Pro` 版本生效 [管理记忆](../../raw/application-user-guide/memory-library-overview/create-memory/manage-memory.md) |
| `profile_schema` | 用户画像模板 ID | 可选 | 仅当需提取画像时必传；未传则仅处理事实记忆 |

## 使用方式

1. **快速启动（默认记忆库）**：  
   - 开通服务后，调用 `AddMemory` 写入对话（含 `user_id` 和 `messages`）；  
   - 通过 `SearchMemory` 检索（传入 `user_id` 和当前 `messages`）；  
   - 示例见 [快速开始](../../raw/application-user-guide/memory-library-overview/overview/quickstart.md)。  

2. **自定义记忆库与规则**：  
   - 在控制台创建新记忆库，进入 **记忆规则** 标签页配置：  
     - *事实记忆规则*：设置规则指令、自动更新、过期时间、`plan_version`；  
     - *用户画像规则*：定义字段名、描述、初始值及对应 `plan_version`。  
   - 每个记忆库最多支持 50 条事实规则 + 50 条画像规则 [配置记忆规则](../../raw/application-user-guide/memory-library-overview/create-memory/configure-rules.md)。  

3. **用户画像全流程**：  
   - 先调用 `CreateProfileSchema` 创建模板；  
   - `AddMemory` 时传入 `profile_schema` ID 触发结构化抽取；  
   - 异步等待后调用 `GetUserProfile` 获取结果（需重试机制） [使用用户画像](../../raw/application-user-guide/memory-library-overview/create-memory/user-profile.md)。  

4. **插件化集成（OpenClaw）**：  
   - 安装 `@modelstudio/modelstudio-memory-for-openclaw` 插件；  
   - 配置 `apiKey` 和 `userId`，启用 `autoCapture`/`autoRecall`；  
   - Agent 自动完成记忆捕获与注入，无需修改业务逻辑 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/best-practices/modelstudio-memory-for-openclaw.md)。

## 限制和注意事项

- **限流**：阿里云账号级别总限流 3000 QPM；其中 `AddMemory` ≤ 120 QPM，`SearchMemory` ≤ 300 QPM；超限返回 HTTP `429` [限流说明](../../raw/application-user-guide/memory-library-overview/integration-overview/limits.md)。  
- **商业化时间点**：**2026 年 8 月 20 日 10:00（北京时间）起正式计费**，此前为免费体验期；Add/Search 调用区分 Pro/Lite 计费 [计费说明](../../raw/application-user-guide/memory-library-overview/integration-overview/billing.md)。  
- **免费额度**：商业化后赠送 1500 次 Add（分 6 类规格）、5000 次 Search（2 类规格）、10,000 条长期存储（无有效期）；额度 3 个月内有效，逾期作废 [计费说明](../../raw/application-user-guide/memory-library-overview/integration-overview/billing.md)。  
- **默认记忆库**：每个账号自带且**不可删除**，但可编辑名称、描述及规则；其预置的“默认项目”规则可修改但不可删除 [创建与删除记忆库](../../raw/application-user-guide/memory-library-overview/create-memory.md)。  
- **异步行为**：用户画像提取为异步过程，首次 `GetUserProfile` 可能返回空值，需按业务逻辑重试 [使用用户画像](../../raw/application-user-guide/memory-library-overview/create-memory/user-profile.md)。

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


