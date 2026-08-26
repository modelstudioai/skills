# Qwen-Audio-3.0-ASR-Flash-Streaming/Fun-ASR-Realtime实时语音识别Android SDK

本文档提供了Qwen-Audio-3.0-ASR-Flash-Streaming/Fun-ASR-Realtime实时语音识别Android SDK的详细使用指南，帮助您将语音转换为文本。

**用户指南：**关于模型介绍和选型建议请参见[语音识别](raw/model-user-guide/model-experience/asr-model.md)。

## 快速开始

1.  [获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)
    
2.  **下载SDK并运行示例代码：**
    -   [下载最新SDK整合包](https://help.aliyun.com/zh/isi/sdk-selection-and-download)。
    -   解压 ZIP 包。在 `app/libs` 目录中获取 AAR 格式 SDK，并添加到项目依赖。  
        需要 Android CPP 接入时，使用 ZIP 包内的 `android_libs` 与 `android_include` 获取动态库和头文件。  
          
        
    -   用 Android Studio 打开工程。示例代码位于`DashFunAsrSpeechTranscriberActivity.java`，替换 API Key 后体验功能。

### 调用步骤

1.  初始化 SDK
2.  按业务需求设置参数：通过[initialize](https://help.aliyun.com/zh/model-studio/android-sdk-for-fun-asr-real-time-service#ae6d7dd9cfad3)接口的`parameters`参数设置[连接与控制参数](https://help.aliyun.com/zh/model-studio/android-sdk-for-fun-asr-real-time-service#57acf5ecc1w8j)；通过[setParams](https://help.aliyun.com/zh/model-studio/android-sdk-for-fun-asr-real-time-service#a23e0d85d7ymt)接口设置[语音识别效果参数](https://help.aliyun.com/zh/model-studio/android-sdk-for-fun-asr-real-time-service#d20cce9518kla)。
3.  调用[startDialog](https://help.aliyun.com/zh/model-studio/android-sdk-for-fun-asr-real-time-service#7d33691bdb32v)启动识别流程。
4.  在[onNuiAudioStateChanged](https://help.aliyun.com/zh/model-studio/android-sdk-for-fun-asr-real-time-service#bc71fe2545pfy)回调中，根据音频状态开启录音设备。
5.  在[onNuiNeedAudioData](https://help.aliyun.com/zh/model-studio/android-sdk-for-fun-asr-real-time-service#12577ebc97awb)回调中持续提供录音数据，或者通过updateAudio持续推送录音数据。
6.  在[onNuiEventCallback](https://help.aliyun.com/zh/model-studio/android-sdk-for-fun-asr-real-time-service#163c1ef871tqt)回调中监听事件并获取语音识别结果。
7.  调用[stopDialog](https://help.aliyun.com/zh/model-studio/android-sdk-for-fun-asr-real-time-service#047417083bahi)停止识别，并通过监听EVENT\_TRANSCRIBER\_COMPLETE事件确认识别已结束。
8.  当识别功能不再使用时，调用[release](https://help.aliyun.com/zh/model-studio/android-sdk-for-fun-asr-real-time-service#44bf12ed9a4g9)接口释放 SDK 资源。

## 请求参数

### 连接与控制参数

通过在[initialize](https://help.aliyun.com/zh/model-studio/android-sdk-for-fun-asr-real-time-service#ae6d7dd9cfad3)接口的`parameters`参数中传入一个JSON字符串来配置。

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
    
    audio\_update\_manually
    
    `String`
    
    否
    
    是否启用主动推送音频数据模式，默认值："false"。
    
    当设置为"true"启用主动推送音频数据模式时，且SDK版本支持端侧音频能力（如AEC、VAD），则默认开启端侧音频能力。
    
    workspace
    
    `String`
    
    否
    
    当参数audio\_update\_manually设置为"true"时，且启用端侧音频能力（如AEC、VAD）时，必须设置workspace，即端侧资源文件存储的路径。
    
    `debug_path`
    
    `String`
    
    否
    
    日志文件的存储路径。
    
    此参数仅在调用[initialize](https://help.aliyun.com/zh/model-studio/android-sdk-for-fun-asr-real-time-service#ae6d7dd9cfad3)接口时将`save_log`设为true时生效。此时必须设置日志文件路径，否则将报错。
    
    本地最多保留两个日志文件。
    
    `save_wav`
    
    `String`
    
    否
    
    是否保存调试用的音频文件。音频文件保存于`debug_path`下。
    
    默认值："false"。
    
    取值范围：
    
    -   "true"：是
        
    -   "false"：否
        
    
    此参数仅在调用[initialize](https://help.aliyun.com/zh/model-studio/android-sdk-for-fun-asr-real-time-service#ae6d7dd9cfad3)接口时将`save_log`设为true时生效。 同时，`debug_path`也必须被设置。
    
    `max_log_file_size`
    
    `int`
    
    否
    
    设定日志文件的最大字节数。
    
    此参数仅在调用[initialize](https://help.aliyun.com/zh/model-studio/android-sdk-for-fun-asr-real-time-service#ae6d7dd9cfad3)接口时将`save_log`设为true时生效。
    
    默认值：104857600（100 \* 1024 \* 1024 字节, 即 100MiB）。
    
    `log_track_level`
    
    `int`
    
    否
    
    控制通过日志回调（`onNuiLogTrackCallback`）对外发送的日志内容的过滤级别。
    
    默认值：2。
    
    取值范围：
    
    -   0：LOG\_LEVEL\_VERBOSE
        
    -   1：LOG\_LEVEL\_DEBUG
        
    -   2：LOG\_LEVEL\_INFO
        
    -   3：LOG\_LEVEL\_WARNING
        
    -   4：LOG\_LEVEL\_ERROR
        
    -   5：LOG\_LEVEL\_NONE（表示关闭此功能）
        
    
    注意：`log_track_level`与`level`（通过[initialize](https://help.aliyun.com/zh/model-studio/android-sdk-for-fun-asr-real-time-service#ae6d7dd9cfad3)接口设置）共同决定最终回调的日志。一条日志的级别数值必须同时大于或等于`log_track_level`和`level`的值，才会被回调。例如，`log_track_level`设为2 (INFO)，`level`设为3 (WARNING)，则只有WARNING及以上级别（数值>=3）的日志才会被回调。
    
    enable\_reconnection
    
    `String`
    
    否
    
    是否开启断网续传功能，默认值："false"。
    
    aec\_params
    
    `object`
    
    否
    
    端侧AEC能力高级参数配置对象。当参数audio\_update\_manually设置为"true"时才启用此配置对象。
    
    aec\_params.enable\_aec
    
    `boolean`
    
    否
    
    是否开启端侧AEC回声消除能力。
    
    当参数audio\_update\_manually设置为"true"时，且SDK版本支持端侧AEC音频能力，则默认开启。
    
    aec\_params.save\_audio
    
    `boolean`
    
    否
    
    是否开启端侧AEC回声消除模块音频存储功能。
    
    当`save_wav`为"true"，且设置了`debug_path`，则默认开启，将AEC运行音频数据存储到`debug_path`下。
    
    aec\_params.enable\_aec\_data\_callback
    
    `boolean`
    
    否
    
    是否将AEC后的数据送给用户，默认false；开启后在onNuiAssistEventCallback的EVENT\_AEC\_DATA接收。
    
    vad\_params
    
    `object`
    
    否
    
    端侧VAD能力高级参数配置对象。当参数audio\_update\_manually设置为"true"时才启用此配置对象。
    
    vad\_params.enable\_aec
    
    `boolean`
    
    否
    
    是否开启端侧VAD人声检测能力。
    
    当参数audio\_update\_manually设置为"true"时，且SDK版本支持端侧VAD音频能力，则默认开启。
    
    vad\_params.save\_audio
    
    `boolean`
    
    否
    
    是否开启端侧VAD人声检测模块音频存储功能。
    
    当`save_wav`为"true"，且设置了`debug_path`，则默认开启，将VAD运行音频数据存储到`debug_path`下。
    

### 语音识别效果参数

通过在[setParams](https://help.aliyun.com/zh/model-studio/android-sdk-for-fun-asr-real-time-service#a23e0d85d7ymt)接口的`params`参数中传入一个JSON字符串来配置。

-   **参数示例：**以下为 JSON 字符串示例，参数未完整列出。请按实际需求在编码时补充：

```
{
    "service_type": 4,
    "nls_config": {
        "model": "qwen-audio-3.0-asr-flash-streaming",
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
    
    指定模型名。支持Qwen-Audio-3.0-ASR-Flash-Streaming和Fun-ASR-Realtime系列模型，详情请参见[支持的模型与地域](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide#4a43cc1bb7kxg)。
    
    `nls_config.sr_format`
    
    `string`
    
    是
    
    音频格式。
    
    取值范围：
    
    -   `pcm`
    -   `opus`
    
    **重要**opus：用户传入PCM格式音频，由SDK内部完成opus编码。
    
    `nls_config.sample_rate`
    
    `int`
    
    是
    
    采样率（Hz）。
    
    取值范围：8k模型仅支持 8000 Hz，其他模型支持任意采样率。
    
    **重要**当开启端侧音频能力（如AEC、VAD）时，不支持8000Hz。
    
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
    
    `nls_config.instant_vocabulary`
    
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
    -   fun-asr-mtl-realtime、fun-asr-mtl-realtime-2025-12-10：
        
        -   zh: 中文
        -   en: 英文
        -   ja: 日语
        -   ko：韩语
        -   vi：越南语
        -   id：印尼语
        -   th：泰语
    
    `nls_config.speech_noise_threshold`
    
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
    
    `nls_config.special_word_filter`
    
    `object`
    
    否
    
    指定在语音识别过程中需要处理的敏感词，并支持对不同敏感词设置不同的处理方式。详情请参见[敏感词过滤](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide#rt03_sensitive_h3)。
    
    `nls_config.enable_connection_fast_check`
    
    `boolean`
    
    否
    
    启动快速检测网络的功能，即尽快反馈出断网情况，默认关闭。
    

## 关键接口

### NativeNui

#### initialize

初始化语音识别SDK实例。SDK为单例模式，在调用[release](https://help.aliyun.com/zh/model-studio/android-sdk-for-fun-asr-real-time-service#44bf12ed9a4g9)前禁止重复初始化。

此接口会引起阻塞，应在非UI线程调用。

-   **方法签名**

```
public synchronized int initialize(final INativeNuiCallback callback,
                                   String parameters,
                                   final Constants.LogLevel level,
                                   final boolean save_log)
```

-   **参数说明**
    
    **参数**
    
    **类型**
    
    **说明**
    
    `callback`
    
    `INativeNuiCallback`
    
    事件和数据回调接口的实现。
    
    `parameters`
    
    `String`
    
    JSON字符串，包含鉴权、连接和调试参数。参见[连接与控制参数](https://help.aliyun.com/zh/model-studio/android-sdk-for-fun-asr-real-time-service#57acf5ecc1w8j)。
    
    `level`
    
    `Constants.LogLevel`
    
    控制SDK自身日志的打印级别。
    
    `save_log`
    
    `boolean`
    
    是否保存本地日志。若为`true`，须在[连接与控制参数](https://help.aliyun.com/zh/model-studio/android-sdk-for-fun-asr-real-time-service#57acf5ecc1w8j)中通过`debug_path`指定路径，并可通过`max_log_file_size`设置文件大小。
    
-   **返回值说明**
    
    返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。
    

#### setParams

以JSON格式设置[语音识别效果参数](https://help.aliyun.com/zh/model-studio/android-sdk-for-fun-asr-real-time-service#d20cce9518kla)。在[startDialog](https://help.aliyun.com/zh/model-studio/android-sdk-for-fun-asr-real-time-service#7d33691bdb32v)之前调用。

-   **方法签名**

```
public synchronized int setParams(String params)
```

-   **参数说明**
    
    **参数**
    
    **类型**
    
    **说明**
    
    `params`
    
    `String`
    
    [语音识别效果参数](https://help.aliyun.com/zh/model-studio/android-sdk-for-fun-asr-real-time-service#d20cce9518kla)。
    
-   **返回值说明**
    
    返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。
    

#### startDialog

开始识别。

-   **方法签名**

```
public synchronized int startDialog(VadMode vad_mode, String dialog_params)
```

-   **参数说明**
    
    **参数**
    
    **类型**
    
    **说明**
    
    `vad_mode`
    
    `VadMode`
    
    VAD模式。固定为`VadMode.TYPE_P2T`。
    
    `dialog_params`
    
    `String`
    
    如果[连接与控制参数](https://help.aliyun.com/zh/model-studio/android-sdk-for-fun-asr-real-time-service#57acf5ecc1w8j)的`apikey`参数使用的是[临时API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)，当其过期时，可在此处进行更新。
    
    如果需要通过上下文增强来提升识别准确率，则在此处进行更新。
    
    内容为JSON格式：
    
    ```
    {
      "apikey": "st-****",
      "input_context": [
        {
          "role": "user",
          "content": [
            {
              "text": "xxxxx",
              "type": "input_text"
            }
          ]
        }
      ]
    }
    ```
    
-   **返回值说明**
    
    返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。
    

#### stopDialog

结束识别，调用该接口后，服务端将返回最终识别结果并结束任务。

-   **方法签名**

```
public synchronized int stopDialog();
```

-   **返回值说明**
    
    返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。
    

#### cancelDialog

立即结束识别，调用该接口后，不等待服务端返回最终识别结果就立即结束任务。

-   **方法签名**

```
public synchronized int cancelDialog();
```

-   **返回值说明**
    
    返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。
    

#### updateAction

在交互过程中下发对话动作指令，用于更新识别上下文等运行时行为。

-   **方法签名**

```
public synchronized int updateAction(String params);
```

-   **参数说明**
    
    **参数**
    
    **类型**
    
    **说明**
    
    `params`
    
    `String`
    
    JSON形式的字符串，用于更新识别上下文等运行时行为。
    
    `params.type`
    
    `String`
    
    固定"action"。
    
    `params.command`
    
    `String`
    
    具体的运行指令，当前支持"context"、"play\_start"、"play\_over"。
    
    -   `context:`
    
    即时更新上下文增强来提升识别准确率。
    
    -   `play_start:`
    
    当使用端侧AEC时，通过此指令通知SDK内部AEC播放器开始播放音频。
    
    -   `play_over:`
    
    当使用端侧AEC时，通过此指令通知SDK内部AEC播放器已经播放结束。
    
    `params.context`
    
    `String`
    
    当`command`为`"context"`时，即时更新上下文增强来提升识别准确率。参数值是JSON格式的字符串，示例如下。
    

```
{
  "context": [
    {
      "role": "user",
      "content": [
        {
          "text": "xxx",
          "type": "input_text"
        }
      ]
    }
  ]
}
```

-   **返回值说明**
    
    返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。
    

#### updateAudio

参数audio\_update\_manually设置为"true"时，录音数据不再是通过onNuiNeedAudioData填入，而是用此接口主动推送。

-   **方法签名**

```
public synchronized int updateAudio(byte[] data, int len,
                                    boolean first_pack);
```

-   **参数说明**
    
    **参数**
    
    **类型**
    
    **说明**
    
    `data`
    
    `byte[]`
    
    推送的音频数据。
    
    `len`
    
    `int`
    
    推送的音频数据的字节数。
    
    `first_pack`
    
    `boolean`
    
    请忽略，无需关注此参数。
    
-   **返回值说明**
    
    返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。
    

#### updateRefAudio

参数audio\_update\_manually设置为"true"时，且启用了端侧AEC回声消除能力，则需要用此接口推送播放器播放的音频数据作为参考信号。

-   **方法签名**

```
public synchronized int updateRefAudio(byte[] data, int len,
                                       boolean first_pack);
```

-   **参数说明**
    
    **参数**
    
    **类型**
    
    **说明**
    
    `data`
    
    `byte[]`
    
    推送的音频数据。
    
    `len`
    
    `int`
    
    推送的音频数据的字节数。
    
    `first_pack`
    
    `boolean`
    
    请忽略，无需关注此参数。
    
-   **返回值说明**
    
    返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。
    

#### release

释放SDK所有内部资源。此方法调用后，SDK实例将变为不可用状态，如需再次使用，必须重新调用[initialize](https://help.aliyun.com/zh/model-studio/android-sdk-for-fun-asr-real-time-service#ae6d7dd9cfad3)进行初始化。

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
    

### INativeNuiCallback：监听回调

#### onNuiEventCallback：监听事件和语音识别结果

-   **方法签名**

```
void onNuiEventCallback(NuiEvent event, final int resultCode, final int arg2, KwsResult kwsResult, AsrResult asrResult);
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
    
    `arg2`
    
    `int`
    
    保留参数。
    
    `asrResult`
    
    `AsrResult`
    
    语音识别结果。
    
    `kwsResult`
    
    `KwsResult`
    
    语音唤醒功能。无需关注该参数。
    

#### onNuiAudioStateChanged：监听音频状态

SDK 通过此回调通知何时应该开始或停止录音。

-   **方法签名**

```
void onNuiAudioStateChanged(AudioState state);
```

-   **AudioState状态说明**
    
    **状态**
    
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
int onNuiNeedAudioData(byte[] buffer, int len);
```

-   **参数说明**
    
    **参数**
    
    **类型**
    
    **说明**
    
    `buffer`
    
    `byte[]`
    
    填充的音频数据。
    
    `len`
    
    `int`
    
    填充的音频数据的字节数。
    
-   **返回值说明**
    
    实际填充的字节数。
    

#### onNuiAssistEventCallback：辅助数据和信息结果

此回调用于接收 SDK 内部的辅助事件和相关数据。

-   **方法签名**

```
void onNuiAssistEventCallback_(int event, byte[] info, int info_len,
                               byte[] data);
```

-   **参数说明**
    
    **参数**
    
    **类型**
    
    **说明**
    
    `event`
    
    `int`
    
    `NuiEvent`事件
    
    `info`
    
    `String`
    
    无需关注该参数。
    
    `info_len`
    
    `int`
    
    无需关注该参数。
    
    `data`
    
    `byte[]`
    
    辅助数据，比如AEC回声消除后的音频数据。
    
-   **返回值说明**
    
    实际填充的字节数。
    

#### onNuiLogTrackCallback：监听追踪日志

此回调用于接收 SDK 内部的详细日志，方便进行问题定位和调试。

```
default void onNuiLogTrackCallback(Constants.LogLevel level, String log)
```

### `NuiEvent`：事件类型

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

EVENT\_ASR\_WARN

语音识别过程中出现不影响运行的警告，比如开启断网续传后的断网事件。

EVENT\_ASR\_ERROR

语音识别过程中出现错误。

EVENT\_MIC\_ERROR

因连续2秒未收到任何音频数据而触发。

EVENT\_SENTENCE\_END

检测到一句话结束，此时会返回一句完整的识别结果。

EVENT\_TRANSCRIBER\_COMPLETE

语音识别结束。

EVENT\_AEC\_DATA

AEC回声消除后的音频数据。
