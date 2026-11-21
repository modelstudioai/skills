# C# SDK 接口与事件

Bailian.DashScope SDK 客户端类参考，涵盖语音识别、语音合成、实时语音对话与实时翻译的方法、事件、属性及结果对象。

## FunAsrSpeechTranscriber

### 方法

`ct`（`CancellationToken`，可选）：用于取消本次异步调用。

方法签名

返回值

说明

`StartAsync(CancellationToken ct = default)`

`Task`

建立连接并等待 `task-started`。

`SendAudioAsync(ReadOnlyMemory<byte> pcmFrame, CancellationToken ct = default)`

`Task`

任务启动后发送一帧音频。

`StopAsync(CancellationToken ct = default)`

`Task`

发送 `finish-task`，等待最终结果和 `task-finished`；重复调用复用本次任务结果。

`CancelAsync()`

`Task`

立即关闭连接，可重复调用。

`TranscribePcmStreamAsync(Stream pcm, int frameMilliseconds = 20, CancellationToken ct = default)`

`Task<IReadOnlyList<RecognitionSentence>>`

读取 PCM 流、分帧发送并返回定稿句子；帧长默认 20 毫秒。

`DisposeAsync()`

`ValueTask`

释放客户端资源。

`SendContextAsync(JsonArray context, CancellationToken ct = default)`

`Task`

发送协议格式的上下文数组。

**说明**仅适用于 Qwen-Audio-ASR-Message 系列。

### 事件

事件

类型

说明

`TranscriberStarted`

`EventHandler`

任务已启动。

`SentenceBegin`

`EventHandler<RecognitionSentenceEventArgs>`

句子开始。

`PartialResult`

`EventHandler<RecognitionSentenceEventArgs>`

中间识别结果。

`SentenceEnd`

`EventHandler<RecognitionSentenceEventArgs>`

句子的最终识别结果。

`Completed`

`EventHandler<TranscriptionCompletedEventArgs>`

任务已完成。

`Failed`

`EventHandler<DashScopeErrorEventArgs>`

任务失败或意外断开连接。

### 属性

属性

类型

说明

`TaskId`

`string`

本次识别任务的标识符。

### 结果对象

从 `RawPayload` 的 `usage` 读取模型返回的用量字段。完成事件中可能不包含兼容的时长字段。

#### RecognitionSentenceEventArgs

属性

类型

说明

`Sentence`

`RecognitionSentence`

句子详情。

`RawPayload`

`JsonObject?`

原始响应 JSON。

#### RecognitionSentence

属性

类型

说明

`SentenceId`

`int`

标识符。

`BeginTimeMs`

`long`

开始时间，单位毫秒。

`EndTimeMs`

`long?`

结束时间，单位毫秒；定稿前可能为空。

`Text`

`string`

文本。

`IsBegin`

`bool`

是否标识句子开始。

`IsEnd`

`bool`

是否为句子最终结果。

`ChannelId`

`int`

音轨索引，从 0 开始。

`SpeakerId`

`string?`

说话人标识。

`Words`

`IReadOnlyList<RecognitionWord>`

字词详情。

`StashText`

`string?`

暂存识别文本。

`RequestId`

`string?`

标识符。

#### RecognitionWord

属性

类型

说明

`BeginTimeMs`

`long`

开始时间，单位毫秒。

`EndTimeMs`

`long?`

结束时间，单位毫秒；定稿前可能为空。

`Text`

`string`

文本。

`Punctuation`

`string`

标点。

`Fixed`

`bool?`

字词是否已定稿。

`SpeakerId`

`string?`

说话人标识。

#### TranscriptionCompletedEventArgs

属性

类型

说明

`UsageDurationSeconds`

`float?`

音频时长，单位秒，对应 `usage.duration`。

`RawPayload`

`JsonObject?`

原始响应 JSON。

## CosyVoiceSpeechSynthesizer

### 方法

`ct`（`CancellationToken`，可选）：用于取消本次异步调用。

方法签名

返回值

说明

