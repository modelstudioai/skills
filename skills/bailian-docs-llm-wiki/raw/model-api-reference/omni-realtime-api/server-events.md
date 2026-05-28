# 服务端事件

本文介绍 Qwen-Omni-Realtime API 的服务端事件，包括工具调用（Function Calling）相关事件。

> 相关文档：[实时（Qwen-Omni-Realtime）](https://help.aliyun.com/zh/model-studio/realtime)。

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
    "event_id": "event_RdvlSpbBb2ssyBjYrDHjt",
    "type": "session.created",
    "session": {
        "object": "realtime.session",
        "model": "qwen3-omni-flash-realtime",
        "modalities": [
            "text",
            "audio"
        ],
        "voice": "Cherry",
        "input_audio_format": "pcm",
        "output_audio_format": "pcm",
        "input_audio_transcription": {
            "model": "qwen3-asr-flash-realtime"
        },
        "turn_detection": {
            // 取值为server_vad或semantic_vad（仅qwen3.5-omni-realtime支持）
            "type": "server_vad",
            "threshold": 0.5,
            "prefix_padding_ms": 300,
            "silence_duration_ms": 800,
            "create_response": true,
            "interrupt_response": true
        },
        "enable_search": false,
        "search_options": {},
        "tools": [],
        "temperature": 0.8,
        "id": "sess_Ov7GOXoNXhNjlxXtOGKQS"
    }
}
```

**type** `_string_`

事件类型，固定为`session.created`。

**session** `_object_`

会话的配置信息。

**属性**

**object** `_string_`

固定为`realtime.session`。

**model** `_string_`

使用的模型。

**modalities** `_array_`

模型输出模态设置。

**voice** `_string_`

模型生成音频的音色。

**input\_audio\_format** `_string_`

用户输入音频的格式，当前仅支持设为`pcm`。输入音频要求为16 kHz采样率的PCM音频流。

**output\_audio\_format** `_string_`

模型输出音频的格式，当前仅支持设为`pcm`。输出音频为24 kHz采样率的PCM音频流。当前不支持自定义输出采样率。

**input\_audio\_transcription** `_object_`

语音转录的配置。

**属性**

**model** `_string_`

语音转录模型，固定为`qwen3-asr-flash-realtime`，不支持修改。

**turn\_detection** `_object_`

语音活动检测（VAD）的配置。

**属性**

**type** `_string_`

VAD类型。取值：`server_vad`（默认值）或 `semantic_vad`。详情请参见[客户端事件](https://help.aliyun.com/zh/model-studio/client-events#7c8172272codm)。

**threshold** `_float_`

VAD检测阈值。

**silence\_duration\_ms** `_integer_`

检测语音停止的静音持续时间。

**enable\_search** `_boolean_`

是否启用联网搜索功能。仅 Qwen3.5-Omni-Realtime 模型支持。

**search\_options** `_object_`

联网搜索选项配置。

**temperature** `_float_`

模型的温度参数。

## **session.updated**

收到用户的 `session.update` 请求后，若处理成功，则返回此事件；若出错，则返回 `error` 事件。

**event\_id** `_string_`

本次事件唯一标识符。

```
{
    "event_id": "event_X1HsXS4b4uptp6yo1LgKd",
    "type": "session.updated",
    "session": {
        "id": "sess_Aih6vAcY5Ddt6jwFx1tCa",
        "object": "realtime.session",
        "model": "qwen3-omni-flash-realtime",
        "modalities": [
            "text",
            "audio"
        ],
        "instructions": "你是个人助理小云，请你准确且友好地解答用户的问题，始终以乐于助人的态度回应。",
        "voice": "Cherry",
        "input_audio_format": "pcm",
        "output_audio_format": "pcm",
        "input_audio_transcription": {
            "model": "qwen3-asr-flash-realtime"
        },
        "turn_detection": {
            // 取值为server_vad或semantic_vad（仅qwen3.5-omni-realtime支持）
            "type": "server_vad",
            "threshold": 0.1,
            "prefix_padding_ms": 500,
            "silence_duration_ms": 900,
            "create_response": true,
            "interrupt_response": true
        },
        "enable_search": true,
        "search_options": {
            "enable_source": true
        },
        "tools": [
            {
                "type": "function",
                "function": {
                    "name": "get_current_weather",
                    "description": "当你想查询指定城市的天气时非常有用。",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {"type": "string", "description": "城市名称"}
                        },
                        "required": ["location"]
                    }
                }
            }
        ],
        "temperature": 0.8,
        "max_response_output_token": "inf",
        "max_tokens": 16384,
        "repetition_penalty": 1.05,
        "presence_penalty": 0.0,
        "top_k": 50,
        "top_p": 1.0,
        "seed":-1
    }
}
```

**type** `_string_`

事件类型，固定为`session.updated`。

**session** `_object_`

会话的配置信息。

**属性**

**temperature** `_float_`

模型的温度参数。

**modalities** `_array_`

模型输出模态设置。

**voice** `_string_`

模型生成音频的音色。

**instructions** `_string_`

模型的目标与角色。

**input\_audio\_format** `_string_`

用户输入音频的格式，当前仅支持设为`pcm`。输入音频要求为16 kHz采样率的PCM音频流。

**output\_audio\_format** `_string_`

模型输出音频的格式，当前仅支持设为`pcm`。输出音频为24 kHz采样率的PCM音频流。当前不支持自定义输出采样率。

**input\_audio\_transcription** `_object_`

语音转录的配置。

**属性**

**model** `_string_`

语音转录模型，固定为`qwen3-asr-flash-realtime`，不支持修改。

**turn\_detection** `_object_`

语音活动检测（VAD）的配置。

**属性**

**type** `_string_`

VAD类型。取值：`server_vad`（默认值）或 `semantic_vad`。详情请参见[客户端事件](https://help.aliyun.com/zh/model-studio/client-events#7c8172272codm)。

**threshold** `_float_`

VAD检测阈值。

**silence\_duration\_ms** `_integer_`

检测语音停止的静音持续时间。

**enable\_search** `_boolean_`（可选）

是否启用联网搜索功能。仅 Qwen3.5-Omni-Realtime 模型支持。

**search\_options** `_object_`（可选）

联网搜索选项配置。

**tools** `_array_`（可选）

工具定义列表。配置后模型可根据用户输入自主决定是否调用工具。

**属性**

**type** `_string_`（必选）

固定为 `function`。

**function.name** `_string_`（必选）

自定义的工具函数名称，建议使用与函数相同的名称，如`get_current_weather`或`get_current_time`。

**function.description** `_string_`（可选）

对工具函数功能的描述，大模型会参考该字段来选择是否使用该工具函数。

**function.parameters** `_object_`（可选）

对工具函数入参的描述，大模型会参考该字段来进行入参的提取。如果工具函数不需要输入参数，则无需指定。

**属性**

**type** `_string_`（必选）

固定为 `object`。

**properties** `_object_`（可选）

描述各入参的名称、数据类型与描述。Key 值为入参的名称，Value 值为包含数据类型（`type`）与描述（`description`）的对象。

**required** `_array_`（可选）

指定哪些入参为必填项。

**top\_p**`_float_`

核采样的概率阈值。

**top\_k** `_integer_`

模型生成过程中，采样候选集的大小。

**max\_tokens** `_integer_`

模型在本次请求返回的最大 Token 数。

**repetition\_penalty** `_float_`

控制模型生成时，连续序列中的重复度_。_

**presence\_penalty** `_float_`

控制模型在生成内容时的重复度。

**seed** `_integer_`

模型在每次请求时，运行结果一致性程度。

## **input\_audio\_buffer.speech\_started**

在 VAD 模式下，当服务端在音频缓冲区中检测到语音开始时，会返回此事件。

> 若服务端尚未检测到语音，则每次向缓冲区添加音频时都可能触发此事件。

**event\_id** `_string_`

本次事件唯一标识符。

```
{
    "event_id": "event_Pvp8nEhsQuGCQbFJ9x58n",
    "type": "input_audio_buffer.speech_started",
    "audio_start_ms": 3647,
    "item_id": "item_YbAiGvK2H7YaS34o4R6Ba"
}
```

**type** `_string_`

事件类型，固定为`input_audio_buffer.speech_started`。

**audio\_start\_ms** `_integer_`

从音频开始写入缓冲区到首次检测到语音所经过的毫秒数。

**item\_id** `_string_`

语音停止时将创建的用户消息项的 ID。

> 用户消息项用于将用户输入追加到对话历史，供模型后续推理与生成使用。

## **input\_audio\_buffer.speech\_stopped**

在 VAD 模式下，当音频缓冲区中检测到语音结束时，服务端会返回此事件。

同时，服务端还会返回一个 `conversation.item.created` 事件，以创建对应的用户消息项。

**event\_id** `_string_`

本次事件唯一标识符。

```
{
    "event_id": "event_UhQiqNVRsgUiq4KUS5Xb5",
    "type": "input_audio_buffer.speech_stopped",
    "audio_end_ms": 4453,
    "item_id": "item_YbAiGvK2H7YaS34o4R6Ba"
}
```

**type** `_string_`

事件类型，固定为`input_audio_buffer.speech_stopped`。

**audio\_end\_ms** `_integer_`

语音停止时刻距会话开始经过的毫秒数。

**item\_id** `_string_`

将创建的用户消息项的 ID。

## **input\_audio\_buffer.committed**

当输入音频缓冲区被提交时返回此事件。

-   在VAD模式下，当检测到用户说话结束时，服务端会自动提交音频缓冲区并返回此事件。
    
-   在 Manual 模式下，当客户端发送`input_audio_buffer.commit`事件后，服务端返回此事件。
    

**event\_id** `_string_`

本次事件唯一标识符。

```
{
    "event_id": "event_Iy6sUzL1nmdFgshFYxJEz",
    "type": "input_audio_buffer.committed",
    "item_id": "item_YbAiGvK2H7YaS34o4R6Ba"
}
```

**type** `_string_`

事件类型，固定为`input_audio_buffer.committed`。

**item\_id** `_string_`

将创建的用户消息项的 ID。

## **input\_audio\_buffer.cleared**

客户端发送`input_audio_buffer.clear`事件后，服务端将返回此事件。

**event\_id** `_string_`

本次事件唯一标识符。

```
{
  "event_id": "event_RoUu4T8yExPMI37GKwaOC",
  "type": "input_audio_buffer.cleared"
}
```

**type** `_string_`

事件类型，固定为`input_audio_buffer.cleared`。

## **conversation.item.created**

当对话项创建时返回此事件。

**event\_id** `_string_`

本次事件唯一标识符。

```
{
    "event_id": "event_JEfkrr9gO3Ny7Xcv9bGVd",
    "type": "conversation.item.created",
    "item": {
        "id": "item_YbAiGvK2H7YaS34o4R6Ba",
        "object": "realtime.item",
        "type": "message",
        "status": "in_progress",
        "role": "assistant",
        "content": [
            {
                "type": "input_audio"
            }
        ]
    }
}
// 工具调用场景
{
    "event_id": "event_S1hkaIQgcuQD8OEdOpGHQ",
    "type": "conversation.item.created",
    "item": {
        "id": "item_FEG9qJGNkPcdf4et3p7BV",
        "object": "realtime.item",
        "type": "function_call",
        "status": "in_progress",
        "call_id": "call_bc0a7fb7235840f69ecfe4",
        "name": "get_current_weather",
        "arguments": ""
    }
}
```

**type** `_string_`

事件类型，固定为`conversation.item.created`。

**item** `_object_`

要添加到对话中的项。

**属性**

**id** `_string_`

对话项的唯一ID。

**object** `_string_`

始终为 `realtime.item` 。

**status** `_string_`

对话项的状态。

**role** `_string_`

消息的角色。

**content** `_string_`

消息的内容。当 type 为 `message` 时存在。

**type** `_string_`

对话项的类型。可选值为 `message`（常规消息）或 `function_call`（工具调用）。

**name** `_string_`

当 type 为 `function_call` 时，被调用的函数名称。

**call\_id** `_string_`

当 type 为 `function_call` 时，本次函数调用的唯一 ID。

**arguments** `_string_`

当 type 为 `function_call` 时，函数调用的参数（JSON 字符串）。

## **conversation.item.input\_audio\_transcription.delta**

开启输入音频转录后，此事件会在用户说话过程中高频发送，用于展示实时识别的中间结果。您可以通过拼接 `text` + `stash` 获取当前最完整的句子预览。

**event\_id** `_string_`

本次事件唯一标识符。

```
{
    "event_id": "event_C7jzoeSFuiwOZS6tR14yx",
    "type": "conversation.item.input_audio_transcription.delta",
    "item_id": "item_ThVYhLHOdeXb4bBSvzSFF",
    "content_index": 0,
    "text": "",
    "stash": "今天天气怎么样？",
    "language": "zh",
    "emotion": "neutral",
    "obfuscation": "ABEXGYmxdmc97u"
}
```

在任何时刻，要获取当前最完整的句子预览，都需要将这两个字段拼接起来：实时预览句子 = `text` + `stash`。

**点击查看示例**

假设用户正在说："今天天气不错，阳光明媚。"

以下是您可能会收到的事件流以及如何解读它们：

**时间点**

**用户说话进度**

**API 响应 (text 和 stash)**

**客户端 UI 应显示 (text + stash)**

T1

"今天……"

text: ""

stash: "今天"

今天

T2

"……天气……"

text: ""

stash: "今天天气"

今天天气

T3

"……不错"

text: "今天"

stash: "天气不错"

今天天气不错

（注意，"今天"已被确认并移入text）

T4

（短暂停顿）

text: "今天天气不错，"

stash: ""

今天天气不错，

（前半句完全确认）

T5

"……阳光……"

text: "今天天气不错，"

stash: "阳光"

今天天气不错，阳光

T6

"……明媚。"

text: "今天天气不错，"

stash: "阳光明媚。"

今天天气不错，阳光明媚。

T7

（结束说话）

\-

使用 conversation.item.input\_audio\_transcription.completed 的 transcript 内容作为最终结果。

**type** `_string_`

事件类型，固定为`conversation.item.input_audio_transcription.delta`。

**item\_id** `_string_`

关联的对话项 ID。

**content\_index** `_integer_`

包含音频的内容部分的索引。

**text** `_string_`

已确认的文本前缀。这是当前句子中，模型已确认不会再变更的部分。

**stash** `_string_`

预识别的文本后缀。这是紧跟在已确认部分之后，模型仍在处理、可能会被修正的临时草稿。

**language** `_string_`

被识别音频的语种。

**emotion** `_string_`

被识别音频的情感。可选值：`neutral`（平静）、`happy`（愉快）、`sad`（悲伤）、`angry`（愤怒）、`surprised`（惊讶）、`disgusted`（厌恶）、`fearful`（恐惧）。

## **conversation.item.input\_audio\_transcription.completed**

此事件表示用户音频写入缓冲区后生成的转录结果。其转录由内置的语音识别模型（固定为 `qwen3-asr-flash-realtime`）处理，不支持修改。

> 语音识别模型生成的转录文本可能与 Qwen-Omni-Realtime 模型的理解存在差异，仅供参考。

**event\_id** `_string_`

本次事件唯一标识符。

```
{
    "event_id": "event_FrrZcxiDfTB9LD9p4pVng",
    "type": "conversation.item.input_audio_transcription.completed",
    "item_id": "item_YbAiGvK2H7YaS34o4R6Ba",
    "content_index": 0,
    "transcript": "喂，你好。"
}
```

**type** `_string_`

事件类型，固定为`conversation.item.input_audio_transcription.completed`。

**item\_id** `_string_`

用户消息项的 ID。

**content\_index** _integer_

当前固定为0。

**transcript** `_string_`

转录的文本内容。

## **conversation.item.input\_audio\_transcription.failed**

启用输入音频转录后，若用户音频转录失败，服务端会返回此事件。此事件独立于 `error` 事件，便于客户端识别。

**event\_id** `_string_`

本次事件唯一标识符。

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

**type** `_string_`

事件类型，固定为`conversation.item.input_audio_transcription.failed`。

**item\_id** `_string_`

用户消息项的 ID。

**content\_index** `_integer_`

当前固定为0。

**error** `_object_`

错误信息。

**属性**

**code** `_string_`

错误码。

**message** `_string_`

错误消息。

**param** `_string_`

错误相关的参数。

## **response.created**

当服务端生成新的模型响应时，会返回此事件。

**event\_id** `_string_`

本次事件唯一标识符。

```
{
    "event_id": "event_XuDavMzQN3KKepqGu3KRh",
    "type": "response.created",
    "response": {
        "id": "resp_HaVOPdbmX6vifiV5pAfJY",
        "object": "realtime.response",
        "conversation_id": "conv_FjJaccpnvwHNo9cPVuzGc",
        "status": "in_progress",
        "modalities": [
            "text",
            "audio"
        ],
        "voice": "Cherry",
        "output_audio_format": "pcm",
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

响应的唯一 ID。

**conversation\_id** `_string_`

当前会话的唯一ID。

**object** `_string_`

对象类型，此事件下固定为`realtime.response`。

**status** `_string_`

响应的状态。在`[completed, failed, in_progress, or incomplete]`范围内。

**modalities** `_array_`

响应的模态。

**voice** `_string_`

模型生成音频的音色。

**output** `_string_`

此事件下目前为空。

## **response.done**

响应生成完成后，服务端会返回此事件。事件中的 `response` 对象包含除原始音频数据外的全部输出项。

**event\_id** `_string_`

本次事件唯一标识符。

```
{
    "event_id": "event_CSaxRRYLvbrfexDXAEuDG",
    "type": "response.done",
    "response": {
        "id": "resp_HaVOPdbmX6vifiV5pAfJY",
        "object": "realtime.response",
        "conversation_id": "conv_FjJaccpnvwHNo9cPVuzGc",
        "status": "completed",
        "modalities": [
            "text",
            "audio"
        ],
        "voice": "Cherry",
        "output_audio_format": "pcm",
        "output": [
            {
                "id": "item_Ls6MtCUWO7LM4E59QziNv",
                "object": "realtime.item",
                "type": "message",
                "status": "completed",
                "role": "assistant",
                "content": [
                    {
                        "type": "audio",
                        "transcript": "你好呀！有什么我可以帮你的吗？"
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
            },
            "plugins": {
                "search": {
                    "count": 1,
                    "strategy": "agent"
                }
            }
        }
    }
}
// 工具调用场景
{
    "event_id": "event_T1EFAJp43X2DWtDRmxTtx",
    "type": "response.done",
    "response": {
        "id": "resp_TucN5QgymL5MA8vkJvFlS",
        "object": "realtime.response",
        "conversation_id": "conv_SEDZESRlefT8WvLSmEn6E",
        "status": "completed",
        "modalities": ["text", "audio"],
        "voice": "Ethan",
        "output_audio_format": "pcm",
        "output": [
            {
                "id": "item_FEG9qJGNkPcdf4et3p7BV",
                "object": "realtime.item",
                "type": "function_call",
                "status": "completed",
                "call_id": "call_bc0a7fb7235840f69ecfe4",
                "name": "get_current_weather",
                "arguments": " {\"location\": \"杭州\"}"
            }
        ],
        "usage": {
            "total_tokens": 567,
            "input_tokens": 524,
            "output_tokens": 43,
            "input_tokens_details": {
                "text_tokens": 487,
                "audio_tokens": 37
            },
            "output_tokens_details": {
                "text_tokens": 43
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

响应的唯一 ID。

**conversation\_id** `_string_`

当前会话的唯一ID。

**object** `_string_`

对象类型，此事件下固定为`realtime.response`。

**status** `_string_`

响应的状态。

**modalities** `_array_`

响应的模态。

**voice** `_string_`

模型生成音频的音色。

**output** `_object_`

响应的输出。

**属性**

**id** `_string_`

响应输出对应的ID。

**type** `_string_`

输出项的类型，可选值为 `message`（常规消息）或 `function_call`（工具调用）。

**object** `_string_`

输出项的对象类型，当前固定为`realtime.item`。

**status** `_string_`

输出项的状态。

**role** `_string_`

输出项的角色。

**content** `_array_`

输出项的内容。当 type 为 `message` 时存在。

**属性**

**type** `_string_`

输出内容的类型。输出为纯文本时，为`text`；输出包含音频时，为`audio`。

**text** `_string_`

输出的文本内容。

**transcript** `_string_`

音频转录为文字后的内容。

**name** `_string_`

当 type 为 `function_call` 时，被调用的函数名称。

**call\_id** `_string_`

当 type 为 `function_call` 时，函数调用的唯一 ID。

**arguments** `_string_`

当 type 为 `function_call` 时，函数调用的完整参数（JSON 字符串）。

**usage** `_object_`

本次响应的 Token 消耗信息。

**属性**

**total\_tokens** `_integer_`

本次响应消耗的总 Token 数。

**input\_tokens** `_integer_`

输入 Token 数。

**output\_tokens** `_integer_`

输出 Token 数。

**input\_tokens\_details** `_object_`

输入 Token 的分项详情，包含 `text_tokens`（文本 Token 数）和 `audio_tokens`（音频 Token 数）。

**output\_tokens\_details** `_object_`

输出 Token 的分项详情，包含 `text_tokens`（文本 Token 数）和 `audio_tokens`（音频 Token 数）。

**plugins** `_object_`（可选）

插件使用计量信息。启用联网搜索（`enable_search`）时返回。

**属性**

**search** `_object_`

联网搜索计量信息。

**属性**

**count** `_integer_`

搜索次数。

**strategy** `_string_`

搜索策略。

## **response.text.delta**

当输出模态仅包含文本，且模型增量生成新的文本时，服务端将返回此事件。

**event\_id** `_string_`

本次事件唯一标识符。

```
{
    "delta": "喂",
    "event_id": "event_TH49MauuPmRo1RGaMSlP7",
    "type": "response.text.delta",
    "response_id": "resp_PrRSvPVpnCExdUOGHHLuP",
    "item_id": "item_L8IRm9kRXFpxoOjDqDC96",
    "output_index": 0,
    "content_index": 0
}
```

**type** `_string_`

事件类型，固定为`response.text.delta`。

**delta** `_string_`

返回的增量文本。

**response\_id** `_string_`

回复的ID。

**item\_id** `_string_`

消息项ID，可以关联同一个消息项。

**output\_index** `_integer_`

响应中输出项的索引, 目前固定为 0。

**content\_index** `_integer_`

响应中输出项中内部部分的索引, 目前固定为 0。

## **response.text.done**

当输出模态仅包含文本，且模型生成的文本结束时，服务端将返回此事件。

> 当响应中断、不完整或取消时，也会返回此事件。

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

响应的ID。

**item\_id** `_string_`

消息项ID。

**output\_index**`_integer_`

响应输出项的索引。

**content\_index**`_integer_`

响应输出项的索引。

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
  "delta": "{base64 audio}"
}
```

**type** `_string_`

事件类型，固定为`response.audio.delta`。

**response\_id** `_string_`

响应的ID。

**item\_id** `_string_`

消息项ID。

**output\_index**`_integer_`

响应输出项的索引。

**content\_index**`_integer_`

响应输出项的索引。

**delta** `_string_`

模型增量输出的音频数据，使用Base64编码。

## **response.audio.done**

当输出模态包含音频，且模型完成生成音频数据时，服务端将返回此事件。

> 当响应中断、不完整或取消时，也会返回此事件。

**event\_id** `_string_`

本次事件唯一标识符。

```
{
    "event_id": "event_Le1TDl7VfyHQxl47DtGxI",
    "type": "response.audio.done",
    "response_id": "resp_HaVOPdbmX6vifiV5pAfJY",
    "item_id": "item_Ls6MtCUWO7LM4E59QziNv",
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

**output\_index**`_integer_`

响应输出项的索引。

**content\_index**`_integer_`

响应输出项的索引。

## **response.audio\_transcript.delta**

当输出模态包含音频，且模型增量生成新的音频对应的文本时，服务端将返回 `response.audio_transcript.delta` 事件。

**event\_id** `_string_`

本次事件唯一标识符。

```
{
    "event_id": "event_BksW7fOwnyavZdDxIzZYM",
    "type": "response.audio_transcript.delta",
    "response_id": "resp_HaVOPdbmX6vifiV5pAfJY",
    "item_id": "item_Ls6MtCUWO7LM4E59QziNv",
    "output_index": 0,
    "content_index": 0,
    "delta": "有什么"
}
```

**type** `_string_`

事件类型，固定为`response.audio_transcript.delta`。

**response\_id** `_string_`

响应的ID。

**item\_id** `_string_`

消息项ID。

**output\_index**`_integer_`

响应输出项的索引。

**content\_index**`_integer_`

响应输出项的索引。

**delta** `_string_`

增量文本。

## **response.audio\_transcript.done**

当输出模态包含音频，且模型完成音频转录后，服务端将返回 `response.audio_transcript.done` 事件。

**event\_id** `_string_`

本次事件唯一标识符。

```
{
    "event_id": "event_X49tL2WerT4WjxcmH16lS",
    "type": "response.audio_transcript.done",
    "response_id": "resp_HaVOPdbmX6vifiV5pAfJY",
    "item_id": "item_Ls6MtCUWO7LM4E59QziNv",
    "output_index": 0,
    "content_index": 0,
    "transcript": "你好呀！有什么我可以帮你的吗？"
}
```

**type** `_string_`

事件类型，固定为`response.audio_transcript.done`。

**response\_id** `_string_`

响应的ID。

**item\_id** `_string_`

消息项ID。

**output\_index**`_integer_`

响应输出项的索引。

**content\_index**`_integer_`

响应输出项的索引。

**transcript** `_string_`

完整文本。

## **response.function\_call\_arguments.delta**

当模型以流式方式生成函数调用的参数字符串时，每产生一段新内容，服务端推送一次本事件。客户端应按接收顺序将各事件中的 `delta` 字段拼接，得到与当前进度一致的参数文本；完整内容以随后的 `response.function_call_arguments.done` 为准。

**event\_id** `_string_`

本次事件唯一标识符。

```
{
    "event_id": "event_SlKoJyEbPEqLq14DSM1u5",
    "type": "response.function_call_arguments.delta",
    "response_id": "resp_JnTOsWXlFhKcFohZbtfz6",
    "item_id": "item_Rhcms7CauTNsQprV5S4Hr",
    "output_index": 0,
    "call_id": "call_2be200f4cafe419b9530dd",
    "delta": " {\"location\": \"北京\"}"
}
```

**type** `_string_`

事件类型，固定为`response.function_call_arguments.delta`。

**response\_id** `_string_`

响应的ID。

**item\_id** `_string_`

消息项ID。

**output\_index**`_integer_`

该响应中输出项的索引。

**call\_id** `_string_`

本次函数调用的唯一 ID，与同一轮中的 `done` 事件保持一致。

**delta** `_string_`

本段新增的参数字符串片段（增量）。需按顺序拼接。

## **response.function\_call\_arguments.done**

函数调用参数已全部生成完毕。本事件中的 `arguments` 为完整的参数字符串。客户端可在收到本事件后解析参数并调用本地工具函数；应以本事件中的完整 `arguments` 为准，而非 `delta` 拼接结果。

**event\_id** `_string_`

本次事件唯一标识符。

```
{
    "event_id": "event_X6suLyuL5agdH7r6koesM",
    "type": "response.function_call_arguments.done",
    "response_id": "resp_JnTOsWXlFhKcFohZbtfz6",
    "item_id": "item_Rhcms7CauTNsQprV5S4Hr",
    "output_index": 0,
    "name": "get_current_weather",
    "call_id": "call_2be200f4cafe419b9530dd",
    "arguments": " {\"location\": \"北京\"}"
}
```

**type** `_string_`

事件类型，固定为`response.function_call_arguments.done`。

**response\_id** `_string_`

响应的ID。

**item\_id** `_string_`

消息项ID。

**output\_index**`_integer_`

该响应中输出项的索引。

**call\_id** `_string_`

本次函数调用的唯一 ID。

**name** `_string_`

被调用的函数名称。

**arguments** `_string_`

函数调用的完整参数，一般以 JSON 字符串形式表示。

## **response.output\_item.added**

在响应生成过程中创建新项目时，服务端返回此事件。项目类型可以是 `message`（常规消息）或 `function_call`（工具调用）。

**event\_id** `_string_`

本次事件唯一标识符。

```
{
    "event_id": "event_DsCO341DEVtiATtCB6BUY",
    "type": "response.output_item.added",
    "response_id": "resp_HaVOPdbmX6vifiV5pAfJY",
    "output_index": 0,
    "item": {
        "id": "item_Ls6MtCUWO7LM4E59QziNv",
        "object": "realtime.item",
        "type": "message",
        "status": "in_progress",
        "role": "assistant",
        "content": []
    }
}
// 工具调用场景
{
    "event_id": "event_HXmKt5pGoiRtXx7Hq7zpN",
    "type": "response.output_item.added",
    "response_id": "resp_TucN5QgymL5MA8vkJvFlS",
    "output_index": 0,
    "item": {
        "id": "item_FEG9qJGNkPcdf4et3p7BV",
        "object": "realtime.item",
        "type": "function_call",
        "status": "in_progress",
        "call_id": "call_bc0a7fb7235840f69ecfe4",
        "name": "get_current_weather",
        "arguments": ""
    }
}
```

**type** `_string_`

事件类型，固定为`response.output_item.added`。

**response\_id** `_string_`

响应的ID。

**output\_index**`_integer_`

响应输出项的索引。

**item**`_object_`

输出项信息。

**属性**

**id** `_string_`

输出项的唯一ID。

**object** `_string_`

始终为 `realtime.item` 。

**status** `_string_`

输出项的状态。

**role** `_string_`

发送消息的角色。

**content** `_string_`

消息的内容。当 type 为 `message` 时存在。

**type** `_string_`

输出项的类型。可选值为 `message`（常规消息）或 `function_call`（工具调用）。

**name** `_string_`

当 type 为 `function_call` 时，被调用的函数名称。

**call\_id** `_string_`

当 type 为 `function_call` 时，本次函数调用的唯一 ID。

**arguments** `_string_`

当 type 为 `function_call` 时，函数调用的参数（JSON 字符串）。在 added 事件中初始为空字符串。

## **response.output\_item.done**

当新的项目输出完成时，服务端返回此事件。

**event\_id** `_string_`

本次事件唯一标识符。

```
{
    "event_id": "event_MEu5nlLw1LsOguHiehIP8",
    "type": "response.output_item.done",
    "response_id": "resp_HaVOPdbmX6vifiV5pAfJY",
    "output_index": 0,
    "item": {
        "id": "item_Ls6MtCUWO7LM4E59QziNv",
        "object": "realtime.item",
        "type": "message",
        "status": "completed",
        "role": "assistant",
        "content": [
            {
                "type": "audio",
                "text": "你好呀！有什么我可以帮你的吗？"
            }
        ]
    }
}
// 工具调用场景
{
    "event_id": "event_FHspdfAnCyjuME3mmAwSY",
    "type": "response.output_item.done",
    "response_id": "resp_TucN5QgymL5MA8vkJvFlS",
    "output_index": 0,
    "item": {
        "id": "item_FEG9qJGNkPcdf4et3p7BV",
        "object": "realtime.item",
        "type": "function_call",
        "status": "completed",
        "call_id": "call_bc0a7fb7235840f69ecfe4",
        "name": "get_current_weather",
        "arguments": " {\"location\": \"杭州\"}"
    }
}
```

**type** `_string_`

事件类型，固定为`response.output_item.done`。

**response\_id** `_string_`

响应的ID。

**output\_index**`_integer_`

响应输出项的索引。

**item**`_object_`

输出项信息。

**属性**

**id** `_string_`

输出项的唯一ID。

**object** `_string_`

始终为 `realtime.item` 。

**status** `_string_`

输出项的状态。

**role** `_string_`

发送消息的角色。

**content** `_string_`

消息的内容。当 type 为 `message` 时存在。

**type** `_string_`

输出项的类型。可选值为 `message`（常规消息）或 `function_call`（工具调用）。

**name** `_string_`

当 type 为 `function_call` 时，被调用的函数名称。

**call\_id** `_string_`

当 type 为 `function_call` 时，本次函数调用的唯一 ID。

**arguments** `_string_`

当 type 为 `function_call` 时，函数调用的完整参数（JSON 字符串）。

## **response.content\_part.added**

在响应生成过程中，向助手消息项中添加新内容部分时，服务端返回此事件。

**event\_id** `_string_`

本次事件唯一标识符。

```
{
    "event_id": "event_AVBOmrgY3C8bjlRajfSUT",
    "type": "response.content_part.added",
    "response_id": "resp_HaVOPdbmX6vifiV5pAfJY",
    "item_id": "item_Ls6MtCUWO7LM4E59QziNv",
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

**output\_index**`_integer_`

响应输出项的索引，目前固定为 0。

**content\_index**`_integer_`

响应输出项中内部部分的索引, 目前固定为 0。

**part**`_object_`

输出项信息。

**属性**

**type** `_string_`

内容部分的类型。

**text** `_string_`

内容部分的文本。

## **response.content\_part.done**

在助手消息项中的内容部分完成流式传输时，服务端返回此事件。

**event\_id** `_string_`

本次事件唯一标识符。

```
{
    "event_id": "event_Il8HD19v58Qr5IBkw7LtN",
    "type": "response.content_part.done",
    "response_id": "resp_HaVOPdbmX6vifiV5pAfJY",
    "item_id": "item_Ls6MtCUWO7LM4E59QziNv",
    "output_index": 0,
    "content_index": 0,
    "part": {
        "type": "audio",
        "text": "你好呀！有什么我可以帮你的吗？"
    }
}
```

**type** `_string_`

事件类型，固定为`response.content_part.done`。

**response\_id** `_string_`

响应的ID。

**item\_id** `_string_`

消息项ID。

**output\_index**`_integer_`

响应输出项的索引，目前固定为 0。

**content\_index**`_integer_`

该项内容数组中内容部分的索引，目前固定为 0。

**part**`_object_`

输出项信息。

**属性**

**type** `_string_`

内容部分的类型。

**text** `_string_`

内容部分的文本。
