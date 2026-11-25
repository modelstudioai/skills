# 非实时语音识别（Qwen-Audio-ASR）Android SDK

Qwen-Audio-ASR非实时语音识别Android SDK可将语音转换为文本。

关于支持的音频格式、文件大小限制、时长限制等输入要求，请参见[音频规格](../model-user-guide/model-experience/speech-and-audio/speech-recognition/asr-model.md#asr_audio_spec02)。

<a id="快速开始"></a>

## 快速开始

1.  **获取API Key：**[获取API Key](../model-api-reference/preparations/get-api-key.md)，为安全起见，推荐将API Key配置到环境变量。
2.  **下载SDK并运行示例代码：**
    -   [下载最新SDK整合包](https://help.aliyun.com/zh/model-studio/sdk-selection-and-download)。
    -   解压 ZIP 包。在 `app/libs` 目录中获取 AAR 格式 SDK，并添加到项目依赖。 需要 Android CPP 接入时，使用 ZIP 包内的 `android_libs` 与 `android_include` 获取动态库和头文件。
    -   用 Android Studio 打开工程。示例代码位于`DashFunAsrFlashFileTranscriberActivity.java`，替换 API Key 后体验功能。

<a id="调用步骤"></a>

### 调用步骤

<a id="同步模式"></a>

#### 同步模式

1.  初始化 SDK
    
2.  按业务需求配置相关参数
    
3.  调用 `startFileTranscriber` 发送非实时语音识别请求，并等待结果返回。
    
4.  在`onFileTransEventCallback`接口中监听`EVENT_FILE_TRANS_RESULT` 事件，获取最终识别结果。
    
5.  调用 `release` 释放 SDK 资源
    

<a id="请求参数"></a>

## 请求参数

<a id="连接与控制参数"></a>

<a id="connection-parameters"></a>

### 连接与控制参数

通过在`initialize`接口的`parameters`参数中传入一个JSON字符串来配置。

**参数示例：**以下为 JSON 字符串示例，参数未完整列出。请按实际需求在编码时补充：

<a id="code-block"></a>

```json
{
    "url": "wss://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation",
    "apikey": "st-****",
    "device_id": "my_device_id",
    "service_mode": "1"
}
```

**参数说明**

<table><thead><tr><th><strong>参数</strong></th><th><strong>类型</strong></th><th><strong>是否必须</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><p><code>url</code></p></td><td><p><code>String</code></p></td><td><p>是</p></td><td><p>服务地址：</p><ul><li><code>wss://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation</code></li><li><p>华北2（北京）：<code>wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation</code></p></li><li><p>新加坡：<code>wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation</code></p></li></ul><p>调用时，请将 <code>{WorkspaceId}</code> 替换为真实的 <a href="../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain">Workspace ID</a>。</p></td></tr><tr><td><p><code>apikey</code></p></td><td><p><code>String</code></p></td><td><p>是</p></td><td><p>API Key。</p></td></tr><tr><td><p><code>service_mode</code></p></td><td><p><code>String</code></p></td><td><p>是</p></td><td><p>运行模式。非实时语音识别固定为 <code>&quot;1&quot;</code>。</p></td></tr><tr><td><p><code>device_id</code></p></td><td><p><code>String</code></p></td><td><p>是</p></td><td><p>用于标识终端用户的唯一字符串，可设为应用内用户ID或客户端生成的设备唯一标识符。此ID主要用于日志追踪和问题排查。</p></td></tr><tr><td><p><code>debug_path</code></p></td><td><p><code>String</code></p></td><td><p>否</p></td><td><p>日志文件的存储路径。 此参数仅在调用<code>initialize</code>接口时将<code>save_log</code>设为true时生效。此时必须设置日志文件路径，否则将报错。 本地最多保留两个日志文件。</p></td></tr><tr><td><p><code>max_log_file_size</code></p></td><td><p><code>int</code></p></td><td><p>否</p></td><td><p>设定日志文件的最大字节数。 此参数仅在调用<code>initialize</code>接口时将<code>save_log</code>设为true时生效。 默认值：104857600（100 * 1024 * 1024 字节, 即 100MiB）。</p></td></tr><tr><td><p><code>log_track_level</code></p></td><td><p><code>int</code></p></td><td><p>否</p></td><td><p>控制通过日志回调（<code>onFileTransLogTrackCallback</code>）对外发送的日志内容的过滤级别。 默认值：2。 取值范围：</p><ul><li>0： LOG_LEVEL_VERBOSE</li><li>1： LOG_LEVEL_DEBUG</li><li>2： LOG_LEVEL_INFO</li><li>3： LOG_LEVEL_WARNING</li><li>4： LOG_LEVEL_ERROR</li><li>5： LOG_LEVEL_NONE（表示关闭此功能）</li></ul><div><div><p><strong>说明</strong><code>log_track_level</code>与<code>level</code>（通过<code>initialize</code>接口设置）共同决定最终回调的日志。一条日志的级别数值必须同时大于或等于<code>log_track_level</code>和<code>level</code>的值，才会被回调。例如，<code>log_track_level</code>设为2 (INFO)，<code>level</code>设为3 (WARNING)，则只有WARNING及以上级别（数值&gt;=3）的日志才会被回调。</p></div></div></td></tr></tbody></table>

<a id="语音识别效果参数"></a>

<a id="recognition-parameters"></a>

### 语音识别效果参数

通过`startFileTranscriber`接口配置所有语音识别效果参数。

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
    "model": "qwen-audio-3.0-asr-flash"
  }
}
```

**参数说明**

<table><thead><tr><th><strong>参数</strong></th><th><strong>类型</strong></th><th><strong>是否必须</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><p><code>apikey</code></p></td><td><p><code>string</code></p></td><td><p>否</p></td><td><p>如果连接与控制参数的<code>apikey</code>使用的是<a href="../model-api-reference/more-about-models/generate-temporary-api-key.md">临时API Key</a>，可在此处进行更新，以免超时失效。</p></td></tr><tr><td><p><code>nls_config</code></p></td><td><p><code>object</code></p></td><td><p>是</p></td><td><p>语音识别核心配置对象，包含模型选择、识别效果控制等关键参数。</p></td></tr><tr><td><p><code>nls_config.model</code></p></td><td><p><code>string</code></p></td><td><p>是</p></td><td><p>模型名称。</p></td></tr><tr><td><p><code>nls_config.format</code></p></td><td><p><code>string</code></p></td><td><p>是</p></td><td><p>音频格式。根据实际音频格式填写，支持<code>wav</code>、<code>mp3</code>、<code>opus</code>等。详情请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/asr-model.md#asr_audio_spec02">音频规格</a>。</p></td></tr><tr><td><p><code>nls_config.sample_rate</code></p></td><td><p><code>string</code></p></td><td><p>否</p></td><td><p>音频采样率，单位Hz。例如<code>16000</code>表示16kHz采样率。详情请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/asr-model.md#asr_audio_spec02">音频规格</a>。</p></td></tr><tr><td><p><code>nls_config.vocabulary_id</code></p></td><td><p><code>string</code></p></td><td><p>否</p></td><td><p>预编译热词列表 ID。 需预先调用创建热词列表接口生成，识别时传入该 ID 即可使用列表中的热词。 适用于词汇已知且相对稳定、需要跨请求复用同一词表的场景。 使用方法请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/improve-asr-accuracy.md#hw_precompiled_h3">预编译热词</a>。</p></td></tr><tr><td><p><code>nls_config.instant_vocabulary</code></p></td><td><p><code>object</code></p></td><td><p>否</p></td><td><p>即时热词。</p><p>以键值对形式传入，键为热词文本（<code>string</code>），值为热词权重（<code>integer</code>），无需预先创建热词列表。权重取值范围为 [1, 5] 或 50：取 [1, 5] 时值越大模型越倾向输出该词；取 50 时为超级热词，召回率大幅提升，但超级热词数量最多不超过 50 个。</p><p>适用于临时性、会话级别的热词优化。</p><p>与预编译热词同时配置时，系统会合并两类热词；合并后超过 2000 个时，随机选择 2000 个使用。使用方法请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/improve-asr-accuracy.md#hw_instant_h3">即时热词</a>。</p><a id="code-block-3"></a><pre class="language-json"><code>{
  &quot;张三&quot;: 5,
  &quot;李四&quot;: 5
}
</code></pre></td></tr><tr><td><p><code>nls_config.language_hints</code></p></td><td><p><code>array[string]</code></p></td><td><p>否</p></td><td><p>设置待识别语言代码。如果无法提前确定语种，可不设置，模型会自动识别语种。最多支持设置 4 个值，超出时仅前 4 个生效。</p><p>指定语种代码可提升识别准确率。</p><a id="accordion-支持的语言代码"></a><section><p>支持的语言代码</p><div><ul><li>zh: 中文</li><li>en: 英文</li><li>ja: 日语</li><li>ko: 韩语</li><li>vi: 越南语</li><li>th: 泰语</li><li>id: 印尼语</li><li>ms: 马来语</li><li>tl: 菲律宾语</li><li>hi: 印地语</li><li>ar: 阿拉伯语</li><li>fr: 法语</li><li>de: 德语</li><li>es: 西班牙语</li><li>pt: 葡萄牙语</li><li>ru: 俄语</li><li>it: 意大利语</li><li>nl: 荷兰语</li><li>sv: 瑞典语</li><li>da: 丹麦语</li><li>fi: 芬兰语</li><li>no: 挪威语</li><li>el: 希腊语</li><li>pl: 波兰语</li><li>cs: 捷克语</li><li>hu: 匈牙利语</li><li>ro: 罗马尼亚语</li><li>bg: 保加利亚语</li><li>hr: 克罗地亚语</li><li>sk: 斯洛伐克语</li></ul><p><code>qwen-audio-3.1-asr-flash</code> 还支持以下语言代码：</p><ul><li>tr: 土耳其语</li><li>fa: 波斯语</li><li>mr: 马拉地语</li><li>ml: 马拉雅拉姆语</li><li>ne: 尼泊尔语</li><li>ky: 吉尔吉斯语</li><li>az: 阿塞拜疆语</li><li>ka: 格鲁吉亚语</li><li>hy: 亚美尼亚语</li><li>sl: 斯洛文尼亚语</li><li>sq: 阿尔巴尼亚语</li><li>et: 爱沙尼亚语</li><li>lv: 拉脱维亚语</li><li>lt: 立陶宛语</li><li>ca: 加泰罗尼亚语</li><li>eu: 巴斯克语</li><li>gl: 加利西亚语</li><li>or: 奥里亚语</li><li>dv: 迪维希语</li><li>as: 阿萨姆语</li><li>kmr: 北库尔德语</li><li>tig: 提格雷语</li><li>fy: 西弗里西亚语</li><li>ba: 巴什基尔语</li><li>be: 白俄罗斯语</li><li>tt: 鞑靼语</li><li>ia: 国际语</li><li>mhr: 草原马里语</li><li>tok: 道本语</li></ul></div></section></td></tr><tr><td><p><code>messages</code></p></td><td><p><code>array[object]</code></p></td><td><p>是</p></td><td><p>消息列表。包含当前待识别的音频，以及可选的对话上下文（用于提升识别效果）。</p><strong>详见如下说明。</strong></td></tr></tbody></table>

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

<table><thead><tr><th><strong>参数</strong></th><th><strong>类型</strong></th><th><strong>是否必须</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><p><code>type</code></p></td><td><p><code>string</code></p></td><td><p>是</p></td><td><p>内容类型。每个请求至少需要一条<code>input_audio</code>类型的消息。取值范围：</p><ul><li><p><code>input_audio</code>（必选）：当前待识别的音频输入（role为user），需同时传入<code>input_audio</code>对象。</p></li><li><p><code>input_text</code>（可选，上下文）：前几轮用户语音的识别结果或领域相关的词表（role为user），需同时传入<code>text</code>字段。</p></li><li><p><code>text</code>（可选，上下文）：前几轮大语言模型的回复内容（role为assistant），需同时传入<code>text</code>字段。</p></li></ul></td></tr><tr><td><p><code>input_audio</code></p></td><td><p><code>object</code></p></td><td><p>否</p></td><td><p>当<code>type</code>为<code>input_audio</code>时必填。</p></td></tr><tr><td><p><code>input_audio.data</code></p></td><td><p><code>string</code></p></td><td><p>是</p></td><td><p>待识别音频数据。关于支持的音频格式、文件大小限制、时长限制等输入要求，请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/asr-model.md#asr_audio_spec02">音频规格</a>。支持以下两种方式：</p><ul><li><p><strong>音频文件URL</strong>：直接传入可公开访问的音频文件地址。</p></li><li><p><strong>Base64 Data URI</strong>：采用Data URI格式传入Base64编码的音频数据，值由<code>data:{MIME_TYPE};base64,</code>前缀与Base64编码的音频数据拼接而成。支持的MIME类型包括<code>audio/wav</code>、<code>audio/mp3</code>等。</p></li></ul><p>示例（URL方式）：<code><a href="https://example.com/audio/sample.wav">https://example.com/audio/sample.wav</a></code></p><p>示例（Base64方式）：<code>data:audio/wav;base64,{BASE64_ENCODED_DATA}</code></p></td></tr><tr><td><p><code>text</code></p></td><td><p><code>string</code></p></td><td><p>否</p></td><td><p>当<code>type</code>为<code>input_text</code>时，填入前几轮用户语音的识别结果或领域相关的词表；当<code>type</code>为<code>text</code>时，填入前几轮大语言模型的回复内容。文本按字符数计算，每个字符计为 1。每轮上下文中所有消息的 <code>text</code> 字段长度之和不超过 400 个字符，超出部分从末尾截断。</p></td></tr></tbody></table>

<a id="关键接口"></a>

## 关键接口

<a id="nativenui"></a>

### NativeNui

<a id="initialize"></a>

<a id="initialize-2"></a>

#### initialize

初始化语音识别SDK实例。SDK为单例模式，在调用`release`前禁止重复初始化。

此接口会引起阻塞，应在非UI线程调用。

**方法签名**

<a id="code-block-4"></a>

```java
public synchronized int initialize(final INativeFileTransCallback callback,
                                   String parameters,
                                   final Constants.LogLevel level,
                                   final boolean save_log)
