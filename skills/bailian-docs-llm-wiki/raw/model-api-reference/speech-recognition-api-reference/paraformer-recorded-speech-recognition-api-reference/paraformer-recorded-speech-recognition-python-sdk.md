# Paraformer录音文件识别Python SDK

本文介绍Paraformer录音文件识别Python SDK的参数和接口细节。

**用户指南：**关于模型介绍和选型建议请参见[录音文件识别-Fun-ASR/Paraformer/SenseVoice](https://help.aliyun.com/zh/model-studio/recording-file-recognition)。

## **前提条件**

-   已开通服务并[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。请[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)，而非硬编码在代码中，防范因代码泄露导致的安全风险。
    
    **说明**
    
    当您需要为第三方应用或用户提供临时访问权限，或者希望严格控制敏感数据访问、删除等高风险操作时，建议使用[临时鉴权Token](https://help.aliyun.com/zh/model-studio/generate-temporary-api-key)。
    
    与长期有效的 API Key 相比，临时鉴权 Token 具备时效性短（60秒）、安全性高的特点，适用于临时调用场景，能有效降低API Key泄露的风险。
    
    使用方式：在代码中，将原本用于鉴权的 API Key 替换为获取到的临时鉴权 Token 即可。
    
-   [安装最新版DashScope SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。
    

## **快速开始**

[核心类（Transcription）](#adcb5e9bddbyq)提供了异步提交任务、同步等待任务结束和异步查询任务执行结果的接口。可通过如下两种调用方式进行录音文件识别：

-   异步提交任务+同步等待任务结束：提交任务后，阻塞当前线程直到任务结束并获取识别结果。
    
-   异步提交任务+异步查询任务执行结果：提交任务后，在需要的时候通过调用查询任务接口获取任务的执行结果。
    

### **异步提交任务+同步等待任务结束**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2768418771/CAEQURiBgMCvo5zjpxkiIDQyNzUwZjVjMWM3MjQ5Nzg4ODBjNDRjNzE1ZGFiOGFj4709861_20241015153444.149.svg)

1.  调用[核心类（Transcription）](#adcb5e9bddbyq)的`async_call`方法并设置[请求参数](#340f6879fci7d)。
    
    **说明**
    
    -   文件转写服务对通过API提交的任务采取尽力服务原则进行处理。任务提交后将进入排队（`PENDING`）状态，排队时间取决于队列长度和文件时长，无法明确给出，通常在数分钟内。任务开始处理后，语音识别将以数百倍加速完成。
        
    -   每一个任务完成后，识别结果和URL下载链接有效期为24小时，超时后无法查询任务或通过先前查询结果中的URL下载结果。
        
    
2.  调用[核心类（Transcription）](#adcb5e9bddbyq)的`wait`方法同步等待任务结束。
    
    任务的状态包括`PENDING`、`RUNNING`、`SUCCEEDED`和`FAILED`。当任务处于`PENDING`或`RUNNING`状态时，`wait`接口将被阻塞。当任务处于`SUCCEEDED`或`FAILED`状态时，`wait`接口不再阻塞并返回任务的执行结果。
    
    `wait`返回[TranscriptionResponse](#c4fe4e43ee4n6)。
    

点击查看完整示例

```
from http import HTTPStatus
from dashscope.audio.asr import Transcription
import json

# 若没有将API Key配置到环境变量中，需将下面这行代码注释放开，并将apiKey替换为自己的API Key
# import dashscope
# dashscope.api_key = "apiKey"

task_response = Transcription.async_call(
    model='paraformer-v2',
    file_urls=['https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav',
               'https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav'],
    language_hints=['zh', 'en']  # “language_hints”只支持paraformer-v2模型
)

transcribe_response = Transcription.wait(task=task_response.output.task_id)
if transcribe_response.status_code == HTTPStatus.OK:
    print(json.dumps(transcribe_response.output, indent=4, ensure_ascii=False))
    print('transcription done!')
```

### **异步提交任务+异步查询任务执行结果**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2768418771/CAEQURiBgMCN3qzkpxkiIGE0YmU4YTdjMWNiNzRmYjJhMjFlMWZkZmFmOWQ1NmEx4709861_20241015153444.149.svg)

1.  调用[核心类（Transcription）](#adcb5e9bddbyq)的`async_call`方法并设置[请求参数](#340f6879fci7d)。
    
    **说明**
    
    -   文件转写服务对通过API提交的任务采取尽力服务原则进行处理。任务提交后将进入排队（`PENDING`）状态，排队时间取决于队列长度和文件时长，无法明确给出，通常在数分钟内。任务开始处理后，语音识别将以数百倍加速完成。
        
    -   每一个任务完成后，识别结果和URL下载链接有效期为24小时，超时后无法查询任务或通过先前查询结果中的URL下载结果。
        
    
2.  循环调用[核心类（Transcription）](#adcb5e9bddbyq)的`fetch`方法直到获取最终的任务结果。
    
    当任务状态为`SUCCEEDED`或`FAILED`时，停止轮询并处理结果。
    
    `fetch`返回[TranscriptionResponse](#c4fe4e43ee4n6)。
    

点击查看完整示例

```
from http import HTTPStatus
from dashscope.audio.asr import Transcription
import json

# 若没有将API Key配置到环境变量中，需将下面这行代码注释放开，并将apiKey替换为自己的API Key
# import dashscope
# dashscope.api_key = "apiKey"

transcribe_response = Transcription.async_call(
    model='paraformer-v2',
    file_urls=['https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav',
               'https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav'],
    language_hints=['zh', 'en']  # “language_hints”只支持paraformer-v2模型
)

while True:
    if transcribe_response.output.task_status == 'SUCCEEDED' or transcribe_response.output.task_status == 'FAILED':
        break
    transcribe_response = Transcription.fetch(task=transcribe_response.output.task_id)

if transcribe_response.status_code == HTTPStatus.OK:
    print(json.dumps(transcribe_response.output, indent=4, ensure_ascii=False))
    print('transcription done!')
```

## **请求参数**

请求参数通过[核心类（Transcription）](#adcb5e9bddbyq)的`async_call`方法进行设置。

**重要**

说话人分离功能（`diarization_enabled`）仅适用于单声道音频，多声道音频不支持说话人分离。如果您的音频为多声道格式，需先将其转换为单声道后再启用说话人分离。可使用ffmpeg进行转换：`ffmpeg -i input.wav -ac 1 output_mono.wav`。

**参数**

**类型**

**默认值**

**是否必须**

**说明**

model

str

\-

是

指定用于音视频文件转写的Paraformer模型名。参见[支持的模型](https://help.aliyun.com/zh/model-studio/recording-file-recognition#da60323c9ea75)。

file\_urls

list\[str\]

\-

是

音视频文件转写的URL列表，支持HTTP / HTTPS协议，单次请求最多支持100个URL。

若录音文件存储在阿里云OSS，使用SDK方式不支持使用以 oss://为前缀的临时 URL。

vocabulary\_id

str

\-

否

最新热词ID，支持最新v2系列模型并配置语种信息，此次语音识别中生效此热词ID对应的热词信息。默认不启用。使用方法请参考[定制热词](https://help.aliyun.com/zh/model-studio/custom-hot-words/)。

phrase\_id

str

\-

否

热词ID，此次语音识别中生效此热词ID对应的热词信息。默认不启用。

注：`phrase_id`为v1版本模型热词方案，不支持v2及后续系列模型。支持该方式热词的模型列表请参考[Paraformer语音识别热词定制与管理](https://help.aliyun.com/zh/model-studio/paraformer-asr-phrase-manager)。

channel\_id

list\[int\]

\[0\]

否

指定在多音轨音频文件中需要识别的音轨索引，索引从 0 开始。例如，\[0\] 表示识别第一个音轨，\[0, 1\] 表示同时识别第一和第二个音轨。如果省略此参数，则默认处理第一个音轨。

**重要**

指定的每一个音轨都将独立计费。例如，为单个文件请求 \[0, 1\] 会产生两笔独立的费用。

disfluency\_removal\_enabled

bool

False

否

过滤语气词，默认关闭。

timestamp\_alignment\_enabled

bool

False

否

是否启用时间戳校准功能，默认关闭。

special\_word\_filter

str

\-

否

指定在语音识别过程中需要处理的敏感词，并支持对不同敏感词设置不同的处理方式。

若未传入该参数，系统将启用系统内置的敏感词过滤逻辑，识别结果中与[阿里云百炼敏感词表](https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/%E7%99%BE%E7%82%BC%E6%95%8F%E6%84%9F%E8%AF%8D%E5%88%97%E8%A1%A8_20230716.words.txt)匹配的词语将被替换为等长的`*`。

若传入该参数，则可实现以下敏感词处理策略：

-   替换为 `*`：将匹配的敏感词替换为等长的 `*`；
    
-   直接过滤：将匹配的敏感词从识别结果中完全移除。
    

该参数的值应为一个 JSON 字符串，其结构如下所示：

```
{
  "filter_with_signed": {
    "word_list": ["测试"]
  },
  "filter_with_empty": {
    "word_list": ["开始", "发生"]
  },
  "system_reserved_filter": true
}
```

JSON字段说明：

-   `filter_with_signed`
    
    -   类型：对象。
        
    -   是否必填：否。
        
    -   描述：配置需替换为`*`的敏感词列表。识别结果中匹配的词语将被等长的 `*` 替代。
        
    -   示例：以上述JSON为例，“帮我测试一下这段代码”的语音识别结果将会是“帮我\*\*一下这段代码”。
        
    -   内部字段：
        
        -   `word_list`: 字符串数组，列出需被替换的敏感词。
            
-   `filter_with_empty`
    
    -   类型：对象。
        
    -   是否必填：否。
        
    -   描述：配置需从识别结果中移除（过滤）的敏感词列表。识别结果中匹配的词语将被完全删除。
        
    -   示例：以上述JSON为例，“比赛这就要开始了吗？”的语音识别结果将会是“比赛这就要了吗”。
        
    -   内部字段：
        
        -   `word_list`: 字符串数组，列出需被完全移除（过滤）的敏感词。
            
-   `system_reserved_filter`
    
    -   类型：布尔值。
        
    -   是否必填：否。
        
    -   默认值：true。
        
    -   描述：是否启用系统预置的敏感词规则。设为`true`时，将同时启用系统内置的敏感词过滤逻辑，识别结果中与[阿里云百炼敏感词表](https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/%E7%99%BE%E7%82%BC%E6%95%8F%E6%84%9F%E8%AF%8D%E5%88%97%E8%A1%A8_20230716.words.txt)匹配的词语将被替换为等长的`*`。
        

language\_hints

list\[str\]

\["zh", "en"\]

否

指定待识别语音的语言代码。

该参数仅适用于paraformer-v2模型。

支持的语言代码：

-   zh: 中文
    
-   en: 英文
    
-   ja: 日语
    
-   yue: 粤语
    
-   ko: 韩语
    
-   de：德语
    
-   fr：法语
    
-   ru：俄语
    

diarization\_enabled

bool

False

否

自动说话人分离，默认关闭。

仅适用于单声道音频，多声道音频不支持说话人分离。

启用该功能后，识别结果中将显示`speaker_id`字段，用于区分不同说话人。

**说明**

如果启用说话人分离功能，建议音频时长不超过2小时，否则可能导致识别失败或超时。

有关`speaker_id`的示例，请参见[识别结果说明](#a9021178ccl7s)。

speaker\_count

int

\-

否

说话人数量参考值。取值范围为2至100的整数（包含2和100）。

开启说话人分离功能后（`diarization_enabled`设置为true）生效。

默认自动判断说话人数量，如果配置此项，只能辅助算法尽量输出指定人数，无法保证一定会输出此人数。

## **响应结果**

### `**TranscriptionResponse**`

`TranscriptionResponse`封装了任务的基本信息（`task_id`和`task_status`）和执行结果（`output`属性对应的内容，参见[TranscriptionOutput](#3c2916848c07k)）。

点击查看`TranscriptionResponse`结构示例

`async_call`方法返回的`TranscriptionResponse`示例如下，不包含`submit_time`、`scheduled_time`等信息：

```
{
    "status_code":200,
    "request_id":"251aceab-a6aa-9fc4-b7f7-0cc6d3e2a9f3",
    "code":null,
    "message":"",
    "output":{
        "task_id":"7d0a58a3-1dbe-4de9-8cff-5f48213128b0",
        "task_status":"PENDING"
    },
    "usage":null
}
```

如果需要获取`submit_time`、`scheduled_time`等信息，应使用`wait()`或`fetch()`方法，而不是直接从 `async_call()` 的返回值中访问。`wait()`或`fetch()`方法返回的`TranscriptionResponse`示例如下：

## `PENDING`状态

```
{
    "status_code":200,
    "request_id":"251aceab-a6aa-9fc4-b7f7-0cc6d3e2a9f3",
    "code":null,
    "message":"",
    "output":{
        "task_id":"7d0a58a3-1dbe-4de9-8cff-5f48213128b0",
        "task_status":"PENDING",
        "submit_time":"2025-02-13 16:55:08.573",
        "scheduled_time":"2025-02-13 16:55:08.592",
        "task_metrics":{
            "TOTAL":2,
            "SUCCEEDED":0,
            "FAILED":0
        }
    },
    "usage":null
}
```

## `RUNNING`状态

```
{
    "status_code":200,
    "request_id":"d9d530f1-853c-9848-a5f1-f5de59086ff7",
    "code":null,
    "message":"",
    "output":{
        "task_id":"6351feef-9694-45d2-9d32-63454f2ffb8d",
        "task_status":"RUNNING",
        "submit_time":"2025-02-13 17:31:20.681",
        "scheduled_time":"2025-02-13 17:31:20.703",
        "task_metrics":{
            "TOTAL":2,
            "SUCCEEDED":1,
            "FAILED":0
        }
    },
    "usage":null
}
```

## `SUCCEEDED`状态

```
{
    "status_code":200,
    "request_id":"16668704-6702-9e03-8ab7-a32a5d7bb095",
    "code":null,
    "message":"",
    "output":{
        "task_id":"6351feef-9694-45d2-9d32-63454f2ffb8d",
        "task_status":"SUCCEEDED",
        "submit_time":"2025-02-13 17:31:20.681",
        "scheduled_time":"2025-02-13 17:31:20.703",
        "end_time":"2025-02-13 17:31:21.867",
        "results":[
            {
                "file_url":"https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav",
                "transcription_url":"https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/prod/paraformer-v2/20250213/17%3A31/20ee4e4f-0404-4806-b617-c7d4c62eed19-1.json?Expires=1739525481&OSSAccessKeyId=yourOSSAccessKeyId&Signature=3q%2B1uQmRwltd7FPn5HQM2mBKw74%3D",
                "subtask_status":"SUCCEEDED"
            },
            {
                "file_url":"https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav",
                "transcription_url":"https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/prod/paraformer-v2/20250213/17%3A31/be4f14c5-e46b-47ff-b03a-476ae9a45fd3-1.json?Expires=1739525481&OSSAccessKeyId=yourOSSAccessKeyId&Signature=EUX%2FRkGcn46L5d93ihQmpWUeYE4%3D",
                "subtask_status":"SUCCEEDED"
            }
        ],
        "task_metrics":{
            "TOTAL":2,
            "SUCCEEDED":2,
            "FAILED":0
        }
    },
    "usage":{
        "duration":9
    }
}
```

## `FAILED`状态

```
{
    "status_code":200,
    "request_id":"16668704-6702-9e03-8ab7-a32a5d7bb095",
    "code":null,
    "message":"",
    "output":{
        "task_id": "7bac899c-06ec-4a79-8875-xxxxxxxxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2024-12-16 16:30:59.170",
        "scheduled_time": "2024-12-16 16:30:59.204",
        "end_time": "2024-12-16 16:31:02.375",
        "results": [
            {
                "file_url": "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/sensevoice/long_audio_demo_cn.mp3",
                "transcription_url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/prod/paraformer-v2/20241216/xxxx",
                "subtask_status": "SUCCEEDED"
            },
            {
                "file_url": "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/sensevoice/rich_text_exaple_1.wav",
                "code": "InvalidFile.DownloadFailed",
                "message": "The audio file cannot be downloaded.",
                "subtask_status": "FAILED"
            }
        ],
        "task_metrics": {
            "TOTAL": 2,
            "SUCCEEDED": 1,
            "FAILED": 1
        }
    },
    "usage":{
        "duration":9
    }
}
```

需要关注的参数：

**参数**

**说明**

status\_code

HTTP请求状态码。

code

-   最外层的`code`不必关注。
    
-   `output.results`下面的`code`，代表错误码。可以结合`message`字段，对照[错误码](#c70f9758027ph)排查问题。
    

message

-   最外层的`message`不必关注。
    
-   `output.results`下面的`message`，代表错误信息。可以结合`code`字段，对照[错误码](#c70f9758027ph)排查问题。
    

task\_id

任务ID。

task\_status

任务状态。

有`PENDING`、`RUNNING`、`SUCCEEDED`和`FAILED`这四种状态。

当任务包含多个子任务时，只要存在任一子任务成功，整个任务状态将标记为`SUCCEEDED`，需通过`subtask_status`字段判断具体子任务结果。

results

子任务识别结果。

subtask\_status

子任务状态。

有`PENDING`、`RUNNING`、`SUCCEEDED`和`FAILED`这四种状态。

file\_url

被识别音频的URL。

transcription\_url

音频识别结果对应的URL。

识别结果保存为JSON文件，您可以通过`transcription_url`对应的链接下载文件或直接通过HTTP请求读取该文件中的内容。JSON文件的内容请参见[识别结果说明](#a9021178ccl7s)。

### `TranscriptionOutput`

`TranscriptionOutput`对应[TranscriptionResponse](#c4fe4e43ee4n6)的`output`属性，代表当前任务执行结果。

点击查看`TranscriptionOutput`结构示例

## PENDING状态

```
{
    "task_id":"f2f7c2fa-0cd9-4bb2-a283-27b26ee4bb67",
    "task_status":"PENDING",
    "submit_time":"2025-02-13 17:59:27.754",
    "scheduled_time":"2025-02-13 17:59:27.789",
    "task_metrics":{
        "TOTAL":2,
        "SUCCEEDED":0,
        "FAILED":0
    }
}
```

## RUNNING状态

```
{
    "task_id":"f2f7c2fa-0cd9-4bb2-a283-27b26ee4bb67",
    "task_status":"RUNNING",
    "submit_time":"2025-02-13 17:59:27.754",
    "scheduled_time":"2025-02-13 17:59:27.789",
    "task_metrics":{
        "TOTAL":2,
        "SUCCEEDED":0,
        "FAILED":0
    }
}
```

## `SUCCEEDED`状态

```
{
    "task_id":"f2f7c2fa-0cd9-4bb2-a283-27b26ee4bb67",
    "task_status":"SUCCEEDED",
    "submit_time":"2025-02-13 17:59:27.754",
    "scheduled_time":"2025-02-13 17:59:27.789",
    "end_time":"2025-02-13 17:59:28.828",
    "results":[
        {
            "file_url":"https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav",
            "transcription_url":"https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/prod/paraformer-v2/20250213/17%3A59/70e737cc-bf8c-418b-b0c8-83fab192a0fa-1.json?Expires=1739527168&OSSAccessKeyId=yourOSSAccessKeyId&Signature=AtGjIKI%2BdgbzjJIu%2BHsr1R5nSAY%3D",
            "subtask_status":"SUCCEEDED"
        },
        {
            "file_url":"https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav",
            "transcription_url":"https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/prod/paraformer-v2/20250213/17%3A59/ce1ebe74-be78-4ac8-b4f8-8e438a14d1c2-1.json?Expires=1739527168&OSSAccessKeyId=yourOSSAccessKeyId&Signature=z5s0ROpSU8HwiM8WHPNVpkuFG3A%3D",
            "subtask_status":"SUCCEEDED"
        }
    ],
    "task_metrics":{
        "TOTAL":2,
        "SUCCEEDED":2,
        "FAILED":0
    }
}
```

## `FAILED`状态

“`code`”为错误码，“`message`”为错误信息，只有异常情况才有这两个字段，您可以通过这两个字段，对照[错误码](#c70f9758027ph)排查问题。

```
{
    "task_id": "7bac899c-06ec-4a79-8875-xxxxxxxxxxxx",
    "task_status": "SUCCEEDED",
    "submit_time": "2024-12-16 16:30:59.170",
    "scheduled_time": "2024-12-16 16:30:59.204",
    "end_time": "2024-12-16 16:31:02.375",
    "results": [
        {
            "file_url": "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/sensevoice/long_audio_demo_cn.mp3",
            "transcription_url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/prod/paraformer-v2/20241216/xxxx",
            "subtask_status": "SUCCEEDED"
        },
        {
            "file_url": "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/sensevoice/rich_text_exaple_1.wav",
            "code": "InvalidFile.DownloadFailed",
            "message": "The audio file cannot be downloaded.",
            "subtask_status": "FAILED"
        }
    ],
    "task_metrics": {
        "TOTAL": 2,
        "SUCCEEDED": 1,
        "FAILED": 1
    }
}
```

需要关注的参数：

**参数**

**说明**

code

代表错误码。可以结合`message`字段，对照[错误码](#c70f9758027ph)排查问题。

message

代表错误信息。可以结合`code`字段，对照[错误码](#c70f9758027ph)排查问题。

task\_id

任务ID。

task\_status

任务状态。

有`PENDING`、`RUNNING`、`SUCCEEDED`和`FAILED`这四种状态。

当任务包含多个子任务时，只要存在任一子任务成功，整个任务状态将标记为`SUCCEEDED`，需通过`subtask_status`字段判断具体子任务结果。

results

子任务识别结果。

subtask\_status

子任务状态。

有`PENDING`、`RUNNING`、`SUCCEEDED`和`FAILED`这四种状态。

file\_url

被识别音频的URL。

transcription\_url

音频识别结果对应的URL。

识别结果以JSON格式保存在一个JSON文件中，您可以通过`transcription_url`对应的链接下载文件或直接通过HTTP请求读取该文件中的内容。JSON文件的内容请参见[识别结果说明](#a9021178ccl7s)。

### 识别结果说明

识别结果保存为JSON文件。

点击查看识别结果示例

```
{
    "file_url":"https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav",
    "properties":{
        "audio_format":"pcm_s16le",
        "channels":[
            0
        ],
        "original_sampling_rate":16000,
        "original_duration_in_milliseconds":3834
    },
    "transcripts":[
        {
            "channel_id":0,
            "content_duration_in_milliseconds":3720,
            "text":"Hello world, 这里是阿里巴巴语音实验室。",
            "sentences":[
                {
                    "begin_time":100,
                    "end_time":3820,
                    "text":"Hello world, 这里是阿里巴巴语音实验室。",
                    "sentence_id":1,
                    "speaker_id":0, //当开启自动说话人分离功能时才会显示该字段
                    "words":[
                        {
                            "begin_time":100,
                            "end_time":596,
                            "text":"Hello ",
                            "punctuation":""
                        },
                        {
                            "begin_time":596,
                            "end_time":844,
                            "text":"world",
                            "punctuation":", "
                        }
                        // 这里省略其它内容
                    ]
                }
            ]
        }
    ]
}
```

需要关注的参数如下：

**参数**

**类型**

**说明**

audio\_format

string

源文件中音频的格式。

channels

array\[integer\]

源文件中音频的音轨索引信息，对单轨音频返回\[0\]，对双轨音频返回\[0, 1\]，以此类推。

original\_sampling\_rate

integer

源文件中音频的采样率（Hz）。

original\_duration

integer

源文件中的原始音频时长（ms）。

channel\_id

integer

转写结果的音轨索引，以0为起始。

content\_duration

integer

音轨中被判定为语音内容的时长（ms）。

**重要**

Paraformer语音识别模型服务仅对音轨中被判定为语音内容的时长进行语音转写，并据此进行计量计费，非语音内容不计量、不计费。通常情况下语音内容时长会短于原始音频时长。由于对是否存在语音内容的判定是由AI模型给出的，可能与实际情况存在一定误差。

transcript

string

段落级别的语音转写结果。

sentences

array

句子级别的语音转写结果。

words

array

词级别的语音转写结果。

begin\_time

integer

开始时间戳（ms）。

end\_time

integer

结束时间戳（ms）。

text

string

语音转写结果。

speaker\_id

integer

当前说话人的索引，以0为起始，用于区分不同的说话人。

仅在启用说话人分离功能时，该字段才会显示于识别结果中。

punctuation

string

预测出的词之后的标点符号（如有）。

## **关键接口**

### 核心类（`Transcription`）

`Transcription`可以通过“`from dashscope.audio.asr import Transcription`”方式引入。

**成员方法**

**方法签名**

**说明**

async\_call

```
@classmethod
def async_call(cls,
               model: str,
               file_urls: List[str],
               phrase_id: str = None,
               api_key: str = None,
               workspace: str = None,
               **kwargs) -> TranscriptionResponse
```

异步提交语音识别任务。

该方法返回[TranscriptionResponse](#c4fe4e43ee4n6)。

wait

```
@classmethod
def wait(cls,
         task: Union[str, TranscriptionResponse],
         api_key: str = None,
         workspace: str = None,
         **kwargs) -> TranscriptionResponse
```

阻塞当前线程直到异步任务结束（任务状态为`SUCCEEDED`或`FAILED`）。

该方法返回[TranscriptionResponse](#c4fe4e43ee4n6)。

fetch

```
@classmethod
def fetch(cls,
          task: Union[str, TranscriptionResponse],
          api_key: str = None,
          workspace: str = None,
          **kwargs) -> TranscriptionResponse
```

异步查询当前任务执行结果。

该方法返回[TranscriptionResponse](#c4fe4e43ee4n6)。

## **其他接口：批量查询任务状态/取消任务**

详情请参见[管理异步任务](https://help.aliyun.com/zh/model-studio/manage-asynchronous-tasks)：支持批量查询24小时内提交的录音文件识别任务，同时支持取消`PENDING`（排队）状态的任务。

## **错误码**

如遇报错问题，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行排查。

若问题仍未解决，请加入[开发者群](https://github.com/aliyun/alibabacloud-bailian-speech-demo)反馈遇到的问题，并提供Request ID，以便进一步排查问题。

当任务包含多个子任务时，只要存在任一子任务成功，整个任务状态将标记为`SUCCEEDED`，需通过`subtask_status`字段判断具体子任务结果。

错误返回示例：

```
{
    "task_id": "7bac899c-06ec-4a79-8875-xxxxxxxxxxxx",
    "task_status": "SUCCEEDED",
    "submit_time": "2024-12-16 16:30:59.170",
    "scheduled_time": "2024-12-16 16:30:59.204",
    "end_time": "2024-12-16 16:31:02.375",
    "results": [
        {
            "file_url": "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/sensevoice/long_audio_demo_cn.mp3",
            "transcription_url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/prod/paraformer-v2/20241216/xxxx",
            "subtask_status": "SUCCEEDED"
        },
        {
            "file_url": "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/sensevoice/rich_text_exaple_1.wav",
            "code": "InvalidFile.DownloadFailed",
            "message": "The audio file cannot be downloaded.",
            "subtask_status": "FAILED"
        }
    ],
    "task_metrics": {
        "TOTAL": 2,
        "SUCCEEDED": 1,
        "FAILED": 1
    }
}
```

## **更多示例**

更多示例，请参见[GitHub](https://github.com/aliyun/alibabacloud-bailian-speech-demo)。

## **常见问题**

### **功能特性**

#### **Q：是否支持Base64编码方式的音频？**

不支持Base64编码方式的音频。仅支持可通过公网访问的 URL 所指向的音频的识别，不支持识别二进制流，也不支持直接识别本地文件。

#### **Q：如何将音频文件以公网可访问的URL形式提供？**

通常遵循以下几个步骤（这里为您提供一种思路，具体情况因不同存储产品而异，推荐将音频[上传至阿里云OSS](https://help.aliyun.com/zh/oss/user-guide/simple-upload#a632b50f190j8)）：

1、选择存储和托管方式

如以下这几种：

-   对象存储服务（推荐）：
    
    -   使用云服务商的对象存储服务（如[阿里云OSS](https://help.aliyun.com/zh/oss/user-guide/simple-upload#a632b50f190j8)），将音频文件上传到存储桶中，并设置为公开访问。
        
    -   优点：高可用性、支持 CDN 加速、易于管理。
        
-   Web 服务器：
    
    -   将音频文件放置在支持 HTTP/HTTPS 访问的 Web 服务器上（如 Nginx、Apache）。
        
    -   优点：适合小型项目或本地测试。
        
-   内容分发网络（CDN）：
    
    -   将音频文件托管在 CDN 上，通过 CDN 提供的 URL 访问。
        
    -   优点：加速文件传输，适合高并发场景。
        

2、上传音频文件

根据选择的存储/托管方式，将音频上传，如：

-   对象存储服务：
    
    -   登录云服务商的控制台，创建存储桶。
        
    -   上传音频文件，并设置文件权限为“公共读”或生成临时访问链接。
        
-   Web 服务器：
    
    -   将音频文件放置在服务器指定目录下（如 `/var/www/html/audio/`）。
        
    -   确保文件可以通过 HTTP/HTTPS 访问。
        

3、生成公网可访问的URL

例如：

-   对象存储服务：
    
    -   文件上传后，系统会自动生成一个公网访问 URL（通常格式为 `https://<bucket-name>.<region>.aliyuncs.com/<file-name>`）。
        
    -   如果需要更友好的域名，可以绑定自定义域名并开启 HTTPS。
        
-   Web 服务器：
    
    -   文件的访问 URL 通常是服务器地址加上文件路径（如 `https://your-domain.com/audio/file.mp3`）。
        
-   CDN：
    
    -   配置 CDN 加速后，使用 CDN 提供的 URL（如 `https://cdn.your-domain.com/audio/file.mp3`）。
        

4、验证URL的可用性

公网环境下，确保生成的 URL 可以正常访问，例如：

-   在浏览器中打开 URL，检查是否能播放音频文件。
    
-   使用工具（如 `curl` 或 Postman）验证 URL 是否返回正确的 HTTP 响应（状态码 200）。
    

使用SDK时，若录音文件存储在[阿里云OSS](https://help.aliyun.com/zh/oss/user-guide/simple-upload#a632b50f190j8)，不支持使用以 `oss://`为前缀的临时 URL。

使用RESTful API时，若录音文件存储在[阿里云OSS](https://help.aliyun.com/zh/oss/user-guide/simple-upload#a632b50f190j8)，支持使用以 `oss://`为前缀的临时 URL：

**重要**

-   临时 URL 有效期48小时，过期后无法使用，**请勿用于生产环境。**
    
-   文件上传凭证接口限流为 100 QPS 且不支持扩容，**请勿用于生产环境、高并发及压测场景。**
    
-   生产环境建议使用[阿里云OSS](https://help.aliyun.com/zh/oss/user-guide/what-is-oss) 等稳定存储，确保文件长期可用并规避限流问题。
    

#### **Q：多久能获取识别结果？**

任务提交后将进入排队（PENDING）状态，排队时间取决于队列长度和文件时长，无法明确给出，通常在数分钟内，请耐心等待。并且音频时长越长，所需时间越久。

### **故障排查**

如遇代码报错问题，请根据[错误码](#c70f9758027ph)中的信息进行排查。

#### **Q：识别结果和语音播放不同步怎么办？**

将[请求参数](#340f6879fci7d)`timestamp_alignment_enabled`设为`true`将启用时间戳校准功能，能够让识别结果和语音播放同步。

#### **Q：一直轮询不到结果？**

可能是限流原因，请耐心等待。若需扩容，请加入[开发者群](https://github.com/aliyun/alibabacloud-bailian-speech-demo)进行申请。

#### **Q：无法识别语音（无识别结果）是什么原因？**

-   请检查音频是否符合要求（格式、采样率）。
    
-   若是使用了`paraformer-v2`模型，检查`language_hints`的设置是否正确。
    
-   以上都没问题，可通过定制热词，提升对特定词语的识别效果。
    

#### **Q：说话人分离结果全部标记为同一个Speaker怎么办？**

请按以下步骤排查：

1.  检查音频是否为单声道格式。说话人分离功能仅支持单声道音频，多声道音频不支持说话人分离。可使用ffprobe查看音频声道数：`ffprobe -i input.wav -show_entries stream=channels -of default=noprint_wrappers=1`。
    
2.  如果音频为多声道，需先转换为单声道：`ffmpeg -i input.wav -ac 1 output_mono.wav`。
    
3.  确认已正确设置说话人分离参数：`diarization_enabled=true`，并根据实际说话人数设置`speaker_count`参数（取值范围2至100）。
    

### **更多问题**

请参见GitHub [QA](https://github.com/aliyun/alibabacloud-bailian-speech-demo/tree/master/docs/QA)。
