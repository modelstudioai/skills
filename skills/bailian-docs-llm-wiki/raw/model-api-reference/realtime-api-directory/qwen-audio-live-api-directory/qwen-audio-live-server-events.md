# Qwen-Audio-Live 服务端事件

读取会话状态、语音回复和任务执行结果。

通过控制 WebSocket 接收 JSON 事件。使用 WebRTC 或 AOQ 时，先从控制 WebSocket 等待 `session.updated`。媒体连接就绪后，也可通过 WebRTC DataChannel 或 AOQ 数据轨接收服务端事件。

按 `type` 处理事件。回执的 `client_event_id` 对应请求的 `event_id`。服务端事件自己的 `event_id` 标识当前事件。

<a id="session-created"></a>

<a id="live-session-created"></a>

## session.created

连接建立后，服务返回会话的默认信息。发送 `session.update` 后，等待 `session.updated` 确认配置生效。

`type`string必填

事件类型，固定为 `session.created`。

`event_id`string必填

服务端事件 ID。

`session`object必填

默认会话信息。

<a id="accordion-查看子字段"></a>

查看子字段

`id`string必填

业务会话 ID。AOQ Relay 使用独立的 `sid`。

`object`string必填

兼容对象名，例如 `realtime.session`。

`model`string必填

部署的默认前台语音模型。

`modalities`array按模型返回

输出模态。

`voice`string按模型返回

默认音色。

`turn_detection`object按模型返回

默认轮次检测配置。 以下检测参数在 `type` 为 `server_vad` 时返回。

<a id="accordion-查看子字段-2"></a>

查看子字段

`type`string

轮次检测类型。

`threshold`number

语音活动检测阈值。

`prefix_padding_ms`integer

检测到语音开始时保留的前置音频时长，单位为毫秒。

`silence_duration_ms`integer

判定语音结束所需的静音时长，单位为毫秒。

`create_response`boolean

是否在检测到语音结束后自动生成回复。

`interrupt_response`boolean

检测到用户开始讲话时，是否打断正在生成的回复。

`input_audio_transcription`object按模型返回

输入音频转写能力及默认配置。

<a id="accordion-查看子字段-3"></a>

查看子字段

`model`string

用于输入音频转写的模型。

`model_inference`boolean必填

服务具有接入模型的能力。会话配置生效后再开始推理交互。

<a id="code-block"></a>

```json
{
  "type": "session.created",
  "event_id": "evt_created",
  "session": {
    "id": "sess_demo",
    "object": "realtime.session",
    "model": "<默认前台模型 ID>",
    "modalities": [
      "text",
      "audio"
    ],
    "turn_detection": {
      "type": "server_vad"
    },
    "input_audio_transcription": {
      "model": "<转写模型 ID>"
    },
    "model_inference": true
  }
}
```

<a id="session-updated"></a>

<a id="live-session-updated"></a>

## session.updated

会话配置已生效。使用返回的配置。

`type`string必填

事件类型，固定为 `session.updated`。

`event_id`string必填

服务端事件 ID。

`session`object必填

生效的会话配置。含会话元数据和任务模式。

<a id="accordion-查看子字段-4"></a>

查看子字段

`id`string必填

业务会话 ID。

`model`string必填

生效的前台语音模型。

`object`string按配置返回

会话对象类型。

`modalities`array按配置返回

生效的输出模态。

`delegation`object必填

任务模式。

<a id="accordion-查看子字段-5"></a>

查看子字段

`type`string必填

`client` 或 `responses`。

`transport`object按配置返回

返回所选传输方式的连接信息。

<a id="accordion-查看子字段-6"></a>

查看子字段

`type`string按配置返回

使用 WebRTC 时，值为 `rtc`。

`sdp`string按配置返回

使用 WebRTC 时返回 Answer SDP。客户端将它设为远端描述。详见 [WebRTC 接入](../../../_short/qwen-audio-live-webrtc-access-2a873a21a2d29a3b.md)。

`aoq`object按配置返回

使用 AOQ 时返回临时连接信息。请在收到 `session.updated` 后的 5 分钟内使用返回的 `sid` 和临时凭证发起连接。接入步骤见 [AOQ 接入](../../../_short/qwen-audio-live-aoq-access-7fc752b6a8e53044.md)。

<a id="accordion-查看子字段-7"></a>

查看子字段

`sid`string

AOQ 会话 ID。

`aoqTokenForClient`string

