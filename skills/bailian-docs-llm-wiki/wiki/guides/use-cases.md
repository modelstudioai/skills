# use cases

百炼平台提供覆盖文本、图像、视频、语音、多模态等全场景的 AI 用例支持，面向开发者提供从 [Prompt 工程](../concepts/prompt-engineering.md)、RAG 构建、模型调优到实时音视频交互的一站式技术方案。所有用例均基于标准化 API 和 SDK 实现，可直接集成至生产环境。

## 支持的模型/功能

百炼支持三类核心能力模型：
- **文生文（LLM）**：包括 Qwen 系列（如 `qwen3.7-max`）、第三方直供模型（如 `ZHIPU/GLM-5.3`、`kimi/kimi-k3`、`MiniMax/MiniMax-M2.7`、`xiaomi/mimo-v2.5-pro`）及自定义微调模型。所有模型均支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)与 DashScope SDK，部分支持思考模式（通过 `enable_thinking` 或 `reasoning_effort` 参数控制）[DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)。
- **文生图/图生图**：万相系列（`wan-image-api-reference/text-to-image-v2-api-reference.md`）支持中英文 [prompt](prompt.md)、negative_[prompt](prompt.md) 及 [prompt](prompt.md)_extend 智能改写；Vidu 视频生成支持结构化提示词公式与运镜控制 [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)。
- **文生视频/多模态交互**：万相3.0（`wan3-video-generation-prompt-guide.md`）支持文生视频、首帧/首尾帧/参考生视频等8类任务；Qwen-Omni 系列（如 `qwen3.8-omni-flash-realtime`）支持 WebRTC 和 AOQ 协议的实时音视频通话、语音合成（TTS）与语音识别（ASR）[通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)。

> **注意**：多个文档对同一模型的接入方式存在不一致描述。例如，`kimi/kimi-k2.6` 在 [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md) 中明确支持 `enable_thinking` 参数，但在 [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md) 中未提及该参数，仅标注为“纯文本模型”。建议以直供方文档为准。

## 关键参数

不同模态模型的关键参数如下：
- **文生文**：`model`（必填）、`messages`（ChatML 格式）、`stream`（流式开关）、`extra_body`（非标参数载体，如 `enable_thinking: true`, `reasoning_effort: "max"`）。
- **文生图**：`prompt`（正向提示词）、`negative_prompt`（反向提示词）、`parameters.prompt_extend`（V2 默认 `true`）。
- **文生视频**：万相3.0 使用完整公式，含 `[分镜 N（起-止秒）：主体 + 场景 + 运动 + 美学控制]`、`[台词]`、`[负向清单]`；Vidu 支持 `大动态`/`小动态`、`推`/`拉`/`固定`等运镜关键词 [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)。
- **实时音视频（AOQ/WebRTC）**：`turn_detection`（`server_vad`/`semantic_vad`/`null`）、`input_audio_buffer.append`（Manual 模式需显式 commit）、`response.create`（触发回复）。

## 使用方式

1. **[Prompt 工程](../concepts/prompt-engineering.md)**：  
   - 文生文推荐使用 [Prompt框架](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)，包含背景、目的、风格、语气、受众、输出六要素；  
   - 文生图/视频需按公式组织提示词，基础公式为 `主体 + 场景 + 风格/运动`，进阶公式增加镜头语言、氛围词、细节修饰等维度。

2. **RAG 应用构建**：  
   基于 LlamaIndex，使用 `DashScopeParse` 解析 PDF/DOCX 文件，通过 `DashScopeCloudIndex.from_documents()` 创建知识库，再获取 `retriever` 进行检索 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。

3. **实时音视频接入**：  
   - WebRTC 方案需浏览器调用 `RTCPeerConnection`，通过 `getUserMedia` 获取媒体流，添加轨道后建立连接；  
   - AOQ 方案需客户端集成 SDK（Android/iOS/HarmonyOS），由业务 AppServer 代理 Token 鉴权，Audio 轨传音频，Data 轨传事件 [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](../../raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)。

4. **模型调优与部署**：  
   自定义模型需准备 ChatML 格式 JSONL 训练数据（至少 500 条），经调优、部署、评测三阶段闭环迭代 [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)。

## 限制和注意事项

- **地域与域名限制**：多数第三方模型（如 DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun、Unisound）仅支持华北2（北京）地域，且推荐使用业务空间专属域名 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com` 替代通用域名，以获得更高稳定性 [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)。
- **限流策略**：API 按 RPM/TPM（分钟级）、RPS/TPS（瞬时）、Traffic Burst（增速）三维度限流。突发流量推荐启用服务端排队等待（加 `X-DashScope-Queue-Enable: true` 请求头）[限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。
- **缓存与成本**：显式缓存（`cache_control`）可降低 90% 成本，但需确保输入内容确定性；其原生支持 Claude Code、Open Code 等工具，无需额外配置 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)。
- **安全要求**：AOQ 客户端禁止硬编码 API Key，必须由业务 AppServer 代理鉴权并动态下发 Token；移动端需在运行时申请 `RECORD_AUDIO` 权限，iOS 需声明 `NSMicrophoneUsageDescription` [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)。

## 来源文档

- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [视频生成Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
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
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
- [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](../../raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/_short/speech-synthesis-using-aoq-access-qwen-audio-3-0-43022e91dedcb0c1.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)
- [技术解决方案](../../raw/model-user-guide/use-cases/technical-solutions.md)


