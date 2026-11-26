# Paraformer非实时语音识别Android SDK

本文档提供了Paraformer非实时语音识别Android SDK的详细使用指南，帮助您将语音转换为文本。

**用户指南：**[非实时语音识别](../model-user-guide/model-experience/speech-and-audio/speech-recognition/non-realtime-speech-recognition-user-guide.md)

<a id="快速开始"></a>

<a id="abf215f434v5x"></a>

## 快速开始

1.  **获取API Key：**[获取与配置 API Key](../model-api-reference/preparations/get-api-key.md)，为安全起见，推荐将API Key配置到环境变量。
    
    > **说明**
    >
    > 当需要为第三方应用或用户提供临时访问权限，或者希望严格控制敏感数据访问、删除等高风险操作时，建议使用[临时API Key](../model-api-reference/more-about-models/generate-temporary-api-key.md)。临时API Key默认拥有60秒有效期，过期后需重新获取。
    
2.  **下载SDK并运行示例代码：**
    -   [下载最新SDK整合包](../model-api-reference/more-about-models/sdk-selection-and-download.md)。
    -   解压 ZIP 包。在 `app/libs` 目录中获取 AAR 格式 SDK，并添加到项目依赖。  
        需要 Android CPP 接入时，使用 ZIP 包内的 `android_libs` 与 `android_include` 获取动态库和头文件。  
          
        
    -   用 Android Studio 打开工程。示例代码位于`DashParaformerFileTranscriberActivity.java`，替换 API Key 后体验功能。

<a id="调用步骤"></a>

<a id="0701a2d0b75vm"></a>

### 调用步骤

<a id="sec-tabs"></a>

<a id="同步模式"></a>

<a id="同步模式-h4"></a>

#### 同步模式

1.  初始化 SDK
2.  按业务需求配置相关参数
3.  调用 `startFileTranscriber` 启动识别任务（`async_request`设为`false`）
4.  在`onFileTransEventCallback`接口中监听`EVENT_FILE_TRANS_RESULT` 事件，获取最终识别结果
5.  调用 `release` 释放 SDK 资源

<a id="异步模式"></a>

<a id="异步模式-h4"></a>

#### 异步模式

1.  初始化 SDK
2.  按业务需求配置相关参数
3.  调用 `startFileTranscriber` 启动识别任务（`async_request`设为`true`）
4.  调用 `queryFileTranscriber` 主动查询识别进度/结果
5.  在`onFileTransEventCallback`接口中监听`EVENT_FILE_TRANS_QUERY_RESULT`事件，获取当前查询结果
6.  在`onFileTransEventCallback`接口中监听 `EVENT_FILE_TRANS_RESULT` 事件，获取最终识别结果
7.  调用 `release` 释放 SDK 资源

<a id="请求参数"></a>

<a id="a96bfa6340jdd"></a>

## 请求参数

<a id="连接与控制参数"></a>

<a id="57acf5ecc1w8j"></a>

### 连接与控制参数

