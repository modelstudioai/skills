# HappyOyster-Directing-查询Travel状态 API参考

查询 Directing Travel 生命周期、服务端推流状态、已执行文本指令和章节信息，也可同时上报客户端拉流或播放心跳。

## 适用范围

查询 Directing Travel 生命周期、服务端推流状态、已执行文本指令和章节信息，也可同时上报客户端拉流或播放心跳。调用前请确认以下事项：

-   **鉴权要求**：**不强制主 API Key**，主 API Key 或临时 API Key 均可调用。获取方式请参见[获取鉴权凭证](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-quick-start/happyoyster-auth-setup.md)。
-   **前置条件**：使用[客户端进入房间](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-enter-travel-api-reference.md)接口返回的 `encryptedTravelId` 查询。
-   **调用方**：您的服务端或客户端均可调用。建议每 2–5 秒轮询。

## HTTP调用

#### 新加坡

`GET https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/status`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

#### 美国（弗吉尼亚）

`GET https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/status`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

#### 请求参数

#### 查询Travel状态

```
curl --location 'https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/status?encryptedTravelId={encryptedTravelId}&clientStreamStatus=PLAYING&clientStreamStatusTimeMs=1788940800000' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

**Authorization** `string` **（必选）**

API Key 鉴权。不强制主 API Key，主 API Key 或临时 API Key 均可调用。

-   **主 API Key**：以 `sk-` 开头，如 `sk-xxx`。
-   **临时 API Key**：以 `st-` 开头，如 `st-xxx`。

##### Query 参数

**encryptedTravelId** `string` **（必选）**

Directing 加密 Travel ID。由[客户端进入房间](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-enter-travel-api-reference.md)接口返回。

**clientStreamStatus** `string` **（可选）**

客户端 RTC 拉流或播放状态，大小写不敏感。无法识别的值会被忽略。可选值：

-   `DISCONNECTED`：未连接或已离开频道
-   `CONNECTING`：正在连接 RTC 频道
-   `CONNECTED`：已入会，尚未开始播放或首帧未到达
-   `PLAYING`：已收到远端流并正在渲染
-   `BUFFERING`：缓冲中
-   `PAUSED`：客户端暂停播放，不等同于服务端 `pause`
-   `RECONNECTING`：重连中

**clientStreamStatusTimeMs** `long` **（可选）**

客户端状态变更的毫秒时间戳。与 `clientStreamStatus` 配套使用。

#### 响应参数

#### Travel运行中

```
{
    "code": 0,
    "message": null,
    "data": {
        "encryptedTravelId": "trvl_a1b2****",
        "status": "running",
        "rtcStatus": "PUSHING",
        "updateTime": "2026-06-04T00:02:00Z",
        "userInstructions": [
            {
                "instruction": "突然出现一只巨大的机器恐龙",
                "relativeStartTimeMs": 12000,
                "relativeEndTimeMs": 16000,
                "startTime": 12.0,
                "endTime": 16.0,
                "status": "executed"
            }
        ],
        "chapters": [
            {
                "chapterId": 1,
                "title": "第一章",
                "brief": "侦探进入赛博朋克城市",
                "actRange": [0, 10],
                "startTime": 4,
                "endTime": 20,
                "chapterImage": "https://cdn.happyoyster.com/chapters/ch1.jpg"
            }
        ],
        "characterActions": [],
        "environmentActions": []
    }
}
```

#### Travel失败

`errorCode` 取值见[错误码](https://help.aliyun.com/zh/model-studio/happyoyster-error-code#ho-ec-travel-errorcode-title)。

```
{
    "code": 0,
    "message": null,
    "data": {
        "encryptedTravelId": "trvl_a1b2****",
        "status": "failed",
        "rtcStatus": null,
        "updateTime": null,
        "userInstructions": null,
        "chapters": null,
        "characterActions": null,
        "environmentActions": null,
        "errorCode": "TRAVEL_SESSION_INIT_FAILED",
        "errorMessage": "Failed to allocate inference resources."
    }
}
```

**code** `integer`

返回码。`0` 表示成功，非 0 为错误码。

**message** `string`

错误信息。成功时为 `null`。

**data** `object`

响应数据。失败时为 `null`。

属性

**encryptedTravelId** `string`

加密 Travel ID。

**status** `string`

Travel 生命周期状态：

-   `init`：正在初始化会话资源
-   `pending`：排队或等待服务资源
-   `running`：正在运行，可按创建子模式调用支持的控制接口
-   `paused`：已完成服务端暂停；可恢复或回溯
-   `failed`：Travel 失败；原因见 `errorCode` / `errorMessage`
-   `completed`：Travel 已结束，可查询产物

**rtcStatus** `string`

服务端 RTC 推流状态；与客户端上报的 `clientStreamStatus` 不同。

**updateTime** `string`

最近更新时间，ISO 8601 格式。

**userInstructions** `array`

文本指令列表；无数据时为 `null`。每项含 `instruction`、`relativeStartTimeMs` / `relativeEndTimeMs`（相对毫秒）、`startTime` / `endTime`（时间轴秒数）、`status`。

**chapters** `array`

章节列表；尚未触发章节检测时为 `null`。每项含 `chapterId`、`title`、`brief`、`actRange`、`startTime`、`endTime`、`chapterImage`。

**characterActions** `array<string> | null`

Directing 不支持 SDK 动作控制，固定返回空数组；`failed` 时为 `null`。

**environmentActions** `array<string> | null`

Directing 不支持 SDK 环境动作控制，固定返回空数组；`failed` 时为 `null`。

**errorCode** `string`

仅 `status=failed` 时返回；结构化失败原因代码，取值见[错误码](https://help.aliyun.com/zh/model-studio/happyoyster-error-code#ho-ec-travel-errorcode-title)。

**errorMessage** `string`

与 `errorCode` 同时返回；英文失败说明。请按 `errorCode` 分支处理，不要匹配 `errorMessage` 文案。

## 前置状态与调用注意事项

-   建议每 2–5 秒轮询。
-   `running` 状态可按 `creationModel` 调用支持的控制接口：普通模式可 `instruct`、`pause`、`resume`、`rewind`、`end`；剧本模式可 `update-script`、`pause`、`resume`、`rewind`、`end`。
-   本接口不返回 `mode`、`aspectRatio`、`playUrl`、`bgmUrl` 或 `sessionId`；播流配置以[进入房间](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-enter-travel-api-reference.md)响应为准。
-   `clientStreamStatus` 是客户端播放侧心跳，`rtcStatus` 是服务端推流侧状态，两者不可互相替代。
-   `failed` 是终态，不会再产生成片；请按 `errorCode` 展示失败原因，不要展示为「尚未完成」。

## 错误码

如果模型调用失败并返回报错信息，请参见[HappyOyster 错误码](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-error-code.md)进行解决。

## 下一步

Travel 为 `running` 或 `paused` 时：

-   普通模式：[发送过程指令](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-instruct-travel-api-reference.md)。
-   剧本模式：[剧本全量更新](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-update-script-api-reference.md)。
-   通用：[暂停](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-pause-travel-api-reference.md) / [恢复](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-resume-travel-api-reference.md) / [回溯](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-rewind-travel-api-reference.md) / [结束](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-end-travel-api-reference.md)。
