# Fun-ASR-Realtime HarmonyOS SDK

## 前提条件

1.  [获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。移动端应用请勿硬编码长期 API Key。建议由应用服务端[生成临时 API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)，再下发给客户端。
    
2.  [下载最新SDK整合包](https://help.aliyun.com/zh/model-studio/sdk-selection-and-download)，解压后将 `entry/libs/neonui.har` 复制到应用工程的 `entry/libs` 目录，并在 `entry/oh-package.json5` 中添加依赖：
    
    ```
    {
      "dependencies": {
        "neonui": "file:libs/neonui.har"
      }
    }
    ```
    
    如需通过HarmonyOS C++接口接入，可使用整合包 `native/libs` 目录中的动态库和 `native/include` 目录中的头文件。
    
3.  在应用的 `module.json5` 中声明网络和麦克风权限，并在运行时申请麦克风权限。`reason_internet` 和 `reason_microphone` 为示例资源名，请在应用资源中定义对应说明。
    
    ```
    "requestPermissions": [
      {
        "name": "ohos.permission.INTERNET",
        "reason": "$string:reason_internet",
        "usedScene": { "abilities": ["EntryAbility"], "when": "always" }
      },
      {
        "name": "ohos.permission.MICROPHONE",
        "reason": "$string:reason_microphone",
        "usedScene": { "abilities": ["EntryAbility"], "when": "always" }
      }
    ]
    ```
    

## 快速开始

使用DevEco Studio打开整合包中的示例工程。示例页面位于 `entry/src/main/ets/pages/dashscope/DashFunAsrSpeechTranscriberPage.ets`。配置API Key后即可运行。

在示例中使用模型 `fun-asr-realtime`。

## 详细参考

-   [请求参数](https://help.aliyun.com/zh/model-studio/realtime-websocket-harmonyos-sdk-qwen-audio-asr-fun-asr#model-fun-asr-realtime)
-   [接口参考](raw/_short/realtime-websocket-harmonyos-sdk-qwen-audio-asr--dca81ac5acd64dc7.md)
