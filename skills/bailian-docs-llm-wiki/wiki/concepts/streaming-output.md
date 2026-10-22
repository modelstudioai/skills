# 流式输出

流式输出（Streaming Output）是指模型服务在生成响应过程中，将结果以增量、分块的方式持续推送至客户端，而非等待全部内容生成完毕后一次性返回。这种方式显著降低端到端延迟，提升用户交互实时性，是语音助手、实时对话、长文本生成等场景的关键能力。

## 在百炼平台的不同场景中如何使用

- **标准文本生成（RESTful API）**：调用 `/text-generation/generation` 等 DashScope 原生接口或 OpenAI 兼容的 `/chat/completions` 时，设置 `stream=true` 即可启用流式响应。服务端以 Server-Sent Events（SSE）格式返回多个 `data:` 块，每个块包含 `output.choices[0].delta.content` 的增量文本片段，开发者需按顺序拼接还原完整响应。

- **Realtime API（WebSocket）**：专为低延迟交互设计，流式是默认且强制行为（`stream=true` 固定生效）。服务端通过结构化事件（如 `response.text.delta`、`output.audio`、`tool_use`）实时推送中间结果，支持文本、音频、工具调用等多类型增量输出，并允许客户端在任意时刻插入中断指令（`interrupt`）。

- **Omni Realtime API（AOQ/WebSocket/WebRTC）**：面向多模态实时交互，流式输出深度集成 VAD（语音活动检测）、语义断句与音视频同步。除文本增量外，还支持 PCM/WAV 音频流分片（`audio_chunk`）、视觉帧级推理结果（`output.video.frame`）等细粒度流式交付，适用于语音助手、会议实时转写等毫秒级敏感场景。

- **Qwen Responses（OpenAI 兼容扩展）**：在 `/responses` 端点中启用 `stream=true` 后，不仅返回文本增量，还会流式推送工具调用触发（`tool_use`）、联网搜索摘要（`search_result`）、代码执行日志（`code_interpreter_log`）等中间步骤，便于构建透明、可控的 Agent 工作流。

## 关键参数和配置

- `stream`: 布尔值，**必需显式设置为 `true`** 才启用流式输出。所有协议均支持该参数，但行为略有差异：
  - RESTful 接口（如 `/text-generation/generation`）：返回 SSE 格式响应，需解析 `data:` 行；
  - WebSocket 接口（Realtime/Omni）：`stream=true` 是连接 URL 必填查询参数，不可省略；
  - OpenAI 兼容 `/chat/completions`：支持 `stream=true`，但 `/responses` 更推荐用于复杂流式 Agent 场景。

- `response_format`: 仅 Realtime API 支持，取值 `json`（默认，结构化事件）或 `binary`（原始 PCM 音频二进制流），影响流式数据的序列化方式。

- `max_tokens`: 控制单次响应最大输出长度，**流式下仍生效**。当达到上限时，服务端会发送 `done` 或 `end_of_turn` 类型事件终止流，避免无限推送。

- 注意：流式响应不改变模型本身的 token 计费逻辑——所有生成的 token（含流式过程中的每一块）均计入配额；也不改变输入限制（如 `qwen-turbo` 输入上限仍为 8K tokens）。

## 面向开发者提示

- 不要依赖单个流式 chunk 的完整性：`delta.content` 可能为空、含部分 Unicode 字符或中途截断，务必累积处理并校验 UTF-8 边界。
- 实时场景请优先选用 Realtime 或 Omni Realtime API：它们提供事件驱动模型、原生中断支持和多模态同步，远超传统 SSE 流式的能力边界。
- 使用官方 SDK（Python/JS AOQ 客户端）可自动处理重连、帧解码、事件路由与错误恢复，大幅降低流式集成复杂度。
- 流式响应中若出现 `error` 事件（如 `invalid_input_format` 或 `tool_execution_failed`），应立即终止当前流并检查请求参数，不要尝试继续消费后续 chunk。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [qwen api reference](../api/qwen-api-reference.md)


