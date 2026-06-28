# 流式输出

流式输出（Streaming Output）是指模型在生成过程中，将结果以增量数据块（chunk）的形式逐步返回给调用方，而非等待完整生成后一次性返回。百炼平台的文本生成、实时多模态交互、应用调用等场景均支持流式输出，可显著降低首字延迟、提升交互体验。

## 在百炼平台中的使用场景

### 文本生成模型（Qwen 系列）

在 OpenAI 兼容 Chat Completions、Responses、Anthropic 兼容 Messages 以及 DashScope 原生接口中，均可通过设置 `stream` 参数启用流式输出。调用方按 OpenAI/Anthropic 协议约定的 SSE（Server-Sent Events）格式逐块读取 `delta` 内容，拼接后得到完整文本。

- 兼容接口的流式响应字段与对应官方客户端保持一致，可直接复用现有 SDK 与示例代码。
- 仅 Responses 接口由平台自动管理对话历史，其余接口需调用方自行维护上下文。
- 迁移评估时应先确认目标 Qwen 模型在对应兼容接口下是否支持 `stream` 等参数。

### 实时多模态交互（Qwen-Omni-Realtime）

Qwen-Omni-Realtime 基于 WebSocket 长连接实现低延迟的语音/视频/图像对话，本身就是一种流式交互模型：客户端通过 `input_audio_buffer.append` 流式追加音频，服务端通过 `response.delta` 等事件流式返回生成的音频与文本。

- 在 VAD 模式下，服务端自动检测语音起止并触发响应生成；在 Manual 模式下，需客户端显式 `input_audio_buffer.commit` 后 `response.create` 触发生成。
- 流式发送较小数据块可让 VAD 响应更迅速；关闭 `turn_detection` 时每个事件最多放置 15 MiB 音频。
- 可通过 `response.cancel` 取消正在进行的流式响应。

### 应用调用（[智能体应用](agent-application.md) / 工作流应用）

通过 `Application.call` 或 `POST /apps/{app_id}/completion` 调用百炼应用时，同样支持流式返回中间过程与最终结果。开发者可在请求参数中开启流式模式，逐步接收应用编排过程中各节点的输出与最终 `output.text`，适用于对话式 UI、逐字渲染等场景。

## 关键参数与配置

- **`stream`**：布尔型，设为 `true` 启用流式输出，适用于 Chat Completions、Responses、应用调用等接口。
- **`stream_options`**：OpenAI 兼容 Chat Completions 接口下，可在流式输出的最后一行通过 `stream_options={"include_usage": true}` 获取本次请求的 token 用量。
- **`response.create` / `response.cancel`**：实时多模态交互中触发与取消流式响应的客户端事件。
- **`input_audio_buffer.append`**：实时多模态交互中流式追加输入音频，建议分块发送以提升 VAD 响应速度。
- **协议差异**：OpenAI/Anthropic 兼容接口为协议一致性可能不暴露百炼原生全部参数；如需最全的流式相关采样与插件参数，建议改用 DashScope 原生接口。

## 注意事项

- 流式输出需要调用方正确处理增量拼接与连接中断，建议在客户端实现断线重连与异常回退逻辑。
- 实时多模态交互对网络抖动敏感，建议使用[业务空间](workspace.md)专属域名（如 `wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime`）以获得更好性能与稳定性。
- 异步任务（如图像/视频生成）不适用流式输出，应通过任务查询或事件总线 EventBridge 通知获取结果，避免高频轮询触发 20 QPS 限流。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [more about models](../api/more-about-models.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [bailian application calling](../guides/bailian-application-calling.md)


