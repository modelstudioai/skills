# 实时语音识别（Qwen-ASR-Realtime）客户端事件

本文档介绍在与 Qwen-ASR Realtime API 的 WebSocket 会话中，客户端向服务端发送的事件。

**用户指南：**模型介绍、功能特性和完整示例代码请参见[实时语音识别-千问](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide)

## **session.update**

用于更新会话配置，建议在 WebSocket 连接建立后首先发送该事件。建议在WebSocket连接建立成功后，立即发送此事件作为交互的第一步。如果未发送，系统将使用默认配置。

服务端成功处理此事件后，会发送`[服务端事件](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime-server-events#424ef2e774q9p)`事件作为确认。

**参数**

**类型**

**是否必须**

**说明**

type

string

是

事件类型。固定为`session.update`。

event\_id

string

是

事件ID。

session

object

是

包含会话配置的对象。

session.input\_audio\_format

string

否

音频格式。支持`pcm`和`opus`。

默认值：`pcm`。

session.sample\_rate

integer

否

音频采样率（Hz）。支持`16000`和`8000`。

默认值：`16000`。

设置为 `8000` 时，服务端会先升采样到16000Hz再进行识别，可能引入微小延迟。建议仅在源音频为8000Hz（如电话线路）时使用。

session.input\_audio\_transcription

object

否

语音识别相关配置。

session.input\_audio\_transcription.language

string

否

音频源语言。

-   zh：中文（普通话、四川话、闽南语、吴语）
    
-   yue：粤语
    
-   en：英文
    
-   ja：日语
    
-   de：德语
    
-   ko：韩语
    
-   ru：俄语
    
-   fr：法语
    
-   pt：葡萄牙语
    
-   ar：阿拉伯语
    
-   it：意大利语
    
-   es：西班牙语
    
-   hi：印地语
    
-   id：印尼语
    
-   th：泰语
    
-   tr：土耳其语
    
-   uk：乌克兰语
    
-   vi：越南语
    
-   cs：捷克语
    
-   da：丹麦语
    
-   fil：菲律宾语
    
-   fi：芬兰语
    
-   is：冰岛语
    
-   ms：马来语
    
-   no：挪威语
    
-   pl：波兰语
    
-   sv：瑞典语
    

session.turn\_detection

object

否

VAD（Voice Activity Detection，语音活动检测）配置。

它是启用/关闭VAD模式的开关：若将它设为null，则将关闭[VAD 模式](https://help.aliyun.com/zh/model-studio/qwen-asr-realtime-interaction-process#9b49887720jcw)，启用[Manual 模式](https://help.aliyun.com/zh/model-studio/qwen-asr-realtime-interaction-process#ee09a3493fsuc)；反之则相反。

session.turn\_detection.type

string

否，`turn_dection`存在时必须

固定为 `server_vad`。

session.turn\_detection.threshold

float

否

VAD检测阈值。推荐将该值设为`0.0`。

默认值：`0.2`。

取值范围：`[-1, 1]`。

较低的阈值会提高 VAD 的灵敏度，可能将背景噪音误判为语音。较高的阈值则降低灵敏度，有助于在嘈杂环境中减少误触发。

session.turn\_detection.silence\_duration\_ms

integer

否

VAD断句检测阈值（ms）。静音持续时长超过该阈值将被认为是语句结束。推荐将该值设为`400`。

默认值：`800`。

取值范围：`[200, 6000]`。

较低的值（如 300ms）可使模型更快响应，但可能导致在自然停顿处发生不合理的断句。较高的值（如 1200ms）可更好地处理长句内的停顿，但会增加整体响应延迟。

```
{
    "event_id": "event_123",
    "type": "session.update",
    "session": {
        "input_audio_format": "pcm",
        "sample_rate": 16000,
        "input_audio_transcription": {
            "language": "zh"
        },
        "turn_detection": {
            "type": "server_vad",
            "threshold": 0.0,
            "silence_duration_ms": 400
        }
    }
}
```

## **input\_audio\_buffer.append**

用于将音频数据块追加到服务端的输入缓冲区。这是流式发送音频的核心事件。

**不同场景下的区别：**

-   **VAD 模式**：音频缓冲区用于语音活动检测，服务端会自动决定何时提交音频进行识别。
    
-   **非VAD模式**：客户端可以控制每个事件中的音频数据量，单个 `input_audio_buffer.append` 事件中的 `audio` 字段内容最大为 15 MiB。建议流式发送较小的音频块以获得更快的响应。
    

**重要提示**：服务端不会对`input_audio_buffer.append`事件发送任何确认响应。

**参数**

**类型**

**是否必须**

**说明**

type

string

是

事件类型。固定为`input_audio_buffer.append`。

event\_id

string

是

事件ID。

audio

string

是

Base64编码的音频数据。

```
{
  "event_id": "event_2728",
  "type": "input_audio_buffer.append",
  "audio": "<audio> by base64"
}
```

## **input\_audio\_buffer.commit**

非VAD模式下，用于手动触发识别。此事件通知服务端，客户端已发送完一段完整的语音，将当前缓冲区内的所有音频数据作为一个整体进行识别。

**禁用场景：**VAD模式。

服务端成功处理后，会发送`[input_audio_buffer.committed](https://help.aliyun.com/zh/model-studio/qwen-asr-realtime-server-events#1108a3764an0e)`事件作为确认响应。

**参数**

**类型**

**是否必须**

**说明**

type

string

是

事件类型。固定为`input_audio_buffer.commit`。

event\_id

string

是

事件ID。

```
{
  "event_id": "event_789",
   "type": "input_audio_buffer.commit"
}
```

## **session.finish**

用于结束当前会话。

服务端响应流程：

-   已检测到语音：服务端完成最后的语音识别后，发送包含识别结果的`[conversation.item.input_audio_transcription.completed](https://help.aliyun.com/zh/model-studio/qwen-asr-realtime-server-events#403ecacd74qqg)`事件，随后发送[session.finished](https://help.aliyun.com/zh/model-studio/qwen-asr-realtime-server-events#6eaa77339djdv)事件作为会话结束标识。
    
-   未检测到语音：服务端直接发送`[session.finished](https://help.aliyun.com/zh/model-studio/qwen-asr-realtime-server-events#6eaa77339djdv)`事件。
    

客户端监听到`[session.finished](https://help.aliyun.com/zh/model-studio/qwen-asr-realtime-server-events#6eaa77339djdv)`事件后，需主动断开连接。

**参数**

**类型**

**是否必须**

**说明**

type

string

是

事件类型。固定为`session.finish`。

event\_id

string

是

事件ID。

```
{
  "event_id": "event_341",
  "type": "session.finish",
}
```
