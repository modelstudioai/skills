# HappyOyster-Directing-客户端进入房间 API参考

客户端使用 ticket 创建实际 Travel，并获取 RTC 入会配置和 Directing 能力版本。creationModel 决定 Travel 可调用的控制接口。

## 适用范围

客户端使用 `ticket` 创建实际 Travel，并获取 RTC 入会配置。调用前请确认以下事项：

-   **鉴权要求**：**不强制主 API Key**，使用 `ticket` 完成进房校验。获取方式请参见[获取鉴权凭证](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-quick-start/happyoyster-auth-setup.md)。
-   **前置条件**：`ticket` 由[获取体验凭证](raw/_short/happyoyster-directing-get-travel-credential-api--3e983dc0416050b9.md)接口换取，未过期且未使用，对应 World 状态为 `ready`。
-   **调用方**：您的客户端调用。

## HTTP调用

#### 新加坡

`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/enter-travel`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

#### 美国（弗吉尼亚）

`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/enter-travel`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

#### 请求参数

#### 客户端进入房间

```
curl --location 'https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/enter-travel' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "ticket": "{ticket}"
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

未过期且未使用的一次性凭证。由[获取体验凭证](raw/_short/happyoyster-directing-get-travel-credential-api--3e983dc0416050b9.md)接口换取。同一 `ticket` 再次使用返回 `401011`。

**说明**Directing 进房不消费

`maxExperienceTimeSec`，请勿传入。该字段仅 Adventure 生效；若仍传入非法档位，会在模型分流前返回 `400000`。成功响应仍为 `null`。

#### 响应参数

```
{
    "code": 0,
    "message": null,
    "data": {
        "encryptedTravelId": "trvl_a1b2****",
        "encryptedWorldId": "enc_a1b2****",
        "mode": 2,
        "creationModel": "simple",
        "playUrl": null,
        "firstFrame": "https://cdn.happyoyster.com/frames/world_xyz789.jpg",
        "rtcConfig": {
            "channelId": "stream_abc123",
            "appId": "18bca2e3218c46aebf8ff3a32fb12311",
            "token": "007eJxTYOh...",
            "userId": "user_1"
        },
        "version": "storyV2",
        "aspectRatio": null,
        "noStreamAutoEndTimeoutSec": 30,
        "maxExperienceTimeSec": null
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

新创建的加密 Travel ID。后续[查询Travel状态](raw/_short/happyoyster-directing-query-travel-status-api-re-d536083e25c2aee5.md)、回溯、暂停、恢复、结束、产物查询均使用此值。

**encryptedWorldId** `string`

当前 Travel 对应的加密 World ID。

**mode** `integer`

Directing 恒为 `2`。

**creationModel** `string`

`simple` 或 `scriptlist`；决定 Travel 可调用的控制接口：

-   `simple`：`instruct`、`pause`、`resume`、`rewind`、`end`
-   `scriptlist`：`update-script`、`pause`、`resume`、`rewind`、`end`（不支持 `instruct`）

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

Directing 进房版本，固定为 `storyV2`。

**aspectRatio** `null`

Directing 模型固定为 `null`。

**noStreamAutoEndTimeoutSec** `integer`

无推流自动结束超时秒数，默认 30，以实际响应为准。进房后若在此时间内 `rtcStatus` 未进入推流态，应调用[结束Travel](raw/_short/happyoyster-directing-end-travel-api-reference-5fe76226682ff253.md)并传入 `failCode=TRAVEL_NO_STREAM_AUTO_END`。

**maxExperienceTimeSec** `null`

Directing 模型固定为 `null`。

## 前置状态与调用注意事项

-   `ticket` 对应的 World 必须为 `ready`，且 ticket 未过期、未使用。
-   不要传 `maxExperienceTimeSec`。Directing 不按该字段限制体验时长。
-   调用成功即创建 Travel；同一 `ticket` 再次使用返回 `401011`。
-   `creationModel=scriptlist` 时不要调用 `instruct`，应使用[剧本全量更新](raw/_short/happyoyster-directing-update-script-api-referenc-559783f11176cb54.md)。
-   `rtcConfig=null` 表示当前没有可用推流频道，客户端不能据此开始播放。

## 错误码

如果模型调用失败并返回报错信息，请参见[HappyOyster 错误码](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-error-code.md)进行解决。

## 下一步

进房成功后：

-   [查询Travel状态](raw/_short/happyoyster-directing-query-travel-status-api-re-d536083e25c2aee5.md)：每 2–5 秒轮询，按 `creationModel` 调用可用的控制接口。
-   普通模式：[发送过程指令](raw/_short/happyoyster-directing-instruct-travel-api-refere-2cd5aa6eabceb2c4.md)。
-   剧本模式：[剧本全量更新](raw/_short/happyoyster-directing-update-script-api-referenc-559783f11176cb54.md)。
-   通用：[暂停](raw/_short/happyoyster-directing-pause-travel-api-reference-21bb582a9c4e8b95.md) / [恢复](raw/_short/happyoyster-directing-resume-travel-api-referenc-594ac8725680fe8b.md) / [回溯](raw/_short/happyoyster-directing-rewind-travel-api-referenc-869fcb622ca2907a.md) / [结束](raw/_short/happyoyster-directing-end-travel-api-reference-5fe76226682ff253.md)。
