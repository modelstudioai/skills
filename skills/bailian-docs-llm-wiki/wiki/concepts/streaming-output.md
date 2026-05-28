# 流式输出

流式输出（Streaming Output）是一种服务端边推理边推送的通信模式，通过 SSE 或 WebSocket 协议将模型生成的文本 Token 或音频数据分片实时下发至客户端，以显著降低首字节延迟（TTFT）并实现低延迟交互体验。

## 不同场景的使用方式
在百炼平台中，流式输出覆盖多模态与业务交互场景，具体应用方式如下：
* **文本生成与应用调用**：在 [[智能体应用]] 与 [[工作流应用]] 中，开启流式可实现对话内容的实时逐字渲染。适用于长文本生成、复杂工作流状态实时反馈及多轮上下文交互。
* **语音处理 (TTS/ASR)**：
  * **语音合成**：支持 HTTP SSE 与 WebSocket 双向流。模型按生成节奏分片下发音频帧，适用于语音助手与实时播报。
  * **语音识别**：实时流式转写持续接收客户端音频二进制流，配合断句策略输出中间/最终识别结果，适用于直播字幕与语音交互。
* **音乐生成**：基于 SSE 协议分片返回 Base64 编码的音频数据块，避免长音频生成时的长时间阻塞，最终返回完整下载链接与歌词元数据。

## 关键参数与配置
| 参数/配置项 | 适用协议/接口 | 说明与默认值 |
|:---|:---|:---|
| `stream` | HTTP REST / OpenAI 兼容 | 布尔值。设为 `true` 开启 SSE 流式响应。默认 `false`。 |
| `X-DashScope-SSE` | HTTP Header | 字符串。设为 `enable`，用于 TTS、音乐生成等 DashScope 原生 HTTP 接口。 |
| `incremental_output` | 应用调用 | 布尔值。配合 `stream=true` 使用，确保仅返回增量内容，避免历史重复累积。 |
| `turn_detection` | 语音识别 (ASR) | 对象/布尔值。配置 `server_vad` 开启服务端自动断句；设为 `null` 切换为客户端 Manual 模式。 |
| `format` / `sample_rate` | 语音/音乐 | 字符串/整型。指定流式音频编码（`pcm`/`mp3`/`opus`/`wav`）与采样率，客户端需严格对齐解码。 |

## 协议选择与集成建议
* **HTTP + SSE**：适用于对延迟容忍度较高、无需双向实时交互的场景（如应用文本补全、非实时 TTS/音乐生成）。前端需使用 `EventSource` 或兼容库解析 `data: ` 字段并流式拼接。
* **WebSocket (wss)**：适用于低延迟、需双向控制的场景（如实时语音助手、直播字幕转写）。需严格遵循各模型的事件流规范（如 TTS 的 `run-task` → `continue-task` → 二进制帧 → `finish-task`）。
* **SDK 集成**：强烈推荐使用官方 [[DashScope SDK]]。SDK 已封装 `streaming_call()` 或异步回调方法，自动处理鉴权、长连接保活、二进制流拼接与异常重试，大幅降低接入复杂度。

## 限制与注意事项
* **互斥限制**：流式输出 (`stream: true`) 与异步任务模式 (`background: true` 或 `X-DashScope-Async: enable`) **互斥**，同一请求中不可同时开启。
* **输入长度差异**：部分模型（如音乐生成）在流式模式下对 `[[prompt|prompt]]` 或 `lyrics` 的长度限制更为严格，超出阈值或过短均会触发校验失败。
* **协议能力边界**：部分传统模型（如 Sambert TTS）仅支持单向流式，文本必须在初始化事件中一次性完整发送；实时 WebSocket 模型通常不支持 Function Calling 与联网搜索同时开启。
* **前端渲染规范**：流式返回的文本默认包含标准 Markdown 语法，业务侧需集成解析库（如 `marked.js`）进行实时 DOM 转换，不可直接渲染纯文本。
* **连接生命周期管理**：WebSocket 双向流式调用结束后，必须显式发送结束指令（如 `finish-task` 或调用 SDK 的 `streaming_complete()`），否则服务端可能无法输出尾部数据并导致连接泄漏。

## 相关主题
* [[模型推理]]
* [[应用调用]]
* [[语音处理]]
* [[DashScope SDK]]
* [[智能体应用]]
* [[工作流应用]]

## 关联主题页

- [[model-inference|model inference]] — `../guides/model-inference.md`
- [[music-generation-references|music generation references]] — `../api/music-generation-references.md`
- [[speech-synthesis-api-reference|speech synthesis api reference]] — `../api/speech-synthesis-api-reference.md`
- [[speech-recognition-api-reference|speech recognition api reference]] — `../api/speech-recognition-api-reference.md`
- [[application-call|application call]] — `../api/application-call.md`
- [[application-[[support|support]]|application support]] — `../guides/application-[[support|support]].md`

