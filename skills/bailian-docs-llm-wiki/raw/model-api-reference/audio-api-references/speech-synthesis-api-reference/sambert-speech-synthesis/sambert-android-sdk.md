# 语音合成Sambert Android SDK

本文档提供了语音合成Sambert Android SDK的详细使用指南，帮助您将文本转换为高质量、富有表现力的语音。

**用户指南：**关于模型介绍和选型建议请参见[语音合成-Sambert](https://help.aliyun.com/zh/model-studio/text-to-speech)。

**在线体验**：暂不支持。

**重要**

百炼为华北2（北京）地域推出了业务空间专属域名 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，**能够为推理请求提供卓越的性能和更高的稳定性**，建议从 `https://dashscope.aliyuncs.com` 迁移至新域名。

其中 `{WorkspaceId}` 为您的业务空间 ID，可在百炼控制台的**业务空间详情**页面查看。现有域名仍可正常使用。

## **NativeNui**

本SDK基于NativeNui单例架构，通过回调机制处理语音合成事件。

**架构特点**：

-   **单例模式：**通过 `NativeNui.GetInstance()` 获取全局唯一实例
    
-   **回调驱动：**通过 [`INativeTtsCallback`](#8b030fec74e01) 接口接收事件和数据
    
-   **事件类型：**
    
    -   [`TTS_EVENT_START`](#981ff433acpmr)：合成任务开始
        
    -   [`onTtsDataCallback`](#bc71fe2545pfy)：音频数据返回
        
    -   [`TTS_EVENT_END`](#981ff433acpmr)：合成任务结束
        
    -   [`TTS_EVENT_ERROR`](#981ff433acpmr)：合成出错
        

### **使用流程**

1.  [`tts_initialize()`](#ae6d7dd9cfad3) - 初始化SDK，设置回调接口和连接参数
    
2.  [`setparamTts()`](#a23e0d85d7ymt) - 设置语音合成效果参数（模型、音色、音量等）
    
3.  [`startTts()`](#7d33691bdb32v) - 启动语音合成任务
    
4.  [`onTtsDataCallback()`](#bc71fe2545pfy) - 接收音频数据
    
5.  [`tts_release()`](#44bf12ed9a4g9) - 释放SDK资源
    

### **Sambert 方法**

#### **tts\_initialize**

初始化语音合成SDK实例。SDK为单例模式，在调用 [`tts_release()`](#44bf12ed9a4g9) 前禁止重复初始化。

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

[`INativeTtsCallback`](#8b030fec74e01)

事件和数据回调接口的实现。

`ticket`

`String`

JSON字符串，包含鉴权、连接和调试参数。详见下方 ticket 参数说明。

`level`

`Constants.LogLevel`

控制SDK自身日志的打印级别。

`save_log`

`boolean`

是否保存本地日志。若为true，须在 ticket 参数中通过`debug_path`指定路径，并可通过`max_log_file_size`设置文件大小。

**返回值说明：**

返回[错误码](https://help.aliyun.com/zh/isi/support/error-codes)。

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

服务地址，固定为 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference`。

调用时请将`WorkspaceId`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)。

`apikey`

`String`

是

API Key。建议使用时效性短、安全性更高的[临时API Key](https://help.aliyun.com/zh/model-studio/generate-temporary-api-key)，以降低长期有效Key泄露的风险。

`mode_type`

`String`

是

模式类型。必须设置为字符串 `"2"`，代表在线语音合成模式。

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

控制通过日志回调（[`onTtsLogTrackCallback`](#9c10968457gc6)）对外发送的日志内容的过滤级别。

默认值：2。

取值范围：

-   0：LOG\_LEVEL\_VERBOSE
    
-   1：LOG\_LEVEL\_DEBUG
    
-   2：LOG\_LEVEL\_INFO
    
-   3：LOG\_LEVEL\_WARNING
    
-   4：LOG\_LEVEL\_ERROR
    
-   5：LOG\_LEVEL\_NONE（表示关闭此功能）
    

注意：`log_track_level`与`log_level`（通过tts\_initialize接口设置）共同决定最终回调的日志。一条日志的级别数值必须同时大于或等于`log_track_level`和`log_level`的值，才会被回调。例如，`log_track_level`设为2 (INFO)，`log_level`设为3 (WARNING)，则只有WARNING及以上级别（数值>=3）的日志才会被回调。

#### **setparamTts**

以键值对的形式设置语音合成效果参数。在 [`startTts()`](#7d33691bdb32v) 之前调用。

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

**返回值说明：**

返回[错误码](https://help.aliyun.com/zh/isi/support/error-codes)。

**可用参数说明**：

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

-   1：开启。当 format 为 mp3 时，设为 "1" 可开启SDK内置解码器，此时 [onTtsDataCallback](#bc71fe2545pfy) 将返回解码后的PCM数据。
    
-   0：关闭。
    

#### **getparamTts**

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

#### **startTts**

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

任务ID。传入 `null` 时由SDK自动生成。

`text`

`String`

待合成文本。

**返回值说明：**

返回[错误码](https://help.aliyun.com/zh/isi/support/error-codes)。

#### **pauseTts**

暂停当前语音合成任务。任务暂停后，可通过 [`resumeTts()`](#01f640f02bka9) 恢复，或通过 [`cancelTts()`](#8c464959f9lm9) 彻底取消。在任务暂停期间，SDK不支持启动新的合成任务。

注意：此操作仅暂停从服务端的数据拉取，播放器中已缓存的音频数据会继续播放。

**方法签名：**

```
public synchronized int pauseTts()
```

**返回值说明：**

返回[错误码](https://help.aliyun.com/zh/isi/support/error-codes)。

#### **resumeTts**

恢复处于暂停的语音合成任务。

**方法签名：**

```
public synchronized int resumeTts()
```

**返回值说明：**

返回[错误码](https://help.aliyun.com/zh/isi/support/error-codes)。

#### **cancelTts**

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

要取消的任务ID。若传入 `null`，则取消所有正在暂停/进行中的合成任务。

**返回值说明：**

返回[错误码](https://help.aliyun.com/zh/isi/support/error-codes)。

#### **tts\_release**

释放SDK所有内部资源，并强制终止所有正在进行的合成任务。此方法调用后，SDK实例将变为不可用状态，如需再次使用，必须重新调用 [`tts_initialize()`](#ae6d7dd9cfad3) 进行初始化。

**方法签名：**

```
public synchronized int tts_release()
```

**返回值说明：**

返回[错误码](https://help.aliyun.com/zh/isi/support/error-codes)。

## **INativeTtsCallback**

Sambert 语音合成回调接口，用于接收合成事件和音频数据。

### onTtsEventCallback**：监听事件**

**方法签名：**

```
void onTtsEventCallback(TtsEvent event, String task_id, int ret_code);
```

**参数说明：**

**参数**

**类型**

**说明**

`event`

[`TtsEvent`](#981ff433acpmr)

回调事件。

`task_id`

`String`

语音合成任务ID。

`ret_code`

`int`

[错误码](https://help.aliyun.com/zh/isi/support/error-codes)，仅在事件 [TTS\_EVENT\_ERROR](#981ff433acpmr) 中有效。

### onTtsDataCallback**：监听音频数据和时间戳信息**

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

### onTtsLogTrackCallback**：监听追踪日志**

此回调用于接收 SDK 内部的详细日志，方便进行问题定位和调试。

**方法签名：**

```
default void onTtsLogTrackCallback(Constants.LogLevel level, String log)
```

## **TtsEvent**

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

## **示例代码**

1.  **获取API Key：**[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，为安全起见，推荐将API Key配置到环境变量。
    
    **说明**
    
    当需要为第三方应用或用户提供临时访问权限，或者希望严格控制敏感数据访问、删除等高风险操作时，建议使用[临时API Key](https://help.aliyun.com/zh/model-studio/generate-temporary-api-key)。临时API Key默认拥有60秒有效期，过期后需重新获取。
    
2.  **下载SDK并运行示例代码：**
    
    -   [下载最新SDK整合包](https://help.aliyun.com/zh/isi/sdk-selection-and-download)。
        
    -   解压 ZIP 包。在 `app/libs` 目录中获取 AAR 格式 SDK，并添加到项目依赖。  
        需要 Android CPP 接入时，使用 ZIP 包内的 `android_libs` 与 `android_include` 获取动态库和头文件。  
          
          
          
          
          
          
          
        
    -   用 Android Studio 打开工程。示例代码位于`DashSambertTtsActivity.java`，替换 API Key 后体验功能。
        

### **调用步骤**

1.  初始化 SDK。
    
2.  按业务需求设置参数：通过[tts\_initialize](#ae6d7dd9cfad3)接口的`ticket`参数设置连接与控制参数；通过[setparamTts](#a23e0d85d7ymt)接口设置语音合成效果参数。
    
3.  调用 `[startTts](#7d33691bdb32v)` 开始语音合成。
    
4.  在[onTtsDataCallback](#bc71fe2545pfy)回调中获取音频数据，建议使用流式播放。如需保存本地，按追加模式将音频写入同一文件，直到合成完成。
    
5.  任务结束后，调用 `[tts_release](#44bf12ed9a4g9)` 释放SDK资源。
