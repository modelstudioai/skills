# use cases

百炼平台提供覆盖文本、图像、视频、语音、多模态等全场景的 AI 能力，支持从 [Prompt 工程](../concepts/prompt-engineering.md)、RAG 构建、模型微调到实时音视频交互的完整技术栈。开发者可根据业务需求选择合适的能力组合，快速构建生产级 AI 应用。所有能力均通过统一 API 接入，并支持显式缓存、限流控制与三方模型集成等工程化特性。

## 支持的模型/功能

百炼平台支持以下核心模型与功能类别：

- **文生文（LLM）**：包括 Qwen 系列（如 `qwen3.7-max`）、DeepSeek（如 `siliconflow/deepseek-v3.2`）、Kimi（如 `kimi/kimi-k3`）、GLM（如 `ZHIPU/GLM-5.3`）、MiniMax（如 `MiniMax/MiniMax-M2.7`）、MiMo（如 `xiaomi/mimo-v2.5-pro`）、Step（如 `stepfun/step-3.7-flash`）、Unisound（如 `unisound/unisound-u2`）等。所有模型均支持 `enable_thinking` 或 `reasoning_effort` 参数控制思考模式，输出结构化推理过程与最终答案 [原文标题](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)。

- **文生图 / 图生图**：万相系列模型（`wan-image-api-reference/text-to-image-v2-api-reference.md`），支持 `prompt` 与 `negative_prompt` 双向控制，并可启用 `prompt_extend` 由大模型智能扩写提示词 [原文标题](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)。

- **文生视频 / 多模态视频生成**：万相 3.0（`wan3-video-generation-prompt-guide.md`）与 Vidu（`vidu-video-generation-prompt-guide.md`）支持复杂分镜、参考素材融合、声音描述等高阶控制；其中万相 3.0 提供完整的“提示词公式”与“参考素材引用”机制，明确要求按上传顺序编号（图1/图2/音频1） [原文标题](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)。

- **实时音视频交互**：支持 WebRTC（浏览器端低延迟）与 AOQ（跨平台 SDK）双接入路径，覆盖 `qwen3.8-omni-flash-realtime`（全模态）、`qwen-audio-3.1-realtime-plus`（语音对话）、`qwen-audio-3.0-tts-flash`（TTS）、`fun-asr-realtime`（ASR）等模型，区分 VAD 自动轮次与 Manual 按键控制两种会话模式。

