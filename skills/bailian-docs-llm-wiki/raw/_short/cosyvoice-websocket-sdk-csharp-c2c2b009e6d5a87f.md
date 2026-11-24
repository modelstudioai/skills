# CosyVoice C# SDK

## 快速开始

按[SDK简介](https://help.aliyun.com/zh/model-studio/csharp-sdk)安装 SDK 并配置 API Key。将示例地址中的 `WorkspaceId` 替换为同地域的业务空间 ID。

用 `longanhuan_v3` 音色分段合成两句话，将收到的音频依次写入 `output.wav`。运行后即可播放该文件。

```
using DashScope.Speech;

await using var client = new CosyVoiceSpeechSynthesizer(new CosyVoiceSynthesizerOptions
{
    Model = "cosyvoice-v3-flash",
    Voice = "longanhuan_v3",
    Url = "wss://WorkspaceId.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference",
    Format = "wav",
    SampleRate = 16000,
});

using var output = File.Create("output.wav");
await foreach (var chunk in client.StreamAudioAsync(["今天下午三点开会。", "请提前入场。"]))
{
    await output.WriteAsync(chunk);
}
```

## 调用步骤

1.  创建 `CosyVoiceSpeechSynthesizer` 实例，选择与模型匹配的音色和输出格式，并按需订阅 `AudioReceived`、`SentenceProgress` 等事件。
2.  使用 `SendTextAsync` 时，调用 `StartAsync` 建立连接并发送 `run-task`。
3.  调用 `SendTextAsync` 分段发送文本；若已有完整分段文本，也可直接调用 `StreamAudioAsync` 或 `SynthesizeAsync`，无需先调用 `StartAsync`。
4.  在 `AudioReceived` 中接收音频分片，在 `SentenceProgress` 中获取句级进度与时间戳（使用 `StreamAudioAsync` 时直接按顺序读取返回的音频分片）。
5.  使用 `SendTextAsync` 时，文本发送完毕后调用 `StopAsync`，等待 `task-finished`（即 `SynthesisCompleted`）。
6.  如需中断当前合成任务但保留连接，可调用 `CancelSynthesisKeepConnectionAsync`；不再使用时调用 `DisposeAsync` 释放连接。

## 参数说明

创建 `CosyVoiceSpeechSynthesizer` 时传入 `CosyVoiceSynthesizerOptions`。`EnableSsml`、`WordTimestampEnabled`、`EnableAigcTag` 和 `EnableMarkdownFilter` 为 `null` 时，SDK 仍会将其作为 `false` 发送。

参数

类型

默认值

说明

`Model`

`string`

`qwen-audio-3.1-tts-flash`

模型 ID；显式指定本系列模型。

`Voice`

`string`

`longanfengyue_v3.1`

与所选模型匹配的音色 ID，参见 [Qwen-Audio-TTS 可用音色](raw/model-user-guide/model-experience/speech-and-audio/speech-synthesis/tts-voice-list/qwen-audio-tts-voice-list.md)或 [CosyVoice 可用音色](raw/model-user-guide/model-experience/speech-and-audio/speech-synthesis/tts-voice-list/cosyvoice-voice-list.md)。

`Format`

`string`

`pcm`

音频格式。

`SampleRate`

`int`

`22050`

音频采样率，单位 Hz。

`Volume`

`int?`

`null`

音量，取值 0 至 100。

`Rate`

`double?`

`null`

语速倍率。

`Pitch`

`double?`

`null`

语调倍率。

`BitRate`

`int?`

`null`

输出码率，取值 `6` 至 `510` kbps，仅在 `Format` 为 `opus` 或 `mp3` 时生效。

`Seed`

`int?`

`null`

随机种子。

`EnableSsml`

`bool?`

`null`

是否开启 SSML 解析。

**说明**通过一次 `continue-task` 发送完整的 SSML 文本；使用 `SynthesizeAsync` 时只传入一个文本分段。音频可流式接收。

`WordTimestampEnabled`

`bool?`

`null`

是否返回字词级时间戳。

`LanguageHints`

`IList<string>?`

`null`

在 `qwen-audio-3.1-tts-flash` 的多语种或方言音色上，设置方法见 [Qwen-Audio-TTS](raw/model-user-guide/model-experience/speech-and-audio/speech-synthesis/tts-voice-list/qwen-audio-tts-voice-list.md)。CosyVoice 用此字段指定合成目标语言，只处理第一个值，取值见 [CosyVoice · 客户端事件](raw/_short/cosyvoice-client-events-480a8821d2d60e18.md)。

`Instruction`

`string?`

`null`

音色指令。

`EnableAigcTag`

`bool?`

`null`

是否嵌入 AIGC 隐性标识（`wav`、`mp3`、`opus` 格式生效）。

**说明**在 CosyVoice 系列中，仅 `cosyvoice-v3-flash`、`cosyvoice-v3-plus`、`cosyvoice-v2` 支持此参数。

`AigcPropagator`

`string?`

`null`

AIGC 内容传播者标识。

**说明**仅在 `EnableAigcTag` 为 `true` 时下发；在 CosyVoice 系列中，仅 `cosyvoice-v3-flash`、`cosyvoice-v3-plus`、`cosyvoice-v2` 支持。

`AigcPropagateId`

`string?`

`null`

AIGC 内容传播行为标识。

**说明**仅在 `EnableAigcTag` 为 `true` 时下发；在 CosyVoice 系列中，仅 `cosyvoice-v3-flash`、`cosyvoice-v3-plus`、`cosyvoice-v2` 支持。

`HotFixJson`

`string?`

`null`

文本热修复配置，传入包含 `pronunciation` 和 `replace` 规则的 JSON 对象字符串。

**说明**仅 Qwen-Audio-TTS 支持此参数。

`ExtraParametersJson`

`string?`

`null`

JSON 对象字符串，合并到协议的 `parameters` 对象。

`EnableMarkdownFilter`

`bool?`

`null`

是否过滤输入中的 Markdown 标记。

**说明**`cosyvoice-v2` 不支持此参数。
