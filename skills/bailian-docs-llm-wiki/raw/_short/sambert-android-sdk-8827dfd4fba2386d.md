# Sambert Android SDK

使用 Sambert Android SDK 合成语音，了解初始化参数、合成方法及回调事件。

**用户指南：**关于模型介绍和选型建议请参见[语音合成-Sambert](https://help.aliyun.com/zh/model-studio/text-to-speech)。

**在线体验**：暂不支持。

<a id="前提条件"></a>

## 前提条件

[获取与配置 API Key](../model-api-reference/preparations/get-api-key.md)。移动端应用请勿硬编码长期 API Key。建议由应用服务端[生成临时 API Key](../model-api-reference/more-about-models/generate-temporary-api-key.md)，再下发给客户端。

> **重要**
>
> 阿里云百炼为华北2（北京）地域推出了业务空间专属域名，能够为推理请求提供卓越的性能和更高的稳定性，建议从 `dashscope.aliyuncs.com` 迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`。
>
> `{WorkspaceId}`需要替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。现有域名仍可正常使用。

<a id="安装-sdk"></a>

### 安装 SDK

1.  [下载最新 SDK 整合包](https://help.aliyun.com/zh/model-studio/sdk-selection-and-download)。
2.  解压 ZIP 包，将 `app/libs` 目录中的 AAR SDK 添加到项目依赖。
3.  如需接入 Android C++，从 ZIP 包内的 `android_libs` 和 `android_include` 获取动态库和头文件。

<a id="快速开始"></a>

<a id="示例代码"></a>

<a id="abf215f434v5x"></a>

## 快速开始

用 Android Studio 打开示例工程。示例代码位于 `DashSambertTtsActivity.java`，替换 API Key 后运行示例。合成时通过回调接收音频数据。

<a id="调用步骤"></a>

<a id="0701a2d0b75vm"></a>

<a id="使用流程"></a>

<a id="h3archflow5"></a>

### 调用步骤

1.  通过 `NativeNui.GetInstance()` 获取实例。调用 [`tts_initialize()`](sambert-android-sdk-8827dfd4fba2386d.md#ae6d7dd9cfad3)，在 `ticket` 中设置连接与控制参数，并传入回调接口。请在非 UI 线程中调用。
2.  调用 [`setparamTts()`](sambert-android-sdk-8827dfd4fba2386d.md#a23e0d85d7ymt) 设置模型、音色和音量等合成参数。
3.  调用 [`startTts()`](sambert-android-sdk-8827dfd4fba2386d.md#7d33691bdb32v) 开始语音合成。
4.  在[onTtsDataCallback](sambert-android-sdk-8827dfd4fba2386d.md#bc71fe2545pfy)回调中获取音频数据，建议使用流式播放。如需保存本地，按追加模式将音频写入同一文件，直到合成完成。
5.  任务结束后，调用 [`tts_release()`](sambert-android-sdk-8827dfd4fba2386d.md#44bf12ed9a4g9) 释放 SDK 资源。

<a id="请求参数"></a>

## 请求参数

<a id="连接参数-ticket"></a>

<a id="connection-parameters"></a>

### 连接参数（ticket）

**ticket JSON 示例**：

<a id="code-block"></a>

```json
{
    "url": "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference",
    "apikey": "sk-****",
    "device_id": "my_device_id",
    "mode_type": "2"
}
```

**ticket 参数说明：**

<table><thead><tr><th><p><strong>参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>是否必须</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p><code>url</code></p></td><td><p><code>String</code></p></td><td><p>是</p></td><td><p>服务地址，固定为 <code>wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference</code>。</p><p>调用时请将<code>{WorkspaceId}</code>替换为真实的<a href="../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain">Workspace ID</a>。</p></td></tr><tr><td><p><code>apikey</code></p></td><td><p><code>String</code></p></td><td><p>是</p></td><td><p>API Key。建议使用时效性短、安全性更高的<a href="../model-api-reference/more-about-models/generate-temporary-api-key.md">临时API Key</a>，以降低长期有效Key泄露的风险。</p></td></tr><tr><td><p><code>mode_type</code></p></td><td><p><code>String</code></p></td><td><p>是</p></td><td><p>模式类型。必须设置为字符串 <code>&quot;2&quot;</code>，代表在线语音合成模式。</p></td></tr><tr><td><p><code>device_id</code></p></td><td><p><code>String</code></p></td><td><p>是</p></td><td><p>用于标识终端用户的唯一字符串，可设为应用内用户ID或客户端生成的设备唯一标识符。此ID主要用于日志追踪和问题排查。</p></td></tr><tr><td><p><code>debug_path</code></p></td><td><p><code>String</code></p></td><td><p>否</p></td><td><p>日志文件的存储路径。</p><p>此参数仅在调用tts_initialize接口时将<code>save_log</code>设为true时生效。此时必须设置日志文件路径，否则将报错。</p><p>本地最多保留两个日志文件。</p></td></tr><tr><td><p><code>max_log_file_size</code></p></td><td><p><code>int</code></p></td><td><p>否</p></td><td><p>设定日志文件的最大字节数。</p><p>此参数仅在调用tts_initialize接口时将<code>save_log</code>设为true时生效。</p><p>默认值：104857600（100 * 1024 * 1024 字节, 即 100MiB）。</p></td></tr><tr><td><p><code>log_track_level</code></p></td><td><p><code>int</code></p></td><td><p>否</p></td><td><p>控制通过日志回调（<a href="sambert-android-sdk-8827dfd4fba2386d.md#9c10968457gc6"><code>onTtsLogTrackCallback</code></a>）对外发送的日志内容的过滤级别。</p><p>默认值：2。</p><p>取值范围：</p><ul><li><p>0：LOG_LEVEL_VERBOSE</p></li><li><p>1：LOG_LEVEL_DEBUG</p></li><li><p>2：LOG_LEVEL_INFO</p></li><li><p>3：LOG_LEVEL_WARNING</p></li><li><p>4：LOG_LEVEL_ERROR</p></li><li><p>5：LOG_LEVEL_NONE（表示关闭此功能）</p></li></ul><p>注意：<code>log_track_level</code>与<code>log_level</code>（通过tts_initialize接口设置）共同决定最终回调的日志。一条日志的级别数值必须同时大于或等于<code>log_track_level</code>和<code>log_level</code>的值，才会被回调。例如，<code>log_track_level</code>设为2 (INFO)，<code>log_level</code>设为3 (WARNING)，则只有WARNING及以上级别（数值&gt;=3）的日志才会被回调。</p></td></tr></tbody></table>

<a id="合成参数"></a>

<a id="synthesis-parameters"></a>

### 合成参数

<table><thead><tr><th><p><strong>参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>是否必须</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p><code>model</code></p></td><td><p><code>String</code></p></td><td><p>是</p></td><td><div><p>模型名称，如 <code>sambert-zhichu-v1</code>。</p></div></td></tr><tr><td><p><code>format</code></p></td><td><p><code>String</code></p></td><td><p>否</p></td><td><div><p>音频编码格式。</p><p>取值范围：</p><ul><li><p>pcm</p></li><li><p>wav（默认）</p></li><li><p>mp3</p></li></ul></div></td></tr><tr><td><p><code>volume</code></p></td><td><p><code>String</code></p></td><td><p>否</p></td><td><div><p>音量。</p><p>默认值：50。</p><p>取值范围：[0, 100]。</p></div></td></tr><tr><td><p><code>sample_rate</code></p></td><td><p><code>String</code></p></td><td><p>否</p></td><td><div><p>音频采样率（Hz）。</p><p>取值范围：8000, 16000（默认）, 22050, 24000。</p></div></td></tr><tr><td><p><code>rate</code></p></td><td><p><code>String</code></p></td><td><p>否</p></td><td><div><p>语速。</p><p>默认值：1.0。</p><p>取值范围：[0.5, 2.0]。</p></div></td></tr><tr><td><p><code>pitch</code></p></td><td><p><code>String</code></p></td><td><p>否</p></td><td><div><p>音调。</p><p>默认值：1.0。</p><p>取值范围：[0.5, 2.0]。</p></div></td></tr><tr><td><p><code>word_timestamp_enabled</code></p></td><td><p><code>String</code></p></td><td><p>否</p></td><td><div><p>是否开启字级别时间戳。</p><p>默认值：false。</p><p>适用范围：所有 Sambert 模型。</p></div></td></tr><tr><td><p><code>phoneme_timestamp_enabled</code></p></td><td><p><code>String</code></p></td><td><p>否</p></td><td><div><p>是否开启音素级别时间戳。</p><p>默认值：false。</p><p>需要先开启 word_timestamp_enabled。</p></div></td></tr><tr><td><p><code>enable_audio_decoder</code></p></td><td><p><code>String</code></p></td><td><p>否</p></td><td><p>是否开启内置音频解码器。</p><p>默认值：0。</p><p>取值范围：</p><ul><li><p>1：开启。当 format 为 mp3 时，设为 &quot;1&quot; 可开启SDK内置解码器，此时 <a href="sambert-android-sdk-8827dfd4fba2386d.md#bc71fe2545pfy">onTtsDataCallback</a> 将返回解码后的PCM数据。</p></li><li><p>0：关闭。</p></li></ul></td></tr></tbody></table>

<a id="接口参考"></a>

## 接口参考

<a id="nativenui"></a>

<a id="h2arch4d5"></a>

### NativeNui

本SDK基于NativeNui单例架构，通过回调机制处理语音合成事件。

**架构特点**：

-   **单例模式：**通过 `NativeNui.GetInstance()` 获取全局唯一实例
    
-   **回调驱动：**通过 [`INativeTtsCallback`](sambert-android-sdk-8827dfd4fba2386d.md#8b030fec74e01) 接口接收事件和数据
    
-   **事件类型：**
    -   [`TTS_EVENT_START`](sambert-android-sdk-8827dfd4fba2386d.md#981ff433acpmr)：合成任务开始
    -   [`onTtsDataCallback`](sambert-android-sdk-8827dfd4fba2386d.md#bc71fe2545pfy)：音频数据返回
    -   [`TTS_EVENT_END`](sambert-android-sdk-8827dfd4fba2386d.md#981ff433acpmr)：合成任务结束
    -   [`TTS_EVENT_ERROR`](sambert-android-sdk-8827dfd4fba2386d.md#981ff433acpmr)：合成出错

<a id="tts-initialize"></a>

<a id="ae6d7dd9cfad3"></a>

<a id="sambert-方法"></a>

<a id="h3sambertmethods"></a>

#### tts\_initialize

初始化语音合成SDK实例。SDK为单例模式，在调用 [`tts_release()`](sambert-android-sdk-8827dfd4fba2386d.md#44bf12ed9a4g9) 前禁止重复初始化。

此接口会引起阻塞，应在非UI线程调用。

**方法签名：**

<a id="code-block-2"></a>

```java
public synchronized int tts_initialize(INativeTtsCallback callback,
                                       String ticket,
                                       final Constants.LogLevel level,
                                       boolean save_log)
```

**参数说明：**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `callback` | [`INativeTtsCallback`](sambert-android-sdk-8827dfd4fba2386d.md#8b030fec74e01) | 事件和数据回调接口的实现。 |
| `ticket` | `String` | JSON字符串，包含鉴权、连接和调试参数。详见[连接参数](#connection-parameters)。 |
| `level` | `Constants.LogLevel` | 控制SDK自身日志的打印级别。 |
| `save_log` | `boolean` | 是否保存本地日志。若为true，须在 ticket 参数中通过`debug_path`指定路径，并可通过`max_log_file_size`设置文件大小。 |

<a id="setparamtts"></a>

<a id="a23e0d85d7ymt"></a>

#### setparamTts

以键值对的形式设置语音合成效果参数。在 [`startTts()`](sambert-android-sdk-8827dfd4fba2386d.md#7d33691bdb32v) 之前调用。

**方法签名：**

<a id="code-block-3"></a>

```java
public synchronized int setparamTts(String param, String value)
```

**参数说明：**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `param` | `String` | 参数名。 |
| `value` | `String` | 参数值。 |

可设置的键和值见[合成参数](#synthesis-parameters)。

<a id="getparamtts"></a>

<a id="119bb1cb6atc3"></a>

#### getparamTts

获取参数值。主要用于错误排查。

**方法签名：**

<a id="code-block-4"></a>

```java
public String getparamTts(String param);
```

**参数说明：**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `param` | `String` | 参数名。目前仅支持"error\_msg"。 |

**返回值说明：**

返回参数值。

<a id="starttts"></a>

<a id="7d33691bdb32v"></a>

#### startTts

启动语音合成任务。合成结果通过回调返回。

**方法签名：**

<a id="code-block-5"></a>

```java
public synchronized int startTts(String priority, String taskid, String text)
```

**参数说明：**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `priority` | `String` | 任务优先级。请将其设为1。 |
| `taskid` | `String` | 任务ID。传入 `null` 时由SDK自动生成。 |
| `text` | `String` | 待合成文本。 |

<a id="pausetts"></a>

<a id="047417083bahi"></a>

#### pauseTts

暂停当前语音合成任务。任务暂停后，可通过 [`resumeTts()`](sambert-android-sdk-8827dfd4fba2386d.md#01f640f02bka9) 恢复，或通过 [`cancelTts()`](sambert-android-sdk-8827dfd4fba2386d.md#8c464959f9lm9) 彻底取消。在任务暂停期间，SDK不支持启动新的合成任务。

注意：此操作仅暂停从服务端的数据拉取，播放器中已缓存的音频数据会继续播放。

**方法签名：**

<a id="code-block-6"></a>

```java
public synchronized int pauseTts()
```

<a id="resumetts"></a>

<a id="01f640f02bka9"></a>

#### resumeTts

恢复处于暂停的语音合成任务。

**方法签名：**

<a id="code-block-7"></a>

```java
public synchronized int resumeTts()
```

<a id="canceltts"></a>

<a id="8c464959f9lm9"></a>

#### cancelTts

取消合成任务。

注意：此操作仅取消从服务端的数据拉取，播放器中已缓存的音频数据会继续播放。

**方法签名：**

<a id="code-block-8"></a>

```java
public synchronized int cancelTts(String taskid)
```

**参数说明：**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `taskid` | `String` | 要取消的任务ID。若传入 `null`，则取消所有正在暂停/进行中的合成任务。 |

<a id="tts-release"></a>

<a id="44bf12ed9a4g9"></a>

#### tts\_release

释放SDK所有内部资源，并强制终止所有正在进行的合成任务。此方法调用后，SDK实例将变为不可用状态，如需再次使用，必须重新调用 [`tts_initialize()`](sambert-android-sdk-8827dfd4fba2386d.md#ae6d7dd9cfad3) 进行初始化。

**方法签名：**

<a id="code-block-9"></a>

```java
public synchronized int tts_release()
```

<a id="inativettscallback"></a>

<a id="8b030fec74e01"></a>

### INativeTtsCallback

Sambert 语音合成回调接口，用于接收合成事件和音频数据。

<a id="onttseventcallback-监听事件"></a>

<a id="163c1ef871tqt"></a>

#### onTtsEventCallback：监听事件

**方法签名：**

<a id="code-block-10"></a>

```java
void onTtsEventCallback(TtsEvent event, String task_id, int ret_code);
```

**参数说明：**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `event` | [`TtsEvent`](sambert-android-sdk-8827dfd4fba2386d.md#981ff433acpmr) | 回调事件。 |
| `task_id` | `String` | 语音合成任务ID。 |
| `ret_code` | `int` | 仅在出现 [TTS\_EVENT\_ERROR](sambert-android-sdk-8827dfd4fba2386d.md#981ff433acpmr) 事件时有效。 |

<a id="onttsdatacallback-监听音频数据和时间戳信息"></a>

<a id="bc71fe2545pfy"></a>

#### onTtsDataCallback：监听音频数据和时间戳信息

合成过程中，SDK 会连续触发此回调，需在回调中获取音频数据。

**方法签名：**

<a id="code-block-11"></a>

```java
void onTtsDataCallback(String info, int info_len, byte[] data);
```

**参数说明：**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `info` | `String` | JSON格式的时间戳结果。`word_timestamp_enabled`设为`"1"`时生效。 |
| `info_len` | `int` | info字段的数据长度，可忽略。 |
| `data` | `byte[]` | 返回当前片段的音频数据。 |

<a id="onttslogtrackcallback-监听追踪日志"></a>

<a id="9c10968457gc6"></a>

#### onTtsLogTrackCallback：监听追踪日志

此回调用于接收 SDK 内部的详细日志，方便进行问题定位和调试。

**方法签名：**

<a id="code-block-12"></a>

```java
default void onTtsLogTrackCallback(Constants.LogLevel level, String log)
```

<a id="ttsevent"></a>

<a id="981ff433acpmr"></a>

### TtsEvent

Sambert 语音合成事件类型枚举。

<table><thead><tr><th><strong>事件</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><p>TTS_EVENT_START</p></td><td><p>合成任务开始，即将有音频数据返回。</p></td></tr><tr><td><p>TTS_EVENT_END</p></td><td><p>合成任务正常结束，所有音频数据已通过回调送出。</p></td></tr><tr><td><p>TTS_EVENT_CANCEL</p></td><td><p>合成任务已取消。</p></td></tr><tr><td><p>TTS_EVENT_PAUSE</p></td><td><p>合成任务已暂停。</p></td></tr><tr><td><p>TTS_EVENT_RESUME</p></td><td><p>合成任务已恢复。</p></td></tr><tr><td><p>TTS_EVENT_ERROR</p></td><td><p>合成过程中发生错误。此时可通过<code>getparamTTS(&quot;error_msg&quot;)</code>获取详细错误信息。</p><a id="code-block-13"></a><pre class="language-json"><code>{
  &quot;header&quot;: {
    &quot;task_id&quot;: &quot;xxxxxxxxx&quot;,
    &quot;event&quot;: &quot;task-failed&quot;,
    &quot;error_code&quot;: &quot;InvalidParameter&quot;,
    &quot;error_message&quot;: &quot;Please ensure input text is valid.&quot;,
    &quot;attributes&quot;: {}
  },
  &quot;payload&quot;: {}
}
</code></pre></td></tr></tbody></table>
