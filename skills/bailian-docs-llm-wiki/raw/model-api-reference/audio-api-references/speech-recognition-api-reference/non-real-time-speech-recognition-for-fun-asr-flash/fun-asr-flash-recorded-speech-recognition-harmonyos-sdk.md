# 非实时语音识别（Qwen-Audio-3.x-ASR-Flash/Fun-ASR-Flash）HarmonyOS SDK

Qwen-Audio-3.x-ASR-Flash/Fun-ASR-Flash非实时语音识别HarmonyOS SDK可将语音转换为文本。

**用户指南：**[非实时语音识别](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide)。关于支持的音频格式、文件大小限制、时长限制等输入要求，请参见[音频规格](https://help.aliyun.com/zh/model-studio/asr-model#asr_audio_spec02)。

## 快速开始

1.  **获取API Key：**[获取API Key](raw/model-api-reference/preparations/get-api-key.md)，为安全起见，推荐将API Key配置到环境变量。
2.  **下载SDK并运行示例代码：**
    -   [下载最新SDK整合包](https://help.aliyun.com/zh/isi/sdk-selection-and-download)。
    -   解压 TAR 包。在 `neonui` 目录中获取 HAR 格式 SDK，并添加到项目依赖。需要 C++ 接入时，使用 TAR 包内的 `native/libs` 与 `native/include` 获取动态库和头文件。
    -   用 DevEco Studio 打开工程。示例代码位于 `DashFunAsrFlashFileTranscriberPage.ets`，替换 API Key 后体验功能。

### 调用步骤

#### 同步模式

1.  初始化 SDK
    
2.  按业务需求配置相关参数
    
3.  调用 `startFileTranscriber` 发送非实时语音识别请求，并等待结果返回。
    
4.  在`onFileTransEventCallback`接口中监听`EVENT_FILE_TRANS_RESULT` 事件，获取最终识别结果。
    
5.  调用 `release` 释放 SDK 资源
    

## 请求参数

### 连接与控制参数

通过在[initializeFileTrans](#initializefiletrans)接口的`parameters`参数中传入一个JSON字符串来配置。

**参数示例：**以下为 JSON 字符串示例，参数未完整列出。请按实际需求在编码时补充：

```
{
    "url": "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation",
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

`string`

是

服务地址，固定为 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`。调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

`apikey`

`string`

是

API Key。建议使用时效性短、安全性更高的[临时API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)，以降低长期有效Key泄露的风险。

`service_mode`

`string`

是

运行模式。非实时语音识别固定为 `"1"`。

`device_id`

`string`

是

用于标识终端用户的唯一字符串，可设为应用内用户ID或客户端生成的设备唯一标识符。此ID主要用于日志追踪和问题排查。

`debug_path`

`string`

否

日志文件的存储路径。 此参数仅在调用[initializeFileTrans](#initializefiletrans)接口时将`save_log`设为true时生效。此时必须设置日志文件路径，否则将报错。 本地最多保留两个日志文件。

`max_log_file_size`

`number`

否

设定日志文件的最大字节数。 此参数仅在调用[initializeFileTrans](#initializefiletrans)接口时将`save_log`设为true时生效。 默认值：104857600（100 \* 1024 \* 1024 字节, 即 100MiB）。

### 语音识别效果参数

通过[setParams](#setparams)接口配置`nls_config`参数，或者通过[startFileTranscriber](#startfiletranscriber)接口配置所有语音识别效果参数。

**参数示例：**以下为 JSON 字符串示例，参数未完整列出。请按实际需求在编码时补充：

```
{
  "apikey": "st-****",
  "messages": [
    {
      "content": [
        {
          "input_audio": {
            "data": "{YOUR_AUDIO_URL}"
          },
          "type": "input_audio"
        }
      ],
      "role": "user"
    }
  ],
  "nls_config": {
    "format": "mp3",
    "model": "qwen-audio-3.0-asr-flash"
  }
}
```
**参数说明**

**参数**

**类型**

**是否必须**

**说明**

`apikey`

`string`

否

如果[连接与控制参数](#connection-parameters)的`apikey`使用的是[临时API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)，可在此处进行更新，以免超时失效。

`nls_config`

`object`

是

语音识别核心配置对象，包含模型选择、识别效果控制等关键参数。

`nls_config.model`

`string`

是

指定示例调用的模型。模型信息请参见[支持的模型与地域](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide#4a43cc1bb7kxg)。

`nls_config.format`

`string`

是

音频格式。根据实际音频格式填写，支持`wav`、`mp3`、`opus`等。详情请参见[音频规格](https://help.aliyun.com/zh/model-studio/asr-model#asr_audio_spec02)。

`nls_config.sample_rate`

`string`

否

音频采样率，单位Hz。例如`16000`表示16kHz采样率。详情请参见[音频规格](https://help.aliyun.com/zh/model-studio/asr-model#asr_audio_spec02)。

`nls_config.vocabulary_id`

`string`

否

预编译热词列表 ID。 需预先调用创建热词列表接口生成，识别时传入该 ID 即可使用列表中的热词。 适用于词汇已知且相对稳定、需要跨请求复用同一词表的场景。 使用方法请参见[预编译热词](https://help.aliyun.com/zh/model-studio/improve-asr-accuracy#hw_precompiled_h3)。

`nls_config.instant_vocabulary`

`object`

否

即时热词。  
以键值对形式传入，键为热词文本（`string`），值为热词权重（`integer`），无需预先创建热词列表。权重取值范围为 \[1, 5\] 或 50：取 \[1, 5\] 时值越大模型越倾向输出该词；取 50 时为超级热词，召回率大幅提升，但超级热词数量最多不超过 50 个。  
适用于临时性、会话级别的热词优化。  
与预编译热词同时配置时，系统会合并两类热词；合并后超过 2000 个时，随机选择 2000 个使用。使用方法请参见[即时热词](https://help.aliyun.com/zh/model-studio/improve-asr-accuracy#hw_instant_h3)。  

**重要**即时热词的适用模型及限制请参见[即时热词](https://help.aliyun.com/zh/model-studio/improve-asr-accuracy#hw_instant_h3)。

  
```
{
 "张三": 5,
 "李四": 5
}
```

`nls_config.language_hints`

`array[string]`

否

设置待识别语言代码。如果无法提前确定语种，可不设置，模型会自动识别语种。  
对于 Qwen-Audio-3.x-ASR-Flash 系列模型，最多支持设置 4 个值，即便设置超出 4 个，也仅前 4 个生效；对于 Fun-ASR-Flash 系列模型，仅支持设置 1 个值，即便设置多个，也仅第一个生效。

-   Qwen-Audio-3.x-ASR-Flash、fun-asr-flash-2026-06-15：
-   zh: 中文
-   en: 英文
-   ja: 日语
-   ko：韩语
-   vi：越南语
-   th：泰语
-   id：印尼语
-   ms：马来语
-   tl：菲律宾语
-   hi：印地语
-   ar：阿拉伯语
-   fr：法语
-   de：德语
-   es：西班牙语
-   pt：葡萄牙语
-   ru：俄语
-   it：意大利语
-   nl：荷兰语
-   sv：瑞典语
-   da：丹麦语
-   fi：芬兰语
-   no：挪威语
-   el：希腊语
-   pl：波兰语
-   cs：捷克语
-   hu：匈牙利语
-   ro：罗马尼亚语
-   bg：保加利亚语
-   hr：克罗地亚语
-   sk：斯洛伐克语

messages

`array[object]`

是

消息列表。包含当前待识别的音频，以及可选的对话上下文（用于提升识别效果）。  
**详见如下说明。**

**messages参数说明：**

**重要**上下文功能用于提升专有词汇的识别准确率，使用方法详见[上下文增强](https://help.aliyun.com/zh/model-studio/improve-asr-accuracy#ctx_enhance_h2)。

**约束**：上下文消息（`input_text` 和 `text` 类型）各最多 5 条，超出时保留最近的 5 条。每轮上下文文本总长度（`user` 和 `assistant` 的 `text` 字段长度之和）不超过 400 个字符（按字符数计算，每个字符计为 1），超出部分从末尾截断。

**重要**携带上下文时，`messages` 中的消息顺序有要求：上下文消息必须按对话轮次排列，每轮中 `user`（`input_text` 类型）必须在对应的 `assistant`（`text` 类型）之前；包含 `input_audio` 的 `user` 消息必须放在 `messages` 数组的最后。

**参数**

**类型**

**是否必须**

**说明**

role

`string`

是

消息角色。取值范围：

-   `user`（必选）：用户消息。type为`input_audio`时表示当前待识别的音频；type为`input_text`时表示前几轮的识别结果或领域相关的词表（可选，上下文）。
-   `assistant`（可选，上下文）：前几轮大语言模型的回复内容。

content

`array[object]`

是

消息内容列表。详细如下说明。

**content参数说明：**

**参数**

**类型**

**是否必须**

**说明**

type

`string`

是

内容类型。每个请求至少需要一条`input_audio`类型的消息。取值范围：

-   `input_audio`（必选）：当前待识别的音频输入（role为user），需同时传入`input_audio`对象。
-   `input_text`（可选，上下文）：前几轮用户语音的识别结果或领域相关的词表（role为user），需同时传入`text`字段。
-   `text`（可选，上下文）：前几轮大语言模型的回复内容（role为assistant），需同时传入`text`字段。

input\_audio

`object`

否

当`type`为`input_audio`时必填。

input\_audio.data

string

是

待识别音频数据。关于支持的音频格式、文件大小限制、时长限制等输入要求，请参见[音频规格](https://help.aliyun.com/zh/model-studio/asr-model#asr_audio_spec02)。支持以下两种方式：

-   **音频文件URL**：直接传入可公开访问的音频文件地址。
-   **Base64 Data URI**：采用Data URI格式传入Base64编码的音频数据，值由`data:{MIME_TYPE};base64,`前缀与Base64编码的音频数据拼接而成。支持的MIME类型包括`audio/wav`、`audio/mp3`等。  
    示例（URL方式）：`[https://example.com/audio/sample.wav](https://example.com/audio/sample.wav)`  
    示例（Base64方式）：`data:audio/wav;base64,{BASE64_ENCODED_DATA}`

text

`string`

否

当`type`为`input_text`时，填入前几轮用户语音的识别结果或领域相关的词表；当`type`为`text`时，填入前几轮大语言模型的回复内容。文本按字符数计算，每个字符计为 1。每轮上下文中所有消息的 `text` 字段长度之和不超过 400 个字符，超出部分从末尾截断。

## 关键接口

### NativeNui

#### initializeFileTrans

初始化语音识别SDK实例。

**说明**与实时语音识别不同，非实时（录音文件）转录必须使用 `initializeFileTrans` 方法并传入 [INativeFileTransCallback](#file-trans-callback) 回调，而不是 `initialize`。

此接口会引起阻塞，应在非UI线程调用。

**方法签名**
```
public initializeFileTrans(callback: INativeFileTransCallback,
                           parameters: string,
                           level: number,
                           save_log: boolean = false): number
```
**参数说明**

**参数**

**类型**

**说明**

`callback`

`INativeFileTransCallback`

文件转录事件和数据回调接口的实现。

`parameters`

`string`

JSON字符串，包含鉴权、连接和调试参数。参见[连接与控制参数](#connection-parameters)。

`level`

`number`

控制SDK自身日志的打印级别，取值为枚举。

`save_log`

`boolean`

是否保存本地日志。若为`true`，须在[连接与控制参数](#connection-parameters)中通过`debug_path`指定路径，并可通过`max_log_file_size`设置文件大小。

**返回值说明**

返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。

#### setParams

此接口用于独立设置或更新 `nls_config` 参数。如果所有参数都在[startFileTranscriber](#startfiletranscriber)中一次性提供，则无需调用此方法。

**方法签名**
```
public setParams(params: string): number
```
**参数说明**

**参数**

**类型**

**说明**

`params`

`string`

[语音识别效果参数](#recognition-parameters)中的`nls_config`参数，`nls_config`之外的参数不支持通过该方法进行设置。

**返回值说明**

返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。

#### startFileTranscriber

开始识别。

**方法签名**
```
public startFileTranscriber(params: string, task_id: ArrayBuffer): number
```
**参数说明**

**参数**

**类型**

**说明**

`params`

`string`

[语音识别效果参数](#recognition-parameters)。  
示例：  

```
{
 "apikey": "st-****",
 "messages": [
 {
 "content": [
 {
 "input_audio": {
 "data": "{YOUR_AUDIO_URL}"
 },
 "type": "input_audio"
 }
 ],
 "role": "user"
 }
 ],
 "nls_config": {
 "format": "mp3",
 "model": "qwen-audio-3.0-asr-flash"
 }
}
```

`task_id`

`ArrayBuffer`

任务ID缓冲区。SDK会将内部生成的随机任务ID字符串写入该缓冲区，要求缓冲区字节长度必须 **\>= 33字节**（示例中使用 `new ArrayBuffer(64)`）。调用成功后可通过转码获取该任务的`task_id`。

**返回值说明**

返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。

#### queryFileTranscriber

此接口用于主动查询一个异步任务的当前状态和结果。调用成功后，结果将通过`onFileTransEventCallback`回调中的 `EVENT_FILE_TRANS_QUERY_RESULT` 事件返回。

**方法签名**
```
public queryFileTranscriber(task_id: string): number
```
**参数说明**

**参数**

**类型**

**说明**

`task_id`

`string`

待查询的任务ID（由 `startFileTranscriber` 写入缓冲区获得）。

**返回值说明**

返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。

#### cancelFileTranscriber

立即取消当前任务。

**方法签名**
```
public cancelFileTranscriber(task_id: string): number
```
**参数说明**

**参数**

**类型**

**说明**

`task_id`

`string`

待取消的任务ID。

**返回值说明**

返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。

#### release

释放SDK所有内部资源。此方法调用后，SDK实例将变为不可用状态，如需再次使用，必须重新调用[initializeFileTrans](#initializefiletrans)进行初始化。

**方法签名**
```
public release(): number
```
**返回值说明**

返回错误码，参见[错误码查询](https://help.aliyun.com/zh/isi/support/error-codes)。

#### GetVersion

获得当前SDK版本信息。

**方法签名**
```
public GetVersion(): string
```
**返回值说明**

当前SDK版本信息。

### INativeFileTransCallback：监听回调

#### onFileTransEventCallback：监听事件和语音识别结果

**方法签名**
```
onFileTransEventCallback: (event: Constants.NuiEvent, resultCode: number, finish: number,
                           asrResult: AsrResult, taskId: string) => void;
```
**参数说明**

**参数**

**类型**

**说明**

`event`

`Constants.NuiEvent`

回调事件。

`resultCode`

`number`

[错误码](https://help.aliyun.com/zh/isi/support/error-codes)，在出现EVENT\_ASR\_ERROR事件时有效。

`finish`

`number`

任务是否结束标记。

`asrResult`

`AsrResult`

语音识别结果。

`taskId`

`string`

任务ID。

#### onFileTransLogTrackCallback：监听追踪日志

此回调用于接收 SDK 内部的详细日志，方便进行问题定位和调试。

使用此回调需下载 20260908 或更新的 HarmonyOS SDK 包。

```
onFileTransLogTrackCallback?: (level: Constants.LogLevel, log: string) => void;
```

### 事件类型

HarmonyOS SDK 中事件类型通过 `Constants.NuiEvent` 枚举定义，以下列出录音文件转录相关的事件：

**事件**

**说明**

EVENT\_FILE\_TRANS\_CONNECTED

连接服务成功。

EVENT\_FILE\_TRANS\_UPLOADED

上传待识别音频文件成功。

EVENT\_FILE\_TRANS\_QUERY\_RESULT

查询任务结果。

EVENT\_FILE\_TRANS\_RESULT

识别最终结果。

EVENT\_ASR\_ERROR

语音识别过程中出现错误。
