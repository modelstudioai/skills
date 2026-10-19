# 核心 API 功能对比：Application Call、Frameworks、Vector and Sort

## 对比目的与背景  
在百炼平台构建生产级 AI 应用时，开发者需根据技术目标（如调用已部署智能体、快速集成大模型能力、或实现语义检索/RAG）选择最适配的 API 能力层。`Application Call`、`Frameworks` 和 `Vector and Sort` 三类能力定位清晰但边界易混淆：  
- **Application Call** 面向「应用级编排」，聚焦已发布 Agent/Workflow 的端到端调用；  
- **Frameworks** 面向「开发框架协同」，解决 LlamaIndex/Spring AI 等主流生态与百炼底层模型的标准化对接；  
- **Vector and Sort** 面向「基础语义计算」，提供向量化、多模态表征、重排序等原子能力，是 RAG、搜索、聚类等场景的底层支撑。  

本对比旨在帮助开发者基于**功能目标、输入输出形态、工程耦合度、计费模型**等维度，快速完成技术选型决策，避免能力误用（如用 Frameworks 直接调用工作流，或用 Application Call 实现批量向量化）。

---

## 关键维度对比表

| 维度 | Application Call | Frameworks | Vector and Sort |
|------|------------------|------------|-----------------|
| **核心定位** | 调用已发布的[智能体（Agent）](../concepts/agent.md)或工作流（Workflow）应用，支持完整业务逻辑执行 | 将百炼大模型能力嵌入主流开发框架（LlamaIndex/Spring AI），降低协议对接成本 | 提供文本/多模态[向量化（Embedding）](../concepts/embedding.md)与文本重排序（Rerank）等基础语义计算能力 |
| **输入格式** | • DashScope API：`prompt`（字符串）或 `messages`（消息数组）<br>• Responses API：`input`（字符串或消息数组）<br>• 支持多模态：`image_list` / `input_image` / `input_file`（PDF/DOCX/MP3等） | • 统一遵循 `v1/chat/completions` 语义<br>• 输入为标准 `messages` 数组（system/user/assistant）<br>• 不直接支持文件/图像输入（需预处理为文本） | • 文本向量：`string` / `array<string>` / `file`（URL）<br>• 多模态向量：`{"contents": [...]}`（含 text/image/video 字段）<br>• 排序：`{"query": "...", "documents": [...]}` |
| **输出格式** | • 同步：完整响应对象（含 `output.text`、`output.thoughts`、`output.tool_calls` 等）<br>• 流式：SSE 分块（`event: message`, `data: {...}`）<br>• 异步：返回 `task_id`，需轮询结果 | • 框架原生响应对象（如 LlamaIndex 的 `StreamingResponse` 或 Spring AI 的 `ChatResponse`）<br>• 输出结构与框架约定一致，非百炼原始响应 | • 文本/多模态向量：`{"data": [{"embedding": [...], "index": 0}]}`（同步）或异步任务结果<br>• 排序：`{"results": [{"index": 0, "relevance_score": 0.92}]}` |
| **支持模型/能力** | • 应用类型：新版 Agent（2.0）、旧版 Agent、Workflow<br>• 模型绑定：由应用配置决定（如 Qwen-Max、Qwen-Plus）<br>• 高级功能：长期记忆（`memory_id`）、RAG 检索（`rag_options`）、思考过程（`enable_thinking`）、节点级流式（`flow_stream_mode`） | • 模型 ID 显式指定（如 `qwen-max`, `qwen-plus`）<br>• 支持工具调用（`tools` 字段透传）<br>• 仅限 `chat/completions` 类模型，不支持 Embedding/Rerank 模型 | • 文本向量：`qwen3.7-text-embedding`, `text-embedding-v4`, `text-embedding-async-v2` 等<br>• 多模态向量：`qwen3-vl-embedding`, `tongyi-embedding-vision-plus` 等<br>• 排序：`qwen3-rerank`, `qwen3-vl-rerank`, `gte-rerank-v2`（即将下线） |
| **API 端点** | • DashScope 原生：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`<br>• OpenAI 兼容（Responses）：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses` | • 统一兼容 OpenAI `v1/chat/completions` 协议<br>• Base URL：`https://dashscope.aliyuncs.com/compatible-mode/v1`（默认）或自定义 Workspace 地域地址 | • 向量：`POST https://dashscope.aliyuncs.com/api/v1/services/embeddings/text-embedding/...`<br>• 多模态：`POST https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/...`<br>• 排序：`POST https://dashscope.aliyuncs.com/api/v1/services/rerank/...`<br>• **无 OpenAI 兼容路由** |
| **计费方式** | • 按调用次数 + 模型 Token 消耗计费（输入+输出）<br>• 工作流按节点执行次数叠加计费<br>• 免费额度：新用户享 1000 次/月调用 + 50 万 Token（北京地域） | • 完全继承所选模型的计费规则（如 `qwen-max` 按其 Token 计费）<br>• 无额外框架封装费用<br>• 免费额度同对应模型（如 `qwen-plus` 的免费额度） | • 文本向量：按输入 Token 计费（`qwen3.7-text-embedding`：0.0002 元/千 Token）<br>• 多模态向量：按输入内容复杂度分档（文本+图像分辨率）<br>• 排序：按 `query + documents` 总 Token 计费<br>• 免费额度差异大（如 `text-embedding-async-v2` 北京地域 2000 万 Token/月，`qwen3-rerank` 无免费额度） |
| **典型场景** | • 客服对话机器人（带记忆与 RAG）<br>• 自动化审批工作流（多节点条件分支）<br>• 多模态报告生成（上传 PDF+提问）<br>• 需要思考链（CoT）审计的合规场景 | • 基于 LlamaIndex 构建知识库问答系统<br>• Spring Boot 应用中集成百炼大模型进行摘要/改写<br>• 快速验证不同模型（`qwen-plus` vs `qwen-max`）对同一 prompt 的效果 | • RAG 系统中的文档向量化与查询向量生成<br>• 跨模态搜索（用文字搜图片/视频）<br>• 搜索引擎结果重排序（提升 Top-10 相关性）<br>• 文本聚类与相似度分析 |

