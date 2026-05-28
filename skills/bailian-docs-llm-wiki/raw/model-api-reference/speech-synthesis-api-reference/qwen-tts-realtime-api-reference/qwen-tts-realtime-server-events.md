# 服务端事件

本文介绍 Qwen-TTS-Realtime API 的服务端事件。

> 相关文档：[实时语音合成-千问](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide)。

## **error**

不论是遇到客户端错误还是服务端错误，服务端都会响应该事件。

**event\_id** `_string_`

服务端事件ID。

```
{
  "event_id": "event_QzAVZRVa9hKqM5VOaHunh",
  "type": "error",
  "error": {
    "code": "invalid_value",
    "message": "Session update error: session already started or finished or failed."
  }
}
```

**type** `_string_`

事件类型，固定为`error`。

**error** `_object_`

错误详情。

**属性**

**code** _string_

错误码。

**message** _string_

错误信息。

## **session.created**

客户端连接到服务端后，响应的第一个事件，该事件返回时会携带服务端对此次连接的默认配置信息。

**event\_id** `_string_`

服务端事件ID。

```
{
  "event_id": "event_xxx",
  "type": "session.created",
  "session": {
    "object": "realtime.session",
    "mode": "server_commit",
    "model": "qwen-tts-realtime",
    "voice": "Cherry",
    "response_format": "pcm",
    "sample_rate": 24000,
    "id": "sess_xxx"
  }
}
```

**type** `_string_`

事件类型，固定为`session.created`。

**session** `_object_`

会话配置。

**属性**

**id** `_string_`

会话ID。

**object** `_string_`

会话服务名。

**mode** `_string_`

交互模式，`server_commit`或`commit`。

**model** `_string_`

使用的模型。

**voice** `_string_`

使用的音色。

**response\_format** `_string_`

音频格式。

**sample\_rate** `_integer_`

音频采样率。

## **session.updated**

接收到客户端的`session.update`请求并正确处理后返回。如果出现错误，则直接返回error事件。

**event\_id** `_string_`

服务端事件ID。

```
{
  "event_id": "event_xxx",
  "type": "session.updated",
  "session": {
    "id": "sess_xxx",
    "object": "realtime.session",
    "model": "qwen-tts-realtime",
    "voice": "Cherry",
    "language_type": "Chinese",
    "mode": "commit",
    "response_format": "pcm",
    "sample_rate": 24000
  }
}
```

**type** `_string_`

事件类型，固定为`session.updated`。

**session** `_object_`

会话配置。

**属性**

**id** `_string_`

会话ID。

**object** `_string_`

会话服务名。

**mode** `_string_`

交互模式，`server_commit`或`commit`。

**model** `_string_`

使用的模型。

**voice** `_string_`

使用的音色。

**response\_format** `_string_`

音频格式。

**sample\_rate** `_integer_`

音频采样率。

**language\_type** `_string_`

音频语种。

## **input\_text\_buffer.committed**

客户端发送`input_text_buffer.commit`事件后，服务端的响应事件。

**event\_id** `_string_`

服务端事件ID。

```
{
  "event_id": "event_FC6MA88wS2oEeXkPvWsxX",
  "type": "input_text_buffer.committed",
  "item_id": ""
}
```

**type** `_string_`

事件类型，固定为`input_text_buffer.committed`。

**item\_id** `_string_`

将创建的用户消息项的 ID。

## **input\_text\_buffer.****cleared**

客户端发送`input_audio_buffer.clear`事件后，服务端的响应事件。

**event\_id** `_string_`

服务端事件ID。

```
{
    "event_id": "event_1122",
    "type": "input_text_buffer.cleared"
}
```

**type** `_string_`

事件类型，固定为`input_text_buffer.cleared`。

## **response.created**

客户端发送`input_text_buffer.commit`事件后，服务端的响应事件。

**event\_id** `_string_`

服务端事件ID。

```
{
  "event_id": "event_IMnLqDvG6Ahhk7sWV2uOs",
  "type": "response.created",
  "response": {
    "id": "resp_USvBwHktHcz76r6GaIJUV",
    "object": "realtime.response",
    "conversation_id": "",
    "status": "in_progress",
    "voice": "Cherry",
    "output": []
  }
}
```

**type** `_string_`

事件类型，固定为`response.created`。

**response** `_object_`

响应详情。

**属性**

**id** `_string_`

响应ID。

**object** `_string_`

对象类型，在此事件下固定为`realtime.response`。

**status** `_string_`

响应的最终状态，取值范围：

-   completed
    
-   failed
    
-   in\_progress
    
-   incomplete
    

**voice** `_string_`

