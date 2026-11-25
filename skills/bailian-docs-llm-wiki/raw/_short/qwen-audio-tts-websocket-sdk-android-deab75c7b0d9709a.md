# Qwen-Audio-TTS Android SDK

使用 CosyVoice 时，请参见 [CosyVoice Android SDK](cosyvoice-websocket-sdk-android-a3c227256eefa5f2.md)。

<a id="前提条件"></a>

<a id="model-cosyvoice-abf215f434v5x"></a>

## 前提条件

1.  [获取与配置 API Key](../model-api-reference/preparations/get-api-key.md)。移动端应用请勿硬编码长期 API Key。建议由应用服务端[生成临时 API Key](../model-api-reference/more-about-models/generate-temporary-api-key.md)，再下发给客户端。
    
2.  **下载SDK并运行示例代码：**
    -   [下载最新SDK整合包](https://help.aliyun.com/zh/model-studio/sdk-selection-and-download)。
    -   解压 ZIP 包。在 `app/libs` 目录中获取 AAR 格式 SDK，并添加到项目依赖。  
        需要 Android CPP 接入时，使用 ZIP 包内的 `android_libs` 与 `android_include` 获取动态库和头文件。  
        

<a id="快速开始"></a>

<a id="model-qwen-audio-tts-abf215f434v5x"></a>

<a id="shared-21"></a>

<a id="示例代码"></a>

## 快速开始

用 Android Studio 打开工程。示例代码位于`DashCosyVoiceStreamTtsActivity.java`，替换 API Key 后体验功能。

在示例中使用模型 `qwen-audio-3.0-tts-flash`。

<a id="调用方式"></a>

<a id="model-qwen-audio-tts-0701a2d0b75vm"></a>

<a id="shared-23"></a>

### 调用方式

<a id="model-cosyvoice-0701a2d0b75vm"></a>

<table><thead><tr><th><strong>调用方式</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td>一次性输入待合成文本</td><td><strong>调用步骤：</strong><ol><li>初始化 SDK 和播放器组件。</li><li>按业务需求设置参数。</li><li>调用 <code>playStreamInputTts</code>或<code>asyncPlayStreamInputTts</code>发送文本并开始语音合成。</li><li>接收到 <code>STREAM_INPUT_TTS_EVENT_SYNTHESIS_COMPLETE</code> 回调，语音合成结束。</li></ol><strong>适用场景：</strong><ul><li>短文本合成</li><li>需要使用 SSML 标记语言</li></ul></td></tr><tr><td>流式输入待合成文本</td><td><strong>调用步骤：</strong><ol><li>初始化 SDK 和播放器组件。</li><li>按业务需求设置参数。</li><li>调用 <code>startStreamInputTts</code> 开始流式文本语音合成。</li><li>调用 <code>sendStreamInputTts</code> 持续发送文本。</li><li>在<code>onStreamInputTtsDataCallback</code>中，获取二进制音频数据。</li><li>调用 <code>stopStreamInputTts</code> 或 <code>asyncStopStreamInputTts</code> 结束发送，等待合成完成。</li><li>接收到 <code>STREAM_INPUT_TTS_EVENT_SYNTHESIS_COMPLETE</code> 回调，语音合成结束。</li></ol><strong>适用场景：</strong><ul><li>实时对话、长文本“边说边合”</li><li>此方式不支持 SSML 标记语言</li></ul></td></tr></tbody></table>

<a id="请求参数"></a>

<a id="request-parameters"></a>

## 请求参数

<a id="qwen-audio-tts"></a>

<a id="tts-params-qwen-audio-tts"></a>

### Qwen-Audio-TTS

**parameters JSON 示例**：

<a id="code-block"></a>

```json
{
    "model": "qwen-audio-3.0-tts-flash",
    "voice": "longanlingxi",
    "format": "mp3",
    "volume": 50,
    "rate": 1.0,
    "pitch": 1.0
}
```

**parameters 参数说明**：

<table><thead><tr><th><strong>参数</strong></th><th><strong>类型</strong></th><th><strong>是否必须</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><code>model</code></td><td><code>String</code></td><td>是</td><td>模型名称。</td></tr><tr><td><code>voice</code></td><td><code>String</code></td><td>是</td><td>语音合成所使用的音色。<ul><li><strong>系统音色</strong>：参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-synthesis/tts-voice-list/qwen-audio-tts-voice-list.md">Qwen-Audio-TTS音色列表</a></li><li><strong>复刻音色</strong>：通过声音复刻功能定制</li><li><strong>声音设计音色</strong>：通过声音设计功能定制</li></ul></td></tr><tr><td><code>format</code></td><td><code>String</code></td><td>否</td><td>音频编码格式。<p>取值范围：</p><ul><li>pcm</li><li>wav</li><li>mp3（默认）</li><li>opus</li></ul></td></tr><tr><td><code>enable_audio_decoder</code></td><td><code>boolean</code></td><td>否</td><td>是否启用 SDK 内部解码器。默认值：false。<p>仅在音频编码格式为 opus 或 mp3 时生效。启用后，SDK 将 opus 或 mp3 音频数据解码为 PCM 数据后返回。</p></td></tr><tr><td><code>volume</code></td><td><code>int</code></td><td>否</td><td>音量。<p>默认值：50。</p><p>取值范围：[0, 100]。</p></td></tr><tr><td><code>sample_rate</code></td><td><code>int</code></td><td>否</td><td>音频采样率（Hz）。<p>取值范围：8000, 16000, 22050（默认）, 24000, 44100, 48000。</p></td></tr><tr><td><code>rate</code></td><td><code>float</code></td><td>否</td><td>语速。<p>默认值：1.0。</p><p>取值范围：[0.5, 2.0]。</p></td></tr><tr><td><code>pitch</code></td><td><code>float</code></td><td>否</td><td>音调。<p>默认值：1.0。</p><p>取值范围：[0.5, 2.0]。</p></td></tr><tr><td><code>bit_rate</code></td><td><code>int</code></td><td>否</td><td>音频码率（kbps）。音频格式为mp3或opus时，支持通过<code>bit_rate</code>参数调整码率。<p>默认值：32。</p><p>取值范围：[6, 510]。</p></td></tr><tr><td><code>enable_ssml</code></td><td><code>boolean</code></td><td>否</td><td>是否开启SSML功能。<p>默认值：false。</p><ul><li>true：开启。</li><li>false：关闭。</li></ul><p>SSML 的使用限制（支持的模型、音色和接口），请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-synthesis/ssml-latex-user-guide.md#sl01_constraint_h3">使用限制</a>。</p></td></tr><tr><td><code>word_timestamp_enabled</code></td><td><code>boolean</code></td><td>否</td><td>是否开启字级别时间戳。<p>默认值：false。</p><p>仅在流式输出模式下可用。支持复刻音色；支持的系统音色请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-synthesis/tts-voice-list/qwen-audio-tts-voice-list.md">Qwen-Audio-TTS音色列表</a>。</p><blockquote><p>时间戳结果在<code>INativeStreamInputTtsCallback</code>的all_response中。</p></blockquote></td></tr><tr><td><code>seed</code></td><td><code>int</code></td><td>否</td><td>生成时使用的随机数种子，使合成的效果产生变化。在模型版本、文本、音色及其他参数均相同的前提下，使用相同的seed可复现相同的合成结果。<p>默认值0。</p><p>取值范围：[0, 65535]。</p></td></tr><tr><td><code>language_hints</code></td><td><code>String[]</code></td><td>否</td><td><div><div><p><strong>说明</strong>使用 qwen-audio-3.1-tts-flash 的多语种与方言音色时，可通过此参数指定语种或方言。具体用法请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-synthesis/tts-voice-list/qwen-audio-tts-voice-list.md#qwen-tts31-language-hints">多语种与方言音色的设置方法</a>。</p></div></div><p>指定语音合成的目标语言，提升合成效果。</p><p>当数字、缩写、符号等朗读方式或者小语种合成效果不符合预期时使用，例如：</p><ul><li>数字朗读方式不符合预期，“hello, this is 110”读成“hello, this is one one zero”而非“hello, this is 幺幺零”</li><li>符号朗读不准确，“@”读成“艾特”而非“at”</li><li>小语种合成效果差，合成不自然</li></ul><a id="accordion-取值范围"></a><section><p>取值范围</p><div><ul><li><p>zh：中文</p></li><li><p>en：英语</p></li><li><p>fr：法语</p></li><li><p>de：德语</p></li><li><p>ja：日语</p></li><li><p>ko：韩语</p></li><li><p>ru：俄语</p></li><li><p>pt：葡萄牙语</p></li><li><p>th：泰语</p></li><li><p>id：印尼语</p></li><li><p>vi：越南语</p></li><li><p>es：西班牙语</p></li><li><p>it：意大利语</p></li><li><p>ms：马来西亚语</p></li><li><p>fil：菲律宾语</p></li><li><p>ar：阿拉伯语</p></li><li><p>other：其他语种（适用于 <code>qwen-audio-3.1-tts-flash</code>）</p><p>保加利亚语、荷兰语、匈牙利语、罗马尼亚语、丹麦语、克罗地亚语、希腊语、捷克语、挪威语、瑞典语、印地语、斯洛伐克语、芬兰语、乌尔都语、塞尔维亚语、墨西哥西班牙语、立陶宛语、拉脱维亚语、土耳其语、波斯语、希伯来语、蒙古语、斯洛文尼亚语、阿塞拜疆语、波兰语、加泰罗尼亚语、高棉语、巴西葡萄牙语、老挝语、格鲁吉亚语、南非荷兰语、尼泊尔语、白俄罗斯语、马拉雅拉姆语、卢森堡语、阿尔巴尼亚语、泰米尔语、僧伽罗语、泰卢固语、爱沙尼亚语、宿务语、波斯尼亚语、缅甸语、亚美尼亚语、拉丁语、冰岛语、马耳他语、斯瓦希里语、哈萨克语、塞舌尔克里奥尔语、乌克兰语。</p></li></ul></div></section><div><div><p><strong>说明</strong></p><ul><li>此参数为数组，但当前版本仅处理第一个元素，因此建议只传入一个值。</li><li>此参数用于指定语音合成的目标语言，该设置与声音复刻时的样本音频的语种无关。如需设置复刻任务的源语言，请参见<a href="voice-clone-design-http-api-b6a5abbe2d5d2730.md#h2-create">声音复刻API参考</a>。</li></ul></div></div></td></tr><tr><td><code>instruction</code></td><td><code>String</code></td><td>否</td><td>设置指令，用于控制方言、情感或角色等合成效果。<p>使用说明请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-synthesis/realtime-tts-user-guide.md#12884a10929p9">指令控制</a>。</p></td></tr><tr><td><code>enable_aigc_tag</code></td><td><code>boolean</code></td><td>否</td><td>是否在生成的音频中添加AIGC隐性标识。设置为true时，会将隐性标识嵌入到支持格式（wav/mp3/opus）的音频中。<p>默认值：false。</p></td></tr><tr><td><code>aigc_propagator</code></td><td><code>String</code></td><td>否</td><td>设置AIGC隐性标识中的 <code>ContentPropagator</code> 字段，用于标识内容的传播者。仅在 <code>enable_aigc_tag</code> 为 <code>true</code> 时生效。<p>默认值：阿里云UID。</p></td></tr><tr><td><code>aigc_propagate_id</code></td><td><code>String</code></td><td>否</td><td>设置AIGC隐性标识中的 <code>PropagateID</code> 字段，用于唯一标识一次具体的传播行为。仅在 <code>enable_aigc_tag</code> 为 <code>true</code> 时生效。<p>默认值：本次语音合成请求Request ID。</p></td></tr><tr><td><code>hot_fix</code></td><td><code>object</code></td><td>否</td><td>文本热修复配置，用于自定义指定词语的发音或对待合成文本进行替换。<p>参数介绍：</p><ul><li>pronunciation：自定义发音。指定词语的拼音标注，用于纠正默认发音不准确的情况。</li><li>replace：文本替换。在语音合成前将指定词语替换为目标文本，替换后的文本将作为实际合成内容。</li></ul><p>示例：</p><a id="code-block-2"></a><pre class="language-json"><code>&quot;hot_fix&quot;: {
  &quot;pronunciation&quot;: [
    {&quot;天气&quot;: &quot;tian1 qi4&quot;}
  ],
  &quot;replace&quot;: [
    {&quot;今天&quot;: &quot;金天&quot;}
  ]
}
</code></pre></td></tr><tr><td><p><code>enable_markdown_filter</code></p></td><td><p><code>boolean</code></p></td><td><p>否</p></td><td><p>是否启用 Markdown 过滤。启用后，服务会在合成前将 Markdown 转换成适合朗读的文本。</p><p>默认值：<code>false</code>。设为 <code>true</code> 启用。</p></td></tr></tbody></table>

