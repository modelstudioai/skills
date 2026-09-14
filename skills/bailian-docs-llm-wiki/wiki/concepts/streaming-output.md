# 流式输出

流式输出（Streaming Output）是指模型服务在生成响应过程中，将结果以增量方式分块、实时返回给客户端，而非等待全部内容生成完毕后一次性返回。这种方式显著降低端到端延迟，提升用户交互体验，并支持 token 级别实时渲染、中断控制与低延迟语音/文本协同等高级场景。

## 在百炼平台的不同场景中，这个概念如何使用

- **标准文本生成（OpenAI/Anthropic 兼容接口）**：通过设置 `stream: true` 启用流式响应，服务按 token 或语义单元（如词元、标点、句子片段）持续推送 `delta.content`（OpenAI）或 `delta.text`（Anthropic）字段，适用于聊天界面逐字显示、实时翻译等场景。

- **DashScope 原生接口**：流式响应为可选能力，启用后返回结构化 chunk（含 `output.text`、`usage`、`finish_reason` 等），支持更精细的调试与监控；部分参数（如 `incremental_output`）需与 `stream: true` 协同配置，否则请求将被拒绝（400 错误）。

- **Realtime API（WebSocket / HTTP/2）**：流式为**强制模式**（`stream` 必须为 `true`），采用事件驱动设计，返回标准化 SSE 事件流（如 `content_block_delta`、`tool_use`、`message_stop`），支持毫秒级响应、输入中断（`input_interrupt`）、工具调用与多模态流式输入（图像/音频 base64 或 PCM 流）。

- **Omni Realtime API（全双工多模态）**：深度集成流式能力，提供双向事件流（`input_audio_buffer` → `response_text_delta` → `audio_chunk`），实现 ASR-LLM-TTS 端到端低延迟闭环，适用于智能座舱、实时会议助手等对时延敏感场景。

- **异步任务与非流式服务（如 test-1）**：明确**不支持**流式输出。例如 `test-1` 服务仅提供同步 `/v1/chat/completions` 接口，`stream: true` 将被忽略或直接报错，开发者需选择其他支持流式的模型（如 `qwen-plus`）或接口（如 Realtime API）替代。

> ⚠️ 注意：流式能力与模型、接口协议、部署形态强绑定——并非所有模型都支持所有流式协议（如 `qwen-vl` 不支持 Anthropic Messages 流式），也并非所有接口默认启用（如 DashScope 原生接口需显式开启）。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 | 所属接口 |
|------|------|------|------|-----------|
| `stream` | boolean | 否（除 Realtime API 外） | 启用流式响应；设为 `true` 后，响应体转为 SSE 格式（HTTP）或事件帧（WebSocket） | OpenAI/Anthropic/DashScope 原生 |
| `incremental_output` | boolean | 否（但部分版本强制要求） | 控制是否返回增量式中间结果；Qwen3 及后续版本启用 `stream` 时**必须同时设置为 `true`**，否则返回 400 | DashScope 原生（v2024.09+） |
| `max_tokens` | integer | 否 | 限制单次响应最大 token 数；流式场景下影响最终截断位置（如 Realtime API 硬上限 8192） | 全部支持流式的接口 |
| `temperature` / `top_p` | number | 否 | 影响流式输出的随机性与连贯性；建议流式场景下适当降低 `temperature`（如 0.3–0.7）以提升首 token 稳定性 | 全部支持流式的接口 |

- **协议适配要点**：
  - OpenAI 兼容：解析 `data: {"choices":[{"delta":{"content":"..."},"index":0}]}`  
  - Anthropic 兼容：解析 `data: {"type":"content_block_delta","delta":{"text":"..."}}`  
  - DashScope 原生：解析 `{"output":{"text":"..."},"usage":{"input_tokens":...}}`（每个 chunk 包含完整 usage）  
  - Realtime/Omni Realtime：按事件类型（`content_block_delta`, `response_text_delta`, `audio_chunk`）分别处理，需实现事件分发逻辑  

- **客户端必备实践**：
  - 使用 `fetch` 的 `ReadableStream` 或 `EventSource`（HTTP）/ WebSocket（`onmessage`）接收流；
  - 实现 chunk 解析容错（跳过空行、`data:` 前缀、JSON 解析异常）；
  - 对 `finish_reason`（`stop`/`length`/`tool_calls`/`content_filter`）做业务判断，避免截断误判；
  - 流式场景下**务必设置超时**（推荐 60–120s），防止连接挂起。

面向开发者，请始终以实际接口文档为准：流式能力不是全局开关，而是由「模型 + 接口协议 + 部署版本」三者共同决定。调用前请通过 `GET /v1/models` 查询目标模型的 `capabilities` 字段（如 `"streaming": true`），并验证所用 endpoint 是否在[官方支持列表](https://help.aliyun.com/zh/model-studio/streaming-api-support)中。

## 关联主题页

- [test 1](../guides/test-1.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [release notes](../guides/release-notes.md)
- [more about models](../api/more-about-models.md)


