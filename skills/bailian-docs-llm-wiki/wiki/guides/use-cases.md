# use cases

百炼平台提供覆盖文本、图像、视频、语音、实时交互等多模态场景的完整能力矩阵，支持从基础生成到复杂工作流编排的各类业务需求。本文档面向开发者，系统梳理核心使用场景、关键参数、调用方式及实践约束，帮助您快速选型并规避常见陷阱。

## 支持的模型/功能

百炼支持三大类模型调用路径：  
- **原生模型**：包括通义千问系列（如 `qwen3.7-max`、`qwen3.8-omni-flash-realtime`）、万相系列（`wanx-text-to-image-v2`、`wan3-video-generation`）等，具备完整 API 控制能力；  
- **三方模型**：通过统一接入层集成 DeepSeek、Kimi、GLM、MiniMax、Stepfun 等 14+ 主流厂商模型，[三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md) 提供全量清单与地域限制说明；  
- **Legacy 模型**：部分历史图像工具（如 `wanx-virtualmodel`、`shoemodel-v1`、`image-instance-segmentation`）仍可调用，但已明确标注为**免费体验且不支持付费**，[历史模型指南](../../raw/model-user-guide/use-cases/legacy-resources.md) 建议优先迁移至新版万相或千问编辑模型。

> **注意**：`wanx-virtualmodel`、`shoemodel-v1`、`image-instance-segmentation`、`image-erase-completion`、`wanx-x-painting` 等 5 个 Legacy 图像模型均仅限华北2（北京）地域调用，且免费额度用完后不可续订，官方明确推荐迁移到 [图像编辑-千问](../../raw/model-user-guide/model-experience/image-and-video-generation/image-model/image-edit-guide/qwen-image-edit-guide.md) 或 [图像编辑-万相2.1](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md)。

## 关键参数

不同模态任务的关键参数差异显著，需严格按规范设置：  
- **文生文（LLM）**：核心为 `messages` 数组，支持 `system`/`user`/`assistant` 角色；若启用深度思考，需传 `enable_thinking: true`（非 OpenAI 标准参数，须通过 `extra_body` 透传）或 `reasoning_effort`（如 `"max"`），详见 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)；  
- **文生图**：必需 `prompt`（正向提示词）与可选 `negative_prompt`（反向提示词），V2 版本支持 `prompt_extend: true` 启用大模型智能扩写；  
- **文生视频**：`prompt` 描述画面内容与运动，`wan3.0` 还支持结构化分镜语法（如 `分镜1（00:00-00:03）：...`）及 `sound_description` 控制音效；  
- **实时语音交互（AOQ/RTCPeerConnection）**：关键参数为 `turn_detection`（`server_vad` 或 `null`），决定由服务端自动切分轮次还是客户端手动控制起止。

## 使用方式

- **API 调用**：所有模型均支持 HTTP 直连与 SDK 调用。[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)需配置 `base_url` 为业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），[DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md) 文档详细列出了各地域端点；  
- **SDK 集成**：语音类（TTS/ASR）推荐使用 AOQ Client SDK，需按平台导入 `AoqClientSdk` 及 `PluginOpus` 插件，并声明 `RECORD_AUDIO` 等运行时权限；WebRTC 场景则直接调用浏览器原生 `RTCPeerConnection`；  
- **低代码工具**：Prompt 优化、RAG 知识库、多模态交互套件等提供可视化配置界面，例如 RAG 应用可通过 [LlamaIndex 集成方案](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md) 快速构建。

## 限制和注意事项

- **地域与认证强绑定**：所有华北2（北京）专属模型（如 `kimi-k3`、`unisound-u2`、`stepfun/step-3.7-flash`）必须使用该地域的 API Key 和 Workspace ID，跨地域调用将失败；  
- **并发与限流**：语音合成高并发需配置对象池（如 Java 的 `COSYVOICE_OBJECTPOOL_SIZE`），模型限流按主账号维度统计，RAM 用户与业务空间共享配额，详见 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)；  
- **缓存与成本**：显式缓存（`cache_control`）可降低 90% 成本，但需在请求中显式标记；其效果依赖输入确定性，动态 system prompt（如含当前时间）会显著降低跨会话命中率；  
- **实时流式处理**：AOQ 场景下，`qwen-audio-3.1-asr-flash-streaming` 要求客户端先缓存音频再倍速补发，而 `qwen3.8-omni-flash-realtime` 的 WebRTC 模式仅支持 `server_vad`，不支持手动模式。

## 来源文档

- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)
- [视频生成Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [语音合成高并发最佳实践](../../raw/model-user-guide/use-cases/tts-high-concurrency-best-practices.md)
- [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [Ling-蚂蚁数科](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/antdigital.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
- [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
- [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [使用 AOQ 接入 qwen-audio-3.1-asr-flash-streaming 实现语音输入法](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/voice-input-using-aoq-access-qwen-audio-asr.md)
- [使用 AOQ 接入 qwen3.8-livetranslate-flash-realtime 实现实时语音翻译](../../raw/_short/real-time-translation-using-aoq-access-qwen-live-9b4d3056b2eade2b.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/_short/speech-synthesis-using-aoq-access-qwen-audio-3-0-43022e91dedcb0c1.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)
- [技术解决方案](../../raw/model-user-guide/use-cases/technical-solutions.md)
- [历史模型指南](../../raw/model-user-guide/use-cases/legacy-resources.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [图像生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation.md)
- [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](../../raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)
- [虚拟模特生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/virtual-model-generation.md)
- [鞋靴模特](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/shoes-and-boots-model.md)
- [人物实例分割](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/image-instance-segmentation.md)
- [图像擦除补全](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/image-erasure-and-completion.md)
- [图像局部重绘](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/vary-region.md)
- [通用图像编辑-万相2.1](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md)
- [涂鸦作画](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/sketch-to-image.md)
- [创意海报生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/creative-poster-generation-overview.md)
- [视频生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation.md)
- [视频编辑2.1](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/wan-vace-guide.md)
- [万相-图生视频-基于首帧](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-guide.md)
- [图生视频-基于首尾帧](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-first-and-last-frames-guide.md)
- [人像风格重绘](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/style-repaint.md)


