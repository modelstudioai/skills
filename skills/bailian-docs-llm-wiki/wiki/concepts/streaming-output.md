# 流式输出

流式输出（Streaming）是指模型推理服务在生成响应过程中，将结果以增量、分块的方式持续返回给客户端，而非等待全部内容生成完毕后一次性返回。这种方式显著降低用户感知延迟，提升交互实时性，是构建对话式 AI、实时音视频处理、长文本生成等场景的关键能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **文本生成（Chat Completions）**：[OpenAI 兼容接口](openai-compatible-api.md)和 DashScope 原生接口均支持 `stream=true` 参数。启用后，服务端按 token 或语义单元（如中文词/标点）分批返回 `content` 片段，客户端可逐块渲染、实时朗读或做中间处理（如敏感词拦截）。适用于客服机器人、编程辅助、写作助手等需要低首字延迟（Time to First [Token](token.md), TTFT）的场景。

- **[多模态](multi-modal.md)实时交互（Omni Realtime API）**：基于 WebSocket 的双向流式协议，天然支持[多模态](multi-modal.md)流式输出。服务端可并发推送 `output.text.delta`（文本增量）、`output.audio.delta`（TTS 音频分片）、`output.image.chunk`（图像生成中间帧）等事件，实现语音-文本-图像的同步流式响应，端到端 P95 延迟控制在 800 ms 内。

- **语音识别（ASR）与合成（TTS）**：专用模型如 `qwen-audio-3.1-asr-flash-streaming` 和 `qwen-audio-3.1-tts-flash` 显式设计为流式输入/输出。ASR 支持音频流边传边识，TTS 支持文本流式输入并实时返回音频流，适用于实时会议转录、语音导航等强实时性场景。

- **三方模型集成（DeepSeek、Kimi、GLM 等）**：只要模型本身支持流式能力且百炼平台已开启该功能（绝大多数主流模型均已支持），开发者只需统一设置 `stream=true` 即可获得流式响应，无需适配不同模型的底层协议差异。

## 关键参数和配置

- **`stream`**：布尔类型，必需参数。设为 `true` 启用流式输出；设为 `false`（默认）则返回完整响应。所有支持流式的接口均要求显式声明此参数。

- **`stream_options.include_usage`**（可选）：仅 DashScope 原生接口支持。设为 `true` 可在流式响应末尾的 `data: [DONE]` 前，额外返回包含 `prompt_tokens`、`completion_tokens`、`total_tokens` 的 usage 字段，便于精确计费与监控。

- **客户端解析要求**：
  - [OpenAI 兼容接口](openai-compatible-api.md)：响应为 Server-Sent Events（SSE），每行以 `data: ` 开头，需按行解析 JSON 并忽略空行及 `data: [DONE]`；
  - DashScope 原生接口：返回标准 JSON Lines（NDJSON），每行一个完整 JSON 对象，无前缀；
  - Omni Realtime API：基于 WebSocket，需监听指定事件类型（如 `output.text.delta`），按事件结构解析 payload。

- **注意事项**：
  - 流式响应不支持 `response_format="json_object"`（结构化输出）——二者互斥，需根据需求二选一；
  - `max_tokens` 仍生效，流式输出会在达到上限时自动终止；
  - 错误不会中断流，而是以带 `error` 字段的独立事件行发出（如 `data: {"error": {"code": "invalid_parameter", ...}}`），客户端应具备容错解析能力。

面向开发者：优先使用 OpenAI Python SDK（`stream=True`）或 DashScope SDK 的 `stream=True` 模式调用；避免手动拼接 SSE/NDJSON 解析逻辑，SDK 已内置健壮流处理器；对实时性敏感场景（如语音），务必选用标注 `-realtime` 或 `-streaming` 后缀的专用模型。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [use cases](../guides/use-cases.md)


