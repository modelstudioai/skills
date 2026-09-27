# use cases

百炼平台提供覆盖文本、图像、视频、语音等多模态生成与理解能力的完整用例体系，支持从 Prompt 工程、RAG 构建、模型微调到实时音视频交互的全链路开发。所有用例均基于统一 API 接口设计，可直接集成至生产环境，适用于开发者快速验证业务逻辑并规模化落地。

## 支持的模型/功能

百炼支持三类核心能力模型：

- **文生文（LLM）**：包括 Qwen 系列（如 `qwen3.7-max`）、三方直供模型（如 `ZHIPU/GLM-5.3`、`kimi/kimi-k3`、`MiniMax-M2.7`）及自定义微调模型。所有模型均支持 OpenAI 兼容协议与 DashScope SDK，部分支持 `enable_thinking` 或 `reasoning_effort` 参数控制推理深度 [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)。

- **文生图/图生图（万相）**：`万相-文生图V2` 支持 [prompt](prompt.md) 智能扩写（`prompt_extend: true`），`万相3.0` 提供多任务类型（文生视频、首尾帧生视频、参考生视频等）及完整分镜控制能力 [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)。

- **实时音视频（Realtime & AOQ）**：`qwen3.8-omni-flash-realtime` 和 `qwen-audio-3.1-realtime-plus` 支持 WebRTC 浏览器端低延迟通话；`fun-asr-realtime` 和 `qwen-audio-3.0-tts-flash` 通过 AOQ 协议实现语音识别与合成 [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)。

> **注意**：文档中 `kimi/kimi-k2.5`（[Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)）、`deepseek-v3.2-exp`（[DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)）等模型已明确标注下架时间（2026年），实际调用前需确认模型状态，优先选用推荐替代型号（如 `qwen3.7-plus`）。

## 关键参数

不同模态任务依赖特定参数组合，开发者需按场景精确配置：

- **Prompt 相关**：
  - 文生文：`system`、`messages` 结构化输入；支持 `cache_control` 标记启用显式缓存（需 Anthropic 协议接入）。
  - 文生图：`prompt`（正向描述）、`negative_prompt`（反向过滤），V2 版本默认启用 `prompt_extend: true` 进行大模型智能改写。
  - 视频生成：`prompt` 需遵循公式结构（主体+场景+运动→进阶含美学控制/分镜/声音），万相3.0 支持 `负向清单` 和 `参考素材引用（图N/视频N）`。

- **实时交互**：
  - WebRTC 模式：仅支持 `server_vad` 或 `semantic_vad`，不支持手动模式；需通过 `RTCPeerConnection` 管理音视频轨道。
  - AOQ 模式：`turn_detection` 控制轮次检测方式（`null` 表示 Manual 模式，需客户端显式发送 `input_audio_buffer.commit` 和 `response.create`）。

- **性能与控制**：
  - 所有模型支持 `stream: true` 流式响应；三方模型（如 GLM、MiniMax）需通过 `extra_body` 传入非标准参数（如 `reasoning_effort`）。
  - RAG 场景中，`DashScopeCloudIndex` 创建知识库时需指定 `business space ID`，否则默认使用全局空间 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。

## 使用方式

- **Prompt 工程**：推荐采用结构化框架（背景/目的/风格/语气/受众/输出），避免模糊表述；对高频复用 Prompt，应启用显式缓存以降低 90% 成本 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)。

- **RAG 开发**：使用 `DashScopeParse` 解析 PDF/DOCX 文件（单文件 ≤100MB，≤1000页），再通过 `DashScopeCloudIndex.from_documents()` 创建托管索引，无需自行部署向量数据库。

- **实时音视频**：
  - 浏览器端：WebRTC 方案需代理 SDP 交换（因 CORS 限制），正式环境由 AppServer 代理。
  - 移动端：AOQ SDK 需按平台导入 `.aar`/`.framework`/`.har` 及 Opus 插件，并动态申请 `RECORD_AUDIO` 权限（语音识别/合成场景除外）。

- **三方模型调用**：必须使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），而非通用 `dashscope.aliyuncs.com`，以获得更高稳定性与性能 [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)。

## 限制和注意事项

- **限流机制**：API 按主账号维度、按模型独立计算 RPM/TPM（分钟级）、RPS/TPS（瞬时）及 Traffic Burst（增速）三重限流。突发流量触发时，优先尝试服务端排队等待（添加 `X-DashScope-Queue-Enable: true` 请求头）[限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。

- **地域与模型绑定**：多数三方模型（DeepSeek、Kimi、GLM、MiniMax、Stepfun 等）仅在华北2（北京）地域可用，且需对应地域的 API Key；跨地域调用将失败。

- **文件与资源约束**：
  - 文档解析：`DashScopeParse` 限制单文件 ≤100MB 且 ≤1000页。
  - 视频生成：万相3.0 多镜头视频需严格按 `分镜N（起-止秒）` 格式书写时间戳，否则解析失败。
  - 缓存：显式缓存仅对完全相同的 `cache_control` 标记内容 100% 命中，动态 system [prompt](prompt.md)（如含当前目录/日期）会降低跨会话命中率。

- **安全合规**：API Key 必须保存于服务端，严禁硬编码至客户端代码或提交至仓库；AOQ 方案必须通过 AppServer 实现 [Token](../concepts/token.md) 鉴权，杜绝密钥泄露风险。

## 来源文档

- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [视频生成Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](../../raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)
- [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/_short/speech-synthesis-using-aoq-access-qwen-audio-3-0-43022e91dedcb0c1.md)
- [技术解决方案](../../raw/model-user-guide/use-cases/technical-solutions.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)


