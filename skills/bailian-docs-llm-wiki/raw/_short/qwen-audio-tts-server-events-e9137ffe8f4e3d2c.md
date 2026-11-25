# Qwen-Audio-TTS服务端事件

Qwen-Audio-TTS 服务端事件参考，介绍任务启动、句子合成、任务完成和任务失败的字段及对应请求。

<a id="事件交互流程"></a>

## 事件交互流程

1.  发送 [run-task](qwen-audio-tts-client-events-26c1ffacfaed1e62.md#run-task) 启动并配置任务，等待 [task-started](qwen-audio-tts-server-events-e9137ffe8f4e3d2c.md#task-started)。
2.  收到 `task-started` 后，通过 [continue-task](qwen-audio-tts-client-events-26c1ffacfaed1e62.md#continue-task) 发送文本，同时接收 [result-generated](qwen-audio-tts-server-events-e9137ffe8f4e3d2c.md#result-generated) 和合成音频。
3.  文本全部发送完毕后，发送 [finish-task](qwen-audio-tts-client-events-26c1ffacfaed1e62.md#finish-task)，继续接收剩余结果和音频，直到收到 [task-finished](qwen-audio-tts-server-events-e9137ffe8f4e3d2c.md#task-finished)；任务失败时返回 [task-failed](qwen-audio-tts-server-events-e9137ffe8f4e3d2c.md#task-failed)。

`result-generated` 返回句子元信息，音频数据通过独立通道传输：WebSocket 使用二进制帧，AOQ 使用 Audio Track。连接、鉴权和音频传输方式请参见 [WebSocket API](qwen-audio-tts-websocket-api-6f9e2d20cf04ea96.md) 或 [AOQ 接入](../model-api-reference/realtime-api-directory/realtime-tts-model-apis/qwen-audio-tts-api/qwen-audio-tts-aoq-access.md)。

<a id="task-started"></a>

<a id="h3e7k9n3q5"></a>

## task-started

任务启动成功，是客户端开始发送待合成文本的信号。

> **重要**
>
> **收到 `task-started` 后才能发送 `continue-task`。** `run-task` 只用于启动和配置任务，待合成文本通过 `continue-task` 发送。

`header`object

`task_id`string

客户端生成的任务 ID。

`event`string

事件类型，固定为 `task-started`。

`payload`object

无内容，为空对象。

<a id="code-block"></a>

```json
{
  "header": {
    "action": "run-task",
    "task_id": "a39861ca-2fd0-4d6e-a75c-79aa66a5c2d6",
    "streaming": "duplex"
  },
  "payload": {
    "input": {},
    "task_group": "audio",
    "task": "tts",
    "function": "SpeechSynthesizer",
    "model": "qwen-audio-3.1-tts-flash",
    "parameters": {
      "text_type": "PlainText",
      "voice": "longanhuan_v3.1",
      "format": "mp3",
      "sample_rate": 22050
    }
  }
}
```

<a id="code-block-2"></a>

```json
{
  "header": {
    "task_id": "a39861ca-2fd0-4d6e-a75c-79aa66a5c2d6",
    "task_uuid": "cc20c8fbbe9a4553be4e2efb2c37a913",
    "event": "task-started",
    "attributes": {}
  },
  "payload": {}
}
```

<a id="result-generated"></a>

<a id="h4r9t7v9x3"></a>

## result-generated

返回句子元信息，包括句子开始、音频数据块标记和句子结束。

> **重要**
>
> **`sentence-end` 只表示当前句子合成结束，不表示整个任务结束。** 任务结束以 `task-finished` 为准。音频通过 WebSocket 二进制帧或 AOQ Audio Track 返回。

`header`object

`task_id`string

客户端生成的任务 ID。

`event`string

事件类型，固定为 `result-generated`。

`payload`object

`output`object

输出信息。

`sentence`object

`index`integer

句子编号，从 0 开始。

`words`array

字级别时间戳信息数组。

`text`string

字的文本内容。

`begin_index`integer

字在句子中的开始位置索引，从 0 开始。

`end_index`integer

字在句子中的结束位置索引，从 1 开始。

`begin_time`integer

字对应音频的开始时间戳，单位：毫秒。

`end_time`integer

字对应音频的结束时间戳，单位：毫秒。

`type`string

子事件类型，取值：

-   `sentence-begin`：句子开始，返回待合成的文本内容
-   `sentence-synthesis`：标识音频数据块，每个事件后立即通过 WebSocket binary 通道传输一个音频数据帧
-   `sentence-end`：句子结束，返回文本内容和用量信息（`usage`）

`original_text`string

分句后的句子文本内容。

`usage`object

<a id="usage-fields"></a>

计费用量，在 `sentence-end` 事件中返回。

> **说明**
>
> -   `usage` 表示当前任务的累计用量，**不要将各事件中的 `usage` 相加**。任务完成后，以 `task-finished` 中的最终累计用量为准。
> -   qwen-audio-3.1-tts-flash：按输入和输出 Token 计费，用量分别对应 `input_tokens` 和 `output_tokens`，合计见 `total_tokens`。
> -   qwen-audio-3.1-tts-plus：按字符计费（`characters`），同时返回上述 Token 统计字段。
> -   qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash：按字符计费（`characters`）。

`input_tokens`integer

本次请求的输入 Token 数。

`output_tokens`integer

本次请求的输出 Token 数。

`total_tokens`integer

输入和输出 Token 数之和。

`characters`integer

累计计费字符数。

以下示例在启动任务时已设置 `word_timestamp_enabled=true`。

<a id="sec-tabs"></a>

<a id="sentence-begin"></a>

<a id="sentence-begin-h4"></a>

#### sentence-begin

<a id="code-block-3"></a>

```json
{
  "header": {
    "action": "continue-task",
    "task_id": "c67b3308-1737-4bfe-8292-6961cfa67bbe",
    "streaming": "duplex"
  },
  "payload": {
    "input": {
      "text": "你好，欢迎使用语音合成。"
    }
  }
}
```

<a id="code-block-4"></a>

```json
{
  "header": {
    "task_id": "c67b3308-1737-4bfe-8292-6961cfa67bbe",
    "event": "result-generated",
    "attributes": {
      "x-dashscope-inner-response-type": "ws"
    }
  },
  "payload": {
    "output": {
      "sentence": {
        "index": 0,
        "words": [
          {
            "text": "你",
            "begin_index": 0,
            "end_index": 1,
            "begin_time": 80,
            "end_time": 240
          },
          {
            "text": "好",
            "begin_index": 1,
            "end_index": 2,
            "begin_time": 240,
            "end_time": 320
          },
          {
            "text": "，",
            "begin_index": 2,
            "end_index": 3,
            "begin_time": 320,
            "end_time": 640
          },
          {
            "text": "欢",
            "begin_index": 3,
            "end_index": 4,
            "begin_time": 720,
            "end_time": 960
          },
          {
            "text": "迎",
            "begin_index": 4,
            "end_index": 5,
            "begin_time": 960,
            "end_time": 1120
          },
          {
            "text": "使",
            "begin_index": 5,
            "end_index": 6,
            "begin_time": 1120,
            "end_time": 1200
          },
          {
            "text": "用",
            "begin_index": 6,
            "end_index": 7,
            "begin_time": 1200,
            "end_time": 1360
          },
          {
            "text": "语",
            "begin_index": 7,
            "end_index": 8,
            "begin_time": 1360,
            "end_time": 1520
          },
          {
            "text": "音",
            "begin_index": 8,
            "end_index": 9,
            "begin_time": 1520,
            "end_time": 1680
          }
        ]
      },
      "type": "sentence-begin",
      "original_text": "你好，欢迎使用语音合成。",
      "normalized_text": "你好，欢迎使用语音合成。"
    }
  }
}
```

<a id="sentence-synthesis"></a>

<a id="sentence-synthesis-h4"></a>

#### sentence-synthesis

<a id="code-block-5"></a>

```json
{
  "header": {
    "action": "continue-task",
    "task_id": "c67b3308-1737-4bfe-8292-6961cfa67bbe",
    "streaming": "duplex"
  },
  "payload": {
    "input": {
      "text": "你好，欢迎使用语音合成。"
    }
  }
}
```

<a id="code-block-6"></a>

```json
{
  "header": {
    "task_id": "c67b3308-1737-4bfe-8292-6961cfa67bbe",
    "event": "result-generated",
    "attributes": {
      "x-dashscope-inner-response-type": "ws"
    }
  },
  "payload": {
    "output": {
      "sentence": {
        "index": 0,
        "words": [
          {
            "text": "你",
            "begin_index": 0,
            "end_index": 1,
            "begin_time": 80,
            "end_time": 240
          },
          {
            "text": "好",
            "begin_index": 1,
            "end_index": 2,
            "begin_time": 240,
            "end_time": 320
          },
          {
            "text": "，",
            "begin_index": 2,
            "end_index": 3,
            "begin_time": 320,
            "end_time": 640
          },
          {
            "text": "欢",
            "begin_index": 3,
            "end_index": 4,
            "begin_time": 720,
            "end_time": 960
          },
          {
            "text": "迎",
            "begin_index": 4,
            "end_index": 5,
            "begin_time": 960,
            "end_time": 1120
          },
          {
            "text": "使",
            "begin_index": 5,
            "end_index": 6,
            "begin_time": 1120,
            "end_time": 1200
          },
          {
            "text": "用",
            "begin_index": 6,
            "end_index": 7,
            "begin_time": 1200,
            "end_time": 1360
          },
          {
            "text": "语",
            "begin_index": 7,
            "end_index": 8,
            "begin_time": 1360,
            "end_time": 1520
          },
          {
            "text": "音",
            "begin_index": 8,
            "end_index": 9,
            "begin_time": 1520,
            "end_time": 1680
          }
        ]
      },
      "type": "sentence-synthesis"
    }
  }
}
```

<a id="sentence-end"></a>

<a id="sentence-end-h4"></a>

#### sentence-end

<a id="code-block-7"></a>

```json
{
  "header": {
    "action": "continue-task",
    "task_id": "c67b3308-1737-4bfe-8292-6961cfa67bbe",
    "streaming": "duplex"
  },
  "payload": {
    "input": {
      "text": "你好，欢迎使用语音合成。"
    }
  }
}
```

<a id="code-block-8"></a>

```json
{
  "header": {
    "task_id": "c67b3308-1737-4bfe-8292-6961cfa67bbe",
    "event": "result-generated",
    "attributes": {
      "x-dashscope-inner-response-type": "ws"
    }
  },
  "payload": {
    "output": {
      "sentence": {
        "index": 0,
        "words": [
          {
            "text": "你",
            "begin_index": 0,
            "end_index": 1,
            "begin_time": 80,
            "end_time": 240
          },
          {
            "text": "好",
            "begin_index": 1,
            "end_index": 2,
            "begin_time": 240,
            "end_time": 320
          },
          {
            "text": "，",
            "begin_index": 2,
            "end_index": 3,
            "begin_time": 320,
            "end_time": 640
          },
          {
            "text": "欢",
            "begin_index": 3,
            "end_index": 4,
            "begin_time": 720,
            "end_time": 960
          },
          {
            "text": "迎",
            "begin_index": 4,
            "end_index": 5,
            "begin_time": 960,
            "end_time": 1120
          },
          {
            "text": "使",
            "begin_index": 5,
            "end_index": 6,
            "begin_time": 1120,
            "end_time": 1200
          },
          {
            "text": "用",
            "begin_index": 6,
            "end_index": 7,
            "begin_time": 1200,
            "end_time": 1360
          },
          {
            "text": "语",
            "begin_index": 7,
            "end_index": 8,
            "begin_time": 1360,
            "end_time": 1520
          },
          {
            "text": "音",
            "begin_index": 8,
            "end_index": 9,
            "begin_time": 1520,
            "end_time": 1680
          },
          {
            "text": "合",
            "begin_index": 9,
            "end_index": 10,
            "begin_time": 1680,
            "end_time": 1920
          },
          {
            "text": "成。",
            "begin_index": 10,
            "end_index": 11,
            "begin_time": 1920,
            "end_time": 2080
          }
        ]
      },
      "type": "sentence-end",
      "original_text": "你好，欢迎使用语音合成。",
      "normalized_text": "你好，欢迎使用语音合成。"
    },
    "usage": {
      "input_tokens": 12,
      "output_tokens": 29,
      "total_tokens": 41,
      "characters": 22
    }
  }
}
```

<a id="task-finished"></a>

<a id="h8d9f5h7j9"></a>

## task-finished

服务端返回 `task-finished` 事件，标志任务已结束。客户端可以关闭 WebSocket 连接或复用连接开启新任务。

`header`object

`task_id`string

客户端生成的任务 ID。

`event`string

事件类型，固定为 `task-finished`。

`payload`object

`usage`object

字段含义与 [`result-generated` 的 usage](#usage-fields) 相同。

<a id="code-block-9"></a>

```json
{
  "header": {
    "action": "finish-task",
    "task_id": "a39861ca-2fd0-4d6e-a75c-79aa66a5c2d6",
    "streaming": "duplex"
  },
  "payload": {
    "input": {}
  }
}
```

<a id="code-block-10"></a>

```json
{
  "header": {
    "task_id": "a39861ca-2fd0-4d6e-a75c-79aa66a5c2d6",
    "event": "task-finished",
    "attributes": {
      "x-dashscope-inner-response-type": "ws"
    }
  },
  "payload": {
    "output": {},
    "usage": {
      "input_tokens": 12,
      "output_tokens": 29,
      "total_tokens": 41,
      "characters": 22
    }
  }
}
```

<a id="task-failed"></a>

<a id="h4h9j5m7p9"></a>

## task-failed

当任务失败时，服务端返回 `task-failed` 事件。客户端需要关闭 WebSocket 连接并处理错误。

`header`object

`task_id`string

客户端生成的任务 ID。

`event`string

事件类型，固定为 `task-failed`。

`error_code`string

错误码。

`error_message`string

具体错误信息。

以下示例使用不支持的音频格式；任务启动后发送文本，服务端随后返回错误。错误码和错误信息随失败原因而变化。

<a id="code-block-11"></a>

```json
{
  "header": {
    "action": "run-task",
    "task_id": "7b091c3c-4b35-4c54-9b22-250749ce1b74",
    "streaming": "duplex"
  },
  "payload": {
    "input": {},
    "task_group": "audio",
    "task": "tts",
    "function": "SpeechSynthesizer",
    "model": "qwen-audio-3.1-tts-flash",
    "parameters": {
      "text_type": "PlainText",
      "voice": "longanhuan_v3.1",
      "format": "invalid-format",
      "sample_rate": 22050
    }
  }
}
```

<a id="code-block-12"></a>

```json
{
  "header": {
    "task_id": "7b091c3c-4b35-4c54-9b22-250749ce1b74",
    "event": "task-failed",
    "error_code": "InvalidParameter",
    "error_message": "Request format is invalid!"
  },
  "payload": {}
}
```
