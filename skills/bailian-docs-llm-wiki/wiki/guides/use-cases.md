# use cases

百炼平台提供覆盖文本、图像、视频、语音等多模态任务的完整用例体系，支持从基础 [Prompt 工程](../concepts/prompt-engineering.md)到复杂实时交互的全栈开发。本文档结构化梳理核心能力边界、关键参数、调用方式及工程约束，面向开发者提供可直接落地的技术参考。

## 支持的模型/功能

百炼支持三大类模型能力：**文生文（LLM）**、**多模态生成（文生图/文生视频/图生视频等）** 和 **实时音视频交互（Realtime/AOQ）**。

- **文生文**：除自研 Qwen 系列外，还集成 DeepSeek、Kimi、GLM、MiniMax、MiMo、Ling、Stepfun、Unisound 等十余家第三方模型，均通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 DashScope 原生 API 接入。各模型普遍支持 `enable_thinking` 或 `reasoning_effort` 参数控制推理深度，但具体行为存在差异（见下文“关键参数”）。  
- **多模态生成**：覆盖万相（WanX）全系模型，包括 [文生图V2](raw/model-user-guide/use-cases/text-to-image-prompt.md)、[万相3.0视频生成](raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)、[Vidu视频生成](raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)，以及图像编辑类能力（如通用图像编辑、人像风格重绘、虚拟模特生成等）。  
- **实时音视频**：提供 WebRTC 和 AOQ 两种接入路径，支持 qwen3.8-omni-flash-realtime、qwen-audio-3.1-asr-flash-streaming、qwen3.8-livetranslate-flash-realtime 等模型，适用于低延迟通话、语音输入法、实时翻译、TTS 合成等场景。

> **注意**：文档 38（虚拟模特生成）、39（鞋靴模特）、40（人物实例分割）、41（图像擦除补全）均明确标注“当前仅提供免费体验，免费额度用完后不可调用且不支持付费”，而文档 35 的总览页未作此说明，存在信息不一致。实际使用应以各子模型文档为准。

## 关键参数

不同任务类型的关键参数设计逻辑高度统一，但语义和取值范围有显著区别：

- **Prompt 相关参数**：  
  - 文生文：无显式 `prompt` 字段，由 `messages` 数组承载；`system` 角色消息用于设定背景与目的，是 Prompt 框架的核心组成部分（参见 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)）。  
  - 文生图：`prompt`（正向提示词）和 `negative_prompt`（反向提示词）为必需字段；V2 版本额外支持 `prompt_extend: true/false` 控制是否启用大模型智能改写。  
  - 文生视频：万相3.0 使用结构化公式，包含 `[分镜 N（起-止秒）：主体 + 场景 + 运动 + 美学控制]` 等模块；Vidu 则强调 `主体/场景+场景描述+环境描述+艺术风格/媒介` 的线性组合，并支持 `大动态`、`左移`、`固定镜头` 等触发关键词（参见 [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)）。  

- **思考模式参数**：  
  多数第三方模型（DeepSeek、Kimi、GLM、MiniMax、MiMo、Ling、Stepfun、Unisound）均支持开启推理过程输出，但参数名和默认行为不一：`enable_thinking`（DeepSeek/Kimi/MiMo/Ling）、`reasoning_effort`（Kimi/GLM/Unisound）、`thinking`（Unisound）、或完全默认开启（Stepfun）。需严格按各模型文档配置，例如 `stepfun/step-3.7-flash` 不支持关闭思考模式，而 `kimi/kimi-k2.6` 默认开启但可通过 `enable_thinking: false` 关闭。

- **实时交互参数**：  
  WebRTC 模式强制使用服务端 VAD（`server_vad` 或 `semantic_vad`），不支持手动模式；AOQ 的 Manual 模式则需将 `turn_detection` 设为 `null`，并由客户端显式调用 `input_audio_buffer.commit` 和 `response.create`（参见 [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)）。

## 使用方式

