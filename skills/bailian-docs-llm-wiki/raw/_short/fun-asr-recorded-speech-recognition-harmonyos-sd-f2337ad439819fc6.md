# Fun-ASR非实时语音识别HarmonyOS SDK

使用Fun-ASR非实时语音识别HarmonyOS SDK将音视频文件转换为文本。

<a id="快速开始"></a>

## 快速开始

1.  **获取 API Key：** 参见[获取 API Key](../model-api-reference/preparations/get-api-key.md)。建议将 API Key 配置到环境变量中。
2.  **下载 SDK 并运行示例代码：**
    -   [下载最新 SDK 整合包](../model-api-reference/more-about-models/sdk-selection-and-download.md)。
    -   解压 TAR 包。在 `neonui` 目录中获取 HAR 格式 SDK，并添加到项目依赖。 需要 C++ 接入时，使用 TAR 包内的 `native/libs` 与 `native/include` 获取动态库和头文件。
    -   用 DevEco Studio 打开工程。示例代码位于 `DashFunAsrFileTranscriberPage.ets` 中，替换 API Key 后即可体验功能。

<a id="调用步骤"></a>

### 调用步骤

<a id="同步模式"></a>

#### 同步模式

1.  初始化 SDK。
2.  按业务需求配置相关参数。
3.  调用 `startFileTranscriber` 启动识别任务，并将 `async_request` 设为 `false`。
4.  在 `onFileTransEventCallback` 回调中监听 `EVENT_FILE_TRANS_RESULT` 事件，获取最终识别结果。
5.  调用 `release` 释放 SDK 资源。

<a id="异步模式"></a>

#### 异步模式

1.  初始化 SDK。
2.  按业务需求配置相关参数。
3.  调用 `startFileTranscriber` 启动识别任务，并将 `async_request` 设为 `true`。
4.  调用 `queryFileTranscriber` 主动查询识别进度或结果。
5.  在 `onFileTransEventCallback` 回调中监听 `EVENT_FILE_TRANS_QUERY_RESULT` 事件，获取当前查询结果。
6.  在 `onFileTransEventCallback` 回调中监听 `EVENT_FILE_TRANS_RESULT` 事件，获取最终识别结果。
7.  调用 `release` 释放 SDK 资源。

<a id="请求参数"></a>

## 请求参数

<a id="连接与控制参数"></a>

### 连接与控制参数

在 `initializeFileTrans` 接口的 `parameters` 参数中传入 JSON 字符串进行配置。

**参数示例**

以下为 JSON 字符串示例，参数未完整列出。请按实际需求在编码时补充：

<a id="code-block"></a>

```json
{
    "url": "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/asr/transcription",
    "apikey": "st-****",
    "device_id": "my_device_id",
    "service_mode": "1"
}
```

**参数说明**

