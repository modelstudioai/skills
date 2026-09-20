# Qwen-Audio-3.0-Realtime实时语音对话Android SDK

使用Qwen-Audio-3.0-Realtime实时语音对话Android SDK，实现实时音频输入以及语音或文本输出。

**用户指南：**关于模型介绍和选型建议请参见[实时语音对话](https://help.aliyun.com/zh/model-studio/qwen-audio-realtime-user-guides)。

## 快速开始

1.  [获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)
2.  **下载 SDK 并运行示例代码：**
    -   [下载最新 SDK 整合包](https://help.aliyun.com/zh/isi/sdk-selection-and-download)。
    -   解压 ZIP 包。在 `app/libs` 目录中获取 AAR 格式 SDK，并添加到项目依赖。需要 Android C++ 接入时，使用 ZIP 包内的 `android_libs` 与 `android_include` 获取动态库和头文件。
    -   用 Android Studio 打开工程。示例代码位于`DashQwenAudioChatActivity.java`，替换 API Key 后体验功能。

### 调用步骤

1.  初始化 SDK
2.  按业务需求设置参数：通过[initialize](https://help.aliyun.com/zh/model-studio/android-sdk-for-qwen-audio-realtime-service#initialize)接口的`parameters`参数设置[连接与控制参数](https://help.aliyun.com/zh/model-studio/android-sdk-for-qwen-audio-realtime-service#connection-and-control-parameters)；通过[setParams](https://help.aliyun.com/zh/model-studio/android-sdk-for-qwen-audio-realtime-service#set-params)接口设置[语音对话效果参数](https://help.aliyun.com/zh/model-studio/android-sdk-for-qwen-audio-realtime-service#conversation-parameters)。
3.  调用[startDialog](https://help.aliyun.com/zh/model-studio/android-sdk-for-qwen-audio-realtime-service#start-dialog)启动对话流程。
4.  在[onNuiAudioStateChanged](https://help.aliyun.com/zh/model-studio/android-sdk-for-qwen-audio-realtime-service#on-nui-audio-state-changed)回调中，根据音频状态开启录音设备。
5.  在[onNuiNeedAudioData](https://help.aliyun.com/zh/model-studio/android-sdk-for-qwen-audio-realtime-service#on-nui-need-audio-data)回调中持续提供录音数据，或者通过[updateAudio](https://help.aliyun.com/zh/model-studio/android-sdk-for-qwen-audio-realtime-service#update-audio)持续推送录音数据。
6.  在[onNuiAssistEventCallback](https://help.aliyun.com/zh/model-studio/android-sdk-for-qwen-audio-realtime-service#on-nui-assist-event-callback)回调中持续获得 AI 返回的语音数据。
7.  在[onNuiEventCallback](https://help.aliyun.com/zh/model-studio/android-sdk-for-qwen-audio-realtime-service#on-nui-event-callback)回调中监听事件并获取事件信息。
8.  调用[stopDialog](https://help.aliyun.com/zh/model-studio/android-sdk-for-qwen-audio-realtime-service#stop-dialog)停止对话，并通过监听EVENT\_TRANSCRIBER\_COMPLETE事件确认对话已结束。
9.  当对话功能不再使用时，调用[release](https://help.aliyun.com/zh/model-studio/android-sdk-for-qwen-audio-realtime-service#release)接口释放 SDK 资源。

## 请求参数

### 连接与控制参数

通过在[initialize](https://help.aliyun.com/zh/model-studio/android-sdk-for-qwen-audio-realtime-service#initialize)接口的`parameters`参数中传入一个 JSON 字符串来配置。

**参数示例：**以下为 JSON 字符串示例，参数未完整列出。请按实际需求在编码时补充：

```
{
    "url": "wss://dashscope.aliyuncs.com/api-ws/v1/inference",
    "apikey": "st-****",
    "device_id": "my_device_id",
    "service_mode": "1"
}
```
**参数说明**

**参数**

**类型**

**是否必须**

**说明**

`url`

`String`

是

服务地址：

-   `wss://dashscope.aliyuncs.com/api-ws/v1/realtime?model=<model_name>`
-   华北2（北京）：`wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime?model=<model_name>`
-   新加坡：`wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime?model=<model_name>`

调用时，请将 `{WorkspaceId}` 替换为真实的 [Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)。

`apikey`

`String`

是

API Key。

`service_mode`

`String`

是

运行模式。实时语音对话固定为 `"1"`。

`device_id`

`String`

是

用于标识终端用户的唯一字符串，可设为应用内用户 ID或客户端生成的设备唯一标识符。此 ID主要用于日志追踪和问题排查。

audio\_update\_manually

`String`

否

是否启用主动推送音频数据模式，默认值："false"。  
当设置为"true"启用主动推送音频数据模式时，且SDK版本支持端侧音频能力（如AEC、VAD），则默认开启端侧音频能力。

workspace

`String`

否

当参数audio\_update\_manually设置为"true"时，且启用端侧音频能力（如AEC、VAD）时，必须设置workspace，即端侧资源文件存储的路径。

`debug_path`

`String`

否

日志文件的存储路径。 此参数仅在调用[initialize](https://help.aliyun.com/zh/model-studio/android-sdk-for-qwen-audio-realtime-service#initialize)接口时将`save_log`设为true时生效。此时必须设置日志文件路径，否则将报错。 本地最多保留两个日志文件。

`save_wav`

`String`

否

是否保存调试用的音频文件。音频文件保存于`debug_path`下。  
默认值："false"。  
取值范围：

-   "true"：是
-   "false"：否

此参数仅在调用[initialize](https://help.aliyun.com/zh/model-studio/android-sdk-for-qwen-audio-realtime-service#initialize)接口时将`save_log`设为true时生效。 同时，`debug_path`也必须被设置。

`max_log_file_size`

`int`

否

设定日志文件的最大字节数。  
此参数仅在调用[initialize](https://help.aliyun.com/zh/model-studio/android-sdk-for-qwen-audio-realtime-service#initialize)接口时将`save_log`设为true时生效。  
默认值：104857600（100 \* 1024 \* 1024 字节, 即 100MiB）。

`log_track_level`

`int`

否

控制通过日志回调（`onNuiLogTrackCallback`）对外发送的日志内容的过滤级别。  
默认值：2。  
取值范围：

-   0：LOG\_LEVEL\_VERBOSE
-   1：LOG\_LEVEL\_DEBUG
-   2：LOG\_LEVEL\_INFO
-   3：LOG\_LEVEL\_WARNING
-   4：LOG\_LEVEL\_ERROR
-   5：LOG\_LEVEL\_NONE（表示关闭此功能）

注意：`log_track_level`与`level`（通过[initialize](https://help.aliyun.com/zh/model-studio/android-sdk-for-qwen-audio-realtime-service#initialize)接口设置）共同决定最终回调的日志。一条日志的级别数值必须同时大于或等于`log_track_level`和`level`的值，才会被回调。例如，`log_track_level`设为2 (INFO)，`level`设为3 (WARNING)，则只有WARNING及以上级别（数值>=3）的日志才会被回调。

aec\_params

`object`

否

端侧AEC能力高级参数配置对象。当参数audio\_update\_manually设置为"true"时才启用此配置对象。

aec\_params.enable\_aec

`boolean`

否

是否开启端侧AEC回声消除能力。  
当参数audio\_update\_manually设置为"true"时，且SDK版本支持端侧AEC音频能力，则默认开启。

aec\_params.save\_audio

`boolean`

否

是否开启端侧AEC回声消除模块音频存储功能。 当`save_wav`为"true"，且设置了`debug_path`，则默认开启，将AEC运行音频数据存储到`debug_path`下。

aec\_params.enable\_aec\_data\_callback

`boolean`

否

是否将AEC后的数据送给用户，默认false；开启后在onNuiAssistEventCallback的EVENT\_AEC\_DATA接收。

vad\_params

`object`

否

端侧VAD能力高级参数配置对象。  
当参数audio\_update\_manually设置为"true"时才启用此配置对象。

vad\_params.enable\_vad

`boolean`

否

是否开启端侧VAD人声检测能力。  
当参数audio\_update\_manually设置为"true"时，且SDK版本支持端侧VAD音频能力，则默认开启。

vad\_params.save\_audio

`boolean`

否

是否开启端侧VAD人声检测模块音频存储功能。  
当`save_wav`为"true"，且设置了`debug_path`，则默认开启，将VAD运行音频数据存储到`debug_path`下。

### 语音对话效果参数

通过在[setParams](https://help.aliyun.com/zh/model-studio/android-sdk-for-qwen-audio-realtime-service#set-params)接口的`params`参数中传入一个 JSON 字符串来配置。

**参数示例：**以下为 JSON 字符串示例，参数未完整列出。请按实际需求在编码时补充：

```
{
    "service_type": 4,
    "nls_config": {
        "model": "qwen-audio-3.1-realtime-plus",
        "sr_format": "pcm"
    }
}
```
**参数说明**

**一级参数**

**类型**

**是否必须**

**说明**

`service_type`

`int`

是

语音服务类型。实时语音对话固定为 `4`。

`nls_config`

`object`

是

语音对话核心配置对象，包含模型选择、对话效果控制等关键参数。

`nls_config.model`

`string`

是

指定模型名。支持qwen-audio-3.1-realtime-plus、qwen-audio-3.0-realtime-plus和qwen-audio-3.0-realtime-flash系列模型。

`nls_config.sr_format`

`string`

是

输入音频格式。当前仅支持 `pcm`（16kHz 16bit 单声道），为默认值。

`nls_config.modalities`

`string`

否

array 格式的字符串，模型输出模态设置，可选值：

-   `["text"]`：仅输出文本。
-   `["audio", "text"]`（默认值）：同时输出文本和音频。

nls\_config.voice

`string`

否

TTS 音色名称，3.1 Plus 的默认值为 `longanqian_v3.1`，3.0 Plus/Flash 的默认值为 `longanqian`。支持两种类型，仅可在第一次 `session.update` 中设置，后续传入将被忽略。

-   **系统音色**：可选值：`longanqian`、`longanlingxin`、`longanlingxi`、`longanxiaoxin`、`longanlufeng`。
-   **声音复刻音色**：通过声音复刻 API 创建，将返回的 `voice_id` 填入此参数。详见[音色配置](https://help.aliyun.com/zh/model-studio/qwen-audio-realtime-user-guides#fc60h311)。

3.1 Plus 还支持 `longanqian_v3.1`、`longanhuan_v3.1`、`longanlingxin_v3.1`、`longanfengyue_v3.1`、`xunanchuan`、`beth_v3.1`、`betty_v3.1`、`cally_v3.1`。

nls\_config.enable\_speech\_emotion

`boolean`

否

是否开启情绪增强功能。开启后，回复音色的情绪变化更明显。默认值：`true`。可选值：`true`、`false`。

nls\_config.instructions

`string`

否

系统指令，用于设定模型的角色身份、回答风格和行为偏好。对整个会话生效。

nls\_config.max\_history\_turns

`int`

否

允许单次请求的最大历史 QA 轮数。取值范围为 1-50，默认值为 20。

nls\_config.tools

`string`

否

array 格式的字符串。Function Calling 工具定义列表。配置后模型可根据用户输入自主决定是否调用工具。  
内部参数说明：  
**type**`string`**（必选）**  
固定为 `function`。  
**function.name**`string`**（必选）**  
工具函数名称。  
**function.description**`string`（可选）  
对工具函数功能的描述，模型据此判断是否调用该工具。  
**function.parameters**`object`（可选）  
对工具函数入参的描述，模型据此提取所需入参。若函数无需入参，可不指定。  
示例：

```
[
  {
    "type": "function",
    "function": {
      "name": "get_weather",
      "description": "查询指定城市的天气信息。",
      "parameters": {
        "type": "object",
        "properties": {
          "city": {
            "type": "string",
            "description": "城市"
          }
        },
        "required": [
          "city"
        ]
      }
    }
  }
]
```

nls\_config.turn\_detection

`string`

否

JSON 对象形式的字符串。轮次检测配置。不设置时则切换为 push-to-talk 模式（手动提交音频并触发推理）。否则启用双工对话模式。

nls\_config.turn\_detection.type

`string`

否

VAD 类型，可选值：

-   `server_vad`（默认值）：基于声学特征检测语音起止，自动触发推理。
-   `smart_turn`：融合声学感知与语义理解的智能轮次检测，通过声学与语义双重判断轮次边界。无语义的声音（如”嗯”、”啊”）不会触发对话轮或打断模型播报。

nls\_config.turn\_detection.threshold

float

否

VAD灵敏度，**仅在 server\_vad 模式下生效（smart\_turn 模式下无效）**。值越低，VAD越灵敏，越容易将微弱声音（包括背景噪音）识别为语音；值越高，越不灵敏，需要更清晰、音量更大的语音才能触发。  
取值范围为\[-1.0, 1.0\]，默认值为 0.5。

nls\_config.turn\_detection.silence\_duration\_ms

`int`

否

语音结束后需保持静音的最短时间（毫秒），**仅在 server\_vad 模式下生效（smart\_turn 模式下无效）**。超时即触发模型响应。值越低，响应越快，但可能在短暂停顿时误触发。  
取值范围为\[200, 6000\]，默认值为 800。对话场景推荐 400-800。

nls\_config.turn\_detection.voiceprint\_audio\_urls

`string`

否

array形式的字符串。**仅在 smart\_turn 模式下生效。**目标用户预录音频的公网可访问 URL 列表，用于说话人增强。传入后，模型将在双工对话中精准锁定目标说话人，有效忽略旁人声音与背景噪声。最多支持 5 个 URL。音频格式要求：16kHz PCM 或 WAV。

## 关键接口

### NativeNui

#### initialize

初始化语音对话SDK 实例。SDK 为单例模式，在调用[release](https://help.aliyun.com/zh/model-studio/android-sdk-for-qwen-audio-realtime-service#release)前禁止重复初始化。

此接口会引起阻塞，应在非UI 线程调用。

**方法签名**
```
public synchronized int initialize(final INativeNuiCallback callback,
                                   String parameters,
                                   final Constants.LogLevel level,
                                   final boolean save_log)
```
**参数说明**

**参数**

**类型**

**说明**

`callback`

`INativeNuiCallback`

事件和数据回调接口的实现。

`parameters`

`String`

JSON 字符串，包含鉴权、连接和调试参数。参见[连接与控制参数](https://help.aliyun.com/zh/model-studio/android-sdk-for-qwen-audio-realtime-service#connection-and-control-parameters)。

`level`

`Constants.LogLevel`

控制SDK自身日志的打印级别。

`save_log`

`boolean`

是否保存本地日志。若为`true`，须在[连接与控制参数](https://help.aliyun.com/zh/model-studio/android-sdk-for-qwen-audio-realtime-service#connection-and-control-parameters)中通过`debug_path`指定路径，并可通过`max_log_file_size`设置文件大小。

**返回值说明**

返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。

#### setParams

以 JSON 格式设置[语音对话效果参数](https://help.aliyun.com/zh/model-studio/android-sdk-for-qwen-audio-realtime-service#conversation-parameters)。在[startDialog](https://help.aliyun.com/zh/model-studio/android-sdk-for-qwen-audio-realtime-service#start-dialog)之前调用。

**方法签名**
```
public synchronized int setParams(String params)
```
**参数说明**

**参数**

**类型**

**说明**

`params`

`String`

[语音对话效果参数](https://help.aliyun.com/zh/model-studio/android-sdk-for-qwen-audio-realtime-service#conversation-parameters)。

**返回值说明**

返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。

#### startDialog

开始对话。

**方法签名**
```
public synchronized int startDialog(VadMode vad_mode, String dialog_params)
```
**参数说明**

**参数**

**类型**

**说明**

`vad_mode`

`VadMode`

VAD模式。固定为`VadMode.TYPE_P2T`。

`dialog_params`

`String`

如果[连接与控制参数](https://help.aliyun.com/zh/model-studio/android-sdk-for-qwen-audio-realtime-service#connection-and-control-parameters)的`apikey`参数使用的是[临时API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)，当其过期时，可在此处进行更新。  
内容为JSON 格式：

```
{
  "apikey": "st-****"
}
```

**返回值说明**

返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。

#### stopDialog

结束对话，调用该接口后，服务端将返回最终对话结果并结束任务。

**方法签名**
```
public synchronized int stopDialog();
```
**返回值说明**

返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。

#### cancelDialog

立即结束对话，调用该接口后，不等待服务端返回最终对话结果就立即结束任务。

**方法签名**
```
public synchronized int cancelDialog();
```
**返回值说明**

返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。

#### updateAction

在交互过程中下发对话动作指令，用于更新对话上下文等运行时行为。

**方法签名**
```
public synchronized int updateAction(String params);
```
**参数说明**

**参数**

**类型**

**说明**

`params`

`String`

JSON 形式的字符串，用于更新对话上下文等运行时行为。

`params.type`

`String`

固定"action"。

`params.command`

`String`

具体的运行指令，当前支持 `function_call`、`play_start`、`play_over`。

-   `function_call`：更新函数调用请求的指令。
-   `play_start`：当使用端侧AEC时，通过此指令通知SDK内部AEC播放器开始播放音频。
-   `play_over`：当使用端侧AEC时，通过此指令通知SDK内部AEC播放器已经播放结束。

`params.context`

`String`

当`command`为`"function_call"`时，更新函数调用请求。

`params.context.type`

`String`

事件类型，当`command`为`"function_call"`时必须设置。

-   `conversation.item.create`：手动向对话上下文插入一条对话项。可用于注入历史上下文、补充文本信息，或写回 Function Calling 的工具执行结果。
-   `response.create`：在`conversation.item.create`指令发送后，通过此指令触发二轮推理。

`params.context.item`

`object`

`params.context.type`为conversation.item.create时必须设置，表示要创建的对话项。详见如下。

`params.context.response`

`object`

`params.context.type`为response.create时可设置，表示用于覆盖本轮推理的会话默认配置。不传时使用当前会话配置。详见如下。

`context.item`参数：

**参数**

**类型**

**说明**

id

`String`

可选。对话项的唯一标识符。不传时由服务端自动生成。若指定的 ID 已存在于对话中，会返回错误。

type

`String`

必选。对话项类型，可选值：

-   `message`：普通对话消息。
-   `function_call`：函数调用请求。通常由服务端生成，客户端也可用于补充历史上下文。
-   `function_call_output`：工具执行结果。客户端收到 `function_call` 后执行工具，并用该类型写回结果。

role

`String`

`message` 类型必选。消息角色，可选值：`system`、`user`、`assistant`。

content

array

`message` 类型必选。消息内容列表。每个元素包含 `type` 和对应的数据字段。  
**各 role 支持的 content 类型**：  
**system**  
`input_text`：系统消息，必填字段 `text`。  
**user**

-   `input_text`：用户文本输入，必填字段 `text`。
-   `input_audio`：用户音频输入，必填字段 `audio`（Base64 编码）。

**assistant**  
`output_text`：助手文本输出，必填字段 `text`。

call\_id

`String`

（`function_call` / `function_call_output` 类型必选）  
函数调用的唯一标识符，用于关联请求和结果。

name

`String`

（`function_call` 类型必选）  
要调用的函数名称。

arguments

`String`

`function_call` 类型必选）  
函数调用参数，JSON 字符串格式。

output

`String`

（`function_call_output` 类型必选）  
工具执行结果，JSON 字符串格式。

`context.response`参数：

**参数**

**类型**

**说明**

modalities

`array`

array 格式的字符串，模型输出模态设置，可选值：

-   `["text"]`：仅输出文本。
-   `["audio", "text"]`（默认值）：同时输出文本和音频。

voice

string

覆盖本轮的 TTS 音色。

示例：

```
{
  "type": "action",
  "command": "function_call",
  "context": {
    "item": {
      "call_id": "call_xxxx",
      "output": "{\"city\":\"杭州\",\"condition\":\"晴\",\"temperature\":18}",
      "type": "function_call_output"
    },
    "type": "conversation.item.create"
  }
}

{
  "type": "action",
  "command": "function_call",
  "context": {
    "response": {
      "modalities": [
        "text",
        "audio"
      ]
    },
    "type": "response.create"
  }
}
```
**返回值说明**

返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。

#### updateAudio

参数audio\_update\_manually设置为"true"时，录音数据不再是通过onNuiNeedAudioData填入，而是用此接口主动推送。

**方法签名**
```
public synchronized int updateAudio(byte[ ] data, int len,
                                    boolean first_pack);
```
**参数说明**

**参数**

**类型**

**说明**

`data`

`byte[]`

推送的音频数据。

`len`

`int`

推送的音频数据的字节数。

`first_pack`

`boolean`

请忽略，无需关注此参数。

**返回值说明**

返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。

#### updateRefAudio

参数audio\_update\_manually设置为"true"时，且启用了端侧AEC回声消除能力，则需要用此接口推送播放器播放的音频数据作为参考信号。

**方法签名**
```
public synchronized int updateRefAudio(byte[ ] data, int len,

                                       boolean first_pack);
```
**参数说明**

**参数**

**类型**

**说明**

`data`

`byte[]`

推送的音频数据。

`len`

`int`

推送的音频数据的字节数。

`first_pack`

`boolean`

请忽略，无需关注此参数。

**返回值说明**

返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。

#### release

释放SDK所有内部资源。此方法调用后，SDK 实例将变为不可用状态，如需再次使用，必须重新调用[initialize](https://help.aliyun.com/zh/model-studio/android-sdk-for-qwen-audio-realtime-service#initialize)进行初始化。

**方法签名**
```
public synchronized int release();
```
**返回值说明**

返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。

#### GetVersion

获得当前SDK版本信息。

**方法签名**
```
public synchronized String GetVersion();
```
**返回值说明**

当前SDK版本信息。

### INativeNuiCallback：监听回调

#### onNuiEventCallback：监听事件信息

**方法签名**
```
void onNuiEventCallback(NuiEvent event, final int resultCode, final int arg2, KwsResult kwsResult, AsrResult asrResult);
```
**参数说明**

**参数**

**类型**

**说明**

`event`

`NuiEvent`

回调事件。

`resultCode`

`int`

[错误码](https://help.aliyun.com/zh/isi/support/error-codes)，在出现EVENT\_ASR\_ERROR事件时有效。

`arg2`

`int`

保留参数。

`asrResult`

`AsrResult`

语音识别结果。

`kwsResult`

`KwsResult`

语音唤醒功能。无需关注该参数。

#### onNuiAudioStateChanged：监听音频状态

SDK 通过此回调通知何时应该开始或停止录音。

**方法签名**
```
void onNuiAudioStateChanged(AudioState state);
```
**AudioState状态说明**

**状态**

**说明**

`STATE_OPEN`

交互启动，可以打开录音设备进行录音。

`STATE_PAUSE`

交互停止，可以停止录音。

`STATE_CLOSE`

SDK 实例已释放，可以彻底关闭录音设备。

#### onNuiNeedAudioData：填充待处理音频数据

开始对话后，该回调被连续触发，需在其中提供待处理的音频数据。参数audio\_update\_manually设置为"true"时可不关注这个回调。

**方法签名**
```
int onNuiNeedAudioData(byte[ ] buffer, int len);
```
**参数说明**

**参数**

**类型**

**说明**

`buffer`

`byte[]`

填充的音频数据。

`len`

`int`

填充的音频数据的字节数。

**返回值说明**

实际填充的字节数。

#### onNuiAssistEventCallback：辅助数据和信息结果

此回调用于接收 SDK 内部的辅助事件和相关数据。

**方法签名**
```
void onNuiAssistEventCallback_(int event, byte[ ] info, int info_len,
                               byte[ ] data);
```
**参数说明**

**参数**

**类型**

**说明**

`event`

`int`

`NuiEvent`事件

`info`

`String`

无需关注该参数。

`info_len`

`int`

无需关注该参数。

`data`

`byte[]`

辅助数据，比如AI返回的TTS音频。

#### onNuiLogTrackCallback：监听追踪日志

此回调用于接收 SDK 内部的详细日志，方便进行问题定位和调试。

```
default void onNuiLogTrackCallback(Constants.LogLevel level, String log)
```

### NuiEvent：事件类型

**事件**

**说明**

EVENT\_TRANSCRIBER\_STARTED

任务启动成功。

EVENT\_VAD\_START

任务启动后即触发该事件。不代表检测到人声起点。

EVENT\_VAD\_END

检测到人声终点。

EVENT\_ASR\_PARTIAL\_RESULT

语音识别中间结果。

EVENT\_ASR\_ERROR

语音对话过程中出现错误。

EVENT\_MIC\_ERROR

因连续2秒未收到任何音频数据而触发。

EVENT\_SENTENCE\_END

检测到一句话结束，此时会返回一句完整的识别结果。

EVENT\_TRANSCRIBER\_COMPLETE

语音对话结束。

EVENT\_AUDIO\_TRANSCRIPTION

音频模式下的文字字幕增量事件，流式返回字幕片段。

EVENT\_AUDIO\_TRANSCRIPTION\_COMPLETED

音频模式下的字幕输出完成事件。

EVENT\_OTHER\_RESULT

其他未归类事件信息，比如function\_call的返回结果等。

EVENT\_ASR\_TTS\_START

AI开始返回TTS数据。

EVENT\_ASR\_TTS\_DATA

AI返回的TTS数据。

EVENT\_ASR\_TTS\_COMPLETE

AI返回TTS数据结束。

EVENT\_AEC\_DATA

AEC回声消除后的音频数据。