- **API 调用**：所有模型均支持 HTTP RESTful API 和 SDK（Python/Java/Node.js）调用。地域敏感型服务（如华北2北京）要求 `base_url` 中嵌入 `{WorkspaceId}` 并匹配对应地域的 API Key；[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)需设置 `model` 字段为完整模型 ID（如 `deepseek-v4-pro`、`kimi/kimi-k3.1-pro`）。  
- **[Prompt 工程](../concepts/prompt-engineering.md)**：推荐使用 [Prompt 框架](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)（背景+目的+风格）构建清晰指令；对图像/视频任务，应优先采用进阶公式（如文生图的“主体+场景+风格+镜头语言+氛围词”），并在必要时利用平台提供的 Prompt 一键优化工具。  
- **实时流式处理**：WebRTC 需处理 `RTCPeerConnection` 生命周期与 `ontrack` 回调；AOQ 需区分 Audio 轨（传输 Opus 音频）与 Data 轨（传输 JSON 事件），并严格遵循 `run-task` → `result-generated` → `finish-task` 的 Inference 协议流程。  
- **[异步任务](../concepts/asynchronous-task.md)**：图像/视频类模型（如虚拟模特、人像分割）因计算耗时长，必须采用异步模式：先调用任务创建接口获取 `task_id`，再轮询查询结果接口。

## 限制和注意事项

- **地域与权限强绑定**：绝大多数第三方模型（DeepSeek、Kimi、GLM、MiniMax、MiMo、Ling、Stepfun、Unisound）及图像/视频类服务（万相、Vidu、虚拟模特等）均**仅限华北2（北京）地域使用**，且必须使用该地域的 API Key 和业务空间 ID。跨地域调用将失败。  
- **限流策略双重约束**：百炼 API 同时受 **RPM/TPM（每分钟请求数/[Token](../concepts/token.md) 数）** 和 **RPS/TPS（每秒请求数/[Token](../concepts/token.md) 数）** 限制，突发流量易触发 `429` 错误。推荐优先启用 [服务端排队等待](raw/model-user-guide/use-cases/rate-limiting-best-practices.md)（加 `X-DashScope-Queue-Enable: true` 请求头），而非简单重试。  
- **缓存与成本权衡**：显式缓存（`cache_control`）可降低 90% 成本，但仅对完全相同的 Prompt 输入生效；其价值在高频复用场景（如 Agent 的 system reminder）中最为显著，首次写入有 25% 额外开销。  
- **免费额度陷阱**：多个图像处理模型（`wanx-style-repaint-v1`、`shoemodel-v1`、`image-instance-segmentation`、`image-erase-completion`）虽提供免费额度，但明确声明“用完即停、不支持付费”，生产环境需提前规划替代方案（如迁移到 [图像编辑-万相2.1](raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md)）。  
- **安全红线**：API Key 必须存储于服务端（AppServer），**严禁硬编码至客户端代码或前端 JS**；移动端需通过 AppServer 动态签发临时凭证（如 AOQ [Token](../concepts/token.md)），避免密钥泄露风险。

## 来源文档

- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)
- [视频生成Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Ling-蚂蚁数科](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/antdigital.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
- [使用 AOQ 接入 qwen-audio-3.1-asr-flash-streaming 实现语音输入法](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/voice-input-using-aoq-access-qwen-audio-asr.md)
- [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](../../raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)
- [使用 AOQ 接入 qwen3.8-livetranslate-flash-realtime 实现实时语音翻译](../../raw/_short/real-time-translation-using-aoq-access-qwen-live-9b4d3056b2eade2b.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/_short/speech-synthesis-using-aoq-access-qwen-audio-3-0-43022e91dedcb0c1.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)
- [图像生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation.md)
- [通用图像编辑-万相2.1](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md)
- [人像风格重绘](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/style-repaint.md)
- [虚拟模特生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/virtual-model-generation.md)
- [鞋靴模特](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/shoes-and-boots-model.md)
- [人物实例分割](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/image-instance-segmentation.md)
- [图像擦除补全](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/image-erasure-and-completion.md)
- [图像局部重绘](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/vary-region.md)
- [创意海报生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/creative-poster-generation-overview.md)
- [涂鸦作画](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/sketch-to-image.md)
- [视频生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation.md)
- [技术解决方案](../../raw/model-user-guide/use-cases/technical-solutions.md)
- [视频编辑2.1](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/wan-vace-guide.md)
- [图生视频-基于首尾帧](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-first-and-last-frames-guide.md)
- [万相-图生视频-基于首帧](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-guide.md)
- [历史模型指南](../../raw/model-user-guide/use-cases/legacy-resources.md)


