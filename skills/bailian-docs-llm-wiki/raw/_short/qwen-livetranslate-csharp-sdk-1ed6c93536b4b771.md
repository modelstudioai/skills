# Qwen-LiveTranslate-Realtime C# SDK

使用 C# SDK 通过 WebSocket 调用 Qwen-LiveTranslate-Realtime，将输入语音实时翻译为目标语言的文本和音频。

## 安装 SDK

下载 [Bailian.DashScope-1.1.0.zip](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9000.zip) 并解压。在 C# 项目中使用时，从[本地 NuGet 源安装 SDK](https://help.aliyun.com/zh/model-studio/qwen-audio-realtime-csharp-sdk#install-sdk)。

## 快速开始

运行随包提供的示例需要 .NET 10 SDK。`demo/nuget.config` 已将 `packages/` 配置为本地 NuGet 源。

1.  [获取 API Key](raw/model-api-reference/preparations/get-api-key.md)，并设置环境变量 `DASHSCOPE_API_KEY`。
2.  在解压目录的 `demo/` 下准备 `input.pcm`，然后运行以下命令。输入必须是 16 kHz、单声道、16 bit 小端裸 PCM。若源文件为 WAV，先转为裸 PCM。

输出译音时，显式传入模型支持的音色。此示例使用 `Serena`。

```
dotnet run --project DashScope.Cli --framework net10.0 -p:TargetFrameworks=net10.0 -- translate --audio input.pcm --model qwen3.8-livetranslate-flash-realtime --source zh --target en --voice Serena --output translated.pcm
```

命令行示例按 20 毫秒一帧发送文件，并在末尾补约 1 秒静音。终端显示原文转写和译文，译音写入 `translated.pcm`。

## C# 调用示例

以下程序将一段裸 PCM 音频按实时节奏发送，等待应答结束，再将音频写到 `output.pcm`。创建 .NET 控制台项目，添加 `Bailian.DashScope` 后，用以下代码替换 `Program.cs`。

```
using DashScope.Qwen;

if (args.Length < 2)
    throw new ArgumentException("Usage: <input.pcm> <model> [voice]");

using var timeout = new CancellationTokenSource(TimeSpan.FromSeconds(60));
var ct = timeout.Token;
await using var client = new QwenLiveTranslator(new QwenLiveTranslateOptions
{
    Model = args[1],
    Voice = args.Length > 2 ? args[2] : null,
    Modalities = ["text", "audio"],
    SourceLanguage = "zh",
    TargetLanguage = "en",
    SampleRate = 16000,
});

using var output = File.Create("output.pcm");
var completed = new TaskCompletionSource<string?>(TaskCreationOptions.RunContinuationsAsynchronously);
client.TranslationCompleted += (_, e) => Console.WriteLine(e.Text);
client.TranslatedAudioChunk += (_, e) => output.Write(e.Pcm);
client.ResponseCompleted += (_, e) => completed.TrySetResult(e.Status);
client.ErrorOccurred += (_, e) => completed.TrySetException(
    new InvalidOperationException($"{e.ServerErrorCode}: {e.ServerErrorMessage}"));

await client.ConnectAsync(ct);
using var input = File.OpenRead(args[0]);
var frame = new byte[640];
int size;
while ((size = await input.ReadAsync(frame.AsMemory(), ct)) > 0)
{
    await client.AppendAudioAsync(frame.AsMemory(0, size), ct);
    await Task.Delay(20, ct);
}

Array.Clear(frame);
for (var i = 0; i < 60; i++)
{
    await client.AppendAudioAsync(frame, ct);
    await Task.Delay(20, ct);
}

await client.FinishAsync(ct);
var status = await completed.Task.WaitAsync(ct);
if (status != "completed" || output.Length == 0)
    throw new InvalidOperationException($"Status: {status}, audio bytes: {output.Length}");
```

将快速开始中的裸 PCM 文件放到项目目录，运行。

```
dotnet run -- input.pcm qwen3.8-livetranslate-flash-realtime Serena
```

## API 参考

使用 `DashScope.Qwen.QwenLiveTranslator`，创建实例时传入 `QwenLiveTranslateOptions`。3.5 和 3.8 的服务端配置和事件字段有差异，具体以对应模型的[客户端事件](raw/model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory/live-translator-client-events.md)为准。

### 连接与翻译选项

选项

类型

默认值

说明

`ApiKey`

`string?`

`null`

百炼 API Key。未设置时读取 `DASHSCOPE_API_KEY`。

`Url`

`string`

`wss://dashscope.aliyuncs.com/api-ws/v1/realtime`

WebSocket 地址。SDK 将 `Model` 拼接到 URL 的 `model` 查询参数。

`WorkspaceId`

`string?`

`null`

业务空间 ID。设置后通过 `X-DashScope-WorkSpace` 请求头传递。使用业务空间专属域名时，通过 `Url` 指定完整地址。

`ConnectTimeout`

`TimeSpan`

`10 s`

建立 WebSocket 连接的超时。

`StartTimeout`

`TimeSpan`

`10 s`

等待 `session.created` 的超时。

`StopTimeout`

`TimeSpan`

`10 s`

等待 `session.finished` 的超时，适用于等待该事件的收尾方式。

`FinishMode`

`QwenRealtimeFinishMode?`

`null`

留空时按模型选择收尾方式。可读取实例的 `FinishMode` 查看实际取值。

`Model`

`string`

