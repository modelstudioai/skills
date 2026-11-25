# 音频打标 HTTP API

提交录音文件，异步获取按时间标注的语音、音效和背景声，以及整段录音的场景描述。

> **说明**
>
> 示例使用华北2（北京）地域。将 `WORKSPACE_ID` 设为[业务空间 ID](https://bailian.console.aliyun.com/cn-beijing/settings/workspace)，将 `DASHSCOPE_API_KEY` 设为该地域的 [API Key](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key)。

<a id="提交任务"></a>

<a id="submit-task"></a>

## 提交任务

提交一个音频或视频文件，创建异步标注任务。

POST`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/asr/transcription`

<a id="请求头"></a>

### 请求头

`Authorization`string必填

`Bearer $DASHSCOPE_API_KEY`。

`Content-Type`string必填

`application/json`

`X-DashScope-Async`string必填

固定为 `enable`，以异步方式处理文件。

<a id="请求体"></a>

### 请求体

`model`string必填

音频标注模型 ID，例如 `qwen-audio-3.1-captioner`。

`input`object必填

`file_url`string必填

单个音频或视频文件的 HTTP(S) 下载地址。

`parameters`object可选

`channel_id`array\[integer\]可选

要处理的声道编号，从 0 开始。单声道文件可传 `[0]`；处理多声道时传入多个编号。

<a id="返回参数"></a>

### 返回参数

`output`object

`task_id`string

服务端生成的任务 ID。保存此值，用于查询任务。

`task_status`string

任务状态。

`request_id`string

本次请求的 ID，用于排查错误。

<a id="code-block"></a>

```bash
curl --request POST "https://${WORKSPACE_ID}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/asr/transcription" \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --header "X-DashScope-Async: enable" \
  --data '{
    "model": "qwen-audio-3.1-captioner",
    "input": {
      "file_url": "https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/audios/6a4b3c2d1e0f9093.wav"
    },
    "parameters": {"channel_id": [0]}
  }'
```

<a id="code-block-2"></a>

```json
{
  "output": {
    "task_id": "12345678-abcd-4abc-8123-123456789abc",
    "task_status": "PENDING"
  },
  "request_id": "01234567-abcd-4abc-8234-123456789abc"
}
```

<a id="查询任务"></a>

<a id="query-task"></a>

## 查询任务

根据任务 ID 查询处理状态。任务成功后，响应中包含标注结果的下载地址。

GET`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

<a id="路径参数"></a>

### 路径参数

`task_id`string必填

提交时返回的任务 ID。

<a id="返回参数-2"></a>

### 返回参数

`request_id`string

本次请求的 ID，用于排查错误。

`output`object

`task_id`string

服务端生成的任务 ID。保存此值，用于查询任务。

`task_status`string

任务状态：

-   `PENDING`：排队中，稍后再查询。
-   `RUNNING`：处理中，稍后再查询。
-   `SUCCEEDED`：任务成功，检查文件状态并下载结果。
-   `FAILED`：任务失败。
-   `CANCELED`：任务已取消。

`submit_time`string

提交任务的时间。

`scheduled_time`string

任务开始调度的时间。

`end_time`string

任务结束的时间。

`file_url`string

提交的文件地址。

`subtask_status`string

文件处理状态。`SUCCEEDED` 表示该文件已生成标注结果。

`transcription_url`string

成功后返回的结果文件下载地址，有效期为 24 小时。使用完整 URL 下载，包括查询字符串。

<a id="code-block-3"></a>

```bash
curl "https://${WORKSPACE_ID}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/${TASK_ID}" \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

<a id="code-block-4"></a>

```json
{
  "request_id": "01234567-abcd-4abc-8234-123456789abc",
  "output": {
    "task_id": "12345678-abcd-4abc-8123-123456789abc",
    "task_status": "SUCCEEDED",
    "submit_time": "2026-11-23 11:00:00.000",
    "scheduled_time": "2026-11-23 11:00:01.000",
    "end_time": "2026-11-23 11:00:08.000",
    "file_url": "https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/audios/6a4b3c2d1e0f9093.wav",
    "subtask_status": "SUCCEEDED",
    "transcription_url": "https://example.com/result.json?signature=..."
  }
}
```

<a id="下载并解析结果"></a>

<a id="download-result"></a>

## 下载并解析结果

任务成功后，可下载各声道的标注结果文件。文件包含原始音频属性、分段标注和 Token 用量。

<a id="结果文件"></a>

### 结果文件

`file_url`string

输入文件的地址。

`properties`object

输入音频的属性。

`audio_format`string

音频编码格式，例如 `pcm_s16le`。

`channels`array\[integer\]

声道编号列表。

`original_sampling_rate`integer

原始音频采样率，单位为 Hz。

`original_duration_in_milliseconds`integer

原始音频时长，单位为毫秒。

`transcripts`array\[object\]

每个元素对应一个声道。

`channel_id`integer

声道编号。

`content_duration_in_milliseconds`integer

该声道的标注时长，单位为毫秒。

`text`string

包含该声道标注结果的 JSON 字符串。

`sentences`array\[object\]

该声道的分段标注。

`begin_time`integer

片段起始位置，单位为毫秒。

`end_time`integer

片段结束位置，单位为毫秒。

`text`string

该片段的标注文本。

`speaker_id`integer

说话人编号（如返回）。

`usage`object

本次任务的 Token 用量。

`input_tokens`integer

输入 Token 数。

`output_tokens`integer

输出 Token 数。

`total_tokens`integer

输入和输出 Token 总数。

<a id="标注内容"></a>

### 标注内容

解析结果文件中的 `transcripts[].text` 后，可读取以下字段。

`sound_segments`array\[object\]

音效和声音事件。

`start_time`string

相对于当前音频片段起点的开始时间，格式为 `MM:SS.cc`（分:秒.百分秒）。跨段时可以为负值。

`end_time`string

相对于当前片段起点的结束时间，格式为 `MM:SS.cc`。

`tag`array\[string\]

声音事件标签。

`description`string

声音描述，无描述时为空字符串。

`speech_segments`array\[object\]

人声片段。

`start`string

相对于当前音频片段起点的开始时间，格式为 `MM:SS.cc`（分:秒.百分秒）。跨段时可以为负值。

`end`string

相对于当前片段起点的结束时间，格式为 `MM:SS.cc`。

`language`array\[string\]

语种及口音标签，无人声时为空列表。

`text`string

转写文本，可包含说话人、语气和句内声音事件的标注。

`para`object

片段的表达方式和说话人信息。

`speech_mode`string

表达方式。取值：

-   `唱歌`
-   `说唱`
-   `朗诵`
-   `播报`
-   `解说`
-   `讲解`
-   `演讲`
-   `讲故事`
-   `访谈`
-   `闲聊`
-   `独白`
-   `无人声`

`speed`string

语速。无人声时为空字符串。其他取值：

-   `极慢`
-   `偏慢`
-   `中速`
-   `偏快`
-   `极快`
-   `短促`

`volume`string

音量。无人声时为空字符串。其他取值：

-   `轻声`
-   `中等`
-   `偏大`
-   `高亢`

`intonation`string

描述语调、重音、情绪及其变化。

`speaker`array\[string\]

片段中的说话人角色。

`speaker_index`array\[string\]

片段中的说话人编号，用于关联整段录音的说话人信息。

`background_segments`array\[object\]

背景音乐、持续的环境声或安静时段。

`start_time`string

相对于当前音频片段起点的开始时间，格式为 `MM:SS.cc`（分:秒.百分秒）。跨段时可以为负值。

`end_time`string

相对于当前片段起点的结束时间，格式为 `MM:SS.cc`。

`description`array\[string\]

背景声描述。

`speech_globals`object

整段录音的说话人信息。

`speakers`array\[object\]

按说话人汇总的描述。

`speaker_index`string

说话人编号，例如 `SPK_0`。

`role`string

说话人的角色描述。

`gender`string

对声音性别特征的描述。

`age`string

听感上的年龄段。

`name`string

可识别时返回的姓名。

`description`string

对说话人的综合描述。

`voice`object

声音特征。

`nature`array\[string\]

声音气质标签。

`texture`array\[string\]

音色质感标签。

`global`object

整段录音的场景与情绪描述。

`scene`object

整体场景。

`description`string

场景描述。

`format`array\[string\]

内容形式。

`topic`array\[string\]

内容主题。

`style`array\[string\]

风格标签。

`emotion`object

情绪及变化。

`overall`array\[string\]

整体情绪标签。

`flow`array\[array\[string\]\]

情绪变化阶段。每项依次包含阶段标题和变化描述。

<a id="code-block-5"></a>

```bash
curl --fail "$TRANSCRIPTION_URL" -o annotation.json
```

<a id="code-block-6"></a>

```python
import json

with open("annotation.json", encoding="utf-8") as f:
    result = json.load(f)

for channel in result["transcripts"]:
    annotation = json.loads(channel["text"])
    for segment in annotation["speech_segments"]:
        print(channel["channel_id"], segment["start"], segment["end"], segment["text"])
    for segment in annotation["background_segments"]:
        print(segment["start_time"], segment["end_time"], segment["description"])
```

<a id="code-block-7"></a>

```json
{
  "sound_segments": [
    {
      "start_time": "00:00.00",
      "end_time": "00:06.08",
      "tag": [
        "合成语音"
      ],
      "description": "吐字清晰，全程音量稳定。"
    }
  ],
  "speech_segments": [
    {
      "start": "00:00.00",
      "end": "00:06.08",
      "language": [
        "中文-普通话"
      ],
      "text": "[说话人:职场女职员]请把七元项目的报告发给罗科，下周我们要上线玄书系统。",
      "para": {
        "speech_mode": "播报",
        "speed": "中速",
        "volume": "中等",
        "intonation": "语气正式平稳",
        "speaker": [
          "职场女职员"
        ],
        "speaker_index": [
          "SPK_0"
        ]
      }
    }
  ],
  "background_segments": [
    {
      "start_time": "00:00.00",
      "end_time": "00:06.08",
      "description": [
        "背景环境安静"
      ]
    }
  ],
  "speech_globals": {
    "speakers": [
      {
        "speaker_index": "SPK_0",
        "role": "职场女职员",
        "description": "声音清亮，语速平稳。",
        "voice": {
          "nature": [
            "干练",
            "正式"
          ],
          "texture": [
            "清亮"
          ]
        }
      }
    ]
  },
  "global": {
    "scene": {
      "description": "说话人正在交代工作安排。",
      "format": [
        "工作指令传达"
      ],
      "topic": [
        "项目工作安排",
        "系统上线筹备"
      ],
      "style": [
        "正式商务"
      ]
    },
    "emotion": {
      "overall": [
        "中性正式"
      ],
      "flow": [
        [
          "指令传达",
          "语调平稳。"
        ]
      ]
    }
  }
}
```
