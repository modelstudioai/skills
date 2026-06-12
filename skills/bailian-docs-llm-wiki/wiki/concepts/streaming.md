# 流式输出

流式输出（Streaming）是指服务端在生成结果的过程中，将数据分片逐步返回给客户端的传输方式，而非等待完整结果生成后再一次性返回。在百炼平台中，流式输出广泛应用于文本生成、语音合成、音乐生成等场景，可显著降低首次响应延迟，提升用户体验。

## 百炼平台中的流式输出场景

### 文本生成

通义千问（Qwen）系列模型支持通过 [OpenAI 兼容接口](openai-compatible-api.md)、[DashScope 接口](dashscope-api.md)等进行流式文本生成。设置 `stream=true` 后，模型会以 Server-Sent Events（SSE）协议逐 token 推送生成内容，客户端可边接收边渲染，实现"打字机"效果。

### 实时多模态交互

Qwen-Omni-Realtime API 基于 WebSocket 协议，天然支持流式双向通信。服务端通过 `response.audio.delta` 等事件逐帧返回音频数据，同时通过 `response.text.delta` 返回文本转录，实现低延迟的实时语音对话。

### 语音合成

百炼平台的语音合成引擎均支持流式输出：

- **Qwen-TTS**：非实时模式通过 HTTP 流式返回音频；实时模式（Qwen-TTS-Realtime）通过 WebSocket 事件驱动，支持流式文本输入和实时音频输出。
- **CosyVoice**：通过 WebSocket 协议的 `continue-task` 事件实现流式文本追加与实时音频合成。
- **Sambert**：仅支持一次性输入（`run-task`），不支持流式输入。

### 音乐生成

Fun-Music API 支持 SSE 流式输出模式。请求时设置 `X-DashScope-SSE: enable` 请求头后，服务端以 SSE 事件逐步返回 Base64 编码的音频片段（`output.audio.data`），最终消息中附带完整音频的 OSS 下载链接。

### 应用调用

百炼智能体应用和工作流应用的 API 同样支持流式输出，通过设置 `stream=true` 或对应 SDK 参数，可以逐步接收应用的回复内容。

## 关键参数和配置

### HTTP / REST 接口

| 参数 / 请求头 | 说明 |
| --- | --- |
| `stream` | 设为 `true` 启用流式输出，响应以 SSE 格式逐段返回 |
| `X-DashScope-SSE` | 设为 `enable` 启用 SSE 流式（DashScope 原生接口使用） |

### WebSocket 接口

WebSocket 协议本身即为双向流式通信，无需额外参数即可获得流式输出。服务端通过事件（如 `response.audio.delta`、`response.text.delta`）逐帧推送数据，客户端监听对应事件即可实时处理。

### 流式响应的通用结构

- **中间消息**：包含增量数据片段，`finish_reason` 通常为 `null`
- **最终消息**：`finish_reason` 为 `stop`，可能附带完整结果的汇总信息（如完整音频 URL、用量统计等）

## 流式与非流式的选择建议

| 场景 | 推荐模式 | 理由 |
| --- | --- | --- |
| 实时对话、聊天机器人 | 流式 | 降低首 token 延迟，提升交互体感 |
| 实时语音合成 | 流式 | 边合成边播放，减少等待时间 |
| 批量离线处理 | 非流式 | 实现简单，一次获取完整结果 |
| 需要完整结果后再处理 | 非流式 | 避免拼接逻辑，降低客户端复杂度 |

## 注意事项

- 流式模式下客户端需要自行拼接增量数据以获得完整结果。
- 不同接口的流式协议有所差异：HTTP 接口使用 SSE，WebSocket 接口使用事件驱动，开发者需根据所选接口适配解析逻辑。
- 部分功能（如音乐生成的歌词长度限制）在流式与非流式模式下存在差异，请参考对应 API 文档确认具体约束。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [speech synthesis api reference](../api/speech-synthesis-api-reference.md)
- [audio api references](../api/audio-api-references.md)
- [music generation references](../api/music-generation-references.md)
- [bailian application calling](../guides/bailian-application-calling.md)


