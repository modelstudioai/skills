# Qwen-Audio-ASR-Filetrans非实时语音识别iOS SDK

本文档提供了Qwen-Audio-ASR-Filetrans非实时语音识别iOS SDK的详细使用指南，帮助您将语音转换为文本。

关于支持的音频格式、文件大小限制、时长限制等输入要求，请参见[音频规格](../model-user-guide/model-experience/speech-and-audio/speech-recognition/asr-model.md#asr_audio_spec02)。

<a id="快速开始"></a>

<a id="a7fed77afbder"></a>

## 快速开始

1.  **获取API Key：**[获取API Key](../model-api-reference/preparations/get-api-key.md)
    
2.  **下载SDK并运行示例代码：**
    -   [下载最新SDK整合包](https://help.aliyun.com/zh/model-studio/sdk-selection-and-download)。
    -   解压 ZIP 包，将其中的 nuisdk.framework 添加到工程。
    -   在 Build Phases → Link Binary With Libraries 中添加 `nuisdk.xcframework`。
    -   在 General → Frameworks, Libraries, and Embedded Content 中将 `nuisdk.xcframework` 设置为 Embed & Sign。
    -   用 Xcode 打开示例工程。示例代码位于`DashFunAsrFileTranscriberViewController.m`，替换 API Key 后体验功能。

<a id="调用步骤"></a>

<a id="0701a2d0b75vm"></a>

### 调用步骤

<a id="sec-tabs"></a>

<a id="同步模式"></a>

<a id="同步模式-h4"></a>

#### 同步模式

1.  初始化 SDK
2.  按业务需求配置相关参数
3.  当 `async_request` 设为 `false` 时，调用 `nui_file_trans_start` 发送非实时语音识别请求，并等待结果返回。
4.  在`onFileTransEventCallback`接口中监听`EVENT_FILE_TRANS_RESULT` 事件，获取最终识别结果
5.  调用 `nui_release` 释放 SDK 资源

<a id="异步模式"></a>

<a id="异步模式-h4"></a>

#### 异步模式

1.  初始化 SDK
2.  按业务需求配置相关参数
3.  当 `async_request` 设为 `true` 时，调用 `nui_file_trans_start` 发送非实时语音识别请求。
4.  调用 `nui_file_trans_query` 主动查询识别进度/结果
5.  在`onFileTransEventCallback`接口中监听`EVENT_FILE_TRANS_QUERY_RESULT`事件，获取当前查询结果
6.  在`onFileTransEventCallback`接口中监听 `EVENT_FILE_TRANS_RESULT` 事件，获取最终识别结果
7.  调用 `nui_release` 释放 SDK 资源

<a id="请求参数"></a>

<a id="a96bfa6340jdd"></a>

## 请求参数

<a id="连接与控制参数"></a>

<a id="57acf5ecc1w8j"></a>

### 连接与控制参数

通过在`nui_initialize`接口的`parameters`参数中传入一个JSON字符串来配置。

**参数示例**

以下为 JSON 字符串示例，参数未完整列出。请按实际需求在编码时补充：

<a id="code-block"></a>

```json
{
    "url": "wss://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription",
    "apikey": "st-****",
    "device_id": "my_device_id",
    "service_mode": "1"
}
```

**参数说明**

<table><thead><tr><th><strong>参数</strong></th><th><strong>类型</strong></th><th><strong>是否必须</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><p><code>url</code></p></td><td><p><code>String</code></p></td><td><p>是</p></td><td><p>服务地址：</p><ul><li><code>wss://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription</code></li><li><p>华北2（北京）：<code>wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/asr/transcription</code></p></li><li><p>新加坡：<code>wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/audio/asr/transcription</code></p></li></ul><p>调用时，请将 <code>{WorkspaceId}</code> 替换为真实的 <a href="../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain">Workspace ID</a>。</p></td></tr><tr><td><p><code>apikey</code></p></td><td><p><code>String</code></p></td><td><p>是</p></td><td><p>API Key。</p></td></tr><tr><td><p><code>service_mode</code></p></td><td><p><code>String</code></p></td><td><p>是</p></td><td><p>运行模式。非实时语音识别固定为 <code>&quot;1&quot;</code>。</p></td></tr><tr><td><p><code>device_id</code></p></td><td><p><code>String</code></p></td><td><p>是</p></td><td><p>用于标识终端用户的唯一字符串，可设为应用内用户ID或客户端生成的设备唯一标识符。此ID主要用于日志追踪和问题排查。</p></td></tr><tr><td><p><code>debug_path</code></p></td><td><p><code>String</code></p></td><td><p>否</p></td><td><p>日志文件的存储路径。</p><p>此参数仅在调用<code>nui_initialize</code>接口时将<code>save_log</code>设为<code>YES</code>时生效。此时必须设置日志文件路径，否则将报错。</p><p>本地最多保留两个日志文件。</p></td></tr><tr><td><p><code>max_log_file_size</code></p></td><td><p><code>int</code></p></td><td><p>否</p></td><td><p>设定日志文件的最大字节数。</p><p>此参数仅在调用<code>nui_initialize</code>接口时将<code>save_log</code>设为<code>YES</code>时生效。</p><p>默认值：104857600（100 * 1024 * 1024 字节, 即 100MiB）。</p></td></tr><tr><td><p><code>log_track_level</code></p></td><td><p><code>int</code></p></td><td><p>否</p></td><td><p>控制通过日志回调（<code>onFileTransLogTrackCallback</code>）对外发送的日志内容的过滤级别。</p><p>默认值：2。</p><p>取值范围：</p><ul><li><p>0：LOG_LEVEL_VERBOSE</p></li><li><p>1：LOG_LEVEL_DEBUG</p></li><li><p>2：LOG_LEVEL_INFO</p></li><li><p>3：LOG_LEVEL_WARNING</p></li><li><p>4：LOG_LEVEL_ERROR</p></li><li><p>5：LOG_LEVEL_NONE（表示关闭此功能）</p></li></ul><p>注意：<code>log_track_level</code>与<code>level</code>（通过<code>nui_initialize</code>接口设置）共同决定最终回调的日志。一条日志的级别数值必须同时大于或等于<code>log_track_level</code>和<code>level</code>的值，才会被回调。例如，<code>log_track_level</code>设为2 (INFO)，<code>level</code>设为3 (WARNING)，则只有WARNING及以上级别（数值&gt;=3）的日志才会被回调。</p></td></tr></tbody></table>

<a id="语音识别效果参数"></a>

<a id="d20cce9518kla"></a>

### 语音识别效果参数

通过`nui_file_trans_start`接口配置所有语音识别效果参数。

**参数示例**

以下为 JSON 字符串示例，参数未完整列出。请按实际需求在编码时补充：

<a id="code-block-2"></a>

```json
{
    "apikey": "st-****",
    "file_urls": [
        "{YOUR_AUDIO_URL}"
    ],
    "async_request": false,
    "nls_config": {
        "model":"qwen-audio-3.0-asr-flash-filetrans",
        "diarization_enabled": false
    }
}
```

**参数说明**

<table><thead><tr><th><strong>参数</strong></th><th><strong>类型</strong></th><th><strong>是否必须</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><p><code>file_urls</code></p></td><td><p><code>array[string]</code></p></td><td><p>是</p></td><td><p>音视频文件转写的URL列表，支持HTTP / HTTPS协议，单次请求仅支持1个URL。关于支持的音频格式、文件大小限制、时长限制等输入要求，请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/asr-model.md#asr_audio_spec02">音频规格</a>。</p><p>若录音文件存储在阿里云OSS，使用RESTful API方式支持使用以<code>oss://</code>为前缀的临时 URL，使用SDK方式不支持使用以 oss://为前缀的临时 URL。</p><div><div><p><strong>重要</strong></p><ul><li><p>临时 URL 有效期48小时，过期后无法使用，<strong>请勿用于生产环境。</strong></p></li><li><p>文件上传凭证接口限流为 100 QPS 且不支持扩容，<strong>请勿用于生产环境、高并发及压测场景。</strong></p></li><li><p>生产环境建议使用<a href="https://help.aliyun.com/zh/oss/user-guide/what-is-oss">阿里云OSS</a> 等稳定存储，确保文件长期可用并规避限流问题。</p></li><li><p>录音文件URL设置成OSS临时公网访问不通该如何处理？请求头中将<code>X-DashScope-OssResourceResolve</code>设为<code>enable</code>（不推荐该方式）。</p><p>SDK不支持对请求头进行配置。</p></li></ul></div></div></td></tr><tr><td><p><code>async_request</code></p></td><td><p><code>boolean</code></p></td><td><p>否</p></td><td><p>语音识别是否为异步请求。</p><p>默认值：<code>false</code>。</p><p>取值范围：</p><ul><li>true：异步请求</li><li>false：同步请求</li></ul></td></tr><tr><td><p><code>apikey</code></p></td><td><p><code>string</code></p></td><td><p>否</p></td><td><p>如果连接与控制参数的<code>apikey</code>使用的是<a href="../model-api-reference/more-about-models/generate-temporary-api-key.md">临时API Key</a>，可在此处进行更新，以免超时失效。</p></td></tr><tr><td><p><code>nls_config</code></p></td><td><p><code>object</code></p></td><td><p>是</p></td><td><p>语音识别核心配置对象，包含模型选择、识别效果控制等关键参数。</p></td></tr><tr><td><p><code>nls_config.model</code></p></td><td><p><code>string</code></p></td><td><p>是</p></td><td><p>模型名称。</p></td></tr><tr><td><p><code>nls_config.special_word_filter</code></p></td><td><p><code>object</code></p></td><td><p>否</p></td><td><p>指定在语音识别过程中需要处理的敏感词，并支持对不同敏感词设置不同的处理方式。详情请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/non-realtime-speech-recognition-user-guide.md#nrt03_sensitive_h3">敏感词过滤</a>。</p></td></tr><tr><td><p><code>nls_config.channel_id</code></p></td><td><p><code>array[integer]</code></p></td><td><p>否</p></td><td><p>指定在多音轨音频文件中需要识别的音轨索引，索引从 0 开始。例如，[0] 表示识别第一个音轨，[0, 1] 表示同时识别第一和第二个音轨。如果省略此参数，则默认处理第一个音轨。</p><div><div><p><strong>重要</strong>指定的每一个音轨都将独立计费。例如，为单个文件请求 [0, 1] 会产生两笔独立的费用。</p></div></div><p>默认值：[0]。</p></td></tr><tr><td><p><code>nls_config.diarization_enabled</code></p></td><td><p><code>boolean</code></p></td><td><p>否</p></td><td><p>是否启用说话人分离，默认关闭。</p><p>仅适用于单声道音频，多声道音频不支持说话人分离。</p><p>启用该功能后，识别结果中将显示<code>speaker_id</code>字段，用于区分不同说话人。</p><div><div><p><strong>说明</strong>如果启用说话人分离功能，建议音频时长不超过2小时，否则可能导致识别失败或超时。</p></div></div><p>默认值：false。</p><p>有关<code>speaker_id</code>的示例，请参见<a href="qwen-audio-asr-filetrans-python-sdk-e244defb9b1288ee.md#a9021178ccl7s">识别结果说明</a>。</p></td></tr><tr><td><p><code>nls_config.speaker_count</code></p></td><td><p><code>integer</code></p></td><td><p>否</p></td><td><div><div><p><strong>重要</strong>仅在开启说话人分离功能（<code>diarization_enabled</code>设置为<code>true</code>）时生效。</p></div></div><p>说话人数量参考值。取值范围为2至100的整数（包含2和100）。</p><p>默认自动判断说话人数量，如果配置此项，只能辅助算法尽量输出指定人数，无法保证一定会输出此人数。</p><p>无默认值。</p></td></tr><tr><td><p><code>nls_config.vocabulary_id</code></p></td><td><p><code>string</code></p></td><td><p>否</p></td><td><p>预编译热词列表 ID。</p><p>需预先调用创建热词列表接口生成，识别时传入该 ID 即可使用列表中的热词。</p><p>适用于词汇已知且相对稳定、需要跨请求复用同一词表的场景。</p><p>使用方法请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/improve-asr-accuracy.md#hw_precompiled_h3">预编译热词</a>。</p></td></tr><tr><td><p><code>nls_config.input_context</code></p></td><td><p><code>array</code></p></td><td><p>否</p></td><td><p>消息列表，包含用于提升识别效果的可选对话上下文。</p><div><div><p><strong>重要</strong>上下文功能用于提升专有词汇的识别准确率，使用方法请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/improve-asr-accuracy.md#ctx_enhance_h2">上下文增强</a>。</p><p>上下文消息（<code>input_text</code> 和 <code>text</code> 类型）各最多 5 条，超出时保留最近的 5 条。每轮上下文文本总长度（<code>user</code> 和 <code>assistant</code> 的 <code>text</code> 字段长度之和）不超过 400 个字符，每个字符计为 1，超出部分从末尾截断。</p></div></div><div><div><p><strong>重要</strong>携带上下文时，<code>messages</code> 中的消息必须按对话轮次排列，每轮中 <code>user</code>（<code>input_text</code> 类型）必须在对应的 <code>assistant</code>（<code>text</code> 类型）之前；包含 <code>input_audio</code> 的 <code>user</code> 消息必须放在 <code>messages</code> 数组的最后。</p></div></div><a id="code-block-3"></a><pre class="language-json"><code>[
  {
    &quot;role&quot;: &quot;user&quot;,
    &quot;content&quot;: [
      {
        &quot;type&quot;: &quot;input_text&quot;,
        &quot;text&quot;: &quot;你好啊，我是通义千问，有什么可以帮助你的？&quot;
      }
    ]
  }
]
</code></pre></td></tr><tr><td><p><code>nls_config.instant_vocabulary</code></p></td><td><p><code>object</code></p></td><td><p>否</p></td><td><p>即时热词，以键值对形式传入：键为热词文本（<code>string</code>），值为热词权重（<code>integer</code>），无需预先创建热词列表。适用于临时性、会话级别的热词优化。</p><p>权重取值范围为 1 至 5 或 50。取 1 至 5 时，值越大，模型越倾向于输出该词；取 50 时为超级热词，召回率大幅提升，但超级热词最多不超过 50 个。</p><p>与预编译热词同时配置时，系统会合并两类热词；合并后超过 2000 个时，随机选择 2000 个使用。使用方法请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/improve-asr-accuracy.md#hw_instant_h3">即时热词</a>。</p><div><div><p><strong>重要</strong>即时热词的适用模型及限制请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/improve-asr-accuracy.md#hw_instant_h3">即时热词</a>。</p></div></div><a id="code-block-4"></a><pre class="language-json"><code>{
  &quot;张三&quot;: 5,
  &quot;李四&quot;: 5
}
</code></pre></td></tr><tr><td><p><code>nls_config.language_hints</code></p></td><td><p><code>array[string]</code></p></td><td><p>否</p></td><td><p>设置待识别语言代码。如果无法提前确定语种，可不设置，模型会自动识别语种。</p><p>最多支持设置 4 个值，超出时仅前 4 个生效。</p><a id="accordion-点击查看支持的语言代码"></a><section><p>点击查看支持的语言代码</p><div><ul><li>zh: 中文</li><li>en: 英文</li><li>ja: 日语</li><li>ko：韩语</li><li>vi：越南语</li><li>th：泰语</li><li>id：印尼语</li><li>ms：马来语</li><li>tl：菲律宾语</li><li>hi：印地语</li><li>ar：阿拉伯语</li><li>fr：法语</li><li>de：德语</li><li>es：西班牙语</li><li>pt：葡萄牙语</li><li>ru：俄语</li><li>it：意大利语</li><li>nl：荷兰语</li><li>sv：瑞典语</li><li>da：丹麦语</li><li>fi：芬兰语</li><li>no：挪威语</li><li>el：希腊语</li><li>pl：波兰语</li><li>cs：捷克语</li><li>hu：匈牙利语</li><li>ro：罗马尼亚语</li><li>bg：保加利亚语</li><li>hr：克罗地亚语</li><li>sk：斯洛伐克语</li></ul></div></section></td></tr></tbody></table>

