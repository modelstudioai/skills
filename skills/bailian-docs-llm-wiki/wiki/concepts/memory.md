# 长期记忆

长期记忆是百炼平台为大模型应用提供的**跨会话、结构化、语义可检索的持久化记忆服务**，用于突破大模型上下文窗口限制，实现用户状态、行为意图与固有特征的自动沉淀与智能复用。

## 在百炼平台的不同场景中，这个概念如何使用

长期记忆不是独立运行的模块，而是深度集成于百炼核心应用范式中，按需启用、自动协同：

- **智能体（Agent 2.0）应用**：在控制台创建 Agent 时，开启「长期记忆」开关后，系统自动在每次对话 `completion` 调用前后执行记忆写入（`AddMemory`）与检索（`SearchMemory`）。检索结果以 `memory_nodes` 形式注入 Prompt，支撑个性化响应与连续任务规划。调用 API 时通过 `memory_id` 参数显式启用（仅对 Agent 应用有效）。

- **工作流（Workflow）应用**：不直接内置长期记忆能力，但可通过 **OpenClaw 插件** 或自定义 HTTP 节点调用长期记忆 API（如 `/add-async` 和 `/memory_nodes/search`），实现记忆驱动的流程分支（例如：“若用户历史有健身目标，则推荐运动计划”）。

- **高代码应用**：开发者可直接集成 `dashscope` SDK 或调用 REST API，在 Python 服务中自主控制记忆生命周期——例如，在用户登录后预加载画像，在工具调用后写入技能记录，在生成回复前注入相关事实。

- **安全防护体系**：长期记忆内容（包括事实记忆文本、用户画像字段）默认接受**输入/输出内容安全检测**；启用高级防护后，还支持记忆窃取行为审计与知识投毒风险识别，确保记忆数据本身可信、合规、可控。

> ✅ 注意：当前所有文档所指“长期记忆”均指向统一升级后的 **记忆库（Memory Library）服务**，旧版功能已下线，无兼容或并存版本。

## 关键参数和配置

| 参数 | 说明 | 推荐值 | 备注 |
|------|------|--------|------|
| `user_id` | **必填**，用户级隔离标识符 | 字符串（如 `"u_12345"`） | 所有读写操作均以此为维度，确保多租户数据隔离 |
| `plan_version` | 计费与能力策略版本 | `"Pro"`（推荐） / `"Lite"` | `"Pro"` 支持 Rerank、`min_score` 过滤；`"Lite"` 仅基础检索，不计费但能力受限 |
| `top_k` | 检索返回最大条数 | `5–10`（生产环境常用） | 默认值未显式声明，API 示例多用 `10`；过高易引入噪声，过低可能漏召关键信息 |
| `min_score` | 相似度阈值（仅 `plan_version="Pro"` 生效） | `0.6`（起始推荐） | 范围 `0.0–1.0`；`<0.5` 易召回无关项，`>0.7` 可能漏召；需结合业务效果微调 |
| `memory_types` | 指定检索类型 | `["observation", "skill"]` 或 `["profile"]` | 控制搜索范围，避免混检干扰；默认全类型 |
| `extract_mode` | 写入时抽取控制模式 | `"profile_only"` / `"all"` | 同步写入时可指定仅提取画像，降低延迟；异步写入（`/add-async`）更推荐全量处理 |

- **异步写入必备**：当需高精度用户画像提取或批量处理多条消息时，必须使用 `/add-async` 接口，并轮询 `GET /events/{event_id}` 获取最终结果（`status=SUCCEEDED` 后 `result` 字段才有效）。
- **画像模板依赖**：提取用户画像需提前在控制台或通过 `/profile_schemas` API 创建并传入 `profile_schema_id`；模板字段变更后，新写入将按新结构生效。

## 面向开发者，简洁实用

- **快速上手三步**：  
  1️⃣ 开通：控制台 → [记忆库页面](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/memory/list) → 点击「立即开通」；  
  2️⃣ 写入：`POST /api/v2/apps/memory/add`，传 `user_id` + `messages`（事实）或 `+ profile_schema_id`（画像）；  
  3️⃣ 检索：`POST /api/v2/apps/memory/memory_nodes/search`，传 `user_id` + 当前 `messages`，结果自动注入 Agent Prompt 或供你手动解析。

- **避坑提示**：  
  ▪ 用户画像提取为**异步过程**，`AddMemory` 后立即调用 `GetUserProfile` 可能返回空，建议等待 2–5 秒或改用 `/add-async` + 事件轮询；  
  ▪ `min_score` 在 `"Lite"` 版本下**不生效**，勿配置；  
  ▪ 免费额度仅限首 3 个月（商业化起始日：2026-08-20），建议尽早压测并规划配额；  
  ▪ 所有接口受账号级限流约束（`AddMemory ≤ 120 QPM`, `SearchMemory ≤ 300 QPM`），超限返回 `429`，务必实现指数退避重试。

- **调试建议**：  
  使用 `GET /memory_nodes?user_id=xxx&page_num=1&page_size=20` 浏览原始记忆节点，验证提取质量；  
  在 Agent 调试面板中开启「显示注入记忆」开关，直观查看哪些 `memory_nodes` 被实际用于本次推理。

## 关联主题页

- [memory library overview](../guides/memory-library-overview.md)
- [long term memory new](../api/long-term-memory-new.md)
- [llm application](../guides/llm-application.md)
- [application call](../api/application-call.md)
- [security guide](../guides/security-guide.md)


