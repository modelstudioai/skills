# SDK简介

安装并配置百炼 C# SDK，按模型系列选择客户端，了解任务收尾、超时和错误处理。

## 开始使用

### 准备工作

-   安装 .NET 8 SDK 或 .NET 10 SDK。
-   [获取 API Key](raw/model-api-reference/preparations/get-api-key.md)，并设置环境变量 `DASHSCOPE_API_KEY`。

**警告**长期 API Key 应保存在服务端，不要写入对外分发的桌面端、移动端或浏览器应用。保护方法请参见[API Key 防泄漏最佳实践](raw/model-user-guide/security-and-compliance/api-key-leak-prevention.md)。

### 安装 SDK

下载并解压 [Bailian.DashScope-1.1.1.zip](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/files/6a4b3c2d1e0f9014.zip)。

NuGet 包名是 `Bailian.DashScope`，程序集是 `DashScope.dll`，根命名空间为 `DashScope`。无需安装原生库或其他 NuGet 依赖。

#### 本地 NuGet 源（推荐）

将解压后的 `packages/` 目录用作本地 NuGet 源。

**说明**以下示例使用 .NET 8。如使用 .NET 10，将命令和路径中的 `net8.0` 替换为 `net10.0`。

```
dotnet new console --framework net8.0 --name SpeechExample
cd SpeechExample
dotnet add package Bailian.DashScope --version 1.1.1 --source "/path/to/Bailian.DashScope-1.1.1/packages"
```

#### 直接引用 DLL

直接引用 DLL 时，按目标框架选择 `sdk/net8.0/DashScope.dll` 或 `sdk/net10.0/DashScope.dll`。将 `DashScope.xml` 放在 DLL 同一目录可在 IDE 中查看接口注释。

```
<ItemGroup>
  <Reference Include="DashScope">
    <HintPath>/path/to/Bailian.DashScope-1.1.1/sdk/net8.0/DashScope.dll</HintPath>
  </Reference>
</ItemGroup>
```

在解压后的包目录中执行以下命令可校验文件完整性：

```
shasum -a 256 -c SHA256SUMS.txt
```

### 配置连接

#### 公共参数

参数

类型

说明

`ApiKey`

`string?`

API Key；未设置时读取 `DASHSCOPE_API_KEY`。

`WorkspaceId`

`string?`

业务空间 ID，通过 `X-DashScope-WorkSpace` 请求头发送。

`Url`

`string`

完整接口地址。

#### 配置接口地址

设置 `WorkspaceId` 只添加业务空间请求头，不会修改接口地址。使用业务空间专属域名时，通过 `Url` 设置完整地址。

实时多模态、实时语音对话和实时音视频翻译通过 WebSocket URL 的 `model` 查询参数传递模型名，SDK 会自动添加。语音识别、语音合成和音频生成通过请求体传递模型名。

能力

URL

实时语音识别 / 实时语音合成 / 音频生成

`wss://WorkspaceId.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference`

实时多模态 / 实时语音对话 / 实时音视频翻译

`wss://WorkspaceId.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`

Qwen-Audio-ASR-Filetrans / Fun-ASR / Paraformer

`https://WorkspaceId.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/asr/transcription`

Qwen-Audio-ASR / Fun-ASR-Flash

