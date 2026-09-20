# use cases

百炼平台提供覆盖文本、图像、视频、语音等多模态生成与理解的完整能力，支持从 Prompt 工程、RAG 应用构建到实时音视频交互的端到端场景。开发者可根据业务需求选择对应模型与接入方式，并需关注限流、缓存、地域与参数兼容性等关键约束。

## 支持的模型/功能

百炼支持三类核心能力模型：

- **文生文（LLM）**：包括 Qwen 系列（如 `qwen3.7-max`）、三方直供模型（如 `deepseek-v3.2`、`kimi/kimi-k3`、`ZHIPU/GLM-5.3`、`MiniMax/MiniMax-M2.7`、`xiaomi/mimo-v2.5-pro`、`stepfun/step-3.7-flash`、`unisound/unisound-u2`），均支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)及 DashScope SDK 调用 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)。
- **文生图/图生图**：万相系列模型（`wan-image-v2`、`wan-image-v1`）支持正向/反向提示词、智能扩写（`prompt_extend`）及结构化提示词框架 [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)。
- **文生视频/图生视频/参考生视频**：万相视频模型（`wan-video-v3.0` 等）与 Vidu 模型支持多公式提示词（基础/进阶/图生/声音/多镜头）、运镜控制与风格化参数 [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md) 和 [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)。
- **实时音视频**：`qwen3.5-omni-plus-realtime`、`qwen-audio-3.1-realtime-plus`、`qwen-audio-3.0-tts-flash`、`fun-asr-realtime` 等模型通过 WebRTC 或 AOQ 协议支持低延迟语音对话、TTS 合成与 ASR 识别。

> **注意**：多个三方模型文档存在下架时间冲突。例如，`deepseek-v3.2`（文档10）与 `deepseek-v4-pro`（文档12）均标注将于 2026年10月10日下架，但 `kimi-k2-thinking`（文档13）标注为 2026年7月9日下架，`kimi/kimi-k2.5`（文档14）为 2026年8月31日下架。实际部署时请以控制台最新公告为准，优先选用推荐替代模型（如 `qwen3.7-plus`）。

## 关键参数

不同模型类型的关键参数如下：

- **文生文**：通用参数包括 `model`、`messages`、`stream`；思考模式相关参数为 `enable_thinking`（DeepSeek、MiMo、Stepfun、Unisound）或 `reasoning_effort`（Kimi、GLM-ZHIPU），均需通过 `extra_body`（Python SDK）或顶层字段（Node.js SDK）传入。
- **文生图**：必需参数为 `prompt`（正向提示词）和 `negative_prompt`（反向提示词）；`wan-image-v2` 额外支持 `prompt_extend: true/false` 控制智能改写开关。
- **文生视频**：必需参数为 `prompt`；万相模型支持 `motion`、`aesthetic_control`、`style`；Vidu 模型支持 `dynamic_control`（大/中/小动态）、`camera_movement`（推/拉/左移等）及 `video_style`（2D动漫、3D渲染等）。
- **实时音视频（AOQ）**：`turn_detection` 参数决定轮次控制模式——设为 `null` 表示 Manual 模式（按键触发），设为 `{"type": "server_vad"}` 表示服务端 VAD 自动检测 [使用 AOQ 接入 qwen3.5-omni-plus-realtime 实现按键语音对话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/use-aoq-to-access-qwen3-5-omni-plus-realtime-to-realize-key-voice-dialogue.md)。

## 使用方式

- **API 调用**：所有模型均支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（需配置 `base_url` 为 `{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`）或 DashScope 原生 SDK（需设置 `base_http_api_url`）。地域与 Workspace ID 必须匹配，华北2（北京）为多数三方模型唯一支持地域。
- **Prompt 工程**：文生文推荐使用 [Prompt 框架](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)（背景/目的/风格/语气/受众/输出）；文生图/视频需按公式组织提示词（主体+场景+运动/风格+镜头+氛围），并善用词典细化维度。
- **RAG 应用**：基于 LlamaIndex，使用 `DashScopeParse` 解析文档，`DashScopeCloudIndex` 创建知识库，再通过 `DashScopeCloudRetriever` 或 `query_engine` 调用 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。
- **实时交互**：WebRTC 方案适用于浏览器端（需处理 CORS 限制）；AOQ 方案适用于移动端（Android/iOS/HarmonyOS），需由 AppServer 代理 Token 鉴权并管理权限（`RECORD_AUDIO`、`CAMERA`）。

## 限制和注意事项

- **限流**：百炼 API 按 RPM/TPM（分钟级）、RPS/TPS（瞬时）、Traffic Burst（增速）三维度限流。突发流量建议启用服务端排队等待（加 `X-DashScope-Queue-Enable: true` 请求头）；高频调用应结合 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md) 中的客户端令牌桶或架构层 MQ 削峰。
- **缓存**：显式缓存（`cache_control`）仅对 Anthropic 协议接入的工具（如 Claude Code、OpenCode）原生支持，且需确保请求中包含 `cache_control={"type": "ephemeral"}` 标记；非 Anthropic 协议调用不生效。
- **地域与模型绑定**：绝大多数三方模型（DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun、Unisound）仅在华北2（北京）可用；万相图像/视频模型支持多地域，但需查阅具体 API 文档确认。
- **安全与合规**：API Key 必须保存于服务端（AppServer），严禁硬编码于客户端；训练数据需完成脱敏处理；实时音视频需在运行时申请 `RECORD_AUDIO` 权限，并在 iOS/Android/HarmonyOS 的配置文件中声明用途描述。

## 来源文档

- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
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
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
- [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [使用 AOQ 接入 qwen3.5-omni-plus-realtime 实现按键语音对话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/use-aoq-to-access-qwen3-5-omni-plus-realtime-to-realize-key-voice-dialogue.md)
- [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/real-time-voice-conversation-using-aoq-access-qwen-audio-3-0-realtime-plus.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/speech-synthesis-using-aoq-access-qwen-audio-3-0-tts-flash.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/real-time-speech-recognition-using-aoq-access-fun-asr-realtime.md)