`qwen3.5-livetranslate-flash-realtime`

模型 ID。

`Modalities`

`IList<string>`

`["text", "audio"]`

输出模态。仅需译文时设为 `["text"]`。

`Voice`

`string?`

`null`

输出译音时使用的音色。未设置时由服务端选择默认值。使用 3.8 并输出语音时指定该模型支持的音色。

`EnableVoiceClone`

`bool?`

`null`

译音的声音复刻开关。

`VoiceCloneFrequency`

`string`

`once`

`once` 在会话开始时复刻一次，`always` 逐句复刻，`never` 使用已有的复刻音色 ID。按型号核对可用方式。

`SampleRate`

`int`

`16000`

输入采样率，单位为 Hz。选择所用型号支持的采样率。

`InputAudioFormat`

`string`

`pcm`

输入音频格式。SDK 选项接受 `pcm` 或 `opus`，具体可用格式以模型的客户端事件参考为准。

`OutputAudioFormat`

`string?`

`null`

输出音频格式，例如 `pcm`。留空时使用服务端默认值。

`TranscriptionModel`

`string?`

`qwen3-asr-flash-realtime`

源语音识别模型。使用 `qwen3.5-livetranslate-flash-realtime` 时，将此项和 `SourceLanguage` 都设为 `null` 可省略 `input_audio_transcription` 配置。3.8 的源语音识别始终开启。

`SourceLanguage`

`string?`

`null`

源语言代码，例如 `zh`。留空时由服务端自动检测。

`TargetLanguage`

`string`

`en`

目标语言代码，例如 `en`。

`SkipSameLanguageText`

`bool?`

`null`

源语言与目标语言相同时跳过译文输出。按所用版本确认支持情况。

`SkipSameLanguageAudio`

`bool?`

`null`

源语言与目标语言相同时跳过译音输出。按所用版本确认支持情况。

`CorpusPhrases`

`IDictionary<string, string>?`

`null`

翻译热词，从源词映射到目标词，对应 `translation.corpus.phrases`。

`VadThreshold`

`double?`

`0.5`

服务端 VAD 阈值，取值 -1.0 至 1.0。

`VadSilenceMs`

`int`

`1000`

服务端判定语音结束前需要的静音时长，单位为毫秒。

`EnableDebugInfo`

`bool?`

`null`

请求服务端返回调试信息。

使用 3.8 做音视频翻译时，先按[WebSocket 接入](raw/_short/livetranslate-realtime-websocket-access-69ee95b6726440dc.md)将 `session.input_modalities` 设为 `["audio", "video"]`，再随音频发送图片帧。`AppendImageAsync` 负责发送图片帧。配置或发送 SDK 未封装的字段时，可以用 `SendRawEventAsync` 发送完整的客户端事件。

### 方法

除 `DisposeAsync` 外，下列方法返回 `Task`。`ct` 为可选取消令牌。

方法

说明

`ConnectAsync(CancellationToken ct = default)`

建立连接，等待 `session.created`，然后发送 `session.update`。

`AppendAudioAsync(ReadOnlyMemory<byte> pcm, CancellationToken ct = default)`

发送一帧音频。SDK 将字节编码为 Base64 并通过 `input_audio_buffer.append` 发送。

`AppendImageAsync(string imageBase64, CancellationToken ct = default)`

发送一帧 Base64 图像，对应 `input_image_buffer.append`。使用支持图片输入的模型并提前启用音频和图片输入。

`SendRawEventAsync(string frameJson, CancellationToken ct = default)`

原样发送一条完整的客户端事件 JSON，可用于 SDK 尚未单独封装的事件。

`FinishAsync(CancellationToken ct = default)`

按实际 `FinishMode` 正常结束会话。

`AbortAsync()`

立即关闭连接，放弃在途结果。

`DisposeAsync()`

异步释放资源，返回 `ValueTask`。

### 事件

事件

事件参数

触发条件

`SessionReady`

`string?`

会话就绪，值为 `session.id`。

`SourceTranscriptUpdated`

`QwenTranscriptEventArgs`

当前的源语音转写。启用源语音转写后才返回。

`SourceTranscriptCompleted`

`QwenTranscriptEventArgs`

一句源语音的最终转写。

`TranslationTextDelta`

`QwenTextDeltaEventArgs`

译文增量。需要最终译文时，读取 `TranslationCompleted`。

`TranslationCompleted`

`QwenTranscriptEventArgs`

本句的完整译文。

`TranslatedAudioChunk`

`QwenAudioChunkEventArgs`

译音分片。音频格式和采样率以会话配置和模型实际返回为准。

`TranslatedAudioCompleted`

`EventArgs`

本轮译音全部下发。

`ResponseCompleted`

`QwenResponseSummary`

收到 `response.done`，返回状态和用量。

`RawServerEvent`

`QwenServerEventArgs`

原始服务端事件，可读取事件类型和 JSON 对象。

`ErrorOccurred`

`DashScopeErrorEventArgs`

服务端错误或连接异常。

事件参数字段见 [C# SDK 结果对象](https://help.aliyun.com/zh/model-studio/qwen-audio-realtime-csharp-sdk#result-types)。翻译场景的用量为会话累计值。

### 会话收尾

如果不再发送音频，调用 `FinishAsync` 结束会话，让服务端返回剩余的译文和译音。LiveTranslate 默认使用 `FinishAndWait`，发送 `session.finish` 并等待 `session.finished`。
