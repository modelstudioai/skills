# use cases

百炼平台的 use cases 覆盖多模态生成、大模型推理、实时音视频交互、RAG 构建及模型定制等核心场景。开发者可根据业务需求选择对应能力，结合结构化 [Prompt 工程](../concepts/prompt-engineering.md)、显式缓存、限流控制等最佳实践提升稳定性与效率。所有用例均基于阿里云百炼统一 API 体系，支持 OpenAI 兼容与 DashScope 原生协议。

## 支持的模型/功能

- **多模态生成**：万相系列（wan3.0、wan2.x）支持文生视频、图生视频、参考生视频等 10+ 任务类型，涵盖首尾帧过渡、风格迁移、音频对齐等高级能力；Vidu 模型提供精细化运镜控制与导演风格触发词 [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)。
- **文本生成与理解**：除通义千问系列外，平台集成 DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun、Unisound 等主流三方模型，均支持思考模式（`enable_thinking`/`reasoning_effort`）、流式响应与结构化输出 [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)。
- **实时音视频交互**：qwen3.8-omni-flash-realtime、qwen-audio-3.1-realtime-plus、fun-asr-realtime 等模型通过 AOQ 或 WebRTC 协议实现低延迟语音对话、TTS 合成与 ASR 识别，支持 Manual/VAD 双模式轮次控制 [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)。
- **检索增强（RAG）**：基于 LlamaIndex 的 `DashScopeCloudIndex` 提供文档解析、知识库构建与检索一体化流程，支持 PDF/DOCX 在线切分与多业务空间隔离 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。
- **模型定制与部署**：支持 LoRA 微调、全参数微调及量化部署，训练数据需符合 ChatML 格式（jsonl），最小建议量为 500 条高质量样本 [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)。

> **注意**：部分三方模型存在地域限制。例如，Kimi-月之暗面、DeepSeek-硅基流动、MiMo-小米等文档均明确标注“仅华北2（北京）地域可用”，而 Kimi（阿里云版）、GLM（阿里云版）等则支持多地域（如新加坡、东京、弗吉尼亚）。开发者需严格按模型文档指定地域配置 `base_url`，否则请求将失败。

## 关键参数

- **Prompt 相关**：
  - `prompt` / `negative_prompt`：文生图必需字段，分别控制正向描述与排除内容；
  - `prompt_extend`：文生图 V2 特有开关，默认 `true`，启用大模型智能扩写；
  - 多模态视频生成中，`prompt` 需遵循分镜公式，支持 `图N`/`视频N`/`音频N` 引用语法 [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)。
- **推理控制**：
  - `enable_thinking` / `reasoning_effort`：控制思考模式开启与深度，非 OpenAI 标准参数，须通过 `extra_body`（Python SDK）或顶层参数（Node.js SDK）传入；
  - `stream` + `stream_options.include_usage`：启用流式响应并返回 Token 消耗；
  - `cache_control`：显式缓存标记，用于 `system`/`user` 消息级缓存命中控制。
- **实时交互**：
  - `turn_detection`：设为 `null` 启用 Manual 模式（按键控制），设为 `{"type": "server_vad"}` 启用服务端 VAD 自动检测；
  - `input_audio_buffer.append` / `.commit`：Manual 模式下客户端需显式提交音频段。

## 使用方式

- **API 调用**：统一采用 [OpenAI 兼容接口](../concepts/openai-compatibility.md)（推荐）或 DashScope 原生接口。OpenAI 方式需配置 `base_url` 为 `{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`，并确保 `DASHSCOPE_API_KEY` 环境变量已设置。
- **SDK 集成**：Python 使用 `openai==1.45.0+` 或 `dashscope>=1.25.0`；移动端接入 AOQ SDK 需按平台导入 `.aar`/`.framework`/`.har` 及 Opus 插件，并声明必要权限（如 `RECORD_AUDIO`）。
- **[Prompt 工程](../concepts/prompt-engineering.md)**：
  - 文生图推荐进阶公式：`主体（描述）+ 场景（描述）+ 风格 + 镜头语言 + 氛围词 + 细节修饰`；
  - 视频生成优先使用多镜头公式：`总体描述 + 镜头序号 + 时间戳 + 分镜内容`，确保时间轴对齐；
  - LLM 文本生成应采用 Prompt 框架（背景/目的/风格/语气/受众/输出），避免模糊指令。
- **缓存与限流**：
  - 显式缓存需在 `messages` 中为关键消息添加 `"cache_control": {"type": "ephemeral"}`；
  - 应对限流首选平台层方案：添加 `X-DashScope-Queue-Enable: true` 请求头启用服务端排队，或使用 Batch API 合并请求。

## 限制和注意事项

- **模型生命周期**：部分旧版模型已明确标注下架时间，如 `deepseek-r1-distill-qwen-14b` 等将于 2026 年 10 月 10 日下架，`kimi/kimi-k2.5` 将于 2026 年 8 月 31 日下架，文档中均已给出替代型号建议，开发者需及时迁移。
- **地域与协议约束**：
  - WebRTC 方案受浏览器 CORS 限制，Demo 中需通过 curl 代理 SDP 交换；生产环境必须由业务后端代理；
  - AOQ 实时语音识别（fun-asr-realtime）使用 Inference 协议，而 qwen-audio-3.1-realtime-plus 使用 Realtime 协议，二者事件语义与客户端处理逻辑不同，不可混用。
- **资源与配额**：
  - 自定义模型训练需消耗 GPU 实例时长，部署后产生独占实例费用；
  - 显式缓存首次写入产生 25% 额外开销，但后续命中可节省 90% 成本，适合高频复用场景；
  - 百炼 API 按 RPM/TPM/RPS/TPS/增速多维限流，错误码 `Throttling.RateQuota` 对应请求频率超限，需配合令牌桶或并发信号量进行客户端流控 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。

## 来源文档

- [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [视频生成Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)
- [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
- [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
- [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](../../raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/_short/speech-synthesis-using-aoq-access-qwen-audio-3-0-43022e91dedcb0c1.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)
- [技术解决方案](../../raw/model-user-guide/use-cases/technical-solutions.md)


