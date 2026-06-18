# 实时语音识别（Fun-ASR）服务端事件

本文介绍 Fun-ASR 实时语音识别服务通过 WebSocket 推送给客户端的服务端事件，包括 task-started、result-generated、task-finished、task-failed 四类事件的数据结构与字段含义。

**用户指南：**关于模型介绍和选型建议请参见[语音识别](https://help.aliyun.com/zh/model-studio/asr-model/)。

**事件交互流程**：如需了解事件交互时序，请参见[WebSocket API](https://help.aliyun.com/zh/model-studio/fun-asr-realtime-websocket-api)。

### **task-started**

**说明**：任务启动成功，客户端可开始发送音频数据。

**header** `_object_`

**属性**

**task\_id** `_string_`

客户端生成的任务 ID（UUID 格式）。

**event** `_string_`

事件类型，固定为 `task-started`。

**attributes** `_object_`

附加属性（通常为空）。

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

**payload** `_object_`

固定为`{}`。

### **result-generated**

**说明**：识别结果，包含中间结果（sentence\_end=false）和最终结果（sentence\_end=true）。

**header** `_object_`

**属性**

**task\_id** `_string_`

客户端生成的任务 ID（UUID 格式）。

**event** `_string_`

事件类型，固定为 `result-generated`。

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
        "begin_time": 170,
        "end_time": 920,
        "text": "好，我知道了",
        "heartbeat": false,
        "sentence_end": true,
        "sentence_id": 1,
        "words": [
          {
            "begin_time": 170,
            "end_time": 295,
            "text": "好",
            "punctuation": "，"
          },
          {
            "begin_time": 295,
            "end_time": 503,
            "text": "我",
            "punctuation": ""
          },
          {
            "begin_time": 503,
            "end_time": 711,
            "text": "知道",
            "punctuation": ""
          },
          {
            "begin_time": 711,
            "end_time": 920,
            "text": "了",
            "punctuation": ""
          }
        ]
      }
    },
    "usage": {
      "duration": 3
    }
  }
}
```

**payload** `_object_`

**属性**

**output** `_object_`

**属性**

**usage** `_object_`

当`payload.output.sentence.sentence_end`为`false`（当前句子未结束）时，`usage`为`null`。

当`payload.output.sentence.sentence_end`为`true`（当前句子已结束）时，`usage.duration`为当前任务计费时长。

**属性**

**duration** `_integer_`

任务计费时长（s）。

**属性**

**sentence** `_object_`

**属性**

**begin\_time** `_integer_`

句子开始时间（ms）。

**end\_time** `_integer_`

句子结束时间（ms）。

**text** `_string_`

识别文本。

**heartbeat** `_boolean_`

若为 true，可跳过该结果（心跳包）。

**sentence\_end** `_boolean_`

是否句子结束（true=最终结果，false=中间结果）。

**sentence\_id** `_integer_`

句子的序号标识。正常识别结果中，sentence\_id 从 1 开始递增。当 heartbeat 为 true 时（即心跳包），sentence\_id 固定为 0。

**words** `_array[object]_`

字时间戳信息。

**属性**

**begin\_time** `_integer_`

字开始时间（ms）。

**end\_time** `_integer_`

字结束时间（ms）。

**text** `_string_`

识别文本。

**punctuation** `_string_`

标点符号。

### **task-finished**

**说明**：任务正常结束，可关闭连接或复用连接。

**header** `_object_`

**属性**

**task\_id** `_string_`

客户端生成的任务 ID（UUID 格式）。

**event** `_string_`

事件类型，固定为 `task-finished`。

**attributes** `_object_`

附加属性（通常为空）。

```
{
    "header": {
        "task_id": "2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx",
        "event": "task-finished",
        "attributes": {}
    },
    "payload": {
        "output": {},
        "usage": null
    }
}
```

**payload** `_object_`

无需关注其中内容，通常为`{}`。

### **task-failed**

**说明**：任务失败，连接会被关闭，无法复用。

**header** `_object_`

**属性**

**task\_id** `_string_`

客户端生成的任务 ID（UUID 格式）。

**event** `_string_`

事件类型，固定为 `task-failed`。

**error\_code** `_string_`

错误类型描述。

**error\_message** `_string_`

具体错误原因。

**attributes** `_object_`

附加属性（通常为空）。

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

**payload** `_object_`

固定为`{}`。
