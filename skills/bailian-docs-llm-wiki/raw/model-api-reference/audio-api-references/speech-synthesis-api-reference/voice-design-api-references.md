# 声音设计API参考

本文介绍声音设计的HTTP API接口详情，包括创建音色、查询音色列表、查询音色详情和删除音色四个操作。

**用户指南：**[声音设计](raw/model-user-guide/model-experience/speech-synthesis/voice-design-user-guide.md)。

## 接口地址

#### 华北2（北京）

`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

**重要**阿里云百炼为华北2（北京）地域推出了业务空间专属域名，能够为推理请求提供卓越的性能和更高的稳定性，建议迁移至新域名：

-   华北2（北京）地域：从 `dashscope.aliyuncs.com` 迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`

`{WorkspaceId}`需要替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。现有域名仍可正常使用。

## 请求头

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

## 创建音色

### 请求体

**model**`string`**（必选）**

声音设计模型。取值：

-   `voice-enrollment`：Qwen-Audio-TTS/CosyVoice声音设计。

**input**`object`**（必选）**

输入参数对象。

属性

**action** `string`**（必选）**

操作类型。

-   Qwen-Audio-TTS/CosyVoice（`voice-enrollment`）：固定为`create_voice`。

**target\_model** `string`**（必选）**

驱动音色的语音合成模型。必须与后续调用语音合成接口时使用的模型一致，否则合成会失败。

**voice\_prompt** `string`**（必选）**

声音描述文本，仅支持中文和英文。

-   Qwen-Audio-TTS/CosyVoice（`voice-enrollment`）：最大长度500字符。

**preview\_text** `string`**（必选）**

预览音频对应的文本。

-   Qwen-Audio-TTS/CosyVoice（`voice-enrollment`）：最小长度15字符，最大长度200字符，支持中文和英文。

**prefix** `string`**（必选）**

**重要**仅适用于Qwen-Audio-TTS/CosyVoice（model为`voice-enrollment`时）。

音色名称前缀，仅允许数字和英文字母，不超过10个字符。生成的音色名格式：`{target_model}-vd-{prefix}-{唯一标识}`

**language\_hints** `array[string]`（可选）

**重要**仅适用于Qwen-Audio-TTS/CosyVoice（model为`voice-enrollment`时）。

指定生成音色的语言倾向，影响音色的语言特征和发音倾向，建议根据实际使用场景选择对应语言代码。若使用该参数，设置的语种须与 `preview_text` 的语种一致。

此参数为数组，但当前版本仅处理第一个元素。

取值范围：

-   zh：中文
-   en：英文

默认值：\["zh"\]。

**parameters**`object`（可选）

声音设计的参数配置。

属性

**sample\_rate** `int`（可选）

预览音频采样率（Hz）。

-   Qwen-Audio-TTS/CosyVoice支持：16000、24000、48000。

默认值：24000。

**response\_format** `string`（可选）

预览音频格式。

-   Qwen-Audio-TTS/CosyVoice支持：pcm、wav、mp3。

默认值：wav。

以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。

Qwen-Audio-TTS/CosyVoice声音设计

```
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "voice-enrollment",
    "input": {
        "action": "create_voice",
        "target_model": "cosyvoice-v3.5-plus",
        "voice_prompt": "沉稳的中年男性，音色低沉浑厚",
        "preview_text": "各位听众朋友们大家好，欢迎收听本期节目",
        "prefix": "announcer",
        "language_hints": ["zh"]
    },
    "parameters": {
        "sample_rate": 24000,
        "response_format": "wav"
    }
}'
```

### 返回体

**request\_id**`string`

本次调用的唯一标识符。

**output**`object`

模型返回的数据。

属性

**voice\_id**`string`

音色 ID，可用于语音合成接口的 `voice` 参数。

**preview\_audio**`object`

预览音频数据。

属性

**data** `string`

预览音频数据，Base64编码。

**sample\_rate** `int`

预览音频采样率（Hz）。

**response\_format** `string`

预览音频格式。

**target\_model**`string`

驱动音色的语音合成模型。

**usage**`object`

本次请求用量信息。

属性

**count** `integer`

创建的音色数量，固定为1。

Qwen-Audio-TTS/CosyVoice声音设计

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

## 查询音色列表

