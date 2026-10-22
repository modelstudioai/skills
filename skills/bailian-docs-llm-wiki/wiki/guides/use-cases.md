# use cases

百炼平台的 use cases 覆盖从基础文本生成到多模态视频创作、实时音视频交互、RAG 应用构建及模型服务集成等完整技术栈。本文档面向开发者，系统梳理核心能力边界、关键参数配置、调用方式与工程约束，聚焦可落地的技术实践。

## 支持的模型/功能

百炼支持三大类模型能力：**文生文（LLM）**、**多模态生成（文生图/文生视频/图生视频/参考生视频）** 和 **实时音视频（ASR/TTS/LiveTranslate/Omni）**。

- **文生文**：除通义千问系列外，还集成 DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun、Unisound 等第三方模型，均通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 DashScope SDK 调用 [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)。各模型在思考模式（`enable_thinking`/`reasoning_effort`）、上下文长度、工具调用等能力上存在差异，需按文档确认支持项。
- **多模态生成**：
  - 文生图：万相-文生图 V1/V2，支持 `prompt`（正向）与 `negative_prompt`（反向）双参数，V2 默认启用大模型智能改写（`prompt_extend: true`）[文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)。
  - 视频生成：万相3.0、万相2.x 及 Vidu 均提供结构化提示词公式，支持分镜控制、声音描述、多参考素材融合等高级能力 [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)。
- **实时音视频**：通过 WebRTC 或 AOQ 协议接入 qwen3.8-omni-flash-realtime、qwen-audio-3.1-asr-flash-streaming、qwen3.8-livetranslate-flash-realtime 等模型，支持 Manual/VAD 两种轮次控制模式，适用于语音输入法、按键对话、实时翻译等低延迟场景 [使用 AOQ 接入 qwen-audio-3.1-asr-flash-streaming 实现语音输入法](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/voice-input-using-aoq-access-qwen-audio-asr.md)。

> **注意**：Vidu 与万相系列视频模型的提示词公式和词典体系不兼容，Vidu 强调“主体/场景+场景描述+环境描述+艺术风格/媒介”四段式结构，并提供独立的运镜、特效、导演风格等关键词词典；而万相3.0 采用更细粒度的 `[分镜 N（起-止秒）：主体 + 场景 + 运动 + 美学控制]` 结构。开发者需根据目标模型选用对应指南。

## 关键参数

不同模型类型的关键参数差异显著，需严格遵循 API 规范：

- **文生文通用参数**：`model`（模型 ID）、`messages`（ChatML 格式）、`stream`（流式开关）。第三方模型普遍扩展非标准参数：`enable_thinking`（开启思考链）、`reasoning_effort`（控制推理深度）、`preserve_thinking`（多轮传递思考过程），均需通过 `extra_body`（Python SDK）或顶层字段（Node.js SDK）传入。
- **文生图参数**：`prompt`（必需，中英文）、`negative_prompt`（可选）、`prompt_extend`（仅 V2，默认 `true`）。
- **视频生成参数**：除 `prompt` 外，万相3.0 支持 `prompt_extend`、分镜时间戳、台词、音效等复合字段；Vidu 则依赖“动态控制”“运镜控制”“导演风格”等关键词触发效果。
- **实时音视频参数**：WebRTC 模式下需配置 `server_vad` 或 `semantic_vad`；AOQ 模式下通过 `turn_detection: null` 启用 Manual 模式，并配合 `input_audio_buffer.commit` 和 `response.create` 控制轮次。

## 使用方式

- **API 调用**：所有模型均支持 HTTP RESTful 接口与 SDK（Python/Java/Node.js）。[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)需配置 `base_url` 为业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），并确保 API Key 与地域匹配。
- **SDK 集成**：
  - LlamaIndex RAG：使用 `llama-index-llms-dashscope` 和 `llama-index-indices-managed-dashscope` 包，通过 `DashScopeCloudIndex` 创建/读取知识库 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。
  - AOQ 实时 SDK：需按平台（Android/iOS/HarmonyOS）导入 `AoqClientSdk` 及 Opus 插件，配置 ABI 和运行时权限（如 `RECORD_AUDIO`），并通过 AppServer 代理 Token 鉴权。
- **缓存与性能优化**：
  - 显式缓存：对高频复用 Prompt，可在请求中添加 `cache_control` 标记，首次写入成本为标准价 25%，后续命中节省 90% 成本 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)。
  - 高并发 TTS：使用对象池复用合成对象与 WebSocket 连接，Python 需 `dashscope>=1.25.2`，Java 需 `dashscope-sdk-java>=2.16.6` 并集成 `commons-pool2`。

## 限制和注意事项

- **地域与模型绑定**：多数第三方模型（DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun、Unisound）仅限华北2（北京）地域调用，且需使用该地域的 API Key 和业务空间 ID。跨地域调用将失败。
- **限流策略**：API 按 RPM（每分钟请求数）、TPM（每分钟 Token 数）、RPS（每秒请求数）、TPS（每秒 Token 数）及 Traffic Burst（突发流量）四维度限流。突发流量触发后恢复时间约 1 分钟，推荐优先启用服务端排队等待（加 `X-DashScope-Queue-Enable: true` 请求头）[限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。
- **实时音视频约束**：
  - WebRTC 模式受浏览器 CORS 限制，SDP 交换需由业务后端代理，Demo 中需手动 curl。
  - AOQ 模式下，`qwen-audio-3.0-tts-flash` 不需要麦克风权限，但 `qwen-audio-3.1-asr-flash-streaming` 和 `fun-asr-realtime` 必须申请 `RECORD_AUDIO` 权限。
- **模型生命周期**：部分模型存在下线计划，例如 MiMo-v2.5-pro 将于 2026 年 10 月 21 日下线，需提前迁移至 `xiaomi/mimo-v2.6-pro-ultraspeed`。

## 来源文档

- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)
- [视频生成Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [语音合成高并发最佳实践](../../raw/model-user-guide/use-cases/tts-high-concurrency-best-practices.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
- [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [使用 AOQ 接入 qwen-audio-3.1-asr-flash-streaming 实现语音输入法](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/voice-input-using-aoq-access-qwen-audio-asr.md)
- [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
- [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](../../raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)
- [使用 AOQ 接入 qwen3.8-livetranslate-flash-realtime 实现实时语音翻译](../../raw/_short/real-time-translation-using-aoq-access-qwen-live-9b4d3056b2eade2b.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/_short/speech-synthesis-using-aoq-access-qwen-audio-3-0-43022e91dedcb0c1.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)
- [技术解决方案](../../raw/model-user-guide/use-cases/technical-solutions.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)


