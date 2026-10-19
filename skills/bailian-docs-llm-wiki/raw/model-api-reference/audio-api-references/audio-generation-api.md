# 音频生成 API参考

使用 HTTPS 接口提交文本提示词和参考音频，获取生成的音频文件。本文说明请求参数、响应结构和错误处理。

## 接入前准备

获取 [API Key](raw/model-api-reference/preparations/get-api-key.md) 和[业务空间 ID](raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)，分别配置为环境变量 `DASHSCOPE_API_KEY` 和 `SFM_WORKSPACE_ID`。

请求方法为 HTTPS POST，端点如下，其中 `{WorkspaceId}` 为业务空间 ID：

```
https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/SpeechSynthesizer
```

### 请求头

字段

必填

说明

Authorization

是

`Bearer <API Key>`

Content-Type

是

`application/json`

## 调用示例

```
curl --request POST \
  "https://$SFM_WORKSPACE_ID.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/SpeechSynthesizer" \
  --max-time 300 \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "qwen-audio-3.1-tts-next",
    "input": {
      "text_prompt": "一位女性清晰地说：“你好，欢迎使用。”",
      "format": "wav",
      "sample_rate": 48000,
      "channels": 2
    }
  }'
```

响应示例（ID 和下载地址已替换为示意值）：

```
{
  "request_id": "example-request-id",
  "output": {
    "finish_reason": "stop",
    "audio": {
      "data": "",
      "url": "https://example.com/generated.wav",
      "id": "audio_example-request-id",
      "expires_at": 1789616932,
      "duration": 1.12
    }
  },
  "usage": {
    "duration": 1
  }
}
```

使用实际响应中的 `output.audio.url` 下载文件，URL 有效期为 24 小时。不要使用上述示意地址下载。

## 请求参数

`model` 位于请求体顶层，其余生成参数位于 `input` 对象内。

字段

类型

必填

默认值

说明

model

string

是

—

模型 ID，见支持的模型。

input

object

是

—

音频生成输入。

input.text\_prompt

string

是

—

音频描述或待合成文本。参考音频按顺序使用 `@voice1`、`@voice2`、`@voice3` 引用。长度上限见模型表。

input.references

array

否

—

参考音频列表。不传时仅使用文本生成。当前模型最多支持 3 条，每条最长 30 秒、不超过 10 MB。

input.references\[\].audio\_url

string

条件必填

—

服务端可访问的公网音频 URL，与 `audio_data` 二选一。

input.references\[\].audio\_data

string

条件必填

—

音频 data URI：`data:{mime_type};base64,{base64_encoded_data}`。与 `audio_url` 二选一。

input.format

string

否

wav

输出格式：`wav`、`mp3`、`pcm`。不支持 Opus 输出。

input.sample\_rate

integer

否

48000

输出采样率，单位 Hz：8000、16000、24000、44100、48000。

input.channels

integer

否

2

声道数：1（单声道）、2（双声道）。

input.volume

integer

否

50

音量，取值范围 \[0, 100\]。

input.enable\_cbr

boolean

否

false

仅 MP3 生效。true 为恒定码率（CBR），false 为可变码率（VBR）。

input.bit\_rate

integer

否

128

仅 MP3 CBR 生效，单位 kbps。实际输出受采样率及 MP3 编码档位约束，见下表。

input.quality

integer

否

5

仅 MP3 VBR 生效。取值范围 \[0, 9\]，0 为最高质量。

input.rate

float

否

1.0

语速，取值范围 \[0.5, 2.0\]。

input.seed

integer

否

42

请求级别随机种子。

input.enable\_aigc\_tag

boolean

否

false

是否在生成音频中添加 AIGC 标识水印。

参考音频支持 WAV、MP3 和 OGG Opus，不支持裸 PCM。参考音频格式与输出格式是两套限制：可以输入 OGG Opus，但不能输出 Opus。

参考音频须通过 URL 或 Base64 提交，不支持使用系统音色或声音复刻音色 ID。

### MP3 CBR 码率

采样率（Hz）

输出码率下限（kbps）

输出码率上限（kbps）

8000

8

64

16000、24000

8

160

44100、48000

32

320

码率由采样率和 MP3 编码档位共同决定。表中为输出码率范围，不表示支持区间内的任意整数；超出范围的指定值会被限制在对应范围内。

