# Qwen-Omni-Realtime WebSocket 接入

Qwen-Omni-Realtime WebSocket 接入

<a id="适用范围"></a>

## 适用范围

本文面向 Qwen-Omni-Realtime。示例模型为 `qwen3.8-omni-flash-realtime`，`qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime` 的配置参见事件参考。历史型号 `qwen3-omni-flash-realtime-2025-09-15` 的参数参见 [Python SDK](../../../_short/realtime-websocket-python-sdk-qwen-omni-realtime-e50924065f85dda8.md)。

-   使用所选地域和业务空间对应的 [API Key](../../preparations/get-api-key.md) 与 [API Host](https://bailian.console.aliyun.com/cn-beijing/settings/workspace)（不含协议和路径）。
-   北京域名：`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`。
-   长期 API Key 保存在服务端，不放入浏览器或移动端应用。

<a id="地址与鉴权"></a>

<a id="websocket-endpoints"></a>

<a id="接入地址"></a>

## 地址与鉴权

通过查询参数 `model` 指定要调用的模型。

WebSocket`wss://WorkspaceId.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime?model=qwen3.8-omni-flash-realtime`

`qwen3.8-omni-flash-realtime` 必须使用业务空间专属域名。旧型号可继续使用原域名：北京为 `wss://dashscope.aliyuncs.com`，新加坡为 `wss://dashscope-intl.aliyuncs.com`。详情参见 [Python SDK](../../../_short/realtime-websocket-python-sdk-qwen-omni-realtime-e50924065f85dda8.md)。

在 WebSocket 握手请求头中设置 `Authorization: Bearer <API_KEY>`。不要把长期 API Key 放入浏览器或移动端。

可选的 `user-agent` 请求头用于标识客户端。通用 WebSocket 接入资料还列有 `X-DashScope-WorkSpace`（业务空间 ID）和 `X-DashScope-DataInspection`（数据合规检查配置），这两个请求头按模型要求使用。

临时 API Key 的生成方式和权限说明参见[生成临时 API Key](../../more-about-models/generate-temporary-api-key.md)。

以下业务空间地址以 `qwen3.5-omni-plus-realtime` 为例。

-   华北2（北京） `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime?model=qwen3.5-omni-plus-realtime`
-   新加坡 `wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime?model=qwen3.5-omni-plus-realtime`

将 `{WorkspaceId}` 替换为所选地域的[业务空间 ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="会话配置"></a>

## 会话配置

建立连接并收到 `session.created` 后发送 `session.update`。收到 `session.updated` 确认后再发送输入；错误通过 `error` 事件处理。

以下示例对应 `qwen3.8-omni-flash-realtime`，其他版本使用各自事件参考中的配置，不混用字段层级。

<a id="code-block"></a>

```json
{
  "type": "session.update",
  "session": {
    "modalities": [
      "text",
      "audio"
    ],
    "voice": "Tina",
    "turn_detection": {
      "type": "server_vad"
    }
  }
}
```

<a id="输入-结果与结束"></a>

## 输入、结果与结束

音频通过 `input_audio_buffer.append` 发送；输入格式、提交条件和图像输入限制见[客户端事件](client-events.md)。处理[服务端事件](server-events.md)中的结果、状态和错误，不将连接建立视为业务请求已完成。

自动轮次与 Manual 模式、Function Calling 和 MCP 的时序见[交互流程](#websocket-workflow)。接收完所需结果后关闭 WebSocket 连接。

<a id="交互流程"></a>

<a id="websocket-workflow"></a>

<a id="接入流程"></a>

## 交互流程

<a id="vad-模式"></a>

<a id="9b49887720jcw"></a>

### VAD 模式

将[客户端事件](client-events.md)事件的`session.turn_detection.type` 设为`"server_vad"`以启用 VAD 模式。在 VAD 模式下，服务端对传入的音频进行语音活动检测，并在检测到作出响应。此模式适用于客户端到服务器始终发送音频的情况，也是当前的默认模式。

![server\_vad](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0520773571/p991064.svg)

-   服务端在检测到语音开始时发送`input_audio_buffer.speech_started` 事件。
-   客户端随时可以选择通过发送 `input_audio_buffer.append` 事件将音频追加到缓冲区。
-   服务端在检测到语音结束时发送`input_audio_buffer.speech_stopped`事件。
-   服务端通过发送 `input_audio_buffer.committed` 事件来提交输入音频缓冲区。
-   服务端发送 `conversation.item.created` 事件，其中包含从音频缓冲区创建的用户消息项。

<a id="function-calling-流程"></a>

<a id="613b113654ayb"></a>

#### Function Calling 流程

在 VAD 模式下，当服务端生成的响应需要客户端执行 Function Calling 工具时，遵循以下交互流程：

![image.svg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3014236771/p1067613.svg)

-   服务端在检测到语音结束并生成响应时，识别到需要调用工具。
-   服务端发送 `response.function_call_arguments.delta` 事件，包含工具调用参数的增量数据。
-   服务端发送 `response.function_call_arguments.done` 事件，表示工具调用参数传递完成。
-   客户端执行工具调用并获取结果。
-   客户端通过 `conversation.item.create` 事件发送工具调用结果。
-   客户端发送 `response.create` 事件，触发服务端基于工具调用结果生成响应。

<a id="manual-模式"></a>

<a id="ee09a3493fsuc"></a>

### Manual 模式

将[客户端事件](client-events.md)事件的`session.turn_detection` 设为 null 以启用 Manual 模式。此模式下，客户端通过显式发送`input_audio_buffer.commit` 和`response.create`事件请求服务器响应。适用于按下即说场景，如聊天软件中的发送语音。

![manual](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0520773571/p991066.svg)

-   客户端可以通过发送 `input_audio_buffer.append` 事件将音频追加到缓冲区。
-   客户端通过发送 `input_audio_buffer.commit`事件来提交输入音频缓冲区。 该提交会在对话中创建一个新的用户消息项。
-   服务器通过发送 `input_audio_buffer.committed`事件进行响应。
-   客户端发送 `response.create` 事件，触发模型生成最终响应。
-   服务器通过发送 `conversation.item.created`事件进行响应。

<a id="function-calling-流程-2"></a>

<a id="9c958b42d8xkl"></a>

#### Function Calling 流程

![image.svg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3014236771/p1067740.svg)

在 Manual 模式下，当服务端生成的响应需要客户端执行 Function Calling 工具时，遵循以下交互流程：

-   客户端发送 `response.create` 事件后，服务端生成响应并识别到需要调用工具。
-   服务端发送 `response.function_call_arguments.delta` 事件，包含工具调用参数的增量数据。
-   服务端发送 `response.function_call_arguments.done` 事件，表示工具调用参数传递完成。
-   客户端执行工具调用并获取结果。
-   客户端通过 `conversation.item.create` 事件发送工具调用结果。
-   客户端发送 `response.create` 事件，触发模型生成最终响应。
-   服务端基于工具调用结果生成响应，并通过 `response.audio.delta` 或 `response.text.delta` 事件返回给客户端。

<a id="mcp-工具调用"></a>

<a id="qwen38-mcp-flow"></a>

## MCP 工具调用

以下流程适用于 Qwen3.8-Omni-Flash-Realtime，可与上述 VAD 或 Manual 模式配合使用。

Function Calling 与 MCP 可以在同一会话的 `session.tools` 中配置，不能同时启用联网搜索（`enable_search`）。百炼不额外收取 MCP 工具调用费，模型推理仍按模型价格计费。

MCP 由服务端执行工具，前述 Function Calling 流程则由客户端执行工具，两者的结果回传方式不同。

<a id="工具发现"></a>

<a id="websocket-flow-section-7"></a>

### 工具发现

客户端通过 `session.update` 配置 MCP 服务后，由 Realtime 服务异步发现工具，交互流程如下：

![MCP 工具发现时序图](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/images/6a4b3c2d1e0f92df.png)

本节时序图中，`opt` 表示满足条件时执行，`alt` 表示按条件选择不同分支，`par` 表示并行处理。

-   `session.updated` 仅表示 MCP 配置已接受，不表示工具已经可用。
-   `mcp_list_tools.in_progress` 可能早于 `session.updated` 到达。
-   客户端可以在工具发现完成前继续发送音频或 `response.create`；但只有发现完成后的 Response 才能使用对应 MCP 工具。
-   工具发现成功时，服务端先发送包含最终工具列表的 `conversation.item.created`，再发送 `mcp_list_tools.completed`。
-   工具发现失败时，服务端先发送包含 error 的 `conversation.item.created`，再发送 `mcp_list_tools.failed`。

<a id="mcp-调用与续答"></a>

<a id="websocket-flow-section-8"></a>

### MCP 调用与续答

模型选择 MCP 工具后，由 Realtime 服务执行工具调用；需要审批时，客户端先回复审批结果。交互流程如下：

![MCP 工具调用、审批与续答时序图](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/images/6a4b3c2d1e0f92de.png)

审批拒绝或超时会直接触发 `response.mcp_call.failed`，不执行工具，也不会经过 `response.mcp_call.in_progress`。无需审批或审批通过时，典型事件顺序如下：

<a id="code-block-2"></a>

```text
response.output_item.added（mcp_call）
→ response.mcp_call_arguments.delta
→ response.mcp_call_arguments.done
→ 可选：conversation.item.created（mcp_approval_request）
→ 可选：conversation.item.create（mcp_approval_response）
→ response.mcp_call.in_progress
→ response.mcp_call.completed 或 response.mcp_call.failed
→ response.output_item.done（最终 mcp_call）
→ response.done（父 Response）
```

服务端会在同一父 Response 的全部 MCP item 进入终态后发送 `response.done`。其中 `response.output` 已包含最终 mcp\_call 快照：成功项为 completed 并包含 output；失败项为 failed 并包含 error。

如果需要模型基于 MCP 结果继续生成回答，客户端应在收到父 `response.done` 后发送一次不附带 MCP 结果的 `response.create`。

参见[客户端 MCP 工具配置](client-events.md#session-tools-mcp)、[审批回复](client-events.md#qwen38-mcp-approval-response)、[MCP 服务端事件](server-events.md#qwen38-server)和[MCP 对话项](server-events.md#mcp-items)。

<a id="使用限制"></a>

<a id="qwen38-mcp-limits"></a>

### 使用限制

以下为每个会话的 MCP 默认约束：

| 项目 | 默认值 |
| --- | --- |
| MCP 服务数 | 8 |
| MCP 工具数 | 128 |
| 工具发现超时 | 30 秒 |
| 审批超时 | 60 秒 |
| 工具执行超时 | 30 秒 |
| 单次上游响应大小 | 2 MB |
| 累计工具结果大小 | 8 MB |
| 累计工具调用数 | 256 |

<a id="错误处理"></a>

## 错误处理

握手失败时，核对域名、地域、业务空间、API Key、模型名称及模型开通状态与权限。连接建立后，根据 `error` 事件定位问题，并参见[错误码](../../preparations/error-code.md)。保留事件 ID 便于排查，不以无响应判定协议不支持。

<a id="sdk-与参考"></a>

<a id="websocket-sdk-reference"></a>

<a id="sdk"></a>

## SDK 与参考

-   [Python SDK](../../../_short/realtime-websocket-python-sdk-qwen-omni-realtime-e50924065f85dda8.md)
-   [Java SDK](../../../_short/omni-realtime-java-sdk-13dfd16f685872d7.md)
-   [C# SDK](../../../_short/omni-realtime-csharp-sdk-f5e5dc6601296458.md)

![](data:image/png;base64,)
