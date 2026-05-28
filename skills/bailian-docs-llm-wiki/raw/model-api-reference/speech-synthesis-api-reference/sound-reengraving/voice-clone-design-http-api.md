# 声音复刻HTTP API参考

本文介绍声音复刻的HTTP API接口详情，包括创建音色、查询音色列表、查询音色详情、更新音色和删除音色等操作。

**用户指南：**[声音复刻](https://help.aliyun.com/zh/model-studio/voice-cloning-user-guide)。

## **服务端点****（CosyVoice/Qwen-TTS）**

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

`POST https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization`

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

`POST https://dashscope-intl.aliyuncs.com/api/v1/services/audio/tts/customization`

## **服务端点（MiniMax）**

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

HTTP请求地址：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

SDK调用配置的base\_url：`https://dashscope.aliyuncs.com/api/v1`

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

请求体的媒体类型。CosyVoice/Qwen-TTS固定为`application/json`，MiniMax固定为`application/json; charset=utf-8`。

## **创建音色****（CosyVoice/Qwen-TTS）**

### **请求体**

以下为北京地域URL，若使用新加坡地域的模型，需将URL替换为：`https://dashscope-intl.aliyuncs.com/api/v1/services/audio/tts/customization`。

## CosyVoice声音复刻

```
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "voice-enrollment",
    "input": {
        "action": "create_voice",
        "target_model": "cosyvoice-v3.5-plus",
        "prefix": "myvoice",
        "url": "https://your-audio-url.wav",
        "language_hints": ["zh"]
    }
}'
```

## Qwen声音复刻

```
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-voice-enrollment",
    "input": {
        "action": "create",
        "target_model": "qwen3-tts-vc-realtime-2026-01-15",
        "preferred_name": "myvoice",
        "audio": {"data": "data:audio/mpeg;base64,{base64_encoded_audio}"}
    }
}'
```

**model** `_string_` **（必选）**

声音复刻模型。取值：

-   `voice-enrollment`：CosyVoice声音复刻。
    
-   `qwen-voice-enrollment`：Qwen声音复刻。
    

**input** `_object_` **（必选）**

输入参数对象。

**属性**

**action** `_string_` **（必选）**

操作类型。

-   CosyVoice（`voice-enrollment`）：固定为`create_voice`。
    
-   Qwen（`qwen-voice-enrollment`）：固定为`create`。
    

**target\_model** `_string_` **（必选）**

驱动音色的语音合成模型。必须与后续调用语音合成接口时使用的模型一致，否则合成会失败。

**url** `_string_` **（条件必选）**

**重要**

仅适用于CosyVoice声音复刻（model为`voice-enrollment`时）。

用于复刻音色的音频文件URL，要求公网可访问。

**audio** `_object_` **（条件必选）**

**重要**

仅适用于Qwen声音复刻（model为`qwen-voice-enrollment`时）。

音频数据，支持两种提交方式：

-   Data URL（Base64编码）：格式为`{"data": "data:{mime_type};base64,{base64_encoded_data}"}`，支持的MIME类型：`audio/wav`、`audio/mpeg`、`audio/mp4`。
    
-   音频URL：格式为`{"data": "https://your-audio-url.wav"}`，URL必须公网可访问且无需鉴权。
    

**text** `_string_` （可选）

**重要**

仅适用于Qwen声音复刻（model为`qwen-voice-enrollment`时）。

音频对应的文本内容，用于辅助提升复刻效果。

**prefix** `_string_` **（条件必选）**

**重要**

仅适用于CosyVoice（model为`voice-enrollment`时）。

音色名称前缀，仅允许数字和英文字母，不超过10个字符。生成的音色名格式：`{target_model}-{prefix}-{唯一标识}`。

**preferred\_name** `_string_` **（条件必选）**

**重要**

仅适用于Qwen声音复刻（model为`qwen-voice-enrollment`时）。

音色名称前缀，仅允许数字、英文字母和下划线，不超过16个字符。

**language\_hints** `_array[string]_` （可选）

**重要**

仅适用于CosyVoice声音复刻（model为`voice-enrollment`时），且仅cosyvoice-v3.5-plus、v3.5-flash、v3-plus和v3-flash模型支持。

辅助模型识别样本音频的语种，从而更准确地提取音色特征，提升复刻效果。若设置的语种与实际音频语种不符（例如为中文音频设置 `en`），系统将忽略该设置并自动检测语种。

此参数为数组，但当前版本仅处理第一个元素。

取值范围（因模型而异）：

-   cosyvoice-v3-plus：
    
    -   zh：中文
        
    -   en：英文
        
    -   fr：法语
        
    -   de：德语
        
    -   ja：日语
        
    -   ko：韩语
        
    -   ru：俄语
        
-   cosyvoice-v3.5-plus、cosyvoice-v3.5-flash、cosyvoice-v3-flash：
    
    -   zh：中文
        
    -   en：英文
        
    -   fr：法语
        
    -   de：德语
        
    -   ja：日语
        
    -   ko：韩语
        
    -   ru：俄语
        
    -   pt：葡萄牙语
        
    -   th：泰语
        
    -   id：印尼语
        
    -   vi：越南语
        

默认值：\["zh"\]。

**language** `_string_` （可选）

**重要**

仅适用于Qwen声音复刻（model为`qwen-voice-enrollment`时）。

指定 `audio.data` 音频对应的语种。若使用该参数，设置的语种须与实际用于复刻的音频语种一致。

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

**max\_prompt\_audio\_length** `_float_` （可选）

**重要**

仅适用于CosyVoice声音复刻（model为`voice-enrollment`时），且仅cosyvoice-v3.5-plus、v3.5-flash和v3-flash模型支持。

音频预处理后用于声音复刻的参考音频最大时长（秒）。取值范围：\[3.0, 30.0\]。时间越长效果越好。

默认值：10.0。

**enable\_preprocess** `_boolean_` （可选）

**重要**

仅适用于CosyVoice声音复刻（model为`voice-enrollment`时），且仅cosyvoice-v3.5-plus、v3.5-flash和v3-flash模型支持。

是否开启音频预处理（降噪、音频增强、音量规整）。有背景噪音时建议开启；安静环境建议关闭以最大程度还原音色。

默认值：false。

### **返回体**

## CosyVoice声音复刻

```
{
    "output": {
        "voice_id": "cosyvoice-v3.5-plus-myvoice-xxxxxx"
    },
    "usage": {
        "count": 1
    },
    "request_id": "xxxx-xxxx-xxxx"
}
```

## Qwen声音复刻

```
{
    "output": {
        "voice": "yourVoice",
        "target_model": "qwen3-tts-vc-realtime-2026-01-15"
    },
    "usage": {
        "count": 1
    },
    "request_id": "xxxx-xxxx-xxxx"
}
```

**重要**

CosyVoice返回`voice_id`字段，Qwen返回`voice`字段。Qwen声音复刻还可能返回`fallback_mode`和`fallback_reason`字段。

**request\_id** `_string_`

本次调用的唯一标识符。

**output** `_object_`

模型返回的数据。

**属性**

**voice\_id / voice** `_string_`

音色ID。CosyVoice返回`voice_id`，Qwen返回`voice`。可直接用于语音合成接口的voice参数。

**target\_model** `_string_`

**重要**

仅Qwen返回。

驱动音色的语音合成模型。

**fallback\_mode** `_boolean_`

**重要**

仅适用于Qwen声音复刻（model为`qwen-voice-enrollment`时）。

是否以降级模式创建音色。当音频质量不佳或与文本不匹配时，该值为`true`，表示复刻效果可能不理想。

**fallback\_reason** `_string_`

**重要**

仅当`fallback_mode`为`true`时返回。

降级原因。可能的值包括`no_merged_segments`（无法合并音频片段）、`no_valid_asr_segments`（音频与文本严重不匹配）等。

**usage** `_object_`

本次请求用量信息。

**属性**

**count** `_integer_`

创建的音色数量，固定为1。

## **创建音色（MiniMax）**

> 音色复刻请求会生成一段试听音频，试听音频按所选模型的同步语音合成单价额外计费。

### **请求体**

```
curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
  -H "Authorization: Bearer ${DASH_APIKEY}" \
  -H 'Content-Type: application/json; charset=utf-8' \
  -d '{
    "input": {
      "action": "voice_clone",
      "voice_id": "bailian-test-voice-22",
      "audio_url": "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/cosyvoice/cosyvoice-zeroshot-sample.wav",
      "text": "今天天气怎么样？"
    },
    "model": "MiniMax/speech-2.8-turbo"
  }'
```

**model** `_string_` **（必选）**

指定合成试听音频使用的语音模型。

支持的模型：

-   MiniMax/speech-2.8-hd
    
-   MiniMax/speech-02-hd
    
-   MiniMax/speech-2.8-turbo
    
-   MiniMax/speech-02-turbo
    

**input** `_object_` **（必选）**

**属性**

**action** `_string_` **（必选）**

需要进行的操作，支持设置为：`voice_clone`（声音克隆）

**audio\_url** `_string_` **（必选）**

需要复刻的音频文件 URL，音频需符合以下规范：

-   音频格式需为：mp3、m4a、wav 格式
    
-   音频的时长最少应不低于 10 秒，最长应不超过 5 分钟
    
-   音频文件大小需不超过 20 MB
    

**clone\_prompt** `_object_` **（可选）**

音色复刻示例音频，提供本参数将有助于增强语音合成的音色相似度和稳定性。若使用本参数，需准备一小段示例音频。

**属性**

**prompt\_audio** `_string_` **（可选）**

示例音频文件 URL，音频需符合以下规范：

-   音频格式需为：mp3、m4a、wav 格式
    
-   音频时长小于 8 秒
    
-   音频文件大小需不超过 20 MB
    

**prompt\_text** `_string_` **（可选）**

示例音频的对应文本，需确保和音频内容一致，句末需有标点符号做结尾。

**text** `_string_` **（必选）**

复刻声音期望试听的内容。限制 1000 字符以内。

> 试听将根据字符数正常收取语音合成费用，收费标准参见[MiniMax模型价格](https://help.aliyun.com/zh/model-studio/model-pricing#8296764fe3l4x)。

-   语气词标签：仅当模型选择 `speech-2.8-hd` 或 `speech-2.8-turbo` 时，支持在文本中插入语气词标签。支持的语气词：`(laughs)`（笑声）、`(chuckle)`（轻笑）、`(coughs)`（咳嗽）、`(clear-throat)`（清嗓子）、`(groans)`（呻吟）、`(breath)`（正常换气）、`(pant)`（喘气）、`(inhale)`（吸气）、`(exhale)`（呼气）、`(gasps)`（倒吸气）、`(sniffs)`（吸鼻子）、`(sighs)`（叹气）、`(snorts)`（喷鼻息）、`(burps)`（打嗝）、`(lip-smacking)`（咂嘴）、`(humming)`（哼唱）、`(hissing)`（嘶嘶声）、`(emm)`（嗯）、`(whistles)`（口哨）、`(sneezes)`（喷嚏）、`(crying)`（抽泣）、`(applause)`（鼓掌）
    

**voice\_id** `_string_` **（必选）**

克隆音色的 voice\_id，正确示例："MiniMax001"。用户进行自定义 voice\_id 时需注意：

-   自定义的 voice\_id 长度范围\[8,256\]
    
-   首字符必须为英文字母
    
-   允许数字、字母、-、\_
    
-   末位字符不可为 -、\_
    
-   voice\_id 不可与已有 id 重复，否则会报错
    

> 该参数全局唯一，建议使用时间戳等个性化信息命名。

**language\_boost**`enum<string>`**（可选）**默认值：null

是否增强对指定的小语种和方言的识别能力。可设置为 `auto` 让模型自主判断。

**可用选项**

`Chinese`, `Chinese,Yue`, `English`, `Arabic`, `Russian`, `Spanish`, `French`, `Portuguese`, `German`, `Turkish`, `Dutch`, `Ukrainian`, `Vietnamese`, `Indonesian`, `Japanese`, `Italian`, `Korean`, `Thai`, `Polish`, `Romanian`, `Greek`, `Czech`, `Finnish`, `Hindi`, `Bulgarian`, `Danish`, `Hebrew`, `Malay`, `Persian`, `Slovak`, `Swedish`, `Croatian`, `Filipino`, `Hungarian`, `Norwegian`, `Slovenian`, `Catalan`, `Nynorsk`, `Tamil`, `Afrikaans`,`auto`

**need\_noise\_reduction** `boolean` **（可选）**默认值：false

音频复刻参数，表示是否开启降噪，默认值为 false。

**need\_volume\_normalization**`boolean` **（可选）**默认值：false

是否开启音量归一化。

**aigc\_watermark**`boolean` **（可选）**默认值：false

是否在合成试听音频的末尾添加音频节奏标识。

### **返回体**

```
{
    "output": {
        "base_resp": {
            "status_code": 0,
            "status_msg": "success"
        },
        "demo_audio": "https://minimax-algeng-chat-tts.oss-cn-wulanchabu.aliyuncs.com/audio%2Feffect%2F05fdf023562aea84632d2a8c01c2366f_1773059375796_1311.mp3?Expires=1773232175&OSSAccessKeyId=LTAI************&Signature=z2GwvhFZ3d33BggWRGU8Jb24sZA%3D",
        "input_sensitive": false,
        "input_sensitive_type": 0
    },
    "usage": {
        "characters": 18
    },
    "request_id": "b1160386-ebf1-913f-9275-ef176c5e1c91"
}
```

**request\_id** `_string_`

本次调用的唯一标识符。

**output** `_object_`

**属性**

**input\_sensitive**`_boolean_`

输入音频是否命中风控。

**input\_sensitive\_type** `_integer_`

输入音频命中风控的类型，取值为以下其一：

-   0：正常
    
-   1：严重违规
    
-   2：色情
    
-   3：广告
    
-   4：违禁
    
-   5：谩骂
    
-   6：暴恐
    
-   7：其他
    

**demo\_audio**`_string_`

链接形式的试听音频。

**base\_resp**`_object_`

**属性**

**status\_code**`_integer_`

状态码

-   0: 请求结果正常
    
-   1000：未知错误
    
-   1001：超时
    
-   1002：触发限流
    
-   1004：鉴权失败
    
-   1013：服务内部错误
    
-   2013：输入格式信息不正常
    
-   2038：无复刻权限，请检查账号认证状态
    

**status\_msg**`_string_`

状态详情

**usage** `_object_`

本次请求的字符用量。

**属性**

**characters** `_integer_`

输入文本的字符数。

## **查询音色列表**

**重要**

MiniMax不支持该功能。

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

## Qwen声音复刻

```
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-voice-enrollment",
    "input": {
        "action": "list",
        "page_size": 10,
        "page_index": 0
    }
}'
```

**model** `_string_` **（必选）**

声音复刻模型。取值：

-   `voice-enrollment`：CosyVoice声音复刻。
    
-   `qwen-voice-enrollment`：Qwen声音复刻。
    

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
                "voice_id": "cosyvoice-v3.5-plus-myvoice-xxxxxx",
                "gmt_create": "2024-12-11 13:38:02",
                "gmt_modified": "2024-12-11 13:38:02",
                "status": "OK"
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
        "total_count": 2,
        "voice_list": [
            {
                "voice": "yourVoice1",
                "gmt_create": "2025-08-11 17:59:32",
                "gmt_modified": "2025-08-11 17:59:32",
                "language": "zh",
                "target_model": "qwen3-tts-vc-realtime-2026-01-15"
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

查询到的音色列表。CosyVoice和Qwen均使用`voice_list`字段名。

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

**usage** `_object_`

本次请求用量信息。

**属性**

**count** `_integer_`

CosyVoice固定为1。Qwen固定为0。

## **查询音色详情**

**重要**

仅适用于CosyVoice（model为`voice-enrollment`时）。Qwen和MiniMax模型不支持查询音色详情操作。

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

**model** `_string_` **（必选）**

固定为`voice-enrollment`（CosyVoice）。

**input** `_object_` **（必选）**

输入参数对象。

**属性**

**action** `_string_` **（必选）**

固定为`query_voice`。

**voice\_id** `_string_` **（必选）**

要查询的音色ID。

### **返回体**

```
{
    "output": {
        "gmt_create": "2024-12-11 13:38:02",
        "resource_link": "https://yourAudioFileUrl",
        "target_model": "cosyvoice-v3.5-plus",
        "gmt_modified": "2024-12-11 13:38:02",
        "status": "OK"
    },
    "usage": {
        "count": 1
    },
    "request_id": "xxxx-xxxx-xxxx"
}
```

**request\_id** `_string_`

本次调用的唯一标识符。

**output** `_object_`

模型返回的数据。

**属性**

**resource\_link** `_string_`

音频文件的URL地址。

**gmt\_create** `_string_`

创建时间。

**gmt\_modified** `_string_`

修改时间。

**status** `_string_`

音色状态，取值参见"音色状态说明"。

**target\_model** `_string_`

驱动音色的语音合成模型。

**usage** `_object_`

本次请求用量信息。

**属性**

**count** `_integer_`

固定为1。

## **更新音色**

**重要**

仅适用于CosyVoice声音复刻（model为`voice-enrollment`时）。Qwen和MiniMax模型不支持更新操作。

### **请求体**

以下为北京地域URL，若使用新加坡地域的模型，需将URL替换为：`https://dashscope-intl.aliyuncs.com/api/v1/services/audio/tts/customization`。

```
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "voice-enrollment",
    "input": {
        "action": "update_voice",
        "voice_id": "yourVoiceId",
        "url": "https://new-audio-url.wav"
    }
}'
```

**model** `_string_` **（必选）**

固定为`voice-enrollment`。

**input** `_object_` **（必选）**

输入参数对象。

**属性**

**action** `_string_` **（必选）**

固定为`update_voice`。

**voice\_id** `_string_` **（必选）**

要更新的音色ID。

**url** `_string_` **（必选）**

新的音频文件URL，要求公网可访问。

### **返回体**

```
{
    "output": {},
    "usage": {
        "count": 1
    },
    "request_id": "xxxx-xxxx-xxxx"
}
```

**request\_id** `_string_`

本次调用的唯一标识符。

**output** `_object_`

模型返回的数据，更新操作返回空对象。

**usage** `_object_`

本次请求用量信息。

**属性**

**count** `_integer_`

固定为1。

## **删除音色**

**重要**

MiniMax不支持该功能。

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

## Qwen声音复刻

```
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-voice-enrollment",
    "input": {
        "action": "delete",
        "voice": "yourVoice"
    }
}'
```

**model** `_string_` **（必选）**

声音复刻模型。取值：

-   `voice-enrollment`：CosyVoice声音复刻。
    
-   `qwen-voice-enrollment`：Qwen声音复刻。
    

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