客户端连接 Relay 时使用的临时令牌。

`clientRelayCertFingerprint`string

Relay 的 TLS 证书指纹。

`clientRelayEndpoints`array

可连接的 Relay 地址列表。

<a id="accordion-查看子字段-8"></a>

查看子字段

`endpoint`string

Relay 地址。

`port`integer

Relay 端口。

`route_index`integer

Relay 路由索引。

`extraInfo`object

附加连接信息。

<a id="accordion-查看子字段-9"></a>

查看子字段

`workspaceIdHash`string

业务空间 ID 的哈希值。

<a id="sec-tabs"></a>

<a id="websocket"></a>

<a id="websocket-h4"></a>

#### WebSocket

<a id="code-block-2"></a>

```json
{
  "type": "session.updated",
  "event_id": "evt_updated",
  "session": {
    "id": "sess_demo",
    "object": "realtime.session",
    "model": "qwen-audio-4.0-realtime-preview",
    "modalities": [
      "text",
      "audio"
    ],
    "delegation": {
      "type": "client"
    }
  }
}
```

<a id="webrtc-节选"></a>

<a id="webrtc-节选-h4"></a>

#### WebRTC（节选）

<a id="code-block-3"></a>

```json
{
  "type": "session.updated",
  "event_id": "evt_updated",
  "session": {
    "id": "sess_demo",
    "transport": {
      "type": "rtc",
      "sdp": "<Answer SDP>"
    }
  }
}
```

<a id="aoq-节选"></a>

<a id="aoq-节选-h4"></a>

#### AOQ（节选）

<a id="code-block-4"></a>

```json
{
  "type": "session.updated",
  "event_id": "evt_updated",
  "session": {
    "id": "sess_demo",
    "transport": {
      "aoq": {
        "sid": "<AOQ session ID>",
        "aoqTokenForClient": "<temporary token>",
        "clientRelayCertFingerprint": "<Relay TLS certificate fingerprint>",
        "clientRelayEndpoints": [
          {
            "endpoint": "192.0.2.10",
            "port": 8443,
            "route_index": 0
          }
        ],
        "extraInfo": {
          "workspaceIdHash": "<workspace ID hash>"
        }
      }
    }
  }
}
```

<a id="session-input-audio-muted"></a>

<a id="live-input-audio-muted"></a>

## session.input\_audio.muted

输入已静音。

`type`string必填

事件类型，固定为 `session.input_audio.muted`。

`event_id`string必填

服务端事件 ID。

`client_event_id`string可选

对应客户端请求的 `event_id`。

<a id="code-block-5"></a>

```json
{
  "type": "session.input_audio.muted",
  "event_id": "evt_muted",
  "client_event_id": "evt_mute"
}
```

<a id="session-input-audio-unmuted"></a>

<a id="live-input-audio-unmuted"></a>

## session.input\_audio.unmuted

输入已恢复。

`type`string必填

事件类型，固定为 `session.input_audio.unmuted`。

`event_id`string必填

服务端事件 ID。

`client_event_id`string可选

对应客户端请求的 `event_id`。

<a id="code-block-6"></a>

```json
{
  "type": "session.input_audio.unmuted",
  "event_id": "evt_unmuted",
  "client_event_id": "evt_unmute"
}
```

<a id="session-input-transcript-delta"></a>

<a id="live-input-transcript-delta"></a>

## session.input\_transcript.delta

收到用户语音的转写。

`type`string必填

事件类型，固定为 `session.input_transcript.delta`。

`event_id`string必填

服务端事件 ID。

`delta`string必填

本次返回的转写文本。

`start_ms`number必填

会话时间线上的开始时间，单位为毫秒。

`end_ms`number必填

会话时间线上的结束时间，单位为毫秒。

<a id="code-block-7"></a>

```json
{
  "type": "session.input_transcript.delta",
  "event_id": "evt_input_transcript",
  "delta": "帮我查库存。",
  "start_ms": 1600,
  "end_ms": 1600
}
```

<a id="session-output-transcript-delta"></a>

<a id="live-output-transcript-delta"></a>

## session.output\_transcript.delta

收到前台语音回复的字幕。字幕时间戳用于定位会话时间线。

`type`string必填

事件类型，固定为 `session.output_transcript.delta`。

`event_id`string必填

服务端事件 ID。

`delta`string必填

本次返回的回复文本。

`start_ms`number必填