使用的音色。

**output** `_array_`

在此事件下为空。

## **response.output\_item.added**

当新的item项需要输出时，服务端返回此事件。

**event\_id** `_string_`

服务端事件ID。

```
{
  "event_id": "event_INDGnGNulaXCrStd9ZM5X",
  "type": "response.output_item.added",
  "response_id": "resp_USvBwHktHcz76r6GaIJUV",
  "output_index": 0,
  "item": {
    "id": "item_FIrYGaNVK3rbIZqeY4QjM",
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

响应的ID。

**output\_index** `_integer_`

响应输出项的索引，目前固定为0。

**item** `_object_`

输出项信息。

**属性**

**id** `_string_`

输出项ID。

**object** `_string_`

始终为 `realtime.item`。

**status** `_string_`

输出项的状态。

**content** `_array_`

消息的内容。

## **response.content\_part.added**

当新的内容项需要输出时，服务端返回此事件。

**event\_id** `_string_`

服务端事件ID。

```
{
  "event_id": "event_DigZ95MWN36YYyyjcENoq",
  "type": "response.content_part.added",
  "response_id": "resp_USvBwHktHcz76r6GaIJUV",
  "item_id": "item_FIrYGaNVK3rbIZqeY4QjM",
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

响应的ID。

**item\_id** `_string_`

消息项ID。

**output\_index** `_integer_`

响应输出项的索引，目前固定为0。

**content\_index** `_integer_`

响应输出项中内部部分的索引，目前固定为0。

**part** `_object_`

已完成的内容部分。

**属性**

**type** `_string_`

内容部分的类型。

**text** `_string_`

内容部分的文本。

## **response.audio.delta**

当模型增量生成新的audio数据时，系统会返回服务器 response.audio.delta 事件。

**event\_id** `_string_`

服务端事件ID。

```
{
  "event_id": "event_B1osWMZBtrEQbiIwW0qHQ",
  "type": "response.audio.delta",
  "response_id": "resp_B1osWTzBb8hO0WsELHgVP",
  "item_id": "item_B1osWH81fXDoyim1T5fsF",
  "output_index": 0,
  "content_index": 0,
  "delta": "base64 audio"
}
```

**type** `_string_`

事件类型，固定为`response.audio.delta`。

**response\_id** `_string_`

响应的ID。

**item\_id** `_string_`

消息项ID。

**output\_index** `_integer_`

响应输出项的索引，目前固定为0。

**content\_index** `_integer_`

响应输出项中内部部分的索引，目前固定为0。

**delta** `_string_`

模型增量输出的audio数据，使用Base64编码。

## **response.content\_part.done**

当新的内容项输出完成时，服务端返回此事件。

**event\_id** `_string_`

服务端事件ID。

```
{
  "event_id": "event_Vo2YUjlYQJ4colH8nVzkU",
  "type": "response.content_part.done",
  "response_id": "resp_USvBwHktHcz76r6GaIJUV",
  "item_id": "item_FIrYGaNVK3rbIZqeY4QjM",
  "output_index": 0,
  "content_index": 0,
  "part": {
    "type": "audio",
    "text": ""
  }
}
```

**type** `_string_`

事件类型，固定为`response.content_part.done`。

**response\_id** `_string_`

响应的ID。

**item\_id** `_string_`

消息项ID。

**output\_index** `_integer_`

响应输出项的索引，目前固定为0。

**content\_index** `_integer_`

响应输出项中内部部分的索引，目前固定为0。

**part** `_object_`

已完成的内容部分。

**属性**

**type** `_string_`

内容部分的类型。

**text** `_string_`

内容部分的文本。

## **response.output\_item.done**

当新的item输出完成时，服务端返回此事件。

**event\_id** `_string_`

服务端事件ID。

```
{
  "event_id": "event_LO6SJRKIQ9NBayyYB8a1A",
  "type": "response.output_item.done",
  "response_id": "resp_USvBwHktHcz76r6GaIJUV",
  "output_index": 0,
  "item": {
    "id": "item_FIrYGaNVK3rbIZqeY4QjM",
    "object": "realtime.item",
    "type": "message",
    "status": "completed",
    "role": "assistant",
    "content": [
      {
        "type": "audio",
        "text": ""
      }
    ]
  }
}
```

**type** `_string_`

事件类型，固定为`response.output_item.done`。

**response\_id** `_string_`

响应的ID。

**output\_index** `_integer_`

响应输出项的索引，目前固定为0。

**item** `_object_`

输出项信息。

**属性**

**id** `_string_`

输出项ID。

**object** `_string_`

始终为 `realtime.item`。

**status** `_string_`

输出项的状态。

**content** `_array_`

消息的内容。

## **response.audio.done**

当模型生成audio数据完成时，系统会返回服务器 response.audio.done 事件。

**event\_id** `_string_`

服务端事件ID。

```
{
  "event_id": "event_LZaOHPzXYMUXGBcVkBmKX",
  "type": "response.audio.done",
  "response_id": "resp_USvBwHktHcz76r6GaIJUV",
  "item_id": "item_FIrYGaNVK3rbIZqeY4QjM",
  "output_index": 0,
  "content_index": 0
}
```

**type** `_string_`

事件类型，固定为`response.audio.done`。

**response\_id** `_string_`

响应的ID。

**item\_id** `_string_`

消息项ID。

**output\_index** `_integer_`

响应输出项的索引，目前固定为0。

**content\_index** `_integer_`

响应输出项中内部部分的索引，目前固定为0。

## **response.done**

当响应生成完成时，服务端会返回此事件。该事件中包含的 Response 对象将包含 Response 中的所有输出项，但不包括已返回的原始音频数据。

**event\_id** `_string_`

服务端事件ID。

## Qwen3-TTS Realtime

```
{
    "event_id": "event_Aemy83XqHFFDDSeJIDn6N",
    "type": "response.done",
    "response": {
        "id": "resp_LFeR42yXZ9SxUAeXjmyTz",
        "object": "realtime.response",
        "conversation_id": "",
        "status": "completed",
        "modalities": [
            "text",
            "audio"
        ],
        "voice": "Cherry",
        "output": [
            {
                "id": "item_Ae1lv2XmRljRSG96L8Zm1",
                "object": "realtime.item",
                "type": "message",
                "status": "completed",
                "role": "assistant",
                "content": [
                    {
                        "type": "audio",
                        "transcript": ""
                    }
                ]
            }
        ],
        "usage": {
            "characters": 25
        }
    }
}
```

## Qwen-TTS Realtime

```
{
  "event_id": "event_xxx",
  "type": "response.done",
  "response": {
    "id": "resp_xxx",
    "object": "realtime.response",
    "conversation_id": "",
    "status": "completed",
    "modalities": [
      "text",
      "audio"
    ],
    "voice": "Cherry",
    "output": [
      {
        "id": "item_FIrYGaNVK3rbIZqeY4QjM",
        "object": "realtime.item",
        "type": "message",
        "status": "completed",
        "role": "assistant",
        "content": [
          {
            "type": "audio",
            "transcript": ""
          }
        ]
      }
    ],
    "usage": {
      "total_tokens": 67,
      "input_tokens": 3,
      "output_tokens": 64,
      "input_tokens_details": {
        "text_tokens": 3
      },
      "output_tokens_details": {
        "text_tokens": 0,
        "audio_tokens": 64
      }
    }
  }
}
```

**type** `_string_`

事件类型，固定为`response.done`。

**response\_id** `_string_`

响应的ID。

**response** `_object_`

响应详情。

**属性**

**id** `_string_`

响应ID。

**object** `_string_`

对象类型，在此事件下固定为`realtime.response`。

**output** `_array_`

响应的输出。

**usage** `_object_`

本次语音合成计费信息。

**属性**

**characters** `_integer_`

Qwen3-TTS Realtime计费字符数。

**total\_tokens** `_integer_`

Qwen-TTS Realtime输入和输出（合成的音频）内容总长度（Token）。

**input\_tokens** `_integer_`

Qwen-TTS Realtime输入内容总长度（Token）。

**output\_tokens** `_integer_`

Qwen-TTS Realtime输出内容总长度（Token）。

**input\_tokens\_details** `_integer_`

Qwen-TTS Realtime输入内容长度（Token）详情。

**input\_tokens\_details.text\_tokens** `_integer_`

Qwen-TTS Realtime输入文本内容总长度（Token）。

**output\_tokens\_details** `_integer_`

Qwen-TTS Realtime输出内容长度（Token）详情。

**output\_tokens\_details.text\_tokens** `_integer_`

Qwen-TTS Realtime输出文本内容总长度（Token）。

**output\_tokens\_details.audio\_tokens** `_integer_`

Qwen-TTS Realtime输出音频内容总长度（Token）。

音频转换为 Token 的规则：每1秒的音频对应 50个 Token 。若音频时长不足1秒，则按 50个 Token 计算。

## **session.finished**

当所有响应生成完成时，服务端会返回此事件。

**event\_id** `_string_`

服务端事件ID。

```
{
  "event_id": "event_2239",
  "type": "session.finished"
}
```

**type** `_string_`

事件类型，固定为`session.finished`。
