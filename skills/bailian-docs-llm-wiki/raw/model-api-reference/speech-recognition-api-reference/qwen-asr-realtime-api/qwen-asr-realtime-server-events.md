# 实时语音识别（Qwen-ASR-Realtime）服务端事件

本文档介绍在与 Qwen-ASR Realtime API 的 WebSocket 会话中，服务端向客户端发送的事件。

**用户指南：**模型介绍、功能特性和完整示例代码请参见[实时语音识别-千问](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide)

## **error**

当服务端检测到错误（包括客户端错误和服务端错误）时，向客户端发送的事件。

**参数**

**类型**

**说明**

type

string

事件类型。固定为`error`。

event\_id

string

事件ID。

error.type

string

错误类型。

error.code

string

错误代码。

error.message

string

具体的报错信息。请按[错误信息](https://help.aliyun.com/zh/model-studio/error-code)所示的解决方案进行处理。

error.param

string

与错误相关的参数。

error.event\_id

string

与错误相关的事件ID。

```
{
  "event_id": "event_B2uoU7VOt1AAITsPRPH9n",
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "code": "invalid_value",
    "message": "Invalid value: 'whisper-1xx'. Supported values are: 'whisper-1'.",
    "param": "session.input_audio_transcription.model",
    "event_id": "event_123"
  }
}
```

## **session.created**

当客户端成功连接到服务端后，服务端响应的第一个事件。该事件包含服务端为此次连接设置的默认配置信息。

**参数**

**类型**

**说明**

type

string

事件类型。固定为`session.created`。

event\_id

string

事件ID。

session.id

string

本次 WebSocket 会话的ID。

session.object

string

固定为`realtime.session`。

session.model

string

当前调用的[模型](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide#ff8c59ef0busr)名称。

session.modalities

array\[string\]

模型输出模态，固定为`["text"]`。

session.input\_audio\_format

string

输入音频格式。

session.input\_audio\_transcription

object

语音识别相关配置参数。详情参见客户端[session.update](https://help.aliyun.com/zh/model-studio/qwen-asr-realtime-client-events#af43722339yva)事件`input_audio_transcription`参数。

session.turn\_detection

object

VAD（Voice Activity Detection，语音活动检测）配置。

session.turn\_detection.type

string

固定为`server_vad`。

session.turn\_detection.threshold

float

VAD检测阈值。

session.turn\_detection.silence\_duration\_ms

integer

VAD断句检测阈值（ms）。

```
{
    "event_id": "event_1234",
    "type": "session.created",
    "session": {
        "id": "sess_001",
        "object": "realtime.session",
        "model": "qwen3-asr-flash-realtime",
        "modalities": ["text"],
        "input_audio_format": "pcm16",
        "input_audio_transcription": null,
        "turn_detection": {
            "type": "server_vad",
            "threshold": 0.5,
            "silence_duration_ms": 200
        }
    }
}
```

## **session.updated**

当客户端发送[session.update](https://help.aliyun.com/zh/model-studio/qwen-asr-realtime-client-events#af43722339yva)事件并成功被服务端处理后，服务端将发送该事件。如果处理过程中出现错误，则直接发送 error 事件。

**参数**

**类型**

**说明**

type

string

事件类型。固定为`session.updated`。

其他参数含义同[session.created](#2c04b24bc3wlo)。

```
{
    "event_id": "event_1234",
    "type": "session.updated",
    "session": {
        "id": "sess_001",
        "object": "realtime.session",
        "model": "gpt-4o-realtime-preview-2024-12-17",
        "modalities": ["text"],
        "input_audio_format": "pcm16",
        "input_audio_transcription": null,
        "turn_detection": {
            "type": "server_vad",
            "threshold": 0.5,
            "silence_duration_ms": 200
        }
    }
}
```

## **input\_audio\_buffer.**speech\_started

此事件仅在 VAD 模式下发送。当服务端在音频缓冲区中检测到语音开始时发送。

该事件可能在每次音频添加到缓冲区时发生（除非已检测到语音开始）。

**参数**

**类型**

**说明**

type

string

事件类型。固定为`input_audio_buffer.speech_started`。

event\_id

string

事件ID。

audio\_start\_ms

integer

在会话期间，从音频开始写入缓冲区到首次检测到语音时的毫秒数。

item\_id

string

将创建的用户消息项的 ID。

```
{
  "event_id": "event_B1lV7FPbgTv9qGxPI1tH4",
  "type": "input_audio_buffer.speech_started",
  "audio_start_ms": 64,
  "item_id": "item_B1lV7jWLscp4mMV8hSs8c"
}
```

## **input\_audio\_buffer.**speech\_stopped

此事件仅在 VAD 模式下发送。当服务端在音频缓冲区中检测到语音结束时发送。

该事件触发后，服务端将紧接着发送一个[conversation.item.created](#04dabbb9b6eto)事件，包含从音频缓冲区创建的用户消息项。

**参数**

**类型**

**说明**

type

string

事件类型。固定为`input_audio_buffer.speech_stopped`。

event\_id

string

事件ID。

audio\_end\_ms

integer

从会话开始到语音停止的毫秒数。

item\_id

string

当语音停止时将创建的用户消息项的 ID。

```
{
  "event_id": "event_B3GGEYh2orwNIdhUagZPz",
  "type": "input_audio_buffer.speech_stopped",
  "audio_end_ms": 28128,
  "item_id": "item_B3GGE8ry4yqbqJGzrVhEM"
}
```

## **input\_audio\_buffer.committed**

-   **VAD模式：**当客户端完成音频数据发送（通过[input\_audio\_buffer.append](https://help.aliyun.com/zh/model-studio/qwen-asr-realtime-client-events#a42f8e9111n72)事件）后，服务端发送该事件。
    
-   **非VAD模式：**客户端完成音频数据发送（通过[input\_audio\_buffer.append](https://help.aliyun.com/zh/model-studio/qwen-asr-realtime-client-events#a42f8e9111n72)事件）并发送[input\_audio\_buffer.commit](https://help.aliyun.com/zh/model-studio/qwen-asr-realtime-client-events#d6d5cd90f3q4c)事件后，服务端发送该事件。
    

**参数**

**类型**

**说明**

type

string

事件类型。固定为`input_audio_buffer.committed`。

event\_id

string

事件ID。

previous\_item\_id

string

前一个对话项的ID

item\_id

string

将创建的用户对话项的 ID。

```
{
    "event_id": "event_1121",
    "type": "input_audio_buffer.committed",
    "previous_item_id": "msg_001",
    "item_id": "msg_002"
}
```

## conversation.item.created

当对话项（item）创建时发送该事件。

**参数**

**类型**

**说明**

type

string

事件类型。固定为`conversation.item.created`。

event\_id

string

事件ID。

previous\_item\_id

string

前一个对话项的ID

item

object

要添加到对话中的条目。

item.id

string

对话项的唯一ID。

item.object

string

固定为 `realtime.item` 。

item.type

string

固定为`message`。

item.status

string

对话项的状态。

item.role

string

消息发送的角色。

item.content

array\[object\]

消息的内容。

item.content.type

string

固定为`input_audio`。

item.content.transcript

string

固定为`null`。完整的识别结果通过[conversation.item.input\_audio\_transcription.completed](#403ecacd74qqg)事件提供。

```
{
  "type": "conversation.item.created",
  "event_id": "event_B3GGKbCfBZTpqFHZ0P8vg",
  "previous_item_id": "item_B3GGE8ry4yqbqJGzrVhEM",
  "item": {
    "id": "item_B3GGEPlolCqdMiVbYIf5L",
    "object": "realtime.item",
    "type": "message",
    "status": "completed",
    "role": "user",
    "content": [
      {
        "type": "input_audio",
        "transcript": null
      }
    ]
  }
}
```

## conversation.item.input\_audio\_transcription.text

此事件会高频发送，用于展示实时识别结果。

**参数**

**类型**

**说明**

type

string

事件类型。固定为`conversation.item.input_audio_transcription.text`。

event\_id

string

事件ID。

item\_id

string

关联的对话项ID。

content\_index

integer

包含音频的内容部分的索引。

language

string

被识别音频的语种。当请求参数`language`已指定语种时，该值与所指定的参数一致。

可能的值如下：

-   zh：中文（普通话、四川话、闽南语、吴语）
    
-   yue：粤语
    
-   en：英文
    
-   ja：日语
    
-   de：德语
    
-   ko：韩语
    
-   ru：俄语
    
-   fr：法语
    
-   pt：葡萄牙语
    
-   ar：阿拉伯语
    
-   it：意大利语
    
-   es：西班牙语
    
-   hi：印地语
    
-   id：印尼语
    
-   th：泰语
    
-   tr：土耳其语
    
-   uk：乌克兰语
    
-   vi：越南语
    

emotion

string

被识别音频的情感。支持的情感如下：

-   `surprised`：惊讶
    
-   `neutral`：平静
    
-   `happy`：愉快
    
-   `sad`：悲伤
    
-   `disgusted`：厌恶
    
-   `angry`：愤怒
    
-   `fearful`：恐惧
    

text

string

已确认的文本前缀。这是当前句子中，模型已确认不会再变更的部分。

stash

string

预识别的文本后缀。这是紧跟在已确认部分之后，模型仍在处理、可能会被修正的临时草稿。

```
{
  "event_id": "event_R7Pfu8QVBfP5HmpcbEFSd",
  "type": "conversation.item.input_audio_transcription.text",
  "item_id": "item_MpJQPNQzqVRc9aC9zMwSj",
  "content_index": 0,
  "language": "zh",
  "emotion": "neutral",
  "text": "",
  "stash": "北京的"
}
```

在任何时刻，要获取当前最完整的句子预览，都需要将这两个字段拼接起来：实时预览句子 = `text` + `stash`。

**点击查看示例**

假设用户正在说：“今天天气不错，阳光明媚。”

以下是您可能会收到的事件流以及如何解读它们：

**时间点**

**用户说话进度**

**API 响应 (text 和 stash)**

**客户端 UI 应显示 (text + stash)**

T1

“今天……”

text: ""

stash: "今天"

今天

T2

“……天气……”

text: ""

stash: "今天天气"

今天天气

T3

“……不错”

text: "今天"

stash: "天气不错"

今天天气不错

（注意，“今天”已被确认并移入text）

T4

（短暂停顿）

text: "今天天气不错，"

stash: ""

今天天气不错，

（前半句完全确认）

T5

“……阳光……”

text: "今天天气不错，"

stash: "阳光"

今天天气不错，阳光

T6

“……明媚。”

text: "今天天气不错，"

stash: "阳光明媚。"

今天天气不错，阳光明媚。

T7

（结束说话）

\-

使用[conversation.item.input\_audio\_transcription.completed](#403ecacd74qqg)的transcript的内容作为最终结果。

## conversation.item.input\_audio\_transcription.completed

向客户端发送最终识别结果。此事件标志着一个对话项（item）的结束。

**参数**

**类型**

**说明**

type

string

事件类型。固定为`conversation.item.input_audio_transcription.completed`。

event\_id

string

事件ID。

item\_id

string

关联的对话项ID。

content\_index

integer

包含音频的内容部分的索引。

language

string

被识别音频的语种。当请求参数`language`已指定语种时，该值与所指定的参数一致。

可能的值如下：

-   zh：中文（普通话、四川话、闽南语、吴语）
    
-   yue：粤语
    
-   en：英文
    
-   ja：日语
    
-   de：德语
    
-   ko：韩语
    
-   ru：俄语
    
-   fr：法语
    
-   pt：葡萄牙语
    
-   ar：阿拉伯语
    
-   it：意大利语
    
-   es：西班牙语
    
-   hi：印地语
    
-   id：印尼语
    
-   th：泰语
    
-   tr：土耳其语
    
-   uk：乌克兰语
    
-   vi：越南语
    

emotion

string

被识别音频的情感。支持的情感如下：

-   `surprised`：惊讶
    
-   `neutral`：平静
    
-   `happy`：愉快
    
-   `sad`：悲伤
    
-   `disgusted`：厌恶
    
-   `angry`：愤怒
    
-   `fearful`：恐惧
    

transcript

string

识别结果。

```
{
  "event_id": "event_B3GGEjPT2sLzjBM74W6kB",
  "type": "conversation.item.input_audio_transcription.completed",
  "item_id": "item_B3GGC53jGOuIFcjZkmEQ9",
  "content_index": 0,
  "language": "zh",
  "emotion": "neutral",
  "transcript": "今天天气怎么样"
}
```

## conversation.item.input\_audio\_transcription.failed

当输入了音频但是识别失败时，服务端发送该事件。与其他 `error` 事件分开处理，便于客户端识别相关的具体项目。

**参数**

**类型**

**说明**

type

string

事件类型。固定为`conversation.item.input_audio_transcription.failed`。

item\_id

string

关联的对话项ID。

content\_index

integer

包含音频的内容部分的索引。

error.code

string

错误代码。

error.message

string

错误消息。

error.param

string

错误相关的参数。

```
{
  "type": "conversation.item.input_audio_transcription.failed",
  "item_id": "<item_id>",
  "content_index": 0,
  "error": {
    "code": "<code>",
    "message": "<message>",
    "param": "<param>"
  }
}
```

## session.finished

会话结束事件，表示当前会话中，所有音频识别已完成。

该事件只有在客户端发送`[session.finish](https://help.aliyun.com/zh/model-studio/qwen-asr-realtime-client-events#147ce70052d4z)`后才会发送，客户端接收到该事件后可主动断开连接。

**参数**

**类型**

**说明**

type

string

事件类型。固定为`session.finished`。

event\_id

string

事件ID。

```
{
  "event_id": "event_2239",
  "type": "session.finished"
}
```