```

**参数说明**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `callback` | `INativeFileTransCallback` | 事件和数据回调接口的实现。 |
| `parameters` | `String` | JSON字符串，包含鉴权、连接和调试参数。参见连接与控制参数。 |
| `level` | `Constants.LogLevel` | 控制SDK自身日志的打印级别。 |
| `save_log` | `boolean` | 是否保存本地日志。若为`true`，须在连接与控制参数中通过`debug_path`指定路径，并可通过`max_log_file_size`设置文件大小。 |

<a id="setparams"></a>

<a id="setparams-2"></a>

#### setParams

此接口用于独立设置或更新 `nls_config` 参数。如果所有参数都在`startFileTranscriber`中一次性提供，则无需调用此方法。

**方法签名**

<a id="code-block-5"></a>

```java
public synchronized int setParams(String params);
```

**参数说明**

<table><thead><tr><th><strong>参数</strong></th><th><strong>类型</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><p><code>params</code></p></td><td><p><code>String</code></p></td><td><p>语音识别效果参数中的<code>nls_config</code>和messages参数。</p><p>示例：</p><a id="code-block-6"></a><pre class="language-json"><code>{
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
    &quot;model&quot;: &quot;qwen-audio-3.0-asr-flash&quot;
  }
}
</code></pre></td></tr></tbody></table>

<a id="startfiletranscriber"></a>

<a id="startfiletranscriber-2"></a>

#### startFileTranscriber

开始识别。

**方法签名**

<a id="code-block-7"></a>

```java
public synchronized int startFileTranscriber(String params, byte[ ] task_id)
```

**参数说明**

<table><thead><tr><th><strong>参数</strong></th><th><strong>类型</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><p><code>params</code></p></td><td><p><code>String</code></p></td><td><p>语音识别效果参数。 示例：</p><a id="code-block-8"></a><pre class="language-json"><code>{
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
    &quot;model&quot;: &quot;qwen-audio-3.0-asr-flash&quot;
  }
}
</code></pre></td></tr><tr><td><p><code>task_id</code></p></td><td><p><code>byte[ ]</code></p></td><td><p>可不关注，可填null</p></td></tr></tbody></table>

<a id="queryfiletranscriber"></a>

#### queryFileTranscriber

此非实时语音识别功能仅支持同步请求，无需关注此接口。

<a id="cancelfiletranscriber"></a>

#### cancelFileTranscriber

立即取消当前任务。

**方法签名**

<a id="code-block-9"></a>

```java
public synchronized int cancelFileTranscriber(String task_id)
```

**参数说明**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `task_id` | `String` | 待取消的任务ID。通过EVENT\_FILE\_TRANS\_UPLOADED获取。 |

<a id="release"></a>

<a id="release-2"></a>

#### release

释放SDK所有内部资源。此方法调用后，SDK实例将变为不可用状态，如需再次使用，必须重新调用`initialize`进行初始化。

**方法签名**

<a id="code-block-10"></a>

```java
public synchronized int release();
```

<a id="getversion"></a>

#### GetVersion

获得当前SDK版本信息。

**方法签名**

<a id="code-block-11"></a>

```java
public synchronized String GetVersion();
```

**返回值说明**

当前SDK版本信息。

<a id="inativefiletranscallback-监听回调"></a>

<a id="file-trans-callback"></a>

### INativeFileTransCallback：监听回调

<a id="onfiletranseventcallback-监听事件和语音识别结果"></a>

#### onFileTransEventCallback：监听事件和语音识别结果

**方法签名**

<a id="code-block-12"></a>

```java
void onFileTransEventCallback(NuiEvent event, final int resultCode, final int arg2, AsrResult asrResult, String taskId);
```

**参数说明**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `event` | `NuiEvent` | 回调事件。 |
| `resultCode` | `int` | 仅在出现 `EVENT_ASR_ERROR` 事件时有效。 |
| `asrResult` | `AsrResult` | 语音识别结果。 |
| `taskId` | `String` | 任务ID。 |
| `arg2` | `int` | 保留参数。 |

<a id="onfiletranslogtrackcallback-监听追踪日志"></a>

<a id="log-callback"></a>

#### onFileTransLogTrackCallback：监听追踪日志

此回调用于接收 SDK 内部的详细日志，方便进行问题定位和调试。

<a id="code-block-13"></a>

```java
default void onFileTransLogTrackCallback(Constants.LogLevel level, String log)
```

<a id="事件类型"></a>

### 事件类型

| 事件 | 说明 |
| --- | --- |
| `EVENT_FILE_TRANS_CONNECTED` | 连接服务成功。 |
| `EVENT_FILE_TRANS_UPLOADED` | 上传待识别音频文件成功，此时可获得当前任务的task\_id。 |
| `EVENT_FILE_TRANS_RESULT` | 识别最终结果。 |
| `EVENT_ASR_ERROR` | 语音识别过程中出现错误。 |
