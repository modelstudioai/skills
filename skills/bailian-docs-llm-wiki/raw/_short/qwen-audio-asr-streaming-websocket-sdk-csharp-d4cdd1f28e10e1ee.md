# Qwen-Audio-ASR-Streaming C# SDK

## 快速开始

按[SDK简介](raw/model-api-reference/realtime-api-directory/realtime-websocket-sdk/realtime-websocket-csharp-sdk/csharp-sdk.md)安装 SDK 并配置 API Key。将示例地址中的 `WorkspaceId` 替换为同地域的业务空间 ID。

将[示例音频](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/audios/6a4b3c2d1e0f9093.wav)保存为 `asr_example.wav`。示例分块读取文件，模拟实时输入，无需麦克风。

识别音频，在控制台打印中间结果和每句话的最终文本。

```
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

## 详细参考

-   [请求参数](https://help.aliyun.com/zh/model-studio/qwen-audio-asr-streaming-csharp-sdk#options)
-   [接口参考](https://help.aliyun.com/zh/model-studio/qwen-audio-asr-streaming-csharp-sdk#workflow)
