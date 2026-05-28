# MiniMax同步语音合成API参考

## **支持的模型**

**模型名称**

**语音合成单价（每万字符）**

[复刻一个音色](https://help.aliyun.com/zh/model-studio/mini-clone-api)

**免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

MiniMax/speech-2.8-hd

3.5元

9.9元

（在首次使用复刻出来的音色进行语音合成的时候收取）

无

MiniMax/speech-02-hd

3.5元

MiniMax/speech-2.8-turbo

2元

MiniMax/speech-02-turbo

2元

## **URL**

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

HTTP请求地址：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

SDK调用配置的base\_url：`https://dashscope.aliyuncs.com/api/v1`

## **Headers**

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

是否启用 SSE（Server-Sent Events）流式输出。设为 `enable` 时，服务端将以流式事件逐步返回结果，适用于实时性要求较高的场景。不设置时，使用默认的同步响应模式。

## **请求体**

## 非流式

```
curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
  "model": "MiniMax/speech-2.8-hd",
  "input": {
    "text": "今天是不是很开心呀(laughs)，当然了！",
    "voice_setting": {
      "voice_id": "male-qn-qingse",
      "speed": 1,
      "vol": 1,
      "pitch": 0,
      "emotion": "happy"
    },
    "audio_setting": {
      "sample_rate": 32000,
      "bitrate": 128000,
      "format": "mp3",
      "channel": 1
    },
    "pronunciation_dict": {
      "tone": [
        "处理/(chu3)(li3)",
        "危险/dangerous"
      ]
    },
    "subtitle_enable": false
  }
}'
```

## 流式

```
curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-H "X-DashScope-SSE: enable" \
-d '{
  "model": "MiniMax/speech-2.8-hd",
  "input": {
    "text": "今天是不是很开心呀(laughs)，当然了！",
    "voice_setting": {
      "voice_id": "male-qn-qingse",
      "speed": 1,
      "vol": 1,
      "pitch": 0,
      "emotion": "happy"
    },
    "audio_setting": {
      "sample_rate": 32000,
      "bitrate": 128000,
      "format": "mp3",
      "channel": 1
    },
    "pronunciation_dict": {
      "tone": [
        "处理/(chu3)(li3)",
        "危险/dangerous"
      ]
    },
    "subtitle_enable": false
  }
}'
```

**model** `_string_` **（必选）**

模型名称。支持：

MiniMax/speech-2.8-hd

MiniMax/speech-02-hd

MiniMax/speech-2.8-turbo

MiniMax/speech-02-turbo

**input** `_object_` **（必选）**

**属性**

**text** `_string_` **（必选）**

待合成语音的文本。

长度限制小于 10000 字符，若文本长度大于 3000 字符，推荐使用流式输出。

**stream\_options** `_object_` （可选）

流式输出的配置项，仅在请求头 `X-DashScope-SSE: enable` 时生效。

**属性**

**exclude\_aggregated\_audio** `_boolean_` （可选） 默认值为`false`

控制流式输出的合成结束帧中，`audio` 字段是否返回本次合成的完整音频（即此前所有合成中分块拼接后的整段 hex 数据）。

取值范围：

-   `false`：合成结束帧的 `audio` 字段返回所有分块拼接后的完整音频，客户端可在流结束时直接取用整段音频，无需自行拼接前面的分块。
    
-   `true`：合成结束帧的 `audio` 字段为空字符串，整段音频需由客户端将此前所有合成中分块的 `audio` 按顺序自行拼接得到。可显著减少尾包体积与传输耗时，适用于客户端已经按 chunk 边接收边播放、或自行累积保存音频的场景。
    

**说明**

该参数仅在流式输出场景下生效；非流式输出场景下设置无效。

**voice\_setting** `_object_` **（必选）**

**属性**

**voice\_id** `_string_` **（必选）**

设置音色ID。

若需要设置混合音色，请设置 `timbre_weights` 参数，本参数设置为空值。

**speed** `_float_` （可选） 默认值为`1.0`

设置语速。

取值范围：`[0.5, 2.0]`。

**vol** `_float_` （可选） 默认值为`1.0`

设置音量。

取值范围：`(0.0, 10.0]`。

**pitch** `_integer_` （可选） 默认值为`0`

设置音高。

取值范围：`[-12, 12]`。

**emotion** `_string_` （可选） 无默认值

设置情感。模型会根据输入文本自动匹配合适的情感，一般无需手动指定。

取值范围：

-   `happy`：高兴
    
-   `sad`：悲伤
    
-   `angry`：愤怒
    
-   `fearful`：害怕
    
-   `disgusted`：厌恶
    
-   `surprised`：惊讶
    
-   `calm`：中性
    
-   `whisper`：低语
    

**说明**

`speech-2.8-hd`, `speech-2.8-turbo` 模型不支持 `whisper`

**text\_normalization** `_boolean_` （可选） 默认值为`false`

是否启用中文、英语文本规范化，开启后可提升数字阅读场景的性能，但会略微增加延迟。

取值范围：

-   `true`：开启
    
-   `false`：关闭
    

**latex\_read** `_boolean_` （可选） 默认值为`false`

是否启用朗读 LaTeX 公式的功能。

取值范围：

-   `true`：开启
    
-   `false`：关闭
    

示例：

x\=2a−b±b2−4ac​​

如上公式应表示为：`$$x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$$`。

**说明**

-   仅支持中文，开启该功能后，`language_boost`参数会被设置为`Chinese`。
    
-   请求中的公式需要在公式的首尾加上 `$$`。
    
-   请求中公式若有 `"\"`，需转义成 `"\\"`。
    

**audio\_setting** `_object_` （可选）

**属性**

**sample\_rate** `_integer_` （可选） 默认值为`32000`

设置生成的音频的采样率（单位为Hz）。

取值范围：

-   `8000`
    
-   `16000`
    
-   `22050`
    
-   `24000`
    
-   `32000`
    
-   `44100`
    

**bitrate** `_integer_` （可选） 默认值为`128000`

设置生成的音频的码率（单位kbps）。

取值范围：

-   `32000`
    
-   `64000`
    
-   `128000`
    
-   `256000`
    

**说明**

该参数仅在`format`参数为`mp3`时生效。对于其他格式，该参数将被忽略。

**format** `_string_` （可选） 默认值为`mp3`

设置生成的音频的格式。

取值范围：

-   `mp3`
    
-   `pcm`
    
-   `flac`
    
-   `wav`
    

**channel** `_integer_` （可选） 默认值为`1`

设置生成的音频的声道数。

取值范围：

-   `1`：单声道
    
-   `2`：双声道
    

**force\_cbr** `_boolean_` （可选） 默认值为`false`

是否以恒定码率进行音频编码。

取值范围：

-   `true`：是
    
-   `false`：否
    

**说明**

仅流式输出且音频格式为`mp3`时该参数生效。

**pronunciation\_dict** `_object_` （可选）

**属性**

**tone** `_string[]_` （可选）

定义需要特殊标注的文字或符号对应的注音或发音替换规则。

> 使用 / 作为分隔符。

在中文文本中，声调用数字表示：一声为 1，二声为 2，三声为 3，四声为 4，轻声为 5。

示例：

`["燕少飞/(yan4)(shao3)(fei1)", "omg/oh my god"]`

**timbre\_weights** `_object[]_` （可选）

若需要设置混合音色，请对该参数进行设置。最多支持 4 种音色混合。

**属性**

**voice\_id** `_string_` **（必选）**

设置音色ID。

**weight** `_integer_` **（必选）**

设置音色所占权重，必须与 `voice_id` 同步填写。单一音色取值占比越高，合成音色与该音色相似度越高。

取值范围：`[1, 100]`。

**language\_boost** `_string_` （可选） 默认值为`null`

是否增强对指定的小语种和方言的识别能力。可设置为 `auto` 让模型自主判断。

取值范围（点击查看）：

-   `Chinese`
    
-   `Chinese,Yue`
    
-   `English`
    
-   `Arabic`
    
-   `Russian`
    
-   `Spanish`
    
-   `French`
    
-   `Portuguese`
    
-   `German`
    
-   `Turkish`
    
-   `Dutch`
    
-   `Ukrainian`
    
-   `Vietnamese`
    
-   `Indonesian`
    
-   `Japanese`
    
-   `Italian`
    
-   `Korean`
    
-   `Thai`
    
-   `Polish`
    
-   `Romanian`
    
-   `Greek`
    
-   `Czech`
    
-   `Finnish`
    
-   `Hindi`
    
-   `Bulgarian`
    
-   `Danish`
    
-   `Hebrew`
    
-   `Malay`
    
-   `Persian`
    
-   `Slovak`
    
-   `Swedish`
    
-   `Croatian`
    
-   `Filipino`
    
-   `Hungarian`
    
-   `Norwegian`
    
-   `Slovenian`
    
-   `Catalan`
    
-   `Nynorsk`
    
-   `Tamil`
    
-   `Afrikaans`
    
-   `auto`
    

**voice\_modify** `_object_` （可选）

设置声音效果，该参数支持的音频格式：

-   非流式：`mp3`、`wav`、`flac`
    
-   流式：`mp3`
    

**属性**

**pitch** `_integer_` （可选） 无默认值

设置音高（低沉/明亮）。

数值越低声音越低沉，数值越高声音越明亮。

取值范围：`[-100, 100]`。

**intensity** `_integer_` （可选） 无默认值

设置强度（力量感/柔和）。

数值越低声音越刚劲，数值越高声音越轻柔。

取值范围：`[-100, 100]`。

**timbre** `_integer_` （可选） 无默认值

设置音色明暗程度（磁性/清脆）。

数值越低声音越浑厚，数值越高声音越清脆。

取值范围：`[-100, 100]`。

**sound\_effects** `_string_` （可选） 无默认值

设置音效。

取值范围：

-   `spacious_echo`：空旷回音
    
-   `auditorium_echo`：礼堂广播
    
-   `lofi_telephone`：电话失真
    
-   `robotic`：电音
    

**subtitle\_enable** `_boolean_` （可选） 默认值为`false`

是否开启字幕。

取值范围：

-   `true`：是
    
-   `false`：否
    

**说明**

该参数仅在非流式输出场景下有效，且仅对 `speech-2.8-hd`, `speech-2.8-turbo`, `speech-2.6-hd`, `speech-2.6-turbo`, `speech-02-hd`, `speech-02-turbo`, `speech-01-hd`, `speech-01-turbo` 模型有效。

**output\_format** `_string_` （可选） 默认值为`hex`

设置输出结果形式。

取值范围：

-   `url`：语音合成结果以URL形式返回，有效期为24小时
    
-   `hex`：语音合成结果以二进制形式返回
    

**说明**

该参数仅在非流式场景中生效（流式场景只返回`hex`形式）。

**aigc\_watermark** `_boolean_` （可选） 默认值为`false`

是否在合成音频末尾添加 AIGC 隐性标识。

取值范围：

-   `true`：是
    
-   `false`：否
    

**说明**

该参数仅在非流式输出场景下有效。

## **返回体**

## 非流式

```
{
    "output": {
        "base_resp": {
            "status_code": 0,
            "status_msg": "success"
        },
        "data": {
            "audio": "<hex编码的audio>",
            "status": 2
        },
        "extra_info": {
            "audio_channel": 1,
            "audio_format": "mp3",
            "audio_length": 3528,
            "audio_sample_rate": 16000,
            "audio_size": 58164,
            "bitrate": 128000,
            "invisible_character_ratio": 0,
            "usage_characters": 26,
            "word_count": 14
        },
        "trace_id": "05fdef92e4c1b32283e3d1c456971a80"
    },
    "usage": {
        "characters": 26
    },
    "request_id": "233b9516-1038-9697-b458-87e95a1f8108"
}
```

## 流式

```
{
    "output": {
        "base_resp": {
            "status_code": 0,
            "status_msg": "success"
        },
        "data": {
            "audio": "<hex编码的audio>",
            "status": 2
        },
        "extra_info": {
            "audio_channel": 1,
            "audio_format": "mp3",
            "audio_length": 3528,
            "audio_sample_rate": 16000,
            "audio_size": 58164,
            "bitrate": 128000,
            "invisible_character_ratio": 0,
            "usage_characters": 26,
            "word_count": 14
        },
        "trace_id": "05fdef92e4c1b32283e3d1c456971a80"
    },
    "usage": {
        "characters": 26
    },
    "request_id": "233b9516-1038-9697-b458-87e95a1f8108"
}
```

**request\_id** `_string_`

本次调用的唯一标识符。

**output** `_object_`

模型返回的数据。

**属性**

**base\_resp** `_object_`

本次请求的状态码和详情。

**属性**

**status\_code** `_integer_`

状态码。

您可在header中获取本次会话的trace\_id，用于在咨询/反馈时帮助定位问题

-   `0`: 请求结果正常
    
-   `1000`: 未知错误
    
-   `1001`: 超时
    
-   `1002`: 触发限流
    
-   `1004`: 鉴权失败
    
-   `1039`: 触发 TPM 限流
    
-   `1042`: 非法字符超过 10%
    
-   `2013`: 输入参数信息不正常
    

更多内容可查看 [**错误码查询列表**](https://platform.minimaxi.com/docs/api-reference/errorcode) 了解详情

**status\_msg** `_string_`

状态详情。

**data** `_object_`

返回的合成数据对象，可能为 null，需进行非空判断。

**属性**

**atudio** `_string_`

合成后的音频数据，采用 hex 编码，格式与请求中（`output_format`参数）指定的输出格式一致。

**status** `_integer_`

当前音频流状态：1 表示合成中，2 表示合成结束

**extra\_info** `_object_`

**属性**

**audio\_length**`_integer_`

音频时长（毫秒）

**audio\_sample\_rate**`_integer_`

音频采样率

**audio\_size**`_integer_`

音频文件大小（字节）

**bitrate**`_integer_`

音频比特率

**audio\_format** `_string_`

生成音频文件的格式。取值范围 `[mp3, pcm, flac]`

可用选项： `mp3`, `pcm`, `flac`。

[**​**](https://platform.minimaxi.com/docs/api-reference/speech-t2a-http#response-extra-info-audio-channel)**audio\_channel** `_integer_`

生成音频声道数,1：单声道，2：双声道

[**​**](https://platform.minimaxi.com/docs/api-reference/speech-t2a-http#response-extra-info-invisible-character-ratio)**invisible\_character\_ratio** `_float_`

非法字符占比.非法字符不超过 10%（包含 10%），音频会正常生成,并返回非法字符占比数据；如超过 10% 将进行报错

[**​**](https://platform.minimaxi.com/docs/api-reference/speech-t2a-http#response-extra-info-usage-characters)**usage\_characters**`_integer_`

计费字符数

**word\_count**`_integer_`

已发音的字数统计，包含汉字、数字、字母，不包含标点符号

**trace\_id** `_string_`

本次会话的 id，用于在咨询/反馈时帮助定位问题

**base\_resp** `_object_`

本次请求的状态码和详情。

**属性**

**atudio** `_string_`

合成后的音频数据，采用 hex 编码，格式与请求中（`output_format`参数）指定的输出格式一致。

**usage** `_object_`

本次请求的字符用量。

**属性**

**characters** `_integer_`

输入文本的字符数。
