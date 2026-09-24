# use cases

百炼平台提供覆盖文本、图像、视频、语音、实时交互等多模态场景的完整能力矩阵，支持从基础 Prompt 工程到复杂 RAG 应用、自定义模型调优及第三方模型集成的全栈式开发。本文档面向开发者，结构化梳理核心使用模式、关键参数、接入方式与实践约束，帮助您快速定位适配方案并规避常见陷阱。

## 支持的模型/功能

百炼支持三大类模型能力：**原生大模型（Qwen 系列）**、**多模态生成模型（万相、Vidu、Qwen-Omni）** 和 **第三方直供模型（DeepSeek、Kimi、GLM、MiniMax 等）**。

- **文生文（Text-to-Text）**：以 `qwen3.7-max`、`qwen3.8-omni-flash-realtime` 为代表，支持标准 Chat Completion、流式响应、思考链（reasoning_content）输出及显式缓存。[文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md) 提供了从基础框架到自动优化的完整方法论。
- **文生图（Text-to-Image）**：通过 `万相-文生图V2` 实现，支持 `prompt`（正向提示词）、`negative_prompt`（反向提示词）及 `prompt_extend`（智能扩写）参数，推荐启用默认的 `prompt_extend: true` 以提升生成质量。详见 [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)。
- **文生视频/图生视频**：`万相3.0` 和 `Vidu` 提供差异化能力。万相3.0 支持多任务类型（文生视频、首尾帧生视频、参考生视频等）及结构化分镜提示词；Vidu 则强调初阶公式（主体/场景+描述+风格）与运镜/特效关键词控制。二者均需严格遵循地域与业务空间 ID 的 URL 配置。
- **实时音视频**：`qwen3.8-omni-flash-realtime` 是核心实时模型，支持 WebRTC（浏览器端）和 AOQ（移动端/嵌入式）双通道接入，提供 Manual 模式（按键触发）与 VAD 模式（服务端自动检测）两种会话控制策略。[通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md) 文档详细说明了浏览器端低延迟实现细节。
- **第三方模型**：通过 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)或 DashScope SDK 接入 DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun、Unisound 等厂商模型。所有直供模型均仅限华北2（北京）地域使用，且普遍支持 `enable_thinking` 或 `reasoning_effort` 参数开启思考模式。注意不同文档对同一模型的下架时间存在差异，需交叉核验。

> **注意**：文档 10（DeepSeek-阿里云）称 `deepseek-v3` 系列将于 2026年10月10日下架，而文档 11（DeepSeek-硅基流动）与文档 12（DeepSeek-快手万擎）未提具体下架时间。实际部署应以控制台最新公告为准，避免依赖已计划下线的模型。

## 关键参数

不同模型类型的关键参数设计目标明确，需按场景精准设置：

- **Prompt 相关**：
  - `prompt`：所有生成类模型的核心输入，必须清晰、具体、结构化。推荐使用 [Prompt框架](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)（背景/目的/风格/语气/受众/输出）构建。
  - `negative_prompt`：仅文生图模型（万相V1/V2）支持，用于排除不希望出现的元素（如“人物”、“文字水印”）。
  - `prompt_extend`：万相V2 特有布尔参数，默认 `true`，开启后由大模型自动扩写提示词，显著提升图像质量。
  - `cache_control`：显式缓存标记，用于 Anthropic 协议接入（如 Claude Code、Open Code），可实现 100% 确定性命中，大幅降低成本。

- **推理控制**：
  - `enable_thinking` / `reasoning_effort`：适用于 DeepSeek、Kimi、GLM、MiMo、Stepfun、Unisound 等第三方模型及部分 Qwen 模型。设为 `true` 或 `"max"` 可返回 `reasoning_content` 字段，用于调试与可解释性分析。
  - `server_vad` / `semantic_vad`：实时语音模型（如 `qwen3.8-omni-flash-realtime`）的服务端语音活动检测参数，决定轮次自动切分逻辑。
  - `turn_detection: null`：Manual 模式开关，客户端需自行发送 `input_audio_buffer.commit` 和 `response.create` 控制会话节奏。