<a id="关键接口"></a>

<a id="737b46fda6cbf"></a>

## 关键接口

<a id="neonui"></a>

<a id="4bed3999d9kx0"></a>

### NeoNui

<a id="nui-initialize"></a>

<a id="05eab5125e2pm"></a>

#### nui\_initialize

初始化语音识别SDK实例。SDK为单例模式，在调用 `nui_release` 前禁止重复初始化。

**方法签名**

<a id="code-block-5"></a>

```text
-(NuiResultCode) nui_initialize:(const char *)parameters
                       logLevel:(NuiSdkLogLevel)level
                        saveLog:(BOOL)save_log;
```

**参数说明**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `parameters` | `char*` | JSON字符串，包含鉴权、连接和调试参数。参见连接与控制参数。 |
| `level` | `NuiSdkLogLevel` | 控制SDK自身日志的打印级别。 |
| `save_log` | `BOOL` | 是否保存本地日志。若为`YES`，须在连接与控制参数通过`debug_path`指定路径，并可通过`max_log_file_size`设置文件大小。 |

<a id="nui-set-params"></a>

<a id="763672f3f8dgw"></a>

#### nui\_set\_params

此接口用于独立设置或更新 `nls_config` 参数。如果所有参数都在`nui_file_trans_start`中一次性提供，则无需调用此方法。

