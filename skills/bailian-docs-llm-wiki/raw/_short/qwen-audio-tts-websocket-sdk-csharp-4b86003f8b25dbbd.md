# Qwen-Audio-TTS C# SDK

## 快速开始

按[SDK简介](raw/model-api-reference/realtime-api-directory/realtime-websocket-sdk/realtime-websocket-csharp-sdk/csharp-sdk.md)安装 SDK 并配置 API Key。将示例地址中的 `WorkspaceId` 替换为同地域的业务空间 ID。

用 `longanfengyue_v3.1` 音色分段合成两句话，将收到的音频依次写入 `output.wav`。运行后即可播放该文件。

```
using DashScope.Speech;

await using var client = new CosyVoiceSpeechSynthesizer(new CosyVoiceSynthesizerOptions
{
    Model = "qwen-audio-3.1-tts-flash",
    Voice = "longanfengyue_v3.1",
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

## 详细参考

-   [请求参数](https://help.aliyun.com/zh/model-studio/qwen-audio-tts-csharp-sdk#options)
-   [接口参考](https://help.aliyun.com/zh/model-studio/qwen-audio-tts-csharp-sdk#workflow)
