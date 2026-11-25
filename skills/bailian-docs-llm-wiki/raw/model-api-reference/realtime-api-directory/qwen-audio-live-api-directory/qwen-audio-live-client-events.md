# Qwen-Audio-Live 客户端事件

配置会话、发送音频并回传任务结果。

通过控制 WebSocket 发送 JSON 事件。连接和鉴权见 [WebSocket 接入](qwen-audio-live-websocket-access.md)。

<a id="session-update"></a>

<a id="live-session-update"></a>

## session.update

发送此事件可配置会话，包括前台模型、对话指令和音频传输方式。省略 `session.transport` 时，音频通过控制 WebSocket 收发。服务通过 [`session.updated`](qwen-audio-live-server-events.md#live-session-updated) 确认配置已生效。仅用 WebSocket 时，收到确认后即可发送音频。使用 WebRTC 或 AOQ 时，还需等待媒体连接就绪。

`type`string必填

事件类型，固定为 `session.update`。

`event_id`string必填

客户端事件 ID。非空，最长 128 字符。

`session`object必填

会话配置。

<a id="accordion-查看子字段"></a>

查看子字段

`model`string必填

会话使用的前台语音模型 ID。可选 `qwen-audio-4.0-realtime-preview` 或 `qwen-audio-3.1-realtime-flash`。

双工对话使用 `qwen-audio-4.0-realtime-preview`，并将 `turn_detection.type` 设为 `duplex`。

`instructions`string可选

初次配置会话时，如果省略 `session.instructions`，前台模型使用内置提示词。填写后，您提供的提示词会覆盖内置提示词。

`modalities`array可选

输出模态。默认包含 `audio` 和 `text`。

<a id="live-session-voice"></a>

`voice`string可选

前台模型使用的系统音色 ID。默认值为 `yunshu`。

| 音色名称 | 音色 ID |
| --- | --- |
| 云舒 | `yunshu` |
| 小满 | `xiaoman` |
| 晚风 | `wanfeng` |
| 青柚 | `qingyou` |
| 破晓 | `poxiao` |
| 麦芽 | `maiya` |
| 乌龙 | `wulong` |
| 雪松 | `xuesong` |

`turn_detection`object可选

轮次检测配置。

<a id="accordion-查看子字段-2"></a>

查看子字段

`type`string必填

使用双工对话时设为 `duplex`，前台模型选择 `qwen-audio-4.0-realtime-preview`。

`input_audio_format`string可选

输入格式。纯 WebSocket 使用 `pcm`，默认 16 kHz、单声道 PCM16LE。

`output_audio_format`string可选

输出格式。纯 WebSocket 使用 `pcm`，默认 24 kHz、单声道 PCM16LE。

`tools`array\[object\]可选

应用可以执行的前台函数。默认为空数组。

<a id="accordion-查看子字段-3"></a>

查看子字段

`type`string

工具类型。自定义函数填 `function`。

`name`string

函数名。

`description`string

函数用途。

`parameters`object

使用 JSON Schema 描述函数参数。

<a id="accordion-查看子字段-4"></a>

查看子字段

`type`string

参数结构类型。对象填 `object`。

`properties`object

按参数名定义参数的类型和约束。键名由应用定义。

`required`array\[string\]

必填参数的名称列表。

`additionalProperties`boolean | object

控制是否允许传入未声明的参数。设为 `false` 时拒绝未声明参数。

`delegation`object必填

任务执行方式。

<a id="accordion-查看子字段-5"></a>

查看子字段

`type`string必填

`client` 由应用执行任务。`responses` 由服务调用后台 Responses 模型。

`responses`object条件必填

Responses 模式必填。百炼将此处列出的配置传给后台模型。工具定义的格式见 [Responses API](../../qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。

<a id="accordion-查看子字段-6"></a>

查看子字段

`model`string必填

处理委派任务的后台 Responses 模型 ID，例如 `qwen4-max`。

`instructions`string可选

Responses 模式下的后台任务提示词由您配置。省略时，百炼不提供内置的后台提示词。

`tools`array\[object\]可选

声明供后台模型使用的工具。 工具元素通过 `type` 选择结构。以下字段适用于自定义函数（`type` 为 `function`）。

<a id="accordion-查看子字段-7"></a>

查看子字段

`type`string

工具类型。自定义函数填 `function`。

`name`string

函数名。

`description`string

函数用途。

`parameters`object

使用 JSON Schema 描述函数参数。

<a id="accordion-查看子字段-8"></a>

查看子字段

`type`string

参数结构类型。对象填 `object`。

`properties`object

按参数名定义参数的类型和约束。键名由应用定义。

`required`array\[string\]

必填参数的名称列表。

`additionalProperties`boolean | object

控制是否允许传入未声明的参数。设为 `false` 时拒绝未声明参数。

`transport`object可选

省略或传空对象时使用 WebSocket。

<a id="accordion-查看子字段-9"></a>

查看子字段

`type`string条件必填

显式选择传输方式时填写。`websocket` 使用 WebSocket，`rtc` 使用 WebRTC，`aoq` 使用 AOQ。

`sdp`string条件必填

当 `type` 为 `rtc` 时必填。传入客户端生成的 Offer SDP。见 [WebRTC 接入](../../../_short/qwen-audio-live-webrtc-access-2a873a21a2d29a3b.md)。

`aoq`object可选

AOQ 配置。

<a id="accordion-查看子字段-10"></a>

查看子字段

`ws_audio`boolean可选

是否通过 WebSocket 附加一份下行音频。默认 `false`。

<a id="sec-tabs"></a>

<a id="client-模式"></a>

<a id="client-模式-h4"></a>

#### Client 模式

<a id="code-block"></a>

```json
{
  "type": "session.update",
  "event_id": "evt_update_client",
  "session": {
    "model": "qwen-audio-4.0-realtime-preview",
    "modalities": [
      "text",
      "audio"
    ],
    "turn_detection": {
      "type": "duplex"
    },
    "delegation": {
      "type": "client"
    }
  }
}
```

<a id="responses-模式"></a>

<a id="responses-模式-h4"></a>

#### Responses 模式

<a id="code-block-2"></a>

```json
{
  "type": "session.update",
  "event_id": "evt_update_responses",
  "session": {
    "model": "qwen-audio-4.0-realtime-preview",
    "modalities": [
      "text",
      "audio"
    ],
    "turn_detection": {
      "type": "duplex"
    },
    "delegation": {
      "type": "responses",
      "responses": {
        "model": "qwen4-max"
      }
    }
  }
}
```

<a id="session-input-audio-append"></a>

<a id="live-input-audio-append"></a>

## session.input\_audio.append

仅用 WebSocket 接入时，通过此事件发送一帧音频。使用 WebRTC 时，通过 WebRTC 媒体轨道发送音频。使用 AOQ 时，通过 AOQ 媒体连接发送音频。

`type`string必填

事件类型，固定为 `session.input_audio.append`。

`event_id`string可选

客户端事件 ID。非空，最长 128 字符。

`audio`string必填

Base64 编码的 16 kHz、16 位、单声道 PCM16LE。

<a id="code-block-3"></a>

```json
{
  "type": "session.input_audio.append",
  "audio": "AAAAAA=="
}
```

<a id="session-input-audio-mute"></a>

<a id="live-input-audio-mute"></a>

## session.input\_audio.mute

将输入静音。服务返回 `session.input_audio.muted`。

`type`string必填

事件类型，固定为 `session.input_audio.mute`。

`event_id`string可选

客户端事件 ID。非空，最长 128 字符。

<a id="code-block-4"></a>

```json
{
  "type": "session.input_audio.mute",
  "event_id": "evt_mute"
}
```

<a id="session-input-audio-unmute"></a>

<a id="live-input-audio-unmute"></a>

## session.input\_audio.unmute

恢复音频输入。服务返回 `session.input_audio.unmuted`。

`type`string必填

事件类型，固定为 `session.input_audio.unmute`。

`event_id`string可选

客户端事件 ID。非空，最长 128 字符。

<a id="code-block-5"></a>

```json
{
  "type": "session.input_audio.unmute",
  "event_id": "evt_unmute"
}
```

<a id="session-item-create"></a>

<a id="live-item-create"></a>

## session.item.create

输入用户文本，或回传前台函数结果。应用对同一 `call_id` 只执行一次函数。

`type`string必填

事件类型，固定为 `session.item.create`。

`event_id`string可选

客户端事件 ID。非空，最长 128 字符。

`item`object按用途填写

待写入的会话内容。

<a id="accordion-查看子字段-11"></a>

查看子字段

`type`string必填

填 `message` 或 `function_call_output`。

`role`string按类型填写

消息发送者的角色。下方的用户文本示例使用 `user`。

`content`array按类型填写

`message` 的内容。

<a id="accordion-查看子字段-12"></a>

查看子字段

`type`string必填

文本输入填 `input_text`。

`text`string必填

用户文本。

`call_id`string按类型填写

`function_call_output` 对应的前台函数调用 ID。

`output`string按类型填写

`function_call_output` 的字符串结果。

<a id="sec-tabs-2"></a>

<a id="回传函数结果"></a>

<a id="回传函数结果-h4"></a>

#### 回传函数结果

<a id="code-block-6"></a>

```json
{
  "type": "session.item.create",
  "event_id": "evt_function_result",
  "item": {
    "type": "function_call_output",
    "call_id": "call_stock",
    "output": "{\"stock\":7}"
  }
}
```

<a id="输入文本"></a>

<a id="输入文本-h4"></a>

#### 输入文本

<a id="code-block-7"></a>

```json
{
  "type": "session.item.create",
  "event_id": "evt_user_message",
  "item": {
    "role": "user",
    "type": "message",
    "content": [
      {
        "type": "input_text",
        "text": "请查询雨伞库存。"
      }
    ]
  }
}
```

<a id="session-thinking-append"></a>

<a id="live-thinking-append"></a>

## session.thinking.append

更新任务进度。服务返回 `session.thinking.appended`。

`type`string必填

事件类型，固定为 `session.thinking.append`。

`event_id`string可选

客户端事件 ID。非空，最长 128 字符。

`delegation_id`string必填

使用当前连接收到的 `session.delegation.created` 中的 ID。

`content`string必填

任务进度。

`start_ms`number可选

会话时间线上的开始时间，单位为毫秒。

`end_ms`number可选

结束时间，单位为毫秒。与 `start_ms` 成对提供。两者须为有限非负数，结束时间不得早于开始时间。

<a id="code-block-8"></a>

```json
{
  "type": "session.thinking.append",
  "event_id": "evt_thinking",
  "delegation_id": "task_stock",
  "content": "正在查询库存。"
}
```

<a id="session-instruction-append"></a>

<a id="live-instruction-append"></a>

## session.instruction.append

提供需要用户补充的问题。服务返回 `session.instructions.appended`。

`type`string必填

事件类型，固定为 `session.instruction.append`。

`event_id`string可选

客户端事件 ID。非空，最长 128 字符。

`delegation_id`string必填

使用当前连接收到的 `session.delegation.created` 中的 ID。

`task_id`string可选

通常省略。

`content`string必填

需要用户补充的信息。

`start_ms`number可选

会话时间线上的开始时间，单位为毫秒。

`end_ms`number可选

结束时间，单位为毫秒。与 `start_ms` 成对提供。两者须为有限非负数，结束时间不得早于开始时间。

<a id="code-block-9"></a>

```json
{
  "type": "session.instruction.append",
  "event_id": "evt_instruction",
  "delegation_id": "task_stock",
  "content": "请问要查哪种商品的库存？"
}
```

<a id="session-commentary-append"></a>

<a id="live-commentary-append"></a>

## session.commentary.append

回传本连接受理的任务结果，也可提交用户文本。服务返回 `session.commentary.appended`。

`type`string必填

事件类型，固定为 `session.commentary.append`。

`event_id`string可选

客户端事件 ID。非空，最长 128 字符。

`delegation_id`string任务回传时必填

使用当前连接收到的 `session.delegation.created` 中的 ID。

`content`string可选

任务结果或用户文本。

`start_ms`number可选

会话时间线上的开始时间，单位为毫秒。

`end_ms`number可选

结束时间，单位为毫秒。与 `start_ms` 成对提供。两者须为有限非负数，结束时间不得早于开始时间。

`error`object可选

任务错误信息。

<a id="sec-tabs-3"></a>

<a id="回传任务结果"></a>

<a id="回传任务结果-h4"></a>

#### 回传任务结果

<a id="code-block-10"></a>

```json
{
  "type": "session.commentary.append",
  "event_id": "evt_stock_result",
  "delegation_id": "task_stock",
  "content": "库存还有七把雨伞。"
}
```

<a id="输入文本-2"></a>

<a id="输入文本-2-h4"></a>

#### 输入文本

<a id="code-block-11"></a>

```json
{
  "type": "session.commentary.append",
  "event_id": "evt_user_text",
  "content": "请查询雨伞库存。"
}
```

<a id="response-item-create"></a>

<a id="live-response-item-create"></a>

## response.item.create

在 Responses 模式中添加后台输入。随后发送 `response.create` 启动生成。

`type`string必填

事件类型，固定为 `response.item.create`。

`event_id`string可选

客户端事件 ID。非空，最长 128 字符。

`item`object必填

后台输入。支持 `message` 和 `function_call_output`。

<a id="accordion-查看子字段-13"></a>

查看子字段

`type`string必填

输入项类型。

`role`string按类型填写

消息发送者的角色。下方的用户文本示例使用 `user`。

`content`array按类型填写

用户消息内容。

<a id="accordion-查看子字段-14"></a>

查看子字段

`type`string必填

文本输入填 `input_text`。

`text`string必填

用户文本。

`call_id`string

`function_call_output` 的函数调用 ID。使用后台事件返回的 `call_id`。

`output`string

`function_call_output` 的函数结果，格式为字符串。

<a id="sec-tabs-4"></a>

<a id="输入文本-3"></a>

<a id="输入文本-3-h4"></a>

#### 输入文本

<a id="code-block-12"></a>

```json
{
  "type": "response.item.create",
  "event_id": "evt_backend_item",
  "item": {
    "role": "user",
    "type": "message",
    "content": [
      {
        "type": "input_text",
        "text": "请查询雨伞库存。"
      }
    ]
  }
}
```

<a id="回传后台函数结果"></a>

<a id="回传后台函数结果-h4"></a>

#### 回传后台函数结果

<a id="code-block-13"></a>

```json
{
  "type": "response.item.create",
  "event_id": "evt_backend_output",
  "item": {
    "type": "function_call_output",
    "call_id": "call_stock_001",
    "output": "{\"stock\":7}"
  }
}
```

<a id="response-create"></a>

<a id="live-response-create"></a>

## response.create

应用通过此事件发起后台任务后，直接从 `response.event` 读取后台事件。只有前台模型自动委派任务时，服务才会发送 `session.delegation.created`。

`type`string必填

事件类型，固定为 `response.create`。

`event_id`string可选

客户端事件 ID。非空，最长 128 字符。

`response`object可选

传入后台生成配置。配置格式参见 [Responses API](../../qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。

<a id="code-block-14"></a>

```json
{
  "type": "response.create",
  "event_id": "evt_backend_create"
}
```

<a id="session-close"></a>

<a id="live-session-close"></a>

## session.close

结束会话。服务返回 `session.closed`。

`type`string必填

事件类型，固定为 `session.close`。

`event_id`string必填

客户端事件 ID。非空，最长 128 字符。

<a id="code-block-15"></a>

```json
{
  "type": "session.close",
  "event_id": "evt_close"
}
```
