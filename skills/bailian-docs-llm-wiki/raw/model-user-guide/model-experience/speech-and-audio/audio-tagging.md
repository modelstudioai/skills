# 音频打标

对录制好的音频或视频文件进行异步打标，获取带时间信息的语音、音效、背景声及整段录音的场景描述。

<a id="功能介绍"></a>

## 功能介绍

-   **全信息音频转写与摘要**：支持对输入音频中的语音内容、说话人信息，时间戳，环境声、音效、背景音乐等多维信息进行全要素提取与语义转写，并能自动生成结构化的音频内容摘要。
-   **声学场景深度分析**：支持对环境音效、背景噪音类型及空间声学特征进行分类与识别，为声学场景理解与音频监控提供精准沉淀。
-   **复杂场景音轨分离**：专为多人对话及重叠声学环境优化，能够精准提取并分离不同说话人语音以及背景音频要素，显著提升复杂音频场景下的解析质量。
-   **高效音频剪辑与标注**：能够输出毫秒级的时间戳与多轨标记，方便后续音频自动化剪辑、轴线对齐以及大规模数据集的自动化标注与处理。

<a id="开始使用"></a>

## 开始使用

以下示例以华北2（北京）为例。在百炼控制台[获取 API Key](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key)，将其设为环境变量 `DASHSCOPE_API_KEY` 的值，并将示例中的 `{WorkspaceId}` 替换为同一地域的[业务空间 ID](https://bailian.console.aliyun.com/cn-beijing/settings/workspace)。

以下 Python 示例提交一段普通话录音，等待任务完成后，下载并解析各声道的标注结果。

<a id="code-block"></a>

```python
import json
import os
import time
from urllib.request import Request, urlopen

base_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
auth = {"Authorization": "Bearer " + os.environ["DASHSCOPE_API_KEY"]}
body = {
    "model": "qwen-audio-3.1-captioner",
    "input": {"file_url": "https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/audios/6a4b3c2d1e0f9093.wav"},
    "parameters": {"channel_id": [0]},
}
request = Request(
    base_url + "/services/audio/asr/transcription",
    data=json.dumps(body).encode(),
    headers={**auth, "Content-Type": "application/json", "X-DashScope-Async": "enable"},
)
with urlopen(request, timeout=30) as response:
    task_id = json.load(response)["output"]["task_id"]

while True:
    with urlopen(Request(f"{base_url}/tasks/{task_id}", headers=auth), timeout=30) as response:
        output = json.load(response)["output"]
    if output["task_status"] not in ("PENDING", "RUNNING"):
        break
    time.sleep(3)

if output["task_status"] != "SUCCEEDED" or output.get("subtask_status") != "SUCCEEDED":
    raise RuntimeError(output.get("message") or output)
with urlopen(output["transcription_url"], timeout=30) as response:
    result = json.load(response)
for channel in result["transcripts"]:
    annotations = json.loads(channel["text"])
    print(json.dumps(annotations, ensure_ascii=False, indent=2))
```

示例按声道输出标注结果，包括语音及其时间位置、音效和背景声，以及整段录音的场景描述。

<a id="输入要求"></a>

## 输入要求

-   输入方式：每次提交一个公网可直接下载的音频或视频文件 URL。
-   文件大小与时长：不超过 2 GB，时长不超过 5 分钟。
-   音频和视频格式：`aac`、`amr`、`avi`、`flac`、`flv`、`m4a`、`mkv`、`mov`、`mp3`、`mp4`、`mpeg`、`ogg`、`opus`、`wav`、`webm`、`wma`、`wmv`。
-   采样率：不低于 8 kHz。
-   语种：中文、英语、日语、韩语、法语、德语、西班牙语。

<a id="支持的模型"></a>

## 支持的模型

<a id="sec-tabs"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

-   **Qwen-Audio-3.1-Captioner：**qwen-audio-3.1-captioner

<a id="api-参考"></a>

## API 参考

-   [音频打标 HTTP API](../../../model-api-reference/audio-api-directory/qwen-audio-asr-captioner-http-api.md)
