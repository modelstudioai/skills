# 服务端事件

本文介绍 qwen3.5-livetranslate-flash-realtime API 的服务端事件。

> 相关文档：[实时语音/音视频翻译-千问](https://help.aliyun.com/zh/model-studio/qwen3-5-livetranslate-flash-realtime)。

## **error**

服务端返回的错误信息。

**event\_id** `_string_`

本次事件唯一标识符。

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

**type** `_string_`

事件类型，固定为`error`。

**error** `_object_`

错误的详细信息。

**属性**

**type** `_string_`

错误类型。

**code** `_string_`

错误码。

**message** `_string_`

错误信息。

**param** `_string_`

与错误相关的参数，如`session.modalities`。

## **session.created**

客户端连接后，服务端返回的第一个事件，包含本次连接的默认配置信息。

**event\_id** `_string_`

本次事件唯一标识符。

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
        "input_audio_format": "pcm16",
        "output_audio_format": "pcm24",
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

**type** `_string_`

事件类型，固定为`session.created`。

**session** `_object_`

会话的配置。

**属性**

**id** `_string_`

会话的唯一标识符。

**object** `_string_`

固定为`realtime.session`。

**model** `_string_`

使用的模型。

**modalities** `_array_`

模型输出模态设置。

**voice** `_string_`

模型生成音频的音色。

**input\_audio\_format** `_string_`

输入音频的格式，固定为`pcm16`。

**output\_audio\_format** `_string_`

输出音频的格式，固定为`pcm24`。

**translation** `_object_` （可选）

翻译配置。

**属性**

**language** `_string_` （可选）

设置的翻译目标语种。

**corpus** `_object_` （可选）

热词配置，用于提升特定词汇的翻译准确性。

**属性**

**corpus.phrases** `_object_` （可选）

热词映射表。key 为源语言词汇，value 为目标语言对应翻译，参见[支持的语种](https://help.aliyun.com/zh/model-studio/qwen3-5-livetranslate-flash-realtime#4ffd192226f0s)。

## **session.updated**

收到用户的 `session.update` 请求后，若处理成功，则返回此事件；若出错，则返回 `error` 事件。

**event\_id** `_string_`

本次事件唯一标识符。

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

**type** `_string_`

事件类型，固定为`session.updated`。

**session** `_object_`

会话的配置。

**属性**

**id** `_string_`

会话的唯一标识符。

**object** `_string_`

固定为`realtime.session`。

**model** `_string_`

使用的模型。

**modalities** `_array_`

模型输出模态设置。

**voice** `_string_`

模型生成音频的音色。

**sample\_rate** `_integer_` （可选）

输入音频的采样率。

**input\_audio\_format** `_string_`

输入音频的格式，固定为`pcm`。

**output\_audio\_format** `_string_`

输出音频的格式，固定为`pcm`。

**translation** `_object_` （可选）

翻译配置。

**属性**

**language** `_string_` （可选）

设置的翻译目标语种。

**corpus** `_object_` （可选）

热词配置，用于提升特定词汇的翻译准确性。

**属性**

**corpus.phrases** `_object_` （可选）

热词映射表。key 为源语言词汇，value 为目标语言对应翻译。

## **session.finished**

会话结束事件，表示当前会话中，所有音频翻译已完成。

该事件在客户端发送[session.finish](https://help.aliyun.com/zh/model-studio/live-translator-client-events#f8075550b26jf)后才会发送，客户端接收到该事件后可主动断开连接。

**event\_id** `_string_`

本次事件唯一标识符。

```
{
    "event_id": "event_xxx",
    "type": "session.finished"
}
```

**type** `_string_`

事件类型，固定为`session.finished`。

## **response.created**

当服务端生成新的模型响应时，会返回此事件。

**event\_id** `_string_`

本次事件唯一标识符。

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
        "output_audio_format": "pcm24",
        "output": []
    }
}
```

**type** `_string_`

事件类型，固定为`response.created`。

**response** `_object_`

响应对象。

**属性**

**id** `_string_`

响应的唯一标识符。

**conversation\_id** `_string_`

当前会话的唯一标识符。

**object** `_string_`

对象类型，此事件下固定为`realtime.response`。

**status** `_string_`

响应状态，取值范围：

-   `completed`（已完成）
    
-   `failed`（失败）
    
-   `in_progress`（进行中）
    
-   `incomplete`（不完整）
    

**modalities** `_array_`

响应的模态。

**voice** `_string_`

模型生成音频的音色。

**output\_audio\_format** `_string_`

输出音频的格式，固定为`pcm24`。

**output** `_string_`

此事件下目前为空。

## **response.done**

响应生成完成后，服务端会返回此事件。事件中的 `response` 对象包含除原始音频数据外的全部输出项。

**event\_id** `_string_`

本次事件唯一标识符。

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
    "output_audio_format": "pcm24",
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

**type** `_string_`

事件类型，固定为`response.done`。

**response** `_object_`

响应对象。

**属性**

**id** `_string_`

响应的唯一标识符。

**conversation\_id** `_string_`

当前会话的唯一标识符。

**object** `_string_`

对象类型，此事件下固定为`realtime.response`。

**status** `_string_`

响应的状态。

**modalities** `_array_`

响应的模态。

**voice** `_string_`

模型生成音频的音色。

**output\_audio\_format** `_string_`

输出音频的格式，固定为`pcm24`。

**output** `_object_`

响应的输出。

**属性**

**id** `_string_`

响应输出的唯一标识符。

**type** `_string_`

输出项的类型，当前固定为`message`。

**object** `_string_`

输出项的对象类型，当前固定为`realtime.item`。

**status** `_string_`

输出项的状态。

**role** `_string_`

输出项的角色。

**content** `_array_`

输出项的内容。

**属性**

**type** `_string_`

输出内容的类型。输出为纯文本时，为`text`；输出包含音频时，为`audio`。

**text** `_string_`

输出的文本内容。

**transcript** `_string_`

音频转录为文字后的内容。

**usage** `_object_`

本次响应的 Token 消耗信息。

## **response.text.text**

当输出模态仅包含文本，且模型增量生成新的文本时，服务端将返回此事件。

**event\_id** `_string_`

本次事件唯一标识符。

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

**type** `_string_`

事件类型，固定为`response.text.text`。

**text** `_string_`

返回的增量文本。

**response\_id** `_string_`

回复的ID。

**item\_id** `_string_`

消息项ID，可以关联同一个消息项。

**output\_index** `_integer_`

目前固定为 0。

**content\_index** `_integer_`

目前固定为 0。

**stash** `_string_`

初步生成的临时文本，与当前 `text` 拼接后构成临时生成结果；系统会通过 `response.text.text` 事件持续更新 `text` 和 `stash`，直至收到[response.text.done](#d675635a94jfb)事件，此时可通过 `text` 字段获取完整的最终文本。

## **response.text.done**

当输出模态仅包含文本，且模型生成的文本结束时，服务端返回此事件。

> 当响应中断、不完整或取消时，服务端也会返回此事件。

**event\_id** `_string_`

本次事件唯一标识符。

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

**type** `_string_`

事件类型，固定为`response.text.done`。

**response\_id** `_string_`

响应的唯一标识符。

**item\_id** `_string_`

消息项的唯一标识符。

**output\_index**`_integer_`

目前固定为 0。

**content\_index**`_integer_`

目前固定为 0。

**text** `_string_`

模型输出的完整文本。

## **response.audio.delta**

当输出模态包含音频，且模型增量生成新的音频数据时，服务端将返回此事件。

**event\_id** `_string_`

本次事件唯一标识符。

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

**type** `_string_`

事件类型，固定为`response.audio.delta`。

**response\_id** `_string_`

响应的唯一标识符。

**item\_id** `_string_`

消息项唯一标识符。

**output\_index**_integer_

目前固定为 0。

**content\_index**`_integer_`

目前固定为 0。

**delta** `_string_`

模型增量输出的音频数据，使用Base64编码。

## **response.audio.done**

当输出模态包含音频，且模型生成音频结束时，服务端返回此事件。

> 当响应中断、不完整或取消时，服务端也会返回此事件。

> 该事件不返回完整音频数据。

**event\_id** `_string_`

本次事件唯一标识符。

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

**type** `_string_`

事件类型，固定为`response.audio.done`。

**response\_id** `_string_`

响应的唯一标识符。

**item\_id** `_string_`

消息项唯一标识符。

**output\_index**`_integer_`

目前固定为 0。

**content\_index**`_integer_`

目前固定为 0。

## **conversation.item.input\_audio\_transcription.text**

当配置了`input_audio_transcription.model`参数时，服务端会流式返回输入音频的语音识别结果（源语言原文）。

**event\_id** `_string_`

本次事件唯一标识符。

```
{
    "event_id": "event_xxx",
    "type": "conversation.item.input_audio_transcription.text",
    "item_id": "item_xxx",
    "content_index": 0,
    "text": "",
    "stash": "今天天气真好",
    "language": "zh"
}
```

**type** `_string_`

事件类型，固定为`conversation.item.input_audio_transcription.text`。

**item\_id** `_string_`

消息项唯一标识符。

**content\_index** `_integer_`

目前固定为 0。

**text** `_string_`

已确认的识别文本。

**stash** `_string_`

待确认的识别文本（可能会被后续事件修正）。

**language** `_string_`

检测到的源语种。

## **conversation.item.input\_audio\_transcription.completed**

当配置了`input_audio_transcription.model`参数时，语音识别完成后服务端会返回此事件，包含最终的完整识别结果。

**event\_id** `_string_`

本次事件唯一标识符。

```
{
    "event_id": "event_xxx",
    "type": "conversation.item.input_audio_transcription.completed",
    "item_id": "item_xxx",
    "content_index": 0,
    "transcript": "今天天气真好，我们一起去公园散步吧。",
    "language": "zh"
}
```

**type** `_string_`

事件类型，固定为`conversation.item.input_audio_transcription.completed`。

**item\_id** `_string_`

消息项唯一标识符。

**content\_index** `_integer_`

目前固定为 0。

**transcript** `_string_`

完整的语音识别结果（源语言原文）。

**language** `_string_`

检测到的源语种。

## **response.audio\_transcript.text**

当输出模态包含音频时，服务端可能返回此事件，用于展示实时翻译内容。

**event\_id** `_string_`

本次事件唯一标识符。

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

**type** `_string_`

事件类型，固定为`response.audio_transcript.text`。

**response\_id** `_string_`

响应的唯一标识符。

**item\_id** `_string_`

消息项唯一标识符。

**output\_index**`_integer_`

目前固定为 0。

**content\_index**`_integer_`

目前固定为 0。

**text** `_string_`

已确认无误的翻译文本片段。

**stash** `_string_`

初步翻译的临时文本，与当前 `text` 拼接后构成临时翻译结果；系统会通过 `response.audio_transcript.text` 事件持续更新 `text` 和 `stash`，直至收到[response.audio\_transcript.done](#f4d1698567bsm)事件，此时可通过 `transcript` 字段获取完整的最终翻译文本。

## **response.audio\_transcript.done**

当输出模态包含音频，且模型生成文本结束时，服务端返回此事件。

**event\_id** `_string_`

本次事件唯一标识符。

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

**type** `_string_`

事件类型，固定为`response.audio_transcript.done`。

**response\_id** `_string_`

响应的唯一标识符。

**item\_id** `_string_`

消息项唯一标识符。

**output\_index**`_integer_`

目前固定为 0。

**content\_index**`_integer_`

目前固定为 0。

**transcript** `_string_`

完整文本。

## **response.output\_item.added**

在响应生成过程中创建新输出项时，服务端返回此事件。

**event\_id** `_string_`

本次事件唯一标识符。

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

**type** `_string_`

事件类型，固定为`response.output_item.added`。

**response\_id** `_string_`

响应的唯一标识符。

**output\_index**`_integer_`

目前固定为 0。

**item**`_object_`

输出项信息。

**属性**

**id** `_string_`

输出项的唯一标识符。

**type** `_string_`

固定为 `message`。

**object** `_string_`

始终为 `realtime.item` 。

**status** `_string_`

输出项的状态。

**role** `_string_`

消息的角色。

**content** `_string_`

消息的内容。

## **response.output\_item.done**

当新的项输出完成时，服务端返回此事件。

**event\_id** `_string_`

本次事件唯一标识符。

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

**type** `_string_`

事件类型，固定为`response.output_item.done`。

**response\_id** `_string_`

响应的唯一标识符。

**output\_index**`_integer_`

目前固定为 0。

**item**`_object_`

输出项信息。

**属性**

**id** `_string_`

输出项的唯一标识符。

**object** `_string_`

始终为 `realtime.item` 。

**type** `_string_`

固定为 `message`。

**status** `_string_`

输出项的状态。

**role** `_string_`

发送消息的角色。

**content** `_string_`

消息的内容。

## **response.content\_part.added**

当新的内容部分输出时，服务端返回此事件。

**event\_id** `_string_`

本次事件唯一标识符。

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

**type** `_string_`

事件类型，固定为`response.content_part.added`。

**response\_id** `_string_`

响应的唯一标识符。

**item\_id** `_string_`

消息项唯一标识符。

**output\_index**`_integer_`

目前固定为 0。

**content\_index**`_integer_`

目前固定为 0。

**part**`_object_`

输出项信息。

**属性**

**type** `_string_`

内容部分的类型。

**text** `_string_`

内容部分的文本。

## **response.content\_part.done**

当新的内容部分输出完成时，服务端返回此事件。

**event\_id** `_string_`

本次事件唯一标识符。

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

**type** `_string_`

事件类型，固定为`response.content_part.done`。

**response\_id** `_string_`

响应的唯一标识符。

**item\_id** `_string_`

消息项唯一标识符。

**output\_index**`_integer_`

目前固定为 0。

**content\_index**`_integer_`

目前固定为 0。

**part**`_object_`

输出项信息。

**属性**

**type** `_string_`

内容部分的类型。

**text** `_string_`

内容部分的文本。
