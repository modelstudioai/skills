# 非实时语音合成Qwen-Audio-TTS Java SDK参考

本文介绍非实时语音合成Qwen-Audio-TTS的Java SDK调用方法，支持非流式和流式两种调用模式。

> **重要**
>
> 本文描述的功能仅在华北2（北京）地域可用。

> **重要**
>
> 阿里云百炼为华北2（北京）地域推出了业务空间专属域名，能够为推理请求提供卓越的性能和更高的稳定性，建议从 `dashscope.aliyuncs.com` 迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`。

<a id="前提条件"></a>

<a id="h2-cv1a2b3d"></a>

## 前提条件

-   已[获取与配置 API Key](../model-api-reference/preparations/get-api-key.md)并将其配置到环境变量
-   已安装符合版本要求的DashScope Java SDK，建议[安装最新版](../model-api-reference/preparations/install-sdk.md)，SDK版本需≥2.22.15

<a id="httpspeechsynthesizer-类"></a>

<a id="h2-cv2a3b4d"></a>

## HttpSpeechSynthesizer 类

**包路径**：`com.alibaba.dashscope.audio.http_tts.HttpSpeechSynthesizer`

**功能**：基于HTTP的语音合成，支持非流式和流式两种调用方式。

<a id="构造方法"></a>

<a id="h3-cv2a3b5b"></a>

### 构造方法

<a id="code-block"></a>

```java
public HttpSpeechSynthesizer()
```

创建HttpSpeechSynthesizer实例，使用默认配置。SDK会自动从环境变量`DASHSCOPE_API_KEY`或`Constants.apiKey`获取API Key。

<a id="callandreturnaudio-非流式调用-返回音频数据"></a>

<a id="h3-cv2a3b6b"></a>

### callAndReturnAudio() - 非流式调用（返回音频数据）

**方法签名**：

<a id="code-block-2"></a>

```java
public ByteBuffer callAndReturnAudio(HttpSpeechSynthesisParam param) throws ApiException, NoApiKeyException, InputRequiredException
```

**参数说明**：

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `param` | [HttpSpeechSynthesisParam](#h2-cv3a4b5c) | 语音合成参数对象，包含模型、文本、音色等配置。 |

**返回值**：`ByteBuffer`，包含完整的音频数据。可通过`remaining()`获取音频大小（字节）。

<a id="call-非流式调用-返回音频url"></a>

<a id="h3-cv2a3b7b"></a>

### call() - 非流式调用（返回音频URL）

**方法签名**：

<a id="code-block-3"></a>

```java
public HttpSpeechSynthesisResult call(HttpSpeechSynthesisParam param) throws ApiException, NoApiKeyException, InputRequiredException
```

**参数说明**：

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `param` | `HttpSpeechSynthesisParam` | 语音合成参数对象。 |

**返回值**：`HttpSpeechSynthesisResult`对象，通过`getAudioInfo().getUrl()`获取音频下载URL，URL有效期有限，可通过`getAudioInfo().getExpiresAt()`获取过期时间。

<a id="streamcall-流式调用"></a>

<a id="h3-cv2a3b8b"></a>

### streamCall() - 流式调用

**方法签名**：

<a id="code-block-4"></a>

```java
public void streamCall(HttpSpeechSynthesisParam param, ResultCallback<HttpSpeechSynthesisResult> callback) throws ApiException, NoApiKeyException, InputRequiredException
```

**参数说明**：

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `param` | `HttpSpeechSynthesisParam` | 语音合成参数对象。 |
| `callback` | `ResultCallback<HttpSpeechSynthesisResult>` | 回调对象，需实现`onEvent`（接收音频分片）、`onComplete`（合成完成）、`onError`（错误处理）三个方法。 |

该方法为异步调用，音频数据通过回调函数分片返回，适用于对首包延迟有要求的场景。

**ResultCallback 回调方法**：

`com.alibaba.dashscope.common.ResultCallback`是DashScope SDK提供的通用回调接口，需实现以下三个方法：

| 方法 | 参数 | 说明 |
| --- | --- | --- |
| `onEvent` | `HttpSpeechSynthesisResult result` | 每接收到一个音频分片时触发。通过`result.hasAudioData()`判断是否包含音频数据，通过`result.getAudioDataSize()`获取分片大小。 |
| `onComplete` | 无 | 语音合成完成时触发，表示所有音频分片已接收完毕。 |
| `onError` | `Exception e` | 合成过程中发生错误时触发，可通过`e.getMessage()`获取错误信息。 |

<a id="httpspeechsynthesisparam-类"></a>

<a id="h2-cv3a4b5c"></a>

## HttpSpeechSynthesisParam 类

**包路径**：`com.alibaba.dashscope.audio.http_tts.HttpSpeechSynthesisParam`

通过Builder模式构建参数对象。

部分参数没有专用的Builder方法，需要通过继承自父类的`parameter(String key, Object value)`方法或`parameters(Map<String, Object>)`方法进行设置，详见下表中的说明。

<table><thead><tr><th><strong>方法</strong></th><th><strong>类型</strong></th><th><strong>必填</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td>model(String)</td><td><code>String</code></td><td>是</td><td>语音合成模型。</td></tr><tr><td>text(String)</td><td><code>String</code></td><td>是</td><td>待合成文本。<p>支持 SSML 和 LaTeX 格式输入。将待合成文本替换为对应格式即可。</p><ul><li>使用 SSML 时，需同时将 <code>enable_ssml</code> 设置为 <code>true</code>。支持的 SSML 标签及用法，请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-synthesis/ssml-latex-user-guide.md">SSML 与 LaTeX</a>。</li><li>使用 LaTeX 时，将待合成文本替换为 LaTeX 格式即可，无需额外配置。支持的 LaTeX 语法及用法，请参见<a href="https://help.aliyun.com/zh/model-studio/latex-capability-support-description">LaTeX 公式转语音</a>。</li></ul></td></tr><tr><td>voice(String)</td><td><code>String</code></td><td>是</td><td>音色。<p>取值范围：</p><ul><li>系统音色：参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-synthesis/tts-voice-list/qwen-audio-tts-voice-list.md">Qwen-Audio-TTS音色列表</a></li><li>声音复刻音色：如何创建音色请参见<a href="voice-clone-design-http-api-b6a5abbe2d5d2730.md">声音复刻HTTP API参考</a></li><li>声音设计音色：如何创建音色请参见<a href="../model-api-reference/voice-customization-api-directory/voice-design-api-references.md">声音设计API参考</a></li></ul></td></tr><tr><td>format(String)</td><td><code>String</code></td><td>否</td><td>音频编码格式。<p>默认值：mp3。</p><p>取值范围：</p><ul><li>mp3</li><li>pcm</li><li>wav</li><li>opus</li></ul></td></tr><tr><td>sampleRate(int)</td><td><code>int</code></td><td>否</td><td>音频采样率（Hz）。<p>取值范围：8000, 16000, 22050（默认）, 24000, 44100, 48000。</p></td></tr><tr><td>volume(int)</td><td><code>int</code></td><td>否</td><td>音量。<p>默认值：50。</p><p>取值范围：[0, 100]。</p></td></tr><tr><td>rate(float)</td><td><code>float</code></td><td>否</td><td>语速。<p>默认值：1.0。</p><p>取值范围：[0.5, 2.0]。</p></td></tr><tr><td>pitch(float)</td><td><code>float</code></td><td>否</td><td>音调。<p>默认值：1.0。</p><p>取值范围：[0.5, 2.0]。</p></td></tr><tr><td><code>enable_ssml</code></td><td><code>boolean</code></td><td>否</td><td>是否开启SSML功能。设置为<code>true</code>时，<code>text</code>参数需传入SSML格式文本。支持的SSML标签及用法，请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-synthesis/ssml-latex-user-guide.md">SSML 与 LaTeX</a>。SSML 的使用限制（支持的模型、音色和接口），请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-synthesis/ssml-latex-user-guide.md#sl01_constraint_h3">使用限制</a>。<p>默认值：false。</p><p><code>enable_ssml</code>需要通过<code>HttpSpeechSynthesisParam</code>实例的<code>parameter</code>方法或者<code>parameters</code>方法进行设置：</p><a id="fig-code-group"></a><div><a id="fig-code-group-通过parameter设置-tab"></a>通过parameter设置<div><a id="code-code-group-通过parameter设置"></a><pre class="language-java"><code>HttpSpeechSynthesisParam param = HttpSpeechSynthesisParam.builder()
    .model(&quot;qwen-audio-3.0-tts-flash&quot;)
    .text(&quot;&lt;speak&gt;你好&lt;/speak&gt;&quot;)
    .voice(&quot;longanhuan_v3.6&quot;)
    .parameter(&quot;enable_ssml&quot;, true)
    .build();
</code></pre></div><a id="fig-code-group-通过parameters设置-tab"></a>通过parameters设置<div><a id="code-code-group-通过parameters设置"></a><pre class="language-java"><code>HttpSpeechSynthesisParam param = HttpSpeechSynthesisParam.builder()
    .model(&quot;qwen-audio-3.0-tts-flash&quot;)
    .text(&quot;&lt;speak&gt;你好&lt;/speak&gt;&quot;)
    .voice(&quot;longanhuan_v3.6&quot;)
    .parameters(Collections.singletonMap(&quot;enable_ssml&quot;, true))
    .build();
</code></pre></div></div></td></tr><tr><td><code>word_timestamp_enabled</code></td><td><code>boolean</code></td><td>否</td><td>是否开启字级别时间戳。<p>默认值：false。</p><p>仅在流式输出模式下可用。支持复刻音色；支持的系统音色请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-synthesis/tts-voice-list/qwen-audio-tts-voice-list.md">Qwen-Audio-TTS音色列表</a>。</p><p><code>word_timestamp_enabled</code>需要通过<code>HttpSpeechSynthesisParam</code>实例的<code>parameter</code>方法或者<code>parameters</code>方法进行设置：</p><a id="fig-code-group-2"></a><div><a id="fig-code-group-2-通过parameter设置-tab"></a>通过parameter设置<div><a id="code-code-group-2-通过parameter设置"></a><pre class="language-java"><code>HttpSpeechSynthesisParam param = HttpSpeechSynthesisParam.builder()
    .model(&quot;qwen-audio-3.0-tts-flash&quot;)
    .text(&quot;我家的后面有一个很大的花园。&quot;)
    .voice(&quot;longanhuan_v3.6&quot;)
    .parameter(&quot;word_timestamp_enabled&quot;, true)
    .build();
</code></pre></div><a id="fig-code-group-2-通过parameters设置-tab"></a>通过parameters设置<div><a id="code-code-group-2-通过parameters设置"></a><pre class="language-java"><code>HttpSpeechSynthesisParam param = HttpSpeechSynthesisParam.builder()
    .model(&quot;qwen-audio-3.0-tts-flash&quot;)
    .text(&quot;我家的后面有一个很大的花园。&quot;)
    .voice(&quot;longanhuan_v3.6&quot;)
    .parameters(Collections.singletonMap(&quot;word_timestamp_enabled&quot;, true))
    .build();
</code></pre></div></div></td></tr><tr><td><code>seed</code></td><td><code>int</code></td><td>否</td><td>生成时使用的随机数种子，使合成的效果产生变化。在模型版本、文本、音色及其他参数均相同的前提下，使用相同的seed可复现相同的合成结果。<p>默认值0。</p><p>取值范围：[0, 65535]。</p><p><code>seed</code>需要通过<code>HttpSpeechSynthesisParam</code>实例的<code>parameter</code>方法或者<code>parameters</code>方法进行设置：</p><a id="fig-code-group-3"></a><div><a id="fig-code-group-3-通过parameter设置-tab"></a>通过parameter设置<div><a id="code-code-group-3-通过parameter设置"></a><pre class="language-java"><code>HttpSpeechSynthesisParam param = HttpSpeechSynthesisParam.builder()
    .model(&quot;qwen-audio-3.0-tts-flash&quot;)
    .text(&quot;我家的后面有一个很大的花园。&quot;)
    .voice(&quot;longanhuan_v3.6&quot;)
    .parameter(&quot;seed&quot;, 1234)
    .build();
</code></pre></div><a id="fig-code-group-3-通过parameters设置-tab"></a>通过parameters设置<div><a id="code-code-group-3-通过parameters设置"></a><pre class="language-java"><code>HttpSpeechSynthesisParam param = HttpSpeechSynthesisParam.builder()
    .model(&quot;qwen-audio-3.0-tts-flash&quot;)
    .text(&quot;我家的后面有一个很大的花园。&quot;)
    .voice(&quot;longanhuan_v3.6&quot;)
    .parameters(Collections.singletonMap(&quot;seed&quot;, 1234))
    .build();
</code></pre></div></div></td></tr><tr><td><code>language_hints</code></td><td><code>List</code></td><td>否</td><td><div><div><p><strong>重要</strong></p><ul><li>此参数为数组，但当前版本仅处理第一个元素，因此建议只传入一个值。</li><li>此参数用于指定语音合成的目标语言，该设置与声音复刻时的样本音频的语种无关。如需设置复刻任务的源语言，请参见<a href="voice-clone-design-http-api-b6a5abbe2d5d2730.md#h2-create">声音复刻API参考</a>。</li></ul></div></div><p>指定语音合成的目标语言，提升合成效果。</p><p>当数字、缩写、符号等朗读方式或者小语种合成效果不符合预期时使用，例如：</p><ul><li>数字朗读方式不符合预期，“hello, this is 110”读成“hello, this is one one zero”而非“hello, this is 幺幺零”</li><li>符号朗读不准确，“@”读成“艾特”而非“at”</li><li>小语种合成效果差，合成不自然</li></ul><a id="accordion-取值范围"></a><section><p>取值范围</p><div><ul><li><p>zh：中文</p></li><li><p>en：英语</p></li><li><p>fr：法语</p></li><li><p>de：德语</p></li><li><p>ja：日语</p></li><li><p>ko：韩语</p></li><li><p>ru：俄语</p></li><li><p>pt：葡萄牙语</p></li><li><p>th：泰语</p></li><li><p>id：印尼语</p></li><li><p>vi：越南语</p></li><li><p>es：西班牙语</p></li><li><p>it：意大利语</p></li><li><p>ms：马来西亚语</p></li><li><p>fil：菲律宾语</p></li><li><p>ar：阿拉伯语</p></li><li><p>other：其他语种（适用于 <code>qwen-audio-3.1-tts-flash</code>）</p><p>保加利亚语、荷兰语、匈牙利语、罗马尼亚语、丹麦语、克罗地亚语、希腊语、捷克语、挪威语、瑞典语、印地语、斯洛伐克语、芬兰语、乌尔都语、塞尔维亚语、墨西哥西班牙语、立陶宛语、拉脱维亚语、土耳其语、波斯语、希伯来语、蒙古语、斯洛文尼亚语、阿塞拜疆语、波兰语、加泰罗尼亚语、高棉语、巴西葡萄牙语、老挝语、格鲁吉亚语、南非荷兰语、尼泊尔语、白俄罗斯语、马拉雅拉姆语、卢森堡语、阿尔巴尼亚语、泰米尔语、僧伽罗语、泰卢固语、爱沙尼亚语、宿务语、波斯尼亚语、缅甸语、亚美尼亚语、拉丁语、冰岛语、马耳他语、斯瓦希里语、哈萨克语、塞舌尔克里奥尔语、乌克兰语。</p></li></ul></div></section><p><code>language_hints</code>需要通过<code>HttpSpeechSynthesisParam</code>实例的<code>parameter</code>方法或者<code>parameters</code>方法进行设置：</p><a id="fig-code-group-4"></a><div><a id="fig-code-group-4-通过parameter设置-tab"></a>通过parameter设置<div><a id="code-code-group-4-通过parameter设置"></a><pre class="language-java"><code>HttpSpeechSynthesisParam param = HttpSpeechSynthesisParam.builder()
    .model(&quot;qwen-audio-3.0-tts-flash&quot;)
    .text(&quot;我家的后面有一个很大的花园。&quot;)
    .voice(&quot;longanhuan_v3.6&quot;)
    .parameter(&quot;language_hints&quot;, Arrays.asList(&quot;zh&quot;))
    .build();
</code></pre></div><a id="fig-code-group-4-通过parameters设置-tab"></a>通过parameters设置<div><a id="code-code-group-4-通过parameters设置"></a><pre class="language-java"><code>HttpSpeechSynthesisParam param = HttpSpeechSynthesisParam.builder()
    .model(&quot;qwen-audio-3.0-tts-flash&quot;)
    .text(&quot;我家的后面有一个很大的花园。&quot;)
    .voice(&quot;longanhuan_v3.6&quot;)
    .parameters(Collections.singletonMap(&quot;language_hints&quot;, Arrays.asList(&quot;zh&quot;)))
    .build();
</code></pre></div></div></td></tr><tr><td><code>instruction</code></td><td><code>String</code></td><td>否</td><td>设置指令，用于控制方言、情感或角色等合成效果。<p>具体用法请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-synthesis/non-realtime-tts-user-guide.md">非实时语音合成</a>。</p><p><code>instruction</code>需要通过<code>HttpSpeechSynthesisParam</code>实例的<code>parameter</code>方法或者<code>parameters</code>方法进行设置：</p><a id="fig-code-group-5"></a><div><a id="fig-code-group-5-通过parameter设置-tab"></a>通过parameter设置<div><a id="code-code-group-5-通过parameter设置"></a><pre class="language-java"><code>HttpSpeechSynthesisParam param = HttpSpeechSynthesisParam.builder()
    .model(&quot;qwen-audio-3.0-tts-flash&quot;)
    .text(&quot;我家的后面有一个很大的花园。&quot;)
    .voice(&quot;longanhuan_v3.6&quot;)
    .parameter(&quot;instruction&quot;, &quot;请用非常开心的语气说话。&quot;)
    .build();
</code></pre></div><a id="fig-code-group-5-通过parameters设置-tab"></a>通过parameters设置<div><a id="code-code-group-5-通过parameters设置"></a><pre class="language-java"><code>HttpSpeechSynthesisParam param = HttpSpeechSynthesisParam.builder()
    .model(&quot;qwen-audio-3.0-tts-flash&quot;)
    .text(&quot;我家的后面有一个很大的花园。&quot;)
    .voice(&quot;longanhuan_v3.6&quot;)
    .parameters(Collections.singletonMap(&quot;instruction&quot;, &quot;请用非常开心的语气说话。&quot;))
    .build();
</code></pre></div></div></td></tr><tr><td><code>bit_rate</code></td><td><code>int</code></td><td>否</td><td>音频码率（单位：kbps）。<p>默认值：32。</p><p>取值范围：[6, 510]。</p><div><div><p><strong>重要</strong>仅在<code>format</code>为<code>opus</code>时支持使用该参数。</p></div></div><p><code>bit_rate</code>需要通过<code>HttpSpeechSynthesisParam</code>实例的<code>parameter</code>方法或者<code>parameters</code>方法进行设置：</p><a id="fig-code-group-6"></a><div><a id="fig-code-group-6-通过parameter设置-tab"></a>通过parameter设置<div><a id="code-code-group-6-通过parameter设置"></a><pre class="language-java"><code>HttpSpeechSynthesisParam param = HttpSpeechSynthesisParam.builder()
    .model(&quot;qwen-audio-3.0-tts-flash&quot;)
    .text(&quot;我家的后面有一个很大的花园。&quot;)
    .voice(&quot;longanhuan_v3.6&quot;)
    .format(&quot;opus&quot;)
    .parameter(&quot;bit_rate&quot;, 32)
    .build();
</code></pre></div><a id="fig-code-group-6-通过parameters设置-tab"></a>通过parameters设置<div><a id="code-code-group-6-通过parameters设置"></a><pre class="language-java"><code>HttpSpeechSynthesisParam param = HttpSpeechSynthesisParam.builder()
    .model(&quot;qwen-audio-3.0-tts-flash&quot;)
    .text(&quot;我家的后面有一个很大的花园。&quot;)
    .voice(&quot;longanhuan_v3.6&quot;)
    .format(&quot;opus&quot;)
    .parameters(Collections.singletonMap(&quot;bit_rate&quot;, 32))
    .build();
</code></pre></div></div></td></tr><tr><td><code>enable_aigc_tag</code></td><td><code>boolean</code></td><td>否</td><td>是否在生成的音频中添加AIGC隐性标识。设置为true时，会将隐性标识嵌入到支持格式（wav/mp3/opus）的音频中。<p>默认值：false。</p><p><code>enable_aigc_tag</code>需要通过<code>HttpSpeechSynthesisParam</code>实例的<code>parameter</code>方法或者<code>parameters</code>方法进行设置：</p><a id="fig-code-group-7"></a><div><a id="fig-code-group-7-通过parameter设置-tab"></a>通过parameter设置<div><a id="code-code-group-7-通过parameter设置"></a><pre class="language-java"><code>HttpSpeechSynthesisParam param = HttpSpeechSynthesisParam.builder()
    .model(&quot;qwen-audio-3.0-tts-flash&quot;)
    .text(&quot;我家的后面有一个很大的花园。&quot;)
    .voice(&quot;longanhuan_v3.6&quot;)
    .parameter(&quot;enable_aigc_tag&quot;, true)
    .build();
</code></pre></div><a id="fig-code-group-7-通过parameters设置-tab"></a>通过parameters设置<div><a id="code-code-group-7-通过parameters设置"></a><pre class="language-java"><code>HttpSpeechSynthesisParam param = HttpSpeechSynthesisParam.builder()
    .model(&quot;qwen-audio-3.0-tts-flash&quot;)
    .text(&quot;我家的后面有一个很大的花园。&quot;)
    .voice(&quot;longanhuan_v3.6&quot;)
    .parameters(Collections.singletonMap(&quot;enable_aigc_tag&quot;, true))
    .build();
</code></pre></div></div></td></tr><tr><td><code>aigc_propagator</code></td><td><code>String</code></td><td>否</td><td>设置AIGC隐性标识中的 <code>ContentPropagator</code> 字段，用于标识内容的传播者。仅在 <code>enable_aigc_tag</code> 为 <code>true</code> 时生效。<p>默认值：阿里云UID。</p><p><code>aigc_propagator</code>需要通过<code>HttpSpeechSynthesisParam</code>实例的<code>parameter</code>方法或者<code>parameters</code>方法进行设置：</p><a id="fig-code-group-8"></a><div><a id="fig-code-group-8-通过parameter设置-tab"></a>通过parameter设置<div><a id="code-code-group-8-通过parameter设置"></a><pre class="language-java"><code>HttpSpeechSynthesisParam param = HttpSpeechSynthesisParam.builder()
    .model(&quot;qwen-audio-3.0-tts-flash&quot;)
    .text(&quot;我家的后面有一个很大的花园。&quot;)
    .voice(&quot;longanhuan_v3.6&quot;)
    .parameter(&quot;enable_aigc_tag&quot;, true)
    .parameter(&quot;aigc_propagator&quot;, &quot;xxxx&quot;)
    .build();
</code></pre></div><a id="fig-code-group-8-通过parameters设置-tab"></a>通过parameters设置<div><a id="code-code-group-8-通过parameters设置"></a><pre class="language-java"><code>Map&lt;String, Object&gt; map = new HashMap&lt;&gt;();
map.put(&quot;enable_aigc_tag&quot;, true);
map.put(&quot;aigc_propagator&quot;, &quot;xxxx&quot;);

HttpSpeechSynthesisParam param = HttpSpeechSynthesisParam.builder()
    .model(&quot;qwen-audio-3.0-tts-flash&quot;)
    .text(&quot;我家的后面有一个很大的花园。&quot;)
    .voice(&quot;longanhuan_v3.6&quot;)
    .parameters(map)
    .build();
</code></pre></div></div></td></tr><tr><td><code>aigc_propagate_id</code></td><td><code>String</code></td><td>否</td><td>设置AIGC隐性标识中的 <code>PropagateID</code> 字段，用于唯一标识一次具体的传播行为。仅在 <code>enable_aigc_tag</code> 为 <code>true</code> 时生效。<p>默认值：本次语音合成请求Request ID。</p><p><code>aigc_propagate_id</code>需要通过<code>HttpSpeechSynthesisParam</code>实例的<code>parameter</code>方法或者<code>parameters</code>方法进行设置：</p><a id="fig-code-group-9"></a><div><a id="fig-code-group-9-通过parameter设置-tab"></a>通过parameter设置<div><a id="code-code-group-9-通过parameter设置"></a><pre class="language-java"><code>HttpSpeechSynthesisParam param = HttpSpeechSynthesisParam.builder()
    .model(&quot;qwen-audio-3.0-tts-flash&quot;)
    .text(&quot;我家的后面有一个很大的花园。&quot;)
    .voice(&quot;longanhuan_v3.6&quot;)
    .parameter(&quot;enable_aigc_tag&quot;, true)
    .parameter(&quot;aigc_propagate_id&quot;, &quot;xxxx&quot;)
    .build();
</code></pre></div><a id="fig-code-group-9-通过parameters设置-tab"></a>通过parameters设置<div><a id="code-code-group-9-通过parameters设置"></a><pre class="language-java"><code>Map&lt;String, Object&gt; map = new HashMap&lt;&gt;();
map.put(&quot;enable_aigc_tag&quot;, true);
map.put(&quot;aigc_propagate_id&quot;, &quot;xxxx&quot;);

HttpSpeechSynthesisParam param = HttpSpeechSynthesisParam.builder()
    .model(&quot;qwen-audio-3.0-tts-flash&quot;)
    .text(&quot;我家的后面有一个很大的花园。&quot;)
    .voice(&quot;longanhuan_v3.6&quot;)
    .parameters(map)
    .build();
</code></pre></div></div></td></tr><tr><td><code>hot_fix</code></td><td><code>Map</code></td><td>否</td><td>文本热修复配置，用于自定义指定词语的发音或对待合成文本进行替换。<p>参数介绍：</p><ul><li>pronunciation：自定义发音。指定词语的拼音标注，用于纠正默认发音不准确的情况。</li><li>replace：文本替换。在语音合成前将指定词语替换为目标文本，替换后的文本将作为实际合成内容。</li></ul><p>示例：</p><a id="code-block-5"></a><pre class="language-json"><code>&quot;hot_fix&quot;: {
  &quot;pronunciation&quot;: [
    {&quot;天气&quot;: &quot;tian1 qi4&quot;}
  ],
  &quot;replace&quot;: [
    {&quot;今天&quot;: &quot;金天&quot;}
  ]
}
</code></pre><p><code>hot_fix</code>需要通过<code>HttpSpeechSynthesisParam</code>实例的<code>parameter</code>方法或者<code>parameters</code>方法进行设置：</p><a id="fig-code-group-10"></a><div><a id="fig-code-group-10-通过parameter设置-tab"></a>通过parameter设置<div><a id="code-code-group-10-通过parameter设置"></a><pre class="language-java"><code>Map&lt;String, Object&gt; hotFix = new HashMap&lt;&gt;();

List&lt;Map&lt;String, String&gt;&gt; pronunciation = new ArrayList&lt;&gt;();
Map&lt;String, String&gt; pronItem = new HashMap&lt;&gt;();
pronItem.put(&quot;天气&quot;, &quot;tian1 qi4&quot;);
pronunciation.add(pronItem);
hotFix.put(&quot;pronunciation&quot;, pronunciation);

List&lt;Map&lt;String, String&gt;&gt; replace = new ArrayList&lt;&gt;();
Map&lt;String, String&gt; replaceItem = new HashMap&lt;&gt;();
replaceItem.put(&quot;今天&quot;, &quot;金天&quot;);
replace.add(replaceItem);
hotFix.put(&quot;replace&quot;, replace);

HttpSpeechSynthesisParam param = HttpSpeechSynthesisParam.builder()
    .model(&quot;qwen-audio-3.0-tts-flash&quot;)
    .text(&quot;今天天气真好。&quot;)
    .voice(&quot;longanhuan_v3.6&quot;)
    .parameter(&quot;hot_fix&quot;, hotFix)
    .build();
</code></pre></div><a id="fig-code-group-10-通过parameters设置-tab"></a>通过parameters设置<div><a id="code-code-group-10-通过parameters设置"></a><pre class="language-java"><code>// 构建hotFix对象同上
HttpSpeechSynthesisParam param = HttpSpeechSynthesisParam.builder()
    .model(&quot;qwen-audio-3.0-tts-flash&quot;)
    .text(&quot;今天天气真好。&quot;)
    .voice(&quot;longanhuan_v3.6&quot;)
    .parameters(Collections.singletonMap(&quot;hot_fix&quot;, hotFix))
    .build();
</code></pre></div></div></td></tr><tr><td><p><code>enable_markdown_filter</code></p></td><td><p><code>boolean</code></p></td><td><p>否</p></td><td><p>是否启用 Markdown 过滤。启用后，服务会在合成前将 Markdown 转换成适合朗读的文本。</p><p>默认值：<code>false</code>。设为 <code>true</code> 启用。</p><p>通过 <code>parameter(&quot;enable_markdown_filter&quot;, true)</code> 启用。</p></td></tr></tbody></table>

<a id="示例代码"></a>

<a id="h2-cv4a5b6b"></a>

## 示例代码

以下示例展示Qwen-Audio-TTS语音合成的非流式和流式调用方式。运行前请确保已设置环境变量`DASHSCOPE_API_KEY`。

> **重要**
>
> 不同模型需使用匹配的音色。更换模型时，请同步更换音色，并确认音色支持目标语言。具体对应关系请参见[Qwen-Audio-TTS音色列表](../model-user-guide/model-experience/speech-and-audio/speech-synthesis/tts-voice-list/qwen-audio-tts-voice-list.md)。

<a id="sec-tabs"></a>

<a id="非流式调用"></a>

<a id="非流式调用-h4"></a>

#### 非流式调用

<a id="h3-cv4a5b7b"></a>

非流式调用会等待服务端合成完成后一次性返回结果。根据返回类型的不同，提供以下两种方式：

-   `callAndReturnAudio()`：返回音频二进制数据（ByteBuffer），适用于直接保存或处理音频的场景。
-   `call()`：返回音频URL，适用于需要通过URL下载音频的场景。

<a id="code-block-6"></a>

```java
import com.alibaba.dashscope.audio.http_tts.AudioInfo;
import com.alibaba.dashscope.audio.http_tts.HttpSpeechSynthesisParam;
import com.alibaba.dashscope.audio.http_tts.HttpSpeechSynthesisResult;
import com.alibaba.dashscope.audio.http_tts.HttpSpeechSynthesizer;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;

