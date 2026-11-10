# use cases

百炼平台提供覆盖文本、图像、视频、语音、实时交互等多模态场景的丰富用例，支持从基础 Prompt 工程、RAG 构建到高并发音视频处理的全栈开发需求。本文档面向开发者，结构化梳理核心能力边界、关键参数与实践约束，帮助快速选型与落地。

## 支持的模型/功能

百炼支持三大类模型调用路径：  
- **原生模型**：包括文生文（如 `qwen3.7-max`）、文生图（`wanx-text-to-image-v2`）、文生视频（`wan3-video-generation`）、语音合成（`qwen-audio-tts`）等阿里云自研模型；  
- **三方模型**：通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 DashScope SDK 接入 DeepSeek、Kimi、GLM、MiniMax、Stepfun、Ling 等 10+ 家厂商模型，详见 [三方模型调用教程](raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)；  
- **实时交互模型**：专为低延迟设计的 `qwen3.8-omni-flash-realtime`、`qwen-audio-3.1-realtime-plus` 等，需配合 WebRTC 或 AOQ SDK 使用，参见 [实时音视频接入](raw/model-user-guide/use-cases/realtime-audio-video-integration.md)。  

> **注意**：部分历史图像模型（如 `wanx-style-repaint-v1`、`shoemodel-v1`、`image-instance-segmentation`）已进入免费体验阶段，额度用尽后不可调用且不支持付费，官方推荐迁移到 [图像编辑-万相2.1](raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md) 或 [图像编辑-千问](raw/model-user-guide/model-experience/image-and-video-generation/image-model/image-edit-guide/qwen-image-edit-guide.md) 等替代方案。

## 关键参数

不同模态任务的关键参数存在显著差异：  
- **文生文**：核心为 `messages`（含 `role`/`content`），高级能力依赖 `enable_thinking`（控制思考模式）、`reasoning_effort`（控制推理深度）等非标准参数，各三方模型实现方式不一（如 DeepSeek 通过 `extra_body` 传入，Kimi 直接作为顶层字段）；  
- **文生图/视频**：`prompt`（正向提示词）与 `negative_prompt`（反向提示词）为必填项；万相 V2 及 Wan3 支持 `prompt_extend: true` 启用大模型智能扩写，该功能在 [文生图Prompt指南](raw/model-user-guide/use-cases/text-to-image-prompt.md) 中有详细说明；  
- **实时语音模型**：`turn_detection` 参数决定轮次控制策略——`server_vad` 或 `semantic_vad` 表示服务端自动检测，`null` 表示客户端手动控制（如按键通话），该配置逻辑在 [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md) 中明确区分；  
- **显式缓存**：通过 `cache_control` 字段标记可缓存消息（如 `{"type": "ephemeral"}`），仅 Anthropic 协议兼容端点（如 `qwen3.7-max`）原生支持，详见 [显式缓存最佳实践](raw/model-user-guide/use-cases/explicit-cache-guide.md)。

## 使用方式

- **Prompt 工程**：推荐采用结构化框架，文生文使用「背景+目的+风格」三要素，文生图/视频则按「主体+场景+运动/风格+镜头语言」分层描述；万相 3.0 支持更细粒度的 `分镜 N（起-止秒）` 语法，大幅提升多镜头叙事可控性；  
- **RAG 应用构建**：基于 LlamaIndex，需先用 `DashScopeParse` 解析文档（支持 PDF/DOCX，单文件 ≤100MB），再通过 `DashScopeCloudIndex.from_documents()` 创建知识库，完整流程见 [基于LlamaIndex构建RAG应用](raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)；  
- **高并发优化**：语音合成场景必须复用连接池——Python 使用 `dashscope>=2.0.1` 的对象池，Java 需搭配 `commons-pool2`，并发数建议设为峰值的 1.5–2 倍；限流应对则优先启用平台级 [服务端排队等待](raw/model-user-guide/use-cases/rate-limiting-best-practices.md)，仅需添加请求头即可生效；  
- **实时音视频**：WebRTC 模式适用于浏览器端，需处理 SDP 交换代理；AOQ 模式适用于移动端（Android/iOS/HarmonyOS），需集成 `AoqClientSdk` 及 `PluginOpus` 插件，并动态申请 `RECORD_AUDIO` 权限。

## 限制和注意事项

- **地域与 API Key 绑定**：绝大多数三方模型（DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun、Unisound、Ling）及所有实时模型仅支持华北2（北京）地域，且必须使用该地域生成的 API Key，跨地域调用将失败；  
- **免费额度与计费切换**：`wanx-style-repaint-v1`、`virtualmodel-v2`、`shoemodel-v1`、`image-instance-segmentation`、`image-erase-completion` 等历史图像模型均处于“免费体验”状态，额度耗尽后服务不可用，无付费通道，迁移路径已在对应文档中明确；  
- **模型能力差异**：`stepfun/step-3.7-flash` 默认强制开启思考模式且不支持关闭；而 `xiaomi/mimo-v2.5-pro` 虽默认开启，但可通过 `enable_thinking: false` 显式关闭——此类行为不一致需在代码中按模型 ID 分支处理；  
- **安全与合规**：API Key 必须由业务 AppServer 代理获取并下发临时凭证，严禁硬编码于客户端（尤其 Android/iOS）；所有音视频权限（`RECORD_AUDIO`/`CAMERA`）须在运行时动态申请，不得预声明。

## 来源文档

- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [视频生成Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)
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
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [Ling-蚂蚁数科](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/antdigital.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
- [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [使用 AOQ 接入 qwen-audio-3.1-asr-flash-streaming 实现语音输入法](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/voice-input-using-aoq-access-qwen-audio-asr.md)
- [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
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
- [鞋靴模特](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/shoes-and-boots-model.md)
- [人物实例分割](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/image-instance-segmentation.md)
- [图像擦除补全](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/image-erasure-and-completion.md)
- [图像局部重绘](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/vary-region.md)
- [创意海报生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/creative-poster-generation-overview.md)
- [涂鸦作画](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/sketch-to-image.md)
- [视频编辑2.1](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/wan-vace-guide.md)
- [视频生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation.md)
- [万相-图生视频-基于首帧](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-guide.md)
- [图生视频-基于首尾帧](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-first-and-last-frames-guide.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)


