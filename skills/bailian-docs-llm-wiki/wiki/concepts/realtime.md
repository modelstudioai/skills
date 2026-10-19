# 实时交互

实时交互是指在用户与 AI 系统之间建立低延迟、流式、双向可控的会话通道，支持语音/文本/视频等多模态输入，并以增量方式（token 或音频帧）实时生成响应，同时允许客户端在会话中动态干预（如中断、暂停、切换轮次）。其核心目标是模拟自然对话节奏，端到端延迟通常控制在 300–800ms 以内，适用于智能客服、虚拟助手、同声传译、会议纪要等强时效性场景。

## 在百炼平台的不同场景中如何使用

- **Omni 多模态实时交互**：通过 `Qwen-Omni-Realtime` 系列模型（如 `qwen3.8-omni-flash-realtime`），基于 WebSocket / AOQ / WebRTC 协议实现音视频+文本混合输入与文本+音频混合输出。典型流程为：建连 → 收到 `session.created` → 调用 `session.update` 配置模态、VAD、工具等 → 流式发送音频 chunk 或文本事件 → 接收 `delta.text` 和/或 `delta.audio` 增量帧。

- **通用 Realtime API**：面向轻量级语音/文本流场景，使用 `qwen-audio-realtime`、`qwen2.5-7b-realtime` 等模型，通过标准 WebSocket 连接（`wss://dashscope.aliyuncs.com/realtime/v1/chat`）发起初始化帧（Init Frame），后续逐帧提交输入数据（如 PCM 音频 chunk），服务端以 Delta Frame 形式返回流式 token 或合成音频。

- **实时音视频套件集成**：结合 WebRTC（浏览器端）或 AOQ SDK（移动端/嵌入式），接入 `qwen3.8-livetranslate-flash-realtime`（实时翻译）、`fun-asr-realtime`（流式语音识别）等专用模型，由 SDK 封装媒体流采集、编解码、网络传输与事件调度，开发者只需关注业务逻辑（如 `input_audio_buffer.append()` → `.commit()` → 监听 `response.create`）。

## 关键参数和配置

| 参数 | 作用 | 典型值/约束 | 注意事项 |
|------|------|-------------|----------|
| `modalities`（Omni） | 指定输出模态 | `["text"]` 或 `["text","audio"]` | 必须显式声明；纯文本不触发 TTS |
| `turn_detection` | 控制说话轮次检测方式 | `{ "type": "server_vad", "threshold": 0.5, "silence_duration_ms": 800 }` | `server_vad`（声学）低开销；`semantic_vad`（语义）更准但需更高算力；设为 `null` 表示手动轮次控制（Manual Mode） |
| `audio.input.format` / `audio.output.format` | 音频编解码规格 | 输入：`{"type":"pcm","sample_rate":16000}`；输出：`{"type":"wav","sample_rate":24000}` | 多通道音频仅 `qwen3.8-omni-flash-realtime` 支持，且限 `pcm`+`16000`+`s16le`+`interleaved` |
| `stream=true`（通用 Realtime） | 强制启用流式响应 | `true`（必填） | Realtime API 不接受非流式调用；REST 风格请求将被拒绝 |
| `input_format`（通用 Realtime） | 声明输入数据类型 | `"audio/wav"`、`"text/plain"`、`"video/mp4"` | 音频必须为 16kHz/16bit/mono，否则报 `invalid_input_format` |
| `enable_search` / `tools` | 启用联网搜索或[函数调用](function-calling.md) | `true` / `[{"type":"function",...}]` | 二者互斥；不可与 `server_vad` 在同一会话中混用（需语义 VAD 或 Manual Mode） |
| `voice` / `audio.output.voice` | 指定合成音色 | `"longanlingxin"`、`"Tina"`、`"Cherry"` | 优先使用 `audio.output.voice`；旧字段 `session.voice` 仅兼容，已废弃 |

> ⚠️ 所有配置均通过 `session.update`（Omni）或 Init Frame（通用 Realtime）一次性提交，不支持运行时热更新。VAD 灵敏度、静音时长、温度（`temperature`）、最大输出长度（`max_tokens`）等参数直接影响响应及时性与稳定性，建议在真实设备上实测调优。

## 面向开发者的小贴士

- **首选 AOQ SDK**：比原生 WebSocket 更健壮，内置重连、帧序列化、带宽自适应与 QUIC 优化，Python/JS/Android/iOS 全平台支持；
- **连接生命周期 ≤ 300 秒**：超时后需重建连接；高并发场景建议复用连接池（AOQ）或预热连接；
- **避免阻塞主线程**：音频采集、编码、发送必须异步；推荐使用 Web Audio API（浏览器）或 AudioRecord（Android）配合后台线程处理；
- **调试从 VAD 开始**：若出现“抢话”或“响应滞后”，优先检查 `turn_detection.threshold` 和 `silence_duration_ms` 是否匹配实际环境噪声水平；
- **日志关键事件**：记录 `session.created`、`input.commit`、`response.start`、`response.end` 时间戳，用于端到端延迟归因分析。

## 关联主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [use cases](../guides/use-cases.md)


