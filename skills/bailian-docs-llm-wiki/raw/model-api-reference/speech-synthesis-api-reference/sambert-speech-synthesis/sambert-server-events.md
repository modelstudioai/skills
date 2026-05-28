# Sambert服务端事件

**用户指南：**关于模型介绍和选型建议请参见[语音合成](https://help.aliyun.com/zh/model-studio/tts-model/)。

## **task-started**

当客户端发送 `run-task` 指令后，服务端返回 `task-started` 事件，标志任务已成功开启。

**header.task\_id** `_string_`

客户端生成的任务 ID。

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

**header.event** `_string_`

事件类型，固定为 `task-started`。

**payload** `_object_`

无内容，为空对象。

## **result-generated**

客户端发送文本后，服务端持续返回 `result-generated` 事件。该事件在 `output.sentence` 中直接返回完整的时间戳信息，包括字级别和音素级别时间戳（需启用相应参数）。

**header.task\_id** `_string_`

客户端生成的任务 ID。

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
        "end_time": 1162,
        "words": [
          {
            "text": "床",
            "begin_time": 0,
            "end_time": 263,
            "phonemes": [
              {
                "begin_time": 0,
                "end_time": 119,
                "text": "ch_c",
                "tone": 2
              }
            ]
          }
        ]
      }
    },
    "usage": {
      "characters": 6
    }
  }
}
```

**header.event** `_string_`

事件类型，固定为 `result-generated`。

**payload.output** `_object_`

输出信息。

**属性**

**sentence.begin\_time** `_integer_`

句子开始时间戳，单位：毫秒。

**sentence.end\_time** `_integer_`

句子结束时间戳，单位：毫秒。

**sentence.words** `_array_`

字级别时间戳信息数组。

**words 元素属性**

**text** `_string_`

字的文本内容。

**begin\_time** `_integer_`

字对应音频的开始时间戳，单位：毫秒。

**end\_time** `_integer_`

字对应音频的结束时间戳，单位：毫秒。

**phonemes** `_array_`**（需启用 phoneme\_timestamp\_enabled）**

音素级别时间戳信息数组。

**phonemes 元素属性**

**text** `_string_`

音素文本。

**tone** `_integer_`

音调。

**begin\_time** `_integer_`

音素开始时间戳，单位：毫秒。

**end\_time** `_integer_`

音素结束时间戳，单位：毫秒。

**payload.usage** `_object_`

计费信息。

**属性**

**characters** _integer_

截止当前累计的计费字符数。

## **task-finished**

服务端返回 `task-finished` 事件，标志任务已结束。客户端可以关闭 WebSocket 连接或复用连接开启新任务。

**header.task\_id** `_string_`

客户端生成的任务 ID。

```
{
  "header": {
    "task_id": "2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx",
    "event": "task-finished",
    "attributes": {
      "request_uuid": "0a9dba9e-d3a6-45a4-be6d-xxxxxxxxxxxx"
    }
  },
  "payload": {
    "usage": {
      "characters": 13
    }
  }
}
```

**header.event** `_string_`

事件类型，固定为 `task-finished`。

**payload.usage.characters** `_integer_`

截止当前累计的计费字符数。

## **task-failed**

当任务失败时，服务端返回 `task-failed` 事件。客户端需要关闭 WebSocket 连接并处理错误。

**header.task\_id** `_string_`

客户端生成的任务 ID。

```
{
  "header": {
    "task_id": "2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx",
    "event": "task-failed",
    "error_code": "InvalidParameter",
    "error_message": "[tts:]Engine return error code: 418",
    "attributes": {}
  },
  "payload": {}
}
```

**header.event** `_string_`

事件类型，固定为 `task-failed`。

**header.error\_code** `_string_`

错误码。

**header.error\_message** `_string_`

具体错误信息。
