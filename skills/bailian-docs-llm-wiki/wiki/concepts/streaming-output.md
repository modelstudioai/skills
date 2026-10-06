# 流式输出

流式输出（Streaming Output）是百炼平台提供的一种实时响应机制，允许模型在生成过程中将结果以增量方式分块返回，而非等待全部内容完成后再一次性交付。该机制显著降低端到端延迟，提升用户交互体验，尤其适用于对话、语音、多模态实时处理等对响应速度敏感的场景。

## 在百炼平台的不同场景中，这个概念如何使用

- **标准模型 API（RESTful）**：通过设置请求 Header `Accept: text/event-stream` 并解析 Server-Sent Events（SSE）格式响应实现流式输出。每条 `data:` 行包含一个 JSON 片段（如 `{"output":{"text":"Hello"}}`），客户端需逐帧拼接并渲染。
  
- **Application Call（智能体/工作流调用）**：支持两种协议下的流式开关：
  - DashScope 原生 API：在请求 Header 中添加 `X-DashScope-SSE: enable`；
  - OpenAI 兼容 Responses API：在请求体中传入 `stream=true`（布尔值）。

- **Realtime API（WebSocket）**：**强制流式**，不支持同步模式。所有响应均以事件形式推送（如 `response.text.delta`、`response.audio.delta`），客户端需监听并消费增量数据流。

- **Omni Realtime API（多模态 WebSocket）**：同样为强制流式，`stream=true` 是 URL 必填参数；服务端按语义粒度（如 token、音频帧、图像区域描述）持续推送 `output` 和 `progress` 事件。

- **开发工具与客户端（CLI / IDE / Web）**：当底层调用启用 `stream=true`（或对应配置如 `--stream`、`stream: true`）时，工具自动处理 SSE 或 WebSocket 流，并以“打字机效果”实时呈现输出，开发者无需手动解析协议。

## 关键参数和配置

| 场景 | 启用方式 | 关键参数/头 | 说明 |
|------|----------|-------------|------|
| RESTful 模型 API | Header + 响应解析 | `Accept: text/event-stream` | 必须设置，否则返回完整 JSON；响应为 SSE 格式，需按行解析 `data:` 字段 |
| Application Call（DashScope） | Header | `X-DashScope-SSE: enable` | 仅此 Header 生效，`stream` 字段在请求体中被忽略 |
| Application Call（Responses API） | 请求体 | `"stream": true` | 直接在 JSON payload 中声明；兼容 OpenAI v1 格式 |
| Realtime API / Omni Realtime API | 协议级强制 | 无显式开关 | WebSocket 连接即开启流式；`stream=false` 不被接受，会报错或静默忽略 |

> ⚠️ 注意：  
> - 所有流式接口均要求客户端具备事件解析与错误恢复能力（如重连、心跳、帧序号校验）；推荐优先使用百炼官方 SDK（如 AOQ SDK）而非裸 WebSocket 封装。  
> - 流式响应中，`finish_reason` 字段仅在最后一帧出现，用于标识生成结束原因（如 `"stop"`、`"length"`、`"tool_calls"`）；中间帧仅含 `delta` 或 `text` 增量内容。  
> - 若需获取完整响应，可自行缓存所有 `delta` 并拼接 `output.text`；但注意部分多模态流（如音频 delta）需按二进制帧重组，不可简单字符串拼接。

## 面向开发者，简洁实用

- ✅ **快速启用**：RESTful 调用加 `Accept: text/event-stream`；Application Call 选 Responses 协议则直接设 `"stream": true`。  
- ✅ **安全兜底**：流式请求失败时，服务端仍保证至少返回一个含 `error` 字段的 SSE 事件（如 `data: {"error":{...}}`），请务必监听并处理。  
- ✅ **性能提示**：流式不降低总计算耗时，但大幅改善首 token 延迟（TTFT）和 token 间隔（ITL）；建议搭配 `max_output_tokens` 限制防止无限生成。  
- ❌ **避免踩坑**：不要在流式请求中同时设置 `stream=false`；不要忽略 `event:` 类型字段（如 `event: message`）；不要假设所有 `data:` 行都是合法 JSON（空行、注释行需跳过）。  
- 🛠️ **调试建议**：用 `curl -N` 或 Postman 的 SSE 插件直接测试；生产环境务必实现超时控制（如单帧等待 >5s 则中断连接）和断线重连逻辑。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [application call](../api/application-call.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)


