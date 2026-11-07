# use cases

百炼平台提供覆盖文本、图像、视频、语音、多模态等全场景的 AI 能力，支持从 Prompt 工程、RAG 构建、模型微调到实时音视频交互的完整技术栈。本文档面向开发者，结构化梳理核心使用场景、关键参数、接入方式及注意事项，帮助您快速选型并规避常见陷阱。

## 支持的模型/功能

百炼支持三大类能力：**原生模型服务**（如 Qwen 系列、万相系列）、**三方模型直供**（如 DeepSeek、Kimi、GLM、MiniMax、Stepfun 等）和**实时音视频交互套件**（WebRTC/AOQ）。其中：

- **文生文**：所有大语言模型均支持基础文本生成，推荐结合 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md) 使用 Prompt 框架提升输出稳定性；
- **文生图/图生图**：万相 V1/V2/V3.0 及历史模型（如 wanx-style-repaint-v1、wanx-virtualmodel）提供丰富编辑能力，但需注意 [历史模型指南](../../raw/model-user-guide/use-cases/legacy-resources.md) 中明确标注的地域与 API Key 限制；
- **文生视频/多模态视频**：万相 3.0、Vidu 及 legacy 视频模型均支持结构化 Prompt，但 Vidu 的提示词词典与万相 3.0 的分镜语法存在显著差异，不可混用；
- **实时音视频**：qwen3.8-omni-flash-realtime、qwen-audio-*、fun-asr-realtime 等模型通过 WebRTC 或 AOQ 协议接入，适用于低延迟对话、翻译、ASR、TTS 场景。

> **注意**：文档 41（虚拟模特生成）与文档 42（人物实例分割）均明确声明对应模型“仅提供免费体验，免费额度用完后不可调用且不支持付费”，而文档 39（万相2.1图像编辑）未作此限制，实际部署时应优先评估替代方案（如 qwen-image-edit）的长期可用性。

## 关键参数

不同模态模型的关键参数设计逻辑一致，但语义与取值范围各异：

- **Prompt 相关**：`prompt`（正向描述）、`negative_prompt`（反向约束）为文生图/视频通用参数；万相 3.0 新增 `prompt_extend`（默认开启智能改写）；Vidu 支持 `dynamic_control` 类关键词（如“大动态”）直接调控运动幅度；
- **思考模式控制**：DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun、Unisound、Ling 等三方模型普遍支持 `enable_thinking` 或 `thinking` 参数（非 OpenAI 标准），需通过 `extra_body`（Python SDK）或顶层字段（Node.js）传入；部分模型（如 stepfun/step-3.7-flash）默认强制开启且不可关闭；
- **实时交互控制**：AOQ 场景下，`turn_detection` 决定轮次划分方式（`server_vad` / `semantic_vad` / `null` for Manual mode）；WebRTC 场景下仅支持服务端 VAD，不支持 Manual 模式；
- **缓存与性能**：显式缓存依赖 `cache_control` 标记，需在请求消息中显式指定 `type: "ephemeral"` 或 `"persistent"`；高并发 TTS 需配置对象池容量（如 `COSYVOICE_OBJECTPOOL_SIZE`），避免连接耗尽。

## 使用方式

接入流程遵循“准备 → 调用 → 处理”三阶段：

1. **准备**：获取 API Key 并配置环境变量（[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)）；确认业务空间 ID 与地域（如华北2北京必须使用 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）；安装对应 SDK（DashScope ≥2.0.1 或 OpenAI SDK）；
2. **调用**：
   - 文本/图像/视频类模型：通过 RESTful API 或 SDK 同步/异步调用，注意异步任务需轮询 `task_id` 获取结果；
   - 实时音视频：WebRTC 需浏览器端创建 `RTCPeerConnection` 并处理 SDP 交换；AOQ 需客户端集成 SDK、申请临时 Token、建立连接后分轨（Audio/Data）传输；
   - RAG 应用：基于 LlamaIndex，使用 `DashScopeCloudIndex` 和 `DashScopeParse` 解析器构建知识库，详见 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)；
3. **处理**：流式响应需按 `delta.content` / `delta.reasoning_content` 分段解析；非流式响应需检查 `usage` 字段计费；AOQ 场景需监听 `result-generated`、`task-finished` 等事件。

## 限制和注意事项

- **地域与模型绑定严格**：所有三方模型（DeepSeek、Kimi、GLM、MiniMax 等）及多数 legacy 图像/视频模型（文档 39–43）均强制要求华北2（北京）地域 API Key 与 endpoint，跨地域调用将失败；
- **限流维度双重约束**：百炼 API 同时限制 RPM/TPM（分钟级）与 RPS/TPS（瞬时），突发流量易触发 `429` 错误；推荐优先启用 [服务端排队等待](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)（加 `X-DashScope-Queue-Enable: true` 请求头）而非简单重试；
- **缓存成本权衡**：显式缓存首次写入成本为标准价 25%，后续命中节省 90%；但若命中率低于约 1.2 次/缓存项，则总体成本高于无缓存方案，需结合业务访问 pattern 评估；
- **三方模型参数兼容性风险**：`enable_thinking`、`reasoning_effort`、`preserve_thinking` 等参数非 OpenAI 标准，不同供应商实现细节不一（如 Kimi 的 `reasoning_effort` 与 MiMo 的 `enable_thinking` 默认行为不同），务必以对应模型文档为准；
- **实时协议选择约束**：qwen-audio-3.1-asr-flash-streaming 必须使用 Inference 协议（`run-task`/`finish-task`），而 qwen3.8-omni-flash-realtime 必须使用 Realtime 协议（`input_audio_buffer.append`/`response.create`），协议错配将导致连接异常或无响应。

## 来源文档

- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)
- [视频生成Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [语音合成高并发最佳实践](../../raw/model-user-guide/use-cases/tts-high-concurrency-best-practices.md)
- [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [Ling-蚂蚁数科](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/antdigital.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
- [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
- [使用 AOQ 接入 qwen-audio-3.1-asr-flash-streaming 实现语音输入法](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/voice-input-using-aoq-access-qwen-audio-asr.md)
- [使用 AOQ 接入 qwen3.8-livetranslate-flash-realtime 实现实时语音翻译](../../raw/_short/real-time-translation-using-aoq-access-qwen-live-9b4d3056b2eade2b.md)
- [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](../../raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/_short/speech-synthesis-using-aoq-access-qwen-audio-3-0-43022e91dedcb0c1.md)
- [技术解决方案](../../raw/model-user-guide/use-cases/technical-solutions.md)
- [历史模型指南](../../raw/model-user-guide/use-cases/legacy-resources.md)
- [图像生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation.md)
- [通用图像编辑-万相2.1](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md)
- [人像风格重绘](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/style-repaint.md)
- [虚拟模特生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/virtual-model-generation.md)
- [人物实例分割](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/image-instance-segmentation.md)
- [鞋靴模特](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/shoes-and-boots-model.md)
- [图像擦除补全](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/image-erasure-and-completion.md)
- [创意海报生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/creative-poster-generation-overview.md)
- [图像局部重绘](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/vary-region.md)
- [视频生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation.md)
- [涂鸦作画](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/sketch-to-image.md)
- [视频编辑2.1](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/wan-vace-guide.md)
- [图生视频-基于首尾帧](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-first-and-last-frames-guide.md)
- [万相-图生视频-基于首帧](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-guide.md)


