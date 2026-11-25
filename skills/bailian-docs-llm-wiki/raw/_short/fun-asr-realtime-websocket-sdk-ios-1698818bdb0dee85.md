# Fun-ASR-Realtime iOS SDK

<a id="前提条件"></a>

## 前提条件

1.  [获取与配置 API Key](../model-api-reference/preparations/get-api-key.md)。移动端应用请勿硬编码长期 API Key。建议由应用服务端[生成临时 API Key](../model-api-reference/more-about-models/generate-temporary-api-key.md)，再下发给客户端。

<a id="安装-sdk"></a>

### 安装 SDK

-   [下载最新SDK整合包](https://help.aliyun.com/zh/model-studio/sdk-selection-and-download)。
-   解压 ZIP 包，将其中的 nuisdk.xcframework 添加到工程。
-   在 Build Phases → Link Binary With Libraries 中添加 nuisdk.xcframework。
-   在 General → Frameworks, Libraries, and Embedded Content 中将 nuisdk.xcframework 设置为 Embed & Sign。

<a id="快速开始"></a>

<a id="model-qwen-audio-asr-streaming-a7fed77afbder"></a>

<a id="shared-1"></a>

## 快速开始

用 Xcode 打开示例工程。示例代码位于`DashFunAsrSpeechTranscriberViewController.m`，替换 API Key 后体验功能。

在示例中使用模型 `fun-asr-realtime`。

<a id="model-qwen-audio-asr-message-a7fed77afbder"></a>

<a id="model-fun-asr-realtime-a7fed77afbder"></a>

<a id="调用步骤"></a>

<a id="model-qwen-audio-asr-streaming-bccc719ce3r6a"></a>

<a id="shared-4"></a>

<a id="model-qwen-audio-asr-message-bccc719ce3r6a"></a>

<a id="调用步骤-2"></a>

### 调用步骤

<a id="model-fun-asr-realtime-bccc719ce3r6a"></a>

1.  初始化 SDK
2.  按业务需求设置参数：通过`nui_initialize`接口设置连接与控制参数；通过`nui_set_params`接口设置语音识别效果参数。
3.  调用`nui_dialog_start`启动识别流程。
4.  在`onNuiAudioStateChanged`回调中，根据音频状态开启录音设备。
5.  在`onNuiNeedAudioData`回调中持续提供录音数据，或者通过`nui_update_audio_data`持续推送录音数据。
6.  在`onNuiEventCallback`回调中监听事件并获取语音识别结果。
7.  调用`nui_dialog_cancel`停止识别，并通过监听EVENT\_TRANSCRIBER\_COMPLETE事件确认识别已结束。
8.  当识别功能不再使用时，调用`nui_release`接口释放 SDK 资源。

**Qwen-Audio-ASR-Message · 接口参考**

[nui\_initialize](qwen-asr-message-websocket-sdk-ios-fb447b88c464d9d4.md#model-qwen-audio-asr-message-05eab5125e2pm)、[连接与控制参数](qwen-asr-message-websocket-sdk-ios-fb447b88c464d9d4.md#model-qwen-audio-asr-message-57acf5ecc1w8j)、[nui\_set\_params](qwen-asr-message-websocket-sdk-ios-fb447b88c464d9d4.md#model-qwen-audio-asr-message-763672f3f8dgw)、[语音识别效果参数](qwen-asr-message-websocket-sdk-ios-fb447b88c464d9d4.md#model-qwen-audio-asr-message-d20cce9518kla)、[nui\_dialog\_start](qwen-asr-message-websocket-sdk-ios-fb447b88c464d9d4.md#model-qwen-audio-asr-message-8fe6ea298apzu)、[onNuiAudioStateChanged](qwen-asr-message-websocket-sdk-ios-fb447b88c464d9d4.md#model-qwen-audio-asr-message-bc71fe2545pfy)、[onNuiNeedAudioData](qwen-asr-message-websocket-sdk-ios-fb447b88c464d9d4.md#model-qwen-audio-asr-message-46174611d31qf)、[nui\_update\_audio\_data](qwen-asr-message-websocket-sdk-ios-fb447b88c464d9d4.md#model-qwen-audio-asr-message-nui-update-audio-data)、[onNuiEventCallback](qwen-asr-message-websocket-sdk-ios-fb447b88c464d9d4.md#model-qwen-audio-asr-message-163c1ef871tqt)、[nui\_dialog\_cancel](qwen-asr-message-websocket-sdk-ios-fb447b88c464d9d4.md#model-qwen-audio-asr-message-156934a01bzjc)、[nui\_release](#model-qwen-audio-asr-message-6c2931e9ae3eq)

<a id="请求参数"></a>

## 请求参数

<a id="fun-asr-realtime"></a>

<a id="model-fun-asr-realtime"></a>

<a id="model-fun-asr-realtime-a96bfa6340jdd"></a>

<a id="请求参数-3"></a>

### Fun-ASR-Realtime

<a id="连接与控制参数"></a>

<a id="model-fun-asr-realtime-57acf5ecc1w8j"></a>

#### 连接与控制参数

通过在`nui_initialize`接口的`parameters`参数中传入一个JSON字符串来配置。

**参数示例：**以下为 JSON 字符串示例，参数未完整列出。请按实际需求在编码时补充：

<a id="code-block"></a>

```json
{
    "url": "wss://dashscope.aliyuncs.com/api-ws/v1/inference",
    "apikey": "st-****",
    "device_id": "my_device_id",
    "service_mode": "1"
}
```

**参数说明**

<table><thead><tr><th><strong>参数</strong></th><th><strong>类型</strong></th><th><strong>是否必须</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><code>url</code></td><td><code>String</code></td><td>是</td><td>服务地址：<ul><li><code>wss://dashscope.aliyuncs.com/api-ws/v1/inference</code></li><li>华北2（北京）：<code>wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference</code></li><li>新加坡：<code>wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/inference</code></li></ul>调用时，请将 <code>{WorkspaceId}</code> 替换为真实的 <a href="../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain">Workspace ID</a>。</td></tr><tr><td><code>apikey</code></td><td><code>String</code></td><td>是</td><td>API Key。</td></tr><tr><td><code>service_mode</code></td><td><code>String</code></td><td>是</td><td>运行模式。实时语音识别固定为 <code>&quot;1&quot;</code>。</td></tr><tr><td><code>device_id</code></td><td><code>String</code></td><td>是</td><td>用于标识终端用户的唯一字符串，可设为应用内用户ID或客户端生成的设备唯一标识符。此ID主要用于日志追踪和问题排查。</td></tr><tr><td><code>audio_update_manually</code></td><td><code>String</code></td><td>否</td><td>是否启用主动推送音频数据模式。默认值：<code>&quot;false&quot;</code>。设为 <code>&quot;true&quot;</code>，且 SDK 版本支持端侧音频能力（如 AEC、VAD）时，默认启用端侧音频能力。</td></tr><tr><td><code>workspace</code></td><td><code>String</code></td><td>否</td><td>端侧资源文件的存储路径。当 <code>audio_update_manually</code> 设为 <code>&quot;true&quot;</code> 且启用端侧音频能力（如 AEC、VAD）时，必须设置此参数。</td></tr><tr><td><code>debug_path</code></td><td><code>String</code></td><td>否</td><td>日志文件的存储路径。此参数仅在调用<code>nui_initialize</code>接口时将<code>save_log</code>设为<code>YES</code>时生效。此时必须设置日志文件路径，否则将报错。本地最多保留两个日志文件。</td></tr><tr><td><code>save_wav</code></td><td><code>String</code></td><td>否</td><td>是否保存调试用的音频文件。音频文件保存于<code>debug_path</code>下。默认值：&quot;false&quot;。取值范围：<ul><li>&quot;true&quot;：是</li><li>&quot;false&quot;：否</li></ul>此参数仅在调用<code>nui_initialize</code>接口时将<code>save_log</code>设为true时生效。 同时，<code>debug_path</code>也必须被设置。</td></tr><tr><td><code>max_log_file_size</code></td><td><code>int</code></td><td>否</td><td>设定日志文件的最大字节数。此参数仅在调用<code>nui_initialize</code>接口时将<code>save_log</code>设为<code>YES</code>时生效。默认值：104857600（100 * 1024 * 1024 字节, 即 100MiB）。</td></tr><tr><td><code>log_track_level</code></td><td><code>int</code></td><td>否</td><td>控制通过日志回调（<code>onNuiLogTrackCallback</code>）对外发送的日志内容的过滤级别。默认值：2。取值范围：<ul><li>0：LOG_LEVEL_VERBOSE</li><li>1：LOG_LEVEL_DEBUG</li><li>2：LOG_LEVEL_INFO</li><li>3：LOG_LEVEL_WARNING</li><li>4：LOG_LEVEL_ERROR</li><li>5：LOG_LEVEL_NONE（表示关闭此功能）</li></ul>注意：<code>log_track_level</code>与<code>level</code>（通过<code>nui_initialize</code>接口设置）共同决定最终回调的日志。一条日志的级别数值必须同时大于或等于<code>log_track_level</code>和<code>level</code>的值，才会被回调。例如，<code>log_track_level</code>设为2 (INFO)，<code>level</code>设为3 (WARNING)，则只有WARNING及以上级别（数值&gt;=3）的日志才会被回调。</td></tr></tbody></table>

<a id="语音识别效果参数"></a>

<a id="model-fun-asr-realtime-d20cce9518kla"></a>

#### 语音识别效果参数

通过在`nui_set_params`接口的`params`参数中传入一个JSON字符串来配置。

**参数示例：**以下为 JSON 字符串示例，参数未完整列出。请按实际需求在编码时补充：

<a id="code-block-2"></a>

```json
{
    "service_type": 4,
    "nls_config": {
        "model": "fun-asr-realtime",
        "sr_format": "pcm",
        "sample_rate": "16000"
    }
}
```

**参数说明**

<table><thead><tr><th><strong>一级参数</strong></th><th><strong>类型</strong></th><th><strong>是否必须</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><code>service_type</code></td><td><code>int</code></td><td>是</td><td>语音服务类型。实时语音识别固定为 <code>4</code>。</td></tr><tr><td><code>nls_config</code></td><td><code>object</code></td><td>是</td><td>语音识别核心配置对象，包含模型选择、识别效果控制等关键参数。</td></tr><tr><td><code>nls_config.model</code></td><td><code>string</code></td><td>是</td><td>模型名称。</td></tr><tr><td><code>nls_config.sr_format</code></td><td><code>string</code></td><td>是</td><td>音频格式。<p>取值范围：</p><ul><li><code>pcm</code></li><li><code>opus</code></li></ul><div><div><p><strong>重要</strong>传入 PCM 格式的音频数据时，如果将该参数设为 <code>opus</code>，SDK 会在内部完成 Opus 编码。</p></div></div></td></tr><tr><td><code>nls_config.sample_rate</code></td><td><code>int</code></td><td>是</td><td>采样率（Hz）。<p>取值范围：8k模型仅支持 8000 Hz，其他模型支持任意采样率。</p><div><div><p><strong>重要</strong>启用端侧音频能力（如 AEC、VAD）时，不支持 8000 Hz。</p></div></div></td></tr><tr><td><code>nls_config.max_sentence_silence</code></td><td><code>int</code></td><td>否</td><td>VAD 断句静音阈值（ms）。当一段语音后的静音时长超过该阈值时，系统会判定该句子已结束。<p>默认值：1300。</p><p>取值范围：[200, 6000]。</p></td></tr><tr><td><code>nls_config.multi_threshold_mode_enabled</code></td><td><code>boolean</code></td><td>否</td><td><p>是否启用多阈值模式。启用后可防止 VAD 断句切割过长。</p><p>默认值：false。</p></td></tr><tr><td><code>nls_config.heartbeat</code></td><td><code>boolean</code></td><td>否</td><td>是否启用心跳包。<p>默认值：false。</p><ul><li>true：在持续发送静音音频的情况下，可保持与服务端的连接不中断。</li><li>false（默认）：即使持续发送静音音频，连接也将在一定时间后因超时而断开。</li></ul><p>静音音频指的是在音频文件或数据流中没有声音信号的内容。静音音频可以通过多种方法生成，例如使用音频编辑软件如Audacity或Adobe Audition，或者通过命令行工具如FFmpeg。</p></td></tr><tr><td><code>nls_config.vocabulary_id</code></td><td><code>string</code></td><td>否</td><td>预编译热词列表 ID。<p>需预先调用创建热词列表接口生成，识别时传入该 ID 即可使用列表中的热词。</p><p>适用于词汇已知且相对稳定、需要跨请求复用同一词表的场景。</p><p>使用方法请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/improve-asr-accuracy.md#hw_precompiled_h3">预编译热词</a>。</p></td></tr><tr><td><code>nls_config.language_hints</code></td><td><code>array[string]</code></td><td>否</td><td>待识别音频语种。无默认值，不设置时模型自动识别。<p>仅支持设置 1 个值，设置多个时仅第一个生效。</p><a id="accordion-点击查看支持的语言代码"></a><section><p>点击查看支持的语言代码</p><div><ul><li><p>fun-asr-realtime：</p><ul><li>zh: 中文</li><li>en: 英文</li><li>ja: 日语</li><li>ko：韩语</li><li>vi：越南语</li><li>th：泰语</li><li>id：印尼语</li><li>ms：马来语</li><li>tl：菲律宾语</li><li>hi：印地语</li><li>ar：阿拉伯语</li><li>fr：法语</li><li>de：德语</li><li>es：西班牙语</li><li>pt：葡萄牙语</li><li>ru：俄语</li><li>it：意大利语</li><li>nl：荷兰语</li><li>sv：瑞典语</li><li>da：丹麦语</li><li>fi：芬兰语</li><li>no：挪威语</li><li>el：希腊语</li><li>pl：波兰语</li><li>cs：捷克语</li><li>hu：匈牙利语</li><li>ro：罗马尼亚语</li><li>bg：保加利亚语</li><li>hr：克罗地亚语</li><li>sk：斯洛伐克语</li></ul></li><li><p>fun-asr-realtime-2026-02-28：</p><ul><li>zh: 中文</li><li>en: 英文</li><li>ja: 日语</li></ul></li><li><p>fun-asr-flash-8k-realtime、fun-asr-flash-8k-realtime-2026-01-28：</p><ul><li>zh: 中文</li></ul></li></ul></div></section></td></tr><tr><td><code>nls_config.speech_noise_threshold</code></td><td><code>float</code></td><td>否</td><td>语音与噪音的判定阈值，用于调整语音活动检测（VAD）的灵敏度。<p>取值范围：[-1.0, 1.0]。</p><p>取值说明：</p><ul><li>取值越接近 -1：降低噪音判定阈值，噪音被识别为语音的概率增大，可能导致更多噪音被转写</li><li>取值越接近 +1：提高噪音判定阈值，语音被误判为噪音的概率增大，可能导致部分语音被过滤</li></ul><p>此参数为高级配置参数，调整可能显著影响识别效果，建议：</p><ul><li>调整前充分测试验证效果</li><li>根据实际音频环境小幅度调整（建议步长 0.1）</li></ul></td></tr><tr><td><code>nls_config.special_word_filter</code></td><td><code>object</code></td><td>否</td><td>指定在语音识别过程中需要处理的敏感词，并支持对不同敏感词设置不同的处理方式。详情请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/real-time-speech-recognition-user-guide.md#rt03_sensitive_h3">敏感词过滤</a>。</td></tr><tr><td><code>nls_config.enable_connection_fast_check</code></td><td><code>BOOL</code></td><td>否</td><td>是否启用快速网络检测，以便尽快反馈断网情况。默认值：<code>NO</code>。</td></tr></tbody></table>

<a id="接口参考"></a>

<a id="通用参考-qwen-audio-asr-streaming-fun-asr-realtime"></a>

## 接口参考

<a id="共用接口"></a>

<a id="通用参考"></a>

### 共用接口

<a id="nui-release"></a>

<a id="model-qwen-audio-asr-streaming-6c2931e9ae3eq"></a>

<a id="shared-6"></a>

#### nui\_release

<a id="model-qwen-audio-asr-message-6c2931e9ae3eq"></a>

<a id="model-fun-asr-realtime-6c2931e9ae3eq"></a>

释放SDK所有内部资源，并强制终止所有正在进行的任务。此方法调用后，SDK实例将变为不可用状态，如需再次使用，必须重新调用 `nui_initialize` 进行初始化。

**方法签名**

<a id="code-block-3"></a>

```text
-(NuiResultCode) nui_release;
```

<a id="nui-get-version"></a>

<a id="model-qwen-audio-asr-streaming-d691f902dfmyg"></a>

<a id="shared-9"></a>

#### nui\_get\_version

<a id="model-qwen-audio-asr-message-d691f902dfmyg"></a>

<a id="model-fun-asr-realtime-d691f902dfmyg"></a>

获得当前SDK版本信息。此接口需在 `nui_initialize` 之后调用才有返回值。

**方法签名**

<a id="code-block-4"></a>

```text
-(const char*) nui_get_version;
```

**返回值说明**

当前SDK版本信息。

<a id="nui-get-all-response"></a>

<a id="model-qwen-audio-asr-streaming-5351814f1aj65"></a>

<a id="shared-12"></a>

#### nui\_get\_all\_response

<a id="model-qwen-audio-asr-message-5351814f1aj65"></a>

<a id="model-fun-asr-realtime-5351814f1aj65"></a>

获得当前事件回调的完整信息。

**方法签名**

<a id="code-block-5"></a>

```text
-(const char*) nui_get_all_response;
```

**返回值说明**

JSON字符串格式的完整事件信息。

<a id="onnuilogtrackcallback-监听追踪日志"></a>

<a id="model-qwen-audio-asr-streaming-9c10968457gc6"></a>

<a id="shared-15"></a>

#### onNuiLogTrackCallback：监听追踪日志

<a id="model-qwen-audio-asr-message-9c10968457gc6"></a>

<a id="model-fun-asr-realtime-9c10968457gc6"></a>

此回调用于接收 SDK 内部的详细日志，方便进行问题定位和调试。

<a id="code-block-6"></a>

```text
-(void) onNuiLogTrackCallback:(NuiSdkLogLevel)level
                   logMessage:(const char *)log;
```

<a id="fun-asr-realtime-2"></a>

### Fun-ASR-Realtime

<a id="关键接口"></a>

<a id="model-fun-asr-realtime-737b46fda6cbf"></a>

#### 关键接口

<a id="model-fun-asr-realtime-4bed3999d9kx0"></a>

<a id="neonui-3"></a>

##### NeoNui

<a id="model-fun-asr-realtime-05eab5125e2pm"></a>

###### nui\_initialize

初始化语音识别SDK实例。SDK为单例模式，在调用 `nui_release` 前禁止重复初始化。

**方法签名**

<a id="code-block-7"></a>

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

<a id="model-fun-asr-realtime-763672f3f8dgw"></a>

###### nui\_set\_params

以JSON格式设置语音识别效果参数。在 `nui_dialog_start` 之前调用。

**方法签名**

<a id="code-block-8"></a>

```text
-(NuiResultCode) nui_set_params:(const char *)params;
```

**参数说明**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `params` | `char*` | 语音识别效果参数。 |

<a id="model-fun-asr-realtime-8fe6ea298apzu"></a>

###### nui\_dialog\_start

开始识别。

**方法签名**

<a id="code-block-9"></a>

```text
-(NuiResultCode) nui_dialog_start:(NuiVadMode)vad_mode
                      dialogParam:(const char *)dialog_params;
```

**参数说明**

<table><thead><tr><th><strong>参数</strong></th><th><strong>类型</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><code>vad_mode</code></td><td><code>NuiVadMode</code></td><td>VAD模式。固定为<code>MODE_P2T</code>。</td></tr><tr><td><code>dialog_params</code></td><td><code>char*</code></td><td>如果连接与控制参数的<code>apikey</code>参数使用的是<a href="../model-api-reference/more-about-models/generate-temporary-api-key.md">临时API Key</a>，当其过期时，可在此处更新。如果需要通过上下文增强来提升识别准确率，也可在此处传入上下文。<p>内容为JSON格式：</p><a id="code-block-10"></a><pre class="language-json"><code>{
  &quot;apikey&quot;: &quot;st-****&quot;,
  &quot;input_context&quot;: [
    {
      &quot;role&quot;: &quot;user&quot;,
      &quot;content&quot;: [
        {
          &quot;text&quot;: &quot;xxxxx&quot;,
          &quot;type&quot;: &quot;input_text&quot;
        }
      ]
    }
  ]
}
</code></pre></td></tr></tbody></table>

<a id="model-fun-asr-realtime-156934a01bzjc"></a>

###### nui\_dialog\_cancel

结束识别或者立即取消当前交互。

**方法签名**

<a id="code-block-11"></a>

```text
-(NuiResultCode) nui_dialog_cancel:(BOOL)force;
```

**参数说明**

<table><thead><tr><th><strong>参数</strong></th><th><strong>类型</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><code>force</code></td><td><code>BOOL</code></td><td>是否强制结束而忽略最终结果。<ul><li><code>YES</code>：不等待服务端返回最终识别结果就立即结束任务。</li><li><code>NO</code>：结束任务，但是会等待完整结果返回。</li></ul></td></tr></tbody></table>

<a id="model-fun-asr-realtime-nui-dialog-action"></a>

###### nui\_dialog\_action

发送运行时动作，通知端侧 AEC 播放状态。

**方法签名**

<a id="code-block-12"></a>

```text
-(NuiResultCode) nui_dialog_action:(const char *)action_params;
```

**参数说明**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `action_params` | `char*` | 包含运行时动作的 JSON 字符串。 |
| `action_params.type` | `String` | 固定为 `"action"`。 |
| `action_params.command` | `String` | `play_start`: 使用端侧 AEC 时，通知 SDK 播放器开始播放音频。<br><br>`play_over`: 使用端侧 AEC 时，通知 SDK 播放器已结束播放音频。 |

<a id="model-fun-asr-realtime-nui-update-audio-data"></a>

###### nui\_update\_audio\_data

当 `audio_update_manually` 设为 `"true"` 时，录音数据不再通过 `onNuiNeedAudioData` 填入，而是通过此接口主动推送。

**方法签名**

<a id="code-block-13"></a>

```text
-(NuiResultCode) nui_update_audio_data:(const char *)data
                                    Len:(int)length
                              FirstPack:(BOOL)first_pack;
```

**参数说明**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `data` | `const char *` | 推送的音频数据。 |
| `length` | `int` | 推送的音频数据的字节数。 |
| `first_pack` | `BOOL` | 无需关注此参数。 |

<a id="model-fun-asr-realtime-nui-push-reference-data"></a>

###### nui\_push\_reference\_data

当 `audio_update_manually` 设为 `"true"` 且启用端侧 AEC 回声消除能力时，需要通过此接口推送播放器播放的音频数据作为参考信号。

**方法签名**

<a id="code-block-14"></a>

```text
-(NuiResultCode) nui_push_reference_data:(const char *)data
                                     Len:(int)length
                               FirstPack:(BOOL)first_pack;
```

**参数说明**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `data` | `const char *` | 推送的音频数据。 |
| `length` | `int` | 推送的音频数据的字节数。 |
| `first_pack` | `BOOL` | 无需关注此参数。 |

<a id="model-fun-asr-realtime-8b030fec74e01"></a>

<a id="neonuisdkdelegate-监听回调-3"></a>

##### NeoNuiSdkDelegate：监听回调

<a id="model-fun-asr-realtime-163c1ef871tqt"></a>

###### onNuiEventCallback：监听事件和语音识别结果

**方法签名**

<a id="code-block-15"></a>

```text
-(void) onNuiEventCallback:(NuiCallbackEvent)nuiEvent
                    dialog:(long)dialog
                 kwsResult:(const char *)wuw
                 asrResult:(const char *)asr_result
                  ifFinish:(BOOL)finish
                   retCode:(int)code;
```

**参数说明**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `nuiEvent` | `NuiCallbackEvent` | 回调事件。 |
| `dialog` | `long` | 会话编码，无需关注该参数。 |
| `wuw` | `char*` | 语音唤醒功能。无需关注该参数。 |
| `asr_result` | `char*` | 语音识别结果。 |
| `finish` | `BOOL` | 本轮识别是否结束标志。 |
| `code` | `int` | 仅在出现 `EVENT_ASR_ERROR` 事件时有效。 |

<a id="model-fun-asr-realtime-bc71fe2545pfy"></a>

###### onNuiAudioStateChanged：监听音频状态

SDK 通过此回调通知何时应该开始或停止录音。

**方法签名**

<a id="code-block-16"></a>

```text
-(void) onNuiAudioStateChanged:(NuiAudioState)state;
```

**NuiAudioState状态说明**

| 参数 | 说明 |
| --- | --- |
| `STATE_OPEN` | 交互启动，可以打开录音设备进行录音。 |
| `STATE_PAUSE` | 交互停止，可以停止录音。 |
| `STATE_CLOSE` | SDK 实例已释放，可以彻底关闭录音设备。 |

<a id="model-fun-asr-realtime-46174611d31qf"></a>

###### onNuiNeedAudioData：填充待识别音频数据

开始识别后，该回调被连续触发，需在其中提供待识别音频数据。

**方法签名**

<a id="code-block-17"></a>

```text
-(int) onNuiNeedAudioData:(char *)audioData length:(int)len;
```

**参数说明**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `audioData` | `char *` | 填充的音频数据。 |
| `len` | `int` | 填充的音频数据的字节数。 |

<a id="model-fun-asr-realtime-on-nui-assist-event-callback"></a>

###### onNuiAssistEventCallback：辅助数据和信息结果

此回调用于接收 SDK 内部的辅助事件和相关数据。

**方法签名**

<a id="code-block-18"></a>

```text
-(void) onNuiAssistEventCallback:(NuiCallbackEvent)nuiEvent
                            info:(char*)info
                         infoLen:(int)info_len
                          buffer:(char*)buffer
                             len:(int)len;
```

**参数说明**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `nuiEvent` | `NuiCallbackEvent` | 回调事件。 |
| `info` | `char *` | 无需关注此参数。 |
| `info_len` | `int` | 无需关注此参数。 |
| `buffer` | `char *` | 辅助数据，例如 AEC 回声消除后的音频数据。 |
| `len` | `int` | 辅助数据的字节数。 |

<a id="model-fun-asr-realtime-981ff433acpmr"></a>

<a id="nuicallbackevent-事件类型-3"></a>

##### NuiCallbackEvent：事件类型

| 事件 | 说明 |
| --- | --- |
| `EVENT_TRANSCRIBER_STARTED` | 任务启动成功。 |
| `EVENT_VAD_START` | 任务启动后即触发该事件。不代表检测到人声起点。 |
| `EVENT_VAD_END` | 检测到人声终点。 |
| `EVENT_ASR_PARTIAL_RESULT` | 语音识别中间结果。 |
| `EVENT_ASR_ERROR` | 语音识别过程中出现错误。 |
| `EVENT_MIC_ERROR` | 因连续2秒未收到任何音频数据而触发。 |
| `EVENT_SENTENCE_END` | 检测到一句话结束，此时会返回一句完整的识别结果。 |
| `EVENT_TRANSCRIBER_COMPLETE` | 语音识别结束。 |
| `EVENT_AEC_DATA` | AEC 回声消除后的音频数据。 |
