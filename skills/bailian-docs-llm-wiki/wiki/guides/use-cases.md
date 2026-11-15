# use cases

百炼平台提供覆盖文本、图像、视频、语音、多模态等全场景的AI能力，支持从基础生成到复杂工作流编排的多样化用例。开发者可根据业务需求选择预置模型、三方模型或自定义模型，并结合Prompt工程、缓存、限流、实时音视频等机制构建稳定高效的AI应用。

## 支持的模型/功能

百炼支持三大类核心能力模型：  
- **文生文（LLM）**：包括通义千问系列（如 `qwen3.7-max`）、三方模型（如 `kimi/kimi-k3.1-pro`、`ZHIPU/GLM-5.3`、`stepfun/step-5-preview`）及自定义微调模型；所有模型均支持思考模式（通过 `enable_thinking` 或 `reasoning_effort` 控制），详见 [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md) 和 [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)。  
- **文生图/图像编辑**：万相系列（`wanx-text-to-image-v2`、`wanx-style-repaint-v1`、`wanx-x-painting`）及通用图像编辑（`wanx-image-edit`）；部分历史模型（如 `wanx-virtualmodel`、`shoemodel-v1`）仅限免费体验且不支持付费调用，推荐迁移到 [图像编辑-万相2.1](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md)。  
- **文生视频/多模态**：万相3.0（`wan3-video-generation`）、Vidu（`vidu-video-generation`）及三方视频模型；同时支持图生视频、首尾帧生视频、参考生视频等多种任务类型，参见 [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)。  
- **实时音视频**：涵盖实时语音对话（`qwen-audio-3.1-realtime-plus`）、语音识别（`fun-asr-realtime`）、语音合成（`qwen-audio-3.0-tts-flash`）、实时翻译（`qwen3.8-livetranslate-flash-realtime`）等，统一通过 AOQ 或 WebRTC 协议接入。

> **注意**：文档 38、39、40、41、42 均明确标注对应模型（如 `wanx-virtualmodel`、`shoemodel-v1`、`image-instance-segmentation` 等）“当前仅提供免费体验，免费额度用完后不可调用且不支持付费”，与文档 36 中 `wanx-image-edit` 的商用支持状态存在矛盾。实际开发中应以控制台模型市场最新可开通状态为准，优先选用有明确计费路径的模型。

## 关键参数

不同模态模型的关键参数设计高度结构化：  
- **文生文**：核心参数为 `messages`（含 `role`/`content`），思考模式需显式传入 `enable_thinking: true`（非 OpenAI 标准参数，须通过 `extra_body` 传递）或 `reasoning_effort`（如 `"max"`）；流式响应需设置 `stream: true` 及 `stream_options.include_usage: true`。  
- **文生图**：`prompt`（正向提示词）和 `negative_prompt`（反向提示词）为必需字段；V2 版本额外支持 `prompt_extend: true` 启用大模型智能改写，详见 [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)。  
- **文生视频**：基础公式为 `主体 + 场景 + 运动`，进阶支持分镜描述（`分镜N（起-止秒）：...`）、声音描述（人声/音效/BGM）及负向清单；万相3.0 还支持 `参考素材引用` 和 `台词` 等多模态控制。  
- **实时音视频（AOQ）**：关键配置在会话初始化阶段，如 `turn_detection`（设为 `null` 表示 Manual 模式，由客户端控制语音起止）、`server_vad`（服务端 VAD 模式）；音频传输需配合 Opus 插件，权限需动态申请（如 Android 的 `RECORD_AUDIO`）。

## 使用方式

标准调用流程遵循“准备→调用→处理”三步：  
1. **准备**：获取并配置 API Key 到环境变量（避免硬编码）；确认地域与业务空间 ID（`{WorkspaceId}`）；安装对应 SDK（如 `dashscope`、`openai`）或集成 AOQ Client SDK（需导入 Opus 插件）。  
2. **调用**：  
   - LLM/图像/视频类请求使用 RESTful API 或 SDK 同步/[异步调用](../concepts/asynchronous-invocation.md)（图像类多为异步，需轮询 `task_id`）；  
   - 实时音视频类必须通过 AOQ 或 WebRTC 建立长连接：WebRTC 需创建 `RTCPeerConnection` 并处理 `ontrack` 回调；AOQ 需先向业务 AppServer 获取临时凭证，再初始化 `AoqClientEngine`。  
3. **处理**：解析响应结构（如 `reasoning_content`/`content` 分离思考与结果）、处理流式数据（逐 chunk 提取 `delta.reasoning_content`）、管理媒体流（绑定 `audio` 元素播放远端流）及错误重试（结合限流策略）。

## 限制和注意事项

- **地域与认证约束**：绝大多数三方模型（DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun、Unisound、Ling）及历史图像模型明确限定仅支持 **华北2（北京）地域**，且必须使用该地域的 API Key 和专属域名（如 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）；跨地域调用将失败。  
- **限流机制**：API 按 RPM/TPM（每分钟请求数/Token 数）、RPS/TPS（每秒峰值）、Traffic Burst（突发流量）三维度限流；触发 `429` 错误时，推荐优先启用平台层的[服务端排队等待](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)（加 `X-DashScope-Queue-Enable: enable` 请求头），而非简单重试。  
- **缓存与成本**：显式缓存（`cache_control`）可降低 90% 成本，但仅对 Anthropic 协议接入的工具（如 Claude Code、Open Code）原生支持；普通 OpenAI 兼容调用需自行实现请求哈希与本地缓存逻辑。  
- **安全与合规**：API Key 必须保存在服务端（AppServer），严禁嵌入客户端代码；移动端需动态申请 `RECORD_AUDIO`/`CAMERA` 权限；涉及用户语音/图像数据时，须确保符合隐私法规。

## 来源文档

- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
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
- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [Ling-蚂蚁数科](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/antdigital.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
- [使用 AOQ 接入 qwen3.8-livetranslate-flash-realtime 实现实时语音翻译](../../raw/_short/real-time-translation-using-aoq-access-qwen-live-9b4d3056b2eade2b.md)
- [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](../../raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/_short/speech-synthesis-using-aoq-access-qwen-audio-3-0-43022e91dedcb0c1.md)
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
- [使用 AOQ 接入 qwen-audio-3.1-asr-flash-streaming 实现语音输入法](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/voice-input-using-aoq-access-qwen-audio-asr.md)
- [创意海报生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/creative-poster-generation-overview.md)
- [视频生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation.md)
- [视频编辑2.1](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/wan-vace-guide.md)
- [图生视频-基于首尾帧](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-first-and-last-frames-guide.md)
- [万相-图生视频-基于首帧](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-guide.md)
- [涂鸦作画](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/sketch-to-image.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)


