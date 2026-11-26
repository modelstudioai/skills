# Paraformer Android SDK

本文档提供了Paraformer实时语音识别Android SDK的详细使用指南，帮助您将语音转换为文本。

> **重要**
>
> 阿里云百炼为华北2（北京）地域推出了业务空间专属域名，能够为推理请求提供卓越的性能和更高的稳定性，建议从 `dashscope.aliyuncs.com` 迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`。
>
> `{WorkspaceId}`需要替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。现有域名仍可正常使用。

**用户指南：**关于模型介绍和选型建议请参见[实时语音识别-Fun-ASR/Paraformer](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition)。

<a id="前提条件"></a>

## 前提条件

1.  [获取与配置 API Key](../model-api-reference/preparations/get-api-key.md)。移动端应用请勿硬编码长期 API Key。建议由应用服务端[生成临时 API Key](../model-api-reference/more-about-models/generate-temporary-api-key.md)，再下发给客户端。

<a id="安装-sdk"></a>

### 安装 SDK

-   [下载最新SDK整合包](../model-api-reference/more-about-models/sdk-selection-and-download.md)。
-   解压 ZIP 包。在 `app/libs` 目录中获取 AAR 格式 SDK，并添加到项目依赖。  
    需要 Android CPP 接入时，使用 ZIP 包内的 `android_libs` 与 `android_include` 获取动态库和头文件。  
      
    

<a id="快速开始"></a>

<a id="abf215f434v5x"></a>

## 快速开始

用 Android Studio 打开工程。示例代码位于`DashParaformerSpeechTranscriberActivity.java`，替换 API Key 后体验功能。

<a id="调用步骤"></a>

<a id="0701a2d0b75vm"></a>

### 调用步骤

1.  初始化 SDK
2.  按业务需求设置参数：通过[initialize](android-sdk-for-paraformer-real-time-service-9e7815d0b3adcb41.md#ae6d7dd9cfad3)接口的`parameters`参数设置[连接与控制参数](android-sdk-for-paraformer-real-time-service-9e7815d0b3adcb41.md#57acf5ecc1w8j)；通过[setParams](android-sdk-for-paraformer-real-time-service-9e7815d0b3adcb41.md#a23e0d85d7ymt)接口设置[语音识别效果参数](android-sdk-for-paraformer-real-time-service-9e7815d0b3adcb41.md#d20cce9518kla)。
3.  调用[startDialog](android-sdk-for-paraformer-real-time-service-9e7815d0b3adcb41.md#7d33691bdb32v)启动识别流程。
4.  在[onNuiAudioStateChanged](android-sdk-for-paraformer-real-time-service-9e7815d0b3adcb41.md#bc71fe2545pfy)回调中，根据音频状态开启录音设备。
5.  在[onNuiNeedAudioData](android-sdk-for-paraformer-real-time-service-9e7815d0b3adcb41.md#12577ebc97awb)回调中持续提供录音数据。
6.  在[onNuiEventCallback](android-sdk-for-paraformer-real-time-service-9e7815d0b3adcb41.md#163c1ef871tqt)回调中监听事件并获取语音识别结果。
7.  调用[stopDialog](android-sdk-for-paraformer-real-time-service-9e7815d0b3adcb41.md#047417083bahi)停止识别，并通过监听EVENT\_TRANSCRIBER\_COMPLETE事件确认识别已结束。
8.  当识别功能不再使用时，调用[release](android-sdk-for-paraformer-real-time-service-9e7815d0b3adcb41.md#44bf12ed9a4g9)接口释放 SDK 资源。

<a id="请求参数"></a>

<a id="a96bfa6340jdd"></a>

## 请求参数

<a id="连接与控制参数"></a>

<a id="57acf5ecc1w8j"></a>

### 连接与控制参数

通过在[initialize](android-sdk-for-paraformer-real-time-service-9e7815d0b3adcb41.md#ae6d7dd9cfad3)接口的`parameters`参数中传入一个JSON字符串来配置。

-   **参数示例：**以下为 JSON 字符串示例，参数未完整列出。请按实际需求在编码时补充：

<a id="code-block"></a>

```json
{
    "url": "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference",
    "apikey": "st-****",
    "device_id": "my_device_id",
    "service_mode": "1"
}
```

-   **参数说明**
    
    <table><thead><tr><th><p><strong>参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>是否必须</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p><code>url</code></p></td><td><p><code>String</code></p></td><td><p>是</p></td><td><p>服务地址，固定为 <code>wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference</code>。调用时请将<code>{WorkspaceId}</code>替换为真实的<a href="../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain">Workspace ID</a>。</p></td></tr><tr><td><p><code>apikey</code></p></td><td><p><code>String</code></p></td><td><p>是</p></td><td><p>API Key。建议使用时效性短、安全性更高的<a href="../model-api-reference/more-about-models/generate-temporary-api-key.md">临时API Key</a>，以降低长期有效Key泄露的风险。</p></td></tr><tr><td><p><code>service_mode</code></p></td><td><p><code>String</code></p></td><td><p>是</p></td><td><p>运行模式。实时语音识别固定为 <code>&quot;1&quot;</code>。</p></td></tr><tr><td><p><code>device_id</code></p></td><td><p><code>String</code></p></td><td><p>是</p></td><td><p>用于标识终端用户的唯一字符串，可设为应用内用户ID或客户端生成的设备唯一标识符。此ID主要用于日志追踪和问题排查。</p></td></tr><tr><td><p><code>debug_path</code></p></td><td><p><code>String</code></p></td><td><p>否</p></td><td><p>日志文件的存储路径。</p><p>此参数仅在调用<a href="android-sdk-for-paraformer-real-time-service-9e7815d0b3adcb41.md#ae6d7dd9cfad3">initialize</a>接口时将<code>save_log</code>设为true时生效。此时必须设置日志文件路径，否则将报错。</p><p>本地最多保留两个日志文件。</p></td></tr><tr><td><p><code>save_wav</code></p></td><td><p><code>String</code></p></td><td><p>否</p></td><td><p>是否保存调试用的音频文件。音频文件保存于<code>debug_path</code>下。</p><p>默认值：&quot;false&quot;。</p><p>取值范围：</p><ul><li><p>&quot;true&quot;：是</p></li><li><p>&quot;false&quot;：否</p></li></ul><p>此参数仅在调用<a href="android-sdk-for-paraformer-real-time-service-9e7815d0b3adcb41.md#ae6d7dd9cfad3">initialize</a>接口时将<code>save_log</code>设为true时生效。 同时，<code>debug_path</code>也必须被设置。</p></td></tr><tr><td><p><code>max_log_file_size</code></p></td><td><p><code>int</code></p></td><td><p>否</p></td><td><p>设定日志文件的最大字节数。</p><p>此参数仅在调用<a href="android-sdk-for-paraformer-real-time-service-9e7815d0b3adcb41.md#ae6d7dd9cfad3">initialize</a>接口时将<code>save_log</code>设为true时生效。</p><p>默认值：104857600（100 * 1024 * 1024 字节，即 100MiB）。</p></td></tr><tr><td><p><code>log_track_level</code></p></td><td><p><code>int</code></p></td><td><p>否</p></td><td><p>控制通过日志回调（<code>onNuiLogTrackCallback</code>）对外发送的日志内容的过滤级别。</p><p>默认值：2。</p><p>取值范围：</p><ul><li><p>0：LOG_LEVEL_VERBOSE</p></li><li><p>1：LOG_LEVEL_DEBUG</p></li><li><p>2：LOG_LEVEL_INFO</p></li><li><p>3：LOG_LEVEL_WARNING</p></li><li><p>4：LOG_LEVEL_ERROR</p></li><li><p>5：LOG_LEVEL_NONE（表示关闭此功能）</p></li></ul><p>注意：<code>log_track_level</code>与<code>level</code>（通过<a href="android-sdk-for-paraformer-real-time-service-9e7815d0b3adcb41.md#ae6d7dd9cfad3">initialize</a>接口设置）共同决定最终回调的日志。一条日志的级别数值必须同时大于或等于<code>log_track_level</code>和<code>level</code>的值，才会被回调。例如，<code>log_track_level</code>设为2 (INFO)，<code>level</code>设为3 (WARNING)，则只有WARNING及以上级别（数值&gt;=3）的日志才会被回调。</p></td></tr></tbody></table>
    

<a id="语音识别效果参数"></a>

<a id="d20cce9518kla"></a>

### 语音识别效果参数

通过在[setParams](android-sdk-for-paraformer-real-time-service-9e7815d0b3adcb41.md#a23e0d85d7ymt)接口的`params`参数中传入一个JSON字符串来配置。

-   **参数示例：**以下为 JSON 字符串示例，参数未完整列出。请按实际需求在编码时补充：

<a id="code-block-2"></a>

```json
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
    
    <table><thead><tr><th><strong>一级参数</strong></th><th><strong>类型</strong></th><th><strong>是否必须</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><p><code>service_type</code></p></td><td><p><code>int</code></p></td><td><p>是</p></td><td><p>语音服务类型。实时语音识别固定为 <code>4</code>。</p></td></tr><tr><td><p><code>nls_config</code></p></td><td><p><code>object</code></p></td><td><p>是</p></td><td><p>语音识别核心配置对象，包含模型选择、识别效果控制等关键参数。</p></td></tr><tr><td><p><code>nls_config.model</code></p></td><td><p><code>string</code></p></td><td><p>是</p></td><td><p>语音识别<a href="websocket-for-paraformer-real-time-service-71905b8ff2bb55c1.md">模型</a>。</p></td></tr><tr><td><p><code>nls_config.sr_format</code></p></td><td><p><code>string</code></p></td><td><p>是</p></td><td><p>待识别音频格式。</p><p>支持的音频格式：pcm、wav、opus。</p><div><div><p><strong>重要</strong></p><ul><li>opus：必须为PCM编码，SDK内部会将其编码成OPUS格式；</li><li>wav/pcm：必须为PCM编码。</li></ul></div></div></td></tr><tr><td><p><code>nls_config.sample_rate</code></p></td><td><p><code>int</code></p></td><td><p>是</p></td><td><p>待识别音频采样率（单位Hz）。</p><p>因模型而异：</p><ul><li><p>paraformer-realtime-v2支持任意采样率。</p></li><li><p>paraformer-realtime-8k-v2仅支持8000Hz采样率。</p></li></ul></td></tr><tr><td><p><code>nls_config.disfluency_removal_enabled</code></p></td><td><p><code>boolean</code></p></td><td><p>否</p></td><td><p>是否过滤语气词，如“嗯”、“啊”等。</p><p>默认值：false。</p></td></tr><tr><td><p><code>nls_config.language_hints</code></p></td><td><p><code>array[string]</code></p></td><td><p>否</p></td><td><p>设置待识别语言代码。如果无法提前确定语种，可不设置，模型会自动识别语种。</p><p>支持的语言代码：</p><ul><li>zh: 中文</li><li>en: 英文</li><li>ja: 日语</li><li>yue: 粤语</li><li>ko: 韩语</li><li>de：德语</li><li>fr：法语</li><li>ru：俄语</li></ul><p>该参数仅对支持多语言的<a href="websocket-for-paraformer-real-time-service-71905b8ff2bb55c1.md">模型</a>生效</p></td></tr><tr><td><p><code>nls_config.semantic_punctuation_enabled</code></p></td><td><p><code>boolean</code></p></td><td><p>否</p></td><td><p>设置断句模式。</p><p>默认值：false。</p><p>取值范围：</p><ul><li>true：开启语义断句，关闭VAD断句。</li><li>false：开启VAD断句，关闭语义断句。</li></ul><p>语义断句准确性更高，适合会议转写场景；VAD（Voice Activity Detection，语音活动检测）断句延迟较低，适合实时交互场景。</p><p>该参数仅在模型为v2及更高版本时生效。</p></td></tr><tr><td><p><code>nls_config.max_sentence_silence</code></p></td><td><p><code>int</code></p></td><td><p>否</p></td><td><p>VAD（Voice Activity Detection，语音活动检测）断句的静音时长阈值（单位为ms）。</p><p>默认值：800。</p><p>取值范围：[200, 6000]。</p><p>当一段语音后的静音时长超过该阈值时，系统会判定该句子已结束。</p><p>该参数仅在<code>semantic_punctuation_enabled</code>参数为false且模型为v2及更高版本时生效。</p></td></tr><tr><td><p><code>nls_config.multi_threshold_mode_enabled</code></p></td><td><p><code>boolean</code></p></td><td><p>否</p></td><td><p>是否开启防过长切割模式。开启可防止VAD断句切割过长。</p><p>默认值：false（关闭）。</p><p>取值范围：</p><ul><li>true：开启</li><li>false：关闭</li></ul><p>该参数仅在<code>semantic_punctuation_enabled</code>参数为false且模型为v2及更高版本时生效。</p></td></tr><tr><td><p><code>nls_config.punctuation_prediction_enabled</code></p></td><td><p><code>boolean</code></p></td><td><p>否</p></td><td><p>是否在识别结果中自动添加标点符号。</p><p>默认值：true（是）。</p><p>取值范围：</p><ul><li>true：是</li><li>false：否</li></ul><p>该参数仅在模型为v2及更高版本时生效。</p></td></tr><tr><td><p><code>nls_config.heartbeat</code></p></td><td><p><code>boolean</code></p></td><td><p>否</p></td><td><p>是否和服务端保持长连接。</p><p>默认值：false。</p><p>取值范围：</p><ul><li>true：在持续发送静音音频的情况下，可保持与服务端的连接不中断。</li><li>false：即使持续发送静音音频，连接也将在一定时间后因超时而断开。该超时为服务端默认行为，客户端不可配置。</li></ul><p>该参数仅在模型为v2及更高版本时生效。</p></td></tr><tr><td><p><code>nls_config.inverse_text_normalization_enabled</code></p></td><td><p><code>boolean</code></p></td><td><p>否</p></td><td><p>是否开启ITN（Inverse Text Normalization，逆文本正则化）。开启后，中文数字将转换为阿拉伯数字。</p><p>默认值：true（开启）。</p><p>取值范围：</p><ul><li>true：开启</li><li>false：关闭</li></ul><p>该参数仅在模型为v2及更高版本时生效。</p></td></tr><tr><td><p><code>nls_config.vocabulary_id</code></p></td><td><p><code>string</code></p></td><td><p>否</p></td><td><p>热词词表ID，用于提升特定词汇的识别准确率。该参数适用于v2及更高版本模型。热词的使用方法请参见<a href="../model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words.md">定制热词</a>。</p></td></tr></tbody></table>
    

