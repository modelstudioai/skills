# 向量检索、沙箱环境与实时推理服务对比

本对比旨在帮助开发者在百炼平台技术选型中，清晰区分**向量检索（Vector & Sort）**、**沙箱环境（Sandbox API）** 和**实时推理服务（Omni Realtime API）** 三类核心能力的定位、边界与适用阶段。三者分别服务于**语义理解与召回增强**、**安全可控的代码执行与环境隔离**、**低延迟多模态人机交互**三大范式，虽同属百炼 AI 基础设施层，但在设计目标、数据流模型、资源模型与工程约束上存在本质差异。本文提供结构化对比与场景化建议，助力团队避免功能误用、提升集成效率。

## 关键维度对比

| 维度 | 向量检索（Vector & Sort） | 沙箱环境（Sandbox API） | 实时推理服务（Omni Realtime API） |
|------|---------------------------|---------------------------|-----------------------------------|
| **核心目标** | 将非结构化内容（文本/图像/视频）映射为可计算的稠密向量，并支持语义相似度排序；支撑 RAG、聚类、跨模态搜索等下游任务 | 提供隔离、可控、可复现的 Linux 运行时环境，用于安全执行用户代码（Python/Shell/JS 等）、运行第三方工具或调试 Agent 行为 | 实现端到端毫秒级多模态（语音+文本+工具）实时交互，支持流式响应、VAD、上下文感知与动态工具调用 |
| **输入格式** | • 文本向量：`string` / `array<string>` / `file`<br>• 多模态向量：`contents: [{"text":"..."},{"image":"url"}]`<br>• Rerank：`{"query": "...", "documents": [...]}` | • 模版创建：`cpuCount`, `memoryMB`, `mntConfig`（挂载文件 ID）等 JSON 配置<br>• 实例操作：`sandboxID` 路径参数 + `timeout`, `allow_internet_access` 等 Body 参数 | • 客户端事件流（WebSocket/AOQ/WebRTC）：<br> – `session.update`（配置）<br> – `input_audio_buffer.append`（音频 Base64）<br> – `conversation.item.create`（文本/工具结果）<br> – `response.cancel`（中断） |
| **输出格式** | • 向量：`{"data": [{"embedding": [0.12, -0.87, ...], "index": 0}], "usage": {...}}`（float 或 base64）<br>• Rerank：`{"results": [{"index": 0, "relevance_score": 0.92}, ...]}` | • 实例管理：JSON 响应含 `sandboxID`, `status`, `domain`, `envdAccessToken` 等元信息<br>• 执行结果：需通过 `envdAccessToken` 连接沙箱后，使用 `exec` 或 `run` 接口获取 stdout/stderr（非平台直接返回） | • 服务端事件流（Server-Sent Events）：<br> – `conversation.item.created`（消息/工具调用）<br> – `response.text.delta`（流式文本）<br> – `response.audio.delta`（PCM 音频 chunk）<br> – `response.done`（完成）<br> – `input_audio_buffer.speech_stopped`（VAD 触发） |
| **支持模型/能力** | • 文本嵌入：`qwen3.7-text-embedding`, `text-embedding-v4`, `text-embedding-async-v2`<br>• 多模态嵌入：`qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06`<br>• 排序（Rerank）：`qwen3-rerank`, `qwen3-vl-rerank`, `gte-rerank-v2`（即将下线） | • 无“模型”概念；基于容器镜像构建的沙箱模版（Template），支持自定义 OS、依赖、环境变量与挂载文件<br>• 兼容 E2B 协议，支持 Python/Node.js/Shell 等任意语言运行时 | • 实时大模型：`qwen3.8-omni-flash-realtime`, `qwen3.5-omni-plus-realtime`, `qwen3.5-omni-flash-realtime` 等<br>• 支持 VAD（server/semantic）、Function Calling、MCP、联网搜索（`enable_search`）、视频输入（仅 qwen3.8） |
| **API 端点（典型）** | • 同步向量：`POST /api/v1/services/aigc/text-embedding`<br>• 异步批处理：`POST /api/v1/services/aigc/text-embedding/batch`<br>• Rerank：`POST /api/v1/services/aigc/rerank` | • 创建模版：`POST /v3/templates`<br>• 创建实例：`POST /v2/sandboxes`<br>• 连接实例：`POST /v2/sandboxes/{sandboxID}/connect`<br>• 文件上传：`POST /api/v1/agentstudio/files` | • WebSocket 连接：`wss://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/realtime/omni`<br>• AOQ/WebRTC：见对应接入文档<br>• 所有交互基于客户端事件（Client Events）驱动 |
| **计费方式** | • 按 **[Token](../concepts/token.md) 数量** 计费（输入 [Token](../concepts/token.md) + 输出 [Token](../concepts/token.md)）<br>• 同步/异步接口单价不同（如 `text-embedding-v4` vs `text-embedding-async-v2`）<br>• 北京地域部分模型享 90 天免费额度（如 100 万 Token） | • 按 **沙箱实例运行时长（秒）** 计费<br>• 模版构建不计费，但占用工作空间存储（≤100 GB）<br>• 实例空闲超时（`autoPauseTime`）后暂停不计费，恢复后继续计费 | • 按 **会话时长（秒）** + **音频处理时长（秒）** + **Token 数量** 组合计费<br>• 语音输入/输出、文本生成、工具调用均计入不同计量项<br>• 未启用 `enable_search` 时不产生额外搜索费用 |
| **典型场景** | • 构建 RAG 系统的向量数据库索引<br>• 对搜索召回结果做相关性重排序（Rerank）<br>• 图文混合内容的跨模态相似检索（如“找和这张图描述一致的新闻稿”）<br>• 文本聚类、去重、分类预处理 | • 安全执行用户上传的 Python 脚本（如数据分析、PDF 解析）<br>• Agent 工具链中调用本地 CLI 工具（如 `curl`, `ffmpeg`, `pandas`）<br>• 模型推理前的数据清洗/特征工程（隔离敏感逻辑）<br>• 调试复杂 Agent 的中间步骤输出 | • 语音助手（支持打断、静音检测、自然对话）<br>• 实时会议转录与摘要（语音→文本→摘要→语音播报）<br>• 智能客服（多轮问答+实时调用订单系统 API）<br>• 教育场景口语评测（语音输入→ASR→评分→语音反馈） |

