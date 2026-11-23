# 流式输出

流式输出（Streaming Output）是指模型服务在生成响应过程中，将结果以增量方式、按 token（或帧、chunk）为单位持续返回给客户端，而非等待全部内容生成完毕后一次性返回。这种方式显著降低端到端延迟，提升用户感知的响应实时性，适用于对话交互、实时语音处理、长文本生成等对低延迟敏感的场景。

## 在百炼平台的不同场景中，这个概念如何使用

- **文本生成（同步 API）**：通过 HTTP POST 请求调用 `/text-generation/generation` 等端点时，设置 `stream=true` 参数，即可启用逐 token 流式响应。响应体为 Server-Sent Events（SSE）格式，每行以 `data:` 开头，包含一个 JSON 对象（如 `{"output": {"text": "今"}}`），客户端需按行解析并拼接。

- **CLI 工具**：`bailian chat` 命令支持 `--stream` 标志（如 `bailian chat --model qwen-max --prompt "你好" --stream`），输出将以实时滚动方式打印，便于调试和终端交互。

- **实时音视频 API（WebSocket）**：所有实时模型（如 `qwen-audio-realtime`、`qwen2-asr-16k`、`qwen-omni-realtime`）**强制要求流式传输**，通过 WebSocket 连接持续收发事件（如 `output.text`、`output.audio`）。其中 `is_final: true` 字段标识最终结果，中间结果（partial transcript、临时音频 chunk）可直接用于 UI 渲染或前端反馈。

- **应用层（Agent/RAG）**：在构建 AI 应用时，可通过 `stream=True` 启用流式输出；若需更精细控制增量更新（避免重复渲染），可额外指定 `incremental_output=True`，此时每次返回仅含本次新增 token，而非累计全文。

> ⚠️ 注意：流式输出与结构化输出（如 `response_format: json`）互斥——二者不可同时启用，否则将导致解析失败或服务端拒绝。

## 关键参数和配置

| 参数名 | 类型 | 说明 | 所属场景 |
|--------|------|------|----------|
| `stream` | boolean | 必填（实时 API）或可选（HTTP API）；设为 `true` 启用流式响应 | 全部模型 API（REST & WebSocket） |
| `incremental_output` | boolean | 仅在应用层（Agent/RAG）有效；设为 `true` 时，每次流式事件仅返回新增内容（非全量重发） | Application Support（Agent/RAG） |
| `response_format` | string | 仅支持 `json`；**不可与 `stream=true` 同时使用** | CLI、HTTP API（文本生成） |
| `enable_silence_detection` | boolean | 实时 ASR/TTS 场景中，需显式设为 `true` 才启用静音检测逻辑 | Realtime API（ASR/TTS） |

- **HTTP 流式响应头要求**：客户端需设置 `Accept: text/event-stream`，并正确处理 SSE 协议（忽略空行、解析 `data:` 字段、处理 `event:` 类型）。
- **WebSocket 流式约束**：必须严格遵循握手流程（先 `session.update`，待收到 `session.updated` 后再发送媒体流），否则中间结果可能丢失。

## 面向开发者，简洁实用

- ✅ **推荐做法**：  
  - 对话类应用默认启用 `stream=true`，配合前端打字机效果提升体验；  
  - 实时语音场景务必使用 WebSocket + `stream=true`，禁用任何轮询替代方案；  
  - 解析流式响应时，始终检查 `is_final` 字段判断是否为终态结果（尤其在 ASR/TTS 中）；  
  - 使用 SDK 时，优先选用内置流式方法（如 Python SDK 的 `Generation.call(..., stream=True)`），避免手动解析 SSE。

- ❌ **禁止行为**：  
  - 在流式请求中传入 `response_format=json` 或 `--response-format json`；  
  - 对实时 API 使用 HTTP GET/POST 轮询模拟流式（将返回 `405 Method Not Allowed`）；  
  - 忽略 `is_final` 字段直接将 partial 结果作为最终答案（易导致语义错误）。

- 🛠 **调试提示**：  
  - 若流式响应中断，检查 WebSocket 连接是否超时（实时会话最长 300 秒）、网络是否丢包；  
  - HTTP 流式请求超时请调高客户端 timeout（建议 ≥ 120s），避免因网络抖动被提前终止；  
  - CLI 流式输出异常时，运行 `bailian chat --help` 确认当前版本是否支持 `--stream`（v2.0+）。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [getting started](../guides/getting-started.md)
- [realtime api directory](../api/realtime-api-directory.md)
- [api overview](../api/api-overview.md)
- [more about models](../api/more-about-models.md)
- [application support](../guides/application-support.md)