`https://WorkspaceId.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

### 验证安装与配置

在解压包的 `demo/DashScope.Cli/` 目录运行以下命令。示例将音频转换为 16 kHz 单声道 PCM，再调用实时语音识别。将 `WorkspaceId` 替换为与 API Key 对应的业务空间 ID。

```
dotnet build -p:TargetFrameworks=net8.0
curl -fL "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav" -o input.wav
ffmpeg -i input.wav -f s16le -ac 1 -ar 16000 input.pcm
dotnet bin/Debug/net8.0/DashScope.Cli.dll asr --audio input.pcm --model qwen-audio-3.1-asr-flash-streaming --url "wss://WorkspaceId.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference"
```

## 适用范围和支持模型

该 SDK 是纯托管的 .NET 客户端，负责向百炼发送音频或文本并接收结果，不提供本地采集、编解码、唤醒、端侧 VAD 或回声消除。

类型

支持模型

C# 客户端

实时多模态

-   **Qwen-Omni-Realtime**：qwen3.8-omni-flash-realtime、qwen3.5-omni-plus-realtime、qwen3.5-omni-plus-realtime-2026-03-15、qwen3.5-omni-flash-realtime、qwen3.5-omni-flash-realtime-2026-03-15、qwen3-omni-flash-realtime-2025-09-15

`QwenRealtimeConversation`

实时语音识别

-   **Qwen-Audio-ASR-Streaming**：qwen-audio-3.1-asr-flash-streaming、qwen-audio-3.0-asr-flash-streaming
-   **Qwen-Audio-ASR-Message**：qwen-audio-3.1-asr-flash-message
-   **Fun-ASR-Realtime**：fun-asr-realtime、fun-asr-flash-8k-realtime、fun-asr-realtime-2026-02-28、fun-asr-flash-8k-realtime-2026-01-28
-   **Paraformer**：paraformer-realtime-v2、paraformer-realtime-8k-v2

`FunAsrSpeechTranscriber`

实时语音合成

-   **Qwen-Audio-TTS**：qwen-audio-3.1-tts-flash、qwen-audio-3.1-tts-plus、qwen-audio-3.0-tts-flash、qwen-audio-3.0-tts-plus
-   **CosyVoice**：cosyvoice-v3.5-plus、cosyvoice-v3.5-flash、cosyvoice-v3-flash、cosyvoice-v3-plus、cosyvoice-v2

`CosyVoiceSpeechSynthesizer`

实时语音合成

-   **Sambert（仅北京地域）**：sambert-beth-v1、sambert-betty-v1、sambert-brian-v1、sambert-cally-v1、sambert-camila-v1、sambert-cindy-v1、sambert-clara-v1、sambert-donna-v1、sambert-eva-v1、sambert-hanna-v1、sambert-indah-v1、sambert-perla-v1、sambert-waan-v1、sambert-zhichu-v1、sambert-zhida-v1、sambert-zhide-v1、sambert-zhifei-v1、sambert-zhigui-v1、sambert-zhihao-v1、sambert-zhijia-v1、sambert-zhijing-v1、sambert-zhilun-v1、sambert-zhimao-v1、sambert-zhimiao-emo-v1、sambert-zhiming-v1、sambert-zhimo-v1、sambert-zhina-v1、sambert-zhinan-v1、sambert-zhiqi-v1、sambert-zhiqian-v1、sambert-zhiru-v1、sambert-zhishu-v1、sambert-zhishuo-v1、sambert-zhistella-v1、sambert-zhiting-v1、sambert-zhiwei-v1、sambert-zhixiang-v1、sambert-zhixiao-v1、sambert-zhiya-v1、sambert-zhiye-v1、sambert-zhiying-v1、sambert-zhiyuan-v1、sambert-zhiyue-v1

`SambertSpeechSynthesizer`

音频生成

-   **Qwen-Audio-TTS-Next**：qwen-audio-3.1-tts-next

`CosyVoiceSpeechSynthesizer`

实时语音对话

-   **Qwen-Audio-Realtime**：qwen-audio-3.1-realtime-plus、qwen-audio-3.1-realtime-flash、qwen-audio-3.0-realtime-plus、qwen-audio-3.0-realtime-flash

`QwenRealtimeConversation`

实时音视频翻译

-   **Qwen-LiveTranslate-Realtime**：qwen3.5-livetranslate-flash-realtime、qwen3.5-livetranslate-flash-realtime-2026-05-19、qwen3.8-livetranslate-flash-realtime

`QwenLiveTranslator`

非实时语音识别（异步）

-   **Qwen-Audio-ASR-Filetrans**：qwen-audio-3.1-asr-flash-filetrans、qwen-audio-3.0-asr-flash-filetrans
-   **Fun-ASR**：fun-asr
-   **Paraformer**：paraformer-v2、paraformer-8k-v2

`FunAsrFileTranscriber`

非实时语音识别（单次请求）

-   **Qwen-Audio-ASR**：qwen-audio-3.1-asr-flash、qwen-audio-3.0-asr-flash
-   **Fun-ASR-Flash**：fun-asr-flash-2026-06-15

`FunAsrFlashFileTranscriber`

在已编译的示例工程目录中运行以下命令，可查看随包示例程序内置的模型清单。

```
dotnet bin/Debug/net8.0/DashScope.Cli.dll models --names-only
```

## 注意事项

### 模型与音色兼容性

多个模型系列共用一个客户端类时，请显式设置 `Model`，否则 SDK 将使用该类的默认模型。SDK 的 `ModelRouting` 方法按名称匹配部分模型系列。确定模型可用的客户端时，请以本页支持模型表为准。

更换合成模型时，同时检查音色是否支持该模型。Qwen-Audio-TTS 和 CosyVoice 共用一个客户端，但音色不能因此通用。选择音色请参见[Qwen-Audio-TTS音色列表](raw/model-user-guide/model-experience/speech-and-audio/speech-synthesis/tts-voice-list/qwen-audio-tts-voice-list.md)和[CosyVoice音色列表](raw/model-user-guide/model-experience/speech-and-audio/speech-synthesis/tts-voice-list/cosyvoice-voice-list.md)。

### 结束或取消调用

#### 实时语音识别

实时识别和双工合成用 `StopAsync()` 等待最终结果。重复调用不会再次触发完成事件。若要丢弃在途结果，调用 `CancelAsync()` 立即断开连接；该方法可重复调用。

在 `StopAsync()` 等待期间取消，正在等待的调用会收到 240069；取消完成后再调用 `StopAsync()` 会收到 240014。未正常结束任务就直接释放，会通过 `Failed` 事件报告 240069。

#### 实时语音对话

对话或翻译应在最后一轮应答结束后调用 `FinishAsync()`，客户端按模型选择 `FinishMode`。

#### 非实时语音识别

异步文件转写中，取消本地等待并不会取消服务端任务；如需取消，须在任务排队时调用 `CancelTaskAsync(taskId)`。

#### Sambert

Sambert 每个实例一次提交完整文本，用 `Model` 选择发音人，没有独立的 `Voice` 参数。调用 `StartAsync(text)` 后用 `WaitFinishedAsync()` 等待服务端结束任务。

## 错误码

调用失败时，等待调用结果可能抛出 `DashScopeException`。实时语音识别和语音合成还可通过 `Failed` 事件接收连接错误。

使用 `ServerErrorCode` 和 `ServerErrorMessage` 排查服务端错误。联系技术支持时，请提供本次调用返回的 `TaskId` 和 `RequestId`（如有）。

错误码

DashScopeErrorCode

说明

240001

`ConfigInvalid`

配置无效。

240002

`IllegalParam`

参数无效或缺少参数。

240014

`StateInvalid`

当前状态不允许该操作。

240051

`UpdateAudioError`

发送音频失败。

240062

`NetworkError`

网络或连接错误。

240069

`SocketClosed`

连接已关闭；根据错误消息区分本地取消或对端关闭。

240070

`AuthFailed`

鉴权失败。

240072

`HttpSendFailed`

HTTP 请求发送失败。

240073

`HttpReceiveFailed`

HTTP 响应体为空。

240074

`HttpResponseInvalid`

响应不是合法 JSON，或缺少必需字段。

240075

`HttpServerError`

服务端返回错误，查看服务端错误字段。

240080

`ServerError`

服务端返回 `task-failed`，请查看 `ServerErrorCode`。

240091

`ConnectionTimeout`

建立连接的超时。

240092

`StartTimeout`

等待任务启动事件的超时。

240093

`StopTimeout`

等待任务完成的超时。
