# use cases

百炼平台的 use cases 文档系统性地覆盖了从文本、图像、视频生成到实时音视频交互、RAG 构建、模型调优等核心应用场景。本文档面向开发者，聚焦可落地的技术实践，整合了提示词工程、API 调用规范、参数配置、流控策略及关键限制，帮助快速选型并规避常见陷阱。

## 支持的模型/功能

百炼支持多模态全栈能力，涵盖文生文、文生图、文生视频、图生视频、参考生视频、实时语音对话、语音识别与合成、RAG 应用构建、自定义模型训练及三方模型集成。

- **文生文**：提供通用大模型（如 Qwen 系列）及深度思考模型（如 `kimi/kimi-k3.1-pro`、`ZHIPU/GLM-5.3`、`xiaomi/mimo-v2.6-pro-ultraspeed`），均支持 `enable_thinking` 或 `reasoning_effort` 参数控制推理深度 [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)。
- **文生图与图像编辑**：主力模型为万相系列，包括 `万相-文生图V2`、`万相-通用图像编辑模型（wanx-image-edit）` 及历史模型如 `wanx-style-repaint-v1`（人像风格重绘）和 `wanx-x-painting`（图像局部重绘）[文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)。
- **视频生成**：支持 `万相3.0`、`Vidu` 及 legacy 模型，任务类型覆盖文生视频、首帧/首尾帧生视频、多模态参考生视频（主体/运动/风格/音频/白模/分镜/关键帧/网页）[万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)。
- **实时音视频**：通过 WebRTC 或 AOQ SDK 接入 `qwen3.8-omni-flash-realtime`（音视频通话）、`qwen-audio-3.1-asr-flash-streaming`（语音输入法）、`qwen3.8-livetranslate-flash-realtime`（实时翻译）等模型 [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)。
- **RAG 与知识库**：支持基于 LlamaIndex 构建 RAG 应用，使用 `DashScopeParse` 解析器处理 PDF/DOCX 等文档，并上传至百炼知识库服务 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。

> **注意**：部分历史图像模型（如 `shoemodel-v1`、`image-instance-segmentation`、`image-erase-completion`、`wanx-poster-generation-v1`）当前仅提供免费体验，额度用完后不可调用且不支持付费，官方明确推荐迁移到 `wanx-image-edit` 或 `text-to-image` 等新模型 [图像擦除补全](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/image-erasure-and-completion.md)。

## 关键参数

不同模态模型的关键参数设计高度结构化，需严格遵循文档约定：

- **文生图**：核心参数为 `prompt`（正向描述）与 `negative_prompt`（反向排除），V2 版本额外支持 `prompt_extend: true` 启用大模型智能改写 [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)。
- **视频生成**：`prompt` 需按“主体+场景+运动”基础公式组织；万相3.0 还支持 `task_type` 显式指定任务（如 `text_to_video`、`image_to_video_by_first_and_last_frame`）；Vidu 模型则依赖关键词触发运镜（如 `镜头向左移动`）或动态强度（如 `大动态`）[Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)。
- **深度思考模型**：`enable_thinking`（非 OpenAI 标准参数，需通过 `extra_body` 传入）或 `reasoning_effort`（OpenAI 标准参数）控制是否输出推理过程及强度等级 [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)。
- **实时语音模型**：`turn_detection` 参数决定轮次控制模式——设为 `server_vad` 或 `semantic_vad` 启用服务端自动检测，设为 `null` 则进入 Manual 模式由客户端显式提交音频与触发回复 [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)。
- **显式缓存**：通过 `cache_control` 字段（如 `{"type": "ephemeral"}`）在请求中声明缓存意图，适用于高频复用 Prompt 的 Agent 场景 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)。

## 使用方式

- **API 调用**：统一采用 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 DashScope 原生 API。OpenAI 方式需配置 `base_url` 为地域专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），并确保 `model` 字段填写完整模型 ID（如 `kimi/kimi-k3.1-pro`）；DashScope 方式则使用 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1` [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)。
- **SDK 集成**：Python 开发者推荐使用 `dashscope` 或 `openai` SDK；移动端需导入 AOQ Client SDK 及 Opus 插件，并在 `AndroidManifest.xml` 或 `Info.plist` 中声明必要权限（如 `RECORD_AUDIO`、`CAMERA`）[通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)。
- **Prompt 工程**：文生文推荐使用 Prompt 框架（角色+任务+约束+示例）；文生图/视频必须遵循结构化公式（如“主体+场景+风格”或“主体+场景+运动”），避免模糊术语与复杂句式 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)。
- **RAG 构建**：使用 `DashScopeParse` 解析器加载本地文件或文件夹，再通过 `SimpleDirectoryReader` 提取内容，最终上传至百炼知识库 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。

## 限制和注意事项

- **地域与认证强绑定**：绝大多数三方模型（DeepSeek、Kimi、GLM、MiniMax、MiMo、Unisound、Ling）及历史图像模型仅支持华北2（北京）地域，且必须使用该地域的 API Key 和业务空间 ID [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)。
- **限流维度双重约束**：API 同时受 RPM/TPM（分钟级）与 RPS/TPS（瞬时）限制，突发流量（Traffic Burst）会触发动态增速限制。单纯重试无效，需结合服务端排队、Batch API 或客户端自适应拥塞控制 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。
- **输入格式硬性要求**：图像类模型对输入有严格限制——`shoemodel-v1` 要求模特图与鞋靴图长宽比在 `[2:3, 3:2]` 内；`image-instance-segmentation` 要求单边分辨率在 `512–4096`；所有 URL 不得含中文字符 [鞋靴模特](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/shoes-and-boots-model.md)。
- **模型生命周期风险**：`xiaomi/mimo-v2.5-pro` 将于 2026 年 10 月 21 日下线，必须提前迁移至 `xiaomi/mimo-v2.6-pro-ultraspeed`；历史图像模型普遍标注“仅免费体验”，无后续付费路径，应尽快评估替代方案 [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)。

## 来源文档

- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [视频生成Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)
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
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [Ling-蚂蚁数科](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/antdigital.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
- [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
- [使用 AOQ 接入 qwen-audio-3.1-asr-flash-streaming 实现语音输入法](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/voice-input-using-aoq-access-qwen-audio-asr.md)
- [使用 AOQ 接入 qwen3.8-livetranslate-flash-realtime 实现实时语音翻译](../../raw/_short/real-time-translation-using-aoq-access-qwen-live-9b4d3056b2eade2b.md)
- [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](../../raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/_short/speech-synthesis-using-aoq-access-qwen-audio-3-0-43022e91dedcb0c1.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)
- [技术解决方案](../../raw/model-user-guide/use-cases/technical-solutions.md)
- [历史模型指南](../../raw/model-user-guide/use-cases/legacy-resources.md)
- [图像生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation.md)
- [通用图像编辑-万相2.1](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md)
- [人像风格重绘](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/style-repaint.md)
- [鞋靴模特](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/shoes-and-boots-model.md)
- [人物实例分割](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/image-instance-segmentation.md)
- [图像擦除补全](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/image-erasure-and-completion.md)
- [图像局部重绘](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/vary-region.md)
- [创意海报生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/creative-poster-generation-overview.md)
- [涂鸦作画](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/sketch-to-image.md)
- [视频生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation.md)
- [视频编辑2.1](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/wan-vace-guide.md)
- [图生视频-基于首尾帧](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-first-and-last-frames-guide.md)
- [万相-图生视频-基于首帧](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-guide.md)
- [虚拟模特生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/virtual-model-generation.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)


