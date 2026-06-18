# Sambert客户端事件

**用户指南：**关于模型介绍和选型建议请参见[语音合成](https://help.aliyun.com/zh/model-studio/tts-model/)。

**重要**

Sambert仅支持在北京地域使用。

## **run-task**

**说明**：启动语音合成任务，设置模型、采样率等参数，并一次性发送待合成文本。

**发送时机**：建立 WebSocket 连接后立即发送。

**响应事件**：服务端返回 task-started 事件。

**重要**

Sambert 不支持流式输入，待合成文本需要在 run-task 的 `input.text` 中一次性发送。不支持 continue-task 和 finish-task 指令。

**header** `_object_` **（必选）**

**属性**

**action** `_string_` **（必选）**

指令类型，固定为 `run-task`。

**task\_id** `_string_` **（必选）**

客户端生成的任务 ID（UUID 格式），用于关联后续事件。

**streaming** `_string_` **（必选）**

固定为 `out`

```
{
    "header": {
        "action": "run-task",
        "task_id": "2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx",
        "streaming": "out"
    },
    "payload": {
        "task_group": "audio",
        "task": "tts",
        "function": "SpeechSynthesizer",
        "model": "sambert-zhichu-v1",
        "parameters": {
            "text_type": "PlainText",
            "format": "wav",
            "sample_rate": 16000,
            "volume": 50,
            "rate": 1.0,
            "pitch": 1.0,
            "word_timestamp_enabled": true,
            "phoneme_timestamp_enabled": true
        },
        "input": {
            "text": "待合成文本"
        }
    }
}
```

**payload** `_object_` **（必选）**

**属性**

**task\_group** `_string_` **（必选）**

任务组，固定为 `audio`。

**task** `_string_` **（必选）**

任务类型，固定为 `tts`。

**function** `_string_` **（必选）**

功能类型，固定为 `SpeechSynthesizer`。

**model** `_string_` **（必选）**

模型名称，如 `sambert-zhichu-v1`。

**input** `_object_` **（必选）**

输入数据，包含 `text` 字段，直接传入待合成文本。

**text** `_string_` **（必选）**

待合成文本。

**parameters** `_object_` **（必选）**

语音合成参数。

**属性**

**text\_type** `_string_` **（必选）**

固定为 `PlainText`。

**format** `_string_` （可选）

音频编码格式。

取值范围：

-   pcm
    
-   wav（默认）
    
-   mp3
    

**sample\_rate** `_integer_` （可选）

音频采样率（Hz）。

取值范围：8000, 16000（默认）, 22050, 24000。

**volume** `_integer_` （可选）

音量。

默认值：50。

取值范围：\[0, 100\]。

**rate** `_float_` （可选）

语速。

默认值：1.0。

取值范围：\[0.5, 2.0\]。

**pitch** `_float_` （可选）

音调。

默认值：1.0。

取值范围：\[0.5, 2.0\]。

**word\_timestamp\_enabled** `_boolean_` （可选）

是否开启字级别时间戳。

默认值：false。

适用范围：所有 Sambert 模型。

**phoneme\_timestamp\_enabled** `_boolean_` （可选）

是否开启音素级别时间戳。

默认值：false。

需要先开启 word\_timestamp\_enabled。
