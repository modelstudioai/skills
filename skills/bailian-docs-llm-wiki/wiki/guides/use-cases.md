# use cases

百炼平台的 use cases 覆盖文生文、文生图、文生视频、多模态实时音视频、RAG 构建、模型微调与部署、限流应对及显式缓存等核心场景。本文档面向开发者，结构化梳理各用例的技术要点、参数规范与实践约束，聚焦可落地的工程细节，避免概念性描述。

## 支持的模型/功能

百炼支持三类主流能力路径：  
- **生成式文本**：包括 Qwen 系列（如 `qwen3.7-max`）、三方模型（如 `kimi/kimi-k3.1-pro`、`ZHIPU/GLM-5.3`、`MiniMax-M2.7`）及思考增强模型（均支持 `reasoning_content` 字段与 `reasoning_effort` 控制）；[DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md) 提供更长上下文，而 [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md) 支持联网搜索与上下文缓存。  
- **多模态生成**：万相系列覆盖文生图（`wanx-text-to-image-v2`）、图生视频（`wanx-image-to-video`）、文生视频（`wanx-text-to-video`），以及 Vidu 视频生成；[万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md) 提供全模态分镜控制能力。  
- **实时交互与工具链**：AOQ 与 WebRTC 支持 `qwen3.8-omni-flash-realtime` 等实时音视频模型；RAG 场景推荐使用 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md) 的托管索引方案；图像编辑类任务则涵盖虚拟模特、鞋靴试穿、人物分割等遗留能力（见 [历史模型指南](../../raw/model-user-guide/use-cases/legacy-resources.md)）。

> **注意**：文档 39–43 明确指出 `wanx-virtualmodel`、`shoemodel-v1`、`image-instance-segmentation` 等模型“仅提供免费体验，免费额度用完后不可调用且不支持付费”，并推荐迁移到 `wanx-image-edit` 或 `qwen-image-edit` 等替代方案。该策略与当前主推的万相2.1和Qwen图像编辑路线一致，需在集成时主动规避已停服模型。

## 关键参数

不同模态模型的关键参数存在显著差异，开发者须严格按接口规范传参：  
- **文本生成**：`messages`（必填，OpenAI 兼容格式）、`stream`（流式开关）、`reasoning_effort`（思考强度，取值 `low`/`medium`/`high`/`max`/`xhigh`）、`enable_thinking`（非标准参数，需通过 `extra_body` 传入）。部分模型（如 `stepfun/step-3.7-flash`）默认开启思考且不可关闭。  
- **文生图**：`prompt`（正向提示词）、`negative_prompt`（反向提示词）、`prompt_extend`（V2 默认 `true`，启用大模型智能改写）。  
- **文生视频**：除 `prompt` 外，`wan3.0` 引入结构化字段如 `分镜 N（起-止秒）`、`台词`、`音效/BGM`、`负向清单`；Vidu 则依赖 `主体/场景+场景描述+环境描述+艺术风格/媒介` 公式及运镜关键词（如 `镜头推进`、`固定镜头`）。  
- **实时音视频（AOQ）**：`turn_detection` 决定轮次控制模式（`server_vad`/`semantic_vad`/`null`），Manual 模式下需显式调用 `input_audio_buffer.commit` 和 `response.create`；WebRTC 仅支持服务端 VAD 模式。  
- **RAG 与缓存**：`DASHSCOPE_WORKSPACE_ID` 必须设置以指定业务空间；显式缓存需在请求中注入 `cache_control` 标记（如 `{"type": "ephemeral"}`），且仅 Anthropic 协议兼容端点原生支持。

## 使用方式

