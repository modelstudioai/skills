# Sambert iOS SDK

使用 Sambert iOS SDK 合成语音，了解初始化参数、合成方法及回调事件。

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

1.  [下载最新SDK整合包](../model-api-reference/more-about-models/sdk-selection-and-download.md)。
2.  解压 `.tar.gz` 整合包，将 `Release/nuisdk.xcframework` 添加到 Xcode 工程。
3.  在 Build Phases → Link Binary With Libraries 中添加 `nuisdk.xcframework`。
4.  在 General → Frameworks, Libraries, and Embedded Content 中将 `nuisdk.xcframework` 设置为 Embed & Sign。

<a id="快速开始"></a>

<a id="示例代码"></a>

<a id="a7fed77afbder"></a>

## 快速开始

用 Xcode 打开示例工程。示例代码位于 `DashSambertTTSViewController`，替换 API Key 后运行示例。合成时通过回调接收音频数据。

<a id="调用步骤"></a>

<a id="使用流程"></a>

<a id="h3flowios"></a>

<a id="bccc719ce3r6a"></a>

### 调用步骤

1.  调用 `NeoNui.sharedInstance()` 获取实例，并通过 [`nui_tts_initialize`](#05eab5125e2pm) 设置回调和连接参数。
2.  调用 [`nui_tts_set_param`](#763672f3f8dgw) 设置模型、音量等合成参数。
3.  调用 `nui_tts_play` 开始语音合成。
4.  在 [`onNuiTtsUserdataCallback`](#bc71fe2545pfy)回调中获取音频数据，建议使用流式播放。如需保存本地，按追加模式将音频写入同一文件，直到合成完成。
5.  任务结束后，调用`nui_tts_release`释放SDK资源。

<a id="请求参数"></a>

## 请求参数

<a id="连接参数-parameters"></a>

<a id="connection-parameters"></a>

### 连接参数（parameters）

**parameters JSON 示例**：以下为 JSON 字符串示例，参数未完整列出。请按实际需求在编码时补充：

<a id="code-block"></a>

```json
{
    "url": "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference",
    "apikey": "st-****",
    "device_id": "my_device_id"
}
```

**parameters 参数说明：**

<table><thead><tr><th><p><strong>参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>是否必须</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p><code>url</code></p></td><td><p><code>String</code></p></td><td><p>是</p></td><td><p>服务地址，固定为 <code>wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference</code>。</p><p>调用时请将<code>{WorkspaceId}</code>替换为真实的<a href="../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain">Workspace ID</a>。</p></td></tr><tr><td><p><code>apikey</code></p></td><td><p><code>String</code></p></td><td><p>是</p></td><td><p>API Key。建议使用时效性短、安全性更高的<a href="../model-api-reference/more-about-models/generate-temporary-api-key.md">临时API Key</a>，以降低长期有效Key泄露的风险。</p></td></tr><tr><td><p><code>device_id</code></p></td><td><p><code>String</code></p></td><td><p>是</p></td><td><p>用于标识终端用户的唯一字符串，可设为应用内用户ID或客户端生成的设备唯一标识符。此ID主要用于日志追踪和问题排查。</p></td></tr><tr><td><p><code>debug_path</code></p></td><td><p><code>String</code></p></td><td><p>否</p></td><td><p>日志文件的存储路径。</p><p>此参数仅在调用<a href="sambert-ios-sdk-3a58fd71fde42af6.md">nui_tts_initialize</a>接口时将<a href="sambert-ios-sdk-3a58fd71fde42af6.md"><code>save_log</code></a>设为<code>YES</code>时生效。此时必须设置日志文件路径，否则将报错。</p><p>本地最多保留两个日志文件。</p></td></tr><tr><td><p><code>max_log_file_size</code></p></td><td><p><code>int</code></p></td><td><p>否</p></td><td><p>设定日志文件的最大字节数。</p><p>此参数仅在调用<a href="sambert-ios-sdk-3a58fd71fde42af6.md">nui_tts_initialize</a>接口时将<a href="sambert-ios-sdk-3a58fd71fde42af6.md"><code>save_log</code></a>设为<code>YES</code>时生效。</p><p>默认值：104857600（100 * 1024 * 1024 字节, 即 100MiB）。</p></td></tr><tr><td><p><code>log_track_level</code></p></td><td><p><code>int</code></p></td><td><p>否</p></td><td><p>控制通过日志回调（<a href="sambert-ios-sdk-3a58fd71fde42af6.md">onNuiTtsLogTrackCallback</a>）对外发送的日志内容的过滤级别。</p><p>默认值：2。</p><p>取值范围：</p><ul><li><p>0：LOG_LEVEL_VERBOSE</p></li><li><p>1：LOG_LEVEL_DEBUG</p></li><li><p>2：LOG_LEVEL_INFO</p></li><li><p>3：LOG_LEVEL_WARNING</p></li><li><p>4：LOG_LEVEL_ERROR</p></li><li><p>5：LOG_LEVEL_NONE（表示关闭此功能）</p></li></ul><p>注意：<code>log_track_level</code>与<a href="sambert-ios-sdk-3a58fd71fde42af6.md"><code>level</code></a>（通过<a href="sambert-ios-sdk-3a58fd71fde42af6.md">nui_tts_initialize</a>接口设置）共同决定最终回调的日志。一条日志的级别数值必须同时大于或等于<code>log_track_level</code>和<a href="sambert-ios-sdk-3a58fd71fde42af6.md"><code>level</code></a>的值，才会被回调。例如，<code>log_track_level</code>设为2 (INFO)，<a href="sambert-ios-sdk-3a58fd71fde42af6.md"><code>level</code></a>设为3 (WARNING)，则只有WARNING及以上级别（数值&gt;=3）的日志才会被回调。</p></td></tr></tbody></table>

<a id="合成参数"></a>

<a id="synthesis-parameters"></a>

### 合成参数

<table><thead><tr><th><p><strong>参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>是否必须</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p><code>model</code></p></td><td><p><code>String</code></p></td><td><p>是</p></td><td><div><p>模型名称，如 <code>sambert-zhichu-v1</code>。</p></div></td></tr><tr><td><p><code>format</code></p></td><td><p><code>String</code></p></td><td><p>否</p></td><td><div><p>音频编码格式。</p><p>取值范围：</p><ul><li><p>pcm</p></li><li><p>wav（默认）</p></li><li><p>mp3</p></li></ul></div></td></tr><tr><td><p><code>volume</code></p></td><td><p><code>String</code></p></td><td><p>否</p></td><td><div><p>音量。</p><p>默认值：50。</p><p>取值范围：[0, 100]。</p></div></td></tr><tr><td><p><code>sample_rate</code></p></td><td><p><code>String</code></p></td><td><p>否</p></td><td><div><p>音频采样率（Hz）。</p><p>取值范围：8000, 16000（默认）, 22050, 24000。</p></div></td></tr><tr><td><p><code>rate</code></p></td><td><p><code>String</code></p></td><td><p>否</p></td><td><div><p>语速。</p><p>默认值：1.0。</p><p>取值范围：[0.5, 2.0]。</p></div></td></tr><tr><td><p><code>pitch</code></p></td><td><p><code>String</code></p></td><td><p>否</p></td><td><div><p>音调。</p><p>默认值：1.0。</p><p>取值范围：[0.5, 2.0]。</p></div></td></tr><tr><td><p><code>word_timestamp_enabled</code></p></td><td><p><code>String</code></p></td><td><p>否</p></td><td><div><p>是否开启字级别时间戳。</p><p>默认值：false。</p><p>适用范围：所有 Sambert 模型。</p></div></td></tr><tr><td><p><code>phoneme_timestamp_enabled</code></p></td><td><p><code>String</code></p></td><td><p>否</p></td><td><div><p>是否开启音素级别时间戳。</p><p>默认值：false。</p><p>需要先开启 word_timestamp_enabled。</p></div></td></tr><tr><td><p><code>enable_audio_decoder</code></p></td><td><p><code>String</code></p></td><td><p>否</p></td><td><p>是否开启内置音频解码器。</p><p>默认值：0。</p><p>取值范围：</p><ul><li><p>1：开启。当 format 为 mp3 时，设为 &quot;1&quot; 可开启SDK内置解码器，此时 onNuiTtsUserdataCallback 将返回解码后的PCM数据。</p></li><li><p>0：关闭。</p></li></ul></td></tr></tbody></table>

<a id="接口参考"></a>

## 接口参考

<a id="neonui"></a>

<a id="h2-3j8v6n2m"></a>

### NeoNui

本SDK基于NeoNui单例架构，通过回调机制处理语音合成事件。

**架构特点**：

-   **单例模式：**通过 `NeoNui.sharedInstance()` 获取全局唯一实例
    
-   **回调驱动：**通过 [`NeoNuiTtsDelegate`](sambert-ios-sdk-3a58fd71fde42af6.md#8b030fec74e01) 协议接收事件和数据
    
-   **事件类型：**
    -   [`TTS_EVENT_START`](sambert-ios-sdk-3a58fd71fde42af6.md#981ff433acpmr)：合成任务开始
    -   [`onNuiTtsUserdataCallback`](sambert-ios-sdk-3a58fd71fde42af6.md#bc71fe2545pfy)：音频数据返回
    -   [`TTS_EVENT_END`](sambert-ios-sdk-3a58fd71fde42af6.md#981ff433acpmr)：合成任务结束
    -   [`TTS_EVENT_ERROR`](sambert-ios-sdk-3a58fd71fde42af6.md#981ff433acpmr)：合成出错

<a id="nui-tts-initialize"></a>

<a id="sambert-方法"></a>

<a id="h3sambertmethods"></a>

<a id="05eab5125e2pm"></a>

#### nui\_tts\_initialize

初始化语音合成SDK实例。SDK为单例模式，在调用 [`nui_tts_release`](sambert-ios-sdk-3a58fd71fde42af6.md)前禁止重复初始化。

**方法签名：**

<a id="code-block-2"></a>

```text
-(int) nui_tts_initialize:(const char *)parameters
                 logLevel:(NuiSdkLogLevel)level
                  saveLog:(BOOL)save_log;
```

**参数说明：**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `parameters` | `char*` | JSON字符串，包含鉴权、连接和调试参数。详见下方 parameters 参数说明。 |
| `level` | [`NuiSdkLogLevel`](sambert-ios-sdk-3a58fd71fde42af6.md#h2nuisdkloglevel) | 控制SDK自身日志的打印级别。 |
| `save_log` | `BOOL` | 是否保存本地日志。若为`YES`，须在 parameters 中通过`debug_path`指定路径，并可通过`max_log_file_size`设置文件大小。 |

`parameters` 的字段和示例见[连接参数](#connection-parameters)。

<a id="nui-tts-set-param"></a>

<a id="763672f3f8dgw"></a>

#### nui\_tts\_set\_param

以键值对的形式设置参数。在 [`nui_tts_play`](sambert-ios-sdk-3a58fd71fde42af6.md)之前调用。

**方法签名：**

<a id="code-block-3"></a>

```text
-(int) nui_tts_set_param:(const char *)param
                   value:(const char *)value;
```

**参数说明：**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `param` | `char*` | 参数名。 |
| `value` | `char*` | 参数值。 |

可设置的键和值见[合成参数](#synthesis-parameters)。

<a id="nui-tts-get-param"></a>

<a id="cdbe73c6abhdn"></a>

#### nui\_tts\_get\_param

获取参数值。主要用于错误排查。

**方法签名：**

<a id="code-block-4"></a>

```text
-(const char *) nui_tts_get_param:(const char *)param;
```

**参数说明：**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `param` | `char*` | 参数。目前仅支持"error\_msg"。 |

**返回值说明：**

返回参数值。

<a id="nui-tts-play"></a>

<a id="8fe6ea298apzu"></a>

#### nui\_tts\_play

启动一个语音合成任务。

**方法签名：**

<a id="code-block-5"></a>

```text
-(int) nui_tts_play:(const char *)priority
             taskId:(const char *)taskid
              text:(const char *)text;
```

**参数说明：**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `priority` | `char*` | 任务优先级。请将其设为1。 |
| `taskid` | `char*` | 任务ID。传入 `null` 时由SDK自动生成。 |
| `text` | `char*` | 待合成文本。 |

<a id="nui-tts-pause"></a>

<a id="ebbc09fb2fz8y"></a>

#### nui\_tts\_pause

暂停当前语音合成任务。任务暂停后，可通过 [`nui_tts_resume`](sambert-ios-sdk-3a58fd71fde42af6.md)恢复，或通过 [`nui_tts_cancel`](sambert-ios-sdk-3a58fd71fde42af6.md)彻底取消。在任务暂停期间，SDK不支持启动新的合成任务。

注意：此操作仅暂停从服务端的数据拉取，播放器中已缓存的音频数据会继续播放。

**方法签名：**

<a id="code-block-6"></a>

```text
-(int) nui_tts_pause;
```

<a id="nui-tts-resume"></a>

<a id="448e8ffafd72e"></a>

#### nui\_tts\_resume

恢复处于暂停的语音合成任务。

**方法签名：**

<a id="code-block-7"></a>

```text
-(int) nui_tts_resume;
```

<a id="nui-tts-cancel"></a>

<a id="156934a01bzjc"></a>

#### nui\_tts\_cancel

取消合成任务。

注意：此操作仅取消从服务端的数据拉取，播放器中已缓存的音频数据会继续播放。

**方法签名：**

<a id="code-block-8"></a>

```text
-(int) nui_tts_cancel:(const char *)taskid;
```

**参数说明：**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `taskid` | `char*` | 要取消的任务ID。若传入 `null`，则取消所有正在暂停/进行中的合成任务。 |

<a id="nui-tts-release"></a>

<a id="6c2931e9ae3eq"></a>

#### nui\_tts\_release

释放SDK所有内部资源，并强制终止所有正在进行的合成任务。此方法调用后，SDK实例将变为不可用状态，如需再次使用，必须重新调用 [`nui_tts_initialize`](sambert-ios-sdk-3a58fd71fde42af6.md)进行初始化。

**方法签名：**

<a id="code-block-9"></a>

```text
-(int) nui_tts_release;
```

<a id="neonuittsdelegate"></a>

<a id="8b030fec74e01"></a>

<a id="方法"></a>

<a id="h3nuittsdelmios"></a>

### NeoNuiTtsDelegate

Sambert 语音合成回调协议，用于接收合成事件、音频数据和日志。

<a id="onnuittseventcallback-监听事件"></a>

<a id="163c1ef871tqt"></a>

#### onNuiTtsEventCallback：监听事件

**方法签名：**

<a id="code-block-10"></a>

```text
- (void)onNuiTtsEventCallback:(NuiSdkTtsEvent)event taskId:(char*)taskid code:(int)code;
```

**参数说明：**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `event` | [`NuiSdkTtsEvent`](sambert-ios-sdk-3a58fd71fde42af6.md#981ff433acpmr) | 回调事件。 |
| `taskid` | `char*` | 语音合成任务ID。 |
| `code` | `int` | 仅在出现 [TTS\_EVENT\_ERROR](sambert-ios-sdk-3a58fd71fde42af6.md#981ff433acpmr) 事件时有效。 |

<a id="onnuittsuserdatacallback-监听音频数据和时间戳信息"></a>

<a id="bc71fe2545pfy"></a>

#### onNuiTtsUserdataCallback：监听音频数据和时间戳信息

**方法签名：**

<a id="code-block-11"></a>

```text
- (void)onNuiTtsUserdataCallback:(char*)info infoLen:(int)info_len buffer:(char*)buffer len:(int)len taskId:(char*)task_id;
```

**参数说明：**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `info` | `char*` | JSON格式的时间戳结果。`word_timestamp_enabled`设为`"1"`时生效。 |
| `info_len` | `int` | info字段的数据长度，可忽略。 |
| `buffer` | `char*` | 返回当前片段的音频数据。 |
| `len` | `int` | 音频数据的长度（字节）。 |
| `task_id` | `char*` | 语音合成任务ID。 |

<a id="onnuittslogtrackcallback-监听追踪日志"></a>

<a id="9c10968457gc6"></a>

#### onNuiTtsLogTrackCallback：监听追踪日志

此回调用于接收 SDK 内部的详细日志，方便进行问题定位和调试。

**方法签名：**

<a id="code-block-12"></a>

```text
- (void)onNuiTtsLogTrackCallback:(NuiSdkLogLevel)level
                      logMessage:(const char *)log;
```

**参数说明：**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `level` | [`NuiSdkLogLevel`](sambert-ios-sdk-3a58fd71fde42af6.md#h2nuisdkloglevel) | 日志级别。 |
| `log` | `char*` | 日志内容。 |

<a id="nuisdkttsevent"></a>

<a id="981ff433acpmr"></a>

### NuiSdkTtsEvent

Sambert 语音合成事件类型枚举。

<table><thead><tr><th><strong>事件</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><p>TTS_EVENT_START</p></td><td><p>合成任务开始，即将有音频数据返回。</p></td></tr><tr><td><p>TTS_EVENT_END</p></td><td><p>合成任务正常结束，所有音频数据已通过回调送出。</p></td></tr><tr><td><p>TTS_EVENT_CANCEL</p></td><td><p>合成任务已取消。</p></td></tr><tr><td><p>TTS_EVENT_PAUSE</p></td><td><p>合成任务已暂停。</p></td></tr><tr><td><p>TTS_EVENT_RESUME</p></td><td><p>合成任务已恢复。</p></td></tr><tr><td><p>TTS_EVENT_ERROR</p></td><td><p>合成过程中发生错误。此时可通过<code>nui_tts_get_param: &quot;error_msg&quot;</code>获取详细错误信息。</p><a id="code-block-13"></a><pre class="language-json"><code>{
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

<a id="nuisdkloglevel"></a>

<a id="h2nuisdkloglevel"></a>

### NuiSdkLogLevel

SDK 日志级别枚举，用于控制日志输出。

| 级别 | 说明 |
| --- | --- |
| 0：LOG\_LEVEL\_VERBOSE | 最详细的日志，包含所有调试信息。 |
| 1：LOG\_LEVEL\_DEBUG | 调试级别日志。 |
| 2：LOG\_LEVEL\_INFO | 常规信息级别日志（默认值）。 |
| 3：LOG\_LEVEL\_WARNING | 警告级别日志。 |
| 4：LOG\_LEVEL\_ERROR | 错误级别日志。 |
| 5：LOG\_LEVEL\_NONE | 关闭日志输出。 |
