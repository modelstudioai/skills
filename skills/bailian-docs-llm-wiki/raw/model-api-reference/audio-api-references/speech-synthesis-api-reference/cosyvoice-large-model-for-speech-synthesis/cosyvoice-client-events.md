# Qwen-Audio-TTS/CosyVoice客户端事件

**用户指南：**关于模型介绍和选型建议请参见[语音合成](https://help.aliyun.com/zh/model-studio/tts-model/)。

## **run-task**

**说明**：启动语音合成任务，设置模型、音色、采样率等参数。

**发送时机**：建立 WebSocket 连接后立即发送。

**响应事件**：服务端返回 task-started 事件后才能发送后续指令。

**header** `_object_` **（必选）**

**属性**

**action** `_string_` **（必选）**

指令类型，固定为 `run-task`。

**task\_id** `_string_` **（必选）**

客户端生成的任务 ID（UUID 格式），用于关联后续事件。和后续 continue-task、finish-task 中的 task\_id 保持一致。

**streaming** `_string_` **（必选）**

固定为 `duplex`

```
{
    "header": {
        "action": "run-task",
        "task_id": "2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx",
        "streaming": "duplex"
    },
    "payload": {
        "task_group": "audio",
        "task": "tts",
        "function": "SpeechSynthesizer",
        "model": "qwen-audio-3.0-tts-flash",
        "parameters": {
            "text_type": "PlainText",
            "voice": "longanlingxi",
            "format": "mp3",
            "sample_rate": 22050,
            "volume": 50,
            "rate": 1.0,
            "pitch": 1.0,
            "enable_ssml": false
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

任务类型，固定为 `tts`。

**function** `_string_` **（必选）**

功能类型，固定为 `SpeechSynthesizer`。

**model** `_string_` **（必选）**

模型名称。

**input** `_object_` **（必选）**

输入数据：固定为空对象 `{}`，待合成文本通过 continue-task 指令发送。

**parameters** `_object_` **（必选）**

语音合成参数。

**属性**

**text\_type** `_string_` **（必选）**

固定为 `PlainText`。

**voice** `_string_` **（必选）**

语音合成所使用的音色。

-   **系统音色**：参见[CosyVoice音色列表](https://help.aliyun.com/zh/model-studio/cosyvoice-voice-list)
    
-   **复刻音色**：通过声音复刻功能定制
    
-   **声音设计音色**：通过声音设计功能定制
    

**format** `_string_` （可选）

音频编码格式。

取值范围：

-   pcm
    
-   wav
    
-   mp3（默认）
    
-   opus
    

**重要**

`cosyvoice-v1`不支持opus格式。

**sample\_rate** `_integer_` （可选）

音频采样率（Hz）。

取值范围：8000, 16000, 22050（默认）, 24000, 44100, 48000。

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

**bit\_rate** `_integer_` （可选）

音频码率（kbps）。音频格式为opus时，支持通过`bit_rate`参数调整码率。

默认值：32。

取值范围：\[6, 510\]。

`cosyvoice-v1`模型不支持该参数。

**enable\_ssml** `_boolean_` （可选）

是否开启 SSML 功能。

默认值：false。

设为 true 后，仅允许发送一次 continue-task 指令。

SSML 的使用限制（支持的模型、音色和接口），请参见[使用限制](https://help.aliyun.com/zh/model-studio/ssml-latex-user-guide#sl01-constraint-h3)。

**word\_timestamp\_enabled** `_boolean_` （可选）

是否开启字级别时间戳。

默认值：false。

仅在流式输出模式下可用。支持的音色范围：cosyvoice-v3.5-plus、cosyvoice-v3.5-flash、cosyvoice-v3-flash、cosyvoice-v3-plus和cosyvoice-v2模型的复刻音色，以及[CosyVoice音色列表](https://help.aliyun.com/zh/model-studio/cosyvoice-voice-list)中标记为支持的系统音色。qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash及其他模型的复刻音色不支持此功能。

**seed** `_integer_` （可选）

生成时使用的随机数种子，使合成的效果产生变化。在模型版本、文本、音色及其他参数均相同的前提下，使用相同的seed可复现相同的合成结果。

默认值0。

取值范围：\[0, 65535\]。

cosyvoice-v1不支持该参数。

**language\_hints** `_array[string]_` （可选）

**重要**

-   此参数为数组，但当前版本仅处理第一个元素，因此建议只传入一个值。
    
-   此参数用于指定语音合成的目标语言，该设置与声音复刻时的样本音频的语种无关。如需设置复刻任务的源语言，请参见声音复刻API参考。
    

指定语音合成的目标语言，提升合成效果。cosyvoice-v1不支持该功能。

当数字、缩写、符号等朗读方式或者小语种合成效果不符合预期时使用，例如：

-   数字朗读方式不符合预期，“hello, this is 110”读成“hello, this is one one zero”而非“hello, this is 幺幺零”
    
-   符号朗读不准确，“@”读成“艾特”而非“at”
    
-   小语种合成效果差，合成不自然
    

取值范围：

-   zh：中文
    
-   en：英文
    
-   fr：法语
    
-   de：德语
    
-   ja：日语
    
-   ko：韩语
    
-   ru：俄语
    
-   pt：葡萄牙语
    
-   th：泰语
    
-   id：印尼语
    
-   vi：越南语
    
-   it：意大利语
    
-   ms：马来语
    

**instruction** `_string_` （可选）

设置指令，用于控制方言、情感或角色等合成效果。具体使用说明请参见[指令控制](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#12884a10929p9)。

**enable\_aigc\_tag** `_boolean_` （可选）

是否在生成的音频中添加AIGC隐性标识。设置为true时，会将隐性标识嵌入到支持格式（wav/mp3/opus）的音频中。

默认值：false。

仅qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash、cosyvoice-v3-flash、cosyvoice-v3-plus、cosyvoice-v2支持该功能。

**aigc\_propagator** `_string_` （可选）

设置AIGC隐性标识中的 `ContentPropagator` 字段，用于标识内容的传播者。仅在 `enable_aigc_tag` 为 `true` 时生效。

默认值：阿里云UID。

仅qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash、cosyvoice-v3-flash、cosyvoice-v3-plus、cosyvoice-v2支持该功能。

**aigc\_propagate\_id** `_string_` （可选）

设置AIGC隐性标识中的 `PropagateID` 字段，用于唯一标识一次具体的传播行为。仅在 `enable_aigc_tag` 为 `true` 时生效。

默认值：本次语音合成请求Request ID。

仅qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash、cosyvoice-v3-flash、cosyvoice-v3-plus、cosyvoice-v2支持该功能。

**hot\_fix** `_object_` （可选）

文本热修复配置，用于自定义指定词语的发音或对待合成文本进行替换。

qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash、cosyvoice-v2、cosyvoice-v1不支持该功能。

参数介绍：

-   pronunciation：自定义发音。指定词语的拼音标注，用于纠正默认发音不准确的情况。
    
-   replace：文本替换。在语音合成前将指定词语替换为目标文本，替换后的文本将作为实际合成内容。
    

示例：

```
"hot_fix": {
  "pronunciation": [
    {"天气": "tian1 qi4"}
  ],
  "replace": [
    {"今天": "金天"}
  ]
}
```

**enable\_markdown\_filter** `_boolean_` （可选）

**重要**

仅cosyvoice-v3-flash复刻音色支持该功能。

是否启用 Markdown 过滤。启用该功能后，系统在合成语音前自动过滤输入文本中的 Markdown 标记符号，避免将其朗读为文字内容。

默认值：false。

取值范围：

-   true：启用Markdown过滤
    
-   false：禁用Markdown过滤
    

## **continue-task**

**说明**：用于发送待合成文本。可一次性发送，也可分段按顺序发送。

**发送时机**：在接收到服务端返回的 task-started 事件后。

**数量限制**：

-   单次调用最多发送 20000 字符
    
-   累计最多发送 200000 字符
    
-   发送间隔不得超过 23 秒，否则连接超时
    

**header** `_object_` **（必选）**

**属性**

**action** `_string_` **（必选）**

指令类型，固定为 `continue-task`。

**task\_id** `_string_` **（必选）**

任务 ID（UUID 格式），需要和 run-task 中的 task\_id 保持一致。

**streaming** `_string_` **（必选）**

固定为 `duplex`。

```
{
    "header": {
        "action": "continue-task",
        "task_id": "2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx",
        "streaming": "duplex"
    },
    "payload": {
        "input": {
            "text": "床前明月光，疑是地上霜"
        }
    }
}
```

**payload** `_object_` **（必选）**

**属性**

**input** `_object_` **（必选）**

包含待合成文本。

**text** `_string_` **（必选）**

待合成文本。单次最多 20000 字符，累计最多 200000 字符。

## **finish-task**

**说明**：通知服务端文本发送完毕，请求结束任务。

**发送时机**：所有文本发送完毕后立即发送。

**响应事件**：服务端返回 task-finished 事件。

**header** `_object_` **（必选）**

**属性**

**action** `_string_` **（必选）**

指令类型，固定为 `finish-task`。

**task\_id** `_string_` **（必选）**

任务 ID（UUID 格式），需要和 run-task 中的 task\_id 保持一致。

**streaming** `_string_` **（必选）**

固定为 `duplex`

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

固定为 `{}`。
