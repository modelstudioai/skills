# Qwen-Audio-ASR-Streaming Android SDK

其他模型 — [Qwen-Audio-ASR-Message Android SDK](qwen-asr-message-websocket-sdk-android-b9e8e19722b5d570.md) · [Fun-ASR-Realtime Android SDK](fun-asr-realtime-websocket-sdk-android-263995507ca5b758.md)

<a id="前提条件"></a>

## 前提条件

1.  [获取与配置 API Key](../model-api-reference/preparations/get-api-key.md)。移动端应用请勿硬编码长期 API Key。建议由应用服务端[生成临时 API Key](../model-api-reference/more-about-models/generate-temporary-api-key.md)，再下发给客户端。

<a id="安装-sdk"></a>

### 安装 SDK

-   [下载最新SDK整合包](../model-api-reference/more-about-models/sdk-selection-and-download.md)。
    
-   解压 ZIP 包。在 `app/libs` 目录中获取 AAR 格式 SDK，并添加到项目依赖。
    
    需要 Android CPP 接入时，使用 ZIP 包内的 `android_libs` 与 `android_include` 获取动态库和头文件。
    

<a id="快速开始"></a>

<a id="model-qwen-audio-asr-streaming-abf215f434v5x"></a>

<a id="shared-1"></a>

## 快速开始

用 Android Studio 打开工程。示例代码位于`DashFunAsrSpeechTranscriberActivity.java`，替换 API Key 后体验功能。

在示例中使用模型 `qwen-audio-3.1-asr-flash-streaming`。

<a id="model-qwen-audio-asr-message-abf215f434v5x"></a>

<a id="model-fun-asr-realtime-abf215f434v5x"></a>

<a id="调用步骤"></a>

<a id="model-qwen-audio-asr-streaming-0701a2d0b75vm"></a>

<a id="shared-4"></a>

<a id="model-qwen-audio-asr-message-0701a2d0b75vm"></a>

<a id="调用步骤-2"></a>

### 调用步骤

<a id="model-fun-asr-realtime-0701a2d0b75vm"></a>

1.  初始化 SDK
2.  按业务需求设置参数：通过`initialize`接口的`parameters`参数设置连接与控制参数；通过`setParams`接口设置语音识别效果参数。
3.  调用`startDialog`启动识别流程。
4.  在`onNuiAudioStateChanged`回调中，根据音频状态开启录音设备。
5.  在`onNuiNeedAudioData`回调中持续提供录音数据，或者通过`updateAudio`持续推送录音数据。
6.  在`onNuiEventCallback`回调中监听事件并获取语音识别结果。
7.  调用`stopDialog`停止识别，并通过监听EVENT\_TRANSCRIBER\_COMPLETE事件确认识别已结束。
8.  当识别功能不再使用时，调用`release`接口释放 SDK 资源。

**Qwen-Audio-ASR-Message · 接口参考**

