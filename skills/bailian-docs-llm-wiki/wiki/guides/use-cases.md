# use cases

阿里云百炼平台提供覆盖文本、多模态、语音、视频等全模态的 AI 应用场景支持，面向开发者提供开箱即用的解决方案与灵活可扩展的底层能力。核心价值在于将复杂模型能力封装为可组合、可编排、可部署的标准化服务，降低从原型验证到生产落地的技术门槛。所有方案均基于真实业务痛点设计，并已在电商客服、教育辅学、深度研究、影视创作等垂直领域完成闭环验证。

## 支持的模型/功能

百炼支持两类模型调用路径：**平台原生模型**（如 `qwen3.7-plus`、`qwen3.5-omni-plus-realtime`）和**三方直供模型**（如 DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun、Unisound 等）。所有模型均通过统一 API 接口（OpenAI 兼容或 DashScope 原生协议）接入，支持流式响应、思考模式（`enable_thinking`/`reasoning_effort`）、多模态输入（文本+图像+视频）及实时音视频交互。

关键功能矩阵如下：
- **智能体与工作流**：支持 RAG（[检索增强生成](../concepts/rag.md)）、自主决策 Agent、可视化对话流编排，典型应用见 [高效搭建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md)。
- **多模态理解与生成**：覆盖文生文（Prompt 工程）、文生图（万相 V1/V2）、文生视频/图生视频（万相 V2.6+）、文档转视频（LLM 驱动），并支持 Vidu 专用 Prompt 词典与运镜控制。
- **实时语音交互**：提供 WebRTC 浏览器端低延迟通话（`qwen3.5-omni-plus-realtime`）、AOQ 移动端 SDK（支持 Manual/VAD 模式）、ASR（`fun-asr-realtime`）与 TTS（`qwen-audio-3.0-tts-flash`）全链路能力。
- **专业领域增强**：包括 LlamaIndex 集成 RAG、Qwen-Deep-Research 深度分析引擎、AI 解题批改（`qwen3-vl-plus`）、自定义模型微调与评测。

> **注意**：部分三方模型（如 `deepseek-v3.*`、`kimi-k2-instruct`、`MiniMax-M2.1`、`glm-4.*`）已明确标注下架时间（2026 年 7–10 月），文档中推荐迁移至 `qwen3.7-plus` 等 Qwen 系列新模型，实际开发中应以控制台最新可用模型列表为准。

## 关键参数

不同任务类型对应差异化参数体系，需严格按模型文档配置：

- **文本生成类**（Chat Completion）：  
  `model`（必填，如 `"qwen3.7-max"`）、`messages`（标准 ChatML 格式）、`stream`（布尔值）、`extra_body`（非标参数载体，用于 `enable_thinking`、`reasoning_effort`、`preserve_thinking` 等）。

- **文生图类**（万相）：  
  `prompt`（正向提示词）、`negative_prompt`（反向提示词）、`parameters.prompt_extend`（是否启用大模型智能扩写，默认 `true`）。

- **文生视频类**（万相）：  
  基础公式为 `主体 + 场景 + 运动`；进阶需补充 `美学控制`（镜头/运镜）与 `风格化`；图生视频则聚焦 `运动 + 运镜`；声音控制需显式声明 `人声/音效/BGM` 描述。

- **实时语音类**（AOQ/WebRTC）：  
  `turn_detection`（`null` 表 Manual 模式，`{"type": "server_vad"}` 表 VAD 模式）、`input_audio_buffer.append/commit`（Manual 模式必需）、`response.create`（触发回复）。

- **缓存与限流**：  
  显式缓存需在请求中注入 `cache_control` 字段（如 `{"type": "ephemeral"}`）；限流应对需关注 `RPM/TPM`（分钟级）、`RPS/TPS`（瞬时）及 `Traffic Burst`（增速）三重维度。

## 使用方式

### 1. 快速启动
- 所有方案均提供 **15–30 分钟快速部署路径**，依赖函数计算（FC）+ 百炼模型服务组合，支持一键部署与免费试用额度（如 [深度研究](../../raw/model-user-guide/use-cases/deep-research.md) 方案成本约 6 元）。
- 开发者可直接复用官方代码示例（Python/Node.js），仅需替换 `base_url`（含 `{WorkspaceId}`）、`DASHSCOPE_API_KEY` 及 `model` 名称。

### 2. 集成范式
- **RAG 应用**：通过 `llama-index-indices-managed-dashscope` SDK 封装知识库创建、检索与问答流程，无需自行管理向量数据库。
- **Agent 工作流**：使用百炼控制台可视化编排节点（LLM 调用、工具调用、条件分支），或通过 Flow SDK 编程式构建。
- **实时交互**：WebRTC 方案需浏览器端处理 SDP 交换（Demo 中依赖 curl 代理）；AOQ 方案必须由业务 AppServer 代理 Token 鉴权，禁止客户端硬编码 API Key。

### 3. 提示工程
- 文生文：采用 [Prompt 框架](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)，结构化定义 `背景/目的/风格/语气/受众/输出` 六要素。
- 文生图/视频：遵循分层公式（基础→进阶→多镜头），善用 [Vidu 视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md) 中的运镜与氛围词典提升可控性。

## 限制和注意事项

- **地域与模型绑定**：绝大多数三方模型（DeepSeek、Kimi、GLM、MiniMax 等）**仅在华北2（北京）地域可用**，且需使用专属业务空间域名 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，跨地域调用将失败。
- **API Key 安全**：所有客户端 SDK 示例均要求 `DASHSCOPE_API_KEY` 通过环境变量注入，**严禁硬编码于前端代码或提交至 Git 仓库**；AOQ 方案强制要求业务后端代理鉴权。
- **资源约束**：
  - 文件解析：`DashScopeParse` 支持单文件 ≤100MB、≤1000 页（[基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)）。
  - 实时语音：WebRTC 模式下视频发送帧率需降至 2fps（Canvas 降帧），音频必须启用回声消除（内置）。
- **缓存与限流协同**：显式缓存（`cache_control`）可降低 90% 成本，但仅对完全相同的 `prompt` + `model` + `parameters` 组合生效；限流触发时，单纯重试无效，须结合 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md) 中的排队、批处理或架构兜底策略。

## 来源文档

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
- [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-multimodal-dialog.md)
- [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-omni-realtime.md)
- [通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-aoq-omni-realtime.md)
- [使用 AOQ 接入 qwen3.5-omni-plus-realtime 实现按键语音对话](../../raw/model-user-guide/use-cases/use-aoq-to-access-qwen3-5-omni-plus-realtime-to-realize-key-voice-dialogue.md)
- [使用 AOQ 接入 qwen-audio-3.0-realtime-plus 实现实时语音对话](../../raw/model-user-guide/use-cases/real-time-voice-conversation-using-aoq-access-qwen-audio-3-0-realtime-plus.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/model-user-guide/use-cases/speech-synthesis-using-aoq-access-qwen-audio-3-0-tts-flash.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/model-user-guide/use-cases/real-time-speech-recognition-using-aoq-access-fun-asr-realtime.md)
- [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)


