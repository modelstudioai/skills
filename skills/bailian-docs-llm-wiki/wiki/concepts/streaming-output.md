# 流式输出

流式输出（Streaming Output）是百炼平台将 AI 模型的生成结果以增量分片方式持续推送给客户端的技术，区别于传统"等待完整结果后一次性返回"的同步模式。它显著降低了首字节延迟，使语音合成、实时对话、音乐生成等场景可以在模型仍在生成后续内容时就开始播放或处理已到达的部分。

## 两种协议形态

百炼平台的流式输出根据场景分为两类协议：

| 协议 | 适用场景 | 特点 |
| --- | --- | --- |
| **WebSocket 双向流** | 实时语音合成（CosyVoice、Qwen-TTS Realtime）、实时语音识别（Fun-ASR、Paraformer、Qwen-ASR）、实时多模态对话（Qwen-Omni-Realtime） | 客户端与服务端保持长连接，双向持续收发数据；延迟最低，适合实时交互 |
| **HTTP SSE（Server-Sent Events）** | 非实时语音合成（CosyVoice HTTP、Qwen-TTS 非实时）、音乐生成（Fun-Music） | 客户端发起单次 HTTP 请求，服务端通过 SSE 分块返回；接入简单，适合单向推送 |

## 在百炼各场景中的使用方式

### 实时语音合成（WebSocket）

CosyVoice 和 Qwen-TTS Realtime 通过 WebSocket 进行实时流式合成：

- **CosyVoice**：客户端通过 `run-task` → 多次 `continue-task`（携带文本片段）→ `finish-task` 三步事件驱动合成，服务端将音频以二进制分片持续推回。
- **Qwen-TTS Realtime**：提供 ServerCommit（服务端自动判断分段）和 Commit（客户端显式提交）两种模式；音频通过 `response.audio.delta`（Base64 编码）分片下发。

### 实时语音识别（WebSocket）

- **Fun-ASR / Paraformer 实时**：客户端持续发送音频流，服务端持续推送 `result-generated` 事件，其中包含中间结果（`sentence_end=false`）和最终结果（`sentence_end=true`）。
- **Qwen-ASR 实时**：支持 VAD 自动断句和 Manual 手动提交两种模式，持续返回识别结果。

### 实时多模态对话（WebSocket）

Qwen-Omni-Realtime 将语音输入、图像输入与模型响应整合在一条 WebSocket 连接中。模型的语音输出通过 `response.audio.delta` 流式下发，客户端收到分片即可开始播放，无需等待整句合成完毕。

### 非实时合成与音乐生成（HTTP SSE）

对于非交互场景，可通过在 HTTP 请求头中添加 `X-DashScope-SSE: enable` 启用流式返回：

- **非实时 CosyVoice / Qwen-TTS**：开启 SSE 后，音频数据以分片形式逐步返回。
- **音乐生成（Fun-Music）**：中间消息的 `output.audio.data` 为 Base64 音频片段（`finish_reason` 为 `"null"`），最终消息补全完整音频 URL、歌词、采样率等元信息（`finish_reason` 为 `stop`）。

## 关键参数与配置

### SSE 流式输出

| 参数 | 位置 | 说明 |
| --- | --- | --- |
| `X-DashScope-SSE` | HTTP 请求头 | 设为 `enable` 启用 SSE 流式返回 |

### WebSocket 流式输出

不同模型的交互事件和参数有所差异，常见配置包括：

| 参数 | 适用模型 | 说明 |
| --- | --- | --- |
| `format` | CosyVoice / ASR 系列 | 音频编码格式：`pcm`、`wav`、`mp3`、`opus` |
| `sample_rate` | CosyVoice / ASR 系列 | 采样率，如 16000、24000、44100、48000 Hz |
| `turn_detection` | Qwen-Omni-Realtime / Qwen-ASR | 交互模式：`server_vad`（自动断句）、`semantic_vad`（语义断句）或 `null`（手动模式） |
| `mode` | Qwen-TTS Realtime | `ServerCommit`（服务端分段）或 `Commit`（客户端显式提交） |

### 流式响应的消息结构

- **WebSocket**：通过事件类型区分中间结果与最终结果（如 `result-generated` 的 `sentence_end` 字段、`response.audio.delta` 与 `response.audio.done`）。
- **SSE**：通过 `finish_reason` 字段判断——`"null"` 表示中间片段，`"stop"` 表示生成结束。

## 开发者建议

1. **优先选择 WebSocket**：需要实时交互（对话、同传、实时播报）的场景务必使用 WebSocket 协议，SSE 无法满足双向低延迟需求。
2. **及时消费分片**：流式输出的价值在于"边生成边播放/展示"，客户端应做好缓冲区管理，避免攒齐所有分片后再处理。
3. **正确处理结束信号**：无论 WebSocket 还是 SSE，都需要监听结束事件（`done` / `finish_reason: stop`）后再执行清理或拼接最终结果。
4. **关注地域差异**：WebSocket 和 SSE 端点按华北2（北京）与新加坡分别提供，新加坡地域需使用新版 `{WorkspaceId}` 域名。

## 关联主题页

- [speech synthesis api reference](../api/speech-synthesis-api-reference.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [speech recognition api reference](../api/speech-recognition-api-reference.md)
- [music generation references](../api/music-generation-references.md)
- [audio api references](../api/audio-api-references.md)


