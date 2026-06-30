# 语音合成Sambert iOS SDK

本文档提供了语音合成Sambert iOS SDK的详细使用指南，帮助您将文本转换为高质量、富有表现力的语音。

**用户指南：**关于模型介绍和选型建议请参见[语音合成-Sambert](https://help.aliyun.com/zh/model-studio/text-to-speech)。

**在线体验**：暂不支持。

## **快速开始**

1.  **获取API Key：**[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)
    
    **说明**
    
    当需要为第三方应用或用户提供临时访问权限，或者希望严格控制敏感数据访问、删除等高风险操作时，建议使用[临时API Key](https://help.aliyun.com/zh/model-studio/generate-temporary-api-key)。临时API Key拥有固定的60秒有效期，过期后需重新获取。
    
2.  **下载SDK并运行示例代码：**
    
    -   [下载最新SDK整合包](https://help.aliyun.com/zh/isi/sdk-selection-and-download)。
        
    -   解压 ZIP 包，将其中的 nuisdk.framework 添加到工程。
        
    -   在 Build Phases → Link Binary With Libraries 中添加 nuisdk.framework。
        
    -   在 General → Frameworks, Libraries, and Embedded Content 中将 nuisdk.framework 设置为 Embed & Sign。
        
    -   用 Xcode 打开示例工程。示例代码位于`DashSambertTTSViewController`，替换 API Key 后体验功能。
        

### **调用步骤**

1.  初始化 SDK。
    
2.  按业务需求设置参数：通过[nui\_tts\_initialize](#05eab5125e2pm)接口的`parameters`参数设置[连接与控制参数](#57acf5ecc1w8j)；通过[nui\_tts\_set\_param](#763672f3f8dgw)接口设置[语音合成效果参数](#d20cce9518kla)。
    
3.  调用 `[nui_tts_play](#8fe6ea298apzu)` 开始语音合成。
    
4.  在[onNuiTtsUserdataCallback](#bc71fe2545pfy)回调中获取音频数据，建议使用流式播放。如需保存本地，按追加模式将音频写入同一文件，直到合成完成。
    
5.  任务结束后，调用`[nui_tts_release](#6c2931e9ae3eq)`释放SDK资源。
    

## **请求参数**

### 连接与控制参数

通过在[nui\_tts\_initialize](#05eab5125e2pm)接口的`parameters`参数中传入一个JSON字符串来配置。

-   **参数示例：**以下为 JSON 字符串示例，参数未完整列出。请按实际需求在编码时补充：
    
    ```
    {
        "url": "wss://dashscope.aliyuncs.com/api-ws/v1/inference",
        "apikey": "st-****",
        "device_id": "my_device_id"
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
    
    `device_id`
    
    `String`
    
    是
    
    用于标识终端用户的唯一字符串，可设为应用内用户ID或客户端生成的设备唯一标识符。此ID主要用于日志追踪和问题排查。
    
    `debug_path`
    
    `String`
    
    否
    
    日志文件的存储路径。
    
    此参数仅在调用[nui\_tts\_initialize](#05eab5125e2pm)接口时将`save_log`设为`YES`时生效。此时必须设置日志文件路径，否则将报错。
    
    本地最多保留两个日志文件。
    
    `max_log_file_size`
    
    `int`
    
    否
    
    设定日志文件的最大字节数。
    
    此参数仅在调用[nui\_tts\_initialize](#05eab5125e2pm)接口时将`save_log`设为`YES`时生效。
    
    默认值：104857600（100 \* 1024 \* 1024 字节, 即 100MiB）。
    
    `log_track_level`
    
    `int`
    
    否
    
    控制通过日志回调（[onNuiTtsLogTrackCallback](#9c10968457gc6)）对外发送的日志内容的过滤级别。
    
    默认值：2。
    
    取值范围：
    
    -   0：LOG\_LEVEL\_VERBOSE
        
    -   1：LOG\_LEVEL\_DEBUG
        
    -   2：LOG\_LEVEL\_INFO
        
    -   3：LOG\_LEVEL\_WARNING
        
    -   4：LOG\_LEVEL\_ERROR
        
    -   5：LOG\_LEVEL\_NONE（表示关闭此功能）
        
    
    注意：`log_track_level`与`level`（通过[nui\_tts\_initialize](#05eab5125e2pm)接口设置）共同决定最终回调的日志。一条日志的级别数值必须同时大于或等于`log_track_level`和`level`的值，才会被回调。例如，`log_track_level`设为2 (INFO)，`level`设为3 (WARNING)，则只有WARNING及以上级别（数值>=3）的日志才会被回调。
    

### **语音合成效果参数**

通过[nui\_tts\_set\_param](#763672f3f8dgw)接口进行设置。

**参数**

**类型**

**是否必须**

**说明**

`model`

`String`

是

语音合成[模型](#a737f8b6f8gx0)。

`format`

`String`

否

音频编码格式。支持 pcm、wav、mp3。

默认值：pcm。

`volume`

`String`

否

音量。

默认值：50。

取值范围：\[0, 100\]。50代表标准音量。音量大小与该值呈线性关系，0为静音，100为最大音量。

`sample_rate`

`String`

否

采样率（单位Hz）。

默认值：模型对应的默认采样率。

推荐使用[模型](#a737f8b6f8gx0)的默认值。若不匹配，服务端会进行重采样。

`rate`

`String`

否

语速。

默认值：1.0。

取值范围：\[0.5, 2.0\]。1.0为标准语速，小于1.0则减慢，大于1.0则加快。

`pitch`

`String`

否

音高。该值作为音高调节的乘数，但其与听感上的音高变化并非严格的线性或对数关系，建议通过测试选择合适的值。

默认值：1.0。

取值范围：\[0.5, 2.0\]。1.0为音色自然音高。大于1.0则音高变高，小于1.0则音高变低。

`word_timestamp_enabled`

`String`

否

是否开启字级别时间戳。

默认值：0。

取值范围：

-   1：开启。
    
-   0：关闭。
    

`phoneme_timestamp_enabled`

`String`

否

是否开启音素级别时间戳。此参数仅在 `word_timestamp_enabled` 设为1（开启）时生效。

默认值：0。

取值范围：

-   1：开启。
    
-   0：关闭。
    

`enable_audio_decoder`

`String`

否

是否开启内置音频解码器。

默认值：0。

取值范围：

-   1：开启。当 format 为 mp3 时，设为 "1" 可开启SDK内置解码器，此时 onTtsDataCallback 将返回解码后的PCM数据。
    
-   0：关闭。
    

## **关键接口**

### NeoNuiTts

#### nui\_tts\_initialize

初始化语音合成SDK实例。SDK为单例模式，在调用 `[nui_tts_release](#6c2931e9ae3eq)` 前禁止重复初始化。

-   **方法签名**
    
    ```
    -(int) nui_tts_initialize:(const char *)parameters
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
    

#### nui\_tts\_set\_param

以键值对的形式设置[语音合成效果参数](#d20cce9518kla)。在 `[nui_tts_play](#8fe6ea298apzu)` 之前调用。

-   **方法签名**
    
    ```
    -(int) nui_tts_set_param:(const char *)param
                       value:(const char *)value;
    ```
    
-   **参数说明**
    
    **参数**
    
    **类型**
    
    **说明**
    
    `param`
    
    `char*`
    
    [语音合成效果参数名](#d20cce9518kla)。
    
    `value`
    
    `char*`
    
    [语音合成效果参数值](#d20cce9518kla)。
    
-   **返回值说明**
    
    返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。
    

#### nui\_tts\_get\_param

获取参数值。主要用于错误排查。

-   **方法签名**
    
    ```
    -(const char *) nui_tts_get_param:(const char *)param;
    ```
    
-   **参数说明**
    
    **参数**
    
    **类型**
    
    **说明**
    
    `param`
    
    `char*`
    
    参数。目前仅支持“error\_msg”。
    
-   **返回值说明**
    
    返回参数值。
    

#### nui\_tts\_play

启动一个语音合成任务。

-   **方法签名**
    
    ```
    -(int) nui_tts_play:(const char *)priority
                 taskId:(const char *)taskid
                  text:(const char *)text;
    ```
    
-   **参数说明**
    
    **参数**
    
    **类型**
    
    **说明**
    
    `priority`
    
    `char*`
    
    任务优先级。请将其设为1。
    
    `taskid`
    
    `char*`
    
    任务ID。传入 `null` 时由SDK自动生成。
    
    `text`
    
    `char*`
    
    待合成文本。
    
-   **返回值说明**
    
    返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。
    

#### nui\_tts\_pause

暂停当前语音合成任务。任务暂停后，可通过 `[nui_tts_resume](#448e8ffafd72e)` 恢复，或通过 `[nui_tts_cancel](#156934a01bzjc)` 彻底取消。在任务暂停期间，SDK不支持启动新的合成任务。

注意：此操作仅暂停从服务端的数据拉取，播放器中已缓存的音频数据会继续播放。

-   **方法签名**
    
    ```
    -(int) nui_tts_pause;
    ```
    
-   **返回值说明**
    
    返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。
    

#### nui\_tts\_resume

恢复处于暂停的语音合成任务。

-   **方法签名**
    
    ```
    -(int) nui_tts_resume;
    ```
    
-   **返回值说明**
    
    返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。
    

#### nui\_tts\_cancel

取消合成任务。

注意：此操作仅取消从服务端的数据拉取，播放器中已缓存的音频数据会继续播放。

-   **方法签名**
    
    ```
    -(int) nui_tts_cancel:(const char *)taskid;
    ```
    
-   **参数说明**
    
    **参数**
    
    **类型**
    
    **说明**
    
    `taskid`
    
    `char*`
    
    要取消的任务ID。若传入 `null`，则取消所有正在暂停/进行中的合成任务。
    
-   **返回值说明**
    
    返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。
    

#### nui\_tts\_release

释放SDK所有内部资源，并强制终止所有正在进行的合成任务。此方法调用后，SDK实例将变为不可用状态，如需再次使用，必须重新调用 `[nui_tts_initialize](#05eab5125e2pm)` 进行初始化。

-   **方法签名**
    
    ```
    -(int) nui_tts_release;
    ```
    
-   **返回值说明**
    
    返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。
    

### NeoNuiTtsDelegate**：监听回调**

#### onNuiTtsEventCallback**：监听事件**

-   **方法签名**
    
    ```
    - (void)onNuiTtsEventCallback:(NuiSdkTtsEvent)event taskId:(char*)taskid code:(int)code;
    ```
    
-   **参数说明**
    
    **参数**
    
    **类型**
    
    **说明**
    
    `event`
    
    `NuiSdkTtsEvent`
    
    回调事件。
    
    `taskid`
    
    `char*`
    
    语音合成任务ID。
    
    `code`
    
    `int`
    
    错误码，仅在事件 TTS\_EVENT\_ERROR 中有效。参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。
    

#### onNuiTtsUserdataCallback**：监听音频数据和时间戳信息**

-   **方法签名**
    
    ```
    - (void)onNuiTtsUserdataCallback:(char*)info infoLen:(int)info_len buffer:(char*)buffer len:(int)len taskId:(char*)task_id;
    ```
    
-   **参数说明**
    
    **参数**
    
    **类型**
    
    **说明**
    
    `info`
    
    `char*`
    
    JSON格式的时间戳结果。[语音合成效果参数](#d20cce9518kla)`word_timestamp_enabled`设为`"1"`时生效。
    
    `info_len`
    
    `int`
    
    info字段的数据长度，可忽略。
    
    `buffer`
    
    `char*`
    
    返回当前片段的音频数据。
    
    `len`
    
    `int`
    
    音频数据的长度（字节）。
    
    `task_id`
    
    `char*`
    
    语音合成任务ID。
    

#### onNuiTtsLogTrackCallback**：监听追踪日志**

此回调用于接收 SDK 内部的详细日志，方便进行问题定位和调试。

```
- (void)onNuiTtsLogTrackCallback:(NuiSdkLogLevel)level
                      logMessage:(const char *)log;
```

### NuiSdkTtsEvent**：事件类型**

**事件**

**说明**

TTS\_EVENT\_START

合成任务开始，即将有音频数据返回。

TTS\_EVENT\_END

合成任务正常结束，所有音频数据已通过回调送出。

TTS\_EVENT\_CANCEL

合成任务已取消。

TTS\_EVENT\_PAUSE

合成任务已暂停。

TTS\_EVENT\_RESUME

合成任务已恢复。

TTS\_EVENT\_ERROR

合成过程中发生错误。此时可通过`nui_tts_get_param: "error_msg"`获取详细错误信息。

```
{
  "header": {
    "task_id": "xxxxxxxxx",
    "event": "task-failed",
    "error_code": "InvalidParameter",
    "error_message": "Please ensure input text is valid.",
    "attributes": {}
  },
  "payload": {}
}
```

## **模型列表**

**说明**

默认采样率代表当前模型的最佳采样率，缺省条件下默认按照该采样率输出，同时支持降采样或升采样。如知妙音色，默认采样率16 kHz，使用时可以降采样到8 kHz，但升采样到48 kHz时不会有额外效果提升。

**音色**

**音频试听（右键保存音频）**

**model参数**

**时间戳支持**

**适用场景**

**特色**

**语言**

**默认采样率（Hz）**

知楠

sambert-zhinan-v1

是

通用场景

广告男声

中文+英文

48k

知琪

sambert-zhiqi-v1

是

通用场景

温柔女声

中文+英文

48k

知厨

sambert-zhichu-v1

是

新闻播报

舌尖男声

中文+英文

48k

知德

sambert-zhide-v1

是

新闻播报

新闻男声

中文+英文

48k

知佳

sambert-zhijia-v1

是

新闻播报

标准女声

中文+英文

48k

知茹

sambert-zhiru-v1

是

新闻播报

新闻女声

中文+英文

48k

知倩

sambert-zhiqian-v1

是

配音解说、新闻播报

资讯女声

中文+英文

48k

知祥

sambert-zhixiang-v1

是

配音解说

磁性男声

中文+英文

48k

知薇

sambert-zhiwei-v1

是

阅读产品简介

萝莉女声

中文+英文

48k

知浩

sambert-zhihao-v1

是

通用场景

咨询男声

中文+英文

16k

知婧

sambert-zhijing-v1

是

通用场景

严厉女声

中文+英文

16k

知茗

sambert-zhiming-v1

是

通用场景

诙谐男声

中文+英文

16k

知墨

sambert-zhimo-v1

是

通用场景

情感男声

中文+英文

16k

知娜

sambert-zhina-v1

是

通用场景

浙普女声

中文+英文

16k

知树

sambert-zhishu-v1

是

通用场景

资讯男声

中文+英文

16k

知莎

sambert-zhistella-v1

是

通用场景

知性女声

中文+英文

16k

知婷

sambert-zhiting-v1

是

通用场景

电台女声

中文+英文

16k

知笑

sambert-zhixiao-v1

是

通用场景

资讯女声

中文+英文

16k

知雅

sambert-zhiya-v1

是

通用场景

严厉女声

中文+英文

16k

知晔

sambert-zhiye-v1

是

通用场景

青年男声

中文+英文

16k

知颖

sambert-zhiying-v1

是

通用场景

软萌童声

中文+英文

16k

知媛

sambert-zhiyuan-v1

是

通用场景

知心姐姐

中文+英文

16k

知悦

sambert-zhiyue-v1

是

客服

温柔女声

中文+英文

16k

知柜

sambert-zhigui-v1

是

阅读产品简介

直播女声

中文+英文

16k

知硕

sambert-zhishuo-v1

是

数字人

自然男声

中文+英文

16k

知妙（多情感）

sambert-zhimiao-emo-v1

是

阅读产品简介、数字人、直播

多种情感女声

中文+英文

16k

知猫

sambert-zhimao-v1

是

阅读产品简介、配音解说、数字人、直播

直播女声

中文+英文

16k

知伦

sambert-zhilun-v1

是

配音解说

悬疑解说

中文+英文

16k

知飞

sambert-zhifei-v1

是

配音解说

激昂解说

中文+英文

16k

知达

sambert-zhida-v1

是

新闻播报

标准男声

中文+英文

16k

Camila

sambert-camila-v1

否

通用场景

西班牙语女声

西班牙语

16k

Perla

sambert-perla-v1

否

通用场景

意大利语女声

意大利语

16k

Indah

sambert-indah-v1

否

通用场景

印尼语女声

印尼语

16k

Clara

sambert-clara-v1

否

通用场景

法语女声

法语

16k

Hanna

sambert-hanna-v1

否

通用场景

德语女声

德语

16k

Beth

sambert-beth-v1

是

通用场景

咨询女声

美式英文

16k

Betty

sambert-betty-v1

是

通用场景

客服女声

美式英文

16k

Cally

sambert-cally-v1

是

通用场景

自然女声

美式英文

16k

Cindy

sambert-cindy-v1

是

通用场景

对话女声

美式英文

16k

Eva

sambert-eva-v1

是

通用场景

陪伴女声

美式英文

16k

Donna

sambert-donna-v1

是

通用场景

教育女声

美式英文

16k

Brian

sambert-brian-v1

是

通用场景

客服男声

美式英文

16k

Waan

sambert-waan-v1

否

通用场景

泰语女声

泰语

16k
