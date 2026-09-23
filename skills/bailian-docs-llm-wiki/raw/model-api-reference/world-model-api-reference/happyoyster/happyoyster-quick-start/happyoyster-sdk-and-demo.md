# 下载 SDK 与 Demo

下载 HappyOyster 各端客户端 SDK 与服务端 Demo 参考实现。

## 客户端 SDK 与 Demo

SDK 封装了 RTC 连接与 Travel 控制，开箱即用。请根据您的目标平台选择对应 SDK 文档：

**平台**

**接入指南**

**API 参考**

**SDK 包**

**Demo**

Android

[接入指南](raw/_short/happyoyster-android-sdk-integration-guide-0ec60cb58a01b74a.md)

[API 参考](raw/_short/happyoyster-android-sdk-api-reference-2e55bd454caa0124.md)

[Maven：cn.happyoyster:opensdk](https://central.sonatype.com/artifact/cn.happyoyster/opensdk)（最新稳定版）

[源码](https://github.com/Future-Living-Lab/happyoyster-sdk-demo-android/blob/main/README.zh-CN.md) ｜ [Playground体验](raw/_short/happyoyster-android-playground-guide-9f72e5f97e240161.md)

iOS

[接入指南](raw/_short/happyoyster-ios-sdk-integration-guide-41ea7eabc2facd22.md)

[API 参考](raw/model-api-reference/world-model-api-reference/happyoyster/client-sdk/ios-sdk-2/happyoyster-ios-sdk-api-reference.md)

[CocoaPods：HappyOysterSDK](https://cocoapods.org/pods/HappyOysterSDK)（1.0.3，公开 Trunk）

[源码](https://github.com/Future-Living-Lab/happyoyster-sdk-demo-ios)

Web

[接入指南](raw/_short/happyoyster-web-sdk-integration-guide-b01827224f96aa20.md)

[API 参考](raw/model-api-reference/world-model-api-reference/happyoyster/client-sdk/web-sdk/happyoyster-web-sdk-api-reference.md)

[npm包：@happy-oyster/js-sdk](https://www.npmjs.com/package/@happy-oyster/js-sdk)

[开箱即用的前端Demo（附带Node服务）](https://github.com/Future-Living-Lab/happyoyster-sdk-demo-web/blob/main/README.zh-CN.md)

## 服务端 Demo

服务端 Demo 通过 `/server-api/*` 演示 temporary API Key（token）签发、一次性 `ticket` 换取，以及 World、历史、产物等服务端接口逻辑，供您自建后端参考。

**服务端**

**Demo**

Node

[Node服务端参考实现](https://github.com/Future-Living-Lab/happyoyster-sdk-demo-node/blob/main/docs/zh/README.md)

Python

[Python服务端参考实现](https://github.com/Future-Living-Lab/happyoyster-sdk-demo-python/blob/main/docs/zh/README.md)

**说明****生产环境请在自有后端实现**，不要直接依赖 Demo 中的服务。
