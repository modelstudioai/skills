# use cases

百炼平台提供覆盖文本、图像、视频、语音、实时交互等多模态场景的完整用例支持，涵盖从 Prompt 工程、RAG 构建、模型微调到音视频实时通话的端到端实践路径。所有用例均基于可直接调用的 API 或 SDK 实现，面向开发者设计，强调可复现性与工程落地性。

## 支持的模型/功能

百炼支持三大类核心能力：  
- **文生类**：包括文生文（如 `qwen3.7-max`）、文生图（[万相-文生图V2](raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)）、文生视频（[万相3.0](raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)）；  
- **三方模型集成**：支持 DeepSeek（[硅基流动](raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)、阿里云、快手万擎）、Kimi（[月之暗面](raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)）、GLM（[智谱](raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)）、MiniMax、MiMo、Stepfun、Unisound 等直供模型；  
- **实时音视频**：通过 WebRTC 或 AOQ 协议接入 `qwen3.8-omni-flash-realtime`、`qwen-audio-3.1-realtime-plus`、`fun-asr-realtime` 等实时模型，支持 VAD 自动轮次或 Manual 按键控制两种模式。

> **注意**：多个三方模型文档（如 [DeepSeek-阿里云](raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)、[Kimi](raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)、[GLM](raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)、[MiniMax](raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)）均标注了明确的下架时间（2026年7–10月），且统一推荐迁移至 `qwen3.7-plus`/`qwen3.8-max` 等通义系列模型。该迁移建议具有一致性，开发者应优先采用通义新模型以保障长期可用性。

## 关键参数

不同模态任务的关键参数存在显著差异，需按场景严格配置：  
- **文生文**：`messages`（ChatML 格式）、`stream`、`enable_thinking`（启用思考链）、`reasoning_effort`（控制推理深度）；  
- **文生图**：`prompt`（正向提示词）、`negative_prompt`（反向提示词）、`prompt_extend`（是否启用大模型智能改写，默认 `true`）；  
- **文生视频**：`prompt`（支持多镜头公式）、`prompt_extend`（V2 默认开启）、`negative_prompt`（V2 支持）；  
- **实时音视频（AOQ）**：`turn_detection`（设为 `null` 表示 Manual 模式）、`input_audio_buffer.append`（仅 Manual 模式需显式调用）、`response.create`（触发回复）；  
- **显式缓存**：`cache_control`（需在 system [prompt](prompt.md) 或 user message 中显式声明，详见 [显式缓存最佳实践](raw/model-user-guide/use-cases/explicit-cache-guide.md)）。

## 使用方式

- **Prompt 工程**：推荐使用结构化框架（背景/目的/风格/语气/受众/输出）设计文生文 Prompt；对文生图/视频，采用“主体+场景+运动/风格+镜头语言+氛围词”进阶公式，并善用 [万相3.0视频生成Prompt指南](raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md) 提供的分镜语法；  
- **RAG 应用**：基于 LlamaIndex，通过 `DashScopeParse` 解析文档，`DashScopeCloudIndex` 创建知识库，再获取 `DashScopeCloudRetriever`；  
- **自定义模型**：遵循“调优→部署→评测”三步流程，训练数据需为 ChatML 格式 `.jsonl` 文件，至少 500 条；  
- **实时交互**：WebRTC 方式适用于浏览器低延迟语音，需处理 SDP 交换与媒体轨道管理；AOQ 方式适用于移动端，需由 AppServer 代理 [Token](../concepts/token.md) 鉴权，并按 Inference 或 Realtime 协议处理 Audio/Data 双轨事件；  
- **限流应对**：优先启用平台层“服务端排队等待”（加 `X-DashScope-Queue-Timeout` 请求头），再结合客户端令牌桶或并发信号量控制，详见 [限流应对最佳实践](raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。

## 限制和注意事项

- **地域与域名约束**：绝大多数三方模型（DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun、Unisound）及实时音视频服务**仅支持华北2（北京）地域**，且强烈建议使用业务空间专属域名 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com` 而非通用 `dashscope.aliyuncs.com`；  
- **[Token](../concepts/token.md) 与配额**：显式缓存首次写入产生额外 25% [Token](../concepts/token.md) 开销，但后续命中可节省 90% 成本；限流按主账号+模型独立计算，分钟级（RPM/TPM）与瞬时（RPS/TPS）双重约束，突发流量易触发 `429` 错误；  
- **文件与内容限制**：`DashScopeParse` 文档解析要求单文件 ≤100MB 且 ≤1000 页；文生图 V1 不支持 `prompt_extend` 参数；  
- **安全合规**：API Key 必须保存于服务端，严禁硬编码至客户端代码或提交至仓库；实时音视频需动态申请 `RECORD_AUDIO`/`CAMERA` 运行时权限；  
- **模型兼容性**：[OpenAI 兼容接口](../concepts/openai-compatible-api.md)中，`enable_thinking`、`reasoning_effort`、`thinking` 等非标准参数必须通过 `extra_body`（Python SDK）或顶层参数（Node.js SDK）传入，否则被忽略。

## 来源文档

- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)
- [视频生成Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
- [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](../../raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)
- [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/_short/speech-synthesis-using-aoq-access-qwen-audio-3-0-43022e91dedcb0c1.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)
- [技术解决方案](../../raw/model-user-guide/use-cases/technical-solutions.md)


