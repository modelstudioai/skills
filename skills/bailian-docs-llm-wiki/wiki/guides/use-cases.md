# use cases

百炼平台的 use cases 文档面向开发者，系统梳理了主流 AI 应用场景下的模型能力、参数配置、调用方式及关键约束。本文整合文生图、文生视频、三方模型集成、实时音视频、RAG 等核心实践路径，聚焦可落地的技术细节，避免概念性描述，强调参数级控制与工程适配。

## 支持的模型/功能

百炼支持多模态生成与推理两大类 use case：

- **生成类**：覆盖文生图（万相 V1/V2）、文生视频（万相 3.0、Vidu）、图生视频、参考生视频等全链路视觉生成能力；[万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md) 明确支持首帧/首尾帧/主体/运动/风格/音频等 8 类参考生视频任务。
- **推理类**：提供原生 Qwen 系列（如 `qwen3.8-omni-flash-realtime`）、三方直供模型（DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun、Unisound）及专用模型（`fun-asr-realtime`、`qwen-audio-3.0-tts-flash`）。所有三方模型均通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 DashScope SDK 接入，且多数支持 `enable_thinking` 或 `reasoning_effort` 参数控制推理深度。
- **增强类**：支持 RAG 场景下基于 LlamaIndex 的知识库构建与检索，依赖 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md) 提供的 `DashScopeCloudIndex` 和 `DashScopeCloudRetriever`。

> **注意**：多个文档存在模型下架时间冲突。例如，[Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md) 文档称 `kimi-k2-instruct` 等于 2026年7月9日下架，而 [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md) 文档则标注 `kimi/kimi-k2.5` 下架时间为 2026年8月31日。实际部署应以控制台最新公告为准，优先迁移至 `qwen3.8-*` 系列。

## 关键参数

不同 use case 的核心参数高度结构化，需严格按模型要求传入：

- **文生图**：`prompt`（正向提示词）、`negative_prompt`（反向提示词）、`prompt_extend`（V2 特有，默认 `true`，开启大模型智能改写）——详见 [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)。
- **视频生成**：除基础 `prompt` 外，万相 3.0 引入分镜语法（`分镜N（起-止秒）：...`）、参考素材引用（`图1`/`视频2`/`音频3`）、负向清单；Vidu 则依赖运镜关键词（`推`/`拉`/`固定`）、动态控制（`大动态`/`小动态`）和导演风格（`宫崎骏风格`）等触发式词典。
- **三方模型推理**：`enable_thinking`（布尔值，控制是否输出 `reasoning_content`）、`reasoning_effort`（字符串，`max`/`high`/`xhigh` 控制推理强度）为通用非标准参数，必须通过 `extra_body`（Python SDK）或顶层字段（Node.js SDK）传入。
- **实时音视频**：`turn_detection` 是关键会话控制参数：设为 `null` 启用 Manual 模式（客户端按键控制音频提交），设为 `server_vad` 或 `semantic_vad` 启用服务端 VAD 自动检测。

## 使用方式

调用方式按场景分为三类：

- **API 直连**：所有模型均支持 HTTP RESTful 调用，需配置地域专属 endpoint（如华北2为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），并传入 `DASHSCOPE_API_KEY`。
- **SDK 集成**：推荐使用 DashScope Python/Java SDK 或 OpenAI 兼容 SDK。三方模型示例代码统一采用 `OpenAI` 客户端初始化，并通过 `base_url` 指向百炼兼容层。
- **框架嵌入**：RAG 场景需安装 `llama-index-llms-dashscope` 和 `llama-index-indices-managed-dashscope` 包，通过 `DashScopeCloudIndex.from_documents()` 创建知识库，再调用 `index.as_retriever()` 获取检索器。

## 限制和注意事项

- **地域强约束**：绝大多数三方模型（DeepSeek-硅基流动、Kimi-月之暗面、GLM-智谱、MiniMax、MiMo、Stepfun、Unisound）仅在华北2（北京）地域可用，且必须使用业务空间专属域名 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，旧域名 `https://dashscope.aliyuncs.com` 已不推荐。
- **限流双维度**：API 受 RPM（每分钟请求数）和 TPM（每分钟 [Token](../concepts/token.md) 数）双重限制，瞬时超限（RPS/TPS）或流量突增（Traffic Burst）均会返回 `429`。[限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md) 明确建议优先启用服务端排队等待（加 `X-DashScope-Queue-Enable: true` 请求头）。
- **缓存与成本**：显式缓存需在请求中添加 `cache_control` 标记，首次写入成本为标准价 25%，后续命中节省 90% 成本；但 Claude Code 默认注入的动态 system prompt（含 git 状态、日期）会导致跨会话命中率下降，需通过 `--exclude-dynamic-system-prompt-sections` 参数优化。
- **安全合规**：AOQ 实时方案严禁将 `DASHSCOPE_API_KEY` 硬编码至客户端，必须由业务 AppServer 代理鉴权并下发临时 [Token](../concepts/token.md)；训练数据需完成脱敏处理，移除个人身份信息与敏感词汇。

## 来源文档

- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)
- [视频生成Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
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
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
- [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
- [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](../../raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/_short/speech-synthesis-using-aoq-access-qwen-audio-3-0-43022e91dedcb0c1.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)
- [技术解决方案](../../raw/model-user-guide/use-cases/technical-solutions.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)


