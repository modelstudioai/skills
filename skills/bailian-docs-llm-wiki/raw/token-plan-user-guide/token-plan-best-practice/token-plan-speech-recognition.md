# 接入语音识别模型

让 Agent 工具把本地音频或音频 URL 提交给 Token Plan 语音识别模型，返回转写文本。

## 支持的模型

模型

能力

类型

`qwen-audio-3.0-asr-flash`

语音识别

非实时

更多模型以 [个人版](https://help.aliyun.com/zh/model-studio/token-plan-personal-overview#tppo-h-models)和[团队版](https://help.aliyun.com/zh/model-studio/token-plan-team-overview#tpto-h-models)支持的模型 为准。

## 前提

-   已订阅 Token Plan。个人版在 [我的订阅（个人版）](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal) 获取以 `sk-sp-` 开头的 API Key；团队版在 [成员管理](https://bailian.console.aliyun.com/cn-beijing/subscription/uac-admin/organization/members/list) 分配席位后获取 API Key。
-   本地已安装 Python 3.9 及以上版本。
-   音频为公网可访问的 URL，或本地文件。音频时长不超过 5 分钟，支持 `wav`、`mp3`、`opus` 等格式，具体限制见[音频规格](https://help.aliyun.com/zh/model-studio/asr-model#asr_audio_spec02)。

## 接口

`POST https://token-plan.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

请求头使用 `Authorization: Bearer $ANTHROPIC_AUTH_TOKEN`。请求体和响应字段见下文。

## 步骤一：创建 Slash Command

将套餐 API Key（以 `sk-sp-` 为前缀）配置为环境变量 `$ANTHROPIC_AUTH_TOKEN`，供后续脚本鉴权使用。

在项目根目录创建 `.claude/commands/speech-to-text.md`，写入以下内容：

```
调用 Token Plan 语音识别 API，将音频转写为文字。

音频文件或 URL：$ARGUMENTS

## 步骤

1. 确认输入是本地音频路径或公网可访问的 URL。音频时长不超过 5 分钟，格式和大小限制以百炼语音识别文档中的音频规格为准。
2. 安装依赖：pip install requests
3. 使用 Bash 工具执行以下 Python 脚本完成识别。脚本优先读取 TOKEN_PLAN_API_KEY，其次读取 ANTHROPIC_AUTH_TOKEN；不要展示 Key，也不要写入文件或日志。

```python
import base64
import json
import os
import sys
from pathlib import Path

import requests

MIME_TYPES = {
    "aac": "audio/aac",
    "amr": "audio/amr",
    "flac": "audio/flac",
    "m4a": "audio/mp4",
    "mp3": "audio/mpeg",
    "ogg": "audio/ogg",
    "opus": "audio/opus",
    "wav": "audio/wav",
    "webm": "audio/webm",
}

source = sys.argv[1]
key = os.environ.get("TOKEN_PLAN_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN")
if not key:
    raise SystemExit("Token Plan API Key not found.")

if source.startswith(("http://", "https://")):
    audio_data = source
    audio_format = Path(source.split("?")[0]).suffix.lstrip(".").lower() or "mp3"
else:
    path = Path(source)
    audio_format = path.suffix.lstrip(".").lower()
    mime_type = MIME_TYPES.get(audio_format, f"audio/{audio_format}")
    audio_data = f"data:{mime_type};base64,{base64.b64encode(path.read_bytes()).decode()}"

payload = {
    "model": "qwen-audio-3.0-asr-flash",
    "input": {
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "input_audio", "input_audio": {"data": audio_data}}
                ],
            }
        ]
    },
    "parameters": {"format": audio_format},
}

response = requests.post(
    "https://token-plan.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation",
    headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    json=payload,
    timeout=300,
)
if not response.ok:
    raise SystemExit(f"{response.status_code}: {response.text}")
result = response.json()
print(result.get("output", {}).get("text") or json.dumps(result, ensure_ascii=False, indent=2))
```

4. 输出识别文本。需要详细结果时，展示返回 JSON 中的 `output.sentence.text` 和 `output.sentence.words` 字段。
```

## 步骤二：识别音频

在 Claude Code 中输入 `/speech-to-text ./meeting.wav`，或传入音频 URL：`/speech-to-text https://example.com/audio.mp3`。

## 请求要点

参数

说明

`model`

固定为 `qwen-audio-3.0-asr-flash`。

`input.messages[0].content[0].input_audio.data`

音频 URL，或 `data:audio/{format};base64,{data}` 格式的 Base64 Data URI。

`parameters.format`

必填，音频格式，例如 `wav`、`mp3`。

`parameters.sample_rate`

可选，音频采样率，例如 `16000`。

`parameters.language_hints`

可选，待识别语言代码，最多 4 个，例如 `["zh"]`。

完整参数和响应字段见[非实时语音识别（Qwen-Audio-ASR）HTTP API](raw/_short/qwen-audio-asr-http-api-90b9d62787e911f4.md)。

## 返回结果

-   识别文本：`output.text`。
-   句子级结果：`output.sentence.text`、`output.sentence.words`（词级时间戳）。
-   音频时长：`usage.duration`，单位秒。

## 其他工具

其他工具的扩展机制和配置文件路径，参见[接入概览](https://help.aliyun.com/zh/model-studio/token-plan-integration-overview#tp-ext-tools)中的“工具配置路径”。

## 限制

-   Token Plan 当前提供非实时语音识别模型 `qwen-audio-3.0-asr-flash`。
-   单次音频时长不超过 5 分钟，文件大小和格式以[音频规格](https://help.aliyun.com/zh/model-studio/asr-model#asr_audio_spec02)为准。
-   语音识别使用 DashScope 协议接口，Endpoint 为 `https://token-plan.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`。
