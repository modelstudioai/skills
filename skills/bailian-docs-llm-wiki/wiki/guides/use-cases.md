# use cases

百炼平台的 use cases 覆盖多模态生成、RAG 构建、实时音视频交互、模型调优与三方集成等核心场景。本文档面向开发者，结构化梳理各用例的技术要点、参数规范与实践约束，聚焦可落地的工程细节，避免概念性描述。

## 支持的模型/功能

百炼提供两类主流能力：**原生模型服务**（如万相文生图/视频、Qwen-Omni-Realtime）和**三方模型接入**（如 DeepSeek、Kimi、GLM 等）。  
- **图像生成**：支持 `wanx-text-to-image-v2`（文生图V2）、`wanx-style-repaint-v1`（人像风格重绘）、`wanx-x-painting`（图像局部重绘）等；其中万相系列模型统一采用 `prompt`/`negative_prompt` 参数，V2 版本额外支持 `prompt_extend: true` 启用大模型智能改写 [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)。  
- **视频生成**：覆盖文生视频、图生视频、参考生视频等任务类型，万相3.0 支持完整提示词公式（含分镜、台词、音效、负向清单），而 Vidu 模型则强调“主体/场景+场景描述+环境描述+艺术风格/媒介”的初阶结构 [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)。  
- **实时音视频**：通过 WebRTC 或 AOQ 协议接入 `qwen3.8-omni-flash-realtime`、`qwen-audio-3.1-asr-flash-streaming` 等模型，支持 VAD 自动轮次检测或 Manual 按键控制模式 [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)。  
- **三方模型**：DeepSeek、Kimi、GLM、MiniMax 等均通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)调用，但参数行为存在差异：例如 `enable_thinking` 在 DeepSeek（硅基流动）中为 `extra_body` 字段，而在 Kimi（月之暗面）中需配合 `reasoning_effort` 使用；GLM-5.3 则明确要求华北2（北京）专属域名以保障稳定性 [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)。

> **注意**：文档 39–43 中多个 legacy 图像模型（如 `wanx-virtualmodel`、`shoemodel-v1`、`image-instance-segmentation`）均标注“仅免费体验，额度用完后不可调用且不支持付费”，并推荐迁移到 `wanx-image-edit` 或 `qwen-image-edit-guide`。该策略与文档 1 中万相V2作为主力文生图模型的定位一致，表明平台已将资源重心转向新版通用编辑能力。

## 关键参数

不同模态模型的关键参数设计高度结构化，但需严格区分上下文语义：  
- **文本生成类**（LLM）：`messages` 为必填数组，`stream` 控制[流式输出](../concepts/streaming-output.md)，`reasoning_effort`（可选值 `low`/`medium`/`high`/`max`/`xhigh`）控制思考深度；`enable_thinking` 非 OpenAI 标准参数，须通过 `extra_body`（Python SDK）或顶层字段（Node.js）传入。  
- **图像生成类**：`prompt`（正向描述）、`negative_prompt`（负向过滤）为通用参数；万相V2 增加 `prompt_extend`（布尔值，默认 `true`）启用智能扩写；局部重绘类模型还需 `image_url`（原图）、`mask_image_url`（涂抹区域）及 `parameters.dilate_flag`（掩码膨胀开关）。  
- **视频生成类**：万相3.0 支持 `reference_images`（图N）、`audio_references`（音频N）等引用标识；Vidu 模型依赖运镜关键词（如 `镜头向左移动`、`固定镜头`）和动态控制词（如 `大动态`、`小动态`）触发特定效果。  
- **实时音视频类**：WebRTC 模式下 `server_vad` 为强制启用项，不支持手动模式；AOQ 模式中 `turn_detection` 设为 `null` 表示 Manual 模式，需客户端显式调用 `input_audio_buffer.commit` 和 `response.create`。

## 使用方式

