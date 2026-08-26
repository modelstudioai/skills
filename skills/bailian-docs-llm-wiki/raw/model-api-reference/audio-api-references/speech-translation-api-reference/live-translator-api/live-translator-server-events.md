# 服务端事件

本文介绍 qwen3.5-livetranslate-flash-realtime API 的服务端事件。

> 相关文档：[实时语音/音视频翻译-千问](https://help.aliyun.com/zh/model-studio/qwen3-5-livetranslate-flash-realtime)。

## error

服务端返回的错误信息。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为`error`。

**error**`object`

错误的详细信息。

属性

**type**`string`

错误类型。

**code**`string`

错误码。

**message**`string`

错误信息。

**param**`string`

与错误相关的参数，如`session.modalities`。

```
{
  "event_id": "event_RoUu4T8yExPMI37GKwaOC",
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "code": "invalid_value",
    "message": "Invalid modalities: ['audio']. Supported combinations are: ['text'] and ['audio', 'text'].",
    "param": "session.modalities"
  }
}
```

## session.created

客户端连接后，服务端返回的第一个事件，包含本次连接的默认配置信息。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为`session.created`。

**session**`object`

会话的配置。

属性

**id**`string`

会话的唯一标识符。

**object**`string`

固定为`realtime.session`。

**model**`string`

使用的模型。

**modalities**`array`

模型输出模态设置。

**voice**`string`

模型生成音频的音色。

**input\_audio\_format**`string`

输入音频的格式，默认为`pcm`。

**sample\_rate**`integer`

输入音频的采样率，单位为Hz。

**output\_audio\_format**`string`

输出音频的格式，默认为`pcm`。

**turn\_detection**`object`

VAD（语音活动检测）配置。

**translation**`object`（可选）

翻译配置。

属性

**language**`string`（可选）

设置的翻译目标语种。

**corpus**`object` （可选）

热词配置，用于提升特定词汇的翻译准确性。

属性

**corpus.phrases**`object` （可选）

热词映射表。key 为源语言词汇，value 为目标语言对应翻译，参见[支持的语种](https://help.aliyun.com/zh/model-studio/qwen3-5-livetranslate-flash-realtime#4ffd192226f0s) 。

```
{
    "event_id": "event_QxBGpjBDmDDQQWDtrqBKB",
    "type": "session.created",
    "session": {
        "id": "sess_OozZ1vtbPt2muDflHODIH",
        "object": "realtime.session",
        "model": "qwen3.5-livetranslate-flash-realtime",
        "modalities": [
            "text",
            "audio"
        ],
        "voice": "Cherry",
        "input_audio_format": "pcm",
        "sample_rate": 16000,
        "output_audio_format": "pcm",
        "turn_detection": {
            "type": "server_vad",
            "threshold": 0.2,
            "silence_duration_ms": 1000
        },
        "translation": {
           "language": "en",
           "corpus": {
               "phrases": {
                   "人工智能": "Artificial Intelligence",
                   "机器学习": "Machine Learning"
               }
           }
        }
    }
}
```

## session.updated

收到用户的 `session.update` 请求后，若处理成功，则返回此事件；若出错，则返回 `error` 事件。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为`session.updated`。

**session**`object`

会话的配置。

属性

**id**`string`

会话的唯一标识符。

**object**`string`

固定为`realtime.session`。

**model**`string`

使用的模型。

**modalities**`array`

模型输出模态设置。

**voice**`string`

模型生成音频的音色。

**sample\_rate**`integer`（可选）

输入音频的采样率。

**input\_audio\_format**`string`

输入音频的格式，固定为`pcm`。

**output\_audio\_format**`string`

输出音频的格式，固定为`pcm`。

**input\_audio\_transcription**`object`

输入音频转录配置。仅在会话配置了`input_audio_transcription.model`参数时返回。

属性

**model**`string`

语音识别模型。

**language**`string`

设置的语音识别语种。

**turn\_detection**`object`

VAD（语音活动检测）配置。Manual 模式下（客户端在`session.update`中将该参数设为`null`）不返回此字段。

属性

**type**`string`

VAD 类型，固定为`server_vad`。

**threshold**`float`

VAD 检测灵敏度。

**prefix\_padding\_ms**`integer`

语音开始前保留的音频时长（毫秒），避免丢失语音起始部分。

**silence\_duration\_ms**`integer`

语音结束后需保持静音的最短时长（毫秒），超过该时长即判定语音结束。

**create\_response**`boolean`

VAD 检测到语音结束后，是否自动触发翻译响应。

**interrupt\_response**`boolean`

VAD 检测到新一轮语音开始时，是否打断当前正在生成的翻译响应。

**translation**`object`（可选）

翻译配置。

属性

**language**`string`（可选）

设置的翻译目标语种。

**corpus**`object`（可选）

热词配置，用于提升特定词汇的翻译准确性。

属性

**corpus.phrases**`object`（可选）

热词映射表。key 为源语言词汇，value 为目标语言对应翻译。

**enable\_voice\_clone**`boolean`

是否启用声音复刻。

**voice\_clone\_options**`object`

声音复刻控制参数，仅在`enable_voice_clone`为`true`时返回。

属性

**frequency**`string`

音色复刻频率。

```
{
    "event_id": "event_QxBGpjBDmDDQQWDtrqBKB",
    "type": "session.updated",
    "session": {
        "id": "sess_OozZ1vtbPt2muDflHODIH",
        "object": "realtime.session",
        "model": "qwen3.5-livetranslate-flash-realtime",
        "modalities": [
            "text",
            "audio"
        ],
        "voice": "Ethan",
        "sample_rate": 16000,
        "input_audio_format": "pcm",
        "output_audio_format": "pcm",
        "input_audio_transcription": {
            "model": "qwen3-asr-flash-realtime",
            "language": "zh"
        },
        "turn_detection": {
            "type": "server_vad",
            "threshold": 0.2,
            "prefix_padding_ms": 300,
            "silence_duration_ms": 1000,
            "create_response": true,
            "interrupt_response": true
        },
        "translation": {
           "language": "en",
           "corpus": {
               "phrases": {
                   "人工智能": "Artificial Intelligence",
                   "机器学习": "Machine Learning"
               }
           }
        },
        "enable_voice_clone": true,
        "voice_clone_options": {
            "frequency": "once"
        }
    }
}
```

## session.finished

会话结束事件，表示当前会话中，所有音频翻译已完成。

该事件在客户端发送[session.finish](https://help.aliyun.com/zh/model-studio/live-translator-client-events#f8075550b26jf)后才会发送，客户端接收到该事件后可主动断开连接。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为`session.finished`。

```
{
    "event_id": "event_xxx",
    "type": "session.finished"
}
```

## response.created

当服务端生成新的模型响应时，会返回此事件。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为`response.created`。

**response**`object`

响应对象。

属性

**id** `string`

响应的唯一标识符。

**conversation\_id** `string`

当前会话的唯一标识符。

**object** `string`

对象类型，此事件下固定为`realtime.response`。

**status** `string`

响应状态，取值范围：

-   `completed`（已完成）
-   `failed`（失败）
-   `in_progress`（进行中）
-   `incomplete`（不完整）

**modalities** `array`

响应的模态。

**voice** `string`

模型生成音频的音色。

**output\_audio\_format**`string`

输出音频的格式。

**output** `string`

此事件下目前为空。

```
{
    "event_id": "event_L8hHVI5jYis6BzAjnPWJh",
    "type": "response.created",
    "response": {
        "id": "resp_P79OOMs8LnrXVpiIHUCKR",
        "object": "realtime.response",
        "conversation_id": "conv_UFClXtYkRkFXrs48y8pmK",
        "status": "in_progress",
        "modalities": [
            "text",
            "audio"
        ],
        "voice": "Cherry",
        "output_audio_format": "pcm16",
        "output": []
    }
}
```

## response.done

响应生成完成后，服务端会返回此事件。事件中的 `response` 对象包含除原始音频数据外的全部输出项。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为`response.done`。

**response**`object`

响应对象。

属性

**id** `string`

响应的唯一标识符。

**conversation\_id** `string`

当前会话的唯一标识符。

**object** `string`

对象类型，此事件下固定为`realtime.response`。

**status** `string`

响应的状态。

**modalities** `array`

响应的模态。

**voice** `string`

模型生成音频的音色。

**output\_audio\_format**`string`

输出音频的格式。

**output** `object`

响应的输出。

属性

**id** `string`

响应输出的唯一标识符。

**type** `string`

输出项的类型，当前固定为`message`。

**object** `string`

输出项的对象类型，当前固定为`realtime.item`。

**status** `string`

输出项的状态。

**role** `string`

输出项的角色。

**content** `array`

输出项的内容。

属性

**type** `string`

输出内容的类型。输出为纯文本时，为`text`；输出包含音频时，为`audio`。

**text** `string`

输出的文本内容。

**transcript** `string`

音频转录为文字后的内容。

**usage** `object`

本次响应的 Token 消耗信息。

```
{
  "event_id": "event_CNea8oXNipVanSg2VIzkO",
  "type": "response.done",
  "response": {
    "id": "resp_TfhYTqej692vsGA2jNEtH",
    "object": "realtime.response",
    "conversation_id": "conv_ZtyLfKVm8XqLwYRlsuDih",
    "status": "completed",
    "modalities": [
      "text",
      "audio"
    ],
    "voice": "Cherry",
    "output_audio_format": "pcm16",
    "output": [
      {
        "id": "item_MKtkMwN9RtcyE9eJShyWy",
        "object": "realtime.item",
        "type": "message",
        "status": "completed",
        "role": "assistant",
        "content": [
          {
            "type": "audio",
            "transcript": "Hello? "
          }
        ]
      }
    ],
    "usage": {
      "total_tokens": 56,
      "input_tokens": 47,
      "output_tokens": 9,
      "input_tokens_details": {
        "text_tokens": 20,
        "audio_tokens": 27
      },
      "output_tokens_details": {
        "text_tokens": 2,
        "audio_tokens": 7
      }
    }
  }
}
```

## response.text.text

当输出模态仅包含文本，且模型增量生成新的文本时，服务端将返回此事件。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为`response.text.text`。

**text**`string`

返回的增量文本。

**response\_id**`string`

回复的ID。

**item\_id**`string`

消息项ID，可以关联同一个消息项。

**output\_index**`integer`

目前固定为 0。

**content\_index**`integer`

目前固定为 0。

**stash**`string`

初步生成的临时文本，与当前 `text` 拼接后构成临时生成结果；系统会通过 `response.text.text` 事件持续更新 `text` 和 `stash`，直至收到[response.text.done](https://help.aliyun.com/zh/model-studio/live-translator-server-events#d675635a94jfb)事件，此时可通过 `text` 字段获取完整的最终文本。

```
{
    "event_id": "event_B1lIeyOXR7qJMEExbqtTG",
    "type": "response.text.text",
    "response_id": "resp_B1lIdtjF4Noqpn5NOjznj",
    "item_id": "item_B1lIdJsAJlJiFs8ztWpJt",
    "output_index": 0,
    "content_index": 0,
    "text": "How are",
    "stash": " you today?"
}
```

## response.text.done

当输出模态仅包含文本，且模型生成的文本结束时，服务端返回此事件。

> 当响应中断、不完整或取消时，服务端也会返回此事件。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为`response.text.done`。

**response\_id**`string`

响应的唯一标识符。

**item\_id**`string`

消息项的唯一标识符。

**output\_index**`integer`

目前固定为 0。

**content\_index**`integer`

目前固定为 0。

**text** `string`

模型输出的完整文本。

```
{
    "event_id": "event_B1lIeE2Nac33zn5V7h2mm",
    "type": "response.text.done",
    "response_id": "resp_B1lIdtjF4Noqpn5NOjznj",
    "item_id": "item_B1lIdJsAJlJiFs8ztWpJt",
    "output_index": 0,
    "content_index": 0,
    "text": "How can I assist you today?"
}
```

## response.audio.delta

当输出模态包含音频，且模型增量生成新的音频数据时，服务端将返回此事件。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为`response.audio.delta`。

**response\_id**`string`

响应的唯一标识符。

**item\_id**`string`

消息项唯一标识符。

**output\_index**_integer_

目前固定为 0。

**content\_index**`integer`

目前固定为 0。

**delta** `string`

模型增量输出的音频数据，使用Base64编码。

```
{
    "event_id": "event_B1osWMZBtrEQbiIwW0qHQ",
    "type": "response.audio.delta",
    "response_id": "resp_P79OOMs8LnrXVpiIHUCKR",
    "item_id": "item_OFaPGtzfWCPyGzxnuEX9i",
    "output_index": 0,
    "content_index": 0,
    "delta": "UklGRnoGAABXQVZFZm10IBAAAAAB..."
}
```

## response.audio.done

当输出模态包含音频，且模型生成音频结束时，服务端返回此事件。

> 当响应中断、不完整或取消时，服务端也会返回此事件。

> 该事件不返回完整音频数据。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为`response.audio.done`。

**response\_id**`string`

响应的唯一标识符。

**item\_id**`string`

消息项唯一标识符。

**output\_index**`integer`

目前固定为 0。

**content\_index**`integer`

目前固定为 0。

```
{
    "event_id": "event_B1osWMWoDRYyITDyNYcBu",
    "type": "response.audio.done",
    "response_id": "resp_P79OOMs8LnrXVpiIHUCKR",
    "item_id": "item_OFaPGtzfWCPyGzxnuEX9i",
    "output_index": 0,
    "content_index": 0
}
```

## input\_audio\_buffer.speech\_started

当服务端 VAD（语音活动检测）检测到用户开始说话时，返回此事件。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为`input_audio_buffer.speech_started`。

**audio\_start\_ms**`integer`

检测到语音开始的时间点（毫秒），相对于音频流开始的偏移量。

**item\_id**`string`

关联的消息项唯一标识符。

```
{
    "event_id": "event_xxx",
    "type": "input_audio_buffer.speech_started",
    "audio_start_ms": 568,
    "item_id": "item_xxx"
}
```

## input\_audio\_buffer.speech\_stopped

当服务端 VAD 检测到用户停止说话时，返回此事件，标志本轮语音输入结束。由于翻译响应基于流式语音同步生成，实际的翻译响应可能已经在语音输入过程中开始，无需等待此事件。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为`input_audio_buffer.speech_stopped`。

**audio\_end\_ms**`integer`

检测到语音结束的时间点（毫秒），相对于音频流开始的偏移量。

**item\_id**`string`

关联的消息项唯一标识符。

```
{
    "event_id": "event_xxx",
    "type": "input_audio_buffer.speech_stopped",
    "audio_end_ms": 3900,
    "item_id": "item_xxx"
}
```

## input\_audio\_buffer.committed

Manual 模式（`turn_detection`为`null`）下，客户端发送`input_audio_buffer.commit`事件后，服务端返回此事件进行确认，并自动开始生成翻译响应。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为`input_audio_buffer.committed`。

```
{
    "event_id": "event_xxx",
    "type": "input_audio_buffer.committed"
}
```

## input\_audio\_buffer.cleared

客户端发送`input_audio_buffer.clear`事件后，服务端返回此事件进行确认，表示已清空缓冲区中尚未提交的音频数据。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为`input_audio_buffer.cleared`。

```
{
    "event_id": "event_xxx",
    "type": "input_audio_buffer.cleared"
}
```

## conversation.item.created

当对话中创建新的消息项时，服务端返回此事件。以下场景会触发此事件：

-   服务端开始生成翻译响应时，创建对应的 assistant 消息项（此时`content`为空数组，内容随流式响应逐步填充）。
-   Manual 模式下，客户端发送`input_audio_buffer.commit`事件后，服务端会额外创建一个对应用户输入音频的消息项（`content`中包含`{"type": "input_audio"}`）。

对于同一个 VAD 片段，服务端会分别创建语音识别结果和翻译结果消息项。语音识别结果消息项的 `item.id` 与翻译结果事件的 `previous_item_id` 相同。客户端可据此关联原文和译文，并同时展示。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为`conversation.item.created`。

**previous\_item\_id**`string`

前一消息项的唯一标识符。对于翻译结果事件，该值与同一 VAD 片段的语音识别结果消息项 `item.id` 相同。

**item**`object`

消息项信息。

属性

**id**`string`

消息项的唯一标识符。

**type**`string`

固定为`message`。

**object**`string`

固定为`realtime.item`。

**status**`string`

消息项的状态。

**role**`string`

消息的角色，取值为`assistant`或`user`。

**content**`array`

消息的内容。响应刚创建时为空数组，随流式响应逐步填充；Manual 模式下 commit 产生的用户消息项中包含`{"type": "input_audio"}`。

```
{
    "event_id": "event_xxx",
    "type": "conversation.item.created",
    "previous_item_id": "item_asr_xxx",
    "item": {
        "id": "item_translation_xxx",
        "object": "realtime.item",
        "type": "message",
        "status": "in_progress",
        "role": "assistant",
        "content": []
    }
}
```

## conversation.item.input\_audio\_transcription.text

当配置了`input_audio_transcription.model`参数时，服务端会流式返回输入音频的语音识别结果（源语言原文）。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为`conversation.item.input_audio_transcription.text`。

**item\_id**`string`

消息项唯一标识符。

**content\_index**`integer`

目前固定为 0。

**text**`string`

已确认的识别文本。

**stash**`string`

待确认的识别文本（可能会被后续事件修正）。

**language**`string`

检测到的源语种。

**emotion**`string`

被识别音频的情感。支持的情感如下：

-   `surprised`：惊讶
-   `neutral`：平静
-   `happy`：愉快
-   `sad`：悲伤
-   `disgusted`：厌恶
-   `angry`：愤怒
-   `fearful`：恐惧

```
{
    "event_id": "event_xxx",
    "type": "conversation.item.input_audio_transcription.text",
    "item_id": "item_xxx",
    "content_index": 0,
    "text": "",
    "stash": "今天天气真好",
    "language": "zh",
    "emotion": "neutral"
}
```

## conversation.item.input\_audio\_transcription.completed

当配置了`input_audio_transcription.model`参数时，语音识别完成后服务端会返回此事件，包含最终的完整识别结果。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为`conversation.item.input_audio_transcription.completed`。

**item\_id**`string`

消息项唯一标识符。

**content\_index**`integer`

目前固定为 0。

**transcript**`string`

完整的语音识别结果（源语言原文）。

**language**`string`

检测到的源语种。

**emotion**`string`

被识别音频的情感。支持的情感如下：

-   `surprised`：惊讶
-   `neutral`：平静
-   `happy`：愉快
-   `sad`：悲伤
-   `disgusted`：厌恶
-   `angry`：愤怒
-   `fearful`：恐惧

```
{
    "event_id": "event_xxx",
    "type": "conversation.item.input_audio_transcription.completed",
    "item_id": "item_xxx",
    "content_index": 0,
    "transcript": "今天天气真好，我们一起去公园散步吧。",
    "language": "zh",
    "emotion": ""
}
```

## conversation.item.input\_audio\_transcription.failed

当输入了音频但识别失败时，服务端发送该事件。与其他`error`事件分开处理，便于客户端识别相关的具体项目。

**type**`string`

事件类型，固定为`conversation.item.input_audio_transcription.failed`。

**item\_id**`string`

关联的对话项 ID。

**content\_index**`integer`

包含音频的内容部分的索引。

**error.code**`string`

错误代码。

**error.message**`string`

错误消息。

```
{
    "event_id": "event_xxx",
    "type": "conversation.item.input_audio_transcription.failed",
    "item_id": "item_xxx",
    "content_index": 0,
    "error": {
        "code": "xxx",
        "message": "xxx",
        "param": "xxx"
    }
}
```

## response.audio\_transcript.text

当输出模态包含音频时，服务端可能返回此事件，用于展示实时翻译内容。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为`response.audio_transcript.text`。

**response\_id**`string`

响应的唯一标识符。

**item\_id**`string`

消息项唯一标识符。

**output\_index**`integer`

目前固定为 0。

**content\_index**`integer`

目前固定为 0。

**text**`string`

已确认无误的翻译文本片段。

**stash**`string`

初步翻译的临时文本，与当前 `text` 拼接后构成临时翻译结果；系统会通过 `response.audio_transcript.text` 事件持续更新 `text` 和 `stash`，直至收到[response.audio\_transcript.done](https://help.aliyun.com/zh/model-studio/live-translator-server-events#f4d1698567bsm)事件，此时可通过 `transcript` 字段获取完整的最终翻译文本。

```
{
  "event_id": "event_xxx",
  "type": "response.audio_transcript.text",
  "response_id": "resp_xxx",
  "item_id": "item_xxx",
  "output_index": 0,
  "content_index": 0,
  "text": "Hello,",
  "stash": " who are you?"
}
```

## response.audio\_transcript.done

当输出模态包含音频，且模型生成文本结束时，服务端返回此事件。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为`response.audio_transcript.done`。

**response\_id**`string`

响应的唯一标识符。

**item\_id**`string`

消息项唯一标识符。

**output\_index**`integer`

目前固定为 0。

**content\_index**`integer`

目前固定为 0。

**transcript**`string`

完整文本。

```
{
    "event_id": "event_VN4Q4GJugLcc1S23viW8E",
    "type": "response.audio_transcript.done",
    "response_id": "resp_P79OOMs8LnrXVpiIHUCKR",
    "item_id": "item_JvJauNH2CTXb1D9WV6pD4",
    "output_index": 0,
    "content_index": 0,
    "transcript": "How can I assist you today?"
}
```

## response.output\_item.added

在响应生成过程中创建新输出项时，服务端返回此事件。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为`response.output_item.added`。

**response\_id**`string`

响应的唯一标识符。

**output\_index**`integer`

目前固定为 0。

**item**`object`

输出项信息。

属性

**id**`string`

输出项的唯一标识符。

**type**`string`

固定为 `message`。

**object**`string`

始终为 `realtime.item` 。

**status**`string`

输出项的状态。

**role**`string`

消息的角色。

**content**`string`

消息的内容。

```
{
    "event_id": "event_B4O5yPt3Gjnjy5eYH3plG",
    "type": "response.output_item.added",
    "response_id": "resp_P79OOMs8LnrXVpiIHUCKR",
    "output_index": 0,
    "item": {
        "id": "item_OFaPGtzfWCPyGzxnuEX9i",
        "object": "realtime.item",
        "type": "message",
        "status": "in_progress",
        "role": "assistant",
        "content": []
    }
}
```

## response.output\_item.done

当新的项输出完成时，服务端返回此事件。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为`response.output_item.done`。

**response\_id**`string`

响应的唯一标识符。

**output\_index**`integer`

目前固定为 0。

**item**`object`

输出项信息。

属性

**id**`string`

输出项的唯一标识符。

**object**`string`

始终为 `realtime.item` 。

**type**`string`

固定为 `message`。

**status**`string`

输出项的状态。

**role**`string`

发送消息的角色。

**content**`string`

消息的内容。

```
{
    "event_id": "event_XkiwbYTBC9Wcdwy6uYJ2G",
    "type": "response.output_item.done",
    "response_id": "resp_P79OOMs8LnrXVpiIHUCKR",
    "output_index": 0,
    "item": {
        "id": "item_JvJauNH2CTXb1D9WV6pD4",
        "object": "realtime.item",
        "type": "message",
        "status": "completed",
        "role": "assistant",
        "content": [
            {
                "type": "audio",
                "text": "你好，我是阿里云研发的大规模语言模型，我叫千问。有什么我可以帮助你的吗？"
            }
        ]
    }
}
```

## response.content\_part.added

当新的内容部分输出时，服务端返回此事件。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为`response.content_part.added`。

**response\_id**`string`

响应的唯一标识符。

**item\_id**`string`

消息项唯一标识符。

**output\_index**`integer`

目前固定为 0。

**content\_index**`integer`

目前固定为 0。

**part**`object`

输出项信息。

属性

**type**`string`

内容部分的类型。

**text**`string`

内容部分的文本。

```
{
    "event_id": "event_J2UixwYKZsXg7c9YXZetL",
    "type": "response.content_part.added",
    "response_id": "resp_P79OOMs8LnrXVpiIHUCKR",
    "item_id": "item_OFaPGtzfWCPyGzxnuEX9i",
    "output_index": 0,
    "content_index": 0,
    "part": {
        "type": "audio",
        "text": ""
    }
}
```

## response.content\_part.done

当新的内容部分输出完成时，服务端返回此事件。

**event\_id**`string`

本次事件唯一标识符。

**type**`string`

事件类型，固定为`response.content_part.done`。

**response\_id**`string`

响应的唯一标识符。

**item\_id**`string`

消息项唯一标识符。

**output\_index**`integer`

目前固定为 0。

**content\_index**`integer`

目前固定为 0。

**part**`object`

输出项信息。

属性

**type**`string`

内容部分的类型。

**text**`string`

内容部分的文本。

```
{
    "event_id": "event_VN4Q4GJugLcc1S23viW8E",
    "type": "response.content_part.done",
    "response_id": "resp_P79OOMs8LnrXVpiIHUCKR",
    "item_id": "item_JvJauNH2CTXb1D9WV6pD4",
    "output_index": 0,
    "content_index": 0,
    "part": {
        "type": "audio",
        "text": "你好，我是阿里云研发的大规模语言模型，我叫千问。有什么我可以帮助你的吗？"
    }
}
```