<a id="接口参考"></a>

<a id="通用参考"></a>

<a id="sdk-reference"></a>

## 接口参考

<a id="nativenui"></a>

<a id="model-qwen-audio-tts-h2arch4d5"></a>

<a id="shared-1"></a>

### NativeNui

<a id="model-cosyvoice-h2arch4d5"></a>

本SDK支持创建多个 NativeNui 实例，并通过回调机制处理语音合成事件。

**架构特点**：

-   **多例模式：**通过 `new NativeNui(Constants.ModeType.MODE_STREAM_INPUT_TTS)` 创建实例
    
-   **回调驱动：**通过 `INativeStreamInputTtsCallback` 接口接收事件和数据
    
-   **事件类型：**
    -   `STREAM_INPUT_TTS_EVENT_SYNTHESIS_STARTED`：合成任务开始
    -   `onStreamInputTtsDataCallback`：音频数据返回
    -   `STREAM_INPUT_TTS_EVENT_SYNTHESIS_COMPLETE`：合成任务结束
    -   `STREAM_INPUT_TTS_EVENT_TASK_FAILED`：合成出错

<a id="sendstreaminputtts"></a>

<a id="model-qwen-audio-tts-9e9bf0b955cit"></a>

<a id="shared-3"></a>

### sendStreamInputTts

