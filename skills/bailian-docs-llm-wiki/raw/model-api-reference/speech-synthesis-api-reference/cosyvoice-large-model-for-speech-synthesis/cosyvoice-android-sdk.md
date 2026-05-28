# 语音合成CosyVoice Android SDK

本文档提供了语音合成CosyVoice Android SDK的详细使用指南，帮助您将文本转换为高质量、富有表现力的语音。

**用户指南：**关于模型介绍和选型建议请参见[语音合成](https://help.aliyun.com/zh/model-studio/tts-model/)。

## **NativeNui**

本SDK基于NativeNui单例架构，通过回调机制处理语音合成事件。

**架构特点**：

-   **单例模式：**通过 `NativeNui.GetInstance()` 获取全局唯一实例
    
-   **回调驱动：**通过 [`INativeStreamInputTtsCallback`](#secstreamcallback) 接口接收事件和数据
    
-   **事件类型：**
    
    -   [`STREAM_INPUT_TTS_EVENT_SYNTHESIS_STARTED`](#secstreamevent)：合成任务开始
        
    -   [`onStreamInputTtsDataCallback`](#secstreamdatacallback)：音频数据返回
        
    -   [`STREAM_INPUT_TTS_EVENT_SYNTHESIS_COMPLETE`](#secstreamevent)：合成任务结束
        
    -   [`STREAM_INPUT_TTS_EVENT_TASK_FAILED`](#secstreamevent)：合成出错
        

### **使用流程**

CosyVoice 支持一次性输入和流式输入两种调用方式。

**一次性输入**：适用于短文本合成、需要使用 SSML 标记语言的场景。

1.  [`startStreamInputTts()`](#secstartstreamtts)\- 初始化SDK，设置回调接口和连接参数
    
2.  [`playStreamInputTts()`](#secplaystreamtts)或 [`asyncPlayStreamInputTts()`](#secasyncplaystreamtts)\- 发送文本并开始语音合成
    
3.  [`onStreamInputTtsDataCallback()`](#secstreamdatacallback)\- 接收音频数据
    
4.  [`STREAM_INPUT_TTS_EVENT_SYNTHESIS_COMPLETE`](#secstreamevent)\- 语音合成结束
    

**流式输入**：适用于实时对话、长文本“边说边合”的场景。此方式不支持 SSML 标记语言。

1.  [`startStreamInputTts()`](#secstartstreamtts)\- 初始化SDK，设置回调接口和连接参数
    
2.  [`sendStreamInputTts()`](#secsendstreamtts)\- 持续发送待合成文本
    
3.  [`onStreamInputTtsDataCallback()`](#secstreamdatacallback)\- 接收音频数据
    
4.  [`stopStreamInputTts()`](#secstopstreamtts)或 [`asyncStopStreamInputTts()`](#secasyncstopstreamtts)\- 结束发送，等待合成完成
    
5.  [`STREAM_INPUT_TTS_EVENT_SYNTHESIS_COMPLETE`](#secstreamevent)\- 语音合成结束
    

### **startStreamInputTts**

启动双向流式语音合成，建立与服务端的连接，并注册回调以接收事件和音频数据。

此接口可能会引起阻塞，应在非UI线程调用。

**方法签名：**

```
public synchronized int startStreamInputTts(INativeStreamInputTtsCallback callback,
                                            String ticket,
                                            String parameters,
                                            String session_id,
                                            int log_level,
                                            boolean save_log)
```

**参数说明：**

**参数**

**类型**

**说明**

`callback`

[`INativeStreamInputTtsCallback`](#secstreamcallback)

事件和数据回调接口的实现。

`ticket`

`String`

JSON字符串，包含鉴权、连接和调试参数。详见下方 ticket 参数说明。

`parameters`

`String`

JSON字符串，包含语音合成的具体效果参数。详见下方 parameters 参数说明。

`session_id`

`String`

客户端指定的会话ID。若不传入，服务端将自动生成。

`log_level`

`int`

控制SDK自身日志的打印级别。

取值范围：

-   0：LOG\_LEVEL\_VERBOSE
    
-   1：LOG\_LEVEL\_DEBUG
    
-   2：LOG\_LEVEL\_INFO
    
-   3：LOG\_LEVEL\_WARNING
    
-   4：LOG\_LEVEL\_ERROR
    
-   5：LOG\_LEVEL\_NONE（表示关闭此功能）
    

`save_log`

`boolean`

是否保存本地日志。若为true，须在ticket 参数中通过`debug_path`指定路径，并可通过`max_log_file_size`设置文件大小。

**返回值说明：**

返回[错误码](https://help.aliyun.com/zh/isi/support/error-codes)。

**ticket JSON 示例**：

```
{
    "url": "wss://dashscope.aliyuncs.com/api-ws/v1/inference",
    "apikey": "sk-****",
    "device_id": "my_device_id"
}
```

**ticket 参数说明：**

**参数**

**类型**

**是否必须**

**说明**

`url`

`String`

是

服务地址，固定为 `wss://dashscope.aliyuncs.com/api-ws/v1/inference`。

`apikey`

`String`

是

API Key。建议使用时效性短、安全性更高的[临时API Key](https://help.aliyun.com/zh/model-studio/generate-temporary-api-key)，以降低长期有效Key泄露的风险。

`device_id`

`String`

是

用于标识终端用户的唯一字符串，可设为应用内用户ID或客户端生成的设备唯一标识符。此ID主要用于日志追踪和问题排查。

`complete_waiting_ms`

`int`

否

调用[stop接口](#secstopstreamtts)后，等待合成完成事件（[STREAM\_INPUT\_TTS\_EVENT\_SYNTHESIS\_COMPLETE](#secstreamevent)）的超时时间（毫秒）。

默认值：10000。

`debug_path`

`String`

否

日志文件的存储路径。

此参数仅在调用[startStreamInputTts](#secstartstreamtts)、[playStreamInputTts](#secplaystreamtts)或[asyncPlayStreamInputTts](#secasyncplaystreamtts)接口时将`save_log`设为true时生效。此时必须设置日志文件路径，否则将报错。

本地最多保留两个日志文件。

`max_log_file_size`

`int`

否

设定日志文件的最大字节数。

此参数仅在调用[startStreamInputTts](#secstartstreamtts)、[playStreamInputTts](#secplaystreamtts)或[asyncPlayStreamInputTts](#secasyncplaystreamtts)接口时将`save_log`设为true时生效。

默认值：104857600（100 \* 1024 \* 1024 字节, 即 100MiB）。

`log_track_level`

`int`

否

控制通过日志回调（[`onStreamInputTtsLogTrackCallback`](#secstreamlogcallback)）对外发送的日志内容的过滤级别。

默认值：2。

取值范围：

-   0：LOG\_LEVEL\_VERBOSE
    
-   1：LOG\_LEVEL\_DEBUG
    
-   2：LOG\_LEVEL\_INFO
    
-   3：LOG\_LEVEL\_WARNING
    
-   4：LOG\_LEVEL\_ERROR
    
-   5：LOG\_LEVEL\_NONE（表示关闭此功能）
    

注意：`log_track_level`与`log_level`（通过[startStreamInputTts](#secstartstreamtts)、[playStreamInputTts](#secplaystreamtts)或[asyncPlayStreamInputTts](#secasyncplaystreamtts)接口设置）共同决定最终回调的日志。一条日志的级别数值必须同时大于或等于`log_track_level`和`log_level`的值，才会被回调。例如，`log_track_level`设为2 (INFO)，`log_level`设为3 (WARNING)，则只有WARNING及以上级别（数值>=3）的日志才会被回调。

**parameters JSON 示例**：

```
{
    "model": "cosyvoice-v2",
    "voice": "longxiaochun",
    "format": "mp3",
    "volume": 50,
    "rate": 1.0,
    "pitch": 1.0
}
```

**parameters 参数说明**：

**参数**

**类型**

**是否必须**

**说明**

`model`

`String`

是

模型名称。

`voice`

`String`

是

语音合成所使用的音色。

-   **系统音色**：参见[音色列表](https://help.aliyun.com/zh/model-studio/cosyvoice-voice-list)
    
-   **复刻音色**：通过声音复刻功能定制
    
-   **声音设计音色**：通过声音设计功能定制
    

`format`

`String`

否

音频编码格式。

取值范围：

-   pcm
    
-   wav
    
-   mp3（默认）
    
-   opus
    

**重要**

`cosyvoice-v1`不支持opus格式。

`volume`

`int`

否

音量。

默认值：50。

取值范围：\[0, 100\]。

`sample_rate`

`int`

否

音频采样率（Hz）。

取值范围：8000, 16000, 22050（默认）, 24000, 44100, 48000。

`rate`

`float`

否

语速。

默认值：1.0。

取值范围：\[0.5, 2.0\]。

`pitch`

`float`

否

音调。

默认值：1.0。

取值范围：\[0.5, 2.0\]。

`bit_rate`

`int`

否

音频码率（kbps）。音频格式为opus时，支持通过`bit_rate`参数调整码率。

默认值：32。

取值范围：\[6, 510\]。

`cosyvoice-v1`模型不支持该参数。

`enable_ssml`

`boolean`

否

是否开启SSML功能。

默认值：false。

-   true：开启。
    
-   false：关闭。
    

`word_timestamp_enabled`

`boolean`

否

是否开启字级别时间戳。

默认值：false。

适用范围：仅适用于cosyvoice-v3-flash、cosyvoice-v3-plus和cosyvoice-v2模型的复刻音色，以及[音色列表](https://help.aliyun.com/zh/model-studio/cosyvoice-voice-list)中标记为支持的系统音色。

> 时间戳结果在[INativeStreamInputTtsCallback](#secstreamcallback)的all\_response中。

`seed`

`int`

否

生成时使用的随机数种子，使合成的效果产生变化。在模型版本、文本、音色及其他参数均相同的前提下，使用相同的seed可复现相同的合成结果。

默认值0。

取值范围：\[0, 65535\]。

cosyvoice-v1不支持该参数。

`language_hints`

`String[]`

否

**重要**

-   此参数为数组，但当前版本仅处理第一个元素，因此建议只传入一个值。
    
-   此参数用于指定语音合成的目标语言，该设置与声音复刻时的样本音频的语种无关。如需设置复刻任务的源语言，请参见声音复刻API参考。
    

指定语音合成的目标语言，提升合成效果。cosyvoice-v1不支持该功能。

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
    

`instruction`

`String`

否

设置指令，用于控制方言、情感或角色等合成效果。

使用说明请参见[指令控制](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#12884a10929p9)。

`enable_aigc_tag`

`boolean`

否

是否在生成的音频中添加AIGC隐性标识。设置为true时，会将隐性标识嵌入到支持格式（wav/mp3/opus）的音频中。

默认值：false。

仅cosyvoice-v3-flash、cosyvoice-v3-plus、cosyvoice-v2支持该功能。

`aigc_propagator`

`String`

否

设置AIGC隐性标识中的 `ContentPropagator` 字段，用于标识内容的传播者。仅在 `enable_aigc_tag` 为 `true` 时生效。

默认值：阿里云UID。

仅cosyvoice-v3-flash、cosyvoice-v3-plus、cosyvoice-v2支持该功能。

`aigc_propagate_id`

`String`

否

设置AIGC隐性标识中的 `PropagateID` 字段，用于唯一标识一次具体的传播行为。仅在 `enable_aigc_tag` 为 `true` 时生效。

默认值：本次语音合成请求Request ID。

仅cosyvoice-v3-flash、cosyvoice-v3-plus、cosyvoice-v2支持该功能。

### **sendStreamInputTts**

发送待合成的文本，与 [startStreamInputTts](#secstartstreamtts) 搭配使用。

在调用 [startStreamInputTts](#secstartstreamtts) 后，使用此接口持续发送文本。

所有文本发送完毕后，需调用[stopStreamInputTts](#secstopstreamtts)或[asyncStopStreamInputTts](#secasyncstopstreamtts)来结束发送。

**方法签名：**

```
public synchronized int sendStreamInputTts(String text)
```

**参数说明：**

**参数**

**类型**

**说明**

`text`

`String`

待合成文本。不支持[SSML](https://help.aliyun.com/zh/model-studio/introduction-to-cosyvoice-ssml-markup-language)。如果传入的文本包含SSML标签，这些标签将被当作普通文本读出，不会被解析。

**返回值说明：**

返回[错误码](https://help.aliyun.com/zh/isi/support/error-codes)。

### **stopStreamInputTts**

同步接口，通知服务端文本已全部发送，并阻塞等待所有音频数据合成并收到 [STREAM\_INPUT\_TTS\_EVENT\_SYNTHESIS\_COMPLETE](#secstreamevent)。

阻塞等待的超时时间由参数 [complete\_waiting\_ms](#secstartstreamtts) 控制。

**方法签名：**

```
public synchronized int stopStreamInputTts()
```

**返回值说明：**

返回[错误码](https://help.aliyun.com/zh/isi/support/error-codes)。

### **asyncStopStreamInputTts**

异步接口，通知服务端文本已全部发送。调用后立即返回，合成在后台继续进行。

通过 [STREAM\_INPUT\_TTS\_EVENT\_SYNTHESIS\_COMPLETE](#secstreamevent) 事件判断合成是否完成。

**方法签名：**

```
public synchronized int asyncStopStreamInputTts()
```

**返回值说明：**

返回[错误码](https://help.aliyun.com/zh/isi/support/error-codes)。

### **cancelStreamInputTts**

立即中断与服务端的连接并终止当前合成任务。调用后不会再收到任何音频数据回调。

**方法签名：**

```
public synchronized int cancelStreamInputTts()
```

**返回值说明：**

返回[错误码](https://help.aliyun.com/zh/isi/support/error-codes)。

### **playStreamInputTts**

同步执行的一次性合成接口。该接口会发送文本、阻塞并等待接收所有音频数据，直到合成完成后才返回。无需再调用[stop接口](#secstopstreamtts)。

该接口默认启用SSML。如果显式设置enable\_ssml，则以用户设置为准。

此接口应在非UI线程调用。

**方法签名：**

```
public synchronized int playStreamInputTts(INativeStreamInputTtsCallback callback,
                                           String ticket,
                                           String parameters,
                                           String text,
                                           String session_id,
                                           int log_level,
                                           boolean save_log)
```

**参数说明：**

callback、ticket等参数与[startStreamInputTts](#secstartstreamtts)接口中的定义相同。

**参数**

**类型**

**说明**

`text`

`String`

待合成文本。支持[SSML](https://help.aliyun.com/zh/model-studio/introduction-to-cosyvoice-ssml-markup-language)。

**返回值说明：**

返回[错误码](https://help.aliyun.com/zh/isi/support/error-codes)。

### **asyncPlayStreamInputTts**

异步执行的一次性合成接口。调用后立即返回，合成任务在后台进行，结果通过回调返回。无需再调用[stop接口](#secstopstreamtts)。

该接口默认启用SSML。如果显式设置enable\_ssml，则以用户设置为准。

**方法签名：**

```
public synchronized int asyncPlayStreamInputTts(INativeStreamInputTtsCallback callback,
                                           String ticket,
                                           String parameters,
                                           String text,
                                           String session_id,
                                           int log_level,
                                           boolean save_log)
```

**参数说明：**

callback、ticket等参数与[startStreamInputTts](#secstartstreamtts)接口中的定义相同。

**参数**

**类型**

**说明**

`text`

`String`

待合成文本。支持[SSML](https://help.aliyun.com/zh/model-studio/introduction-to-cosyvoice-ssml-markup-language)。

**返回值说明：**

返回[错误码](https://help.aliyun.com/zh/isi/support/error-codes)。

## **INativeStreamInputTtsCallback**

CosyVoice 流式语音合成回调接口，用于接收合成事件、音频数据和日志。

### **onStreamInputTtsEventCallback：监听事件**

**方法签名：**

```
void onStreamInputTtsEventCallback(StreamInputTtsEvent event,
                                   String task_id,
                                   String session_id,
                                   int ret_code,
                                   String error_msg,
                                   String timestamp,
                                   String all_response);
```

**参数说明：**

**参数**

**类型**

**说明**

`event`

[`StreamInputTtsEvent`](#secstreamevent)

回调事件。

`task_id`

`String`

语音合成任务ID。

`session_id`

`String`

会话ID。客户端传入则原样返回；未传入时由服务端生成。

`ret_code`

`int`

[错误码](https://help.aliyun.com/zh/isi/support/error-codes)，仅在事件 [STREAM\_INPUT\_TTS\_EVENT\_TASK\_FAILED](#secstreamevent) 中有效。

`error_msg`

`String`

错误信息，仅在事件 [STREAM\_INPUT\_TTS\_EVENT\_TASK\_FAILED](#secstreamevent) 中有效。

`timestamp`

`String`

合成结果的时间戳信息。

`all_response`

`String`

完整的 JSON 字符串响应。可解析以获取所需数据。

### **onStreamInputTtsDataCallback：监听音频数据**

合成过程中，SDK 会连续触发此回调，需在回调中获取音频数据。

**方法签名：**

```
void onStreamInputTtsDataCallback(byte[] data);
```

**参数说明：**

**参数**

**类型**

**说明**

`data`

`byte[]`

返回当前片段的音频数据，可用于：

-   合成完整的音频文件并播放。
    
-   通过支持流式播放的播放器实时播放。
    

注意：

-   对 mp3/opus 压缩格式，分段传输必须使用流式播放器，不能逐帧播放，否则可能解码失败。
    
-   组装完整文件时需采用追加模式写入同一文件。
    
-   对于 wav 和 mp3 格式，仅在第一次 onStreamInputTtsDataCallback 回调的数据中包含文件头，后续回调均为纯音频数据。处理时需将所有回调的 `buffer` 按顺序拼接。opus 格式的每一帧都是独立的 Ogg page，可直接拼接。
    

### **onStreamInputTtsLogTrackCallback：监听追踪日志**

此回调用于接收 SDK 内部的详细日志，方便进行问题定位和调试。

**方法签名：**

```
default void onStreamInputTtsLogTrackCallback(Constants.LogLevel level, String log)
```

## **StreamInputTtsEvent**

CosyVoice 流式语音合成事件类型枚举。

**事件**

**说明**

STREAM\_INPUT\_TTS\_EVENT\_SYNTHESIS\_STARTED

表示服务端已成功接收请求并开始处理。通常在此事件后，[`onStreamInputTtsDataCallback`](#secstreamdatacallback)将很快开始返回第一批音频数据。

STREAM\_INPUT\_TTS\_EVENT\_SENTENCE\_SYNTHESIS

语音合成运行过程中的信息，包括计费信息等。

STREAM\_INPUT\_TTS\_EVENT\_SYNTHESIS\_COMPLETE

表示服务端已发送完全部音频数据，此后 [`onStreamInputTtsEventCallback`](#secstreameventcallback)将不会再被调用。收到此事件是数据流结束的明确信号。

STREAM\_INPUT\_TTS\_EVENT\_TASK\_FAILED

表示任务失败。此时可从[INativeStreamInputTtsCallback](#secstreamcallback)的all\_response获得task\_id、error\_code、error\_message用于判断具体错误。

```
{
    "header": {
        "task_id": "2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx",
        "event": "task-failed",
        "error_code": "InvalidParameter",
        "error_message": "[tts:]Engine return error code: 418",
        "attributes": {}
    },
    "payload": {}
}
```

## **示例代码**

1.  **获取API Key：**[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，为安全起见，推荐将API Key配置到环境变量。
    
    **说明**
    
    当您需要为第三方应用或用户提供临时访问权限，或者希望严格控制敏感数据访问、删除等高风险操作时，建议使用[临时API Key](https://help.aliyun.com/zh/model-studio/generate-temporary-api-key)。临时API Key拥有固定的60秒有效期，过期后需重新获取。
    
2.  **下载SDK并运行示例代码：**
    
    -   [下载最新SDK整合包](https://help.aliyun.com/zh/isi/sdk-selection-and-download)。
        
    -   解压 ZIP 包。在 `app/libs` 目录中获取 AAR 格式 SDK，并添加到项目依赖。  
        需要 Android CPP 接入时，使用 ZIP 包内的 `android_libs` 与 `android_include` 获取动态库和头文件。
        
    -   用 Android Studio 打开工程。示例代码位于`DashCosyVoiceStreamTtsActivity.java`，替换 API Key 后体验功能。
        

### **调用方式**

**调用方式**

**说明**

一次性输入待合成文本

**调用步骤：**

1.  初始化 SDK 和播放器组件。
    
2.  按业务需求设置参数。
    
3.  调用 [playStreamInputTts](#be00eb5c18hnz)或`[asyncPlayStreamInputTts](#2d43b13c45u3g)`发送文本并开始语音合成。
    
4.  接收到 `STREAM_INPUT_TTS_EVENT_SYNTHESIS_COMPLETE` 回调，语音合成结束。
    

**适用场景：**

-   短文本合成
    
-   需要使用 SSML 标记语言
    

流式输入待合成文本

**调用步骤：**

1.  初始化 SDK 和播放器组件。
    
2.  按业务需求设置参数。
    
3.  调用 `[startStreamInputTts](#05eab5125e2pm)` 开始流式文本语音合成。
    
4.  调用 `[sendStreamInputTts](#9e9bf0b955cit)` 持续发送文本。
    
5.  在`[onStreamInputTtsDataCallback](#bc71fe2545pfy)`中，获取二进制音频数据。
    
6.  调用 `[stopStreamInputTts](#eec84caadcq73)` 或 `[asyncStopStreamInputTts](#20ff030ae9j4f)` 结束发送，等待合成完成。
    
7.  接收到 `STREAM_INPUT_TTS_EVENT_SYNTHESIS_COMPLETE` 回调，语音合成结束。
    

**适用场景：**

-   实时对话、长文本“边说边合”
    
-   此方式不支持 SSML 标记语言
    

## **高级功能**

### **SSML 标记语言**

**目的**：通过在文本中嵌入 XML 标签，实现对发音、语速、停顿等细节的精确控制。

**使用限制**：仅支持[一次性输入待合成文本](#f8b7cc6ae3s40)（`[playStreamInputTts](#be00eb5c18hnz)` 或 `[asyncPlayStreamInputTts](#2d43b13c45u3g)` 接口），不支持[流式输入待合成文本](#2e911197440yt)（`[sendStreamInputTts](#9e9bf0b955cit)` 接口）。

**使用方法**：调用 `[playStreamInputTts](#be00eb5c18hnz)`或`[asyncPlayStreamInputTts](#2d43b13c45u3g)`接口时，SDK 会自动启用 SSML，此时直接在 `text` 参数中传入包含 SSML 标签的文本即可。

更多说明请参见 [SSML标记语言介绍](https://help.aliyun.com/zh/model-studio/introduction-to-cosyvoice-ssml-markup-language)。

### **数学表达式**

**目的**：使模型能够正确朗读常见的数学公式和表达式。

**使用方法**：直接在 `text` 参数中传入包含 LaTeX 格式的数学表达式的文本即可。更多说明请参见 [LaTeX 公式转语音](https://help.aliyun.com/zh/model-studio/latex-capability-support-description)。
