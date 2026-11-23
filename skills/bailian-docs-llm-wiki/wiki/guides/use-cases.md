# use cases

百炼平台提供覆盖文本、图像、视频、语音等多模态场景的丰富用例，支持从基础 Prompt 工程、RAG 构建、模型微调到实时音视频交互的全链路开发。所有用例均基于统一 API 体系设计，开发者可按需组合使用，快速落地业务需求。

## 支持的模型/功能

百炼支持三类核心能力模型：

- **文生文（LLM）**：包括 Qwen 系列（如 `qwen3.7-max`）、DeepSeek（如 `deepseek-v4.1-flash`）、Kimi（如 `kimi/kimi-k3.1-pro`）、GLM（如 `ZHIPU/GLM-5.3`）、MiniMax（如 `MiniMax/MiniMax-M2.7`）、Stepfun（如 `stepfun/step-3.7-flash`）、MiMo（如 `xiaomi/mimo-v2.6-pro-ultraspeed`）、Ling（如 `antdigital/Ling-3.1-flash`）、Unisound（如 `unisound/unisound-u2`）等主流三方模型，均通过 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)或 DashScope 原生 API 调用。[三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md) 提供了完整接入路径。

- **文生图/图生图**：万相系列模型（如 `wanx-text-to-image-v2`、`wanx-style-repaint-v1`、`wanx-x-painting`），支持提示词驱动的图像生成、风格重绘、局部编辑、擦除补全等。[文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md) 给出了结构化提示词公式与词典。

- **文生视频/图生视频/多模态视频**：万相 3.0（`wan3-video-generation`）、Vidu（`vidu-video-generation`）及历史模型（如 `wanx-video-generation`），支持单镜头/多镜头叙事、首帧/首尾帧生成、参考生视频（主体/运动/风格/音频等多维参考）等复杂任务。[万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md) 和 [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md) 分别提供了面向不同引擎的提示词框架。

- **实时音视频**：Qwen-Omni-Realtime、Qwen-Audio-Realtime-Plus、Fun-ASR-Realtime、Qwen-LiveTranslate-Flash-Realtime、Qwen-Audio-TTS-Flash 等模型，配合 WebRTC 或 AOQ SDK，实现低延迟语音对话、实时翻译、语音输入法、语音合成等端侧交互能力。

> **注意**：文档 36–43 中列出的 `wanx-style-repaint-v1`、`shoemodel-v1`、`wanx-virtualmodel`、`image-erase-completion`、`wanx-x-painting` 等模型均标注为“仅提供免费体验，额度用完后不可调用且不支持付费”，并明确推荐迁移到 [图像编辑-万相2.1](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md) 或 [图像编辑-千问](../../raw/model-user-guide/model-experience/image-and-video-generation/image-model/image-edit-guide/qwen-image-edit-guide.md)。该迁移建议具有强制性，旧模型已进入 EOL（End-of-Life）状态。

## 关键参数

不同模态模型的关键参数存在显著差异，需严格匹配：

- **文生文**：通用参数为 `messages`（含 `role`/`content`），部分模型支持扩展参数：
  - `enable_thinking`（非 OpenAI 标准）：控制思考模式开关，用于 DeepSeek、Kimi、MiMo、Ling、Unisound 等模型（见 [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)、[Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md) 等文档）。
  - `reasoning_effort`（OpenAI 标准）：控制思考深度（`low`/`medium`/`high`/`max`/`xhigh`），影响 `reasoning_content` 输出粒度。
  - `stream` + `stream_options.include_usage`：启用[流式输出](../concepts/streaming.md)并返回 Token 消耗。

- **文生图**：核心参数为 `prompt`（正向提示词）和 `negative_prompt`（反向提示词）。万相 V2 额外支持 `prompt_extend: true` 启用大模型智能改写。

- **文生视频**：基础参数为 `prompt`；万相 3.0 支持结构化字段如 `reference_images`、`audio_references`、分镜描述（`分镜N（起-止秒）：...`）；Vidu 支持 `dynamic_control`（大/中/小动态）、运镜关键词（`推`/`拉`/`固定`）、风格关键词（`宫崎骏风格`/`水墨风格`）等。

- **实时音视频（AOQ）**：关键参数在连接配置与事件协议中体现：
  - `turn_detection`：设为 `null` 表示 Manual 模式（按键控制），设为 `{"type": "server_vad"}` 表示服务端 VAD 自动检测。
  - `input_audio_buffer.append` / `commit`：Manual 模式下必须显式调用 `commit` 提交音频。
  - `response.create`：Manual 模式下必须显式触发模型回复。

