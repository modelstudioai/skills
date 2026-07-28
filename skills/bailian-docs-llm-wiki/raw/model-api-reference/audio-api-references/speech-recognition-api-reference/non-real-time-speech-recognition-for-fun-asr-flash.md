# 非实时语音识别（Fun-ASR-Flash）API参考

本文介绍Fun-ASR-Flash非实时语音识别HTTP API的参数和接口细节。

**用户指南：**[非实时语音识别](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide)。关于支持的音频格式、文件大小限制、时长限制等输入要求，请参见[音频规格](https://help.aliyun.com/zh/model-studio/asr-model/#asr-audio-spec02)。

**重要**

该功能不支持SDK调用。

## **服务端点**

## 华北2（北京）

`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)。

## 新加坡

`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)。

**重要**

阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，能够为推理请求提供卓越的性能和更高的稳定性，建议迁移至新域名：

-   华北2（北京）地域：从 `dashscope.aliyuncs.com` 迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
    
-   新加坡地域：从 `dashscope-intl.aliyuncs.com` 迁移至 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
    

`{WorkspaceId}`需要替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)。现有域名仍可正常使用。

## **请求头**

**参数**

**类型**

**是否必选**

**说明**

Authorization

string

是

鉴权令牌，格式为`Bearer <your_api_key>`，使用时将"`<your_api_key>`"替换为实际的API Key。

Content-Type

string

是

请求体的媒体类型，固定为`application/json`。

X-DashScope-SSE

string

是

用于控制是否以SSE流式方式返回结果。设置为`enable`时开启SSE流式返回模式，服务端会分多次返回中间识别结果和最终结果；设置为`disable`或不传该参数则仅返回最终结果。

## **请求体**

以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。

## 非流式

