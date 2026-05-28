# Paraformer录音文件识别RESTful API

本文介绍Paraformer录音文件识别RESTful API的参数和接口细节。

**用户指南：**关于模型介绍和选型建议请参见[录音文件识别-Fun-ASR/Paraformer/SenseVoice](https://help.aliyun.com/zh/model-studio/recording-file-recognition)。

目前提供了[提交任务接口](#418f2ac8ecxm4)和[查询任务接口](#480630e0582sb)，通常情况下，您可以先调用提交任务接口上传识别任务，然后循环调用查询任务接口，直至任务完成。

## **前提条件**

已开通服务并[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。请[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)，而非硬编码在代码中，防范因代码泄露导致的安全风险。

**说明**

当您需要为第三方应用或用户提供临时访问权限，或者希望严格控制敏感数据访问、删除等高风险操作时，建议使用[临时鉴权Token](https://help.aliyun.com/zh/model-studio/generate-temporary-api-key)。

与长期有效的 API Key 相比，临时鉴权 Token 具备时效性短（60秒）、安全性高的特点，适用于临时调用场景，能有效降低API Key泄露的风险。

使用方式：在代码中，将原本用于鉴权的 API Key 替换为获取到的临时鉴权 Token 即可。

## **提交任务接口**

### **基本信息**

**接口描述**

提交语音识别任务。

**URL**

```
https://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription
```

**请求方法**

POST

**请求头**

```
Authorization: Bearer {api-key} // 需替换为您自己的API Key
Content-Type: application/json
X-DashScope-Async: enable // 请勿遗漏该请求头，否则无法提交任务
```

**消息体**

包含所有[请求参数](#493b0f8f2ap0y)的消息体如下，对于可选字段，在实际业务中可根据需求省略：

```
{
    "model":"paraformer-v2", //模型名，必选
    "input":{
        "file_urls":[
            "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav",
            "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav"
        ] //待识别文件，必选
    }
    "parameters":{
        "channel_id":[
            0
        ], //音轨索引，可选
        "disfluency_removal_enabled":false, //过滤语气词开关，可选
        "timestamp_alignment_enabled": false, //是否启用时间戳校准功能，可选
        "special_word_filter": "xxx", //敏感词，可选
        "language_hints":[ // 当前该参数仅适用于paraformer-v2模型，其他模型不要使用该字段
            "zh",
            "en"
        ],
        "diarization_enabled":false, //自动说话人分离，可选
        "speaker_count": 2 //说话人数量参考，可选
    }
}
```

### **请求参数**

**点击查看请求示例**

以下为调用提交任务接口的cURL示例：

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription' \
     --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
     --header "Content-Type: application/json" \
     --header "X-DashScope-Async: enable" \
     --data '{"model":"paraformer-v2","input":{"file_urls":["https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav",
              "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav"]},"parameters":{"channel_id":[0]}}'
```

**参数**

**类型**

**默认值**

**是否必须**

**说明**

model

string

\-

是

指定用于音视频文件转写的Paraformer模型名。参见[支持的模型](https://help.aliyun.com/zh/model-studio/recording-file-recognition#da60323c9ea75)。

file\_urls

array\[string\]

\-

是

音视频文件转写的URL列表，支持HTTP / HTTPS协议，单次请求最多支持100个URL。

**重要**

URL中如果包含空格、中文或其他特殊字符，必须先进行URL编码（例如将空格替换为`%20`），否则可能导致文件下载失败，返回`InvalidFile.DownloadFailed`错误。

若录音文件存储在阿里云OSS，使用RESTful API方式支持使用以 oss://为前缀的临时 URL。

**重要**

-   临时 URL 有效期48小时，过期后无法使用，**请勿用于生产环境。**
    
-   文件上传凭证接口限流为 100 QPS 且不支持扩容，**请勿用于生产环境、高并发及压测场景。**
    
-   生产环境建议使用[阿里云OSS](https://help.aliyun.com/zh/oss/user-guide/what-is-oss) 等稳定存储，确保文件长期可用并规避限流问题。
    

vocabulary\_id

string

\-

否

最新热词ID，支持最新v2系列模型并配置语种信息，此次语音识别中生效此热词ID对应的热词信息。默认不启用。使用方法请参考[定制热词](https://help.aliyun.com/zh/model-studio/custom-hot-words/)。

resource\_id

string

\-

否

热词ID，此次语音识别中生效此热词ID对应的热词信息。默认不启用。

注：`resource_id`对应SDK中的`phrase_id`字段，`phrase_id`为v1版本模型热词方案，不支持v2及后续系列模型。支持该方式热词的模型列表请参考[Paraformer语音识别热词定制与管理](https://help.aliyun.com/zh/model-studio/paraformer-asr-phrase-manager)。

resource\_type

string

\-

否

固定字符串"asr\_phrase"，和"resource\_id"需同时使用。

channel\_id

array\[integer\]

\[0\]

否

指定在多音轨音频文件中需要识别的音轨索引，索引从 0 开始。例如，\[0\] 表示识别第一个音轨，\[0, 1\] 表示同时识别第一和第二个音轨。如果省略此参数，则默认处理第一个音轨。

**重要**

指定的每一个音轨都将独立计费。例如，为单个文件请求 \[0, 1\] 会产生两笔独立的费用。

disfluency\_removal\_enabled

boolean

false

否

过滤语气词，默认关闭。

timestamp\_alignment\_enabled

boolean

false

否

是否启用时间戳校准功能，默认关闭。

special\_word\_filter

string

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

array\[string\]

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

boolean

false

否

自动说话人分离，默认关闭。

仅适用于单声道音频，多声道音频不支持说话人分离。

启用该功能后，识别结果中将显示`speaker_id`字段，用于区分不同说话人。

**说明**

如果启用说话人分离功能，建议音频时长不超过2小时，否则可能导致识别失败或超时。

有关`speaker_id`的示例，请参见[识别结果说明](#a9021178ccl7s)。

speaker\_count

integer

\-

否

说话人数量参考值。取值范围为2至100的整数（包含2和100）。

开启说话人分离功能后（diarization\_enabled设置为true）生效。

默认自动判断说话人数量，如果配置此项，只能辅助算法尽量输出指定人数，无法保证一定会输出此人数。

### **响应参数**

**点击查看响应示例**

```
{
  "output": {
    "task_status": "PENDING",
    "task_id": "c2e5d63b-96e1-4607-bb91-************"
  },
  "request_id": "77ae55ae-be17-97b8-9942--************"
}
```

**参数**

**类型**

**说明**

task\_status

string

任务状态。

task\_id

string

任务ID。该ID在[查询任务接口](#480630e0582sb)中作为[请求参数](#0634617fe8jqg)传入。

## **查询任务接口**

### **基本信息**

**接口描述**

查询语音识别任务执行情况和结果。

**URL**

```
https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
```

**请求方法**

POST

**请求头**

```
Authorization: Bearer {api-key} // 需替换为您自己的API Key
```

**消息体**

无。

### **请求参数**

**点击查看请求示例**

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}' --header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

**参数**

**类型**

**默认值**

**是否必须**

**说明**

task\_id

string

\-

是

查询任务需指定其ID，该ID为[提交任务接口](#418f2ac8ecxm4)被调用后返回的`task_id`。

### **响应参数**

**点击查看响应示例**

当任务包含多个子任务时，只要存在任一子任务成功，整个任务状态将标记为`SUCCEEDED`，需通过`subtask_status`字段判断具体子任务结果。

## 正常示例

```
{
  "request_id": "f9e1afad-94d3-997e-a83b-************",
  "output": {
    "task_id": "f86ec806-4d73-485f-a24f-************",
    "task_status": "SUCCEEDED",
    "submit_time": "2024-09-12 15:11:40.041",
    "scheduled_time": "2024-09-12 15:11:40.071",
    "end_time": "2024-09-12 15:11:40.903",
    "results": [
      {
        "file_url": "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav",
        "transcription_url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/pre/filetrans-16k/20240912/15%3A11/3bdf7689-b598-409d-806a-121cff5e4a31-1.json?Expires=1726211500&OSSAccessKeyId=yourOSSAccessKeyId&Signature=Fj%2BaF%2FH0Kayj3w3My2ECBeP****%3D",
        "subtask_status": "SUCCEEDED"
      },
      {
        "file_url": "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav",
        "transcription_url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/pre/filetrans-16k/20240912/15%3A11/409a4b92-445b-4dd8-8c1d-f110954d82d8-1.json?Expires=1726211500&OSSAccessKeyId=yourOSSAccessKeyId&Signature=v5Owy5qoAfT7mzGmQgH0g8C****%3D",
        "subtask_status": "SUCCEEDED"
      }
    ],
    "task_metrics": {
      "TOTAL": 2,
      "SUCCEEDED": 2,
      "FAILED": 0
    }
  },
  "usage": {
    "duration": 9
  }
}
```

## 异常示例

“`code`”为错误码，“`message`”为错误信息，只有异常情况才有这两个字段，您可以通过这两个字段，对照[错误码](#1dd0e8e854p6w)排查问题。

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

**参数**

**类型**

**说明**

task\_id

string

被查询任务的ID。

task\_status

string

被查询任务的状态。

**说明**

当任务包含多个子任务时，只要存在任一子任务成功，整个任务状态将标记为`SUCCEEDED`，需通过`subtask_status`字段判断具体子任务结果。

subtask\_status

string

子任务状态。

file\_url

string

文件转写任务中所处理的文件URL。

transcription\_url

string

获取识别结果对应的链接。该链接有效期为24小时，超时后无法查询任务或通过先前查询结果中的URL下载结果。

识别结果保存为JSON文件，您可以通过上述链接下载该文件或直接通过HTTP请求读取该文件中的内容。

JSON数据中各字段含义请参见[识别结果说明](#a9021178ccl7s)。

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

## **其他接口：批量查询任务状态/取消任务**

详情请参见[管理异步任务](https://help.aliyun.com/zh/model-studio/manage-asynchronous-tasks)：支持批量查询24小时内提交的录音文件识别任务，同时支持取消`PENDING`（排队）状态的任务。

## **完整示例**

您可以使用编程语言自带的HTTP类库，来实现提交和查询任务的请求：先调用提交任务接口上传识别任务，然后循环调用查询任务接口，直至任务完成。

以Python为例，代码如下：

```
import requests
import json
import time

api_key = "your-dashscope-api-key"  # 在此处替换为您的API Key
file_urls = [
    "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav",
    "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav",
]
language_hints = ["zh", "en"]

# 提交文件转写任务，包含待转写文件url列表
def submit_task(apikey, file_urls) -> str:

    headers = {
        "Authorization": f"Bearer {apikey}",
        "Content-Type": "application/json",
        "X-DashScope-Async": "enable",
    }
    data = {
        "model": "paraformer-v2",
        "input": {"file_urls": file_urls},
        "parameters": {
            "channel_id": [0],
            "language_hints": language_hints
        },
    }
    # 录音文件转写服务url
    service_url = (
        "https://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription"
    )
    response = requests.post(
        service_url, headers=headers, data=json.dumps(data)
    )

    # 打印响应内容
    if response.status_code == 200:
        return response.json()["output"]["task_id"]
    else:
        print("task failed!")
        print(response.json())
        return None

# 循环查询任务状态直到成功
def wait_for_complete(task_id):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-DashScope-Async": "enable",
    }

    pending = True
    while pending:
        # 查询任务状态服务url
        service_url = f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}"
        response = requests.post(
            service_url, headers=headers
        )
        if response.status_code == 200:
            status = response.json()['output']['task_status']
            if status == 'SUCCEEDED':
                print("task succeeded!")
                pending = False
                return response.json()['output']['results']
            elif status == 'RUNNING' or status == 'PENDING':
                pass
            else:
                print("task failed!")
                pending = False
        else:
            print("query failed!")
            pending = False
        print(response.json())
        time.sleep(0.1)

