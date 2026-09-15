# use cases

阿里云百炼平台提供覆盖文本、图像、视频、语音、多模态及智能体等全栈能力的 AI 应用构建支持，面向开发者提供开箱即用的场景化解决方案。用户无需从零搭建基础设施，即可基于预置模型、可视化编排、RAG 知识库和实时音视频 SDK 快速实现生产级应用。所有方案均通过函数计算等 Serverless 服务封装，具备弹性伸缩与按量付费特性。

## 支持的模型/功能

百炼支持两类核心能力：**原生模型服务**与**三方模型直供**。

- **原生模型**：包括 Qwen 系列（如 `qwen3-vl-plus`、`qwen3.7-max`）、万相（Wan2.7/Wan3.0 图像/视频生成）、HappyHorse 视频生成、Qwen-Deep-Research 专用模型等，覆盖文生文、文生图、文生视频、图生视频、深度研究、AI 教辅等垂直场景 [高效搭建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md)。
- **三方模型直供**：通过统一 API 接入 DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun、Unisound 等厂商模型，支持 OpenAI 兼容协议与 DashScope 协议，且多数模型提供 `enable_thinking` 或 `reasoning_effort` 参数控制推理深度 [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)。
- **实时交互能力**：提供 `qwen3.5-omni-plus-realtime`（音视频双模态）、`qwen-audio-3.0-realtime-plus`（语音）、`qwen-audio-3.0-tts-flash`（TTS）、`fun-asr-realtime`（ASR）四类实时模型，并配套 AOQ Client SDK 与 WebRTC 接入方案，支持 Android/iOS/HarmonyOS/浏览器端低延迟交互 [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-omni-realtime.md)。

> **注意**：多个三方模型文档（如 [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)、[Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)、[MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)）均声明部分旧版本模型将于 2026 年下架，但各文档下架时间点不一致（如 DeepSeek 系列为 2026-10-10，Kimi-K2-Instruct 为 2026-07-09），实际应以控制台最新公告为准。

## 关键参数

不同模态任务需关注特定参数：

- **文生文 Prompt**：推荐使用结构化 Prompt 框架（背景/目的/风格/语气/受众/输出），并善用阿里云百炼内置的 Prompt 一键优化工具 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)。
- **文生图/视频**：`prompt`（正向提示词）与 `negative_prompt`（反向提示词）为核心；文生图 V2 支持 `prompt_extend: true` 启用大模型智能扩写；文生视频支持 `enable_thinking` 控制推理模式，并可叠加声音描述（人声/音效/BGM）与多镜头分镜语法 [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)、[文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)。
- **RAG 应用**：依赖 `DASHSCOPE_WORKSPACE_ID` 环境变量指定业务空间；文档解析支持 `.pdf/.doc/.docx`（单文件 ≤100MB，≤1000 页）；知识库创建后可通过 `DashScopeCloudIndex` 和 `DashScopeCloudRetriever` 访问 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。
- **实时音视频**：WebRTC 模式仅支持 `server_vad` 或 `semantic_vad`，不支持手动模式；AOQ Manual 模式需显式调用 `input_audio_buffer.commit` 与 `response.create` 控制轮次 [使用 AOQ 接入 qwen3.5-omni-plus-realtime 实现按键语音对话](../../raw/model-user-guide/use-cases/use-aoq-to-access-qwen3-5-omni-plus-realtime-to-realize-key-voice-dialogue.md)。

## 使用方式

典型接入路径如下：

1. **准备环境**：获取 API Key 并配置至环境变量或 SDK；开通对应模型服务（如知识库、多模态应用）；确认地域与业务空间 ID。
2. **选择部署形态**：
   - *Serverless 快速验证*：基于函数计算（FC）部署，如 [深度研究：生成你的独家洞察报告](../../raw/model-user-guide/use-cases/deep-research.md)、[AI 解题 + 批改：推动课程教学智变](../../raw/model-user-guide/use-cases/ai-homework-helper.md) 均采用此模式，15 分钟内可完成。
   - *SDK 集成*：调用 DashScope SDK 或 OpenAI 兼容 SDK，适用于自定义逻辑强的场景（如 RAG、Prompt 工程）。
   - *实时交互*：WebRTC 用于浏览器端音视频；AOQ SDK 用于移动端（Android/iOS/HarmonyOS），需集成对应平台 SDK 并申请运行时权限。
3. **调用与编排**：使用百炼控制台可视化流程编排（如无限画布影视创作），或通过代码调用 API（如 LlamaIndex 集成 RAG、AOQ 发送音频流）。

## 限制和注意事项

- **限流策略**：API 按 RPM/TPM（分钟级）、RPS/TPS（瞬时）、Traffic Burst（增速）三维度限流，触发后通常 1 分钟内恢复。高并发场景需结合 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md) 中的服务端排队、客户端令牌桶或架构层 MQ 削峰方案。
- **缓存机制**：显式缓存（`cache_control`）可实现 100% 确定性命中，首次写入成本为标准价 25%，后续命中节省 90% 成本；Claude Code、Open Code 等工具原生支持，但需注意动态 system [prompt](prompt.md)（如 git 状态）会降低跨会话命中率 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)。
- **地域与兼容性**：绝大多数三方模型（DeepSeek、Kimi、GLM、MiniMax 等）仅在华北2（北京）地域可用；WebRTC 方案受 CORS 限制，Demo 需 curl 代理，正式环境必须由业务后端代理 SDP 交换 [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-multimodal-dialog.md)。
- **模型生命周期**：所有三方模型均存在明确下架时间（见各模型文档），且新旧模型间 API 行为可能存在差异（如思考模式参数名不统一：`enable_thinking` vs `reasoning_effort` vs `thinking`），迁移前需充分测试。

## 来源文档

- [高效搭建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md)
- [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)
- [深度研究：生成你的独家洞察报告](../../raw/model-user-guide/use-cases/deep-research.md)
- [AI 解题 + 批改：推动课程教学智变](../../raw/model-user-guide/use-cases/ai-homework-helper.md)
- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
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
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-multimodal-dialog.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-aoq-omni-realtime.md)
- [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-omni-realtime.md)
- [使用 AOQ 接入 qwen3.5-omni-plus-realtime 实现按键语音对话](../../raw/model-user-guide/use-cases/use-aoq-to-access-qwen3-5-omni-plus-realtime-to-realize-key-voice-dialogue.md)
- [使用 AOQ 接入 qwen-audio-3.0-realtime-plus 实现实时语音对话](../../raw/model-user-guide/use-cases/real-time-voice-conversation-using-aoq-access-qwen-audio-3-0-realtime-plus.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/model-user-guide/use-cases/speech-synthesis-using-aoq-access-qwen-audio-3-0-tts-flash.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/model-user-guide/use-cases/real-time-speech-recognition-using-aoq-access-fun-asr-realtime.md)


