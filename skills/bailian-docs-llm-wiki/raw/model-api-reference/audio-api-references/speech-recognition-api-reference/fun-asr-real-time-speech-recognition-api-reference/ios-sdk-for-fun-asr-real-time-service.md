# Qwen-Audio-3.0-ASR-Flash-Streaming/Fun-ASR-Realtime实时语音识别iOS SDK

本文档提供了Qwen-Audio-3.0-ASR-Flash-Streaming/Fun-ASR-Realtime实时语音识别iOS SDK的详细使用指南，帮助您将语音转换为文本。

**用户指南：**关于模型介绍和选型建议请参见[语音识别](raw/model-user-guide/model-experience/asr-model.md)。

## 快速开始

1.  **获取API Key：**[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)
    
2.  **下载SDK并运行示例代码：**
    -   [下载最新SDK整合包](https://help.aliyun.com/zh/isi/sdk-selection-and-download)。
    -   解压 ZIP 包，将其中的 nuisdk.framework 添加到工程。
    -   在 Build Phases → Link Binary With Libraries 中添加 nuisdk.framework。
    -   在 General → Frameworks, Libraries, and Embedded Content 中将 nuisdk.framework 设置为 Embed & Sign。
    -   用 Xcode 打开示例工程。示例代码位于`DashFunAsrSpeechTranscriberViewController.m`，替换 API Key 后体验功能。

### 调用步骤

1.  初始化 SDK
2.  按业务需求设置参数：通过[nui\_initialize](https://help.aliyun.com/zh/model-studio/ios-sdk-for-fun-asr-real-time-service#05eab5125e2pm)接口设置[连接与控制参数](https://help.aliyun.com/zh/model-studio/ios-sdk-for-fun-asr-real-time-service#57acf5ecc1w8j)；通过[nui\_set\_params](https://help.aliyun.com/zh/model-studio/ios-sdk-for-fun-asr-real-time-service#763672f3f8dgw)接口设置[语音识别效果参数](https://help.aliyun.com/zh/model-studio/ios-sdk-for-fun-asr-real-time-service#d20cce9518kla)。
3.  调用[nui\_dialog\_start](https://help.aliyun.com/zh/model-studio/ios-sdk-for-fun-asr-real-time-service#8fe6ea298apzu)启动识别流程。
4.  在[onNuiAudioStateChanged](https://help.aliyun.com/zh/model-studio/ios-sdk-for-fun-asr-real-time-service#bc71fe2545pfy)回调中，根据音频状态开启录音设备。
5.  在[onNuiNeedAudioData](https://help.aliyun.com/zh/model-studio/ios-sdk-for-fun-asr-real-time-service#46174611d31qf)回调中持续提供录音数据。
6.  在[onNuiEventCallback](https://help.aliyun.com/zh/model-studio/ios-sdk-for-fun-asr-real-time-service#163c1ef871tqt)回调中监听事件并获取语音识别结果。
7.  调用[nui\_dialog\_cancel](https://help.aliyun.com/zh/model-studio/ios-sdk-for-fun-asr-real-time-service#156934a01bzjc)停止识别，并通过监听EVENT\_TRANSCRIBER\_COMPLETE事件确认识别已结束。
8.  当识别功能不再使用时，调用[nui\_release](https://help.aliyun.com/zh/model-studio/ios-sdk-for-fun-asr-real-time-service#6c2931e9ae3eq)接口释放 SDK 资源。

## 请求参数

### 连接与控制参数

通过在[nui\_initialize](https://help.aliyun.com/zh/model-studio/ios-sdk-for-fun-asr-real-time-service#05eab5125e2pm)接口的`parameters`参数中传入一个JSON字符串来配置。

-   **参数示例：**以下为 JSON 字符串示例，参数未完整列出。请按实际需求在编码时补充：

```
{
    "url": "wss://dashscope.aliyuncs.com/api-ws/v1/inference",
    "apikey": "st-****",
    "device_id": "my_device_id",
    "service_mode": "1"
}
```

-   **参数说明**
    
    **参数**
    
    **类型**
    
    **是否必须**
    
    **说明**
    
    `url`
    
    `String`
    
    是
    
    服务地址，固定为 `wss://dashscope.aliyuncs.com/api-ws/v1/inference`。
    
    `apikey`
    
    `String`
    
    是
    
    API Key。
    
    `service_mode`
    
    `String`
    
    是
    
    运行模式。实时语音识别固定为 `"1"`。
    
    `device_id`
    
    `String`
    
    是
    
    用于标识终端用户的唯一字符串，可设为应用内用户ID或客户端生成的设备唯一标识符。此ID主要用于日志追踪和问题排查。
    
    `debug_path`
    
    `String`
    
    否
    
    日志文件的存储路径。
    
    此参数仅在调用[nui\_initialize](https://help.aliyun.com/zh/model-studio/ios-sdk-for-fun-asr-real-time-service#05eab5125e2pm)接口时将`save_log`设为`YES`时生效。此时必须设置日志文件路径，否则将报错。
    
    本地最多保留两个日志文件。
    
    `save_wav`
    
    `String`
    
    否
    
    是否保存调试用的音频文件。音频文件保存于`debug_path`下。
    
    默认值："false"。
    
    取值范围：
    
    -   "true"：是
        
    -   "false"：否
        
    
    此参数仅在调用[nui\_initialize](https://help.aliyun.com/zh/model-studio/ios-sdk-for-fun-asr-real-time-service#05eab5125e2pm)接口时将`save_log`设为true时生效。 同时，`debug_path`也必须被设置。
    
    `max_log_file_size`
    
    `int`
    
    否
    
    设定日志文件的最大字节数。
    
    此参数仅在调用[nui\_initialize](https://help.aliyun.com/zh/model-studio/ios-sdk-for-fun-asr-real-time-service#05eab5125e2pm)接口时将`save_log`设为`YES`时生效。
    
    默认值：104857600（100 \* 1024 \* 1024 字节, 即 100MiB）。
    
    `log_track_level`
    
    `int`
    
    否
    
    控制通过日志回调（[onNuiLogTrackCallback](https://help.aliyun.com/zh/model-studio/ios-sdk-for-fun-asr-real-time-service#9c10968457gc6)）对外发送的日志内容的过滤级别。
    
    默认值：2。
    
    取值范围：
    
    -   0：LOG\_LEVEL\_VERBOSE
        
    -   1：LOG\_LEVEL\_DEBUG
        
    -   2：LOG\_LEVEL\_INFO
        
    -   3：LOG\_LEVEL\_WARNING
        
    -   4：LOG\_LEVEL\_ERROR
        
    -   5：LOG\_LEVEL\_NONE（表示关闭此功能）
        
    
    注意：`log_track_level`与`level`（通过[nui\_initialize](https://help.aliyun.com/zh/model-studio/ios-sdk-for-fun-asr-real-time-service#05eab5125e2pm)接口设置）共同决定最终回调的日志。一条日志的级别数值必须同时大于或等于`log_track_level`和`level`的值，才会被回调。例如，`log_track_level`设为2 (INFO)，`level`设为3 (WARNING)，则只有WARNING及以上级别（数值>=3）的日志才会被回调。
    

### 语音识别效果参数

通过在[nui\_set\_params](https://help.aliyun.com/zh/model-studio/ios-sdk-for-fun-asr-real-time-service#763672f3f8dgw)接口的`params`参数中传入一个JSON字符串来配置。

-   **参数示例：**以下为 JSON 字符串示例，参数未完整列出。请按实际需求在编码时补充：

```
{
    "service_type": 4,
    "nls_config": {
        "model": "qwen-audio-3.0-asr-flash-streaming",
        "sr_format": "pcm",
        "sample_rate": "16000",
        "parameters": {
            "speech_noise_threshold": 0.0
        }
    }
}
```

-   **参数说明**
    
    **一级参数**
    
    **类型**
    
    **是否必须**
    
    **说明**
    
    `service_type`
    
    `int`
    
    是
    
    语音服务类型。实时语音识别固定为 `4`。
    
    `nls_config`
    
    `object`
    
    是
    
    语音识别核心配置对象，包含模型选择、识别效果控制等关键参数。
    
    `nls_config.model`
    
    `string`
    
    是
    
    指定模型名。支持Qwen-Audio-3.0-ASR-Flash-Streaming和Fun-ASR-Realtime系列模型，详情请参见[支持的模型与地域](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide#4a43cc1bb7kxg)。
    
    `nls_config.sr_format`
    
    `string`
    
    是
    
    音频格式。
    
    取值范围：
    
    -   `pcm`
    -   `wav`
    -   `mp3`
    -   `opus`
    -   `speex`
    -   `aac`
    -   `amr`
    
    **重要**opus/speex：必须使用Ogg封装；
    
    wav：必须为PCM编码；
    
    amr：仅支持AMR-NB类型。
    
    `nls_config.sample_rate`
    
    `int`
    
    是
    
    采样率（Hz）。
    
    取值范围：8k模型仅支持 8000 Hz，其他模型支持任意采样率。
    
    `nls_config.semantic_punctuation_enabled`
    
    `boolean`
    
    否
    
    是否启用语义断句。
    
    默认值：false。
    
    -   true：开启语义断句，关闭 VAD 断句。
    -   false（默认）：开启 VAD 断句，关闭语义断句。
    
    语义断句准确性更高，适合会议转写场景；VAD（Voice Activity Detection，语音活动检测）断句延迟较低，适合交互场景。
    
    `nls_config.max_sentence_silence`
    
    `int`
    
    否
    
    VAD 断句静音阈值（ms）。当一段语音后的静音时长超过该阈值时，系统会判定该句子已结束。当`semantic_punctuation_enabled`为true时，不作为`sentence_end`返回依据，但设置过小可能会影响识别效果。
    
    默认值：1300。
    
    取值范围：\[200, 6000\]。
    
    `nls_config.multi_threshold_mode_enabled`
    
    `boolean`
    
    否
    
    **重要**仅在`semantic_punctuation_enabled`参数为false时生效。
    
    是否启用多阈值模式。启用后可防止 VAD 断句切割过长。
    
    默认值：false。
    
    `nls_config.heartbeat`
    
    `boolean`
    
    否
    
    是否启用心跳包。
    
    默认值：false。
    
    -   true：在持续发送静音音频的情况下，可保持与服务端的连接不中断。
    -   false（默认）：即使持续发送静音音频，连接也将在一定时间后因超时而断开。
    
    静音音频指的是在音频文件或数据流中没有声音信号的内容。静音音频可以通过多种方法生成，例如使用音频编辑软件如Audacity或Adobe Audition，或者通过命令行工具如FFmpeg。
    
    `nls_config.vocabulary_id`
    
    `string`
    
    否
    
    预编译热词列表 ID。
    
    需预先调用创建热词列表接口生成，识别时传入该 ID 即可使用列表中的热词。
    
    适用于词汇已知且相对稳定、需要跨请求复用同一词表的场景。
    
    使用方法请参见[预编译热词](https://help.aliyun.com/zh/model-studio/improve-asr-accuracy#hw_precompiled_h3)。
    
    `nls_config.parameters.vocabulary`
    
    `object`
    
    否
    
    即时热词。
    
    以键值对形式传入，键为热词文本（`string`），值为热词权重（`integer`），无需预先创建热词列表。权重取值范围为 \[1, 5\] 或 50：取 \[1, 5\] 时值越大模型越倾向输出该词；取 50 时为超级热词，召回率大幅提升，但超级热词数量最多不超过 50 个。
    
    适用于临时性、会话级别的热词优化。
    
    与预编译热词同时配置时，仅即时热词生效。使用方法请参见[即时热词](https://help.aliyun.com/zh/model-studio/improve-asr-accuracy#hw_instant_h3)。
    
    **重要**仅`qwen-audio-3.0-asr-flash-streaming`支持即时热词。
    
    `nls_config.language_hints`
    
    `array[string]`
    
    否
    
    待识别音频语种。无默认值，不设置时模型自动识别。
    
    对于 Qwen-Audio-3.0-ASR-Flash-Streaming 系列模型，最多支持设置 4 个值，即便设置超出 4 个，也仅前 4 个生效；对于 Fun-ASR-Realtime 系列模型，仅支持设置 1 个值，即便设置多个，也仅第一个生效。
    
    点击查看支持的语言代码
    
    -   qwen-audio-3.0-asr-flash-streaming、fun-asr-realtime、fun-asr-realtime-2025-11-07：
        
        -   zh: 中文
        -   en: 英文
        -   ja: 日语
        -   ko：韩语
        -   vi：越南语
        -   th：泰语
        -   id：印尼语
        -   ms：马来语
        -   tl：菲律宾语
        -   hi：印地语
        -   ar：阿拉伯语
        -   fr：法语
        -   de：德语
        -   es：西班牙语
        -   pt：葡萄牙语
        -   ru：俄语
        -   it：意大利语
        -   nl：荷兰语
        -   sv：瑞典语
        -   da：丹麦语
        -   fi：芬兰语
        -   no：挪威语
        -   el：希腊语
        -   pl：波兰语
        -   cs：捷克语
        -   hu：匈牙利语
        -   ro：罗马尼亚语
        -   bg：保加利亚语
        -   hr：克罗地亚语
        -   sk：斯洛伐克语
    -   fun-asr-realtime-2026-02-28：
        
        -   zh: 中文
        -   en: 英文
        -   ja: 日语
    -   fun-asr-realtime-2025-09-15：
        
        -   zh: 中文
        -   en: 英文
    -   fun-asr-flash-8k-realtime、fun-asr-flash-8k-realtime-2026-01-28：
        
        -   zh: 中文
    
    `nls_config.parameters`
    
    `object`
    
    否
    
    配置其他参数，内容为JSON Object格式。
    
    `nls_config.parameters.speech_noise_threshold`
    
    `float`
    
    否
    
    语音与噪音的判定阈值，用于调整语音活动检测（VAD）的灵敏度。
    
    取值范围：\[-1.0, 1.0\]。
    
    取值说明：
    
    -   取值越接近 -1：降低噪音判定阈值，噪音被识别为语音的概率增大，可能导致更多噪音被转写
    -   取值越接近 +1：提高噪音判定阈值，语音被误判为噪音的概率增大，可能导致部分语音被过滤
    
    此参数为高级配置参数，调整可能显著影响识别效果，建议：
    
    -   调整前充分测试验证效果
    -   根据实际音频环境小幅度调整（建议步长 0.1）
    
    `nls_config.parameters.special_word_filter`
    
    `object`
    
    否
    
    指定在语音识别过程中需要处理的敏感词，并支持对不同敏感词设置不同的处理方式。详情请参见[敏感词过滤](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide#rt03_sensitive_h3)。
    

## 关键接口

### NeoNui

#### nui\_initialize

初始化语音识别SDK实例。SDK为单例模式，在调用 `nui_release` 前禁止重复初始化。

-   **方法签名**

```
-(NuiResultCode) nui_initialize:(const char *)parameters
                       logLevel:(NuiSdkLogLevel)level
                        saveLog:(BOOL)save_log;
```

-   **参数说明**
    
    **参数**
    
    **类型**
    
    **说明**
    
    `parameters`
    
    `char*`
    
    JSON字符串，包含鉴权、连接和调试参数。参见[连接与控制参数](https://help.aliyun.com/zh/model-studio/ios-sdk-for-fun-asr-real-time-service#57acf5ecc1w8j)。
    
    `level`
    
    `NuiSdkLogLevel`
    
    控制SDK自身日志的打印级别。
    
    `save_log`
    
    BOOL
    
    是否保存本地日志。若为`YES`，须在[连接与控制参数](https://help.aliyun.com/zh/model-studio/ios-sdk-for-fun-asr-real-time-service#57acf5ecc1w8j)通过`debug_path`指定路径，并可通过`max_log_file_size`设置文件大小。
    
-   **返回值说明**
    
    返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。
    

#### nui\_set\_params

以JSON格式设置[语音识别效果参数](https://help.aliyun.com/zh/model-studio/ios-sdk-for-fun-asr-real-time-service#d20cce9518kla)。在 `nui_dialog_start` 之前调用。

-   **方法签名**

```
-(NuiResultCode) nui_set_params:(const char *)params;
```

-   **参数说明**
    
    **参数**
    
    **类型**
    
    **说明**
    
    `params`
    
    `char*`
    
    [语音识别效果参数](https://help.aliyun.com/zh/model-studio/ios-sdk-for-fun-asr-real-time-service#d20cce9518kla)。
    
-   **返回值说明**
    
    返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。
    

#### nui\_dialog\_start

开始识别。

-   **方法签名**

```
-(NuiResultCode) nui_dialog_start:(NuiVadMode)vad_mode
                      dialogParam:(const char *)dialog_params;
```

-   **参数说明**
    
    **参数**
    
    **类型**
    
    **说明**
    
    `vad_mode`
    
    `NuiVadMode`
    
    VAD模式。固定为`MODE_P2T`。
    
    `dialog_params`
    
    `char*`
    
    如果[连接与控制参数](https://help.aliyun.com/zh/model-studio/ios-sdk-for-fun-asr-real-time-service#57acf5ecc1w8j)的`apikey`参数使用的是[临时API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)，当其过期时，可在此处进行更新。
    
    内容为JSON格式：
    
    ```
    {
      "apikey": "st-****"
    }
    ```
    
-   **返回值说明**
    
    返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。
    

#### nui\_dialog\_cancel

结束识别或者立即取消当前交互。

-   **方法签名**

```
-(NuiResultCode) nui_dialog_cancel:(BOOL)force;
```

-   **参数说明**
    
    **参数**
    
    **类型**
    
    **说明**
    
    `force`
    
    `BOOL`
    
    是否强制结束而忽略最终结果。
    
    -   `YES`：不等待服务端返回最终识别结果就立即结束任务。
        
    -   `NO`：结束任务，但是会等待完整结果返回。
        
    
-   **返回值说明**
    
    返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。
    

#### nui\_release

释放SDK所有内部资源，并强制终止所有正在进行的任务。此方法调用后，SDK实例将变为不可用状态，如需再次使用，必须重新调用 `nui_initialize` 进行初始化。

-   **方法签名**

```
-(NuiResultCode) nui_release;
```

-   **返回值说明**
    
    返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。
    

#### nui\_get\_version

获得当前SDK版本信息。

-   **方法签名**

```
-(const char*) nui_get_version;
```

-   **返回值说明**
    
    当前SDK版本信息。
    

#### nui\_get\_all\_response

获得当前事件回调的完整信息。

-   **方法签名**

```
-(const char*) nui_get_all_response;
```

-   **返回值说明**
    
    JSON字符串格式的完整事件信息。
    

### NeoNuiSdkDelegate：监听回调

#### onNuiEventCallback：监听事件和语音识别结果

-   **方法签名**

```
-(void) onNuiEventCallback:(NuiCallbackEvent)nuiEvent
                    dialog:(long)dialog
                 kwsResult:(const char *)wuw
                 asrResult:(const char *)asr_result
                  ifFinish:(BOOL)finish
                   retCode:(int)code;
```

-   **参数说明**
    
    **参数**
    
    **类型**
    
    **说明**
    
    `nuiEvent`
    
    `NuiCallbackEvent`
    
    回调事件。
    
    `dialog`
    
    `long`
    
    会话编码，无需关注该参数。
    
    `wuw`
    
    `char*`
    
    语音唤醒功能。无需关注该参数。
    
    `asr_result`
    
    `char*`
    
    语音识别结果。
    
    `finish`
    
    `BOOL`
    
    本轮识别是否结束标志。
    
    `code`
    
    `int`
    
    错误码，在出现EVENT\_ASR\_ERROR事件时有效，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。
    

#### onNuiAudioStateChanged：监听音频状态

SDK 通过此回调通知何时应该开始或停止录音。

-   **方法签名**

```
-(void) onNuiAudioStateChanged:(NuiAudioState)state;
```

-   **NuiAudioState状态说明**
    
    **参数**
    
    **说明**
    
    `STATE_OPEN`
    
    交互启动，可以打开录音设备进行录音。
    
    `STATE_PAUSE`
    
    交互停止，可以停止录音。
    
    `STATE_CLOSE`
    
    SDK 实例已释放，可以彻底关闭录音设备。
    

#### onNuiNeedAudioData：填充待识别音频数据

开始识别后，该回调被连续触发，需在其中提供待识别音频数据。

-   **方法签名**

```
-(int) onNuiNeedAudioData:(char *)audioData length:(int)len;
```

-   **参数说明**
    
    **参数**
    
    **类型**
    
    **说明**
    
    `audioData`
    
    `char *`
    
    填充的音频数据。
    
    `len`
    
    `int`
    
    填充的音频数据的字节数。
    

#### onNuiLogTrackCallback：监听追踪日志

此回调用于接收 SDK 内部的详细日志，方便进行问题定位和调试。

```
-(void) onNuiLogTrackCallback:(NuiSdkLogLevel)level
                   logMessage:(const char *)log;
```

### NuiCallbackEvent：事件类型

**事件**

**说明**

EVENT\_TRANSCRIBER\_STARTED

任务启动成功。

EVENT\_VAD\_START

任务启动后即触发该事件。不代表检测到人声起点。

EVENT\_VAD\_END

检测到人声终点。

EVENT\_ASR\_PARTIAL\_RESULT

语音识别中间结果。

EVENT\_ASR\_ERROR

语音识别过程中出现错误。

EVENT\_MIC\_ERROR

因连续2秒未收到任何音频数据而触发。

EVENT\_SENTENCE\_END

检测到一句话结束，此时会返回一句完整的识别结果。

EVENT\_TRANSCRIBER\_COMPLETE

语音识别结束。
