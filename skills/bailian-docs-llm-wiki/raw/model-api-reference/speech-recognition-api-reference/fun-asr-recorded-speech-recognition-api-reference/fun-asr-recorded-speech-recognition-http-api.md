# Fun-ASR录音文件识别HTTP API参考

本文介绍Fun-ASR录音文件识别HTTP API的参数和接口细节。

**用户指南：**关于模型介绍和选型建议请参见[语音识别](https://help.aliyun.com/zh/model-studio/asr-model/)。

## **DashScope异步调用**

### **流程说明**

与DashScope同步调用（一次请求、立即返回结果）不同，异步调用专为处理长音频文件或耗时较长的任务设计，该模式采用“提交-轮询”的两步式流程，避免了因长时间等待而导致的请求超时：

1.  第一步：提交任务
    
    -   客户端发起一个异步处理请求。
        
    -   服务器验证请求后，不会立即执行任务，而是返回一个唯一的 `task_id`，表示任务已成功创建。
        
2.  第二步：获取结果
    
    -   客户端使用获取到的 `task_id`，通过轮询方式反复调用结果查询接口。
        
    -   当任务处理完成后，结果查询接口将返回最终的识别结果。
        

### **服务端点**

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

提交任务接口：`POST https://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription`

查询任务接口：`GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

提交任务接口：`POST https://dashscope-intl.aliyuncs.com/api/v1/services/audio/asr/transcription`

查询任务接口：`GET https://dashscope-intl.aliyuncs.com/api/v1/tasks/{task_id}`

### **请求头**

**参数**

**类型**

**是否必选**

**说明**

Authorization

string

是

鉴权令牌，格式为`Bearer <your_api_key>`，使用时，将"`<your_api_key>`"替换为实际的API Key。提交任务接口和查询任务接口均需要传入。

Content-Type

string

是

请求体的媒体类型。仅提交任务接口需要传入，固定为`application/json`。

X-DashScope-Async

string

是

异步任务标识。仅提交任务接口需要传入，固定为`enable`，请勿遗漏，否则无法提交任务。

### **提交任务接口**

提交语音识别任务。该接口异步返回，业务侧需结合[查询任务接口](#480630e0582sb)轮询任务状态。

#### **请求体**

以下为北京地域URL，若使用新加坡地域的模型，需将URL替换为：`https://dashscope-intl.aliyuncs.com/api/v1/services/audio/asr/transcription`。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription' \
     --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
     --header "Content-Type: application/json" \
     --header "X-DashScope-Async: enable" \
     --data '{
    "model": "fun-asr",
    "input": {
        "file_urls": [
            "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav",
            "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav"
        ]
    },
    "parameters": {
        "channel_id": [0]
    }
}'
```

**model** `_string_` **（必选）**

指定用于音视频文件转写的模型名。

取值范围：

-   fun-asr
    
-   fun-asr-2025-11-07
    
-   fun-asr-2025-08-25
    
-   fun-asr-mtl
    
-   fun-asr-mtl-2025-08-25
    

**input** `_object_` **（必选）**

输入参数对象。

**属性**

**file\_urls** `_array[string]_` **（必选）**

音视频文件转写的URL列表，支持HTTP / HTTPS协议，单次请求最多支持100个URL。

若录音文件存储在阿里云OSS，使用RESTful API方式支持使用以`oss://`为前缀的临时 URL。

**重要**

-   临时 URL 有效期48小时，过期后无法使用，**请勿用于生产环境。**
    
-   文件上传凭证接口限流为 100 QPS 且不支持扩容，**请勿用于生产环境、高并发及压测场景。**
    
-   生产环境建议使用[阿里云OSS](https://help.aliyun.com/zh/oss/user-guide/what-is-oss) 等稳定存储，确保文件长期可用并规避限流问题。
    
-   录音文件URL设置成OSS临时公网访问不通该如何处理？[请求头](#h2-hd)中将`X-DashScope-OssResourceResolve`设为`enable`（不推荐该方式）。
    
    Java SDK或者Python SDK不支持对请求头进行配置。
    

**parameters** `_object_` （可选）

请求参数对象。

**属性**

**vocabulary\_id** `_string_` （可选）

热词ID，此次语音识别中生效此热词ID对应的热词信息。默认不启用。使用方法请参考[定制热词](https://help.aliyun.com/zh/model-studio/custom-hot-words/)。

**channel\_id** `_array[integer]_` （可选）

指定在多音轨音频文件中需要识别的音轨索引，索引从 0 开始。例如，\[0\] 表示识别第一个音轨，\[0, 1\] 表示同时识别第一和第二个音轨。如果省略此参数，则默认处理第一个音轨。

**重要**

指定的每一个音轨都将独立计费。例如，为单个文件请求 \[0, 1\] 会产生两笔独立的费用。

默认值：\[0\]。

**special\_word\_filter** `_string_` （可选）

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
        

**diarization\_enabled** `_boolean_` （可选）

自动说话人分离，默认关闭。

仅适用于单声道音频，多声道音频不支持说话人分离。

启用该功能后，识别结果中将显示`speaker_id`字段，用于区分不同说话人。

**说明**

如果启用说话人分离功能，建议音频时长不超过2小时，否则可能导致识别失败或超时。

有关`speaker_id`的示例，请参见[识别结果说明](#5882b67243tcg)。

默认值：false。

**speaker\_count** `_integer_` （可选）

**重要**

仅在开启说话人分离功能（`diarization_enabled`设置为`true`）时生效。

说话人数量参考值。取值范围为2至100的整数（包含2和100）。

默认自动判断说话人数量，如果配置此项，只能辅助算法尽量输出指定人数，无法保证一定会输出此人数。

**language\_hints** `_array[string]_` （可选）

设置待识别语言代码。如果无法提前确定语种，可不设置，模型会自动识别语种。

系统仅读取数组中的首个值。多余值将被忽略。

不同模型支持的语言代码如下：

-   fun-asr、fun-asr-2025-11-07、fun-asr-mtl、fun-asr-mtl-2025-08-25：
    
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
        
-   fun-asr-2025-08-25：
    
    -   zh: 中文
        
    -   en: 英文
        

#### **返回体**

```
{
  "output": {
    "task_status": "PENDING",
    "task_id": "c2e5d63b-96e1-4607-bb91-************"
  },
  "request_id": "77ae55ae-be17-97b8-9942--************"
}
```

**request\_id** `_string_`

本次调用的唯一标识符。

**output** `_object_`

提交任务返回的数据。

**属性**

**task\_id** `_string_`

任务ID。该ID在[查询任务接口](#480630e0582sb)中作为[string](#0634617fe8jqg)传入。

**task\_status** `_string_`

任务状态。提交成功时返回`PENDING`。

### **查询任务接口**

查询语音识别任务的执行情况和结果。建议轮询调用直至任务终态。

#### **请求体**

以下为北京地域URL，若使用新加坡地域的模型，需将URL替换为：`https://dashscope-intl.aliyuncs.com/api/v1/tasks/{task_id}`。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}' \
     --header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

**task\_id** `_string_` **（必选）**

**重要**

该参数为URL路径参数，无请求体。

查询任务需指定其ID，该ID为[提交任务接口](#418f2ac8ecxm4)被调用后返回的`task_id`。

#### **返回体**

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

**request\_id** `_string_`

本次调用的唯一标识符。

**output** `_object_`

查询任务返回的数据。

**属性**

**task\_id** `_string_`

被查询任务的ID。

**task\_status** `_string_`

被查询任务的状态。

**说明**

当任务包含多个子任务时，只要存在任一子任务成功，整个任务状态将标记为`SUCCEEDED`，需通过`subtask_status`字段判断具体子任务结果。

**submit\_time** `_string_`

任务提交时间。

**scheduled\_time** `_string_`

任务被调度执行的时间。

**end\_time** `_string_`

任务结束时间。

**results** `_array[object]_`

每个待识别音频文件对应的子任务结果列表。

**属性**

**subtask\_status** `_string_`

子任务状态。

**file\_url** `_string_`

文件转写任务中所处理的文件URL。

**transcription\_url** `_string_`

获取识别结果对应的链接。该链接有效期为24小时，超时后无法查询任务或通过先前查询结果中的URL下载结果。

识别结果保存为JSON文件，您可以通过上述链接下载该文件或直接通过HTTP请求读取该文件中的内容。JSON数据中各字段含义请参见[识别结果说明](#5882b67243tcg)。

**code** `_string_`

**重要**

仅当子任务失败时返回。

子任务失败的错误码。

**message** `_string_`

**重要**

仅当子任务失败时返回。

子任务失败的错误信息。

**task\_metrics** `_object_`

任务整体执行情况统计。

**属性**

**TOTAL** `_integer_`

子任务总数。

**SUCCEEDED** `_integer_`

成功的子任务数。

**FAILED** `_integer_`

失败的子任务数。

### **其他接口：批量查询任务状态/取消任务**

详情请参见[管理异步任务](https://help.aliyun.com/zh/model-studio/manage-asynchronous-tasks)：支持批量查询24小时内提交的录音文件识别任务，同时支持取消`PENDING`（排队）状态的任务。

### **识别结果说明**

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

original\_duration\_in\_milliseconds

integer

源文件中的原始音频时长（ms）。

channel\_id

integer

转写结果的音轨索引，以0为起始。

content\_duration

integer

音轨中被判定为语音内容的时长（ms）。

**重要**

语音识别模型服务仅对音轨中被判定为语音内容的时长进行语音转写，并据此进行计量计费，非语音内容不计量、不计费。通常情况下语音内容时长会短于原始音频时长。由于对是否存在语音内容的判定是由AI模型给出的，可能与实际情况存在一定误差。

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

## **DashScope同步调用**

**重要**

该功能只支持北京地域。

### **服务端点**

`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

### **请求头**

**参数**

**类型**

**是否必选**

**说明**

Authorization

string

是

鉴权令牌，格式为`Bearer <your_api_key>`，使用时将“`<your_api_key>`”替换为实际的API Key。

Content-Type

string

是

请求体的媒体类型，固定为`application/json`。

X-DashScope-SSE

string

是

用于控制是否以SSE流式方式返回结果。设置为`enable`时开启SSE流式返回模式，服务端会分多次返回中间识别结果和最终结果；设置为`disable`或不传该参数则仅返回最终结果。

### **请求体**

## 非流式

```
curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
     --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
     --header "Content-Type: application/json" \
     --header "X-DashScope-SSE: disable" \
     --data '{
    "model": "fun-asr-realtime",
    "input": {
        "messages": []
    },
    "parameters": {
        "audio_address": "https://example.com/audio/sample.mp3",
        "format": "mp3"
    },
    "resources": []
}'
```

## 流式

```
curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
     --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
     --header "Content-Type: application/json" \
     --header "X-DashScope-SSE: enable" \
     --data '{
    "model": "fun-asr-realtime",
    "input": {
        "messages": []
    },
    "parameters": {
        "audio_address": "https://example.com/audio/sample.mp3",
        "format": "mp3"
    },
    "resources": []
}'
```

**model** `_string_` **（必选）**

模型名称。默认值`fun-asr-realtime`。

取值范围：

-   `fun-asr-realtime`（稳定版模型）
    
-   `fun-asr-realtime-2026-02-28`（即 Fun-Realtime-ASR-preview）
    

**input** `_object_` **（条件必选）**

输入信息。与输入音频文件URL方式（通过`parameters.audio_address`传入）二选一，使用Base64方式上传音频时需要填写。

**属性**

**messages** `_array(object)_` **（必选）**

消息列表。

**属性**

**content** `_array(object)_` **（必选）**

用户消息的内容。仅允许设置一组消息。

**属性**

**audio** `_string_` **（必选）**

待识别音频，采用Data URI格式传入Base64编码的音频数据。

使用Base64方式上传音频时需要填写。

值由`data:{MIME_TYPE};base64,`前缀与Base64编码的音频数据拼接而成。支持的MIME类型包括`audio/wav`、`audio/mp3`等。

示例：`data:audio/wav;base64,{BASE64_ENCODED_DATA}`

**role** `_string_` **（必选）**

用户消息的角色，固定为`user`。使用Base64方式上传音频时需要填写。

**parameters** `_object_` **（必选）**

模型参数。

**属性**

**audio\_address** `_string_` **（条件必选）**

音频文件URL地址。与Base64方式（通过`input.messages`传入）二选一，使用URL方式时必填。需为可公开访问的地址。

**format** `_string_` **（必选）**

音频格式。根据实际音频格式填写，支持`wav`、`mp3`、`opus`等。

**vad\_enabled** `_boolean_` （可选）

是否启用端点检测（VAD）。

默认为`true`（启用 VAD 检测）。

设为 `false` 时关闭 VAD 检测；但当音频时长超过 1 分钟时，系统将自动启用 VAD 检测，忽略此参数设置。

**resources** `_array_` （可选）

资源列表，预留字段，当前可传空数组`[]`。

### **返回体**

## 非流式

```
{
    "output": {
        "sentence": {
            "begin_time": 160,
            "channel_id": 0,
            "end_time": 1680,
            "sentence_end": true,
            "sentence_id": 1,
            "text": "欢迎使用阿里云。",
            "words": [
                {"begin_time": 160, "end_time": 520, "fixed": true, "punctuation": "", "text": "欢迎"},
                {"begin_time": 520, "end_time": 880, "fixed": true, "punctuation": "", "text": "使用"},
                {"begin_time": 880, "end_time": 1280, "fixed": true, "punctuation": "", "text": "阿里"},
                {"begin_time": 1280, "end_time": 1680, "fixed": true, "punctuation": "。", "text": "云"}
            ]
        },
        "text": "欢迎使用阿里云。"
    },
    "usage": {
        "duration": 2
    },
    "request_id": "eff4c092-2289-9b43-a4cd-80e591fa90f5"
}
```

## 流式

设置`X-DashScope-SSE: enable`时，服务端以Server-Sent Events协议分多次返回中间识别结果和最终结果。每个SSE事件格式如下：

```
id:{序列号}
event:result
:HTTP_STATUS/200
data:{JSON数据}
```

中间结果（句子开始、词逐步增长）：

```
id:1
event:result
:HTTP_STATUS/200
data:{"output":{"sentence":{"sentence_id":1,"sentence_end":false,"sentence_begin":true,"words":[],"begin_time":0,"text":"","channel_id":0},"text":""},"request_id":"372d19b3-993f-9288-adf0-a99f7606bd30"}

id:2
event:result
:HTTP_STATUS/200
data:{"output":{"sentence":{"words":[{"end_time":520,"punctuation":"","begin_time":160,"fixed":false,"text":"欢迎"}],"begin_time":160,"text":"欢迎","channel_id":0,"sentence_id":1,"sentence_end":false},"text":"欢迎"},"request_id":"372d19b3-993f-9288-adf0-a99f7606bd30"}

id:3
event:result
:HTTP_STATUS/200
data:{"output":{"sentence":{"words":[{"end_time":520,"punctuation":"","begin_time":160,"fixed":false,"text":"欢迎"},{"end_time":880,"punctuation":"","begin_time":520,"fixed":false,"text":"使用"}],"begin_time":160,"text":"欢迎使用","channel_id":0,"sentence_id":1,"sentence_end":false},"text":"欢迎使用"},"request_id":"372d19b3-993f-9288-adf0-a99f7606bd30"}
```

最终结果（句子结束，包含`usage`）：

```
id:4
event:result
:HTTP_STATUS/200
data:{"output":{"sentence":{"sentence_id":1,"sentence_end":true,"end_time":1680,"words":[{"end_time":520,"punctuation":"","begin_time":160,"fixed":true,"text":"欢迎"},{"end_time":880,"punctuation":"","begin_time":520,"fixed":true,"text":"使用"},{"end_time":1280,"punctuation":"","begin_time":880,"fixed":true,"text":"阿里"},{"end_time":1680,"punctuation":"。","begin_time":1280,"fixed":true,"text":"云"}],"begin_time":160,"text":"欢迎使用阿里云。","channel_id":0},"text":"欢迎使用阿里云。"},"usage":{"duration":2},"request_id":"372d19b3-993f-9288-adf0-a99f7606bd30"}
```

**request\_id** `_string_`

本次请求的唯一标识。

**output** `_object_`

输出结果。

**属性**

**text** `_string_`

当前累积的完整识别文本。

**sentence** `_object_`

当前句子的详细信息。

**属性**

**sentence\_id** `_integer_`

句子编号，从1开始。

**sentence\_end** `_boolean_`

是否为该句的最终结果。为`true`时表示该句识别完成。

**begin\_time** `_integer_`

句子开始时间，单位毫秒。

**end\_time** `_integer_`

句子结束时间，单位毫秒。仅在`sentence_end`为`true`时返回。

**text** `_string_`

当前句子的识别文本。

**channel\_id** `_integer_`

声道编号，从0开始。

**words** `_array_`

词级别时间戳列表。

**属性**

**text** `_string_`

词文本。

**begin\_time** `_integer_`

词开始时间，单位毫秒。

**end\_time** `_integer_`

词结束时间，单位毫秒。

**punctuation** `_string_`

词后的标点符号。无标点时为空字符串。

**fixed** `_boolean_`

词是否已稳定。`false`表示后续事件中该词的时间戳可能调整。

**usage** `_object_`

用量信息。仅在`sentence_end`为`true`时返回。

**属性**

**duration** `_integer_`

已处理的音频时长，单位秒。

### **SSE 流式结果处理逻辑**

在流式模式下，客户端需关注以下处理要点：

1.  每收到一个SSE事件，解析`data`字段中的JSON。
    
2.  通过`output.sentence.sentence_end`判断当前句子是否结束：当该值为`true`时，该句识别完成，词级时间戳已稳定，可作为最终结果使用；当该值为`false`时，识别仍在进行中，文本和时间戳可能在后续事件中更新。
    
3.  `usage`信息仅在句子结束事件中返回，可用于计量音频处理时长。
