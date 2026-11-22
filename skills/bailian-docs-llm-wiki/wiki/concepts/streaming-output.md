# 流式输出

流式输出（Streaming Output）是百炼平台核心的实时响应机制，指模型服务在推理过程中**边计算、边生成、边传输**结果，而非等待全部输出完成后再一次性返回。该机制显著降低端到端延迟，提升交互自然度，是构建语音对话、实时翻译、长文本生成等低延迟场景的底层能力支撑。

## 在百炼平台的不同场景中如何使用

流式输出在百炼平台中并非统一实现，而是根据调用协议与模型类型差异化启用：

- **实时 API（WebSocket 协议）**：所有实时能力（ASR/TTS/音频对话/[多模态](multi-modal.md)交互）**强制启用流式**，无非流式选项。数据以帧（frame）为单位持续收发（如 `output.text`、`output.audio`），支持毫秒级响应与双向实时控制（如中断、暂停、参数热更新）。  
- **Model Experience（HTTP 协议）**：对文本生成类模型（如 `qwen-turbo`, `qwen-plus`）和部分语音生成模型（如 `qwen-audio`），通过请求体中 `stream: true` 显式开启。响应为 Server-Sent Events（SSE）格式，每条 `data:` 行包含一个 JSON chunk（含 `delta.content` 或 `delta.audio`）。  
- **[OpenAI 兼容接口](openai-compatible-api.md)**：`/chat/completions` 和 `/responses` 支持 `stream: true`，行为与 OpenAI 一致；但 `Qwen-Audio` 等专用模型**不支持该协议下的流式**，需切回 DashScope 原生协议或实时 WebSocket。  
- **框架集成（LlamaIndex / Spring AI）**：通过 `stream=True` 参数或 `StreamingChatClient` 启用，底层自动适配对应协议的流式解析逻辑，并提供标准回调（如 `on_llm_new_token`），开发者无需处理原始 SSE 或帧解析。  
- **全模态与非生成类模型**：`qwen2.5-omni`、向量嵌入（`text-embedding-*`）、OCR 等模型**不支持流式输出**，设置 `stream=true` 将被静默忽略或报错。

> ⚠️ 注意：流式输出不改变模型计算逻辑，仅影响传输方式。首 token 延迟（Time to First [Token](token.md), TTFT）仍受模型大小、输入长度、网络带宽影响，建议结合 `temperature=0`、`top_p=1` 等确定性参数优化可预测性。

## 关键参数和配置

| 参数 | 类型 | 作用 | 说明 |
|------|------|------|------|
| `stream` | boolean | 全局开关 | 必须显式设为 `true` 才启用流式；默认 `false`（非流式）。实时 API 中此参数强制为 `true`，传 `false` 将拒绝连接。 |
| `enable_thinking`（Batch 场景） | boolean | 控制推理过程是否流式化 | 仅在 OpenAI 兼容 Batch 接口生效，开启后思考步骤（reasoning）也将分块输出，增加 `reasoning_tokens` 成本。 |
| `max_tokens`（流式下） | integer | 输出长度上限 | 仍生效，但流式响应会在达到上限时发送 `finish_reason: "length"` 的终止 chunk，而非截断内容。 |
| `delta.content` / `delta.audio` | string / base64 | 流式 chunk 内容字段 | 每个 chunk 仅含本次增量内容（非完整累积），客户端需自行拼接。注意：首 chunk 的 `delta.content` 可能为空字符串，需判空处理。 |

- **传输格式**：  
  - HTTP 流式：SSE（`Content-Type: text/event-stream`），每行以 `data:` 开头，末尾双换行符分隔。  
  - WebSocket 流式：二进制或 JSON 帧（遵循 MIP 协议），需按 `event` 类型（如 `output.text`）解析 payload。  
- **错误处理**：流式过程中发生错误（如鉴权失败、模型超时）会立即发送 `error` 类型帧或 SSE `event: error`，后续 chunk 不再发送。务必监听错误事件并主动关闭连接/流。

## 面向开发者：简洁实用建议

- ✅ **优先使用官方 SDK**：WebSocket SDK 自动处理重连、心跳、帧校验；Python/JS SDK 对 HTTP 流式封装了 `iter_lines()` 或 `async for chunk in response` 接口，避免手动解析 SSE。  
- ✅ **始终检查 `finish_reason`**：流式结束时必有 `finish_reason` 字段（`"stop"`/`"length"`/`"tool_calls"`/`"error"`），据此判断是否正常完成。  
- ✅ **前端防抖与节流**：流式文本逐字到达，UI 渲染（如打字机效果）建议添加 20–50ms 节流，避免频繁重绘；音频流需对接 Web Audio API 实时解码播放。  
- ❌ **勿假设 chunk 大小均匀**：网络抖动、模型计算波动会导致 chunk 间隔和内容长度不均，切勿依赖固定时间间隔或字符数做状态判断。  
- ❌ **不要在流式中修改 `parameters`**：HTTP 流式请求参数在初始化时锁定；WebSocket 流式需发送 `session.update` 帧动态调整，且部分参数（如 `model`）不可热更新。

## 关联主题页

- [realtime api directory](../api/realtime-api-directory.md)
- [model experience](../guides/model-experience.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [frameworks](../api/frameworks.md)
- [qwen api reference](../api/qwen-api-reference.md)


