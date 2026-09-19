# memory library [overview](overview.md)

记忆库是百炼平台为大模型提供的跨会话[长期记忆](../concepts/memory.md)服务，通过自动从对话中提取关键信息并持久化存储为事实记忆与用户画像，在后续交互中基于语义检索并注入上下文，使智能体具备持续理解用户偏好和历史信息的能力。它以 `user_id` 为隔离维度，支持多应用共享或独立配置，并提供开放 API 与控制台双路径管理。

## 支持的模型/功能

- **两类记忆内容**：  
  - **事实记忆**：自动从对话中提取动态事件信息（如“用户每天上午9点需要喝水提醒”），适用于临时性、时效性强的上下文；  
  - **用户画像**：基于预定义模板提取结构化用户属性（如年龄、职业、爱好），适用于固定、长期稳定的用户特征。两者可协同使用，[核心概念](../../raw/application-user-guide/memory-library-overview/memory/concepts.md)中对此有明确定义。  
- **双模式集成**：支持 **Agent Harness**（百炼智能体原生集成）与 **插件**（如 OpenClaw 工作流）两种接入方式，详见[集成方式概览](../../raw/application-user-guide/memory-library-overview/overview.md)。  
- **自动记忆生命周期管理**：插件方案（如 `modelstudio-memory-for-openclaw`）支持 `autoCapture`（对话结束自动提取）与 `autoRecall`（对话开始前自动召回），实现零侵入式记忆闭环 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/best-practices/modelstudio-memory-for-openclaw.md)。

> **注意**：文档 4（`long-term-memory.md`）中提出的“记忆片段（MemoryNode）”与“记忆变量”术语，与当前统一术语体系不一致——后者已被“事实记忆”和“用户画像”取代。该文档描述的功能逻辑（如字段级手动配置、模型推理开关）实际已整合进记忆规则中的“用户画像规则”配置流程，开发者应以[配置记忆规则](../../raw/application-user-guide/memory-library-overview/create-memory/configure-rules.md)为准，避免混淆旧概念。

## 关键参数

- **`user_id`**：记忆实体唯一标识符，用于跨会话、跨请求隔离记忆空间，所有读写操作均以此为作用域。  
- **`plan_version`**：控制 Add/Search 调用策略版本的核心参数，取值 `Pro` 或 `Lite`：  
  - `Pro`：开启 Rerank 重排序，检索质量更高，适用于对准确性要求高的场景；  
  - `Lite`：跳过 Rerank，成本更低、延迟更小，适用于高频调用场景。  
  Add 的 `plan_version` 由记忆规则配置决定；Search 的 `plan_version` 由请求参数独立指定（不传默认 `Pro`），二者解耦。详细对比见[计费说明](../../raw/application-user-guide/memory-library-overview/overview/billing.md)。  
- **`min_score`（相似度阈值）**：范围 `0.0–1.0`，用于过滤低相关性结果，建议值 `0.5–0.7`；过低易引入噪声，过高可能漏召。  
- **`top_k`**：单次检索返回的最大记忆条数，取值范围 `1–100`，需按业务精度与 [Token](../concepts/token.md) 成本权衡设置。

## 使用方式

1. **快速验证**：使用默认记忆库，3 步完成端到端流程——调用 `AddMemory` 写入对话 → 控制台或 `ListMemory` 查看 → `SearchMemory` 检索并注入 Prompt [快速开始](../../raw/application-user-guide/memory-library-overview/memory/quickstart.md)。  
2. **自定义配置**：  
   - 创建独立记忆库（非必须，但推荐用于多业务隔离）；  
   - 在**记忆规则**页配置最多 50 条事实记忆规则（含过期时间、`plan_version`）和 50 条用户画像规则（含字段定义、初始值）；  
   - 用户画像需先调用 `CreateProfileSchema` 创建模板，再在 `AddMemory` 中传入 `profile_schema` 参数触发结构化提取。  
3. **API 调用**：全部接口通过 DashScope 网关 `https://dashscope.aliyuncs.com/api/v2/apps/memory/` 提供，支持 RESTful 与 Python SDK（`agentscope-runtime`）两种调用方式，鉴权使用 `DASHSCOPE_API_KEY`。

## 限制和注意事项

- **限流**：阿里云账号级别全局限流——全部接口总计 ≤ 3000 QPM；其中 `AddMemory` ≤ 120 QPM，`SearchMemory` ≤ 300 QPM；超限返回 HTTP `429`，需实现退避重试 [限流说明](../../raw/application-user-guide/memory-library-overview/overview/limits.md)。  
- **商业化与免费额度**：2026 年 8 月 20 日起正式计费，赠送 3 个月免费额度（Add 1500 次、Search 5000 次、存储 10,000 条长期有效），超出部分按 `Pro`/`Lite` 版本单价计费。  
- **异步行为**：用户画像提取为异步过程，调用 `AddMemory` 后需等待约 3 秒再调用 `GetUserProfile` 获取结果，否则可能返回空值。  
- **默认记忆库不可删除**：仅可编辑名称、描述及规则，其预置的“默认项目”规则可修改但不可删除；自定义记忆库可随时删除，且数据不可恢复。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)
- [记忆库概览](../../raw/application-user-guide/memory-library-overview/memory.md)
- [长期记忆](../../raw/application-user-guide/memory-library-overview/memory/long-term-memory.md)
- [快速开始](../../raw/application-user-guide/memory-library-overview/memory/quickstart.md)
- [核心概念](../../raw/application-user-guide/memory-library-overview/memory/concepts.md)
- [创建与删除记忆库](../../raw/application-user-guide/memory-library-overview/create-memory.md)
- [配置记忆规则](../../raw/application-user-guide/memory-library-overview/create-memory/configure-rules.md)
- [管理记忆](../../raw/application-user-guide/memory-library-overview/create-memory/manage-memory.md)
- [集成方式概览](../../raw/application-user-guide/memory-library-overview/overview.md)
- [计费说明](../../raw/application-user-guide/memory-library-overview/overview/billing.md)
- [限流说明](../../raw/application-user-guide/memory-library-overview/overview/limits.md)
- [常见问题](../../raw/application-user-guide/memory-library-overview/overview/faq.md)
- [最佳实践](../../raw/application-user-guide/memory-library-overview/best-practices.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/best-practices/modelstudio-memory-for-openclaw.md)
- [使用用户画像](../../raw/application-user-guide/memory-library-overview/create-memory/user-profile.md)


