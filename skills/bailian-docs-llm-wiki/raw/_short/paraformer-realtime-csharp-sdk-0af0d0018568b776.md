# Paraformer 实时语音识别 C# SDK 接入

通过 C# SDK 向 Paraformer 流式发送音频并接收识别结果。

<a id="快速开始"></a>

<a id="quick-start"></a>

## 快速开始

<a id="installation"></a>

按[SDK简介](../model-api-reference/more-about-models/csharp-speech-sdk/csharp-sdk.md)安装 SDK 并配置 API Key。将示例地址中的 `WorkspaceId` 替换为同地域的业务空间 ID。

将[示例音频](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/audios/6a4b3c2d1e0f9093.wav)保存为 `asr_example.wav`。示例分块读取文件，模拟实时输入，无需麦克风。

识别音频，在控制台打印每句话的最终文本。

<a id="code-block"></a>

```csharp
using DashScope.Speech;

await using var client = new FunAsrSpeechTranscriber(new FunAsrTranscriberOptions
{
    Model = "paraformer-realtime-v2",
    Url = "wss://WorkspaceId.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference",
    Format = "wav",
    SampleRate = 16000,
});
client.SentenceEnd += (_, e) => Console.WriteLine(e.Sentence.Text);

using var audio = File.OpenRead("asr_example.wav");
byte[] buffer = new byte[3200];
await client.StartAsync();
int count;
while ((count = await audio.ReadAsync(buffer)) > 0)
{
    await client.SendAudioAsync(buffer.AsMemory(0, count));
    await Task.Delay(100);
}
await client.StopAsync();
```

<a id="调用步骤"></a>

<a id="workflow"></a>

## 调用步骤

1.  创建 `FunAsrSpeechTranscriber` 实例，将 `Model` 设为 `paraformer-realtime-v2`（或 `paraformer-realtime-8k-v2`），并订阅 `SentenceEnd` 等事件。
2.  调用 `StartAsync` 建立连接并发送 `run-task`，等待 `task-started`。
3.  在 `TranscriberStarted` 之后调用 `SendAudioAsync` 按音频播放节奏持续上行音频帧。
4.  在 `SentenceEnd` 中获取每句话的最终识别结果。
5.  音频送完后调用 `StopAsync`，等待 `task-finished`（即 `Completed`）。
6.  不再使用时调用 `DisposeAsync` 释放连接。

<a id="参数说明"></a>

<a id="options"></a>

## 参数说明

<a id="api-reference"></a>

创建 `FunAsrSpeechTranscriber` 时传入 `FunAsrTranscriberOptions`。可选字段为 `null` 时不发送给服务端。

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `Model` | `string` | `qwen-audio-3.1-asr-flash-streaming` | 模型 ID；显式指定本系列模型。 |
| `Format` | `string` | `pcm` | 音频格式。 |
| `SampleRate` | `int` | `16000` | 音频采样率，单位 Hz（须与输入音频实际采样率一致）。<br><br>> **说明**<br>><br>> `paraformer-realtime-v2` 支持任意采样率；`paraformer-realtime-8k-v2` 仅支持 `8000` Hz。 |
| `SemanticPunctuationEnabled` | `bool?` | `null` | 是否启用语义断句。 |
| `MaxSentenceSilence` | `int?` | `null` | VAD 断句的静音阈值，单位毫秒。 |
| `MultiThresholdModeEnabled` | `bool?` | `null` | 是否启用多阈值 VAD 断句。 |
| `DisfluencyRemovalEnabled` | `bool?` | `null` | 是否过滤语气词。 |
| `Heartbeat` | `bool?` | `null` | 持续发送静音音频时是否保持连接。 |
| `VocabularyId` | `string?` | `null` | 预编译热词表 ID。 |
| `LanguageHints` | `IList<string>?` | `null` | 语种提示。 |
| `ExtraParametersJson` | `string?` | `null` | JSON 对象字符串，合并到协议的 `parameters` 对象。 |
