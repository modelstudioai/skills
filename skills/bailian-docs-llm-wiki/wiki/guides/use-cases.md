# use cases

百炼平台提供覆盖文本、图像、视频、语音等多模态生成与理解能力的完整用例体系，支持从基础 [Prompt 工程](../concepts/prompt-engineering.md)到复杂 Agent 构建的全栈开发。核心能力围绕模型调用、提示词优化、缓存加速、实时交互及三方集成展开，所有用例均基于生产环境验证的最佳实践。

## 支持的模型/功能

百炼支持文生文、文生图、文生视频、图生视频、参考生视频、实时音视频对话、RAG 应用构建、自定义模型微调等主流 AI 用例。具体模型包括：

- **文生文**：Qwen 系列（如 `qwen3.7-max`）、DeepSeek（`siliconflow/deepseek-v3.2`）、Kimi（`kimi/kimi-k3`）、GLM（`ZHIPU/GLM-5.3`）、MiniMax（`MiniMax/MiniMax-M2.7`）、Stepfun（`stepfun/step-3.7-flash`）、MiMo（`xiaomi/mimo-v2.5-pro`）、Unisound（`unisound/unisound-u2`）等 [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)；
- **文生图**：万相系列（`wan-image-v2`、`wan-image-v1`）[文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)；
- **文生视频/多模态视频生成**：万相 3.0（`wan3`）、Vidu（`vidu`）[万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)、[Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)；
- **实时音视频**：`qwen3.8-omni-flash-realtime`、`qwen-audio-3.1-realtime-plus`、`qwen-audio-3.0-tts-flash`、`fun-asr-realtime`，支持 WebRTC 和 AOQ 两种接入协议；
- **RAG 与知识增强**：基于 LlamaIndex 的检索增强应用构建 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)；
- **模型定制**：支持 LoRA 微调、部署与评测全流程 [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)。

> **注意**：多个三方模型文档（如 DeepSeek、Kimi、GLM、MiniMax）均明确标注了模型下架时间（集中于 2026 年 7–10 月），并统一推荐迁移到 Qwen 系列新模型（如 `qwen3.7-plus`、`qwen3.8-max`）。开发者应优先选用推荐模型，避免依赖即将下线的旧版本。

## 关键参数

不同模态任务的关键参数存在显著差异，需按模型类型严格配置：

- **文生文**：通用 `messages` 结构；支持 `enable_thinking`（控制思考模式）、`reasoning_effort`（控制推理深度）、`cache_control`（显式缓存标记）等非标准扩展参数；
- **文生图**：`prompt`（正向提示词）、`negative_prompt`（反向提示词）、`prompt_extend`（是否启用大模型智能改写，默认 `true`）；
- **文生视频（万相）**：`prompt`（主体+场景+运动）、`parameters.prompt_extend`（同文生图）、分镜结构（`分镜N（起-止秒）：...`）；
- **Vidu 视频**：强调“主体/场景+场景描述+环境描述+艺术风格/媒介”公式，支持 `大动态`、`左移`、`固定镜头` 等运镜关键词；
- **实时音视频（AOQ/WebRTC）**：`turn_detection`（设为 `null` 启用手动模式，或 `server_vad`/`semantic_vad` 启用服务端 VAD）、`input_audio_buffer.append`（手动模式下禁用）；
- **显式缓存**：通过请求体中 `cache_control` 字段（值为 `{"type": "ephemeral"}`）启用，首次写入产生 25% 额外开销，后续命中节省 90% 成本 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)。

## 使用方式

### 提示词工程
- **文生文**：推荐使用结构化 Prompt 框架（背景、目的、风格、语气、受众、输出格式），并利用平台内置的 [Prompt一键优化工具](https://bailian.console.aliyun.com/flow-agent/component-manage/prompt) 进行自动扩写 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)；
- **文生图/视频**：采用分层公式——基础公式（主体+场景+风格/运动）用于快速试错，进阶公式（主体描述+场景描述+美学控制+氛围词+细节修饰）用于精细控制；
- **万相 3.0 多镜头视频**：必须使用完整公式，包含总体描述、分镜时间戳、参考素材引用（图N/视频N/音频N）、台词、音效、负向清单等要素。

### 部署与调用
- **三方模型**：统一通过 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)调用，需配置地域专属 `base_url`（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），模型名格式为 `<provider>/<model-id>`（如 `siliconflow/deepseek-v3.2`）；
- **实时音视频**：
  - WebRTC 方案适用于浏览器端低延迟语音，需处理 SDP 交换（通常由后端代理）；
  - AOQ 方案适用于移动端（Android/iOS/HarmonyOS），需导入 SDK 及 Opus 插件，并通过业务 AppServer 代理 [Token](../concepts/token.md) 鉴权；
- **RAG 应用**：使用 `DashScopeCloudIndex` 封装知识库，通过 `DashScopeCloudRetriever` 获取检索器，无缝集成至 LlamaIndex 流程。

### 缓存与性能优化
- 显式缓存适用于高频复用相同 Prompt 的场景，尤其适合 Agent 中的 system reminder、recap 等固定上下文片段；
- 对于 Claude Code、Open Code 等工具，接入百炼 Anthropic 兼容端点后默认启用缓存，无需额外配置；
- 限流应对需分层实施：平台侧启用服务端排队或提升 PTU 配额；客户端实现令牌桶或并发信号量；架构侧引入 MQ 削峰或模型降级兜底 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。

## 限制和注意事项

- **地域与权限约束**：绝大多数三方模型（DeepSeek-硅基流动、Kimi-月之暗面、GLM-智谱、MiniMax-稀宇科技、MiMo、Stepfun、Unisound）仅支持华北2（北京）地域，且要求 API Key 必须从此地域获取；
- **模型生命周期**：DeepSeek、Kimi、GLM、MiniMax 等模型存在明确下架时间（2026 年中旬至年末），文档中已多次强调迁移路径，开发者需主动规划升级；
- **实时音视频权限**：WebRTC 方案需浏览器麦克风/摄像头权限；AOQ 方案需在各平台 manifest 文件中声明 `RECORD_AUDIO`、`CAMERA` 等权限，并在运行时动态申请；
- **缓存确定性**：显式缓存要求输入内容完全一致（含空格、标点、换行）才能 100% 命中，动态字段（如日期、git 状态）需移至 user message 以提升跨会话命中率；
- **文件处理限制**：`DashScopeParse` 文档解析器要求单个 PDF/DOC/DOCX 文件 ≤ 100MB 且 ≤ 1000 页 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。

## 来源文档

- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)
- [视频生成Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
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
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)


