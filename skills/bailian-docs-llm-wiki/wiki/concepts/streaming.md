# 流式输出

流式输出（Streaming Output）是指模型服务在生成响应过程中，将结果以增量方式分块（chunk）实时返回给客户端，而非等待全部内容生成完毕后一次性返回。这种方式显著降低端到端延迟，提升用户感知的响应速度，并支持实时渲染、语音合成、中断控制等交互场景。

## 在百炼平台的不同场景中如何使用

流式输出是百炼平台多项核心能力的基础机制，具体应用因调用方式和模型类型而异：

- **标准大模型 API（`/v1/chat/completions`）**：通过请求参数 `stream=true` 启用。响应为 Server-Sent Events（SSE）格式，每帧包含一个 `delta` 字段（增量文本），客户端需按行解析并拼接完整响应。适用于 Web 控制台、聊天 UI、代码补全等需要“边生成边展示”的场景。

- **智能体与工作流调用（Application Call）**：同样通过 `stream=true` 开启。除基础文本流外，还支持：
  - `incremental_output=true`：启用更细粒度的 token 级增量（如单字/词级）；
  - `flow_stream_mode=message_format_plus`：工作流节点级流式推送，可区分不同节点的输出来源；
  - `enable_thinking=true` + `has_thoughts=true`：同步流式返回思考过程（如 Chain-of-Thought 中间步骤）。

- **Realtime API（WebSocket/AOQ/WebRTC）**：**必须启用流式**（`stream=true` 为强制参数）。采用二进制或 JSON 帧协议，每帧携带 `delta`、`audio_chunk` 或 `event` 类型字段，支持毫秒级低延迟传输。适用于语音助手、实时会议纪要、音视频流处理等强实时场景。

- **Omni Realtime API（多模态[实时交互](realtime.md)）**：基于 WebSocket 或 AOQ 协议，天然流式设计。文本输出以 `text_delta` 帧持续推送；音频输出以 `audio_delta` 帧（PCM/WAV raw data）实时下发，可直接喂入播放器或 ASR 模块，实现“说一半、听一半”的自然交互。

## 关键参数和配置

| 参数名 | 类型 | 作用 | 默认值 | 注意事项 |
|--------|------|------|--------|----------|
| `stream` | boolean | 全局开关：启用流式输出 | `false`（REST）、`true`（Realtime） | 所有支持流式的接口均需显式设置；Realtime API 中为必填且必须为 `true` |
| `incremental_output` | boolean | （Application Call 专用）启用更细粒度的增量输出（如单 token） | `false` | 仅 DashScope 协议支持；开启后 `delta` 内容更小、频率更高，适合高精度渲染 |
| `flow_stream_mode` | string | （Workflow 专用）指定工作流流式输出格式 | `"message"` | 可选 `"message"`（默认）或 `"message_format_plus"`（含节点 ID 和元数据） |
| `enable_thinking` / `has_thoughts` | boolean | （Application Call）流式返回推理过程 | `false` | 需同时设为 `true` 才生效；思考内容通过 `thought` 字段流式推送 |

> ⚠️ 注意：  
> - 流式响应的 HTTP 状态码始终为 `200 OK`，错误需通过响应流中的 `error` 事件帧判断；  
> - 客户端必须正确处理 SSE 的 `data:` 前缀、空行分隔及重连逻辑（Realtime API 则需处理 WebSocket `close` 与重连）；  
> - 流式调用不改变配额计费逻辑：仍按实际生成的总 token 数计费，与是否流式无关。

## 面向开发者提示

- **首选官方 SDK**：Python/JS/Android/iOS 的 DashScope SDK 已内置流式解析器（如 `StreamResponseIterator`），避免手动处理 SSE 或 WebSocket 帧解析；
- **务必设置超时**：流式连接可能因网络或模型卡顿长时间无响应，建议设置 `timeout=60s`（REST）或 `ping_interval=30s`（WebSocket）；
- **增量内容需拼接**：`delta.content` 是当前 chunk 的文本片段，完整响应 = 所有 `delta.content` 拼接（注意空格、标点连续性）；
- **错误处理在流内**：不要依赖 HTTP 状态码判断失败，监听 `event: error` 帧或 `{"error":{...}}` 结构；
- **调试建议**：用 `curl -N` 或浏览器 DevTools 的 Network → EventStream 查看原始流，确认分块节奏与内容完整性。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [application call](../api/application-call.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)


