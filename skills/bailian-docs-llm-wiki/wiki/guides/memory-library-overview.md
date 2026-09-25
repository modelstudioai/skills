# memory library [overview](overview.md)

[记忆](../concepts/memory.md)库是百炼平台为大模型提供的跨会话长期[记忆](../concepts/memory.md)服务，通过自动从对话中提取关键信息并持久化存储为事实[记忆](../concepts/memory.md)和用户画像，在后续交互中基于语义检索并注入上下文，使智能体具备持续理解用户偏好与历史行为的能力。它以 `user_id` 为隔离维度，支持多应用共享或按业务场景独立管理，并提供开放 API 与控制台双路径集成。

## 支持的模型/功能

- **两类核心记忆类型**：
  - **事实记忆**：自动从对话中提取动态事件信息（如“用户每天上午9点需要喝水提醒”），适用于临时性、时效性强的上下文。
  - **用户画像**：基于预定义模板提取结构化用户属性（如年龄、职业、爱好），适用于固定、长期稳定的用户特征。两者可协同使用，[核心概念](../../raw/application-user-guide/memory-library-overview/memory/concepts.md)文档详细说明了其适用边界与组合逻辑。
- **两种集成方式**：支持 **Agent Harness**（面向百炼智能体的零代码配置）和 **插件**（面向 OpenClaw 等工作流的 SDK 集成），详见[集成方式概览](../../raw/application-user-guide/memory-library-overview/integration-overview.md)。
- **自动能力**：通过 `autoCapture`（对话结束自动提取）与 `autoRecall`（对话开始前自动检索）机制实现无感记忆闭环，[为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/best-practices/modelstudio-memory-for-openclaw.md)展示了该能力在真实 Agent 中的落地效果。

> **注意**：文档 4 中将记忆体（Memory）拆分为“记忆片段（MemoryNode）”和“记忆变量”，并强调后者权重更高；而文档 1/3/6/8 统一采用“事实记忆”与“用户画像”的二分法，且未提及“记忆变量”这一术语。当前官方统一术语体系以[核心概念](../../raw/application-user-guide/memory-library-overview/memory/concepts.md)为准，“记忆变量”属于旧版长期记忆功能的遗留表述，新记忆库中对应能力已由“用户画像规则”覆盖。

## 关键参数

- `user_id`：记忆实体 ID，是所有读写操作的隔离主键，不同 `user_id` 的记忆完全隔离。
- `plan_version`：控制策略版本，取值 `Pro` 或 `Lite`：
  - `Add` 调用的版本由**事实记忆规则**中配置的 `plan_version` 决定（创建/编辑规则时设置）；
  - `Search` 调用的版本由请求参数 `plan_version` 独立控制（不传默认 `Pro`）；
  - `Pro` 版本启用 Rerank，检索质量更高；`Lite` 版本跳过 Rerank，成本更低、延迟更优。
- `top_k`：单次检索最大返回条数，范围 1–100，建议根据 Prompt 上下文容量合理设置。
- `min_score`：相似度阈值（0.0–1.0），用于过滤低相关性结果，推荐值 0.5–0.7；该参数在 `SearchMemory` API 中生效，[管理记忆](../../raw/application-user-guide/memory-library-overview/create-memory/manage-memory.md)文档给出了调试建议。
- `profile_schema`：用户画像模板 ID，调用 `AddMemory` 时传入此参数方可触发画像字段提取。

## 使用方式

1. **快速启动**：使用默认记忆库，三步完成端到端验证——调用 `AddMemory` 写入对话、通过控制台或 `ListMemory` 查看、调用 `SearchMemory` 检索并注入 Prompt，完整示例见[快速开始](../../raw/application-user-guide/memory-library-overview/memory/quickstart.md)。
2. **自定义配置**：
   - 创建独立记忆库（支持命名、描述、多规则管理），最多可配置 50 条事实记忆规则 + 50 条用户画像规则；
   - 在记忆规则中定义提取指令、过期时间（7/30/180 天或永不过期）、策略版本等；
   - 通过 `CreateProfileSchema` 创建画像模板，再在 `AddMemory` 中指定 `profile_schema` 触发结构化提取。
3. **API 调用**：所有接口通过 DashScope 网关 `https://dashscope.aliyuncs.com/api/v2/apps/memory/` 提供，需 `DASHSCOPE_API_KEY` 鉴权。完整接口清单与参数说明参见[长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。

## 限制和注意事项

- **限流**：阿里云账号级别全局限流——全部接口合计 ≤ 3000 QPM；`AddMemory` ≤ 120 QPM；`SearchMemory` ≤ 300 QPM。超限返回 HTTP `429`，需实现退避重试。
- **商业化时间点**：记忆库将于 **2026 年 8 月 20 日 10:00（北京时间）** 正式开始计费，[计费说明](../../raw/application-user-guide/memory-library-overview/integration-overview/billing.md)明确区分 Pro/Lite 版本单价及免费额度（Add 免费 1500 次/3 个月，Search 免费 5000 次/3 个月，存储 10,000 条永久免费）。
- **默认记忆库不可删除**：每个账号自带一个默认记忆库，仅支持编辑名称、描述及规则，不可删除；自定义记忆库可随时删除，但数据将**不可恢复**。
- **异步行为**：用户画像提取为异步过程，首次调用 `GetUserProfile` 可能返回空值，需按业务逻辑重试（如等待 3 秒后查询）。
- **存储隔离**：记忆内容以 `user_id` 为单位隔离，同一 `user_id` 下不同记忆库的数据**不互通**；若需跨库共享，须通过应用层聚合。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)
- [记忆库概览](../../raw/application-user-guide/memory-library-overview/memory.md)
- [长期记忆](../../raw/application-user-guide/memory-library-overview/memory/long-term-memory.md)
- [快速开始](../../raw/application-user-guide/memory-library-overview/memory/quickstart.md)
- [核心概念](../../raw/application-user-guide/memory-library-overview/memory/concepts.md)
- [创建与删除记忆库](../../raw/application-user-guide/memory-library-overview/create-memory.md)
- [配置记忆规则](../../raw/application-user-guide/memory-library-overview/create-memory/configure-rules.md)
- [使用用户画像](../../raw/application-user-guide/memory-library-overview/create-memory/user-profile.md)
- [管理记忆](../../raw/application-user-guide/memory-library-overview/create-memory/manage-memory.md)
- [集成方式概览](../../raw/application-user-guide/memory-library-overview/integration-overview.md)
- [计费说明](../../raw/application-user-guide/memory-library-overview/integration-overview/billing.md)
- [限流说明](../../raw/application-user-guide/memory-library-overview/integration-overview/limits.md)
- [最佳实践](../../raw/application-user-guide/memory-library-overview/best-practices.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/best-practices/modelstudio-memory-for-openclaw.md)
- [常见问题](../../raw/application-user-guide/memory-library-overview/integration-overview/faq.md)