[initialize](qwen-asr-message-websocket-sdk-android-b9e8e19722b5d570.md#model-qwen-audio-asr-message-ae6d7dd9cfad3)、[连接与控制参数](qwen-asr-message-websocket-sdk-android-b9e8e19722b5d570.md#model-qwen-audio-asr-message-57acf5ecc1w8j)、[setParams](qwen-asr-message-websocket-sdk-android-b9e8e19722b5d570.md#model-qwen-audio-asr-message-a23e0d85d7ymt)、[语音识别效果参数](qwen-asr-message-websocket-sdk-android-b9e8e19722b5d570.md#model-qwen-audio-asr-message-d20cce9518kla)、[startDialog](qwen-asr-message-websocket-sdk-android-b9e8e19722b5d570.md#model-qwen-audio-asr-message-7d33691bdb32v)、[onNuiAudioStateChanged](qwen-asr-message-websocket-sdk-android-b9e8e19722b5d570.md#model-qwen-audio-asr-message-bc71fe2545pfy)、[onNuiNeedAudioData](qwen-asr-message-websocket-sdk-android-b9e8e19722b5d570.md#model-qwen-audio-asr-message-12577ebc97awb)、[updateAudio](qwen-asr-message-websocket-sdk-android-b9e8e19722b5d570.md#model-qwen-audio-asr-message-ed321b83adxga)、[onNuiEventCallback](qwen-asr-message-websocket-sdk-android-b9e8e19722b5d570.md#model-qwen-audio-asr-message-163c1ef871tqt)、[stopDialog](#model-qwen-audio-asr-message-047417083bahi)、[release](qwen-asr-message-websocket-sdk-android-b9e8e19722b5d570.md#model-qwen-audio-asr-message-44bf12ed9a4g9)

<a id="请求参数"></a>

## 请求参数

<a id="qwen-audio-asr-streaming"></a>

<a id="model-qwen-audio-asr-streaming"></a>

<a id="model-qwen-audio-asr-streaming-a96bfa6340jdd"></a>

### Qwen-Audio-ASR-Streaming

<a id="连接与控制参数"></a>

<a id="model-qwen-audio-asr-streaming-57acf5ecc1w8j"></a>

#### 连接与控制参数

通过在`initialize`接口的`parameters`参数中传入一个JSON字符串来配置。

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

<table><thead><tr><th><strong>参数</strong></th><th><strong>类型</strong></th><th><strong>是否必须</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><p><code>url</code></p></td><td><p><code>String</code></p></td><td><p>是</p></td><td><p>服务地址：</p><ul><li><p><code>wss://dashscope.aliyuncs.com/api-ws/v1/inference</code></p></li><li><p>华北2（北京）：<code>wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference</code></p></li><li><p>新加坡：<code>wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/inference</code></p></li></ul><p>调用时，请将 <code>{WorkspaceId}</code> 替换为真实的 <a href="../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain">Workspace ID</a>。</p></td></tr><tr><td><p><code>apikey</code></p></td><td><p><code>String</code></p></td><td><p>是</p></td><td><p>API Key。</p></td></tr><tr><td><p><code>service_mode</code></p></td><td><p><code>String</code></p></td><td><p>是</p></td><td><p>运行模式。实时语音识别固定为 <code>&quot;1&quot;</code>。</p></td></tr><tr><td><p><code>device_id</code></p></td><td><p><code>String</code></p></td><td><p>是</p></td><td><p>用于标识终端用户的唯一字符串，可设为应用内用户ID或客户端生成的设备唯一标识符。此ID主要用于日志追踪和问题排查。</p></td></tr><tr><td><p><code>audio_update_manually</code></p></td><td><p><code>String</code></p></td><td><p>否</p></td><td><p>是否启用主动推送音频数据模式，默认值：&quot;false&quot;。</p><p>当设置为&quot;true&quot;启用主动推送音频数据模式时，且SDK版本支持端侧音频能力（如AEC、VAD），则默认开启端侧音频能力。</p></td></tr><tr><td><p><code>workspace</code></p></td><td><p><code>String</code></p></td><td><p>否</p></td><td><p>当参数audio_update_manually设置为&quot;true&quot;时，且启用端侧音频能力（如AEC、VAD）时，必须设置workspace，即端侧资源文件存储的路径。</p></td></tr><tr><td><p><code>debug_path</code></p></td><td><p><code>String</code></p></td><td><p>否</p></td><td><p>日志文件的存储路径。</p><p>此参数仅在调用<code>initialize</code>接口时将<code>save_log</code>设为true时生效。此时必须设置日志文件路径，否则将报错。</p><p>本地最多保留两个日志文件。</p></td></tr><tr><td><p><code>save_wav</code></p></td><td><p><code>String</code></p></td><td><p>否</p></td><td><p>是否保存调试用的音频文件。音频文件保存于<code>debug_path</code>下。</p><p>默认值：&quot;false&quot;。</p><p>取值范围：</p><ul><li><p>&quot;true&quot;：是</p></li><li><p>&quot;false&quot;：否</p></li></ul><p>此参数仅在调用<code>initialize</code>接口时将<code>save_log</code>设为true时生效。 同时，<code>debug_path</code>也必须被设置。</p></td></tr><tr><td><p><code>max_log_file_size</code></p></td><td><p><code>int</code></p></td><td><p>否</p></td><td><p>设定日志文件的最大字节数。</p><p>此参数仅在调用<code>initialize</code>接口时将<code>save_log</code>设为true时生效。</p><p>默认值：104857600（100 * 1024 * 1024 字节, 即 100MiB）。</p></td></tr><tr><td><p><code>log_track_level</code></p></td><td><p><code>int</code></p></td><td><p>否</p></td><td><p>控制通过日志回调（<code>onNuiLogTrackCallback</code>）对外发送的日志内容的过滤级别。</p><p>默认值：2。</p><p>取值范围：</p><ul><li><p>0：LOG_LEVEL_VERBOSE</p></li><li><p>1：LOG_LEVEL_DEBUG</p></li><li><p>2：LOG_LEVEL_INFO</p></li><li><p>3：LOG_LEVEL_WARNING</p></li><li><p>4：LOG_LEVEL_ERROR</p></li><li><p>5：LOG_LEVEL_NONE（表示关闭此功能）</p></li></ul><p>注意：<code>log_track_level</code>与<code>level</code>（通过<code>initialize</code>接口设置）共同决定最终回调的日志。一条日志的级别数值必须同时大于或等于<code>log_track_level</code>和<code>level</code>的值，才会被回调。例如，<code>log_track_level</code>设为2 (INFO)，<code>level</code>设为3 (WARNING)，则只有WARNING及以上级别（数值&gt;=3）的日志才会被回调。</p></td></tr><tr><td><p><code>enable_reconnection</code></p></td><td><p><code>String</code></p></td><td><p>否</p></td><td><p>是否开启断网续传功能，默认值：&quot;false&quot;。</p></td></tr><tr><td><p><code>aec_params</code></p></td><td><p><code>object</code></p></td><td><p>否</p></td><td><p>端侧AEC能力高级参数配置对象。当参数audio_update_manually设置为&quot;true&quot;时才启用此配置对象。</p></td></tr><tr><td><p><code>aec_params.enable_aec</code></p></td><td><p><code>boolean</code></p></td><td><p>否</p></td><td><p>是否开启端侧AEC回声消除能力。</p><p>当参数audio_update_manually设置为&quot;true&quot;时，且SDK版本支持端侧AEC音频能力，则默认开启。</p></td></tr><tr><td><p><code>aec_params.save_audio</code></p></td><td><p><code>boolean</code></p></td><td><p>否</p></td><td><p>是否开启端侧AEC回声消除模块音频存储功能。</p><p>当<code>save_wav</code>为&quot;true&quot;，且设置了<code>debug_path</code>，则默认开启，将AEC运行音频数据存储到<code>debug_path</code>下。</p></td></tr><tr><td><p><code>aec_params.enable_aec_data_callback</code></p></td><td><p><code>boolean</code></p></td><td><p>否</p></td><td><p>是否将AEC后的数据送给用户，默认false；开启后在onNuiAssistEventCallback的EVENT_AEC_DATA接收。</p></td></tr><tr><td><p><code>vad_params</code></p></td><td><p><code>object</code></p></td><td><p>否</p></td><td><p>端侧VAD能力高级参数配置对象。当参数audio_update_manually设置为&quot;true&quot;时才启用此配置对象。</p></td></tr><tr><td><p><code>vad_params.enable_aec</code></p></td><td><p><code>boolean</code></p></td><td><p>否</p></td><td><p>是否开启端侧VAD人声检测能力。</p><p>当参数audio_update_manually设置为&quot;true&quot;时，且SDK版本支持端侧VAD音频能力，则默认开启。</p></td></tr><tr><td><p><code>vad_params.save_audio</code></p></td><td><p><code>boolean</code></p></td><td><p>否</p></td><td><p>是否开启端侧VAD人声检测模块音频存储功能。</p><p>当<code>save_wav</code>为&quot;true&quot;，且设置了<code>debug_path</code>，则默认开启，将VAD运行音频数据存储到<code>debug_path</code>下。</p></td></tr></tbody></table>

<a id="语音识别效果参数"></a>

<a id="model-qwen-audio-asr-streaming-d20cce9518kla"></a>

#### 语音识别效果参数

通过在`setParams`接口的`params`参数中传入一个JSON字符串来配置。

**参数示例：**以下为 JSON 字符串示例，参数未完整列出。请按实际需求在编码时补充：

<a id="code-block-2"></a>

```json
{
    "service_type": 4,
    "nls_config": {
        "model": "qwen-audio-3.0-asr-flash-streaming",
        "sr_format": "pcm",
        "sample_rate": "16000"
    }
}
```

**参数说明**

<table><thead><tr><th><strong>一级参数</strong></th><th><strong>类型</strong></th><th><strong>是否必须</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><p><code>service_type</code></p></td><td><p><code>int</code></p></td><td><p>是</p></td><td><p>语音服务类型。实时语音识别固定为 <code>4</code>。</p></td></tr><tr><td><p><code>nls_config</code></p></td><td><p><code>object</code></p></td><td><p>是</p></td><td><p>语音识别核心配置对象，包含模型选择、识别效果控制等关键参数。</p></td></tr><tr><td><p><code>nls_config.model</code></p></td><td><p><code>string</code></p></td><td><p>是</p></td><td><p>模型名称。</p></td></tr><tr><td><p><code>nls_config.sr_format</code></p></td><td><p><code>string</code></p></td><td><p>是</p></td><td><p>音频格式。</p><p>取值范围：</p><ul><li><code>pcm</code></li><li><code>opus</code></li></ul><div><div><p><strong>重要</strong>opus：用户传入PCM格式音频，由SDK内部完成opus编码。</p></div></div></td></tr><tr><td><p><code>nls_config.sample_rate</code></p></td><td><p><code>int</code></p></td><td><p>是</p></td><td><p>采样率（Hz），支持任意采样率。</p><div><div><p><strong>重要</strong>当开启端侧音频能力（如AEC、VAD）时，不支持8000Hz。</p></div></div></td></tr><tr><td><p><code>nls_config.keep_dialect</code></p></td><td><p><code>boolean</code></p></td><td><p>否</p></td><td><p>是否保留方言表达，默认值为 <code>false</code>。<code>false</code>：将方言转写为普通话文本；<code>true</code>：保留方言表达。</p><div><div><p><strong>说明</strong>适用于 <code>qwen-audio-3.1-asr-flash-streaming</code>。</p></div></div></td></tr><tr><td><p><code>nls_config.vad_model</code></p></td><td><p><code>string</code></p></td><td><p>否</p></td><td><p>VAD 模型，默认值为 <code>far_field_meeting_16k</code>。</p><ul><li><code>near_meeting_16k</code>：近场场景。</li><li><code>far_field_meeting_16k</code>：远场场景。</li></ul><div><div><p><strong>说明</strong>适用于 <code>qwen-audio-3.1-asr-flash-streaming</code>。</p></div></div></td></tr><tr><td><p><code>nls_config.max_sentence_silence</code></p></td><td><p><code>int</code></p></td><td><p>否</p></td><td><p>VAD 断句静音阈值（ms）。当一段语音后的静音时长超过该阈值时，系统会判定该句子已结束。</p><p>默认值：800。</p><p>取值范围：[200, 6000]。</p></td></tr><tr><td><p><code>nls_config.multi_threshold_mode_enabled</code></p></td><td><p><code>boolean</code></p></td><td><p>否</p></td><td><p>是否启用多阈值模式。启用后可防止 VAD 断句切割过长。</p><p>默认值：false。</p></td></tr><tr><td><p><code>nls_config.heartbeat</code></p></td><td><p><code>boolean</code></p></td><td><p>否</p></td><td><p>是否启用心跳包。</p><p>默认值：false。</p><ul><li>true：在持续发送静音音频的情况下，可保持与服务端的连接不中断。</li><li>false（默认）：即使持续发送静音音频，连接也将在一定时间后因超时而断开。</li></ul><p>静音音频指的是在音频文件或数据流中没有声音信号的内容。静音音频可以通过多种方法生成，例如使用音频编辑软件如Audacity或Adobe Audition，或者通过命令行工具如FFmpeg。</p></td></tr><tr><td><p><code>nls_config.vocabulary_id</code></p></td><td><p><code>string</code></p></td><td><p>否</p></td><td><p>预编译热词列表 ID。</p><p>需预先调用创建热词列表接口生成，识别时传入该 ID 即可使用列表中的热词。</p><p>适用于词汇已知且相对稳定、需要跨请求复用同一词表的场景。</p><p>使用方法请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/improve-asr-accuracy.md#hw_precompiled_h3">预编译热词</a>。</p></td></tr><tr><td><p><code>nls_config.instant_vocabulary</code></p></td><td><p><code>object</code></p></td><td><p>否</p></td><td><p>即时热词。</p><p>以键值对形式传入，键为热词文本（<code>string</code>），值为热词权重（<code>integer</code>），无需预先创建热词列表。权重取值范围为 [1, 5] 或 50：取 [1, 5] 时值越大模型越倾向输出该词；取 50 时为超级热词，召回率大幅提升，但超级热词数量最多不超过 50 个。</p><p>适用于临时性、会话级别的热词优化。</p><p>与预编译热词同时配置时，系统会合并两类热词；合并后超过 2000 个时，随机选择 2000 个使用。使用方法、适用模型及限制请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/improve-asr-accuracy.md#hw_instant_h3">即时热词</a>。</p></td></tr><tr><td><p><code>nls_config.language_hints</code></p></td><td><p><code>array[string]</code></p></td><td><p>否</p></td><td><p>待识别音频语种。无默认值，不设置时模型自动识别。</p><p>最多支持设置 4 个值，超出时仅前 4 个生效。</p><a id="accordion-点击查看支持的语言代码"></a><section><p>点击查看支持的语言代码</p><div><ul><li>zh: 中文</li><li>en: 英文</li><li>ja: 日语</li><li>ko：韩语</li><li>vi：越南语</li><li>th：泰语</li><li>id：印尼语</li><li>ms：马来语</li><li>tl：菲律宾语</li><li>hi：印地语</li><li>ar：阿拉伯语</li><li>fr：法语</li><li>de：德语</li><li>es：西班牙语</li><li>pt：葡萄牙语</li><li>ru：俄语</li><li>it：意大利语</li><li>nl：荷兰语</li><li>sv：瑞典语</li><li>da：丹麦语</li><li>fi：芬兰语</li><li>no：挪威语</li><li>el：希腊语</li><li>pl：波兰语</li><li>cs：捷克语</li><li>hu：匈牙利语</li><li>ro：罗马尼亚语</li><li>bg：保加利亚语</li><li>hr：克罗地亚语</li><li>sk：斯洛伐克语</li></ul></div></section></td></tr><tr><td><p><code>nls_config.speech_noise_threshold</code></p></td><td><p><code>float</code></p></td><td><p>否</p></td><td><p>语音与噪音的判定阈值，用于调整语音活动检测（VAD）的灵敏度。</p><p>取值范围：[-1.0, 1.0]。</p><p>取值说明：</p><ul><li>取值越接近 -1：降低噪音判定阈值，噪音被识别为语音的概率增大，可能导致更多噪音被转写</li><li>取值越接近 +1：提高噪音判定阈值，语音被误判为噪音的概率增大，可能导致部分语音被过滤</li></ul><p>此参数为高级配置参数，调整可能显著影响识别效果，建议：</p><ul><li>调整前充分测试验证效果</li><li>根据实际音频环境小幅度调整（建议步长 0.1）</li></ul></td></tr><tr><td><p><code>nls_config.special_word_filter</code></p></td><td><p><code>object</code></p></td><td><p>否</p></td><td><p>指定在语音识别过程中需要处理的敏感词，并支持对不同敏感词设置不同的处理方式。详情请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/real-time-speech-recognition-user-guide.md#rt03_sensitive_h3">敏感词过滤</a>。</p></td></tr><tr><td><p><code>nls_config.enable_connection_fast_check</code></p></td><td><p><code>boolean</code></p></td><td><p>否</p></td><td><p>启动快速检测网络的功能，即尽快反馈出断网情况，默认关闭。</p></td></tr></tbody></table>

<a id="接口参考"></a>

## 接口参考

<a id="共用接口"></a>

<a id="通用参考"></a>

### 共用接口

<a id="stopdialog"></a>

<a id="model-qwen-audio-asr-streaming-047417083bahi"></a>

<a id="shared-6"></a>

#### stopDialog

<a id="model-qwen-audio-asr-message-047417083bahi"></a>

<a id="model-fun-asr-realtime-047417083bahi"></a>

结束识别，调用该接口后，服务端将返回最终识别结果并结束任务。

**方法签名**

<a id="code-block-3"></a>

```java
public synchronized int stopDialog();
```

<a id="canceldialog"></a>

<a id="model-qwen-audio-asr-streaming-8c464959f9lm9"></a>

<a id="shared-9"></a>

#### cancelDialog

<a id="model-qwen-audio-asr-message-8c464959f9lm9"></a>

<a id="model-fun-asr-realtime-8c464959f9lm9"></a>

立即结束识别，调用该接口后，不等待服务端返回最终识别结果就立即结束任务。

**方法签名**

<a id="code-block-4"></a>

```java
public synchronized int cancelDialog();
```

<a id="getversion"></a>

<a id="model-qwen-audio-asr-streaming-36cbf0689bzon"></a>

<a id="shared-14"></a>

#### GetVersion

<a id="model-qwen-audio-asr-message-36cbf0689bzon"></a>

<a id="model-fun-asr-realtime-36cbf0689bzon"></a>

获得当前SDK版本信息。

**方法签名**

<a id="code-block-5"></a>

```java
public synchronized String GetVersion();
```

**返回值说明**

当前SDK版本信息。

<a id="onnuilogtrackcallback-监听追踪日志"></a>

<a id="model-qwen-audio-asr-streaming-9c10968457gc6"></a>

<a id="shared-17"></a>

#### onNuiLogTrackCallback：监听追踪日志

<a id="model-qwen-audio-asr-message-9c10968457gc6"></a>

<a id="model-fun-asr-realtime-9c10968457gc6"></a>

此回调用于接收 SDK 内部的详细日志，方便进行问题定位和调试。

<a id="code-block-6"></a>

```java
default void onNuiLogTrackCallback(Constants.LogLevel level, String log)
```

<a id="qwen-audio-asr-streaming-fun-asr-realtime"></a>

<a id="通用参考-qwen-audio-asr-streaming-fun-asr-realtime"></a>

### Qwen-Audio-ASR-Streaming / Fun-ASR-Realtime

<a id="release"></a>

<a id="model-qwen-audio-asr-streaming-44bf12ed9a4g9"></a>

<a id="shared-12"></a>

#### release

<a id="model-fun-asr-realtime-44bf12ed9a4g9"></a>

释放SDK所有内部资源。此方法调用后，SDK实例将变为不可用状态，如需再次使用，必须重新调用`initialize`进行初始化。

**方法签名**

<a id="code-block-7"></a>

```java
public synchronized int release();
```

<a id="qwen-audio-asr-streaming-2"></a>

### Qwen-Audio-ASR-Streaming

<a id="关键接口"></a>

<a id="model-qwen-audio-asr-streaming-737b46fda6cbf"></a>

#### 关键接口

<a id="model-qwen-audio-asr-streaming-4bed3999d9kx0"></a>

<a id="nativenui"></a>

##### NativeNui

<a id="model-qwen-audio-asr-streaming-ae6d7dd9cfad3"></a>

###### initialize

初始化语音识别SDK实例。SDK为单例模式，在调用`release`前禁止重复初始化。

此接口会引起阻塞，应在非UI线程调用。

**方法签名**

<a id="code-block-8"></a>

```java
public synchronized int initialize(final INativeNuiCallback callback,
                                   String parameters,
                                   final Constants.LogLevel level,
                                   final boolean save_log)
```

**参数说明**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `callback` | `INativeNuiCallback` | 事件和数据回调接口的实现。 |
| `parameters` | `String` | JSON字符串，包含鉴权、连接和调试参数。参见连接与控制参数。 |
| `level` | `Constants.LogLevel` | 控制SDK自身日志的打印级别。 |
| `save_log` | `boolean` | 是否保存本地日志。若为`true`，须在连接与控制参数中通过`debug_path`指定路径，并可通过`max_log_file_size`设置文件大小。 |

<a id="model-qwen-audio-asr-streaming-a23e0d85d7ymt"></a>

###### setParams

以JSON格式设置语音识别效果参数。在`startDialog`之前调用。

**方法签名**

<a id="code-block-9"></a>

```java
public synchronized int setParams(String params)
```

**参数说明**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `params` | `String` | 语音识别效果参数。 |

<a id="model-qwen-audio-asr-streaming-7d33691bdb32v"></a>

###### startDialog

开始识别。

**方法签名**

<a id="code-block-10"></a>

```java
public synchronized int startDialog(VadMode vad_mode, String dialog_params)
```

**参数说明**

<table><thead><tr><th><strong>参数</strong></th><th><strong>类型</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><p><code>vad_mode</code></p></td><td><p><code>VadMode</code></p></td><td><p>VAD模式。固定为<code>VadMode.TYPE_P2T</code>。</p></td></tr><tr><td><p><code>dialog_params</code></p></td><td><p><code>String</code></p></td><td><p>如果连接与控制参数的<code>apikey</code>参数使用的是<a href="../model-api-reference/more-about-models/generate-temporary-api-key.md">临时API Key</a>，当其过期时，可在此处进行更新。</p><p>如果需要通过上下文增强来提升识别准确率，则在此处进行更新。</p><p>内容为JSON格式：</p><a id="code-block-11"></a><pre class="language-json"><code>{
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

<a id="model-qwen-audio-asr-streaming-cc82ea7551yjs"></a>

###### updateAction

发送运行时动作，通知端侧 AEC 播放状态。

**方法签名**

<a id="code-block-12"></a>

```java
public synchronized int updateAction(String params);
```

**参数说明**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `params` | `String` | 包含运行时动作的 JSON 字符串。 |
| `params.type` | `String` | 固定"action"。 |
| `params.command` | `String` | `play_start`: 使用端侧 AEC 时，通知 SDK 播放器开始播放音频。<br><br>`play_over`: 使用端侧 AEC 时，通知 SDK 播放器已结束播放音频。 |

<a id="model-qwen-audio-asr-streaming-ed321b83adxga"></a>

###### updateAudio

参数audio\_update\_manually设置为"true"时，录音数据不再是通过onNuiNeedAudioData填入，而是用此接口主动推送。

**方法签名**

<a id="code-block-13"></a>

```java
public synchronized int updateAudio(byte[] data, int len,
                                    boolean first_pack);
```

**参数说明**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `data` | `byte[]` | 推送的音频数据。 |
| `len` | `int` | 推送的音频数据的字节数。 |
| `first_pack` | `boolean` | 请忽略，无需关注此参数。 |

<a id="model-qwen-audio-asr-streaming-45f4db270cn9n"></a>

###### updateRefAudio

参数audio\_update\_manually设置为"true"时，且启用了端侧AEC回声消除能力，则需要用此接口推送播放器播放的音频数据作为参考信号。

**方法签名**

<a id="code-block-14"></a>

```java
public synchronized int updateRefAudio(byte[] data, int len,
                                       boolean first_pack);
```

**参数说明**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `data` | `byte[]` | 推送的音频数据。 |
| `len` | `int` | 推送的音频数据的字节数。 |
| `first_pack` | `boolean` | 请忽略，无需关注此参数。 |

<a id="model-qwen-audio-asr-streaming-8b030fec74e01"></a>

<a id="inativenuicallback-监听回调"></a>

##### INativeNuiCallback：监听回调

<a id="model-qwen-audio-asr-streaming-163c1ef871tqt"></a>

###### onNuiEventCallback：监听事件和语音识别结果

**方法签名**

<a id="code-block-15"></a>

```java
void onNuiEventCallback(NuiEvent event, final int resultCode, final int arg2, KwsResult kwsResult, AsrResult asrResult);
```

**参数说明**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `event` | `NuiEvent` | 回调事件。 |
| `resultCode` | `int` | 仅在出现 `EVENT_ASR_ERROR` 事件时有效。 |
| `arg2` | `int` | 保留参数。 |
| `asrResult` | `AsrResult` | 语音识别结果。 |
| `kwsResult` | `KwsResult` | 语音唤醒功能。无需关注该参数。 |

<a id="model-qwen-audio-asr-streaming-bc71fe2545pfy"></a>

###### onNuiAudioStateChanged：监听音频状态

SDK 通过此回调通知何时应该开始或停止录音。

**方法签名**

<a id="code-block-16"></a>

```java
void onNuiAudioStateChanged(AudioState state);
```

**AudioState状态说明**

| 状态 | 说明 |
| --- | --- |
| `STATE_OPEN` | 交互启动，可以打开录音设备进行录音。 |
| `STATE_PAUSE` | 交互停止，可以停止录音。 |
| `STATE_CLOSE` | SDK 实例已释放，可以彻底关闭录音设备。 |

<a id="model-qwen-audio-asr-streaming-12577ebc97awb"></a>

###### onNuiNeedAudioData：填充待识别音频数据

开始识别后，该回调被连续触发，需在其中提供待识别音频数据。

**方法签名**

<a id="code-block-17"></a>

```java
int onNuiNeedAudioData(byte[] buffer, int len);
```

**参数说明**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `buffer` | `byte[]` | 填充的音频数据。 |
| `len` | `int` | 填充的音频数据的字节数。 |

**返回值说明**

实际填充的字节数。

<a id="model-qwen-audio-asr-streaming-e4ec9d44e7t32"></a>

###### onNuiAssistEventCallback：辅助数据和信息结果

此回调用于接收 SDK 内部的辅助事件和相关数据。

**方法签名**

<a id="code-block-18"></a>

```java
void onNuiAssistEventCallback_(int event, byte[] info, int info_len,
                               byte[] data);
```

**参数说明**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `event` | `int` | `NuiEvent`事件 |
| `info` | `String` | 无需关注该参数。 |
| `info_len` | `int` | 无需关注该参数。 |
| `data` | `byte[]` | 辅助数据，比如AEC回声消除后的音频数据。 |

<a id="model-qwen-audio-asr-streaming-981ff433acpmr"></a>

<a id="nuievent-事件类型"></a>

##### `NuiEvent`：事件类型

| 事件 | 说明 |
| --- | --- |
| `EVENT_TRANSCRIBER_STARTED` | 任务启动成功。 |
| `EVENT_VAD_START` | 任务启动后即触发该事件。不代表检测到人声起点。 |
| `EVENT_VAD_END` | 检测到人声终点。 |
| `EVENT_ASR_PARTIAL_RESULT` | 语音识别中间结果。 |
| `EVENT_ASR_WARN` | 语音识别过程中出现不影响运行的警告，比如开启断网续传后的断网事件。 |
| `EVENT_ASR_ERROR` | 语音识别过程中出现错误。 |
| `EVENT_MIC_ERROR` | 因连续2秒未收到任何音频数据而触发。 |
| `EVENT_SENTENCE_END` | 检测到一句话结束，此时会返回一句完整的识别结果。 |
| `EVENT_TRANSCRIBER_COMPLETE` | 语音识别结束。 |
| `EVENT_AEC_DATA` | AEC回声消除后的音频数据。 |