task_id = submit_task(apikey=api_key, file_urls=file_urls)
print("task_id: ", task_id)
result = wait_for_complete(task_id)
print("transcription result: ", result)
```

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

如遇代码报错问题，请根据[错误码](#1dd0e8e854p6w)中的信息进行排查。

#### **Q：识别结果和语音播放不同步怎么办？**

将[请求参数](#493b0f8f2ap0y)`timestamp_alignment_enabled`设为`true`将启用时间戳校准功能，能够让识别结果和语音播放同步。

#### **Q：提交任务后返回InvalidFile.DownloadFailed错误怎么办？**

请检查文件URL中是否包含空格、中文等特殊字符。如果文件名包含空格（例如"第八节 学生伤害事故处理办法.mp4"），需要将空格替换为`%20`进行URL编码后再传入`file_urls`参数。

#### **Q：录音文件URL设置成OSS临时公网访问不通该如何处理？**

headers中将`X-DashScope-OssResourceResolve`设为`enable`。

不推荐该方式。

[Java SDK](https://help.aliyun.com/zh/model-studio/paraformer-recorded-speech-recognition-java-sdk)或者[Python SDK](https://help.aliyun.com/zh/model-studio/paraformer-recorded-speech-recognition-python-sdk)不支持对headers进行配置。

#### **Q：一直轮询不到结果？**

可能是限流原因，请耐心等待。若需扩容，请加入[开发者群](https://github.com/aliyun/alibabacloud-bailian-speech-demo)进行申请。

#### **Q：无法识别语音（无识别结果）是什么原因？**

-   请检查音频是否符合要求（格式、采样率）。
    
-   若是使用了`paraformer-v2`模型，检查`language_hints`的设置是否正确。
    
-   以上都没问题，可通过定制热词，提升对特定词语的识别效果。
    

### **更多问题**

请参见GitHub [QA](https://github.com/aliyun/alibabacloud-bailian-speech-demo/tree/master/docs/QA)。
