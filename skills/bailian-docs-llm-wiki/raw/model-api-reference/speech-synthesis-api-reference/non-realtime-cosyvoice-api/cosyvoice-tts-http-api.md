# 非实时语音合成CosyVoice HTTP API参考

本文介绍非实时语音合成CosyVoice的HTTP调用方法，支持非流式和流式两种调用模式。

**用户指南**：参见[非实时语音合成](https://help.aliyun.com/zh/model-studio/non-realtime-tts-user-guide)。

**重要**

该功能仅在[中国内地部署范围](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)（北京地域）下可用。

## **服务端点**

`POST https://dashscope.aliyuncs.com/api/v1/services/audio/tts/SpeechSynthesizer`

## **请求头**

**参数**

**类型**

**是否必选**

**说明**

Authorization

string

是

鉴权令牌，格式为`Bearer <your_api_key>`，使用时，将“`<your_api_key>`”替换为实际的API Key。

Content-Type

string

是

请求体的媒体类型，固定为`application/json`。

X-DashScope-SSE

string

否

用于控制是否以流式方式返回输出结果。仅在流式合成时使用该参数，参数值固定为`enable`。

## **请求体**

## 非流式

```
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/audio/tts/SpeechSynthesizer \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "cosyvoice-v3-flash",
    "input": {
      "text": "我家的后面有一个很大的花园。",
      "voice": "longanyang",
      "format": "wav",
      "sample_rate": 24000
    }
}'
```

## 流式

```
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/audio/tts/SpeechSynthesizer \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-H "X-DashScope-SSE: enable" \
-d '{
    "model": "cosyvoice-v3-flash",
    "input": {
      "text": "我家的后面有一个很大的花园。",
      "voice": "longanyang",
      "format": "wav",
      "sample_rate": 24000
    }
}'
```

**model** `_string_` **（必选）**

语音合成模型。

取值范围：

-   cosyvoice-v3.5-plus
    
-   cosyvoice-v3.5-flash
    
-   cosyvoice-v3-plus
    
-   cosyvoice-v3-flash
    
-   cosyvoice-v2
    

**input** `_object_` **（必选）**

输入参数对象**。**

**属性**

**text** `_string_` **（必选）**

待合成文本。

支持 SSML 和 LaTeX 格式输入。将待合成文本替换为对应格式即可。

-   使用 SSML 时，需同时将 `enable_ssml` 设置为 `true`。支持的 SSML 标签及用法，请参见[SSML标记语言介绍](https://help.aliyun.com/zh/model-studio/introduction-to-cosyvoice-ssml-markup-language)。
    
-   使用 LaTeX 时，将待合成文本替换为 LaTeX 格式即可，无需额外配置。支持的 LaTeX 语法及用法，请参见[LaTeX 公式转语音](https://help.aliyun.com/zh/model-studio/latex-capability-support-description)。
    

**voice** `_string_` **（必选）**

音色。

取值范围：

-   系统音色：参见[音色列表](https://help.aliyun.com/zh/model-studio/cosyvoice-voice-list)
    
-   声音复刻音色：如何创建音色请参见[CosyVoice声音复刻/设计API](https://help.aliyun.com/zh/model-studio/cosyvoice-clone-design-api)
    
-   声音设计音色：如何创建音色请参见[CosyVoice声音复刻/设计API](https://help.aliyun.com/zh/model-studio/cosyvoice-clone-design-api)
    

**format** `_string_` （可选）

音频编码格式。

默认值：mp3。

取值范围：

-   mp3
    
-   pcm
    
-   wav
    
-   opus
    

**sample\_rate** `_integer_` （可选）

音频采样率（Hz）。

取值范围：8000, 16000, 22050（默认）, 24000, 44100, 48000。

**volume** `_integer_` （可选）

音量。

默认值：50。

取值范围：\[0, 100\]。

**rate** `_float_` （可选）

语速。

默认值：1.0。

取值范围：\[0.5, 2.0\]。

**bit\_rate** `_integer_` （可选）

音频码率（单位：kbps）。

默认值：32。

取值范围：\[6, 510\]。

**重要**

仅在`format`为`opus`时支持使用该参数。

**pitch** `_float_` （可选）

音调。

默认值：1.0。

取值范围：\[0.5, 2.0\]。

**enable\_ssml** `_boolean_` （可选）

是否开启SSML功能。

**word\_timestamp\_enabled** `_boolean_` （可选）

是否开启字级别时间戳。

默认值：false。

适用范围：仅适用于cosyvoice-v3-flash、cosyvoice-v3-plus和cosyvoice-v2模型的复刻音色，以及[音色列表](https://help.aliyun.com/zh/model-studio/cosyvoice-voice-list)中标记为支持的系统音色。

**seed** `_integer_` （可选）

生成时使用的随机数种子，使合成的效果产生变化。在模型版本、文本、音色及其他参数均相同的前提下，使用相同的seed可复现相同的合成结果。

默认值0。

取值范围：\[0, 65535\]。

**language\_hints** `_array[string]_` （可选）

**重要**

-   此参数为数组，但当前版本仅处理第一个元素，因此建议只传入一个值。
    
-   此参数用于指定语音合成的目标语言，该设置与声音复刻时的样本音频的语种无关。如需设置复刻任务的源语言，请参见声音复刻API参考。
    

指定语音合成的目标语言，提升合成效果。

当数字、缩写、符号等朗读方式或者小语种合成效果不符合预期时使用，例如：

-   数字朗读方式不符合预期，“hello, this is 110”读成“hello, this is one one zero”而非“hello, this is 幺幺零”
    
-   符号朗读不准确，“@”读成“艾特”而非“at”
    
-   小语种合成效果差，合成不自然
    

取值范围：

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
    

**instruction** `_string_` （可选）

设置指令，用于控制方言、情感或角色等合成效果。

具体用法请参见[非实时语音合成](https://help.aliyun.com/zh/model-studio/non-realtime-tts-user-guide)。

**enable\_aigc\_tag** `_boolean_` （可选）

是否在生成的音频中添加AIGC隐性标识。设置为true时，会将隐性标识嵌入到支持格式（wav/mp3/opus）的音频中。

默认值：false。

仅cosyvoice-v3-flash、cosyvoice-v3-plus、cosyvoice-v2支持该功能。

**aigc\_propagator** `_string_` （可选）

设置AIGC隐性标识中的 `ContentPropagator` 字段，用于标识内容的传播者。仅在 `enable_aigc_tag` 为 `true` 时生效。

默认值：阿里云UID。

仅cosyvoice-v3-flash、cosyvoice-v3-plus、cosyvoice-v2支持该功能。

**aigc\_propagate\_id** `_string_` （可选）

设置AIGC隐性标识中的 `PropagateID` 字段，用于唯一标识一次具体的传播行为。仅在 `enable_aigc_tag` 为 `true` 时生效。

默认值：本次语音合成请求Request ID。

仅cosyvoice-v3-flash、cosyvoice-v3-plus、cosyvoice-v2支持该功能。

**hot\_fix** `_object_` （可选）

文本热修复配置，用于自定义指定词语的发音或对待合成文本进行替换。

cosyvoice-v2不支持该功能。

参数介绍：

-   pronunciation：自定义发音。指定词语的拼音标注，用于纠正默认发音不准确的情况。
    
-   replace：文本替换。在语音合成前将指定词语替换为目标文本，替换后的文本将作为实际合成内容。
    

示例：

```
"hot_fix": {
  "pronunciation": [
    {"天气": "tian1 qi4"}
  ],
  "replace": [
    {"今天": "金天"}
  ]
}
```

**enable\_markdown\_filter** `_boolean_` （可选）

**重要**

仅cosyvoice-v3-flash复刻音色支持该功能。

是否启用 Markdown 过滤。启用该功能后，系统在合成语音前自动过滤输入文本中的 Markdown 标记符号，避免将其朗读为文字内容。

默认值：false。

取值范围：

-   true：启用Markdown过滤
    
-   false：禁用Markdown过滤
    

## **返回体**

## 非流式

```
{
    "request_id": "ee88b03d-0457-9286-8c67-xxxxxxxxxxxx",
    "output": {
        "finish_reason": "stop",
        "audio": {
            "data": "",
            "url": "http://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/pre/cosyvoice-v3-flash/20260304/xxxxxxxx/ee88b03d-0457-9286-8c67-xxxxxxxxxxxx.wav?xxxxxxx",
            "id": "audio_ee88b03d-0457-9286-8c67-xxxxxxxxxxxx",
            "expires_at": 1772697707
        }
    },
    "usage": {
        "characters": 15
    }
}
```

## 流式

中间结果：

```
{
    "request_id": "8ac1cd04-06af-9a63-b031-xxxxxxxxxxxx",
    "output": {
        "finish_reason": "null",
        "type": "sentence-begin",
        "original_text": "我家的后面有一个很大的花园。",
        "sentence": {
            "index": 0,
            "words": []
        },
        "audio": {
            "data": "",
            "id": "audio_ee88b03d-0457-9286-8c67-xxxxxxxxxxxx",
            "expires_at": 1772697707
        }
    },
    "usage": {
        "characters": 15
    }
}
```

最终结果：

```
{
    "request_id": "8ac1cd04-06af-9a63-b031-xxxxxxxxxxxx",
    "output": {
        "finish_reason": "stop",
        "audio": {
            "data": "",
            "url": "http://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/pre/cosyvoice-v3-flash/20260304/xxxxxxxx/8ac1cd04-06af-9a63-b031-xxxxxxxxxxxx.wav?xxxxxxx",
            "id": "audio_8ac1cd04-06af-9a63-b031-xxxxxxxxxxxx",
            "expires_at": 1772698611,
        }
    },
    "usage": {
        "characters": 15
    }
}
```

**request\_id** `_string_`

本次调用的唯一标识符。

**output** `_object_`

模型返回的数据。

**属性**

**finish\_reason** `_string_`

任务停止原因，自然停止时为`stop`。

取值范围：

-   null：语音合成中
    
-   stop：语音合成结束
    

**type** `_string_`

子事件类型。仅流式合成时返回该值。

取值范围：

-   sentence-begin：标识句子开始，返回待合成的句子文本内容
    
-   sentence-synthesis：标识音频数据块
    
    -   一个句子的合成过程中会产生多个`sentence-synthesis`事件，每个对应一个音频数据块
        
    -   客户端需要按顺序接收这些音频数据块并以追加模式写入同一文件
        
    -   `sentence-synthesis`事件与其后的音频数据帧是一一对应的关系，不会出现错位
        
-   sentence-end：标识句子结束，返回句子文本内容和累计的计费字符数
    

**original\_text** `_string_`

对用户输入文本进行分句后的句内容。最后一个句子可能没有此字段。

**sentence** `_object_`

句子信息。

**属性**

**index** `_integer_`

句子的编号，从0开始。

**words** `_array_`

每句话对应的字的信息。

**属性**

**text** `_string_`

字。

**begin\_index** `_integer_`

字在句子中的开始位置索引，从 0 开始。

**end\_index** `_integer_`

字在句子中的结束位置索引，从 1 开始。

**begin\_time** `_integer_`

字对应音频的开始时间戳，单位为毫秒。

**end\_time** `_integer_`

字对应音频的结束时间戳，单位为毫秒。

**audio** `_object_`

合成的音频数据。

**属性**

**data** `_string_`

流式合成时输出Base64格式音频数据。非流式合成时为空。

**url** `_string_`

模型输出的完整音频文件的URL，有效期24小时。

**id** `_string_`

模型输出的音频信息对应的ID。

**expires\_at** `_integer_`

`url` 过期时间戳。

**usage** `_object_`

本次请求的字符用量。

**属性**

**characters** `_integer_`

本次请求中计费的有效字符数。
