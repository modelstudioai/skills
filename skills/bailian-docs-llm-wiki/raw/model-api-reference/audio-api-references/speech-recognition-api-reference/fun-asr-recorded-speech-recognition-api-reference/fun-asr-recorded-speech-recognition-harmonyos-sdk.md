# Qwen-Audio-3.x-ASR-Flash-Filetrans/Fun-ASR非实时语音识别HarmonyOS SDK

使用Qwen-Audio-3.x-ASR-Flash-Filetrans/Fun-ASR非实时语音识别HarmonyOS SDK将音视频文件转换为文本。

**用户指南：** 参见[非实时语音识别](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide)。关于支持的音频格式、文件大小限制和时长限制等输入要求，请参见[音频规格](https://help.aliyun.com/zh/model-studio/asr-model#asr_audio_spec02)。

## 快速开始

1.  **获取 API Key：** 参见[获取 API Key](raw/model-api-reference/preparations/get-api-key.md)。建议将 API Key 配置到环境变量中。
2.  **下载 SDK 并运行示例代码：**
    -   [下载最新 SDK 整合包](https://help.aliyun.com/zh/isi/sdk-selection-and-download)。
    -   解压 TAR 包。在 `neonui` 目录中获取 HAR 格式 SDK，并添加到项目依赖。 需要 C++ 接入时，使用 TAR 包内的 `native/libs` 与 `native/include` 获取动态库和头文件。
    -   用 DevEco Studio 打开工程。示例代码位于 `DashFunAsrFileTranscriberPage.ets` 中，替换 API Key 后即可体验功能。

### 调用步骤

#### 同步模式

1.  初始化 SDK。
2.  按业务需求配置相关参数。
3.  调用 `startFileTranscriber` 启动识别任务，并将 `async_request` 设为 `false`。
4.  在 `onFileTransEventCallback` 回调中监听 `EVENT_FILE_TRANS_RESULT` 事件，获取最终识别结果。
5.  调用 `release` 释放 SDK 资源。

#### 异步模式

1.  初始化 SDK。
2.  按业务需求配置相关参数。
3.  调用 `startFileTranscriber` 启动识别任务，并将 `async_request` 设为 `true`。
4.  调用 `queryFileTranscriber` 主动查询识别进度或结果。
5.  在 `onFileTransEventCallback` 回调中监听 `EVENT_FILE_TRANS_QUERY_RESULT` 事件，获取当前查询结果。
6.  在 `onFileTransEventCallback` 回调中监听 `EVENT_FILE_TRANS_RESULT` 事件，获取最终识别结果。
7.  调用 `release` 释放 SDK 资源。

## 请求参数

### 连接与控制参数

在 [initializeFileTrans](#initializefiletrans) 接口的 `parameters` 参数中传入 JSON 字符串进行配置。 **参数示例：**以下为 JSON 字符串示例，参数未完整列出。请按实际需求在编码时补充：

```
{
    "url": "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/asr/transcription",
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

服务地址，固定为 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/asr/transcription`。调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

`apikey`

`string`

是

API Key。建议使用时效性短、安全性更高的[临时API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)，以降低长期有效Key泄露的风险。

`service_mode`

`string`

是

运行模式。非实时语音识别固定为 `"1"`。

`device_id`

`string`

是

用于标识终端用户的唯一字符串，可设为应用内用户ID或客户端生成的设备唯一标识符。此ID主要用于日志追踪和问题排查。

`debug_path`

`string`

否

日志文件的存储路径。 此参数仅在调用[initializeFileTrans](#initializefiletrans)接口时将`save_log`设为true时生效。此时必须设置日志文件路径，否则将报错。 本地最多保留两个日志文件。

`max_log_file_size`

`number`

否

设定日志文件的最大字节数。 此参数仅在调用[initializeFileTrans](#initializefiletrans)接口时将`save_log`设为true时生效。 默认值：104857600（100 \* 1024 \* 1024 字节, 即 100MiB）。

### 语音识别效果参数

通过 [setParams](#setparams) 接口配置 `nls_config` 参数，或者通过 [startFileTranscriber](#startfiletranscriber) 接口配置所有语音识别效果参数。 **参数示例：**以下为 JSON 字符串示例，参数未完整列出。请按实际需求在编码时补充：

```
{
    "file_urls": [
        "{YOUR_AUDIO_URL}"
    ],
    "async_request": false,
    "nls_config": {
        "model":"qwen-audio-3.0-asr-flash-filetrans",
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

音视频文件转写的URL列表，支持HTTP / HTTPS协议，单次请求仅支持1个URL。关于支持的音频格式、文件大小限制、时长限制等输入要求，请参见[音频规格](https://help.aliyun.com/zh/model-studio/asr-model#asr_audio_spec02)。 若录音文件存储在阿里云OSS，使用RESTful API方式支持使用以`oss://`为前缀的临时 URL，使用SDK方式不支持使用以 oss://为前缀的临时 URL。

**重要**

-   临时 URL 有效期48小时，过期后无法使用，**请勿用于生产环境。**
-   文件上传凭证接口限流为 100 QPS 且不支持扩容，**请勿用于生产环境、高并发及压测场景。**
-   生产环境建议使用[阿里云OSS](https://help.aliyun.com/zh/oss/user-guide/what-is-oss) 等稳定存储，确保文件长期可用并规避限流问题。

\- 录音文件URL设置成OSS临时公网访问不通该如何处理？请求头中将`X-DashScope-OssResourceResolve`设为`enable`（不推荐该方式）。 SDK不支持对请求头进行配置。

`async_request`

`boolean`

否

语音识别是否为异步请求。 默认值：`false`。 取值范围： - true：异步请求 - false：同步请求

`apikey`

`string`

否

如果[连接与控制参数](#%E8%BF%9E%E6%8E%A5%E4%B8%8E%E6%8E%A7%E5%88%B6%E5%8F%82%E6%95%B0)的`apikey`使用的是[临时API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)，可在此处进行更新，以免超时失效。

`nls_config`

`object`

是

语音识别核心配置对象，包含模型选择、识别效果控制等关键参数。

`nls_config.model`

`string`

是

指定示例调用的模型。模型信息请参见[支持的模型与地域](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide#4a43cc1bb7kxg)。

`nls_config.special_word_filter`

`object`

否

指定在语音识别过程中需要处理的敏感词，并支持对不同敏感词设置不同的处理方式。详情请参见[敏感词过滤](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide#nrt03_sensitive_h3)。

`nls_config.channel_id`

`array[integer]`

否

指定在多音轨音频文件中需要识别的音轨索引，索引从 0 开始。例如，`[0]` 表示识别第一个音轨，`[0, 1]` 表示同时识别第一和第二个音轨。如果省略此参数，则默认处理第一个音轨。

**重要**指定的每一个音轨都将独立计费。例如，为单个文件请求 `[0, 1]` 会产生两笔独立的费用。

默认值：`[0]`。

`nls_config.diarization_enabled`

`boolean`

否

是否启用说话人分离，默认关闭。 仅适用于单声道音频，多声道音频不支持说话人分离。 启用该功能后，识别结果中将显示`speaker_id`字段，用于区分不同说话人。

**说明**如果启用说话人分离功能，建议音频时长不超过2小时，否则可能导致识别失败或超时。

默认值：false。 有关`speaker_id`的示例，请参见[识别结果说明](https://help.aliyun.com/zh/model-studio/funauidio-asr-recorded-speech-recognition-python-sdk#a9021178ccl7s)。

`nls_config.speaker_count`

`integer`

否

**重要**仅在开启说话人分离功能（`diarization_enabled`设置为`true`）时生效。

说话人数量参考值。取值范围为2至100的整数（包含2和100）。 默认自动判断说话人数量，如果配置此项，只能辅助算法尽量输出指定人数，无法保证一定会输出此人数。 无默认值。

`nls_config.vocabulary_id`

`string`

否

预编译热词列表 ID。 需预先调用创建热词列表接口生成，识别时传入该 ID 即可使用列表中的热词。 适用于词汇已知且相对稳定、需要跨请求复用同一词表的场景。 使用方法请参见[预编译热词](https://help.aliyun.com/zh/model-studio/improve-asr-accuracy#hw_precompiled_h3)。

`nls_config.language_hints`

`array[string]`

否

设置待识别语言代码。如果无法提前确定语种，可不设置，模型会自动识别语种。 对于 Qwen-Audio-3.x-ASR-Flash-Filetrans 系列模型，最多支持设置 4 个值，即便设置超出 4 个，也仅前 4 个生效；对于 Fun-ASR 系列模型，仅支持设置 1 个值，即便设置多个，也仅第一个生效。 点击查看支持的语言代码 - Qwen-Audio-3.x-ASR-Flash-Filetrans、fun-asr、fun-asr-2025-11-07、fun-asr-mtl、fun-asr-mtl-2025-08-25： - zh: 中文 - en: 英文 - ja: 日语 - ko：韩语 - vi：越南语 - th：泰语 - id：印尼语 - ms：马来语 - tl：菲律宾语 - hi：印地语 - ar：阿拉伯语 - fr：法语 - de：德语 - es：西班牙语 - pt：葡萄牙语 - ru：俄语 - it：意大利语 - nl：荷兰语 - sv：瑞典语 - da：丹麦语 - fi：芬兰语 - no：挪威语 - el：希腊语 - pl：波兰语 - cs：捷克语 - hu：匈牙利语 - ro：罗马尼亚语 - bg：保加利亚语 - hr：克罗地亚语 - sk：斯洛伐克语 - fun-asr-2025-08-25： - zh: 中文 - en: 英文

`nls_config.parameters`

`object`

否

配置其他参数，内容为JSON Object格式。

## 关键接口

### NativeNui

#### initializeFileTrans

初始化语音转录 SDK 实例。在调用 [release](#release) 前禁止重复初始化。

**说明**与实时语音识别不同，非实时（录音文件）转录必须使用 `initializeFileTrans` 方法并传入 [INativeFileTransCallback](#inativefiletranscallback) 回调，而不是 `initialize`。

该接口会阻塞调用线程，请在非 UI 线程中调用。

-   **方法签名**

```
public initializeFileTrans(callback: INativeFileTransCallback,
                           parameters: string,
                           level: number,
                           save_log: boolean = false): number
```

-   **参数说明**

**参数**

**类型**

**说明**

`callback`

`INativeFileTransCallback`

文件转录事件和数据回调接口的实现。

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

此接口用于独立设置或更新 `nls_config` 参数。如果所有参数都在[startFileTranscriber](#startfiletranscriber)中一次性提供，则无需调用此方法。

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

[语音识别效果参数](#%E8%AF%AD%E9%9F%B3%E8%AF%86%E5%88%AB%E6%95%88%E6%9E%9C%E5%8F%82%E6%95%B0)中的`nls_config`参数，`nls_config`之外的参数不支持通过该方法进行设置。 示例： `{ "nls_config": { "model":"qwen-audio-3.0-asr-flash-filetrans", "diarization_enabled": false } }`

-   **返回值说明**

返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。

#### startFileTranscriber

开始识别。

-   **方法签名**

```
public startFileTranscriber(params: string, task_id: ArrayBuffer): number
```

-   **参数说明**

**参数**

**类型**

**说明**

`params`

`string`

[语音识别效果参数](#%E8%AF%AD%E9%9F%B3%E8%AF%86%E5%88%AB%E6%95%88%E6%9E%9C%E5%8F%82%E6%95%B0)。 示例： `{ "file_urls": [ "{YOUR_AUDIO_URL}" ], "async_request": false, "nls_config": { "model":"qwen-audio-3.0-asr-flash-filetrans", "diarization_enabled": false } }`

`task_id`

`ArrayBuffer`

任务ID缓冲区。SDK会将内部生成的随机任务ID字符串写入该缓冲区，要求缓冲区字节长度必须大于或等于33字节（示例中使用 `new ArrayBuffer(64)`）。调用成功后可通过转码获取该任务的`task_id`。

-   **返回值说明**

返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。

#### queryFileTranscriber

此接口用于主动查询一个异步任务的当前状态和结果。调用成功后，结果将通过`onFileTransEventCallback`回调中的 `EVENT_FILE_TRANS_QUERY_RESULT` 事件返回。

-   **方法签名**

```
public queryFileTranscriber(task_id: string): number
```

-   **参数说明**

**参数**

**类型**

**说明**

`task_id`

`string`

待查询的任务ID（由 `startFileTranscriber` 写入缓冲区获得）。

-   **返回值说明**

返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。

#### cancelFileTranscriber

立即取消当前任务。

-   **方法签名**

```
public cancelFileTranscriber(task_id: string): number
```

-   **参数说明**

**参数**

**类型**

**说明**

`task_id`

`string`

待取消的任务ID。

-   **返回值说明**

返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。

#### release

释放 SDK 的所有内部资源。调用后，SDK 实例将不可用；如需再次使用，必须重新调用 [initializeFileTrans](#initializefiletrans) 进行初始化。

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

### INativeFileTransCallback

定义文件转录过程中的事件与识别结果回调。

#### onFileTransEventCallback

监听文件转录事件并获取语音识别结果。

-   **方法签名**

```
onFileTransEventCallback: (event: Constants.NuiEvent, resultCode: number, finish: number,
                           asrResult: AsrResult, taskId: string) => void;
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

`finish`

`number`

任务是否结束标记。

`asrResult`

`AsrResult`

语音识别结果。

`taskId`

`string`

任务ID。

### Constants.NuiEvent

HarmonyOS SDK 中事件类型通过 `Constants.NuiEvent` 枚举定义，以下列出录音文件转录相关的事件：

**事件**

**说明**

`EVENT_FILE_TRANS_CONNECTED`

连接服务成功。

`EVENT_FILE_TRANS_UPLOADED`

上传待识别音频文件成功。

`EVENT_FILE_TRANS_QUERY_RESULT`

查询任务结果。

`EVENT_FILE_TRANS_RESULT`

识别最终结果。

`EVENT_ASR_ERROR`

语音识别过程中出现错误。

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

## 结果下载

非实时语音识别结果为异步生成，`EVENT_FILE_TRANS_RESULT` 事件返回的应答中包含 `transcription_url`，识别文本需通过该 URL 下载获取（JSON 格式）。注意该 URL 具有有效期，应及时下载。