<a id="接口参考"></a>

<a id="737b46fda6cbf"></a>

<a id="关键接口"></a>

## 接口参考

<a id="nativenui"></a>

<a id="4bed3999d9kx0"></a>

### NativeNui

<a id="initialize"></a>

<a id="ae6d7dd9cfad3"></a>

#### initialize

初始化语音识别SDK实例。SDK为单例模式，在调用[release](android-sdk-for-paraformer-real-time-service-9e7815d0b3adcb41.md#44bf12ed9a4g9)前禁止重复初始化。

此接口会引起阻塞，应在非UI线程调用。

-   **方法签名**

<a id="code-block-3"></a>

```java
public synchronized int initialize(final INativeNuiCallback callback,
                                   String parameters,
                                   final Constants.LogLevel level,
                                   final boolean save_log)
```

-   **参数说明**
    
    | 参数 | 类型 | 说明 |
    | --- | --- | --- |
    | `callback` | `INativeNuiCallback` | 事件和数据回调接口的实现。 |
    | `parameters` | `String` | JSON字符串，包含鉴权、连接和调试参数。参见[连接与控制参数](android-sdk-for-paraformer-real-time-service-9e7815d0b3adcb41.md#57acf5ecc1w8j)。 |
    | `level` | `Constants.LogLevel` | 控制SDK自身日志的打印级别。 |
    | `save_log` | `boolean` | 是否保存本地日志。若为`true`，须在[连接与控制参数](android-sdk-for-paraformer-real-time-service-9e7815d0b3adcb41.md#57acf5ecc1w8j)中通过`debug_path`指定路径，并可通过`max_log_file_size`设置文件大小。 |
    
-   **返回值说明**

<a id="setparams"></a>

<a id="a23e0d85d7ymt"></a>

#### setParams

以JSON格式设置语音识别效果参数。在[startDialog](android-sdk-for-paraformer-real-time-service-9e7815d0b3adcb41.md#7d33691bdb32v)之前调用。

-   **方法签名**

<a id="code-block-4"></a>

```java
public synchronized int setParams(String params)
```

-   **参数说明**
    
    | 参数 | 类型 | 说明 |
    | --- | --- | --- |
    | `params` | `String` | [语音识别效果参数](android-sdk-for-paraformer-real-time-service-9e7815d0b3adcb41.md#d20cce9518kla)。 |
    
-   **返回值说明**

<a id="startdialog"></a>

<a id="7d33691bdb32v"></a>

#### startDialog

开始识别。

-   **方法签名**

<a id="code-block-5"></a>

```java
public synchronized int startDialog(VadMode vad_mode, String dialog_params)
```

-   **参数说明**
    
    <table><thead><tr><th><strong>参数</strong></th><th><strong>类型</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><p><code>vad_mode</code></p></td><td><p><code>VadMode</code></p></td><td><p>VAD模式。固定为<code>VadMode.TYPE_P2T</code>。</p></td></tr><tr><td><p><code>dialog_params</code></p></td><td><p><code>String</code></p></td><td><p>当<a href="android-sdk-for-paraformer-real-time-service-9e7815d0b3adcb41.md#57acf5ecc1w8j">连接与控制参数</a>的<code>apikey</code>参数对应的<a href="../model-api-reference/more-about-models/generate-temporary-api-key.md">临时API Key</a>过期时，可在此处进行更新。</p><p>内容为JSON格式：</p><a id="code-block-6"></a><pre class="language-json"><code>{
      &quot;apikey&quot;: &quot;st-****&quot;
    }
    </code></pre></td></tr></tbody></table>
    
-   **返回值说明**

<a id="stopdialog"></a>

<a id="047417083bahi"></a>

#### stopDialog

结束识别，调用该接口后，服务端将返回最终识别结果并结束任务。

-   **方法签名**

<a id="code-block-7"></a>

```java
public synchronized int stopDialog();
```

-   **返回值说明**

<a id="canceldialog"></a>

<a id="8c464959f9lm9"></a>

#### cancelDialog

立即结束识别，调用该接口后，不等待服务端返回最终识别结果就立即结束任务。

-   **方法签名**

<a id="code-block-8"></a>

```java
public synchronized int cancelDialog();
```

-   **返回值说明**

<a id="release"></a>

<a id="44bf12ed9a4g9"></a>

#### release

释放SDK所有内部资源。此方法调用后，SDK实例将变为不可用状态，如需再次使用，必须重新调用[initialize](android-sdk-for-paraformer-real-time-service-9e7815d0b3adcb41.md#ae6d7dd9cfad3)进行初始化。

-   **方法签名**

<a id="code-block-9"></a>

```java
public synchronized int release();
```

-   **返回值说明**

<a id="getversion"></a>

<a id="36cbf0689bzon"></a>

#### GetVersion

获得当前SDK版本信息。

-   **方法签名**

<a id="code-block-10"></a>

```java
public synchronized String GetVersion();
```

-   **返回值说明**
    
    当前SDK版本信息。
    

<a id="inativenuicallback-监听回调"></a>

<a id="8b030fec74e01"></a>

### INativeNuiCallback：监听回调

<a id="onnuieventcallback-监听事件和语音识别结果"></a>

<a id="163c1ef871tqt"></a>

#### onNuiEventCallback：监听事件和语音识别结果

-   **方法签名**

<a id="code-block-11"></a>

```java
void onNuiEventCallback(NuiEvent event, final int resultCode, final int arg2, KwsResult kwsResult, AsrResult asrResult);
```

-   **参数说明**
    
    | 参数 | 类型 | 说明 |
    | --- | --- | --- |
    | `event` | `NuiEvent` | 回调事件。 |
    | `resultCode` | `int` | 仅在出现 `EVENT_ASR_ERROR` 事件时有效。 |
    | `asrResult` | `AsrResult` | 语音识别结果。 |
    | `kwsResult` | `KwsResult` | 语音唤醒功能。无需关注该参数。 |
    | `arg2` | `int` | 保留参数。 |
    

<a id="onnuiaudiostatechanged-监听音频状态"></a>

<a id="bc71fe2545pfy"></a>

#### onNuiAudioStateChanged：监听音频状态

SDK 通过此回调通知何时应该开始或停止录音。

-   **方法签名**

<a id="code-block-12"></a>

```java
void onNuiAudioStateChanged(AudioState state);
```

-   **AudioState状态说明**
    
    | 状态 | 说明 |
    | --- | --- |
    | `STATE_OPEN` | 交互启动，可以打开录音设备进行录音。 |
    | `STATE_PAUSE` | 交互停止，可以停止录音。 |
    | `STATE_CLOSE` | SDK 实例已释放，可以彻底关闭录音设备。 |
    

<a id="onnuineedaudiodata-填充待识别音频数据"></a>

<a id="12577ebc97awb"></a>

#### onNuiNeedAudioData：填充待识别音频数据

开始识别后，该回调被连续触发，需在其中提供待识别音频数据。

-   **方法签名**

<a id="code-block-13"></a>

```java
int onNuiNeedAudioData(byte[] buffer, int len);
```

-   **参数说明**
    
    | 参数 | 类型 | 说明 |
    | --- | --- | --- |
    | `buffer` | `byte[]` | 填充的音频数据。 |
    | `len` | `int` | 填充的音频数据的字节数。 |
    
-   **返回值说明**
    
    实际填充的字节数。
    

<a id="onnuilogtrackcallback-监听追踪日志"></a>

<a id="9c10968457gc6"></a>

#### onNuiLogTrackCallback：监听追踪日志

此回调用于接收 SDK 内部的详细日志，方便进行问题定位和调试。

<a id="code-block-14"></a>

```java
default void onNuiLogTrackCallback(Constants.LogLevel level, String log)
```

<a id="nuievent-事件类型"></a>

<a id="981ff433acpmr"></a>

### `NuiEvent`：事件类型

| 事件 | 说明 |
| --- | --- |
| EVENT\_TRANSCRIBER\_STARTED | 任务启动成功。 |
| EVENT\_VAD\_START | 任务启动后即触发该事件。不代表检测到人声起点。 |
| EVENT\_VAD\_END | 检测到人声终点。 |
| EVENT\_ASR\_PARTIAL\_RESULT | 语音识别中间结果。 |
| EVENT\_ASR\_ERROR | 语音识别过程中出现错误。 |
| EVENT\_MIC\_ERROR | 因连续2秒未收到任何音频数据而触发。 |
| EVENT\_SENTENCE\_END | 检测到一句话结束，此时会返回一句完整的识别结果。 |
| EVENT\_TRANSCRIBER\_COMPLETE | 语音识别结束。 |
