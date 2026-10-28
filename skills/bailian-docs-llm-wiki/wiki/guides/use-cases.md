# use cases

百炼平台提供覆盖文本、图像、视频、语音、实时音视频等多模态场景的完整AI能力矩阵，支持从Prompt工程、模型调用、RAG构建到高并发流控与缓存优化的全链路开发实践。本文档面向开发者，系统梳理核心使用模式、关键参数、接入方式及关键约束，帮助您快速定位适配方案并规避常见陷阱。

## 支持的模型/功能

百炼支持三类主流模型调用路径：  
- **自研模型**：如 `qwen3.8-omni-flash-realtime`（实时多模态）、`qwen-audio-3.1-asr-flash-streaming`（流式语音识别）、`qwen3.8-livetranslate-flash-realtime`（实时语音翻译）等，均通过 AOQ 或 WebRTC 协议提供低延迟交互能力 [使用 AOQ 接入 qwen3.8-livetranslate-flash-realtime 实现实时语音翻译](../../raw/_short/real-time-translation-using-aoq-access-qwen-live-9b4d3056b2eade2b.md)；  
- **三方直供模型**：包括 DeepSeek（阿里云/硅基流动/快手万擎三版本）、Kimi（月之暗面/阿里云双源）、GLM（智谱/阿里云）、MiniMax、MiMo、Stepfun、Unisound 等，均支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)调用，但地域与功能存在差异；  
- **多模态生成模型**：文生图（万相 V1/V2）、文生视频（万相 3.0、Vidu）、图生视频、参考生视频等，各模型对 Prompt 结构、参数（如 `prompt_extend`、`negative_prompt`）和素材组合规则有明确要求 [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)。

> **注意**：DeepSeek 模型存在多个供应商版本，其中“硅基流动”版支持更长上下文，而“阿里云”版支持联网搜索与上下文缓存，二者功能不互通，需按业务需求严格区分 [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md) 与 [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)。

## 关键参数

不同模态模型的关键控制参数高度结构化：  
- **文本生成类**：通用参数包括 `model`、`messages`、`stream`；思考模式相关参数因厂商而异——DeepSeek 使用 `enable_thinking`，Kimi 使用 `reasoning_effort`，GLM-智谱同时支持 `enable_thinking` 和 `reasoning_effort`，Unisound 使用 `thinking: {"type": "enabled"}`；  
- **文生图类**：核心为 `prompt`（正向提示词）与 `negative_prompt`（反向提示词），万相 V2 额外支持 `prompt_extend: true` 启用大模型智能改写；  
- **视频生成类**：万相 3.0 支持多维度结构化 Prompt，含 `[分镜 N（起-止秒）]`、`[台词]`、`[音效/BGM]`、`[负向清单]` 等要素；Vidu 则强调“主体/场景+场景描述+环境描述+艺术风格/媒介”的初阶公式，并提供运镜、动态、特效等关键词词典 [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)；  
- **实时音视频类**：AOQ 协议下需配置 `turn_detection`（`null` 表示 Manual 模式，`server_vad` 表示服务端 VAD 模式），WebRTC 模式则依赖 `RTCPeerConnection` 的 ICE 配置与媒体轨道管理。

## 使用方式

接入流程遵循“准备→配置→调用→处理”四步法：  
- **准备阶段**：获取 API Key 并配置至环境变量或 SDK；开通对应模型服务（如在控制台 Marketplace 中点击“立即开通”）；对于 AOQ/WebRTC 场景，还需申请业务空间 ID 并配置 [Token](../concepts/token.md) 鉴权服务端代理；  
- **配置阶段**：根据模型类型选择协议（OpenAI 兼容 / DashScope / AOQ / WebRTC），设置正确的 `base_url` 或 endpoint（注意 `{WorkspaceId}` 和地域后缀，如 `cn-beijing.maas.aliyuncs.com`）；  
- **调用阶段**：文本类直接构造 `messages`；多模态类需按规范组织输入（如万相 3.0 的分镜结构、Vidu 的运镜关键词）；实时类需初始化 SDK 实例、注册事件监听器（如 `ontrack`、`onconnectionstatechange`）；  
- **处理阶段**：流式响应需按 `delta.reasoning_content` 与 `delta.content` 分离处理思考过程与最终输出；AOQ 需区分 Audio 轨（音频流）与 Data 轨（协议事件）；WebRTC 需手动绑定远端流至 `<audio>` 元素播放。

## 限制和注意事项

- **地域强约束**：绝大多数三方模型（DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun、Unisound）仅支持华北2（北京）地域，跨地域调用将失败；例外是 Kimi、GLM、DeepSeek（Responses API）等少数模型支持多地域，但需严格匹配文档中列出的可用地域列表；  
- **并发与限流**：所有 API 均受 RPM/TPM（分钟级）、RPS/TPS（瞬时）及 Traffic Burst（增速）三重限流约束，需结合 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md) 配置客户端重试、服务端排队或架构层 MQ 削峰；  
- **缓存与成本**：显式缓存（`cache_control`）可降低 90% 成本，但仅对 Anthropic 协议接入的工具（如 Claude Code、Open Code）原生支持，且需注意 `DISABLE_PROMPT_CACHING` 环境变量的模型粒度控制；  
- **实时类权限与兼容性**：WebRTC 方案需浏览器麦克风/摄像头权限，且受 CORS 限制需后端代理 SDP 交换；AOQ 方案需在各平台（Android/iOS/HarmonyOS）正确声明权限并导入 Opus 插件；  
- **模型生命周期**：部分模型存在下线计划，例如 MiMo `xiaomi/mimo-v2.5-pro` 将于 2026 年 10 月 21 日下线，必须提前迁移至 `xiaomi/mimo-v2.6-pro-ultraspeed`。

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
- [语音合成高并发最佳实践](../../raw/model-user-guide/use-cases/tts-high-concurrency-best-practices.md)
- [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
- [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [使用 AOQ 接入 qwen-audio-3.1-asr-flash-streaming 实现语音输入法](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/voice-input-using-aoq-access-qwen-audio-asr.md)
- [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
- [使用 AOQ 接入 qwen3.8-livetranslate-flash-realtime 实现实时语音翻译](../../raw/_short/real-time-translation-using-aoq-access-qwen-live-9b4d3056b2eade2b.md)
- [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](../../raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/_short/speech-synthesis-using-aoq-access-qwen-audio-3-0-43022e91dedcb0c1.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)
- [技术解决方案](../../raw/model-user-guide/use-cases/technical-solutions.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)


