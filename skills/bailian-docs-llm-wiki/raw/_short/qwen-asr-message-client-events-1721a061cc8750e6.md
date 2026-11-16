# Qwen-Audio-ASR-Message客户端事件

Qwen-Audio-ASR-Message 客户端事件参考，介绍 run-task、continue-task、finish-task 的字段、发送顺序及对应服务端事件。

## 事件交互流程

1.  发送 [run-task](https://help.aliyun.com/zh/model-studio/qwen-asr-message-client-events#run-task)，收到 [task-started](https://help.aliyun.com/zh/model-studio/qwen-asr-message-server-events#task-started) 后开始发送音频。
2.  持续发送音频，同时接收 [result-generated](https://help.aliyun.com/zh/model-studio/qwen-asr-message-server-events#result-generated)。
3.  任务运行期间，可通过 [continue-task](https://help.aliyun.com/zh/model-studio/qwen-asr-message-client-events#continue-task) 更新对话上下文；音频仍通过音频通道发送。
4.  音频发送完毕后发送 [finish-task](https://help.aliyun.com/zh/model-studio/qwen-asr-message-client-events#finish-task)，继续接收结果，直到收到 [task-finished](https://help.aliyun.com/zh/model-studio/qwen-asr-message-server-events#task-finished)；任务失败时返回 [task-failed](https://help.aliyun.com/zh/model-studio/qwen-asr-message-server-events#task-failed)。

音频数据不通过 `run-task` 发送：WebSocket 使用二进制帧，AOQ 使用 Audio Track。连接、鉴权和音频传输方式请参见 [WebSocket API](raw/_short/qwen-asr-message-websocket-api-8b78d8662335cafa.md) 或 [AOQ 接入](raw/_short/qwen-asr-message-aoq-access-7699c2c24f2a0149.md)。

## run-task

建立连接后，客户端发送 `run-task` 事件，启动语音识别任务并设置模型、音频格式、采样率等参数。

**重要****收到 `task-started` 后才能发送音频。** `run-task` 仅用于启动和配置任务，不携带音频数据。

`header`object必填

`action`string必填

指令类型，固定为 `run-task`。

`task_id`string必填

客户端生成的任务 ID（UUID 格式），用于关联后续事件。

`streaming`string必填

固定为 `duplex`。

`payload`object必填

`task_group`string必填

任务组，固定为 `audio`。

`task`string必填

任务类型，固定为 `asr`。

`function`string必填

功能类型。固定为`recognition`。

`model`string必填

模型名称。

`parameters`object必填

语音识别参数。

`format`string必填

音频格式。

取值范围：

-   `pcm`
-   `wav`
-   `mp3`
-   `opus`
-   `speex`
-   `aac`
-   `amr`

**说明**

-   `opus`/`speex`：必须使用Ogg封装
-   `wav`：必须为PCM编码
-   `amr`：仅支持AMR-NB类型。

`sample_rate`integer必填

采样率（Hz）。

仅支持 `16000` Hz。

`disfluency_removal_enabled`boolean可选

是否过滤语气词并对输出结果进行润色，默认值为 `false`。设置为 `true` 时启用。

`intermediate_result_enabled`boolean可选

是否返回流式中间结果，默认值为 `false`。设置为 `true` 时返回流式中间结果。

`keep_dialect`boolean可选

是否保留方言表达，默认值为 `false`。`false`：将方言转写为普通话文本；`true`：保留方言表达。

**说明**仅在最终结果（`sentence_end=true`）生效，中间结果（`sentence_end=false`）不支持。

`vad_model`string可选

VAD 模型，默认值为 `far_field_meeting_16k`。

-   `near_meeting_16k`：近场场景。
-   `far_field_meeting_16k`：远场场景。

`vocabulary_id`string可选

预编译热词列表 ID。

需预先调用创建热词列表接口生成，识别时传入该 ID 即可使用列表中的热词。

适用于词汇已知且相对稳定、需要跨请求复用同一词表的场景。

使用方法请参见[预编译热词](https://help.aliyun.com/zh/model-studio/improve-asr-accuracy#hw_precompiled_h3)。

`vocabulary`object可选

即时热词。

以键值对形式传入，键为热词文本（`string`），值为热词权重（`integer`），无需预先创建热词列表。权重取值范围为 \[1, 5\] 或 50：取 \[1, 5\] 时值越大模型越倾向输出该词；取 50 时为超级热词，召回率大幅提升，但超级热词数量最多不超过 50 个。

适用于临时性、会话级别的热词优化。

**说明**与预编译热词同时配置时，系统会合并两类热词；合并后超过 2000 个时，随机选择 2000 个使用。使用方法请参见[即时热词](https://help.aliyun.com/zh/model-studio/improve-asr-accuracy#hw_instant_h3)。

`language_hints`array\[string\]可选

待识别音频语种。无默认值，不设置时模型自动识别。

最多支持设置 4 个值，超出时仅前 4 个生效。

点击查看支持的语言代码

-   `zh`: 中文
-   `en`: 英文
-   `ja`: 日语
-   `ko`：韩语
-   `vi`：越南语
-   `th`：泰语
-   `id`：印尼语
-   `ms`：马来语
-   `tl`：菲律宾语
-   `hi`：印地语
-   `ar`：阿拉伯语
-   `fr`：法语
-   `de`：德语
-   `es`：西班牙语
-   `pt`：葡萄牙语
-   `ru`：俄语
-   `it`：意大利语
-   `nl`：荷兰语
-   `sv`：瑞典语
-   `da`：丹麦语
-   `fi`：芬兰语
-   `no`：挪威语
-   `el`：希腊语
-   `pl`：波兰语
-   `cs`：捷克语
-   `hu`：匈牙利语
-   `ro`：罗马尼亚语
-   `bg`：保加利亚语
-   `hr`：克罗地亚语
-   `sk`：斯洛伐克语

**说明**仅在最终结果（`sentence_end=true`）生效，中间结果（`sentence_end=false`）不支持。

`max_sentence_silence`integer可选

VAD 断句静音阈值（ms）。当一段语音后的静音时长超过该阈值时，系统会判定该句子已结束。

默认值：800。

取值范围：\[200, 6000\]。

`heartbeat`boolean可选

是否启用心跳包。

默认值：`false`。

-   `true`：在持续发送静音音频的情况下，可保持与服务端的连接不中断。
-   `false`（默认）：即使持续发送静音音频，连接也将在一定时间后因超时而断开。

静音音频指的是在音频文件或数据流中没有声音信号的内容。静音音频可以通过多种方法生成，例如使用音频编辑软件如Audacity或Adobe Audition，或者通过命令行工具如FFmpeg。

`speech_noise_threshold`float可选

语音与噪音的判定阈值，用于调整语音活动检测（VAD）的灵敏度。

取值范围：\[-1.0, 1.0\]。

取值说明：

-   取值越接近 -1：降低噪音判定阈值，噪音被识别为语音的概率增大，可能导致更多噪音被转写
-   取值越接近 +1：提高噪音判定阈值，语音被误判为噪音的概率增大，可能导致部分语音被过滤

此参数为高级配置参数，调整可能显著影响识别效果，建议：

-   调整前充分测试验证效果
-   根据实际音频环境小幅度调整（建议步长 0.1）

`input`object必填

输入对象。不携带上下文时传入`{}`。

`context`array\[object\]可选

对话上下文，用于辅助识别、提升专有词汇的识别准确率。使用方法详见[上下文增强](https://help.aliyun.com/zh/model-studio/improve-asr-accuracy#ctx_enhance_h2)。

**说明**

-   消息数量：`input_text` 和 `text` 类型的上下文消息各最多 5 条，超出时保留最近的 5 条。
-   文本长度：每轮 `user` 和 `assistant` 的 `text` 字段总长度不超过 400 个字符，每个字符计为 1；超出部分从末尾截断。
-   消息顺序：按对话轮次排列，每轮中 `user`（`input_text` 类型）必须在对应的 `assistant`（`text` 类型）之前。

`role`string必填

消息角色。取值范围：

-   `user`：前几轮用户语音的识别结果或领域相关的词表。
-   `assistant`：前几轮大语言模型的回复内容。

`content`array\[object\]必填

消息内容列表。

`type`string必填

内容类型。取值范围：

-   `input_text`：前几轮用户语音的识别结果或领域相关的词表（`role` 为 `user` 时使用），需同时传入 `text` 字段。
-   `text`：前几轮大语言模型的回复内容（`role` 为 `assistant` 时使用），需同时传入 `text` 字段。

`text`string必填

文本内容。当 `type` 为 `input_text` 时，填入前几轮用户语音的识别结果或领域相关的词表；当 `type` 为 `text` 时，填入前几轮大语言模型的回复内容。

#### 基本请求

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

#### 携带上下文

```
{
  "header": {
    "action": "run-task",
    "task_id": "f9311d98-2146-45b2-b82b-4bf961aef4bc",
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
              "text": "我在祺元项目工作，负责璇枢系统。我的同事叫洛柯。"
            }
          ]
        },
        {
          "role": "assistant",
          "content": [
            {
              "type": "text",
              "text": "好的，我们继续讨论祺元项目、璇枢系统和洛柯的工作。"
            }
          ]
        }
      ]
    },
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
    "task_id": "f9311d98-2146-45b2-b82b-4bf961aef4bc",
    "task_uuid": "5a5f8a374b204e509968596161a6a207",
    "event": "task-started",
    "attributes": {}
  },
  "payload": {}
}
```

#### 即时热词

```
{
  "header": {
    "action": "run-task",
    "task_id": "6dd0acc8-1649-4ba5-a2b3-ee1b543a2b1a",
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
      "vocabulary": {
        "祺元": 4,
        "洛柯": 4,
        "璇枢": 4
      }
    }
  }
}
```
```
{
  "header": {
    "task_id": "6dd0acc8-1649-4ba5-a2b3-ee1b543a2b1a",
    "task_uuid": "3040e76eca9742838822b06d48bcda8a",
    "event": "task-started",
    "attributes": {}
  },
  "payload": {}
}
```

## continue-task

收到 `task-started` 后，客户端可在任务运行期间发送 `continue-task` 事件，更新对话上下文以辅助后续识别。

`header`object必填

`action`string必填

指令类型，固定为 `continue-task`。

`task_id`string必填

客户端生成的任务 ID（UUID 格式），需与[run-task](https://help.aliyun.com/zh/model-studio/qwen-asr-message-client-events#9cae7e7b85ebm)事件中的 `task_id` 保持一致。

`streaming`string必填

固定为 `duplex`。

`payload`object必填

`input`object必填

`context`array\[object\]可选

对话上下文，用于辅助识别、提升专有词汇的识别准确率。使用方法详见[上下文增强](https://help.aliyun.com/zh/model-studio/improve-asr-accuracy#ctx_enhance_h2)。

**说明**

-   消息数量：`input_text` 和 `text` 类型的上下文消息各最多 5 条，超出时保留最近的 5 条。
-   文本长度：每轮 `user` 和 `assistant` 的 `text` 字段总长度不超过 400 个字符，每个字符计为 1；超出部分从末尾截断。
-   消息顺序：按对话轮次排列，每轮中 `user`（`input_text` 类型）必须在对应的 `assistant`（`text` 类型）之前。

`role`string必填

消息角色。取值范围：

-   `user`：前几轮用户语音的识别结果或领域相关的词表。
-   `assistant`：前几轮大语言模型的回复内容。

`content`array\[object\]必填

消息内容列表。

`type`string必填

内容类型。取值范围：

-   `input_text`：前几轮用户语音的识别结果或领域相关的词表（`role` 为 `user` 时使用），需同时传入 `text` 字段。
-   `text`：前几轮大语言模型的回复内容（`role` 为 `assistant` 时使用），需同时传入 `text` 字段。

`text`string必填

文本内容。当 `type` 为 `input_text` 时，填入前几轮用户语音的识别结果或领域相关的词表；当 `type` 为 `text` 时，填入前几轮大语言模型的回复内容。

以下示例先更新上下文，再继续发送音频；返回示例是随后收到的识别结果。

```
{
  "header": {
    "action": "continue-task",
    "task_id": "d3329aa4-1edf-46f7-8991-7f96b83c94ca",
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
              "text": "我在祺元项目工作，负责璇枢系统。我的同事叫洛柯。"
            }
          ]
        },
        {
          "role": "assistant",
          "content": [
            {
              "type": "text",
              "text": "好的，我们继续讨论祺元项目、璇枢系统和洛柯的工作。"
            }
          ]
        }
      ]
    }
  }
}
```
```
{
  "header": {
    "task_id": "d3329aa4-1edf-46f7-8991-7f96b83c94ca",
    "event": "result-generated",
    "attributes": {}
  },
  "payload": {
    "output": {
      "sentence": {
        "sentence_id": 1,
        "begin_time": 160,
        "end_time": 6390,
        "text": "请把祺元项目的报告发给洛柯，下周我们要上线璇枢系统。",
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
            "text": "祺",
            "punctuation": "",
            "fixed": false
          },
          {
            "begin_time": 840,
            "end_time": 1160,
            "text": "元",
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
            "text": "洛",
            "punctuation": "",
            "fixed": false
          },
          {
            "begin_time": 2840,
            "end_time": 3480,
            "text": "柯",
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
            "text": "璇",
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
      "input_tokens": 118,
      "output_tokens": 16,
      "total_tokens": 134
    }
  }
}
```

## finish-task

所有音频数据发送完毕后，客户端发送 `finish-task` 事件，通知服务端音频发送完毕并请求结束任务。

**重要****发送 `finish-task` 后，仍需接收剩余识别结果，直到收到 `task-finished`。** `task_id` 必须与 `run-task` 中的值一致。

`header`object必填

`action`string必填

指令类型，固定为 `finish-task`。

`task_id`string必填

客户端生成的任务 ID（UUID 格式），需与[run-task](https://help.aliyun.com/zh/model-studio/qwen-asr-message-client-events#9cae7e7b85ebm)事件中的 `task_id` 保持一致。

`streaming`string必填

固定为 `duplex`。

`payload`object必填

`input`object必填

固定为`{}`。

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
