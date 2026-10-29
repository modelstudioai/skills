# use cases

百炼平台提供覆盖文本、图像、视频、语音等多模态场景的完整 AI 应用能力，支持从 [Prompt 工程](../concepts/prompt-engineering.md)、RAG 构建、模型微调到实时音视频交互的全栈开发路径。本文档面向开发者，结构化梳理核心使用模式、关键参数、接入方式及约束条件，所有内容均基于平台当前稳定 API 与控制台功能。

## 支持的模型/功能

百炼支持三类主流使用路径：  
- **原生模型调用**：包括文生文（如 Qwen 系列）、文生图（万相 V1/V2）、文生视频（万相 3.0、Vidu）、语音合成（Qwen-Audio-TTS、CosyVoice）及语音识别（fun-asr-realtime）等；  
- **三方模型集成**：通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 DashScope SDK 接入 DeepSeek、Kimi、GLM、MiniMax、Stepfun、MiMo、Unisound、Ling 等十余家厂商模型，[DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)与[DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)在上下文长度与联网能力上存在差异；  
- **实时音视频交互**：基于 WebRTC 或 AOQ 协议接入 qwen3.8-omni-flash-realtime、qwen-audio-3.1-realtime-plus 等低延迟模型，支持按键语音对话、实时翻译、语音输入法等硬件级场景。

> **注意**：部分三方模型（如 `xiaomi/mimo-v2.5-pro`）已明确标注下线时间（2026年10月21日），应优先迁移至替代型号（如 `xiaomi/mimo-v2.6-pro-ultraspeed`）——详见 [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)。

## 关键参数

不同模态任务的关键参数设计高度结构化：  
- **文生文**：核心为 `messages`（ChatML 格式），支持 `stream`、`enable_thinking`（触发推理过程）、`reasoning_effort`（控制思考深度）等非标参数；  
- **文生图**：`prompt`（正向描述）与 `negative_prompt`（反向排除）为必需字段，万相 V2 支持 `prompt_extend: true` 启用大模型智能扩写；  
- **文生视频**：万相 3.0 采用全要素公式，包含 `[总体描述] + [参考素材引用] + [分镜 N（起-止秒）：主体+场景+运动+美学控制] + [台词] + [音效/BGM] + [风格/情绪] + [负向清单]`，[万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md) 提供完整示例；  
- **实时音视频（AOQ/WebRTC）**：`turn_detection` 控制轮次模式（`server_vad` 自动检测 vs `null` 手动提交），`input_audio_buffer.append/commit` 和 `response.create` 为 Manual 模式关键事件。

## 使用方式

- **[Prompt 工程](../concepts/prompt-engineering.md)**：推荐使用标准化框架（背景+目的+风格+语气+受众+输出），并善用 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md) 中的一键优化工具自动扩写；  
- **RAG 应用**：基于 LlamaIndex 集成时，需先通过 `DashScopeParse` 解析文档（支持 PDF/DOCX，单文件 ≤100MB），再调用 `DashScopeCloudIndex.from_documents()` 创建知识库；  
- **高并发调用**：语音合成类服务（Qwen-Audio-TTS、CosyVoice）必须使用对象池复用连接，Python 需 `dashscope>=2.0.1`，Java 需 `dashscope-sdk-java>=2.16.6` 并集成 `commons-pool2`；  
- **三方模型接入**：统一使用 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` 域名（华北2地域），`model` 字段需严格匹配控制台开通的 ID（如 `kimi/kimi-k3`、`ZHIPU/GLM-5.3`），`enable_thinking` 等非标参数须通过 `extra_body` 传入。

## 限制和注意事项

- **限流机制**：按主账号维度独立计算 RPM/TPM（分钟级）、RPS/TPS（瞬时）、Traffic Burst（增速），触发后通常 1 分钟内恢复；突发流量优先尝试服务端排队（加 `X-DashScope-Queue-Enable: true` 请求头）；  
- **缓存策略**：显式缓存（`cache_control`）仅对 Anthropic 协议兼容工具（Claude Code、Open Code）原生支持，且需配置对应地域的专用 endpoint（如 `https://dashscope.aliyuncs.com/apps/anthropic`）；  
- **地域与权限**：90% 的三方模型（DeepSeek、Kimi、GLM、MiniMax 等）仅限华北2（北京）地域使用，且必须使用该地域的 API Key 与业务空间 ID；WebRTC 场景因 CORS 限制，SDP 交换需由业务后端代理完成；  
- **安全要求**：API Key 严禁硬编码于客户端，所有移动端/前端接入必须经 AppServer 代理鉴权并下发临时 [Token](../concepts/token.md)（参见 [Token 鉴权](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)）。

## 来源文档

- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [视频生成Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)
- [语音合成高并发最佳实践](../../raw/model-user-guide/use-cases/tts-high-concurrency-best-practices.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
- [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
- [使用 AOQ 接入 qwen-audio-3.1-asr-flash-streaming 实现语音输入法](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/voice-input-using-aoq-access-qwen-audio-asr.md)
- [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](../../raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/_short/speech-synthesis-using-aoq-access-qwen-audio-3-0-43022e91dedcb0c1.md)
- [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)
- [技术解决方案](../../raw/model-user-guide/use-cases/technical-solutions.md)
- [使用 AOQ 接入 qwen3.8-livetranslate-flash-realtime 实现实时语音翻译](../../raw/_short/real-time-translation-using-aoq-access-qwen-live-9b4d3056b2eade2b.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [Ling-蚂蚁数科](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/antdigital.md)


