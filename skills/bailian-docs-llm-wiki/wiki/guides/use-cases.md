# use cases

百炼平台提供覆盖文本、图像、视频、语音等多模态场景的完整 AI 应用能力，支持从 Prompt 工程、RAG 构建、模型微调到实时音视频交互的端到端开发流程。开发者可根据业务需求选择预置能力或组合调用，快速落地生产级应用。

## 支持的模型/功能

百炼支持三大类核心能力：**文生文（LLM）**、**文生图/文生视频（多模态生成）** 和 **实时音视频（Realtime/AOQ）**。

- **文生文**：除百炼自研 Qwen 系列外，还集成 DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun、Unisound 等主流三方模型，均通过 [OpenAI 兼容接口](../concepts/openai-compatibility.md)或 DashScope SDK 调用 [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)。所有模型均支持 `enable_thinking` 或 `reasoning_effort` 参数控制思考模式输出。
- **文生图/文生视频**：万相（WanXiang）系列模型覆盖 V1/V2/V3.0 及 Vidu，分别对应不同提示词结构与参数体系。万相3.0 支持多模态参考（图/视频/音频/网页等）与分镜级控制 [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)；Vidu 则强调风格化关键词与运镜术语的精准匹配 [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)。
- **实时音视频**：提供 WebRTC 与 AOQ 两种接入路径。WebRTC 适用于浏览器低延迟场景（如多模态交互套件），AOQ 则面向移动端和嵌入式设备，支持 Manual/VAD 模式切换、按键语音、语音输入法、TTS 合成等多种子场景 [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)。

> **注意**：文档中关于 `enable_thinking` 参数的默认行为存在不一致描述。例如 [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md) 明确说明“控制支持该参数的模型是否开启思考模式”，而 [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md) 则声明“mimo-v2.5-pro 默认开启思考模式”。实际调用时应以具体模型文档为准，并在请求中显式传参避免歧义。

## 关键参数

不同能力域的关键参数差异显著，需按模型类型区分：

- **文生文通用参数**：`model`（必填）、`messages`（ChatML 格式）、`stream`（流式开关）、`stream_options.include_usage`（流式返回 Token）。思考模式相关参数（如 `enable_thinking`, `reasoning_effort`, `thinking`）均为非 OpenAI 标准字段，须通过 `extra_body`（Python SDK）或顶层参数（Node.js SDK）传入。
- **文生图参数**：`prompt`（正向提示词）、`negative_prompt`（反向提示词）、`prompt_extend`（V2 默认 `true`，启用大模型智能改写）。
- **文生视频参数**：万相3.0 使用结构化分镜语法，关键字段包括 `分镜 N（起-止秒）`、`台词`、`音效 / BGM`、`负向清单`；Vidu 强依赖运镜关键词（如 `镜头推`、`固定镜头`）与风格词（如 `宫崎骏风格`、`水墨风格`）。
- **实时音视频参数**：WebRTC 场景下由服务端控制 VAD 模式（`server_vad` 或 `semantic_vad`），Manual 模式需客户端显式调用 `input_audio_buffer.commit` 和 `response.create`；AOQ 场景下通过 `turn_detection: null` 启用 Manual 模式，并依赖 `run-task`/`continue-task` 事件协议。

## 使用方式

- **Prompt 工程**：推荐采用标准化框架（背景+目的+风格+语气+受众+输出），并优先使用百炼内置的 [Prompt一键优化工具](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md) 进行自动扩写。文生图/视频需严格遵循对应公式（如基础公式：主体+场景+风格；进阶公式：主体描述+场景描述+镜头语言+氛围词+细节修饰）。
- **RAG 应用**：基于 LlamaIndex，使用 `DashScopeParse` 解析文档（支持 PDF/DOCX，单文件 ≤100MB），再通过 `DashScopeCloudIndex` 创建知识库索引 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。
- **模型微调与部署**：通过控制台“模型调优→模型部署→模型评测”三步流程完成，训练数据需为 ChatML 格式 JSONL，建议 ≥500 条 [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)。
- **限流与缓存**：高频调用场景应启用显式缓存（`cache_control` 字段），可降低 90% 成本；突发流量需结合平台排队（加 `X-DashScope-Queue-Enable: true` 请求头）、客户端令牌桶及架构层 MQ 削峰 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)、[显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)。

## 限制和注意事项

- **地域与接入点约束**：绝大多数三方模型（DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun、Unisound）仅支持华北2（北京）地域，且必须使用业务空间专属域名 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，不可混用 `https://dashscope.aliyuncs.com` [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)。
- **文件与内容限制**：`DashScopeParse` 文档解析器要求单个文件 ≤100MB 且 ≤1000 页；万相文生图 V2 的 `prompt` 长度上限为 768 字符；实时音视频场景中，WebRTC 受 CORS 限制，SDP 交换需后端代理，不可浏览器直连。
- **安全与合规**：API Key 必须保存在服务端（AppServer），严禁硬编码至客户端代码或提交至仓库；所有用户上传数据需经脱敏处理，移除 PII 信息 [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)。
- **计费影响项**：Prompt 优化工具、显式缓存首次写入、思考模式推理、长上下文（>128K）均会产生额外 Token 消耗，需在成本评估中纳入 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)。

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
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
- [使用 AOQ 接入 qwen-audio-3.1-asr-flash-streaming 实现语音输入法](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/voice-input-using-aoq-access-qwen-audio-asr.md)
- [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](../../raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/_short/speech-synthesis-using-aoq-access-qwen-audio-3-0-43022e91dedcb0c1.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)
- [技术解决方案](../../raw/model-user-guide/use-cases/technical-solutions.md)