<a id="model-cosyvoice-9e9bf0b955cit"></a>

发送待合成的文本，与 `startStreamInputTts` 搭配使用。

在调用 `startStreamInputTts` 后，使用此接口持续发送文本。

所有文本发送完毕后，需调用`stopStreamInputTts`或`asyncStopStreamInputTts`来结束发送。

**方法签名：**

<a id="code-block-3"></a>

```java
public synchronized int sendStreamInputTts(String text)
```

**参数说明：**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `text` | `String` | 待合成文本。不支持[SSML](../model-user-guide/model-experience/speech-and-audio/speech-synthesis/ssml-latex-user-guide.md)。如果传入的文本包含SSML标签，这些标签将被当作普通文本读出，不会被解析。 |

<a id="stopstreaminputtts"></a>

<a id="model-qwen-audio-tts-eec84caadcq73"></a>

<a id="shared-5"></a>

### stopStreamInputTts

<a id="model-cosyvoice-eec84caadcq73"></a>

同步接口，通知服务端文本已全部发送，并阻塞等待所有音频数据合成并收到 `STREAM_INPUT_TTS_EVENT_SYNTHESIS_COMPLETE`。

阻塞等待的超时时间由参数 `complete_waiting_ms` 控制。

**方法签名：**

<a id="code-block-4"></a>

