# 应用开发框架与工具对比：Managed Agents、Frameworks 与 Toolkits and Frameworks

## 对比目的与背景

在百炼平台构建 AI 原生应用时，开发者面临多种技术路径选择：是直接调用原子能力、复用成熟框架封装，还是采用全托管智能体服务？当前平台提供三类核心抽象层——**Managed Agents（托管智能体）**、**Frameworks（框架集成层）** 和 **Toolkits and Frameworks（工具包与 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)）**。它们定位不同、能力边界清晰，但存在功能重叠区域（如工具调用、会话管理、RAG 构建），易引发选型困惑。

本对比旨在为开发者提供结构化、可操作的技术决策依据：明确各方案的适用边界、能力约束、运维成本与扩展性特征，避免“高配低用”或“低配硬扛”，助力快速落地稳定、可维护、可演进的生产级 AI 应用。

---

## 关键维度对比表

| 维度 | Managed Agents | Frameworks（LlamaIndex / Spring AI Alibaba） | Toolkits and Frameworks（[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)） |
|------|----------------|-----------------------------------------------|---------------------------------------------|
| **输入格式** | JSON（含 `input`, `session_id`, `context_id`, `tools` 等字段）；支持纯文本或结构化指令 | 多样：<br>• LlamaIndex：`Document` 对象、`Node` 列表、`QueryBundle`<br>• Spring AI：`Message`/`ChatClient` 抽象、`Document` 流 | 标准 OpenAI Schema：<br>• `chat/completions`：`messages[]` 数组<br>• `responses`：`input` 字符串或结构化对象<br>• `conversations`：`messages` + 生命周期操作 |
| **输出格式** | Server-Sent Events（SSE）流式事件（`message`, `tool_call`, `done` 等类型），需客户端解析事件流 | 同步返回：<br>• LlamaIndex：`Response` 对象（含 `response`, `source_nodes`, `metadata`）<br>• Spring AI：`ChatResponse` 或 `RetrievalResponse` | 同步 JSON 响应（兼容 OpenAI 格式）：<br>• `chat/completions` → `choices[0].message.content`<br>• `responses` → `output_text` / `tool_calls`<br>• `conversations` → `messages` 历史快照 |
| **支持模型** | 严格白名单：仅 `qwen-max`、`qwen-plus`、`qwen-turbo`（其他模型调用返回 `400 UnsupportedModel`） | 全量百炼文本模型（`qwen-*`, `deepseek-*`, `glm-*`, `kimi-*` 等）+ Embedding（`text-embedding-v1/v2/v3`）+ Rerank（`gte-rerank*`） | 最广谱支持：<br>• 文本：`qwen3.8-max`、`qwen3.7-plus`、`qwen-long`、`qwen-coder-turbo` 等全系 Qwen 及第三方模型<br>• [多模态](../concepts/multi-modal.md)：`qwen3-vl-plus`、`qwen-vl-ocr`<br>• Embedding：`text-embedding-v4`、`qwen3.7-text-embedding`<br>• 不支持：`Qwen-Audio`（非兼容协议） |
| **API 端点** | 专属 REST API：<br>• `POST /v1/agents`（创建）<br>• `POST /v1/agents/{id}/sessions`（会话）<br>• `POST /v1/contexts`（长期记忆） | SDK 封装调用，无统一端点：<br>• LlamaIndex：通过 `DashScopeLLM` 等组件内部路由至百炼对应服务<br>• Spring AI：`spring-ai-dashscope` 自动适配 `DASHSCOPE_API_KEY` 和 `WORKSPACE_ID` | OpenAI 兼容端点（按功能分域）：<br>• Chat：`{workspace}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions`<br>• Responses：`.../responses`<br>• Conversations：`.../conversations`<br>• Batch：`batch.dashscope.aliyuncs.com/...` |
| **计费方式** | 按 **Agent 实例运行时长（秒） + [Token](../concepts/token.md) 消耗（输入/输出）** 双维度计费：<br>• 运行时长：实例存活期间持续计费（含空闲期）<br>• [Token](../concepts/token.md)：按实际处理 token 计费（含工具调用、上下文分片） | 按 **调用次数 + [Token](../concepts/token.md) 消耗 + 云端资源使用** 计费：<br>• LLM/Embedding/Rerank 调用单独计费<br>• `DashScopeCloudIndex` 产生向量索引存储费、检索调用费<br>• `DashScopeParse` 按页/文件计费 | 按 **API 调用 + Token 消耗** 计费：<br>• 每次请求独立计费（无运行时长成本）<br>• Token 精确到字符级（兼容 OpenAI 计费逻辑）<br>• Batch 场景支持[异步任务](../concepts/asynchronous-task.md)计费 |
| **典型场景** | • 长期在线客服 Agent（7×24 运行）<br>• 多轮复杂任务助手（需跨 session 上下文恢复）<br>• 事件驱动工作流（如订单状态变更触发自动跟进）<br>• 需强可观测性与生命周期管理的企业级 Agent | • 快速构建 RAG 应用（本地 or 云端知识库）<br>• 结构化文档智能分析（PDF/DOCX 表格提取 + 语义切分）<br>• 企业级 Spring Boot AI 微服务集成<br>• 需深度定制检索流程（自定义 Node Parser / Postprocessor） | • OpenAI 生态快速迁移（零代码改造）<br>• [多模态](../concepts/multi-modal.md)应用（图文理解、OCR、视频摘要）<br>• 批量推理（千级文档批量问答）<br>• 需灵活控制会话状态（Conversations API）<br>• LangChain / LlamaIndex 等框架的底层能力增强 |
| **状态管理能力** | ✅ 原生支持：<br>• `session_id` 自动维护多轮对话状态（7 天有效期）<br>• `context_id` 绑定外部向量库实现长期记忆<br>• Webhook 事件驱动状态变更通知 | ⚠️ 有限支持：<br>• LlamaIndex：`VectorStoreIndex` 本地状态；`DashScopeCloudIndex` 云端状态由平台托管，但不暴露 session 控制权<br>• Spring AI：`ChatClient` 支持内存级会话，无持久化 | ✅ 强支持：<br>• `Conversations API` 提供完整 CRUD 会话管理<br>• `Responses API` 通过 `previous_response_id` 自动注入上下文<br>• 客户端可完全自主控制消息历史 |
| **工具调用（Function Calling）** | ✅ 原生支持：<br>• `tools` 字段声明（OpenAI 兼容格式）<br>• 平台自动调度、错误重试、结果注入 | ⚠️ 依赖框架能力：<br>• LlamaIndex：需结合 `ToolSelection` + `ToolOutputParser` 手动编排<br>• Spring AI：`DashScopeAgent` 支持，但需显式配置 `ToolExecutor` | ✅ 原生支持：<br>• `chat/completions` 和 `responses` 接口均支持 `tool_choice` / `tools` 参数<br>• 内置工具（搜索、网页抓取、代码解释器）开箱即用 |
| **部署与运维负担** | ✅ 零运维：<br>• 平台全托管（扩缩容、监控、日志、故障恢复）<br>• 无需容器、GPU、网络策略配置 | ⚠️ 中等运维：<br>• SDK 运行于用户环境（本地/云服务器/K8s）<br>• 云端组件（如 CloudIndex）由百炼托管，但 SDK 集成需自行维护版本与依赖 | ✅ 低运维：<br>• 纯 API 调用，无服务部署概念<br>• 依赖 SDK 版本管理，无基础设施负担 |

