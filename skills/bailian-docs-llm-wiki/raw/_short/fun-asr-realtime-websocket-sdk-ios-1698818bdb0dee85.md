# Fun-ASR-Realtime iOS SDK

## 前提条件

1.  [获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。移动端应用请勿硬编码长期 API Key。建议由应用服务端[生成临时 API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)，再下发给客户端。

### 安装 SDK

-   [下载最新SDK整合包](https://help.aliyun.com/zh/model-studio/sdk-selection-and-download)。
-   解压 ZIP 包，将其中的 nuisdk.xcframework 添加到工程。
-   在 Build Phases → Link Binary With Libraries 中添加 nuisdk.xcframework。
-   在 General → Frameworks, Libraries, and Embedded Content 中将 nuisdk.xcframework 设置为 Embed & Sign。

## 快速开始

用 Xcode 打开示例工程。示例代码位于`DashFunAsrSpeechTranscriberViewController.m`，替换 API Key 后体验功能。

在示例中使用模型 `fun-asr-realtime`。

## 详细参考

-   [请求参数](https://help.aliyun.com/zh/model-studio/realtime-websocket-ios-sdk-qwen-audio-asr-fun-asr#model-fun-asr-realtime)
-   [接口参考](raw/_short/realtime-websocket-ios-sdk-qwen-audio-asr-fun-as-cd3e96089443ba08.md)