```java
public synchronized int stopStreamInputTts()
```

<a id="asyncstopstreaminputtts"></a>

<a id="model-qwen-audio-tts-20ff030ae9j4f"></a>

<a id="shared-7"></a>

### asyncStopStreamInputTts

<a id="model-cosyvoice-20ff030ae9j4f"></a>

异步接口，通知服务端文本已全部发送。调用后立即返回，合成在后台继续进行。

通过 `STREAM_INPUT_TTS_EVENT_SYNTHESIS_COMPLETE` 事件判断合成是否完成。

**方法签名：**

<a id="code-block-5"></a>

```java
public synchronized int asyncStopStreamInputTts()
```

<a id="cancelstreaminputtts"></a>

<a id="model-qwen-audio-tts-20bb6c23b6ngx"></a>

<a id="shared-9"></a>

### cancelStreamInputTts

<a id="model-cosyvoice-20bb6c23b6ngx"></a>

立即中断与服务端的连接并终止当前合成任务。调用后不会再收到任何音频数据回调。

**方法签名：**

<a id="code-block-6"></a>

```java
public synchronized int cancelStreamInputTts()
```

<a id="playstreaminputtts"></a>

<a id="model-qwen-audio-tts-be00eb5c18hnz"></a>

<a id="shared-11"></a>

