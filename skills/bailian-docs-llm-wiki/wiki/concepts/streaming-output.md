# 流式输出

流式输出（Streaming）是百炼平台提供的一种实时响应机制，允许模型在生成过程中持续分块返回结果，而非等待全部内容完成后再一次性返回。它显著降低端到端延迟，提升用户交互体验，尤其适用于对话界面、实时翻译、代码补全等对响应速度敏感的场景。

## 在百炼平台的不同场景中，这个概念如何使用

- **文本生成（Chat/Completions）**：调用 `qwen-max`、`qwen-turbo` 等 LLM 时，设置 `stream=true` 后，API 返回 Server-Sent Events（SSE）格式的响应流，每个 `data:` chunk 包含部分生成文本（`delta.content`）及可选的 token 统计信息。适用于 Web 前端逐字渲染、CLI 实时打印等。
  
- **多模态模型（如 `qwen-vl`、`qwen-omni`）**：仅部分支持流式输出，且当前限于文本输出部分（即视觉理解后的文字描述可流式返回，图像/音频本身不流式）。需查阅具体模型文档确认支持状态。

- **[函数调用](function-calling.md)（Tool Calling）与 Agent 场景**：在 `/responses` 接口（OpenAI 兼容 Responses 协议）中启用 `stream=true`，可流式获取工具调用决策、执行日志及最终答案；但工具参数解析阶段不流式，仅最终回复阶段流式。

- **语音与音频模型（如 `qwen-audio`）**：**不支持流式输出**。该类模型必须使用 DashScope 原生接口，且仅支持同步响应（`stream=false`），返回完整转录文本或结构化结果。

> ⚠️ 注意：流式响应仅保证 chunk 的顺序性，不保证每个 chunk 对应严格意义上的“单个 token”或语义完整单元（如中文词、标点）；应用层应按 SSE 协议拼接 `delta.content` 并做增量处理，不可依赖 chunk 边界做语义切分。

## 关键参数和配置

- **核心开关**：`stream`（布尔值），必须显式设为 `true` 才启用流式输出。默认为 `false`。
  - HTTP 请求中作为 JSON 字段传入（如 `"stream": true`）；
  - CLI 中通过 `--stream` 标志启用（如 `bailian chat --model qwen-turbo --message "你好" --stream`）；
  - Python SDK 中通过 `stream=True` 参数控制（如 `Generation.call(..., stream=True)`）。

- **协议适配要求**：
  - OpenAI 兼容 `/chat/completions` 和 `/responses` 接口：返回标准 SSE 格式，事件类型为 `event: message` 或 `event: error`；
  - Anthropic 兼容 `/v1/messages`：**不支持流式输出**；
  - DashScope 原生接口（如 `/text-generation/generation`）：返回 SSE，但事件名可能为 `event: result`，需按实际响应头 `Content-Type: text/event-stream` 解析。

- **配套注意事项**：
  - `max_tokens` 在流式模式下实际生效值可能略低于设定值（服务端需预留终止标记空间）；
  - 流式响应中若发生错误，会发送 `event: error` 事件，但错误详情较简略，**务必同时检查 HTTP 状态码（如 `400`/`500`）和响应头 `X-DashScope-Status`**；
  - 客户端需实现健壮的 SSE 解析器（自动重连、字段提取、UTF-8 编码处理），推荐使用成熟库（如 JavaScript 的 `EventSource`、Python 的 `sseclient-py`）。

面向开发者：启用流式输出只需加一个参数，但务必做好客户端流解析与错误兜底——这是获得低延迟体验的关键一步。

## 关联主题页

- [getting started](../guides/getting-started.md)
- [model experience](../guides/model-experience.md)
- [application support](../guides/application-support.md)
- [qwen api reference](../api/qwen-api-reference.md)


