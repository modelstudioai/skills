# use cases

百炼平台提供覆盖文本、图像、视频、语音等多模态场景的丰富用例支持，开发者可根据业务需求选择对应模型与接入方式。本文档系统梳理核心能力边界、关键参数配置、标准化使用方式及常见约束，帮助开发者快速落地生产级应用。

## 支持的模型/功能

百炼支持三类主流用例模型体系：  
- **文生类模型**：包括 Qwen 系列（如 `qwen3.8-omni-flash-realtime`）、三方模型（如 `deepseek-v4.1-flash`、`kimi/kimi-k3`、`MiniMax/MiniMax-M2.7`、`ZHIPU/GLM-5.3`）及自定义微调模型，适用于对话、推理、代码生成等任务；  
- **多模态生成模型**：涵盖万相（`wan3.0`、`wan2.7`）、Vidu、Qwen-Omni 等，支持文生图、文生视频、图生视频、首尾帧生成、参考生视频等多种输入组合；  
- **实时音视频模型**：通过 WebRTC 或 AOQ 协议接入，包括 `qwen-audio-3.1-asr-flash-streaming`（语音识别）、`qwen3.8-livetranslate-flash-realtime`（实时翻译）、`qwen-audio-3.0-tts-flash`（语音合成）等，专为低延迟交互优化。  

> **注意**：部分三方模型存在地域限制。例如，`DeepSeek-硅基流动` [原文标题](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md) 和 `Kimi-月之暗面` [原文标题](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md) 均明确要求仅限华北2（北京）地域使用，而 `GLM-智谱` [原文标题](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md) 则推荐迁移至专属业务空间域名以获得更高稳定性，与通用 `dashscope.aliyuncs.com` 域名存在服务路径差异。

## 关键参数

不同模型类型的关键参数设计目标一致：提升输出可控性与一致性。  
- **文本生成类**：通用参数包括 `model`、`messages`、`stream`；思考模式相关参数（如 `enable_thinking`、`reasoning_effort`）在 `DeepSeek`、`Kimi`、`GLM`、`MiniMax`、`MiMo`、`Stepfun`、`Unisound` 等模型中广泛存在，但命名与默认值不统一（如 `Unisound` 使用 `thinking: {"type": "enabled"}`，而 `Stepfun` 使用 `enable_thinking: true`）；  
- **文生图/文生视频类**：核心参数为 `prompt`（正向提示词）与 `negative_prompt`（反向提示词），万相 V2 及 Wan3.0 还支持 `prompt_extend: true` 启用智能扩写；Vidu 支持更细粒度控制，如 `大动态`、`左移`、`宫崎骏风格` 等关键词直接触发特定效果；  
- **实时音视频类**：协议层参数决定交互模式，如 `turn_detection: null` 表示 Manual 模式（按键控制），`server_vad` 或 `semantic_vad` 表示服务端自动语音活动检测（VAD）；AOQ 场景下需显式管理 `run-task`/`finish-task` 事件生命周期。

## 使用方式

标准接入流程遵循“准备→配置→调用→处理”四步法：  
1. **准备**：获取并安全配置 API Key（推荐环境变量方式），开通对应模型服务（如通过控制台市场页），确认业务空间 ID 与地域匹配；  
2. **配置**：根据模型类型选择协议（OpenAI 兼容或 DashScope 原生），设置 `base_url`（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），注意 `{WorkspaceId}` 需替换为实际值；  
3. **调用**：构造请求体，文本类使用 `messages` 数组，多模态类填充 `prompt` 字段，实时类需初始化 AOQ/WebRTC 连接并注册 `ontrack`、`onconnectionstatechange` 等回调；  
4. **处理**：流式响应需按 `delta.content` 或 `delta.reasoning_content` 分段解析；实时音频需绑定 `remoteAudio.srcObject` 并处理 `result-generated` 事件；缓存优化可启用 `cache_control` 标记（如 Claude Code 工具原生支持）[原文标题](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)。

## 限制和注意事项

- **限流机制**：API 按主账号维度对 RPM（每分钟请求数）、TPM（每分钟 [Token](../concepts/token.md) 数）、RPS（每秒请求数）、TPS（每秒 [Token](../concepts/token.md) 数）及 Traffic Burst（突发流量）独立限流，各模型配额参见 [rate-limit.md](raw/model-user-guide/get-started-with-models/rate-limit.md)；  
- **地域与协议约束**：多数三方模型（如 DeepSeek、Kimi、GLM、MiniMax）仅在华北2（北京）提供完整功能，且 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)与 DashScope 原生接口的参数支持存在差异（如 `extra_body` 用于非标参数传递）；  
- **实时交互特殊要求**：WebRTC 方案受浏览器 CORS 限制，SDP 交换需后端代理；AOQ 方案必须由 AppServer 统一申请 [Token](../concepts/token.md) 鉴权，禁止客户端硬编码 API Key；  
- **模型生命周期**：部分模型存在下线计划，如 `xiaomi/mimo-v2.5-pro` 将于 2026 年 10 月 21 日下线，文档已明确建议迁移到 `xiaomi/mimo-v2.6-pro-ultraspeed` [原文标题](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)；  
- **缓存与成本**：显式缓存首次写入有 25% 额外开销，但命中后可节省 90% 成本，适用于高频复用 Prompt 的工业级 Agent 场景 [原文标题](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)。

## 来源文档

- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)
- [视频生成Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
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
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
- [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
- [使用 AOQ 接入 qwen-audio-3.1-asr-flash-streaming 实现语音输入法](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/voice-input-using-aoq-access-qwen-audio-asr.md)
- [使用 AOQ 接入 qwen3.8-livetranslate-flash-realtime 实现实时语音翻译](../../raw/_short/real-time-translation-using-aoq-access-qwen-live-9b4d3056b2eade2b.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/_short/speech-synthesis-using-aoq-access-qwen-audio-3-0-43022e91dedcb0c1.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [技术解决方案](../../raw/model-user-guide/use-cases/technical-solutions.md)
- [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](../../raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)