### playStreamInputTts

<a id="model-cosyvoice-be00eb5c18hnz"></a>

同步执行的一次性合成接口。该接口会发送文本、阻塞并等待接收所有音频数据，直到合成完成后才返回。无需再调用stop接口。

该接口默认启用SSML。如果显式设置`enable_ssml`，则以用户设置为准。

此接口应在非UI线程调用。

**方法签名：**

<a id="code-block-7"></a>

```java
public synchronized int playStreamInputTts(INativeStreamInputTtsCallback callback,
                                           String ticket,
                                           String parameters,
                                           String text,
                                           String session_id,
                                           int log_level,
                                           boolean save_log)
```

**参数说明：**

callback、ticket等参数与`startStreamInputTts`接口中的定义相同。

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `text` | `String` | 待合成文本。支持[SSML](../model-user-guide/model-experience/speech-and-audio/speech-synthesis/ssml-latex-user-guide.md)。 |

<a id="asyncplaystreaminputtts"></a>

<a id="model-qwen-audio-tts-2d43b13c45u3g"></a>

<a id="shared-13"></a>

### asyncPlayStreamInputTts

<a id="model-cosyvoice-2d43b13c45u3g"></a>

异步执行的一次性合成接口。调用后立即返回，合成任务在后台进行，结果通过回调返回。无需再调用stop接口。

该接口默认启用SSML。如果显式设置`enable_ssml`，则以用户设置为准。

**方法签名：**

<a id="code-block-8"></a>

```java
public synchronized int asyncPlayStreamInputTts(INativeStreamInputTtsCallback callback,
                                           String ticket,
                                           String parameters,
                                           String text,
                                           String session_id,
                                           int log_level,
                                           boolean save_log)
```

**参数说明：**

callback、ticket等参数与`startStreamInputTts`接口中的定义相同。

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `text` | `String` | 待合成文本。支持[SSML](../model-user-guide/model-experience/speech-and-audio/speech-synthesis/ssml-latex-user-guide.md)。 |

<a id="onstreaminputttseventcallback-监听事件"></a>

<a id="model-qwen-audio-tts-163c1ef871tqt"></a>

<a id="shared-15"></a>

### onStreamInputTtsEventCallback：监听事件

<a id="model-cosyvoice-163c1ef871tqt"></a>

**方法签名：**

<a id="code-block-9"></a>

```java
void onStreamInputTtsEventCallback(StreamInputTtsEvent event,
                                   String task_id,
                                   String session_id,
                                   int ret_code,
                                   String error_msg,
                                   String timestamp,
                                   String all_response);
```

**参数说明：**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `event` | `StreamInputTtsEvent` | 回调事件。 |
| `task_id` | `String` | 语音合成任务ID。 |
| `session_id` | `String` | 会话ID。客户端传入则原样返回；未传入时由服务端生成。 |
| `ret_code` | `int` | 仅在出现 `STREAM_INPUT_TTS_EVENT_TASK_FAILED` 事件时有效。 |
| `error_msg` | `String` | 错误信息，仅在事件 `STREAM_INPUT_TTS_EVENT_TASK_FAILED` 中有效。 |
| `timestamp` | `String` | 合成结果的时间戳信息。 |
| `all_response` | `String` | 完整的 JSON 字符串响应。可解析以获取所需数据。 |

<a id="onstreaminputttsdatacallback-监听音频数据"></a>

<a id="model-qwen-audio-tts-bc71fe2545pfy"></a>

<a id="shared-17"></a>

### onStreamInputTtsDataCallback：监听音频数据

<a id="model-cosyvoice-bc71fe2545pfy"></a>

合成过程中，SDK 会连续触发此回调，需在回调中获取音频数据。

**方法签名：**

<a id="code-block-10"></a>

```java
void onStreamInputTtsDataCallback(byte[] data);
```

**参数说明：**

