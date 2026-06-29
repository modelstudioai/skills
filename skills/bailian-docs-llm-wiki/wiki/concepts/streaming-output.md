# 流式输出

流式输出（Streaming Output）指模型在生成响应过程中，将内容按增量片段持续返回给客户端，而非等整段结果生成完毕再一次性返回。百炼平台在文本生成、应用调用、实时[多模态](multimodal.md)交互等多种场景下均支持流式输出，用于降低首字延迟、提升交互体验，并支撑需要边生成边消费的业务（如实时语音对话、深度研究的反问确认阶段）。

## 在百炼平台的不同场景

### 文本生成模型（Qwen 系列）

百炼为 Qwen 系列提供 OpenAI 兼容 Chat Completions、OpenAI 兼容 Responses、Anthropic 兼容 Messages 与 DashScope 原生四种接口，均通过请求中的 `stream` 参数控制是否流式输出。迁移评估时应先确认目标 Qwen 模型在对应兼容接口下是否支持 `stream` 等所需参数。兼容接口为保证协议一致性可能不暴露原生全部参数，如需最全的采样参数与插件能力，建议改用 DashScope 原生接口。

### 应用调用（智能体 / 工作流 / Agent 2.0）

百炼应用提供两套 API，均支持流式：

- **OpenAI 兼容 Responses API**：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`，通过 `stream`（boolean，默认 `false`）开启，适合复用 OpenAI 生态代码库与工具链，支持同步/异步、流式、[多模态](multimodal.md)。
- **DashScope 原生 API**：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`，功能更全、性能更高，新版智能体、工作流、旧版智能体均支持。

调用前需先在控制台获取应用 ID（及子业务空间的 Workspace ID）与 API Key。

### 实时[多模态](multimodal.md)交互（Qwen-Omni-Realtime）

实时多模态交互基于 WebSocket 长连接，本质上即流式：通过客户端事件与服务端事件的双向消息流驱动会话。客户端用 `input_audio_buffer.append` 持续追加 Base64 音频片段，服务端在 VAD 模式下自动检测语音起止并触发响应，在 Manual 模式下由客户端用 `input_audio_buffer.commit` + `response.create` 显式触发。流式发送较小数据块可让 VAD 响应更迅速；Manual 模式下关闭 `turn_detection` 时，每个事件最多放置 15 MiB 音频。相关事件包括 `response.create`（触发生成）、`response.cancel`（取消正在进行的响应）、`session.updated` 等。

### 专用模型（[more](../api/more.md)-models）

`farui-plus`、`tongyi-intent-detect-v3`、`qwen-mt-plus`、`qwen3.5-ocr`、`gui-plus` 等专用模型同样通过 `stream`（bool，可选）控制流式输出。其中 `qwen-deep-research` 采用两阶段流程，**第一步反问确认阶段必须将 `stream` 设为 `true`**，以便客户端实时读取反问内容并回传确认；该模型当前仅支持 Python DashScope SDK、仅华北2（北京）地域。

## 关键参数与配置

- **`stream`**（文本/应用/专用模型，boolean，默认 `false`）：是否启用流式输出。开启后响应以增量片段（SSE 或 WebSocket 消息）形式返回，客户端需按对应协议逐片段解析。
- **`response.create` / `response.cancel`**（Omni Realtime）：在 WebSocket 会话中显式触发或取消流式响应；VAD 模式下响应由服务端自动生成，Manual 模式或工具调用回传结果后需手动发送 `response.create`。
- **`input_audio_buffer.append`**：向实时会话的输入音频缓冲区流式追加音频片段，是实时流式输入的核心事件。
- **地域与域名**：流式接口的地域与 Base URL 与非流式一致，例如华北2（北京）推荐使用业务空间专属域名 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`，新加坡为 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`；Omni Realtime 走 WebSocket，北京为 `wss://dashscope.aliyuncs.com/api-ws/v1/realtime`。

## 注意事项

- 流式响应需客户端按 SSE 或 WebSocket 协议逐片段解析并拼接，错误处理（断连、超时、部分片段失败）需在业务侧实现。
- 不同接口对流式的支持字段存在差异：兼容接口可能不暴露原生全部参数，需最全流式控制能力时优先选 DashScope 原生接口。
- 实时多模态场景下，音频片段大小与发送节奏直接影响 VAD 灵敏度与首响应延迟，建议流式发送较小数据块。
- `qwen-deep-research` 反问阶段强制 `stream=true`，是少见的"必须流式"场景，集成时需特别处理。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [application call](../api/application-call.md)
- [more models](../api/more-models.md)


