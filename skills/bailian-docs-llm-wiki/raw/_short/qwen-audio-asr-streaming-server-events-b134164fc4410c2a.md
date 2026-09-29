# 实时语音识别（Qwen-Audio-ASR-Streaming）服务端事件

本文介绍 Qwen-Audio-ASR-Streaming 实时语音识别服务通过 WebSocket 推送给客户端的服务端事件，包括 task-started、result-generated、task-finished、task-failed 四类事件的数据结构与字段含义。

## task-started

任务启动成功，客户端可开始发送音频数据。

**header**`object`

属性

**task\_id**`string`

客户端生成的任务 ID（UUID 格式）。

**event**`string`

事件类型，固定为 `task-started`。

**attributes**`object`

附加属性（通常为空）。

**payload**`object`

固定为`{}`。

```
{
    "header": {
        "task_id": "2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx",
        "event": "task-started",
        "attributes": {}
    },
    "payload": {}
}
```

## result-generated

识别结果，包含中间结果（sentence\_end=false）和最终结果（sentence\_end=true）。其中，新句子的首个中间结果包含 sentence\_begin=true。

**header**`object`

属性

**task\_id**`string`

客户端生成的任务 ID（UUID 格式）。

**event**`string`

事件类型，固定为 `result-generated`。

**payload**`object`

属性

**output**`object`

属性

**sentence**`object`

属性

**begin\_time**`integer`

句子开始时间（ms）。

**end\_time**`integer`

句子结束时间（ms）。

**text**`string`

识别文本。

**heartbeat**`boolean`

若为 true，可跳过该结果（心跳包）。

**sentence\_begin**`boolean`

用于标识句子开始。

**sentence\_end**`boolean`

是否句子结束（true=最终结果，false=中间结果）。

**sentence\_id**`integer`

句子的序号标识。正常识别结果中，sentence\_id 从 1 开始递增。当 heartbeat 为 true 时（即心跳包），sentence\_id 固定为 0。

**words**`array[object]`

字时间戳信息。

属性

**begin\_time**`integer`

字开始时间（ms）。

**end\_time**`integer`

字结束时间（ms）。

**text**`string`

识别文本。

**punctuation**`string`

标点符号。

**usage**`object`

当前任务的累计用量。

属性

**input\_tokens**`integer`

累计输入 Token 数。

**说明**适用于 `qwen-audio-3.1-asr-flash-streaming`。

**output\_tokens**`integer`

累计输出 Token 数。

**说明**适用于 `qwen-audio-3.1-asr-flash-streaming`。

**total\_tokens**`integer`

累计 Token 总数，为输入和输出 Token 数之和。

**说明**适用于 `qwen-audio-3.1-asr-flash-streaming`。

**duration**`integer`

累计音频时长（秒）。

**说明**用于 `qwen-audio-3.0-asr-flash-streaming` 的计费。

**句子开始结果：**
```
{
  "header": {
    "task_id": "2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx",
    "event": "result-generated",
    "attributes": {}
  },
  "payload": {
    "output": {
      "sentence": {
        "begin_time": 0,
        "end_time": null,
        "text": "",
        "sentence_begin": true,
        "sentence_end": false,
        "sentence_id": 1,
        "words": []
      }
    }
  }
}
```
**最终结果：**
```
{
  "header": {
    "task_id": "2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx",
    "event": "result-generated",
    "attributes": {}
  },
  "payload": {
    "output": {
      "sentence": {
        "sentence_id": 1,
        "begin_time": 160,
        "end_time": 1640,
        "text": "欢迎使用阿里云。",
        "channel_id": 0,
        "speaker_id": null,
        "sentence_end": true,
        "words": [
          {
            "begin_time": 160,
            "end_time": 520,
            "text": "欢迎",
            "punctuation": "",
            "fixed": true,
            "speaker_id": null
          },
          {
            "begin_time": 520,
            "end_time": 880,
            "text": "使用",
            "punctuation": "",
            "fixed": true,
            "speaker_id": null
          },
          {
            "begin_time": 880,
            "end_time": 1640,
            "text": "阿里云",
            "punctuation": "。",
            "fixed": true,
            "speaker_id": null
          }
        ],
        "stash": {
          "sentence_id": 2,
          "text": "",
          "begin_time": 1640,
          "current_time": 1640,
          "words": []
        }
      },
      "text": "欢迎使用阿里云。",
      "request_id": "95372ce8e6704bcc8747da94789c15ca",
      "output": {
        "sentence": {
          "sentence_id": 1,
          "begin_time": 160,
          "end_time": 1640,
          "text": "欢迎使用阿里云。",
          "channel_id": 0,
          "speaker_id": null,
          "sentence_end": true,
          "words": [
            {
              "begin_time": 160,
              "end_time": 520,
              "text": "欢迎",
              "punctuation": "",
              "fixed": true,
              "speaker_id": null
            },
            {
              "begin_time": 520,
              "end_time": 880,
              "text": "使用",
              "punctuation": "",
              "fixed": true,
              "speaker_id": null
            },
            {
              "begin_time": 880,
              "end_time": 1640,
              "text": "阿里云",
              "punctuation": "。",
              "fixed": true,
              "speaker_id": null
            }
          ],
          "stash": {
            "sentence_id": 2,
            "text": "",
            "begin_time": 1640,
            "current_time": 1640,
            "words": []
          }
        },
        "text": "欢迎使用阿里云。",
        "request_id": "95372ce8e6704bcc8747da94789c15ca"
      },
      "usage": {
        "duration": 2,
        "input_tokens": 85,
        "output_tokens": 4,
        "total_tokens": 89
      }
    },
    "usage": {
      "duration": 2,
      "input_tokens": 85,
      "output_tokens": 4,
      "total_tokens": 89
    }
  }
}
```

## task-finished

任务正常结束，可关闭连接或复用连接。

**header**`object`

属性

**task\_id**`string`

客户端生成的任务 ID（UUID 格式）。

**event**`string`

事件类型，固定为 `task-finished`。

**attributes**`object`

附加属性（通常为空）。

**payload.usage**`object`

任务结束时的累计用量。字段含义与 [result-generated.usage](#usage-fields)相同。

```
{
  "header": {
    "task_id": "2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx",
    "event": "task-finished",
    "attributes": {}
  },
  "payload": {
    "output": {},
    "usage": {
      "duration": 9,
      "input_tokens": 365,
      "output_tokens": 12,
      "total_tokens": 377
    }
  }
}
```

## task-failed

任务失败，连接会被关闭，无法复用。

**header**`object`

属性

**task\_id**`string`

客户端生成的任务 ID（UUID 格式）。

**event**`string`

事件类型，固定为 `task-failed`。

**error\_code**`string`

错误类型描述。

**error\_message**`string`

具体错误原因。

**attributes**`object`

附加属性（通常为空）。

**payload**`object`

固定为`{}`。

```
{
    "header": {
        "task_id": "2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx",
        "event": "task-failed",
        "error_code": "CLIENT_ERROR",
        "error_message": "request timeout after 23 seconds.",
        "attributes": {}
    },
    "payload": {}
}
```