**方法签名**

<a id="code-block-6"></a>

```text
-(NuiResultCode) nui_set_params:(const char *)params;
```

**参数说明**

<table><thead><tr><th><strong>参数</strong></th><th><strong>类型</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><p><code>params</code></p></td><td><p><code>char*</code></p></td><td><p>语音识别效果参数中的<code>nls_config</code>参数，<code>nls_config</code>之外的参数不支持通过该方法进行设置。</p><p>示例：</p><a id="code-block-7"></a><pre class="language-json"><code>{
    &quot;nls_config&quot;: {
        &quot;model&quot;:&quot;qwen-audio-3.0-asr-flash-filetrans&quot;,
        &quot;diarization_enabled&quot;: false
    }
}
</code></pre></td></tr></tbody></table>

<a id="nui-file-trans-start"></a>

<a id="8fe6ea298apzu"></a>

#### nui\_file\_trans\_start

开始识别。

**方法签名**

<a id="code-block-8"></a>

```text
-(NuiResultCode) nui_file_trans_start:(const char *)params
                               taskId:(char *)task_id;
```

**参数说明**

<table><thead><tr><th><strong>参数</strong></th><th><strong>类型</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><p><code>params</code></p></td><td><p><code>char*</code></p></td><td><p>语音识别效果参数。</p><p>示例：</p><a id="code-block-9"></a><pre class="language-json"><code>{
    &quot;file_urls&quot;: [
        &quot;{YOUR_AUDIO_URL}&quot;
    ],
    &quot;async_request&quot;: false,
    &quot;nls_config&quot;: {
        &quot;model&quot;:&quot;qwen-audio-3.0-asr-flash-filetrans&quot;,
        &quot;diarization_enabled&quot;: false
    }
}
</code></pre></td></tr><tr><td><p><code>task_id</code></p></td><td><p><code>char*</code></p></td><td><p>任务ID，SDK内部生成随机字符串，在此接口调用成功后可获得task_id。</p></td></tr></tbody></table>

