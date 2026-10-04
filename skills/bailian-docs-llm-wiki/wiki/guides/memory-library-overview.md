# memory library [overview](overview.md)

记忆库是百炼平台为大模型提供的跨会话[长期记忆](../concepts/memory.md)服务，通过自动从对话中提取关键信息并持久化存储，解决大模型上下文窗口限制导致的“每次对话从零开始”问题。它支持两种核心记忆类型：动态的**事实记忆**（如事件、提醒）和结构化的**用户画像**（如年龄、职业），并在后续对话中基于语义检索相关记忆注入 Prompt，实现个性化、连贯的智能体交互。该服务以开放 API 为核心，同时提供控制台可视化管理能力。

## 支持的模型/功能

- **记忆类型**：  
  - **事实记忆**：自动从 `messages` 中提取关键事件（如“每天上午9点提醒我喝水”），适用于动态、时效性信息；  
  - **用户画像**：基于预定义模板（`profile_schema`）提取结构化属性（如“年龄=28，职业=工程师”），适用于固定用户属性。两者可独立或协同使用。  
- **集成路径**：支持 **Agent Harness**（百炼智能体原生集成）与 **插件**（如 OpenClaw 工作流插件）两种方式，详见[集成方式概览](raw/application-user-guide/memory-library-overview/integration-overview.md)。  
- **自动化能力**：插件模式支持 `autoCapture`（对话结束自动写入）与 `autoRecall`（对话开始前自动检索），大幅降低接入成本 [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/best-practices/modelstudio-memory-for-openclaw.md)。

## 关键参数

| 参数 | 说明 | 取值/范围 | 备注 |
|------|------|-----------|------|
| `user_id` | 记忆实体 ID，用于跨会话隔离 | 字符串 | **必填**，不同 `user_id` 的记忆完全隔离 |
| `plan_version` | 策略版本，控制 Rerank 是否启用 | `"Pro"` / `"Lite"` | `Add` 调用由记忆规则配置决定；`Search` 调用由请求参数独立控制，默认 `Pro` |
| `top_k` | 检索最大召回数量 | `1–100` | 控制返回记忆条数，影响 [Token](../concepts/token.md) 消耗与响应延迟 |
| `min_score` | 相似度阈值（Pro 版生效） | `0.0–1.0` | 建议 `0.5–0.7`；过低引入噪声，过高漏召 [管理记忆](../../raw/application-user-guide/memory-library-overview/create-memory/manage-memory.md) |
| `memory_library_id` | 指定目标记忆库 | 字符串 | 不传时默认使用账号下默认记忆库 |
| `profile_schema` | 用户画像模板 ID | 字符串 | `AddMemory` 中传入才触发画像提取 |

> **注意**：文档 4 和文档 11 对 `plan_version` 默认行为描述一致（不传默认 `Pro`），但文档 7 在“用户画像规则”配置说明中称“不传默认 Pro”，而文档 11 明确画像写入 Lite 单价为 ¥0.025/次（区别于事实记忆 Lite 的 ¥0.018），表明二者策略版本虽同名，但计费与底层处理逻辑已分离，需严格按接口类型区分配置。

## 使用方式

1. **快速验证（3 步）**：  
   - 调用 `AddMemory` 写入对话（含 `user_id` 和 `messages`）；  
   - 通过控制台「记忆详情」页输入 `user_id` 查看提取结果；  
   - 调用 `SearchMemory` 检索（传入相同 `user_id` 和当前 `messages`），将返回结果注入 Prompt 即可。完整示例见[快速开始](../../raw/application-user-guide/memory-library-overview/overview/quickstart.md)。  

2. **生产级配置**：  
   - 创建自定义记忆库（非必须，但推荐用于多业务隔离）；  
   - 在「记忆规则」页配置事实记忆规则（含过期时间、`plan_version`）和用户画像规则（含字段定义）；  
   - 用户画像需先调用 `CreateProfileSchema` 创建模板，再在 `AddMemory` 中传入 `profile_schema` ID 才生效 [使用用户画像](../../raw/application-user-guide/memory-library-overview/create-memory/user-profile.md)。  

3. **SDK 支持**：  
   - Python 推荐使用 `agentscope-runtime`（`pip install agentscope-runtime`），封装了 `AddMemory`、`SearchMemory` 等异步工具；  
   - 所有接口均通过 DashScope 网关（`https://dashscope.aliyuncs.com/api/v2/apps/memory/`）提供，采用 `Bearer $DASHSCOPE_API_KEY` 鉴权。

## 限制和注意事项

- **限流**：阿里云账号级别全局限流——全部接口 ≤ 3000 QPM；`AddMemory` ≤ 120 QPM；`SearchMemory` ≤ 300 QPM。超限返回 HTTP `429`，需实现退避重试 [限流说明](raw/application-user-guide/memory-library-overview/integration-overview/limits.md)。  
- **商业化时间点**：**2026 年 8 月 20 日 10:00（北京时间）起正式计费**，Add/Search 调用按 `Pro`/`Lite` 版本分计费项，免费额度仅限 3 个月内有效 [计费说明](raw/application-user-guide/memory-library-overview/integration-overview/billing.md)。  
- **默认记忆库**：每个账号自带且**不可删除**，但可编辑名称、描述及规则；其预置的“默认项目”规则可修改但不可删除。  
- **异步行为**：用户画像提取为异步过程，`AddMemory` 返回后需等待数秒再调用 `GetUserProfile`，否则可能返回空值 [使用用户画像](../../raw/application-user-guide/memory-library-overview/create-memory/user-profile.md)。  
- **存储有效期**：事实记忆/用户画像默认永不过期，除非在规则中显式配置过期时间（如 7 天、180 天）；存储本身按 `¥0.002/万条/小时` 计费，长期有效。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)
- [记忆库概览](../../raw/application-user-guide/memory-library-overview/overview.md)
- [核心概念](../../raw/application-user-guide/memory-library-overview/overview/concepts.md)
- [快速开始](../../raw/application-user-guide/memory-library-overview/overview/quickstart.md)
- [创建与删除记忆库](../../raw/application-user-guide/memory-library-overview/create-memory.md)
- [配置记忆规则](../../raw/application-user-guide/memory-library-overview/create-memory/configure-rules.md)
- [管理记忆](../../raw/application-user-guide/memory-library-overview/create-memory/manage-memory.md)
- [使用用户画像](../../raw/application-user-guide/memory-library-overview/create-memory/user-profile.md)
- [集成方式概览](../../raw/application-user-guide/memory-library-overview/integration-overview.md)
- [计费说明](../../raw/application-user-guide/memory-library-overview/integration-overview/billing.md)
- [限流说明](../../raw/application-user-guide/memory-library-overview/integration-overview/limits.md)
- [常见问题](../../raw/application-user-guide/memory-library-overview/integration-overview/faq.md)
- [最佳实践](../../raw/application-user-guide/memory-library-overview/best-practices.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/best-practices/modelstudio-memory-for-openclaw.md)