<table><thead><tr><th><strong>参数</strong></th><th><strong>类型</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><code>data</code></td><td><code>byte[]</code></td><td>返回当前片段的音频数据，可用于：<ul><li>合成完整的音频文件并播放。</li><li>通过支持流式播放的播放器实时播放。</li></ul><p>注意：</p><ul><li>对 mp3/opus 压缩格式，分段传输必须使用流式播放器，不能逐帧播放，否则可能解码失败。</li><li>组装完整文件时需采用追加模式写入同一文件。</li><li>对于 wav 和 mp3 格式，仅在第一次 <code>onStreamInputTtsDataCallback</code> 回调的数据中包含文件头，后续回调均为纯音频数据。处理时需将所有回调的 <code>buffer</code> 按顺序拼接。opus 格式的每一帧都是独立的 Ogg page，可直接拼接。</li></ul></td></tr></tbody></table>

<a id="onstreaminputttslogtrackcallback-监听追踪日志"></a>

<a id="model-qwen-audio-tts-9c10968457gc6"></a>

<a id="shared-19"></a>

### onStreamInputTtsLogTrackCallback：监听追踪日志

<a id="model-cosyvoice-9c10968457gc6"></a>

此回调用于接收 SDK 内部的详细日志，方便进行问题定位和调试。

**方法签名：**

<a id="code-block-11"></a>

```java
default void onStreamInputTtsLogTrackCallback(Constants.LogLevel level, String log)
```

<a id="ssml-标记语言"></a>

<a id="model-qwen-audio-tts-f01a7c4dcfw2d"></a>

<a id="shared-25"></a>

### SSML 标记语言

<a id="model-cosyvoice-f01a7c4dcfw2d"></a>

**目的**：通过在文本中嵌入 XML 标签，实现对发音、语速、停顿等细节的精确控制。

**使用限制**：仅支持一次性输入待合成文本（`playStreamInputTts` 或 `asyncPlayStreamInputTts` 接口），不支持流式输入待合成文本（`sendStreamInputTts` 接口）。

**使用方法**：调用 `playStreamInputTts`或`asyncPlayStreamInputTts`接口时，SDK 会自动启用 SSML，此时直接在 `text` 参数中传入包含 SSML 标签的文本即可。

更多说明请参见 [SSML 与 LaTeX](../model-user-guide/model-experience/speech-and-audio/speech-synthesis/ssml-latex-user-guide.md)。

<a id="数学表达式"></a>

<a id="model-qwen-audio-tts-d0191ed1a3uhf"></a>

<a id="shared-27"></a>

### 数学表达式

<a id="model-cosyvoice-d0191ed1a3uhf"></a>

**目的**：使模型能够正确朗读常见的数学公式和表达式。

