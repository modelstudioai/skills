# 客户端事件

本文介绍 qwen3.5-livetranslate-flash-realtime API 的客户端事件。

> 相关文档：[实时语音/音视频翻译-千问](https://help.aliyun.com/zh/model-studio/qwen3-5-livetranslate-flash-realtime)。

## **session.update**

客户端建立 WebSocket 连接后，需首先发送该事件，用于更新会话的默认配置。

服务端收到 `session.update` 事件后，会校验参数。如果参数不合法，则返回错误；如果参数合法，则更新并返回完整的配置。

**type** `_string_` **(必选)**

事件类型，固定为`session.update`。

```
{
  "event_id": "event_ToPZqeobitzUJnt3QqtWg",
  "type": "session.update",
  "session": {
    "modalities": [
      "text",
      "audio"
    ],
    "voice": "Tina",
    "sample_rate": 16000,
    "input_audio_format": "pcm",
    "output_audio_format": "pcm",
    "input_audio_transcription": {
      "model": "qwen3-asr-flash-realtime",
      "language": "zh"
    },
    "translation": {
      "language": "en",
      "corpus": {
        "phrases": {
          "人工智能": "Artificial Intelligence",
          "机器学习": "Machine Learning"
        }
      }
    }
  }
}
```

启用声音复刻（`frequency=once`）的示例：

```
{
  "event_id": "event_ToPZqeobitzUJnt3QqtWg",
  "type": "session.update",
  "session": {
    "modalities": [
      "text",
      "audio"
    ],
    "voice": "default",
    "enable_voice_clone": true,
    "voice_clone_options": {
      "frequency": "once"
    },
    "sample_rate": 16000,
    "input_audio_format": "pcm",
    "output_audio_format": "pcm",
    "translation": {
      "language": "en"
    }
  }
}
```

**session** `_object_` （可选）

会话配置。

**属性**

**modalities** `_array_` （可选）

模型输出模态设置，可选值：

-   \["text"\]
    
    仅输出文本。
    
-   \["text","audio"\]（默认值）
    
    输出文本与音频。
    

**voice** `_string_` （可选）

生成音频的音色。未启用声音复刻时，可设置为系统预设音色，可选值参见[支持的音色](https://help.aliyun.com/zh/model-studio/qwen3-5-livetranslate-flash-realtime#0a5bde7593gdk)。Qwen3.5-LiveTranslate-Flash-Realtime默认音色为： `Tina`。Qwen3-LiveTranslate-Flash-Realtime默认音色为： `Cherry`。

> 启用声音复刻（`enable_voice_clone`为`true`）时，`voice`的取值取决于`frequency`：当`frequency`为`once`或`always`时，必须设置为`default`；当`frequency`为`never`时，设置为用户预先复刻的音色 ID。此时不可设置为系统预设音色，否则服务端会返回错误。

**enable\_voice\_clone** `_boolean_` （可选）

是否启用声音复刻。默认值为`false`。启用后，模型会基于输入音频复刻音色用于翻译输出，此时`voice`不再使用系统预设音色，需设置为`default`或用户预先通过[声音复刻API](https://help.aliyun.com/zh/model-studio/qwen-omni-voice-cloning)复刻的音色 ID。

**voice\_clone\_options** `_object_` （可选）

声音复刻控制参数，仅在`enable_voice_clone`为`true`时生效。

**属性**

**voice\_clone\_options.frequency** `_string_` （可选）

音色复刻频率，可选值：

-   `never`
    
    不在服务端进行音色复刻，使用用户预先复刻好的音色。此时`voice`需设置为用户的复刻音色 ID。
    
-   `once`
    
    会话开始时基于输入音频进行一次音色复刻，后续输出复用该音色。适合单人演讲场景。此时`voice`需设置为`default`。
    
-   `always`
    
    每次输出前基于输入音频进行实时音色复刻，音色跟随输入动态变化。适合多人对话场景。此时`voice`需设置为`default`。
    

**sample\_rate** `_integer_` （可选）

输入音频的采样率，单位为Hz。可选值：

-   8000
    
-   16000（默认）
    

**input\_audio\_transcription** `_object_` （可选）

输入音频相关配置。

**属性**

**model** `_string_` （可选）

语音识别模型。配置后，服务端会在翻译的同时返回输入音频的语音识别结果（源语言原文），通过`conversation.item.input_audio_transcription.text`和`conversation.item.input_audio_transcription.completed`事件返回。

可选值：`qwen3-asr-flash-realtime`。

**language** `_string_` （可选）

翻译源语种，可选值：[支持的语种](https://help.aliyun.com/zh/model-studio/qwen3-5-livetranslate-flash-realtime#4ffd192226f0s)。默认值为`en`。

**input\_audio\_format** `_string_` （可选）

用户输入音频格式，可选值：

-   `pcm`（默认）
    
    未压缩的原始音频数据。
    
-   `opus`
    
    有损压缩音频编码，支持低延迟传输，适用于网络语音场景。
    

**output\_audio\_format** `_string_` （可选）

输出音频格式，当前仅支持设为`pcm`。

**translation** `_object_` （可选）

翻译配置。

**属性**

**language** `_string_` （可选）

翻译目标语种，可选值：[支持的语种](https://help.aliyun.com/zh/model-studio/qwen3-5-livetranslate-flash-realtime#4ffd192226f0s)。默认值为`en`。

**corpus** `_object_` （可选）

热词配置，用于提升特定词汇的翻译准确性。

**属性**

**corpus.phrases** `_object_` （可选）

热词映射表。key 为源语言词汇，value 为目标语言对应翻译。

示例：`{"人工智能": "Artificial Intelligence"}`

## **input\_audio\_buffer.append**

向输入音频缓冲区追加音频字节。服务端使用此缓冲区检测并决定语音提交时机。

**type** `_string_` **(必选)**

事件类型，固定为`input_audio_buffer.append`。

```
{
    "event_id": "event_xxx",
    "type": "input_audio_buffer.append",
    "audio": "xxx"
}
```

**audio** `_string_` **(必选)**

Base64 编码的音频数据。

## **input\_image\_buffer.append**

用于将图像数据添加到图像缓冲区。图像可来自本地文件，或从视频流实时采集。

目前对图片输入有以下限制：

-   图像格式必须为 JPG 或 JPEG。建议分辨率为 480p 或 720p以获得最佳性能，最高不超过 1080p；
    
-   单张图片大小不大于500KB（Base64编码前）；
    
-   图片数据需要经过Base64编码；
    
-   以不超过每秒 2 张的频率向缓冲区添加图像；
    
-   发送 input\_image\_buffer.append 事件前，至少发送过一次 input\_audio\_buffer.append 事件。
    

**type** `_string_` **(必选)**

事件类型，固定为`input_image_buffer.append`。

```
{
    "event_id": "event_xxx",
    "type": "input_image_buffer.append",
    "image": "xxx"
}
```

**image** `_string_` **(必选）**

Base64 编码的图像数据。

## **session.finish**

用于结束当前会话。发送此事件后，服务端响应流程：

-   已检测到语音：服务端完成语音识别后，发送包含识别结果的[conversation.item.input\_audio\_transcription.completed](https://help.aliyun.com/zh/model-studio/live-translator-server-events#asr003comph2)事件，随后发送[session.finished](https://help.aliyun.com/zh/model-studio/qwen-asr-realtime-server-events#6eaa77339djdv)事件作为会话结束标识。
    
-   未检测到语音：服务端直接发送`[session.finished](https://help.aliyun.com/zh/model-studio/qwen-asr-realtime-server-events#6eaa77339djdv)`事件。
    

客户端监听到`[session.finished](https://help.aliyun.com/zh/model-studio/qwen-asr-realtime-server-events#6eaa77339djdv)`事件后，需主动断开连接。

**type** `_string_` **(必选)**

事件类型，固定为`session.finish`。

```
{
    "event_id": "event_xxx",
    "type": "session.finish"
}
```
