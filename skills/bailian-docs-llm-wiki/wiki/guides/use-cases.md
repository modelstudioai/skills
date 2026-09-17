# use cases

百炼平台提供覆盖文本、图像、视频、语音、[多模态](../concepts/multi-modal.md)等多维度的 AI 生成与交互能力，支持从 Prompt 工程、RAG 构建、模型微调到实时音视频通话的全栈式用例。本文档面向开发者，结构化梳理核心能力边界、参数规范与工程实践要点，避免营销性描述，聚焦可落地的技术决策依据。

## 支持的模型/功能

百炼支持两类模型接入路径：**百炼原生模型**（如 qwen3 系列、万相系列）和**三方直供模型**（如 DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun、Unisound 等）。所有模型均通过统一 API 接口调用，但部署地域、限流策略与功能特性存在差异。

- **文生文（Text-to-Text）**：支持通用对话、代码生成、Prompt 工程优化、RAG 应用构建（如基于 LlamaIndex 的知识库检索）[原文标题](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。
- **文生图/图生图（Text/Image-to-Image）**：万相 V1/V2 模型，支持 [prompt](prompt.md) 扩展、negative [prompt](prompt.md)、风格控制与镜头语言 [原文标题](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)。
- **文生视频/图生视频（Text/Image-to-Video）**：万相（Wan）与 Vidu 模型，支持多镜头叙事、运镜控制、声音描述及美学参数调节 [原文标题](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)。
- **文档转视频（Document-to-Video）**：端到端自动化流程，将 PDF/DOCX 文档切片、生成图文幻灯片、合成语音与字幕并剪辑成视频 [原文标题](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)。
- **实时音视频交互**：通过 WebRTC（浏览器端）或 AOQ SDK（移动端/HarmonyOS/Linux）接入 qwen3.5-omni-plus-realtime、qwen-audio-3.0-realtime-plus 等模型，支持 VAD 自动轮次或 Manual 按键模式 [原文标题](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)。
- **语音识别与合成**：fun-asr-realtime（实时转写）、qwen-audio-3.0-tts-flash（流式语音合成），均基于 AOQ Inference 协议。

> **注意**：多个三方模型文档存在下架时间冲突。例如，`DeepSeek-阿里云` 文档（文档 9）称 deepseek-v3 系列将于 2026 年 10 月 10 日下架；而 `GLM` 文档（文档 30）同样标注 glm-4.6/4.7 下架时间为 2026 年 10 月 10 日；但 `Kimi-月之暗面` 文档（文档 12）则指出 kimi/kimi-k2.5 将于 2026 年 8 月 31 日下架。这些时间点不一致，建议以百炼控制台实际模型状态为准，并优先选用推荐替代模型（如 qwen3.7-plus）。

## 关键参数

不同模态任务依赖特定参数组合，需严格遵循接口规范：

- **Prompt 相关参数**：
  - `prompt`（正向提示词）与 `negative_prompt`（反向提示词）用于文生图；
  - `prompt_extend: true/false` 控制万相 V2 是否启用大模型智能扩写；
  - 视频生成中需区分 `主体+场景+运动`（基础）与 `主体描述+场景描述+运动描述+美学控制+风格化`（进阶）公式；
  - Vidu 支持 `大动态/中动态/小动态` 等关键词精确控制运动幅度 [原文标题](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)。

- **推理控制参数**：
  - `enable_thinking`（或 `thinking`、`reasoning_effort`）：控制是否开启思考模式及推理深度，适用于 DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun、Unisound 等多数三方模型；
  - `server_vad` / `semantic_vad` / `null`：实时语音场景中决定轮次检测方式（服务端 VAD 或客户端 Manual 模式）；
  - `cache_control`：显式缓存标记，仅在 Anthropic 兼容协议（如 Claude Code、OpenCode）中生效，用于稳定命中缓存 [原文标题](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)。

- **音视频传输参数**：
  - WebRTC 场景中，`iceServers: []` 表示服务端采用 ICE-lite 模式，无需客户端配置 STUN/TURN；
  - AOQ 场景中，Audio 轨传输 PCM/Opus 音频流，Data 轨传输事件（如 `run-task`、`response.create`），二者严格分离。

## 使用方式

- **API 调用**：所有模型均支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（推荐）与 DashScope 原生 SDK。OpenAI 兼容需配置 `base_url` 为 `{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`；DashScope SDK 需设置 `base_http_api_url` 为 `{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1`。
- **SDK 集成**：RAG 场景推荐使用 `llama-index-llms-dashscope` 和 `llama-index-indices-managed-dashscope` 包；实时音视频必须集成 AOQ Client SDK 或浏览器原生 WebRTC API。
- **控制台辅助工具**：Prompt 一键优化工具位于 [Prompt 页面](https://bailian.console.aliyun.com/flow-agent/component-manage/prompt)，可自动扩写与细节添加，但会消耗 [Token](../concepts/token.md) 并按推理计费 [原文标题](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)。
- **环境准备**：所有用例均要求先获取 API Key 并配置至环境变量（`DASHSCOPE_API_KEY`），且多数需指定业务空间 ID（`DASHSCOPE_WORKSPACE_ID`）。

## 限制和注意事项

- **地域绑定**：绝大多数三方模型（DeepSeek-硅基流动、Kimi-月之暗面、GLM-智谱、MiniMax-稀宇科技、MiMo、Stepfun、Unisound）**仅支持华北2（北京）地域**，调用时必须使用该地域的 API Key 与 `base_url`；而百炼原生模型（如万相、qwen3）支持多地域。
- **限流机制**：百炼 API 按主账号、模型维度独立计算 RPM/TPM（分钟级）、RPS/TPS（瞬时）及 Traffic Burst（增速）三类限流。突发流量触发 `429` 错误时，优先尝试服务端排队等待（加 `X-DashScope-Queue-Enable: true` 请求头）[原文标题](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。
- **缓存适用性**：显式缓存（`cache_control`）仅对 Anthropic 协议兼容的工具（Claude Code、OpenCode）开箱即用；其他模型需自行实现应用层缓存逻辑。
- **安全约束**：API Key 必须由业务 AppServer 代理鉴权，**严禁硬编码于客户端代码或提交至代码仓库**（尤其 AOQ 场景）；移动端需动态申请 `RECORD_AUDIO` 权限，Web 端需用户主动授予权限。
- **文件限制**：文档解析（如 DashScopeParse）要求单个文件 ≤100MB 且 ≤1000 页；FFmpeg/Marp 等本地工具需提前安装并确保环境可用。

## 来源文档

- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [使用 AOQ 接入 qwen3.5-omni-plus-realtime 实现按键语音对话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/use-aoq-to-access-qwen3-5-omni-plus-realtime-to-realize-key-voice-dialogue.md)
- [使用 AOQ 接入 qwen-audio-3.0-realtime-plus 实现实时语音对话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/real-time-voice-conversation-using-aoq-access-qwen-audio-3-0-realtime-plus.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/real-time-speech-recognition-using-aoq-access-fun-asr-realtime.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/speech-synthesis-using-aoq-access-qwen-audio-3-0-tts-flash.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)


