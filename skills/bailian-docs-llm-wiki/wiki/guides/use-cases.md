# use cases

百炼平台的 use cases 覆盖从基础文本生成到多模态实时交互的完整技术谱系，核心围绕“如何用模型解决具体问题”展开。本文档结构化梳理了主流应用场景所依赖的模型能力、关键参数配置、标准调用方式及工程约束，面向开发者提供可直接落地的技术参考。所有实践均基于平台当前稳定 API 与控制台功能，不包含实验性或已下线特性。

## 支持的模型/功能

百炼支持两类核心模型调用路径：  
- **原生模型服务**：包括文生文（Qwen 系列）、文生图（万相系列）、文生视频（万相3.0、Vidu）、语音合成（Qwen-Audio-TTS、CosyVoice）及实时音视频模型（qwen3.8-omni-flash-realtime、qwen3.8-livetranslate-flash-realtime）。  
- **三方模型集成**：通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 DashScope SDK 接入 DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun、Ling、Unisound 等厂商直供模型，详见 [三方模型调用教程](raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)。  

> **注意**：部分三方模型存在地域限制。例如，[DeepSeek-硅基流动](raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md) 和 [Kimi-月之暗面](raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md) 均明确要求仅限华北2（北京）地域使用，而 [GLM](raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md) 则支持华北2、美国、德国、新加坡、中国香港等多地域。跨地域调用将失败，需严格匹配业务空间 ID 与 endpoint。

实时交互类模型（如 `qwen3.8-omni-flash-realtime`）需配合特定接入协议：WebRTC 适用于浏览器端低延迟音视频通话，AOQ 则覆盖 Android/iOS/HarmonyOS 等移动端场景，二者在媒体传输、事件语义和权限配置上存在本质差异，不可混用。

## 关键参数

不同模态任务的关键参数高度结构化：  
- **文生文**：核心为 `messages`（含 system/user/assistant 角色），支持 `stream`（流式）、`enable_thinking`（思考模式）、`reasoning_effort`（推理深度）等扩展参数；`enable_thinking` 在 DeepSeek、Kimi、MiMo、Stepfun、Ling、Unisound 等模型中均为非 OpenAI 标准参数，需通过 `extra_body`（Python SDK）或顶层字段（Node.js SDK）传入。  
- **文生图**：`prompt`（正向提示词）与 `negative_prompt`（反向提示词）为必需参数；万相 V2 新增 `prompt_extend`（默认 `true`），启用大模型智能扩写，该功能按 [Token](../concepts/token.md) 计费。  
- **文生视频**：万相3.0 支持全要素公式，包含 `[总体描述] + [参考素材引用] + [分镜 N（起-止秒）：主体+场景+运动+美学控制] + [台词] + [音效/BGM] + [风格/情绪] + [负向清单]`；Vidu 则采用更轻量的 `"主体/场景+场景描述+环境描述+艺术风格/媒介"` 结构。  
- **实时音视频**：`turn_detection` 参数决定轮次控制模式——设为 `null` 启用 Manual 模式（客户端按键控制起止），设为 `server_vad` 或 `semantic_vad` 则启用服务端 VAD 自动检测；`input_audio_buffer.commit` 和 `response.create` 仅在 Manual 模式下由客户端显式触发。

## 使用方式

- **Prompt 工程**：所有生成类任务均强依赖提示词质量。推荐采用结构化框架：背景 + 目的 + 风格 + 语气 + 受众 + 输出格式（见 [文生文Prompt指南](raw/model-user-guide/use-cases/prompt-engineering-guide.md)）；对视频任务，必须按模型支持的分镜语法精确标注时间戳与运镜指令。  
- **RAG 应用构建**：基于 LlamaIndex 的方案需先通过 `DashScopeParse` 解析文档（支持 PDF/DOC/DOCX，单文件 ≤100MB、≤1000页），再调用 `DashScopeCloudIndex.from_documents()` 创建知识库索引。  
- **实时交互接入**：  
  - WebRTC 方案需在浏览器中创建 `RTCPeerConnection`，通过 `getUserMedia` 获取媒体流，并处理 `ontrack` 回调播放远端音频；  
  - AOQ 方案需在移动端导入 `AoqClientSdk` 及 `PluginOpus` 插件，动态申请 `RECORD_AUDIO` 权限，并通过 Data 轨发送 `run-task`/`finish-task` 控制音频生命周期。  
- **高并发优化**：语音合成场景应复用对象池（如 Python 的 `dashscope>=2.0.1`、Java 的 `commons-pool2`），避免重复建连；限流应对需组合平台配置（如服务端排队等待）、客户端流控（自适应拥塞控制）与架构兜底（MQ 削峰）。

## 限制和注意事项

- **限流机制**：API 按主账号维度独立计算 RPM（每分钟请求数）、TPM（每分钟 [Token](../concepts/token.md) 数）、RPS（每秒请求数）、TPS（每秒 [Token](../concepts/token.md) 数）及 Traffic Burst（突发流量）。触发后通常 1 分钟内恢复，但需主动监控 [模型用量监控](raw/model-user-guide/model-monitoring/model-telemetry.md)。  
- **缓存策略**：显式缓存（`cache_control`）仅在 Anthropic 协议端点（如 Claude Code、Open Code）原生支持，且需确保请求中携带标记；其成本优势显著（首次写入仅增 25% 开销，命中节省 90% 成本），但对动态内容（如含时间戳的 system prompt）需关闭动态部分以提升跨会话命中率。  
- **模型生命周期**：第三方模型存在下线风险，例如 [MiMo-小米](raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md) 明确标注 `xiaomi/mimo-v2.5-pro` 将于 2026 年 10 月 21 日下线，必须迁移至 `xiaomi/mimo-v2.6-pro-ultraspeed`。  
- **地域与权限硬约束**：所有三方模型文档（如 DeepSeek、Kimi、GLM、MiniMax）均强调华北2（北京）为默认或唯一支持地域；移动端 AOQ 接入必须动态申请 `RECORD_AUDIO` 权限，且 `CAMERA` 权限仅在启用视频时才需声明——此为系统级强制要求，未满足将导致功能不可用。

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
- [语音合成高并发最佳实践](../../raw/model-user-guide/use-cases/tts-high-concurrency-best-practices.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [Ling-蚂蚁数科](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/antdigital.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
- [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
- [使用 AOQ 接入 qwen-audio-3.1-asr-flash-streaming 实现语音输入法](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/voice-input-using-aoq-access-qwen-audio-asr.md)
- [使用 AOQ 接入 qwen3.8-livetranslate-flash-realtime 实现实时语音翻译](../../raw/_short/real-time-translation-using-aoq-access-qwen-live-9b4d3056b2eade2b.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/_short/speech-synthesis-using-aoq-access-qwen-audio-3-0-43022e91dedcb0c1.md)
- [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](../../raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)
- [技术解决方案](../../raw/model-user-guide/use-cases/technical-solutions.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)