所有用例均遵循统一接入范式：  
1. **前置准备**：获取 API Key 并配置为环境变量（`DASHSCOPE_API_KEY`），确认业务空间 ID（`{WorkspaceId}`）及地域（如 `cn-beijing`）；  
2. **SDK/HTTP 调用**：  
   - [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)：`base_url` 统一为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`，模型 ID 直接填入 `model` 字段；  
   - DashScope 原生接口：需指定 `region`（如 `"cn-beijing"`）与 `workspace` 参数；  
3. **异步任务处理**：图像/视频类 API（如 `wanx-style-repaint-v1`、`wanx-poster-generation-v1`）强制异步，需先调用任务创建接口获取 `task_id`，再轮询查询结果；  
4. **工具链集成**：  
   - RAG 场景使用 `DashScopeCloudIndex` 替代本地索引，依赖 `DashScopeParse` 解析 PDF/DOCX（单文件 ≤100MB，≤1000页）；  
   - Prompt 优化可调用控制台内置工具或 `wan3-pe` Skill（需下载 ZIP 并在对话框输入 `/wan3-pe`）；  
   - 显式缓存对 Claude Code、OpenCode 等工具原生支持，无需修改代码逻辑。

## 限制和注意事项

- **地域与模型绑定**：绝大多数三方模型（如 Kimi、GLM、MiniMax）仅在华北2（北京）可用；GLM 在美国（弗吉尼亚）、德国（法兰克福）等多地提供服务，但需核对 [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md) 文档中的地域支持列表。  
- **限流维度**：API 同时受 RPM（每分钟请求数）、TPM（每分钟 Token 数）、RPS（每秒请求数）、TPS（每秒 Token 数）及 Traffic Burst（突发流量）四重限制；[限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md) 推荐优先启用“服务端排队等待”（加 `X-DashScope-Queue-Enable: true` 请求头）。  
- **免费额度与停服风险**：`wanx-virtualmodel`、`shoemodel-v1`、`image-erase-completion` 等遗留模型明确标注“免费额度用完即停用”，且无付费通道；新项目应直接选用 `wanx-image-edit` 或 `qwen-image-edit`。  
- **安全与合规**：API Key 严禁硬编码至客户端（如 Android/iOS App），必须由业务 AppServer 代理鉴权；AOQ 场景中凭证需每次连接前动态申请。  
- **调试建议**：Prompt 质量直接影响生成效果，推荐从基础公式（如文生图的“主体+场景+风格”）起步，逐步叠加细节；视频类任务建议先验证单分镜，再组合多分镜。

## 来源文档

- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [视频生成Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [Ling-蚂蚁数科](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/antdigital.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
- [使用 AOQ 接入 qwen-audio-3.1-asr-flash-streaming 实现语音输入法](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/voice-input-using-aoq-access-qwen-audio-asr.md)
- [使用 AOQ 接入 qwen3.8-livetranslate-flash-realtime 实现实时语音翻译](../../raw/_short/real-time-translation-using-aoq-access-qwen-live-9b4d3056b2eade2b.md)
- [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](../../raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/_short/speech-synthesis-using-aoq-access-qwen-audio-3-0-43022e91dedcb0c1.md)
- [技术解决方案](../../raw/model-user-guide/use-cases/technical-solutions.md)
- [历史模型指南](../../raw/model-user-guide/use-cases/legacy-resources.md)
- [图像生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation.md)
- [通用图像编辑-万相2.1](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md)
- [人像风格重绘](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/style-repaint.md)
- [虚拟模特生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/virtual-model-generation.md)
- [鞋靴模特](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/shoes-and-boots-model.md)
- [人物实例分割](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/image-instance-segmentation.md)
- [图像擦除补全](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/image-erasure-and-completion.md)
- [创意海报生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/creative-poster-generation-overview.md)
- [图像局部重绘](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/vary-region.md)
- [视频生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation.md)
- [涂鸦作画](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/sketch-to-image.md)
- [图生视频-基于首尾帧](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-first-and-last-frames-guide.md)
- [视频编辑2.1](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/wan-vace-guide.md)
- [万相-图生视频-基于首帧](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-guide.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)


