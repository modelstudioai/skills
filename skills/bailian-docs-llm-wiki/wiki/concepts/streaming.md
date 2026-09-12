# 流式输出

流式输出（Streaming Output）是指模型服务在生成响应过程中，不等待全部内容完成，而是以增量方式（如逐 token、逐帧或逐 chunk）持续向客户端推送结果的通信模式。该模式显著降低端到端延迟，提升用户体验，尤其适用于实时对话、语音交互、长文本生成等对响应速度敏感的场景。

## 在百炼平台的不同场景中，这个概念如何使用

流式输出在百炼平台中并非单一接口特性，而是贯穿多个 API 范式的**核心交互范式**，具体体现为以下三类实现：

- **RESTful 流式（SSE）**：  
  通过标准 HTTP POST 调用 `/v1/chat/completions` 等接口时，设置 `stream=true`，服务端按 Server-Sent Events（SSE）协议返回多行 `data: {...}` 响应。每行包含一个增量片段（如 `content.delta`），客户端需逐行解析、拼接并实时渲染。适用于通用文本生成、[函数调用](function-calling.md)（`tool_choice="auto"`）、结构化输出（JSON Schema 模式除外）等场景。

- **Realtime API（WebSocket）**：  
  专为低延迟设计，基于 WebSocket 协议建立长连接。客户端发送 `session.create` 帧后，服务端以事件帧（如 `content.delta`、`response.text.delta`）形式逐 token 或逐音频块推送响应。支持动态中断（`session.cancel`）、上下文保持与双向指令交互，适用于实时语音对话、流式 ASR/TTS、[多模态](multi-modal.md)协同等强实时性需求。

- **Audio/Video 相关流式能力**：  
  - 音频类 API（如 TTS、ASR 实时模式）通过 `response_format=stream` 参数启用流式响应，返回二进制音频流或 SSE 文本流；  
  - Omni Realtime API 采用纯二进制帧传输音频输入，并同步返回文本 delta 与音频 delta 事件，实现毫秒级端到端流式闭环；  
  - 视频生成 API 当前**不支持流式输出**，所有视频任务均为异步生成，返回 `video_url` 下载链接。

> ⚠️ 注意：流式能力与模型强绑定。例如 `qwen-audio` 仅在 Realtime API 中支持流式 ASR；`qwen-omni-realtime` 专属模型不兼容 RESTful 流式；而 `musicgen-v1` 等部分音频模型暂不支持流式。

## 关键参数和配置

| 参数名 | 所属接口 | 类型 | 必填 | 说明 |
|--------|----------|------|------|------|
| `stream` | RESTful `/v1/chat/completions` 等 | boolean | 是 | 必须设为 `true`；设为 `false` 或缺失则返回完整 JSON 响应 |
| `stream` | Realtime API | boolean | 是 | 固定为 `true`；设为 `false` 将直接返回 `400 Bad Request` |
| `response_format=stream` | Audio API（如 TTS/ASR） | string | 否（按需启用） | 替代默认 `json` 格式，启用流式响应（SSE 或二进制流） |
| `enable_interim_results` | Omni Realtime API | boolean | 否 | 控制是否返回 ASR 中间识别结果（`is_final=false`），用于实时字幕等场景 |

- **HTTP 头部要求**：  
  - RESTful 流式：需设置 `Accept: text/event-stream`；  
  - WebSocket 接口：必须携带 `Authorization: Bearer <api_key>` 和 `X-DashScope-Date`（ISO8601 格式时间戳）。

- **客户端处理要点**：  
  - 解析 SSE：按行读取，忽略空行和注释行（以 `:` 开头），提取 `data:` 后的 JSON；  
  - 处理 WebSocket 帧：区分 `text` 帧（JSON 事件）与 `binary` 帧（原始音频数据）；  
  - 容错：监听 `error` 事件、超时（Realtime API 连接上限 300 秒，Omni 为 180 秒）及网络中断，实现自动重连（推荐使用 AOQ SDK）。

## 面向开发者，简洁实用

- ✅ **优先选型建议**：  
  - 通用文本流 → 用 RESTful SSE（简单集成，兼容性好）；  
  - 语音/[多模态](multi-modal.md)实时交互 → 用 Realtime API 或 Omni Realtime API（低延迟、双向控制）；  
  - 需要音频流下载 → 用 Audio API 的 `response_format=stream`。

- ✅ **调试技巧**：  
  - 使用 `curl -N` 查看 SSE 响应流；  
  - WebSocket 调试推荐 `wscat` 工具或浏览器 DevTools 的 Network → WS 标签页；  
  - 所有流式响应均以 `content.done`、`response.done` 或 `session.close` 事件标志结束，务必监听以释放资源。

- ❌ **常见陷阱**：  
  - 忘记设置 `Accept: text/event-stream` 导致 RESTful 流式返回 `406 Not Acceptable`；  
  - 在 Realtime API 中传入 `function calling` 工具定义 —— 该能力当前**不支持流式**；  
  - 对 `max_tokens` 期望过严：流式下实际生成 token 数可能略超设定值（因 tokenizer 分词边界对齐），请预留缓冲。

- 📌 **一句话总结**：流式输出 = 更快首字响应 + 更低感知延迟 + 更强交互控制，但需客户端主动适配流式协议与生命周期管理。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [audio api references](../api/audio-api-references.md)
- [video generation api](../api/video-generation-api.md)
- [release notes](../guides/release-notes.md)


