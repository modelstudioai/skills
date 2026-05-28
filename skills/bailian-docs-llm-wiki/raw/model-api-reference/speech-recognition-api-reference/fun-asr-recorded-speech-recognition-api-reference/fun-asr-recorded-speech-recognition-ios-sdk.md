# Fun-ASR录音文件识别iOS SDK

本文档提供了Fun-ASR录音文件识别iOS SDK的详细使用指南，帮助您将语音转换为文本。

**用户指南：**关于模型介绍和选型建议请参见[录音文件识别](https://help.aliyun.com/zh/model-studio/recording-file-recognition)

## **快速开始**

1.  **获取API Key：**[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)
    
2.  **下载SDK并运行示例代码：**
    
    -   [下载最新SDK整合包](https://help.aliyun.com/zh/isi/sdk-selection-and-download)。
        
    -   解压 ZIP 包，将其中的 nuisdk.framework 添加到工程。
        
    -   在 Build Phases → Link Binary With Libraries 中添加 nuisdk.framework。
        
    -   在 General → Frameworks, Libraries, and Embedded Content 中将 nuisdk.framework 设置为 Embed & Sign。
        
    -   用 Xcode 打开示例工程。示例代码位于`DashFunAsrFileTranscriberViewController.m`，替换 API Key 后体验功能。
        

### **调用步骤**

## 同步模式

1.  初始化 SDK
    
2.  按业务需求配置相关参数
    
3.  调用`[nui_file_trans_start](#8fe6ea298apzu)`启动识别任务（`async_request`设为`false`）
    
4.  在`[onFileTransEventCallback](#163c1ef871tqt)`接口中监听`EVENT_FILE_TRANS_RESULT` 事件，获取最终识别结果
    
5.  调用 `[nui_release](#6c2931e9ae3eq)` 释放 SDK 资源
    

## 异步模式

1.  初始化 SDK
    
2.  按业务需求配置相关参数
    
3.  调用 `[nui_file_trans_start](#8fe6ea298apzu)` 启动识别任务（`async_request`设为`true`）
    
4.  调用 `[nui_file_trans_query](#d894d1c6f41ke)` 主动查询识别进度/结果
    
5.  在`[onFileTransEventCallback](#163c1ef871tqt)`接口中监听`EVENT_FILE_TRANS_QUERY_RESULT`事件，获取当前查询结果
    
6.  在`[onFileTransEventCallback](#163c1ef871tqt)`接口中监听 `EVENT_FILE_TRANS_RESULT` 事件，获取最终识别结果
    
7.  调用 `[nui_release](#6c2931e9ae3eq)` 释放 SDK 资源
    

## **请求参数**

### 连接与控制参数

通过在`[nui_initialize](#05eab5125e2pm)`接口的`parameters`参数中传入一个JSON字符串来配置。

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
    
    API Key。
    
    `service_mode`
    
    `String`
    
    是
    
    运行模式。录音文件识别固定为 `"1"`。
    
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
    
    `max_log_file_size`
    
    `int`
    
    否
    
    设定日志文件的最大字节数。
    
    此参数仅在调用[nui\_initialize](#05eab5125e2pm)接口时将`save_log`设为`YES`时生效。
    
    默认值：104857600（100 \* 1024 \* 1024 字节, 即 100MiB）。
    
    `log_track_level`
    
    `int`
    
    否
    
    控制通过日志回调（[onFileTransLogTrackCallback](#9c10968457gc6)）对外发送的日志内容的过滤级别。
    
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

通过`[nui_set_params](#763672f3f8dgw)`接口配置nl\_config参数，或者通过`[nui_file_trans_start](#8fe6ea298apzu)`接口配置所有语音识别效果参数。

-   **参数示例：**以下为 JSON 字符串示例，参数未完整列出。请按实际需求在编码时补充：
    
    ```
    {
        "file_urls": [
            "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav",
            "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav"
        ],
        "async_request": false,
        "nls_config": {
            "model":"fun-asr",
            "diarization_enabled": false,
            "parameters": {
                "speech_noise_threshold": 0.0
            }
        }
    }
    ```
    
-   **参数说明**
    
    **参数**
    
    **类型**
    
    **是否必须**
    
    **说明**
    
    `file_urls`
    
    `array[string]`
    
    是
    
    音视频文件转写的URL列表，支持HTTP / HTTPS协议，单次请求最多支持100个URL。
    
    若录音文件存储在阿里云OSS，使用SDK方式不支持使用以 oss://为前缀的临时 URL。
    
    -   **音频格式**：`aac`、`amr`、`avi`、`flac`、`flv`、`m4a`、`mkv`、`mov`、`mp3`、`mp4`、`mpeg`、`ogg`、`opus`、`wav`、`webm`、`wma`、`wmv`
        
        **重要**
        
        由于音视频格式及其变种众多，技术上无法穷尽测试，API不能保证所有格式均能够被正确识别。请通过测试验证您所提供的文件能够获得正常的语音识别结果。
        
    -   **音频采样率：**任意
        
    -   **音频文件大小和时长**：音频文件不超过2GB；时长在12小时以内。
        
        如果希望处理的文件超过了上述限制，可尝试对文件进行预处理以降低文件尺寸。有关文件预处理的最佳实践可以查阅[预处理视频文件以提高文件转写效率（针对录音文件识别场景）](https://help.aliyun.com/zh/model-studio/paraformer-best-practices#c5dda0a0cf2x9)。
        
    
    `async_request`
    
    `boolean`
    
    否
    
    语音识别是否为异步请求。
    
    默认值：`false`。
    
    取值范围：
    
    -   true：异步请求
        
    -   false：同步请求
        
    
    `apikey`
    
    `string`
    
    否
    
    如果[连接与控制参数](#57acf5ecc1w8j)的`apikey`使用的是[临时API Key](https://help.aliyun.com/zh/model-studio/generate-temporary-api-key)，可在此处进行更新，以免超时失效。
    
    `nls_config`
    
    `object`
    
    是
    
    语音识别核心配置对象，包含模型选择、识别效果控制等关键参数。
    
    `nls_config.model`
    
    `string`
    
    是
    
    语音识别[模型](https://help.aliyun.com/zh/model-studio/funauidio-asr-recorded-speech-recognition-python-sdk#47e6ae42d1u1b)。
    
    `nls_config.special_word_filter`
    
    `object`
    
    否
    
    指定在语音识别过程中需要处理的敏感词，并支持对不同敏感词设置不同的处理方式。
    
    若未传入该参数，系统将启用系统内置的敏感词过滤逻辑，识别结果中与[阿里云百炼敏感词表](https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/%E7%99%BE%E7%82%BC%E6%95%8F%E6%84%9F%E8%AF%8D%E5%88%97%E8%A1%A8_20230716.words.txt)匹配的词语将被替换为等长的`*`。
    
    若传入该参数，则可实现以下敏感词处理策略：
    
    -   替换为 `*`：将匹配的敏感词替换为等长的 `*`；
        
    -   直接过滤：将匹配的敏感词从识别结果中完全移除。
        
    
    该参数的值应为一个 JSON Object，其结构如下所示：
    
    ```
    {
      "filter_with_signed": {
        "word_list": ["测试"]
      },
      "filter_with_empty": {
        "word_list": ["开始", "发生"]
      },
      "system_reserved_filter": true
    }
    ```
    
    JSON字段说明：
    
    -   `filter_with_signed`
        
        -   类型：对象。
            
        -   是否必填：否。
            
        -   描述：配置需替换为`*`的敏感词列表。识别结果中匹配的词语将被等长的 `*` 替代。
            
        -   示例：以上述JSON为例，“帮我测试一下这段代码”的语音识别结果将会是“帮我\*\*一下这段代码”。
            
        -   内部字段：
            
            -   `word_list`: 字符串数组，列出需被替换的敏感词。
                
    -   `filter_with_empty`
        
        -   类型：对象。
            
        -   是否必填：否。
            
        -   描述：配置需从识别结果中移除（过滤）的敏感词列表。识别结果中匹配的词语将被完全删除。
            
        -   示例：以上述JSON为例，“比赛这就要开始了吗？”的语音识别结果将会是“比赛这就要了吗”。
            
        -   内部字段：
            
            -   `word_list`: 字符串数组，列出需被完全移除（过滤）的敏感词。
                
    -   `system_reserved_filter`
        
        -   类型：布尔值。
            
        -   是否必填：否。
            
        -   默认值：true。
            
        -   描述：是否启用系统预置的敏感词规则。设为`true`时，将同时启用系统内置的敏感词过滤逻辑，识别结果中与[阿里云百炼敏感词表](https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/%E7%99%BE%E7%82%BC%E6%95%8F%E6%84%9F%E8%AF%8D%E5%88%97%E8%A1%A8_20230716.words.txt)匹配的词语将被替换为等长的`*`。
            
    
    `nls_config.channel_id`
    
    `array[integer]`
    
    否
    
    指定在多音轨音频文件中需要识别的音轨索引，索引从 0 开始。例如，\[0\] 表示识别第一个音轨，\[0, 1\] 表示同时识别第一和第二个音轨。如果省略此参数，则默认处理第一个音轨。
    
    **重要**
    
    指定的每一个音轨都将独立计费。例如，为单个文件请求 \[0, 1\] 会产生两笔独立的费用。
    
    默认值：`[0]`
    
    `nls_config.diarization_enabled`
    
    `boolean`
    
    否
    
    自动说话人分离，默认关闭。
    
    仅适用于单声道音频，多声道音频不支持说话人分离。
    
    启用该功能后，识别结果中将显示`speaker_id`字段，用于区分不同说话人。
    
    **说明**
    
    如果启用说话人分离功能，建议音频时长不超过2小时，否则可能导致识别失败或超时。
    
    有关`speaker_id`的示例，请参见[识别结果说明](https://help.aliyun.com/zh/model-studio/funauidio-asr-recorded-speech-recognition-python-sdk#a9021178ccl7s)。
    
    `nls_config.speaker_count`
    
    `integer`
    
    否
    
    说话人数量参考值。若要使用该功能，需将`diarization_enabled`设置为`true`。
    
    默认自动判断说话人数量，如果配置此项，只能辅助算法尽量输出指定人数，无法保证一定会输出此人数。
    
    取值范围：`[2, 100]`。该功能用于区分多个说话人，因此最少需要设置2。
    
    `nls_config.vocabulary_id`
    
    `string`
    
    否
    
    热词词表ID，用于提升特定词汇的识别准确率。该参数适用于v2及更高版本模型。热词的使用方法请参见[定制热词](https://help.aliyun.com/zh/model-studio/custom-hot-words/)。
    
    `nls_config.language_hints`
    
    `array[string]`
    
    否
    
    设置待识别语言代码。如果无法提前确定语种，可不设置，模型会自动识别语种。
    
    系统仅读取数组中的首个值。多余值将被忽略。
    
    不同模型支持的语言代码如下：
    
    -   fun-asr、fun-asr-2025-11-07、fun-asr-mtl、fun-asr-mtl-2025-08-25：
        
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
            
    -   fun-asr-2025-08-25：
        
        -   zh: 中文
            
        -   en: 英文
            
    
    `nls_config.parameters`
    
    `object`
    
    否
    
    配置其他参数，内容为JSON Object格式。
    

## **关键接口**

### NeoNui

#### nui\_initialize

初始化语音识别SDK实例。SDK为单例模式，在调用 `[nui_release](#6c2931e9ae3eq)` 前禁止重复初始化。

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
    
    `BOOL`
    
    是否保存本地日志。若为`YES`，须在[连接与控制参数](#57acf5ecc1w8j)通过`debug_path`指定路径，并可通过`max_log_file_size`设置文件大小。
    
-   **返回值说明**
    
    返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。
    

#### nui\_set\_params

此接口用于独立设置或更新 `nls_config` 参数。如果所有参数都在`[nui_file_trans_start](#8fe6ea298apzu)`中一次性提供，则无需调用此方法。

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
    
    [语音识别效果参数](#d20cce9518kla)中的`nls_config`参数，`nls_config`之外的参数不支持通过该方法进行设置。
    
    示例：
    
    ```
    {
        "nls_config": {
            "model":"fun-asr",
            "diarization_enabled": false
        }
    }
    ```
    
-   **返回值说明**
    
    返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。
    

#### nui\_file\_trans\_start

开始识别。

-   **方法签名**
    
    ```
    -(NuiResultCode) nui_file_trans_start(const char *params, char *task_id);
    ```
    
-   **参数说明**
    
    **参数**
    
    **类型**
    
    **说明**
    
    `params`
    
    `char*`
    
    [语音识别效果参数](#d20cce9518kla)。
    
    示例：
    
    ```
    {
        "file_urls": [
            "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav",
            "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav"
        ],
        "async_request": false,
        "nls_config": {
            "model":"fun-asr",
            "diarization_enabled": false
        }
    }
    ```
    
    `task_id`
    
    `char*`
    
    任务ID，SDK内部生成随机字符串，在此接口调用成功后可获得task\_id。
    
-   **返回值说明**
    
    返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。
    

#### nui\_file\_trans\_query

此接口用于主动查询一个异步任务的当前状态和结果。调用成功后，结果将通过`[onFileTransEventCallback](#163c1ef871tqt)`回调中的 `EVENT_FILE_TRANS_QUERY_RESULT` 事件返回。

-   **方法签名**
    
    ```
    -(NuiResultCode) nui_file_trans_query(const char *task_id);
    ```
    
-   **参数说明**
    
    **参数**
    
    **类型**
    
    **说明**
    
    `task_id`
    
    `char*`
    
    待查询的任务ID。
    
-   **返回值说明**
    
    返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。
    

#### nui\_file\_trans\_cancel

立即取消当前任务。

-   **方法签名**
    
    ```
    -(NuiResultCode) nui_file_trans_cancel(const char *task_id);
    ```
    
-   **参数说明**
    
    **参数**
    
    **类型**
    
    **说明**
    
    `task_id`
    
    `char*`
    
    待取消的任务ID。
    
-   **返回值说明**
    
    返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。
    

#### nui\_release

释放SDK所有内部资源，并强制终止所有正在进行的任务。此方法调用后，SDK实例将变为不可用状态，如需再次使用，必须重新调用 `[nui_initialize](#05eab5125e2pm)` 进行初始化。

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
    

### NeoNuiSdkDelegate**：监听回调**

#### onFileTransEventCallback**：监听事件和语音识别结果**

-   **方法签名**
    
    ```
    -(void) onFileTransEventCallback:(NuiCallbackEvent)nuiEvent
                           asrResult:(const char *)asr_result
                              taskId:(const char *)task_id
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
    
    `asr_result`
    
    `char*`
    
    语音识别结果。
    
    `task_id`
    
    `char*`
    
    任务ID。
    
    `finish`
    
    `BOOL`
    
    本轮识别是否结束标志。
    
    `code`
    
    `int`
    
    错误码，在出现EVENT\_ASR\_ERROR事件时有效，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。
    

#### onFileTransLogTrackCallback**：监听追踪日志**

此回调用于接收 SDK 内部的详细日志，方便进行问题定位和调试。

```
-(void)onFileTransLogTrackCallback:(NuiSdkLogLevel)level
                        logMessage:(const char *)log;
```

### NuiCallbackEvent**：事件类型**

**事件**

**说明**

EVENT\_FILE\_TRANS\_CONNECTED

连接服务成功。

EVENT\_FILE\_TRANS\_UPLOADED

上传待识别音频文件成功。

EVENT\_FILE\_TRANS\_QUERY\_RESULT

查询任务结果。

EVENT\_FILE\_TRANS\_RESULT

识别最终结果。

EVENT\_ASR\_ERROR

语音识别过程中出现错误。