| 参数 | 类型 | 是否必须 | 说明 |
| --- | --- | --- | --- |
| `url` | `string` | 是 | 服务地址，固定为 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/asr/transcription`。调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。 |
| `apikey` | `string` | 是 | API Key。建议使用时效性短、安全性更高的[临时API Key](../model-api-reference/more-about-models/generate-temporary-api-key.md)，以降低长期有效Key泄露的风险。 |
| `service_mode` | `string` | 是 | 运行模式。非实时语音识别固定为 `"1"`。 |
| `device_id` | `string` | 是 | 用于标识终端用户的唯一字符串，可设为应用内用户ID或客户端生成的设备唯一标识符。此ID主要用于日志追踪和问题排查。 |
| `debug_path` | `string` | 否 | 日志文件的存储路径。 此参数仅在调用`initializeFileTrans`接口时将`save_log`设为true时生效。此时必须设置日志文件路径，否则将报错。 本地最多保留两个日志文件。 |
| `max_log_file_size` | `number` | 否 | 设定日志文件的最大字节数。 此参数仅在调用`initializeFileTrans`接口时将`save_log`设为true时生效。 默认值：104857600（100 \* 1024 \* 1024 字节, 即 100MiB）。 |

<a id="语音识别效果参数"></a>

### 语音识别效果参数

通过 `setParams` 接口配置 `nls_config` 参数，或者通过 `startFileTranscriber` 接口配置所有语音识别效果参数。

**参数示例**

以下为 JSON 字符串示例，参数未完整列出。请按实际需求在编码时补充：

<a id="code-block-2"></a>

```json
{
    "file_urls": [
        "{YOUR_AUDIO_URL}"
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

**参数说明**

<table><thead><tr><th><strong>参数</strong></th><th><strong>类型</strong></th><th><strong>是否必须</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><p><code>file_urls</code></p></td><td><p><code>array[string]</code></p></td><td><p>是</p></td><td><p>音视频文件转写的URL列表，支持HTTP / HTTPS协议，单次请求仅支持1个URL。关于支持的音频格式、文件大小限制、时长限制等输入要求，请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/asr-model.md#asr_audio_spec02">音频规格</a>。 若录音文件存储在阿里云OSS，使用RESTful API方式支持使用以<code>oss://</code>为前缀的临时 URL，使用SDK方式不支持使用以 oss://为前缀的临时 URL。</p><div><div><p><strong>重要</strong></p><ul><li><p>临时 URL 有效期48小时，过期后无法使用，<strong>请勿用于生产环境。</strong></p></li><li><p>文件上传凭证接口限流为 100 QPS 且不支持扩容，<strong>请勿用于生产环境、高并发及压测场景。</strong></p></li><li><p>生产环境建议使用<a href="https://help.aliyun.com/zh/oss/user-guide/what-is-oss">阿里云OSS</a> 等稳定存储，确保文件长期可用并规避限流问题。</p></li></ul></div></div><ul><li>录音文件URL设置成OSS临时公网访问不通该如何处理？请求头中将<code>X-DashScope-OssResourceResolve</code>设为<code>enable</code>（不推荐该方式）。 SDK不支持对请求头进行配置。</li></ul></td></tr><tr><td><p><code>async_request</code></p></td><td><p><code>boolean</code></p></td><td><p>否</p></td><td><p>语音识别是否为异步请求。 默认值：<code>false</code>。 取值范围： - true：异步请求 - false：同步请求</p></td></tr><tr><td><p><code>apikey</code></p></td><td><p><code>string</code></p></td><td><p>否</p></td><td><p>如果连接与控制参数的<code>apikey</code>使用的是<a href="../model-api-reference/more-about-models/generate-temporary-api-key.md">临时API Key</a>，可在此处进行更新，以免超时失效。</p></td></tr><tr><td><p><code>nls_config</code></p></td><td><p><code>object</code></p></td><td><p>是</p></td><td><p>语音识别核心配置对象，包含模型选择、识别效果控制等关键参数。</p></td></tr><tr><td><p><code>nls_config.model</code></p></td><td><p><code>string</code></p></td><td><p>是</p></td><td><p>模型名称。</p></td></tr><tr><td><p><code>nls_config.special_word_filter</code></p></td><td><p><code>object</code></p></td><td><p>否</p></td><td><p>指定在语音识别过程中需要处理的敏感词，并支持对不同敏感词设置不同的处理方式。详情请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/non-realtime-speech-recognition-user-guide.md#nrt03_sensitive_h3">敏感词过滤</a>。</p></td></tr><tr><td><p><code>nls_config.channel_id</code></p></td><td><p><code>array[integer]</code></p></td><td><p>否</p></td><td><p>指定在多音轨音频文件中需要识别的音轨索引，索引从 0 开始。例如，<code>[0]</code> 表示识别第一个音轨，<code>[0, 1]</code> 表示同时识别第一和第二个音轨。如果省略此参数，则默认处理第一个音轨。</p><div><div><p><strong>重要</strong>指定的每一个音轨都将独立计费。例如，为单个文件请求 <code>[0, 1]</code> 会产生两笔独立的费用。</p></div></div><p>默认值：<code>[0]</code>。</p></td></tr><tr><td><p><code>nls_config.diarization_enabled</code></p></td><td><p><code>boolean</code></p></td><td><p>否</p></td><td><p>是否启用说话人分离，默认关闭。 仅适用于单声道音频，多声道音频不支持说话人分离。 启用该功能后，识别结果中将显示<code>speaker_id</code>字段，用于区分不同说话人。</p><div><div><p><strong>说明</strong>如果启用说话人分离功能，建议音频时长不超过2小时，否则可能导致识别失败或超时。</p></div></div><p>默认值：false。 有关<code>speaker_id</code>的示例，请参见<a href="funauidio-asr-recorded-speech-recognition-python-d69dda8f4675042c.md#a9021178ccl7s">识别结果说明</a>。</p></td></tr><tr><td><p><code>nls_config.speaker_count</code></p></td><td><p><code>integer</code></p></td><td><p>否</p></td><td><div><div><p><strong>重要</strong>仅在开启说话人分离功能（<code>diarization_enabled</code>设置为<code>true</code>）时生效。</p></div></div><p>说话人数量参考值。取值范围为2至100的整数（包含2和100）。 默认自动判断说话人数量，如果配置此项，只能辅助算法尽量输出指定人数，无法保证一定会输出此人数。 无默认值。</p></td></tr><tr><td><p><code>nls_config.vocabulary_id</code></p></td><td><p><code>string</code></p></td><td><p>否</p></td><td><p>预编译热词列表 ID。 需预先调用创建热词列表接口生成，识别时传入该 ID 即可使用列表中的热词。 适用于词汇已知且相对稳定、需要跨请求复用同一词表的场景。 使用方法请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/improve-asr-accuracy.md#hw_precompiled_h3">预编译热词</a>。</p></td></tr><tr><td><p><code>nls_config.language_hints</code></p></td><td><p><code>array[string]</code></p></td><td><p>否</p></td><td><p>设置待识别语言代码。如果无法提前确定语种，可不设置，模型会自动识别语种。最多支持设置 1 个值，超出时仅前 1 个生效。</p><a id="accordion-点击查看支持的语言代码"></a><section><p>点击查看支持的语言代码</p><div><ul><li>zh: 中文</li><li>en: 英文</li><li>ja: 日语</li><li>ko：韩语</li><li>vi：越南语</li><li>th：泰语</li><li>id：印尼语</li><li>ms：马来语</li><li>tl：菲律宾语</li><li>hi：印地语</li><li>ar：阿拉伯语</li><li>fr：法语</li><li>de：德语</li><li>es：西班牙语</li><li>pt：葡萄牙语</li><li>ru：俄语</li><li>it：意大利语</li><li>nl：荷兰语</li><li>sv：瑞典语</li><li>da：丹麦语</li><li>fi：芬兰语</li><li>no：挪威语</li><li>el：希腊语</li><li>pl：波兰语</li><li>cs：捷克语</li><li>hu：匈牙利语</li><li>ro：罗马尼亚语</li><li>bg：保加利亚语</li><li>hr：克罗地亚语</li><li>sk：斯洛伐克语</li></ul></div></section></td></tr><tr><td><p><code>nls_config.parameters</code></p></td><td><p><code>object</code></p></td><td><p>否</p></td><td><p>配置其他参数，内容为JSON Object格式。</p></td></tr></tbody></table>

<a id="关键接口"></a>

## 关键接口

<a id="nativenui"></a>

### NativeNui

<a id="initializefiletrans"></a>

#### initializeFileTrans

初始化语音转录 SDK 实例。在调用 `release` 前禁止重复初始化。

> **说明**
>
> 与实时语音识别不同，非实时（录音文件）转录必须使用 `initializeFileTrans` 方法并传入 `INativeFileTransCallback` 回调，而不是 `initialize`。

该接口会阻塞调用线程，请在非 UI 线程中调用。

**方法签名**

<a id="code-block-3"></a>

```typescript
public initializeFileTrans(callback: INativeFileTransCallback,
                           parameters: string,
                           level: number,
                           save_log: boolean = false): number
```

**参数说明**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `callback` | `INativeFileTransCallback` | 文件转录事件和数据回调接口的实现。 |
| `parameters` | `string` | JSON字符串，包含鉴权、连接和调试参数。参见连接与控制参数。 |
| `level` | `number` | 控制SDK自身日志的打印级别，取值为`Constants.LogLevel`枚举。 |
| `save_log` | `boolean` | 是否保存本地日志。若为`true`，须在连接与控制参数中通过`debug_path`指定路径，并可通过`max_log_file_size`设置文件大小。 |

<a id="setparams"></a>

#### setParams

此接口用于独立设置或更新 `nls_config` 参数。如果所有参数都在`startFileTranscriber`中一次性提供，则无需调用此方法。

**方法签名**

<a id="code-block-4"></a>

```typescript
public setParams(params: string): number
```

**参数说明**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `params` | `string` | 语音识别效果参数中的`nls_config`参数，`nls_config`之外的参数不支持通过该方法进行设置。 示例： `{ "nls_config": { "model":"fun-asr", "diarization_enabled": false } }` |

<a id="startfiletranscriber"></a>

#### startFileTranscriber

开始识别。

**方法签名**

<a id="code-block-5"></a>

```typescript
public startFileTranscriber(params: string, task_id: ArrayBuffer): number
```

**参数说明**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `params` | `string` | 语音识别效果参数。 示例： `{ "file_urls": [ "{YOUR_AUDIO_URL}" ], "async_request": false, "nls_config": { "model":"fun-asr", "diarization_enabled": false } }` |
| `task_id` | `ArrayBuffer` | 任务ID缓冲区。SDK会将内部生成的随机任务ID字符串写入该缓冲区，要求缓冲区字节长度必须大于或等于33字节（示例中使用 `new ArrayBuffer(64)`）。调用成功后可通过转码获取该任务的`task_id`。 |

<a id="queryfiletranscriber"></a>

#### queryFileTranscriber

此接口用于主动查询一个异步任务的当前状态和结果。调用成功后，结果将通过`onFileTransEventCallback`回调中的 `EVENT_FILE_TRANS_QUERY_RESULT` 事件返回。

**方法签名**

<a id="code-block-6"></a>

```typescript
public queryFileTranscriber(task_id: string): number
```

**参数说明**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `task_id` | `string` | 待查询的任务ID（由 `startFileTranscriber` 写入缓冲区获得）。 |

<a id="cancelfiletranscriber"></a>

#### cancelFileTranscriber

立即取消当前任务。

**方法签名**

<a id="code-block-7"></a>

```typescript
public cancelFileTranscriber(task_id: string): number
```

**参数说明**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `task_id` | `string` | 待取消的任务ID。 |

<a id="release"></a>

#### release

释放 SDK 的所有内部资源。调用后，SDK 实例将不可用；如需再次使用，必须重新调用 `initializeFileTrans` 进行初始化。

**方法签名**

<a id="code-block-8"></a>

```typescript
public release(): number
```

<a id="getversion"></a>

#### GetVersion

获取当前 SDK 版本信息。

**方法签名**

<a id="code-block-9"></a>

```typescript
public GetVersion(): string
```

**返回值说明**

当前 SDK 版本信息。

<a id="inativefiletranscallback"></a>

### INativeFileTransCallback

定义文件转录过程中的事件与识别结果回调。

<a id="onfiletranseventcallback"></a>

#### onFileTransEventCallback

监听文件转录事件并获取语音识别结果。

**方法签名**

<a id="code-block-10"></a>

```typescript
onFileTransEventCallback: (event: Constants.NuiEvent, resultCode: number, finish: number,
                           asrResult: AsrResult, taskId: string) => void;
```

**参数说明**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `event` | `Constants.NuiEvent` | 回调事件。 |
| `resultCode` | `number` | 仅在出现 `EVENT_ASR_ERROR` 事件时有效。 |
| `finish` | `number` | 任务是否结束标记。 |
| `asrResult` | `AsrResult` | 语音识别结果。 |
| `taskId` | `string` | 任务ID。 |

<a id="constants-nuievent"></a>

### Constants.NuiEvent

HarmonyOS SDK 中事件类型通过 `Constants.NuiEvent` 枚举定义，以下列出录音文件转录相关的事件：

| 事件 | 说明 |
| --- | --- |
| `EVENT_FILE_TRANS_CONNECTED` | 连接服务成功。 |
| `EVENT_FILE_TRANS_UPLOADED` | 上传待识别音频文件成功。 |
| `EVENT_FILE_TRANS_QUERY_RESULT` | 查询任务结果。 |
| `EVENT_FILE_TRANS_RESULT` | 识别最终结果。 |
| `EVENT_ASR_ERROR` | 语音识别过程中出现错误。 |

<a id="辅助类型"></a>

## 辅助类型

<a id="constants-loglevel"></a>

### Constants.LogLevel

`level` 参数的取值枚举：

| 值 | 说明 |
| --- | --- |
| `LOG_LEVEL_VERBOSE` | 最详细日志。 |
| `LOG_LEVEL_DEBUG` | 调试日志。 |
| `LOG_LEVEL_INFO` | 普通信息日志（默认）。 |
| `LOG_LEVEL_WARNING` | 警告日志。 |
| `LOG_LEVEL_ERROR` | 错误日志。 |
| `LOG_LEVEL_NONE` | 关闭日志。 |

<a id="结果下载"></a>

## 结果下载

非实时语音识别结果为异步生成，`EVENT_FILE_TRANS_RESULT` 事件返回的应答中包含 `transcription_url`，识别文本需通过该 URL 下载获取（JSON 格式）。注意该 URL 具有有效期，应及时下载。
