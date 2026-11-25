# Qwen-Audio-Realtime Android SDK

使用 Qwen-Audio-Realtime 实时语音对话 Android SDK，实现实时音频输入以及语音或文本输出。

连接与鉴权参见 [WebSocket 接入](../model-api-reference/realtime-api-directory/audio-realtime-api-directory/audio-realtime-websocket-access.md)；事件字段与 JSON 示例参见[客户端事件](../model-api-reference/realtime-api-directory/audio-realtime-api-directory/fun-audiochat-client-events.md)和[服务端事件](../model-api-reference/realtime-api-directory/audio-realtime-api-directory/qwen-audio-realtime-server-events.md)。

**用户指南：**关于模型介绍和选型建议请参见[实时语音对话](../model-user-guide/model-experience/speech-and-audio/speech-to-speech/qwen-audio-realtime-user-guides.md)。

<a id="前提条件"></a>

## 前提条件

1.  [获取与配置 API Key](../model-api-reference/preparations/get-api-key.md)。移动端应用请勿硬编码长期 API Key。建议由应用服务端[生成临时 API Key](../model-api-reference/more-about-models/generate-temporary-api-key.md)，再下发给客户端。

<a id="安装-sdk"></a>

### 安装 SDK

-   [下载最新 SDK 整合包](https://help.aliyun.com/zh/model-studio/sdk-selection-and-download)。
-   解压 ZIP 包。在 `app/libs` 目录中获取 AAR 格式 SDK，并添加到项目依赖。需要 Android C++ 接入时，使用 ZIP 包内的 `android_libs` 与 `android_include` 获取动态库和头文件。

<a id="快速开始"></a>

<a id="quick-start"></a>

## 快速开始

用 Android Studio 打开工程。示例代码位于`DashQwenAudioChatActivity.java`，替换 API Key 后体验功能。

<a id="调用步骤"></a>

<a id="call-procedure"></a>

### 调用步骤

1.  初始化 SDK
2.  按业务需求设置参数：通过[initialize](android-sdk-for-qwen-audio-realtime-service-fbe978d80b5ee150.md#initialize)接口的`parameters`参数设置[连接与控制参数](android-sdk-for-qwen-audio-realtime-service-fbe978d80b5ee150.md#connection-and-control-parameters)；通过[setParams](android-sdk-for-qwen-audio-realtime-service-fbe978d80b5ee150.md#set-params)接口设置[语音对话效果参数](android-sdk-for-qwen-audio-realtime-service-fbe978d80b5ee150.md#conversation-parameters)。
3.  调用[startDialog](android-sdk-for-qwen-audio-realtime-service-fbe978d80b5ee150.md#start-dialog)启动对话流程。
4.  在[onNuiAudioStateChanged](android-sdk-for-qwen-audio-realtime-service-fbe978d80b5ee150.md#on-nui-audio-state-changed)回调中，根据音频状态开启录音设备。
5.  在[onNuiNeedAudioData](android-sdk-for-qwen-audio-realtime-service-fbe978d80b5ee150.md#on-nui-need-audio-data)回调中持续提供录音数据，或者通过[updateAudio](android-sdk-for-qwen-audio-realtime-service-fbe978d80b5ee150.md#update-audio)持续推送录音数据。
6.  在[onNuiAssistEventCallback](android-sdk-for-qwen-audio-realtime-service-fbe978d80b5ee150.md#on-nui-assist-event-callback)回调中持续获得 AI 返回的语音数据。
7.  在[onNuiEventCallback](android-sdk-for-qwen-audio-realtime-service-fbe978d80b5ee150.md#on-nui-event-callback)回调中监听事件并获取事件信息。
8.  调用[stopDialog](android-sdk-for-qwen-audio-realtime-service-fbe978d80b5ee150.md#stop-dialog)停止对话，并通过监听EVENT\_TRANSCRIBER\_COMPLETE事件确认对话已结束。
9.  当对话功能不再使用时，调用[release](android-sdk-for-qwen-audio-realtime-service-fbe978d80b5ee150.md#release)接口释放 SDK 资源。

<a id="请求参数"></a>

<a id="request-parameters"></a>

## 请求参数

<a id="连接与控制参数"></a>

<a id="connection-and-control-parameters"></a>

### 连接与控制参数

通过在[initialize](android-sdk-for-qwen-audio-realtime-service-fbe978d80b5ee150.md#initialize)接口的`parameters`参数中传入一个 JSON 字符串来配置。

**参数示例：**以下为 JSON 字符串示例，参数未完整列出。请按实际需求在编码时补充：

示例使用 `qwen-audio-3.1-realtime-plus`。更换模型时，请同步修改 URL 中的 `model` 和[语音对话效果参数](#conversation-parameters)中的 `nls_config.model`。

<a id="code-block"></a>

```text
{
    "url": "wss://dashscope.aliyuncs.com/api-ws/v1/realtime?model=qwen-audio-3.1-realtime-plus",
    "apikey": "st-****",
    "device_id": "my_device_id",
    "service_mode": "1"
}
```

**参数说明**

<table><thead><tr><th><strong>参数</strong></th><th><strong>类型</strong></th><th><strong>是否必须</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><p><code>url</code></p></td><td><p><code>String</code></p></td><td><p>是</p></td><td><p>服务地址：</p><ul><li><code>wss://dashscope.aliyuncs.com/api-ws/v1/realtime?model=&lt;model_name&gt;</code></li><li>华北2（北京）：<code>wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime?model=&lt;model_name&gt;</code></li><li>新加坡：<code>wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime?model=&lt;model_name&gt;</code></li></ul>调用时，请将 <code>{WorkspaceId}</code> 替换为真实的<a href="../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain">Workspace ID</a>。<p></p></td></tr><tr><td><p><code>apikey</code></p></td><td><p><code>String</code></p></td><td><p>是</p></td><td><p>API Key。</p></td></tr><tr><td><p><code>service_mode</code></p></td><td><p><code>String</code></p></td><td><p>是</p></td><td><p>运行模式。实时语音对话固定为 <code>&quot;1&quot;</code>。</p></td></tr><tr><td><p><code>device_id</code></p></td><td><p><code>String</code></p></td><td><p>是</p></td><td><p>用于标识终端用户的唯一字符串，可设为应用内用户 ID或客户端生成的设备唯一标识符。此 ID主要用于日志追踪和问题排查。</p></td></tr><tr><td><p>audio_update_manually</p></td><td><p><code>String</code></p></td><td><p>否</p></td><td><p>是否启用主动推送音频数据模式，默认值：&quot;false&quot;。<br>当设置为&quot;true&quot;启用主动推送音频数据模式时，且SDK版本支持端侧音频能力（如AEC、VAD），则默认开启端侧音频能力。</p></td></tr><tr><td><p>workspace</p></td><td><p><code>String</code></p></td><td><p>否</p></td><td><p>当参数audio_update_manually设置为&quot;true&quot;时，且启用端侧音频能力（如AEC、VAD）时，必须设置workspace，即端侧资源文件存储的路径。</p></td></tr><tr><td><p><code>debug_path</code></p></td><td><p><code>String</code></p></td><td><p>否</p></td><td><p>日志文件的存储路径。 此参数仅在调用<a href="android-sdk-for-qwen-audio-realtime-service-fbe978d80b5ee150.md#initialize">initialize</a>接口时将<code>save_log</code>设为true时生效。此时必须设置日志文件路径，否则将报错。 本地最多保留两个日志文件。</p></td></tr><tr><td><p><code>save_wav</code></p></td><td><p><code>String</code></p></td><td><p>否</p></td><td><p>是否保存调试用的音频文件。音频文件保存于<code>debug_path</code>下。<br>默认值：&quot;false&quot;。<br>取值范围：</p><ul><li>&quot;true&quot;：是</li><li>&quot;false&quot;：否</li></ul>此参数仅在调用<a href="android-sdk-for-qwen-audio-realtime-service-fbe978d80b5ee150.md#initialize">initialize</a>接口时将<code>save_log</code>设为true时生效。 同时，<code>debug_path</code>也必须被设置。<p></p></td></tr><tr><td><p><code>max_log_file_size</code></p></td><td><p><code>int</code></p></td><td><p>否</p></td><td><p>设定日志文件的最大字节数。<br>此参数仅在调用<a href="android-sdk-for-qwen-audio-realtime-service-fbe978d80b5ee150.md#initialize">initialize</a>接口时将<code>save_log</code>设为true时生效。<br>默认值：104857600（100 * 1024 * 1024 字节, 即 100MiB）。</p></td></tr><tr><td><p><code>log_track_level</code></p></td><td><p><code>int</code></p></td><td><p>否</p></td><td><p>控制通过日志回调（<code>onNuiLogTrackCallback</code>）对外发送的日志内容的过滤级别。<br>默认值：2。<br>取值范围：</p><ul><li>0：LOG_LEVEL_VERBOSE</li><li>1：LOG_LEVEL_DEBUG</li><li>2：LOG_LEVEL_INFO</li><li>3：LOG_LEVEL_WARNING</li><li>4：LOG_LEVEL_ERROR</li><li>5：LOG_LEVEL_NONE（表示关闭此功能）</li></ul>注意：<code>log_track_level</code>与<code>level</code>（通过<a href="android-sdk-for-qwen-audio-realtime-service-fbe978d80b5ee150.md#initialize">initialize</a>接口设置）共同决定最终回调的日志。一条日志的级别数值必须同时大于或等于<code>log_track_level</code>和<code>level</code>的值，才会被回调。例如，<code>log_track_level</code>设为2 (INFO)，<code>level</code>设为3 (WARNING)，则只有WARNING及以上级别（数值&gt;=3）的日志才会被回调。<p></p></td></tr><tr><td><p>aec_params</p></td><td><p><code>object</code></p></td><td><p>否</p></td><td><p>端侧AEC能力高级参数配置对象。当参数audio_update_manually设置为&quot;true&quot;时才启用此配置对象。</p></td></tr><tr><td><p>aec_params.enable_aec</p></td><td><p><code>boolean</code></p></td><td><p>否</p></td><td><p>是否开启端侧AEC回声消除能力。<br>当参数audio_update_manually设置为&quot;true&quot;时，且SDK版本支持端侧AEC音频能力，则默认开启。</p></td></tr><tr><td><p>aec_params.save_audio</p></td><td><p><code>boolean</code></p></td><td><p>否</p></td><td><p>是否开启端侧AEC回声消除模块音频存储功能。 当<code>save_wav</code>为&quot;true&quot;，且设置了<code>debug_path</code>，则默认开启，将AEC运行音频数据存储到<code>debug_path</code>下。</p></td></tr><tr><td><p>aec_params.enable_aec_data_callback</p></td><td><p><code>boolean</code></p></td><td><p>否</p></td><td><p>是否将AEC后的数据送给用户，默认false；开启后在onNuiAssistEventCallback的EVENT_AEC_DATA接收。</p></td></tr><tr><td><p>vad_params</p></td><td><p><code>object</code></p></td><td><p>否</p></td><td><p>端侧VAD能力高级参数配置对象。<br>当参数audio_update_manually设置为&quot;true&quot;时才启用此配置对象。</p></td></tr><tr><td><p>vad_params.enable_vad</p></td><td><p><code>boolean</code></p></td><td><p>否</p></td><td><p>是否开启端侧VAD人声检测能力。<br>当参数audio_update_manually设置为&quot;true&quot;时，且SDK版本支持端侧VAD音频能力，则默认开启。</p></td></tr><tr><td><p>vad_params.save_audio</p></td><td><p><code>boolean</code></p></td><td><p>否</p></td><td><p>是否开启端侧VAD人声检测模块音频存储功能。<br>当<code>save_wav</code>为&quot;true&quot;，且设置了<code>debug_path</code>，则默认开启，将VAD运行音频数据存储到<code>debug_path</code>下。</p></td></tr></tbody></table>

<a id="语音对话效果参数"></a>

<a id="conversation-parameters"></a>

### 语音对话效果参数

通过在[setParams](android-sdk-for-qwen-audio-realtime-service-fbe978d80b5ee150.md#set-params)接口的`params`参数中传入一个 JSON 字符串来配置。

**参数示例：**以下为 JSON 字符串示例，参数未完整列出。请按实际需求在编码时补充：

<a id="code-block-2"></a>

```text
{
    "service_type": 4,
    "nls_config": {
        "model": "qwen-audio-3.1-realtime-plus",
        "sr_format": "pcm"
    }
}
```

**参数说明**

<table><thead><tr><th><strong>一级参数</strong></th><th><strong>类型</strong></th><th><strong>是否必须</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><p><code>service_type</code></p></td><td><p><code>int</code></p></td><td><p>是</p></td><td><p>语音服务类型。实时语音对话固定为 <code>4</code>。</p></td></tr><tr><td><p><code>nls_config</code></p></td><td><p><code>object</code></p></td><td><p>是</p></td><td><p>语音对话核心配置对象，包含模型选择、对话效果控制等关键参数。</p></td></tr><tr><td><p><code>nls_config.model</code></p></td><td><p><code>string</code></p></td><td><p>是</p></td><td><p>指定模型名。支持qwen-audio-3.1-realtime-plus、qwen-audio-3.1-realtime-flash、qwen-audio-3.0-realtime-plus和qwen-audio-3.0-realtime-flash系列模型。</p></td></tr><tr><td><p><code>nls_config.sr_format</code></p></td><td><p><code>string</code></p></td><td><p>是</p></td><td><p>输入音频格式。当前仅支持 <code>pcm</code>（16kHz 16bit 单声道），为默认值。</p></td></tr><tr><td><p><code>nls_config.modalities</code></p></td><td><p><code>string</code></p></td><td><p>否</p></td><td><p>array 格式的字符串，模型输出模态设置，可选值：</p><ul><li><code>[&quot;text&quot;]</code>：仅输出文本。</li><li><code>[&quot;audio&quot;, &quot;text&quot;]</code>（默认值）：同时输出文本和音频。</li></ul><p></p></td></tr><tr><td><p>nls_config.voice</p></td><td><p><code>string</code></p></td><td><p>否</p></td><td><p>TTS 音色名称。3.1 Plus/Flash 的默认值为 <code>longanqian_v3.1</code>，3.0 Plus/Flash 的默认值为 <code>longanqian</code>。仅可在第一次 <code>session.update</code> 中设置，后续传入将被忽略。</p><ul><li><strong>3.1 Plus/Flash 系统音色</strong>：可选值包括 <code>longanqian_v3.1</code> 和 3.1 TTS Plus/Flash 音色列表中的全部音色，完整范围请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-to-speech/qwen-audio-realtime-user-guides.md#fc60h311">音色配置</a>。</li><li><strong>3.0 Plus/Flash 系统音色</strong>：<code>longanqian</code>、<code>longanlingxin</code>、<code>longanlingxi</code>、<code>longanxiaoxin</code>、<code>longanlufeng</code>。</li><li><strong>声音复刻音色</strong>：通过声音复刻 API 创建，将返回的 <code>voice_id</code> 填入此参数。详见<a href="../model-user-guide/model-experience/speech-and-audio/speech-to-speech/qwen-audio-realtime-user-guides.md#fc60h311">音色配置</a>。</li></ul></td></tr><tr><td><p>nls_config.enable_speech_emotion</p></td><td><p><code>boolean</code></p></td><td><p>否</p></td><td><p>是否开启情绪增强功能。开启后，回复音色的情绪变化更明显。默认值：<code>true</code>。可选值：<code>true</code>、<code>false</code>。</p></td></tr><tr><td><p>nls_config.instructions</p></td><td><p><code>string</code></p></td><td><p>否</p></td><td><p>系统指令，用于设定模型的角色身份、回答风格和行为偏好。对整个会话生效。</p></td></tr><tr><td><p>nls_config.max_history_turns</p></td><td><p><code>int</code></p></td><td><p>否</p></td><td><p>允许单次请求的最大历史 QA 轮数。取值范围为 1-50，默认值为 20。</p></td></tr><tr><td><p>nls_config.tools</p></td><td><p><code>string</code></p></td><td><p>否</p></td><td><p>array 格式的字符串。Function Calling 工具定义列表。配置后模型可根据用户输入自主决定是否调用工具。<br>内部参数说明：<br><strong>type</strong><code>string</code><strong>（必选）</strong><br>固定为 <code>function</code>。<br><strong>function.name</strong><code>string</code><strong>（必选）</strong><br>工具函数名称。<br><strong>function.description</strong><code>string</code>（可选）<br>对工具函数功能的描述，模型据此判断是否调用该工具。<br><strong>function.parameters</strong><code>object</code>（可选）<br>对工具函数入参的描述，模型据此提取所需入参。若函数无需入参，可不指定。<br>示例：</p><a id="code-block-3"></a><pre class="language-json"><code>[
  {
    &quot;type&quot;: &quot;function&quot;,
    &quot;function&quot;: {
      &quot;name&quot;: &quot;get_weather&quot;,
      &quot;description&quot;: &quot;查询指定城市的天气信息。&quot;,
      &quot;parameters&quot;: {
        &quot;type&quot;: &quot;object&quot;,
        &quot;properties&quot;: {
          &quot;city&quot;: {
            &quot;type&quot;: &quot;string&quot;,
            &quot;description&quot;: &quot;城市&quot;
          }
        },
        &quot;required&quot;: [
          &quot;city&quot;
        ]
      }
    }
  }
]
</code></pre></td></tr><tr><td><p>nls_config.turn_detection</p></td><td><p><code>string</code></p></td><td><p>否</p></td><td><p>以下轮次检测字段说明适用于 <code>qwen-audio-3.1-realtime-plus</code>、<code>qwen-audio-3.1-realtime-flash</code>、<code>qwen-audio-3.0-realtime-plus</code> 和 <code>qwen-audio-3.0-realtime-flash</code>。</p><p>JSON 对象形式的字符串。轮次检测配置。不设置时则切换为 push-to-talk 模式（手动提交音频并触发推理）。否则启用双工对话模式。</p></td></tr><tr><td><p>nls_config.turn_detection.type</p></td><td><p><code>string</code></p></td><td><p>否</p></td><td><p>VAD 类型，可选值：</p><ul><li><code>server_vad</code>（默认值）：基于声学特征检测语音起止，自动触发推理。</li><li><code>smart_turn</code>：融合声学感知与语义理解的智能轮次检测，通过声学与语义双重判断轮次边界。无语义的声音（如”嗯”、”啊”）不会触发对话轮或打断模型播报。</li><li><code>smart_turn_v2</code>（推荐使用）：在 <code>smart_turn</code> 基础上增强对话上下文理解，更好地判断多人场景中的交互意图。减少旁人说话或无关插话造成的误回复、误打断。</li></ul><p></p></td></tr><tr><td><p>nls_config.turn_detection.threshold</p></td><td><p>float</p></td><td><p>否</p></td><td><p>VAD 灵敏度。适用于 <code>server_vad</code>、<code>smart_turn</code> 和 <code>smart_turn_v2</code>。值越低，越容易将微弱声音（包括背景噪音）识别为语音；值越高，越需要清晰、响亮的语音才能触发检测。<br>取值范围为[-1.0, 1.0]，默认值为 0.5。</p></td></tr><tr><td><p>nls_config.turn_detection.silence_duration_ms</p></td><td><p><code>int</code></p></td><td><p>否</p></td><td><p>语音结束后的最短静音时间（毫秒）。<strong>仅在 server_vad 模式下生效（smart_turn 和 smart_turn_v2 模式下无效）</strong>。静音达到该时长后，触发模型响应。值越低，响应越快，但短暂停顿也可能误触发。<br>取值范围为[200, 6000]，默认值为 800。对话场景推荐 400-800。</p></td></tr><tr><td><p>nls_config.turn_detection.voiceprint_audio_urls</p></td><td><p><code>string</code></p></td><td><p>否</p></td><td><p>array形式的字符串。<strong>在 smart_turn 和 smart_turn_v2 模式下生效。</strong>目标用户预录音频的公网可访问 URL 列表，用于说话人增强。模型通过这些音频在双工对话中锁定目标说话人，忽略旁人声音和背景噪声。最多支持 5 个 URL。音频格式要求：16kHz PCM 或 WAV。</p></td></tr></tbody></table>

<a id="接口参考"></a>

<a id="key-interfaces"></a>

<a id="关键接口"></a>

## 接口参考

<a id="nativenui"></a>

<a id="native-nui"></a>

### NativeNui

<a id="initialize-初始化-sdk"></a>

<a id="initialize"></a>

#### `initialize` · 初始化 SDK

初始化语音对话SDK 实例。SDK 为单例模式，在调用[release](android-sdk-for-qwen-audio-realtime-service-fbe978d80b5ee150.md#release)前禁止重复初始化。

此接口会引起阻塞，应在非UI 线程调用。

**方法签名**

<a id="code-block-4"></a>

```text
public synchronized int initialize(final INativeNuiCallback callback,
                                   String parameters,
                                   final Constants.LogLevel level,
                                   final boolean save_log)
```

**参数说明**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `callback` | `INativeNuiCallback` | 事件和数据回调接口的实现。 |
| `parameters` | `String` | JSON 字符串，包含鉴权、连接和调试参数。参见[连接与控制参数](android-sdk-for-qwen-audio-realtime-service-fbe978d80b5ee150.md#connection-and-control-parameters)。 |
| `level` | `Constants.LogLevel` | 控制SDK自身日志的打印级别。 |
| `save_log` | `boolean` | 是否保存本地日志。若为`true`，须在[连接与控制参数](android-sdk-for-qwen-audio-realtime-service-fbe978d80b5ee150.md#connection-and-control-parameters)中通过`debug_path`指定路径，并可通过`max_log_file_size`设置文件大小。 |

<a id="setparams"></a>

<a id="set-params"></a>

#### setParams

以 JSON 格式设置[语音对话效果参数](android-sdk-for-qwen-audio-realtime-service-fbe978d80b5ee150.md#conversation-parameters)。在[startDialog](android-sdk-for-qwen-audio-realtime-service-fbe978d80b5ee150.md#start-dialog)之前调用。

**方法签名**

<a id="code-block-5"></a>

```text
public synchronized int setParams(String params)
```

**参数说明**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `params` | `String` | [语音对话效果参数](android-sdk-for-qwen-audio-realtime-service-fbe978d80b5ee150.md#conversation-parameters)。 |

<a id="startdialog"></a>

<a id="start-dialog"></a>

#### startDialog

开始对话。

**方法签名**

<a id="code-block-6"></a>

```text
public synchronized int startDialog(VadMode vad_mode, String dialog_params)
```

**参数说明**

<table><thead><tr><th><strong>参数</strong></th><th><strong>类型</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><p><code>vad_mode</code></p></td><td><p><code>VadMode</code></p></td><td><p>VAD模式。固定为<code>VadMode.TYPE_P2T</code>。</p></td></tr><tr><td><p><code>dialog_params</code></p></td><td><p><code>String</code></p></td><td><p>如果<a href="android-sdk-for-qwen-audio-realtime-service-fbe978d80b5ee150.md#connection-and-control-parameters">连接与控制参数</a>的<code>apikey</code>参数使用的是<a href="../model-api-reference/more-about-models/generate-temporary-api-key.md">临时API Key</a>，当其过期时，可在此处进行更新。<br>内容为JSON 格式：</p><a id="code-block-7"></a><pre class="language-json"><code>{
  &quot;apikey&quot;: &quot;st-****&quot;
}
</code></pre></td></tr></tbody></table>

<a id="stopdialog"></a>

<a id="stop-dialog"></a>

#### stopDialog

结束对话，调用该接口后，服务端将返回最终对话结果并结束任务。

**方法签名**

<a id="code-block-8"></a>

```text
public synchronized int stopDialog();
```

<a id="canceldialog"></a>

<a id="cancel-dialog"></a>

#### cancelDialog

立即结束对话，调用该接口后，不等待服务端返回最终对话结果就立即结束任务。

**方法签名**

<a id="code-block-9"></a>

```text
public synchronized int cancelDialog();
```

<a id="updateaction"></a>

<a id="update-action"></a>

#### updateAction

在交互过程中下发对话动作指令，用于更新对话上下文等运行时行为。

**方法签名**

<a id="code-block-10"></a>

```text
public synchronized int updateAction(String params);
```

**参数说明**

<table><thead><tr><th><strong>参数</strong></th><th><strong>类型</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><p><code>params</code></p></td><td><p><code>String</code></p></td><td><p>JSON 形式的字符串，用于更新对话上下文等运行时行为。</p></td></tr><tr><td><p><code>params.type</code></p></td><td><p><code>String</code></p></td><td><p>固定&quot;action&quot;。</p></td></tr><tr><td><p><code>params.command</code></p></td><td><p><code>String</code></p></td><td><p>具体的运行指令，当前支持 <code>function_call</code>、<code>play_start</code>、<code>play_over</code>。</p><ul><li><code>function_call</code>：更新函数调用请求的指令。</li><li><code>play_start</code>：当使用端侧AEC时，通过此指令通知SDK内部AEC播放器开始播放音频。</li><li><code>play_over</code>：当使用端侧AEC时，通过此指令通知SDK内部AEC播放器已经播放结束。</li></ul><p></p></td></tr><tr><td><p><code>params.context</code></p></td><td><p><code>String</code></p></td><td><p>当<code>command</code>为<code>&quot;function_call&quot;</code>时，更新函数调用请求。</p></td></tr><tr><td><p><code>params.context.type</code></p></td><td><p><code>String</code></p></td><td><p>事件类型，当<code>command</code>为<code>&quot;function_call&quot;</code>时必须设置。</p><ul><li><code>conversation.item.create</code>：手动向对话上下文插入一条对话项。可用于注入历史上下文、补充文本信息，或写回 Function Calling 的工具执行结果。</li><li><code>response.create</code>：在<code>conversation.item.create</code>指令发送后，通过此指令触发二轮推理。</li></ul><p></p></td></tr><tr><td><p><code>params.context.item</code></p></td><td><p><code>object</code></p></td><td><p><code>params.context.type</code>为conversation.item.create时必须设置，表示要创建的对话项。详见如下。</p></td></tr><tr><td><p><code>params.context.response</code></p></td><td><p><code>object</code></p></td><td><p><code>params.context.type</code>为response.create时可设置，表示用于覆盖本轮推理的会话默认配置。不传时使用当前会话配置。详见如下。</p></td></tr></tbody></table>

`context.item`参数：

<table><thead><tr><th><strong>参数</strong></th><th><strong>类型</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><p>id</p></td><td><p><code>String</code></p></td><td><p>可选。对话项的唯一标识符。不传时由服务端自动生成。若指定的 ID 已存在于对话中，会返回错误。</p></td></tr><tr><td><p>type</p></td><td><p><code>String</code></p></td><td><p>必选。对话项类型，可选值：</p><ul><li><code>message</code>：普通对话消息。</li><li><code>function_call</code>：函数调用请求。通常由服务端生成，客户端也可用于补充历史上下文。</li><li><code>function_call_output</code>：工具执行结果。客户端收到 <code>function_call</code> 后执行工具，并用该类型写回结果。</li></ul><p></p></td></tr><tr><td><p>role</p></td><td><p><code>String</code></p></td><td><p><code>message</code> 类型必选。消息角色，可选值：<code>system</code>、<code>user</code>、<code>assistant</code>。</p></td></tr><tr><td><p>content</p></td><td><p>array</p></td><td><p><code>message</code> 类型必选。消息内容列表。每个元素包含 <code>type</code> 和对应的数据字段。<br><strong>各 role 支持的 content 类型</strong>：<br><strong>system</strong><br><code>input_text</code>：系统消息，必填字段 <code>text</code>。<br><strong>user</strong></p><ul><li><code>input_text</code>：用户文本输入，必填字段 <code>text</code>。</li><li><code>input_audio</code>：用户音频输入，必填字段 <code>audio</code>（Base64 编码）。</li></ul><strong>assistant</strong><br><code>output_text</code>：助手文本输出，必填字段 <code>text</code>。<p></p></td></tr><tr><td><p>call_id</p></td><td><p><code>String</code></p></td><td><p>（<code>function_call</code> / <code>function_call_output</code> 类型必选）<br>函数调用的唯一标识符，用于关联请求和结果。</p></td></tr><tr><td><p>name</p></td><td><p><code>String</code></p></td><td><p>（<code>function_call</code> 类型必选）<br>要调用的函数名称。</p></td></tr><tr><td><p>arguments</p></td><td><p><code>String</code></p></td><td><p><code>function_call</code> 类型必选）<br>函数调用参数，JSON 字符串格式。</p></td></tr><tr><td><p>output</p></td><td><p><code>String</code></p></td><td><p>（<code>function_call_output</code> 类型必选）<br>工具执行结果，JSON 字符串格式。</p></td></tr></tbody></table>

`context.response`参数：

<table><thead><tr><th><strong>参数</strong></th><th><strong>类型</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><p>modalities</p></td><td><p><code>array</code></p></td><td><p>array 格式的字符串，模型输出模态设置，可选值：</p><ul><li><code>[&quot;text&quot;]</code>：仅输出文本。</li><li><code>[&quot;audio&quot;, &quot;text&quot;]</code>（默认值）：同时输出文本和音频。</li></ul><p></p></td></tr><tr><td><p>voice</p></td><td><p>string</p></td><td><p>覆盖本轮的 TTS 音色。</p></td></tr></tbody></table>

示例：

<a id="code-block-11"></a>

```text
{
  "type": "action",
  "command": "function_call",
  "context": {
    "item": {
      "call_id": "call_xxxx",
      "output": "{\"city\":\"杭州\",\"condition\":\"晴\",\"temperature\":18}",
      "type": "function_call_output"
    },
    "type": "conversation.item.create"
  }
}

{
  "type": "action",
  "command": "function_call",
  "context": {
    "response": {
      "modalities": [
        "text",
        "audio"
      ]
    },
    "type": "response.create"
  }
}
```

<a id="updateaudio"></a>

<a id="update-audio"></a>

#### updateAudio

参数audio\_update\_manually设置为"true"时，录音数据不再是通过onNuiNeedAudioData填入，而是用此接口主动推送。

**方法签名**

<a id="code-block-12"></a>

```text
public synchronized int updateAudio(byte[ ] data, int len,
                                    boolean first_pack);
```

**参数说明**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `data` | `byte[]` | 推送的音频数据。 |
| `len` | `int` | 推送的音频数据的字节数。 |
| `first_pack` | `boolean` | 请忽略，无需关注此参数。 |

<a id="updaterefaudio"></a>

<a id="update-ref-audio"></a>

#### updateRefAudio

参数audio\_update\_manually设置为"true"时，且启用了端侧AEC回声消除能力，则需要用此接口推送播放器播放的音频数据作为参考信号。

**方法签名**

<a id="code-block-13"></a>

```text
public synchronized int updateRefAudio(byte[ ] data, int len,

                                       boolean first_pack);
```

**参数说明**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `data` | `byte[]` | 推送的音频数据。 |
| `len` | `int` | 推送的音频数据的字节数。 |
| `first_pack` | `boolean` | 请忽略，无需关注此参数。 |

<a id="release-释放-sdk-资源"></a>

<a id="release"></a>

#### `release` · 释放 SDK 资源

释放SDK所有内部资源。此方法调用后，SDK 实例将变为不可用状态，如需再次使用，必须重新调用[initialize](android-sdk-for-qwen-audio-realtime-service-fbe978d80b5ee150.md#initialize)进行初始化。

**方法签名**

<a id="code-block-14"></a>

```text
public synchronized int release();
```

<a id="getversion"></a>

<a id="get-version"></a>

#### GetVersion

获得当前SDK版本信息。

**方法签名**

<a id="code-block-15"></a>

```text
public synchronized String GetVersion();
```

**返回值说明**

当前SDK版本信息。

<a id="inativenuicallback-监听回调"></a>

<a id="native-nui-callback"></a>

### INativeNuiCallback：监听回调

<a id="onnuieventcallback-监听事件信息"></a>

<a id="on-nui-event-callback"></a>

#### onNuiEventCallback：监听事件信息

**方法签名**

<a id="code-block-16"></a>

```text
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

<a id="onnuiaudiostatechanged-监听音频状态"></a>

<a id="on-nui-audio-state-changed"></a>

#### onNuiAudioStateChanged：监听音频状态

SDK 通过此回调通知何时应该开始或停止录音。

**方法签名**

<a id="code-block-17"></a>

```text
void onNuiAudioStateChanged(AudioState state);
```

**AudioState状态说明**

| 状态 | 说明 |
| --- | --- |
| `STATE_OPEN` | 交互启动，可以打开录音设备进行录音。 |
| `STATE_PAUSE` | 交互停止，可以停止录音。 |
| `STATE_CLOSE` | SDK 实例已释放，可以彻底关闭录音设备。 |

<a id="onnuineedaudiodata-填充待处理音频数据"></a>

<a id="on-nui-need-audio-data"></a>

#### onNuiNeedAudioData：填充待处理音频数据

开始对话后，该回调被连续触发，需在其中提供待处理的音频数据。参数audio\_update\_manually设置为"true"时可不关注这个回调。

**方法签名**

<a id="code-block-18"></a>

```text
int onNuiNeedAudioData(byte[ ] buffer, int len);
```

**参数说明**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `buffer` | `byte[]` | 填充的音频数据。 |
| `len` | `int` | 填充的音频数据的字节数。 |

**返回值说明**

实际填充的字节数。

<a id="onnuiassisteventcallback-辅助数据和信息结果"></a>

<a id="on-nui-assist-event-callback"></a>

#### onNuiAssistEventCallback：辅助数据和信息结果

此回调用于接收 SDK 内部的辅助事件和相关数据。

**方法签名**

<a id="code-block-19"></a>

```text
void onNuiAssistEventCallback_(int event, byte[ ] info, int info_len,
                               byte[ ] data);
```

**参数说明**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `event` | `int` | `NuiEvent`事件 |
| `info` | `String` | 无需关注该参数。 |
| `info_len` | `int` | 无需关注该参数。 |
| `data` | `byte[]` | 辅助数据，比如AI返回的TTS音频。 |

<a id="onnuilogtrackcallback-监听追踪日志"></a>

<a id="on-nui-log-track-callback"></a>

#### onNuiLogTrackCallback：监听追踪日志

此回调用于接收 SDK 内部的详细日志，方便进行问题定位和调试。

<a id="code-block-20"></a>

```text
default void onNuiLogTrackCallback(Constants.LogLevel level, String log)
```

<a id="nuievent-事件类型"></a>

<a id="event-types"></a>

### NuiEvent：事件类型

| 事件 | 说明 |
| --- | --- |
| EVENT\_TRANSCRIBER\_STARTED | 任务启动成功。 |
| EVENT\_VAD\_START | 任务启动后即触发该事件。不代表检测到人声起点。 |
| EVENT\_VAD\_END | 检测到人声终点。 |
| EVENT\_ASR\_PARTIAL\_RESULT | 语音识别中间结果。 |
| EVENT\_ASR\_ERROR | 语音对话过程中出现错误。 |
| EVENT\_MIC\_ERROR | 因连续2秒未收到任何音频数据而触发。 |
| EVENT\_SENTENCE\_END | 检测到一句话结束，此时会返回一句完整的识别结果。 |
| EVENT\_TRANSCRIBER\_COMPLETE | 语音对话结束。 |
| EVENT\_AUDIO\_TRANSCRIPTION | 音频模式下的文字字幕增量事件，流式返回字幕片段。 |
| EVENT\_AUDIO\_TRANSCRIPTION\_COMPLETED | 音频模式下的字幕输出完成事件。 |
| EVENT\_OTHER\_RESULT | 其他未归类事件信息，比如function\_call的返回结果等。 |
| EVENT\_ASR\_TTS\_START | AI开始返回TTS数据。 |
| EVENT\_ASR\_TTS\_DATA | AI返回的TTS数据。 |
| EVENT\_ASR\_TTS\_COMPLETE | AI返回TTS数据结束。 |
| EVENT\_AEC\_DATA | AEC回声消除后的音频数据。 |
