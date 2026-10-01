# use cases

百炼平台提供覆盖文本、图像、视频、语音等多模态内容生成与理解的完整用例体系，支持从基础 Prompt 工程到复杂 Agent 构建、实时音视频交互及模型定制化调优。开发者可根据业务需求选择对应能力组合，快速集成 AI 能力。

## 支持的模型/功能

百炼支持两类核心模型能力：**原生模型服务**（如 Qwen 系列、万相系列）和**三方直供模型**（如 DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun、Unisound 等）。所有模型均通过统一 API 接入，支持 OpenAI 兼容协议与 DashScope SDK。

- **文生文**：支持通用对话、代码生成、Prompt 优化、RAG 应用构建（如 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)）。
- **文生图/图生图**：万相 V1/V2 提供中英文提示词支持，含 `prompt`（正向）与 `negative_prompt`（反向）双参数，并支持大模型智能扩写（`prompt_extend`）。
- **文生视频/图生视频/参考生视频**：万相 3.0 支持多任务类型（文生视频、首尾帧生视频、风格参考等），并引入结构化分镜公式；Vidu 模型则强调“主体/场景+场景描述+环境描述+艺术风格/媒介”的初阶公式与运镜控制词典。
- **实时音视频**：通过 WebRTC 或 AOQ 协议接入 qwen3.8-omni-flash-realtime、qwen-audio-3.1-realtime-plus、fun-asr-realtime 等模型，支持 VAD 自动轮次或 Manual 按键控制模式。
- **模型定制**：支持基于业务数据微调自定义 LLM（[自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)），适用于垂直领域精度提升。

> **注意**：部分三方模型（如 `deepseek-v3`、`kimi-k2.5`、`glm-4.6`、`MiniMax-M2.1`）已明确标注下架时间（2026 年 7–10 月），文档中推荐迁移至 Qwen 系列新模型，实际开发中应优先选用 `qwen3.7-plus`、`qwen3.8-max` 等当前主力型号。

## 关键参数

不同模态任务的关键参数存在显著差异，需按模型类型严格匹配：

- **文生文**：`messages`（ChatML 格式）、`model`、`temperature`、`top_p`；显式缓存依赖 `cache_control` 字段（见 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)）。
- **文生图**：`prompt`（必需）、`negative_prompt`（可选）、`prompt_extend`（V2 默认 `true`）。
- **万相 3.0 视频**：支持结构化提示词，含 `[分镜 N（起-止秒）：...]`、`[台词]`、`[音效/BGM]`、`[负向清单]` 等区块；参考素材通过 `图N/视频N/音频N` 编号引用。
- **Vidu 视频**：强调关键词触发，如 `大动态`、`镜头推`、`宫崎骏风格`、`水墨风格` 等，需结合 [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md) 中的词典使用。
- **实时音视频（AOQ/WebRTC）**：`turn_detection`（`server_vad`/`semantic_vad`/`null`）、`input_audio_buffer.append/commit`、`response.create`；Manual 模式下必须显式调用 commit 与 create。

## 使用方式

1. **API 调用**：所有模型均支持 HTTP RESTful API 与 OpenAI 兼容 SDK（Python/Node.js/Java 等）。[OpenAI 兼容接口](../concepts/openai-compatibility.md)需配置 `base_url` 为地域专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），并传入 `model` 名称（如 `qwen3.7-max`、`siliconflow/deepseek-v3.2`）。
2. **Prompt 工程**：
   - 文生文推荐使用 [Prompt 框架](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)，包含背景、目的、风格、语气、受众、输出六要素；
   - 文生图/视频需按公式组织提示词，基础公式聚焦主体+场景+运动/风格，进阶公式叠加镜头语言、氛围词、细节修饰；
   - 万相 3.0 支持 `/wan3-pe` Skill 进行提示词自动调优。
3. **RAG 集成**：通过 `llama-index-indices-managed-dashscope` 包直接对接百炼知识库，无需自行搭建向量库。
4. **实时交互**：WebRTC 适用于浏览器端低延迟场景；AOQ 更适合移动端（Android/iOS/HarmonyOS），需由 AppServer 代理 Token 鉴权。

## 限制和注意事项

- **限流机制**：百炼 API 按 RPM（每分钟请求数）、TPM（每分钟 Token 数）、RPS（每秒请求数）、TPS（每秒 Token 数）及 Traffic Burst（突发流量）四维限流。高并发场景需结合 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md) 实施客户端重试、服务端排队或架构级 MQ 削峰。
- **地域与模型绑定**：多数三方模型（DeepSeek-硅基流动、Kimi-月之暗面、GLM-智谱、MiniMax-稀宇科技等）仅在华北2（北京）地域可用，且需使用该地域的 API Key 和业务空间 ID。
- **缓存成本**：显式缓存首次写入产生 25% 额外开销，但命中后节省 90% 成本；需确保相同输入内容稳定复用，否则收益递减。
- **文件与资源约束**：文档解析（如 DashScopeParse）要求单个 PDF/DOCX 文件 ≤100MB 且 ≤1000 页；视频生成对首帧图分辨率、时长有隐式限制，超限可能导致静止或截断。
- **安全合规**：训练数据需脱敏处理（移除 PII 及敏感词）；API Key 必须存储于服务端，严禁硬编码至客户端代码或提交至仓库。

## 来源文档

- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [视频生成Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
- [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/_short/speech-synthesis-using-aoq-access-qwen-audio-3-0-43022e91dedcb0c1.md)
- [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](../../raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)
- [技术解决方案](../../raw/model-user-guide/use-cases/technical-solutions.md)