`StartAsync(CancellationToken ct = default)`

`Task`

建立连接并等待 `task-started`。

`SendTextAsync(string text, CancellationToken ct = default)`

`Task`

任务启动后追加一段文本。

`StopAsync(CancellationToken ct = default)`

`Task`

发送 `finish-task`，等待最终结果和 `task-finished`；重复调用复用本次任务结果。

`CancelSynthesisKeepConnectionAsync(CancellationToken ct = default)`

`Task`

通过 `input.directive=cancel` 取消合成并等待 `task-finished`，不主动关闭连接。

`CancelAsync()`

`Task`

立即关闭连接，可重复调用。

`StreamAudioAsync(IEnumerable<string> segments, TimeSpan? sendInterval = null, CancellationToken ct = default)`

`IAsyncEnumerable<ReadOnlyMemory<byte>>`

发送文本分段并逐片返回音频。`sendInterval=null` 使用 200 毫秒间隔；`TimeSpan.Zero` 不等待。

`SynthesizeAsync(IEnumerable<string> segments, TimeSpan? sendInterval = null, CancellationToken ct = default)`

`Task<byte[]>`

收集 `StreamAudioAsync` 的全部音频并返回字节数组；`sendInterval` 规则相同。

`DisposeAsync()`

`ValueTask`

释放客户端资源。

### 事件

事件

类型

说明

`SynthesisStarted`

`EventHandler`

任务已启动。

`AudioReceived`

`EventHandler<ReadOnlyMemory<byte>>`

按顺序返回的音频字节，依次追加可得到输出文件。

`SentenceProgress`

`EventHandler<SynthesisSentenceEventArgs>`

句子合成进度：开始、合成中、结束。

`SynthesisCompleted`

`EventHandler`

任务已完成。

`Failed`

`EventHandler<DashScopeErrorEventArgs>`

任务失败或意外断开连接。

### 属性

属性

类型

说明

`TaskId`

`string`

本次合成任务的标识符。

`Usage`

`SynthesisUsage?`

任务完成后读取。`SynthesizeAsync` 或 `StopAsync` 返回后，读取 `Characters` 获取本次任务的总字符数；服务端未返回用量时，`Usage` 为 `null`。

**说明**`qwen-audio-3.1-tts-flash` 按 Token 计费；`qwen-audio-3.1-tts-plus` 按字符计费。两者均返回 `InputTokens`、`OutputTokens` 和 `TotalTokens`。

### 结果对象

#### SynthesisSentenceEventArgs

属性

类型

说明

`Phase`

`SynthesisSentencePhase`

`Begin` / `Synthesis` / `End`. 句子合成进度：开始、合成中、结束。

`SentenceIndex`

`int`

标识符。

`OriginalText`

`string?`

原始输入文本。

`NormalizedText`

`string?`

规范化后的合成文本。

`BilledCharacters`

`int?`

服务端返回的 `usage.characters`。

`Words`

`JsonNode?`

字词详情。

## SambertSpeechSynthesizer

### 方法

`ct`（`CancellationToken`，可选）：用于取消本次异步调用。

方法签名

返回值

说明

`StartAsync(string text, CancellationToken ct = default)`

`Task`

一次发送完整文本并等待 `task-started`。

`WaitFinishedAsync(CancellationToken ct = default)`

`Task`

等待服务端自行完成；Sambert 不发送 `finish-task`。

`CancelAsync()`

`Task`

立即关闭连接，可重复调用。

`StreamAudioAsync(string text, CancellationToken ct = default)`

`IAsyncEnumerable<ReadOnlyMemory<byte>>`

一次提交完整文本，逐片返回音频直至完成。

`SynthesizeAsync(string text, CancellationToken ct = default)`

`Task<byte[]>`

一次提交完整文本，返回全部音频字节数组。

`DisposeAsync()`

`ValueTask`

释放客户端资源。

### 事件

事件

类型

说明

`SynthesisStarted`

`EventHandler`

任务已启动。

`AudioReceived`

`EventHandler<ReadOnlyMemory<byte>>`