### 请求体

**model**`string`**（必选）**

声音设计模型。取值：

-   `voice-enrollment`：Qwen-Audio-TTS/CosyVoice声音设计。

**input**`object`**（必选）**

输入参数对象。

属性

**action** `string`**（必选）**

固定为 `list_voice`。

**prefix** `string`（可选）

**重要**仅适用于Qwen-Audio-TTS/CosyVoice。

按前缀筛选音色。

**page\_index** `integer`（可选）

页码索引。

**page\_size** `integer`（可选）

每页包含数据条数。

以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。

Qwen-Audio-TTS/CosyVoice

```
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization \
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

### 返回体

**request\_id**`string`

本次调用的唯一标识符。

**output**`object`

模型返回的数据。

属性

**voice\_list**`array[object]`

查询到的音色列表。

属性

**voice\_id**`string`

音色 ID，可用于语音合成接口的 `voice` 参数。

**gmt\_create**`string`

创建时间。

**gmt\_modified**`string`

修改时间。

**status**`string`

**重要**仅Qwen-Audio-TTS/CosyVoice返回。

音色状态，取值参见"音色状态说明"。

**voice\_prompt**`string`

声音描述文本。

**preview\_text**`string`

预览音频文本。

**usage**`object`

本次请求用量信息。

属性

**count** `integer`

固定为 1。

Qwen-Audio-TTS/CosyVoice

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

## 查询音色详情

### 请求体

**model**`string`**（必选）**

声音设计模型。取值：

-   `voice-enrollment`：Qwen-Audio-TTS/CosyVoice声音设计。

**input**`object`**（必选）**

输入参数对象。

属性

**action** `string`**（必选）**

固定为 `query_voice`。

**voice\_id** `string`**（必选）**

**重要**仅适用于Qwen-Audio-TTS/CosyVoice。

要查询的音色ID。

以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。

Qwen-Audio-TTS/CosyVoice

```
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization \
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

### 返回体

**request\_id**`string`

本次调用的唯一标识符。

**output**`object`

模型返回的数据。

属性

**voice\_id**`string`

音色 ID，可用于语音合成接口的 `voice` 参数。

**gmt\_create**`string`

创建时间。

**gmt\_modified**`string`

修改时间。

**status**`string`

**重要**仅Qwen-Audio-TTS/CosyVoice返回。

音色状态，取值参见"音色状态说明"。

**target\_model**`string`

驱动音色的语音合成模型。

**voice\_prompt**`string`

**重要**仅Qwen-Audio-TTS/CosyVoice声音设计返回。

声音描述文本。

**preview\_text**`string`

**重要**仅Qwen-Audio-TTS/CosyVoice声音设计返回。

预览音频文本。

**usage**`object`

本次请求用量信息。

属性

**count** `integer`

固定为1。

Qwen-Audio-TTS/CosyVoice声音设计

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
    "usage": {
        "count": 1
    },
    "request_id": "xxxx-xxxx-xxxx"
}
```

## 删除音色

### 请求体

**model**`string`**（必选）**

声音设计模型。取值：

-   `voice-enrollment`：Qwen-Audio-TTS/CosyVoice声音设计。

**input**`object`**（必选）**

输入参数对象。

属性

**action** `string`**（必选）**

固定为 `delete_voice`。

**voice\_id** `string`**（必选）**

**重要**仅适用于Qwen-Audio-TTS/CosyVoice。

要删除的音色ID。

以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。

Qwen-Audio-TTS/CosyVoice

```
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization \
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

### 返回体

**request\_id**`string`

本次调用的唯一标识符。

**output**`object`

模型返回的数据，为空对象。

**usage**`object`

本次请求用量信息。

属性

**count** `integer`

固定为1。

Qwen-Audio-TTS/CosyVoice

```
{
    "output": {},
    "usage": {
        "count": 1
    },
    "request_id": "xxxx-xxxx-xxxx"
}
```

## 音色状态说明

音色创建后会经过审核流程。以下状态适用于 Qwen-Audio-TTS/CosyVoice（`model` 为 `voice-enrollment`）。

**状态**

**说明**

DEPLOYING

审核中/处理中。

OK

审核通过，可正常使用。

UNDEPLOYED

审核未通过，不可使用。