会话时间线上的开始时间，单位为毫秒。

`end_ms`number必填

会话时间线上的结束时间，单位为毫秒。

<a id="code-block-8"></a>

```json
{
  "type": "session.output_transcript.delta",
  "event_id": "evt_output_transcript",
  "delta": "库存还有七把雨伞。",
  "start_ms": 5400,
  "end_ms": 5400
}
```

<a id="session-output-audio-delta"></a>

<a id="live-output-audio-delta"></a>

## session.output\_audio.delta

收到前台语音的音频分片。

`type`string必填

事件类型，固定为 `session.output_audio.delta`。

`event_id`string可选

服务端事件 ID。

`delta`string必填

Base64 编码的 24 kHz 单声道 PCM16LE 原始音频。解码后字节数为偶数。音频没有 WAV 文件头。

`start_ms`number必填

会话时间线上的开始时间，单位为毫秒。

`end_ms`number必填

会话时间线上的结束时间，单位为毫秒。

<a id="code-block-9"></a>

```json
{
  "type": "session.output_audio.delta",
  "delta": "AAAAAA==",
  "start_ms": 5400,
  "end_ms": 5420
}
```

<a id="session-delegation-created"></a>

<a id="live-delegation-created"></a>

## session.delegation.created

前台模型派发任务。Client 和 Responses 模式都可收到该事件。回传任务结果时，使用对应任务事件中的 `delegation_id`。

`type`string必填

事件类型，固定为 `session.delegation.created`。

`event_id`string必填

服务端事件 ID。

`offset_ms`number必填

本次派发在会话时间线上的偏移，单位为毫秒。

`delegation_id`string必填

本次派发对应的任务 ID。

`task_id`string可选

任务 ID。回传时使用 `delegation_id`。

`summary`string任务派发时返回

本次派发的任务摘要。

`context`object任务派发时返回

任务受理时的上下文快照。

<a id="accordion-查看子字段-10"></a>

查看子字段

`summary`string必填

上下文摘要。

`messages`array\[object\]任务派发时返回

上下文消息。

<a id="accordion-查看子字段-11"></a>

查看子字段

`seq`integer

消息在上下文中的序号。

`item_id`string

消息项 ID。

`role`string

消息发送方的角色。

`source`string

消息来源。

`audio_start_ms`integer

音频开始时间在会话时间线上的偏移，单位为毫秒。

`audio_end_ms`integer

音频结束时间在会话时间线上的偏移，单位为毫秒。

`playback`string

音频播放状态。

`content`string

消息文本。

`incomplete`boolean

上下文快照是否不完整。

`truncated`boolean

上下文快照是否已截断。

`supplements`array按任务返回

本批受理的补充内容及各自的上下文。

<a id="accordion-查看子字段-12"></a>

查看子字段

`summary`string必填

补充内容摘要。

`context`object任务派发时返回

任务受理时的上下文快照。

<a id="accordion-查看子字段-13"></a>

查看子字段

`summary`string必填

上下文摘要。

`messages`array任务派发时返回

上下文消息。

`arguments`string可选

兼容字段。JSON 字符串，可包含 `summary`。

<a id="code-block-10"></a>

```json
{
  "type": "session.delegation.created",
  "event_id": "evt_delegation",
  "offset_ms": 3600,
  "delegation_id": "task_stock",
  "task_id": "task_stock",
  "summary": "查询雨伞库存。",
  "context": {
    "summary": "",
    "messages": [
      {
        "seq": 1,
        "item_id": "item_stock_001",
        "role": "user",
        "audio_start_ms": 900,
        "audio_end_ms": 3600,
        "content": "查询雨伞库存。"
      }
    ],
    "incomplete": false,
    "truncated": false
  },
  "supplements": [
    {
      "summary": "查询雨伞库存。",
      "context": {
        "summary": "",
        "messages": []
      }
    }
  ],
  "arguments": "{\"summary\":\"查询雨伞库存。\"}"
}
```

<a id="session-event"></a>

<a id="live-session-event"></a>

## session.event

接收前台函数调用。使用 `call_id` 关联结果。

`type`string必填

事件类型，固定为 `session.event`。

`event_id`string必填

服务端事件 ID。

`client_event_id`string可选

对应客户端请求的 `event_id`。

`event`object必填

前台模型的函数调用事件。

<a id="accordion-查看子字段-14"></a>

查看子字段

`type`string必填

内层事件名。

