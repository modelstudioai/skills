# use cases

百炼平台的 use cases 文档体系覆盖从基础提示工程、多模态生成、模型调优到实时音视频交互等全栈 AI 应用场景。本文档面向开发者，结构化梳理核心能力边界、参数规范与工程实践要点，聚焦可复用的技术路径，避免概念性描述。

## 支持的模型/功能

百炼支持三类主流使用范式：  
- **文生类（Text-to-X）**：包括文生文（如 `qwen3.7-max`）、文生图（[万相-文生图V2](raw/model-user-guide/use-cases/text-to-image-prompt.md)）、文生视频（[万相文生视频API](raw/model-user-guide/use-cases/text-to-video-prompt.md)）及第三方多模态模型（如 `qwen3.8-omni-flash-realtime`）；  
- **模型调优与部署**：支持基于业务数据微调通用大模型，完成训练、部署、评测闭环，适用于客服问答、行业知识增强等场景 [自定义模型调优、部署与评测](raw/model-user-guide/use-cases/model-training-best-practices.md)；  
- **实时交互套件**：提供 WebRTC 与 AOQ 双通道接入方案，覆盖浏览器端低延迟语音（WebRTC）、移动端按键通话（AOQ Manual 模式）、纯语音识别（`fun-asr-realtime`）及流式 TTS（`qwen-audio-3.0-tts-flash`）等硬件级集成能力。

> **注意**：文档中提及的 `kimi-k2-thinking`、`deepseek-v3.2`、`glm-4.6` 等模型均标注了明确下架时间（2026年7–10月），且部分文档（如 [DeepSeek-阿里云](raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)）已推荐迁移至 `qwen3.7-plus` 等 Qwen 系列模型。开发者应以控制台实际可用模型为准，避免依赖已标记淘汰的模型标识。

## 关键参数

不同模态任务的关键参数存在显著差异，需严格按模型文档配置：  
- **文生文**：核心为 `messages` 结构（含 `role`/`content`），支持 `stream`、`temperature`、`top_p` 等通用采样参数；思考型模型（如 `ZHIPU/GLM-5.3`、`stepfun/step-3.7-flash`）需通过 `extra_body={"enable_thinking": true}` 显式启用推理过程，并可选 `reasoning_effort` 控制深度；  
- **文生图**：必填 `prompt`（正向提示词）与 `negative_prompt`（反向提示词），V2 版本支持 `prompt_extend: true` 启用大模型智能扩写；  
- **文生视频**：除 `prompt` 外，`wan3.0` 及以上版本支持 `sound_description`（人声/音效/BGM）、`multi_shot`（分镜控制）等结构化参数；  
- **实时音视频**：`qwen3.8-omni-flash-realtime` 等模型需指定 `turn_detection`（`server_vad` 或 `null`），`fun-asr-realtime` 则使用 `Inference` 协议而非 `Realtime` 协议，协议类型错误将导致连接失败。

## 使用方式

- **Prompt 工程**：推荐采用结构化框架（背景/目的/风格/语气/受众/输出），而非自由文本。[文生文Prompt指南](raw/model-user-guide/use-cases/prompt-engineering-guide.md) 提供一键优化工具入口，但需注意其消耗 [Token](../concepts/token.md) 并按推理计费；  
- **RAG 集成**：基于 LlamaIndex 构建时，必须使用 `DashScopeParse` 解析器处理 `.pdf`/`.docx` 文件（单文件 ≤100MB，≤1000页），并显式设置 `DASHSCOPE_WORKSPACE_ID` 环境变量以绑定业务空间；  
- **缓存优化**：对高频复用 Prompt（如 Agent 的 system reminder），应启用显式缓存（`cache_control` 标记），其成本收益模型为：首次写入 +25% 开销，后续命中节省 90% 成本；  
- **三方模型调用**：所有华北2（北京）地域直供模型（如 `siliconflow/deepseek-v3.2`、`xiaomi/mimo-v2.5-pro`）必须使用业务空间专属域名 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，而非通用 `dashscope.aliyuncs.com`，否则请求将被拒绝。

## 限制和注意事项

- **地域强约束**：绝大多数三方模型（DeepSeek-硅基流动、Kimi-月之暗面、MiMo 等）仅在华北2（北京）地域可用，且 API Key 必须从该地域获取；跨地域调用将返回鉴权失败；  
- **限流策略**：API 按 RPM/TPM（分钟级）、RPS/TPS（瞬时）、Traffic Burst（增速）三维度限流。突发流量触发 `429` 错误时，优先尝试服务端排队（添加 `X-DashScope-Queue-Enable: true` 请求头），而非客户端重试；  
- **实时交互权限**：WebRTC 方案需浏览器主动申请 `microphone`（必需）与 `camera`（可选）权限；AOQ 方案中，Android/iOS/HarmonyOS 均需在 `AndroidManifest.xml`/`Info.plist`/`module.json5` 中声明对应权限，且 `RECORD_AUDIO` 必须动态申请；  
- **安全红线**：API Key 严禁硬编码于客户端（如 Android APK、iOS IPA、前端 JS），必须由业务 AppServer 代理鉴权并下发临时 [Token](../concepts/token.md)；文档 [使用 AOQ 接入 qwen3.8-omni-flash-realtime](raw/model-user-guide/use-cases/realtime-audio-video-integration/use-aoq-to-access-qwen3-5-omni-plus-realtime-to-realize-key-voice-dialogue.md) 明确强调“API Key 只保存在业务 AppServer，不要写入客户端代码”。

## 来源文档

- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/use-aoq-to-access-qwen3-5-omni-plus-realtime-to-realize-key-voice-dialogue.md)
- [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/real-time-voice-conversation-using-aoq-access-qwen-audio-3-0-realtime-plus.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/real-time-speech-recognition-using-aoq-access-fun-asr-realtime.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/speech-synthesis-using-aoq-access-qwen-audio-3-0-tts-flash.md)
- [技术解决方案](../../raw/model-user-guide/use-cases/technical-solutions.md)


