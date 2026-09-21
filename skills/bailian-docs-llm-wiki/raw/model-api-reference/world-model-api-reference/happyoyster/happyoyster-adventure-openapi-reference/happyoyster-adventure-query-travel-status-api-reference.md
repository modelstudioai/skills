# HappyOyster-Adventure-查询Travel状态 API参考

查询 Adventure Travel 生命周期、服务端推流状态和当前世界的动作池，也可同时上报客户端拉流或播放心跳。

## 适用范围

查询 Adventure Travel 生命周期、服务端推流状态和当前世界的动作池，也可同时上报客户端拉流或播放心跳。调用前请确认以下事项：

-   **鉴权要求**：**不强制主 API Key**，主 API Key 或临时 API Key 均可调用。获取方式请参见[获取鉴权凭证](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-quick-start/happyoyster-auth-setup.md)。
-   **前置条件**：使用[客户端进入房间](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference/happyoyster-adventure-enter-travel-api-reference.md)接口返回的 `encryptedTravelId` 查询。
-   **调用方**：您的服务端或客户端均可调用。建议每 2–5 秒轮询。

## HTTP调用

#### 华北2（北京）

`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-adventure/openapi/v1/travels/status`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

#### 新加坡

`GET https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-adventure/openapi/v1/travels/status`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

#### 美国（弗吉尼亚）

`GET https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-adventure/openapi/v1/travels/status`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

#### 请求参数

#### 查询Travel状态

```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-adventure/openapi/v1/travels/status?encryptedTravelId={encryptedTravelId}&clientStreamStatus=PLAYING&clientStreamStatusTimeMs=1788940800000' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

**Authorization** `string` **（必选）**

API Key 鉴权。不强制主 API Key，主 API Key 或临时 API Key 均可调用。

-   **主 API Key**：以 `sk-` 开头，如 `sk-xxx`。
-   **临时 API Key**：以 `st-` 开头，如 `st-xxx`。

##### Query 参数

**encryptedTravelId** `string` **（必选）**

Adventure 加密 Travel ID。由[客户端进入房间](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference/happyoyster-adventure-enter-travel-api-reference.md)接口返回。

**clientStreamStatus** `string` **（可选）**

客户端 RTC 拉流或播放状态，大小写不敏感。无法识别的值会被忽略。可选值：

-   `DISCONNECTED`：未连接或已离开频道
-   `CONNECTING`：正在连接 RTC 频道
-   `CONNECTED`：已入会，尚未开始播放或首帧未到达
-   `PLAYING`：已收到远端流并正在渲染
-   `BUFFERING`：缓冲中
-   `PAUSED`：客户端暂停播放，不表示 Adventure Travel 支持服务端暂停
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
        "userInstructions": null,
        "chapters": null,
        "characterActions": [
            "dash",
            "jump",
            "crouch",
            "attack"
        ],
        "environmentActions": [
            "ride_motorcycle",
            "enter_exit_car"
        ]
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
-   `running`：正在运行，可以通过 SDK `sendCommand` 实时操控
-   `failed`：Travel 失败；原因见 `errorCode` / `errorMessage`
-   `completed`：Travel 已结束，可查询产物

Adventure 产品能力没有 `paused` 状态，不要围绕暂停 / 恢复构建状态机。

**rtcStatus** `string`

服务端 RTC 推流状态；与客户端上报的 `clientStreamStatus` 不同。

**updateTime** `string`

最近更新时间，ISO 8601 格式。

**userInstructions** `null | array`

Adventure 不支持 HTTP `instruct`，探索动作也不会回显到该字段；通常为 `null` 或 `[]`，请忽略。

**chapters** `array`

章节列表；未生成章节数据时为 `null`。

**characterActions** `array<string> | null`

当前角色 / 主体可用动作 ID；无推荐时为 `[]`；`failed` 时为 `null`。通常返回 2–4 个。常见动作：

-   `dash`：前冲
-   `jump`：跳跃
-   `crouch`：下蹲 / 下趴
-   `attack`：攻击

**environmentActions** `array<string> | null`

当前场景可用环境交互动作 ID；无推荐时为 `[]`；`failed` 时为 `null`。服务端按场景从固定动作池中选择 0–3 个，可返回空数组。常见动作：

-   `ride_horse`：骑马
-   `ride_bicycle`：骑自行车
-   `ride_motorcycle`：骑摩托
-   `enter_exit_car`：上下车
-   `open_close_door`：开 / 关门
-   `take_cover`：躲避掩体
-   `car_light`：开车灯；仅当同时返回 `enter_exit_car` 时可能出现
-   `car_horn`：按车喇叭；仅当同时返回 `enter_exit_car` 时可能出现

**errorCode** `string`

仅 `status=failed` 时返回；结构化失败原因代码，取值见[错误码](https://help.aliyun.com/zh/model-studio/happyoyster-error-code#ho-ec-travel-errorcode-title)。

**errorMessage** `string`

与 `errorCode` 同时返回；英文失败说明。请按 `errorCode` 分支处理，不要匹配 `errorMessage` 文案。

## 前置状态与调用注意事项

-   建议每 2–5 秒轮询。
-   Adventure 产品能力没有 `paused` 状态，不要围绕暂停 / 恢复构建状态机。
-   `characterActions` 和 `environmentActions` 是可用动作提示；实际操控仍通过 SDK `sendCommand` 发送。
-   本接口不返回 `mode`、`playUrl`、`bgmUrl` 或 `sessionId`；播流配置以[进入房间](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference/happyoyster-adventure-enter-travel-api-reference.md)响应为准。
-   `clientStreamStatus` 是客户端播放侧心跳，`rtcStatus` 是服务端推流侧状态，两者不可互相替代。
-   Adventure 不支持 HTTP `instruct`、`pause`、`resume`、`rewind`、`update-script`；不要把以下路径作为可用 HTTP 能力集成：`/travels/instruct`、`/travels/pause`、`/travels/resume`、`/travels/rewind`、`/travels/update-script`。
-   `failed` 是终态，不会再产生成片；请按 `errorCode` 展示失败原因，不要展示为「尚未完成」。

## 错误码

如果模型调用失败并返回报错信息，请参见[HappyOyster 错误码](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-error-code.md)进行解决。

## 下一步

Travel 为 `running` 后：

-   客户端通过 SDK `sendCommand` 发送方向、视角和动作控制（可先读取本接口返回的动作池）。
-   [结束Travel](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference/happyoyster-adventure-end-travel-api-reference.md)：结束会话并处理产物。
