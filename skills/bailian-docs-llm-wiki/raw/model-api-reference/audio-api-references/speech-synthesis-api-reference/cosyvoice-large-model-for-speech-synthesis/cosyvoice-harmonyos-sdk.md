# Qwen-Audio-TTS/CosyVoice实时语音合成HarmonyOS SDK

了解实时语音合成HarmonyOS SDK的集成方法、参数、接口、回调和示例代码。

关于模型介绍和选型建议，请参见[语音合成](https://help.aliyun.com/zh/model-studio/tts-model)。

## NativeNui

HarmonyOS SDK通过 `NativeNui` 提供流式文本语音合成能力。

-   通过 `new NativeNui(Constants.ModeType.MODE_STREAM_INPUT_TTS)` 创建流式文本语音合成实例。`NativeNui.GetInstance()` 返回的是 `MODE_DIALOG` 对话模式单例，不能用于流式文本语音合成。
-   流式文本语音合成模式无需调用 `initialize()`。凭证和合成参数由 `startStreamInputTts()`、`playStreamInputTts()` 或 `asyncPlayStreamInputTts()` 直接传入。
-   通过 `INativeStreamInputTtsCallback` 接收合成事件和音频数据。
-   合成任务开始时返回 `STREAM_INPUT_TTS_EVENT_SYNTHESIS_STARTED`，音频数据通过 `onStreamInputTtsDataCallback` 返回，任务结束时返回 `STREAM_INPUT_TTS_EVENT_SYNTHESIS_COMPLETE`，合成出错时返回 `STREAM_INPUT_TTS_EVENT_TASK_FAILED`。

```
import { Constants, INativeStreamInputTtsCallback, NativeNui, StreamInputTtsEvent } from 'neonui';

const nuiInstance = new NativeNui(Constants.ModeType.MODE_STREAM_INPUT_TTS);
```

### 调用流程

Qwen-Audio-TTS/CosyVoice支持一次性输入和流式输入两种调用方式。

**一次性输入**：适用于短文本合成或需要使用[SSML](https://help.aliyun.com/zh/model-studio/ssml-latex-user-guide)的场景。

1.  调用 [playStreamInputTts](#playstreaminputtts) 或 [asyncPlayStreamInputTts](#asyncplaystreaminputtts)，直接传入完整文本并开始合成。前者同步阻塞，后者立即返回并在后台合成。无需先调用 `startStreamInputTts`，也无需再调用停止接口。
2.  在 [onStreamInputTtsDataCallback](#onstreaminputttsdatacallback) 中接收音频数据。
3.  收到 `STREAM_INPUT_TTS_EVENT_SYNTHESIS_COMPLETE` 后，合成结束。

**流式输入**：适用于实时对话或长文本边输入边合成的场景。该方式不支持SSML。

1.  调用 [startStreamInputTts](#startstreaminputtts) 建立连接并设置回调和参数。
2.  调用 [sendStreamInputTts](#sendstreaminputtts) 持续发送文本片段。
3.  在 [onStreamInputTtsDataCallback](#onstreaminputttsdatacallback) 中接收音频数据。
4.  文本发送完毕后，调用 [stopStreamInputTts](#stopstreaminputtts) 结束发送。
5.  收到 `STREAM_INPUT_TTS_EVENT_SYNTHESIS_COMPLETE` 后，合成结束。

不再使用语音合成功能时，调用 [releaseStreamInputTts](#releasestreaminputtts) 释放资源。

单次文本长度和多次累计文本长度均有限制，参见[CosyVoice WebSocket API](raw/model-api-reference/audio-api-references/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-websocket-api.md)。

### startStreamInputTts

启动双向流式语音合成，建立连接并注册回调。该接口可能阻塞，请勿在UI线程调用。

```
startStreamInputTts(
  callback: INativeStreamInputTtsCallback,
  ticket: string,
  parameters: string,
  session_id: string,
  log_level: number,
  save_log: boolean
): number
```

**参数**

**类型**

**说明**

`callback`

`INativeStreamInputTtsCallback`

事件和音频数据回调。

`ticket`

`string`

鉴权、连接和调试参数的JSON字符串。

`parameters`

`string`

语音合成参数的JSON字符串。

`session_id`

`string`

客户端指定的会话ID。传入空字符串时由服务端生成。

`log_level`

`number`

SDK日志级别，可使用 `Constants.LogLevel` 枚举值。取值：0（VERBOSE）、1（DEBUG）、2（INFO）、3（WARNING）、4（ERROR）、5（NONE）。

`save_log`

`boolean`

是否保存本地日志。设为 `true` 时必须在 `ticket` 中设置 `debug_path`。

返回[错误码](https://help.aliyun.com/zh/isi/support/error-codes)，`Constants.NuiResultCode.SUCCESS`（0）表示成功。

#### ticket参数

```
{
  "url": "wss://dashscope.aliyuncs.com/api-ws/v1/inference",
  "apikey": "st-****",
  "device_id": "my_device_id"
}
```

**参数**

**类型**

**是否必须**

**说明**

`url`

`string`

是

服务地址。可使用公共地址 `wss://dashscope.aliyuncs.com/api-ws/v1/inference`，或业务空间专属地址 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference`（北京）和 `wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/inference`（新加坡）。将 `{WorkspaceId}` 替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)。

`apikey`

`string`

是

API Key。建议使用[临时API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)，以降低长期有效Key泄露的风险。

`device_id`

`string`

是

终端用户的唯一标识，可使用应用内用户ID或客户端生成的设备标识，主要用于日志追踪和问题排查。

`complete_waiting_ms`

`number`

否

调用 `stopStreamInputTts(false)` 后等待合成完成事件的超时时间（毫秒），默认值为 `10000`。

`debug_path`

`string`

否

日志文件目录。仅当 `save_log` 为 `true` 时生效，此时必须设置。SDK最多保留两个日志文件。

`max_log_file_size`

`number`

否

单个日志文件的最大字节数。默认值为 `104857600`（100 MiB），仅当 `save_log` 为 `true` 时生效。

`log_track_level`

`number`

否

SDK内部追踪日志过滤级别，默认值为 `2`。取值与 `log_level` 相同。HarmonyOS回调接口当前未开放流式TTS日志回调，过滤后的日志仅在SDK内部输出。

#### parameters参数

```
{
  "model": "qwen-audio-3.0-tts-flash",
  "voice": "longanlingxi",
  "format": "mp3",
  "sample_rate": 24000,
  "volume": 50,
  "rate": 1.0,
  "pitch": 1.0,
  "enable_audio_decoder": true
}
```

**参数**

**类型**

**是否必须**

**说明**

`model`

`string`

是

模型名称。参见[语音合成模型](https://help.aliyun.com/zh/model-studio/tts-model)。

`voice`

`string`

是

音色。系统音色参见[Qwen-Audio-TTS音色列表](https://help.aliyun.com/zh/model-studio/qwen-audio-tts-voice-list)和[CosyVoice音色列表](https://help.aliyun.com/zh/model-studio/cosyvoice-voice-list)；也可使用声音复刻或[声音设计](https://help.aliyun.com/zh/model-studio/voice-design-user-guide)生成的音色。

`format`

`string`

否

音频编码格式，取值为 `pcm`、`wav`、`mp3`（默认）或 `opus`。`cosyvoice-v1` 不支持Opus。

`enable_audio_decoder`

`boolean`

否

是否启用SDK内部解码器，默认值为 `false`。当格式为MP3或Opus时，设为 `true` 可将音频解码为PCM后再通过数据回调返回。

`volume`

`number`

否

音量，默认值为 `50`，取值范围为 `[0, 100]`。

`sample_rate`

`number`

否

采样率（Hz），支持 `8000`、`16000`、`22050`（默认）、`24000`、`44100`、`48000`。

`rate`

`number`

否

语速，默认值为 `1.0`，取值范围为 `[0.5, 2.0]`。

`pitch`

`number`

否

音调，默认值为 `1.0`，取值范围为 `[0.5, 2.0]`。

`bit_rate`

`number`

否

MP3或Opus码率（kbps），默认值为 `32`，取值范围为 `[6, 510]`。`cosyvoice-v1` 不支持。

`enable_ssml`

`boolean`

否

是否启用SSML，默认值为 `false`。支持范围参见[SSML使用限制](https://help.aliyun.com/zh/model-studio/ssml-latex-user-guide#sl01_constraint_h3)。

`word_timestamp_enabled`

`boolean`

否

是否返回字级时间戳，默认值为 `false`，仅在流式输出模式下可用。支持qwen-audio-3.0-tts-plus、qwen-audio-3.1-tts-flash、qwen-audio-3.0-tts-flash、cosyvoice-v3.5-plus、cosyvoice-v3.5-flash、cosyvoice-v3-flash、cosyvoice-v3-plus和cosyvoice-v2的复刻音色，以及[Qwen-Audio-TTS音色列表](https://help.aliyun.com/zh/model-studio/qwen-audio-tts-voice-list)和[CosyVoice音色列表](https://help.aliyun.com/zh/model-studio/cosyvoice-voice-list)中标记为支持的系统音色；其他模型的复刻音色不支持。时间戳结果位于 `INativeStreamInputTtsCallback` 的 `all_response` 中。

`seed`

`number`

否

生成时使用的随机数种子，可改变合成效果。在模型版本、文本、音色和其他参数均相同时，使用相同的 `seed` 可复现相同的合成结果。默认值为 `0`，取值范围为 `[0, 65535]`。`cosyvoice-v1` 不支持。

`language_hints`

`string[]`

否

指定语音合成的目标语言，以提升合成效果。该设置与声音复刻时样本音频的语种无关；如需设置复刻任务的源语言，请参见声音复刻API参考。当前版本仅处理数组的第一个元素，建议只传一个值。当数字、缩写、符号的朗读方式或小语种合成效果不符合预期时，可设置该参数。例如，将 `"hello, this is 110"` 按英语读作“one one zero”而不是中文“幺幺零”，或将 `@` 读作“at”而不是“艾特”。支持 `zh`、`en`、`fr`、`de`、`ja`、`ko`、`ru`、`pt`、`th`、`id`、`vi`、`es`、`it`、`ms`、`fil` 和 `ar`。`cosyvoice-v1` 不支持。

`instruction`

`string`

否

控制方言、情感或角色等效果的指令，参见[指令控制](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#12884a10929p9)。

`enable_aigc_tag`

`boolean`

否

是否嵌入AIGC隐性标识，默认值为 `false`。仅qwen-audio-3.0-tts-plus、qwen-audio-3.1-tts-flash、qwen-audio-3.0-tts-flash、cosyvoice-v3-flash、cosyvoice-v3-plus和cosyvoice-v2支持。

`aigc_propagator`

`string`

否

AIGC标识的 `ContentPropagator` 字段，仅在 `enable_aigc_tag` 为 `true` 时生效。默认值为阿里云UID。支持范围与 `enable_aigc_tag` 相同。

`aigc_propagate_id`

`string`

否

AIGC标识的 `PropagateID` 字段，仅在 `enable_aigc_tag` 为 `true` 时生效。默认值为当前请求ID。支持范围与 `enable_aigc_tag` 相同。

`hot_fix`

`object`

否

文本热修复配置，用于自定义发音或替换文本。`cosyvoice-v2` 和 `cosyvoice-v1` 不支持；Qwen-Audio-3.0-TTS和其他支持模型可使用。格式参见[客户端事件](raw/model-api-reference/audio-api-references/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-client-events.md)。

### sendStreamInputTts

```
sendStreamInputTts(text: string): number
```

在 `startStreamInputTts` 成功后发送待合成的文本片段。该接口不解析SSML标签。全部文本发送完成后，调用 `stopStreamInputTts()`。

**参数**

**类型**

**说明**

`text`

`string`

待合成文本。不支持[SSML](https://help.aliyun.com/zh/model-studio/ssml-latex-user-guide)；SSML标签会被当作普通文本朗读。

返回[错误码](https://help.aliyun.com/zh/isi/support/error-codes)。

### stopStreamInputTts

```
stopStreamInputTts(flag_async: boolean = true): number
```

结束本轮流式输入。

-   `true`（默认）：异步结束，调用后立即返回，通过 `STREAM_INPUT_TTS_EVENT_SYNTHESIS_COMPLETE` 判断合成完成。
-   `false`：同步阻塞，等待全部音频和合成完成事件。等待时间由 `complete_waiting_ms` 控制。

使用同步停止后再调用取消接口可能造成阻塞，建议使用默认的异步方式。

**参数**

**类型**

**说明**

`flag_async`

`boolean`

是否异步结束，默认值为 `true`。设为 `true` 时不阻塞等待服务端响应；设为 `false` 时同步阻塞，等待合成完成。

返回[错误码](https://help.aliyun.com/zh/isi/support/error-codes)。

### cancelStreamInputTts

```
cancelStreamInputTts(): number
```

立即中断连接并终止当前合成任务。调用后不会再收到任何音频数据回调。返回[错误码](https://help.aliyun.com/zh/isi/support/error-codes)。

### cancelStreamInputTtsKeepConnection

```
cancelStreamInputTtsKeepConnection(): number
```

发送协议层取消指令，取消当前合成任务但保持WebSocket连接，适用于需要立即开始下一轮合成的场景，可省去重新建立连接的开销。返回[错误码](https://help.aliyun.com/zh/isi/support/error-codes)。

### playStreamInputTts

```
playStreamInputTts(
  callback: INativeStreamInputTtsCallback,
  ticket: string,
  parameters: string,
  text: string,
  session_id: string,
  log_level: number,
  save_log: boolean
): number
```

同步的一次性合成接口。该接口独立完成初始化、发送文本和接收音频，合成完成后才返回，无需先调用 `startStreamInputTts`，也无需调用停止接口。该接口默认启用SSML；如果显式设置 `enable_ssml`，则以设置值为准。请勿在UI线程调用。

`callback`、`ticket`、`parameters`、`session_id`、`log_level` 和 `save_log` 与 [startStreamInputTts](#startstreaminputtts) 中的定义相同。`text` 为待合成文本，支持[SSML](https://help.aliyun.com/zh/model-studio/ssml-latex-user-guide)。返回[错误码](https://help.aliyun.com/zh/isi/support/error-codes)。

### asyncPlayStreamInputTts

```
asyncPlayStreamInputTts(
  callback: INativeStreamInputTtsCallback,
  ticket: string,
  parameters: string,
  text: string,
  session_id: string,
  log_level: number,
  save_log: boolean
): number
```

异步的一次性合成接口。调用后立即返回，结果通过回调返回。无需先调用 `startStreamInputTts`，也无需调用停止接口。该接口默认启用SSML；如果显式设置 `enable_ssml`，则以设置值为准。

`callback`、`ticket`、`parameters`、`session_id`、`log_level` 和 `save_log` 与 [startStreamInputTts](#startstreaminputtts) 中的定义相同。`text` 为待合成文本，支持[SSML](https://help.aliyun.com/zh/model-studio/ssml-latex-user-guide)。返回[错误码](https://help.aliyun.com/zh/isi/support/error-codes)。

### releaseStreamInputTts

```
releaseStreamInputTts(): number
```

释放流式TTS实例及其占用的资源。建议在页面销毁或不再使用语音合成功能时调用。返回[错误码](https://help.aliyun.com/zh/isi/support/error-codes)。

## INativeStreamInputTtsCallback

```
export interface INativeStreamInputTtsCallback {
  onStreamInputTtsEventCallback(
    event: StreamInputTtsEvent,
    task_id: string,
    session_id: string,
    ret_code: number,
    error_msg: string,
    timestamp: string,
    all_response: string
  ): void;

  onStreamInputTtsDataCallback(data: ArrayBuffer | null): void;
}
```

### onStreamInputTtsEventCallback

**参数**

**类型**

**说明**

`event`

`StreamInputTtsEvent`

合成事件。

`task_id`

`string`

合成任务ID。

`session_id`

`string`

会话ID。客户端传入时原样返回，否则由服务端生成。

`ret_code`

`number`

错误码，仅任务失败事件有效。

`error_msg`

`string`

错误信息，仅任务失败事件有效。

`timestamp`

`string`

时间戳结果。

`all_response`

`string`

服务端完整JSON响应，可用于获取用量、时间戳和错误详情。

### onStreamInputTtsDataCallback

```
onStreamInputTtsDataCallback(data: ArrayBuffer | null): void;
```

连续返回音频片段。处理时需注意：

-   MP3和Opus压缩数据应使用支持流式解码的播放器，或将 `enable_audio_decoder` 设为 `true`，由SDK解码为PCM。
-   组装完整文件时，应按回调顺序追加数据。
-   WAV和MP3仅首个回调包含文件头；Opus的每一帧为独立Ogg page，可按顺序拼接。

## StreamInputTtsEvent

**事件**

**说明**

`STREAM_INPUT_TTS_EVENT_SYNTHESIS_STARTED`

服务端已成功接收请求并开始处理。通常在该事件后，`onStreamInputTtsDataCallback` 很快会返回第一批音频数据。

`STREAM_INPUT_TTS_EVENT_SENTENCE_BEGIN`

服务端开始合成一句文本。

`STREAM_INPUT_TTS_EVENT_SENTENCE_SYNTHESIS`

合成过程信息，包括计费信息和时间戳等。

`STREAM_INPUT_TTS_EVENT_SENTENCE_END`

服务端已完成一句文本的合成。

`STREAM_INPUT_TTS_EVENT_SYNTHESIS_COMPLETE`

服务端已返回全部音频数据，此后不会再调用 `onStreamInputTtsEventCallback`，是数据流结束的明确信号。该事件不表示本地播放器已经播放完成。

`STREAM_INPUT_TTS_EVENT_TASK_FAILED`

合成失败，可从 `all_response` 获取 `task_id`、`error_code` 和 `error_message`，也可通过回调参数 `ret_code` 和 `error_msg` 获取错误信息。

任务失败响应示例：

```
{
  "header": {
    "task_id": "2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx",
    "event": "task-failed",
    "error_code": "InvalidParameter",
    "error_message": "[tts:]Engine return error code: 418",
    "attributes": {}
  },
  "payload": {}
}
```

## 示例代码

1.  [获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。端侧应用请勿硬编码长期有效的API Key。建议由自建服务端获取[临时API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)，再下发到端侧。
2.  [下载最新SDK整合包](https://help.aliyun.com/zh/isi/sdk-selection-and-download)，解压后将 `entry/libs/neonui.har` 复制到应用工程的 `entry/libs` 目录，并在 `entry/oh-package.json5` 中添加依赖：

```
{
  "dependencies": {
    "neonui": "file:libs/neonui.har"
  }
}
```

3.  使用DevEco Studio打开整合包中的示例工程。示例页面位于 `entry/src/main/ets/pages/dashscope/DashCosyVoiceStreamTtsPage.ets`。配置API Key后即可运行。

以下示例展示流式输入的核心流程。音频播放、参数选择和任务状态管理的完整实现，请参考整合包中的 `DashCosyVoiceStreamTtsPage.ets`。

```
import { Constants, INativeStreamInputTtsCallback, NativeNui, StreamInputTtsEvent } from 'neonui';

const callback: INativeStreamInputTtsCallback = {
  onStreamInputTtsEventCallback: (event: StreamInputTtsEvent, taskId: string,
    sessionId: string, retCode: number, errorMsg: string,
    timestamp: string, allResponse: string): void => {
    if (event == StreamInputTtsEvent.STREAM_INPUT_TTS_EVENT_SYNTHESIS_COMPLETE) {
      // 合成完成。
    } else if (event == StreamInputTtsEvent.STREAM_INPUT_TTS_EVENT_TASK_FAILED) {
      // 根据retCode、errorMsg或allResponse处理错误。
    }
  },
  onStreamInputTtsDataCallback: (data: ArrayBuffer | null): void => {
    if (data != null) {
      // 将PCM数据写入AudioRenderer，或按顺序保存编码音频数据。
    }
  }
};

const nuiInstance = new NativeNui(Constants.ModeType.MODE_STREAM_INPUT_TTS);
const ticket: Record<string, Object> = {
  'url': 'wss://dashscope.aliyuncs.com/api-ws/v1/inference',
  'apikey': 'st-****',
  'device_id': 'my_device_id'
};
const parameters: Record<string, Object> = {
  'model': 'qwen-audio-3.0-tts-flash',
  'voice': 'longanlingxi',
  'format': 'mp3',
  'sample_rate': 24000,
  'enable_audio_decoder': true
};

const result = nuiInstance.startStreamInputTts(
  callback,
  JSON.stringify(ticket),
  JSON.stringify(parameters),
  '',
  Constants.LogLevel.LOG_LEVEL_INFO,
  false
);

if (result == Constants.NuiResultCode.SUCCESS) {
  nuiInstance.sendStreamInputTts('你好，');
  nuiInstance.sendStreamInputTts('欢迎使用实时语音合成。');
  nuiInstance.stopStreamInputTts(true);
}

// 在SYNTHESIS_COMPLETE的处理逻辑中调用nuiInstance.releaseStreamInputTts()。
```

一次性输入时，直接调用 `playStreamInputTts` 或 `asyncPlayStreamInputTts`：

```
const oneShotInstance = new NativeNui(Constants.ModeType.MODE_STREAM_INPUT_TTS);
oneShotInstance.asyncPlayStreamInputTts(
  callback,
  JSON.stringify(ticket),
  JSON.stringify(parameters),
  '你好，欢迎使用实时语音合成。',
  '',
  Constants.LogLevel.LOG_LEVEL_INFO,
  false
);
// 在SYNTHESIS_COMPLETE的处理逻辑中调用oneShotInstance.releaseStreamInputTts()。
```

## 高级功能

### SSML标记语言

**目的**：通过在文本中嵌入XML标签，控制发音、语速和停顿等合成细节。

**使用限制**：仅一次性输入接口 `playStreamInputTts` 和 `asyncPlayStreamInputTts` 支持SSML；流式输入接口 `sendStreamInputTts` 不支持。

**使用方法**：调用 `playStreamInputTts` 或 `asyncPlayStreamInputTts` 时，SDK默认启用SSML，直接在 `text` 中传入包含SSML标签的文本。更多信息，请参见[SSML与LaTeX](https://help.aliyun.com/zh/model-studio/ssml-latex-user-guide)。

### 数学表达式

**目的**：使模型能够正确朗读常见的数学公式和表达式。

**使用方法**：在 `text` 中传入包含LaTeX格式数学表达式的文本。支持范围和写法，请参见[LaTeX公式转语音](https://help.aliyun.com/zh/model-studio/latex-capability-support-description)。
