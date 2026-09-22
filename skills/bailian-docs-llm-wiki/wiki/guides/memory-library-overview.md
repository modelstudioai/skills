# memory library [overview](overview.md)

记忆库是为大模型提供跨会话[长期记忆](../concepts/memory.md)的 API 服务，通过自动从对话中提取关键信息并持久化存储为**事实记忆**（动态事件）和**用户画像**（结构化属性），在后续对话中基于语义检索相关记忆并注入上下文，从而突破上下文窗口限制，实现个性化、连贯的智能体交互。它以 `user_id` 为隔离维度，支持多应用共享或细粒度业务隔离，并提供完整的开放接口与控制台管理能力。

## 支持的模型/功能

- **两类核心记忆类型**：  
  - **事实记忆**：自动从对话消息中提取关键事件（如“每天上午9点提醒我喝水”），适用于动态、时效性强的信息；  
  - **用户画像**：基于预定义模板提取结构化属性（如年龄、职业、偏好），适用于相对稳定的用户特征。二者可同时使用，互补增强记忆表达能力。  
- **双模态集成路径**：支持 **Agent Harness**（百炼智能体原生集成）和 **插件**（如 OpenClaw 工作流插件）两种方式接入，详见[集成方式概览](../../raw/application-user-guide/memory-library-overview/integration-overview.md)。  
- **自动记忆生命周期管理**：插件模式下支持 `autoCapture`（对话结束自动提取）与 `autoRecall`（对话开始前自动检索注入），显著降低开发负担 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/best-practices/modelstudio-memory-for-openclaw.md)。

> **注意**：文档 4 中提出的“记忆片段（MemoryNode）”与“记忆变量”概念，与当前统一术语体系存在不一致——新版文档（如[核心概念](../../raw/application-user-guide/memory-library-overview/memory/concepts.md)）已明确采用“事实记忆”和“用户画像”作为标准术语，且“记忆变量”未在 API 接口或控制台配置项中体现，应视为历史表述，以当前 API 和控制台为准。

## 关键参数

- `user_id`：记忆实体唯一标识符，用于跨请求隔离用户数据，是所有读写操作的必需字段。  
- `plan_version`：控制策略版本，取值 `Pro` 或 `Lite`：  
  - **Add 调用**：由记忆规则（project）的 `plan_version` 决定，创建/更新规则时配置；  
  - **Search 调用**：由请求参数 `plan_version` 独立控制，不传默认 `Pro`；  
  - `Pro` 版本启用 Rerank 重排序，检索质量更高；`Lite` 版本跳过 Rerank，成本更低、延迟更优 [计费说明](../../raw/application-user-guide/memory-library-overview/integration-overview/billing.md)。  
- `min_score`（相似度阈值）：范围 `0.0–1.0`，建议设为 `0.5–0.7`，用于过滤低相关性结果；过低易引入噪声，过高可能漏召 [管理记忆](../../raw/application-user-guide/memory-library-overview/create-memory/manage-memory.md)。  
- `top_k`：单次检索最大返回条数，范围 `1–100`，默认 `10`。  

## 使用方式

1. **快速启动**：使用默认记忆库，3 步完成闭环——调用 `AddMemory` 写入对话 → 在控制台**记忆详情**页按 `user_id` 查看 → 调用 `SearchMemory` 检索并注入 Prompt [快速开始](../../raw/application-user-guide/memory-library-overview/memory/quickstart.md)。  
2. **自定义规则**：创建新记忆库后，在**记忆规则**标签页配置最多 50 条事实记忆规则（含过期时间、指令、策略版本）和 50 条用户画像规则（含字段名、描述、初始值） [配置记忆规则](../../raw/application-user-guide/memory-library-overview/create-memory/configure-rules.md)。  
3. **用户画像全流程**：先调用 `CreateProfileSchema` 创建模板，再在 `AddMemory` 请求中传入 `profile_schema` 参数触发结构化抽取，最后调用 `GetUserProfile` 获取结果（需等待约 3 秒异步处理完成） [使用用户画像](../../raw/application-user-guide/memory-library-overview/create-memory/user-profile.md)。  
4. **高级调试**：在控制台**记忆检索**标签页可实时调整 `top_k`、`min_score`、开启“意图判别召回”“改写”“排序”等参数，优化召回效果 [管理记忆](../../raw/application-user-guide/memory-library-overview/create-memory/manage-memory.md)。

## 限制和注意事项

- **限流策略**（阿里云账号级别）：  
  - 全部接口总计 ≤ 3000 QPM；  
  - `AddMemory` ≤ 120 QPM；  
  - `SearchMemory` ≤ 300 QPM；  
  超出返回 HTTP `429`，需实现退避重试 [限流说明](../../raw/application-user-guide/memory-library-overview/integration-overview/limits.md)。  
- **存储与生命周期**：  
  - 默认记忆库不可删除，但可编辑名称、描述及规则；  
  - 记忆内容默认永不过期，除非在创建规则时显式设置过期时间（如 7/30/180 天）；  
  - 删除记忆库将**永久清除所有内容且不可恢复** [创建与删除记忆库](../../raw/application-user-guide/memory-library-overview/create-memory.md)。  
- **商业化与计费**：  
  - 自 **2026 年 8 月 20 日 10:00（北京时间）** 起正式计费；  
  - 免费额度含 1,500 次 Add（分 6 类规格）、5,000 次 Search（分 2 类规格），均限 3 个月内有效；存储 10,000 条长期免费 [计费说明](../../raw/application-user-guide/memory-library-overview/integration-overview/billing.md)。  
- **技术约束**：  
  - `GetUserProfile` 为异步操作，调用 `AddMemory` 后需等待约 3 秒再获取结果；  
  - 检索结果注入 Prompt 会产生额外 [Token](../concepts/token.md) 消耗，该部分费用独立于记忆 API 费用。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)
- [记忆库概览](../../raw/application-user-guide/memory-library-overview/memory.md)
- [长期记忆](../../raw/application-user-guide/memory-library-overview/memory/long-term-memory.md)
- [快速开始](../../raw/application-user-guide/memory-library-overview/memory/quickstart.md)
- [核心概念](../../raw/application-user-guide/memory-library-overview/memory/concepts.md)
- [使用用户画像](../../raw/application-user-guide/memory-library-overview/create-memory/user-profile.md)
- [管理记忆](../../raw/application-user-guide/memory-library-overview/create-memory/manage-memory.md)
- [集成方式概览](../../raw/application-user-guide/memory-library-overview/integration-overview.md)
- [计费说明](../../raw/application-user-guide/memory-library-overview/integration-overview/billing.md)
- [限流说明](../../raw/application-user-guide/memory-library-overview/integration-overview/limits.md)
- [常见问题](../../raw/application-user-guide/memory-library-overview/integration-overview/faq.md)
- [最佳实践](../../raw/application-user-guide/memory-library-overview/best-practices.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/best-practices/modelstudio-memory-for-openclaw.md)
- [创建与删除记忆库](../../raw/application-user-guide/memory-library-overview/create-memory.md)
- [配置记忆规则](../../raw/application-user-guide/memory-library-overview/create-memory/configure-rules.md)


