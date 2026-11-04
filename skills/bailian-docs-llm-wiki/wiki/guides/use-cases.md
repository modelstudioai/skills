# use cases

百炼平台提供覆盖文本、图像、视频、语音、实时交互等多模态场景的完整能力矩阵，支持从基础生成到复杂工作流编排的各类业务需求。本文档面向开发者，系统梳理核心使用场景、关键参数、调用方式及约束条件，帮助您快速选型并规避常见陷阱。

## 支持的模型/功能

百炼支持三类主流使用路径：  
- **原生模型调用**：包括文生文（如 `qwen3.7-max`）、文生图（`wanx2.1-text-to-image-v2`）、文生视频（`wan3.0`、`vidu`）、语音合成（`qwen-audio-3.0-tts-flash`）与识别（`fun-asr-realtime`）等全栈模型；  
- **三方模型集成**：通过 [OpenAI 兼容接口](../concepts/openai-compatibility.md)或 DashScope 原生协议接入 DeepSeek、Kimi、GLM、MiniMax、Stepfun 等 14+ 家厂商模型，详见 [三方模型调用教程](raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)；  
- **高级应用构建**：基于 RAG（如 [基于LlamaIndex构建RAG应用](raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)）、Agent 工作流、实时音视频（WebRTC/AOQ）、文档转视频等端到端方案。

> **注意**：部分历史图像编辑模型（如 `wanx-virtualmodel`、`shoemodel-v1`、`image-instance-segmentation`）已明确标注“仅提供免费体验，额度用完后不可调用且不支持付费”，生产环境应优先选用 [图像编辑-万相2.1](raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md) 或 [图像编辑-千问](raw/model-user-guide/model-experience/image-and-video-generation/image-model/image-edit-guide/qwen-image-edit-guide.md) 等替代方案。

## 关键参数

不同模态模型的关键控制参数存在显著差异：  
- **文生文**：核心为 `prompt` 结构化设计，推荐采用「背景 + 目的 + 风格」Prompt 框架；显式缓存需通过 `cache_control` 字段标记（如 `{"type": "ephemeral"}`），详见 [显式缓存最佳实践](raw/model-user-guide/use-cases/explicit-cache-guide.md)；  
- **文生图/视频**：`prompt`（正向描述）与 `negative_prompt`（反向排除）为必填项；万相 V2/V3 及 Vidu 支持 `prompt_extend: true` 启用大模型智能扩写；Vidu 还支持细粒度运镜控制（如 `镜头推进`、`左移`）和风格关键词（如 `宫崎骏风格`）；  
- **语音与实时交互**：AOQ 协议下需区分 `Audio` 轨（媒体流）与 `Data` 轨（事件），关键参数如 `turn_detection`（`server_vad`/`null` 控制轮次模式）、`stream_options.include_usage`（流式 Token 统计）；  
- **三方模型**：`enable_thinking`（开启思考模式）、`reasoning_effort`（推理深度）为通用非标准参数，需通过 `extra_body`（Python SDK）或顶层字段（Node.js）传入，各模型支持状态不一。

## 使用方式

- **API 调用**：统一使用 `https://{WorkspaceId}.{region}.maas.aliyuncs.com` 域名，需配置 `DASHSCOPE_API_KEY` 与业务空间 ID；异步任务（如图像生成）需轮询 `task_id` 查询结果；  
- **SDK 集成**：Python 推荐 `dashscope>=2.0.1`，Java 推荐 `dashscope-sdk-java>=2.16.6`；AOQ 场景需额外导入 `libPluginOpus.so` 等插件；  
- **Prompt 工程**：文生文推荐使用平台 [Prompt 一键优化工具](https://bailian.console.aliyun.com/flow-agent/component-manage/prompt)；文生图/视频建议按「主体+场景+运动/风格+镜头语言」公式组织；万相3.0 提供 `/wan3-pe` Skill 命令行调试；  
- **实时交互**：WebRTC 适用于浏览器低延迟场景（需处理 CORS 限制），AOQ 适用于移动端（Android/iOS/HarmonyOS），均需服务端代理 Token 鉴权。

## 限制和注意事项

- **地域与权限绑定**：绝大多数模型（如 `wanx-style-repaint-v1`、`qwen3.8-omni-flash-realtime`）**仅限华北2（北京）地域调用**，且必须使用该地域的 API Key 和业务空间 ID；  
- **限流策略**：按主账号维度独立计算 RPM/TPM、RPS/TPS 及 Traffic Burst 三重阈值，突发流量易触发 `429` 错误；推荐优先启用 [服务端排队等待](raw/model-user-guide/use-cases/rate-limiting-best-practices.md)（加 `X-DashScope-Queue-Enable: true` 请求头）；  
- **并发与资源池**：语音合成高并发需配置对象池（如 `COSYVOICE_OBJECTPOOL_SIZE`），Python 池满后仍可能新建连接，Java 需显式设置 `maxTotal`；  
- **安全与合规**：API Key **严禁硬编码至客户端**，必须由业务 AppServer 代理鉴权并下发临时凭证；AOQ 场景中 `RECORD_AUDIO` 权限需运行时动态申请；  
- **模型生命周期**：小米 `xiaomi/mimo-v2.5-pro` 将于 2026 年 10 月 21 日下线，文档明确提示迁移至 `xiaomi/mimo-v2.6-pro-ultraspeed`。

## 来源文档

- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)
- [视频生成Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [语音合成高并发最佳实践](../../raw/model-user-guide/use-cases/tts-high-concurrency-best-practices.md)
- [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [Ling-蚂蚁数科](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/antdigital.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
- [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
- [使用 AOQ 接入 qwen3.8-livetranslate-flash-realtime 实现实时语音翻译](../../raw/_short/real-time-translation-using-aoq-access-qwen-live-9b4d3056b2eade2b.md)
- [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](../../raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/_short/speech-synthesis-using-aoq-access-qwen-audio-3-0-43022e91dedcb0c1.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)
- [技术解决方案](../../raw/model-user-guide/use-cases/technical-solutions.md)
- [历史模型指南](../../raw/model-user-guide/use-cases/legacy-resources.md)
- [图像生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation.md)
- [通用图像编辑-万相2.1](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md)
- [人像风格重绘](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/style-repaint.md)
- [虚拟模特生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/virtual-model-generation.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [鞋靴模特](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/shoes-and-boots-model.md)
- [人物实例分割](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/image-instance-segmentation.md)
- [使用 AOQ 接入 qwen-audio-3.1-asr-flash-streaming 实现语音输入法](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/voice-input-using-aoq-access-qwen-audio-asr.md)
- [图像擦除补全](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/image-erasure-and-completion.md)
- [图像局部重绘](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/vary-region.md)
- [涂鸦作画](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/sketch-to-image.md)
- [视频生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation.md)
- [创意海报生成](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/creative-poster-generation-overview.md)
- [视频编辑2.1](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/wan-vace-guide.md)
- [图生视频-基于首尾帧](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-first-and-last-frames-guide.md)
- [万相-图生视频-基于首帧](../../raw/model-user-guide/use-cases/legacy-resources/legacy-video-generation/image-to-video-guide.md)


