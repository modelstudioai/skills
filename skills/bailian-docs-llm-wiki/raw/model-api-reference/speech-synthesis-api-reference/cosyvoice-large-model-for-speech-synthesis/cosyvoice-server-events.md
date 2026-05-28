# CosyVoice服务端事件

**用户指南：**关于模型介绍和选型建议请参见[语音合成](https://help.aliyun.com/zh/model-studio/tts-model/)。

## **task-started**

当客户端发送 `run-task` 指令后，服务端返回 `task-started` 事件，标志任务已成功开启。只有在接收到该事件后，客户端才能继续发送后续指令。

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

客户端发送文本后，服务端持续返回 `result-generated` 事件。该事件返回句子元信息。

**header.task\_id** `_string_`

客户端生成的任务 ID。

## sentence-begin

```
{
  "header": {
    "task_id": "3f2d5c86-0550-45c0-801f-xxxxxxxxxx",
    "event": "result-generated",
    "attributes": {}
  },
  "payload": {
    "output": {
      "sentence": {
        "index": 0,
        "words": []
      },
      "type": "sentence-begin",
      "original_text": "床前明月光，"
    }
  }
}
```

## sentence-synthesis

```
{
    "header": {
        "task_id": "3f2d5c86-0550-45c0-801f-xxxxxxxxxx",
        "event": "result-generated",
        "attributes": {}
    },
    "payload": {
        "output": {
            "sentence": {
                "index": 0,
                "words": []
            },
            "type": "sentence-synthesis"
        }
    }
}
```

## sentence-end

```
{
  "header": {
    "task_id": "3f2d5c86-0550-45c0-801f-xxxxxxxxxx",
    "event": "result-generated",
    "attributes": {}
  },
  "payload": {
    "output": {
      "sentence": {
        "index": 0,
        "words": [
          {
            "text": "床",
            "begin_index": 0,
            "end_index": 1,
            "begin_time": 0,
            "end_time": 263
          }
        ]
      },
      "type": "sentence-end",
      "original_text": "床前明月光，"
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

**type** `_string_`

子事件类型，取值：

-   `sentence-begin`：句子开始，返回待合成的文本内容
    
-   `sentence-synthesis`：标识音频数据块，每个事件后立即通过 WebSocket binary 通道传输一个音频数据帧
    
-   `sentence-end`：句子结束，返回文本内容和累计字符数
    

**sentence.index** `_integer_`

句子编号，从 0 开始。

**sentence.words** `_array_`

字级别时间戳信息数组。

**words 元素属性**

**text** `_string_`

字的文本内容。

**begin\_index** `_integer_`

字在句子中的开始位置索引，从 0 开始。

**end\_index** `_integer_`

字在句子中的结束位置索引，从 1 开始。

**begin\_time** `_integer_`

字对应音频的开始时间戳，单位：毫秒。

**end\_time** `_integer_`

字对应音频的结束时间戳，单位：毫秒。

**original\_text** `_string_`

分句后的句子文本内容。

**payload.usage** `_object_`

计费信息，在 sentence-end 事件中返回。

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
