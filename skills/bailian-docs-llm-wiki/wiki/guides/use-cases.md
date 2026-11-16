# use cases

百炼平台提供覆盖文本、图像、视频、语音等多模态任务的丰富用例，支持从基础生成到复杂工作流编排的全场景需求。本文档结构化梳理核心能力边界、关键参数配置、调用方式及工程约束，面向开发者提供可直接落地的技术参考。

## 支持的模型/功能

百炼平台支持三大类模型能力：**原生大模型（LLM）**、**多模态生成模型（AIGC）** 和 **实时音视频模型（Realtime）**。

- **原生大模型**：除通义千问系列外，还集成 DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun、Unisound、Ling 等十余家第三方模型，均通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 DashScope 原生 API 接入，支持思考模式（`reasoning_content`）、[流式输出](../concepts/streaming-output.md)、工具调用等高级能力 [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)。  
- **多模态生成模型**：以万相（WanX）和 Vidu 为核心，覆盖文生图、图生图、文生视频、图生视频、音频驱动视频等全链路创作能力。万相3.0 支持 12 类视频生成任务类型，包括首尾帧生视频、风格参考、音频参考、白模渲染等 [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)。Vidu 则提供细粒度运镜控制（推/拉/升/降/固定）、导演风格（宫崎骏、新海诚等）及特效关键词触发机制 [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)。  
- **实时音视频模型**：基于 AOQ 或 WebRTC 协议，支持 qwen3.8-omni-flash-realtime（音视频双模态对话）、qwen-audio-3.1-realtime-plus（低延迟语音对话）、qwen3.8-livetranslate-flash-realtime（实时翻译）、fun-asr-realtime（语音识别）等，适用于智能硬件、语音助手、会议转写等低延迟场景。

> **注意**：文档 39（虚拟模特生成）、41（人物实例分割）、42（鞋靴模特）、43（图像局部重绘）均明确标注“当前仅提供免费体验，免费额度用完后不可调用且不支持付费”，并推荐迁移到 `wanx-image-edit` 或 `qwen-image-edit` 等替代方案。该策略与文档 40（通用图像编辑-万相2.1）的持续维护状态存在明显差异，建议优先采用后者作为生产环境标准接口。

## 关键参数

不同任务类型的关键参数设计高度结构化，需严格遵循模型语义：

- **文本生成类**：核心参数为 `messages`（角色+内容），支持 `stream`（流式）、`reasoning_effort`（思考强度）、`enable_thinking`（是否开启思考模式）。注意 `enable_thinking` 非 OpenAI 标准参数，在 Python SDK 中需通过 `extra_body` 传入（如 DeepSeek、Kimi、MiMo 等模型）[Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)。  
- **图像生成类**：`prompt`（正向提示词）与 `negative_prompt`（负向提示词）为必填项；文生图 V2 支持 `prompt_extend: true` 启用大模型智能扩写；图像编辑类模型（如 `wanx-image-edit`）则需指定 `input.image_url` + `input.prompt` + `input.mask_url`（局部重绘）等组合参数。  
- **视频生成类**：万相3.0 强依赖结构化提示词公式，包含 `[总体描述] + [参考素材引用] + [分镜 N（起-止秒）] + [台词] + [音效/BGM] + [风格/情绪] + [负向清单]`；Vidu 则强调“主体/场景+场景描述+环境描述+艺术风格/媒介”的四段式结构，并通过关键词（如 `镜头向左移动`、`延时摄影`、`宫崎骏风格`）精确触发效果。  
- **实时音视频类**：AOQ 模式下需区分 `Audio 轨`（传输 Opus 音频流）与 `Data 轨`（传输 `run-task`/`result-generated`/`finish-task` 等事件）；WebRTC 模式下需配置 `server_vad` 或 `semantic_vad` 进行服务端语音活动检测，不支持手动模式。

## 使用方式

调用方式按接入协议分为三类，需匹配对应 SDK 或 HTTP 客户端：

