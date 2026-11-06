# AOQ SDK 简介

AOQ SDK 面向实时多模态场景，帮助开发者基于阿里云 Realtime API 快速搭建实时交互应用。

以下实时模型的媒体类型和配置请参见对应的 AOQ 接入文档：

-   [Qwen-Omni-Realtime](raw/model-api-reference/realtime-api-directory/omni-realtime-api-directory/omni-realtime-aoq-access.md)
-   [Qwen-Audio-Realtime](raw/model-api-reference/realtime-api-directory/audio-realtime-api-directory/audio-realtime-aoq-access.md)
-   [Qwen-LiveTranslate-Realtime](raw/model-api-reference/realtime-api-directory/livetranslate-realtime-api-directory/livetranslate-realtime-aoq-access.md)

Qwen-Audio-Realtime 不支持视频输入或输出。

## 各平台 API

-   [Windows](raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api/aoq-windows-sdk-reference.md)
-   [macOS](raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api/aoq-macos-sdk-reference.md)
-   [Electron](raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api/aoq-electron-sdk-reference.md)
-   [Linux C++](raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api/aoq-linux-cpp-sdk-reference.md)
-   [Linux Python](raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api/aoq-linux-python-sdk-reference.md)
-   [Android](raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api/aoq-android-sdk-reference.md)
-   [iOS](raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api/aoq-ios-sdk-reference.md)
-   [HarmonyOS](raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api/aoq-harmony-sdk-reference.md)

其他能力说明请参见[功能参考](raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api/realtime-api-aoq-sdk-function.md)。

## API设计与回调机制

AOQ SDK 采用声明式 API 设计：您只需通过 API 设置期望的目标状态，SDK 会自动判断当前状态并在适当时机完成切换，同时通过回调实时反馈执行进度。无需关心具体的调用时机，也无需重复调用。

## 异常处理机制

AOQ SDK 在遇到异常时会自动尝试恢复，仅在无法自行恢复时才通过回调通知开发者介入处理。无法恢复的错误主要分为两类：物理限制（如网络中断、音视频设备故障、CPU 或内存不足）和外部因素（如 Token 无效）。

## 下载指南

AOQ SDK 为阿里云自研产品，请通过官网下载，详情请参见[SDK下载](raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api/realtime-sdk-download.md)。
