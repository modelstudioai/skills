# Qwen-Audio-ASR-Message服务端事件

Qwen-Audio-ASR-Message 服务端事件参考，介绍任务启动、识别结果、任务完成和任务失败的字段及对应请求。

## 事件交互流程

1.  发送 [run-task](https://help.aliyun.com/zh/model-studio/qwen-asr-message-client-events#run-task)，收到 [task-started](https://help.aliyun.com/zh/model-studio/qwen-asr-message-server-events#task-started) 后开始发送音频。
2.  持续发送音频，同时接收 [result-generated](https://help.aliyun.com/zh/model-studio/qwen-asr-message-server-events#result-generated)。
3.  任务运行期间，可通过 [continue-task](https://help.aliyun.com/zh/model-studio/qwen-asr-message-client-events#continue-task) 更新对话上下文；音频仍通过音频通道发送。
4.  音频发送完毕后发送 [finish-task](https://help.aliyun.com/zh/model-studio/qwen-asr-message-client-events#finish-task)，继续接收结果，直到收到 [task-finished](https://help.aliyun.com/zh/model-studio/qwen-asr-message-server-events#task-finished)；任务失败时返回 [task-failed](https://help.aliyun.com/zh/model-studio/qwen-asr-message-server-events#task-failed)。

音频数据不通过 `run-task` 发送：WebSocket 使用二进制帧，AOQ 使用 Audio Track。连接、鉴权和音频传输方式请参见 [WebSocket API](raw/_short/qwen-asr-message-websocket-api-8b78d8662335cafa.md) 或 [AOQ 接入](raw/_short/qwen-asr-message-aoq-access-7699c2c24f2a0149.md)。

## task-started

任务启动成功，是客户端开始发送音频的信号。

**重要****收到 `task-started` 后才能发送音频。** `run-task` 仅用于启动和配置任务，不携带音频数据。

`header`object

`task_id`string

客户端生成的任务 ID（UUID 格式）。

`event`string

事件类型，固定为 `task-started`。

`attributes`object

附加属性（通常为空）。

`payload`object

固定为`{}`。

```
{
  "header": {
    "action": "run-task",
    "task_id": "1a8804af-8782-4710-8771-1b4f885286bc",
    "streaming": "duplex"
  },
  "payload": {
    "input": {},
    "task_group": "audio",
    "task": "asr",
    "function": "recognition",
    "model": "qwen-audio-3.1-asr-flash-message",
    "parameters": {
      "format": "pcm",
      "sample_rate": 16000
    }
  }
}
```
```
{
  "header": {
    "task_id": "1a8804af-8782-4710-8771-1b4f885286bc",
    "task_uuid": "b48b0ed59585410bb582e0cb0b1f2a46",
    "event": "task-started",
    "attributes": {}
  },
  "payload": {}
}
```

## result-generated

返回识别结果，包括句子开始、中间结果、句子最终结果和心跳。中间结果默认关闭，设置 `intermediate_result_enabled=true` 后开启。

**重要****`sentence_end=true` 仅表示当前句子结束，不表示任务结束。** 心跳结果（`heartbeat=true`）可跳过；任务是否结束以 `task-finished` 为准。

`header`object

`task_id`string

客户端生成的任务 ID（UUID 格式）。

`event`string

事件类型，固定为 `result-generated`。

`payload`object

`output`object

`sentence`object

`sentence_id`integer

句子的序号标识。正常识别结果中，`sentence_id` 从 1 开始递增。当 `heartbeat` 为 `true` 时（即心跳包），`sentence_id` 固定为 0。

`begin_time`integer

句子开始时间（ms）。

`end_time`integer

句子结束时间（ms）。

中间结果或心跳中可能为 `null`。

`text`string

识别文本。

**说明**中间文本可能随识别过程更新，应按 `sentence_id` 更新同一句的展示内容，不要直接拼接中间文本。

`sentence_begin`boolean

为 `true` 时表示句子开始，此时 `text` 可能为空。

`sentence_end`boolean

是否句子结束（`true`\=最终结果，`false`\=中间结果）。

`heartbeat`boolean

若为 `true`，可跳过该结果（心跳包）。

`words`array\[object\]

字时间戳信息。

`begin_time`integer

字开始时间（ms）。

`end_time`integer

字结束时间（ms）。

`text`string

识别文本。

`punctuation`string

标点符号。

`usage`object

当前任务截至本事件的累计用量。

**说明**`usage` 表示当前任务的累计用量，**不要将各事件中的 `usage` 相加**。任务完成后，以 `task-finished` 中的最终累计用量为准。

`duration`integer

累计音频时长（秒），为兼容保留。

`input_tokens`integer

累计输入 Token 数。

`output_tokens`integer

累计输出 Token 数。

`total_tokens`integer

累计 Token 总数，为 `input_tokens` 与 `output_tokens` 之和。

#### 句子开始

```
{
  "header": {
    "action": "run-task",
    "task_id": "1a8804af-8782-4710-8771-1b4f885286bc",
    "streaming": "duplex"
  },
  "payload": {
    "input": {},
    "task_group": "audio",
    "task": "asr",
    "function": "recognition",
    "model": "qwen-audio-3.1-asr-flash-message",
    "parameters": {
      "format": "pcm",
      "sample_rate": 16000
    }
  }
}
```
```
{
  "header": {
    "task_id": "1a8804af-8782-4710-8771-1b4f885286bc",
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
        "sentence_end": false,
        "sentence_begin": true,
        "words": []
      }
    }
  }
}
```

#### 中间结果

```
{
  "header": {
    "action": "run-task",
    "task_id": "c16bd888-70e0-42db-9dc3-b96864e9624e",
    "streaming": "duplex"
  },
  "payload": {
    "input": {},
    "task_group": "audio",
    "task": "asr",
    "function": "recognition",
    "model": "qwen-audio-3.1-asr-flash-message",
    "parameters": {
      "format": "pcm",
      "sample_rate": 16000,
      "intermediate_result_enabled": true
    }
  }
}
```
```
{
  "header": {
    "task_id": "c16bd888-70e0-42db-9dc3-b96864e9624e",
    "event": "result-generated",
    "attributes": {}
  },
  "payload": {
    "output": {
      "sentence": {
        "sentence_id": 1,
        "begin_time": 0,
        "end_time": null,
        "text": "七",
        "sentence_end": false,
        "words": [
          {
            "begin_time": 0,
            "end_time": 0,
            "text": "七",
            "punctuation": "",
            "fixed": false
          }
        ]
      }
    }
  }
}
```

#### 句子最终结果

```
{
  "header": {
    "action": "run-task",
    "task_id": "1a8804af-8782-4710-8771-1b4f885286bc",
    "streaming": "duplex"
  },
  "payload": {
    "input": {},
    "task_group": "audio",
    "task": "asr",
    "function": "recognition",
    "model": "qwen-audio-3.1-asr-flash-message",
    "parameters": {
      "format": "pcm",
      "sample_rate": 16000
    }
  }
}
```
```
{
  "header": {
    "task_id": "1a8804af-8782-4710-8771-1b4f885286bc",
    "event": "result-generated",
    "attributes": {}
  },
  "payload": {
    "output": {
      "sentence": {
        "sentence_id": 1,
        "begin_time": 160,
        "end_time": 6390,
        "text": "请把漆园项目的报告发给罗科，下周我们要上线玄枢系统。",
        "sentence_end": true,
        "words": [
          {
            "begin_time": 160,
            "end_time": 600,
            "text": "请把",
            "punctuation": "",
            "fixed": false
          },
          {
            "begin_time": 600,
            "end_time": 840,
            "text": "漆",
            "punctuation": "",
            "fixed": false
          },
          {
            "begin_time": 840,
            "end_time": 1160,
            "text": "园",
            "punctuation": "",
            "fixed": false
          },
          {
            "begin_time": 1160,
            "end_time": 1680,
            "text": "项目的",
            "punctuation": "",
            "fixed": false
          },
          {
            "begin_time": 1680,
            "end_time": 2160,
            "text": "报告",
            "punctuation": "",
            "fixed": false
          },
          {
            "begin_time": 2160,
            "end_time": 2600,
            "text": "发给",
            "punctuation": "",
            "fixed": false
          },
          {
            "begin_time": 2600,
            "end_time": 2840,
            "text": "罗",
            "punctuation": "",
            "fixed": false
          },
          {
            "begin_time": 2840,
            "end_time": 3480,
            "text": "科",
            "punctuation": "，",
            "fixed": false
          },
          {
            "begin_time": 3480,
            "end_time": 4000,
            "text": "下周",
            "punctuation": "",
            "fixed": false
          },
          {
            "begin_time": 4000,
            "end_time": 4520,
            "text": "我们要",
            "punctuation": "",
            "fixed": false
          },
          {
            "begin_time": 4520,
            "end_time": 5160,
            "text": "上线",
            "punctuation": "",
            "fixed": false
          },
          {
            "begin_time": 5160,
            "end_time": 5400,
            "text": "玄",
            "punctuation": "",
            "fixed": false
          },
          {
            "begin_time": 5400,
            "end_time": 5680,
            "text": "枢",
            "punctuation": "",
            "fixed": false
          },
          {
            "begin_time": 5680,
            "end_time": 5900,
            "text": "系",
            "punctuation": "",
            "fixed": false
          },
          {
            "begin_time": 5900,
            "end_time": 6390,
            "text": "统",
            "punctuation": "。",
            "fixed": false
          }
        ],
        "stash": {
          "sentence_id": 2,
          "text": "",
          "begin_time": 6390,
          "current_time": 6390,
          "words": []
        }
      }
    },
    "usage": {
      "duration": 6,
      "input_tokens": 80,
      "output_tokens": 16,
      "total_tokens": 96
    }
  }
}
```

## task-finished

任务处理完成，全部识别结果已返回。客户端可关闭连接，或复用连接开启新任务。

`header`object

`task_id`string

客户端生成的任务 ID（UUID 格式）。

`event`string

事件类型，固定为 `task-finished`。

`attributes`object

附加属性（通常为空）。

`payload`object

包含 `output`（空对象）和 `usage`（本任务最终累计用量）。`usage` 字段定义与 [result-generated](#9cb9c5831c7cs) 一致。

```
{
  "header": {
    "action": "finish-task",
    "task_id": "1a8804af-8782-4710-8771-1b4f885286bc",
    "streaming": "duplex"
  },
  "payload": {
    "input": {}
  }
}
```
```
{
  "header": {
    "task_id": "1a8804af-8782-4710-8771-1b4f885286bc",
    "event": "task-finished",
    "attributes": {}
  },
  "payload": {
    "output": {},
    "usage": {
      "duration": 6,
      "input_tokens": 80,
      "output_tokens": 16,
      "total_tokens": 96
    }
  }
}
```

## task-failed

任务失败。通过 `error_code` 和 `error_message` 获取错误原因。WebSocket 连接在任务失败后会被关闭，无法复用。

`header`object

`task_id`string

客户端生成的任务 ID（UUID 格式）。

`event`string

事件类型，固定为 `task-failed`。

`error_code`string

错误类型描述。

`error_message`string

具体错误原因。

`attributes`object

附加属性（通常为空）。

`payload`object

固定为`{}`。

以下请求使用不支持的音频格式，用于展示 `task-failed`。错误码和错误信息随失败原因而变化。

```
{
  "header": {
    "action": "run-task",
    "task_id": "5927b897-6890-45cd-9b85-bc58bdaaadfb",
    "streaming": "duplex"
  },
  "payload": {
    "input": {},
    "task_group": "audio",
    "task": "asr",
    "function": "recognition",
    "model": "qwen-audio-3.1-asr-flash-message",
    "parameters": {
      "format": "invalid-format",
      "sample_rate": 16000
    }
  }
}
```
```
{
  "header": {
    "task_id": "5927b897-6890-45cd-9b85-bc58bdaaadfb",
    "event": "task-failed",
    "error_code": "UNSUPPORTED_FORMAT",
    "error_message": "UNSUPPORTED_FORMAT"
  },
  "payload": {}
}
```