- **RAG 与知识增强**：原生支持 LlamaIndex 集成，通过 `DashScopeCloudIndex` 和 `DashScopeCloudRetriever` 实现知识库创建、文档解析（支持 PDF/DOCX，单文件 ≤100MB、≤1000页）与检索 [原文标题](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。

- **文档转视频**：端到端流水线方案，涵盖文档切片→PPT生成→语音合成→字幕对齐→视频剪辑，依赖 Marp 与 FFmpeg 工具链 [原文标题](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)。

> **注意**：多个三方模型文档（如 DeepSeek、Kimi、GLM）均声明部分旧版本将于 2026 年下架（如 `deepseek-v3.2`、`kimi-k2.5`、`glm-4.7`），但各文档推荐的新模型不一致（例如 Kimi 文档推荐 `kimi-k2.6`，而 GLM 文档推荐 `qwen3.8-max`）。实际选型应以[模型市场](https://bailian.console.aliyun.com/cn-beijing/model/market)当前可用模型为准，避免依赖已标记为下架的型号。

## 关键参数

不同能力模块的关键参数如下：

| 能力类型 | 参数名 | 说明 | 示例值 |
|----------|--------|------|--------|
| 文生文 | `enable_thinking`, `reasoning_effort` | 控制是否输出推理过程及深度 | `"max"`, `"high"`, `true` |
| 文生图 | `prompt`, `negative_prompt`, `prompt_extend` | 正向提示、反向过滤、是否启用智能扩写 | `"一只柯基幼犬在泳池游泳"`, `"人物"`, `true` |
| 文生视频（万相3.0） | `prompt`（含分镜语法） | 支持 `[分镜N（起-止秒）：...]` 结构化描述 | `分镜1（00:00-00:03）：大远景...` |
| 实时音视频（AOQ） | `turn_detection` | 设为 `null` 启用 Manual 模式，由客户端控制轮次 | `null` |
| 显式缓存 | `cache_control` | 在消息中添加该字段标记可缓存片段 | `{"type": "ephemeral"}` |
| RAG（LlamaIndex） | `DASHSCOPE_WORKSPACE_ID` | 决定文档解析结果归属的业务空间 | `"ws-xxx"` |

## 使用方式

- **API 调用**：统一使用 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)或 DashScope SDK。OpenAI 方式需配置 `base_url` 为地域专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），并传入 `model` 名称（如 `siliconflow/deepseek-v3.2`）；DashScope 方式需设置 `dashscope.base_http_api_url`。

- **[Prompt 工程](../concepts/prompt-engineering.md)**：
  - 文生文：采用「背景+目的+风格+语气+受众+输出」六要素框架 [原文标题](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)；
  - 文生图/视频：优先使用进阶公式（主体描述+场景描述+运动/美学控制+风格化），避免模糊术语，强化关键风格词复用；
  - 多模态视频：万相 3.0 必须显式引用上传素材（`图1`/`视频2`/`音频1`），Vidu 则依赖关键词词典（如 `左移`、`延时`、`宫崎骏风格`）触发特定效果。

- **RAG 集成**：基于 `llama-index-indices-managed-dashscope` 包，调用 `DashScopeCloudIndex.from_documents()` 创建索引，再通过 `index.as_retriever()` 获取检索器。

- **实时交互**：
  - WebRTC：浏览器端调用 `RTCPeerConnection`，通过 `getUserMedia` 获取媒体流，`addTrack` 推送至服务端；
  - AOQ：移动端集成 SDK，按平台声明权限（Android 需 `RECORD_AUDIO`，iOS 需 `NSMicrophoneUsageDescription`），通过 Data 轨发送事件、Audio 轨收发音频。

- **缓存与限流**：
  - 显式缓存：在消息中添加 `cache_control` 字段，适用于 Agent 中 system [prompt](prompt.md)、recap 等稳定上下文片段；
  - 限流应对：优先启用「服务端排队等待」（加 `X-DashScope-Queue-Enable: true` 请求头），其次采用客户端令牌桶或并发信号量控制。

## 限制和注意事项

- **地域与模型绑定**：绝大多数三方模型（DeepSeek-硅基流动、Kimi-月之暗面、GLM-智谱、MiniMax、MiMo、Stepfun、Unisound）仅支持华北2（北京）地域，且必须使用业务空间专属域名 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，不可混用通用域名 `https://dashscope.aliyuncs.com`。

- **文件与资源限制**：
  - 文档解析：单个 PDF/DOCX 文件 ≤100MB 且 ≤1000页；
  - 视频生成：万相 3.0 输入首帧图分辨率建议 ≤1024×1024，超长视频（>15s）需分段生成；
  - 实时音视频：WebRTC 模式下浏览器受 CORS 限制，SDP 交换需后端代理；AOQ 模式需客户端动态申请麦克风/摄像头权限。

- **计费与配额**：
  - Prompt 优化工具、显式缓存写入均消耗 Token，按模型推理费用计费；
  - 所有 API 均受 RPM/TPM（每分钟请求数/Token 数）、RPS/TPS（每秒峰值）、Traffic Burst（增速突增）三重限流约束，详见[模型限流条件](raw/model-user-guide/get-started-with-models/rate-limit.md)。

- **安全与合规**：
  - API Key 严禁硬编码于客户端代码，必须由业务 AppServer 代理鉴权并下发临时 Token；
  - 训练数据需脱敏处理，移除个人身份信息与敏感内容；
  - 显式缓存默认开启，如需关闭需设置环境变量 `DISABLE_PROMPT_CACHING=1`。

## 来源文档

- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [视频生成Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
- [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](../../raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/_short/speech-synthesis-using-aoq-access-qwen-audio-3-0-43022e91dedcb0c1.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)
- [技术解决方案](../../raw/model-user-guide/use-cases/technical-solutions.md)