按顺序返回的音频字节，依次追加可得到输出文件。

`SentenceTimestamps`

`EventHandler<SambertSentenceEventArgs>`

启用后返回字词或音素时间戳。

`SynthesisCompleted`

`EventHandler`

任务已完成。

`Failed`

`EventHandler<DashScopeErrorEventArgs>`

任务失败或意外断开连接。

### 属性

属性

类型

说明

`TaskId`

`string?`

本次合成任务的标识符。

`Usage`

`SynthesisUsage?`

任务完成后读取。`SynthesizeAsync` 或 `WaitFinishedAsync` 返回后，读取 `Characters` 获取本次任务的总字符数；服务端未返回用量时，`Usage` 为 `null`。

### 结果对象

#### SambertSentenceEventArgs

属性

类型

说明

`BeginTimeMs`

`int?`

开始时间，单位毫秒。

`EndTimeMs`

`int?`

结束时间，单位毫秒；定稿前可能为空。

`Words`

`JsonNode?`

字词详情。 同时启用 `PhonemeTimestampEnabled` 和 `WordTimestampEnabled` 后，每个字词元素中可包含 `phonemes` 数组。

`BilledCharacters`

`int?`

服务端返回的 `usage.characters`。

## FunAsrFileTranscriber

属于 `DashScope.Transcription` 命名空间，用于 `Qwen-Audio-ASR-Flash-Filetrans`、`Fun-ASR` 与 `Paraformer` 录音文件识别的异步提交、轮询与结果下载。

### 方法

`ct`（`CancellationToken`，可选）：用于取消本次异步调用。

方法签名

返回值

说明

`SubmitAsync(FileTranscriptionRequest request, CancellationToken ct = default)`

`Task<FileTranscriptionSubmission>`

提交异步转写任务并立即返回 `TaskId`，不等待任务完成。

`QueryAsync(string taskId, CancellationToken ct = default)`

`Task<FileTranscriptionResult>`

单次查询指定任务的状态和子任务列表。

`WaitForCompletionAsync(string taskId, IProgress<FileTranscriptionResult>? status = null, TimeSpan? timeout = null, TimeSpan? pollInterval = null, CancellationToken ct = default)`

`Task<FileTranscriptionResult>`

轮询等待任务到达终态（`Succeeded`、`Failed` 或 `Canceled`），超时抛出异常。

`DownloadTranscriptionAsync(string transcriptionUrl, CancellationToken ct = default)`

`Task<TranscriptionFile>`

下载并解析子任务 `TranscriptionUrl` 指向的转写结果 JSON 文件。

`TranscribeAsync(FileTranscriptionRequest request, IProgress<FileTranscriptionResult>? status = null, CancellationToken ct = default)`

`Task<IReadOnlyList<FileTranscriptionOutput>>`

一站式完成提交、轮询和下载所有成功子任务的结果文件；整体失败或全部子任务失败时抛出异常。

`CancelTaskAsync(string taskId, CancellationToken ct = default)`

`Task`

取消排队中的任务（仅 `Pending` 状态支持取消）。

`Dispose()`

`void`

释放底层 HTTP 客户端资源。

### 结果对象

#### FileTranscriptionSubmission

属性

类型

说明

`RequestId`

`string`

请求 ID。

`TaskId`

`string`

异步任务 ID（24 小时有效）。

`TaskStatus`

`FunAsrTaskStatus`

当前任务状态。

`Raw`

`JsonObject?`

提交响应原文。

#### FileTranscriptionResult

属性

类型

说明

`RequestId`

`string?`

请求 ID。

`TaskId`

`string`

异步任务 ID。

`TaskStatus`

`FunAsrTaskStatus`

任务状态。

`IsTerminal`

`bool`

是否已到达终态（`Succeeded`、`Failed` 或 `Canceled`）。

`Code`

`string?`

整体失败时的错误码。

`Message`

`string?`

整体失败时的错误信息。

`SubmitTime`

`string?`

任务提交时间。

