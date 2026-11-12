# 非实时语音识别

了解非实时语音识别的模型特性、音频文件调用方式和识别效果优化方法。

## 功能介绍

非实时语音识别将已录制的音视频文件转换为文本，适用于会议转写、通话分析和字幕生成等场景。短音频可在一次请求中获取结果，长音频可提交异步任务处理。

-   **多语言与方言**：支持自动语种检测，识别多种语言及中文方言，具体范围参见[语音识别概述](https://help.aliyun.com/zh/model-studio/asr-model#asr_all02)。
-   **准确率优化**：通过热词辅助识别人名、品牌名等特定词汇，或通过上下文补充对话信息。
-   **文本处理**：支持文本润色、保留方言表达和敏感词过滤。
-   **说话人分离**：为不同说话人的转写结果标注编号，便于整理多人会议和访谈记录。
-   **结构化结果**：返回句子、字词及其时间戳，用于字幕生成、关键词高亮和音频定位。
-   **音频输入**：支持多种音视频格式，可按模型支持范围选择采样率和声道。
-   **长音频转写**：支持单个时长不超过 12 小时、大小不超过 2 GB 的音视频文件异步转写。

**说明**各模型支持的能力有所不同，请核对对应功能的适用范围。需要持续输入音频并边说边返回结果时，参见[实时语音识别](raw/model-user-guide/model-experience/speech-and-audio/speech-recognition/real-time-speech-recognition-user-guide.md)。

**使用场景**

**推荐模型**

**调用方式**

5 分钟以内的短音频，需要直接获取结果

[qwen-audio-3.1-asr-flash](https://bailian.console.aliyun.com/cn-beijing/model/market/detail/qwen-audio-3.1-asr-flash)

同步调用，可选择 SSE 流式输出。

长录音，或需要异步处理的音视频文件

[qwen-audio-3.1-asr-flash-filetrans](https://bailian.console.aliyun.com/cn-beijing/model/market/detail/qwen-audio-3.1-asr-flash-filetrans)

提交异步任务，完成后下载转写结果。

## 开始使用

在控制台[获取 API Key](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key)，并配置 `DASHSCOPE_API_KEY` 环境变量。

以下示例使用公网可访问的 16 kHz、单声道 WAV [示例音频](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/audios/6a4b3c2d1e0f9093.wav)。

#### Qwen-Audio-ASR

示例使用 qwen-audio-3.1-asr-flash，一次提交完整音频，在当前请求中获取最终识别结果。

cURL

```
curl \
  "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -H "X-DashScope-SSE: disable" \
  -d '{
  "model": "qwen-audio-3.1-asr-flash",
  "input": {
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "input_audio",
            "input_audio": {
              "data": "https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/audios/6a4b3c2d1e0f9093.wav"
            }
          }
        ]
      }
    ]
  },
  "parameters": {
    "format": "wav",
    "sample_rate": "16000"
  }
}'
```

Python

```
import json
import os
from urllib.request import Request, urlopen

api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
body = {
    "model": "qwen-audio-3.1-asr-flash",
    "input": {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_audio",
                        "input_audio": {
                            "data": "https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/audios/6a4b3c2d1e0f9093.wav"
                        }
                    }
                ]
            }
        ]
    },
    "parameters": {
        "format": "wav",
        "sample_rate": "16000"
    }
}
request = Request(
    api_url + "/services/aigc/multimodal-generation/generation",
    data=json.dumps(body).encode(),
    headers={
        "Authorization": "Bearer " + os.environ["DASHSCOPE_API_KEY"],
        "Content-Type": "application/json",
    },
)
with urlopen(request) as response:
    result = json.load(response)
print(result["output"]["text"])
```

#### Qwen-Audio-ASR-Filetrans

示例使用 qwen-audio-3.1-asr-flash-filetrans，先提交任务，再查询任务状态，任务成功后下载转写 JSON。

#### cURL

#### 提交任务

```
curl \
  "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/asr/transcription" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -H "X-DashScope-Async: enable" \
  -d '{
  "model": "qwen-audio-3.1-asr-flash-filetrans",
  "input": {
    "file_urls": [
      "https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/audios/6a4b3c2d1e0f9093.wav"
    ]
  },
  "parameters": {}
}'
```

#### 查询任务

将 `{task_id}` 替换为提交接口返回的 `output.task_id`。

-   `PENDING`、`RUNNING`：任务尚未完成，等待后再次查询。
-   `SUCCEEDED`：检查 `output.results[]` 中各文件的 `subtask_status`，获取成功文件的 `transcription_url`。
-   `FAILED`、`CANCELED`：任务未成功完成，读取返回的状态及错误信息。

```
curl \
  "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

#### 下载结果

将 `{transcription_url}` 替换为查询接口返回的结果文件 URL，下载并保存转写 JSON。该 URL 有效期为 24 小时。

```
curl "{transcription_url}" -o transcription.json
```

#### Python

```
import json
import os
import time
from urllib.request import Request, urlopen

api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
headers = {
    "Authorization": "Bearer " + os.environ["DASHSCOPE_API_KEY"],
    "Content-Type": "application/json",
}
body = {
    "model": "qwen-audio-3.1-asr-flash-filetrans",
    "input": {"file_urls": ["https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/audios/6a4b3c2d1e0f9093.wav"]},
    "parameters": {},
}
request = Request(
    api_url + "/services/audio/asr/transcription",
    data=json.dumps(body).encode(),
    headers={**headers, "X-DashScope-Async": "enable"},
)
with urlopen(request) as response:
    task_id = json.load(response)["output"]["task_id"]

while True:
    query = Request(api_url + "/tasks/" + task_id, headers=headers)
    with urlopen(query) as response:
        result = json.load(response)
    status = result["output"]["task_status"]
    if status == "SUCCEEDED":
        break
    if status in ("FAILED", "CANCELED"):
        raise RuntimeError(json.dumps(result, ensure_ascii=False))
    time.sleep(3)

for item in result["output"]["results"]:
    if item["subtask_status"] != "SUCCEEDED":
        raise RuntimeError(json.dumps(item, ensure_ascii=False))
    with urlopen(item["transcription_url"]) as response:
        transcript = json.load(response)
    print(json.dumps(transcript, ensure_ascii=False, indent=2))
```

异步转写结果示例

```
{
  "file_url": "https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/audios/6a4b3c2d1e0f9093.wav",
  "properties": {
    "audio_format": "pcm_s16le",
    "channels": [
      0
    ],
    "original_sampling_rate": 16000,
    "original_duration_in_milliseconds": 6228
  },
  "transcripts": [
    {
      "channel_id": 0,
      "content_duration_in_milliseconds": 5920,
      "text": "请把漆园项目的报告发给罗科，下周我们要上线玄枢系统。",
      "sentences": [
        {
          "begin_time": 160,
          "end_time": 6080,
          "text": "请把漆园项目的报告发给罗科，下周我们要上线玄枢系统。",
          "sentence_id": 1,
          "words": [
            {
              "begin_time": 160,
              "end_time": 600,
              "text": "请把",
              "punctuation": "",
              "confidence": 1.0
            },
            {
              "begin_time": 600,
              "end_time": 840,
              "text": "漆",
              "punctuation": "",
              "confidence": 1.0
            }
          ]
        }
      ]
    }
  ],
  "usage": {
    "input_tokens": 78,
    "output_tokens": 16,
    "total_Tokens": 94
  }
}
```

### 处理识别结果

-   **同步识别**：Qwen-Audio-ASR 的 `output.text` 是当前累计的完整文本，`output.sentence` 是当前句子的详细结果。保存完整转写时读取 `output.text`。
    
-   **异步转写**：任务成功后，下载结果文件，读取 `transcripts[].text` 获取各声道的完整文本；需要字幕或音频定位时，读取 `transcripts[].sentences` 及其中的 `words`。
    
-   **时间戳**：句子和字词中的 `begin_time`、`end_time` 以毫秒表示音频中的起止位置；任务查询结果中的 `end_time` 则是任务完成的日期时间。
    
    **说明**Qwen-Audio-ASR、Qwen-Audio-ASR-Filetrans、Fun-ASR、Fun-ASR-Flash 和 Paraformer 的时间戳固定开启，不支持关闭。Qwen3-ASR-Filetrans 的异步调用也固定返回时间戳，`enable_words` 控制返回句级或字级时间戳，不用于关闭时间戳。
    

## 优化识别效果

根据业务需求调整文本可读性、特定词汇识别、说话人标注和结果返回方式。

### 流式输出

流式输出在提交完整音频后，通过 SSE 分次返回识别结果，便于在整段音频识别完成前展示转写进度。

qwen-audio-3.1-asr-flash、Fun-ASR-Flash 和 Qwen3-ASR-Flash 支持流式输出。Qwen-Audio-ASR-Filetrans、Fun-ASR、Qwen3-ASR-Filetrans 和 Paraformer 等异步转写模型在任务完成后提供结果文件，不支持 SSE 流式输出。

**重要**使用 cURL 接收 SSE 时，添加 `--no-buffer`，避免输出缓冲影响结果展示。

**模型**

**启用方式**

**结果处理与注意事项**

qwen-audio-3.1-asr-flash

`X-DashScope-SSE: enable`

`output.text` 是累计文本，收到更新时替换已有内容。短音频可能只返回一次结果。未开启说话人分离时，词级时间戳在 `output.sentence.words[i].fixed` 为 `true` 后固定；开启后读取 `output.sentences` 中当前及历史句子的结果。

Qwen3-ASR-Flash

OpenAI 兼容 API：`stream: true`。原生 HTTP API：`X-DashScope-SSE: enable`。

OpenAI 兼容响应中的 `choices[].delta.content` 为增量文本，按返回顺序拼接。

Fun-ASR-Flash

`X-DashScope-SSE: enable`

Fun-ASR-Flash 在音频不少于 1 分钟时分次返回结果。

### 热词与上下文增强

人名、产品名或专业术语容易被识别成近音词时，可使用热词指定目标写法；需要补充前几轮对话、业务背景或相关词汇时，可使用上下文增强。支持范围、配置方法及效果示例参见[提升识别准确率](raw/model-user-guide/model-experience/speech-and-audio/speech-recognition/improve-asr-accuracy.md)。

### 文本润色与方言表达

qwen-audio-3.1-asr-flash 支持原生文本润色，可整理口语中的语气词、重复和自我纠正，提高转写文本的可读性。

qwen-audio-3.1-asr-flash 和 qwen-audio-3.1-asr-flash-filetrans 默认将方言转写为普通话文本。需要保留方言特有表达时，设置 `keep_dialect: true`。

### 说话人分离

多人会议或访谈需要区分发言人时，可开启说话人分离。识别结果中的 `speaker_id` 用于区分不同说话人。

**模型**

**开启方式**

**结果位置**

qwen-audio-3.1-asr-flash

`speaker_diarization_enabled: true`

`output.sentences[].speaker_id`

Qwen-Audio-ASR-Filetrans、Fun-ASR、Paraformer

`diarization_enabled: true`

`transcripts[].sentences[].speaker_id`

**说明**说话人分离仅支持单声道音频。异步转写启用该功能时，建议音频时长不超过 2 小时，否则可能导致识别失败或超时。qwen-audio-3.1-asr-flash 开启说话人分离后，`keep_dialect` 和 `language_hints` 不生效。

### 敏感词过滤

需要对转写文本中的指定词语进行遮蔽或移除时，可使用敏感词过滤。Qwen-Audio-ASR-Filetrans、Fun-ASR 和 Paraformer 支持通过 `special_word_filter` 配置自定义替换词表、移除词表及系统预置词表。

## 应用于生产环境

批量转写需要管理音频存储、任务提交与查询频率、完成通知和结果保存。输入准备、回调接入、限流与异常重试参见[语音识别最佳实践](raw/model-user-guide/model-experience/speech-and-audio/speech-recognition/speech-recognition-best-practices.md)。

## 支持的模型与地域

#### 华北2（北京）

-   **Qwen-Audio-ASR：**qwen-audio-3.1-asr-flash、qwen-audio-3.0-asr-flash
-   **Qwen-Audio-ASR-Filetrans：**qwen-audio-3.1-asr-flash-filetrans、qwen-audio-3.0-asr-flash-filetrans
-   **Qwen3-ASR-Flash：**qwen3-asr-flash（稳定版）
-   **Qwen3-ASR-Filetrans：**qwen3-asr-flash-filetrans（稳定版）
-   **Fun-ASR-Flash：**fun-asr-flash-2026-06-15
-   **Fun-ASR：**fun-asr（稳定版）
-   **Paraformer：**paraformer-v2、paraformer-8k-v2

#### 新加坡

-   **Qwen-Audio-ASR：**qwen-audio-3.1-asr-flash、qwen-audio-3.0-asr-flash
-   **Qwen-Audio-ASR-Filetrans：**qwen-audio-3.1-asr-flash-filetrans、qwen-audio-3.0-asr-flash-filetrans
-   **Qwen3-ASR-Flash：**qwen3-asr-flash（稳定版）
-   **Qwen3-ASR-Filetrans：**qwen3-asr-flash-filetrans（稳定版）
-   **Fun-ASR-Flash：**fun-asr-flash-2026-06-15
-   **Fun-ASR：**fun-asr（稳定版）

#### 美国（弗吉尼亚）

**Qwen3-ASR-Flash：**qwen3-asr-flash（稳定版）

## 使用限制

按模型选择输入方式、音频格式和采样率。传入 `format`、`sample_rate` 等参数时，应与实际文件一致。

**说明**Qwen-Audio-ASR-Filetrans、Fun-ASR 和 Paraformer 启用说话人分离时，建议音频时长不超过 2 小时，否则可能导致识别失败或超时。

**模型**

**输入方式**

**音频格式**

**采样率**

**文件大小与时长**

qwen-audio-3.1-asr-flash、qwen-audio-3.0-asr-flash

URL 或 Base64 Data URI，单次 1 个

`aac`、`amr`、`avi`、`flac`、`flv`、`m4a`、`mkv`、`mov`、`mp3`、`mp4`、`mpeg`、`ogg`、`opus`、`wav`、`webm`、`wma`、`wmv`

任意

≤2 GB；≤5 分钟

qwen-audio-3.1-asr-flash-filetrans、qwen-audio-3.0-asr-flash-filetrans

公网可访问的文件 URL，单次 1 个

`aac`、`amr`、`avi`、`flac`、`flv`、`m4a`、`mkv`、`mov`、`mp3`、`mp4`、`mpeg`、`ogg`、`opus`、`wav`、`webm`、`wma`、`wmv`

任意

≤2 GB；≤12 小时

qwen3-asr-flash

URL 或 Base64 Data URI，单次 1 个

`aac`、`amr`、`avi`、`aiff`、`flac`、`flv`、`mkv`、`mp3`、`mpeg`、`ogg`、`opus`、`wav`、`webm`、`wma`、`wmv`

PCM 为 16 kHz；其他格式任意，服务端重采样为 16 kHz

≤10 MB；≤5 分钟

qwen3-asr-flash-filetrans

公网可访问的文件 URL，单次 1 个

`aac`、`amr`、`avi`、`flac`、`flv`、`m4a`、`mkv`、`mov`、`mp3`、`mp4`、`mpeg`、`ogg`、`opus`、`wav`、`webm`、`wma`、`wmv`

PCM 为 16 kHz；其他格式任意，服务端重采样为 16 kHz

≤2 GB；≤12 小时

fun-asr-flash-2026-06-15

URL 或 Base64 Data URI，单次 1 个

`aac`、`amr`、`avi`、`flac`、`flv`、`m4a`、`mkv`、`mov`、`mp3`、`mp4`、`mpeg`、`ogg`、`opus`、`wav`、`webm`、`wma`、`wmv`

任意

≤2 GB；≤5 分钟

fun-asr

公网可访问的文件 URL，单次 1 个

`aac`、`amr`、`avi`、`flac`、`flv`、`m4a`、`mkv`、`mov`、`mp3`、`mp4`、`mpeg`、`ogg`、`opus`、`wav`、`webm`、`wma`、`wmv`

任意

≤2 GB；≤12 小时

paraformer-v2

公网可访问的文件 URL，单次 1 个

`aac`、`amr`、`avi`、`flac`、`flv`、`m4a`、`mkv`、`mov`、`mp3`、`mp4`、`mpeg`、`ogg`、`opus`、`wav`、`webm`、`wma`、`wmv`

任意

≤2 GB；≤12 小时

paraformer-8k-v2

公网可访问的文件 URL，单次 1 个

`aac`、`amr`、`avi`、`flac`、`flv`、`m4a`、`mkv`、`mov`、`mp3`、`mp4`、`mpeg`、`ogg`、`opus`、`wav`、`webm`、`wma`、`wmv`

8 kHz

≤2 GB；≤12 小时

说话人分离使用单声道音频；Paraformer 的 paraformer-8k-v2 仅支持 8 kHz。Qwen3-ASR-Flash 的本地文件输入需由客户端编码或上传，不能将本地路径直接作为 HTTP 音频 URL。

## API 参考

-   [非实时语音识别-Qwen-Audio-ASR API 参考](raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/qwen-audio-asr-api.md)
-   [非实时语音识别-Qwen-Audio-ASR-Filetrans API 参考](raw/model-api-reference/audio-api-directory/speech-recognition-api-reference/qwen-audio-asr-filetrans-api.md)
-   [非实时语音识别-Fun-ASR API 参考](raw/_short/fun-asr-recorded-speech-recognition-api-referenc-b0273c90bb44d4cc.md)
-   [非实时语音识别-Fun-ASR-Flash API 参考](raw/_short/non-real-time-speech-recognition-for-fun-asr-fla-650fa37d535f17b4.md)
-   [非实时语音识别-Qwen3-ASR API 参考](raw/_short/qwen-asr-api-reference-6234af32190b8ba9.md)
-   [非实时语音识别-Paraformer API 参考](raw/_short/paraformer-recorded-speech-recognition-api-refer-3f19f98cbb4ce26b.md)

## 模型应用上架及备案

参见[应用合规备案](raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)。
