# memory library [overview](overview.md)

记忆库是为大模型提供跨会话[长期记忆](../concepts/long-term-memory.md)的 API 服务，通过自动从对话中提取关键信息并持久化存储为事实记忆与用户画像，在后续对话中基于语义检索并注入上下文，从而突破上下文窗口限制，实现个性化、连贯的智能体交互。它以 `user_id` 为隔离维度，支持多应用共享或按业务场景独立部署，所有能力均通过标准化 REST API 暴露。

## 支持的模型/功能

- **两类核心记忆类型**：  
  - **事实记忆**：自动从对话中提取动态事件信息（如“每天上午9点提醒我喝水”），适用于临时性、时效性内容；  
  - **用户画像**：基于预定义模板提取结构化用户属性（如年龄、职业、爱好），适用于固定不变的用户元数据。二者可并存使用，互不干扰。  
- **完整生命周期管理**：支持记忆的写入（`AddMemory`）、异步写入（`AddMemoryAsync`）、分页查询（`ListMemory`）、语义检索（`SearchMemory`）、单条获取（`GetMemoryNode`）、更新（`UpdateMemory`）和删除（`DeleteMemory`）；用户画像还支持模板创建（`CreateProfileSchema`）、列表（`ListProfileSchemas`）与实时获取（`GetUserProfile`）。  
- **双集成路径**：既可通过 **Agent Harness** 在百炼智能体控制台零代码配置启用，也可作为[插件](../concepts/plugin.md)嵌入工作流（如 OpenClaw），详见[集成方式概览](raw/application-user-guide/memory-library-overview/integration-overview.md)。

## 关键参数

- `user_id`：必需，记忆实体唯一标识符，用于跨请求隔离用户数据；不同 `user_id` 的记忆完全隔离。  
- `messages`：必需（`AddMemory`/`SearchMemory`），传入对话历史数组（含 `role` 和 `content`），系统据此自动提取或检索。  
- `profile_schema`：仅 `AddMemory` 写入用户画像时必需，值为 `CreateProfileSchema` 返回的 `profile_schema_id`。  
- `top_k`：`SearchMemory` 可选，默认 `10`，控制最大召回条数（范围 1–100）。  
- `min_score`：`SearchMemory` 可选，相似度阈值（0.0–1.0），默认 `0.3`（Pro 版本生效），建议调优至 `0.5–0.7` 平衡查全率与查准率；Lite 版本忽略此参数。  
- `plan_version`：控制策略版本，`AddMemory` 调用时由记忆规则配置决定，`SearchMemory` 调用时可显式指定（`pro` 或 `lite`），不传默认 `pro`；详见[计费说明](raw/application-user-guide/memory-library-overview/integration-overview/billing.md)。  
- `memory_library_id` / `project_id`：[插件](../concepts/plugin.md)场景下可选，用于指定目标记忆库及规则，未传则使用默认记忆库及其默认规则。

> **注意**：文档 4（快速开始）示例中 `SearchMemory` 请求体包含 `"plan_version": "Lite"`，但文档 7（管理记忆）示例中对应参数为 `"plan_version": "pro"`，且文档 15（核心概念）明确指出 `Search` 的 `plan_version` 由请求参数独立控制、不传默认 `pro`。实际开发应以接口文档为准——`plan_version` 是 `SearchMemory` 的合法请求参数，其取值直接影响是否启用 Rerank，需按业务精度与成本需求显式指定，不可依赖隐式默认。

## 使用方式

1. **开通与准备**：进入[百炼控制台记忆库页面](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list)点击**立即开通**；获取 `DASHSCOPE_API_KEY`（参见[获取 API Key](raw/model-api-reference/preparations/get-api-key.md)）。  
2. **写入记忆**：调用 `POST /api/v2/apps/memory/add`，传入 `user_id` 和 `messages`；若需提取用户画像，额外传入 `profile_schema`。  
3. **检索记忆**：调用 `POST /api/v2/apps/memory/memory_nodes/search`，传入 `user_id` 和当前 `messages`，设置 `top_k` 与 `min_score`；结果可直接注入 Prompt。  
4. **调试与验证**：在控制台[记忆库详情页](raw/application-user-guide/memory-library-overview/memory-library.md)的**记忆详情**与**记忆检索**标签页进行可视化操作；Python 用户可借助 `agentscope-runtime` SDK（如 `AddMemory`, `SearchMemory` 工具类）快速集成。  
5. **高级配置**：通过控制台或 API 创建自定义记忆库、配置最多 50 条事实记忆规则与 50 条用户画像规则（参见[配置记忆规则](raw/application-user-guide/memory-library-overview/create-memory/configure-rules.md)）。

## 限制和注意事项

- **限流**：阿里云账号级别全局限流——全部接口合计 ≤ 3000 QPM；`AddMemory` ≤ 120 QPM；`SearchMemory` ≤ 300 QPM；超限返回 HTTP `429`，需实现退避重试。  
- **商业化时间点**：记忆库将于 **2026 年 8 月 20 日 10:00（北京时间）** 正式开始计费，Add/Search 调用区分 Pro/Lite 策略版本，免费额度（1500 次 Add + 5000 次 Search）自该日起 3 个月内有效；存储 10,000 条永久免费。详细计费规则见[计费说明](raw/application-user-guide/memory-library-overview/integration-overview/billing.md)。  
- **默认记忆库约束**：每个账号自带一个不可删除的默认记忆库，已预置有效期 180 天的“默认项目”事实记忆规则，但可编辑名称、描述及规则参数。  
- **异步行为**：用户画像提取为异步过程，`AddMemory` 后需等待（如 `asyncio.sleep(3)`）再调用 `GetUserProfile`，否则可能返回空值。  
- **策略版本影响**：Pro 版本启用 Rerank 提升检索质量但成本更高（¥0.001/次 Search），Lite 版本跳过 Rerank 成本更低（¥0.00002/次 Search）；Add 调用的版本由记忆规则 `plan_version` 决定，Search 调用的版本由请求参数 `plan_version` 独立控制——二者解耦，修改规则版本仅影响后续新写入的记忆。

## 来源文档

- [记忆库](../../raw/application-user-guide/memory-library-overview/memory-library.md)
- [长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)
- [记忆库概览](../../raw/application-user-guide/memory-library-overview/overview.md)
- [快速开始](../../raw/application-user-guide/memory-library-overview/overview/quickstart.md)
- [创建与删除记忆库](../../raw/application-user-guide/memory-library-overview/create-memory.md)
- [使用用户画像](../../raw/application-user-guide/memory-library-overview/create-memory/user-profile.md)
- [管理记忆](../../raw/application-user-guide/memory-library-overview/create-memory/manage-memory.md)
- [集成方式概览](../../raw/application-user-guide/memory-library-overview/integration-overview.md)
- [计费说明](../../raw/application-user-guide/memory-library-overview/integration-overview/billing.md)
- [限流说明](../../raw/application-user-guide/memory-library-overview/integration-overview/limits.md)
- [常见问题](../../raw/application-user-guide/memory-library-overview/integration-overview/faq.md)
- [最佳实践](../../raw/application-user-guide/memory-library-overview/best-practices.md)
- [为 OpenClaw 配置长期记忆插件](../../raw/application-user-guide/memory-library-overview/best-practices/modelstudio-memory-for-openclaw.md)
- [配置记忆规则](../../raw/application-user-guide/memory-library-overview/create-memory/configure-rules.md)
- [核心概念](../../raw/application-user-guide/memory-library-overview/overview/concepts.md)