<a id="nui-file-trans-query"></a>

<a id="d894d1c6f41ke"></a>

#### nui\_file\_trans\_query

此接口用于主动查询一个异步任务的当前状态和结果。调用成功后，结果将通过`onFileTransEventCallback`回调中的 `EVENT_FILE_TRANS_QUERY_RESULT` 事件返回。

> **说明**
>
> 此处传入的 `task_id` 从 `EVENT_FILE_TRANS_UPLOADED` 事件中获取。

**方法签名**

<a id="code-block-10"></a>

```text
-(NuiResultCode) nui_file_trans_query:(const char *)task_id;
```

**参数说明**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `task_id` | `char*` | 待查询的任务 ID，从 `EVENT_FILE_TRANS_UPLOADED` 事件中获取。 |

<a id="nui-file-trans-cancel"></a>

<a id="156934a01bzjc"></a>

#### nui\_file\_trans\_cancel

立即取消当前任务。

**方法签名**

<a id="code-block-11"></a>

```text
-(NuiResultCode) nui_file_trans_cancel:(const char *)task_id;
```

**参数说明**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `task_id` | `char*` | 待取消的任务 ID，从 `EVENT_FILE_TRANS_UPLOADED` 事件中获取。 |

<a id="nui-release"></a>

<a id="6c2931e9ae3eq"></a>