通过在[initialize](paraformer-recorded-speech-recognition-android-s-13e83d144d148a4f.md#ae6d7dd9cfad3)接口的`parameters`参数中传入一个JSON字符串来配置。

-   **参数示例：**以下为 JSON 字符串示例，参数未完整列出。请按实际需求在编码时补充：

<a id="code-block"></a>

```json
{
    "url": "wss://dashscope.aliyuncs.com/api-ws/v1/inference",
    "apikey": "st-****",
    "device_id": "my_device_id",
    "service_mode": "1"
}
```

-   **参数说明**
    
    <table><thead><tr><th><p><strong>参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>是否必须</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p><code>url</code></p></td><td><p><code>String</code></p></td><td><p>是</p></td><td><p>服务地址，固定为 <code>wss://dashscope.aliyuncs.com/api-ws/v1/inference</code>。</p></td></tr><tr><td><p><code>apikey</code></p></td><td><p><code>String</code></p></td><td><p>是</p></td><td><p>API Key。建议使用时效性短、安全性更高的<a href="../model-api-reference/more-about-models/generate-temporary-api-key.md">临时API Key</a>，以降低长期有效Key泄露的风险。</p></td></tr><tr><td><p><code>service_mode</code></p></td><td><p><code>String</code></p></td><td><p>是</p></td><td><p>运行模式。非实时语音识别固定为 <code>&quot;1&quot;</code>。</p></td></tr><tr><td><p><code>device_id</code></p></td><td><p><code>String</code></p></td><td><p>是</p></td><td><p>用于标识终端用户的唯一字符串，可设为应用内用户ID或客户端生成的设备唯一标识符。此ID主要用于日志追踪和问题排查。</p></td></tr><tr><td><p><code>debug_path</code></p></td><td><p><code>String</code></p></td><td><p>否</p></td><td><p>日志文件的存储路径。</p><p>此参数仅在调用<a href="paraformer-recorded-speech-recognition-android-s-13e83d144d148a4f.md#ae6d7dd9cfad3">initialize</a>接口时将<code>save_log</code>设为true时生效。此时必须设置日志文件路径，否则将报错。</p><p>本地最多保留两个日志文件。</p></td></tr><tr><td><p><code>max_log_file_size</code></p></td><td><p><code>int</code></p></td><td><p>否</p></td><td><p>设定日志文件的最大字节数。</p><p>此参数仅在调用<a href="paraformer-recorded-speech-recognition-android-s-13e83d144d148a4f.md#ae6d7dd9cfad3">initialize</a>接口时将<code>save_log</code>设为true时生效。</p><p>默认值：104857600（100 * 1024 * 1024 字节, 即 100MiB）。</p></td></tr><tr><td><p><code>log_track_level</code></p></td><td><p><code>int</code></p></td><td><p>否</p></td><td><p>控制通过日志回调（<code>onFileTransLogTrackCallback</code>）对外发送的日志内容的过滤级别。</p><p>默认值：2。</p><p>取值范围：</p><ul><li><p>0：LOG_LEVEL_VERBOSE</p></li><li><p>1：LOG_LEVEL_DEBUG</p></li><li><p>2：LOG_LEVEL_INFO</p></li><li><p>3：LOG_LEVEL_WARNING</p></li><li><p>4：LOG_LEVEL_ERROR</p></li><li><p>5：LOG_LEVEL_NONE（表示关闭此功能）</p></li></ul><p>注意：<code>log_track_level</code>与<code>level</code>（通过<a href="paraformer-recorded-speech-recognition-android-s-13e83d144d148a4f.md#ae6d7dd9cfad3">initialize</a>接口设置）共同决定最终回调的日志。一条日志的级别数值必须同时大于或等于<code>log_track_level</code>和<code>level</code>的值，才会被回调。例如，<code>log_track_level</code>设为2 (INFO)，<code>level</code>设为3 (WARNING)，则只有WARNING及以上级别（数值&gt;=3）的日志才会被回调。</p></td></tr></tbody></table>
    

<a id="语音识别效果参数"></a>

<a id="d20cce9518kla"></a>

### 语音识别效果参数

通过setParams接口配置nl\_config参数，或者通过[startFileTranscriber](paraformer-recorded-speech-recognition-android-s-13e83d144d148a4f.md#7d33691bdb32v)接口配置所有语音识别效果参数。

-   **参数示例：**以下为 JSON 字符串示例，参数未完整列出。请按实际需求在编码时补充：

<a id="code-block-2"></a>

```json
{
    "file_urls": [
        "{YOUR_AUDIO_URL}"
    ],
    "async_request": false,
    "nls_config": {
        "model":"paraformer-v2",
        "disfluency_removal_enabled":false,
        "timestamp_alignment_enabled": false
    }
}
```

-   **参数说明**
    
    <table><thead><tr><th><strong>参数</strong></th><th><strong>类型</strong></th><th><strong>是否必须</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><p><code>file_urls</code></p></td><td><p><code>array[string]</code></p></td><td><p>是</p></td><td><p>音视频文件转写的URL列表，支持HTTP / HTTPS协议，单次请求仅支持1个URL。</p><p>若录音文件存储在阿里云OSS，使用SDK方式不支持使用以 oss://为前缀的临时 URL。</p><ul><li><p><strong>音频格式</strong>：<code>aac</code>、<code>amr</code>、<code>avi</code>、<code>flac</code>、<code>flv</code>、<code>m4a</code>、<code>mkv</code>、<code>mov</code>、<code>mp3</code>、<code>mp4</code>、<code>mpeg</code>、<code>ogg</code>、<code>opus</code>、<code>wav</code>、<code>webm</code>、<code>wma</code>、<code>wmv</code></p><div><div><p><strong>重要</strong>由于音视频格式及其变种众多，技术上无法穷尽测试，API不能保证所有格式均能够被正确识别。请通过测试验证您所提供的文件能够获得正常的语音识别结果。</p></div></div></li><li><strong>音频采样率</strong><p>因模型而异：</p><ul><li><p>paraformer-v2 支持任意采样率</p></li><li><p>paraformer-8k-v2 仅支持8kHz采样率</p></li></ul></li><li><p><strong>音频文件大小和时长</strong>：音频文件不超过2GB；时长在12小时以内。</p><p>如果希望处理的文件超过了上述限制，可尝试对文件进行预处理以降低文件尺寸。有关文件预处理的最佳实践可以查阅<a href="paraformer-best-practices-b5bb2777c9abaf3c.md#c5dda0a0cf2x9">预处理视频文件以提高文件转写效率（针对录音文件识别场景）</a>。</p></li></ul></td></tr><tr><td><p><code>async_request</code></p></td><td><p><code>boolean</code></p></td><td><p>否</p></td><td><p>语音识别是否为异步请求。</p><p>默认值：<code>false</code>。</p><p>取值范围：</p><ul><li>true：异步请求</li><li>false：同步请求</li></ul></td></tr><tr><td><p><code>apikey</code></p></td><td><p><code>string</code></p></td><td><p>否</p></td><td><p>如果<a href="paraformer-recorded-speech-recognition-android-s-13e83d144d148a4f.md#57acf5ecc1w8j">连接与控制参数</a>的<code>apikey</code>使用的是<a href="../model-api-reference/more-about-models/generate-temporary-api-key.md">临时API Key</a>，可在此处进行更新，以免超时失效。</p></td></tr><tr><td><p><code>nls_config</code></p></td><td><p><code>object</code></p></td><td><p>是</p></td><td><p>语音识别核心配置对象，包含模型选择、识别效果控制等关键参数。</p></td></tr><tr><td><p><code>nls_config.model</code></p></td><td><p><code>string</code></p></td><td><p>是</p></td><td><p>语音识别<a href="paraformer-recorded-speech-recognition-restful-a-8b487acdee52d08d.md">模型</a>。</p></td></tr><tr><td><p><code>nls_config.language_hints</code></p></td><td><p><code>array[string]</code></p></td><td><p>否</p></td><td><p>指定待识别语音的语言代码。该参数仅适用于paraformer-v2模型。</p><p>默认值：<code>[&quot;zh&quot;, &quot;en&quot;]</code>。</p><p>支持的语言代码：</p><ul><li>zh: 中文</li><li>en: 英文</li><li>ja: 日语</li><li>yue: 粤语</li><li>ko: 韩语</li><li>de：德语</li><li>fr：法语</li><li>ru：俄语</li></ul></td></tr><tr><td><p><code>nls_config.disfluency_removal_enabled</code></p></td><td><p><code>boolean</code></p></td><td><p>否</p></td><td><p>是否过滤语气词，如“嗯”、“啊”等。</p><p>默认值：false。</p><p>取值范围：</p><ul><li>true：过滤</li><li>false：不过滤</li></ul></td></tr><tr><td><p><code>nls_config.timestamp_alignment_enabled</code></p></td><td><p><code>boolean</code></p></td><td><p>否</p></td><td><p>是否启用时间戳校准功能。</p><p>默认值：false。</p><p>取值范围：</p><ul><li>true：开启</li><li>false：关闭</li></ul></td></tr><tr><td><p><code>nls_config.special_word_filter</code></p></td><td><p><code>object</code></p></td><td><p>否</p></td><td><p>指定在语音识别过程中需要处理的敏感词，并支持对不同敏感词设置不同的处理方式。</p><p>若未传入该参数，系统将启用系统内置的敏感词过滤逻辑，识别结果中与<a href="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/%E7%99%BE%E7%82%BC%E6%95%8F%E6%84%9F%E8%AF%8D%E5%88%97%E8%A1%A8_20230716.words.txt">阿里云百炼敏感词表</a>匹配的词语将被替换为等长的<code>*</code>。</p><p>若传入该参数，则可实现以下敏感词处理策略：</p><ul><li>替换为 <code>*</code>：将匹配的敏感词替换为等长的 <code>*</code>；</li><li>直接过滤：将匹配的敏感词从识别结果中完全移除。</li></ul><p>该参数的值应为一个 JSON Object，其结构如下所示：</p><a id="code-block-3"></a><pre class="language-json"><code>{
      &quot;filter_with_signed&quot;: {
        &quot;word_list&quot;: [&quot;测试&quot;]
      },
      &quot;filter_with_empty&quot;: {
        &quot;word_list&quot;: [&quot;开始&quot;, &quot;发生&quot;]
      },
      &quot;system_reserved_filter&quot;: true
    }
    </code></pre><p>JSON字段说明：</p><ul><li><p><code>filter_with_signed</code></p><ul><li><p>类型：对象。</p></li><li><p>是否必填：否。</p></li><li><p>描述：配置需替换为<code>*</code>的敏感词列表。识别结果中匹配的词语将被等长的 <code>*</code> 替代。</p></li><li><p>示例：以上述JSON为例，“帮我测试一下这段代码”的语音识别结果将会是“帮我**一下这段代码”。</p></li><li><p>内部字段：</p><ul><li><code>word_list</code>: 字符串数组，列出需被替换的敏感词。</li></ul></li></ul></li><li><p><code>filter_with_empty</code></p><ul><li><p>类型：对象。</p></li><li><p>是否必填：否。</p></li><li><p>描述：配置需从识别结果中移除（过滤）的敏感词列表。识别结果中匹配的词语将被完全删除。</p></li><li><p>示例：以上述JSON为例，“比赛这就要开始了吗？”的语音识别结果将会是“比赛这就要了吗”。</p></li><li><p>内部字段：</p><ul><li><code>word_list</code>: 字符串数组，列出需被完全移除（过滤）的敏感词。</li></ul></li></ul></li><li><p><code>system_reserved_filter</code></p><ul><li>类型：布尔值。</li><li>是否必填：否。</li><li>默认值：true。</li><li>描述：是否启用系统预置的敏感词规则。设为<code>true</code>时，将同时启用系统内置的敏感词过滤逻辑，识别结果中与<a href="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/%E7%99%BE%E7%82%BC%E6%95%8F%E6%84%9F%E8%AF%8D%E5%88%97%E8%A1%A8_20230716.words.txt">阿里云百炼敏感词表</a>匹配的词语将被替换为等长的<code>*</code>。</li></ul></li></ul></td></tr><tr><td><p><code>nls_config.channel_id</code></p></td><td><p><code>array[integer]</code></p></td><td><p>否</p></td><td><p>指定在多音轨音频文件中需要识别的音轨索引，索引从 0 开始。例如，[0] 表示识别第一个音轨，[0, 1] 表示同时识别第一和第二个音轨。如果省略此参数，则默认处理第一个音轨。</p><div><div><p><strong>重要</strong>指定的每一个音轨都将独立计费。例如，为单个文件请求 [0, 1] 会产生两笔独立的费用。</p></div></div><p>默认值：<code>[0]</code></p></td></tr><tr><td><p><code>nls_config.diarization_enabled</code></p></td><td><p><code>boolean</code></p></td><td><p>否</p></td><td><p>自动说话人分离，默认关闭。</p><p>仅适用于单声道音频，多声道音频不支持说话人分离。</p><p>启用该功能后，识别结果中将显示<code>speaker_id</code>字段，用于区分不同说话人。</p><div><div><p><strong>说明</strong>如果启用说话人分离功能，建议音频时长不超过2小时，否则可能导致识别失败或超时。</p></div></div><p>有关<code>speaker_id</code>的示例，请参见<a href="paraformer-recorded-speech-recognition-restful-a-8b487acdee52d08d.md#a9021178ccl7s">识别结果说明</a>。</p></td></tr><tr><td><p><code>nls_config.speaker_count</code></p></td><td><p><code>integer</code></p></td><td><p>否</p></td><td><p>说话人数量参考值。若要使用该功能，需将<code>diarization_enabled</code>设置为<code>true</code>。</p><p>默认自动判断说话人数量，如果配置此项，只能辅助算法尽量输出指定人数，无法保证一定会输出此人数。</p><p>取值范围：<code>[2, 100]</code>。该功能用于区分多个说话人，因此最少需要设置2。</p></td></tr><tr><td><p><code>nls_config.vocabulary_id</code></p></td><td><p><code>string</code></p></td><td><p>否</p></td><td><p>热词词表ID，用于提升特定词汇的识别准确率。该参数适用于v2及更高版本模型。热词的使用方法请参见<a href="../model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words.md">定制热词</a>。</p></td></tr></tbody></table>
    

<a id="关键接口"></a>

<a id="737b46fda6cbf"></a>

## 关键接口

<a id="nativenui"></a>

<a id="4bed3999d9kx0"></a>

### NativeNui

<a id="initialize"></a>

<a id="ae6d7dd9cfad3"></a>

#### initialize

初始化语音识别SDK实例。SDK为单例模式，在调用[release](paraformer-recorded-speech-recognition-android-s-13e83d144d148a4f.md#44bf12ed9a4g9)前禁止重复初始化。

此接口会引起阻塞，应在非UI线程调用。

-   **方法签名**

<a id="code-block-4"></a>

```java
public synchronized int initialize(final INativeFileTransCallback callback,
                                   String parameters,
                                   final Constants.LogLevel level,
                                   final boolean save_log)
```

-   **参数说明**
    
    | 参数 | 类型 | 说明 |
    | --- | --- | --- |
    | `callback` | `INativeFileTransCallback` | 事件和数据回调接口的实现。 |
    | `parameters` | `String` | JSON字符串，包含鉴权、连接和调试参数。参见[连接与控制参数](paraformer-recorded-speech-recognition-android-s-13e83d144d148a4f.md#57acf5ecc1w8j)。 |
    | `level` | `Constants.LogLevel` | 控制SDK自身日志的打印级别。 |
    | `save_log` | `boolean` | 是否保存本地日志。若为`true`，须在[连接与控制参数](paraformer-recorded-speech-recognition-android-s-13e83d144d148a4f.md#57acf5ecc1w8j)中通过`debug_path`指定路径，并可通过`max_log_file_size`设置文件大小。 |
    
-   **返回值说明**

<a id="setparams"></a>

<a id="a23e0d85d7ymt"></a>

#### setParams

此接口用于独立设置或更新 `nls_config` 参数。如果所有参数都在[startFileTranscriber](paraformer-recorded-speech-recognition-android-s-13e83d144d148a4f.md#7d33691bdb32v)中一次性提供，则无需调用此方法。

-   **方法签名**

<a id="code-block-5"></a>

```java
public synchronized int setParams(String params);
```

-   **参数说明**
    
    <table><thead><tr><th><strong>参数</strong></th><th><strong>类型</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><p><code>params</code></p></td><td><p><code>String</code></p></td><td><p><a href="paraformer-recorded-speech-recognition-android-s-13e83d144d148a4f.md#d20cce9518kla">语音识别效果参数</a>中的<code>nls_config</code>参数，<code>nls_config</code>之外的参数不支持通过该方法进行设置。</p><p>示例：</p><a id="code-block-6"></a><pre class="language-json"><code>{
        &quot;nls_config&quot;: {
            &quot;model&quot;:&quot;paraformer-v2&quot;,
            &quot;disfluency_removal_enabled&quot;:false,
            &quot;timestamp_alignment_enabled&quot;: false
        }
    }
    </code></pre></td></tr></tbody></table>
    
-   **返回值说明**

<a id="startfiletranscriber"></a>

<a id="7d33691bdb32v"></a>

#### startFileTranscriber

开始识别。

-   **方法签名**

<a id="code-block-7"></a>

```java
public synchronized int startFileTranscriber(String params, byte[] task_id)
```

-   **参数说明**
    
    <table><thead><tr><th><strong>参数</strong></th><th><strong>类型</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><p><code>params</code></p></td><td><p><code>String</code></p></td><td><p><a href="paraformer-recorded-speech-recognition-android-s-13e83d144d148a4f.md#d20cce9518kla">语音识别效果参数</a>。</p><p>示例：</p><a id="code-block-8"></a><pre class="language-json"><code>{
        &quot;file_urls&quot;: [
            &quot;{YOUR_AUDIO_URL}&quot;
        ],
        &quot;async_request&quot;: false,
        &quot;nls_config&quot;: {
            &quot;model&quot;:&quot;paraformer-v2&quot;,
            &quot;disfluency_removal_enabled&quot;:false,
            &quot;timestamp_alignment_enabled&quot;: false
        }
    }
    </code></pre></td></tr><tr><td><p><code>task_id</code></p></td><td><p><code>byte[]</code></p></td><td><p>任务ID，SDK内部生成随机字符串，在此接口调用成功后可获得task_id。</p></td></tr></tbody></table>
    
-   **返回值说明**

<a id="queryfiletranscriber"></a>

<a id="047417083bahi"></a>

#### queryFileTranscriber

此接口用于主动查询一个异步任务的当前状态和结果。调用成功后，结果将通过`onFileTransEventCallback`回调中的 `EVENT_FILE_TRANS_QUERY_RESULT` 事件返回。

-   **方法签名**

<a id="code-block-9"></a>

```java
public synchronized int queryFileTranscriber(String task_id)
```

-   **参数说明**
    
    | 参数 | 类型 | 说明 |
    | --- | --- | --- |
    | `task_id` | `byte[]` | 待查询的任务ID。 |
    
-   **返回值说明**

<a id="cancelfiletranscriber"></a>

<a id="8c464959f9lm9"></a>

#### cancelFileTranscriber

立即取消当前任务。

-   **方法签名**

<a id="code-block-10"></a>

```java
public synchronized int cancelFileTranscriber(String task_id)
```

-   **参数说明**
    
    | 参数 | 类型 | 说明 |
    | --- | --- | --- |
    | `task_id` | `byte[]` | 待取消的任务ID。 |
    
-   **返回值说明**

<a id="release"></a>

<a id="44bf12ed9a4g9"></a>

#### release

释放SDK所有内部资源。此方法调用后，SDK实例将变为不可用状态，如需再次使用，必须重新调用[initialize](paraformer-recorded-speech-recognition-android-s-13e83d144d148a4f.md#ae6d7dd9cfad3)进行初始化。

-   **方法签名**

<a id="code-block-11"></a>

```java
public synchronized int release();
```

-   **返回值说明**

<a id="getversion"></a>

<a id="36cbf0689bzon"></a>

#### GetVersion

获得当前SDK版本信息。

-   **方法签名**

<a id="code-block-12"></a>

```java
public synchronized String GetVersion();
```

-   **返回值说明**
    
    当前SDK版本信息。
    

<a id="inativefiletranscallback-监听回调"></a>

<a id="8b030fec74e01"></a>

### INativeFileTransCallback：监听回调

<a id="onfiletranseventcallback-监听事件和语音识别结果"></a>

<a id="163c1ef871tqt"></a>

#### onFileTransEventCallback：监听事件和语音识别结果

-   **方法签名**

<a id="code-block-13"></a>

```java
void onFileTransEventCallback(NuiEvent event, final int resultCode, final int arg2, AsrResult asrResult, String taskId);
```

-   **参数说明**
    
    | 参数 | 类型 | 说明 |
    | --- | --- | --- |
    | `event` | `NuiEvent` | 回调事件。 |
    | `resultCode` | `int` | 仅在出现 `EVENT_ASR_ERROR` 事件时有效。 |
    | `asrResult` | `AsrResult` | 语音识别结果。 |
    | `taskId` | `String` | 任务ID。 |
    | `arg2` | `int` | 保留参数。 |
    

<a id="onfiletranslogtrackcallback-监听追踪日志"></a>

<a id="9c10968457gc6"></a>

#### onFileTransLogTrackCallback：监听追踪日志

此回调用于接收 SDK 内部的详细日志，方便进行问题定位和调试。

<a id="code-block-14"></a>

```java
default void onFileTransLogTrackCallback(Constants.LogLevel level, String log)
```

<a id="nuievent-事件类型"></a>

<a id="981ff433acpmr"></a>

### `NuiEvent`：事件类型

| 事件 | 说明 |
| --- | --- |
| EVENT\_FILE\_TRANS\_CONNECTED | 连接服务成功。 |
| EVENT\_FILE\_TRANS\_UPLOADED | 上传待识别音频文件成功。 |
| EVENT\_FILE\_TRANS\_QUERY\_RESULT | 查询任务结果。 |
| EVENT\_FILE\_TRANS\_RESULT | 识别最终结果。 |
| EVENT\_ASR\_ERROR | 语音识别过程中出现错误。 |
