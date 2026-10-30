# use cases

百炼平台的 use cases 覆盖从基础文本生成到多模态内容创作、实时音视频交互及企业级 RAG 应用的完整技术栈。开发者可根据业务需求选择预置模型、第三方模型或自定义模型，并结合 Prompt 工程、缓存优化、流控策略等最佳实践提升系统稳定性与成本效率。

## 支持的模型/功能

百炼支持三大类模型能力：  
- **文生文（Text-to-Text）**：包括 Qwen 系列、DeepSeek、Kimi、GLM、MiniMax、Ling、MiMo、Stepfun、Unisound 等数十种主流大模型，均通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 DashScope SDK 接入；[DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md) 和 [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md) 等文档明确区分了不同供应商的服务特性与地域限制。  
- **多模态生成**：涵盖文生图（万相 V1/V2）、文生视频（万相 3.0、Vidu）、图生视频、参考生视频等，支持分镜控制、声音描述、风格化参数等精细化指令；[万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md) 提供了全模态提示词公式，而 [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md) 则聚焦于关键词词典与运镜控制。  
- **实时音视频（Realtime）**：提供 WebRTC 与 AOQ 两种接入路径，支持 qwen3.8-omni-flash-realtime、qwen-audio-3.1-asr-flash-streaming、qwen3.8-livetranslate-flash-realtime 等低延迟模型，适用于语音输入法、实时翻译、按键对话等场景；[使用 AOQ 接入 qwen-audio-3.1-asr-flash-streaming 实现语音输入法](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/voice-input-using-aoq-access-qwen-audio-asr.md) 详细说明了音频缓存与倍速补发机制。

> **注意**：部分第三方模型存在地域强约束。例如，[DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md) 和 [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md) 均明确要求仅华北2（北京）可用，且后者推荐迁移到专属域名 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com` 以获得更高稳定性，而旧域名 `https://dashscope.aliyuncs.com` 仍可运行但非最优路径。

## 关键参数

不同任务类型对应关键参数如下：  
- **文生文**：`model`（模型 ID）、`messages`（多轮对话结构）、`stream`（流式开关）、`enable_thinking` 或 `reasoning_effort`（思考模式控制，见 [Ling-蚂蚁数科](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/antdigital.md) 和 [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md) 文档）。  
- **文生图**：`prompt`（正向提示词）、`negative_prompt`（反向提示词）、`prompt_extend`（是否启用大模型智能改写，默认 true，见 [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)）。  
- **文生视频**：除 `prompt` 外，万相 3.0 支持 `prompt_extend`，Vidu 支持 `dynamic_control`（如“大动态”）、`camera_movement`（如“镜头推”）等维度化关键词；[Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md) 的提示词词典是调优核心依据。  
- **实时音视频（AOQ）**：`turn_detection`（设为 `null` 启用手动模式，见 [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)）、`input_audio_buffer.append/commit`（音频分段控制）、`run-task/continue-task`（Inference 协议语义）。

## 使用方式

标准调用流程为：获取 API Key → 配置 Workspace ID 与地域 Endpoint → 构造请求体 → 发送请求。具体方式包括：  
- **SDK 调用**：Python/Java SDK 支持 OpenAI 兼容模式（需设置 `base_url`）和 DashScope 原生模式；[三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md) 汇总了所有第三方模型入口。  
- **Prompt 工程化**：推荐使用结构化框架——文生文采用「背景+目的+风格+受众+输出」五要素；文生图/视频按「主体+场景+运动+美学控制+风格」逐层扩展；[文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md) 提供了一键优化工具链接与框架图示。  
- **RAG 集成**：基于 LlamaIndex，使用 `DashScopeParse` 解析文档，`DashScopeCloudIndex` 创建知识库；[基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md) 给出了完整的 Python 示例与文件大小限制（单文件 ≤100MB，≤1000 页）。  
- **显式缓存**：对高频复用 Prompt 场景，在请求中添加 `cache_control` 字段；[显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md) 明确指出 Claude Code、Open Code 等工具已原生支持，且首次写入仅增加 25% 成本。

## 限制和注意事项

- **地域与模型绑定**：绝大多数第三方模型（如 DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun、Unisound、Ling）仅支持华北2（北京），少数如 Kimi、GLM、DeepSeek 支持新加坡、美国等多地域，但需严格匹配 API Key 所属地域。  
- **限流维度**：API 受 RPM（每分钟请求数）、TPM（每分钟 [Token](../concepts/token.md) 数）、RPS（每秒请求数）、TPS（每秒 [Token](../concepts/token.md) 数）及 Traffic Burst（突发流量）四重约束；[限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md) 强调需同时监控请求与 [Token](../concepts/token.md) 两个维度，单纯重试无效。  
- **实时音视频权限**：WebRTC 方案需浏览器麦克风/摄像头权限，且受 CORS 限制，Demo 中需 curl 代理 SDP；AOQ 方案在 Android/iOS/HarmonyOS 上需声明 `RECORD_AUDIO` 权限并动态申请，iOS 还需 `NSMicrophoneUsageDescription` 描述。  
- **模型下线风险**：部分模型有明确生命周期，如 [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md) 文档注明 `xiaomi/mimo-v2.5-pro` 将于 2026 年 10 月 21 日下线，应提前迁移至 `mimo-v2.6-pro-ultraspeed`。  
- **缓存与 Token 计费**：显式缓存虽降低成本，但其写入操作本身消耗 Token 并计费；[显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md) 明确提示“Prompt优化功能通过调用大模型实现，需要消耗一定量的Token，按照模型推理费用计费”。

## 来源文档

- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)
- [视频生成Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [语音合成高并发最佳实践](../../raw/model-user-guide/use-cases/tts-high-concurrency-best-practices.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [Ling-蚂蚁数科](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/antdigital.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
- [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
- [使用 AOQ 接入 qwen-audio-3.1-asr-flash-streaming 实现语音输入法](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/voice-input-using-aoq-access-qwen-audio-asr.md)
- [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](../../raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/_short/speech-synthesis-using-aoq-access-qwen-audio-3-0-43022e91dedcb0c1.md)
- [技术解决方案](../../raw/model-user-guide/use-cases/technical-solutions.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [使用 AOQ 接入 qwen3.8-livetranslate-flash-realtime 实现实时语音翻译](../../raw/_short/real-time-translation-using-aoq-access-qwen-live-9b4d3056b2eade2b.md)


