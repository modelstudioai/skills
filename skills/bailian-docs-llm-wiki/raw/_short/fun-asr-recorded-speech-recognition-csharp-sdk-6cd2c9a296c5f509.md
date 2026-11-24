# Fun-ASR C# SDK

通过 C# SDK 调用 Fun-ASR 转写音频文件并获取识别结果。

## 快速开始

按[SDK简介](https://help.aliyun.com/zh/model-studio/csharp-sdk)安装 SDK 并配置 API Key。将示例地址中的 `WorkspaceId` 替换为同地域的业务空间 ID。

以下示例使用 `fun-asr` 转写音频文件，并在控制台输出文本。

```
using DashScope.Transcription;

using var client = new FunAsrFileTranscriber(new FileTranscriberOptions
{
    Url = "https://WorkspaceId.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/asr/transcription",
});

var request = new FileTranscriptionRequest
{
    Model = "fun-asr",
    FileUrls = ["https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav"],
};
var results = await client.TranscribeAsync(request);
foreach (var result in results)
    foreach (var channel in result.Transcription.Transcripts)
        Console.WriteLine(channel.Text);
```

## 调用步骤

快速开始中的 `TranscribeAsync` 会提交任务、等待完成并下载结果。如需先取得任务 ID，可分步调用：

1.  创建 `FunAsrFileTranscriber`，将 `FileTranscriberOptions.Url` 设为业务空间的转写接口地址。
2.  创建 `FileTranscriptionRequest`，将 `Model` 设为 `fun-asr`。在 `FileUrls` 中传入一个可公开访问的 HTTP(S) 音频地址，每次请求仅支持一个地址。
3.  调用 `SubmitAsync` 提交请求，保存返回的 `TaskId`。
4.  用 `WaitForCompletionAsync` 等待任务结束，或用 `QueryAsync` 查询一次状态。
5.  逐个检查 `Results` 中的 `SubtaskStatus`。对于成功的子任务，用 `DownloadTranscriptionAsync` 下载 `TranscriptionUrl` 指向的结果，并从 `Transcripts` 读取文本。

方法和结果对象见[接口与事件](https://help.aliyun.com/zh/model-studio/csharp-sdk-methods-and-events#fun-asr-file-transcriber)。

## 参数说明

下表列出本系列支持的 `FileTranscriptionRequest` 请求属性。默认值指 SDK 属性的初始值。协议字段见 [HTTP API](raw/_short/fun-asr-recorded-speech-recognition-http-api-0e04e08da4894bf2.md)。

参数

类型

默认值

说明

`Model`

`string`

`qwen-audio-3.1-asr-flash-filetrans`

模型 ID。

**说明**调用本系列时须显式指定模型 ID，例如 `fun-asr`；不设置时使用表中的 SDK 默认值。

`FileUrls`

`IList<string>`

`[]`

必填。待转写音频的公网 HTTP(S) URL 列表。

**说明**每次请求只支持一个 URL。

`VocabularyId`

`string?`

`null`

预编译热词表 ID，可跨请求复用。

**说明**地域支持范围见[支持的模型与地域](https://help.aliyun.com/zh/model-studio/improve-asr-accuracy#supported-models)。

`Vocabulary`

`IDictionary<string, int>?`

`null`

即时热词，以热词文本为键、整数权重为值。

**说明**权重取 1～5。地域支持范围见[支持的模型与地域](https://help.aliyun.com/zh/model-studio/improve-asr-accuracy#supported-models)。

`ChannelId`

`IList<int>?`

`null`

要识别的音轨索引，从 0 开始。未指定时处理第一个音轨。

**说明**每个选中的音轨独立计费。

`SpecialWordFilter`

`string?`

`null`

敏感词过滤规则。传入 JSON 字符串，可将匹配的词替换为等长的星号或将其移除。

`DiarizationEnabled`

`bool?`

`null`

是否启用说话人分离，默认关闭。

**说明**仅支持单声道音频。启用时，建议音频时长不超过 2 小时。

`SpeakerCount`

`int?`

`null`

说话人数量提示。不设置时自动判断。

**说明**仅在 `DiarizationEnabled` 为 `true` 时生效。取值为 2～100 的整数，实际识别人数可能不同。

`LanguageHints`

`IList<string>?`

`null`

识别语种提示，例如 `["zh"]`。

**说明**传入多个值时，仅第一个生效。

`ExtraParametersJson`

`string?`

`null`

以 JSON 对象字符串传入附加参数。SDK 将其中的字段合并到请求的 `parameters` 对象，仅可传入模型支持的协议字段。
