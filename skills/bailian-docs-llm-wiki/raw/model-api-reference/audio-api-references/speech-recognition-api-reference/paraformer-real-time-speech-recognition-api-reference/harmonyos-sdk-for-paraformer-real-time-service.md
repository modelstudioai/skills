# Paraformer实时语音识别HarmonyOS SDK

使用Paraformer实时语音识别HarmonyOS SDK将语音转换为文本。

**重要**阿里云百炼为华北2（北京）地域提供业务空间专属域名，可提升推理请求的性能和稳定性。建议从 `dashscope.aliyuncs.com` 迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`。

请将 `{WorkspaceId}` 替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。现有域名仍可正常使用。

**用户指南**：关于模型介绍和选型建议请参见[实时语音识别-Fun-ASR/Paraformer](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition)。

**在线体验**：仅 `paraformer-realtime-v2`、`paraformer-realtime-8k-v2` 和 `paraformer-realtime-v1` 支持[在线体验](https://bailian.console.aliyun.com/model/experience/voice)。

## 快速开始

1.  **获取 API Key：** 参见[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。建议将 API Key 配置到环境变量中。
    
    **说明**当需要为第三方应用或用户提供临时访问权限，或者希望严格控制敏感数据访问、删除等高风险操作时，建议使用[临时 API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。临时 API Key 默认有效期为60秒，过期后需重新获取。
    
2.  **下载 SDK 并运行示例代码：**
    
    -   [下载最新 SDK 整合包](https://help.aliyun.com/zh/isi/sdk-selection-and-download)。
    -   解压 TAR 包。在 `neonui` 目录中获取 HAR 格式 SDK，并添加到项目依赖。 需要 C++ 接入时，使用 TAR 包内的 `native/libs` 与 `native/include` 获取动态库和头文件。
    -   用 DevEco Studio 打开工程。示例代码位于 `DashParaformerSpeechTranscriberPage.ets` 中，替换 API Key 后即可体验功能。

### 调用步骤

1.  初始化 SDK。
2.  按业务需求设置参数：通过 [initialize](#initialize) 接口的 `parameters` 参数设置[连接与控制参数](#%E8%BF%9E%E6%8E%A5%E4%B8%8E%E6%8E%A7%E5%88%B6%E5%8F%82%E6%95%B0)；通过 [setParams](#setparams) 接口设置[语音识别效果参数](#%E8%AF%AD%E9%9F%B3%E8%AF%86%E5%88%AB%E6%95%88%E6%9E%9C%E5%8F%82%E6%95%B0)。
3.  调用 [startDialog](#startdialog) 启动识别流程。
4.  在 [onNuiAudioStateChanged](#onnuiaudiostatechanged) 回调中，根据音频状态开启录音设备。
5.  在 [onNuiNeedAudioData](#onnuineedaudiodata) 回调中持续提供录音数据。
6.  在 [onNuiEventCallback](#onnuieventcallback) 回调中监听事件并获取语音识别结果。
7.  调用 [stopDialog](#stopdialog) 停止识别，并通过监听 `EVENT_TRANSCRIBER_COMPLETE` 事件确认识别已结束。
8.  不再使用识别功能时，调用 [release](#release) 接口释放 SDK 资源。

## 请求参数

### 连接与控制参数

在 [initialize](#initialize) 接口的 `parameters` 参数中传入 JSON 字符串进行配置。 **参数示例：**以下为 JSON 字符串示例，参数未完整列出。请按实际需求在编码时补充：

```
{
    "url": "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference",
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

`string`

是

服务地址，固定为 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference`。调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

`apikey`

`string`

是

API Key。建议使用时效性短、安全性更高的[临时API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)，以降低长期有效Key泄露的风险。

`service_mode`

`string`

是

运行模式。实时语音识别固定为 `"1"`。

`device_id`

`string`

是

用于标识终端用户的唯一字符串，可设为应用内用户ID或客户端生成的设备唯一标识符。此ID主要用于日志追踪和问题排查。

`debug_path`

`string`

否

日志文件的存储路径。 此参数仅在调用[initialize](#initialize)接口时将`save_log`设为true时生效。此时必须设置日志文件路径，否则将报错。 本地最多保留两个日志文件。

`save_wav`

`string`

否

是否保存调试用的音频文件。音频文件保存于`debug_path`下。 默认值："false"。 取值范围： - "true"：是 - "false"：否 此参数仅在调用[initialize](#initialize)接口时将`save_log`设为true时生效。 同时，`debug_path`也必须被设置。

`max_log_file_size`

`number`

否

设定日志文件的最大字节数。 此参数仅在调用[initialize](#initialize)接口时将`save_log`设为true时生效。 默认值：104857600（100 \* 1024 \* 1024 字节，即 100MiB）。

`log_track_level`

`number`

否

控制通过日志回调（`onNuiLogTrackCallback`）对外发送的日志内容的过滤级别。 默认值：2。 取值范围： - 0：LOG\_LEVEL\_VERBOSE - 1：LOG\_LEVEL\_DEBUG - 2：LOG\_LEVEL\_INFO - 3：LOG\_LEVEL\_WARNING - 4：LOG\_LEVEL\_ERROR - 5：LOG\_LEVEL\_NONE（表示关闭此功能） 注意：`log_track_level`与`level`（通过[initialize](#initialize)接口设置）共同决定最终回调的日志。一条日志的级别数值必须同时大于或等于`log_track_level`和`level`的值，才会被回调。例如，`log_track_level`设为2 (INFO)，`level`设为3 (WARNING)，则只有WARNING及以上级别（数值>=3）的日志才会被回调。

### 语音识别效果参数

在 [setParams](#setparams) 接口的 `params` 参数中传入 JSON 字符串进行配置。 **参数示例：**以下为 JSON 字符串示例，参数未完整列出。请按实际需求在编码时补充：

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

语音服务类型。实时语音识别固定为 `4`。

`nls_config`

`object`

是

语音识别核心配置对象，包含模型选择、识别效果控制等关键参数。

`nls_config.model`

`string`

是

语音识别[模型](raw/model-api-reference/audio-api-references/speech-recognition-api-reference/paraformer-real-time-speech-recognition-api-reference/websocket-for-paraformer-real-time-service.md)。

`nls_config.sr_format`

`string`

是

待识别音频格式。 支持的音频格式：pcm、wav、opus。

**重要**

-   opus：必须为PCM编码，SDK内部会将其编码成OPUS格式；
-   wav/pcm：必须为PCM编码。

`nls_config.sample_rate`

`int`

是

待识别音频采样率（单位Hz）。 因模型而异： - paraformer-realtime-v2支持任意采样率。 - paraformer-realtime-v1仅支持16000Hz采样。 - paraformer-realtime-8k-v2仅支持8000Hz采样率。 - paraformer-realtime-8k-v1仅支持8000Hz采样率。

`nls_config.disfluency_removal_enabled`

`boolean`

否

是否过滤语气词，如“嗯”、“啊”等。 默认值：false。

`nls_config.language_hints`

`array[string]`

否

设置待识别语言代码。如果无法提前确定语种，可不设置，模型会自动识别语种。 支持的语言代码： - zh: 中文 - en: 英文 - ja: 日语 - yue: 粤语 - ko: 韩语 - de：德语 - fr：法语 - ru：俄语 该参数仅对支持多语言的[模型](raw/model-api-reference/audio-api-references/speech-recognition-api-reference/paraformer-real-time-speech-recognition-api-reference/websocket-for-paraformer-real-time-service.md)生效

`nls_config.semantic_punctuation_enabled`

`boolean`

否

设置断句模式。 默认值：false。 取值范围： - true：开启语义断句，关闭VAD断句。 - false：开启VAD断句，关闭语义断句。 语义断句准确性更高，适合会议转写场景；VAD（Voice Activity Detection，语音活动检测）断句延迟较低，适合实时交互场景。 该参数仅在模型为v2及更高版本时生效。

`nls_config.max_sentence_silence`

`int`

否

VAD（Voice Activity Detection，语音活动检测）断句的静音时长阈值（单位为ms）。 默认值：800。 取值范围：`[200, 6000]`。 当一段语音后的静音时长超过该阈值时，系统会判定该句子已结束。 该参数仅在`semantic_punctuation_enabled`参数为false且模型为v2及更高版本时生效。

`nls_config.multi_threshold_mode_enabled`

`boolean`

否

是否开启防过长切割模式。开启可防止VAD断句切割过长。 默认值：false（关闭）。 取值范围： - true：开启 - false：关闭 该参数仅在`semantic_punctuation_enabled`参数为false且模型为v2及更高版本时生效。

`nls_config.punctuation_prediction_enabled`

`boolean`

否

是否在识别结果中自动添加标点符号。 默认值：true（是）。 取值范围： - true：是 - false：否 该参数仅在模型为v2及更高版本时生效。

`nls_config.heartbeat`

`boolean`

否

是否和服务端保持长连接。 默认值：false。 取值范围： - true：在持续发送静音音频的情况下，可保持与服务端的连接不中断。 - false：即使持续发送静音音频，连接也将在一定时间后因超时而断开。该超时为服务端默认行为，客户端不可配置。 该参数仅在模型为v2及更高版本时生效。

`nls_config.inverse_text_normalization_enabled`

`boolean`

否

是否开启ITN（Inverse Text Normalization，逆文本正则化）。开启后，中文数字将转换为阿拉伯数字。 默认值：true（开启）。 取值范围： - true：开启 - false：关闭 该参数仅在模型为v2及更高版本时生效。

`nls_config.vocabulary_id`

`string`

否

热词词表ID，用于提升特定词汇的识别准确率。该参数适用于v2及更高版本模型。热词的使用方法请参见[定制热词](raw/model-api-reference/audio-api-references/speech-recognition-api-reference/custom-hot-words.md)。

`nls_config.resources`

`array[object]`

否

热词资源配置，用于v1版本模型。功能与`vocabulary_id`相同，但配置方式不同： `resources` 是一个对象数组，其每个元素包含 `resource_id` 和 `resource_type` 字段： - `resource_id`：`string`类型，热词ID。 - `resource_type`：`string`类型，取值为固定字符串“`asr_phrase`”。 示例： `{ "nls_config": { "resources": [ { "resource_id": "xxxxxxxxxxxx", "resource_type": "asr_phrase" } ] } }` 热词的使用方法请参见[Paraformer语音识别热词定制与管理](https://help.aliyun.com/zh/model-studio/paraformer-asr-phrase-manager)。

## 关键接口

### NativeNui

#### initialize

初始化语音识别 SDK 实例。在调用 [release](#release) 前禁止重复初始化。

该接口会阻塞调用线程，请在非 UI 线程中调用。

-   **方法签名**

```
public initialize(callback: INativeNuiCallback,
                  parameters: string,
                  level: number,
                  save_log: boolean = false): number
```

-   **参数说明**

**参数**

**类型**

**说明**

`callback`

`INativeNuiCallback`

事件和数据回调接口的实现。

`parameters`

`string`

JSON字符串，包含鉴权、连接和调试参数。参见[连接与控制参数](#%E8%BF%9E%E6%8E%A5%E4%B8%8E%E6%8E%A7%E5%88%B6%E5%8F%82%E6%95%B0)。

`level`

`number`

控制SDK自身日志的打印级别，取值为[Constants.LogLevel](#constants-loglevel)枚举。

`save_log`

`boolean`

是否保存本地日志。若为`true`，须在[连接与控制参数](#%E8%BF%9E%E6%8E%A5%E4%B8%8E%E6%8E%A7%E5%88%B6%E5%8F%82%E6%95%B0)中通过`debug_path`指定路径，并可通过`max_log_file_size`设置文件大小。

-   **返回值说明**

返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。

#### setParams

以 JSON 格式设置语音识别效果参数。请在 [startDialog](#startdialog) 之前调用。

-   **方法签名**

```
public setParams(params: string): number
```

-   **参数说明**

**参数**

**类型**

**说明**

`params`

`string`

[语音识别效果参数](#%E8%AF%AD%E9%9F%B3%E8%AF%86%E5%88%AB%E6%95%88%E6%9E%9C%E5%8F%82%E6%95%B0)。

-   **返回值说明**

返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。

#### startDialog

开始识别。

-   **方法签名**

```
public startDialog(vad_mode: Constants.VadMode, dialog_params: string): number
```

-   **参数说明**

**参数**

**类型**

**说明**

`vad_mode`

`Constants.VadMode`

VAD模式。固定为`Constants.VadMode.TYPE_P2T`。

`dialog_params`

`string`

当[连接与控制参数](#%E8%BF%9E%E6%8E%A5%E4%B8%8E%E6%8E%A7%E5%88%B6%E5%8F%82%E6%95%B0)的`apikey`参数对应的[临时API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)过期时，可在此处进行更新。 内容为JSON格式： `typescript { "apikey": "st-****" }`

-   **返回值说明**

返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。

#### stopDialog

结束识别，调用该接口后，服务端将返回最终识别结果并结束任务。

-   **方法签名**

```
public stopDialog(): number
```

-   **返回值说明**

返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。

#### cancelDialog

立即结束识别，调用该接口后，不等待服务端返回最终识别结果就立即结束任务。

-   **方法签名**

```
public cancelDialog(): number
```

-   **返回值说明**

返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。

#### release

释放 SDK 的所有内部资源。调用后，SDK 实例将不可用；如需再次使用，必须重新调用 [initialize](#initialize) 进行初始化。

-   **方法签名**

```
public release(): number
```

-   **返回值说明**

返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。

#### GetVersion

获取当前 SDK 版本信息。

-   **方法签名**

```
public GetVersion(): string
```

-   **返回值说明**

当前 SDK 版本信息。

### INativeNuiCallback

用于监听实时语音识别过程中的事件、音频状态、音量和日志等回调。

#### onNuiEventCallback

监听识别事件并获取语音识别结果。

-   **方法签名**

```
onNuiEventCallback: (event: Constants.NuiEvent, resultCode: number, arg2: number,
                    kwsResult: KwsResult, asrResult: AsrResult) => void;
```

-   **参数说明**

**参数**

**类型**

**说明**

`event`

`Constants.NuiEvent`

回调事件。

`resultCode`

`number`

[错误码](https://help.aliyun.com/zh/isi/support/error-codes)，在出现`EVENT_ASR_ERROR`事件时有效。

`asrResult`

`AsrResult`

语音识别结果。

`kwsResult`

`KwsResult`

语音唤醒功能。无需关注该参数。

`arg2`

`number`

保留参数。

#### onNuiAudioStateChanged

监听音频状态变化，以确定何时开始、暂停或停止录音。

-   **方法签名**

```
onNuiAudioStateChanged: (state: Constants.AudioState) => void
```

-   **AudioState状态说明**

**状态**

**说明**

`STATE_OPEN`

交互启动，可以打开录音设备进行录音。

`STATE_PAUSE`

交互暂停，可以暂停录音。

`STATE_CLOSE`

交互停止，可以彻底关闭录音设备。

#### onNuiAudioRMSChanged

监听录音音量变化，可用于 UI 展示。

-   **方法签名**

```
onNuiAudioRMSChanged: (val: number) => number
```

-   **参数说明**

**参数**

**类型**

**说明**

`val`

`number`

录音数据的音量值。输出范围一般为 `[-160, 0]`。

#### onNuiNeedAudioData

识别开始后，该回调会被连续触发，用于持续提供待识别的音频数据。

-   **方法签名**

```
onNuiNeedAudioData: (buffer: ArrayBuffer) => number
```

-   **参数说明**

**参数**

**类型**

**说明**

`buffer`

`ArrayBuffer`

填充的音频数据。SDK会按`buffer.byteLength`获取期望读取的字节数。

-   **返回值说明**

实际填充的字节数。返回`<=0`表示出错或无数据。

#### onNuiLogTrackCallback

监听 SDK 的追踪日志，用于问题定位和调试。

```
onNuiLogTrackCallback: (level: Constants.LogLevel, log: string) => void
```

### Constants.NuiEvent

HarmonyOS SDK 中事件类型通过 `Constants.NuiEvent` 枚举定义，以下列出实时语音识别相关的事件：

**事件**

**说明**

`EVENT_TRANSCRIBER_STARTED`

任务启动成功。

`EVENT_VAD_START`

任务启动后即触发该事件。不代表检测到人声起点。

`EVENT_VAD_END`

检测到人声终点。

`EVENT_ASR_PARTIAL_RESULT`

语音识别中间结果。

`EVENT_ASR_RESULT`

完整的语音识别结果。

`EVENT_ASR_ERROR`

语音识别过程中出现错误。

`EVENT_MIC_ERROR`

因连续2秒未收到任何音频数据而触发。

`EVENT_SENTENCE_START`

检测到一句话开始。

`EVENT_SENTENCE_END`

检测到一句话结束，此时会返回一句完整的识别结果。

`EVENT_TRANSCRIBER_COMPLETE`

语音识别结束。

## 辅助类型

### Constants.LogLevel

`level` 参数的取值枚举：

**值**

**说明**

`LOG_LEVEL_VERBOSE`

最详细日志。

`LOG_LEVEL_DEBUG`

调试日志。

`LOG_LEVEL_INFO`

普通信息日志（默认）。

`LOG_LEVEL_WARNING`

警告日志。

`LOG_LEVEL_ERROR`

错误日志。

`LOG_LEVEL_NONE`

关闭日志。

## 音频设备管理

与 Android 使用 `AudioRecord` 不同，HarmonyOS 通过 `@kit.AudioKit` 的 `AudioCapturer` 进行音频采集。本产品样例已封装为 `AudioRecorder.ets` 工具类，可直接复用。

-   **创建**：`audio.createAudioCapturer(capturerOptions)` 异步创建，采样率固定 16kHz、16bit、单声道（`SAMPLE_RATE_16000`/`CHANNEL_1`/`SAMPLE_FORMAT_S16LE`/`ENCODING_TYPE_RAW`）。
-   **数据事件**：`capturer.on('readData', (buffer: ArrayBuffer) => void)` 持续获得录音数据，数据须先缓入队列，由 `onNuiNeedAudioData` 回调按需拉取。
-   **状态事件**：`capturer.on('stateChange', (state: audio.AudioState) => void)`，`STATE_RUNNING` 表示开始录音，`STATE_STOPPED` 表示停止。
-   **控制**：`start()` 开始、`stop()` 停止、`release()` 释放。

**说明**HarmonyOS 的 `AudioCapturer` 为异步创建，创建完成后才能调用 `start()`。因此不要在 `STATE_OPEN` 时新建并立即启动录音器——应先创建完毕，再在 `STATE_OPEN` 回调中 `start()`（样例在 `doInit` 阶段创建，`onNuiAudioStateChanged` 阶段启动）。`STATE_CLOSE` 时只停止并保留实例复用，统一由 `release` 释放。

### 权限声明

使用录音功能需在 `module.json5` 中声明麦克风权限：

```
{
  "requestPermissions": [
    { "name": "ohos.permission.MICROPHONE" }
  ]
}
```
