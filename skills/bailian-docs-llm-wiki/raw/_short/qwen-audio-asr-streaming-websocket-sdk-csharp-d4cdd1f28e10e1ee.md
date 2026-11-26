# Qwen-Audio-ASR-Streaming C# SDK

其他模型 — [Qwen-Audio-ASR-Message C# SDK](qwen-asr-message-websocket-sdk-csharp-7aa85c2b1a5a929c.md)

<a id="快速开始"></a>

<a id="quick-start"></a>

## 快速开始

<a id="model-qwen-audio-asr-streaming"></a>

<a id="installation"></a>

按[SDK简介](../model-api-reference/more-about-models/csharp-speech-sdk/csharp-sdk.md)安装 SDK 并配置 API Key。将示例地址中的 `WorkspaceId` 替换为同地域的业务空间 ID。

将[示例音频](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/audios/6a4b3c2d1e0f9093.wav)保存为 `asr_example.wav`。示例分块读取文件，模拟实时输入，无需麦克风。

识别音频，在控制台打印中间结果和每句话的最终文本。

<a id="code-block"></a>

```csharp
using DashScope.Speech;

await using var client = new FunAsrSpeechTranscriber(new FunAsrTranscriberOptions
{
    Model = "qwen-audio-3.1-asr-flash-streaming",
    Url = "wss://WorkspaceId.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference",
    Format = "wav",
    SampleRate = 16000,
});
client.PartialResult += (_, e) => Console.WriteLine($"中间结果: {e.Sentence.Text}");
client.SentenceEnd += (_, e) => Console.WriteLine($"定稿: {e.Sentence.Text}");

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

1.  创建 `FunAsrSpeechTranscriber` 实例并订阅事件（如 `SentenceEnd`；需要显示中间结果时再订阅 `PartialResult`）。
    
2.  调用 `StartAsync` 建立连接并发送 `run-task`，等待 `task-started`。
    
3.  在 `TranscriberStarted` 之后调用 `SendAudioAsync` 按音频播放节奏持续上行音频帧。
    
    > **说明**
    >
    > 使用 `Qwen-Audio-ASR-Message` 时，如需在任务运行中更新上下文，可在发送音频期间调用 `SendContextAsync`。
    
4.  在 `SentenceBegin`、`PartialResult`、`SentenceEnd` 中获取中间与最终结果（`PartialResult` 的文本可能变化，以 `SentenceEnd` 的最终文本为准）。
    
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
| `SampleRate` | `int` | `16000` | 音频采样率，单位 Hz。<br><br>> **说明**<br>><br>> `Qwen-Audio-ASR-Message` 仅支持 `16000` Hz。 |
| `MaxSentenceSilence` | `int?` | `null` | VAD 断句的静音阈值，单位毫秒。 |
| `MultiThresholdModeEnabled` | `bool?` | `null` | 是否启用多阈值 VAD 断句。<br><br>> **说明**<br>><br>> 仅适用于 `Qwen-Audio-ASR-Streaming` 系列。 |
| `KeepDialect` | `bool?` | `null` | 是否保留方言表达。<br><br>> **说明**<br>><br>> `Qwen-Audio-ASR-Streaming` 系列仅适用于 `qwen-audio-3.1-asr-flash-streaming`；`Qwen-Audio-ASR-Message` 系列仅在最终识别结果（`SentenceEnd`）中生效，中间结果（`PartialResult`）不支持。 |
| `Heartbeat` | `bool?` | `null` | 持续发送静音音频时是否保持连接。 |
| `VocabularyId` | `string?` | `null` | 预编译热词表 ID。 |
| `Vocabulary` | `IDictionary<string, int>?` | `null` | 即时热词及对应权重。 |
| `LanguageHints` | `IList<string>?` | `null` | 语种提示。 |
| `SpeechNoiseThreshold` | `float?` | `null` | 语音与噪音的判定阈值。 |
| `SpecialWordFilter` | `string?` | `null` | 敏感词过滤规则，传入 JSON 字符串。<br><br>> **说明**<br>><br>> 仅适用于 `Qwen-Audio-ASR-Streaming` 系列。 |
| `ExtraParametersJson` | `string?` | `null` | JSON 对象字符串，合并到协议的 `parameters` 对象。 |
| `IntermediateResultEnabled` | `bool?` | `null` | 是否返回中间结果。默认只返回定稿；设为 `true` 后，可通过 `PartialResult` 接收中间结果。<br><br>> **说明**<br>><br>> 仅适用于 `Qwen-Audio-ASR-Message` 系列（`Qwen-Audio-ASR-Streaming` 系列默认持续返回中间结果）。 |
| `DisfluencyRemovalEnabled` | `bool?` | `null` | 是否过滤语气词。<br><br>> **说明**<br>><br>> 仅适用于 `Qwen-Audio-ASR-Message` 系列。 |
