# Paraformer录音文件识别Android SDK

本文档提供了Paraformer录音文件识别Android SDK的详细使用指南，帮助您将语音转换为文本。

**用户指南：**关于模型介绍和选型建议请参见[录音文件识别](https://help.aliyun.com/zh/model-studio/recording-file-recognition)。

## **快速开始**

1.  **获取API Key：**[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，为安全起见，推荐将API Key配置到环境变量。
    
    **说明**
    
    当需要为第三方应用或用户提供临时访问权限，或者希望严格控制敏感数据访问、删除等高风险操作时，建议使用[临时API Key](https://help.aliyun.com/zh/model-studio/generate-temporary-api-key)。临时API Key默认拥有60秒有效期，过期后需重新获取。
    
2.  **下载SDK并运行示例代码：**
    
    -   [下载最新SDK整合包](https://help.aliyun.com/zh/isi/sdk-selection-and-download)。
        
    -   解压 ZIP 包。在 `app/libs` 目录中获取 AAR 格式 SDK，并添加到项目依赖。  
        需要 Android CPP 接入时，使用 ZIP 包内的 `android_libs` 与 `android_include` 获取动态库和头文件。
        
    -   用 Android Studio 打开工程。示例代码位于`DashParaformerFileTranscriberActivity.java`，替换 API Key 后体验功能。
        

### **调用步骤**

## 同步模式

1.  初始化 SDK
    
2.  按业务需求配置相关参数
    
3.  调用 `[startFileTranscriber](#7d33691bdb32v)` 启动识别任务（`async_request`设为`false`）
    
4.  在`[onFileTransEventCallback](#163c1ef871tqt)`接口中监听`EVENT_FILE_TRANS_RESULT` 事件，获取最终识别结果
    
5.  调用 `[release](#44bf12ed9a4g9)` 释放 SDK 资源
    

## 异步模式

1.  初始化 SDK
    
2.  按业务需求配置相关参数
    
3.  调用 `[startFileTranscriber](#7d33691bdb32v)` 启动识别任务（`async_request`设为`true`）
    
4.  调用 `[queryFileTranscriber](#047417083bahi)` 主动查询识别进度/结果
    
5.  在`[onFileTransEventCallback](#163c1ef871tqt)`接口中监听`EVENT_FILE_TRANS_QUERY_RESULT`事件，获取当前查询结果
    
6.  在`[onFileTransEventCallback](#163c1ef871tqt)`接口中监听 `EVENT_FILE_TRANS_RESULT` 事件，获取最终识别结果
    
7.  调用 `[release](#44bf12ed9a4g9)` 释放 SDK 资源
    

## **请求参数**

### 连接与控制参数

通过在[initialize](#ae6d7dd9cfad3)接口的`parameters`参数中传入一个JSON字符串来配置。

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
    
    运行模式。录音文件识别固定为 `"1"`。
    
    `device_id`
    
    `String`
    
    是
    
    用于标识终端用户的唯一字符串，可设为应用内用户ID或客户端生成的设备唯一标识符。此ID主要用于日志追踪和问题排查。
    
    `debug_path`
    
    `String`
    
    否
    
    日志文件的存储路径。
    
    此参数仅在调用[initialize](#ae6d7dd9cfad3)接口时将`save_log`设为true时生效。此时必须设置日志文件路径，否则将报错。
    
    本地最多保留两个日志文件。
    
    `max_log_file_size`
    
    `int`
    
    否
    
    设定日志文件的最大字节数。
    
    此参数仅在调用[initialize](#ae6d7dd9cfad3)接口时将`save_log`设为true时生效。
    
    默认值：104857600（100 \* 1024 \* 1024 字节, 即 100MiB）。
    
    `log_track_level`
    
    `int`
    
    否
    
    控制通过日志回调（`[onFileTransLogTrackCallback](#9c10968457gc6)`）对外发送的日志内容的过滤级别。
    
    默认值：2。
    
    取值范围：
    
    -   0：LOG\_LEVEL\_VERBOSE
        
    -   1：LOG\_LEVEL\_DEBUG
        
    -   2：LOG\_LEVEL\_INFO
        
    -   3：LOG\_LEVEL\_WARNING
        
    -   4：LOG\_LEVEL\_ERROR
        
    -   5：LOG\_LEVEL\_NONE（表示关闭此功能）
        
    
    注意：`log_track_level`与`level`（通过[initialize](#ae6d7dd9cfad3)接口设置）共同决定最终回调的日志。一条日志的级别数值必须同时大于或等于`log_track_level`和`level`的值，才会被回调。例如，`log_track_level`设为2 (INFO)，`level`设为3 (WARNING)，则只有WARNING及以上级别（数值>=3）的日志才会被回调。
    

### **语音识别效果参数**

通过setParams接口配置nl\_config参数，或者通过[startFileTranscriber](#7d33691bdb32v)接口配置所有语音识别效果参数。

-   **参数示例：**以下为 JSON 字符串示例，参数未完整列出。请按实际需求在编码时补充：
    
    ```
    {
        "file_urls": [
            "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav",
            "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav"
        ],
        "async_request": false,
        "nls_config": {
            "model":"paraformer-v2",
            "disfluency_removal_enabled":false,
            "timestamp_alignment_enabled": false
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
        
    -   **音频采样率**
        
        因模型而异：
        
        -   paraformer-v2 支持任意采样率
            
        -   paraformer-v1 支持任意采样率
            
        -   paraformer-8k-v2 仅支持8kHz采样率
            
        -   paraformer-8k-v1 仅支持8kHz采样率
            
        -   paraformer-mtl-v1 支持16kHz及以上采样率
            
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
    
    语音识别[模型](https://help.aliyun.com/zh/model-studio/paraformer-recorded-speech-recognition-restful-api#47e6ae42d1u1b)。
    
    `nls_config.language_hints`
    
    `array[string]`
    
    否
    
    指定待识别语音的语言代码。该参数仅适用于paraformer-v2模型。
    
    默认值：`["zh", "en"]`。
    
    支持的语言代码：
    
    -   zh: 中文
        
    -   en: 英文
        
    -   ja: 日语
        
    -   yue: 粤语
        
    -   ko: 韩语
        
    -   de：德语
        
    -   fr：法语
        
    -   ru：俄语
        
    
    `nls_config.disfluency_removal_enabled`
    
    `boolean`
    
    否
    
    是否过滤语气词，如“嗯”、“啊”等。
    
    默认值：false。
    
    取值范围：
    
    -   true：过滤
        
    -   false：不过滤
        
    
    `nls_config.timestamp_alignment_enabled`
    
    `boolean`
    
    否
    
    是否启用时间戳校准功能。
    
    默认值：false。
    
    取值范围：
    
    -   true：开启
        
    -   false：关闭
        
    
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
    
    有关`speaker_id`的示例，请参见[识别结果说明](https://help.aliyun.com/zh/model-studio/paraformer-recorded-speech-recognition-restful-api#a9021178ccl7s)。
    
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

### **NativeNui**

#### initialize

初始化语音识别SDK实例。SDK为单例模式，在调用[release](#44bf12ed9a4g9)前禁止重复初始化。

此接口会引起阻塞，应在非UI线程调用。

-   **方法签名**
    
    ```
    public synchronized int initialize(final INativeFileTransCallback callback,
                                       String parameters,
                                       final Constants.LogLevel level,
                                       final boolean save_log)
    ```
    
-   **参数说明**
    
    **参数**
    
    **类型**
    
    **说明**
    
    `callback`
    
    `[INativeFileTransCallback](#8b030fec74e01)`
    
    事件和数据回调接口的实现。
    
    `parameters`
    
    `String`
    
    JSON字符串，包含鉴权、连接和调试参数。参见[连接与控制参数](#57acf5ecc1w8j)。
    
    `level`
    
    `Constants.LogLevel`
    
    控制SDK自身日志的打印级别。
    
    `save_log`
    
    `boolean`
    
    是否保存本地日志。若为`true`，须在[连接与控制参数](#57acf5ecc1w8j)中通过`debug_path`指定路径，并可通过`max_log_file_size`设置文件大小。
    
-   **返回值说明**
    
    返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。
    

#### **setParams**

此接口用于独立设置或更新 `nls_config` 参数。如果所有参数都在[startFileTranscriber](#7d33691bdb32v)中一次性提供，则无需调用此方法。

-   **方法签名**
    
    ```
    public synchronized int setParams(String params);
    ```
    
-   **参数说明**
    
    **参数**
    
    **类型**
    
    **说明**
    
    `params`
    
    `String`
    
    [语音识别效果参数](#d20cce9518kla)中的`nls_config`参数，`nls_config`之外的参数不支持通过该方法进行设置。
    
    示例：
    
    ```
    {
        "nls_config": {
            "model":"paraformer-v2",
            "disfluency_removal_enabled":false,
            "timestamp_alignment_enabled": false
        }
    }
    ```
    
-   **返回值说明**
    
    返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。
    

#### startFileTranscriber

开始识别。

-   **方法签名**
    
    ```
    public synchronized int startFileTranscriber(String params, byte[] task_id)
    ```
    
-   **参数说明**
    
    **参数**
    
    **类型**
    
    **说明**
    
    `params`
    
    `String`
    
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
            "model":"paraformer-v2",
            "disfluency_removal_enabled":false,
            "timestamp_alignment_enabled": false
        }
    }
    ```
    
    `task_id`
    
    `byte[]`
    
    任务ID，SDK内部生成随机字符串，在此接口调用成功后可获得task\_id。
    
-   **返回值说明**
    
    返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。
    

#### queryFileTranscriber

此接口用于主动查询一个异步任务的当前状态和结果。调用成功后，结果将通过`[onFileTransEventCallback](#163c1ef871tqt)`回调中的 `EVENT_FILE_TRANS_QUERY_RESULT` 事件返回。

-   **方法签名**
    
    ```
    public synchronized int queryFileTranscriber(String task_id)
    ```
    
-   **参数说明**
    
    **参数**
    
    **类型**
    
    **说明**
    
    `task_id`
    
    `byte[]`
    
    待查询的任务ID。
    
-   **返回值说明**
    
    返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。
    

#### cancelFileTranscriber

立即取消当前任务。

-   **方法签名**
    
    ```
    public synchronized int cancelFileTranscriber(String task_id)
    ```
    
-   **参数说明**
    
    **参数**
    
    **类型**
    
    **说明**
    
    `task_id`
    
    `byte[]`
    
    待取消的任务ID。
    
-   **返回值说明**
    
    返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。
    

#### **release**

释放SDK所有内部资源。此方法调用后，SDK实例将变为不可用状态，如需再次使用，必须重新调用[initialize](#ae6d7dd9cfad3)进行初始化。

-   **方法签名**
    
    ```
    public synchronized int release();
    ```
    
-   **返回值说明**
    
    返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。
    

#### GetVersion

获得当前SDK版本信息。

-   **方法签名**
    
    ```
    public synchronized String GetVersion();
    ```
    
-   **返回值说明**
    
    当前SDK版本信息。
    

### INativeFileTransCallback**：监听回调**

#### onFileTransEventCallback**：监听事件和语音识别结果**

-   **方法签名**
    
    ```
    void onFileTransEventCallback(NuiEvent event, final int resultCode, final int arg2, AsrResult asrResult, String taskId);
    ```
    
-   **参数说明**
    
    **参数**
    
    **类型**
    
    **说明**
    
    `event`
    
    `NuiEvent`
    
    回调事件。
    
    `resultCode`
    
    `int`
    
    [错误码](https://help.aliyun.com/zh/isi/support/error-codes)，在出现EVENT\_ASR\_ERROR事件时有效。
    
    `asrResult`
    
    `AsrResult`
    
    语音识别结果。
    
    `taskId`
    
    `String`
    
    任务ID。
    
    `arg2`
    
    `int`
    
    保留参数。
    

#### onFileTransLogTrackCallback**：监听追踪日志**

此回调用于接收 SDK 内部的详细日志，方便进行问题定位和调试。

```
default void onFileTransLogTrackCallback(Constants.LogLevel level, String log)
```

### `NuiEvent`**：事件类型**

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
