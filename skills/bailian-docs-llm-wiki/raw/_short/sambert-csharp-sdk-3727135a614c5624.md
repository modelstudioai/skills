# Sambert C# SDK 接入

通过 C# SDK 调用 Sambert 合成语音并接收音频分片。

<a id="快速开始"></a>

<a id="quick-start"></a>

## 快速开始

<a id="installation"></a>

按[SDK简介](https://help.aliyun.com/zh/model-studio/csharp-sdk)安装 SDK 并配置 API Key。将示例地址中的 `WorkspaceId` 替换为同地域的业务空间 ID。

Sambert 仅支持北京地域。用 `sambert-zhichu-v1` 合成一句话，将音频保存为 `output.wav`。

<a id="code-block"></a>

```csharp
using DashScope.Speech;

await using var client = new SambertSpeechSynthesizer(new SambertSynthesizerOptions
{
    Model = "sambert-zhichu-v1",
    Url = "wss://WorkspaceId.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference",
    Format = "wav",
    SampleRate = 16000,
});

var audio = await client.SynthesizeAsync("今天下午三点开会。");
await File.WriteAllBytesAsync("output.wav", audio);
```

<a id="调用步骤"></a>

<a id="workflow"></a>

## 调用步骤

1.  创建 `SambertSpeechSynthesizer` 实例（通过 `Model` 指定发音人，无需单独设置 `Voice`），并按需订阅 `SentenceTimestamps` 等事件。
2.  调用 `SynthesizeAsync` 一次提交完整文本并获取全部音频字节。
3.  如需边接收边播放，改用 `StreamAudioAsync` 逐条读取音频分片。
4.  如需字级时间戳，开启 `WordTimestampEnabled`；如需音素级时间戳，同时开启 `PhonemeTimestampEnabled`，并在 `SentenceTimestamps` 事件中接收。
5.  音频下发完成后由服务端触发 `SynthesisCompleted`；不再使用时调用 `DisposeAsync` 释放连接。

<a id="参数说明"></a>

<a id="options"></a>

## 参数说明

<a id="api-reference"></a>

创建 `SambertSpeechSynthesizer` 时传入 `SambertSynthesizerOptions`。`WordTimestampEnabled` 和 `PhonemeTimestampEnabled` 为 `null` 时，SDK 仍会将其作为 `false` 发送。 Sambert 每个实例一次提交完整文本，用 `Model` 选择发音人，没有独立的 `Voice` 参数。

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `Model` | `string` | `sambert-zhichu-v1` | 模型 ID；显式指定本系列模型。 |
| `Format` | `string` | `wav` | 音频格式。 |
| `SampleRate` | `int` | `16000` | 音频采样率，单位 Hz。 |
| `Volume` | `int?` | `null` | 音量，取值 0 至 100。 |
| `Rate` | `double?` | `null` | 语速倍率。 |
| `Pitch` | `double?` | `null` | 语调倍率。 |
| `WordTimestampEnabled` | `bool?` | `null` | 是否返回字词级时间戳。 |
| `PhonemeTimestampEnabled` | `bool?` | `null` | 是否返回音素时间戳；需同时设置 `WordTimestampEnabled=true`。 |
| `ExtraParametersJson` | `string?` | `null` | JSON 对象字符串，合并到协议的 `parameters` 对象。 |
