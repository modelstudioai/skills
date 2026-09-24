# 实时语音识别（Qwen-Audio-ASR-Message）服务端事件

本文介绍 Qwen-Audio-3.1-ASR-Flash-Message 实时语音识别服务通过 WebSocket 推送给客户端的服务端事件，包括 task-started、result-generated、task-finished、task-failed 四类事件的数据结构与字段含义。

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

识别结果。默认返回句子最终识别文本（`sentence_end=true`）；设置 `intermediate_result_enabled=true` 后还返回中间文本（`sentence_end=false`）。中间文本可能修订，应按 `sentence_id` 更新展示，不要直接拼接。句子开始事件可包含 `sentence_begin=true`，此时文本可能为空。

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

当前任务截至本事件的累计用量。

属性

**duration**`integer`

累计音频时长（秒），为兼容保留。

**input\_tokens**`integer`

累计输入 Token 数。

**output\_tokens**`integer`

累计输出 Token 数。

**total\_tokens**`integer`

累计 Token 总数，为 `input_tokens` 与 `output_tokens` 之和。

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
        "sentence_id": 1,
        "begin_time": 0,
        "end_time": null,
        "text": "",
        "channel_id": 0,
        "speaker_id": null,
        "sentence_end": false,
        "sentence_begin": true,
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
        "begin_time": 120,
        "end_time": 1700,
        "text": "欢迎使用阿里云。",
        "channel_id": 0,
        "speaker_id": null,
        "sentence_end": true,
        "words": [
          {
            "begin_time": 120,
            "end_time": 520,
            "text": "欢迎",
            "punctuation": "",
            "fixed": false,
            "speaker_id": null
          },
          {
            "begin_time": 520,
            "end_time": 880,
            "text": "使用",
            "punctuation": "",
            "fixed": false,
            "speaker_id": null
          },
          {
            "begin_time": 880,
            "end_time": 1700,
            "text": "阿里云",
            "punctuation": "。",
            "fixed": false,
            "speaker_id": null
          }
        ],
        "stash": {
          "sentence_id": 2,
          "text": "",
          "begin_time": 1700,
          "current_time": 1700,
          "words": []
        }
      }
    },
    "usage": {
      "duration": 2,
      "input_tokens": 84,
      "output_tokens": 4,
      "total_tokens": 88
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

**payload**`object`

包含 `output`（空对象）和 `usage`（本任务最终累计用量）。`usage` 字段定义与 [result-generated](#9cb9c5831c7cs) 一致。

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
      "duration": 2,
      "input_tokens": 84,
      "output_tokens": 4,
      "total_tokens": 88
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
