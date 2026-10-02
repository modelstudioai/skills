# use cases

百炼平台提供覆盖文本、图像、视频、语音等多模态生成与理解的完整能力矩阵，支持从基础 [Prompt 工程](../concepts/prompt-engineering.md)到复杂 RAG、实时音视频交互、三方模型集成等典型开发者场景。本文档结构化梳理核心使用模式，聚焦可落地的技术参数、调用方式与关键约束，帮助开发者快速选型并规避常见陷阱。

## 支持的模型/功能

百炼支持三大类核心能力：**文生文（LLM）**、**文生图/图生图（万相系列）**、**文生视频/图生视频（万相3.0、Vidu）**，以及面向专业场景的**实时音视频交互（AOQ/WebRTC）** 和 **RAG 应用构建（LlamaIndex 集成）**。

- **文生文**：除百炼自研 Qwen 系列外，明确支持 DeepSeek、Kimi、GLM、MiniMax、MiMo、Unisound、Stepfun 等十余家三方模型直供服务，均通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 DashScope SDK 调用 [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)。所有三方模型均需在华北2（北京）地域开通并配置对应业务空间 ID。
- **文生图**：主要由万相系列提供，包括 `万相-文生图V1` 和 `万相-文生图V2`，后者支持 `prompt_extend` 参数启用大模型智能改写 [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)。
- **视频生成**：支持 `万相3.0`、`Vidu` 及 `qwen3.8-omni-flash-realtime` 等模型，覆盖文生视频、图生视频、参考生视频、多镜头叙事及实时音视频通话等多种范式 [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)。
- **实时音视频**：通过 AOQ Client SDK 或 WebRTC 实现，支持 `qwen3.8-omni-flash-realtime`（全模态实时对话）、`qwen-audio-3.1-realtime-plus`（语音助手）、`qwen-audio-3.0-tts-flash`（流式语音合成）和 `fun-asr-realtime`（实时语音识别）四类核心能力。
- **RAG 构建**：提供 `DashScopeCloudIndex` 与 `DashScopeCloudRetriever`，深度集成 LlamaIndex 框架，支持文档自动解析、切分与知识库构建 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。

> **注意**：部分三方模型（如 `kimi/kimi-k2.5`、`MiniMax-M2.1`、`glm-4.6`）已明确标注下架时间（2026年7月-10月），文档中推荐的替代模型（如 `qwen3.7-plus`）应作为首选。不同供应商提供的同名模型（如 `deepseek-v3.2`）在功能上存在差异，例如硅基流动版支持更长上下文，而阿里云百炼版支持联网搜索与缓存，需按需选择。

## 关键参数

各能力模块的关键控制参数高度结构化，但命名与语义存在跨模型差异：

- **Prompt 相关**：
  - `prompt`（正向提示词）与 `negative_prompt`（反向提示词）为文生图、文生视频通用参数。
  - `prompt_extend`（布尔值）仅适用于 `万相-文生图V2`，默认 `true`，开启后由大模型对输入 [prompt](prompt.md) 进行智能扩写。
  - `reasoning_effort`（`max`/`high`/`low`）与 `enable_thinking`（布尔值）是 DeepSeek、Kimi、GLM、MiMo、Unisound、Stepfun 等三方模型的通用思考模式控制参数，用于开启/关闭推理过程输出。

- **视频生成**：
  - `wan3.0` 支持 `prompt` + 多类型参考素材（图N/视频N/音频N）+ 分镜描述（含时间戳、镜头语言、台词、音效）的复合结构。
  - `Vidu` 提供细粒度运镜控制关键词（如 `镜头向左移动`、`升镜头`、`固定镜头`）和风格触发词（如 `宫崎骏风格`、`水墨风格`）。

- **实时音视频**：
  - `turn_detection` 参数决定轮次检测模式：设为 `server_vad` 或 `semantic_vad` 启用服务端 VAD；设为 `null` 则进入 Manual 模式，由客户端通过 `input_audio_buffer.commit` 和 `response.create` 显式控制 [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)。
  - `stream_options.include_usage` 是 OpenAI 兼容 SDK 中获取 [Token](../concepts/token.md) 消耗的必需配置。

## 使用方式

调用方式遵循统一的 API 分层设计，但具体实现路径因场景而异：

- **标准 RESTful API / SDK**：所有文生文、文生图、文生视频模型均通过 HTTP POST 请求调用，推荐使用 DashScope Python SDK 或 OpenAI 兼容 SDK。请求体需严格遵循 `input` 与 `parameters` 两层结构，例如万相V2需将 `prompt_extend` 置于 `parameters` 下。
- **LlamaIndex 集成**：需安装 `llama-index-indices-managed-dashscope` 包，通过 `DashScopeCloudIndex.from_documents()` 创建知识库，并使用 `DashScopeCloudRetriever` 获取检索器。
- **实时音视频**：
  - **WebRTC**：浏览器端直接调用 `RTCPeerConnection`，音频/视频轨道通过 `addTrack()` 添加，服务端 SDP 交换需由业务 AppServer 代理完成。
  - **AOQ**：移动端需导入 `AoqClientSdk` 及 `PluginOpus` [插件](../concepts/plugin.md)，通过 `run-task`/`continue-task`/`finish-task` 控制任务生命周期，音频与事件分轨传输。
- **三方模型**：必须使用专属 `base_url`（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），且 `model` 字段需包含供应商前缀（如 `siliconflow/deepseek-v3.2`、`ZHIPU/GLM-5.3`、`xiaomi/mimo-v2.5-pro`）。

## 限制和注意事项

- **地域与业务空间强绑定**：所有三方模型（DeepSeek、Kimi、GLM、MiniMax、MiMo、Unisound、Stepfun）及实时音视频服务（AOQ/WebRTC）均**仅支持华北2（北京）地域**，且必须配置正确的 `WorkspaceId`。其他地域（如新加坡、美国）的 `base_url` 仅对部分模型（如 Kimi、GLM 的 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)）有效，但功能可能受限。
- **限流策略双重约束**：API 同时受 **RPM/TPM（每分钟请求数/[Token](../concepts/token.md)数）** 和 **RPS/TPS（每秒请求数/[Token](../concepts/token.md)数）** 限制，瞬时高并发易触发 `429` 错误。推荐组合使用平台级排队等待（加 `X-DashScope-Queue-Enable: true` 头）与客户端令牌桶/并发信号量 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。
- **显式缓存适用场景明确**：仅当业务要求“稳定命中缓存”（如 Agent 的 system [prompt](prompt.md) 固定复用）或“高频复用相同 Prompt”时才启用。其成本优势需满足“至少一次命中”，首次写入有 25% 额外开销 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)。
- **文件处理硬性约束**：`DashScopeParse` 文档解析器要求单个 `.pdf`/`.docx` 文件大小 ≤ 100MB 且页数 ≤ 1000 页 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。
- **安全红线**：API Key **严禁硬编码于客户端代码或提交至代码仓库**，必须由业务 AppServer 代理鉴权并下发临时 Token [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)。

## 来源文档

- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)
- [视频生成Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
- [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](../../raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/_short/speech-synthesis-using-aoq-access-qwen-audio-3-0-43022e91dedcb0c1.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)
- [技术解决方案](../../raw/model-user-guide/use-cases/technical-solutions.md)


