# Qwen-Audio-TTS Flutter SDK

使用 CosyVoice 时，请参见 [CosyVoice Flutter SDK](raw/_short/cosyvoice-websocket-sdk-flutter-14e4f441e1c1f2d6.md)。

Qwen-Audio-TTS 和 CosyVoice 共用双向流式接口。Flutter 应用可以分次发送文本，并在合成期间接收音频。

## 前提条件

-   为目标平台配置 Flutter 开发环境。示例工程要求 Dart 3.4 及以上、低于 4.0。
-   [获取 API Key](raw/model-api-reference/preparations/get-api-key.md)。请选择与 API Key 同地域的服务地址。使用工作空间专属域名时，还需获取[业务空间 ID](raw/model-user-guide/get-started-with-models/regions.md)。

移动端应用请勿硬编码长期 API Key。调用支持临时 API Key 的模型时，由应用服务端[生成临时 API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)并下发给客户端。

### 安装 SDK

打开[移动端语音 SDK 选型与下载](https://help.aliyun.com/zh/model-studio/sdk-selection-and-download)，在 **Flutter** 标签下下载安装包并解压。

将解压后的 SDK 目录复制到 Flutter 项目的 `packages/aliyun_neonui`，在 `pubspec.yaml` 中添加本地依赖。

```
dependencies:
  aliyun_neonui:
    path: packages/aliyun_neonui
```

运行 `flutter pub get`，然后在 Dart 文件中导入 SDK。

```
import 'package:aliyun_neonui/neonui.dart';
```

## 快速开始

### 运行示例

1.  连接目标设备，在解压后的 SDK 目录中运行以下命令。
    
    ```
    cd example
    flutter pub get
    flutter run
    ```
    
2.  打开示例应用首页的 **百炼(DashScope)**，选择服务地址并填写 **API Key**。使用工作空间专属域名时，同时填写 **WorkspaceId**。
    
3.  打开 **Qwen-Audio-TTS/CosyVoice 双向流式语音合成** 并运行示例。
    

完整示例见整合包中的 `example/lib/pages/dashscope/dash_cosy_voice_stream_tts_page.dart`。

在示例中使用模型 `qwen-audio-3.0-tts-flash`。

### 包内示例提供的模型

-   `qwen-audio-3.1-tts-flash`
-   `qwen-audio-3.1-tts-plus`
-   `qwen-audio-3.0-tts-flash`
-   `qwen-audio-3.0-tts-plus`
-   `cosyvoice-v3-flash`
-   `cosyvoice-v3-plus`

### 调用步骤

下面的方法通过 `NativeNui()` 获取的实例调用。

1.  先订阅 `streamTtsEventStream` 和 `streamTtsAudioStream`，再调用以下方法。
    
2.  下面用请求参数中的连接 JSON 和任务 JSON 分别作为 `ticketJson` 和 `paramsJson`。
    
    ```
    await nui.streamTtsStart(ticket: ticketJson, params: paramsJson);
    await nui.streamTtsSend('你好，');
    await nui.streamTtsSend('欢迎使用语音合成。');
    ```
    
    开始合成后分次发送文本，通过音频流接收并播放返回音频。
    
3.  用 `streamTtsStop` 结束文本输入。收到合成完成事件后调用 `streamTtsRelease`。
    

## 请求参数

下例使用包内示例的一个模型。需要调整其他字段时，可参考同一整合包的 `example/lib/dashscope_params.dart`。更多参数说明见[Android SDK](raw/_short/qwen-audio-tts-websocket-sdk-android-deab75c7b0d9709a.md)、[iOS SDK](raw/_short/qwen-audio-tts-websocket-sdk-ios-20133baf35bd9806.md)、[HarmonyOS SDK](raw/_short/qwen-audio-tts-websocket-sdk-harmonyos-3937eb409e9f327d.md)。

将 `YOUR_WS_HOST` 替换为相应地域的 WebSocket 主机名，`YOUR_DEVICE_ID` 替换为设备标识，并按所选地域设置 `YOUR_API_KEY`。

### 连接参数

将连接参数作为 `ticket` 传入。

```
{
  "apikey": "YOUR_API_KEY",
  "device_id": "YOUR_DEVICE_ID",
  "url": "wss://YOUR_WS_HOST/api-ws/v1/inference"
}
```

### 任务参数

示例中的 JSON 作为字符串传入 Dart 方法。

```
{
  "model": "qwen-audio-3.1-tts-flash",
  "voice": "longanhuan_v3.1",
  "format": "pcm",
  "enable_audio_decoder": false,
  "sample_rate": 24000,
  "volume": 50,
  "rate": 1.0,
  "pitch": 1.0
}
```

`model` 和 `voice` 必须匹配。`format`、`sample_rate` 定义音频输出格式和采样率。示例选择 MP3 或 Opus 时会启用 `enable_audio_decoder`。

## 接口参考

### 方法

返回 `Future<int>` 的方法中，结果码 `0` 表示成功。

方法签名

用途

`Future<int> streamTtsStart({required String ticket, required String params, String sessionId = "", int logLevel = 0, bool saveLog = false})`

创建流式合成会话，传入票据 `ticket` 和参数 `params` 两段 JSON 字符串。

`Future<int> streamTtsSend(String text)`

继续发送一段文本。

`Future<int> streamTtsStop({bool flagAsync = true})`

结束文本输入。`flagAsync` 默认为 `true`，使用异步停止。

`Future<int> streamTtsAsyncPlay({required String ticket, required String params, required String text, String sessionId = "", int logLevel = 0, bool saveLog = false})`

一次提交完整文本，异步接收合成结果。

`Future<int> streamTtsCancel()`

取消当前会话或合成。

`Future<int> streamTtsRelease()`

释放 SDK 资源。

### 事件与音频流

事件从 `streamTtsEventStream` 读取。收到 Dart Map 时，以 `event` 识别事件名，任务类事件的 `resultCode` 可用于判断错误。

音频流 `streamTtsAudioStream` 返回音频分片。应用负责播放音频。

事件

用途

`STREAM_INPUT_TTS_EVENT_SYNTHESIS_STARTED`

合成或回复音频开始

`STREAM_INPUT_TTS_EVENT_SENTENCE_SYNTHESIS`

句级合成事件

`STREAM_INPUT_TTS_EVENT_SYNTHESIS_COMPLETE`

任务或当前音频输出完成

`STREAM_INPUT_TTS_EVENT_TASK_FAILED`

任务失败
