# Qwen-Audio-TTS Android SDK

## 前提条件

1.  [获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。移动端应用请勿硬编码长期 API Key。建议由应用服务端[生成临时 API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)，再下发给客户端。
    
2.  **下载SDK并运行示例代码：**
    -   [下载最新SDK整合包](https://help.aliyun.com/zh/model-studio/sdk-selection-and-download)。
    -   解压 ZIP 包。在 `app/libs` 目录中获取 AAR 格式 SDK，并添加到项目依赖。  
        需要 Android CPP 接入时，使用 ZIP 包内的 `android_libs` 与 `android_include` 获取动态库和头文件。  
        

## 快速开始

用 Android Studio 打开工程。示例代码位于`DashCosyVoiceStreamTtsActivity.java`，替换 API Key 后体验功能。

在示例中使用模型 `qwen-audio-3.0-tts-flash`。

## 详细参考

-   [请求参数](https://help.aliyun.com/zh/model-studio/realtime-websocket-android-sdk-qwen-audio-tts-cosyvoice#model-qwen-audio-tts)
-   [接口参考](raw/_short/realtime-websocket-android-sdk-qwen-audio-tts-co-f71bb6bc1bf039a4.md)
