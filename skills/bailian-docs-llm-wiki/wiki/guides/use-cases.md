# use cases

百炼平台提供覆盖文本、图像、视频、语音、多模态等全栈 AI 能力的工程化使用场景。本文档面向开发者，系统梳理主流用例的技术路径、参数规范与实践约束，聚焦可落地的集成方案，不包含营销性描述。

## 支持的模型/功能

百炼支持三大类核心能力：**文生类（Text-to-X）**、**多模态生成与编辑**、以及**实时音视频交互**。

- **文生类**：包括文生文（Prompt 工程、RAG、自定义模型调优）、文生图（万相 V1/V2）、文生视频（万相 3.0、Vidu）、图生视频（首帧/首尾帧/参考生视频）等。其中 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md) 提供了从基础框架到风格/语气控制的完整 Prompt 设计方法论。
- **多模态生成与编辑**：涵盖图像编辑（万相 2.1 的扩图、去水印、局部重绘）、人像风格重绘、虚拟模特生成、鞋靴模特、图像擦除补全、人物实例分割等。需注意，[历史模型指南](../../raw/model-user-guide/use-cases/legacy-resources.md) 中列出的 `wanx-style-repaint-v1`、`shoemodel-v1`、`image-erase-completion` 等模型当前仅提供免费体验，额度用完后不可调用且不支持付费，官方推荐迁移到 [图像编辑-万相2.1](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md) 或 [图像编辑-千问](../../raw/model-user-guide/model-experience/image-and-video-generation/image-model/image-edit-guide/qwen-image-edit-guide.md)。
- **实时音视频交互**：通过 WebRTC 或 AOQ 协议接入 qwen3.8-omni-flash-realtime、qwen-audio-3.1-asr-flash-streaming、qwen3.8-livetranslate-flash-realtime 等模型，支持低延迟语音对话、实时翻译、语音输入法、TTS 合成等场景。AOQ 方案要求客户端严格按平台（Android/iOS/HarmonyOS）导入 SDK 及 Opus 插件，并动态申请 `RECORD_AUDIO` 权限。

> **注意**：文档 37、39、40、41、42、43 均明确标注“仅适用于华北2（北京）地域”，而文档 15（Kimi）、16（GLM）则支持华北2、新加坡、日本、美国、德国、中国香港共六地。若跨地域部署，需确认模型可用性与 endpoint 配置一致性，避免因地域不匹配导致 `404` 或 `403` 错误。

## 关键参数

不同能力线的关键参数差异显著，开发者需严格遵循模型文档：

- **Prompt 类参数**：`prompt`（正向提示词）、`negative_prompt`（反向提示词）、`prompt_extend`（文生图 V2 的智能改写开关，默认 `true`）。万相 3.0 支持更结构化的参数组合，如 `分镜 N（起-止秒）`、`台词`、`音效/BGM`、`负向清单` 等，详见 [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)。
- **思考模式参数**：DeepSeek、Kimi、MiniMax、Stepfun、MiMo、Unisound、Ling 等三方模型普遍支持 `enable_thinking`（或 `thinking`、`reasoning_effort`）控制推理过程输出。但参数传递方式不统一：OpenAI Python SDK 需通过 `extra_body` 传入非标准参数，而 `reasoning_effort` 是 OpenAI 标准参数可直接传入。
- **实时交互参数**：WebRTC 模式强制使用服务端 VAD（`server_vad` 或 `semantic_vad`），不支持手动模式；AOQ 的 Manual 模式则需将 `turn_detection` 设为 `null` 并由客户端显式调用 `input_audio_buffer.commit` 和 `response.create`。
- **异步任务参数**：图像/视频类 API 普遍采用异步模式，需设置请求头 `X-DashScope-Async: enable`，并通过 `task_id` 轮询查询结果。

## 使用方式

集成路径分为三类，按复杂度递增：

