# 非实时语音识别（Fun-ASR-Flash）HarmonyOS SDK

Fun-ASR-Flash非实时语音识别HarmonyOS SDK可将语音转换为文本。

关于支持的音频格式、文件大小限制、时长限制等输入要求，请参见[音频规格](../model-user-guide/model-experience/speech-and-audio/speech-recognition/asr-model.md#asr_audio_spec02)。

<a id="快速开始"></a>

## 快速开始

1.  **获取API Key：**[获取API Key](../model-api-reference/preparations/get-api-key.md)，为安全起见，推荐将API Key配置到环境变量。
2.  **下载SDK并运行示例代码：**
    -   [下载最新SDK整合包](../model-api-reference/more-about-models/sdk-selection-and-download.md)。
    -   解压 TAR 包。在 `neonui` 目录中获取 HAR 格式 SDK，并添加到项目依赖。需要 C++ 接入时，使用 TAR 包内的 `native/libs` 与 `native/include` 获取动态库和头文件。
    -   用 DevEco Studio 打开工程。示例代码位于 `DashFunAsrFlashFileTranscriberPage.ets`，替换 API Key 后体验功能。

<a id="调用步骤"></a>

### 调用步骤

<a id="同步模式"></a>

#### 同步模式

1.  初始化 SDK
    
2.  按业务需求配置相关参数
    
3.  调用 `startFileTranscriber` 发送非实时语音识别请求，并等待结果返回。
    
4.  在`onFileTransEventCallback`接口中监听`EVENT_FILE_TRANS_RESULT` 事件，获取最终识别结果。
    
5.  调用 `release` 释放 SDK 资源
    

<a id="请求参数"></a>

## 请求参数

<a id="连接与控制参数"></a>

<a id="connection-parameters"></a>

### 连接与控制参数

通过在`initializeFileTrans`接口的`parameters`参数中传入一个JSON字符串来配置。

**参数示例：**以下为 JSON 字符串示例，参数未完整列出。请按实际需求在编码时补充：

<a id="code-block"></a>

```json
{
    "url": "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation",
    "apikey": "st-****",
    "device_id": "my_device_id",
    "service_mode": "1"
}
```

**参数说明**

| 参数 | 类型 | 是否必须 | 说明 |
| --- | --- | --- | --- |
| `url` | `string` | 是 | 服务地址，固定为 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`。调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。 |
| `apikey` | `string` | 是 | API Key。建议使用时效性短、安全性更高的[临时API Key](../model-api-reference/more-about-models/generate-temporary-api-key.md)，以降低长期有效Key泄露的风险。 |
| `service_mode` | `string` | 是 | 运行模式。非实时语音识别固定为 `"1"`。 |
| `device_id` | `string` | 是 | 用于标识终端用户的唯一字符串，可设为应用内用户ID或客户端生成的设备唯一标识符。此ID主要用于日志追踪和问题排查。 |
| `debug_path` | `string` | 否 | 日志文件的存储路径。 此参数仅在调用`initializeFileTrans`接口时将`save_log`设为true时生效。此时必须设置日志文件路径，否则将报错。 本地最多保留两个日志文件。 |
| `max_log_file_size` | `number` | 否 | 设定日志文件的最大字节数。 此参数仅在调用`initializeFileTrans`接口时将`save_log`设为true时生效。 默认值：104857600（100 \* 1024 \* 1024 字节, 即 100MiB）。 |

<a id="语音识别效果参数"></a>

<a id="recognition-parameters"></a>

### 语音识别效果参数

通过`setParams`接口配置`nls_config`参数，或者通过`startFileTranscriber`接口配置所有语音识别效果参数。

**参数示例：**以下为 JSON 字符串示例，参数未完整列出。请按实际需求在编码时补充：

<a id="code-block-2"></a>

```json
{
  "apikey": "st-****",
  "messages": [
    {
      "content": [
        {
          "input_audio": {
            "data": "{YOUR_AUDIO_URL}"
          },
          "type": "input_audio"
        }
      ],
      "role": "user"
    }
  ],
  "nls_config": {
    "format": "mp3",
    "model": "fun-asr-flash-2026-06-15"
  }
}
```

**参数说明**

<table><thead><tr><th><strong>参数</strong></th><th><strong>类型</strong></th><th><strong>是否必须</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><p><code>apikey</code></p></td><td><p><code>string</code></p></td><td><p>否</p></td><td><p>如果连接与控制参数的<code>apikey</code>使用的是<a href="../model-api-reference/more-about-models/generate-temporary-api-key.md">临时API Key</a>，可在此处进行更新，以免超时失效。</p></td></tr><tr><td><p><code>nls_config</code></p></td><td><p><code>object</code></p></td><td><p>是</p></td><td><p>语音识别核心配置对象，包含模型选择、识别效果控制等关键参数。</p></td></tr><tr><td><p><code>nls_config.model</code></p></td><td><p><code>string</code></p></td><td><p>是</p></td><td><p>模型名称。</p></td></tr><tr><td><p><code>nls_config.format</code></p></td><td><p><code>string</code></p></td><td><p>是</p></td><td><p>音频格式。根据实际音频格式填写，支持<code>wav</code>、<code>mp3</code>、<code>opus</code>等。详情请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/asr-model.md#asr_audio_spec02">音频规格</a>。</p></td></tr><tr><td><p><code>nls_config.sample_rate</code></p></td><td><p><code>string</code></p></td><td><p>否</p></td><td><p>音频采样率，单位Hz。例如<code>16000</code>表示16kHz采样率。详情请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/asr-model.md#asr_audio_spec02">音频规格</a>。</p></td></tr><tr><td><p><code>nls_config.vocabulary_id</code></p></td><td><p><code>string</code></p></td><td><p>否</p></td><td><p>预编译热词列表 ID。 需预先调用创建热词列表接口生成，识别时传入该 ID 即可使用列表中的热词。 适用于词汇已知且相对稳定、需要跨请求复用同一词表的场景。 使用方法请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/improve-asr-accuracy.md#hw_precompiled_h3">预编译热词</a>。</p></td></tr><tr><td><p><code>nls_config.language_hints</code></p></td><td><p><code>array[string]</code></p></td><td><p>否</p></td><td><p>设置待识别语言代码。如果无法提前确定语种，可不设置，模型会自动识别语种。最多支持设置 1 个值，超出时仅前 1 个生效。</p><a id="accordion-支持的语言代码"></a><section><p>支持的语言代码</p><div><ul><li>zh: 中文</li><li>en: 英文</li><li>ja: 日语</li><li>ko: 韩语</li><li>vi: 越南语</li><li>th: 泰语</li><li>id: 印尼语</li><li>ms: 马来语</li><li>tl: 菲律宾语</li><li>hi: 印地语</li><li>ar: 阿拉伯语</li><li>fr: 法语</li><li>de: 德语</li><li>es: 西班牙语</li><li>pt: 葡萄牙语</li><li>ru: 俄语</li><li>it: 意大利语</li><li>nl: 荷兰语</li><li>sv: 瑞典语</li><li>da: 丹麦语</li><li>fi: 芬兰语</li><li>no: 挪威语</li><li>el: 希腊语</li><li>pl: 波兰语</li><li>cs: 捷克语</li><li>hu: 匈牙利语</li><li>ro: 罗马尼亚语</li><li>bg: 保加利亚语</li><li>hr: 克罗地亚语</li><li>sk: 斯洛伐克语</li></ul></div></section></td></tr><tr><td><p><code>messages</code></p></td><td><p><code>array[object]</code></p></td><td><p>是</p></td><td><p>消息列表。包含当前待识别的音频，以及可选的对话上下文（用于提升识别效果）。</p><strong>详见如下说明。</strong></td></tr></tbody></table>

**messages参数说明：**

> **重要**
>
> 上下文功能用于提升专有词汇的识别准确率，使用方法详见[上下文增强](../model-user-guide/model-experience/speech-and-audio/speech-recognition/improve-asr-accuracy.md#ctx_enhance_h2)。
>
> 上下文消息（`input_text` 和 `text` 类型）各最多 5 条，超出时保留最近的 5 条。每轮上下文文本总长度（`user` 和 `assistant` 的 `text` 字段长度之和）不超过 400 个字符（按字符数计算，每个字符计为 1），超出部分从末尾截断。

> **重要**
>
> 携带上下文时，`messages` 中的消息顺序有要求：上下文消息必须按对话轮次排列，每轮中 `user`（`input_text` 类型）必须在对应的 `assistant`（`text` 类型）之前；包含 `input_audio` 的 `user` 消息必须放在 `messages` 数组的最后。

<table><thead><tr><th><strong>参数</strong></th><th><strong>类型</strong></th><th><strong>是否必须</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><p><code>role</code></p></td><td><p><code>string</code></p></td><td><p>是</p></td><td><p>消息角色。取值范围：</p><ul><li><p><code>user</code>（必选）：用户消息。type为<code>input_audio</code>时表示当前待识别的音频；type为<code>input_text</code>时表示前几轮的识别结果或领域相关的词表（可选，上下文）。</p></li><li><p><code>assistant</code>（可选，上下文）：前几轮大语言模型的回复内容。</p></li></ul></td></tr><tr><td><p><code>content</code></p></td><td><p><code>array[object]</code></p></td><td><p>是</p></td><td><p>消息内容列表。详细如下说明。</p></td></tr></tbody></table>

**content参数说明：**

<table><thead><tr><th><strong>参数</strong></th><th><strong>类型</strong></th><th><strong>是否必须</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><p><code>type</code></p></td><td><p><code>string</code></p></td><td><p>是</p></td><td><p>内容类型。每个请求至少需要一条<code>input_audio</code>类型的消息。取值范围：</p><ul><li><p><code>input_audio</code>（必选）：当前待识别的音频输入（role为user），需同时传入<code>input_audio</code>对象。</p></li><li><p><code>input_text</code>（可选，上下文）：前几轮用户语音的识别结果或领域相关的词表（role为user），需同时传入<code>text</code>字段。</p></li><li><p><code>text</code>（可选，上下文）：前几轮大语言模型的回复内容（role为assistant），需同时传入<code>text</code>字段。</p></li></ul></td></tr><tr><td><p><code>input_audio</code></p></td><td><p><code>object</code></p></td><td><p>否</p></td><td><p>当<code>type</code>为<code>input_audio</code>时必填。</p></td></tr><tr><td><p><code>input_audio.data</code></p></td><td><p><code>string</code></p></td><td><p>是</p></td><td><p>待识别音频数据。关于支持的音频格式、文件大小限制、时长限制等输入要求，请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/asr-model.md#asr_audio_spec02">音频规格</a>。支持以下两种方式：</p><ul><li><p><strong>音频文件URL</strong>：直接传入可公开访问的音频文件地址。</p></li><li><p><strong>Base64 Data URI</strong>：采用Data URI格式传入Base64编码的音频数据，值由<code>data:{MIME_TYPE};base64,</code>前缀与Base64编码的音频数据拼接而成。支持的MIME类型包括<code>audio/wav</code>、<code>audio/mp3</code>等。</p><p>示例（URL方式）：<code><a href="https://example.com/audio/sample.wav">https://example.com/audio/sample.wav</a></code></p><p>示例（Base64方式）：<code>data:audio/wav;base64,{BASE64_ENCODED_DATA}</code></p></li></ul></td></tr><tr><td><p><code>text</code></p></td><td><p><code>string</code></p></td><td><p>否</p></td><td><p>当<code>type</code>为<code>input_text</code>时，填入前几轮用户语音的识别结果或领域相关的词表；当<code>type</code>为<code>text</code>时，填入前几轮大语言模型的回复内容。文本按字符数计算，每个字符计为 1。每轮上下文中所有消息的 <code>text</code> 字段长度之和不超过 400 个字符，超出部分从末尾截断。</p></td></tr></tbody></table>

<a id="关键接口"></a>

## 关键接口

<a id="nativenui"></a>

### NativeNui

<a id="initializefiletrans"></a>

<a id="initializefiletrans-2"></a>

#### initializeFileTrans

初始化语音识别SDK实例。

> **说明**
>
> 与实时语音识别不同，非实时（录音文件）转录必须使用 `initializeFileTrans` 方法并传入 `INativeFileTransCallback` 回调，而不是 `initialize`。

此接口会引起阻塞，应在非UI线程调用。

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
| `level` | `number` | 控制SDK自身日志的打印级别，取值为枚举。 |
| `save_log` | `boolean` | 是否保存本地日志。若为`true`，须在连接与控制参数中通过`debug_path`指定路径，并可通过`max_log_file_size`设置文件大小。 |

<a id="setparams"></a>

<a id="setparams-2"></a>

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
| `params` | `string` | 语音识别效果参数中的`nls_config`参数，`nls_config`之外的参数不支持通过该方法进行设置。 |

<a id="startfiletranscriber"></a>

<a id="startfiletranscriber-2"></a>

#### startFileTranscriber

开始识别。

**方法签名**

<a id="code-block-5"></a>

```typescript
public startFileTranscriber(params: string, task_id: ArrayBuffer): number
```

**参数说明**

<table><thead><tr><th><strong>参数</strong></th><th><strong>类型</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><p><code>params</code></p></td><td><p><code>string</code></p></td><td><p>语音识别效果参数。</p><p>示例：</p><a id="code-block-6"></a><pre class="language-json"><code>{
 &quot;apikey&quot;: &quot;st-****&quot;,
 &quot;messages&quot;: [
 {
 &quot;content&quot;: [
 {
 &quot;input_audio&quot;: {
 &quot;data&quot;: &quot;{YOUR_AUDIO_URL}&quot;
 },
 &quot;type&quot;: &quot;input_audio&quot;
 }
 ],
 &quot;role&quot;: &quot;user&quot;
 }
 ],
 &quot;nls_config&quot;: {
 &quot;format&quot;: &quot;mp3&quot;,
 &quot;model&quot;: &quot;fun-asr-flash-2026-06-15&quot;
 }
}
</code></pre></td></tr><tr><td><p><code>task_id</code></p></td><td><p><code>ArrayBuffer</code></p></td><td><p>任务ID缓冲区。SDK会将内部生成的随机任务ID字符串写入该缓冲区，要求缓冲区字节长度必须 <strong>&gt;= 33字节</strong>（示例中使用 <code>new ArrayBuffer(64)</code>）。调用成功后可通过转码获取该任务的<code>task_id</code>。</p></td></tr></tbody></table>

<a id="queryfiletranscriber"></a>

#### queryFileTranscriber

此接口用于主动查询一个异步任务的当前状态和结果。调用成功后，结果将通过`onFileTransEventCallback`回调中的 `EVENT_FILE_TRANS_QUERY_RESULT` 事件返回。

**方法签名**

<a id="code-block-7"></a>

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

<a id="code-block-8"></a>

```typescript
public cancelFileTranscriber(task_id: string): number
```

**参数说明**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `task_id` | `string` | 待取消的任务ID。 |

<a id="release"></a>

<a id="release-2"></a>

#### release

释放SDK所有内部资源。此方法调用后，SDK实例将变为不可用状态，如需再次使用，必须重新调用`initializeFileTrans`进行初始化。

**方法签名**

<a id="code-block-9"></a>

```typescript
public release(): number
```

<a id="getversion"></a>

#### GetVersion

获得当前SDK版本信息。

**方法签名**

<a id="code-block-10"></a>

```typescript
public GetVersion(): string
```

**返回值说明**

当前SDK版本信息。

<a id="inativefiletranscallback-监听回调"></a>

<a id="file-trans-callback"></a>

### INativeFileTransCallback：监听回调

<a id="onfiletranseventcallback-监听事件和语音识别结果"></a>

#### onFileTransEventCallback：监听事件和语音识别结果

**方法签名**

<a id="code-block-11"></a>

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

<a id="onfiletranslogtrackcallback-监听追踪日志"></a>

<a id="log-callback"></a>

#### onFileTransLogTrackCallback：监听追踪日志

此回调用于接收 SDK 内部的详细日志，方便进行问题定位和调试。

使用此回调需下载 20260908 或更新的 HarmonyOS SDK 包。

<a id="code-block-12"></a>

```typescript
onFileTransLogTrackCallback?: (level: Constants.LogLevel, log: string) => void;
```

<a id="事件类型"></a>

### 事件类型

HarmonyOS SDK 中事件类型通过 `Constants.NuiEvent` 枚举定义，以下列出录音文件转录相关的事件：

| 事件 | 说明 |
| --- | --- |
| `EVENT_FILE_TRANS_CONNECTED` | 连接服务成功。 |
| `EVENT_FILE_TRANS_UPLOADED` | 上传待识别音频文件成功。 |
| `EVENT_FILE_TRANS_QUERY_RESULT` | 查询任务结果。 |
| `EVENT_FILE_TRANS_RESULT` | 识别最终结果。 |
| `EVENT_ASR_ERROR` | 语音识别过程中出现错误。 |
