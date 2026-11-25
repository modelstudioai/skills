# Qwen-Omni-Realtime C# SDK

使用 C# SDK 通过 WebSocket 调用 Qwen-Omni-Realtime。本页示例以音频为输入，返回文本和音频。

<a id="前提条件"></a>

## 前提条件

[获取 API Key](../model-api-reference/preparations/get-api-key.md)，并设置环境变量 `DASHSCOPE_API_KEY`。

<a id="安装-sdk"></a>

### 安装 SDK

下载 [Bailian.DashScope-1.1.0.zip](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9000.zip) 并解压。在 C# 项目中使用时，从[本地 NuGet 源安装 SDK](qwen-audio-realtime-csharp-sdk-7c78b8d6a3bc97a4.md#install-sdk)。

<a id="快速开始"></a>

## 快速开始

1.  创建 .NET 10 控制台项目，安装 SDK，将[完整 C# 示例](qwen-audio-realtime-csharp-sdk-7c78b8d6a3bc97a4.md#csharp-example)复制到 `Program.cs`。
2.  将 `input.pcm` 放到项目目录。使用 16 kHz、单声道、16 bit 小端裸 PCM。若源文件为 WAV，先转为裸 PCM。

`qwen3.8-omni-flash-realtime` 使用业务空间专属域名。将以下命令中的 `WorkspaceId` 替换为 API Key 对应的业务空间 ID。这里以华北2（北京）为例，接入地址见 [WebSocket 接入](../model-api-reference/realtime-api-directory/omni-realtime-api-directory/omni-realtime-websocket-access.md)。示例的输出音色为 `Tina`。

<a id="code-block"></a>

```bash
export DASHSCOPE_REALTIME_URL="wss://WorkspaceId.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime"
dotnet run -- input.pcm qwen3.8-omni-flash-realtime Tina
```

终端显示应答文本，应答音频写入 `output.pcm`。

<a id="接口参考"></a>

<a id="模型配置与会话收尾"></a>

## 接口参考

选项、方法和事件见 [C# SDK API 参考](qwen-audio-realtime-csharp-sdk-7c78b8d6a3bc97a4.md#realtime-conversation-api)。在最后一轮 `ResponseCompleted` 后调用 `FinishAsync`。SDK 为 Omni Realtime 选择 `CloseOnly`，关闭连接即结束会话。

如需发送图片帧，可用 `SendRawEventAsync` 发送完整事件。配置、输入格式及发送顺序见 [Omni Realtime WebSocket 接入](../model-api-reference/realtime-api-directory/omni-realtime-api-directory/omni-realtime-websocket-access.md)。