- **OpenAI 兼容协议**：适用于所有第三方模型（DeepSeek、Kimi、GLM 等）及部分通义模型。需配置 `base_url` 为地域专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），并通过 `model` 字段指定模型 ID（如 `kimi/kimi-k3.1-pro`）。示例代码中普遍使用 `openai` Python SDK 并设置 `extra_body` 传递非标参数 [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)。  
- **DashScope 原生协议**：适用于万相、通义千问等阿里云自研模型。需使用 `dashscope` SDK，初始化 `Client(workspace="{WorkspaceId}", region="cn-beijing")`，并调用对应模块（如 `dashscope.ImageSynthesis.async_invoke`）。异步任务需轮询 `get_result` 获取最终输出。  
- **AOQ/WebRTC 协议**：适用于实时音视频场景。AOQ 需集成客户端 SDK（Android/iOS/HarmonyOS），通过 `AoqClientEngine` 建立连接，并分别处理 Audio/Data 双轨数据；WebRTC 则需在浏览器端创建 `RTCPeerConnection`，处理 SDP 交换与媒体流绑定，注意 CORS 限制需由业务后端代理解决 [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)。

## 限制和注意事项

- **地域与权限强绑定**：绝大多数 AIGC 和第三方模型（如 DeepSeek、Kimi、GLM、虚拟模特、人像重绘等）明确限定仅支持华北2（北京）地域，且必须使用该地域的 API Key 和业务空间 ID。跨地域调用将失败。  
- **限流维度双重约束**：API 同时受 **RPM/TPM（每分钟请求数/Token 数）** 和 **RPS/TPS（每秒峰值）** 限制，突发流量（Traffic Burst）会触发增速限流。推荐优先启用平台侧的“服务端排队等待”（加 `X-DashScope-Queue-Enable: true` 请求头）而非简单重试 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。  
- **异步任务生命周期管理**：图像/视频类生成任务均为异步模式，返回 `task_id` 后需主动轮询结果。`task_id` 有效期通常为 24 小时（如人像风格重绘），超期后无法查询。  
- **缓存与成本优化**：显式缓存（`cache_control`）对高频复用 Prompt 的 Agent 场景至关重要，首次写入成本为标准价 25%，命中后节省 90% 成本。Claude Code、OpenCode 等工具已原生支持，无需额外配置 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)。  
- **免费额度风险**：多个 Legacy 模型（虚拟模特、人物分割、鞋靴模特、局部重绘）已明确进入“免费体验”阶段，额度耗尽即不可用，且无付费通道。生产系统应避免依赖此类接口，及时迁移至 `wanx-image-edit` 等稳定服务。

## 来源文档

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
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [Ling-蚂蚁数科](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/antdigital.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
- [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
- [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](../../raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)
- [使用 AOQ 接入 qwen-audio-3.1-asr-flash-streaming 实现语音输入法](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/voice-input-using-aoq-access-qwen-audio-asr.md)
- [使用 AOQ 接入 qwen3.8-livetranslate-flash-realtime 实现实时语音翻译](../../raw/_short/real-time-translation-using-aoq-access-qwen-live-9b4d3056b2eade2b.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/_short/speech-synthesis-using-aoq-access-qwen-audio-3-0-43022e91dedcb0c1.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)
- [图像生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation.md)
- [历史模型指南](../../raw/model-user-guide/use-cases/legacy-resources.md)
- [技术解决方案](../../raw/model-user-guide/use-cases/technical-solutions.md)
- [人像风格重绘](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/style-repaint.md)
- [虚拟模特生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/virtual-model-generation.md)
- [通用图像编辑-万相2.1](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md)
- [人物实例分割](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/image-instance-segmentation.md)
- [鞋靴模特](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/shoes-and-boots-model.md)
- [图像局部重绘](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/vary-region.md)
- [图像擦除补全](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/image-erasure-and-completion.md)
- [视频生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation.md)
- [创意海报生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/creative-poster-generation-overview.md)
- [涂鸦作画](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/sketch-to-image.md)
- [图生视频-基于首尾帧](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-first-and-last-frames-guide.md)
- [视频编辑2.1](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/wan-vace-guide.md)
- [万相-图生视频-基于首帧](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-guide.md)


