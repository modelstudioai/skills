# 流式输出

流式输出（Streaming Output）是指模型响应以增量方式分块返回，而非等待全部生成完成后再一次性返回完整结果。它通过持续的数据流（如 WebSocket 帧、SSE 事件或二进制音频 chunk）实时传递 token、文本片段或音视频数据，显著降低端到端延迟，提升交互自然性与用户体验。

## 在百炼平台的不同场景中，这个概念如何使用

流式输出在百炼平台中并非单一能力，而是贯穿多个 API 层级的底层交互范式，具体应用如下：

- **Realtime API（语音/多模态实时交互）**：基于 WebSocket 双向流，支持 `token`（文本 token）、`audio`（PCM/WAV 音频 chunk）、`vad`（语音活动检测事件）等细粒度事件实时下发；客户端可随时发送 `interrupt` 或 `pause` 指令实现语义级中断，适用于语音助手、会议纪要等低延迟场景。

- **Application Call（AI 应用调用）**：通过 `stream=true` 启用 SSE 流式响应，服务端按 `event: message` 返回逐个 token 的 `content` 字段；注意：工具调用结果（`tool_calls`）仅在最终 `event: done` 中完整返回，中间流不包含该结构。

- **Qwen API（通用大模型调用）**：所有 [OpenAI 兼容接口](openai-compatible-api.md)（`chat/completions`）、Anthropic 兼容接口（`messages`）及 DashScope 原生接口均支持 `stream=true` 参数；返回格式遵循对应协议规范（如 OpenAI 的 `delta.content`），适用于对话机器人、代码补全等需要渐进式反馈的场景。

- **Omni Realtime API（多模态实时大模型）**：在 `modalities: ["text", "audio"]` 模式下，文本 token 与音频帧同步流式输出；音频支持 `wav`/`pcm` 格式及 `24000` Hz 采样率，且 VAD 触发后可动态启停音频流，实现“说-听-说”无缝衔接。

- **Application Support（应用层增强）**：除基础流式外，支持 `incremental_output=true`（需配合 `stream=true`），确保每次响应仅包含新增 token，避免重复回传历史内容，降低带宽消耗并简化前端渲染逻辑。

## 关键参数和配置

| 参数名 | 所属接口 | 类型 | 说明 | 默认值 |
|--------|----------|------|------|--------|
| `stream` | 全部（Realtime / Application Call / Qwen API） | `boolean` | 启用流式响应模式 | `false` |
| `incremental_output` | Application Call / Application Support | `boolean` | 在流式下启用增量输出（仅返回新 token） | `false` |
| `audio.output.format.type` | Omni Realtime / Realtime API | `string` | 音频输出编码格式：`pcm` 或 `wav` | `"wav"`（Omni）、`"pcm"`（Realtime） |
| `audio.output.format.sample_rate` | Omni Realtime（实际支持） | `integer` | 音频输出采样率，支持 `24000`（文档已确认） | `24000` |
| `max_output_tokens` / `max_tokens` | Realtime API / Qwen API / Application Call | `integer` | 控制流式响应的最大输出长度，超限触发 `stop` 事件 | 按模型能力设定 |

> ⚠️ 注意：  
> - Realtime API 和 Omni Realtime API **不支持 HTTP/REST 流式**，必须使用 WebSocket 或 WebRTC 协议；  
> - Application Call 的流式响应为 SSE（Server-Sent Events），需客户端正确解析 `data:` 字段；  
> - `incremental_output=true` 仅在 Application Call 中生效，其他接口默认即为增量行为（如 [OpenAI 兼容接口](openai-compatible-api.md)的 `delta` 字段天然增量）。

## 面向开发者，简洁实用

- ✅ **首选流式**：对延迟敏感场景（语音、实时对话），优先选用 Realtime 或 Omni Realtime API；对通用文本生成，直接在 Qwen API 或 Application Call 中设置 `stream=true`。  
- ✅ **处理音频流**：Omni Realtime 中，`audio.output.format.type="wav"` 可直接用于浏览器 `<audio>` 播放；若需低延迟合成，建议用 `pcm` + `sample_rate=24000` 配合 Web Audio API。  
- ✅ **中断与容错**：Realtime 系列支持语义级 `interrupt`，比 TCP 断连更可靠；Application Call 流式无中断机制，超时需由客户端控制重试。  
- ✅ **前端渲染建议**：接收流式 token 后，立即追加至 DOM（避免清空重绘），对 Markdown 内容需自行解析（平台不提供富文本转换）。  
- ❌ **避免陷阱**：不要在流式请求中混用 `stream=false` 参数；`tool_calls` 不会在 Application Call 的中间流中出现；`qwen-omni-turbo-realtime` 等部分模型禁用 `temperature` 等采样参数，配置将被忽略。

## 关联主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [application call](../api/application-call.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [application support](../guides/application-support.md)


