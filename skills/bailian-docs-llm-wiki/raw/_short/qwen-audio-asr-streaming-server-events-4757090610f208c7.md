# Qwen-Audio-ASR-Streaming服务端事件

Qwen-Audio-ASR-Streaming 服务端事件参考，介绍任务启动、识别结果、任务完成和任务失败的字段及对应请求。

<a id="事件交互流程"></a>

## 事件交互流程

1.  发送 [run-task](qwen-audio-asr-streaming-client-events-3240c8efa3976e48.md#run-task)，收到 [task-started](qwen-audio-asr-streaming-server-events-4757090610f208c7.md#task-started) 后开始发送音频。
2.  持续发送音频，同时接收 [result-generated](qwen-audio-asr-streaming-server-events-4757090610f208c7.md#result-generated)。
3.  音频发送完毕后发送 [finish-task](qwen-audio-asr-streaming-client-events-3240c8efa3976e48.md#finish-task)，继续接收结果，直到收到 [task-finished](qwen-audio-asr-streaming-server-events-4757090610f208c7.md#task-finished)；任务失败时返回 [task-failed](qwen-audio-asr-streaming-server-events-4757090610f208c7.md#task-failed)。

音频数据不通过 `run-task` 发送：WebSocket 使用二进制帧，AOQ 使用 Audio Track。连接、鉴权和音频传输方式请参见 [WebSocket API](qwen-audio-asr-streaming-websocket-api-779f1056a08e5525.md) 或 [AOQ 接入](qwen-audio-asr-streaming-aoq-access-7b2cf295190f6172.md)。

<a id="task-started"></a>

<a id="eac316aeacafj"></a>

## task-started

任务启动成功，是客户端开始发送音频的信号。

> **重要**
>
> **收到 `task-started` 后才能发送音频。** `run-task` 仅用于启动和配置任务，不携带音频数据。

`header`object

`task_id`string

客户端生成的任务 ID（UUID 格式）。

`event`string

事件类型，固定为 `task-started`。

`attributes`object

附加属性（通常为空）。

`payload`object

固定为`{}`。

<a id="code-block"></a>

```json
{
  "header": {
    "action": "run-task",
    "task_id": "3756efcf-8388-41c8-832a-9a70bf046f55",
    "streaming": "duplex"
  },
  "payload": {
    "task_group": "audio",
    "task": "asr",
    "function": "recognition",
    "model": "qwen-audio-3.1-asr-flash-streaming",
    "parameters": {
      "format": "pcm",
      "sample_rate": 16000
    },
    "input": {}
  }
}
```

<a id="code-block-2"></a>

```json
{
  "header": {
    "task_id": "3756efcf-8388-41c8-832a-9a70bf046f55",
    "task_uuid": "69dc7ec7af9a40118edc548ac3f3d2b4",
    "event": "task-started",
    "attributes": {}
  },
  "payload": {}
}
```

<a id="result-generated"></a>

<a id="9cb9c5831c7cs"></a>

## result-generated

返回识别结果，包括句子开始、中间结果、句子最终结果和心跳。

> **重要**
>
> **`sentence_end=true` 仅表示当前句子结束，不表示任务结束。** 心跳结果（`heartbeat=true`）可跳过；任务是否结束以 `task-finished` 为准。

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

`end_time`integer | null

句子结束时间（ms）。 中间结果或心跳中可能为 `null`。

`text`string

识别文本。

`sentence_begin`boolean

用于标识句子开始。

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

<a id="usage-fields"></a>

当前任务的累计用量。

> **说明**
>
> `usage` 为当前任务的累计用量，部分中间结果可能不包含该字段。**不要将各事件中的 `usage` 相加。** qwen-audio-3.0-asr-flash-streaming 按时长计费，qwen-audio-3.1-asr-flash-streaming 按 Token 计费；字段适用范围见下文。

`duration`integer

累计音频时长（秒）。

> **说明**
>
> 用于 qwen-audio-3.0-asr-flash-streaming 的计费。

`input_tokens`integer

累计输入 Token 数。

> **说明**
>
> 适用于 qwen-audio-3.1-asr-flash-streaming。

`output_tokens`integer

累计输出 Token 数。

> **说明**
>
> 适用于 qwen-audio-3.1-asr-flash-streaming。

`total_tokens`integer

累计 Token 总数，为输入和输出 Token 数之和。

> **说明**
>
> 适用于 qwen-audio-3.1-asr-flash-streaming。

<a id="sec-tabs"></a>

<a id="句子开始"></a>

<a id="句子开始-h4"></a>

#### 句子开始

收到 `task-started` 后，发送音频。以下示例为服务端随后返回的一条 `result-generated` 事件；音频通过二进制帧（WebSocket）或 Audio Track（AOQ）发送。

<a id="code-block-3"></a>

```json
{
  "header": {
    "action": "run-task",
    "task_id": "3756efcf-8388-41c8-832a-9a70bf046f55",
    "streaming": "duplex"
  },
  "payload": {
    "task_group": "audio",
    "task": "asr",
    "function": "recognition",
    "model": "qwen-audio-3.1-asr-flash-streaming",
    "parameters": {
      "format": "pcm",
      "sample_rate": 16000
    },
    "input": {}
  }
}
```

<a id="code-block-4"></a>

```json
{
  "header": {
    "task_id": "3756efcf-8388-41c8-832a-9a70bf046f55",
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
        "sentence_end": false,
        "sentence_begin": true,
        "words": []
      },
      "text": "",
      "request_id": "3756efcf-8388-41c8-832a-9a70bf046f55",
      "output": {
        "sentence": {
          "sentence_id": 1,
          "begin_time": 0,
          "end_time": null,
          "text": "",
          "channel_id": 0,
          "sentence_end": false,
          "sentence_begin": true,
          "words": []
        },
        "text": "",
        "request_id": "3756efcf-8388-41c8-832a-9a70bf046f55"
      }
    }
  }
}
```

<a id="中间结果"></a>

<a id="中间结果-h4"></a>

#### 中间结果

收到 `task-started` 后，发送音频。以下示例为服务端随后返回的一条 `result-generated` 事件；音频通过二进制帧（WebSocket）或 Audio Track（AOQ）发送。

<a id="code-block-5"></a>

```json
{
  "header": {
    "action": "run-task",
    "task_id": "3756efcf-8388-41c8-832a-9a70bf046f55",
    "streaming": "duplex"
  },
  "payload": {
    "task_group": "audio",
    "task": "asr",
    "function": "recognition",
    "model": "qwen-audio-3.1-asr-flash-streaming",
    "parameters": {
      "format": "pcm",
      "sample_rate": 16000
    },
    "input": {}
  }
}
```

<a id="code-block-6"></a>

```json
{
  "header": {
    "task_id": "3756efcf-8388-41c8-832a-9a70bf046f55",
    "event": "result-generated",
    "attributes": {}
  },
  "payload": {
    "output": {
      "sentence": {
        "sentence_id": 1,
        "begin_time": 0,
        "end_time": null,
        "text": "情感",
        "channel_id": 0,
        "sentence_end": false,
        "words": [
          {
            "begin_time": 0,
            "end_time": 320,
            "text": "情感",
            "punctuation": "",
            "fixed": false,
            "speaker_id": null
          }
        ]
      },
      "text": "情感",
      "request_id": "3756efcf-8388-41c8-832a-9a70bf046f55",
      "output": {
        "sentence": {
          "sentence_id": 1,
          "begin_time": 0,
          "end_time": null,
          "text": "情感",
          "channel_id": 0,
          "sentence_end": false,
          "words": [
            {
              "begin_time": 0,
              "end_time": 320,
              "text": "情感",
              "punctuation": "",
              "fixed": false,
              "speaker_id": null
            }
          ]
        },
        "text": "情感",
        "request_id": "3756efcf-8388-41c8-832a-9a70bf046f55"
      }
    }
  }
}
```

<a id="句子最终结果"></a>

<a id="句子最终结果-h4"></a>

#### 句子最终结果

收到 `task-started` 后，发送音频。以下示例为服务端随后返回的一条 `result-generated` 事件；音频通过二进制帧（WebSocket）或 Audio Track（AOQ）发送。

<a id="code-block-7"></a>

```json
{
  "header": {
    "action": "run-task",
    "task_id": "3756efcf-8388-41c8-832a-9a70bf046f55",
    "streaming": "duplex"
  },
  "payload": {
    "task_group": "audio",
    "task": "asr",
    "function": "recognition",
    "model": "qwen-audio-3.1-asr-flash-streaming",
    "parameters": {
      "format": "pcm",
      "sample_rate": 16000
    },
    "input": {}
  }
}
```

<a id="code-block-8"></a>

```json
{
  "header": {
    "task_id": "3756efcf-8388-41c8-832a-9a70bf046f55",
    "event": "result-generated",
    "attributes": {}
  },
  "payload": {
    "output": {
      "sentence": {
        "sentence_id": 1,
        "begin_time": 160,
        "end_time": 6360,
        "text": "请把漆原项目的报告发给罗科，下周我们要上线悬枢系统。",
        "channel_id": 0,
        "sentence_end": true,
        "words": [
          {
            "begin_time": 160,
            "end_time": 600,
            "text": "请把",
            "punctuation": "",
            "fixed": true,
            "speaker_id": null
          },
          {
            "begin_time": 600,
            "end_time": 840,
            "text": "漆",
            "punctuation": "",
            "fixed": true,
            "speaker_id": null
          },
          {
            "begin_time": 840,
            "end_time": 1160,
            "text": "原",
            "punctuation": "",
            "fixed": true,
            "speaker_id": null
          },
          {
            "begin_time": 1160,
            "end_time": 1680,
            "text": "项目的",
            "punctuation": "",
            "fixed": true,
            "speaker_id": null
          },
          {
            "begin_time": 1680,
            "end_time": 2160,
            "text": "报告",
            "punctuation": "",
            "fixed": true,
            "speaker_id": null
          },
          {
            "begin_time": 2160,
            "end_time": 2600,
            "text": "发给",
            "punctuation": "",
            "fixed": true,
            "speaker_id": null
          },
          {
            "begin_time": 2600,
            "end_time": 2840,
            "text": "罗",
            "punctuation": "",
            "fixed": true,
            "speaker_id": null
          },
          {
            "begin_time": 2840,
            "end_time": 3480,
            "text": "科",
            "punctuation": "，",
            "fixed": true,
            "speaker_id": null
          },
          {
            "begin_time": 3480,
            "end_time": 4000,
            "text": "下周",
            "punctuation": "",
            "fixed": true,
            "speaker_id": null
          },
          {
            "begin_time": 4000,
            "end_time": 4520,
            "text": "我们要",
            "punctuation": "",
            "fixed": true,
            "speaker_id": null
          },
          {
            "begin_time": 4520,
            "end_time": 5160,
            "text": "上线",
            "punctuation": "",
            "fixed": true,
            "speaker_id": null
          },
          {
            "begin_time": 5160,
            "end_time": 5440,
            "text": "悬",
            "punctuation": "",
            "fixed": true,
            "speaker_id": null
          },
          {
            "begin_time": 5440,
            "end_time": 5680,
            "text": "枢",
            "punctuation": "",
            "fixed": true,
            "speaker_id": null
          },
          {
            "begin_time": 5680,
            "end_time": 5900,
            "text": "系",
            "punctuation": "",
            "fixed": true,
            "speaker_id": null
          },
          {
            "begin_time": 5900,
            "end_time": 6360,
            "text": "统",
            "punctuation": "。",
            "fixed": true,
            "speaker_id": null
          }
        ],
        "stash": {
          "sentence_id": 2,
          "text": "",
          "begin_time": 6360,
          "current_time": 6360,
          "words": []
        }
      },
      "text": "请把漆原项目的报告发给罗科，下周我们要上线悬枢系统。",
      "request_id": "3756efcf-8388-41c8-832a-9a70bf046f55",
      "output": {
        "sentence": {
          "sentence_id": 1,
          "begin_time": 160,
          "end_time": 6360,
          "text": "请把漆原项目的报告发给罗科，下周我们要上线悬枢系统。",
          "channel_id": 0,
          "sentence_end": true,
          "words": [
            {
              "begin_time": 160,
              "end_time": 600,
              "text": "请把",
              "punctuation": "",
              "fixed": true,
              "speaker_id": null
            },
            {
              "begin_time": 600,
              "end_time": 840,
              "text": "漆",
              "punctuation": "",
              "fixed": true,
              "speaker_id": null
            },
            {
              "begin_time": 840,
              "end_time": 1160,
              "text": "原",
              "punctuation": "",
              "fixed": true,
              "speaker_id": null
            },
            {
              "begin_time": 1160,
              "end_time": 1680,
              "text": "项目的",
              "punctuation": "",
              "fixed": true,
              "speaker_id": null
            },
            {
              "begin_time": 1680,
              "end_time": 2160,
              "text": "报告",
              "punctuation": "",
              "fixed": true,
              "speaker_id": null
            },
            {
              "begin_time": 2160,
              "end_time": 2600,
              "text": "发给",
              "punctuation": "",
              "fixed": true,
              "speaker_id": null
            },
            {
              "begin_time": 2600,
              "end_time": 2840,
              "text": "罗",
              "punctuation": "",
              "fixed": true,
              "speaker_id": null
            },
            {
              "begin_time": 2840,
              "end_time": 3480,
              "text": "科",
              "punctuation": "，",
              "fixed": true,
              "speaker_id": null
            },
            {
              "begin_time": 3480,
              "end_time": 4000,
              "text": "下周",
              "punctuation": "",
              "fixed": true,
              "speaker_id": null
            },
            {
              "begin_time": 4000,
              "end_time": 4520,
              "text": "我们要",
              "punctuation": "",
              "fixed": true,
              "speaker_id": null
            },
            {
              "begin_time": 4520,
              "end_time": 5160,
              "text": "上线",
              "punctuation": "",
              "fixed": true,
              "speaker_id": null
            },
            {
              "begin_time": 5160,
              "end_time": 5440,
              "text": "悬",
              "punctuation": "",
              "fixed": true,
              "speaker_id": null
            },
            {
              "begin_time": 5440,
              "end_time": 5680,
              "text": "枢",
              "punctuation": "",
              "fixed": true,
              "speaker_id": null
            },
            {
              "begin_time": 5680,
              "end_time": 5900,
              "text": "系",
              "punctuation": "",
              "fixed": true,
              "speaker_id": null
            },
            {
              "begin_time": 5900,
              "end_time": 6360,
              "text": "统",
              "punctuation": "。",
              "fixed": true,
              "speaker_id": null
            }
          ],
          "stash": {
            "sentence_id": 2,
            "text": "",
            "begin_time": 6360,
            "current_time": 6360,
            "words": []
          }
        },
        "text": "请把漆原项目的报告发给罗科，下周我们要上线悬枢系统。",
        "request_id": "3756efcf-8388-41c8-832a-9a70bf046f55"
      },
      "usage": {
        "duration": 6,
        "input_tokens": 80,
        "output_tokens": 16,
        "total_tokens": 96
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

<a id="心跳"></a>

<a id="心跳-h4"></a>

#### 心跳

在 `run-task` 中设置 `heartbeat=true`，持续发送静音音频。以下示例展示服务端返回的心跳事件。

<a id="code-block-9"></a>

```json
{
  "header": {
    "action": "run-task",
    "task_id": "eac269a3-a31d-417a-979d-51066926d8a6",
    "streaming": "duplex"
  },
  "payload": {
    "task_group": "audio",
    "task": "asr",
    "function": "recognition",
    "model": "qwen-audio-3.1-asr-flash-streaming",
    "parameters": {
      "format": "pcm",
      "sample_rate": 16000,
      "heartbeat": true
    },
    "input": {}
  }
}
```

<a id="code-block-10"></a>

```json
{
  "header": {
    "task_id": "eac269a3-a31d-417a-979d-51066926d8a6",
    "event": "result-generated",
    "attributes": {}
  },
  "payload": {
    "output": {
      "sentence": {
        "sentence_id": 0,
        "begin_time": 0,
        "end_time": null,
        "text": "",
        "channel_id": 0,
        "speaker_id": null,
        "sentence_end": false,
        "heartbeat": true,
        "words": []
      },
      "text": "",
      "request_id": "eac269a3-a31d-417a-979d-51066926d8a6",
      "output": {
        "sentence": {
          "sentence_id": 0,
          "begin_time": 0,
          "end_time": null,
          "text": "",
          "channel_id": 0,
          "speaker_id": null,
          "sentence_end": false,
          "heartbeat": true,
          "words": []
        },
        "text": "",
        "request_id": "eac269a3-a31d-417a-979d-51066926d8a6"
      }
    },
    "usage": {
      "duration": 2
    }
  }
}
```

<a id="task-finished"></a>

<a id="b8aefe8e0c5fr"></a>

## task-finished

任务处理完成。收到该事件后，本次任务的识别结果已返回完毕。

`header`object

`task_id`string

客户端生成的任务 ID（UUID 格式）。

`event`string

事件类型，固定为 `task-finished`。

`attributes`object

附加属性（通常为空）。

`payload`object

`usage`object

任务结束时的累计用量。字段含义与 [`result-generated.usage`](#usage-fields)相同。

<a id="code-block-11"></a>

```json
{
  "header": {
    "action": "finish-task",
    "task_id": "3756efcf-8388-41c8-832a-9a70bf046f55",
    "streaming": "duplex"
  },
  "payload": {
    "input": {}
  }
}
```

<a id="code-block-12"></a>

```json
{
  "header": {
    "task_id": "3756efcf-8388-41c8-832a-9a70bf046f55",
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

<a id="task-failed"></a>

<a id="3fb17b3b199fy"></a>

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

<a id="code-block-13"></a>

```json
{
  "header": {
    "action": "run-task",
    "task_id": "9272a5a2-8df4-4f2d-af0e-e544c17f3e42",
    "streaming": "duplex"
  },
  "payload": {
    "task_group": "audio",
    "task": "asr",
    "function": "recognition",
    "model": "qwen-audio-3.1-asr-flash-streaming",
    "parameters": {
      "format": "invalid-format",
      "sample_rate": 16000
    },
    "input": {}
  }
}
```

<a id="code-block-14"></a>

```json
{
  "header": {
    "task_id": "9272a5a2-8df4-4f2d-af0e-e544c17f3e42",
    "event": "task-failed",
    "error_code": "UNSUPPORTED_FORMAT",
    "error_message": "UNSUPPORTED_FORMAT"
  },
  "payload": {}
}
```