`item`object按事件返回

函数调用项。

<a id="accordion-查看子字段-15"></a>

查看子字段

`type`string必填

函数调用项为 `function_call`。

`name`string必填

函数名。

`call_id`string必填

调用 ID。

`arguments`string必填

JSON 字符串形式的函数参数。

`id`string按事件返回

调用项 ID。

`status`string按事件返回

调用项状态。

`output_index`number按事件返回

调用项的输出位置。

`response_id`string按事件返回

前台响应 ID。

<a id="code-block-11"></a>

```json
{
  "type": "session.event",
  "event_id": "evt_frontend_tool",
  "event": {
    "type": "response.output_item.added",
    "item": {
      "type": "function_call",
      "name": "lookup_stock",
      "call_id": "call_stock",
      "arguments": "{\"item\":\"雨伞\"}",
      "id": "item_stock",
      "status": "completed"
    },
    "output_index": 0,
    "response_id": "resp_frontend"
  }
}
```

<a id="response-event"></a>

<a id="live-response-event"></a>

## response.event

服务通过 `response.event` 转发后台模型返回的所有 Responses 流式事件。`event.type` 为 `response.completed` 时，表示后台生成完成。前台语音回复通过字幕和音频事件返回。

`type`string必填

事件类型，固定为 `response.event`。

`event_id`string必填

服务端事件 ID。

`delegation_id`string按事件返回

关联的任务 ID。

`client_event_id`string可选

对应客户端请求的 `event_id`。

`event`object必填