```
curl --location --request POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
     --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
     --header "Content-Type: application/json" \
     --header "X-DashScope-SSE: disable" \
     --data '{
    "model": "fun-asr-flash-2026-06-15",
    "input": {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_audio",
                        "input_audio": {
                            "data": "{YOUR_AUDIO_URL}"
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

## 流式

```
curl --location --request POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
     --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
     --header "Content-Type: application/json" \
     --header "X-DashScope-SSE: enable" \
     --data '{
    "model": "fun-asr-flash-2026-06-15",
    "input": {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_audio",
                        "input_audio": {
                            "data": "{YOUR_AUDIO_URL}"
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

## 携带上下文-非流式

```
curl --location --request POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
     --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
     --header "Content-Type: application/json" \
     --header "X-DashScope-SSE: disable" \
     --data '{
    "model": "fun-asr-flash-2026-06-15",
    "input": {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "你好啊"
                    }
                ]
            },
            {
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": "你好啊，我是通义千问，有什么可以帮助你的？"
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_audio",
                        "input_audio": {
                            "data": "{YOUR_AUDIO_URL}"
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

## 携带上下文-流式

```
curl --location --request POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
     --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
     --header "Content-Type: application/json" \
     --header "X-DashScope-SSE: enable" \
     --data '{
    "model": "fun-asr-flash-2026-06-15",
    "input": {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "你好啊"
                    }
                ]
            },
            {
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": "你好啊，我是通义千问，有什么可以帮助你的？"
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_audio",
                        "input_audio": {
                            "data": "{YOUR_AUDIO_URL}"
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

## Base64

可输入Base64编码数据（[Data URL](https://www.rfc-editor.org/rfc/rfc2397)），格式为：`data:<mediatype>;base64,<data>`。

-   `<mediatype>`：MIME类型
    
    因音频格式而异，例如：
    
    -   WAV：`audio/wav`
        
    -   MP3：`audio/mpeg`
        
-   `<data>`：音频转成的Base64编码的字符串
    
    Base64编码会增大体积，请控制原文件大小，确保编码后仍符合输入音频大小限制（10MB）
    
-   示例：`data:audio/wav;base64,SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4LjI5LjEwMAAAAAAAAAAAAAAA//PAxABQ/BXRbMPe4IQAhl9`
    
    **点击查看示例代码**
    
    Python
    
    ```
    import base64, pathlib
    
    # 请替换为自己的音频文件路径，确保其符合音频要求
    file_path = pathlib.Path("{YOUR_AUDIO_FILE}")
    base64_str = base64.b64encode(file_path.read_bytes()).decode()
    data_uri = f"data:audio/mpeg;base64,{base64_str}"
    ```
    
    Java
    
    ```
    import java.nio.file.*;
    import java.util.Base64;
    
    public class Main {
        /**
         * 请替换为自己的音频文件路径，确保其符合音频要求
         */
        public static String toDataUrl(String filePath) throws Exception {
            byte[] bytes = Files.readAllBytes(Paths.get(filePath));
            String encoded = Base64.getEncoder().encodeToString(bytes);
            return "data:audio/mpeg;base64," + encoded;
        }
    
        public static void main(String[] args) throws Exception {
            System.out.println(toDataUrl("{YOUR_AUDIO_FILE}"));
        }
    }
    ```
    

```
import base64, pathlib
import os
import requests

# 请替换为自己的音频文件路径，确保其符合音频要求
file_path = pathlib.Path("{YOUR_AUDIO_FILE}")
base64_str = base64.b64encode(file_path.read_bytes()).decode()
data_uri = f"data:audio/wav;base64,{base64_str}"

url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"

headers = {
    "Authorization": f"Bearer {os.environ['DASHSCOPE_API_KEY']}",
    "Content-Type": "application/json",
    "X-DashScope-SSE": "disable",
}

payload = {
    "model": "fun-asr-flash-2026-06-15",
    "input": {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_audio",
                        "input_audio": {
                            "data": data_uri,
                        },
                    }
                ],
            }
        ]
    },
    "parameters": {
        "format": "wav",
        "sample_rate": "16000",
    },
}

response = requests.post(url, headers=headers, json=payload)
print(response.status_code)
print(response.json())
```

**model** `_string_` **（必选）**

模型名称，固定为`fun-asr-flash-2026-06-15`。

**input** `_object_` **（必选）**

输入信息。

**属性**

**messages** `_array(object)_` **（必选）**

消息列表。包含当前待识别的音频，以及可选的对话上下文（用于提升识别效果）。

**重要**

上下文功能用于提升专有词汇的识别准确率，使用方法详见[快速开始](https://help.aliyun.com/zh/model-studio/improve-asr-accuracy#ctx-quickstart-sec)。约束：上下文消息（`input_text` 和 `text` 类型）各最多 5 条，超出时保留最近的 5 条。每轮上下文文本总长度（`user` 和 `assistant` 的 `text` 字段长度之和）不超过 400 个字符（按字符数计算，每个字符计为 1），超出部分从末尾截断。

**重要**

携带上下文时，`messages` 中的消息顺序有要求：上下文消息必须按对话轮次排列，每轮中 `user`（`input_text` 类型）必须在对应的 `assistant`（`text` 类型）之前；包含 `input_audio` 的 `user` 消息必须放在 `messages` 数组的最后。

**属性**

**role** `_string_` **（必选）**

消息角色。取值范围：

-   `user`（必选）：用户消息。type为`input_audio`时表示当前待识别的音频；type为`input_text`时表示前几轮的识别结果或领域相关的词表（可选，上下文）。
    
-   `assistant`（可选，上下文）：前几轮大语言模型的回复内容。
    

**content** `_array(object)_` **（必选）**

消息内容列表。

**属性**

**type** `_string_` **（必选）**

内容类型。每个请求至少需要一条`input_audio`类型的消息。取值范围：

-   `input_audio`（必选）：当前待识别的音频输入（role为user），需同时传入`input_audio`对象。
    
-   `input_text`（可选，上下文）：前几轮用户语音的识别结果或领域相关的词表（role为user），需同时传入`text`字段。
    
-   `text`（可选，上下文）：前几轮大语言模型的回复内容（role为assistant），需同时传入`text`字段。
    

**input\_audio** `_object_` **（条件必选）**

当`type`为`input_audio`时必填。

**属性**

**data** `_string_` **（必选）**

待识别音频数据。关于支持的音频格式、文件大小限制、时长限制等输入要求，请参见[音频规格](https://help.aliyun.com/zh/model-studio/asr-model/#asr-audio-spec02)。支持以下两种方式：

-   **音频文件URL**：直接传入可公开访问的音频文件地址。
    
-   **Base64 Data URI**：采用Data URI格式传入Base64编码的音频数据，值由`data:{MIME_TYPE};base64,`前缀与Base64编码的音频数据拼接而成。支持的MIME类型包括`audio/wav`、`audio/mp3`等。
    

示例（URL方式）：`https://example.com/audio/sample.wav`

示例（Base64方式）：`data:audio/wav;base64,{BASE64_ENCODED_DATA}`

**text** `_string_` **（条件必选）**

当`type`为`input_text`时，填入前几轮用户语音的识别结果或领域相关的词表；当`type`为`text`时，填入前几轮大语言模型的回复内容。文本按字符数计算，每个字符计为 1。每轮上下文中所有消息的 `text` 字段长度之和不超过 400 个字符，超出部分从末尾截断。

**parameters** `_object_` **（必选）**

模型参数。

**属性**

**format** `_string_` **（必选）**

音频格式。根据实际音频格式填写，支持`wav`、`mp3`、`opus`等。详情请参见[音频规格](https://help.aliyun.com/zh/model-studio/asr-model/#asr-audio-spec02)。

**sample\_rate** `_string_` （可选）

音频采样率，单位Hz。例如`16000`表示16kHz采样率。详情请参见[音频规格](https://help.aliyun.com/zh/model-studio/asr-model/#asr-audio-spec02)。

## **返回体**

## 非流式

```
{
    "output": {
        "sentence": {
            "begin_time": 760,
            "channel_id": 0,
            "end_time": 3800,
            "sentence_end": true,
            "sentence_id": 1,
            "text": "Hello World，这里是阿里巴巴语音实验室。",
            "words": [
                {"begin_time": 760, "end_time": 1040, "fixed": true, "punctuation": "", "text": "Hello"},
                {"begin_time": 1040, "end_time": 1240, "fixed": true, "punctuation": "，", "text": " World"},
                {"begin_time": 1360, "end_time": 1880, "fixed": true, "punctuation": "", "text": "这里是"},
                {"begin_time": 1880, "end_time": 2520, "fixed": true, "punctuation": "", "text": "阿里巴巴"},
                {"begin_time": 2520, "end_time": 2840, "fixed": true, "punctuation": "", "text": "语音"},
                {"begin_time": 2840, "end_time": 3800, "fixed": true, "punctuation": "。", "text": "实验室"}
            ]
        },
        "text": "Hello World，这里是阿里巴巴语音实验室。"
    },
    "usage": {
        "duration": 4
    },
    "request_id": "40e0734d-096f-9ae3-86c1-a8c013287561"
}
```

## 流式

设置`X-DashScope-SSE: enable`时，服务端以Server-Sent Events协议返回识别结果。SSE事件格式如下：

```
id:{序列号}
event:result
:HTTP_STATUS/200
data:{JSON数据}
```

返回示例：

```
id:1
event:result
:HTTP_STATUS/200
data:{"output":{"sentence":{"sentence_id":1,"sentence_end":true,"end_time":3800,"words":[{"end_time":1040,"punctuation":"","begin_time":760,"fixed":true,"text":"Hello"},{"end_time":1240,"punctuation":"，","begin_time":1040,"fixed":true,"text":" World"},{"end_time":1880,"punctuation":"","begin_time":1360,"fixed":true,"text":"这里是"},{"end_time":2520,"punctuation":"","begin_time":1880,"fixed":true,"text":"阿里巴巴"},{"end_time":2840,"punctuation":"","begin_time":2520,"fixed":true,"text":"语音"},{"end_time":3800,"punctuation":"。","begin_time":2840,"fixed":true,"text":"实验室"}],"begin_time":760,"text":"Hello World，这里是阿里巴巴语音实验室。","channel_id":0},"text":"Hello World，这里是阿里巴巴语音实验室。"},"usage":{"duration":4},"request_id":"fc1582e4-935c-9fc2-a482-a98bf43daa69"}
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