---

## 适用场景建议

| 场景描述 | 推荐方案 | 理由说明 |
|----------|----------|----------|
| **需要调用一个已配置好插件、RAG、记忆和多步骤逻辑的智能体** | ✅ Application Call | 只有该能力支持 `memory_id`、`rag_options`、`flow_stream_mode` 等应用级特性；Frameworks 和 Vector and Sort 无法承载完整 Agent 运行时。 |
| **已有 LlamaIndex 或 Spring AI 项目，希望无缝切换至百炼模型** | ✅ Frameworks | 提供开箱即用的适配器（如 `LlamaIndexLLM`），无需修改业务代码逻辑，仅需替换初始化参数；Application Call 需重构为应用调用模式，Vector and Sort 无 chat 接口。 |
| **构建 RAG 系统，需对百万级文档做向量化，并对召回结果重排序** | ✅ Vector and Sort | 原生支持异步批处理（`text-embedding-async-v2`）、高并发排序（`qwen3-rerank`），且具备严格输入长度控制与维度定制能力；Application Call 无法批量向量化，Frameworks 不提供 Embedding/Rerank 接口。 |
| **需同时使用 Agent 编排 + RAG 检索 + 多模态理解** | ⚠️ **组合使用**：<br>• Application Call（主流程）<br>• Vector and Sort（RAG 检索子模块） | Application Call 的 `rag_options` 内部即调用 Vector and Sort 服务；若需自定义检索逻辑（如混合向量+关键词），应在 Application Call 外部先调用 Vector and Sort 获取结果，再注入 `messages` 中。 |
| **快速原型验证一个 prompt 在不同模型上的效果（如 qwen-max vs qwen-plus）** | ✅ Frameworks（首选）<br>或 ✅ Application Call（次选） | Frameworks 支持通过 `model` 参数一键切换，代码侵入最小；Application Call 需为每个模型单独发布应用，运维成本高。 |

---

## 技术选型参考（面向开发者）

### 选择 Application Call 当且仅当：
- 你的交付物是一个**可复用、可配置、带状态的 AI 应用**（如“合同审核助手”“HR 招聘初筛工作流”）；
- 需要平台级能力：长期对话记忆、RAG 检索、多模态输入、可视化调试（思考过程）、节点级流式反馈；
- 接受应用发布流程（控制台配置 → 发布 → 获取 APP ID）；
- **避坑提示**：勿用于纯文本生成任务（如简单摘要），此时 Frameworks 更轻量；勿用于批量数据处理（如 10 万条日志向量化），此时 Vector and Sort 批处理更经济。

### 选择 Frameworks 当且仅当：
- 你已在使用 **LlamaIndex 或 Spring AI**，且希望**零改造迁移至百炼**；
- 需要灵活切换模型（A/B 测试）、复用框架生态（如 LlamaIndex 的 Retriever、NodeParser）；
- 不依赖 Agent 特性（记忆、RAG、工作流），仅需标准 `chat/completions` 交互；
- **避坑提示**：不支持文件/图像输入（需自行解析为文本）；不支持 Application Call 的高级参数（如 `session_id`, `incremental_output`）；工具调用需确认模型与框架版本兼容性。

### 选择 Vector and Sort 当且仅当：
- 你的需求本质是**语义计算**：将文本/图像映射到向量空间，或对文本相关性打分；
- 需要**高吞吐、低延迟、可预测的性能**（如实时搜索重排序）；
- 需要**精确控制输入格式与输出维度**（如固定 1024 维向量用于 FAISS 索引）；
- **避坑提示**：不提供对话状态管理；不支持流式响应（向量/排序均为同步返回或异步任务）；多模态向量需严格遵循 `{"contents": [...]}` 结构，不可混用 Application Call 的 `image_list` 格式。

> **终极原则**：  
> - **用 Application Call “跑应用”**，  
> - **用 Frameworks “写代码”**，  
> - **用 Vector and Sort “算语义”**。  
> 三者非互斥，而是分层协作——一个企业级 RAG 应用通常同时调用全部三类能力。

## 被对比主题页

- [application call](../api/application-call.md)
- [frameworks](../api/frameworks.md)
- [vector and sort](../api/vector-and-sort.md)