## 使用方式

- **API 直接调用**：所有模型均提供 HTTP API 接口，需配置 `Authorization: Bearer ${DASHSCOPE_API_KEY}` 及地域专属 endpoint（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）。异步任务（如图像/视频生成）需轮询 `task_id` 查询结果。

- **SDK 集成**：
  - 文生文/文生图：推荐使用 `dashscope` Python SDK（v2.0.1+）或 OpenAI Python SDK（v1.0+）。
  - RAG 应用：基于 LlamaIndex，使用 `llama-index-llms-dashscope` 和 `llama-index-indices-managed-dashscope` 包，通过 `DashScopeCloudIndex` 创建知识库 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。
  - 实时音视频：WebRTC 场景使用浏览器原生 API；移动端使用 AOQ Client SDK（Android/iOS/HarmonyOS），需导入 Opus 插件并声明权限。

- **工具辅助**：
  - Prompt 优化：控制台提供 [Prompt 一键优化工具](https://bailian.console.aliyun.com/flow-agent/component-manage/prompt)，支持自动扩写与细节添加。
  - 视频提示词调试：万相 3.0 提供 `/wan3-pe` Skill 命令行调试工具，支持快速迭代提示词。

## 限制和注意事项

- **地域与 API Key 绑定**：绝大多数三方模型（DeepSeek、Kimi、GLM、MiniMax、Stepfun、MiMo、Unisound、Ling）及 Legacy 图像/视频模型**仅支持华北2（北京）地域**，且必须使用该地域的 API Key 和业务空间 ID。跨地域调用将失败。

- **限流策略**：API 按主账号维度、模型独立计算 RPM/TPM、RPS/TPS 及 Traffic Burst 三重限流。突发流量易触发 `429` 错误，推荐优先启用 [服务端排队等待](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)（加 `X-DashScope-Queue-Enable: enable` 请求头）而非简单重试。

- **缓存机制**：显式缓存（`cache_control`）仅对 Anthropic 协议兼容模型（如 Claude Code、Open Code）原生支持，需在 system prompt 或 user message 中注入标记。普通 OpenAI 兼容调用不支持此特性。

- **免费额度与计费**：所有 Legacy 图像/视频模型（文档 37–43）均已停止计费支持，仅保留有限免费额度；新项目应使用万相 2.1 或千问图像编辑替代。文生文模型按 Token 计费，显式缓存首次写入产生 25% 额外开销，但命中后可节省 90% 成本。

- **安全与合规**：API Key 必须保存在服务端（AppServer），**严禁硬编码于客户端代码或提交至代码仓库**（见 [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md) 等文档多次强调）。

## 来源文档

- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)
- [视频生成Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [Ling-蚂蚁数科](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/antdigital.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
- [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
- [使用 AOQ 接入 qwen-audio-3.1-asr-flash-streaming 实现语音输入法](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/voice-input-using-aoq-access-qwen-audio-asr.md)
- [使用 AOQ 接入 qwen3.8-livetranslate-flash-realtime 实现实时语音翻译](../../raw/_short/real-time-translation-using-aoq-access-qwen-live-9b4d3056b2eade2b.md)
- [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](../../raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)
- [技术解决方案](../../raw/model-user-guide/use-cases/technical-solutions.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/_short/speech-synthesis-using-aoq-access-qwen-audio-3-0-43022e91dedcb0c1.md)
- [历史模型指南](../../raw/model-user-guide/use-cases/legacy-resources.md)
- [图像生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation.md)
- [通用图像编辑-万相2.1](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md)
- [人像风格重绘](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/style-repaint.md)
- [鞋靴模特](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/shoes-and-boots-model.md)
- [虚拟模特生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/virtual-model-generation.md)
- [图像擦除补全](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/image-erasure-and-completion.md)
- [图像局部重绘](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/vary-region.md)
- [人物实例分割](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/image-instance-segmentation.md)
- [创意海报生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/creative-poster-generation-overview.md)
- [视频生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation.md)
- [涂鸦作画](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/sketch-to-image.md)
- [视频编辑2.1](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/wan-vace-guide.md)
- [万相-图生视频-基于首帧](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-guide.md)
- [图生视频-基于首尾帧](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-first-and-last-frames-guide.md)


