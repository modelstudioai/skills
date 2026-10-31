# use cases

百炼平台提供覆盖文本、图像、视频、语音、实时交互等多模态场景的完整用例支持。开发者可根据业务需求选择预置模型、三方模型或自定义模型，并结合 Prompt 工程、RAG、缓存、流控等能力构建生产级应用。所有用例均需通过 API Key 调用，部分功能依赖业务空间 ID 与地域专属 Endpoint。

## 支持的模型/功能

- **文生文**：支持 Qwen 系列（如 `qwen3.7-max`）、DeepSeek（如 `deepseek-v4-pro`）、Kimi（如 `kimi/kimi-k3`）、GLM（如 `ZHIPU/GLM-5.3`）、MiniMax（如 `MiniMax-M2.7`）、MiMo（如 `xiaomi/mimo-v2.6-pro-ultraspeed`）、Stepfun（如 `stepfun/step-3.7-flash`）、Unisound（如 `unisound/unisound-u2`）、Ling（如 `antdigital/Ling-3.1-flash`）等主流开源及商业模型，全部通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 DashScope SDK 接入 [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)、[Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md) 等文档详述各模型地域限制与参数差异。
- **文生图/图生图**：万相系列（`wan-image-v2`、`wan-image-v1`），支持正向/反向提示词、智能改写（`prompt_extend`）等能力 [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)。
- **文生视频/图生视频/参考生视频**：万相 3.0（`wan3-video`）、万相 2.x 及 Vidu 模型，支持多镜头分镜、运镜控制、声音描述、风格化等复杂提示词结构 [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)。
- **实时音视频**：`qwen3.8-omni-flash-realtime`、`qwen-audio-3.1-realtime-plus`、`qwen3.8-livetranslate-flash-realtime` 等模型，支持 WebRTC（浏览器端）与 AOQ（移动端/嵌入式）双接入路径，涵盖 VAD 自动轮次与 Manual 按键控制模式 [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)。
- **语音合成与识别**：`Qwen-Audio-TTS`、`CosyVoice`、`Sambert`、`qwen-audio-3.1-asr-flash-streaming`、`fun-asr-realtime`，支持高并发对象池复用与 WebSocket 长连接优化 [语音合成高并发最佳实践](../../raw/model-user-guide/use-cases/tts-high-concurrency-best-practices.md)。
- **RAG 应用**：基于 LlamaIndex 集成百炼知识库服务，支持文档解析（DashScopeParse）、索引创建与检索增强 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。
- **自定义模型**：支持微调训练、部署与评测全流程，适用于领域适配与任务定制 [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)。

> **注意**：不同三方模型对 `enable_thinking`、`reasoning_effort`、`thinking` 等非标准参数的支持方式不一致（如 DeepSeek-硅基流动要求 `extra_body`，而 Stepfun 默认开启且不可关闭），请严格参照对应模型文档配置，避免因参数传递错误导致请求失败。

## 关键参数

- **通用参数**：`model`（必填，指定模型 ID）、`messages`（ChatML 格式对话历史）、`stream`（布尔值，启用[流式输出](../concepts/streaming-output.md)）、`temperature`（控制随机性，默认 0.8）、`max_tokens`（最大输出长度）。
- **Prompt 相关**：
  - 文生文：`system`（系统指令）、`user`/`assistant`（角色消息）；推荐使用 Prompt 框架（背景/目的/风格/语气/受众/输出）提升效果 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)。
  - 文生图：`prompt`（正向提示词）、`negative_prompt`（反向提示词）、`prompt_extend`（是否启用大模型智能改写，默认 `true`）。
  - 视频生成：`prompt`（主体+场景+运动+美学控制+风格化）、`negative_prompt`（可选）、`prompt_extend`（万相 V2/V3 支持）、`audio_description`（声音公式中的人声/音效/BGM 描述）。
- **实时交互参数**：
  - WebRTC：`server_vad`（服务端语音活动检测）、`semantic_vad`（语义级 VAD）；Manual 模式需显式调用 `input_audio_buffer.commit` 和 `response.create`。
  - AOQ：`turn_detection`（设为 `null` 启用 Manual 模式）、`session_id`（会话标识）、`task_id`（任务标识）。