**使用方法**：直接在 `text` 参数中传入包含 LaTeX 格式的数学表达式的文本即可。更多说明请参见 [LaTeX 公式转语音](https://help.aliyun.com/zh/model-studio/latex-capability-support-description)。

<a id="qwen-audio-tts-2"></a>

<a id="model-qwen-audio-tts"></a>

### Qwen-Audio-TTS

<a id="使用流程"></a>

<a id="model-qwen-audio-tts-h3archflow5"></a>

#### 使用流程

Qwen-Audio-TTS 支持一次性输入和流式输入两种调用方式。

**一次性输入**：适用于短文本合成、需要使用 SSML 标记语言的场景。

1.  `playStreamInputTts()`或 `asyncPlayStreamInputTts()`\- 发送一段完整的待合成文本并开始语音合成。前者为同步请求，合成完成后返回；后者为异步请求，发起合成后立即返回
2.  `onStreamInputTtsDataCallback()`\- 接收音频数据
3.  `STREAM_INPUT_TTS_EVENT_SYNTHESIS_COMPLETE`\- 语音合成结束

**流式输入**：适用于实时对话、长文本“边说边合”的场景。此方式不支持 SSML 标记语言。

1.  `startStreamInputTts()`\- 初始化SDK，设置回调接口和连接参数
2.  `sendStreamInputTts()`\- 持续发送待合成文本
3.  `onStreamInputTtsDataCallback()`\- 接收音频数据
4.  `stopStreamInputTts()`或 `asyncStopStreamInputTts()`\- 发送合成结束请求。前者为同步请求，等待合成完成后返回；后者为异步请求，发起请求后立即返回
5.  `STREAM_INPUT_TTS_EVENT_SYNTHESIS_COMPLETE`\- 语音合成结束

<a id="startstreaminputtts"></a>

<a id="model-qwen-audio-tts-05eab5125e2pm"></a>

#### startStreamInputTts

启动双向流式语音合成，建立与服务端的连接，并注册回调以接收事件和音频数据。

此接口可能会引起阻塞，应在非UI线程调用。

**方法签名：**

<a id="code-block-12"></a>

```java
public synchronized int startStreamInputTts(INativeStreamInputTtsCallback callback,
                                            String ticket,
                                            String parameters,
                                            String session_id,
                                            int log_level,
                                            boolean save_log)
```

**参数说明：**

<table><thead><tr><th><strong>参数</strong></th><th><strong>类型</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><code>callback</code></td><td><a href="#model-qwen-audio-tts-h2streamcallback">INativeStreamInputTtsCallback</a></td><td>事件和数据回调接口的实现。</td></tr><tr><td><code>ticket</code></td><td><code>String</code></td><td>JSON字符串，包含鉴权、连接和调试参数。详见下方 ticket 参数说明。</td></tr><tr><td><code>parameters</code></td><td><code>String</code></td><td>JSON字符串，包含语音合成的具体效果参数。详见下方 parameters 参数说明。</td></tr><tr><td><code>session_id</code></td><td><code>String</code></td><td>客户端指定的会话ID。若不传入，服务端将自动生成。</td></tr><tr><td><code>log_level</code></td><td><code>int</code></td><td>控制SDK自身日志的打印级别。<p>取值范围：</p><ul><li>0：LOG_LEVEL_VERBOSE</li><li>1：LOG_LEVEL_DEBUG</li><li>2：LOG_LEVEL_INFO</li><li>3：LOG_LEVEL_WARNING</li><li>4：LOG_LEVEL_ERROR</li><li>5：LOG_LEVEL_NONE（表示关闭此功能）</li></ul></td></tr><tr><td><code>save_log</code></td><td><code>boolean</code></td><td>是否保存本地日志。若为true，须在ticket 参数中通过<code>debug_path</code>指定路径，并可通过<code>max_log_file_size</code>设置文件大小。</td></tr></tbody></table>

**ticket JSON 示例**：

<a id="code-block-13"></a>

```json
{
    "url": "wss://dashscope.aliyuncs.com/api-ws/v1/inference",
    "apikey": "sk-****",
    "device_id": "my_device_id"
}
```

**ticket 参数说明：**

<table><thead><tr><th><strong>参数</strong></th><th><strong>类型</strong></th><th><strong>是否必须</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><code>url</code></td><td><code>String</code></td><td>是</td><td>服务地址：<ul><li><code>wss://dashscope.aliyuncs.com/api-ws/v1/inference</code></li><li>华北2（北京）：<code>wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference</code></li><li>新加坡：<code>wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/inference</code></li></ul><p>调用时，请将 <code>{WorkspaceId}</code> 替换为真实的 <a href="../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain">Workspace ID</a>。</p></td></tr><tr><td><code>apikey</code></td><td><code>String</code></td><td>是</td><td>API Key。建议使用时效性短、安全性更高的<a href="../model-api-reference/more-about-models/generate-temporary-api-key.md">临时API Key</a>，以降低长期有效Key泄露的风险。</td></tr><tr><td><code>device_id</code></td><td><code>String</code></td><td>是</td><td>用于标识终端用户的唯一字符串，可设为应用内用户ID或客户端生成的设备唯一标识符。此ID主要用于日志追踪和问题排查。</td></tr><tr><td><code>complete_waiting_ms</code></td><td><code>int</code></td><td>否</td><td>调用stop接口后，等待合成完成事件（<code>STREAM_INPUT_TTS_EVENT_SYNTHESIS_COMPLETE</code>）的超时时间（毫秒）。<p>默认值：10000。</p></td></tr><tr><td><code>debug_path</code></td><td><code>String</code></td><td>否</td><td>日志文件的存储路径。<p>此参数仅在调用<code>startStreamInputTts</code>、<code>playStreamInputTts</code>或<code>asyncPlayStreamInputTts</code>接口时将<code>save_log</code>设为true时生效。此时必须设置日志文件路径，否则将报错。</p><p>本地最多保留两个日志文件。</p></td></tr><tr><td><code>max_log_file_size</code></td><td><code>int</code></td><td>否</td><td>设定日志文件的最大字节数。<p>此参数仅在调用<code>startStreamInputTts</code>、<code>playStreamInputTts</code>或<code>asyncPlayStreamInputTts</code>接口时将<code>save_log</code>设为true时生效。</p><p>默认值：104857600（100 * 1024 * 1024 字节，即 100MiB）。</p></td></tr><tr><td><code>log_track_level</code></td><td><code>int</code></td><td>否</td><td>控制通过日志回调（<code>onStreamInputTtsLogTrackCallback</code>）对外发送的日志内容的过滤级别。<p>默认值：2。</p><p>取值范围：</p><ul><li>0：LOG_LEVEL_VERBOSE</li><li>1：LOG_LEVEL_DEBUG</li><li>2：LOG_LEVEL_INFO</li><li>3：LOG_LEVEL_WARNING</li><li>4：LOG_LEVEL_ERROR</li><li>5：LOG_LEVEL_NONE（表示关闭此功能）</li></ul><p>注意：<code>log_track_level</code>与<code>log_level</code>（通过<code>startStreamInputTts</code>、<code>playStreamInputTts</code>或<code>asyncPlayStreamInputTts</code>接口设置）共同决定最终回调的日志。一条日志的级别数值必须同时大于或等于<code>log_track_level</code>和<code>log_level</code>的值，才会被回调。例如，<code>log_track_level</code>设为2 (INFO)，<code>log_level</code>设为3 (WARNING)，则只有WARNING及以上级别（数值&gt;=3）的日志才会被回调。</p></td></tr></tbody></table>

请求参数见 [本模型的参数说明](#tts-params-qwen-audio-tts)。

<a id="inativestreaminputttscallback"></a>

<a id="model-qwen-audio-tts-h2streamcallback"></a>

#### INativeStreamInputTtsCallback

Qwen-Audio-TTS 流式语音合成回调接口，用于接收合成事件、音频数据和日志。

<a id="streaminputttsevent"></a>

<a id="model-qwen-audio-tts-h2streamevent"></a>

#### StreamInputTtsEvent

Qwen-Audio-TTS 流式语音合成事件类型枚举。

<table><thead><tr><th><strong>事件</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><code>STREAM_INPUT_TTS_EVENT_SYNTHESIS_STARTED</code></td><td>表示服务端已成功接收请求并开始处理。通常在此事件后，<code>onStreamInputTtsDataCallback</code>将很快开始返回第一批音频数据。</td></tr><tr><td><code>STREAM_INPUT_TTS_EVENT_SENTENCE_SYNTHESIS</code></td><td>语音合成运行过程中的信息，包括计费信息等。</td></tr><tr><td><code>STREAM_INPUT_TTS_EVENT_SYNTHESIS_COMPLETE</code></td><td>表示服务端已发送完全部音频数据，此后 <code>onStreamInputTtsEventCallback</code>将不会再被调用。收到此事件是数据流结束的明确信号。</td></tr><tr><td><code>STREAM_INPUT_TTS_EVENT_TASK_FAILED</code></td><td>表示任务失败。此时可从<code>INativeStreamInputTtsCallback</code>的all_response获得task_id、error_code、error_message用于判断具体错误。<a id="code-block-14"></a><pre class="language-json"><code>{
    &quot;header&quot;: {
        &quot;task_id&quot;: &quot;2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx&quot;,
        &quot;event&quot;: &quot;task-failed&quot;,
        &quot;error_code&quot;: &quot;InvalidParameter&quot;,
        &quot;error_message&quot;: &quot;[tts:]Engine return error code: 418&quot;,
        &quot;attributes&quot;: {}
    },
    &quot;payload&quot;: {}
}
</code></pre></td></tr></tbody></table>

<a id="高级功能"></a>

<a id="model-qwen-audio-tts-c628a837529t1"></a>

#### 高级功能

-   [SSML 标记语言](#shared-25)
-   [数学表达式](#shared-27)
