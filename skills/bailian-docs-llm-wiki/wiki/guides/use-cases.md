# use cases

百炼平台提供覆盖文生文、文生图、文生视频、多模态实时交互、RAG、模型微调与三方模型集成等全栈AI用例。本文档面向开发者，系统梳理各场景支持的模型能力、关键参数、调用方式及核心限制，帮助快速选型与落地。

## 支持的模型/功能

百炼支持三大类生成式AI能力：**文本生成（LLM）**、**多模态生成（图像/视频）** 和 **实时音视频交互（Realtime）**。

- **文本生成**：除自研Qwen系列（如`qwen3.7-max`、`qwen3.8-omni-flash-realtime`）外，还集成DeepSeek、Kimi、GLM、MiniMax、MiMo、Unisound、Stepfun等十余家第三方模型。所有模型均通过OpenAI兼容接口或DashScope SDK接入，[三方模型调用教程](raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)统一说明了开通路径与地域约束。> **注意**：多个文档（如[DeepSeek-阿里云](raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)、[Kimi-月之暗面](raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)、[GLM-智谱](raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)）均强调“仅华北2（北京）地域可用”，但[MiniMax-稀宇科技](raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)未明确地域限制，实际部署应以控制台开通页面为准。

- **多模态生成**：  
  - *文生图*：万相系列（`wan-image-api-reference/text-to-image-v2-api-reference.md`）支持`prompt`与`negative_prompt`双参数，V2版本默认启用大模型智能改写（`prompt_extend: true`）。  
  - *文生视频*：万相3.0（[wan3-video-generation-prompt-guide.md](raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)）支持全模态输入（图/视频/音频/网页），其提示词公式包含分镜、台词、音效等结构化要素；Vidu（[vidu-video-generation-prompt-guide.md](raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)）则侧重运镜与风格关键词触发。

- **实时音视频**：基于AOQ或WebRTC协议，支持三类场景：  
  - *实时对话*：`qwen3.8-omni-flash-realtime`（[best-practice-webrtc-omni-realtime.md](raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)）和`qwen-audio-3.1-realtime-plus`（[real-time-voice-conversation-using-aoq-access-qwen-audio-3-0-realtime-plus.md](raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)）；  
  - *语音合成*：`qwen-audio-3.0-tts-flash`（[speech-synthesis-using-aoq-access-qwen-audio-3-0-tts-flash.md](raw/_short/speech-synthesis-using-aoq-access-qwen-audio-3-0-43022e91dedcb0c1.md)）；  
  - *语音识别*：`fun-asr-realtime`（[real-time-speech-recognition-using-aoq-access-fun-asr-realtime.md](raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)）。

## 关键参数

不同场景的核心参数设计体现其任务特性：

- **Prompt相关参数**：  
  - 文生文：无显式参数，依赖Prompt质量。推荐使用[文生文Prompt指南](raw/model-user-guide/use-cases/prompt-engineering-guide.md)中的框架（背景/目的/风格/语气/受众/输出）提升确定性。  
  - 文生图：`prompt`（正向描述）、`negative_prompt`（反向过滤），V2支持`prompt_extend`开关。  
  - 视频生成：万相3.0采用分镜结构化参数（时间戳、主体、运动、美学控制），Vidu则依赖运镜关键词（如`镜头推近`、`航拍镜头`）和风格词（如`宫崎骏风格`）。

- **推理控制参数**：  
  - 思考模式：DeepSeek、Kimi、GLM、MiMo、Unisound、Stepfun等均支持`enable_thinking`或`reasoning_effort`参数控制是否输出推理过程（见[DeepSeek-硅基流动](raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)、[Kimi-月之暗面](raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)等文档）。  
  - 实时交互：`qwen3.8-omni-flash-realtime`需配置`turn_detection`（`server_vad`或`null`）决定语音轮次由服务端还是客户端控制（[use-aoq-to-access-qwen3-5-omni-plus-realtime-to-realize-key-voice-dialogue.md](raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)）。

- **缓存与限流**：  
  - 显式缓存：通过`cache_control`标记实现确定性命中，适用于Agent长上下文管理（[explicit-cache-guide.md](raw/model-user-guide/use-cases/explicit-cache-guide.md)）。  
  - 限流维度：按主账号、模型独立计算，含RPM/TPM（分钟级）、RPS/TPS（瞬时）、Traffic Burst（增速）三重约束（[rate-limiting-best-practices.md](raw/model-user-guide/use-cases/rate-limiting-best-practices.md)）。

## 使用方式

- **API调用**：所有模型均支持HTTP RESTful API与SDK（DashScope/OpenAI兼容）。关键步骤为：① 获取API Key并配置环境变量；② 根据模型地域要求设置`base_url`（如华北2需替换`{WorkspaceId}`）；③ 构造请求体（含`model`、`messages`或`input.prompt`等）。

- **低代码集成**：  
  - RAG应用：通过LlamaIndex接入，使用`DashScopeCloudIndex`创建知识库（[build-rag-applications-based-on-llamaindex.md](raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)）。  
  - 实时交互：WebRTC方案需浏览器端创建`RTCPeerConnection`并处理媒体流；AOQ方案需在移动端导入SDK并申请`RECORD_AUDIO`权限（[best-practice-aoq-omni-realtime.md](raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)）。

- **工具辅助**：  
  - Prompt优化：控制台提供一键自动扩写工具（[文生文Prompt指南](raw/model-user-guide/use-cases/prompt-engineering-guide.md)）；  
  - 视频调优：万相3.0提供`/wan3-pe` Skill命令行调试（[wan3-video-generation-prompt-guide.md](raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)）。

## 限制和注意事项

- **地域与模型绑定**：绝大多数第三方模型（DeepSeek、Kimi、GLM、MiniMax、MiMo、Unisound、Stepfun）明确限定华北2（北京）地域，且需对应地域的API Key。跨地域调用将失败。

- **废弃模型风险**：多个文档标注模型下架时间，例如`deepseek-v3`系列将于2026年10月10日下架（[DeepSeek-阿里云](raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)），`kimi-k2-instruct`已于2026年7月9日下架（[Kimi](raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)）。生产环境必须及时迁移至推荐替代模型（如`qwen3.7-plus`）。

- **资源约束**：  
  - 文档解析：`DashScopeParse`限制单文件≤100MB且≤1000页（[build-rag-applications-based-on-llamaindex.md](raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)）；  
  - 实时通话：WebRTC方案受浏览器CORS限制，SDP交换需后端代理（[best-practice-webrtc-multimodal-dialog.md](raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)）；  
  - 缓存成本：显式缓存首次写入产生25%额外开销，但后续命中可节省90%成本（[explicit-cache-guide.md](raw/model-user-guide/use-cases/explicit-cache-guide.md)）。

- **安全规范**：API Key严禁硬编码于客户端代码，必须由业务AppServer代理鉴权并下发临时Token（[real-time-voice-conversation-using-aoq-access-qwen-audio-3-0-realtime-plus.md](raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)）。

## 来源文档

- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)
- [视频生成Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)
- [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
- [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](../../raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/_short/speech-synthesis-using-aoq-access-qwen-audio-3-0-43022e91dedcb0c1.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)
- [技术解决方案](../../raw/model-user-guide/use-cases/technical-solutions.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)


