# use cases

百炼平台提供覆盖文本、图像、视频、语音等[多模态](../concepts/multimodal.md)场景的完整AI能力，支持从基础Prompt工程、RAG应用构建到实时音视频交互的端到端落地。本文档面向开发者，系统梳理核心使用场景、模型支持、关键参数与实践约束，帮助您快速选型并规避常见陷阱。

## 支持的模型/功能

百炼支持三大类模型调用路径：  
- **原生模型**：通义千问系列（如 `qwen3.7-max`、`qwen3.5-omni-plus-realtime`）为平台主力模型，全面支持文生文、文生图、文生视频、实时音视频等全栈能力；  
- **三方直供模型**：通过统一OpenAI兼容接口接入DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun、Unisound等厂商模型，但存在地域与功能限制——例如[DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)仅支持华北2（北京）地域，且不支持联网搜索与上下文缓存；  
- **专用模型**：如 `fun-asr-realtime`（实时语音识别）、`qwen-audio-3.0-tts-flash`（语音合成）等，需通过AOQ协议调用，不兼容标准Chat Completions API。

> **注意**：多个三方模型文档存在下架时间冲突。例如[DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)与[GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)均标注`2026年10月10日`下架，而[Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)标注`2026年8月31日`下架。实际生效时间以控制台最新公告为准，建议优先选用推荐迁移目标（如`qwen3.7-plus`）。

## 关键参数

不同模态任务依赖特定参数组合：  
- **文生文**：核心为`prompt`字段，推荐使用[文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)中的结构化框架（背景/目的/风格/语气/受众/输出），避免模糊指令；  
- **文生图**：除`prompt`外，必须设置`negative_prompt`排除干扰元素，并启用`prompt_extend: true`（V2默认开启）以触发大模型智能扩写；  
- **文生视频**：需严格遵循`主体+场景+运动`基础公式或`主体描述+场景描述+运动描述+美学控制+风格化`进阶公式，其中`美学控制`包含景别、运镜等镜头语言参数；  
- **实时音视频**：`qwen3.5-omni-plus-realtime`等模型强制要求`server_vad`或`semantic_vad`模式（WebRTC）或`turn_detection: null`（AOQ Manual模式），不支持客户端手动VAD；  
- **思考模式控制**：`enable_thinking`（DeepSeek/MiMo/Stepfun）、`reasoning_effort`（Kimi/GLM）、`thinking: {"type": "enabled"}`（Unisound）等非标准参数需通过`extra_body`（Python SDK）或顶层参数（Node.js SDK）传入。

## 使用方式

- **Prompt工程**：所有文本生成任务均应优先使用[文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)中的框架设计法，对模糊需求（如“推广新产品”）进行背景、目的、风格等维度拆解；  
- **RAG应用**：基于LlamaIndex构建时，必须使用`DashScopeParse`解析器处理PDF/DOCX文件，并通过`DashScopeCloudIndex`创建知识库，不可直接使用本地向量库；  
- **缓存优化**：显式缓存仅在Anthropic协议端点（如`https://dashscope.aliyuncs.com/apps/anthropic`）生效，需在system [prompt](prompt.md)中添加`cache_control`标记，详见[显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)；  
- **限流应对**：当遇到`429`错误时，优先尝试平台层`服务端排队等待`（添加`X-DashScope-Queue-Enable: true`请求头），而非客户端重试——该方案在突发流量场景下恢复最快；  
- **三方模型接入**：必须使用业务空间专属域名（如`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），禁用通用域名`https://dashscope.aliyuncs.com`，否则可能触发鉴权失败或限流异常。

## 限制和注意事项

- **地域锁定**：所有三方直供模型（DeepSeek/Kimi/GLM/MiniMax等）及实时音视频服务（WebRTC/AOQ）均**仅支持华北2（北京）地域**，跨地域调用将返回`404`或`403`；  
- **[Token](../concepts/token.md)计费差异**：Prompt优化工具、显式缓存首次写入、AOQ连接建立等操作均消耗额外[Token](../concepts/token.md)，需纳入成本预估；  
- **文件处理上限**：`DashScopeParse`解析器单文件限制为100MB且页数≤1000，超限文件需预分割；  
- **视频生成约束**：Vidu等模型对提示词句式敏感，禁止使用“多个主体”“复杂文学修辞”，应采用口语化、分句式描述（如“一只柯基幼犬在大泳池里游泳”优于“泳池中跃动着活泼的柯基幼犬身影”）；  
- **安全红线**：训练自定义模型时，输入数据必须完成脱敏处理（移除PII信息），否则模型部署将被平台自动拦截。

## 来源文档

- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
- [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [使用 AOQ 接入 qwen3.5-omni-plus-realtime 实现按键语音对话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/use-aoq-to-access-qwen3-5-omni-plus-realtime-to-realize-key-voice-dialogue.md)
- [通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [使用 AOQ 接入 qwen-audio-3.0-realtime-plus 实现实时语音对话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/real-time-voice-conversation-using-aoq-access-qwen-audio-3-0-realtime-plus.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/speech-synthesis-using-aoq-access-qwen-audio-3-0-tts-flash.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/real-time-speech-recognition-using-aoq-access-fun-asr-realtime.md)