调用流程遵循“准备→配置→执行→处理”四步范式：  
1. **准备**：获取 API Key 并配置至环境变量（`DASHSCOPE_API_KEY`），确认业务空间 ID（`{WorkspaceId}`）及地域端点（如 `cn-beijing.maas.aliyuncs.com`）；三方模型需额外开通对应服务（如在控制台搜索 `vanchin/deepseek` 并授权）。  
2. **配置**：根据模型类型选择协议——[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)需设置 `base_url`，DashScope 原生接口需指定 `region` 和 `workspace`；实时类模型必须声明媒体权限（Android 需 `RECORD_AUDIO`，iOS 需 `NSMicrophoneUsageDescription`）。  
3. **执行**：异步任务（如图像生成）需两步调用（提交任务 + 轮询结果），同步调用（如 LLM）直接返回响应；AOQ 场景需先从 AppServer 获取临时 Token，再建立连接。  
4. **处理**：流式响应需按 `delta.reasoning_content` / `delta.content` 分段解析；WebRTC 需监听 `ontrack` 事件绑定远端音频流；图像类任务返回 `output.results[0].url` 供下载。

## 限制和注意事项

- **地域强约束**：所有 legacy 图像模型（文档 36–43）、DeepSeek（硅基流动）、Kimi（月之暗面）、GLM（智谱）、MiniMax、MiMo、Stepfun、Unisound、Ling 等三方模型均**仅限华北2（北京）地域**，且必须使用该地域 API Key 和专属域名（如 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），跨地域调用将失败。  
- **免费额度陷阱**：`wanx-virtualmodel`、`shoemodel-v1`、`image-instance-segmentation`、`image-erase-completion`、`wanx-x-painting` 等 5 个 legacy 模型明确标注“免费额度用完后不可调用且不支持付费”，无计费路径，必须迁移至替代方案。  
- **协议兼容性**：WebRTC 模式仅支持服务端 VAD，不兼容 Manual 模式；AOQ 的 `qwen-audio-3.1-asr-flash-streaming` 要求客户端缓存首段音频并倍速补发，否则丢失用户初始语音。  
- **缓存与限流**：显式缓存（Explicit Cache）需在请求中添加 `cache_control` 标记，可实现 100% 确定性命中，但首次写入有 25% 额外开销；限流应对需分层处理——突发流量优先启用服务端排队等待（加 `X-DashScope-Queue-Enable: true` 请求头），高频复用场景则必须启用显式缓存 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。

## 来源文档

- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)
- [视频生成Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
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
- [Ling-蚂蚁数科](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/antdigital.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
- [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
- [使用 AOQ 接入 qwen-audio-3.1-asr-flash-streaming 实现语音输入法](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/voice-input-using-aoq-access-qwen-audio-asr.md)
- [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](../../raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/_short/speech-synthesis-using-aoq-access-qwen-audio-3-0-43022e91dedcb0c1.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)
- [技术解决方案](../../raw/model-user-guide/use-cases/technical-solutions.md)
- [历史模型指南](../../raw/model-user-guide/use-cases/legacy-resources.md)
- [图像生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation.md)
- [通用图像编辑-万相2.1](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md)
- [人像风格重绘](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/style-repaint.md)
- [虚拟模特生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/virtual-model-generation.md)
- [鞋靴模特](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/shoes-and-boots-model.md)
- [人物实例分割](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/image-instance-segmentation.md)
- [图像擦除补全](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/image-erasure-and-completion.md)
- [图像局部重绘](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/vary-region.md)
- [使用 AOQ 接入 qwen3.8-livetranslate-flash-realtime 实现实时语音翻译](../../raw/_short/real-time-translation-using-aoq-access-qwen-live-9b4d3056b2eade2b.md)
- [创意海报生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/creative-poster-generation-overview.md)
- [涂鸦作画](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/sketch-to-image.md)
- [视频生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation.md)
- [视频编辑2.1](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/wan-vace-guide.md)
- [图生视频-基于首尾帧](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-first-and-last-frames-guide.md)
- [万相-图生视频-基于首帧](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-guide.md)


