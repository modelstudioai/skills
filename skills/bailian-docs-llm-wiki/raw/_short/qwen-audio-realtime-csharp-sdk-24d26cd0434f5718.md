# Qwen-Audio-Realtime C# SDK

使用 C# SDK 通过 WebSocket 向 Qwen-Audio-Realtime 实时发送音频，接收文本和音频应答。

## 前提条件

[获取 API Key](raw/model-api-reference/preparations/get-api-key.md)，并设置环境变量 `DASHSCOPE_API_KEY`。

### 安装 SDK

下载 [Bailian.DashScope-1.1.0.zip](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9000.zip) 并解压。SDK 支持 `net8.0` 和 `net10.0`。在项目目录运行以下命令，将示例路径改为解压后的 `packages/` 目录。

```
dotnet add package Bailian.DashScope --version 1.1.0 --source "/path/to/Bailian.DashScope-1.1.0/packages"
```

也可直接引用解压目录 `sdk/net8.0/` 或 `sdk/net10.0/` 下与项目目标框架对应的 `DashScope.dll`。将 `DashScope.xml` 放在 DLL 同一目录可在 IDE 中查看接口注释。

## 快速开始

### 运行随包示例

运行随包提供的示例需要 .NET 10 SDK。`demo/nuget.config` 已将 `packages/` 配置为本地 NuGet 源。

在解压目录的 `demo/` 下准备 `input.pcm`，然后运行以下命令。输入必须是 16 kHz、单声道、16 bit 小端裸 PCM。若源文件为 WAV，先转为裸 PCM。

```
dotnet run --project DashScope.Cli --framework net10.0 -p:TargetFrameworks=net10.0 -- chat --audio input.pcm --model qwen-audio-3.1-realtime-plus --voice longanfengyue_v3.1 --output response.pcm
```

命令行示例按 20 毫秒一帧发送文件，并在末尾补约 1 秒静音。终端显示输入转写和应答文本，应答音频写入 `response.pcm`。

### 在项目中调用

以下程序将一段裸 PCM 音频按实时节奏发送，等待应答结束，再将音频写到 `output.pcm`。创建 .NET 控制台项目，添加 `Bailian.DashScope` 后，用以下代码替换 `Program.cs`。

```
using DashScope.Qwen;

if (args.Length < 2)
    throw new ArgumentException("Usage: <input.pcm> <model> [voice]");

using var timeout = new CancellationTokenSource(TimeSpan.FromSeconds(60));
var ct = timeout.Token;
await using var client = new QwenRealtimeConversation(new QwenRealtimeConversationOptions
{
    Model = args[1],
    Voice = args.Length > 2 ? args[2] : null,
    Url = Environment.GetEnvironmentVariable("DASHSCOPE_REALTIME_URL")
        ?? "wss://dashscope.aliyuncs.com/api-ws/v1/realtime",
    Modalities = ["text", "audio"],
    TurnDetectionMode = QwenTurnDetectionMode.ServerVad,
});

using var output = File.Create("output.pcm");
var completed = new TaskCompletionSource<string?>(TaskCreationOptions.RunContinuationsAsynchronously);
client.AssistantTextCompleted += (_, e) => Console.WriteLine(e.Text);
client.AssistantAudioChunk += (_, e) => output.Write(e.Pcm);
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

var status = await completed.Task.WaitAsync(ct);
await client.FinishAsync(ct);
if (status != "completed" || output.Length == 0)
    throw new InvalidOperationException($"Status: {status}, audio bytes: {output.Length}");
```

将快速开始中的裸 PCM 文件放到项目目录，运行。

```
dotnet run -- input.pcm qwen-audio-3.1-realtime-plus longanfengyue_v3.1
```

## 请求参数

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

`qwen-audio-3.1-realtime-plus`

模型 ID。调用 Omni 时显式设置为所选 Omni Realtime 模型。

`Modalities`

`IList<string>`

`["text", "audio"]`

输出模态。仅需文本时设为 `["text"]`。

`Voice`

`string?`

`null`

输出音频使用的音色。`null` 由服务端选择默认值。Audio 3.1 示例显式传入 `longanfengyue_v3.1`。

`EnableSpeechEmotion`

`bool?`

`null`

情感语音开关，适用范围以模型的客户端事件参考为准。

`Instructions`

`string?`

`null`

系统提示词。

`MaxHistoryTurns`

`int?`

`null`

保留的历史问答轮数，取值 1 至 50。

`ToolsJson`

`string?`

`null`

函数工具定义，传入 OpenAI 格式的 tools JSON 数组字符串。

`TurnDetectionMode`

`QwenTurnDetectionMode`

`ServerVad`

轮次检测模式。`ServerVad` 由服务端检测语音起止。部分模型也支持 `SmartTurn`。`PushToTalk` 由客户端提交音频并请求应答。

`VadThreshold`

`double?`

`null`

服务端 VAD 阈值，取值 -1.0 至 1.0，仅用于 `ServerVad`。

`VadSilenceMs`

`int?`

`null`

句尾静音时长，取值 200 至 6000 毫秒，仅用于 `ServerVad`。未设置时使用服务端默认值，详见各模型的事件参考。

中国站业务空间专属域名可通过 `Url` 配置。地址和地域见 [Audio Realtime WebSocket 接入](raw/model-api-reference/realtime-api-directory/audio-realtime-api-directory/audio-realtime-websocket-access.md) 或 [Omni Realtime WebSocket 接入](raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory/omni-realtime-websocket-access.md)。

## 接口参考

