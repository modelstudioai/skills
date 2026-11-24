# use cases

百炼平台提供覆盖文本、图像、视频、语音、实时交互等多模态场景的完整用例支持，面向开发者提供标准化的 Prompt 设计方法、模型调用接口、参数配置规范及工程化最佳实践。所有用例均基于统一 API 架构，支持 OpenAI 兼容、DashScope 原生及 AOQ 实时协议等多种接入方式。

## 支持的模型/功能

百炼支持三大类模型能力：  
- **文生类**：包括 Qwen 系列（如 `qwen3.7-max`）、三方模型（如 `kimi/kimi-k3.1-pro`、`ZHIPU/GLM-5.3`、`MiniMax-M2.7`）及 RAG 增强模型；[文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md) 提供通用 Prompt 框架与扩写技巧。  
- **多模态生成类**：涵盖万相（WanX）全系图像/视频模型（如 `wanx-text-to-image-v2`、`wan3-video-generation`）、Vidu 视频模型及 Fun-ASR、Qwen-Audio 等语音模型；[文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md) 和 [视频生成Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md) 分别定义了结构化提示词公式。  
- **实时交互类**：支持 WebRTC 与 AOQ 双协议接入 `qwen3.8-omni-flash-realtime`、`qwen-audio-3.1-realtime-plus` 等低延迟模型，适用于音视频通话、语音输入法、实时翻译等场景。

> **注意**：部分历史图像模型（如 `wanx-style-repaint-v1`、`shoemodel-v1`、`image-erase-completion`）已进入免费体验阶段，额度用完后不可调用且不支持付费，官方推荐迁移到 [图像编辑-万相2.1](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md) 或 [文本生成图像](../../raw/model-user-guide/model-experience/image-and-video-generation/image-model/text-to-image.md) 等替代方案。

## 关键参数

不同任务类型的关键参数存在显著差异，需严格按模型文档配置：  
- **文生文**：核心参数为 `messages`（含 `role`/`content`），支持 `stream`、`enable_thinking`（控制思考模式）、`reasoning_effort`（推理强度）等扩展参数；`enable_thinking` 非 OpenAI 标准字段，在 DeepSeek、Kimi、GLM、MiMo 等模型中均需通过 `extra_body` 传入。  
- **文生图/图生图**：必需 `prompt`（正向提示词）与可选 `negative_prompt`（反向提示词）；万相 V2 新增 `prompt_extend: true` 启用大模型智能改写。  
- **视频生成**：除 `prompt` 外，万相 3.0 引入多维结构化参数，包括 `分镜 N（起-止秒）`、`台词`、`音效/BGM`、`负向清单` 等；Vidu 则依赖 `主体/场景+场景描述+环境描述+艺术风格/媒介` 四要素组合。  
- **实时语音类（AOQ）**：采用分轨设计——`Audio` 轨传输音频流，`Data` 轨传输 `run-task`/`finish-task` 等事件；`qwen-audio-3.1-asr-flash-streaming` 要求客户端缓存首段音频并倍速补发以追平延迟。

## 使用方式

开发者可根据技术栈选择适配路径：  
- **标准 API 调用**：使用 DashScope SDK（Python/Java）或 OpenAI 兼容 SDK（如 `openai==1.45.0+`），配置 `base_url` 为业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），确保地域与 Workspace ID 匹配。  
- **RAG 应用构建**：基于 LlamaIndex，通过 `DashScopeCloudIndex` 将解析后的文档注入知识库，配合 `DashScopeParse` 实现 PDF/DOCX 自动切分与结构化提取；详见 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。  
- **实时音视频集成**：WebRTC 方式适用于浏览器端低延迟场景（需处理 SDP 交换代理），AOQ SDK 则覆盖 Android/iOS/HarmonyOS，需导入 `AoqClientSdk` 及 Opus 插件，并动态申请 `RECORD_AUDIO` 权限。  
- **三方模型统一管理**：所有第三方模型（DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun、Unisound、Ling）均通过百炼控制台开通后，复用同一套 OpenAI 兼容调用流程，仅需切换 `model` 参数值。

## 限制和注意事项

- **地域与域名强绑定**：绝大多数模型（如 DeepSeek-硅基流动、Kimi-月之暗面、GLM-智谱、MiMo、Stepfun）明确要求华北2（北京）地域及专属业务空间域名 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，跨地域调用将失败。  
- **限流策略双重约束**：API 同时受 RPM/TPM（分钟级）与 RPS/TPS（瞬时）限制，突发流量易触发 `429` 错误；推荐优先启用 [服务端排队等待](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)（加 `X-DashScope-Queue-Enable: true` 请求头），再结合客户端自适应重试。  
- **显式缓存适用边界**：仅当 Prompt 高度稳定复用时收益显著；Claude Code、OpenCode 等工具原生支持 `cache_control`，但需注意其默认注入的动态信息（如 git 状态）会降低跨会话命中率，建议启用 `--exclude-dynamic-system-prompt-sections` 参数。  
- **历史模型兼容性风险**：`legacy-video-generation` 和 `legacy-image-generation` 下属模型（如 `wanx-virtualmodel`、`virtualmodel-v2`）虽仍可调用，但已停止功能迭代，新项目应优先选用万相 2.1 或 Wan3.0 等新版模型。

## 来源文档

- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [视频生成Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [Ling-蚂蚁数科](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/antdigital.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
- [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [使用 AOQ 接入 qwen-audio-3.1-asr-flash-streaming 实现语音输入法](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/voice-input-using-aoq-access-qwen-audio-asr.md)
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
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [鞋靴模特](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/shoes-and-boots-model.md)
- [图像擦除补全](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/image-erasure-and-completion.md)
- [人物实例分割](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/image-instance-segmentation.md)
- [创意海报生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/creative-poster-generation-overview.md)
- [图像局部重绘](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/vary-region.md)
- [涂鸦作画](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/sketch-to-image.md)
- [视频生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation.md)
- [视频编辑2.1](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/wan-vace-guide.md)
- [图生视频-基于首尾帧](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-first-and-last-frames-guide.md)
- [万相-图生视频-基于首帧](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-guide.md)
- [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)


