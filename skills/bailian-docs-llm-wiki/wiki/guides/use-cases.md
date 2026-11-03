# use cases

百炼平台提供覆盖文本、图像、视频、语音、[多模态](../concepts/multi-modal.md)等全场景的 AI 能力，支持从 Prompt 工程、RAG 构建、模型微调到实时音视频交互的完整技术栈。本文档面向开发者，结构化梳理核心使用场景、关键参数、调用方式及约束条件，帮助快速选型与落地。

## 支持的模型/功能

百炼支持三类模型接入路径：  
- **原生模型**：如 `qwen3.8-omni-flash-realtime`（实时[多模态](../concepts/multi-modal.md)）、`wanx2.1-imageedit`（通用图像编辑）、`qwen-audio-3.1-asr-flash-streaming`（流式语音识别）；  
- **三方模型**：通过 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)或 DashScope SDK 接入 DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun、Ling、Unisound 等厂商模型，[三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md) 提供了各模型的地域限制、参数差异与开通路径；  
- **历史/遗留模型**：如 `wanx-style-repaint-v1`（人像风格重绘）、`shoemodel-v1`（鞋靴模特）、`image-instance-segmentation`（人物实例分割）等，均属华北2（北京）专属、仅限免费体验且不支持付费续用，详见 [历史模型指南](../../raw/model-user-guide/use-cases/legacy-resources.md)。

> **注意**：`wanx-virtualmodel` 和 `virtualmodel-v2` 当前仅提供免费体验，额度用尽后不可调用，官方明确推荐迁移到 [图像编辑-万相2.1](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md) 或 [图像编辑-千问](../../raw/model-user-guide/model-experience/image-and-video-generation/image-model/image-edit-guide/qwen-image-edit-guide.md) 作为替代方案。

## 关键参数

不同模态任务的关键参数存在显著差异：  
- **文生文**：核心为 `prompt` 字段，推荐使用 [Prompt 框架](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)（背景+目的+风格+语气），并可启用 `cache_control` 实现显式缓存；  
- **文生图/图生图**：除 `prompt` 外，需配置 `negative_prompt`（反向提示词）和 `prompt_extend`（V2 默认开启的大模型智能改写）；  
- **文生视频**：`wan3.0` 支持结构化提示词要素，包括 `[分镜 N（起-止秒）：主体 + 场景 + 运动 + 美学控制]`、`[台词]`、`[音效/BGM]`、`[负向清单]`，详见 [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)；  
- **实时音视频**：`qwen3.8-omni-flash-realtime` 等模型依赖 `turn_detection` 参数控制轮次模式（`server_vad`/`semantic_vad`/`null`），Manual 模式需客户端显式调用 `input_audio_buffer.commit` 和 `response.create`。

## 使用方式

- **API 调用**：所有模型均提供 HTTP API 与 SDK 封装（Python/Java/Node.js），需配置 `DASHSCOPE_API_KEY` 及对应地域的 `base_url`（如华北2为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）；  
- **框架集成**：支持 LlamaIndex 构建 RAG 应用，通过 `DashScopeCloudIndex` 直接对接百炼知识库服务，文档解析依赖 `DashScopeParse`；  
- **工具链协同**：  
  - Prompt 优化可借助控制台 [Prompt 一键优化工具](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)；  
  - 视频生成支持 `wan3-pe` Skill 调试（下载 ZIP 后在对话框输入 `/wan3-pe`）；  
  - 实时语音识别（ASR）与合成（TTS）需结合 AOQ Client SDK，按平台（Android/iOS/HarmonyOS）导入 `AoqClientSdk` 与 `PluginOpus` 插件。

## 限制和注意事项

- **地域与权限强绑定**：绝大多数三方模型（DeepSeek、Kimi、GLM、MiMo 等）及全部 Legacy 图像模型仅支持华北2（北京），且必须使用该地域的 API Key 与业务空间 ID；  
- **限流维度双重约束**：API 同时受 **RPM/TPM（分钟级）** 和 **RPS/TPS（瞬时）** 限制，突发流量（Traffic Burst）会动态触发增速限流，建议优先采用 [服务端排队等待](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)（加 `X-DashScope-Queue-Enable: true` 请求头）；  
- **免费额度与生命周期**：Legacy 图像模型（如 `image-erase-completion`、`shoemodel-v1`）虽提供 500 张免费额度，但明确标注“免费额度用完后不可调用且不支持付费”，无降级或续费路径；  
- **缓存与成本权衡**：显式缓存（`cache_control`）首次写入产生 25% 额外开销，但命中后可节省 90% 成本，适用于高频复用相同 Prompt 的工业级 Agent 场景；  
- **实时流式协议差异**：AOQ 接入需区分 `Realtime` 协议（用于 omni-flash-realtime）与 `Inference` 协议（用于 fun-asr-realtime、qwen-audio-3.0-tts-flash），前者事件走 Data 轨、音频走 Audio 轨，后者需通过 `run-task`/`continue-task` 控制任务生命周期。

## 来源文档

- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [视频生成Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
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
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [Ling-蚂蚁数科](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/antdigital.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
- [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
- [使用 AOQ 接入 qwen-audio-3.1-asr-flash-streaming 实现语音输入法](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/voice-input-using-aoq-access-qwen-audio-asr.md)
- [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](../../raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)
- [使用 AOQ 接入 qwen3.8-livetranslate-flash-realtime 实现实时语音翻译](../../raw/_short/real-time-translation-using-aoq-access-qwen-live-9b4d3056b2eade2b.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/_short/speech-synthesis-using-aoq-access-qwen-audio-3-0-43022e91dedcb0c1.md)
- [历史模型指南](../../raw/model-user-guide/use-cases/legacy-resources.md)
- [技术解决方案](../../raw/model-user-guide/use-cases/technical-solutions.md)
- [图像生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation.md)
- [通用图像编辑-万相2.1](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md)
- [人像风格重绘](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/style-repaint.md)
- [虚拟模特生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/virtual-model-generation.md)
- [鞋靴模特](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/shoes-and-boots-model.md)
- [人物实例分割](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/image-instance-segmentation.md)
- [图像擦除补全](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/image-erasure-and-completion.md)
- [图像局部重绘](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/vary-region.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [创意海报生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/creative-poster-generation-overview.md)
- [视频编辑2.1](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/wan-vace-guide.md)
- [图生视频-基于首尾帧](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-first-and-last-frames-guide.md)
- [万相-图生视频-基于首帧](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-guide.md)
- [视频生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation.md)
- [涂鸦作画](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/sketch-to-image.md)


