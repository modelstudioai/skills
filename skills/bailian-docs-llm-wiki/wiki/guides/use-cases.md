# use cases

百炼平台的 use cases 文档面向开发者，系统梳理了模型调用、内容生成、RAG 构建、实时音视频等核心应用场景。本文档整合了 Prompt 工程、多模态生成、三方模型集成、限流与缓存等关键实践，覆盖从基础调用到高阶优化的完整链路，帮助开发者快速落地业务需求。

## 支持的模型/功能

百炼支持文生文、文生图、文生视频、图生视频、参考生视频、视频编辑等多模态生成能力，以及 RAG 检索增强、自定义模型调优、实时音视频对话等专业场景。  
- **文本生成**：支持 Qwen 系列（如 `qwen3.7-max`）、DeepSeek（`deepseek-v4.1-flash`）、Kimi（`kimi-k3.1-pro`）、GLM（`glm-5.2`）、MiniMax（`MiniMax-M2.5`）、MiMo（`xiaomi/mimo-v2.6-pro-ultraspeed`）、Stepfun（`stepfun/step-3.7-flash`）、Unisound（`unisound/unisound-u2`）、Ling（`antdigital/Ling-3.1-flash`）等主流大模型，均通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 DashScope SDK 调用 [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)。  
- **图像生成**：万相系列模型（如 `wanx-text-to-image-v2`）支持文生图、局部重绘、风格重绘、虚拟模特生成等；历史模型如 `wanx-style-repaint-v1` 和 `wanx-x-painting` 仍可调用但仅限免费额度 [图像生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation.md)。  
- **视频生成**：万相3.0（`wanx-video-generation-3.0`）和 Vidu（`vidu-video-generation`）支持文生视频、图生视频、多参考视频生成等，其 Prompt 设计需遵循结构化公式 [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)。  
- **实时音视频**：`qwen3.8-omni-flash-realtime`、`qwen-audio-3.1-asr-flash-streaming`、`qwen3.8-livetranslate-flash-realtime` 等模型通过 WebRTC 或 AOQ SDK 实现低延迟语音交互。

> **注意**：文档 38、39、40、41、42 均明确标注对应模型（如 `wanx-virtualmodel`、`shoemodel-v1`、`image-instance-segmentation`）“当前仅提供免费体验，免费额度用完后不可调用且不支持付费”，而文档 36（万相2.1）和文档 16（文生图V2）则未标注此限制，表明后者为持续维护的主力模型。开发者应优先选用文档 36 和文档 16 所述能力。

## 关键参数

不同模型和任务类型的关键参数差异显著，需严格按规范配置：  
- **Prompt 相关**：文生文使用 `prompt` 字段；文生图支持 `prompt`（正向）和 `negative_prompt`（反向），V2 版本还支持 `prompt_extend`（默认开启智能改写）[文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)；视频生成中 `prompt` 必须包含主体、场景、运动三要素，并可叠加美学控制与风格化描述。  
- **思考模式控制**：DeepSeek、Kimi、MiMo、Stepfun、Unisound、Ling 等模型均支持 `enable_thinking` 或 `reasoning_effort` 参数控制推理深度，但实现方式不同——`enable_thinking` 非 OpenAI 标准参数，需通过 `extra_body` 传入；`reasoning_effort` 是标准参数，可直接传入。  
- **实时音视频**：WebRTC 模式强制使用 `server_vad`，不支持手动模式；AOQ 的 Manual 模式需将 `session.turn_detection` 设为 `null`，并由客户端显式调用 `input_audio_buffer.commit` 和 `response.create`。  
- **缓存控制**：显式缓存需在请求中添加 `cache_control` 标记（如 `{"type": "ephemeral"}`），Claude Code 工具已原生支持，其他工具需手动配置。

## 使用方式

