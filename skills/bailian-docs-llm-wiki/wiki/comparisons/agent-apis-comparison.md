# 智能体开发 API 对比：Flow Agent、Managed Agents 与 RAG

本文旨在帮助开发者在阿里云百炼平台上快速理解三类核心智能体开发能力的技术定位、能力边界与工程适配性，为实际项目中的技术选型提供清晰、可落地的决策依据。随着智能体应用从“单点调用”走向“全栈编排”与“知识增强”，百炼平台提供了分层演进的 API 能力体系：  
- **Flow Agent API** 面向已配置完成的生产级应用，强调**开箱即用与终端集成**；  
- **Managed Agents API** 面向需要深度控制执行逻辑、工具链与生命周期的**可编程智能体构建者**；  
- **RAG API** 则聚焦于**知识库基础设施层**，为检索增强、多源知识融合与语义问答提供原子化能力支撑。  

三者并非互斥替代关系，而是构成“能力底座（RAG）→ 编排引擎（Managed Agents）→ 应用交付（Flow Agent）”的典型分层架构。下表从关键工程维度进行横向对比。

## 关键维度对比

| 维度 | Flow Agent API | Managed Agents API | RAG API |
|------|----------------|---------------------|----------|
| **核心定位** | 已发布智能体/工作流的**终端调用接口**，面向应用集成方 | 可编程智能体的**全生命周期管理接口**，面向 Agent 构建者与平台集成方 | 知识库的**基础设施服务接口**，面向知识工程与检索增强场景 |
| **输入格式** | 单轮：`prompt: string`；多轮：`messages: [{role, content}]`；支持 `session_id` 续写 | `POST /agents/{id}/invoke` 请求体含 `input`（结构化输入）、`tool_choice`、`memory_store_id` 等；支持事件驱动输入（Webhook） | 检索：`query: string` 或 `images: []`；问答：`input.messages: [...]` + `parameters.agent_options.agent_id`；需显式传入 `agent_id`（非知识库 ID） |
| **输出格式** | 同步：标准 JSON 响应（含 `output.text`, `usage`）；流式：SSE 格式（`data: {...}`）；OpenAI 兼容模式返回 `choices[0].message.content` | 结构化事件流（`GET /sessions/{id}/events`）或同步响应（含 `status`, `output`, `tool_calls`, `next_action`）；支持自定义事件 Schema | 检索：`hits: [{chunk_id, content, score, kb_id}]`；问答：SSE 流式响应（`data: {"type":"answer","text":"..."}` 或 `"type":"citation"`） |
| **支持模型** | **不直接暴露模型选择**；通过预发布应用间接支持：<br>• 新版 Agent：启用 `enable_thinking` 调用深度思考模型<br>• 旧版/Workflow：由节点配置自动调度 | **支持显式模型绑定**：创建 `Agent` 时指定 `model_id`（如 `qwen3`、`qwen2.5`），支持 LLM + 工具调用联合编排 | **模型能力内嵌于知识库配置**：<br>• 嵌入模型：`embeddingModelName`（如 `text-embedding-v4`）<br>• 重排模型：`rerankModelName`（如 `qwen3-rerank`）<br>• 多模态：`multimodalEmbeddingModelName` |
| **API 端点（Base URL）** | • DashScope 网关（调用）：`https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`<br>• 百炼 OpenAPI（组件）：`https://bailian.{region}.aliyuncs.com` | `https://bailian.{region}.aliyuncs.com`（统一入口，路径区分资源：`/agents`, `/sessions`, `/skills`） | `https://{workspace_id}.cn-beijing.maas.aliyuncs.com`（所有接口均基于 workspace_id + 地域域名） |
| **认证方式** | **双鉴权体系，严格隔离**：<br>• 应用调用：`Authorization: Bearer <API-Key>`<br>• 组件接口（Prompt/记忆）：AccessKey 签名（ACS3-HMAC-SHA256） | `Authorization: Bearer <API-Key>`（统一 API Key 鉴权，支持细粒度权限策略） | `Authorization: Bearer <API-Key>`（统一 API Key 鉴权，需 `AliyunBailianDataFullAccess` 权限） |
| **计费方式** | 按调用次数与模型 [Token](../concepts/token.md) 消耗计费（归属 DashScope 计费体系）；<br>• `completion` 接口：按输入+输出 token 计费<br>• `responses`（OpenAI 兼容）：同上，异步调用额外收取任务队列费用 | 按 Agent 实例运行时长（秒）+ 工具调用次数 + Memory Store 存储量计费；<br>• `Environment` 运行期间持续计费<br>• `Skill` 调用按次计费 | 按知识库存储量（GB/月）+ 检索 QPS + 问答 [Token](../concepts/token.md) 消耗计费；<br>• 知识库创建/更新免费<br>• 检索 `/search` 和问答 `/chat` 按实际调用量计费 |
| **典型场景** | • 客服对话机器人前端集成<br>• 工作流自动化结果查询（如审批状态推送）<br>• 低代码应用中嵌入预置智能体能力 | • 构建具备多步骤规划、工具调用、外部系统集成的自主 Agent（如 CRM 自动跟进、运维故障诊断）<br>• 企业级 Agent 平台二次开发<br>• 需要会话状态强管控、内存持久化、灰度发布的复杂业务 | • 构建企业私有知识库（文档、手册、FAQ）<br>• 多源数据（OSS、数据库、API）的统一语义检索<br>• 图文混合问答（如产品说明书+截图解析）<br>• 作为 Managed Agents 的知识底座（通过 Skill 调用 RAG 检索结果） |