import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.ByteBuffer;

public class QwenAudioTtsSyncExample {
    static {
        // 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    /**
     * 非流式调用示例一：返回音频数据（ByteBuffer）
     * 调用callAndReturnAudio方法，阻塞等待合成完成后返回完整音频数据。
     */
    public static void syncCallReturnAudio() {
        HttpSpeechSynthesizer synthesizer = new HttpSpeechSynthesizer();

        HttpSpeechSynthesisParam param =
            HttpSpeechSynthesisParam.builder()
                .model("qwen-audio-3.0-tts-flash")  // 更换模型时，需同步更换为对应版本的音色
                .text("我家的后面有一个很大的花园。")
                .voice("longanhuan_v3.6")
                .format("wav")
                .sampleRate(24000)
                // 未配置环境变量时，将下行替换为：apiKey("sk-xxx")，即替换为实际的API Key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                // 通过parameter方法设置额外参数
                // .parameter("seed", 1234)
                // .parameter("enable_ssml", true)
                .build();

        try {
            ByteBuffer audioData = synthesizer.callAndReturnAudio(param);
            if (audioData != null && audioData.hasRemaining()) {
                byte[] bytes = new byte[audioData.remaining()];
                audioData.get(bytes);

                try (FileOutputStream fos = new FileOutputStream("sync_output.wav")) {
                    fos.write(bytes);
                    System.out.println("Audio saved to sync_output.wav, size: " + bytes.length + " bytes");
                } catch (IOException e) {
                    System.err.println("Failed to save audio: " + e.getMessage());
                }
            }
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.err.println("Synthesis failed: " + e.getMessage());
        }
        System.exit(0);
    }

    /**
     * 非流式调用示例二：返回音频URL
     * 调用call方法，返回包含音频URL的结果对象，可通过URL下载音频文件。
     */
    public static void syncCallReturnUrl() {
        HttpSpeechSynthesizer synthesizer = new HttpSpeechSynthesizer();

        HttpSpeechSynthesisParam param =
            HttpSpeechSynthesisParam.builder()
                .model("qwen-audio-3.0-tts-flash")  // 更换模型时，需同步更换为对应版本的音色
                .text("我家的后面有一个很大的花园。")
                .voice("longanhuan_v3.6")
                .format("wav")
                .sampleRate(24000)
                // 未配置环境变量时，将下行替换为：apiKey("sk-xxx")，即替换为实际的API Key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .build();

        try {
            HttpSpeechSynthesisResult result = synthesizer.call(param);
            System.out.println("Request ID: " + result.getRequestId());

            if (result.hasAudioUrl()) {
                AudioInfo audioInfo = result.getAudioInfo();
                System.out.println("Audio URL: " + audioInfo.getUrl());
                System.out.println("Expires At: " + audioInfo.getExpiresAt());
                System.out.println("Remaining Time: " + audioInfo.getRemainingSeconds() + " seconds");
            }
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.err.println("Synthesis failed: " + e.getMessage());
        }
    }

    public static void main(String[] args) {
        // 非流式调用示例一：返回音频数据（ByteBuffer）
        // syncCallReturnAudio();
        // 非流式调用示例二：返回音频URL
        syncCallReturnUrl();
    }
}
```

<a id="流式调用"></a>

<a id="流式调用-h4"></a>

#### 流式调用

<a id="h3-cv4a5b8b"></a>

流式调用通过回调函数分片返回音频数据，无需等待合成完成即可开始处理，适用于对首包延迟有要求的实时播放场景。

<a id="code-block-7"></a>

```java
import com.alibaba.dashscope.audio.http_tts.HttpSpeechSynthesisParam;
import com.alibaba.dashscope.audio.http_tts.HttpSpeechSynthesisResult;
import com.alibaba.dashscope.audio.http_tts.HttpSpeechSynthesizer;
import com.alibaba.dashscope.common.ResultCallback;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;

import java.io.FileOutputStream;
import java.io.IOException;
import java.util.concurrent.CountDownLatch;

public class QwenAudioTtsStreamExample {
    static {
        // 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    public static void streamCallWithCallback() {
        HttpSpeechSynthesizer synthesizer = new HttpSpeechSynthesizer();

        HttpSpeechSynthesisParam param =
                HttpSpeechSynthesisParam.builder()
                        .model("qwen-audio-3.0-tts-flash")  // 更换模型时，需同步更换为对应版本的音色
                        .text("今天天气真好，适合出去玩。")
                        .voice("longanhuan_v3.6")
                        .format("wav")
                        .sampleRate(24000)
                        // 未配置环境变量时，将下行替换为：apiKey("sk-xxx")，即替换为实际的API Key
                        .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                        .build();

        CountDownLatch latch = new CountDownLatch(1);

        // 新增：创建输出文件流
        try (FileOutputStream fos = new FileOutputStream("output.wav")) {

            synthesizer.streamCall(param,
                    new ResultCallback<HttpSpeechSynthesisResult>() {
                        private int chunkCount = 0;

                        @Override
                        public void onEvent(HttpSpeechSynthesisResult result) {
                            chunkCount++;
                            if (result.hasAudioData()) {
                                System.out.println("Received chunk #" + chunkCount
                                        + ", size: " + result.getAudioDataSize() + " bytes");
                                try {
                                    fos.write(result.getAudioData());
                                } catch (IOException e) {
                                    System.err.println("Failed to write audio data: " + e.getMessage());
                                }
                            }
                            if (result.getRequestId() != null) {
                                System.out.println("Request ID: " + result.getRequestId());
                            }
                        }

                        @Override
                        public void onComplete() {
                            System.out.println("Synthesis completed, total chunks: " + chunkCount);
                            System.out.println("Audio saved to output.wav");
                            latch.countDown();
                        }

                        @Override
                        public void onError(Exception e) {
                            System.err.println("Error during synthesis: " + e.getMessage());
                            latch.countDown();
                        }
                    });

            latch.await();

        } catch (ApiException | NoApiKeyException | InputRequiredException | InterruptedException e) {
            System.err.println("Failed: " + e.getMessage());
        } catch (IOException e) {
            System.err.println("Failed to create output file: " + e.getMessage());
        }
    }

    public static void main(String[] args) {
        streamCallWithCallback();
        System.exit(0);
    }
}
```
