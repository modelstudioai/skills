# CosyVoice客户端事件

CosyVoice 客户端事件参考，介绍 run-task、continue-task、finish-task 的字段、发送顺序及对应服务端事件。

## 事件交互流程

1.  发送 [run-task](https://help.aliyun.com/zh/model-studio/cosyvoice-client-events#run-task) 启动并配置任务，等待 [task-started](https://help.aliyun.com/zh/model-studio/cosyvoice-server-events#task-started)。
2.  收到 `task-started` 后，通过 [continue-task](https://help.aliyun.com/zh/model-studio/cosyvoice-client-events#continue-task) 发送文本，同时接收 [result-generated](https://help.aliyun.com/zh/model-studio/cosyvoice-server-events#result-generated) 和合成音频。
3.  文本全部发送完毕后，发送 [finish-task](https://help.aliyun.com/zh/model-studio/cosyvoice-client-events#finish-task)，继续接收剩余结果和音频，直到收到 [task-finished](https://help.aliyun.com/zh/model-studio/cosyvoice-server-events#task-finished)；任务失败时返回 [task-failed](https://help.aliyun.com/zh/model-studio/cosyvoice-server-events#task-failed)。

`result-generated` 返回句子元信息，音频数据通过独立通道传输：WebSocket 使用二进制帧，AOQ 使用 Audio Track。连接、鉴权和音频传输方式请参见 [WebSocket API](raw/_short/cosyvoice-websocket-api-5929268331632771.md) 或 [AOQ 接入](raw/_short/cosyvoice-aoq-access-c0e8e4035486f433.md)。

## run-task

建立连接后，客户端立即发送 `run-task` 事件，启动语音合成任务并设置模型、音色、采样率等参数。

**重要****收到 `task-started` 后才能发送 `continue-task`。** `run-task` 只用于启动和配置任务，待合成文本通过 `continue-task` 发送。

`header`object必填

`action`string必填

指令类型，固定为 `run-task`。

`task_id`string必填

客户端生成的任务 ID（UUID 格式），用于关联后续事件。和后续 `continue-task`、`finish-task` 中的 `task_id` 保持一致。

`streaming`string必填

固定为 `duplex`

`payload`object必填

`task_group`string必填

任务组，固定为 `audio`。

`task`string必填

任务类型，固定为 `tts`。

`function`string必填

功能类型，固定为 `SpeechSynthesizer`。

`model`string必填

模型名称。

`parameters`object必填

语音合成参数。

`text_type`string必填

固定为 `PlainText`。

`voice`string必填

语音合成所使用的音色。

-   **系统音色**：参见[CosyVoice音色列表](raw/model-user-guide/model-experience/speech-and-audio/speech-synthesis/tts-voice-list/cosyvoice-voice-list.md)
-   **复刻音色**：通过音色复刻功能定制
-   **音色设计音色**：通过音色设计功能定制

`format`string可选

音频编码格式。

取值范围：

-   `pcm`
-   `wav`
-   `mp3`（默认）
-   `opus`

`sample_rate`integer可选

音频采样率（Hz）。

取值范围：8000, 16000, 22050（默认）, 24000, 44100, 48000。

`volume`integer可选

音量。

默认值：50。

取值范围：\[0, 100\]。

`rate`float可选

语速。

默认值：1.0。

取值范围：\[0.5, 2.0\]。

`pitch`float可选

音调。

默认值：1.0。

取值范围：\[0.5, 2.0\]。

`bit_rate`integer可选

音频码率（kbps）。音频格式为`mp3`或`opus`时，支持通过`bit_rate`参数调整码率。

默认值：32。

取值范围：\[6, 510\]。

`enable_ssml`boolean可选

是否开启 SSML 功能。

默认值：`false`。

**说明**设为 `true` 后，仅允许发送一次 `continue-task` 指令。

SSML 的使用限制（支持的模型、音色和接口），请参见[使用限制](https://help.aliyun.com/zh/model-studio/ssml-latex-user-guide#sl01_constraint_h3)。

`word_timestamp_enabled`boolean可选

是否开启字级别时间戳。

默认值：`false`。

**说明**仅在流式输出模式下可用。支持的音色范围：cosyvoice-v3.5-plus、cosyvoice-v3.5-flash、cosyvoice-v3-flash、cosyvoice-v3-plus、cosyvoice-v2模型的复刻音色，以及[CosyVoice音色列表](raw/model-user-guide/model-experience/speech-and-audio/speech-synthesis/tts-voice-list/cosyvoice-voice-list.md)中标记为支持的系统音色。其他模型的复刻音色不支持此功能。

`seed`integer可选

生成时使用的随机数种子，使合成的效果产生变化。在模型版本、文本、音色及其他参数均相同的前提下，使用相同的seed可复现相同的合成结果。

默认值0。

取值范围：\[0, 65535\]。

`language_hints`array\[string\]可选

**说明**

-   此参数为数组，但当前版本仅处理第一个元素，因此建议只传入一个值。
-   此参数用于指定语音合成的目标语言，该设置与音色复刻时的样本音频的语种无关。如需设置复刻任务的源语言，请参见[音色复刻API参考](https://help.aliyun.com/zh/model-studio/voice-clone-design-http-api#h2-create)。

指定语音合成的目标语言，提升合成效果。

当数字、缩写、符号等朗读方式或者小语种合成效果不符合预期时使用，例如：

-   数字朗读方式不符合预期，“hello, this is 110”读成“hello, this is one one zero”而非“hello, this is 幺幺零”
-   符号朗读不准确，“@”读成“艾特”而非“at”
-   小语种合成效果差，合成不自然

取值范围

-   `zh`：中文
-   `en`：英语
-   `fr`：法语
-   `de`：德语
-   `ja`：日语
-   `ko`：韩语
-   `ru`：俄语
-   `pt`：葡萄牙语
-   `th`：泰语
-   `id`：印尼语
-   `vi`：越南语
-   `es`：西班牙语
-   `it`：意大利语
-   `ms`：马来西亚语
-   `fil`：菲律宾语
-   `ar`：阿拉伯语

`instruction`string可选

设置指令，用于控制方言、情感或角色等合成效果。具体使用说明请参见[指令控制](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#12884a10929p9)。

`enable_aigc_tag`boolean可选

是否在生成的音频中添加AIGC隐性标识。设置为`true`时，会将隐性标识嵌入到支持格式（`wav`/`mp3`/`opus`）的音频中。

默认值：`false`。

**说明**仅cosyvoice-v3-flash、cosyvoice-v3-plus、cosyvoice-v2支持该功能。

`aigc_propagator`string可选

设置AIGC隐性标识中的 `ContentPropagator` 字段，用于标识内容的传播者。仅在 `enable_aigc_tag` 为 `true` 时生效。

默认值：阿里云UID。

**说明**仅cosyvoice-v3-flash、cosyvoice-v3-plus、cosyvoice-v2支持该功能。

`aigc_propagate_id`string可选

设置AIGC隐性标识中的 `PropagateID` 字段，用于唯一标识一次具体的传播行为。仅在 `enable_aigc_tag` 为 `true` 时生效。

默认值：本次语音合成请求Request ID。

**说明**仅cosyvoice-v3-flash、cosyvoice-v3-plus、cosyvoice-v2支持该功能。

`enable_markdown_filter`boolean可选

**说明**cosyvoice-v2 不支持此功能。

是否启用 Markdown 过滤。启用后，服务会在合成前将 Markdown 转换成适合朗读的文本。

默认值：`false`。

取值范围：

-   `true`：启用Markdown过滤
-   `false`：禁用Markdown过滤

`input`object必填

输入数据：固定为空对象 `{}`，待合成文本通过 `continue-task` 指令发送。

```
{
  "header": {
    "action": "run-task",
    "task_id": "24a2157d-7eb1-4e8e-958f-5af8acfa8929",
    "streaming": "duplex"
  },
  "payload": {
    "input": {},
    "task_group": "audio",
    "task": "tts",
    "function": "SpeechSynthesizer",
    "model": "cosyvoice-v3-plus",
    "parameters": {
      "text_type": "PlainText",
      "voice": "longanyang",
      "format": "mp3",
      "sample_rate": 22050
    }
  }
}
```
```
{
  "header": {
    "task_id": "24a2157d-7eb1-4e8e-958f-5af8acfa8929",
    "task_uuid": "477a77e06a26427eb9745a4f1b1366dc",
    "event": "task-started",
    "attributes": {}
  },
  "payload": {}
}
```

## continue-task

收到 `task-started` 后，客户端发送 `continue-task` 事件提交待合成文本。文本可一次性发送，也可分段按顺序发送。

`header`object必填

`action`string必填

指令类型，固定为 `continue-task`。

`task_id`string必填

任务 ID（UUID 格式），需要和 `run-task` 中的 `task_id` 保持一致。

`streaming`string必填

固定为 `duplex`。

`payload`object必填

`input`object必填

包含待合成文本。

`text`string必填

待合成文本。单次最多 20000 字符，累计最多 200000 字符。

**说明**发送间隔不得超过 23 秒，否则连接超时。

```
{
  "header": {
    "action": "continue-task",
    "task_id": "24a2157d-7eb1-4e8e-958f-5af8acfa8929",
    "streaming": "duplex"
  },
  "payload": {
    "input": {
      "text": "你好，欢迎使用语音合成。"
    }
  }
}
```
```
{
  "header": {
    "task_id": "24a2157d-7eb1-4e8e-958f-5af8acfa8929",
    "event": "result-generated",
    "attributes": {
      "x-dashscope-inner-response-type": "ws"
    }
  },
  "payload": {
    "output": {
      "sentence": {
        "index": 0,
        "words": []
      },
      "type": "sentence-begin",
      "original_text": "你好，欢迎使用语音合成。",
      "normalized_text": "你好，欢迎使用语音合成。"
    }
  }
}
```

## finish-task

所有文本发送完毕后，客户端立即发送 `finish-task` 事件，通知服务端文本发送完毕并请求结束任务。如需取消当前轮次的合成，可在 `input` 中将 `directive` 设为 `cancel`。

**重要****发送 `finish-task` 后，仍需接收剩余合成结果和音频，直到收到 `task-finished`。** 取消任务时，服务端停止输出后续音频并返回 `task-finished`。

`header`object必填

`action`string必填

指令类型，固定为 `finish-task`。

`task_id`string必填

任务 ID（UUID 格式），需要和 `run-task` 中的 `task_id` 保持一致。

`streaming`string必填

固定为 `duplex`

`payload`object必填

`input`object必填

任务输入。为空对象 `{}` 时表示正常结束任务；包含 `directive` 时可用于取消当前轮次的语音合成任务。

`directive`string可选

控制任务结束行为。当前仅支持取值为 `cancel`，表示取消当前轮次的语音合成任务，服务端会立即返回 `task-finished` 事件，且不会输出后续音频。

取消后，可在当前 WebSocket 连接上重新发起语音合成任务（发送新的 `run-task` 事件），无需重新建立连接。

#### 正常结束

```
{
  "header": {
    "action": "finish-task",
    "task_id": "24a2157d-7eb1-4e8e-958f-5af8acfa8929",
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
    "task_id": "24a2157d-7eb1-4e8e-958f-5af8acfa8929",
    "event": "task-finished",
    "attributes": {
      "x-dashscope-inner-response-type": "ws"
    }
  },
  "payload": {
    "output": {},
    "usage": {
      "characters": 22
    }
  }
}
```

#### 取消任务

```
{
  "header": {
    "action": "finish-task",
    "task_id": "701d0875-20f8-4d39-8e50-ee5be2f0e364",
    "streaming": "duplex"
  },
  "payload": {
    "input": {
      "directive": "cancel"
    }
  }
}
```
```
{
  "header": {
    "task_id": "701d0875-20f8-4d39-8e50-ee5be2f0e364",
    "event": "task-finished",
    "attributes": {
      "x-dashscope-inner-response-type": "ws"
    }
  },
  "payload": {
    "output": {}
  }
}
```
