# 接入流程

服务端调用 HappyOyster Open API 准备世界与产物导出，客户端 SDK 完成 RTC 建连与实时互动。

HappyOyster 采用**服务端 + 客户端**分离的接入方式：服务端通过 Open API 管理世界与产物，客户端 SDK 完成实时体验。开始前请先完成[获取鉴权凭证](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-quick-start/happyoyster-auth-setup.md)。

**说明**

-   服务端 Open API 按体验模式拆分为 Adventure（世界探索）/ Directing（实时导演）/ Acting（角色演绎）三套，请根据业务选择对应模式的接口。
-   World 与 Travel 严格属于其创建模型，跨模型访问会返回 `403001`（world）或 `404000`（travel）。
-   SDK **不负责**世界的创建与管理，仅负责客户端实时体验。

## 一、准备世界（服务端 Open API）

1.  **创建世界**，按模式选择接口：[Adventure-创建世界](raw/_short/happyoyster-adventure-create-world-api-reference-b764ec539142394b.md) / [Directing-创建世界](raw/_short/happyoyster-directing-create-world-api-reference-6f3bdbbb6537960b.md) / [Acting-创建世界](raw/_short/happyoyster-acting-create-world-api-reference-47f1f4ec26522c7d.md)。
2.  **轮询构建状态**（3–5 秒间隔）至 `ready`：[Adventure-查询世界构建状态](raw/_short/happyoyster-adventure-query-world-build-status-a-4830e59b84023226.md) / [Directing-查询世界构建状态](raw/_short/happyoyster-directing-query-world-build-status-a-48bf75e27c43945d.md) / [Acting-查询世界构建状态](raw/_short/happyoyster-acting-query-world-build-status-api--5436f98af63bbe85.md)。
3.  **换取 ticket**：使用主 API Key 调用 [Adventure-获取体验凭证](raw/_short/happyoyster-adventure-get-travel-credential-api--d269f4908c7288f2.md) / [Directing-获取体验凭证](raw/_short/happyoyster-directing-get-travel-credential-api--3e983dc0416050b9.md) / [Acting-获取体验凭证](raw/_short/happyoyster-acting-get-travel-credential-api-ref-dfc7dc5832959ca8.md)，获得一次性 `ticket`。
4.  **下发凭证给客户端**：将 `ticket` 与[临时 API Key](https://help.aliyun.com/zh/model-studio/happyoyster-auth-setup#ho-auth-temp-key)（作为 SDK 的 `token`）一并下发。

## 二、实时体验（客户端 SDK）

SDK 封装 RTC 建连、视频播放与交互指令。

1.  **初始化 SDK**：`initialize` + `updateToken`，注入 API Host 与临时 API Key。
    
2.  **开始体验**：`startTravel(ticket)`，SDK 自动进房并建连。
    
3.  **挂载视频**：将 `attachVideo()` 返回的视图加入布局；Acting 依据进房回包的 `aspectRatio` 设置容器方向。
    
4.  **实时互动**：
    
    -   世界探索（Adventure）：调用 `sendCommand` 发送方向 / 视角 / 动作指令。
    -   实时导演（Directing）：调用 `sendInstruct` 发送文本指令驱动剧情。
    -   角色演绎（Acting）：调用 `sendInstruct` 发送文本指令。
5.  **过程控制**：
    
    -   世界探索（Adventure）：不支持暂停、回溯。
    -   实时导演（Directing）：支持 `pause`、`rewind`、`resume`。
    -   角色演绎（Acting）：支持 `pause`、`resume`，不支持 `rewind`。
6.  **结束体验**：`endTravel`，释放 RTC 与资源。
    

## 三、获取产物（服务端 Open API）

Travel 结束后，使用主 API Key 轮询 [Adventure-查询Travel产物](raw/_short/happyoyster-adventure-query-travel-artifacts-api-ae37da872a0bc999.md) / [Directing-查询Travel产物](raw/_short/happyoyster-directing-query-travel-artifacts-api-2da27b6ffc227186.md) / [Acting-查询Travel产物](raw/_short/happyoyster-acting-query-travel-artifacts-api-re-af546d869e863975.md)，直至 `composeStatus = ready`。推荐对外交付 `video.withInstructionAndWatermark`（指令 + 水印合成版）。

## 下一步

-   [下载 SDK 与 Demo](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-quick-start/happyoyster-sdk-and-demo.md)：各端 SDK 包、接入指南、API 参考与开源 Demo。
