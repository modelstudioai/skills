# use cases

百炼平台的 use cases 文档面向开发者，系统梳理了主流应用场景下的模型能力、参数配置、调用方式及关键约束。本文档不覆盖营销型解决方案（如“AI解题+批改”），而是聚焦可编程、可集成的技术实践路径，涵盖文生文、文生图/视频、RAG、模型微调、实时音视频、三方模型接入等核心方向，并强调跨模型一致的工程规范（如 API Key 配置、地域与 Workspace ID 绑定、限流应对）。

## 支持的模型/功能

百炼提供两类核心能力：**原生模型服务**（如 Qwen 系列、万相系列）和**三方模型托管服务**（如 DeepSeek、Kimi、GLM、MiniMax 等）。  
- **文生文**：支持全系列 Qwen 模型（含 qwen3.7-max、qwen3.8-omni-flash-realtime）、DeepSeek-v4、Kimi-k3、GLM-5.3、MiniMax-M2.7 等，均通过 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)或 DashScope 原生 API 调用 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)。  
- **多模态生成**：万相（WanX）系列覆盖文生图（V1/V2）、文生视频（wan3.0）、图生视频、通用图像编辑（wanx-image-edit）、人像风格重绘、虚拟模特、鞋靴模特等；Vidu 视频生成亦提供独立 Prompt 指南 [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)。  
- **实时音视频**：qwen3.8-omni-flash-realtime、qwen-audio-3.1-asr-flash-streaming、qwen3.8-livetranslate-flash-realtime 等模型通过 AOQ 或 WebRTC 协议实现实时交互 [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)。  
- **RAG 与知识库**：支持基于 LlamaIndex 构建 RAG 应用，利用 DashScopeCloudIndex 实现文档解析、索引构建与检索 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。  
- **自定义模型**：提供模型调优（微调）、部署、评测全流程，支持从训练数据准备到独占实例部署的端到端操作。

> **注意**：部分历史图像/视频模型（如 `wanx-style-repaint-v1`、`shoemodel-v1`、`image-instance-segmentation`）当前仅提供免费体验，额度用完后不可调用且不支持付费，官方推荐迁移至万相2.1或千问图像编辑方案 [历史模型指南](../../raw/model-user-guide/use-cases/legacy-resources.md)。

## 关键参数

不同模型类型的关键参数存在显著差异，需严格按文档约定传入：  
- **文生文类**：`model`（必填，如 `"qwen3.7-max"`）、`messages`（标准 ChatML 格式）、`stream`（流式开关）、`reasoning_effort`（控制思考深度，适用于支持 deep thinking 的模型如 Kimi-k3、GLM-5.3）、`enable_thinking`（非 OpenAI 标准参数，需通过 `extra_body` 传入）。  
- **文生图类**（万相 V2）：`prompt`（正向提示词）、`negative_prompt`（反向提示词）、`prompt_extend`（是否启用大模型智能改写，默认 `true`）[文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)。  
- **文生视频类**（wan3.0）：`prompt`（支持结构化公式，含分镜、台词、音效等）、`prompt_extend`（同上）、参考素材引用（如 `图 N`）；Vidu 则强调 `主体/场景+场景描述+环境描述+艺术风格/媒介` 公式及运镜关键词（如 `镜头推`、`固定镜头`）[Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)。  
- **实时音视频类**（AOQ）：`turn_detection`（`null` 表示 Manual 模式，`server_vad` 表示服务端 VAD 模式）、`input_audio_buffer.append`（Manual 模式下需显式调用）、`response.create`（触发回复）；WebRTC 模式仅支持 `server_vad` [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)。  
- **RAG 类**：`DASHSCOPE_WORKSPACE_ID`（决定文档解析结果归属的业务空间）、`ResultType.DASHSCOPE_DOCMIND`（指定文档解析器类型）。

## 使用方式

