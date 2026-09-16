# use cases

百炼平台提供覆盖文本、图像、视频、语音、多模态交互等全栈 AI 能力，支持从简单 Prompt 调用到复杂工作流编排、自定义模型训练与实时音视频对话的多样化生产级场景。所有用例均基于统一 API 体系与模型服务底座，开发者可按需组合能力模块，快速构建端到端 AI 应用。

## 支持的模型/功能

百炼支持三类核心能力接入方式：  
- **原生模型服务**：包括 Qwen 系列（如 `qwen3.7-max`、`qwen3.5-omni-plus-realtime`）、视觉模型（`qwen3-vl-plus`、`wan2.7`、`happyhorse`）及音频模型（`qwen-audio-3.0-tts-flash`、`fun-asr-realtime`）。  
- **三方直供模型**：通过统一 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)调用 DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun、Unisound 等厂商模型，各模型开通与调用方式详见 [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)。  
- **多模态交互套件**：面向硬件终端（AI 眼镜、学习机、机器人）提供开箱即用的 `multimodal-dialog` 套件，支持可视化配置 Agent、音色、提示词与插件，[通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-multimodal-dialog.md) 即为其典型部署形态。

> **注意**：多个三方模型文档（如 [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)、[Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)、[GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)）均明确标注了模型下架时间（2026 年 7–10 月），且一致推荐迁移至 Qwen3 系列。该策略已形成平台级统一演进方向，开发者应优先选用 `qwen3.7-plus` 或更高版本。

## 关键参数

不同模态任务依赖特定参数控制生成质量与行为：  
- **文生文**：核心为 `prompt`，推荐采用结构化 Prompt 框架（背景/目的/风格/语气/受众/输出），并利用 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md) 中的自动优化工具提升效果。  
- **文生图/图生图**：`prompt`（正向描述）与 `negative_prompt`（反向排除）为必需参数；`prompt_extend: true`（默认开启）启用大模型智能扩写，显著提升画面细节。  
- **文生视频/图生视频**：除基础 `prompt` 外，`wan2.7+` 模型支持 `prompt_extend`、`sound_description`（人声/音效/BGM）及多镜头公式（含时间戳与分镜内容），详见 [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)。  
- **实时音视频**：`qwen3.5-omni-plus-realtime` 等模型需配置 `turn_detection`（`server_vad` / `semantic_vad` / `null`），决定语音轮次由服务端自动检测或客户端按键控制，[使用 AOQ 接入 qwen3.5-omni-plus-realtime 实现按键语音对话](../../raw/model-user-guide/use-cases/use-aoq-to-access-qwen3-5-omni-plus-realtime-to-realize-key-voice-dialogue.md) 对此有明确对比说明。

## 使用方式

根据场景复杂度，推荐三种接入路径：  
- **零代码/低代码**：直接使用百炼控制台的「应用市场」或「无限画布」（如 [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)），通过节点拖拽与自然语言指令完成全流程编排。  
- **SDK/API 集成**：调用 DashScope SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)。文本类模型通用 `chat.completions.create`；多模态模型需指定 `input.image_url` 或 `input.video_url`；实时类模型（如 `qwen-audio-3.0-realtime-plus`）必须通过 AOQ Client SDK 或 WebRTC 实现媒体轨分离传输。  
- **工作流与 RAG**：结合 LlamaIndex 构建检索增强应用，[基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md) 提供了从文档解析、知识库创建到 retriever 初始化的完整代码示例；复杂业务逻辑则通过百炼内置流程编排引擎实现，如 [高效搭建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md) 中的电商客服助手案例。

## 限制和注意事项

- **限流机制**：API 同时受 RPM/TPM（分钟级）、RPS/TPS（瞬时）及 Traffic Burst（增速）三重约束。遇 `429` 错误时，优先尝试服务端排队（加 `X-DashScope-Queue-Enable: true` 请求头），而非简单重试；高并发场景需结合 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md) 中的客户端拥塞控制或 MQ 削峰方案。  
- **缓存策略**：显式缓存（`cache_control`）仅对 Anthropic 协议兼容模型（如 `qwen3.7-max`）生效，且需通过 `Claude Code` 或 `Open Code` 等特定工具链启用；普通 OpenAI 接口调用不支持该特性。  
- **地域与域名**：三方模型（如 GLM-智谱、MiniMax）明确要求华北2（北京）地域及专属业务空间域名 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，旧域名 `https://dashscope.aliyuncs.com` 可能导致性能下降或功能异常。  
- **安全合规**：所有客户端 SDK（AOQ/WebRTC）均要求 API Key 严格托管于业务 AppServer，禁止硬编码至前端或移动 App；移动端需动态申请 `RECORD_AUDIO` 权限，并在 Info.plist 或 AndroidManifest.xml 中声明用途说明。

## 来源文档

- [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)
- [高效搭建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md)
- [深度研究：生成你的独家洞察报告](../../raw/model-user-guide/use-cases/deep-research.md)
- [AI 解题 + 批改：推动课程教学智变](../../raw/model-user-guide/use-cases/ai-homework-helper.md)
- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
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
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-multimodal-dialog.md)
- [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-omni-realtime.md)
- [使用 AOQ 接入 qwen3.5-omni-plus-realtime 实现按键语音对话](../../raw/model-user-guide/use-cases/use-aoq-to-access-qwen3-5-omni-plus-realtime-to-realize-key-voice-dialogue.md)
- [通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-aoq-omni-realtime.md)
- [使用 AOQ 接入 qwen-audio-3.0-realtime-plus 实现实时语音对话](../../raw/model-user-guide/use-cases/real-time-voice-conversation-using-aoq-access-qwen-audio-3-0-realtime-plus.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/model-user-guide/use-cases/speech-synthesis-using-aoq-access-qwen-audio-3-0-tts-flash.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/model-user-guide/use-cases/real-time-speech-recognition-using-aoq-access-fun-asr-realtime.md)


