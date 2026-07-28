# 非实时语音识别（Fun-ASR-Realtime）API参考

本文介绍Fun-ASR-Realtime非实时语音识别HTTP API的参数和接口细节。

**用户指南：**[非实时语音识别](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide)。关于支持的音频格式、文件大小限制、时长限制等输入要求，请参见[音频规格](https://help.aliyun.com/zh/model-studio/asr-model/#asr-audio-spec02)。

**重要**

-   该功能只支持北京地域。
    
-   不支持SDK调用。
    

## **服务端点**

`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)。

**重要**

阿里云百炼为华北2（北京）地域推出了业务空间专属域名，能够为推理请求提供卓越的性能和更高的稳定性，建议从 `dashscope.aliyuncs.com` 迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`。

`{WorkspaceId}`需要替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)。现有域名仍可正常使用。

## **请求头**

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

## **请求体**

## 非流式

```
curl --location --request POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
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
curl --location --request POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
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

模型名称。

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

待识别音频，采用Data URI格式传入Base64编码的音频数据。关于支持的音频格式、文件大小限制、时长限制等输入要求，请参见[音频规格](https://help.aliyun.com/zh/model-studio/asr-model/#asr-audio-spec02)。

使用Base64方式上传音频时需要填写。

值由`data:{MIME_TYPE};base64,`前缀与Base64编码的音频数据拼接而成。支持的MIME类型包括`audio/wav`、`audio/mp3`等。

示例：`data:audio/wav;base64,{BASE64_ENCODED_DATA}`

**role** `_string_` **（必选）**

用户消息的角色，固定为`user`。使用Base64方式上传音频时需要填写。

**parameters** `_object_` **（必选）**

模型参数。

**属性**

**audio\_address** `_string_` **（条件必选）**

音频文件URL地址。与Base64方式（通过`input.messages`传入）二选一，使用URL方式时必填。需为可公开访问的地址。关于支持的音频格式、文件大小限制、时长限制等输入要求，请参见[音频规格](https://help.aliyun.com/zh/model-studio/asr-model/#asr-audio-spec02)。

**format** `_string_` **（必选）**

音频格式。根据实际音频格式填写，支持`wav`、`mp3`、`opus`等。详情请参见[音频规格](https://help.aliyun.com/zh/model-studio/asr-model/#asr-audio-spec02)。

**vad\_enabled** `_boolean_` （可选）

是否启用端点检测（VAD）。

默认为`true`（启用 VAD 检测）。

设为 `false` 时关闭 VAD 检测；但当音频时长超过 1 分钟时，系统将自动启用 VAD 检测，忽略此参数设置。

**resources** `_array_` （可选）

资源列表，预留字段，当前可传空数组`[]`。

## **返回体**

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

## **SSE 流式结果处理逻辑**

在流式模式下，客户端需关注以下处理要点：

1.  每收到一个SSE事件，解析`data`字段中的JSON。
    
2.  通过`output.sentence.sentence_end`判断当前句子是否结束：当该值为`true`时，该句识别完成，词级时间戳已稳定，可作为最终结果使用；当该值为`false`时，识别仍在进行中，文本和时间戳可能在后续事件中更新。
    
3.  `usage`信息仅在句子结束事件中返回，可用于计量音频处理时长。