---

## 各方案适用场景建议

### ✅ 优先选择 **Managed Agents** 当：
- 你需要一个 **7×24 在线、有状态、可事件响应** 的智能体（如客户自助服务门户、IoT 设备管家）；
- 业务逻辑复杂，需 **跨多轮、跨会话保持上下文**（例如：用户中断后 3 天内继续办理贷款申请）；
- 团队缺乏 AI Infra 运维能力，要求 **开箱即用的可观测性与 SLA 保障**；
- 工具调用是核心能力，且希望平台 **自动处理失败重试、结果注入、安全网关代理**。

> ❗ 注意：若需使用 `qwen3.8-max` 或[多模态](../concepts/multi-modal.md)模型，此方案不可用。

### ✅ 优先选择 **Frameworks（LlamaIndex / Spring AI Alibaba）** 当：
- 你正在构建 **RAG 应用**，且对 **文档解析质量、检索精度、重排效果** 有严苛要求（如法律合同审查、医疗文献问答）；
- 你已使用 **Spring Boot 技术栈**，希望以声明式配置（`application.yml`）快速集成百炼能力；
- 你需要 **混合本地与云端能力**（如：本地加载私有 Embedding 模型 + 云端调用 DocMind 解析 PDF）；
- 你追求 **工程规范性与团队协作效率**，接受一定学习成本换取长期可维护性。