内层事件对象。客户端根据 `event.type` 读取对应字段。下方仅列出部分子字段。Responses 流式事件的结构见 [Responses 流式输出](../../qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md#94ea60632am5g)。

<a id="accordion-查看子字段-16"></a>

查看子字段

`type`string必填

内层事件名。

`response`object按事件返回

后台响应对象。返回字段随事件类型变化。字段定义见 [Responses 响应对象](../../qwen-api-reference/openai-compatible-responses/retrieve-a-response.md#retrieve-resp-h2)。

<a id="accordion-查看子字段-17"></a>

查看子字段

`id`string按事件返回

后台响应 ID。

`usage`object可选

后台模型的 Token 用量。

<a id="accordion-查看子字段-18"></a>

查看子字段

`input_tokens`integer按事件返回

后台模型消耗的输入 Token 数。

`output_tokens`integer按事件返回

后台模型生成的输出 Token 数。

`total_tokens`integer按事件返回

输入和输出的 Token 总数。

<a id="code-block-12"></a>

```json
{
  "type": "response.event",
  "event_id": "evt_backend_completed",
  "delegation_id": "task_calc",
  "event": {
    "type": "response.completed",
    "response": {
      "id": "resp_calc",
      "usage": {
        "input_tokens": 28,
        "output_tokens": 12,
        "total_tokens": 40
      }
    }
  }
}
```

<a id="session-thinking-appended"></a>

<a id="live-thinking-appended"></a>

## session.thinking.appended

服务已受理任务进度。对于请求 `session.thinking.append`，可用关联字段匹配回执。

`type`string必填

事件类型，固定为 `session.thinking.appended`。

`event_id`string必填

服务端事件 ID。

`start_ms`number必填

会话时间线上的开始时间，单位为毫秒。

`end_ms`number必填

会话时间线上的结束时间，单位为毫秒。

`client_event_id`string可选

对应客户端请求的 `event_id`。

<a id="code-block-13"></a>

```json
{
  "type": "session.thinking.appended",
  "event_id": "evt_ack",
  "start_ms": 2000,
  "end_ms": 2000,
  "client_event_id": "evt_client_request"
}
```

<a id="session-instructions-appended"></a>

<a id="live-instructions-appended"></a>

## session.instructions.appended

服务已受理客户端通过 `session.instruction.append` 提交的追问。请求名用 `instruction`，回执名用 `instructions`。回执包含 `client_event_id` 时，可用它匹配请求的 `event_id`。

`type`string必填

事件类型，固定为 `session.instructions.appended`。

`event_id`string必填

服务端事件 ID。

`start_ms`number必填

会话时间线上的开始时间，单位为毫秒。

`end_ms`number必填

会话时间线上的结束时间，单位为毫秒。

`client_event_id`string可选

对应客户端请求的 `event_id`。

<a id="code-block-14"></a>

```json
{
  "type": "session.instructions.appended",
  "event_id": "evt_ack",
  "start_ms": 2000,
  "end_ms": 2000,
  "client_event_id": "evt_client_request"
}
```

<a id="session-commentary-appended"></a>

<a id="live-commentary-appended"></a>

## session.commentary.appended

服务已受理结果或文本。对于请求 `session.commentary.append`，可用关联字段匹配回执。

`type`string必填

事件类型，固定为 `session.commentary.appended`。

`event_id`string必填

服务端事件 ID。

`start_ms`number必填

会话时间线上的开始时间，单位为毫秒。

`end_ms`number必填

会话时间线上的结束时间，单位为毫秒。

`client_event_id`string可选

对应客户端请求的 `event_id`。

<a id="code-block-15"></a>

```json
{
  "type": "session.commentary.appended",
  "event_id": "evt_ack",
  "start_ms": 2000,
  "end_ms": 2000,
  "client_event_id": "evt_client_request"
}
```

<a id="session-usage-updated"></a>

<a id="live-usage-updated"></a>

## session.usage.updated

会话激活后，服务每 5 秒上报一次累计计费时长，空闲时也会上报。当前值取最新的 `usage.seconds`，最终值从 `session.closed` 中读取。后台模型的 Token 用量见 `response.event`。

`type`string必填

事件类型，固定为 `session.usage.updated`。

`event_id`string必填

服务端事件 ID。

`usage`object必填

会话用量。

<a id="accordion-查看子字段-19"></a>

查看子字段

`seconds`number必填

会话累计计费时长（秒）。连接建立后，取 3 秒与实际会话时长中的较大值。

`context_window`object可选

上下文使用情况。

<a id="accordion-查看子字段-20"></a>

查看子字段

`usage_ratio`number可选

Token 用量除以上下文上限。结果可能滞后。

<a id="code-block-16"></a>

```json
{
  "type": "session.usage.updated",
  "event_id": "evt_usage",
  "usage": {
    "seconds": 32.5
  },
  "context_window": {
    "usage_ratio": 0.12
  }
}
```

<a id="session-closed"></a>

<a id="live-session-closed"></a>

## session.closed

会话已结束。停止发送事件并释放资源。需要继续对话时，建立新连接并初始化会话。

`type`string必填

事件类型，固定为 `session.closed`。

`event_id`string必填

服务端事件 ID。

`reason`string必填

关闭原因。可能为 `close_requested`、`expired`、`content`、`remote_hangup` 或 `connection_lost`。

`session`object必填

会话关闭时返回的配置快照。

<a id="accordion-查看子字段-21"></a>

查看子字段

`id`string随快照返回

业务会话 ID。

`object`string随快照返回

会话对象类型。

`status`string随快照返回

快照中的状态可能仍为 `active`。以 `session.closed` 事件判断会话已关闭。

`model`string随快照返回

会话使用的前台语音模型。

`usage`object必填

会话结束时的最终用量。

<a id="accordion-查看子字段-22"></a>

查看子字段

`seconds`number必填

会话累计计费时长（秒）。连接建立后，取 3 秒与实际会话时长中的较大值。

<a id="code-block-17"></a>

```json
{
  "type": "session.closed",
  "event_id": "evt_closed",
  "reason": "close_requested",
  "session": {
    "id": "sess_demo",
    "object": "realtime.session",
    "status": "active",
    "model": "qwen-audio-4.0-realtime-preview"
  },
  "usage": {
    "seconds": 45.8
  }
}
```

<a id="error"></a>

<a id="live-error"></a>

## error

收到 `error` 时，根据 `error.code` 检查请求和会话状态。如果随后收到 `session.closed`，需要继续对话时再建立新连接并配置会话。

`type`string必填

事件类型，固定为 `error`。

`event_id`string必填

服务端事件 ID。

`error`object必填

错误详情。

<a id="accordion-查看子字段-23"></a>

查看子字段

`type`string必填

`invalid_request_error` 或 `server_error`。

`code`string必填

错误码。例如 `invalid_session_configuration` 或 `invalid_event_state`。

`message`string必填

错误说明。

`event_id`string可选

对应客户端请求的 `event_id`。

<a id="code-block-18"></a>

```json
{
  "type": "error",
  "event_id": "evt_server_error",
  "error": {
    "type": "invalid_request_error",
    "code": "invalid_session_configuration",
    "message": "Invalid session configuration",
    "event_id": "evt_update_client"
  }
}
```
