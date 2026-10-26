# use cases

百炼平台提供覆盖文本、图像、视频、语音、实时交互等多模态场景的完整 AI 应用能力。本文档面向开发者，系统梳理主流 use cases 的模型支持、关键参数、调用方式及实践约束，帮助您快速选型并规避常见陷阱。

## 支持的模型/功能

百炼支持三大类核心能力：**文生文（LLM）**、**文生图/文生视频/图生视频等多模态生成**，以及**实时音视频交互**。其中：

- **文生文**：除通义千问系列外，还集成 DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun、Unisound 等十余家第三方模型，均通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 DashScope 原生协议调用 [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)。所有模型均支持 `enable_thinking` 或 `reasoning_effort` 参数控制思考模式，但具体字段名和默认行为存在差异（见下文“关键参数”）。
- **多模态生成**：万相（WanXiang）系列覆盖文生图（V1/V2）、万相3.0视频生成；Vidu 为独立视频生成模型；此外还支持图生视频、首尾帧生视频、参考生视频等多种任务类型 [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)。
- **实时音视频**：通过 WebRTC 或 AOQ SDK 接入 qwen3.8-omni-flash-realtime、qwen-audio-3.1-asr-flash-streaming、qwen3.8-livetranslate-flash-realtime 等模型，支持语音对话、实时翻译、语音输入法、语音合成等场景 [使用 AOQ 接入 qwen-audio-3.1-asr-flash-streaming 实现语音输入法](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/voice-input-using-aoq-access-qwen-audio-asr.md)。

> **注意**：部分文档对地域支持描述不一致。例如，[GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md) 明确推荐使用华北2（北京）专属域名以获得更高稳定性，而 [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md) 则列出美国、德国、新加坡等多地接入地址。实际调用时，请以控制台开通模型时显示的可用地域为准，并优先采用业务空间专属域名。

## 关键参数

不同模型/任务类型的关键参数高度结构化，需严格按规范传入：

- **文生文通用参数**：
  - `model`：必填，模型 ID（如 `"qwen3.7-max"`、`"ZHIPU/GLM-5.3"`）。
  - `messages`：标准 ChatML 格式消息列表。
  - `stream`：布尔值，控制是否流式响应。
  - `enable_thinking` / `reasoning_effort`：非标准 OpenAI 参数，用于开启思考链。各厂商实现不一：DeepSeek、MiMo、Unisound 默认开启；Stepfun 默认关闭；Kimi 使用 `reasoning_effort: "max"`；MiniMax 在示例中未显式设置（见 [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md) 与 [MiniMax-稀宇科技](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md) 对比）。
- **文生图（万相）参数**：
  - `prompt`：正向提示词，支持中英文。
  - `negative_prompt`：反向提示词。
  - `prompt_extend`（V2 专属）：布尔值，控制是否启用大模型智能改写，默认 `true`。
- **视频生成（万相3.0）参数**：
  - 提示词结构化程度高，支持 `[分镜 N（起-止秒）：主体 + 场景 + 运动 + 美学控制]`、`[台词]`、`[音效/BGM]`、`[负向清单]` 等复合要素。
- **实时音视频（AOQ/WebRTC）参数**：
  - `turn_detection`：决定轮次检测模式（`server_vad`/`semantic_vad`/`null`），直接影响语音起止逻辑。
  - `input_audio_buffer.append` / `commit`：Manual 模式下需显式提交音频缓冲区。

## 使用方式

调用方式分为三类，需匹配对应 SDK 和协议：

- **[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**：适用于所有支持该协议的 LLM 和部分多模态模型（如 `qwen3.8-omni-flash-realtime`）。需配置 `base_url` 为业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），并通过 `extra_body` 传入非标参数（如 `{"enable_thinking": true}`）。
- **DashScope 原生 SDK/API**：适用于万相图像/视频 API、语音合成（TTS）、语音识别（ASR）等。请求体结构更贴近模型语义，例如文生图 V2 的 `parameters.prompt_extend` 字段。
- **AOQ/WebRTC SDK**：专用于实时音视频场景。WebRTC 适合浏览器端低延迟交互；AOQ SDK（Android/iOS/HarmonyOS）提供跨平台统一接口，音频/事件分轨传输，需预导入 Opus 插件并正确声明权限。

## 限制和注意事项

- **地域与模型绑定**：绝大多数第三方模型（DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun、Unisound）仅在华北2（北京）地域可用，且必须使用该地域的 API Key 和业务空间 ID。跨地域调用将失败。
- **限流策略**：API 同时受 RPM（每分钟请求数）、TPM（每分钟 [Token](../concepts/token.md) 数）和 RPS（每秒请求数）三重限制。突发流量易触发 `429` 错误，推荐优先启用平台侧的[服务端排队等待](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)（加 `X-DashScope-Queue-Enable: true` 请求头）。
- **缓存与成本优化**：高频复用相同 Prompt 的场景，应启用[显式缓存](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)，通过 `cache_control` 标记可降低 90% 后续调用成本。
- **实时音视频权限**：客户端必须动态申请 `RECORD_AUDIO` 权限（iOS 需 `NSMicrophoneUsageDescription`），WebRTC 模式还需 `CAMERA`（若启用视频）。AOQ 模式下，纯语音场景无需摄像头权限。
- **模型生命周期**：部分模型有明确下线计划，例如 MiMo-v2.5-pro 将于 2026 年 10 月 21 日下线，文档已明确提示替代方案 [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)。

## 来源文档

- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)
- [视频生成Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [语音合成高并发最佳实践](../../raw/model-user-guide/use-cases/tts-high-concurrency-best-practices.md)
- [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
- [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
- [使用 AOQ 接入 qwen-audio-3.1-asr-flash-streaming 实现语音输入法](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/voice-input-using-aoq-access-qwen-audio-asr.md)
- [使用 AOQ 接入 qwen3.8-livetranslate-flash-realtime 实现实时语音翻译](../../raw/_short/real-time-translation-using-aoq-access-qwen-live-9b4d3056b2eade2b.md)
- [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](../../raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/_short/speech-synthesis-using-aoq-access-qwen-audio-3-0-43022e91dedcb0c1.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)
- [技术解决方案](../../raw/model-user-guide/use-cases/technical-solutions.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)


