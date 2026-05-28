# 声音设计API参考

本文介绍声音设计的HTTP API接口详情，包括创建音色、查询音色列表、查询音色详情和删除音色四个操作。

**用户指南：**[声音设计](https://help.aliyun.com/zh/model-studio/voice-design-user-guide)。

## **服务端点**

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

`POST https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization`

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

`POST https://dashscope-intl.aliyuncs.com/api/v1/services/audio/tts/customization`

## **请求头**

**参数**

**类型**

**是否必选**

**说明**

Authorization

string

是

鉴权令牌，格式为`Bearer <your_api_key>`，使用时，将"`<your_api_key>`"替换为实际的API Key。

Content-Type

string

是

请求体的媒体类型。固定为`application/json`。

## **创建音色**

### **请求体**

以下为北京地域URL，若使用新加坡地域的模型，需将URL替换为：`https://dashscope-intl.aliyuncs.com/api/v1/services/audio/tts/customization`。

## CosyVoice声音设计

```
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "voice-enrollment",
    "input": {
        "action": "create_voice",
        "target_model": "cosyvoice-v3.5-plus",
        "voice_prompt": "沉稳的中年男性，音色低沉浑厚",
        "preview_text": "各位听众朋友，大家好",
        "prefix": "announcer",
        "language_hints": ["zh"]
    },
    "parameters": {
        "sample_rate": 24000,
        "response_format": "wav"
    }
}'
```

## Qwen声音设计

```
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-voice-design",
    "input": {
        "action": "create",
        "target_model": "qwen3-tts-vd-realtime-2026-01-15",
        "preferred_name": "announcer",
        "voice_prompt": "沉稳的中年男性，音色低沉浑厚",
        "preview_text": "各位听众朋友，大家好",
        "language": "zh"
    },
    "parameters": {
        "sample_rate": 24000,
        "response_format": "wav"
    }
}'
```

**model** `_string_` **（必选）**

声音设计模型。取值：

-   `voice-enrollment`：CosyVoice声音设计。
    
-   `qwen-voice-design`：Qwen声音设计。
    

**input** `_object_` **（必选）**

输入参数对象。

**属性**

**action** `_string_` **（必选）**

操作类型。

-   CosyVoice（`voice-enrollment`）：固定为`create_voice`。
    
-   Qwen（`qwen-voice-design`）：固定为`create`。
    

**target\_model** `_string_` **（必选）**

驱动音色的语音合成模型。必须与后续调用语音合成接口时使用的模型一致，否则合成会失败。

**voice\_prompt** `_string_` **（必选）**

声音描述文本，仅支持中文和英文。

-   CosyVoice（`voice-enrollment`）：最大长度500字符。
    
-   Qwen（`qwen-voice-design`）：最大长度2048字符。
    

**preview\_text** `_string_` **（必选）**

预览音频对应的文本。

-   CosyVoice（`voice-enrollment`）：最大长度200字符，支持中文和英文。
    
-   Qwen（`qwen-voice-design`）：最大长度1024字符，支持中文、英文、德语、意大利语、葡萄牙语、西班牙语、日语、韩语、法语、俄语。
    

**prefix** `_string_` **（条件必选）**

**重要**

仅适用于CosyVoice（model为`voice-enrollment`时）。

音色名称前缀，仅允许数字和英文字母，不超过10个字符。生成的音色名格式：`{target_model}-vd-{prefix}-{唯一标识}`

**preferred\_name** `_string_` **（条件必选）**

**重要**

仅适用于Qwen（model为`qwen-voice-design`时）。

音色名称前缀，仅允许数字、英文字母和下划线，不超过16个字符。

**language\_hints** `_array[string]_` （可选）

**重要**

仅适用于CosyVoice（model为`voice-enrollment`时）。

指定生成音色的语言倾向，影响音色的语言特征和发音倾向，建议根据实际使用场景选择对应语言代码。若使用该参数，设置的语种须与 `preview_text` 的语种一致。

此参数为数组，但当前版本仅处理第一个元素。

取值范围：

-   zh：中文
    
-   en：英文
    

默认值：\["zh"\]。

**language** `_string_` （可选）

**重要**

仅适用于Qwen（model为`qwen-voice-design`时）。

指定生成音色的语言倾向，影响音色的语言特征和发音倾向，建议根据实际使用场景选择对应语言代码。若使用该参数，设置的语种须与 `preview_text` 的语种一致。

取值范围：

-   zh：中文
    
-   en：英文
    
-   de：德语
    
-   it：意大利语
    
-   pt：葡萄牙语
    
-   es：西班牙语
    
-   ja：日语
    
-   ko：韩语
    
-   fr：法语
    
-   ru：俄语
    

默认值：zh。

**parameters** `_object_` （可选）

声音设计的参数配置。

**属性**

**sample\_rate** `_int_` （可选）

预览音频采样率（Hz）。

-   CosyVoice支持：16000、24000、48000。
    
-   Qwen支持：8000、16000、24000、48000。
    

默认值：24000。

**response\_format** `_string_` （可选）

预览音频格式。

-   CosyVoice支持：pcm、wav、mp3。
    
-   Qwen支持：pcm、wav、mp3、opus。
    

默认值：wav。

### **返回体**

## CosyVoice声音设计

```
{
    "output": {
        "preview_audio": {
            "data": "{base64_encoded_audio}",
            "sample_rate": 24000,
            "response_format": "wav"
        },
        "target_model": "cosyvoice-v3.5-plus",
        "voice_id": "cosyvoice-v3.5-plus-vd-announcer-xxxxxx"
    },
    "usage": {
        "count": 1
    },
    "request_id": "xxxx-xxxx-xxxx"
}
```

## Qwen声音设计

```
{
    "output": {
        "preview_audio": {
            "data": "{base64_encoded_audio}",
            "sample_rate": 24000,
            "response_format": "wav"
        },
        "target_model": "qwen3-tts-vd-realtime-2026-01-15",
        "voice": "yourVoice"
    },
    "usage": {
        "count": 1
    },
    "request_id": "xxxx-xxxx-xxxx"
}
```

**重要**

CosyVoice返回`voice_id`字段，Qwen返回`voice`字段。

**request\_id** `_string_`

本次调用的唯一标识符。

**output** `_object_`

模型返回的数据。

**属性**

**voice\_id / voice** `_string_`

音色ID。CosyVoice返回`voice_id`，Qwen返回`voice`。可直接用于语音合成接口的voice参数。

**preview\_audio** `_object_`

预览音频数据。

**属性**

**data** `_string_`

预览音频数据，Base64编码。

**sample\_rate** `_int_`

预览音频采样率（Hz）。

**response\_format** `_string_`

预览音频格式。

**target\_model** `_string_`

驱动音色的语音合成模型。

**usage** `_object_`

本次请求用量信息。

**属性**

**count** `_integer_`

创建的音色数量，固定为1。

## **查询音色列表**

### **请求体**

以下为北京地域URL，若使用新加坡地域的模型，需将URL替换为：`https://dashscope-intl.aliyuncs.com/api/v1/services/audio/tts/customization`。

## CosyVoice

```
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "voice-enrollment",
    "input": {
        "action": "list_voice",
        "prefix": "myvoice",
        "page_size": 10,
        "page_index": 0
    }
}'
```

## Qwen声音设计

```
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-voice-design",
    "input": {
        "action": "list",
        "page_size": 10,
        "page_index": 0
    }
}'
```

**model** `_string_` **（必选）**

声音设计模型。取值：

-   `voice-enrollment`：CosyVoice声音设计。
    
-   `qwen-voice-design`：Qwen声音设计。
    

**input** `_object_` **（必选）**

输入参数对象。

**属性**

**action** `_string_` **（必选）**

操作类型。CosyVoice：`list_voice`。Qwen：`list`。

**prefix** `_string_` （可选）

**重要**

仅适用于CosyVoice。

按前缀筛选音色。

**page\_index** `_integer_` （可选）

页码索引。

**page\_size** `_integer_` （可选）

每页包含数据条数。

### **返回体**

## CosyVoice

```
{
    "output": {
        "voice_list": [
            {
                "voice_id": "cosyvoice-v3.5-plus-vd-announcer-xxxxxx",
                "gmt_create": "2025-12-10 14:54:09",
                "gmt_modified": "2025-12-10 17:47:48",
                "status": "OK",
                "voice_prompt": "沉稳的中年男性播音员",
                "preview_text": "各位听众朋友们，大家好"
            }
        ]
    },
    "usage": {
        "count": 1
    },
    "request_id": "xxxx-xxxx-xxxx"
}
```

## Qwen

```
{
    "output": {
        "page_index": 0,
        "page_size": 10,
        "total_count": 1,
        "voice_list": [
            {
                "voice": "yourVoice",
                "gmt_create": "2025-08-11 17:59:32",
                "gmt_modified": "2025-08-11 17:59:32",
                "language": "zh",
                "target_model": "qwen3-tts-vd-realtime-2026-01-15",
                "voice_prompt": "沉稳的中年男性播音员",
                "preview_text": "各位听众朋友们，大家好"
            }
        ]
    },
    "usage": {
        "count": 0
    },
    "request_id": "xxxx-xxxx-xxxx"
}
```

**重要**

CosyVoice返回`voice_list`数组，每项包含`voice_id`字段；Qwen同样返回`voice_list`数组，每项包含`voice`字段。Qwen的output中还包含`page_index`、`page_size`和`total_count`分页信息字段。

**request\_id** `_string_`

本次调用的唯一标识符。

**output** `_object_`

模型返回的数据。

**属性**

**page\_index** `_integer_`

**重要**

仅Qwen返回。

当前页码索引。

**page\_size** `_integer_`

**重要**

仅Qwen返回。

每页数据条数。

**total\_count** `_integer_`

**重要**

仅Qwen返回。

音色总数。

**voice\_list** `_array[object]_`

查询到的音色列表。

**属性**

**voice\_id / voice** `_string_`

音色ID。CosyVoice为`voice_id`，Qwen为`voice`。

**gmt\_create** `_string_`

创建时间。

**gmt\_modified** `_string_`

修改时间。

**status** `_string_`

**重要**

仅CosyVoice返回。

音色状态，取值参见"音色状态说明"。

**target\_model** `_string_`

**重要**

仅Qwen返回。

驱动音色的语音合成模型。

**language** `_string_`

音色语言。

**voice\_prompt** `_string_`

声音描述文本。

**preview\_text** `_string_`

预览音频文本。

**usage** `_object_`

本次请求用量信息。

**属性**

**count** `_integer_`

CosyVoice固定为1。Qwen固定为0。

## **查询音色详情**

### **请求体**

以下为北京地域URL，若使用新加坡地域的模型，需将URL替换为：`https://dashscope-intl.aliyuncs.com/api/v1/services/audio/tts/customization`。

## CosyVoice

```
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "voice-enrollment",
    "input": {
        "action": "query_voice",
        "voice_id": "yourVoiceId"
    }
}'
```

## Qwen声音设计

```
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-voice-design",
    "input": {
        "action": "query",
        "voice": "yourVoice"
    }
}'
```

**model** `_string_` **（必选）**

声音设计模型。取值：

-   `voice-enrollment`：CosyVoice声音设计。
    
-   `qwen-voice-design`：Qwen声音设计。
    

**input** `_object_` **（必选）**

输入参数对象。

**属性**

**action** `_string_` **（必选）**

操作类型。CosyVoice：`query_voice`。Qwen声音设计：`query`。

**voice\_id** `_string_` **（条件必选）**

**重要**

仅适用于CosyVoice。

要查询的音色ID。

**voice** `_string_` **（条件必选）**

**重要**

仅适用于Qwen声音设计（model为`qwen-voice-design`时）。

要查询的音色名称。

### **返回体**

## CosyVoice声音设计

```
{
    "output": {
        "voice_id": "cosyvoice-v3.5-plus-vd-announcer-xxxxxx",
        "gmt_create": "2025-12-10 14:54:09",
        "gmt_modified": "2025-12-10 17:47:48",
        "preview_text": "各位听众朋友们，大家好",
        "target_model": "cosyvoice-v3.5-plus",
        "status": "OK",
        "voice_prompt": "沉稳的中年男性播音员，音色低沉浑厚"
    },
    "usage": {},
    "request_id": "xxxx-xxxx-xxxx"
}
```

## Qwen声音设计

```
{
    "output": {
        "voice": "yourVoice",
        "gmt_create": "2025-08-11 17:59:32",
        "gmt_modified": "2025-08-11 17:59:32",
        "language": "zh",
        "target_model": "qwen3-tts-vd-realtime-2026-01-15"
    },
    "usage": {
        "count": 0
    },
    "request_id": "xxxx-xxxx-xxxx"
}
```

**重要**

CosyVoice声音设计返回`voice_id`、`voice_prompt`等字段。Qwen声音设计返回`voice`和`language`字段。

**request\_id** `_string_`

本次调用的唯一标识符。

**output** `_object_`

模型返回的数据。

**属性**

**voice\_id / voice** `_string_`

音色ID。CosyVoice声音设计返回`voice_id`，Qwen声音设计返回`voice`。

**gmt\_create** `_string_`

创建时间。

**gmt\_modified** `_string_`

修改时间。

**status** `_string_`

**重要**

仅CosyVoice返回。

音色状态，取值参见"音色状态说明"。

**target\_model** `_string_`

驱动音色的语音合成模型。

**language** `_string_`

**重要**

仅Qwen声音设计返回。

音色语言。

**voice\_prompt** `_string_`

**重要**

仅CosyVoice声音设计返回。

声音描述文本。

**preview\_text** `_string_`

**重要**

仅CosyVoice声音设计返回。

预览音频文本。

**usage** `_object_`

本次请求用量信息。

**属性**

**count** `_integer_`

固定为1。

## **删除音色**

### **请求体**

以下为北京地域URL，若使用新加坡地域的模型，需将URL替换为：`https://dashscope-intl.aliyuncs.com/api/v1/services/audio/tts/customization`。

## CosyVoice

```
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "voice-enrollment",
    "input": {
        "action": "delete_voice",
        "voice_id": "yourVoiceId"
    }
}'
```

## Qwen声音设计

```
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-voice-design",
    "input": {
        "action": "delete",
        "voice": "yourVoice"
    }
}'
```

**model** `_string_` **（必选）**

声音设计模型。取值：

-   `voice-enrollment`：CosyVoice声音设计。
    
-   `qwen-voice-design`：Qwen声音设计。
    

**input** `_object_` **（必选）**

输入参数对象。

**属性**

**action** `_string_` **（必选）**

操作类型。CosyVoice：`delete_voice`。Qwen：`delete`。

**voice\_id** `_string_` **（条件必选）**

**重要**

仅适用于CosyVoice。

要删除的音色ID。

**voice** `_string_` **（条件必选）**

**重要**

仅适用于Qwen。

要删除的音色名称。

### **返回体**

## CosyVoice

```
{
    "output": {},
    "usage": {
        "count": 1
    },
    "request_id": "xxxx-xxxx-xxxx"
}
```

## Qwen

```
{
    "output": {
        "voice": "yourVoice"
    },
    "usage": {
        "count": 0
    },
    "request_id": "xxxx-xxxx-xxxx"
}
```

**重要**

CosyVoice的output为空对象，Qwen返回`voice`字段。

**request\_id** `_string_`

本次调用的唯一标识符。

**output** `_object_`

模型返回的数据。CosyVoice返回空对象，Qwen返回已删除的音色名称。

**属性**

**voice** `_string_`

**重要**

仅Qwen返回。

已删除的音色名称。

**usage** `_object_`

本次请求用量信息。

**属性**

**count** `_integer_`

固定为1。

## **音色状态说明**

音色创建后会经过审核流程，以下是各状态的含义。此状态体系仅适用于CosyVoice（model为`voice-enrollment`时），Qwen的查询和列表返回中不包含status字段。

**状态**

**说明**

DEPLOYING

审核中/处理中。

OK

审核通过，可正常使用。

UNDEPLOYED

审核未通过，不可使用。