## 各方案适用场景建议

### ✅ 选择 Flow Agent API 当：
- 你已通过百炼控制台完成智能体或工作流的完整配置（Prompt、记忆、工具等），只需将其能力封装为 API 供前端、小程序或第三方系统调用；
- 项目周期紧，要求“零代码集成”，无需关心底层执行逻辑与状态管理；
- 场景以单轮问答或固定流程多轮交互为主（如表单填写引导、FAQ 回答），对动态工具编排无需求；
- 需要快速上线并复用 DashScope 生态（如 OpenAI 兼容模式、流式 SSE、[异步任务](../concepts/asynchronous-task.md)）。

### ✅ 选择 Managed Agents API 当：
- 你需要完全掌控 Agent 的行为逻辑：例如根据用户意图动态选择工具、实现多跳推理、处理异常分支、注入自定义凭证或回调 Webhook；
- 业务涉及多个外部系统（CRM、ERP、数据库）集成，需通过 `Skill` 封装安全、可复用的函数能力；
- 要求严格的会话生命周期管理（如 Session TTL、内存隔离、灰度发布、版本回滚）；
- 正在构建企业级 Agent 开发平台或低代码 Agent 编排器，需 API 级别的资源抽象（Agent/Environment/Session/MemoryStore）。

### ✅ 选择 RAG API 当：
- 核心需求是构建、维护和检索结构化/非结构化知识资产，而非通用对话能力；
- 数据源多样（PDF、Word、网页、数据库、OSS）、更新频繁，需自动化导入、切片、向量化与监控；
- 问答质量高度依赖精准知识召回（如法律条文引用、医疗指南溯源），需精细控制嵌入/重排模型与检索参数；
- 你计划将 RAG 能力作为模块嵌入到 Managed Agents 中（例如：`Skill` 内部调用 `/knowledge/search` 获取上下文），此时 RAG API 是必备底座。

## 技术选型参考（面向开发者）

| 你的问题 | 推荐方案 | 理由说明 |
|----------|-----------|-----------|
| “我有一个现成的 Prompt 和几个 API 工具，想快速上线一个客服机器人。” | **Flow Agent API** | 控制台拖拽配置 → 发布 → 直接调用 `/completion`，5 分钟完成集成，无需编码管理状态。 |
| “我的 Agent 需要先查订单，再调用物流接口，最后生成摘要并邮件发送——且每步失败要重试或告警。” | **Managed Agents API** | 仅 Flow Agent 无法表达该流程；必须用 `Skill` 封装各步骤，通过 `Environment` 配置重试策略，用 `Webhook` 接收失败事件。 |
| “我们有 10TB 内部文档，需要支持员工用自然语言搜索，并返回带来源的精准答案。” | **RAG API** | Flow Agent 和 Managed Agents 均不提供知识库创建、切片管理、向量索引等能力；必须先用 RAG API 构建知识库，再将其接入 Agent。 |
| “我想让我的 Managed Agent 在每轮对话前自动检索最新产品文档。” | **RAG API + Managed Agents API 组合** | 在 `Skill` 中调用 RAG 的 `/knowledge/search` 接口，将结果注入 `messages` 系统提示，实现 RAG 增强。Flow Agent 无法实现此动态注入。 |
| “我需要审计所有对话历史，并按用户 ID 持久化存储 180 天。” | **Managed Agents API（Memory Store） + 自定义 Skill** | Flow Agent 的 `session_id` 仅保留 1 小时；RAG 不存对话；Managed Agents 的 `Memory Store` 默认 7 天，但可通过 `Skill` 将数据写入外部数据库实现长期留存。 |

> **重要提醒**：  
> - **地域限制**：Flow Agent 的 DashScope 调用接口**仅支持华北2（北京）**；RAG 和 Managed Agents 接口需确认所用 `workspace_id` 对应的地域是否开通服务（当前主流地域均支持）。  
> - **鉴权不可混用**：API Key 与 AccessKey **绝对不可交叉使用**，否则返回 `401 Unauthorized`。请严格按文档选择对应认证方式。  
> - **演进趋势**：新版 Agent（Agent 2.0）正逐步收敛能力至 Managed Agents 体系；[长期记忆](../concepts/long-term-memory.md)（旧）等 Flow Agent 组件接口已标记为兼容性维护，新项目应优先采用 Managed Agents 的 `Memory Store`。  

如需进一步评估具体业务场景的集成路径，建议结合 [百炼控制台能力矩阵](https://bailian.console.aliyun.com) 与各 API 的 [OpenAPI Schema](https://help.aliyun.com/zh/bailian/developer-reference/openapi-specification) 进行端到端验证。

## 被对比主题页

- [flow agent api](../api/flow-agent-api.md)
- [managed agents api](../api/managed-agents-api.md)
- [rag api](../api/rag-api.md)