`ScheduledTime`

`string?`

任务开始调度时间。

`EndTime`

`string?`

任务结束时间。

`UsageDurationSeconds`

`long?`

音频用量时长（秒）。

`Results`

`IReadOnlyList<FileTranscriptionSubtask>`

子任务结果列表；整体 `Succeeded` 时仍需检查各子任务的 `SubtaskStatus`。

`Raw`

`JsonObject?`

查询响应原文。

#### FileTranscriptionSubtask

属性

类型

说明

`FileUrl`

`string`

源音频 URL。

`SubtaskStatus`

`FunAsrTaskStatus`

子任务状态。

`TranscriptionUrl`

`string?`

转写结果 JSON 文件的临时下载链接（24 小时有效）。

`Code`

`string?`

子任务失败时的错误码。

`Message`

`string?`

子任务失败时的错误信息。

#### FileTranscriptionOutput

属性

类型

说明

`Subtask`

`FileTranscriptionSubtask`

子任务元信息。

`Transcription`

`TranscriptionFile`

已下载并解析的转写结果文件。

#### TranscriptionFile

属性

类型

说明

`FileUrl`

`string`

源音频 URL。

`Properties`

`TranscriptionAudioProperties?`

源音频属性。

`Transcripts`

`IReadOnlyList<TranscriptChannel>`

各音轨的转写结果列表。

`Raw`

`JsonObject?`

结果文件原文。

#### TranscriptionAudioProperties

属性

类型

说明

`AudioFormat`

`string?`

音频编码格式（如 `pcm_s16le`）。

`Channels`

`IReadOnlyList<int>`

音轨索引列表。

`OriginalSamplingRate`

`int?`

原始采样率（Hz）。

`OriginalDurationMs`

`long?`

原始音频时长（毫秒）。

#### TranscriptChannel

属性

类型

说明

`ChannelId`

`int`

音轨索引。

`ContentDurationMs`

`long`

有效语音内容时长（毫秒）。

`Text`

`string`

整轨拼接文本。

`Sentences`

`IReadOnlyList<TranscriptSentence>`

句级结果列表。

#### TranscriptSentence

属性

类型

说明

`SentenceId`

`int`

句子序号。

`BeginTimeMs`

`long`

起始时间（毫秒）。

`EndTimeMs`

`long`

结束时间（毫秒）。

`Text`

`string`

句子文本。

`SpeakerId`

`int?`

说话人索引（开启说话人分离时返回）。

`Words`

`IReadOnlyList<TranscriptWord>`

词级时间戳列表。

#### TranscriptWord

属性

类型

说明

`BeginTimeMs`

`long`

词起始时间（毫秒）。

`EndTimeMs`

`long`

词结束时间（毫秒）。

`Text`

`string`

词文本。

`Punctuation`

`string`

词后标点。

## FunAsrFlashFileTranscriber

属于 `DashScope.Transcription` 命名空间，用于 `Qwen-Audio-ASR-Flash` 与 `Fun-ASR-Flash` 的同步或 SSE 流式录音文件识别。

### 方法

`ct`（`CancellationToken`，可选）：用于取消本次异步调用。

方法签名

返回值

说明

`TranscribeAsync(FlashTranscriptionRequest request, CancellationToken ct = default)`

`Task<FlashTranscriptionResult>`

单次同步转写，返回完整的最终识别结果。

`TranscribeStreamingAsync(FlashTranscriptionRequest request, CancellationToken ct = default)`

`IAsyncEnumerable<FlashTranscriptionResult>`

以 SSE 流式逐帧返回句子中间结果与最终结果。

`Dispose()`

`void`

释放底层 HTTP 客户端资源。

### 结果对象

#### FlashTranscriptionResult

属性

类型

说明

`RequestId`

`string`

请求 ID。

`Text`

`string`

完整识别文本。

`Sentence`

`FlashSentence`

当前句子结果（流式模式下逐帧更新）。

`UsageDurationSeconds`

`long?`

已处理音频时长（秒）。

`Raw`

