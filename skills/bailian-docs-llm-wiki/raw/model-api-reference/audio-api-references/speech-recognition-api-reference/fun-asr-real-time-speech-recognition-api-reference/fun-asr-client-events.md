# 实时语音识别（Fun-ASR）客户端事件

本文介绍 Fun-ASR 实时语音识别服务中客户端通过 WebSocket 发送给服务端的客户端事件，包括 run-task（启动任务）、continue-task（更新上下文）、finish-task（结束任务）等指令的数据结构与字段含义。

**用户指南：**关于模型介绍和选型建议请参见[语音识别](https://help.aliyun.com/zh/model-studio/asr-model/)。

**事件交互流程**：如需了解事件交互时序，请参见[WebSocket API](https://help.aliyun.com/zh/model-studio/fun-asr-realtime-websocket-api)。

## **run-task**

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

## 基本请求

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

## 携带上下文

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
        "input": {
            "context": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": "你好啊"
                        }
                    ]
                },
                {
                    "role": "assistant",
                    "content": [
                        {
                            "type": "text",
                            "text": "你好啊，我是通义千问，有什么可以帮助你的？"
                        }
                    ]
                }
            ]
        }
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

[支持的模型](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide#4a43cc1bb7kxg)名称。

**input** `_object_` **（必选）**

输入对象。不携带上下文时传入`{}`。

**重要**

仅 `fun-asr-realtime` 和 `fun-asr-realtime-2025-11-07` 模型支持 context 参数。

**属性**

**context** `_array(object)_` （可选）

对话上下文，用于辅助识别、提升专有词汇的识别准确率。使用方法详见[快速开始](https://help.aliyun.com/zh/model-studio/improve-asr-accuracy#ctx-quickstart-sec)。

**重要**

约束：上下文消息（`input_text` 和 `text` 类型）各最多 5 条，超出时保留最近的 5 条。每轮上下文文本总长度（`user` 和 `assistant` 的 `text` 字段长度之和）不超过 400 个字符（按字符数计算，每个字符计为 1），超出部分从末尾截断。

**重要**

携带上下文时，`context` 中的消息顺序有要求：上下文消息必须按对话轮次排列，每轮中 `user`（`input_text` 类型）必须在对应的 `assistant`（`text` 类型）之前。

**属性**

**role** `_string_` **（必选）**

消息角色。取值范围：

-   `user`：前几轮用户语音的识别结果或领域相关的词表。
    
-   `assistant`：前几轮大语言模型的回复内容。
    

**content** `_array(object)_` **（必选）**

消息内容列表。

**属性**

**type** `_string_` **（必选）**

内容类型。取值范围：

-   `input_text`：前几轮用户语音的识别结果或领域相关的词表（role 为 user 时使用），需同时传入 `text` 字段。
    
-   `text`：前几轮大语言模型的回复内容（role 为 assistant 时使用），需同时传入 `text` 字段。
    

**text** `_string_` **（必选）**

文本内容。当 `type` 为 `input_text` 时，填入前几轮用户语音的识别结果或领域相关的词表；当 `type` 为 `text` 时，填入前几轮大语言模型的回复内容。

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

-   8k模型仅支持 8000 Hz，其他模型支持任意采样率。
    

**vocabulary\_id** `_string_` （可选）

热词列表 ID。

**language\_hints** `_array[string]_` （可选）

待识别音频语种。无默认值，不设置时模型自动识别。

系统仅读取数组中的首个值，多余值将被忽略。

不同模型支持的语言代码如下：

-   fun-asr-realtime、fun-asr-realtime-2025-11-07：
    
    -   zh: 中文
        
    -   en: 英文
        
    -   ja: 日语
        
    -   ko：韩语
        
    -   vi：越南语
        
    -   th：泰语
        
    -   id：印尼语
        
    -   ms：马来语
        
    -   tl：菲律宾语
        
    -   hi：印地语
        
    -   ar：阿拉伯语
        
    -   fr：法语
        
    -   de：德语
        
    -   es：西班牙语
        
    -   pt：葡萄牙语
        
    -   ru：俄语
        
    -   it：意大利语
        
    -   nl：荷兰语
        
    -   sv：瑞典语
        
    -   da：丹麦语
        
    -   fi：芬兰语
        
    -   no：挪威语
        
    -   el：希腊语
        
    -   pl：波兰语
        
    -   cs：捷克语
        
    -   hu：匈牙利语
        
    -   ro：罗马尼亚语
        
    -   bg：保加利亚语
        
    -   hr：克罗地亚语
        
    -   sk：斯洛伐克语
        
-   fun-asr-realtime-2026-02-28：
    
    -   zh: 中文
        
    -   en: 英文
        
    -   ja: 日语
        
-   fun-asr-realtime-2025-09-15：
    
    -   zh: 中文
        
    -   en: 英文
        
-   fun-asr-flash-8k-realtime、fun-asr-flash-8k-realtime-2026-01-28：
    
    -   zh: 中文
        

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

语音与噪音的判定阈值，用于调整语音活动检测（VAD）的灵敏度。

取值范围：\[-1.0, 1.0\]。

取值说明：

-   取值越接近 -1：降低噪音判定阈值，噪音被识别为语音的概率增大，可能导致更多噪音被转写
    
-   取值越接近 +1：提高噪音判定阈值，语音被误判为噪音的概率增大，可能导致部分语音被过滤
    

此参数为高级配置参数，调整可能显著影响识别效果，建议：

-   调整前充分测试验证效果
    
-   根据实际音频环境小幅度调整（建议步长 0.1）
    

**special\_word\_filter** `_string_` （可选）

指定在语音识别过程中需要处理的敏感词，并支持对不同敏感词设置不同的处理方式。详情请参见[敏感词过滤](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide#rt03-sensitive-h3)。

## **continue-task**

**说明**：在任务执行过程中更新对话上下文信息，用于辅助识别。

**发送时机**：任务运行中，需要更新对话上下文时发送。

**重要**

仅 `fun-asr-realtime` 和 `fun-asr-realtime-2025-11-07` 模型支持该事件。

**header** `_object_` **（必选）**

**属性**

**action** `_string_` **（必选）**

指令类型，固定为 `continue-task`。

**task\_id** `_string_` **（必选）**

客户端生成的任务 ID（UUID 格式），需与[run-task](#9cae7e7b85ebm)事件中的 task\_id 保持一致。

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
            "context": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": "你好啊"
                        }
                    ]
                },
                {
                    "role": "assistant",
                    "content": [
                        {
                            "type": "text",
                            "text": "你好啊，我是通义千问，有什么可以帮助你的？"
                        }
                    ]
                }
            ]
        }
    }
}
```

**payload** `_object_` **（必选）**

**属性**

**input** `_object_` **（必选）**

输入对象。

**属性**

**context** `_array(object)_` （可选）

对话上下文，用于辅助识别、提升专有词汇的识别准确率。使用方法详见[快速开始](https://help.aliyun.com/zh/model-studio/improve-asr-accuracy#ctx-quickstart-sec)。

**重要**

约束：上下文消息（`input_text` 和 `text` 类型）各最多 5 条，超出时保留最近的 5 条。每轮上下文文本总长度（`user` 和 `assistant` 的 `text` 字段长度之和）不超过 400 个字符（按字符数计算，每个字符计为 1），超出部分从末尾截断。

**重要**

携带上下文时，`context` 中的消息顺序有要求：上下文消息必须按对话轮次排列，每轮中 `user`（`input_text` 类型）必须在对应的 `assistant`（`text` 类型）之前。

**属性**

**role** `_string_` **（必选）**

消息角色。取值范围：

-   `user`：前几轮用户语音的识别结果或领域相关的词表。
    
-   `assistant`：前几轮大语言模型的回复内容。
    

**content** `_array(object)_` **（必选）**

消息内容列表。

**属性**

**type** `_string_` **（必选）**

内容类型。取值范围：

-   `input_text`：前几轮用户语音的识别结果或领域相关的词表（role 为 user 时使用），需同时传入 `text` 字段。
    
-   `text`：前几轮大语言模型的回复内容（role 为 assistant 时使用），需同时传入 `text` 字段。
    

**text** `_string_` **（必选）**

文本内容。当 `type` 为 `input_text` 时，填入前几轮用户语音的识别结果或领域相关的词表；当 `type` 为 `text` 时，填入前几轮大语言模型的回复内容。

## **finish-task**

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
