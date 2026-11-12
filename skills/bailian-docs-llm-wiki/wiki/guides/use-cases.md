# use cases

百炼平台提供覆盖文本、图像、视频、语音等多模态任务的完整用例体系，支持从基础 Prompt 工程、RAG 应用构建，到高并发实时音视频交互、三方模型集成等生产级场景。所有用例均基于统一 API 体系设计，兼顾易用性与工程可控性。

## 支持的模型/功能

百炼支持三大类核心能力：  
- **文生类模型**：包括通义千问系列（Qwen）、DeepSeek、Kimi、GLM、MiniMax、Stepfun、Ling、MiMo、Unisound 等数十种主流大语言模型，全部通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 DashScope 原生 API 接入；[DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md) 和 [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md) 等文档明确区分了不同供应商在思考模式、联网搜索、缓存支持等方面的差异化能力。  
- **多模态生成模型**：万相（WanX）系列覆盖文生图（V1/V2）、文生视频（Wan3.0）、图生视频、参考生视频等；Vidu 视频生成也提供独立 Prompt 指南；[文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md) 和 [视频生成Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md) 分别定义了结构化提示词公式与要素层级。  
- **实时交互与专业工具链**：qwen3.8-omni-flash-realtime、qwen-audio-3.1-asr-flash-streaming、qwen3.8-livetranslate-flash-realtime 等 Realtime 模型，配合 AOQ 或 WebRTC 协议实现毫秒级语音/视频流处理；同时支持 RAG（如基于 LlamaIndex 构建）、自定义模型调优、显式缓存、限流应对等企业级能力。

> **注意**：部分历史图像/视频模型（如 `wanx-style-repaint-v1`、`shoemodel-v1`）已进入免费体验阶段且不支持付费调用，官方推荐迁移至 [图像编辑-万相2.1](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md) 或 [图像编辑-千问](../../raw/model-user-guide/model-experience/image-and-video-generation/image-model/image-edit-guide/qwen-image-edit-guide.md) 等新能力。

## 关键参数

不同任务类型的关键参数存在显著差异，需严格按模型文档配置：  
- **文本生成类**：通用参数包括 `model`、`messages`、`stream`；思考模式相关参数因模型而异——`enable_thinking`（DeepSeek、MiMo、Ling）、`reasoning_effort`（Kimi、GLM、Unisound）、`thinking`（Unisound）均为非 OpenAI 标准字段，必须通过 `extra_body`（Python SDK）或顶层参数（Node.js SDK）传入；[Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md) 明确指出 `reasoning_effort: "max"` 控制思考强度。  
- **图像/视频生成类**：`prompt`（正向提示词）和 `negative_prompt`（反向提示词）为文生图 V2 必填项；`prompt_extend` 控制是否启用大模型智能改写；万相3.0 支持更细粒度的 `分镜 N（起-止秒）`、`台词`、`音效/BGM`、`负向清单` 等复合参数。  
- **实时音视频类**：AOQ 场景下需关注 `turn_detection`（`null` 表示 Manual 模式，`server_vad` 表示服务端 VAD 模式）、`input_audio_buffer.append/commit`、`response.create` 等协议事件控制参数；WebRTC 场景则依赖 `RTCPeerConnection` 配置与媒体流约束。

## 使用方式

标准调用流程为：开通服务 → 获取 API Key → 配置环境/SDK → 构造请求 → 处理响应。具体实践路径如下：  
- **Prompt 工程**：优先使用 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md) 提出的「背景-目的-风格」框架，并结合平台内置的 Prompt 一键优化工具扩写；文生图/视频需严格遵循对应公式（如「主体+场景+运动」），避免模糊术语。  
- **RAG 应用**：基于 LlamaIndex 的方案需先通过 `DashScopeParse` 解析文档，再调用 `DashScopeCloudIndex.from_documents` 创建知识库索引，全程依赖业务空间 ID 隔离数据域。  
- **实时交互**：WebRTC 方案适用于浏览器低延迟场景，需处理 SDP 交换与媒体流绑定；AOQ 方案适用于移动端，需集成 Opus 插件并按平台规范声明权限（如 Android 的 `RECORD_AUDIO`）。  
- **三方模型**：所有第三方模型（DeepSeek、Kimi、GLM 等）均需在华北2（北京）地域开通并使用专属业务空间域名（`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），跨地域调用将失败。

## 限制和注意事项

- **地域与模型绑定**：绝大多数三方模型（DeepSeek、Kimi、GLM、MiMo、Stepfun、Unisound、Ling）仅支持华北2（北京）地域，且必须使用该地域的 API Key 和业务空间 ID；[GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md) 特别强调新域名 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com` 提供更高稳定性，建议迁移。  
- **限流策略**：API 按主账号维度对 RPM/TPM、RPS/TPS、Traffic Burst 三重限流；突发流量应优先启用「服务端排队等待」（加 `X-DashScope-Queue-Enable: true` 请求头），而非简单重试。  
- **缓存与成本**：显式缓存（`cache_control`）可降低 90% 后续调用成本，但仅 Anthropic 协议接入的工具（如 Claude Code、Open Code）原生支持；普通 HTTP 调用需自行管理缓存标记。  
- **免费额度风险**：`wanx-virtualmodel`、`image-instance-segmentation`、`shoemodel-v1` 等历史模型已停售，免费额度用尽后即不可用，无降级路径，务必提前规划迁移。

## 来源文档

- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [视频生成Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [语音合成高并发最佳实践](../../raw/model-user-guide/use-cases/tts-high-concurrency-best-practices.md)
- [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [Ling-蚂蚁数科](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/antdigital.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
- [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [使用 AOQ 接入 qwen-audio-3.1-asr-flash-streaming 实现语音输入法](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/voice-input-using-aoq-access-qwen-audio-asr.md)
- [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
- [使用 AOQ 接入 qwen3.8-livetranslate-flash-realtime 实现实时语音翻译](../../raw/_short/real-time-translation-using-aoq-access-qwen-live-9b4d3056b2eade2b.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/_short/speech-synthesis-using-aoq-access-qwen-audio-3-0-43022e91dedcb0c1.md)
- [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](../../raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)
- [技术解决方案](../../raw/model-user-guide/use-cases/technical-solutions.md)
- [历史模型指南](../../raw/model-user-guide/use-cases/legacy-resources.md)
- [图像生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation.md)
- [通用图像编辑-万相2.1](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md)
- [人像风格重绘](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/style-repaint.md)
- [虚拟模特生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/virtual-model-generation.md)
- [人物实例分割](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/image-instance-segmentation.md)
- [鞋靴模特](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/shoes-and-boots-model.md)
- [创意海报生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/creative-poster-generation-overview.md)
- [图像局部重绘](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/vary-region.md)
- [图像擦除补全](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/image-erasure-and-completion.md)
- [涂鸦作画](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/sketch-to-image.md)
- [视频生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation.md)
- [视频编辑2.1](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/wan-vace-guide.md)
- [图生视频-基于首尾帧](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-first-and-last-frames-guide.md)
- [万相-图生视频-基于首帧](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-guide.md)


