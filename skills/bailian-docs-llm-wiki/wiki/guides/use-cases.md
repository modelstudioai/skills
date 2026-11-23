# use cases

百炼平台提供覆盖文本、图像、视频、语音、多模态等全场景的 AI 能力，支持从 Prompt 工程、RAG 构建、模型微调到实时音视频交互的完整技术栈。本文档面向开发者，系统梳理核心使用场景、关键参数、调用方式及实践约束，帮助快速选型与落地。

## 支持的模型/功能

百炼支持三类主流能力路径：  
- **原生大模型服务**：包括 Qwen 系列（如 `qwen3.7-max`）、三方模型（如 `deepseek-v4.1-flash`、`kimi/kimi-k3.1-pro`、`ZHIPU/GLM-5.3`）及多模态模型（如 `qwen3.8-omni-flash-realtime`），均通过 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)或 DashScope 原生 API 调用；  
- **生成式多模态模型**：万相（WanX）系列覆盖文生图（V1/V2）、文生视频（wan3.0）、图生视频、风格重绘、虚拟模特等，详见 [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md) 和 [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)；  
- **实时音视频模型**：依托 AOQ 或 WebRTC 协议接入 `qwen-audio-3.1-asr-flash-streaming`、`qwen3.8-livetranslate-flash-realtime`、`fun-asr-realtime` 等低延迟模型，适用于语音输入法、实时翻译、AI 对话等终端场景。

> **注意**：部分历史图像模型（如 `wanx-style-repaint-v1`、`shoemodel-v1`、`wanx-x-painting`）已进入免费体验阶段，额度用尽后不可调用且不支持付费，官方推荐迁移到 [图像编辑-万相2.1](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md) 或 [图像编辑-千问](../../raw/model-user-guide/model-experience/image-and-video-generation/image-model/image-edit-guide/qwen-image-edit-guide.md)。

## 关键参数

不同模型类型的关键参数差异显著，需严格按文档配置：  
- **文本模型**：通用参数包括 `model`、`messages`、`stream`；思考模式相关参数为非标准字段，需通过 `extra_body`（Python SDK）或顶层参数（Node.js SDK）传入，如 `enable_thinking: true`（[DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)）、`reasoning_effort: "max"`（[Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)）；  
- **图像/视频模型**：核心参数为 `prompt`（正向提示词）和 `negative_prompt`（反向提示词），万相 V2 还支持 `prompt_extend: true` 启用智能扩写；视频模型额外支持分镜描述、运动控制、声音描述等结构化字段（[视频生成Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)）；  
- **实时音视频模型**：依赖协议层参数，如 `server_vad`（服务端语音活动检测）、`turn_detection: null`（手动轮次控制）、`input_audio_buffer.append`（音频流提交方式），具体以 [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md) 为准。

## 使用方式

- **Prompt 工程**：推荐使用结构化公式降低试错成本。文生文场景采用「背景+目的+风格+语气」四要素框架（[文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)）；文生图/视频则按「主体+场景+运动+美学控制」分层描述，并结合词典细化镜头、风格、运镜等维度；  
- **RAG 应用构建**：基于 LlamaIndex 集成百炼知识库服务，需先通过 `DashScopeParse` 解析文档，再调用 `DashScopeCloudIndex.from_documents` 创建索引（[基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)）；  
- **实时交互接入**：WebRTC 方案适用于浏览器端低延迟语音（需处理 SDP 交换代理），AOQ 方案适用于移动端（需集成 `AoqClientSdk` 及 Opus 插件），两类方案均要求业务 AppServer 统一管理鉴权凭证；  
- **限流与缓存优化**：高频调用需启用显式缓存（`cache_control` 标记），尤其适用于 Agent 中 system prompt 固定、user message 动态的场景；突发流量可优先启用服务端排队等待（加 `X-DashScope-Queue-Enable: true` 请求头）（[限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)）。

## 限制和注意事项

- **地域与权限约束**：绝大多数三方模型（DeepSeek、Kimi、GLM、MiniMax、MiMo、Unisound、Stepfun、Ling）仅支持华北2（北京）地域调用，且必须使用该地域的 API Key 和业务空间 ID；  
- **异步任务处理**：图像/视频类 API 默认采用异步模式（`X-DashScope-Async: enable`），需先创建任务获取 `task_id`，再轮询查询结果，不可直接同步等待；  
- **输入格式限制**：图像类模型对输入文件有明确要求——分辨率（如局部重绘要求 256×256 至 4096×4096）、大小（多数 ≤10MB）、格式（JPG/PNG/BMP/WEBP）、URL 不含中文；  
- **免费额度风险**：历史图像模型（如 `image-instance-segmentation`、`virtualmodel-v2`）虽提供免费额度，但用尽后即不可用，无降级或续费选项，生产环境务必提前评估替代方案；  
- **协议兼容性**：AOQ 模型使用 Inference 或 Realtime 事件协议，与标准 OpenAI 流式响应结构不同，需按各模型文档解析 `result-generated`、`task-finished` 等事件（[使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)）。

## 来源文档

- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)
- [视频生成Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [Ling-蚂蚁数科](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/antdigital.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
- [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
- [使用 AOQ 接入 qwen3.8-livetranslate-flash-realtime 实现实时语音翻译](../../raw/_short/real-time-translation-using-aoq-access-qwen-live-9b4d3056b2eade2b.md)
- [使用 AOQ 接入 qwen-audio-3.1-asr-flash-streaming 实现语音输入法](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/voice-input-using-aoq-access-qwen-audio-asr.md)
- [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](../../raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/_short/speech-synthesis-using-aoq-access-qwen-audio-3-0-43022e91dedcb0c1.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)
- [技术解决方案](../../raw/model-user-guide/use-cases/technical-solutions.md)
- [历史模型指南](../../raw/model-user-guide/use-cases/legacy-resources.md)
- [图像生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation.md)
- [通用图像编辑-万相2.1](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md)
- [人像风格重绘](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/style-repaint.md)
- [虚拟模特生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/virtual-model-generation.md)
- [人物实例分割](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/image-instance-segmentation.md)
- [鞋靴模特](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/shoes-and-boots-model.md)
- [图像局部重绘](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/vary-region.md)
- [图像擦除补全](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/image-erasure-and-completion.md)
- [创意海报生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/creative-poster-generation-overview.md)
- [视频生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation.md)
- [涂鸦作画](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/sketch-to-image.md)
- [视频编辑2.1](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/wan-vace-guide.md)
- [图生视频-基于首尾帧](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-first-and-last-frames-guide.md)
- [万相-图生视频-基于首帧](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-guide.md)


