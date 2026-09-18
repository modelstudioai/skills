# HappyOyster-Adventure-客户端进入房间 API参考

客户端使用 ticket 创建实际 Travel，并获取 RTC 入会配置和 Adventure 能力版本。maxExperienceTimeSec 仅在 Adventure 模型中生效。

## 适用范围

客户端使用 `ticket` 创建实际 Travel，并获取 RTC 入会配置。`maxExperienceTimeSec` 仅在 Adventure 模型中生效。调用前请确认以下事项：

-   **鉴权要求**：**不强制主 API Key**，使用 `ticket` 完成进房校验。获取方式请参见[获取鉴权凭证](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-quick-start/happyoyster-auth-setup.md)。
-   **前置条件**：`ticket` 由[获取体验凭证](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference/happyoyster-adventure-get-travel-credential-api-reference.md)接口换取，未过期且未使用，对应 World 状态为 `ready`。
-   **调用方**：您的客户端调用。

## HTTP调用

#### 华北2（北京）

`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-adventure/openapi/v1/travels/enter-travel`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

#### 新加坡

`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-adventure/openapi/v1/travels/enter-travel`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

#### 美国（弗吉尼亚）

`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-adventure/openapi/v1/travels/enter-travel`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

#### 请求参数

客户端进入房间

```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-adventure/openapi/v1/travels/enter-travel' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "ticket": "{ticket}",
    "maxExperienceTimeSec": 90
}'
```

**Content-Type**`string`**（必选）**

请求内容类型。此参数必须设置为`application/json`。

**Authorization** `string` **（必选）**

API Key 鉴权。不强制主 API Key，主 API Key 或临时 API Key 均可调用。

-   **主 API Key**：以 `sk-` 开头，如 `sk-xxx`。
-   **临时 API Key**：以 `st-` 开头，如 `st-xxx`。

##### 请求体（Request Body）

**ticket** `string` **（必选）**

未过期且未使用的一次性凭证。由[获取体验凭证](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference/happyoyster-adventure-get-travel-credential-api-reference.md)接口换取。同一 `ticket` 再次使用返回 `401011`。

**maxExperienceTimeSec** `integer` **（可选）**

最大体验时长，单位秒，必须是 JSON 整数。默认 `60`。可选值：

-   `60`
-   `90`
-   `120`

不接受字符串或其它数值（如 `"60"` 不是合法值）；非法档位返回 `400000`。服务端在达到该时长后自动结束 Travel。

#### 响应参数

进房成功

```
{
    "code": 0,
    "message": null,
    "data": {
        "encryptedTravelId": "trvl_a1b2****",
        "encryptedWorldId": "enc_a1b2****",
        "mode": 1,
        "creationModel": "simple",
        "playUrl": null,
        "firstFrame": "https://cdn.happyoyster.com/frames/world_xyz789.jpg",
        "rtcConfig": {
            "channelId": "stream_abc123",
            "appId": "18bca2e3218c46aebf8ff3a32fb12311",
            "token": "007eJxTYOh...",
            "userId": "user_1"
        },
        "version": "wanderV2",
        "aspectRatio": null,
        "noStreamAutoEndTimeoutSec": 30,
        "maxExperienceTimeSec": 90
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

新创建的加密 Travel ID。后续[查询Travel状态](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference/happyoyster-adventure-query-travel-status-api-reference.md)、结束、产物查询均使用此值。

**encryptedWorldId** `string`

当前 Travel 对应的加密 World ID。

**mode** `integer`

Adventure 恒为 `1`。

**creationModel** `string`

Adventure 恒为 `simple`。

**playUrl** `null`

暂不可用，固定为 `null`。

**firstFrame** `string`

World 首帧 URL。

**rtcConfig** `object`

RTC 入会配置；没有可用推流频道时为 `null`，客户端不能据此开始播放。

-   `channelId`：RTC 频道 ID
-   `appId`：平台分配的 RTC 应用 ID
-   `token`：RTC 入会 Token
-   `userId`：RTC 入会用户 ID，固定为 `user_1`

**version** `string`

Adventure 进房版本，固定为 `wanderV2`。须按此版本通过 SDK `sendCommand` 发送控制数据。

**aspectRatio** `null`

Adventure 固定为 `null`；播放器画幅不从本字段读取，跟随首帧图比例。

**noStreamAutoEndTimeoutSec** `integer`

无推流自动结束超时秒数，默认 30，以实际响应为准。进房后若在此时间内 `rtcStatus` 未进入推流态，应调用[结束Travel](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference/happyoyster-adventure-end-travel-api-reference.md)并传入 `failCode=TRAVEL_NO_STREAM_AUTO_END`。

**maxExperienceTimeSec** `integer`

服务端实际采用的体验时长，只会是 `60` / `90` / `120`。达到该时长后服务端自动结束 Travel。

## 前置状态与调用注意事项

-   `ticket` 对应的 World 必须为 `ready`，且 ticket 未过期、未使用。
-   调用成功即创建 Travel；同一 `ticket` 再次使用返回 `401011`。
-   `version` 必须按 `wanderV2` 处理，不能按其它模型的交互协议发送控制数据。
-   服务端在达到 `maxExperienceTimeSec` 后结束体验，客户端应处理随后到达的终态。
-   Adventure 的方向、视角和动作控制不是服务端 HTTP Open API，客户端必须使用对应平台 SDK 的 `sendCommand`，由 SDK 经 RTC DataChannel 发送。
-   `rtcConfig=null` 表示当前没有可用推流频道，客户端不能据此开始播放。

## 错误码

如果模型调用失败并返回报错信息，请参见[HappyOyster 错误码](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-error-code.md)进行解决。

## 下一步

进房成功后：

-   [查询Travel状态](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference/happyoyster-adventure-query-travel-status-api-reference.md)：每 2–5 秒轮询，读取可用动作池。
-   Travel 为 `running` 后，客户端通过 SDK `sendCommand` 发送方向、视角和动作控制。
-   [结束Travel](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference/happyoyster-adventure-end-travel-api-reference.md)：结束会话并处理产物。
