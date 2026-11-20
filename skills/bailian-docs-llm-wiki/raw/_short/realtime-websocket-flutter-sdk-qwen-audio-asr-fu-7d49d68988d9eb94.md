# Qwen-Audio-ASR / Fun-ASR Flutter SDK

Qwen-Audio-ASR / Fun-ASR 的 Flutter SDK 接入指南，包含 Dart 调用流程、请求参数和事件。

实时识别输出转写文字。Qwen-Audio-ASR-Message、Qwen-Audio-ASR-Streaming 和 Fun-ASR 共用会话和收音接口，模型通过 `nls_config.model` 切换。

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
    
3.  打开 **Qwen-Audio-3.x-ASR-Flash-Message/Qwen-Audio-3.x-ASR-Flash-Streaming/Fun-ASR-Realtime 实时语音识别** 并运行示例。
    
    运行收音示例时，请允许应用使用麦克风。
    

完整示例见整合包中的 `example/lib/pages/dashscope/dash_fun_asr_speech_transcriber_page.dart`。

### 包内示例提供的模型

包内示例固定采集 16 kHz 音频。直接运行示例时请选择支持 16 kHz 的模型。使用 `fun-asr-flash-8k-realtime` 时，将 `example/lib/audio_input.dart` 中的录音采样率改为 8 kHz，并将请求参数 `nls_config.sample_rate` 设为 `8000`。

-   `qwen-audio-3.1-asr-flash-message`
-   `qwen-audio-3.1-asr-flash-streaming`
-   `qwen-audio-3.0-asr-flash-streaming`
-   `fun-asr-realtime`
-   `fun-asr-flash-8k-realtime`

### 调用步骤

下面的方法通过 `NativeNui()` 获取的实例调用。

下文的 `initJson` 和 `sessionJson` 分别使用「请求参数」中的连接 JSON 和任务 JSON。每次调用成功后再执行下一步。

1.  先订阅 `eventStream`，再调用以下方法。
    
2.  设置连接和任务参数后开始会话。
    
    ```
    await nui.nuiInitialize(params: initJson);
    await nui.dialogSetParams(sessionJson);
    await nui.dialogStart(vadMode: VadMode.p2t.code, dialogParams: sessionJson);
    ```
    
3.  会话启动成功后采集音频，通过 `sendAudio` 持续发送 PCM 数据。
    
4.  停止采集后调用 `dialogStop`。处理完最后的事件后调用 `nuiRelease` 并取消订阅。
    

## 请求参数

下例使用包内示例的一个模型。需要调整其他字段时，可参考同一整合包的 `example/lib/dashscope_params.dart`。更多参数说明见[Android SDK](raw/_short/realtime-websocket-android-sdk-qwen-audio-asr-fu-2d2d0b5882d75de2.md)、[iOS SDK](raw/_short/realtime-websocket-ios-sdk-qwen-audio-asr-fun-as-cd3e96089443ba08.md)、[HarmonyOS SDK](raw/_short/realtime-websocket-harmonyos-sdk-qwen-audio-asr--dca81ac5acd64dc7.md)。

将 `YOUR_WS_HOST` 替换为相应地域的 WebSocket 主机名，`YOUR_DEVICE_ID` 替换为设备标识，并按所选地域设置 `YOUR_API_KEY`。

### 连接参数

示例中的 JSON 作为字符串传入 Dart 方法。

```
{
  "device_id": "YOUR_DEVICE_ID",
  "url": "wss://YOUR_WS_HOST/api-ws/v1/inference",
  "service_mode": "1"
}
```

### 任务参数

示例中的 JSON 作为字符串传入 Dart 方法。

```
{
  "apikey": "YOUR_API_KEY",
  "nls_config": {
    "model": "qwen-audio-3.1-asr-flash-message",
    "sample_rate": 16000,
    "sr_format": "pcm"
  },
  "service_type": 4
}
```

`nls_config.sample_rate` 和 `nls_config.sr_format` 要与实际输入音频匹配。下例使用 16 kHz PCM。热词和上下文等可选参数按对应模型文档配置。

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

`Future<String?> getAllResponse()`

读取最近的完整识别响应。

### 事件与音频流

事件从 `eventStream` 读取。收到 Dart Map 时，以 `event` 识别事件名，任务类事件的 `resultCode` 可用于判断错误。

读取识别结果时可参考示例对 `asrResult` 和 `asrAllResponse` 的处理。

事件

用途

`EVENT_ASR_PARTIAL_RESULT`

临时识别结果

`EVENT_SENTENCE_END`

当前句的最终识别结果

`EVENT_TRANSCRIBER_COMPLETE`

任务或当前音频输出完成

`EVENT_ASR_ERROR`

任务失败
