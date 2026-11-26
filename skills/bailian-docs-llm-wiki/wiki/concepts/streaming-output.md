# 流式输出

流式输出（Streaming Output）是百炼平台提供的一种实时响应机制，允许模型在生成过程中逐 token（或逐 chunk）向客户端持续推送结果，而非等待全部推理完成后再返回完整响应。该机制显著降低端到端延迟，提升用户体验，尤其适用于对话交互、实时语音合成、长文本生成等对响应速度敏感的场景。

## 在百炼平台的不同场景中，这个概念如何使用

- **标准文本生成（LLM）**：通过 `POST /v1/models/{model_id}/invoke` 接口，设置 `stream: true` 即可启用逐 token 流式返回；配合 `incremental_output: true` 可确保每次事件仅包含新增内容（非累计），避免前端重复渲染。
- **实时音视频模型（ASR/TTS/多模态）**：所有实时 API（如 `/v1/realtime/chat/completions`、`/v1/realtime/asr`）强制要求 `stream: true`，响应采用 Server-Sent Events（SSE）或 WebSocket 流式协议，每帧携带 `delta`（增量文本）、`final`（终局标记）等语义字段。
- **Agent 与[函数调用](function-calling.md)场景**：当模型具备 `function_calling` capability 且启用流式时，工具调用请求与执行结果可分阶段流式返回，支持前端动态渲染思考链与工具执行状态。
- **不支持流式的场景**：图像/视频生成（如 `wanx2.1-t2i-turbo`）、[向量嵌入](vector-embedding.md)（embedding/rerank）及部分异步任务模型不支持流式输出；尝试传入 `stream: true` 将被静默忽略或返回错误。

> ⚠️ 注意：流式能力依赖模型自身的 `capabilities` 声明（如 `"streaming"` 或 `"chat"` + `"streaming"`）。调用前请务必通过 `GET /v2/models/{model}` 查询模型是否支持流式，否则将触发 `400 Bad Request`。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `stream` | boolean | 是（流式场景） | 启用流式响应模式 | `true` |
| `incremental_output` | boolean | 推荐显式设置 | 控制输出是否为增量（`true`）或累计（`false`）；默认行为因 SDK 版本而异，建议始终显式指定 | `true` |
| `stream_options` | object | 否（高级控制） | 包含 `include_usage: boolean` 等子字段，用于在流式末尾附加 token 使用统计（需模型 capability 支持） | `{"include_usage": true}` |

- **HTTP 响应头**：流式响应固定返回 `Content-Type: text/event-stream`。
- **事件格式**：遵循 SSE 标准，每条消息以 `data: {JSON}` 开头，双换行分隔；终局消息可能包含 `event: done` 或 `data: {"finish_reason":"stop"}`。
- **SDK 行为差异**：
  - DashScope Python SDK ≥2.0.1：`stream=True` 默认启用 `incremental_output=True`；
  - OpenAI 兼容 SDK：`stream=True` 对应百炼的增量流式，无需额外配置 `incremental_output`；
  - 旧版 DashScope SDK 1.x：`incremental_output` 需单独传参，且默认为 `False`，迁移时务必检查。

## 面向开发者，简洁实用

- ✅ **立即启用**：只需在请求 body 中添加 `"stream": true`，无需修改 URL 或认证逻辑。
- ✅ **前端解析示例（JavaScript）**：
  ```javascript
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer xxx' },
    body: JSON.stringify({ model_id: 'qwen-plus', input: { messages: [...] }, parameters: { stream: true } })
  });
  const reader = response.body.getReader();
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    const chunk = new TextDecoder().decode(value);
    // 解析 data: {...}\n\n 格式，提取 content 字段
  }
  ```
- ✅ **错误排查**：
  - 返回 `400 Bad Request` + `"message": "stream is not supported"` → 模型不支持流式（查 capability）；
  - 返回 `200` 但无 `text/event-stream` 头 → 请求未正确设置 `stream: true` 或被中间件拦截；
  - 前端收到重复内容 → 未启用 `incremental_output: true`，改用累计模式需自行去重。

- ❌ **不要做**：对不支持流式的模型（如 embedding）强行传 `stream: true`；在非流式接口（如异步任务 `/api/v1/tasks`）中尝试流式解析；在客户端硬编码模型名而非通过 `/v2/models` 动态发现 capability。

## 关联主题页

- [capabilities](../guides/capabilities.md)
- [model experience](../guides/model-experience.md)
- [preparations](../api/preparations.md)
- [more about models](../api/more-about-models.md)
- [application support](../guides/application-support.md)
- [realtime api directory](../api/realtime-api-directory.md)