- **多媒体控制**：
  - `stream_options: { "include_usage": true }`：流式请求中获取 [Token](../concepts/token.md) 消耗统计，对成本监控至关重要。
  - `audio_format`, `video_fps`, `resolution`：AOQ/Webrtc 场景下需在客户端 SDK 层配置，服务端 API 不直接暴露。

## 使用方式

接入流程遵循“准备 → 配置 → 调用 → 处理”四步法：

1. **准备**：获取 API Key 并配置至环境变量（`DASHSCOPE_API_KEY`）；开通对应服务（如知识库、实时音视频）；下载并导入 SDK（DashScope、AOQ、OpenAI Python SDK 等）。
2. **配置**：
   - 地域与业务空间：所有直供模型及万相/Vidu 均需将 `{WorkspaceId}` 替换为真实 ID，并选择正确地域域名（如 `cn-beijing.maas.aliyuncs.com`）。
   - 模型标识：使用完整模型名，如 `siliconflow/deepseek-v3.2`、`kimi/kimi-k3`、`wan3.0`，不可省略供应商前缀。
   - 请求头：显式缓存需添加 `cache-control: private`；限流排队需添加 `X-DashScope-Queue-Enable: true`。
3. **调用**：
   - 同步调用：适用于简单文本生成、RAG 查询等低延迟场景。
   - 流式调用：`stream=True` 是实时语音、长文本生成、思考过程展示的必备选项，需正确处理 `reasoning_content` 与 `content` 字段的分段到达。
   - 多模态输入：图生视频需上传首帧图并传入 `image_url`；参考生视频需在 [prompt](prompt.md) 中引用 `图1`/`视频2` 等编号。
4. **处理**：
   - 错误重试：针对 `429` 限流错误，优先采用 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md) 中的“服务端排队等待”（加请求头）而非简单重试。
   - 缓存管理：显式缓存首次写入有 25% 额外开销，但后续命中可降本 90%，适合高频复用 Prompt 的 Agent 场景。
   - RAG 集成：使用 `llama-index-indices-managed-dashscope` 包，通过 `DashScopeCloudIndex` 创建和读取知识库，无需自行管理向量数据库。

## 限制和注意事项

- **地域与模型绑定**：除 Qwen 原生模型外，所有第三方模型（DeepSeek、Kimi、GLM、MiniMax 等）及 Vidu、万相3.0 均**仅支持华北2（北京）地域**。跨地域调用将失败。
- **限流维度**：API 同时受 RPM（每分钟请求数）、TPM（每分钟 [Token](../concepts/token.md) 数）、RPS（每秒请求数）、TPS（每秒 [Token](../concepts/token.md) 数）及 Traffic Burst（突发流量）五重限制。高并发场景必须结合 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md) 进行客户端流控或架构兜底。
- **文件与内容限制**：
  - 文档解析：`DashScopeParse` 支持单个 PDF/DOC/DOCX 文件 ≤100MB 且 ≤1000 页。
  - 视频生成：万相3.0 单次请求最大时长为 15 秒；Vidu 对提示词长度无明确上限，但过长会导致截断。
- **安全与合规**：
  - API Key 绝不可硬编码于客户端（尤其是 Android/iOS App）。实时语音场景必须通过业务 AppServer 代理鉴权，客户端仅持有短期 Token。
  - 训练数据必须脱敏，移除 PII（个人身份信息）及敏感词汇，符合《生成式人工智能服务管理暂行办法》。
- **模型演进**：第三方模型下架时间分散（如 Kimi-K2-Instruct 于 2026年7月9日下架，GLM-4.6/4.7 于 2026年10月10日下架），文档间存在版本冲突风险。生产环境应定期检查控制台公告并迁移至推荐模型（如 `qwen3.7-plus`）。

## 来源文档

- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)
- [视频生成Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
- [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
- [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](../../raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/_short/speech-synthesis-using-aoq-access-qwen-audio-3-0-43022e91dedcb0c1.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)
- [技术解决方案](../../raw/model-user-guide/use-cases/technical-solutions.md)
- [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)