所有调用均需前置完成三要素配置：**API Key 获取与环境变量设置**、**业务空间 ID（WorkspaceId）确认**、**地域（region）匹配**（如华北2北京需用 `cn-beijing.maas.aliyuncs.com` 域名）。  
- **SDK 调用**：Python 推荐 `dashscope` SDK（>=2.0.1）或 `openai` SDK（配置 `base_url`）；Java 推荐 `dashscope-sdk-java`（>=2.16.6）。三方模型（如 DeepSeek、Kimi）均采用相同 OpenAI 兼容模式，仅 `model` 参数值不同。  
- **HTTP 调用**：[异步任务](../concepts/asynchronous-task.md)（如图像/视频生成）需两步：先 POST 创建任务获取 `task_id`，再 GET 查询结果；同步任务（如文本生成）直接返回响应。  
- **实时协议**：AOQ 场景需集成客户端 SDK，处理 Audio/Data 双轨事件；WebRTC 场景需浏览器原生 `RTCPeerConnection` + SDP 交换（Demo 中需 curl 代理，生产环境由业务后端代理）。  
- **缓存与流控**：显式缓存需在请求中添加 `cache_control` 标记；高并发 TTS 场景建议使用对象池复用连接 [语音合成高并发最佳实践](../../raw/model-user-guide/use-cases/tts-high-concurrency-best-practices.md)；限流应对需结合服务端排队、客户端自适应重试与架构层 MQ 削峰 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。

## 限制和注意事项

- **地域与权限强绑定**：绝大多数模型（如 DeepSeek-硅基流动、Kimi-月之暗面、GLM-智谱、所有实时音视频模型）**仅支持华北2（北京）地域**，且必须使用该地域的 API Key 和 WorkspaceId，跨地域调用将失败。  
- **免费额度与停服风险**：`wanx-virtualmodel`、`shoemodel-v1`、`image-instance-segmentation` 等历史模型已明确标注“仅供免费体验”，额度耗尽即不可用，且无付费通道，需主动迁移至新模型。  
- **参数兼容性陷阱**：`enable_thinking`、`reasoning_effort`、`thinking` 等参数非 OpenAI 标准，Python SDK 必须通过 `extra_body` 传入，Node.js SDK 作为顶层参数，否则被忽略；`stream_options.include_usage` 在流式响应中返回 [Token](../concepts/token.md) 消耗，但部分模型（如 Ling-3.1-flash）要求 `include_usage` 必须为 `true`，设为 `false` 将报错。  
- **输入格式硬约束**：图像类 API 对输入有严格限制——`wanx-style-repaint-v1` 要求 `style_index` 为预设值或 `-1`（自定义风格）；`shoemodel-v1` 要求模特图与鞋靴图比例均在 `[2:3, 3:2]` 内；`image-instance-segmentation` 要求单边分辨率 512–4096 像素。违反即返回 400 错误。  
- **计费与资源隔离**：限流按主账号维度统计，RAM 子账号、业务空间、API Key 共享同一配额；模型部署需独占实例，费用独立于推理调用；显式缓存首次写入产生 25% 额外开销，但后续命中可节省 90% 成本。

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
- [语音合成高并发最佳实践](../../raw/model-user-guide/use-cases/tts-high-concurrency-best-practices.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [Ling-蚂蚁数科](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/antdigital.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
- [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
- [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [使用 AOQ 接入 qwen-audio-3.1-asr-flash-streaming 实现语音输入法](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/voice-input-using-aoq-access-qwen-audio-asr.md)
- [使用 AOQ 接入 qwen3.8-livetranslate-flash-realtime 实现实时语音翻译](../../raw/_short/real-time-translation-using-aoq-access-qwen-live-9b4d3056b2eade2b.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/_short/speech-synthesis-using-aoq-access-qwen-audio-3-0-43022e91dedcb0c1.md)
- [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](../../raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)
- [历史模型指南](../../raw/model-user-guide/use-cases/legacy-resources.md)
- [技术解决方案](../../raw/model-user-guide/use-cases/technical-solutions.md)
- [通用图像编辑-万相2.1](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md)
- [图像生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation.md)
- [人像风格重绘](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/style-repaint.md)
- [虚拟模特生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/virtual-model-generation.md)
- [鞋靴模特](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/shoes-and-boots-model.md)
- [人物实例分割](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/image-instance-segmentation.md)
- [图像局部重绘](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/vary-region.md)
- [创意海报生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/creative-poster-generation-overview.md)
- [图像擦除补全](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/image-erasure-and-completion.md)
- [涂鸦作画](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/sketch-to-image.md)
- [视频生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation.md)
- [视频编辑2.1](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/wan-vace-guide.md)
- [图生视频-基于首尾帧](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-first-and-last-frames-guide.md)
- [万相-图生视频-基于首帧](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-guide.md)