`JsonObject?`

响应原文。

#### FlashSentence

属性

类型

说明

`SentenceId`

`int`

句子序号。

`SentenceEnd`

`bool`

是否为该句的最终结果。

`BeginTimeMs`

`long`

句子起始时间（毫秒）。

`EndTimeMs`

`long?`

句子结束时间（毫秒），仅 `SentenceEnd` 为 `true` 时返回。

`Text`

`string`

句子文本。

`ChannelId`

`int`

声道号。

`Words`

`IReadOnlyList<FlashWord>`

词级时间戳列表。

#### FlashWord

属性

类型

说明

`BeginTimeMs`

`long`

词起始时间（毫秒）。

`EndTimeMs`

`long?`

词结束时间（毫秒）。

`Text`

`string`

词文本。

`Punctuation`

`string`

词后标点。

`Fixed`

`bool?`

为 `false` 时表示该词时间戳在后续中间帧中仍可能调整。

## QwenRealtimeConversation

属于 `DashScope.Qwen` 命名空间，用于 `Qwen-Audio-Realtime` 与 `Qwen-Omni-Realtime` 的实时语音对话。

### 方法

`ct`（`CancellationToken`，可选）：用于取消本次异步调用。

方法签名

返回值

说明

`ConnectAsync(CancellationToken ct = default)`

`Task`

建立连接，等待 `session.created`，然后发送 `session.update`。

`AppendAudioAsync(ReadOnlyMemory<byte> pcm, CancellationToken ct = default)`

`Task`

发送一帧 PCM 音频（内部 Base64 编码后发送 `input_audio_buffer.append`）。

`CommitAudioAsync(CancellationToken ct = default)`

`Task`

在 `PushToTalk` 模式下发送 `input_audio_buffer.commit` 提交音频缓冲。

`CreateResponseAsync(JsonObject? responseOptions = null, CancellationToken ct = default)`

`Task`

发送 `response.create` 请求应答；`responseOptions` 可覆盖本轮配置。

`SendItemAsync(JsonObject item, CancellationToken ct = default)`

`Task`

使用 `conversation.item.create` 向会话插入条目。

`SendFunctionCallOutputAsync(string callId, string outputJson, CancellationToken ct = default)`

`Task`

使用原始 `callId` 和 JSON 结果回传工具调用输出。

`SendRawEventAsync(string frameJson, CancellationToken ct = default)`

`Task`

原样发送一条完整的客户端事件 JSON。

`FinishAsync(CancellationToken ct = default)`

`Task`

按实际 `FinishMode` 正常结束会话。

`AbortAsync()`

`Task`

立即关闭连接，放弃在途结果。

`DisposeAsync()`

`ValueTask`

异步释放客户端资源。

### 事件

事件

类型

触发条件

`SessionReady`

`EventHandler<string?>`

会话就绪，参数为 `session.id`。

`UserSpeechStarted`

`EventHandler<QwenSpeechEventArgs>`

服务端 VAD 检测到用户开始说话。

`UserSpeechStopped`

`EventHandler<QwenSpeechEventArgs>`

服务端 VAD 检测到用户停止说话。

`UserTranscriptUpdated`

`EventHandler<QwenTranscriptEventArgs>`

当前输入语音的中间转写文本。

`UserTranscriptCompleted`

`EventHandler<QwenTranscriptEventArgs>`

一句输入语音的最终转写文本。

`AssistantTextDelta`

`EventHandler<QwenTextDeltaEventArgs>`

应答文本增量。

`AssistantTextCompleted`

`EventHandler<QwenTranscriptEventArgs>`

完整的应答文本。

`AssistantAudioChunk`

`EventHandler<QwenAudioChunkEventArgs>`

应答音频分片（24 kHz 单声道 16 bit 小端裸 PCM）。

`AssistantAudioCompleted`

`EventHandler`

本轮应答音频全部下发完成。

`FunctionCallReceived`

`EventHandler<QwenFunctionCallEventArgs>`

模型请求调用工具。

`ResponseCompleted`