- **Prompt 工程**：推荐使用结构化框架（主体+场景+运动/风格）设计提示词，并利用平台提供的 Prompt 一键优化工具进行扩写和细节补充。  
- **RAG 应用**：基于 LlamaIndex 构建时，需先通过 `DashScopeParse` 解析文档（支持 PDF/DOCX，单文件 ≤100MB），再加载至知识库 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。  
- **三方模型调用**：所有三方模型（DeepSeek、Kimi、GLM 等）均需在华北2（北京）地域开通服务，并使用 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` 作为 Base URL；部分模型（如硅基流动 DeepSeek）支持更长上下文，而阿里云百炼版则支持联网搜索与上下文缓存。  
- **实时音视频接入**：WebRTC 方案适用于浏览器端低延迟场景，需处理 SDP 交换代理；AOQ 方案适用于移动端（Android/iOS/HarmonyOS），需集成 `AoqClientSdk` 及 Opus 插件，并由业务 AppServer 统一管理连接凭证。

## 限制和注意事项

- **地域与 API Key 绑定**：绝大多数三方模型（DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun、Unisound、Ling）及历史图像模型（虚拟模特、鞋靴模特等）均强制要求使用华北2（北京）地域的 API Key，跨地域调用将失败。  
- **限流机制**：API 按 RPM（每分钟请求数）、TPM（每分钟 [Token](../concepts/token.md) 数）、RPS（每秒请求数）、TPS（每秒 [Token](../concepts/token.md) 数）及 Traffic Burst（突发流量）四维限流，触发后通常 1 分钟内恢复。应对策略包括服务端排队（加 `X-DashScope-Queue-Enable: true` 请求头）、Batch API、客户端自适应拥塞控制等 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。  
- **缓存成本**：显式缓存首次写入产生标准价格 25% 的额外开销，后续命中可节省 90% 成本；但若从未命中，则总体成本高于不使用缓存。  
- **模型下线风险**：文档 20 明确提示 `xiaomi/mimo-v2.5-pro` 将于 2026 年 10 月 21 日下线，开发者应尽快迁移至 `xiaomi/mimo-v2.6-pro-ultraspeed`。  
- **SDK 版本依赖**：`qwen-audio-3.1-tts-flash` 的音频接收回调 `onReceivedAudioFrame` 仅在 AOQ SDK 1.4.2 及以上版本支持，旧版本无法实现外部播放器接管。

## 来源文档

- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)
- [视频生成Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [Ling-蚂蚁数科](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/antdigital.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
- [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [使用 AOQ 接入 qwen-audio-3.1-asr-flash-streaming 实现语音输入法](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/voice-input-using-aoq-access-qwen-audio-asr.md)
- [使用 AOQ 接入 qwen3.8-livetranslate-flash-realtime 实现实时语音翻译](../../raw/_short/real-time-translation-using-aoq-access-qwen-live-9b4d3056b2eade2b.md)
- [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](../../raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)
- [使用 AOQ 接入 qwen-audio-3.1-tts-flash 实现语音合成](../../raw/_short/speech-synthesis-using-aoq-access-qwen-audio-3-0-43022e91dedcb0c1.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)
- [技术解决方案](../../raw/model-user-guide/use-cases/technical-solutions.md)
- [历史模型指南](../../raw/model-user-guide/use-cases/legacy-resources.md)
- [图像生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation.md)
- [通用图像编辑-万相2.1](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md)
- [人像风格重绘](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/style-repaint.md)
- [虚拟模特生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/virtual-model-generation.md)
- [鞋靴模特](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/shoes-and-boots-model.md)
- [人物实例分割](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/image-instance-segmentation.md)
- [图像擦除补全](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/image-erasure-and-completion.md)
- [图像局部重绘](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/vary-region.md)
- [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
- [涂鸦作画](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/sketch-to-image.md)
- [创意海报生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/creative-poster-generation-overview.md)
- [视频生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation.md)
- [视频编辑2.1](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/wan-vace-guide.md)
- [图生视频-基于首尾帧](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-first-and-last-frames-guide.md)
- [万相-图生视频-基于首帧](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-guide.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)


