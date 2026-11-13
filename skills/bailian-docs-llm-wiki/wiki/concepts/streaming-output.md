# 流式输出

流式输出（Streaming Output）是百炼平台支持的一种实时响应模式，允许模型在生成过程中逐段（如逐 token、逐 chunk）将结果以 Server-Sent Events（SSE）格式持续推送至客户端，而非等待全部推理完成后再返回完整响应。该机制显著降低端到端延迟，提升用户交互体验，尤其适用于对话类、长文本生成、Agent 工具调用等对响应实时性敏感的场景。

## 在百炼平台的不同场景中如何使用

- **模型调用（Model Experience）**：通过 `model experience` 统一入口（`/v1/models/{model_id}/invoke`）启用流式输出，需在请求 body 中设置 `"stream": true`。仅文本生成类模型（如 `qwen-max`、`qwen-plus`）及部分全模态模型（如 `qwen2.5-omni`）支持；视觉、语音、向量类模型暂不支持流式。
  
- **Agent 应用与 RAG 场景（Application Support）**：在构建智能体或问答应用时，流式输出常与 `incremental_output=true` 配合使用，实现前端“打字机”式实时渲染；当模型调用插件并生成中间结果时，流式响应可同步传递 `tool_calls` 事件，便于前端动态展示工具执行状态。

- **Qwen API 多协议兼容层**：OpenAI 兼容的 `chat/completions` 和 `responses` 接口、Anthropic 兼容的 `messages` 接口均支持 `stream=true` 参数；DashScope 原生协议同样支持，且对流式事件结构定义最完整（含 `delta`、`finish_reason`、`usage` 等字段）。注意：Qwen-Audio、Qwen-VL 等部分多模态模型在 OpenAI 兼容协议下**不支持流式**，须切换至 DashScope 协议。

- **[异步任务](asynchronous-task.md)（More about Models）**：流式输出**不适用于[异步任务](asynchronous-task.md)**（如图像生成、视频合成）。[异步任务](asynchronous-task.md)通过轮询 `/api/v1/tasks/{task_id}` 或事件总线接收最终结果，其本质是“非实时、终态交付”，与流式输出的设计目标正交。

## 关键参数和配置

| 参数 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `stream` | boolean | 启用流式响应的核心开关。设为 `true` 后，HTTP 响应头 `Content-Type` 将为 `text/event-stream`，响应体为 SSE 格式事件流。 | `"stream": true` |
| `incremental_output` | boolean（仅 Application Support 场景） | 控制流式内容是否为增量更新（即每帧只含本次新增内容），避免重复传输历史内容。推荐前端开启此选项以优化渲染性能。 | `"incremental_output": true` |
| `sse_event_name`（SDK 内部） | string | 百炼 SDK 默认使用 `event: message` 标识数据事件；开发者若手动解析 SSE，需按标准格式处理 `data:` 行并忽略空行与注释行（`:` 开头）。 | `event: message\nid: 1\ndata: {"delta":{"content":"你好"}}` |

> ⚠️ 注意事项：
> - 流式响应的 `output` 字段结构与非流式**不一致**：流式返回的是 `{"event": "message", "data": {...}}` 事件流，每帧 `data` 中含 `delta`（增量内容）、`finish_reason`（停止原因）及可选 `usage`；非流式返回的是完整 `{"output": {"text": "...", "choices": [...]}}` 对象。
> - `stream=true` 时，`max_tokens` 等参数行为不变，但 `finish_reason` 可能为 `"stop"`（自然结束）、`"length"`（达长度上限）或 `"tool_calls"`（触发工具调用）。
> - 若请求中同时指定 `stream=true` 和不支持流式的模型（如 `wanx2.1-t2i-turbo`），API 将直接返回 `400 Bad Request` 并提示 `Stream not supported for this model`。

## 面向开发者的实用建议

- ✅ **优先使用 SDK**：Python/Java SDK 自动处理 SSE 解析、重连、超时与错误恢复；避免手动实现 HTTP 流解析。
- ✅ **前端渲染推荐增量模式**：启用 `incremental_output=true` 后，每帧 `delta.content` 可直接追加到 DOM，无需缓存或拼接全量文本。
- ✅ **错误处理需监听 `event: error`**：流式连接可能因网络中断或模型异常终止，务必监听 `event: error` 事件并做降级（如切换为同步调用）。
- ❌ **勿在流式响应中依赖 `output.text` 字段**：该字段仅存在于非流式响应中；流式下请始终解析 `delta.content` 或 `delta.tool_calls`。
- 📌 **调试技巧**：使用 `curl -N` 命令可直观查看原始 SSE 流；生产环境建议添加 `X-Request-ID` 请求头，便于日志关联追踪。

## 关联主题页

- [model experience](../guides/model-experience.md)
- [application support](../guides/application-support.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [more about models](../api/more-about-models.md)