Audio Realtime 和 Omni Realtime 均使用 `DashScope.Qwen.QwenRealtimeConversation`。创建实例时传入 `QwenRealtimeConversationOptions`。默认模型为 Audio Realtime，调用 Omni 时需显式传入 Omni 模型 ID。

### 方法

除 `DisposeAsync` 外，下列方法返回 `Task`。`ct` 为可选取消令牌。

方法

说明

`ConnectAsync(CancellationToken ct = default)`

建立连接，等待 `session.created`，然后发送 `session.update`。

`AppendAudioAsync(ReadOnlyMemory<byte> pcm, CancellationToken ct = default)`

发送一帧音频。SDK 将字节编码为 Base64 并通过 `input_audio_buffer.append` 发送。

`CommitAudioAsync(CancellationToken ct = default)`

在 `PushToTalk` 下用 `input_audio_buffer.commit` 提交音频缓冲。

`CreateResponseAsync(JsonObject? responseOptions = null, CancellationToken ct = default)`

发送 `response.create` 请求应答。`responseOptions` 可覆盖本轮 `response` 配置。

`SendItemAsync(JsonObject item, CancellationToken ct = default)`

使用 `conversation.item.create` 将 `item` 加入会话。

`SendFunctionCallOutputAsync(string callId, string outputJson, CancellationToken ct = default)`

使用事件提供的 `callId` 和结果 JSON 文本回传工具结果。

`SendRawEventAsync(string frameJson, CancellationToken ct = default)`

原样发送一条完整的客户端事件 JSON，可用于 SDK 尚未单独封装的事件。

`FinishAsync(CancellationToken ct = default)`

按实际 `FinishMode` 正常结束会话。

`AbortAsync()`

立即关闭连接，放弃在途结果。

`DisposeAsync()`

异步释放资源，返回 `ValueTask`。

在 `PushToTalk` 模式下，发送音频后依次调用 `CommitAudioAsync` 和 `CreateResponseAsync`。处理函数调用时，收到 `FunctionCallReceived` 后执行工具并回传结果。需要模型继续应答时，再调用 `CreateResponseAsync`。

### 事件

事件

事件参数

触发条件

`SessionReady`

`string?`

会话就绪，值为 `session.id`。

`UserSpeechStarted`

`QwenSpeechEventArgs`

服务端 VAD 检测到用户开始说话。

`UserSpeechStopped`

`QwenSpeechEventArgs`

服务端 VAD 检测到用户停止说话。

`UserTranscriptUpdated`

`QwenTranscriptEventArgs`

当前的输入转写文本，后续可修正。

`UserTranscriptCompleted`

`QwenTranscriptEventArgs`

一句输入语音的最终转写。

`AssistantTextDelta`

`QwenTextDeltaEventArgs`

应答文本增量。按顺序拼接。

`AssistantTextCompleted`

`QwenTranscriptEventArgs`

完整的应答文本。

`AssistantAudioChunk`

`QwenAudioChunkEventArgs`

应答音频分片，24 kHz 单声道 16 bit 小端裸 PCM。

`AssistantAudioCompleted`

`EventArgs`

本轮应答音频全部下发。

`FunctionCallReceived`

`QwenFunctionCallEventArgs`

模型请求调用工具，提供调用 ID、工具名和 JSON 参数。

`ResponseCompleted`

`QwenResponseSummary`

收到 `response.done`，返回状态和用量。

`RawServerEvent`

`QwenServerEventArgs`

原始服务端事件，可读取事件类型和 JSON 对象。

`ErrorOccurred`

`DashScopeErrorEventArgs`

服务端错误或连接异常。

### 结果对象

类型

属性

说明

`QwenResponseSummary`

`Status: string?, FailureReason: string?, TotalTokens: int?, InputTokens: int?, OutputTokens: int?, AudioInputTokens: int?, AudioOutputTokens: int?`

应答状态、失败原因和用量。`Status` 可为 `completed`、`failed` 或 `incomplete`。对话用量按轮返回，翻译用量为会话累计值。

`QwenSpeechEventArgs`

`AudioMs: long, ItemId: string?`

语音起止在输入流中的毫秒位置和条目 ID。

`QwenTranscriptEventArgs`

`Text: string, ItemId: string?`

当前转写或完整文本及条目 ID。

`QwenTextDeltaEventArgs`

`Delta: string, ItemId: string?`

文本增量及条目 ID。

`QwenAudioChunkEventArgs`

`Pcm: byte[]`

音频分片。

`QwenFunctionCallEventArgs`

`CallId: string, Name: string?, ArgumentsJson: string?`

工具调用 ID、名称与参数。回传结果时使用原始 `CallId`。

`QwenServerEventArgs`

`Type: string?, Root: JsonObject`

事件类型和完整 JSON。

`DashScopeErrorEventArgs`

`Code: int, ServerErrorCode: string?, ServerErrorMessage: string?, TaskId: string?, InnerException: Exception?`

SDK 错误码、服务端错误码和消息、任务或会话 ID，以及底层异常。

### 会话收尾

多轮对话可以复用同一条 WebSocket 连接。在最后一轮的 `ResponseCompleted` 到达后调用 `FinishAsync`，避免截断应答。

收尾模式

行为

`FinishWithoutWait`

发送 `session.finish` 后断开。Audio Realtime 默认使用该模式。

`CloseOnly`

直接关闭连接。Omni Realtime 默认使用该模式。

`FinishAndWait`

发送 `session.finish` 并等待 `session.finished`。服务端也可通过关闭连接结束会话。
