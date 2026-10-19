# use cases

百炼平台的 use cases 文档系统性地覆盖了从基础 Prompt 工程、多模态生成（文生图/文生视频/文档转视频）、RAG 应用构建，到模型调优、限流应对、缓存优化及实时音视频接入等核心开发者场景。所有实践均基于平台提供的 API、SDK 和控制台能力，强调可复现性与工程落地性。

## 支持的模型/功能

百炼支持三类主流使用路径：  
- **原生模型服务**：包括 Qwen 系列（如 `qwen3.8-omni-flash-realtime`、`qwen-audio-3.1-asr-flash-streaming`）、万相（`wan3.0` 视频生成、`万相-文生图V2`）、以及语音合成（`Qwen-Audio-TTS`、`CosyVoice`）等；  
- **三方模型集成**：通过 [OpenAI 兼容接口](../concepts/openai-compatibility.md)或 DashScope SDK 接入 DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun、Unisound 等厂商直供模型，[DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md) 与 [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md) 在上下文长度与联网能力上存在差异；  
- **[实时交互](../concepts/realtime.md)套件**：提供 WebRTC（浏览器端）与 AOQ（移动端/嵌入式）双通道，支持 `qwen3.8-omni-flash-realtime`、`qwen3.8-livetranslate-flash-realtime`、`fun-asr-realtime` 等 Realtime 模型，适用于低延迟语音对话、翻译、ASR 等场景。

> **注意**：部分三方模型（如 [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)、[GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)）明确限定仅在华北2（北京）地域可用，而 [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md) 和 [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md) 则支持多地域（含新加坡、美国弗吉尼亚等），部署前需严格核对地域限制。

## 关键参数

不同模态任务的关键参数设计高度结构化：  
- **文生文**：依赖 `messages` 数组（含 `role`/`content`）和可选 `stream`、`enable_thinking`（触发 `reasoning_content` 字段）、`reasoning_effort`（控制思考深度）等扩展参数；  
- **文生图**：核心为 `prompt`（正向提示词）与 `negative_prompt`（反向提示词），`万相-文生图V2` 额外支持 `prompt_extend: true` 启用大模型智能改写；  
- **文生视频**：`prompt` 是主干，`wan3.0` 支持完整公式（含分镜、台词、音效、负向清单），而 `Vidu` 则强调“主体/场景+场景描述+环境描述+艺术风格/媒介”四要素组合；  
- **实时音视频**：`turn_detection` 参数决定轮次控制模式（`server_vad` 或 `null` 表示 Manual 模式），`input_audio_buffer.append` / `.commit` 和 `response.create` 的调用时机直接影响交互逻辑；  
- **显式缓存**：通过 `cache_control: {"type": "ephemeral"}` 标记关键消息（system/user），由 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md) 定义命中策略。

## 使用方式

典型工作流遵循“准备→配置→调用→处理”四步：  
- **Prompt 工程**：优先使用 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md) 中的 Prompt 框架（背景/目的/风格/语气/受众/输出），或借助控制台 Prompt 一键优化工具扩写；  
- **多模态生成**：文生图/视频需按对应公式组织提示词，图生视频需额外传入首帧图；文档转视频则需先切片、再生成图文稿、最后合成音画；  
- **RAG 应用**：基于 LlamaIndex，使用 `DashScopeParse` 解析文档，`DashScopeCloudIndex` 创建知识库，再通过 `retriever` 查询；  
- **实时接入**：WebRTC 方案需在浏览器中创建 `RTCPeerConnection` 并管理媒体流；AOQ 方案需导入 SDK、申请权限、通过 AppServer 获取 Token，并按 Inference 或 Realtime 协议发送事件；  
- **高并发/缓存**：语音合成推荐对象池复用连接；显式缓存需在请求中显式注入 `cache_control`，并注意 Claude Code 默认包含动态信息（如 git 状态）可能降低跨会话命中率。

## 限制和注意事项

- **地域与模型绑定**：多数三方模型（如 Kimi、GLM、MiMo）仅限华北2（北京），调用前必须确认 `base_url` 中 `{WorkspaceId}` 对应的地域域名，否则返回 404；  
- **限流维度**：API 同时受 RPM（每分钟请求数）、TPM（每分钟 Token 数）、RPS（每秒请求数）及 Traffic Burst（突发流量）四重约束，[限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md) 明确建议优先启用服务端排队等待（加 `X-DashScope-Queue-Enable: true` 请求头）；  
- **实时模型模式差异**：WebRTC 仅支持服务端 VAD 模式，不支持 Manual 模式；而 AOQ 的 `qwen3.8-omni-flash-realtime` 同时支持两种模式，需根据业务需求（如按键通话 vs 自动检测）选择 `turn_detection` 配置；  
- **缓存与动态内容**：显式缓存对 system prompt 中的动态字段（日期、目录路径）敏感，[显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md) 建议使用 `--exclude-dynamic-system-prompt-sections` 参数提升跨会话命中率；  
- **三方模型参数兼容性**：`enable_thinking`、`reasoning_effort`、`thinking` 等非 OpenAI 标准参数，在 Python SDK 中需通过 `extra_body` 传入，Node.js SDK 中作为顶层参数，未正确传递将导致参数被忽略。

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
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
- [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
- [使用 AOQ 接入 qwen-audio-3.1-asr-flash-streaming 实现语音输入法](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/voice-input-using-aoq-access-qwen-audio-asr.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [使用 AOQ 接入 qwen3.8-livetranslate-flash-realtime 实现实时语音翻译](../../raw/_short/real-time-translation-using-aoq-access-qwen-live-9b4d3056b2eade2b.md)
- [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)
- [技术解决方案](../../raw/model-user-guide/use-cases/technical-solutions.md)
- [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](../../raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/_short/speech-synthesis-using-aoq-access-qwen-audio-3-0-43022e91dedcb0c1.md)


