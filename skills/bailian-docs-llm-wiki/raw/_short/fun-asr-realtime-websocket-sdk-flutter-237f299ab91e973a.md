# Fun-ASR-Realtime Flutter SDK

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

在示例中使用模型 `fun-asr-realtime`。

## 详细参考

-   [详细参考](raw/_short/realtime-websocket-flutter-sdk-qwen-audio-asr-fu-7d49d68988d9eb94.md)
