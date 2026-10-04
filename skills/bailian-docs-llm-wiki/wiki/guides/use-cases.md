# use cases

百炼平台提供覆盖文本、图像、视频、语音等多模态场景的生成与理解能力，支持从 [Prompt 工程](../concepts/prompt.md)、RAG 构建、三方模型集成到实时音视频交互的完整用例链路。开发者可根据业务需求选择合适的技术路径，所有能力均通过统一 API 接口或 SDK 封装提供，兼顾灵活性与工程落地性。

## 支持的模型/功能

百炼支持两类核心模型能力：**原生模型服务**（如 Qwen 系列、万相系列）和**三方模型直供服务**（如 DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun、Unisound 等）。  
- **文生文**：Qwen3 系列（qwen3.7-max、qwen3.8-omni-flash-realtime）、DeepSeek-v4、Kimi-k3、GLM-5.3 等均支持标准 chat/completions 接口及思考模式（`enable_thinking` 或 `reasoning_effort` 参数），详见 [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)、[Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md) 和 [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)。  
- **文生图**：万相-文生图 V1/V2，支持 `prompt`（正向）与 `negative_prompt`（反向）双参数控制，并可启用 `prompt_extend` 大模型智能改写功能 [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)。  
- **文生视频/图生视频/参考生视频**：万相 3.0、万相 2.x 及 Vidu 模型，支持多镜头分镜、运动控制、风格化、声音描述等结构化提示词表达 [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)、[Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md) 和 [视频生成Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)。  
- **实时音视频交互**：qwen3.8-omni-flash-realtime、qwen-audio-3.1-realtime-plus、fun-asr-realtime、qwen-audio-3.0-tts-flash 等模型通过 AOQ 或 WebRTC 协议接入，支持低延迟语音对话、实时语音识别与流式语音合成 [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)。  
- **RAG 应用构建**：基于 LlamaIndex 集成百炼知识库服务，支持文档解析（DashScopeParse）、索引创建（DashScopeCloudIndex）与检索器初始化 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。  

> **注意**：部分三方模型（如 DeepSeek-v3.x、Kimi-k2-Instruct、GLM-4.x）已明确标注下架时间（2026年7–10月），文档中推荐迁移至 Qwen3 系列新模型，实际开发中应优先选用 `qwen3.7-plus`、`qwen3.8-max` 等当前主力型号。

## 关键参数

不同模态任务依赖特定参数组合，需严格遵循接口规范：

| 任务类型 | 必填参数 | 关键可选参数 | 说明 |
|----------|----------|----------------|------|
| 文生文（OpenAI 兼容） | `model`, `messages` | `extra_body: {enable_thinking: true}`, `stream`, `stream_options.include_usage` | `enable_thinking` 控制是否输出 `reasoning_content`；`stream_options.include_usage` 启用流式 [Token](../concepts/token.md) 统计 |
| 文生图（万相 V2） | `input.prompt` | `input.negative_prompt`, `parameters.prompt_extend` | `prompt_extend` 默认 `true`，开启大模型自动扩写；V1 不支持该参数 |
| 文生视频（万相 3.0） | `input.prompt` | `input.images`, `input.audio`, `parameters.prompt_extend` | 支持多模态输入引用（图N/音频N）；`prompt_extend` 同样适用 |
| 图生视频（Vidu） | `input.prompt`, `input.image_url` | `input.video_url`, `parameters.dynamic_level` | `dynamic_level` 控制运动幅度（`large`/`medium`/`small`） |
| 实时音视频（AOQ） | `session.turn_detection` | `audio_codec`, `video_fps` | `turn_detection: null` 表示 Manual 模式（按键触发）；`server_vad` 表示服务端自动切分轮次 [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md) |
| RAG（LlamaIndex） | `documents`, `index_name` | `os.environ['DASHSCOPE_WORKSPACE_ID']` | 业务空间 ID 决定文档解析与知识库存储位置 |

## 使用方式

1. **API 调用**：所有模型均支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（`/chat/completions`）或 DashScope 原生接口（`/text-generation/generation`），需配置 `base_url` 为对应地域 + 业务空间域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）。  
2. **SDK 集成**：Python 使用 `dashscope` 或 `openai` 客户端；移动端使用 AOQ Client SDK（Android/iOS/HarmonyOS）；Web 端使用 WebRTC 原生 API。  
3. **[Prompt 工程](../concepts/prompt.md)**：  
   - 文生文推荐使用 [Prompt 框架](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)（背景/目的/风格/语气/受众/输出）；  
   - 文生图/视频采用结构化公式（主体+场景+运动+美学控制+风格化），并善用提示词词典细化镜头语言与氛围词；  
   - 万相 3.0 支持 `/wan3-pe` Skill 进行提示词在线调优。  
4. **缓存与限流**：  
   - 显式缓存通过 `cache_control` 标记实现，Claude Code、OpenCode 等工具原生支持 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)；  
   - 限流应对需结合平台排队（加 `X-DashScope-Queue-Enable: true` 请求头）、客户端令牌桶/并发信号量、架构层 MQ 削峰等多级策略 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。  

## 限制和注意事项

- **地域与业务空间绑定**：所有三方模型（DeepSeek、Kimi、GLM、MiniMax 等）及实时音视频服务仅在华北2（北京）地域可用，且必须配置 `WorkspaceId` 到 `base_url`；其他地域（如新加坡、美国）仅支持部分原生模型。  
- **文件解析限制**：DashScopeParse 文档解析器要求单个 PDF/DOCX 文件 ≤100MB 且 ≤1000 页 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。  
- **[Token](../concepts/token.md) 计费差异**：Prompt 优化功能、显式缓存首次写入、思考模式输出 `reasoning_content` 均计入 [Token](../concepts/token.md) 消耗，需在成本评估中纳入 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)。  
- **安全合规要求**：客户端严禁硬编码 `DASHSCOPE_API_KEY`；AOQ 场景下 API Key 必须由业务 AppServer 代理鉴权并下发临时 Token [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)。  
- **模型兼容性**：WebRTC 模式仅支持 `server_vad` 或 `semantic_vad`，不支持 Manual 模式；而 AOQ 的 Manual 模式需显式调用 `input_audio_buffer.commit` 和 `response.create` [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)。

## 来源文档

- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)
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
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
- [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)
- [技术解决方案](../../raw/model-user-guide/use-cases/technical-solutions.md)
- [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](../../raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/_short/speech-synthesis-using-aoq-access-qwen-audio-3-0-43022e91dedcb0c1.md)
- [视频生成Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)


