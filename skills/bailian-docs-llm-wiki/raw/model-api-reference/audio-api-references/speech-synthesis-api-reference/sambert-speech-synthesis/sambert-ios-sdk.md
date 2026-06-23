# 语音合成Sambert iOS SDK

本文档提供了语音合成Sambert iOS SDK的详细使用指南，帮助您将文本转换为高质量、富有表现力的语音。

**用户指南：**关于模型介绍和选型建议请参见[语音合成-Sambert](https://help.aliyun.com/zh/model-studio/text-to-speech)。

**在线体验**：暂不支持。

**重要**

百炼为华北2（北京）地域推出了业务空间专属域名 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，**能够为推理请求提供卓越的性能和更高的稳定性**，建议从 `https://dashscope.aliyuncs.com` 迁移至新域名。

其中 `{WorkspaceId}` 为您的业务空间 ID，可在百炼控制台的**业务空间详情**页面查看。现有域名仍可正常使用。

## **NeoNui**

本SDK基于NeoNui单例架构，通过回调机制处理语音合成事件。

**架构特点**：

-   **单例模式：**通过 `NeoNui.sharedInstance()` 获取全局唯一实例
    
-   **回调驱动：**通过 [`NeoNuiTtsDelegate`](#8b030fec74e01) 协议接收事件和数据
    
-   **事件类型：**
    
    -   [`TTS_EVENT_START`](#981ff433acpmr)：合成任务开始
        
    -   [`onNuiTtsUserdataCallback`](#bc71fe2545pfy)：音频数据返回
        
    -   [`TTS_EVENT_END`](#981ff433acpmr)：合成任务结束
        
    -   [`TTS_EVENT_ERROR`](#981ff433acpmr)：合成出错
        

### **使用流程**

1.  [`nui_tts_initialize()`](#5bb4ef17ebrds) - 初始化SDK，设置回调接口和连接参数
    
2.  [`nui_tts_set_param()`](#38454cd474pbz) - 设置语音合成效果参数（模型、音色、音量等）
    
3.  [`nui_tts_play()`](#secnuiplay) - 启动语音合成任务
    
4.  [`onNuiTtsUserdataCallback()`](#secuserdata) - 接收音频数据
    
5.  [`nui_tts_release()`](#secnuirelease) - 释放SDK资源
    

### **Sambert 方法**

#### nui\_tts\_initialize

初始化语音合成SDK实例。SDK为单例模式，在调用 [`nui_tts_release`](#secnuirelease) 前禁止重复初始化。

**方法签名：**

```
-(int) nui_tts_initialize:(const char *)parameters
                 logLevel:(NuiSdkLogLevel)level
                  saveLog:(BOOL)save_log;
```

**参数说明：**

**参数**

**类型**

**说明**

`parameters`

`char*`

JSON字符串，包含鉴权、连接和调试参数。详见下方 parameters 参数说明。

`level`

[`NuiSdkLogLevel`](#secnuisdkloglevel)

控制SDK自身日志的打印级别。

`save_log`

`BOOL`

是否保存本地日志。若为`YES`，须在 parameters 中通过`debug_path`指定路径，并可通过`max_log_file_size`设置文件大小。

**返回值说明：**

返回[错误码](https://help.aliyun.com/zh/isi/support/error-codes)。

**parameters JSON 示例**：以下为 JSON 字符串示例，参数未完整列出。请按实际需求在编码时补充：

```
{
    "url": "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference",
    "apikey": "st-****",
    "device_id": "my_device_id"
}
```

**parameters 参数说明：**

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

`device_id`

`String`

是

用于标识终端用户的唯一字符串，可设为应用内用户ID或客户端生成的设备唯一标识符。此ID主要用于日志追踪和问题排查。

`debug_path`

`String`

否

日志文件的存储路径。

此参数仅在调用[nui\_tts\_initialize](#5bb4ef17ebrds)接口时将[`save_log`](#3495f9200alb8)设为`YES`时生效。此时必须设置日志文件路径，否则将报错。

本地最多保留两个日志文件。

`max_log_file_size`

`int`

否

设定日志文件的最大字节数。

此参数仅在调用[nui\_tts\_initialize](#5bb4ef17ebrds)接口时将[`save_log`](#3495f9200alb8)设为`YES`时生效。

默认值：104857600（100 \* 1024 \* 1024 字节, 即 100MiB）。

`log_track_level`

`int`

否

控制通过日志回调（[onNuiTtsLogTrackCallback](#3a85f16402i13s)）对外发送的日志内容的过滤级别。

默认值：2。

取值范围：

-   0：LOG\_LEVEL\_VERBOSE
    
-   1：LOG\_LEVEL\_DEBUG
    
-   2：LOG\_LEVEL\_INFO
    
-   3：LOG\_LEVEL\_WARNING
    
-   4：LOG\_LEVEL\_ERROR
    
-   5：LOG\_LEVEL\_NONE（表示关闭此功能）
    

注意：`log_track_level`与[`level`](#5c67f9b2aeaq1)（通过[nui\_tts\_initialize](#5bb4ef17ebrds)接口设置）共同决定最终回调的日志。一条日志的级别数值必须同时大于或等于`log_track_level`和[`level`](#5c67f9b2aeaq1)的值，才会被回调。例如，`log_track_level`设为2 (INFO)，[`level`](#5c67f9b2aeaq1)设为3 (WARNING)，则只有WARNING及以上级别（数值>=3）的日志才会被回调。

#### nui\_tts\_set\_param

以键值对的形式设置参数。在 [`nui_tts_play`](#secnuiplay) 之前调用。

**方法签名：**

```
-(int) nui_tts_set_param:(const char *)param
                   value:(const char *)value;
```

**参数说明：**

**参数**

**类型**

**说明**

`param`

`char*`

参数名。

`value`

`char*`

参数值。

**返回值说明：**

返回[错误码](https://help.aliyun.com/zh/isi/support/error-codes)。

**可用参数说明：**

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

-   1：开启。当 format 为 mp3 时，设为 "1" 可开启SDK内置解码器，此时 onNuiTtsUserdataCallback 将返回解码后的PCM数据。
    
-   0：关闭。
    

#### nui\_tts\_get\_param

获取参数值。主要用于错误排查。

**方法签名：**

```
-(const char *) nui_tts_get_param:(const char *)param;
```

**参数说明：**

**参数**

**类型**

**说明**

`param`

`char*`

参数。目前仅支持"error\_msg"。

**返回值说明：**

返回参数值。

#### nui\_tts\_play

启动一个语音合成任务。

**方法签名：**

```
-(int) nui_tts_play:(const char *)priority
             taskId:(const char *)taskid
              text:(const char *)text;
```

**参数说明：**

**参数**

**类型**

**说明**

`priority`

`char*`

任务优先级。请将其设为1。

`taskid`

`char*`

任务ID。传入 `null` 时由SDK自动生成。

`text`

`char*`

待合成文本。

**返回值说明：**

返回[错误码](https://help.aliyun.com/zh/isi/support/error-codes)。

#### nui\_tts\_pause

暂停当前语音合成任务。任务暂停后，可通过 [`nui_tts_resume`](#secnuiresume) 恢复，或通过 [`nui_tts_cancel`](#secnuicancel) 彻底取消。在任务暂停期间，SDK不支持启动新的合成任务。

注意：此操作仅暂停从服务端的数据拉取，播放器中已缓存的音频数据会继续播放。

**方法签名：**

```
-(int) nui_tts_pause;
```

**返回值说明：**

返回[错误码](https://help.aliyun.com/zh/isi/support/error-codes)。

#### nui\_tts\_resume

恢复处于暂停的语音合成任务。

**方法签名：**

```
-(int) nui_tts_resume;
```

**返回值说明：**

返回[错误码](https://help.aliyun.com/zh/isi/support/error-codes)。

#### nui\_tts\_cancel

取消合成任务。

注意：此操作仅取消从服务端的数据拉取，播放器中已缓存的音频数据会继续播放。

**方法签名：**

```
-(int) nui_tts_cancel:(const char *)taskid;
```

**参数说明：**

**参数**

**类型**

**说明**

`taskid`

`char*`

要取消的任务ID。若传入 `null`，则取消所有正在暂停/进行中的合成任务。

**返回值说明：**

返回[错误码](https://help.aliyun.com/zh/isi/support/error-codes)。

#### nui\_tts\_release

释放SDK所有内部资源，并强制终止所有正在进行的合成任务。此方法调用后，SDK实例将变为不可用状态，如需再次使用，必须重新调用 [`nui_tts_initialize`](#5bb4ef17ebrds) 进行初始化。

**方法签名：**

```
-(int) nui_tts_release;
```

**返回值说明：**

返回[错误码](https://help.aliyun.com/zh/isi/support/error-codes)。

## **NeoNuiTtsDelegate**

Sambert 语音合成回调协议，用于接收合成事件、音频数据和日志。

### **方法**

#### onNuiTtsEventCallback**：监听事件**

**方法签名：**

```
- (void)onNuiTtsEventCallback:(NuiSdkTtsEvent)event taskId:(char*)taskid code:(int)code;
```

**参数说明：**

**参数**

**类型**

**说明**

`event`

[`NuiSdkTtsEvent`](#981ff433acpmr)

回调事件。

`taskid`

`char*`

语音合成任务ID。

`code`

`int`

错误码，仅在事件 [TTS\_EVENT\_ERROR](#981ff433acpmr) 中有效。参见[错误码](https://help.aliyun.com/zh/isi/support/error-codes)。

#### onNuiTtsUserdataCallback**：监听音频数据和时间戳信息**

**方法签名：**

```
- (void)onNuiTtsUserdataCallback:(char*)info infoLen:(int)info_len buffer:(char*)buffer len:(int)len taskId:(char*)task_id;
```

**参数说明：**

**参数**

**类型**

**说明**

`info`

`char*`

JSON格式的时间戳结果。`word_timestamp_enabled`设为`"1"`时生效。

`info_len`

`int`

info字段的数据长度，可忽略。

`buffer`

`char*`

返回当前片段的音频数据。

`len`

`int`

音频数据的长度（字节）。

`task_id`

`char*`

语音合成任务ID。

#### onNuiTtsLogTrackCallback**：监听追踪日志**

此回调用于接收 SDK 内部的详细日志，方便进行问题定位和调试。

**方法签名：**

```
- (void)onNuiTtsLogTrackCallback:(NuiSdkLogLevel)level
                      logMessage:(const char *)log;
```

**参数说明：**

**参数**

**类型**

**说明**

`level`

[`NuiSdkLogLevel`](#secnuisdkloglevel)

日志级别。

`log`

`char*`

日志内容。

## **NuiSdkTtsEvent**

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

合成过程中发生错误。此时可通过`nui_tts_get_param: "error_msg"`获取详细错误信息。

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

## **NuiSdkLogLevel**

SDK 日志级别枚举，用于控制日志输出。

**级别**

**说明**

0：LOG\_LEVEL\_VERBOSE

最详细的日志，包含所有调试信息。

1：LOG\_LEVEL\_DEBUG

调试级别日志。

2：LOG\_LEVEL\_INFO

常规信息级别日志（默认值）。

3：LOG\_LEVEL\_WARNING

警告级别日志。

4：LOG\_LEVEL\_ERROR

错误级别日志。

5：LOG\_LEVEL\_NONE

关闭日志输出。

## **示例代码**

1.  **获取API Key：**[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)
    
    **说明**
    
    当需要为第三方应用或用户提供临时访问权限，或者希望严格控制敏感数据访问、删除等高风险操作时，建议使用[临时API Key](https://help.aliyun.com/zh/model-studio/generate-temporary-api-key)。临时API Key拥有固定的60秒有效期，过期后需重新获取。
    
2.  **下载SDK并运行示例代码：**
    
    -   [下载最新SDK整合包](https://help.aliyun.com/zh/isi/sdk-selection-and-download)。
        
    -   解压 ZIP 包，将其中的 nuisdk.framework 添加到工程。
        
    -   在 Build Phases → Link Binary With Libraries 中添加 nuisdk.framework。
        
    -   在 General → Frameworks, Libraries, and Embedded Content 中将 nuisdk.framework 设置为 Embed & Sign。
        
    -   用 Xcode 打开示例工程。示例代码位于`DashSambertTTSViewController`，替换 API Key 后体验功能。
        

### **调用步骤**

1.  初始化 SDK。
    
2.  按业务需求设置参数：通过[`nui_tts_initialize`](#5bb4ef17ebrds)接口的`parameters`参数设置连接参数；通过[`nui_tts_set_param`](#38454cd474pbz)接口设置语音合成效果参数。
    
3.  调用 `[nui_tts_play](#secnuiplay)` 开始语音合成。
    
4.  在[onNuiTtsUserdataCallback](#secuserdata)回调中获取音频数据，建议使用流式播放。如需保存本地，按追加模式将音频写入同一文件，直到合成完成。
    
5.  任务结束后，调用`[nui_tts_release](#secnuirelease)`释放SDK资源。