`EventHandler<QwenResponseSummary>`

收到 `response.done`，返回状态与用量。

`RawServerEvent`

`EventHandler<QwenServerEventArgs>`

原始服务端事件。

`ErrorOccurred`

`EventHandler<DashScopeErrorEventArgs>`

服务端错误或连接异常。

### 属性

属性

类型

说明

`SessionId`

`string?`

服务端会话 ID。

`FinishMode`

`QwenRealtimeFinishMode`

本次会话实际使用的收尾模式。

### 结果对象

#### QwenResponseSummary

属性

类型

说明

`Status`

`string?`

应答状态，如 `completed`、`failed` 或 `incomplete`。

`FailureReason`

`string?`

失败原因。

`TotalTokens`

`int?`

总 Token 数（对话按轮返回，翻译为会话累计值）。

`InputTokens`

`int?`

输入 Token 数。

`OutputTokens`

`int?`

输出 Token 数。

`AudioInputTokens`

`int?`

音频输入 Token 数。

`AudioOutputTokens`

`int?`

音频输出 Token 数。

#### QwenSpeechEventArgs

属性

类型

说明

`AudioMs`

`long`

语音起止在输入流中的毫秒位置。

`ItemId`

`string?`

条目 ID。

#### QwenTranscriptEventArgs

属性

类型

说明

`Text`

`string`

当前转写或完整文本。

`ItemId`

`string?`

条目 ID。

#### QwenTextDeltaEventArgs

属性

类型

说明

`Delta`

`string`

文本增量片段。

`ItemId`

`string?`

条目 ID。

#### QwenAudioChunkEventArgs

属性

类型

说明

`Pcm`

`byte[]`

音频分片字节。

#### QwenFunctionCallEventArgs

属性

类型

说明

`CallId`

`string`

工具调用 ID，回传结果时需使用原始值。

`Name`

`string?`

工具名称。

`ArgumentsJson`

`string?`

工具参数 JSON 字符串。

#### QwenServerEventArgs

属性

类型

说明

`Type`

`string?`

服务端事件类型。

`Root`

`JsonObject`

完整事件 JSON 对象。

## QwenLiveTranslator

属于 `DashScope.Qwen` 命名空间，用于 `Qwen-LiveTranslate-Realtime` 的实时语音与音视频翻译。

### 方法

`ct`（`CancellationToken`，可选）：用于取消本次异步调用。

方法签名

返回值

说明

`ConnectAsync(CancellationToken ct = default)`

`Task`

建立连接，等待 `session.created`，然后发送 `session.update`。

`AppendAudioAsync(ReadOnlyMemory<byte> pcm, CancellationToken ct = default)`

`Task`

发送一帧 PCM 音频（内部 Base64 编码后发送 `input_audio_buffer.append`）。

`AppendImageAsync(string imageBase64, CancellationToken ct = default)`

`Task`

发送一帧 Base64 图像，对应 `input_image_buffer.append`。

`SendRawEventAsync(string frameJson, CancellationToken ct = default)`

`Task`

原样发送一条完整的客户端事件 JSON。

`FinishAsync(CancellationToken ct = default)`

`Task`

按实际 `FinishMode` 正常结束会话。

`AbortAsync()`

`Task`

立即关闭连接，放弃在途结果。

`DisposeAsync()`

`ValueTask`

异步释放客户端资源。

### 事件

事件

类型

触发条件

`SessionReady`

`EventHandler<string?>`

会话就绪，参数为 `session.id`。

`SourceTranscriptUpdated`

`EventHandler<QwenTranscriptEventArgs>`

源语音的转写更新。

`SourceTranscriptCompleted`

`EventHandler<QwenTranscriptEventArgs>`

一句源语音的最终转写。

`TranslationTextDelta`

`EventHandler<QwenTextDeltaEventArgs>`

译文文本更新。

`TranslationCompleted`

`EventHandler<QwenTranscriptEventArgs>`

本句完整译文。

`TranslatedAudioChunk`

`EventHandler<QwenAudioChunkEventArgs>`