## 提交参考音频

以下 Python 示例使用两条参考音频生成双人对话。先安装 `requests`，准备分别包含两位说话人声音、符合模型限制的 `reference1.wav` 和 `reference2.wav`，并配置前述环境变量。

`references` 按列表顺序分配槽位：第一项 `reference1.wav` 对应 `@voice1`，第二项 `reference2.wav` 对应 `@voice2`。示例将两条音频分别编码为 Base64，并在提示词中引用对应说话人。

```
import base64
import os
from pathlib import Path

import requests

reference1 = base64.b64encode(Path("reference1.wav").read_bytes()).decode("ascii")
reference2 = base64.b64encode(Path("reference2.wav").read_bytes()).decode("ascii")
workspace_id = os.environ["SFM_WORKSPACE_ID"]
endpoint = (
    f"https://{workspace_id}.cn-beijing.maas.aliyuncs.com"
    "/api/v1/services/audio/tts/SpeechSynthesizer"
)
response = requests.post(
    endpoint,
    headers={
        "Authorization": f"Bearer {os.environ['DASHSCOPE_API_KEY']}",
        "Content-Type": "application/json",
    },
    json={
        "model": "qwen-audio-3.1-tts-next",
        "input": {
            "text_prompt": "@voice1 说：“今天阳光很好，一起去散步吧。”@voice2 回答：“好啊，我们去公园。”",
            "references": [
                {"audio_data": f"data:audio/wav;base64,{reference1}"},
                {"audio_data": f"data:audio/wav;base64,{reference2}"}
            ],
            "format": "wav",
        },
    },
    timeout=300,
)
response.raise_for_status()
result = response.json()
audio_response = requests.get(result["output"]["audio"]["url"], timeout=60)
audio_response.raise_for_status()
Path("output.wav").write_bytes(audio_response.content)
```

使用 URL 时，将列表元素替换为 `{"audio_url": "可公开访问的音频URL"}`，不要同时填写 `audio_data`。多人参考按列表顺序编号，不能引用不存在的编号。

## 响应参数

字段

类型

说明

request\_id

string

请求 ID，用于问题排查。

output.finish\_reason

string

正常结束时为 "stop"。

output.audio.data

string

此调用方式下为空字符串；通过 output.audio.url 下载完整音频。

output.audio.url

string

完整音频文件的下载 URL，有效期 24 小时。

output.audio.id

string

生成音频的 ID。

output.audio.expires\_at

integer

下载 URL 的过期时间戳。

output.audio.duration

float

生成音频的时长，单位秒。

usage.duration

integer

本次生成音频的时长，按秒四舍五入。此字段不用于计算 Token 费用。

播客场景单次最多生成 240 秒（4 分钟）音频，其他场景单次最多生成 120 秒。单价请参见[模型调用计费](https://help.aliyun.com/zh/model-studio/model-pricing#audio-generation-pricing)。

## 支持的模型

模型 ID

Prompt 上限

单次生成时长上限

[qwen-audio-3.1-tts-next](raw/model-user-guide/support/model-studio-model-list/model-list-audio-generation/qwen-audio-3-1-tts-next.md)

3000 字符

播客：240 秒（4 分钟）；其他场景：120 秒

场景、试听与提示词写法请参见[音频生成](raw/model-user-guide/model-experience/audio-generation.md)。本文示例使用表中的模型。

## 错误处理

错误响应示例：

```
{
  "request_id": "example-request-id",
  "code": "CLIENT_ERROR",
  "message": "text_prompt exceeds the maximum length of 3000 characters."
}
```

HTTP 状态码

code

处理方式

400

CLIENT\_ERROR

检查 Prompt 长度、参考音频数量与时长、URL/Base64 互斥关系、引用编号，以及是否使用了不支持的 voice 字段。

404

InvalidParameter

若 message 为 "Model not exist."，核对模型 ID、地域及当前账号可用范围。

401

InvalidApiKey

核对 API Key 是否有效。

403

AccessDenied

检查模型调用权限。

429

Throttling.RateQuota

降低请求频率。

400

DataInspectionFailed

检查文本或参考音频是否符合内容安全要求。

500

InternalError

保留 request\_id，稍后重试或联系技术支持。