## 各方案适用场景建议

### ✅ 向量检索（Vector & Sort）适合：
- **您需要将非结构化数据转化为可检索的数学表示**：例如将千万级商品描述、百万张产品图、TB 级视频关键帧生成统一语义向量。
- **您已具备检索系统（如 Elasticsearch、Milvus、PGVector），仅需高质量 Embedding/Rerank 能力**：百炼不托管向量库，专注提供高精度、多模态、可扩展的向量化服务。
- **您对延迟敏感但数据量适中**：同步接口支持 ≤20 条文本/≤500 文档的毫秒级响应；大数据量则选用异步批处理（10 万行/请求）。
- **⚠️ 不适合**：直接运行业务逻辑、执行 Python 代码、处理实时语音流、生成自然语言回复。

### ✅ 沙箱环境（Sandbox API）适合：
- **您需要在可信环境中执行不可信代码**：例如允许终端用户提交 Python 脚本分析其私有 CSV 数据，且要求资源隔离、网络可控、超时自动终止。
- **您的 Agent 需调用本地工具链（非 HTTP API）**：如使用 `ffmpeg` 转码、`pdfplumber` 提取 PDF 表格、`shell` 脚本批量处理文件。
- **您希望复现生产问题或调试 Agent 行为**：通过固定模版（含特定依赖版本）快速拉起一致环境，注入相同输入观察输出。
- **⚠️ 不适合**：高频低延迟 API 调用（沙箱启动耗时秒级）、长期驻留服务（最大运行时长受 `maxRunningTimeout` 限制）、直接处理语音/视频流媒体。

### ✅ 实时推理服务（Omni Realtime API）适合：
- **您构建的是“会说话”的 AI 应用**：要求端到端延迟 <500ms，支持语音输入打断、静音自动结束、流式文本/语音输出。
- **您需要上下文感知的多步交互**：例如用户说“查我昨天的会议记录”，AI 自动调用日历 API → 获取会议 → 调用 ASR 转录 → 总结要点 → 语音播报。
- **您需融合多种模态决策**：如视频会议中，同时分析发言人语音（ASR）、PPT 内容（OCR+Embedding）、共享屏幕（VL 模型理解），再生成摘要。
- **⚠️ 不适合**：离线批量处理（如转录 100 小时录音）、纯文本问答（应优先用 `qwen3` 同步 API）、无需实时性的后台任务（如定时报告生成）。

## 技术选型参考（面向开发者）

| 您的问题 | 推荐方案 | 关键依据 |
|----------|----------|----------|
| “如何把我的 50 万篇文档变成向量，存进 Milvus？” | ✅ 向量检索（`text-embedding-async-v2`） | 异步批处理支持单次 10 万行，高吞吐、低成本；输出标准 float 向量，无缝对接向量数据库 |
| “用户上传一个 Python 脚本，我想安全运行它并返回结果” | ✅ 沙箱环境（Sandbox API） | 提供进程级隔离、资源配额（CPU/Memory）、网络策略（`allow_internet_access` 可控）、文件挂载，符合安全执行规范 |
| “我要做一个语音点餐助手，用户说话时 AI 实时回应，还能查餐厅库存” | ✅ 实时推理服务（`qwen3.8-omni-flash-realtime`） | 原生支持 VAD、流式 audio/text、Function Calling（调用库存 API）、低延迟（AOQ/WebRTC 协议优化） |
| “我的 RAG 应用召回了 100 个文档，想按相关性重新排序” | ✅ 向量检索（Rerank） | `qwen3-rerank` 专为 Top-K 重排优化，比粗排模型精度更高，且支持 `instruct` 引导排序意图 |
| “我需要定期跑一个数据清洗脚本，处理 S3 上的 CSV 并写回” | ⚠️ 沙箱环境（*或* 函数计算 FC） | 沙箱适合复杂依赖/交互式调试；若脚本轻量、无状态、纯 Python，也可考虑 FC（成本更低、启动更快） |
| “我想让 AI 根据用户上传的图片生成一段描述文字” | ❌ 实时推理服务<br>✅ 向量检索（多模态 Embedding）+ 同步 LLM API | Omni Realtime 不提供纯 VL 描述生成；应先用 `qwen3-vl-embedding` 做理解，再调用 `qwen3` 文本模型生成描述 |

> **重要提醒**：  
> - **三者可组合使用**：典型 RAG+Agent 架构中，向量检索负责召回 → 沙箱环境执行数据提取/格式转换 → 实时推理服务整合结果并语音播报。  
> - **关注地域与模型可用性**：北京地域部分向量模型享免费额度，而沙箱与实时服务当前仅支持 `cn-beijing`；新加坡地域模型列表与价格可能不同，请以控制台实时展示为准。  
> - **务必校验输入限制**：向量服务拒绝超限请求（不截断）；沙箱文件扩展名严格校验（`.yml` ✅，`.yml` ❌）；实时服务音频采样率/声道数有硬约束（如 `qwen3.8

## 被对比主题页

- [vector and sort](../api/vector-and-sort.md)
- [sandbox api](../api/sandbox-api.md)
- [omni realtime api](../api/omni-realtime-api.md)


