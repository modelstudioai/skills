# Sambert Android SDK

使用 Sambert Android SDK 合成语音，了解初始化参数、合成方法及回调事件。

**用户指南：**关于模型介绍和选型建议请参见[语音合成-Sambert](https://help.aliyun.com/zh/model-studio/text-to-speech)。

**在线体验**：暂不支持。

## 前提条件

[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。移动端应用请勿硬编码长期 API Key。建议由应用服务端[生成临时 API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)，再下发给客户端。

**重要**阿里云百炼为华北2（北京）地域推出了业务空间专属域名，能够为推理请求提供卓越的性能和更高的稳定性，建议从 `dashscope.aliyuncs.com` 迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`。

`{WorkspaceId}`需要替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。现有域名仍可正常使用。

### 安装 SDK

1.  [下载最新 SDK 整合包](https://help.aliyun.com/zh/model-studio/sdk-selection-and-download)。
2.  解压 ZIP 包，将 `app/libs` 目录中的 AAR SDK 添加到项目依赖。
3.  如需接入 Android C++，从 ZIP 包内的 `android_libs` 和 `android_include` 获取动态库和头文件。

## 快速开始

用 Android Studio 打开示例工程。示例代码位于 `DashSambertTtsActivity.java`，替换 API Key 后运行示例。合成时通过回调接收音频数据。

### 调用步骤

1.  通过 `NativeNui.GetInstance()` 获取实例。调用 [`tts_initialize()`](https://help.aliyun.com/zh/model-studio/sambert-android-sdk#ae6d7dd9cfad3)，在 `ticket` 中设置连接与控制参数，并传入回调接口。请在非 UI 线程中调用。
2.  调用 [`setparamTts()`](https://help.aliyun.com/zh/model-studio/sambert-android-sdk#a23e0d85d7ymt) 设置模型、音色和音量等合成参数。
3.  调用 [`startTts()`](https://help.aliyun.com/zh/model-studio/sambert-android-sdk#7d33691bdb32v) 开始语音合成。
4.  在[onTtsDataCallback](https://help.aliyun.com/zh/model-studio/sambert-android-sdk#bc71fe2545pfy)回调中获取音频数据，建议使用流式播放。如需保存本地，按追加模式将音频写入同一文件，直到合成完成。
5.  任务结束后，调用 [`tts_release()`](https://help.aliyun.com/zh/model-studio/sambert-android-sdk#44bf12ed9a4g9) 释放 SDK 资源。

## 请求参数

### 连接参数（ticket）

**ticket JSON 示例**：

```
{
    "url": "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference",
    "apikey": "sk-****",
    "device_id": "my_device_id",
    "mode_type": "2"
}
```
**ticket 参数说明：**

**参数**

**类型**

**是否必须**

**说明**

`url`

`String`

是

服务地址，固定为 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference`。

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

`apikey`

`String`

是

API Key。建议使用时效性短、安全性更高的[临时API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)，以降低长期有效Key泄露的风险。

`mode_type`

`String`

是

模式类型。必须设置为字符串 `"2"`，代表在线语音合成模式。

`device_id`

`String`

是

用于标识终端用户的唯一字符串，可设为应用内用户ID或客户端生成的设备唯一标识符。此ID主要用于日志追踪和问题排查。

`debug_path`

`String`

否

日志文件的存储路径。

此参数仅在调用tts\_initialize接口时将`save_log`设为true时生效。此时必须设置日志文件路径，否则将报错。

本地最多保留两个日志文件。

`max_log_file_size`

`int`

否

设定日志文件的最大字节数。

此参数仅在调用tts\_initialize接口时将`save_log`设为true时生效。

默认值：104857600（100 \* 1024 \* 1024 字节, 即 100MiB）。

`log_track_level`

`int`

否

控制通过日志回调（[`onTtsLogTrackCallback`](https://help.aliyun.com/zh/model-studio/sambert-android-sdk#9c10968457gc6)）对外发送的日志内容的过滤级别。

默认值：2。

取值范围：

-   0：LOG\_LEVEL\_VERBOSE
    
-   1：LOG\_LEVEL\_DEBUG
    
-   2：LOG\_LEVEL\_INFO
    
-   3：LOG\_LEVEL\_WARNING
    
-   4：LOG\_LEVEL\_ERROR
    
-   5：LOG\_LEVEL\_NONE（表示关闭此功能）
    

注意：`log_track_level`与`log_level`（通过tts\_initialize接口设置）共同决定最终回调的日志。一条日志的级别数值必须同时大于或等于`log_track_level`和`log_level`的值，才会被回调。例如，`log_track_level`设为2 (INFO)，`log_level`设为3 (WARNING)，则只有WARNING及以上级别（数值>=3）的日志才会被回调。

### 合成参数

**参数**

**类型**

**是否必须**

**说明**

`model`

`String`

是

模型名称，如 `sambert-zhichu-v1`。

`format`

`String`

否

音频编码格式。

取值范围：

-   pcm
    
-   wav（默认）
    
-   mp3
    

`volume`

`String`

否

音量。

默认值：50。

取值范围：\[0, 100\]。

`sample_rate`

`String`

否

音频采样率（Hz）。

取值范围：8000, 16000（默认）, 22050, 24000。

`rate`

`String`

否

语速。

默认值：1.0。

取值范围：\[0.5, 2.0\]。

`pitch`

`String`

否

音调。

默认值：1.0。

取值范围：\[0.5, 2.0\]。

`word_timestamp_enabled`

`String`

否

是否开启字级别时间戳。

默认值：false。

适用范围：所有 Sambert 模型。

`phoneme_timestamp_enabled`

`String`

否

是否开启音素级别时间戳。

默认值：false。

需要先开启 word\_timestamp\_enabled。

`enable_audio_decoder`

`String`

否

是否开启内置音频解码器。

默认值：0。

取值范围：

-   1：开启。当 format 为 mp3 时，设为 "1" 可开启SDK内置解码器，此时 [onTtsDataCallback](https://help.aliyun.com/zh/model-studio/sambert-android-sdk#bc71fe2545pfy) 将返回解码后的PCM数据。
    
-   0：关闭。
    

## 接口参考

### NativeNui

本SDK基于NativeNui单例架构，通过回调机制处理语音合成事件。

**架构特点**：

-   **单例模式：**通过 `NativeNui.GetInstance()` 获取全局唯一实例
    
-   **回调驱动：**通过 [`INativeTtsCallback`](https://help.aliyun.com/zh/model-studio/sambert-android-sdk#8b030fec74e01) 接口接收事件和数据
    
-   **事件类型：**
    -   [`TTS_EVENT_START`](https://help.aliyun.com/zh/model-studio/sambert-android-sdk#981ff433acpmr)：合成任务开始
    -   [`onTtsDataCallback`](https://help.aliyun.com/zh/model-studio/sambert-android-sdk#bc71fe2545pfy)：音频数据返回
    -   [`TTS_EVENT_END`](https://help.aliyun.com/zh/model-studio/sambert-android-sdk#981ff433acpmr)：合成任务结束
    -   [`TTS_EVENT_ERROR`](https://help.aliyun.com/zh/model-studio/sambert-android-sdk#981ff433acpmr)：合成出错

#### tts\_initialize

初始化语音合成SDK实例。SDK为单例模式，在调用 [`tts_release()`](https://help.aliyun.com/zh/model-studio/sambert-android-sdk#44bf12ed9a4g9) 前禁止重复初始化。

此接口会引起阻塞，应在非UI线程调用。

**方法签名：**
```
public synchronized int tts_initialize(INativeTtsCallback callback,
                                       String ticket,
                                       final Constants.LogLevel level,
                                       boolean save_log)
```
**参数说明：**

**参数**

**类型**

**说明**

`callback`

[`INativeTtsCallback`](https://help.aliyun.com/zh/model-studio/sambert-android-sdk#8b030fec74e01)

事件和数据回调接口的实现。

`ticket`

`String`

JSON字符串，包含鉴权、连接和调试参数。详见[连接参数](#connection-parameters)。

`level`

`Constants.LogLevel`

控制SDK自身日志的打印级别。

`save_log`

`boolean`

是否保存本地日志。若为true，须在 ticket 参数中通过`debug_path`指定路径，并可通过`max_log_file_size`设置文件大小。

#### setparamTts

以键值对的形式设置语音合成效果参数。在 [`startTts()`](https://help.aliyun.com/zh/model-studio/sambert-android-sdk#7d33691bdb32v) 之前调用。

**方法签名：**
```
public synchronized int setparamTts(String param, String value)
```
**参数说明：**

**参数**

**类型**

**说明**

`param`

`String`

参数名。

`value`

`String`

参数值。

可设置的键和值见[合成参数](#synthesis-parameters)。

#### getparamTts

获取参数值。主要用于错误排查。

**方法签名：**
```
public String getparamTts(String param);
```
**参数说明：**

**参数**

**类型**

**说明**

`param`

`String`

参数名。目前仅支持"error\_msg"。

**返回值说明：**

返回参数值。

#### startTts

启动语音合成任务。合成结果通过回调返回。

**方法签名：**
```
public synchronized int startTts(String priority, String taskid, String text)
```
**参数说明：**

**参数**

**类型**

**说明**

`priority`

`String`

任务优先级。请将其设为1。

`taskid`

`String`

任务ID。传入 `null` 时由SDK自动生成。

`text`

`String`

待合成文本。

#### pauseTts

暂停当前语音合成任务。任务暂停后，可通过 [`resumeTts()`](https://help.aliyun.com/zh/model-studio/sambert-android-sdk#01f640f02bka9) 恢复，或通过 [`cancelTts()`](https://help.aliyun.com/zh/model-studio/sambert-android-sdk#8c464959f9lm9) 彻底取消。在任务暂停期间，SDK不支持启动新的合成任务。

注意：此操作仅暂停从服务端的数据拉取，播放器中已缓存的音频数据会继续播放。

**方法签名：**
```
public synchronized int pauseTts()
```

#### resumeTts

恢复处于暂停的语音合成任务。

**方法签名：**
```
public synchronized int resumeTts()
```

#### cancelTts

取消合成任务。

注意：此操作仅取消从服务端的数据拉取，播放器中已缓存的音频数据会继续播放。

**方法签名：**
```
public synchronized int cancelTts(String taskid)
```
**参数说明：**

**参数**

**类型**

**说明**

`taskid`

`String`

要取消的任务ID。若传入 `null`，则取消所有正在暂停/进行中的合成任务。

#### tts\_release

释放SDK所有内部资源，并强制终止所有正在进行的合成任务。此方法调用后，SDK实例将变为不可用状态，如需再次使用，必须重新调用 [`tts_initialize()`](https://help.aliyun.com/zh/model-studio/sambert-android-sdk#ae6d7dd9cfad3) 进行初始化。

**方法签名：**
```
public synchronized int tts_release()
```

### INativeTtsCallback

Sambert 语音合成回调接口，用于接收合成事件和音频数据。

#### onTtsEventCallback：监听事件

**方法签名：**
```
void onTtsEventCallback(TtsEvent event, String task_id, int ret_code);
```
**参数说明：**

**参数**

**类型**

**说明**

`event`

[`TtsEvent`](https://help.aliyun.com/zh/model-studio/sambert-android-sdk#981ff433acpmr)

回调事件。

`task_id`

`String`

语音合成任务ID。

`ret_code`

`int`

仅在出现 [TTS\_EVENT\_ERROR](https://help.aliyun.com/zh/model-studio/sambert-android-sdk#981ff433acpmr) 事件时有效。

#### onTtsDataCallback：监听音频数据和时间戳信息

合成过程中，SDK 会连续触发此回调，需在回调中获取音频数据。

**方法签名：**
```
void onTtsDataCallback(String info, int info_len, byte[] data);
```
**参数说明：**

**参数**

**类型**

**说明**

`info`

`String`

JSON格式的时间戳结果。`word_timestamp_enabled`设为`"1"`时生效。

`info_len`

`int`

info字段的数据长度，可忽略。

`data`

`byte[]`

返回当前片段的音频数据。

#### onTtsLogTrackCallback：监听追踪日志

此回调用于接收 SDK 内部的详细日志，方便进行问题定位和调试。

**方法签名：**
```
default void onTtsLogTrackCallback(Constants.LogLevel level, String log)
```

### TtsEvent

Sambert 语音合成事件类型枚举。

**事件**

**说明**

TTS\_EVENT\_START

合成任务开始，即将有音频数据返回。

TTS\_EVENT\_END

合成任务正常结束，所有音频数据已通过回调送出。

TTS\_EVENT\_CANCEL

合成任务已取消。

TTS\_EVENT\_PAUSE

合成任务已暂停。

TTS\_EVENT\_RESUME

合成任务已恢复。

TTS\_EVENT\_ERROR

合成过程中发生错误。此时可通过`getparamTTS("error_msg")`获取详细错误信息。

```
{
  "header": {
    "task_id": "xxxxxxxxx",
    "event": "task-failed",
    "error_code": "InvalidParameter",
    "error_message": "Please ensure input text is valid.",
    "attributes": {}
  },
  "payload": {}
}
```
