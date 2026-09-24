# memory library [overview](overview.md)

[记忆](../concepts/memory.md)库是百炼平台为大模型提供的跨会话长期[记忆](../concepts/memory.md)服务，通过自动从对话中提取关键信息并持久化存储为事实[记忆](../concepts/memory.md)与用户画像，在后续对话中基于语义检索相关记忆并注入上下文，使智能体持续理解用户偏好和历史行为。它以 `user_id` 为隔离维度，支持多应用共享、规则驱动的自动化记忆管理，并提供完整的 RESTful API 与控制台操作能力。

## 支持的模型/功能

- **两类核心记忆类型**：  
  - **事实记忆**（MemoryNode）：自动从对话中提取动态事件信息（如“用户每天上午9点需喝水提醒”），适用于临时性、时效性强的上下文；  
  - **用户画像**：基于预定义模板提取结构化用户属性（如年龄、职业、爱好），适用于固定、长期稳定的用户特征。两者可协同使用，实现“动态事件 + 静态画像”的完整用户建模。  
- **两种集成路径**：支持 **Agent Harness**（百炼智能体原生集成，零代码配置）和 **插件模式**（如 OpenClaw 工作流插件），后者通过 `before_agent_start` 和 `agent_end` 钩子实现自动捕获与召回 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/best-practices/modelstudio-memory-for-openclaw.md)。  
- **策略版本支持**：Add 与 Search 操作均支持 `Pro`（开启 Rerank，高精度）与 `Lite`（跳过 Rerank，低成本）两个策略版本，按需平衡效果与成本 [计费说明](../../raw/application-user-guide/memory-library-overview/integration-overview/billing.md)。

> **注意**：文档 4 中提出的“记忆片段（MemoryNode）”与“记忆变量”概念，与文档 1/6/8 定义的“事实记忆”和“用户画像”在语义和实现机制上存在不一致——前者将记忆变量描述为手动定义的键值对（部分支持模型推理），后者则明确将用户画像作为模板驱动的结构化抽取结果。**当前官方统一术语与架构以文档 1 的“事实记忆 / 用户画像”二分法为准**，文档 4 属于旧版长期记忆功能的遗留表述，已不再代表记忆库（Memory Library）当前设计。

## 关键参数

| 参数 | 说明 | 默认值 | 备注 |
|------|------|--------|------|
| `user_id` | 记忆实体唯一标识，用于跨会话/跨请求隔离 | 必填 | 所有 API（Add/Search/List）均以此为隔离维度 |
| `plan_version` | 控制 Add 或 Search 调用的策略版本 | `Pro` | Add 的版本由记忆规则配置决定；Search 的版本由请求参数独立控制，互不影响 |
| `top_k` | 检索最大返回条数 | `10`（API）、控制台默认 `5` | 取值范围 1–100 |
| `min_score` | 相似度阈值（0.0–1.0），过滤低相关性结果 | `0.3`（API）、控制台建议 `0.5–0.7` | 过高易漏召，过低引入噪声；仅 Pro 版本生效 [核心概念](../../raw/application-user-guide/memory-library-overview/memory/concepts.md) |
| `profile_schema` | 用户画像模板 ID，调用 `AddMemory` 时传入以触发画像抽取 | 未传则不提取画像 | 必须配合 `CreateProfileSchema` 创建后使用 |

## 使用方式

1. **快速体验（默认记忆库）**：  
   - 开通服务 → 获取 `DASHSCOPE_API_KEY` → 调用 `AddMemory` 写入对话 → 用 `ListMemory` 查看 → 用 `SearchMemory` 检索 [快速开始](../../raw/application-user-guide/memory-library-overview/memory/quickstart.md)。  
2. **生产级配置**：  
   - 在控制台创建自定义记忆库 → 配置最多 50 条**事实记忆规则**（含过期时间、自动更新开关）和 50 条**用户画像规则**（含字段名、描述、初始值）→ 通过 `CreateProfileSchema` 创建画像模板 → 在 `AddMemory` 请求中传入 `profile_schema` 启动结构化抽取。  
3. **高级控制**：  
   - 使用 `meta_data` 字段为记忆添加业务标签，提升后续检索精度；  
   - 通过 `UpdateMemory` / `DeleteMemory` 精确管理单条记忆；  
   - 插件模式下可直接调用 `memory_search`、`memory_store` 等工具实现运行时记忆交互。

## 限制和注意事项

- **限流**：全账号级别，总计 ≤3000 QPM；其中 `AddMemory` ≤120 QPM，`SearchMemory` ≤300 QPM；超限返回 HTTP `429`，需实现退避重试 [限流说明](../../raw/application-user-guide/memory-library-overview/integration-overview/limits.md)。  
- **商业化时间点**：2026 年 8 月 20 日 10:00（北京时间）起正式计费，此前为免费试用期；免费额度（1500 次 Add + 5000 次 Search）有效期为商业化生效后 3 个月 [计费说明](../../raw/application-user-guide/memory-library-overview/integration-overview/billing.md)。  
- **默认记忆库不可删除**：每个账号自带一个默认记忆库，仅可编辑名称、描述及规则，不可删除；自定义记忆库可随时删除，但数据不可恢复。  
- **异步行为**：用户画像提取为异步过程，首次 `GetUserProfile` 可能返回空值，需按业务逻辑重试（建议等待 ≥3 秒后查询） [使用用户画像](../../raw/application-user-guide/memory-library-overview/create-memory/user-profile.md)。  
- **存储有效期**：事实记忆默认永不过期，除非在规则中显式配置过期时间（7/30/180 天或永不过期）；用户画像无内置过期机制，需主动删除。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [记忆库概览](../../raw/application-user-guide/memory-library-overview/memory.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)
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
- [常见问题](../../raw/application-user-guide/memory-library-overview/integration-overview/faq.md)
- [最佳实践](../../raw/application-user-guide/memory-library-overview/best-practices.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/best-practices/modelstudio-memory-for-openclaw.md)