译音分片。

`TranslatedAudioCompleted`

`EventHandler`

本轮译音全部下发完成。

`ResponseCompleted`

`EventHandler<QwenResponseSummary>`

收到 `response.done`，返回状态与会话累计用量。

`RawServerEvent`

`EventHandler<QwenServerEventArgs>`

原始服务端事件。

`ErrorOccurred`

`EventHandler<DashScopeErrorEventArgs>`

服务端错误或连接异常。

### 属性

属性

类型

说明

`SessionId`

`string?`

服务端会话 ID。

`FinishMode`

`QwenRealtimeFinishMode`

本次会话实际使用的收尾模式。

### 结果对象

#### QwenTranscriptEventArgs

属性

类型

说明

`Text`

`string`

在 SDK 1.1.1 中，`SourceTranscriptUpdated` 对 `qwen3.5-livetranslate-flash-realtime` 返回当前转写，对 `qwen3.8-livetranslate-flash-realtime` 可能返回空字符串。`SourceTranscriptCompleted` 返回本句最终转写，`TranslationCompleted` 返回本句完整译文。

`ItemId`

`string?`

条目 ID。

#### QwenTextDeltaEventArgs

属性

类型

说明

`Delta`

`string`

`qwen3.5-livetranslate-flash-realtime` 的中间译文可能重复，不要逐次拼接；完整译文取 `TranslationCompleted.Text`。`qwen3.8-livetranslate-flash-realtime` 的 `response.text.delta` 是文本增量，可按接收顺序拼接。

`ItemId`

`string?`

条目 ID。

#### QwenAudioChunkEventArgs

属性

类型

说明

`Pcm`

`byte[]`

译音的 PCM 字节；采样率以会话配置和服务端实际返回为准。

#### QwenResponseSummary

属性

类型

说明

`Status`

`string?`

应答状态，如 `completed`、`failed` 或 `incomplete`。

`FailureReason`

`string?`

失败原因；正常完成时为 `null`。

`TotalTokens`

`int?`

当前会话累计的 Token 总数。

`InputTokens`

`int?`

输入 Token 数。

`OutputTokens`

`int?`

输出 Token 数。

`AudioInputTokens`

`int?`

音频输入 Token 数。

`AudioOutputTokens`

`int?`

音频输出 Token 数。

#### QwenServerEventArgs

属性

类型

说明

`Type`

`string?`

服务端事件类型。

`Root`

`JsonObject`

完整的服务端事件 JSON 对象。

## 共用类型

### DashScope.DashScopeErrorEventArgs

属性

类型

说明

`Code`

`int`

SDK 错误码

`ServerErrorCode`

`string?`

服务端错误码

`ServerErrorMessage`

`string?`

服务端错误信息

`TaskId`

`string?`

本次任务的 ID

`InnerException`

`Exception?`

引发错误的底层异常

### DashScope.Speech.SynthesisUsage

属性

类型

说明

`InputTokens`

`int?`

输入 Token 数

`OutputTokens`

`int?`

输出 Token 数

`TotalTokens`

`int?`

总 Token 数

`Characters`

`int?`

服务端返回的字符数

### DashScope.Transcription.FunAsrTaskStatus

成员

说明

`Pending`

排队中。

`Running`

处理中。

`Succeeded`

任务成功。

`Failed`

任务失败。

`Canceled`

任务已取消。

`Unknown`

任务不存在或状态未知。

### DashScope.Qwen.QwenTurnDetectionMode

成员

说明

`ServerVad`

由服务端检测语音起止。

`SmartTurn`

语义轮次检测（部分模型支持）。

`PushToTalk`

由客户端调用 `CommitAudioAsync` 和 `CreateResponseAsync` 控制轮次。

### DashScope.QwenRealtimeFinishMode

成员

说明

`FinishWithoutWait`

发送 `session.finish` 后直接断开。

`CloseOnly`

直接关闭连接。

`FinishAndWait`

发送 `session.finish` 并等待 `session.finished`。
