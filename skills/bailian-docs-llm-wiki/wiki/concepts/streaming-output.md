# 流式输出

流式输出（Streaming Output）是指模型服务在生成响应过程中，将结果以增量方式分块、实时返回给客户端的通信模式，而非等待全部内容生成完毕后一次性返回。该机制显著降低端到端延迟，提升用户交互体验，是语音助手、实时对话、长文本生成等场景的关键能力。

## 在百炼平台的不同场景中如何使用

流式输出在百炼平台中并非单一接口特性，而是贯穿多个调用路径的通用能力，具体应用方式依协议与场景而异：

- **Realtime API（WebSocket）**：强制启用流式输出（`stream=true` 固定），通过 `output.delta` 事件逐 token 推送文本/音频片段，支持实时中断（`enable_interruption=true`）和上下文动态裁剪，适用于低延迟语音交互与音视频流处理。
  
- **Assistant / Application API（HTTP + SSE）**：通过 `stream=true` 参数启用服务器发送事件（SSE）流式响应；若需仅返回本次新增 token（避免重复回传历史内容），须额外设置 `incremental_output=true`，适用于 Web 端聊天界面、Agent 工具编排等需精细控制渲染节奏的场景。

- **Omni Realtime API（AOQ/WebSocket/WebRTC）**：默认启用多模态流式输出（文本+音频），通过 `modalities: ["text", "audio"]` 控制输出类型，并利用 `output.delta`（文本）与 `output.audio.delta`（音频 PCM/WAV 片段）事件实现毫秒级同步；VAD（语音活动检测）与 `smooth_output` 等参数进一步优化流式语音自然度。

- **标准模型 API（REST）**：不原生支持流式输出；如需流式能力，必须切换至 Realtime 或 Assistant API 对应的流式端点，不可在 `/v1/services/aigc/text-generation/generation` 等同步接口中设置 `stream=true`（将被忽略或报错）。

## 关键参数和配置

| 参数名 | 所属场景 | 类型 | 说明 | 默认值 | 注意事项 |
|--------|----------|------|------|--------|----------|
| `stream` | 全场景（Realtime / Assistant / Omni） | `boolean` | 启用流式响应 | Realtime：必填 `true`；Assistant：`false`；Omni：隐式启用 | Realtime API 中不可设为 `false`；Assistant API 中设为 `true` 后响应格式为 SSE |
| `incremental_output` | Assistant / Application API | `boolean` | 在 `stream=true` 下启用增量 token 输出（仅返回本次新增内容） | `false` | 避免前端重复拼接，推荐生产环境开启 |
| `enable_interruption` | Realtime API | `boolean` | 允许客户端发送 `interrupt` 事件中止当前响应流 | `false` | 需配合 WebSocket 客户端逻辑实现“边说边停” |
| `max_output_tokens` / `max_tokens` | Realtime / Omni | `integer` | 单次响应最大输出 token 数（硬限制） | Realtime：1024；Omni：依模型而异（如 `qwen3.8`: 65536） | 超限将截断并触发 `output.end` 事件 |
| `modalities` | Omni Realtime API | `array<string>` | 指定输出模态，如 `["text"]` 或 `["text","audio"]` | `["text","audio"]` | 必须显式声明，否则音频输出不会触发 |

> ⚠️ 注意：`stream` 是功能开关，但**流式协议本身由接口类型决定**——Realtime API 强制 WebSocket 流式，Assistant API 使用 HTTP/SSE 流式，二者不可混用；错误地在 REST 接口传 `stream=true` 将导致无效或报错。

## 面向开发者：简洁实用建议

- ✅ **首选 Realtime API**：若需 <500ms 端到端延迟、语音输入/输出、实时中断，直接使用 `wss://dashscope.aliyuncs.com/realtime/v1/chat`，无需额外配置 `stream`。
- ✅ **Web 应用选 Assistant API + SSE**：前端用 `EventSource` 接收 `data:` 块，配合 `incremental_output=true` 实现平滑打字效果；注意处理 `event: error` 和重连逻辑。
- ✅ **音频流务必校验格式**：Realtime/Omni 的音频输入仅支持 PCM（16-bit, 16kHz mono）；输出格式（`pcm`/`wav`）和采样率（如 24000 Hz）需与模型能力匹配，详见各模型文档。
- ❌ **勿在标准 REST API 中尝试流式**：`/v1/services/aigc/text-generation/generation` 等接口不支持流式，`stream` 参数无效。
- 🛠️ **调试技巧**：使用 `curl -N` 或 Postman 的 SSE 模式观察流式事件；WebSocket 场景推荐使用 [AOQ SDK](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api.md) 封装连接与事件解析。

## 关联主题页

- [realtime api user guide](../api/realtime-api-user-guide.md)
- [application support](../guides/application-support.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [get started with models](../guides/get-started-with-models.md)


