# 实时语音识别（Fun-ASR）客户端事件

本文介绍 Fun-ASR 实时语音识别服务中客户端通过 WebSocket 发送给服务端的客户端事件，包括 run-task（启动任务）和 finish-task（结束任务）两类指令的数据结构与字段含义。

**用户指南：**关于模型介绍和选型建议请参见[语音识别](https://help.aliyun.com/zh/model-studio/asr-model/)。

**事件交互流程**：如需了解事件交互时序，请参见[WebSocket API](https://help.aliyun.com/zh/model-studio/fun-asr-realtime-websocket-api)。

### **run-task**

**说明**：启动语音识别任务，设置模型、音频格式、采样率等参数。

**发送时机**：建立 WebSocket 连接后立即发送。

**响应事件**：服务端返回 `[task-started](https://help.aliyun.com/zh/model-studio/fun-asr-server-events#eac316aeacafj)` 事件后才能发送音频。

**header** `_object_` **（必选）**

**属性**

**action** `_string_` **（必选）**

指令类型，固定为 `run-task`。

**task\_id** `_string_` **（必选）**

客户端生成的任务 ID（UUID 格式），用于关联后续事件。

**streaming** `_string_` **（必选）**

固定为 `duplex`。

```
{
    "header": {
        "action": "run-task",
        "task_id": "2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx",
        "streaming": "duplex"
    },
    "payload": {
        "task_group": "audio",
        "task": "asr",
        "function": "recognition",
        "model": "fun-asr-realtime",
        "parameters": {
            "format": "pcm",
            "sample_rate": 16000
        },
        "input": {}
    }
}
```

**payload** `_object_` **（必选）**

**属性**

**task\_group** `_string_` **（必选）**

任务组，固定为 `audio`。

**task** `_string_` **（必选）**

任务类型，固定为 `asr`。

**function** `_string_` **（必选）**

功能类型。固定为`recognition`。

**model** `_string_` **（必选）**

模型名称。

**input** `_object_` **（必选）**

固定为`{}`。

**parameters** `_object_` **（必选）**

语音识别参数。

**属性**

**format** `_string_` **（必选）**

音频格式。

取值范围：

-   `pcm`
    
-   `wav`
    
-   `mp3`
    
-   `opus`
    
-   `speex`
    
-   `aac`
    
-   `amr`
    

**sample\_rate** `_integer_` **（必选）**

采样率（Hz）。

取值范围：

-   8k模型仅支持 8000 Hz，其他模型仅支持 16000 Hz
    

**vocabulary\_id** `_string_` （可选）

热词列表 ID。

**language\_hints** `_array[string]_` （可选）

待识别音频语种。无默认值，不设置时模型自动识别。

系统仅读取数组中的首个值，多余值将被忽略。

取值范围：

-   zh: 中文
    
-   en: 英文
    
-   ja: 日语
    

**semantic\_punctuation\_enabled** `_boolean_` （可选）

是否启用语义断句。

默认值：false。

-   true：开启语义断句，关闭 VAD 断句。
    
-   false（默认）：开启 VAD 断句，关闭语义断句。
    

语义断句准确性更高，适合会议转写场景；VAD（Voice Activity Detection，语音活动检测）断句延迟较低，适合交互场景。

**max\_sentence\_silence** `_integer_` （可选）

**重要**

-   仅在`semantic_punctuation_enabled`参数为false时生效。
    

VAD 断句静音阈值（ms）。当一段语音后的静音时长超过该阈值时，系统会判定该句子已结束。

默认值：1300。

取值范围：\[200, 6000\]。

**multi\_threshold\_mode\_enabled** `_boolean_` （可选）

**重要**

-   仅在`semantic_punctuation_enabled`参数为false时生效。
    

是否启用多阈值模式。启用后可防止 VAD 断句切割过长。

默认值：false。

**heartbeat** `_boolean_` （可选）

是否启用心跳包。

默认值：false。

-   true：在持续发送静音音频的情况下，可保持与服务端的连接不中断。
    
-   false（默认）：即使持续发送静音音频，连接也将在60秒后因超时而断开。
    

**speech\_noise\_threshold** `_float_` （可选）

**重要**

仅Fun-ASR支持该参数。

语音与噪音的判定阈值，用于调整语音活动检测（VAD）的灵敏度。

取值范围：\[-1.0, 1.0\]。

取值说明：

-   取值越接近 -1：降低噪音判定阈值，噪音被识别为语音的概率增大，可能导致更多噪音被转写
    
-   取值越接近 +1：提高噪音判定阈值，语音被误判为噪音的概率增大，可能导致部分语音被过滤
    

此参数为高级配置参数，调整可能显著影响识别效果，建议：

-   调整前充分测试验证效果
    
-   根据实际音频环境小幅度调整（建议步长 0.1）
    

### **finish-task**

**说明**：通知服务端音频发送完毕，请求结束任务。

**发送时机**：所有音频数据发送完毕后。

**响应事件**：服务端返回 `[task-finished](https://help.aliyun.com/zh/model-studio/fun-asr-server-events#b8aefe8e0c5fr)` 事件。

**header** `_object_` **（必选）**

**属性**

**action** `_string_` **（必选）**

指令类型，固定为 `finish-task`。

**task\_id** `_string_` **（必选）**

客户端生成的任务 ID（UUID 格式），需与[run-task](#9cae7e7b85ebm)事件中的 task\_id 保持一致。

**streaming** `_string_` **（必选）**

固定为 `duplex`。

```
{
    "header": {
        "action": "finish-task",
        "task_id": "2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx",
        "streaming": "duplex"
    },
    "payload": {
        "input": {}
    }
}
```

**payload** `_object_` **（必选）**

**属性**

**input** `_object_` **（必选）**

固定为`{}`。
