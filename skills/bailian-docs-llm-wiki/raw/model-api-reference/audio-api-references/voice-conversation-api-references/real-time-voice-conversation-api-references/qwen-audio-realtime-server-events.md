# Qwen-Audio 实时语音对话服务端事件

Qwen-Audio Realtime API 的服务端事件参考。所有服务端事件均包含 event\_id （服务端自动生成）和 type （事件类型）公共字段。

**用户指南**：[实时语音对话（Qwen-Audio-Realtime）](https://help.aliyun.com/zh/model-studio/qwen-audio-realtime-user-guides)。如需了解事件交互时序，请参见[WebSocket API](raw/model-api-reference/audio-api-references/voice-conversation-api-references/real-time-voice-conversation-api-references/fun-audiochat-realtime-websocket-api.md)。

## error

**说明**：请求错误或服务异常时返回。客户端错误（`invalid_request_error`）不中断连接；服务端错误（`server_error`）将终止连接。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为 `error`。

**error**`object`

错误的详细信息。

属性

**type**`string`

错误类型，如 `invalid_request_error`（客户端错误）或 `server_error`（服务端错误）。

**code**`string`

错误码。

**message**`string`

错误信息。

**param**`string`

与错误相关的参数。

```
{
    "event_id": "event_xxx",
    "type": "error",
    "error": {
        "type": "invalid_request_error",
        "code": "invalid_value",
        "message": "Cannot create response while another response is in progress.",
        "param": "response.create"
    }
}
```

## session.created

**说明**：连接建立后服务端发送的首个事件，携带会话默认配置。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为 `session.created`。

**session**`object`

会话的配置信息。

属性

**object**`string`

固定为 `realtime.session`。

**model**`string`

使用的模型名称。

**modalities**`array`

模型输出模态设置。

**voice**`string`

模型生成音频的音色，为系统音色名称或声音复刻音色的 `voice_id`。

**input\_audio\_transcription**`object`

语音转录的配置。

属性

**model**`string`

语音转录模型，如 `fun-asr`。

**turn\_detection**`object`

轮次检测（VAD）的配置。

**id**`string`

会话唯一标识符。

```
{
    "event_id": "event_KiKZC2zrhNsKFPZ5cTpyA",
    "type": "session.created",
    "session": {
        "object": "realtime.session",
        "model": "qwen-audio-3.0-realtime-plus",
        "modalities": ["text", "audio"],
        "voice": "longanqian",
        "input_audio_transcription": {
            "model": "fun-asr"
        },
        "turn_detection": {
            "type": "server_vad",
            "threshold": 0.5,
            "silence_duration_ms": 800
        },
        "id": "sess_A1LbG2D63WELBSawRbpq8"
    }
}
```

## session.updated

**说明**：收到 `session.update` 请求后，若处理成功，则返回此事件，携带更新后的完整会话配置；若出错，则返回 `error` 事件。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为 `session.updated`。

**session**`object`

更新后的完整会话配置信息。结构与 `session.created` 中的 session 对象一致。

```
{
    "event_id": "event_FMG6kiHbILCGiqXFPA98e",
    "type": "session.updated",
    "session": {
        "id": "sess_A1LbG2D63WELBSawRbpq8",
        "object": "realtime.session",
        "model": "pre-fun-realtime-audiochat-beta-3",
        "modalities": ["text", "audio"],
        "voice": "longanqian",
        "input_audio_transcription": {
            "model": "fun-asr"
        },
        "turn_detection": {
            "type": "smart_turn",
            "threshold": 0.1,
            "silence_duration_ms": 900
        }
    }
}
```

## input\_audio\_buffer.speech\_started

**说明**：VAD 检测到语音开始（server\_vad / smart\_turn 模式）。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为 `input_audio_buffer.speech_started`。

**audio\_start\_ms**`integer`

语音开始的时间戳（毫秒）。

**item\_id**`string`

该段语音最终提交时将创建的 item 的 ID。

```
{
    "event_id": "event_xxx",
    "type": "input_audio_buffer.speech_started",
    "audio_start_ms": 1200,
    "item_id": "item_xxx"
}
```

## input\_audio\_buffer.speech\_stopped

**说明**：VAD 检测到语音结束（server\_vad / smart\_turn 模式）。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为 `input_audio_buffer.speech_stopped`。

**audio\_end\_ms**`integer`

语音结束的时间戳（毫秒）。

**item\_id**`string`

将创建的用户消息项的 ID。

**reason**`string`

仅 smart\_turn 模式返回此字段。取值为 `turn_invalid` 时表示当前 turn 被判定为无效轮（无语义内容），不会触发推理。有效轮次时不返回此字段。

```
{
    "event_id": "event_xxx",
    "type": "input_audio_buffer.speech_stopped",
    "audio_end_ms": 3400,
    "item_id": "item_xxx",
    "reason": "turn_invalid"
}
```

## input\_audio\_buffer.committed

**说明**：音频缓冲已提交为用户消息（push-to-talk 的 commit 或 VAD 自动提交）。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为 `input_audio_buffer.committed`。

**previous\_item\_id**`string`

前一条对话项的 ID。

**item\_id**`string`

创建的用户消息项的 ID。

```
{
    "event_id": "event_xxx",
    "type": "input_audio_buffer.committed",
    "previous_item_id": "item_xxx",
    "item_id": "item_xxx"
}
```

## input\_audio\_buffer.cleared

**说明**：音频缓冲已清空（仅 push-to-talk 模式）。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为 `input_audio_buffer.cleared`。

```
{
    "event_id": "event_xxx",
    "type": "input_audio_buffer.cleared"
}
```

## conversation.item.created

**说明**：新的对话项创建成功。用户音频提交、客户端手动创建或助手响应开始时触发。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为 `conversation.item.created`。

**previous\_item\_id**`string`

前一条对话项的 ID。

**item**`object`

创建的对话项。

属性

**id**`string`

对话项的唯一标识符。

**object**`string`

固定为 `realtime.item`。

**type**`string`

对话项类型：`message`（普通消息）或 `function_call`（函数调用）。

**status**`string`

对话项状态，如 `in_progress`、`completed`。

**role**`string`

消息角色，如 `user`、`assistant`。仅 `message` 类型包含。

**content**`array`

消息内容列表。仅 `message` 类型包含。

```
{
    "event_id": "event_xxx",
    "type": "conversation.item.created",
    "previous_item_id": "item_xxx",
    "item": {
        "id": "item_xxx",
        "object": "realtime.item",
        "type": "message",
        "status": "in_progress",
        "role": "assistant",
        "content": []
    }
}
```

## conversation.item.deleted

**说明**：对话项已删除。客户端发送 `conversation.item.delete` 后返回此确认事件。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为 `conversation.item.deleted`。

**item\_id**`string`

已删除的对话项 ID。

```
{
    "event_id": "event_xxx",
    "type": "conversation.item.deleted",
    "item_id": "item_xxx"
}
```

## conversation.item.retrieved

**说明**：查询对话项成功返回。客户端发送 `conversation.item.retrieve` 后返回此事件。音频类型 content 仅包含转写文本，不返回原始音频数据。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为 `conversation.item.retrieved`。

**item**`object`

查询到的对话项完整信息。

属性

**id**`string`

对话项的唯一标识符。

**object**`string`

固定为 `realtime.item`。

**type**`string`

对话项类型：`message`（普通消息）或 `function_call`（函数调用）。

**role**`string`

消息角色，如 `user`、`assistant`。仅 `message` 类型包含。

**content**`array`

消息内容列表。音频类型 content 仅包含转写文本，不返回原始音频数据。

```
{
    "event_id": "event_xxx",
    "type": "conversation.item.retrieved",
    "item": {
        "id": "item_xxx",
        "object": "realtime.item",
        "type": "message",
        "role": "user",
        "content": [
            {
                "type": "input_audio",
                "transcript": "你好"
            }
        ]
    }
}
```

## conversation.item.input\_audio\_transcription.delta

**说明**：ASR 转写增量结果，在语音识别过程中流式返回。包含情绪和语种检测信息。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为 `conversation.item.input_audio_transcription.delta`。

**item\_id**`string`

关联的对话项 ID。

**content\_index**`integer`

内容部分的索引。

**text**`string`

已确定的转写文本。

**stash**`string`

尚未确定的暂存文本。

```
{
    "event_id": "event_xxx",
    "type": "conversation.item.input_audio_transcription.delta",
    "item_id": "item_xxx",
    "content_index": 0,
    "text": "你好",
    "stash": "世界"
}
```

## conversation.item.input\_audio\_transcription.completed

**说明**：ASR 转写最终结果。转写文本会写入对应 item 的 `transcript` 字段。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为 `conversation.item.input_audio_transcription.completed`。

**item\_id**`string`

关联的对话项 ID。

**content\_index**`integer`

内容部分的索引。

**transcript**`string`

完整的转写文本。

```
{
    "event_id": "event_xxx",
    "type": "conversation.item.input_audio_transcription.completed",
    "item_id": "item_xxx",
    "content_index": 0,
    "transcript": "你好世界"
}
```

## conversation.item.input\_audio\_transcription.failed

**说明**：ASR 转写失败。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为 `conversation.item.input_audio_transcription.failed`。

**item\_id**`string`

关联的对话项 ID。

**content\_index**`integer`

内容部分的索引。

**error**`object`

错误的详细信息。

属性

**type**`string`

错误类型，如 `transcription_error`。

**code**`string`

错误码，如 `transcription_failed`。

**message**`string`

错误信息。

```
{
    "event_id": "event_xxx",
    "type": "conversation.item.input_audio_transcription.failed",
    "item_id": "item_xxx",
    "content_index": 0,
    "error": {
        "type": "transcription_error",
        "code": "transcription_failed",
        "message": "ASR transcription failed"
    }
}
```

## conversation.item.ambient\_audio\_transcription.delta

**说明**：**仅 smart\_turn 模式。**环境音频转写增量结果。当 VAD 检测到语音活动但语义判定为非有效轮次（如噪声、“嗯”、“啊”等无语义内容）时，将 ASR 识别结果以 ambient 事件透传给客户端。该事件不会关联到对话上下文中的任何 item，`item_id` 为独立生成的临时 ID。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为 `conversation.item.ambient_audio_transcription.delta`。

**item\_id**`string`

独立生成的临时 ID，不关联到对话上下文中的任何 item。

**content\_index**`integer`

内容部分的索引。

**text**`string`

已确定的转写文本。

**stash**`string`

尚未确定的暂存文本。

```
{
    "event_id": "event_xxx",
    "type": "conversation.item.ambient_audio_transcription.delta",
    "item_id": "item_xxx",
    "content_index": 0,
    "text": "嗯",
    "stash": ""
}
```

## conversation.item.ambient\_audio\_transcription.completed

**说明**：**仅 smart\_turn 模式。**环境音频转写最终结果。与 delta 事件配对，表示一段环境音频的转写结束。该转写结果不会写入对话上下文。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为 `conversation.item.ambient_audio_transcription.completed`。

**item\_id**`string`

独立生成的临时 ID，不关联到对话上下文。

**content\_index**`integer`

内容部分的索引。

**transcript**`string`

完整的转写文本。

```
{
    "event_id": "event_xxx",
    "type": "conversation.item.ambient_audio_transcription.completed",
    "item_id": "item_xxx",
    "content_index": 0,
    "transcript": "嗯",
}
```

## response.created

**说明**：一轮模型推理开始。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为 `response.created`。

**response**`object`

响应对象。

属性

**id**`string`

响应的唯一标识符。

**object**`string`

固定为 `realtime.response`。

**status**`string`

响应状态，如 `in_progress`。

**modalities**`array`

模型输出模态设置。

**voice**`string`

模型生成音频的音色，为系统音色名称或声音复刻音色的 `voice_id`。

**output**`array`

响应的输出项列表，初始为空数组。

```
{
    "event_id": "event_xxx",
    "type": "response.created",
    "response": {
        "id": "resp_xxx",
        "object": "realtime.response",
        "status": "in_progress",
        "modalities": ["text", "audio"],
        "voice": "longanqian",
        "output": []
    }
}
```

## response.output\_item.added

**说明**：响应中新增一个输出项。普通回复的输出项类型为 `message`；Function Calling 的输出项类型为 `function_call`。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为 `response.output_item.added`。

**response\_id**`string`

关联的响应 ID。

**output\_index**`integer`

输出项在响应中的索引。

**item**`object`

新增的输出项。

属性

**id**`string`

输出项的唯一标识符。

**object**`string`

固定为 `realtime.item`。

**type**`string`

输出项类型：`message`（普通消息）或 `function_call`（函数调用）。

**status**`string`

输出项状态，如 `in_progress`。

**role**`string`

消息角色，固定为 `assistant`。仅 `message` 类型包含。

**content**`array`

消息内容列表。仅 `message` 类型包含。

```
{
    "event_id": "event_xxx",
    "type": "response.output_item.added",
    "response_id": "resp_xxx",
    "output_index": 0,
    "item": {
        "id": "item_xxx",
        "object": "realtime.item",
        "type": "message",
        "status": "in_progress",
        "role": "assistant",
        "content": []
    }
}
```

Function Call 输出项示例：

当输出项为函数调用时，`response.output_item.added` / `conversation.item.created` / `response.output_item.done` 中的 `item` 结构如下：

```
{
    "id": "item_xxx",
    "object": "realtime.item",
    "type": "function_call",
    "status": "completed",
    "call_id": "call_xxx",
    "name": "get_weather",
    "arguments": "{\"city\":\"杭州\"}"
}
```

**说明**一轮响应可包含多个 `function_call`，也可能同时包含普通 `message` 输出和 `function_call` 输出。Function Call 部分不会送入 TTS 播报。

## response.content\_part.added

**说明**：输出项中新增一个内容部分。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为 `response.content_part.added`。

**response\_id**`string`

关联的响应 ID。

**item\_id**`string`

关联的输出项 ID。

**output\_index**`integer`

输出项在响应中的索引。

**content\_index**`integer`

内容部分在输出项中的索引。

**part**`object`

新增的内容部分。

属性

**type**`string`

内容类型，如 `audio`、`text`。

**text**`string`

文本内容，初始为空字符串。

```
{
    "event_id": "event_xxx",
    "type": "response.content_part.added",
    "response_id": "resp_xxx",
    "item_id": "item_xxx",
    "output_index": 0,
    "content_index": 0,
    "part": {
        "type": "audio",
        "text": ""
    }
}
```

## response.text.delta

**说明**：纯文本模式下的文本增量事件，流式返回文本片段。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为 `response.text.delta`。

**response\_id**`string`

关联的响应 ID。

**item\_id**`string`

关联的输出项 ID。

**output\_index**`integer`

输出项在响应中的索引。

**content\_index**`integer`

内容部分在输出项中的索引。

**delta**`string`

文本增量片段。

```
{
    "event_id": "event_xxx",
    "type": "response.text.delta",
    "response_id": "resp_xxx",
    "item_id": "item_xxx",
    "output_index": 0,
    "content_index": 0,
    "delta": "你好"
}
```

## response.text.done

**说明**：纯文本模式下的文本输出完成事件。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为 `response.text.done`。

**response\_id**`string`

关联的响应 ID。

**item\_id**`string`

关联的输出项 ID。

**output\_index**`integer`

输出项在响应中的索引。

**content\_index**`integer`

内容部分在输出项中的索引。

**text**`string`

完整的文本输出。

```
{
    "event_id": "event_xxx",
    "type": "response.text.done",
    "response_id": "resp_xxx",
    "item_id": "item_xxx",
    "output_index": 0,
    "content_index": 0,
    "text": "你好，有什么可以帮助你的吗？"
}
```

## response.audio\_transcript.delta

**说明**：音频模式下的文字字幕增量事件，流式返回字幕片段。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为 `response.audio_transcript.delta`。

**response\_id**`string`

关联的响应 ID。

**item\_id**`string`

关联的输出项 ID。

**output\_index**`integer`

输出项在响应中的索引。

**content\_index**`integer`

内容部分在输出项中的索引。

**delta**`string`

字幕增量片段。

```
{
    "event_id": "event_xxx",
    "type": "response.audio_transcript.delta",
    "response_id": "resp_xxx",
    "item_id": "item_xxx",
    "output_index": 0,
    "content_index": 0,
    "delta": "你好"
}
```

## response.audio\_transcript.done

**说明**：音频模式下的字幕输出完成事件。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为 `response.audio_transcript.done`。

**response\_id**`string`

关联的响应 ID。

**item\_id**`string`

关联的输出项 ID。

**output\_index**`integer`

输出项在响应中的索引。

**content\_index**`integer`

内容部分在输出项中的索引。

**transcript**`string`

完整的字幕文本。

```
{
    "event_id": "event_xxx",
    "type": "response.audio_transcript.done",
    "response_id": "resp_xxx",
    "item_id": "item_xxx",
    "output_index": 0,
    "content_index": 0,
    "transcript": "你好，有什么可以帮助你的吗？"
}
```

## response.audio.delta

**说明**：音频模式下的音频数据增量事件。`delta` 字段为 Base64 编码的 PCM 音频数据。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为 `response.audio.delta`。

**response\_id**`string`

关联的响应 ID。

**item\_id**`string`

关联的输出项 ID。

**output\_index**`integer`

输出项在响应中的索引。

**content\_index**`integer`

内容部分在输出项中的索引。

**delta**`string`

Base64 编码的 PCM 音频数据片段。

```
{
    "event_id": "event_xxx",
    "type": "response.audio.delta",
    "response_id": "resp_xxx",
    "item_id": "item_xxx",
    "output_index": 0,
    "content_index": 0,
    "delta": "<base64 编码的音频数据>"
}
```

## response.audio.done

**说明**：音频模式下的音频输出完成事件，不包含音频数据。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为 `response.audio.done`。

**response\_id**`string`

关联的响应 ID。

**item\_id**`string`

关联的输出项 ID。

**output\_index**`integer`

输出项在响应中的索引。

**content\_index**`integer`

内容部分在输出项中的索引。

```
{
    "event_id": "event_xxx",
    "type": "response.audio.done",
    "response_id": "resp_xxx",
    "item_id": "item_xxx",
    "output_index": 0,
    "content_index": 0
}
```

## response.content\_part.done

**说明**：输出项中的内容部分输出完成。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为 `response.content_part.done`。

**response\_id**`string`

关联的响应 ID。

**item\_id**`string`

关联的输出项 ID。

**output\_index**`integer`

输出项在响应中的索引。

**content\_index**`integer`

内容部分在输出项中的索引。

**part**`object`

完成的内容部分。

属性

**type**`string`

内容类型，如 `audio`、`text`。

**text**`string`

文本内容或音频字幕文本。

```
{
    "event_id": "event_xxx",
    "type": "response.content_part.done",
    "response_id": "resp_xxx",
    "item_id": "item_xxx",
    "output_index": 0,
    "content_index": 0,
    "part": {
        "type": "audio",
        "text": "你好，有什么可以帮助你的吗？"
    }
}
```

## response.output\_item.done

**说明**：响应中的输出项输出完成。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为 `response.output_item.done`。

**response\_id**`string`

关联的响应 ID。

**output\_index**`integer`

输出项在响应中的索引。

**item**`object`

完成的输出项完整信息。

属性

**id**`string`

输出项的唯一标识符。

**object**`string`

固定为 `realtime.item`。

**type**`string`

输出项类型：`message`（普通消息）或 `function_call`（函数调用）。

**status**`string`

输出项状态，如 `completed`。

**role**`string`

消息角色，固定为 `assistant`。仅 `message` 类型包含。

**content**`array`

消息内容列表。仅 `message` 类型包含。

```
{
    "event_id": "event_xxx",
    "type": "response.output_item.done",
    "response_id": "resp_xxx",
    "output_index": 0,
    "item": {
        "id": "item_xxx",
        "object": "realtime.item",
        "type": "message",
        "status": "completed",
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": "你好，有什么可以帮助你的吗？"
            }
        ]
    }
}
```

## response.function\_call\_arguments.delta

**说明**：Function Calling 参数增量。模型决定调用工具时，服务端会先发送 `response.output_item.added`（`item.type=function_call`）和对应的 `conversation.item.created`，随后通过本事件流式输出参数片段。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为 `response.function_call_arguments.delta`。

**response\_id**`string`

关联的响应 ID。

**item\_id**`string`

关联的输出项 ID。

**output\_index**`integer`

输出项在响应中的索引。

**call\_id**`string`

函数调用的唯一标识符。

**delta**`string`

函数调用参数的增量片段（JSON 字符串片段）。

```
{
    "event_id": "event_xxx",
    "type": "response.function_call_arguments.delta",
    "response_id": "resp_xxx",
    "item_id": "item_xxx",
    "output_index": 0,
    "call_id": "call_xxx",
    "delta": "{\"city"
}
```

## response.function\_call\_arguments.done

**说明**：Function Calling 参数输出完成。收到该事件后，客户端应执行对应工具，并通过 `conversation.item.create` 写入 `function_call_output`，随后发送 `response.create` 触发二轮推理。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为 `response.function_call_arguments.done`。

**response\_id**`string`

关联的响应 ID。

**item\_id**`string`

关联的输出项 ID。

**output\_index**`integer`

输出项在响应中的索引。

**call\_id**`string`

函数调用的唯一标识符。

**name**`string`

调用的函数名称。

**arguments**`string`

完整的函数调用参数（JSON 字符串）。

```
{
    "event_id": "event_xxx",
    "type": "response.function_call_arguments.done",
    "response_id": "resp_xxx",
    "item_id": "item_xxx",
    "output_index": 0,
    "call_id": "call_xxx",
    "name": "get_weather",
    "arguments": "{\"city\":\"杭州\"}"
}
```

## response.done

**说明**：一轮推理完成。`status` 表示结束原因。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为 `response.done`。

**response**`object`

完整的响应对象。

属性

**id**`string`

响应的唯一标识符。

**object**`string`

固定为 `realtime.response`。

**status**`string`

响应的结束状态。可选值：

-   `completed`：正常完成。
-   `cancelled`：被打断取消。`status_details.reason` 为 `turn_detected`（VAD 打断）或 `client_cancelled`（客户端取消）。
-   `failed`：LLM 或 TTS 错误。

**status\_details**`object`

状态详情，仅在 `cancelled` 或 `failed` 时存在。

属性

**type**`string`

状态类型，如 `cancelled`。

**reason**`string`

取消原因：`turn_detected`（VAD 打断）或 `client_cancelled`（客户端取消）。

**modalities**`array`

模型输出模态设置。

**voice**`string`

模型生成音频的音色，为系统音色名称或声音复刻音色的 `voice_id`。

**output**`array`

响应的输出项列表，包含完整的 item 对象。

**usage**`object`

本次响应的 Token 消耗信息。仅在 `status` 为 `completed` 时返回。

属性

**total\_tokens**`integer`

本次响应消耗的总 Token 数。

**input\_tokens**`integer`

输入 Token 数。

**output\_tokens**`integer`

输出 Token 数。

**input\_tokens\_details**`object`

输入 Token 的分项详情，包含 `text_tokens`（文本 Token 数）和 `audio_tokens`（音频 Token 数，仅在使用音频模态时存在）。

**output\_tokens\_details**`object`

输出 Token 的分项详情，包含 `text_tokens`（文本 Token 数）和 `audio_tokens`（音频 Token 数，仅在使用音频模态时存在）。

**plugins**`object`（可选）

插件使用计量信息。启用联网搜索（`enable_search`）时返回。

属性

**search**`object`

联网搜索计量信息。

属性

**count**`integer`

搜索次数。

**strategy**`string`

搜索策略。

正常完成

```
{
    "event_id": "event_xxx",
    "type": "response.done",
    "response": {
        "id": "resp_xxx",
        "object": "realtime.response",
        "status": "completed",
        "modalities": ["text", "audio"],
        "voice": "longanqian",
        "output": [
            {
                "id": "item_xxx",
                "object": "realtime.item",
                "type": "message",
                "status": "completed",
                "role": "assistant",
                "content": [
                    {
                        "type": "audio",
                        "transcript": "你好，有什么可以帮助你的吗？"
                    }
                ]
            }
        ],
        "usage": {
            "total_tokens": 377,
            "input_tokens": 336,
            "output_tokens": 41,
            "input_tokens_details": {
                "text_tokens": 228,
                "audio_tokens": 108
            },
            "output_tokens_details": {
                "text_tokens": 9,
                "audio_tokens": 32
            }
        }
    }
}
```

被打断取消

```
{
    "event_id": "event_xxx",
    "type": "response.done",
    "response": {
        "id": "resp_xxx",
        "status": "cancelled",
        "status_details": {
            "type": "cancelled",
            "reason": "turn_detected"
        }
    }
}
```

## voiceprint\_audio\_list.in\_progress

**说明**：声纹注册流程异步进行中。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为 `voiceprint_audio_list.in_progress`。

**item\_id**`string`

声纹注册任务的唯一标识符。

```
{
    "event_id": "event_PaEcN7CCrlhE8q4MM2yND",
    "type": "voiceprint_audio_list.in_progress",
    "item_id": "vp_Y12cA986j1KZ9O9YmAXOA"
}
```

## voiceprint\_audio\_list.completed

**说明**：声纹注册流程已完成。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为 `voiceprint_audio_list.completed`。

**item\_id**`string`

声纹注册任务的唯一标识符。

```
{
    "event_id": "event_PaEcN7CCrlhE8q4MM2yND",
    "type": "voiceprint_audio_list.completed",
    "item_id": "vp_Y12cA986j1KZ9O9YmAXOA"
}
```

## voiceprint\_audio\_list.failed

**说明**：声纹注册失败，不阻塞正常对话调用。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为 `voiceprint_audio_list.failed`。

**item\_id**`string`

声纹注册任务的唯一标识符。

**reason**`string`

失败原因描述。

```
{
    "event_id": "event_PaEcN7CCrlhE8q4MM2yND",
    "type": "voiceprint_audio_list.failed",
    "item_id": "vp_Y12cA986j1KZ9O9YmAXOA",
    "reason": ""
}
```
