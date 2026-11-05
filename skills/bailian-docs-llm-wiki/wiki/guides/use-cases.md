# use cases

百炼平台提供覆盖文本、图像、视频、语音、多模态等全场景的 AI 能力，支持从 [Prompt 工程](../concepts/prompt-engineering.md)、RAG 应用构建到实时音视频交互的完整技术栈。开发者可根据业务需求选择模型、配置参数并集成 SDK，快速落地生产级应用。

## 支持的模型/功能

百炼支持三类核心能力模型：  
- **文本生成类**：包括 Qwen 系列（如 `qwen3.7-max`）、三方模型（如 `deepseek-v4-pro`、`kimi/kimi-k3.1-pro`、`ZHIPU/GLM-5.3`、`MiniMax-M2.7`、`xiaomi/mimo-v2.6-pro-ultraspeed`、`stepfun/step-3.7-flash`、`antdigital/Ling-3.1-flash`、`unisound/unisound-u2`）等，均支持 [OpenAI 兼容接口](../concepts/openai-compatibility.md)与思考模式（通过 `extra_body` 传入 `enable_thinking` 或 `reasoning_effort` 参数）[文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)。  
- **多模态生成类**：涵盖文生图（`wanx-text-to-image-v2`）、文生视频（`wan3-video-generation`、`vidu-video-generation`）、图生视频、参考生视频等，支持结构化提示词公式与多维度美学控制 [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)。  
- **实时交互类**：包括 WebRTC 与 AOQ 双路径的实时音视频方案，如 `qwen3.8-omni-flash-realtime`（WebRTC/Manual/VAD 模式）、`qwen-audio-3.1-asr-flash-streaming`（语音输入法）、`qwen3.8-livetranslate-flash-realtime`（实时翻译）、`qwen-audio-3.0-tts-flash`（流式合成）等 [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)。  

此外还提供 RAG 构建（LlamaIndex 集成）、自定义模型调优、显式缓存、限流应对、语音高并发等工程化能力。

## 关键参数

不同能力对应关键参数如下：  
- **文本模型**：通用参数为 `model`、`messages`；思考模式需通过非标准字段启用，如 `extra_body={"enable_thinking": true}`（DeepSeek/Kimi/MiMo/Unisound）或 `{"reasoning_effort": "max"}`（Kimi/Stepfun），具体以各模型文档为准。  
- **文生图**：核心参数为 `prompt`（正向提示词）与 `negative_prompt`（反向提示词），V2 版本支持 `prompt_extend: true` 启用大模型智能改写 [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)。  
- **文生视频**：基础公式为 `主体 + 场景 + 运动`，进阶支持 `美学控制`（镜头、光线、景别）与 `声音描述`（人声/音效/BGM）；万相3.0 支持完整结构化公式，含分镜、台词、参考素材引用等 [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)。  
- **实时音视频（AOQ/WebRTC）**：关键配置包括 `turn_detection`（`server_vad`/`semantic_vad`/`null`）、`stream_options.include_usage`（仅部分模型支持）、音频编码插件（Opus 必选）、以及 `input_audio_buffer.append` 与 `commit` 的调用时机（Manual 模式下需显式提交）。

## 使用方式

1. **准备环境**：获取 API Key 并配置至环境变量（推荐），开通对应模型服务（如知识库、多模态应用、业务空间），按需安装 SDK（DashScope Python/Java ≥2.0.1，AOQ Client SDK，LlamaIndex 相关包）。  
2. **调用模型**：  
   - 文本类：使用 [OpenAI 兼容接口](../concepts/openai-compatibility.md)（`base_url` 需替换 `{WorkspaceId}` 和地域，如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）或 DashScope 原生 API；  
   - 图像/视频类：通过异步 API 提交任务（`X-DashScope-Async: enable` 头），再轮询 `task_id` 获取结果；  
   - 实时类：WebRTC 方式需浏览器 `getUserMedia` + `RTCPeerConnection`；AOQ 方式需客户端集成 SDK 并由 AppServer 代理 [Token](../concepts/token.md) 鉴权。  
3. **工程集成**：  
   - RAG 应用：使用 `DashScopeCloudIndex` 替代本地索引，配合 `DashScopeParse` 解析 PDF/DOCX [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)；  
   - 高并发 TTS：Python/Java 使用对象池复用连接，避免重复建连开销；  
   - 显式缓存：Claude Code/OpenCode 等工具原生支持，通过 `cache_control` 标记实现确定性命中。

## 限制和注意事项

- **地域与模型绑定严格**：多数三方模型（DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun、Ling、Unisound）及图像/视频类模型（万相、Vidu、虚拟模特、鞋靴模特）**仅支持华北2（北京）地域**，且必须使用该地域的 API Key 和业务空间 ID；跨地域调用将失败。  
- **免费额度与停服风险**：`wanx-virtualmodel`、`virtualmodel-v2`、`shoemodel-v1`、`image-instance-segmentation` 等 legacy 图像模型当前仅提供免费体验，额度用尽后**不可调用且不支持付费**，官方明确建议迁移到 `wanx-image-edit` 或 `qwen-image-edit` [虚拟模特生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/virtual-model-generation.md)。  
- **协议与模式差异**：AOQ 接入需区分 `Realtime` 协议（`qwen-audio-3.1-realtime-plus`）与 `Inference` 协议（`qwen-audio-3.1-asr-flash-streaming`、`fun-asr-realtime`、`qwen-audio-3.0-tts-flash`），二者事件语义、音频传输方式（Audio 轨 vs Data 轨）完全不同，不可混用。  
> **注意**：文档 13（DeepSeek-硅基流动）称其“支持更长上下文”，而文档 12（DeepSeek-阿里云）强调“支持联网搜索与上下文缓存”，但两文档均未说明具体数值，且未在其他模型文档中交叉验证——开发者应以控制台实际测试为准，避免依赖未量化指标。  
> **注意**：文档 4（视频生成Prompt指南）将 `wan3.0/wan2.7/wan2.6/wan2.5` 统一归入“声音公式”，但文档 3（万相3.0视频生成Prompt指南）明确其为独立模型系列，且文档 21（Vidu）完全独立——三者提示词语法、参数名（如 `prompt_extend` vs `prompt_extend` 不存在于 Vidu）、能力边界均不兼容，不可迁移复用。  
- **安全与合规**：API Key **严禁硬编码至客户端代码或提交至仓库**，必须由业务 AppServer 代理鉴权并动态下发 [Token](../concepts/token.md)；移动端需申请 `RECORD_AUDIO` 运行时权限，iOS 需声明 `NSMicrophoneUsageDescription`。

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
- [Ling-蚂蚁数科](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/antdigital.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
- [使用 AOQ 接入 qwen-audio-3.1-asr-flash-streaming 实现语音输入法](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/voice-input-using-aoq-access-qwen-audio-asr.md)
- [使用 AOQ 接入 qwen3.8-livetranslate-flash-realtime 实现实时语音翻译](../../raw/_short/real-time-translation-using-aoq-access-qwen-live-9b4d3056b2eade2b.md)
- [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](../../raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/_short/speech-synthesis-using-aoq-access-qwen-audio-3-0-43022e91dedcb0c1.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)
- [技术解决方案](../../raw/model-user-guide/use-cases/technical-solutions.md)
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
- [历史模型指南](../../raw/model-user-guide/use-cases/legacy-resources.md)
- [视频编辑2.1](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/wan-vace-guide.md)
- [视频生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation.md)
- [万相-图生视频-基于首帧](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-guide.md)
- [图生视频-基于首尾帧](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-first-and-last-frames-guide.md)


