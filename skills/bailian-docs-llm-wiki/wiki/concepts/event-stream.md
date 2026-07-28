# 事件流

事件流（Event Stream）是百炼平台中智能体与客户端之间传递原子消息的机制，涵盖会话状态变更、用户输入、工具调用回执、模型增量输出等。在 Managed Agents API 中通过 SSE（Server-Sent Events）单向推送，在 Realtime API 中通过 WebSocket 双向收发，两者共享"事件即会话内最小消息单元"的语义。

## 在百炼平台中的使用场景

### Managed Agents API 的 SSE 事件流

Managed Agents 会话（Session）内所有交互以 Event 记录存储。开发者通过 REST API 注入事件，并通过 SSE 长连接实时接收平台产生的事件：

- **发送事件**：`POST /sessions/{session_id}/events` — 注入用户消息、工具审批结果、[函数调用](function-calling.md)返回值等。
- **订阅事件流**：`GET /sessions/{session_id}/events/stream` — 建立 SSE 长连接，流式接收实时事件推送，包括状态机流转（`idle` → `running` → `idle` / `terminated`）、工具调用回执等。
- **查询历史**：`GET /sessions/{session_id}/events` — 分页列出会话的事件历史。

Event 类型包括用户消息、工具调用回执、状态变更等，是会话生命周期内不可变的消息记录。

### Realtime API 的双向事件流

Realtime API 基于 WebSocket（以及 WebRTC、AOQ 协议），通过客户端事件与服务端事件的双向交互实现低延迟实时对话：

**客户端事件**（Client → Server）：

| 事件 | 用途 |
| --- | --- |
| `session.update` | 更新会话配置（模态、音色、VAD、工具等） |
| `input_audio_buffer.append` | 追加音频数据（Base64 编码） |
| `input_audio_buffer.commit` | 提交音频缓冲区（Manual 模式必需） |
| `input_audio_buffer.clear` | 清空音频缓冲区 |
| `input_image_buffer.append` | 追加图像数据 |
| `response.create` | 触发模型生成响应 |
| `response.cancel` | 取消正在进行的响应 |
| `conversation.item.create` | 回传工具调用结果 |

**服务端事件**（Server → Client）：

| 事件 | 含义 |
| --- | --- |
| `session.created` | 连接建立，返回默认配置 |
| `session.updated` | 会话配置更新成功 |
| `error` | 错误信息 |
| `input_audio_buffer.speech_started` | VAD 检测到语音开始 |
| `input_audio_buffer.speech_stopped` | VAD 检测到语音结束 |
| `input_audio_buffer.committed` | 音频缓冲区已提交 |
| `response.audio.delta` | 增量音频输出 |
| `response.audio_transcript.delta` | 增量文本转录 |
| `response.done` | 响应完成 |
| `response.function_call_arguments.done` | 工具调用参数完成 |
| `conversation.item.input_audio_transcription.delta` | 实时语音识别中间结果 |

## 关键参数与配置

### Managed Agents API

事件交互无额外配置，事件结构由发送时的 payload 决定。Session 状态机（`idle` → `running` → `idle` / `terminated`）驱动事件流转，归档后 Session 进入 `terminated` 终态不再产生新事件。删除 Session 会硬删除全部事件历史。

### Realtime API

会话参数通过 `session.update` 客户端事件配置：

| 参数 | 说明 | 默认值 |
| --- | --- | --- |
| `modalities` | 输出模态：`["text"]` 或 `["text","audio"]` | `["text","audio"]` |
| `turn_detection.type` | VAD 类型：`server_vad` / `semantic_vad` | `server_vad` |
| `turn_detection.threshold` | VAD 灵敏度，范围 [-1.0, 1.0] | 0.5 |
| `turn_detection.silence_duration_ms` | 静音触发时间（ms），范围 [200, 6000] | 800 |

交互模式分两种：VAD 模式下服务端自动检测语音起止并触发响应，支持语音打断；Manual 模式下由客户端通过 `input_audio_buffer.commit` + `response.create` 手动控制对话节奏。

## 协议与鉴权

事件流依赖底层传输协议的建连鉴权：

- **Managed Agents API**：REST 请求通过 `Authorization: Bearer <API Key>` 鉴权，SSE 流复用同一会话的鉴权上下文。
- **Realtime API WebSocket**：握手时携带 API Key，建连成功后无需重复鉴权。
- **Realtime API AOQ**：采用服务端代理鉴权，API Key 仅保留在 AppServer 侧，客户端使用网关返回的临时 Token 建连。

三种 Realtime 传输协议（WebSocket、WebRTC、AOQ）在弱网表现和端侧支持上差异显著：WebSocket 接入门槛最低适合服务端集成；WebRTC 浏览器原生支持内置回声消除；AOQ 基于 QUIC 抗弱网能力最强，提供移动端原生 SDK。

## 关联主题页

- [managed agents api](../api/managed-agents-api.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../guides/realtime-api-user-guide.md)