> ❗ 注意：不适用于需要毫秒级响应或超长会话（>7 天）的场景；`DashScopeCloudIndex` 不开放自定义切分逻辑。

### ✅ 优先选择 **Toolkits and Frameworks（[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)）** 当：
- 你已有大量基于 OpenAI SDK 的代码，目标是 **最小改动迁移至百炼**；
- 你需要 **多模态能力（图文/OCR/音视频）或批量处理（Batch）**；
- 你构建的是 **轻量级工具链、CLI 工具、低延迟 API 服务**，拒绝任何运行时托管开销；
- 你需 **完全掌控会话生命周期与消息流**（如：跨设备同步聊天记录、自定义消息缓存策略）；
- 你选用 LangChain 等框架，但希望 **绕过其抽象层，直连百炼高性能原生接口**。

> ❗ 注意：无内置状态持久化，需自行实现 `Conversations` 管理；`Qwen-Audio` 等非兼容模型无法使用。

---

## 技术选型参考指南（面向开发者）

| 你的需求 | 推荐方案 | 关键理由 |
|----------|-----------|-----------|
| “我要上线一个能记住用户偏好的电商导购机器人，支持语音唤醒和图片识图” | **Toolkits and Frameworks** | ✅ 支持 `qwen3-vl-plus`（多模态）、`Conversations API`（跨设备记忆）、OpenAI SDK 快速接入；❌ Managed Agents 不支持 VL 模型，Frameworks 对多模态支持弱 |
| “我们是银行，要基于 5000 份监管文档构建合规问答系统，要求表格识别准确率 >95%” | **Frameworks（LlamaIndex + DashScopeParse + DashScopeCloudIndex）** | ✅ `DashScopeParse` 专精 PDF/DOCX 表格与版式还原；`CloudIndex` 自动启用重排与过滤；❌ Toolkits 的 `file-extract` 接口无版式感知，Managed Agents 不提供文档解析能力 |
| “我们需要一个 HR 智能面试官，能发起多轮行为面试、调用 ATS 系统、自动写评估报告，并在候选人离职后自动归档会话” | **Managed Agents** | ✅ 原生 `session_id` + `context_id` + Webhook 事件（`task_completed`, `agent_stopped`）完美匹配；❌ Frameworks 无事件驱动机制，Toolkits 需自行轮询或监听回调 |
| “我们用 LangChain 开发了 PoC，现在要上生产，但发现默认 OpenAI LLM 太慢，想换百炼的 `qwen-long` 加速” | **Toolkits and Frameworks**（LangChain + `ChatOpenAI`） | ✅ 直接替换 `base_url` 和 `model` 即可，零逻辑修改；✅ `qwen-long` 仅在此路径开放；❌ Frameworks 的 `DashScopeLLM` 不支持 `qwen-long` |
| “我们是 SaaS 厂商，要为每个租户动态创建专属知识库 Agent，且租户可自主上传/删除文档” | **Frameworks（Spring AI Alibaba）** | ✅ `DashScopeCloudIndex` 支持按 `workspace_id`

## 被对比主题页

- [managed agents](../guides/managed-agents.md)
- [frameworks](../api/frameworks.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


