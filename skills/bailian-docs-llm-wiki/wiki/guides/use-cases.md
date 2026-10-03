# use cases

本文档汇总百炼平台主流使用场景的技术要点，面向开发者提供结构化、可落地的实践指南。涵盖多模态生成（文生图/文生视频）、大模型[提示工程](../concepts/prompt-engineering.md)、RAG应用构建、实时音视频交互、第三方模型集成及系统级优化（缓存、限流）等核心方向。所有内容均基于官方最新文档提炼，强调参数准确性、调用方式一致性与关键限制。

## 支持的模型/功能

百炼平台提供覆盖文本、图像、视频、语音全模态的生成能力，以及面向企业级应用的RAG、实时交互和系统优化能力：

- **多模态生成**：  
  - 文生图：`万相-文生图V1/V2`（支持 `prompt`/`negative_prompt`/`prompt_extend`）[原文标题](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)  
  - 文生视频/图生视频：`万相3.0`、`万相2.x`、`Vidu`（支持分镜控制、参考素材引用、声音描述）[原文标题](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)  
  - 视频生成统一API：兼容 `text-to-video`、`image-to-video`、`video-to-video` 等多种输入模式 [原文标题](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)

- **大模型与RAG**：  
  - 文生文：`qwen3.x` 系列、`kimi-k3`、`glm-5.3`、`deepseek-v4-pro` 等，均支持 `enable_thinking`/`reasoning_effort` 控制推理深度  
  - RAG构建：基于 `LlamaIndex` 的 `DashScopeCloudIndex` 和 `DashScopeCloudRetriever`，支持文档自动解析与知识库管理 [原文标题](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)

- **实时音视频**：  
  - WebRTC方案：适用于浏览器端低延迟交互，支持 `multimodal-dialog` 套件与 `qwen3.8-omni-flash-realtime`  
  - AOQ方案：适用于移动端（Android/iOS/HarmonyOS），支持 `Manual`（按键触发）与 `VAD`（服务端语音检测）两种轮次控制模式  

- **第三方模型集成**：  
  - 提供 `DeepSeek`（阿里云/硅基流动/快手万擎三路）、`Kimi`（月之暗面/阿里云）、`GLM`（智谱/阿里云）、`MiniMax`、`MiMo`、`Unisound`、`Stepfun` 等直供模型，全部通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 DashScope SDK 接入  

> **注意**：多个第三方模型文档存在下架时间冲突。例如，`kimi/kimi-k2.5` 下架时间为 2026年8月31日（[原文标题](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)），而 `kimi-k2-thinking` 已于 2026年7月9日下架（[原文标题](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)）。开发者应以各模型卡片页最新公告为准，优先选用 `qwen3.7-plus` 等推荐替代模型。

## 关键参数

不同场景的核心参数设计直接影响输出质量与稳定性：

- **文生图**：  
  - `prompt`（正向提示词，中英文均可）与 `negative_prompt`（反向提示词）为必填项；  
  - `prompt_extend: true`（V2默认开启）启用大模型智能改写，提升提示词表达力。

- **视频生成**：  
  - `万相3.0` 支持结构化分镜语法（如 `分镜1（00:00-00:03）：...`）及 `负向清单`；  
  - `Vidu` 支持细粒度运镜控制（`推`/`拉`/`左移`/`固定镜头`）与风格关键词（`宫崎骏风格`/`水墨风格`）；  
  - 所有视频模型均支持 `negative_prompt`（隐式或显式）抑制不期望元素。

- **大模型推理**：  
  - 思考模式通用参数：`enable_thinking: true`（`deepseek`/`mimo`/`unisound`）或 `reasoning_effort: "max"`（`kimi`/`glm`）；  
  - 流式响应需设置 `stream: true`，并正确处理 `reasoning_content` 与 `content` 字段分阶段输出。

- **实时音视频**：  
  - `WebRTC` 方案必须使用 `server_vad` 或 `semantic_vad`，不支持 `manual` 模式；  
  - `AOQ` 方案中 `turn_detection: null` 表示手动控制轮次，需客户端显式发送 `input_audio_buffer.commit` 与 `response.create`。

## 使用方式

- **API调用**：  
  - 统一使用 `OpenAI兼容接口`（推荐）或 `DashScope SDK`；  
  - 地域与业务空间ID必须匹配：华北2（北京）地域 URL 为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`；  
  - 第三方模型命名规范为 `<供应商>/<模型名>`（如 `siliconflow/deepseek-v3.2`、`ZHIPU/GLM-5.3`）。

- **SDK集成**：  
  - `LlamaIndex` 需安装 `llama-index-llms-dashscope` 与 `llama-index-indices-managed-dashscope`；  
  - `AOQ` 客户端需按平台导入对应 SDK（`.aar`/`.framework`/`.har`）及 Opus 插件，并声明必要权限（`RECORD_AUDIO`、`CAMERA`）；  
  - `WebRTC` 浏览器端需通过 `RTCPeerConnection` 建立连接，音频流绑定至 `<audio>` 元素播放。

- **工具链辅助**：  
  - `Prompt一键优化工具`（位于 `/flow-agent/component-manage/prompt`）可自动扩写提示词，但消耗 Token；  
  - `万相3.0 Prompt Skill`（`/wan3-pe` 命令）支持在对话框内实时调试视频提示词。

## 限制和注意事项

- **地域与模型绑定**：  
  多数第三方模型（`DeepSeek`/`Kimi`/`GLM`/`MiniMax`/`MiMo`/`Unisound`/`Stepfun`）仅在华北2（北京）地域可用，且需使用该地域的 API Key 与业务空间 ID。

- **实时交互约束**：  
  - `WebRTC` 方案受 CORS 限制，Demo 中需通过 `curl` 代理 SDP 交换，生产环境必须由业务后端代理；  
  - `AOQ` 的 `Manual` 模式要求客户端严格控制 `commit` 与 `create` 时机，避免音频截断或响应延迟。

- **系统级限制**：  
  - `限流` 按主账号+模型维度独立计算，含 RPM/TPM（分钟级）、RPS/TPS（瞬时）、Traffic Burst（增速）三重规则；  
  - `显式缓存` 仅对 `Anthropic协议`（如 `qwen3.7-max`）原生支持，需在请求中注入 `cache_control` 标记；  
  - `文档解析`（`DashScopeParse`）单文件上限为 100MB 且页数 ≤ 1000。

- **安全与合规**：  
  - API Key **严禁硬编码至客户端代码或提交至仓库**，必须由业务 AppServer 代理鉴权并下发临时 Token；  
  - 训练数据需完成脱敏处理，移除个人身份信息与敏感内容。

## 来源文档

- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)
- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [视频生成Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
- [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
- [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](../../raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/_short/speech-synthesis-using-aoq-access-qwen-audio-3-0-43022e91dedcb0c1.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)
- [技术解决方案](../../raw/model-user-guide/use-cases/technical-solutions.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)


