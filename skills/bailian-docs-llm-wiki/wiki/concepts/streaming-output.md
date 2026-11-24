# 流式输出

流式输出（Streaming Output）是指模型服务在生成响应过程中，将结果以增量、分块的方式持续返回给客户端，而非等待全部内容生成完毕后一次性返回。这种方式显著降低用户感知延迟，支持实时渲染、逐字显示、语音合成等交互场景，是构建低延迟 AI 应用的关键能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **CLI 工具（`bailian-cli`）**：通过 `--stream` 参数启用流式输出，适用于终端交互式对话；注意该模式仅在直接终端输出时生效，不支持管道重定向（如 `| grep`）或后台作业。
- **REST API（DashScope 协议）**：在请求体中设置 `"stream": true`，响应头为 `Content-Type: text/event-stream`，客户端需解析 `event: message` SSE 事件流，每个事件包含 `output.text` 的增量片段及 `usage` 统计。
- **[OpenAI 兼容接口](openai-compatible-interface.md)（`/chat/completions`）**：设置 `stream: true`，响应为标准 OpenAI SSE 格式（`data: {...}`），兼容各类 OpenAI SDK（如 `openai-python` 的 `stream=True`）。
- **Anthropic 兼容接口（`/messages`）**：同样支持 `stream: true`，返回 `content_block_delta` 事件，适配 Anthropic SDK 的流式回调（如 `client.messages.stream(...)`）。
- **实时音视频模型（如 `Qwen-Omni-Realtime`）**：不通过 HTTP 流，而是基于 WebSocket 或 AOQ SDK 实现帧级低延迟流式交互，适用于实时语音转写、双工对话等场景，需专用 SDK 支持。

> ⚠️ 注意：流式输出不适用于异步任务（如 `/jobs` 或 `/tasks` 接口），异步任务始终返回完整结果；多模态模型（如 `qwen3-vl-plus`）的流式能力取决于具体模型实现，部分仅支持文本部分流式，图像/视频解析仍为同步。

## 关键参数和配置

| 参数 | 位置 | 类型 | 说明 |
|------|------|------|------|
| `stream` | 请求体（JSON） | boolean | 必填（若启用流式）。设为 `true` 后，服务端返回 SSE 流；设为 `false` 或省略则为同步响应。 |
| `enable_content_streaming` | AOQ SDK 初始化参数 | boolean | 实时模型专用，控制是否开启媒体内容流式回调（如音频帧、文本 token）。 |
| `max_tokens` / `max_output_tokens` | `parameters` 字段内 | integer | 影响流式输出总长度上限；流式响应中每个 chunk 的 `output_tokens` 累加值不超过此限制。 |
| `temperature`, `top_p` | `parameters` 字段内 | number | 流式与非流式共享采样逻辑，不影响流式行为本身，但影响各 chunk 内容的随机性。 |

- **HTTP Header 要求**：流式请求需设置 `Accept: text/event-stream`（REST/DashScope）或 `Accept: application/json`（OpenAI/Anthropic 兼容接口默认支持）。
- **超时处理**：流式请求默认超时时间与同步请求一致（CLI 为 60 秒，REST API 通常为 120 秒），建议客户端实现心跳保活或断线重连逻辑。
- **错误处理**：流式响应中可能夹杂 `event: error` 事件，携带 `error.code` 和 `error.message`，需监听并终止流解析。

## 面向开发者，简洁实用

- ✅ **推荐做法**：  
  - Web 前端用 `EventSource` 或 `fetch().then(res => res.body.getReader())` 处理 SSE；  
  - Python 用 `httpx.AsyncClient.stream()` 或 `openai.OpenAI().chat.completions.create(stream=True)`；  
  - CLI 调试时优先用 `--stream` 直观观察生成过程，避免重定向；  
  - 实时音视频场景务必使用 AOQ SDK，勿尝试用 HTTP 流模拟。

- ❌ **常见陷阱**：  
  - 在 `bailian-cli` 中对 `--stream` 输出做 `| head -n 5` 会中断连接，导致响应不完整；  
  - [OpenAI 兼容接口](openai-compatible-interface.md)未设置 `stream: true` 却按流式解析 `data:` 行，将解析失败；  
  - 忽略 `event: message` 前的空行或注释行（`event: comment`），导致 JSON 解析异常；  
  - 流式响应中 `usage` 字段仅在最后一个 chunk 完整出现，中间 chunk 的 `usage` 为部分统计或为空。

- 🛠️ **调试提示**：  
  使用 `curl -N`（`-N` 禁用缓冲）可手动验证流式响应：  
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -N --data '{
      "model": "qwen-plus",
      "input": {"messages": [{"role":"user","content":"你好"}]},
      "parameters": {"stream": true}
    }'
  ```

## 关联主题页

- [getting started](../guides/getting-started.md)
- [get started with models](../guides/get-started-with-models.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [more about models](../api/more-about-models.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)


