# Fun-ASR-Flash C# SDK

通过 C# SDK 调用 Fun-ASR-Flash 转写音频文件并获取识别结果。

<a id="快速开始"></a>

<a id="quick-start"></a>

## 快速开始

按[SDK简介](https://help.aliyun.com/zh/model-studio/csharp-sdk)安装 SDK 并配置 API Key。将示例地址中的 `WorkspaceId` 替换为同地域的业务空间 ID。

以下示例使用 `fun-asr-flash-2026-06-15` 转写音频文件，并在控制台输出文本。

<a id="code-block"></a>

```csharp
using DashScope.Transcription;

using var client = new FunAsrFlashFileTranscriber(new FlashFileTranscriberOptions
{
    Url = "https://WorkspaceId.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation",
});
var request = new FlashTranscriptionRequest
{
    Model = "fun-asr-flash-2026-06-15",
    Audio = "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav",
    Format = "wav",
};

var result = await client.TranscribeAsync(request);
Console.WriteLine(result.Text);
```

<a id="调用步骤"></a>

<a id="workflow"></a>

## 调用步骤

1.  创建 `FunAsrFlashFileTranscriber`，将 `FlashFileTranscriberOptions.Url` 设为业务空间的接口地址。
    
2.  创建 `FlashTranscriptionRequest`，将 `Model` 设为 `fun-asr-flash-2026-06-15`。`Audio` 可传入公网 URL、Data URI 或本地文件路径。`Format` 须与音频格式一致；使用裸 PCM 时，将 `SampleRate` 设为实际采样率。
    
3.  调用 `TranscribeAsync`，从返回结果的 `Text` 读取完整转写。
    
4.  如需通过 SSE 接收结果，改用 `TranscribeStreamingAsync`，通过 `await foreach` 读取识别结果。
    
    > **说明**
    >
    > 仅当音频时长不少于 1 分钟时才会分多次返回结果。
    

方法和结果对象见[接口与事件](https://help.aliyun.com/zh/model-studio/csharp-sdk-methods-and-events#fun-asr-flash-file-transcriber)。

<a id="参数说明"></a>

<a id="options"></a>

## 参数说明

下表列出本系列支持的 `FlashTranscriptionRequest` 请求属性。默认值指 SDK 属性的初始值。协议字段见 [HTTP API](fun-asr-flash-recorded-speech-recognition-http-a-7716e5d27dfd9a7b.md)。

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `Model` | `string` | `qwen-audio-3.1-asr-flash` | 模型 ID。<br><br>> **说明**<br>><br>> 调用本系列时须显式指定模型 ID，例如 `fun-asr-flash-2026-06-15`；不设置时使用表中的 SDK 默认值。 |
| `Audio` | `string` | `null` | 必填。待转写音频的公网 URL、Base64 Data URI 或本地文件路径。传入本地路径时，SDK 会读取文件并转为 Data URI。 |
| `Format` | `string` | `wav` | 音频格式，例如 `wav`、`mp3` 或 `pcm`，须与输入音频一致。 |
| `SampleRate` | `int?` | `null` | 音频采样率，单位为 Hz。<br><br>> **说明**<br>><br>> 使用裸 PCM 音频时，须设置为录音的实际采样率。 |
| `VocabularyId` | `string?` | `null` | 预编译热词表 ID，可跨请求复用。<br><br>> **说明**<br>><br>> 地域支持范围见[支持的模型与地域](../model-user-guide/model-experience/speech-and-audio/speech-recognition/improve-asr-accuracy.md#supported-models)。 |
| `LanguageHints` | `IList<string>?` | `null` | 识别语种提示，例如 `["zh"]`。<br><br>> **说明**<br>><br>> 传入多个值时，仅第一个生效。 |
| `Context` | `IList<FlashContextMessage>?` | `null` | 用 `FlashContextMessage.Role` 和 `FlashContextMessage.Text` 指定角色和文本。<br><br>> **说明**<br>><br>> 每轮先传用户消息，再传对应的助手消息；两类消息各最多保留最近 5 条，每轮文本合计最多 400 个字符。 |
| `ExtraParametersJson` | `string?` | `null` | 以 JSON 对象字符串传入附加参数。SDK 将其中的字段合并到请求的 `parameters` 对象，仅可传入模型支持的协议字段。 |