1. **零代码/低代码**：使用控制台 Prompt 优化工具（见 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)）、知识库可视化配置、多模态交互套件应用配置等。
2. **SDK/API 直接调用**：
   - 文生文：使用 DashScope SDK 或 OpenAI 兼容 SDK，注意 `base_url` 必须替换 `{WorkspaceId}` 并匹配地域（如 `cn-beijing.maas.aliyuncs.com`）。
   - 图像/视频：HTTP 异步调用为主，需处理 `task_id` 生命周期（创建 → 轮询 → 获取结果）。
   - 实时音视频：WebRTC 需浏览器端实现 `RTCPeerConnection` 与媒体流管理；AOQ 需各平台 SDK 导入、权限声明、连接凭证鉴权（凭证必须由业务 AppServer 动态下发，严禁硬编码在客户端）。
3. **框架集成**：如基于 LlamaIndex 构建 RAG 应用，需安装 `llama-index-llms-dashscope` 和 `llama-index-indices-managed-dashscope`，并配置 `DASHSCOPE_WORKSPACE_ID` 环境变量以指定业务空间。

## 限制和注意事项

- **地域与模型绑定**：绝大多数 legacy 图像/视频模型（文档 36–43）及三方模型（文档 11–24）均限定华北2（北京）地域，调用前务必核对 API Key 地域、`base_url` 地域、业务空间 ID 地域三者一致。
- **限流策略**：API 按 RPM/TPM（分钟级）、RPS/TPS（瞬时）、Traffic Burst（增速）三维度限流。突发流量触发 `429` 时，优先尝试平台层的“服务端排队等待”（加 `X-DashScope-Queue-Enable: true` 请求头），而非简单重试。
- **缓存与成本**：显式缓存（`cache_control`）可降低 90% 成本，但仅对 Anthropic 协议接入的 Agent/Coding 工具（如 Claude Code、Open Code）原生支持；普通 OpenAI 兼容调用需自行实现缓存逻辑。
- **免费额度风险**：`shoemodel-v1`、`wanx-virtualmodel`、`image-erase-completion`、`image-instance-segmentation` 等模型明确标注“免费额度用完后不可调用且不支持付费”，生产环境应提前规划替代方案。
- **安全合规**：所有客户端 SDK 示例均强调 API Key **不得写入客户端代码或提交至仓库**，必须由业务后端 AppServer 统一鉴权并下发临时凭证。

## 来源文档

- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [视频生成Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [Ling-蚂蚁数科](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/antdigital.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
- [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
- [使用 AOQ 接入 qwen-audio-3.1-asr-flash-streaming 实现语音输入法](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/voice-input-using-aoq-access-qwen-audio-asr.md)
- [使用 AOQ 接入 qwen3.8-livetranslate-flash-realtime 实现实时语音翻译](../../raw/_short/real-time-translation-using-aoq-access-qwen-live-9b4d3056b2eade2b.md)
- [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](../../raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/_short/speech-synthesis-using-aoq-access-qwen-audio-3-0-43022e91dedcb0c1.md)
- [技术解决方案](../../raw/model-user-guide/use-cases/technical-solutions.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)
- [图像生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation.md)
- [通用图像编辑-万相2.1](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md)
- [历史模型指南](../../raw/model-user-guide/use-cases/legacy-resources.md)
- [人像风格重绘](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/style-repaint.md)
- [鞋靴模特](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/shoes-and-boots-model.md)
- [虚拟模特生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/virtual-model-generation.md)
- [图像擦除补全](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/image-erasure-and-completion.md)
- [人物实例分割](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/image-instance-segmentation.md)
- [图像局部重绘](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/vary-region.md)
- [创意海报生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/creative-poster-generation-overview.md)
- [涂鸦作画](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/sketch-to-image.md)
- [视频编辑2.1](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/wan-vace-guide.md)
- [视频生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation.md)
- [图生视频-基于首尾帧](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-first-and-last-frames-guide.md)
- [万相-图生视频-基于首帧](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-guide.md)


