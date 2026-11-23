# Qwen-Audio-Realtime Flutter SDK

Qwen-Audio-Realtime 的 Flutter SDK 接入指南，包含 Dart 调用流程、请求参数和事件。

Qwen-Audio-Realtime 接收实时音频并返回模型回复。应用可根据配置接收回复文本和语音。

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
    
3.  打开 **Qwen-Audio 实时语音对话** 并运行示例。
    
    运行收音示例时，请允许应用使用麦克风。
    

完整示例见整合包中的 `example/lib/pages/dashscope/dash_qwen_audio_chat_page.dart`。

### 包内示例提供的模型

-   `qwen-audio-3.1-realtime-plus`
-   `qwen-audio-3.0-realtime-plus`
-   `qwen-audio-3.0-realtime-flash`

### 调用步骤

下面的方法通过 `NativeNui()` 获取的实例调用。

下文的 `initJson` 和 `sessionJson` 分别使用「请求参数」中的连接 JSON 和任务 JSON。每次调用成功后再执行下一步。

1.  先订阅 `eventStream` 和 `ttsAudioStream`，再调用以下方法。
    
2.  设置连接和任务参数后开始会话。
    
    ```
    await nui.nuiInitialize(params: initJson);
    await nui.dialogSetParams(sessionJson);
    await nui.dialogStart(vadMode: VadMode.p2t.code, dialogParams: sessionJson);
    ```
    
3.  会话启动成功后采集音频，通过 `sendAudio` 持续发送 PCM 数据。包内录音示例采集 16 kHz、16 位、单声道 PCM。
    
    在 iOS 上，先启动麦克风，再启动播放器。如果播放器已启动，请在麦克风启动后重启播放器，以免回复语音无声。
    
4.  停止采集后调用 `dialogStop`。处理完最后的事件后调用 `nuiRelease` 并取消订阅。
    

## 请求参数

下例使用包内示例的一个模型。需要调整其他字段时，可参考同一整合包的 `example/lib/dashscope_params.dart`。更多参数说明见[Android SDK](raw/_short/android-sdk-for-qwen-audio-realtime-service-fbe978d80b5ee150.md)、[iOS SDK](raw/_short/ios-sdk-for-qwen-audio-realtime-service-11c3579f6cded913.md)、[HarmonyOS SDK](raw/_short/harmonyos-sdk-for-qwen-audio-realtime-service-c258297df757a167.md)。

将 `YOUR_WS_HOST` 替换为相应地域的 WebSocket 主机名，`YOUR_DEVICE_ID` 替换为设备标识，并按所选地域设置 `YOUR_API_KEY`。

### 连接参数

示例中的 JSON 作为字符串传入 Dart 方法。

```
{
  "device_id": "YOUR_DEVICE_ID",
  "url": "wss://YOUR_WS_HOST/api-ws/v1/realtime?model=qwen-audio-3.1-realtime-plus",
  "service_mode": "1",
  "audio_update_manually": "false"
}
```

### 任务参数

示例中的 JSON 作为字符串传入 Dart 方法。

```
{
  "apikey": "YOUR_API_KEY",
  "nls_config": {
    "model": "qwen-audio-3.1-realtime-plus",
    "sr_format": "pcm",
    "modalities": "[\"text\",\"audio\"]",
    "voice": "longanqian_v3.1",
    "turn_detection": "{\"type\":\"server_vad\",\"threshold\":0.5,\"silence_duration_ms\":800}"
  },
  "service_type": 4
}
```

URL 查询参数中的 `model` 与 `nls_config.model` 使用同一模型 ID。`modalities` 和 `turn_detection` 在这个 Dart SDK 的请求中是 JSON 字符串。

## 接口参考

### 方法

返回 `Future<int>` 的方法中，结果码 `0` 表示成功。音频发送方法 `sendAudio` 的返回类型为 `Future<Object?>`。

方法签名

用途

`Future<int> nuiInitialize({required String params, int logLevel = 0, bool saveLog = false})`

初始化 SDK。`params` 为连接参数 JSON 字符串。

`Future<int> dialogSetParams(String params)`

设置当前会话的 JSON 参数。

`Future<int> dialogStart({required int vadMode, String dialogParams = "{}"})`

开始会话。`vadMode` 指定断句模式，`dialogParams` 可传入本次会话要使用的 JSON 参数。

`Future<Object?> sendAudio(Uint8List data)`

发送一段 PCM 音频。

`Future<int> dialogStop()`

结束当前采集会话并保留连接。

`Future<int> dialogCancel()`

取消当前会话或合成。

`Future<int> nuiRelease()`

释放 SDK 资源。

`Future<int> dialogAction(String actionParams)`

向会话提交工具调用结果。

### 事件与音频流

事件从 `eventStream` 读取。收到 Dart Map 时，以 `event` 识别事件名，任务类事件的 `resultCode` 可用于判断错误。

音频流 `ttsAudioStream` 返回音频分片。应用负责播放音频。

事件

用途

`EVENT_ASR_PARTIAL_RESULT`

临时识别结果

`EVENT_SENTENCE_END`

当前句的最终识别结果

`EVENT_AUDIO_TRANSCRIPTION_COMPLETED`

语音回复的文本转写完成

`EVENT_ASR_TTS_START`

合成或回复音频开始

`EVENT_ASR_TTS_COMPLETE`

任务或当前音频输出完成

`EVENT_ASR_ERROR`

任务失败
