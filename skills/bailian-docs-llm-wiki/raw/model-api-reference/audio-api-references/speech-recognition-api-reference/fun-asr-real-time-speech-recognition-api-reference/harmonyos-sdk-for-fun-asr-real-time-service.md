# Qwen-Audio-3.x-ASR-Flash-Streaming/Fun-ASR-Realtime实时语音识别HarmonyOS SDK

了解实时语音识别HarmonyOS SDK的集成方法、请求参数、接口、回调和示例代码。

关于模型介绍和选型建议，请参见[语音识别](https://help.aliyun.com/zh/model-studio/asr-model)。

## 快速开始

1.  [获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。端侧应用请勿硬编码长期有效的API Key。建议由自建服务端获取[临时API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)，再下发到端侧。
2.  [下载最新SDK整合包](https://help.aliyun.com/zh/isi/sdk-selection-and-download)，解压后将 `entry/libs/neonui.har` 复制到应用工程的 `entry/libs` 目录，并在 `entry/oh-package.json5` 中添加依赖：

```
{
  "dependencies": {
    "neonui": "file:libs/neonui.har"
  }
}
```

如需通过HarmonyOS C++接口接入，可使用整合包 `native/libs` 目录中的动态库和 `native/include` 目录中的头文件。

3.  在应用的 `module.json5` 中声明网络和麦克风权限，并在运行时申请麦克风权限。`reason_internet` 和 `reason_microphone` 为示例资源名，请在应用资源中定义对应说明。

```
"requestPermissions": [
  {
    "name": "ohos.permission.INTERNET",
    "reason": "$string:reason_internet",
    "usedScene": { "abilities": ["EntryAbility"], "when": "always" }
  },
  {
    "name": "ohos.permission.MICROPHONE",
    "reason": "$string:reason_microphone",
    "usedScene": { "abilities": ["EntryAbility"], "when": "always" }
  }
]
```

4.  使用DevEco Studio打开整合包中的示例工程。示例页面位于 `entry/src/main/ets/pages/dashscope/DashFunAsrSpeechTranscriberPage.ets`。配置API Key后即可运行。

### 调用步骤

1.  创建 `NativeNui(Constants.ModeType.MODE_DIALOG)` 实例。
2.  调用 [initialize](#initialize) 初始化SDK，并设置连接与控制参数。
3.  调用 [setParams](#setparams) 设置模型及识别效果参数。
4.  调用 [startDialog](#startdialog) 启动识别。
5.  在 [onNuiAudioStateChanged](#onnuiaudiostatechanged) 中根据音频状态启动、暂停或关闭录音设备。
6.  在 [onNuiNeedAudioData](#onnuineedaudiodata) 中持续提供录音数据；如果启用了主动推送模式，则调用 [updateAudio](#updateaudio) 推送数据。
7.  在 [onNuiEventCallback](#onnuieventcallback) 中获取识别结果和任务状态。
8.  调用 [stopDialog](#stopdialog) 停止识别，并等待 `EVENT_TRANSCRIBER_COMPLETE` 事件。
9.  不再使用识别功能时，调用 [release](#release) 释放资源。

## 请求参数

### 连接与控制参数

通过 [initialize](#initialize) 的 `parameters` 参数传入JSON字符串。

```
{
  "url": "wss://dashscope.aliyuncs.com/api-ws/v1/inference",
  "device_id": "my_device_id",
  "service_mode": "1",
  "audio_update_manually": "false"
}
```

**参数**

**类型**

**是否必须**

**说明**

`url`

`string`

是

服务地址。可使用公共地址 `wss://dashscope.aliyuncs.com/api-ws/v1/inference`，或业务空间专属地址 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference`（北京）和 `wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/inference`（新加坡）。将 `{WorkspaceId}` 替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

`service_mode`

`string`

是

运行模式。实时语音识别固定为 `"1"`，即 `Constants.ModeFullCloud`。

`device_id`

`string`

是

终端用户的唯一标识，可使用应用内用户ID或客户端生成的设备标识，主要用于日志追踪和问题排查。

`apikey`

`string`

否

API Key。可以在初始化时传入；更推荐通过 [startDialog](#startdialog) 的 `dialog_params` 传入临时API Key。

`audio_update_manually`

`string`

否

是否启用主动推送音频数据模式，默认值为 `"false"`。设为 `"true"` 时通过 [updateAudio](#updateaudio) 主动推送音频数据；设为 `"false"` 时由SDK通过 [onNuiNeedAudioData](#onnuineedaudiodata) 拉取音频数据。设为 `"true"` 且SDK支持端侧AEC、VAD等音频能力时，默认开启相应端侧音频能力。

`workspace`

`string`

否

端侧资源文件的存储路径。`audio_update_manually` 为 `"true"` 且启用AEC或VAD等端侧音频能力时必须设置。

`debug_path`

`string`

否

日志文件目录。仅当 `save_log` 为 `true` 时生效，此时必须设置。SDK最多保留两个日志文件。

`save_wav`

`string`

否

是否保存调试音频，默认值为 `"false"`。音频文件保存在 `debug_path` 下。设为 `"true"` 时还需设置 `debug_path`，并在调用 `initialize` 时将 `save_log` 设为 `true`。

`save_wav_by_id`

`string`

否

是否在开启 `save_wav` 后使用 `task_id` 命名音频文件，以便检索，默认值为 `"false"`。

`max_log_file_size`

`number`

否

单个日志文件的最大字节数。默认值为 `104857600`（100 MiB），仅当 `save_log` 为 `true` 时生效。

`log_track_level`

`number`

否

通过 `onNuiLogTrackCallback` 返回日志的过滤级别，默认值为 `2`。取值：0（VERBOSE）、1（DEBUG）、2（INFO）、3（WARNING）、4（ERROR）、5（NONE）。日志级别必须同时大于或等于 `log_track_level` 和 `initialize` 的 `level`，才会通过回调返回。例如，前者为2、后者为3时，只返回WARNING及以上级别的日志。

`enable_reconnection`

`string`

否

是否开启断网续传，默认值为 `"false"`。

`aec_params`

`object`

否

端侧AEC配置。仅在 `audio_update_manually` 为 `"true"` 时使用。

`aec_params.enable_aec`

`boolean`

否

是否启用端侧AEC。SDK版本支持端侧AEC时默认开启。

`aec_params.save_audio`

`boolean`

否

是否保存AEC处理过程中的音频。开启 `save_wav` 并设置 `debug_path` 后默认开启。

`aec_params.enable_aec_data_callback`

`boolean`

否

是否通过 [onNuiAssistEventCallback](#onnuiassisteventcallback) 的 `EVENT_AEC_DATA` 事件返回AEC处理后的数据，默认值为 `false`。

`vad_params`

`object`

否

端侧VAD配置。仅在 `audio_update_manually` 为 `"true"` 时使用。

`vad_params.enable_vad`

`boolean`

否

是否启用端侧VAD。SDK版本支持端侧VAD时默认开启。

`vad_params.save_audio`

`boolean`

否

是否保存VAD处理过程中的音频。开启 `save_wav` 并设置 `debug_path` 后默认开启。

`audio_config`

`object`

否

SDK拉取音频时的采集配置，仅在 `audio_update_manually` 为 `"false"` 时使用。

`audio_config.mic.enable_volume_calculation`

`boolean`

否

是否计算并上报音量，默认值为 `true`。无需音量回调时可关闭。

`audio_config.mic.volume_mode`

`string`

否

音量计算模式。设为 `"dbfs"` 时，按 `20*log10(rms/32768)` 计算标准dBFS值，满量程为0 dB。

### 语音识别效果参数

通过 [setParams](#setparams) 的 `params` 参数传入JSON字符串。

**说明**`qwen-audio-3.1-asr-flash-message` 模型不支持 `nls_config.language_hints`、`nls_config.semantic_punctuation_enabled`、`nls_config.multi_threshold_mode_enabled`、`nls_config.special_word_filter` 参数。

```
{
  "service_type": 4,
  "nls_config": {
    "model": "qwen-audio-3.0-asr-flash-streaming",
    "sr_format": "opus",
    "sample_rate": 16000
  }
}
```

**参数**

**类型**

**是否必须**

**说明**

`service_type`

`number`

是

语音服务类型。实时语音识别固定为 `4`，即 `Constants.kServiceTypeSpeechTranscriber`。

`nls_config`

`object`

是

识别配置对象。

`nls_config.model`

`string`

是

指定示例调用的模型。模型信息请参见[支持的模型与地域](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide#4a43cc1bb7kxg)。

`nls_config.sr_format`

`string`

是

音频格式，取值为 `pcm` 或 `opus`。设为 `opus` 时，客户端仍传入PCM数据，由SDK编码为Opus。

`nls_config.sample_rate`

`number`

是

采样率（Hz）。8 kHz模型仅支持 `8000`，其他模型支持任意采样率。启用端侧AEC或VAD时不支持8000 Hz。

`nls_config.semantic_punctuation_enabled`

`boolean`

否

是否启用语义断句，默认值为 `false`。`true` 表示启用语义断句并关闭VAD断句，适合对断句准确性要求较高的会议转写场景；`false` 表示启用VAD断句并关闭语义断句，适合对延迟要求较高的交互场景。

`nls_config.max_sentence_silence`

`number`

否

VAD断句静音阈值（毫秒）。一段语音后的静音时长超过该阈值时，系统判定句子结束。默认值为 `1300`，取值范围为 `[200, 6000]`。启用语义断句时，该参数不作为 `sentence_end` 的返回依据，但设置过小仍可能影响识别效果。

`nls_config.multi_threshold_mode_enabled`

`boolean`

否

是否启用多阈值模式，默认值为 `false`。启用后可避免VAD断句切割过长。仅在 `semantic_punctuation_enabled` 为 `false` 时生效。

`nls_config.heartbeat`

`boolean`

否

是否启用心跳包，默认值为 `false`。启用后，在持续发送静音音频时可保持连接；未启用时，连接会在一定时间后因超时而断开。静音音频是音频文件或数据流中不包含声音信号的内容。

`nls_config.vocabulary_id`

`string`

否

预编译热词列表ID。需提前创建热词列表，适用于词汇已知且相对稳定、需要跨请求复用同一词表的场景，参见[预编译热词](https://help.aliyun.com/zh/model-studio/improve-asr-accuracy#hw_precompiled_h3)。

`nls_config.instant_vocabulary`

`object`

否

即时热词，键为热词文本，值为整数权重，无需提前创建热词列表，适用于临时性、会话级热词优化。权重取值为 `[1, 5]` 或 `50`；取 `[1, 5]` 时值越大，模型越倾向输出该词；权重为50的超级热词最多50个。与预编译热词同时配置时，两类热词会合并；超过2000个时随机选择2000个使用。参见[即时热词](https://help.aliyun.com/zh/model-studio/improve-asr-accuracy#hw_instant_h3)。

`nls_config.language_hints`

`string[]`

否

待识别音频的语种，无默认值；不设置时由模型自动识别。Qwen-Audio-3.x-ASR-Flash-Streaming系列最多使用前4个值；Fun-ASR-Realtime系列仅使用第1个值。支持的语言代码参见[实时语音识别用户指南](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide)。

`nls_config.speech_noise_threshold`

`number`

否

VAD语音与噪声判定阈值，取值范围为 `[-1.0, 1.0]`。值越接近-1，噪声越容易被判定为语音，可能转写更多噪声；值越接近1，语音越容易被判定为噪声，可能过滤部分语音。该参数可能显著影响识别效果，建议充分测试后以0.1为步长小幅调整。

`nls_config.special_word_filter`

`object`

否

敏感词过滤配置，参见[敏感词过滤](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide#rt03_sensitive_h3)。

`nls_config.enable_connection_fast_check`

`boolean`

否

是否启用快速网络检测，默认关闭。

## 关键接口

### NativeNui

导入SDK：

```
import { AsrResult, Constants, INativeNuiCallback, KwsResult, NativeNui } from 'neonui';
```

#### 创建实例

```
constructor(mode_type: Constants.ModeType, flag?: string)
```

**参数**

**类型**

**说明**

`mode_type`

`Constants.ModeType`

工作模式。取值为 `MODE_DIALOG`（对话或识别）、`MODE_TTS`（语音合成）和 `MODE_STREAM_INPUT_TTS`（流式文本语音合成）。实时语音识别固定为 `MODE_DIALOG`。

`flag`

`string`

可选的实例标记，用于区分实例日志。

#### initialize

```
initialize(
  callback: INativeNuiCallback,
  parameters: string,
  level: number,
  save_log: boolean = false
): number
```

初始化SDK。该接口可能阻塞，请勿在UI线程调用。

**参数**

**类型**

**说明**

`callback`

`INativeNuiCallback`

事件和数据回调接口。

`parameters`

`string`

[连接与控制参数](#%E8%BF%9E%E6%8E%A5%E4%B8%8E%E6%8E%A7%E5%88%B6%E5%8F%82%E6%95%B0)的JSON字符串。

`level`

`number`

SDK日志级别。取值为 `LOG_LEVEL_VERBOSE`（0）、`LOG_LEVEL_DEBUG`（1）、`LOG_LEVEL_INFO`（2）、`LOG_LEVEL_WARNING`（3）、`LOG_LEVEL_ERROR`（4）和 `LOG_LEVEL_NONE`（5）。

`save_log`

`boolean`

是否保存本地日志，默认值为 `false`。设为 `true` 时必须在 `parameters` 中设置 `debug_path`，并可通过 `max_log_file_size` 设置文件大小。

返回[错误码](https://help.aliyun.com/zh/isi/support/error-codes)。

#### setParams

```
setParams(params: string): number
```

在 `startDialog` 前设置[语音识别效果参数](#%E8%AF%AD%E9%9F%B3%E8%AF%86%E5%88%AB%E6%95%88%E6%9E%9C%E5%8F%82%E6%95%B0)。`params` 为语音识别效果参数的JSON字符串。返回[错误码](https://help.aliyun.com/zh/isi/support/error-codes)。

#### startDialog

```
startDialog(vad_mode: Constants.VadMode, dialog_params: string): number
```

开始识别。

**参数**

**类型**

**说明**

`vad_mode`

`Constants.VadMode`

VAD模式。实时语音识别固定为 `Constants.VadMode.TYPE_P2T`。

`dialog_params`

`string`

JSON字符串。可更新已过期的临时API Key，也可通过 `input_context` 传入上下文增强信息。

示例：

```
{
  "apikey": "st-****",
  "input_context": [
    { "role": "user", "content": [{ "type": "input_text", "text": "示例上下文" }] }
  ]
}
```

返回[错误码](https://help.aliyun.com/zh/isi/support/error-codes)。

#### stopDialog

```
stopDialog(): number
```

通知服务端结束识别并返回最终结果。收到 `EVENT_TRANSCRIBER_COMPLETE` 后，任务结束。返回[错误码](https://help.aliyun.com/zh/isi/support/error-codes)。

#### cancelDialog

```
cancelDialog(): number
```

立即结束识别，不等待服务端返回最终结果。返回[错误码](https://help.aliyun.com/zh/isi/support/error-codes)。

#### dialogAction

```
dialogAction(action_params: string): number
```

发送运行时动作，用于更新识别上下文、通知AEC播放状态等运行时行为。

**参数**

**类型**

**说明**

`action_params`

`string`

JSON字符串。

`action_params.type`

`string`

固定为 `"action"`。

`action_params.command`

`string`

动作指令。支持 `"context"`（更新上下文）、`"play_start"`（通知AEC开始播放参考音）和 `"play_over"`（通知AEC参考音播放结束）。

`action_params.context`

`object[]`

当 `command` 为 `"context"` 时传入的上下文增强内容。

更新上下文示例：

```
{
  "type": "action",
  "command": "context",
  "context": [
    {
      "role": "user",
      "content": [
        { "text": "示例上下文", "type": "input_text" }
      ]
    }
  ]
}
```

返回[错误码](https://help.aliyun.com/zh/isi/support/error-codes)。

#### updateAudio

```
updateAudio(data: ArrayBuffer, first_pack: boolean): number
```

`audio_update_manually` 为 `"true"` 时，通过该接口主动推送录音数据，不再通过 `onNuiNeedAudioData` 填充。

**参数**

**类型**

**说明**

`data`

`ArrayBuffer`

待识别的音频数据。

`first_pack`

`boolean`

是否为首个音频包。首包设为 `true`，后续设为 `false`。

返回[错误码](https://help.aliyun.com/zh/isi/support/error-codes)。

#### pushReferenceData

```
pushReferenceData(data: ArrayBuffer, first_pack: boolean): number
```

`audio_update_manually` 为 `"true"` 且启用端侧AEC时，通过该接口推送播放器播放的参考音频。

**参数**

**类型**

**说明**

`data`

`ArrayBuffer`

参考音频数据。

`first_pack`

`boolean`

是否为首个音频包。首包设为 `true`，后续设为 `false`。

返回[错误码](https://help.aliyun.com/zh/isi/support/error-codes)。

#### release

```
release(): number
```

释放SDK的全部内部资源。调用后实例不可用；如需再次使用，必须重新调用 `initialize`。返回[错误码](https://help.aliyun.com/zh/isi/support/error-codes)。

#### GetVersion

```
GetVersion(): string
```

返回当前SDK版本信息。

#### refreshApikey

```
refreshApikey(apikey: string, url: string = ''): string
```

刷新API Key并返回临时鉴权Token。该接口会进行同步网络调用，请勿在UI线程调用。

**参数**

**类型**

**说明**

`apikey`

`string`

已有的API Key。

`url`

`string`

可选的鉴权服务地址，默认为空；为空时使用默认地址。

### INativeNuiCallback

#### onNuiEventCallback

```
onNuiEventCallback: (
  event: Constants.NuiEvent,
  resultCode: number,
  arg2: number,
  kwsResult: KwsResult,
  asrResult: AsrResult
) => void;
```

接收识别事件和结果。

**参数**

**类型**

**说明**

`event`

`Constants.NuiEvent`

回调事件。

`resultCode`

`number`

[错误码](https://help.aliyun.com/zh/isi/support/error-codes)，在 `EVENT_ASR_ERROR` 事件中有效。

`arg2`

`number`

保留参数。

`kwsResult`

`KwsResult`

语音唤醒结果，实时语音识别场景无需关注。

`asrResult`

`AsrResult`

语音识别结果。`allResponse` 是服务端返回的完整JSON，可从 `header.task_id` 获取任务ID，从 `payload.output.sentence.text` 获取句子文本。

事件类型：

**事件**

**说明**

`EVENT_TRANSCRIBER_STARTED`

任务启动成功。`asrResult.allResponse` 的 `header.task_id` 包含任务ID，建议记录以便排查问题。

`EVENT_VAD_START`

任务启动后触发，不表示检测到人声起点。

`EVENT_VAD_END`

检测到人声终点。

`EVENT_SENTENCE_START`

检测到一句话开始。

`EVENT_ASR_PARTIAL_RESULT`

返回语音识别中间结果。

`EVENT_SENTENCE_END`

检测到一句话结束，并返回一句完整的识别结果。

`EVENT_ASR_WARN`

识别过程中出现不影响运行的警告，例如启用断网续传后的断网事件。

`EVENT_ASR_ERROR`

识别过程中出现错误，错误码通过 `resultCode` 返回。

`EVENT_MIC_ERROR`

连续2秒未收到任何音频数据。请检查录音代码、权限或录音模块是否被其他应用占用。

`EVENT_TRANSCRIBER_COMPLETE`

语音识别结束。

`EVENT_AEC_DATA`

AEC处理后的音频数据，通过 `onNuiAssistEventCallback` 返回。

#### onNuiAudioStateChanged

```
onNuiAudioStateChanged: (state: Constants.AudioState) => void;
```

SDK通过该回调通知应用何时启动或停止录音。

**状态**

**说明**

`STATE_OPEN`

交互启动，可以打开录音设备。

`STATE_PAUSE`

交互停止，可以停止录音。

`STATE_CLOSE`

SDK实例已释放，可以彻底关闭录音设备。

HarmonyOS的 `AudioCapturer` 采用异步方式创建，建议在初始化阶段提前创建录音器实例。收到 `STATE_CLOSE` 时只停止录音并保留实例，以便复用；在统一的 `release` 流程中释放，避免下次收到 `STATE_OPEN` 后重建录音器并立即调用 `start` 时未生效。

#### onNuiNeedAudioData

```
onNuiNeedAudioData: (buffer: ArrayBuffer) => number;
```

SDK拉取音频时连续触发。按 `buffer.byteLength` 填充音频数据，通常为20毫秒的单通道16 bit PCM，并返回实际写入的字节数。返回小于或等于0表示出错或当前无数据。

#### onNuiAudioRMSChanged

```
onNuiAudioRMSChanged: (val: number) => number;
```

返回当前音频音量，可用于更新界面。`audio_config.mic.volume_mode` 为 `"dbfs"` 时，`val` 的范围为 `[-160, 0]`。回调实现返回 `0` 即可。

#### onNuiAssistEventCallback

```
onNuiAssistEventCallback?: (
  event: Constants.NuiEvent,
  info: string,
  infoLen: number,
  data: ArrayBuffer
) => void;
```

可选的辅助事件回调，用于接收SDK内部的辅助事件和相关数据。不关注时可以不实现。

**参数**

**类型**

**说明**

`event`

`Constants.NuiEvent`

辅助事件。

`info`

`string`

附加信息，通常为JSON字符串。

`infoLen`

`number`

附加信息的长度。

`data`

`ArrayBuffer`

辅助数据，例如AEC处理后的音频数据。

#### onNuiLogTrackCallback

```
onNuiLogTrackCallback: (level: Constants.LogLevel, log: string) => void;
```

接收SDK追踪日志。实际返回级别由 `log_track_level` 和 `initialize` 的 `level` 共同决定。

### 结果对象

#### AsrResult

**属性**

**类型**

**说明**

`finish`

`boolean`

当前结果是否结束。

`resultCode`

`number`

结果状态码。

`asrResult`

`string`

识别结果文本；`EVENT_ASR_ERROR` 事件中为错误信息。

`allResponse`

`string`

服务端返回的完整JSON字符串，包含任务ID、句子文本等完整信息。

#### KwsResult

**属性**

**类型**

**说明**

`type`

`Constants.WuwType`

唤醒词类型，实时语音识别场景无需关注。

`kws`

`string`

唤醒词，实时语音识别场景无需关注。

### 常量与枚举

**名称**

**说明**

`Constants.ModeType`

SDK工作模式：`MODE_DIALOG`、`MODE_TTS` 和 `MODE_STREAM_INPUT_TTS`。

`Constants.VadMode`

VAD模式。实时语音识别固定使用 `TYPE_P2T`，由用户调用 `stopDialog` 结束识别。

`Constants.AudioState`

音频状态：`STATE_OPEN`、`STATE_PAUSE` 和 `STATE_CLOSE`。

`Constants.LogLevel`

日志级别：`LOG_LEVEL_VERBOSE`（0）到 `LOG_LEVEL_NONE`（5）。

`Constants.NuiResultCode`

SDK错误码，例如 `SUCCESS`（0）、`ILLEGAL_PARAM`（240002）、`NECESSARY_PARAM_LACK`（240004）和 `SDK_NOT_INIT`（240011）。

`Constants.kServiceTypeSpeechTranscriber`

实时语音识别的 `service_type`，固定为4。

`Constants.ModeFullCloud`

纯云端运行模式，`service_mode` 固定为 `"1"`。

## 示例代码

以下代码展示SDK调用的核心流程。录音队列、权限申请和结果JSON解析等完整实现，请参考整合包中的 `DashFunAsrSpeechTranscriberPage.ets`。

```
import { AsrResult, Constants, INativeNuiCallback, KwsResult, NativeNui } from 'neonui';

const callback: INativeNuiCallback = {
  onNuiEventCallback: (event: Constants.NuiEvent, resultCode: number, arg2: number,
    kwsResult: KwsResult, asrResult: AsrResult): void => {
    if (event == Constants.NuiEvent.EVENT_ASR_PARTIAL_RESULT
      || event == Constants.NuiEvent.EVENT_SENTENCE_END) {
      // 从asrResult.allResponse中解析payload.output.sentence.text。
    } else if (event == Constants.NuiEvent.EVENT_TRANSCRIBER_COMPLETE) {
      // 识别结束。
    } else if (event == Constants.NuiEvent.EVENT_ASR_ERROR) {
      // resultCode为错误码。
    }
  },
  onNuiAudioStateChanged: (state: Constants.AudioState): void => {
    // 根据STATE_OPEN、STATE_PAUSE和STATE_CLOSE控制AudioCapturer。
  },
  onNuiNeedAudioData: (buffer: ArrayBuffer): number => {
    // 从录音队列读取数据并填入buffer，返回实际字节数。
    return 0;
  },
  onNuiAudioRMSChanged: (val: number): number => 0,
  onNuiLogTrackCallback: (level: Constants.LogLevel, log: string): void => {}
};

const nuiInstance = new NativeNui(Constants.ModeType.MODE_DIALOG);

const initParams: Record<string, Object> = {};
initParams['url'] = 'wss://dashscope.aliyuncs.com/api-ws/v1/inference';
initParams['device_id'] = 'my_device_id';
initParams['service_mode'] = Constants.ModeFullCloud;
initParams['audio_update_manually'] = 'false';

const initResult = nuiInstance.initialize(
  callback,
  JSON.stringify(initParams),
  Constants.LogLevel.LOG_LEVEL_DEBUG,
  false
);

if (initResult == Constants.NuiResultCode.SUCCESS) {
  const nlsConfig: Record<string, Object> = {
    'model': 'qwen-audio-3.0-asr-flash-streaming',
    'sr_format': 'opus',
    'sample_rate': 16000
  };
  const params: Record<string, Object> = {
    'service_type': Constants.kServiceTypeSpeechTranscriber,
    'nls_config': nlsConfig
  };
  nuiInstance.setParams(JSON.stringify(params));

  const dialogParams: Record<string, Object> = { 'apikey': 'st-****' };
  nuiInstance.startDialog(Constants.VadMode.TYPE_P2T, JSON.stringify(dialogParams));
}

// 用户结束录音时停止识别，并等待EVENT_TRANSCRIBER_COMPLETE。
function stopRecognition(): void {
  nuiInstance.stopDialog();
}
// 在EVENT_TRANSCRIBER_COMPLETE的处理逻辑中调用nuiInstance.release()。
```

录音设备可使用 `@kit.AudioKit` 的 `AudioCapturer`。音频应为单通道、16 bit PCM，并使用与模型匹配的采样率。

```
import { audio } from '@kit.AudioKit';

const options: audio.AudioCapturerOptions = {
  streamInfo: {
    samplingRate: audio.AudioSamplingRate.SAMPLE_RATE_16000,
    channels: audio.AudioChannel.CHANNEL_1,
    sampleFormat: audio.AudioSampleFormat.SAMPLE_FORMAT_S16LE,
    encodingType: audio.AudioEncodingType.ENCODING_TYPE_RAW
  },
  capturerInfo: {
    source: audio.SourceType.SOURCE_TYPE_MIC,
    capturerFlags: 0
  }
};

const capturer = await audio.createAudioCapturer(options);
capturer.on('readData', (buffer: ArrayBuffer): void => {
  // 回调模式：将数据写入队列，供onNuiNeedAudioData读取。
  // 主动模式：调用nuiInstance.updateAudio(buffer, firstPack)。
});
await capturer.start();
```
