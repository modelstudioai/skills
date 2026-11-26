# Sambert HarmonyOS SDK

使用 Sambert HarmonyOS SDK 合成语音，了解初始化参数、合成方法及回调事件。

**用户指南：** 关于模型介绍和选型建议，请参见[语音合成-Sambert](https://help.aliyun.com/zh/model-studio/text-to-speech)。

**在线体验**：暂不支持。

<a id="前提条件"></a>

## 前提条件

[获取与配置 API Key](../model-api-reference/preparations/get-api-key.md)。移动端应用请勿硬编码长期 API Key。建议由应用服务端[生成临时 API Key](../model-api-reference/more-about-models/generate-temporary-api-key.md)，再下发给客户端。

> **重要**
>
> 阿里云百炼为华北2（北京）地域提供业务空间专属域名，可提升推理请求的性能和稳定性。建议从 `dashscope.aliyuncs.com` 迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`。

请将 `{WorkspaceId}` 替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。现有域名仍可正常使用。

<a id="安装-sdk"></a>

### 安装 SDK

1.  [下载最新 SDK 整合包](../model-api-reference/more-about-models/sdk-selection-and-download.md)。
2.  解压 TAR 包，将 `neonui` 目录中的 HAR SDK 添加到项目依赖。
3.  如需接入 C++，从 TAR 包内的 `native/libs` 和 `native/include` 获取动态库和头文件。

<a id="快速开始"></a>

<a id="示例代码"></a>

## 快速开始

用 DevEco Studio 打开示例工程。示例代码位于 `DashSambertTtsPage.ets`，替换 API Key 后运行示例。合成时通过回调接收音频数据。

<a id="调用步骤"></a>

<a id="使用流程"></a>

### 调用步骤

1.  使用 `new NativeNui(Constants.ModeType.MODE_TTS)` 创建实例。调用 [`tts_initialize`](#tts-initialize)，传入 `NuiTtsSdkListener` 回调和 `ticket` 参数。请在非 UI 线程中调用。
2.  按业务需求设置参数：通过 [setParamTts](#setparamtts) 接口设置模型、格式、采样率、音色和音量等语音合成效果参数。建议在初始化成功后立即设置。
3.  调用 [`startTts`](#starttts) 开始语音合成。
4.  在 [onTtsDataCallback](#onttsdatacallback) 回调中获取音频数据。建议使用流式播放，详情请参见下方音频播放说明。如需保存到本地，请按追加模式将音频写入同一文件，直至合成完成。
5.  任务结束后，调用 [`tts_release`](#tts-release) 释放 SDK 资源。

<a id="音频播放说明"></a>

### 音频播放说明

HarmonyOS 通过 `@kit.AudioKit` 的 `AudioRenderer` 播放合成音频。Sambert 合成音频默认采样率为 **48kHz**，因此需将播放器采样率设置为 48000。

本产品样例已封装为 `AudioPlayer.ets` 工具类，构造时指定采样率：

<a id="code-block"></a>

```typescript
// Sambert默认按48000采样率播放（AudioPlayer默认是16000）
this.mAudioPlayer = new AudioPlayer(this, 48000);
```

播放器通过 `writeData` 回调从队列拉取音频数据，返回 `AudioDataCallbackResult.VALID`/`INVALID`。当 `onTtsEventCallback` 收到 `TTS_EVENT_END` 后，SDK 已合成完所有数据并通过回调送出，此时应标记播放队列推送完成，播放器播完剩余数据后自动停止。

> **说明**
>
> **MP3 播放**：`AudioRenderer` 仅支持 PCM 播放。当 `format` 设为 `mp3` 时，需同时将 `enable_audio_decoder` 设为 `"1"`，SDK 内置解码器会将 mp3 解码成 PCM 后经 `onTtsDataCallback` 返回；`mEncodeType` 仅用于生成的音频文件名扩展，不影响回调数据类型。

<a id="请求参数"></a>

## 请求参数

<a id="连接参数-ticket"></a>

<a id="connection-parameters"></a>

### 连接参数（ticket）

**ticket JSON 示例**：

<a id="code-block-2"></a>

```json
{
    "url": "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference",
    "apikey": "sk-****",
    "device_id": "my_device_id",
    "mode_type": "2"
}
```

**ticket 参数说明：**

| 参数 | 类型 | 是否必须 | 说明 |
| --- | --- | --- | --- |
| `url` | `string` | 是 | 服务地址，固定为 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference`。 调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。 |
| `apikey` | `string` | 是 | API Key。建议使用时效性短、安全性更高的[临时API Key](../model-api-reference/more-about-models/generate-temporary-api-key.md)，以降低长期有效Key泄露的风险。 |
| `mode_type` | `string` | 是 | 模式类型。必须设置为字符串 `"2"`，代表在线语音合成模式（对应 `Constants.TtsModeTypeCloud`）。 |
| `device_id` | `string` | 是 | 用于标识终端用户的唯一字符串，可设为应用内用户ID或客户端生成的设备唯一标识符。此ID主要用于日志追踪和问题排查。 |
| `debug_path` | `string` | 否 | 日志文件的存储路径。 此参数仅在调用tts\_initialize接口时将`save_log`设为true时生效。此时必须设置日志文件路径，否则将报错。 本地最多保留两个日志文件。 |
| `max_log_file_size` | `number` | 否 | 设定日志文件的最大字节数。 此参数仅在调用tts\_initialize接口时将`save_log`设为true时生效。 默认值：104857600（100 \* 1024 \* 1024 字节, 即 100MiB）。 |

<a id="合成参数"></a>

<a id="synthesis-parameters"></a>

### 合成参数

| 参数 | 类型 | 是否必须 | 说明 |
| --- | --- | --- | --- |
| `model` | `string` | 是 | 模型名称，如 `sambert-zhinan-v1`。 |
| `format` | `string` | 否 | 音频编码格式。 取值范围： - pcm - wav - mp3（默认） |
| `volume` | `string` | 否 | 音量。 默认值：50。 取值范围：`[0, 100]`。 |
| `sample_rate` | `string` | 否 | 音频采样率（Hz）。 取值范围：8000, 16000, 22050, 24000, **48000**。Sambert 大部分发音人模型默认采样率为 **48000**，播放器需按对应采样率播放。 |
| `rate` | `string` | 否 | 语速。 默认值：1.0。 取值范围：`[0.5, 2.0]`。 |
| `pitch` | `string` | 否 | 音调。 默认值：1.0。 取值范围：`[0.5, 2.0]`。 |
| `word_timestamp_enabled` | `string` | 否 | 是否开启字级别时间戳。 默认值：false。 适用范围：所有 Sambert 模型。 |
| `phoneme_timestamp_enabled` | `string` | 否 | 是否开启音素级别时间戳。 默认值：false。 需要先开启`word_timestamp_enabled`。 |
| `enable_audio_decoder` | `string` | 否 | 是否开启内置音频解码器。 默认值：0。 取值范围： - 1：开启。当 format 为 mp3 时，设为 "1" 可开启SDK内置解码器，此时 [onTtsDataCallback](#onttsdatacallback) 将返回解码后的PCM数据。 - 0：关闭。 |
| `enable_callback_vol` | `string` | 否 | 是否开启音量回调。设为 `"1"` 后启用 [onTtsVolCallback](#onttsvolcallback) 回调。 |
| `apikey` | `string` | 否 | 运行中刷新临时 API Key。在合成任务开始前通过 `setParamTts('apikey', ...)` 注入最新临时 Key。 |

<a id="接口参考"></a>

## 接口参考

<a id="nativenui"></a>

### NativeNui

本 SDK 基于 NativeNui 架构，通过回调机制处理语音合成事件。

**架构特点**：

-   **实例模式**：通过 `new NativeNui(Constants.ModeType.MODE_TTS)` 创建语音合成实例。
-   **回调驱动**：通过 [NuiTtsSdkListener](#nuittssdklistener) 接口接收事件和数据。
-   **事件类型：**
    -   [NuiSdkTtsEvent](#nuisdkttsevent)：合成任务开始。
    -   [onTtsDataCallback](#onttsdatacallback)：返回音频数据。
    -   [NuiSdkTtsEvent](#nuisdkttsevent)：合成任务结束。
    -   [NuiSdkTtsEvent](#nuisdkttsevent)：合成出错。

<a id="tts-initialize"></a>

<a id="sambert-方法"></a>

#### tts\_initialize

初始化语音合成 SDK 实例。通过 `new NativeNui(Constants.ModeType.MODE_TTS)` 创建实例，每个实例对应一个语音合成通道。同一实例在调用 [tts\_release](#tts-release) 前禁止重复初始化；如需同时处理多个任务，请创建多个实例。

该接口会阻塞调用线程，请在非 UI 线程中调用。

**方法签名：**

<a id="code-block-3"></a>

```typescript
public tts_initialize(callback: NuiTtsSdkListener,
                      ticket: string,
                      level: number,
                      save_log: boolean): number
```

**参数说明：**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `callback` | [NuiTtsSdkListener](#nuittssdklistener) | 事件和数据回调接口的实现。 |
| `ticket` | `string` | JSON字符串，包含鉴权、连接和调试参数。详见[连接参数](#connection-parameters)。 |
| `level` | `number` | 控制SDK自身日志的打印级别，取值为[Constants.LogLevel](#constants-loglevel)枚举。 |
| `save_log` | `boolean` | 是否保存本地日志。若为true，须在 ticket 参数中通过`debug_path`指定路径，并可通过`max_log_file_size`设置文件大小。 |

<a id="setparamtts"></a>

#### setParamTts

以键值对的形式设置语音合成效果参数。在 [startTts](#starttts) 之前调用。

**方法签名：**

<a id="code-block-4"></a>

```typescript
public setParamTts(param: string, value: string): number
```

**参数说明：**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `param` | `string` | 参数名。 |
| `value` | `string` | 参数值。 |

可设置的键和值见[合成参数](#synthesis-parameters)。

<a id="getparamtts"></a>

#### getparamTts

获取参数值。主要用于错误排查。

**方法签名：**

<a id="code-block-5"></a>

```typescript
public getparamTts(param: string): string
```

**参数说明：**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `param` | `string` | 参数名。目前仅支持"error\_msg"。 |

**返回值说明：**

返回参数值。

<a id="starttts"></a>

#### startTts

启动语音合成任务。合成结果通过回调返回。

**方法签名：**

<a id="code-block-6"></a>

```typescript
public startTts(priority: string, taskid: string, text: string): number
```

**参数说明：**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `priority` | `string` | 任务优先级。请将其设为1。 |
| `taskid` | `string` | 任务ID。传入空字符串 `''` 时由SDK自动生成。 |
| `text` | `string` | 待合成文本。 |

<a id="pausetts"></a>

#### pauseTts

暂停当前语音合成任务。任务暂停后，可通过 [resumeTts](#resumetts) 恢复，或通过 [cancelTts](#canceltts) 彻底取消。在任务暂停期间，SDK不支持启动新的合成任务。

注意：此操作仅暂停从服务端的数据拉取，播放器中已缓存的音频数据会继续播放。

**方法签名：**

<a id="code-block-7"></a>

```typescript
public pauseTts(): number
```

<a id="resumetts"></a>

#### resumeTts

恢复处于暂停的语音合成任务。

**方法签名：**

<a id="code-block-8"></a>

```typescript
public resumeTts(): number
```

<a id="canceltts"></a>

#### cancelTts

取消合成任务。

注意：此操作仅取消从服务端的数据拉取，播放器中已缓存的音频数据会继续播放。

**方法签名：**

<a id="code-block-9"></a>

```typescript
public cancelTts(taskid: string): number
```

**参数说明：**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `taskid` | `string` | 要取消的任务ID。若传入空字符串 `''`，则取消所有正在暂停/进行中的合成任务。 |

<a id="tts-release"></a>

#### tts\_release

释放 SDK 的所有内部资源，并强制终止所有正在进行的合成任务。调用后，SDK 实例将不可用；如需再次使用，必须重新调用 [tts\_initialize](#tts-initialize) 进行初始化。

**方法签名：**

<a id="code-block-10"></a>

```typescript
public tts_release(): number
```

<a id="nuittssdklistener"></a>

### NuiTtsSdkListener

Sambert 语音合成回调接口，用于接收合成事件和音频数据。在 HarmonyOS SDK 中，回调接口通过 ArkTS 箭头函数形式定义。

<a id="onttseventcallback"></a>

#### onTtsEventCallback

监听语音合成任务的开始、结束、取消、暂停、恢复和错误事件。

**方法签名：**

<a id="code-block-11"></a>

```typescript
onTtsEventCallback: (event: NuiSdkTtsEvent, taskid: string, ret_code: number) => void;
```

**参数说明：**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `event` | [NuiSdkTtsEvent](#nuisdkttsevent) | 回调事件。 |
| `taskid` | `string` | 语音合成任务ID。 |
| `ret_code` | `number` | 仅在出现 [`TTS_EVENT_ERROR`](#nuisdkttsevent) 事件时有效。 |

<a id="onttsdatacallback"></a>

#### onTtsDataCallback

监听语音合成过程中返回的音频数据和时间戳信息。合成期间，SDK 会连续触发该回调。

**方法签名：**

<a id="code-block-12"></a>

```typescript
onTtsDataCallback: (info: string, info_len: number, buffer: ArrayBuffer | null) => void;
```

**参数说明：**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `info` | `string` | JSON格式的时间戳结果。`word_timestamp_enabled`设为`"1"`时生效。 |
| `info_len` | `number` | info字段的数据长度，可忽略。 |
| `buffer` | `ArrayBuffer \| null` | 返回当前片段的音频数据。可能为`null`，回调中需判空。 |

> **说明**
>
> 底层可能复用`buffer`，若需缓存，请先拷贝一份（如 `new Uint8Array(buffer.slice(0))`）再使用。

<a id="onttsvolcallback"></a>

#### onTtsVolCallback

监听合成音量。启用 `enable_callback_vol` 参数后，该回调返回 SDK 刚收到的合成数据音量，而非当前播放音量。

**方法签名：**

<a id="code-block-13"></a>

```typescript
onTtsVolCallback: (vol: number) => void;
```

**参数说明：**

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `vol` | `number` | 合成数据音量值。 |

<a id="nuisdkttsevent"></a>

### NuiSdkTtsEvent

Sambert 语音合成事件类型枚举。

| 事件 | 说明 |
| --- | --- |
| `TTS_EVENT_START` | 合成任务开始，即将有音频数据返回。 |
| `TTS_EVENT_END` | 合成任务正常结束，所有音频数据已通过回调送出。 |
| `TTS_EVENT_CANCEL` | 合成任务已取消。 |
| `TTS_EVENT_PAUSE` | 合成任务已暂停。 |
| `TTS_EVENT_RESUME` | 合成任务已恢复。 |
| `TTS_EVENT_ERROR` | 合成过程中发生错误。此时可通过`getparamTts("error_msg")`获取详细错误信息。 `{ "header": { "task_id": "xxxxxxxxx", "event": "task-failed", "error_code": "InvalidParameter", "error_message": "Please ensure input text is valid.", "attributes": {} }, "payload": {} }` |

> **重要**
>
> `TTS_EVENT_END` 事件表示 TTS 已合成完并通过回调传回了所有音频数据，**不代表播放器已经播放完了所有音频数据**。

<a id="constants-loglevel"></a>

<a id="辅助类型"></a>

### Constants.LogLevel

`level` 参数的取值枚举：

| 值 | 说明 |
| --- | --- |
| `LOG_LEVEL_VERBOSE` | 最详细日志。 |
| `LOG_LEVEL_DEBUG` | 调试日志。 |
| `LOG_LEVEL_INFO` | 普通信息日志（默认）。 |
| `LOG_LEVEL_WARNING` | 警告日志。 |
| `LOG_LEVEL_ERROR` | 错误日志。 |
| `LOG_LEVEL_NONE` | 关闭日志。 |