#### nui\_release

释放SDK所有内部资源，并强制终止所有正在进行的任务。此方法调用后，SDK实例将变为不可用状态，如需再次使用，必须重新调用 `nui_initialize` 进行初始化。

**方法签名**

<a id="code-block-12"></a>

```text
-(NuiResultCode) nui_release;
```

<a id="nui-get-version"></a>

<a id="d691f902dfmyg"></a>

#### nui\_get\_version

获得当前SDK版本信息。

**方法签名**

<a id="code-block-13"></a>

```text
-(const char*) nui_get_version;
```

**返回值说明**

当前SDK版本信息。

<a id="neonuisdkdelegate-监听回调"></a>

<a id="8b030fec74e01"></a>

### NeoNuiSdkDelegate：监听回调

<a id="onfiletranseventcallback-监听事件和语音识别结果"></a>

<a id="163c1ef871tqt"></a>

#### onFileTransEventCallback：监听事件和语音识别结果

**方法签名**

<a id="code-block-14"></a>

```text
-(void) onFileTransEventCallback:(NuiCallbackEvent)nuiEvent
                       asrResult:(const char *)asr_result
                          taskId:(const char *)task_id
                        ifFinish:(BOOL)finish
                         retCode:(int)code;
```

**参数说明**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `nuiEvent` | `NuiCallbackEvent` | 回调事件。 |
| `asr_result` | `char*` | 语音识别结果。 |
| `task_id` | `char*` | 任务ID。 |
| `finish` | `BOOL` | 本轮识别是否结束标志。 |
| `code` | `int` | 仅在出现 `EVENT_ASR_ERROR` 事件时有效。 |

<a id="onfiletranslogtrackcallback-监听追踪日志"></a>

<a id="9c10968457gc6"></a>

#### onFileTransLogTrackCallback：监听追踪日志

此回调用于接收 SDK 内部的详细日志，方便进行问题定位和调试。

<a id="code-block-15"></a>

```text
-(void)onFileTransLogTrackCallback:(NuiSdkLogLevel)level
                        logMessage:(const char *)log;
```

<a id="nuicallbackevent-事件类型"></a>

<a id="981ff433acpmr"></a>

### NuiCallbackEvent：事件类型

| 事件 | 说明 |
| --- | --- |
| `EVENT_FILE_TRANS_CONNECTED` | 连接服务成功。 |
| `EVENT_FILE_TRANS_UPLOADED` | 上传待识别音频文件成功，此时可获得当前任务的 `task_id`。 |
| `EVENT_FILE_TRANS_QUERY_RESULT` | 查询任务结果。 |
| `EVENT_FILE_TRANS_RESULT` | 识别最终结果。 |
| `EVENT_ASR_ERROR` | 语音识别过程中出现错误。 |
