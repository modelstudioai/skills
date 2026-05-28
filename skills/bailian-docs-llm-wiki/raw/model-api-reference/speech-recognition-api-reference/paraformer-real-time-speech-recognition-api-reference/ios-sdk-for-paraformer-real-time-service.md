# Paraformer实时语音识别iOS SDK

本文档提供了Paraformer实时语音识别iOS SDK的详细使用指南，帮助您将语音转换为文本。

**用户指南：**关于模型介绍和选型建议请参见[实时语音识别-Fun-ASR/Gummy/Paraformer](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition)。

**在线体验**：仅paraformer-realtime-v2、paraformer-realtime-8k-v2和paraformer-realtime-v1支持[在线体验](https://bailian.console.aliyun.com/?tab=model#/efm/model_experience_center/voice)。

## **快速开始**

1.  **获取API Key：**[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)
    
    **说明**
    
    当需要为第三方应用或用户提供临时访问权限，或者希望严格控制敏感数据访问、删除等高风险操作时，建议使用[临时API Key](https://help.aliyun.com/zh/model-studio/generate-temporary-api-key)。临时API Key拥有固定的60秒有效期，过期后需重新获取。
    
2.  **下载SDK并运行示例代码：**
    
    -   [下载最新SDK整合包](https://help.aliyun.com/zh/isi/sdk-selection-and-download)。
        
    -   解压 ZIP 包，将其中的 nuisdk.framework 添加到工程。
        
    -   在 Build Phases → Link Binary With Libraries 中添加 nuisdk.framework。
        
    -   在 General → Frameworks, Libraries, and Embedded Content 中将 nuisdk.framework 设置为 Embed & Sign。
        
    -   用 Xcode 打开示例工程。示例代码位于`DashParaformerSpeechTranscriberViewController`，替换 API Key 后体验功能。
        

### **调用步骤**

1.  初始化 SDK
    
2.  按业务需求设置参数：通过[nui\_initialize](#05eab5125e2pm)接口设置[连接与控制参数](#57acf5ecc1w8j)；通过[nui\_set\_param](#763672f3f8dgw)接口设置[语音识别效果参数](#d20cce9518kla)。
    
3.  调用[nui\_dialog\_start](#8fe6ea298apzu)启动识别流程。
    
4.  在[onNuiAudioStateChanged](#bc71fe2545pfy)回调中，根据音频状态开启录音设备。
    
5.  在[onNuiNeedAudioData](#46174611d31qf)回调中持续提供录音数据。
    
6.  在[onNuiEventCallback](#163c1ef871tqt)回调中监听事件并获取语音识别结果。
    
7.  调用[nui\_dialog\_cancel](#156934a01bzjc)停止识别，并通过监听EVENT\_TRANSCRIBER\_COMPLETE事件确认识别已结束。
    
8.  当识别功能不再使用时，调用[nui\_release](#6c2931e9ae3eq)接口释放 SDK 资源。
    

## **请求参数**

### 连接与控制参数

通过在[nui\_initialize](#05eab5125e2pm)接口的`parameters`参数中传入一个JSON字符串来配置。

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
    
    服务地址，固定为 `wss://dashscope.aliyuncs.com/api-ws/v1/inference`。
    
    `apikey`
    
    `String`
    
    是
    
    API Key。建议使用时效性短、安全性更高的[临时API Key](https://help.aliyun.com/zh/model-studio/generate-temporary-api-key)，以降低长期有效Key泄露的风险。
    
    `service_mode`
    
    `String`
    
    是
    
    运行模式。实时语音识别固定为 `"1"`。
    
    `device_id`
    
    `String`
    
    是
    
    用于标识终端用户的唯一字符串，可设为应用内用户ID或客户端生成的设备唯一标识符。此ID主要用于日志追踪和问题排查。
    
    `debug_path`
    
    `String`
    
    否
    
    日志文件的存储路径。
    
    此参数仅在调用[nui\_initialize](#05eab5125e2pm)接口时将`save_log`设为`YES`时生效。此时必须设置日志文件路径，否则将报错。
    
    本地最多保留两个日志文件。
    
    `save_wav`
    
    `String`
    
    否
    
    是否保存调试用的音频文件。音频文件保存于`debug_path`下。
    
    默认值："false"。
    
    取值范围：
    
    -   "true"：是
        
    -   "false"：否
        
    
    此参数仅在调用[nui\_initialize](#05eab5125e2pm)接口时将`save_log`设为true时生效。 同时，`debug_path`也必须被设置。
    
    `max_log_file_size`
    
    `int`
    
    否
    
    设定日志文件的最大字节数。
    
    此参数仅在调用[nui\_initialize](#05eab5125e2pm)接口时将`save_log`设为`YES`时生效。
    
    默认值：104857600（100 \* 1024 \* 1024 字节, 即 100MiB）。
    
    `log_track_level`
    
    `int`
    
    否
    
    控制通过日志回调（[onNuiLogTrackCallback](#9c10968457gc6)）对外发送的日志内容的过滤级别。
    
    默认值：2。
    
    取值范围：
    
    -   0：LOG\_LEVEL\_VERBOSE
        
    -   1：LOG\_LEVEL\_DEBUG
        
    -   2：LOG\_LEVEL\_INFO
        
    -   3：LOG\_LEVEL\_WARNING
        
    -   4：LOG\_LEVEL\_ERROR
        
    -   5：LOG\_LEVEL\_NONE（表示关闭此功能）
        
    
    注意：`log_track_level`与`level`（通过[nui\_initialize](#05eab5125e2pm)接口设置）共同决定最终回调的日志。一条日志的级别数值必须同时大于或等于`log_track_level`和`level`的值，才会被回调。例如，`log_track_level`设为2 (INFO)，`level`设为3 (WARNING)，则只有WARNING及以上级别（数值>=3）的日志才会被回调。
    

### **语音识别效果参数**

通过在[nui\_set\_param](#763672f3f8dgw)接口的`params`参数中传入一个JSON字符串来配置。

-   **参数示例：**以下为 JSON 字符串示例，参数未完整列出。请按实际需求在编码时补充：
    
    ```
    {
        "service_type": 4,
        "nls_config": {
            "model": "paraformer-realtime-v2",
            "sr_format": "pcm",
            "sample_rate": "16000"
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
    
    语音识别[模型](https://help.aliyun.com/zh/model-studio/websocket-for-paraformer-real-time-service#dbdbfe151dv19)。
    
    `nls_config.sr_format`
    
    `string`
    
    是
    
    待识别音频格式。
    
    支持的音频格式：pcm、wav、opus。
    
    **重要**
    
    -   opus：必须为PCM编码，SDK内部会将其编码成OPUS格式；
        
    -   wav/pcm：必须为PCM编码。
        
    
    `nls_config.sample_rate`
    
    `int`
    
    是
    
    待识别音频采样率（单位Hz）。
    
    因模型而异：
    
    -   paraformer-realtime-v2支持任意采样率。
        
    -   paraformer-realtime-v1仅支持16000Hz采样。
        
    -   paraformer-realtime-8k-v2仅支持8000Hz采样率。
        
    -   paraformer-realtime-8k-v1仅支持8000Hz采样率。
        
    
    `nls_config.disfluency_removal_enabled`
    
    `boolean`
    
    否
    
    是否过滤语气词，如“嗯”、“啊”等。
    
    默认值：false。
    
    `nls_config.language_hints`
    
    `array[string]`
    
    否
    
    设置待识别语言代码。如果无法提前确定语种，可不设置，模型会自动识别语种。
    
    支持的语言代码：
    
    -   zh: 中文
        
    -   en: 英文
        
    -   ja: 日语
        
    -   yue: 粤语
        
    -   ko: 韩语
        
    -   de：德语
        
    -   fr：法语
        
    -   ru：俄语
        
    
    该参数仅对支持多语言的[模型](https://help.aliyun.com/zh/model-studio/websocket-for-paraformer-real-time-service#dbdbfe151dv19)生效
    
    `nls_config.semantic_punctuation_enabled`
    
    `boolean`
    
    否
    
    设置断句模式。
    
    默认值：false。
    
    取值范围：
    
    -   true：开启语义断句，关闭VAD断句。
        
    -   false：开启VAD断句，关闭语义断句。
        
    
    语义断句准确性更高，适合会议转写场景；VAD（Voice Activity Detection，语音活动检测）断句延迟较低，适合实时交互场景。
    
    该参数仅在模型为v2及更高版本时生效。
    
    `nls_config.max_sentence_silence`
    
    `int`
    
    否
    
    VAD（Voice Activity Detection，语音活动检测）断句的静音时长阈值（单位为ms）。
    
    默认值：800。
    
    取值范围：\[200, 6000\]。
    
    当一段语音后的静音时长超过该阈值时，系统会判定该句子已结束。
    
    该参数仅在`semantic_punctuation_enabled`参数为false且模型为v2及更高版本时生效。
    
    `nls_config.multi_threshold_mode_enabled`
    
    `boolean`
    
    否
    
    是否开启防过长切割模式。开启可防止VAD断句切割过长。
    
    默认值：false（关闭）。
    
    取值范围：
    
    -   true：开启
        
    -   false：关闭
        
    
    该参数仅在`semantic_punctuation_enabled`参数为false且模型为v2及更高版本时生效。
    
    `nls_config.punctuation_prediction_enabled`
    
    `boolean`
    
    否
    
    是否在识别结果中自动添加标点符号。
    
    默认值：true（是）。
    
    取值范围：
    
    -   true：是
        
    -   false：否
        
    
    该参数仅在模型为v2及更高版本时生效。
    
    `nls_config.heartbeat`
    
    `boolean`
    
    否
    
    是否和服务端保持长连接。
    
    默认值：false。
    
    取值范围：
    
    -   true：在持续发送静音音频的情况下，可保持与服务端的连接不中断。
        
    -   false：即使持续发送静音音频，连接也将在60秒后因超时而断开。该 60 秒超时为服务端默认行为，客户端不可配置。
        
    
    该参数仅在模型为v2及更高版本时生效。
    
    `nls_config.inverse_text_normalization_enabled`
    
    `boolean`
    
    否
    
    是否开启ITN（Inverse Text Normalization，逆文本正则化）。开启后，中文数字将转换为阿拉伯数字。
    
    默认值：true（开启）。
    
    取值范围：
    
    -   true：开启
        
    -   false：关闭
        
    
    该参数仅在模型为v2及更高版本时生效。
    
    `nls_config.vocabulary_id`
    
    `string`
    
    否
    
    热词词表ID，用于提升特定词汇的识别准确率。该参数适用于v2及更高版本模型。热词的使用方法请参见[定制热词](https://help.aliyun.com/zh/model-studio/custom-hot-words/)。
    
    `nls_config.resources`
    
    `array[object]`
    
    否
    
    热词资源配置，用于v1版本模型。功能与`vocabulary_id`相同，但配置方式不同：
    
    `resources` 是一个对象数组，其每个元素包含 `resource_id` 和 `resource_type` 字段：
    
    -   `resource_id`：`string`类型，热词ID。
        
    -   `resource_type`：`string`类型，取值为固定字符串“`asr_phrase`”。
        
    
    示例：
    
    ```
    {
        "nls_config": {
              "resources": [
                  {
                      "resource_id": "xxxxxxxxxxxx",
                      "resource_type": "asr_phrase"
                  }
              ]
        }
    }
    ```
    
    热词的使用方法请参见[Paraformer语音识别热词定制与管理](https://help.aliyun.com/zh/model-studio/paraformer-asr-phrase-manager)。
    

## **关键接口**

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
    
    JSON字符串，包含鉴权、连接和调试参数。参见[连接与控制参数](#57acf5ecc1w8j)。
    
    `level`
    
    `NuiSdkLogLevel`
    
    控制SDK自身日志的打印级别。
    
    `save_log`
    
    BOOL
    
    是否保存本地日志。若为`YES`，须在[连接与控制参数](#57acf5ecc1w8j)通过`debug_path`指定路径，并可通过`max_log_file_size`设置文件大小。
    
-   **返回值说明**
    
    返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。
    

#### nui\_set\_param

以JSON格式设置语音识别效果参数。在 `nui_dialog_start` 之前调用。

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
    
    [语音识别效果参数](#d20cce9518kla)。
    
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
    
    当[连接与控制参数](#57acf5ecc1w8j)的`apikey`参数对应的[临时API Key](https://help.aliyun.com/zh/model-studio/generate-temporary-api-key)过期时，可在此处进行更新。
    
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
    

### NeoNuiSdkDelegate**：监听回调**

#### onNuiEventCallback**：监听事件和语音识别结果**

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
    
    `[NuiCallbackEvent](#981ff433acpmr)`
    
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
    

#### onNuiAudioStateChanged**：监听音频状态**

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
    

#### onNuiNeedAudioData**：填充待识别音频数据**

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
    

#### onNuiLogTrackCallback**：监听追踪日志**

此回调用于接收 SDK 内部的详细日志，方便进行问题定位和调试。

```
-(void) onNuiLogTrackCallback:(NuiSdkLogLevel)level
                   logMessage:(const char *)log;
```

### NuiCallbackEvent**：事件类型**

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
