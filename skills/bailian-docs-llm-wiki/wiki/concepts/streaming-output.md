# 流式输出

流式输出（Streaming Output）是指模型服务在生成响应过程中，将结果以增量方式分块、实时推送至客户端，而非等待全部内容生成完毕后一次性返回。这种方式显著降低用户感知延迟，适用于对话界面实时渲染、长文本生成监控、以及需要快速反馈的交互场景。

## 在百炼平台的不同场景中，这个概念如何使用

- **应用组件 API（Application Component）**：`chat` 接口支持 `stream=true`，返回 `text/event-stream` 格式的 SSE 响应，每条 `data:` 消息包含一个增量 token 或完整消息片段，便于前端逐字显示。
- **Qwen 模型 API**：DashScope 原生接口与 [OpenAI 兼容接口](openai-compatible-interface.md)均支持 `stream=true`，但字段路径不同：DashScope 返回 `output.choices[0].message.content`，[OpenAI 兼容接口](openai-compatible-interface.md)返回 `delta.content`；二者均需客户端按 SSE 协议解析。
- **应用支持（Application Support）**：流式输出是 Agent 和 RAG 应用前端体验的关键能力，常配合 `incremental_output=True` 启用真正增量模式（即仅返回新增 token，不重复发送历史内容），需 SDK v3.0+ 与服务端协同支持。
- **模型体验（Model Experience）**：统一 `/v1/models/{model_id}/invoke` 路由支持 `stream=true`，但能力受限于模型类型——文本、部分语音模型稳定支持；视觉生成与全模态模型**暂不支持**流式，启用可能导致连接中断或响应截断。

## 关键参数和配置

- `stream`: 布尔值，必填参数（默认 `false`）。设为 `true` 后，服务端切换为 SSE 流式响应模式。
- `incremental_output`: 布尔值（仅部分 SDK 和应用组件支持），启用后确保每次事件仅含新增内容，避免重复传输；非所有接口原生支持，需确认文档标注。
- 客户端必须：
  - 设置请求头 `Accept: text/event-stream`（推荐）；
  - 正确处理 `Content-Type: text/event-stream` 响应；
  - 解析 `data:` 行并去除前缀，对 JSON 字符串做 `JSON.parse()`；
  - 实现连接保活与错误重连（如收到 `event: error` 或连接中断时）。

> ⚠️ 注意：流式响应不改变计费逻辑——仍按最终实际生成的总 token 数计费；且所有流式调用同样受配额与速率限制约束（如 `429 Too Many Requests`）。

## 面向开发者，简洁实用

- ✅ **推荐做法**：前端对话应用务必启用 `stream=true`，搭配防抖渲染（如每 16ms 合并一次 DOM 更新）提升流畅度。
- ✅ **调试技巧**：用 `curl -N` 或浏览器 DevTools 的 Network → EventStream 查看原始流数据，验证是否按预期分块。
- ❌ **避坑提示**：
  - 不要忽略 `event:` 字段（如 `event: message`），部分 SDK 依赖其区分消息类型；
  - [OpenAI 兼容接口](openai-compatible-interface.md)的 `choices[0].delta` 可能为空对象 `{}`（表示结束），需判空处理；
  - 全模态（omni-modal）和图像生成类模型禁用 `stream=true`，否则可能失败；
  - 流式响应中 `usage` 字段仅在最后一条消息中出现，勿在中间事件里尝试读取。

流式输出不是“可选优化”，而是现代 AI 应用的体验基线。请始终在生产环境开启，并做好客户端健壮性处理。

## 关联主题页

- [application component api reference](../api/application-component-api-reference.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [application support](../guides/application-support.md)
- [model experience](../guides/model-experience.md)