- **缓存与流控**：
  - 显式缓存：`cache_control: {"type": "ephemeral"}`（添加至 `system` 或 `user` 消息的 `content` 字段），仅 Anthropic 协议兼容端点支持 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)。
  - 限流应对：`x-dashscope-queue-wait`（服务端排队等待头，用于突发流量缓解）。

## 使用方式

- **API 调用**：所有模型均通过 RESTful API 或 SDK 调用。[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)需配置 `base_url`（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），DashScope SDK 需设置 `workspace` 和 `region`。
- **Prompt 编写**：
  - 文生文：采用“背景+目的+风格+语气+受众+输出”六要素框架，避免模糊表述；可先用 [Prompt一键优化工具](https://bailian.console.aliyun.com/flow-agent/component-manage/prompt) 扩写初稿。
  - 多模态生成：按“基础公式→进阶公式→任务特化公式”渐进式构建，例如万相 3.0 视频提示词需包含 `[总体描述]+[参考素材引用]+[分镜 N（起-止秒）：主体+场景+运动+美学控制]+[台词]+[音效/BGM]+[风格/情绪]+[负向清单]`。
- **RAG 集成**：使用 `DashScopeParse` 解析 PDF/DOCX 文件 → `SimpleDirectoryReader` 加载 → `DashScopeCloudIndex.from_documents()` 创建知识库 → 通过 `retriever.retrieve()` 查询。
- **实时交互**：
  - WebRTC：浏览器端调用 `RTCPeerConnection` 建立连接，`getUserMedia` 获取媒体流，`ontrack` 处理远端音频。
  - AOQ：移动端初始化 `AoqClientEngine`，通过 `sendDataMsg` 发送 `run-task`/`continue-task`，监听 `result-generated` 事件获取结果。
- **高并发优化**：语音合成场景使用对象池（Python/Java SDK 提供），预热连接并复用 `TTSClient` 实例；配置 `DASHSCOPE_CONNECTION_POOL_SIZE` 等底层参数控制资源。

## 限制和注意事项

- **地域与模型绑定**：多数三方模型（如 DeepSeek-硅基流动、Kimi-月之暗面、GLM-智谱、MiMo、Stepfun、Unisound、Ling）**仅支持华北2（北京）地域**，调用时必须使用该地域的 API Key 与 `base_url`；跨地域调用将返回 404 或认证失败。Vidu、万相系列、Qwen 原生模型支持多地域，具体参见各 API 参考文档。
- **Token 与请求限流**：百炼 API 按 RPM（每分钟请求数）、TPM（每分钟 Token 数）、RPS（每秒请求数）、TPS（每秒 Token 数）及 Traffic Burst（突发流量）四维度限流，触发后通常 1 分钟内恢复。高并发场景需结合 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md) 中的服务端排队、客户端自适应拥塞控制或 MQ 削峰方案。
- **文件与数据限制**：`DashScopeParse` 文档解析器要求单个文件 ≤100MB 且 ≤1000 页；知识库上传文件格式支持 PDF/DOCX/TXT 等，但不支持加密 PDF；AOQ 实时语音识别对音频采样率要求为 16kHz，位深 16bit。
- **缓存适用范围**：显式缓存仅在 Anthropic 协议兼容端点（如 `https://dashscope.aliyuncs.com/apps/anthropic`）生效，且需客户端工具（如 Claude Code、OpenCode）原生支持或手动注入 `cache_control` 字段；OpenAI 兼容端点不支持该机制。
- **模型下线风险**：部分旧版模型已明确下线时间，例如 `xiaomi/mimo-v2.5-pro` 将于 2026 年 10 月 21 日停用，文档明确建议迁移到 `xiaomi/mimo-v2.6-pro-ultraspeed` [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)。

## 来源文档

- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [视频生成Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [语音合成高并发最佳实践](../../raw/model-user-guide/use-cases/tts-high-concurrency-best-practices.md)
- [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
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
- [使用 AOQ 接入 qwen3.8-livetranslate-flash-realtime 实现实时语音翻译](../../raw/_short/real-time-translation-using-aoq-access-qwen-live-9b4d3056b2eade2b.md)
- [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](../../raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/_short/speech-synthesis-using-aoq-access-qwen-audio-3-0-43022e91dedcb0c1.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)
- [技术解决方案](../../raw/model-user-guide/use-cases/technical-solutions.md)
- [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)


