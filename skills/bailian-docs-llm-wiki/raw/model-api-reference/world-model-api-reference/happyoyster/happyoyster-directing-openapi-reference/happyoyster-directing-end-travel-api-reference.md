# HappyOyster-Directing-结束Travel API参考

结束 Directing Travel。正常结束时状态变为 completed 并进入产物处理；无推流超时结束时变为 failed，且不生成回放产物。

## 适用范围

结束 Directing Travel。正常结束时状态变为 `completed` 并进入产物处理；无推流超时结束时变为 `failed`，且不生成回放产物。调用前请确认以下事项：

-   **鉴权要求**：**不强制主 API Key**，主 API Key 或临时 API Key 均可调用。获取方式请参见[获取鉴权凭证](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-quick-start/happyoyster-auth-setup.md)。
-   **前置条件**：Travel 必须尚未进入终态，并处于服务端可结束的状态。可通过[查询Travel状态](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-query-travel-status-api-reference.md)接口确认。
-   **调用方**：您的服务端或客户端均可调用。

## HTTP调用

#### 新加坡

`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/end`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

#### 美国（弗吉尼亚）

`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/end`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

#### 请求参数

#### 正常结束

```
curl --location 'https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/end' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "encryptedTravelId": "{encryptedTravelId}",
    "userAgent": "your-client/1.2.0"
}'
```

#### 无推流超时结束

```
curl --location 'https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/end' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "encryptedTravelId": "{encryptedTravelId}",
    "failCode": "TRAVEL_NO_STREAM_AUTO_END",
    "userAgent": "your-client/1.2.0"
}'
```

**Content-Type**`string`**（必选）**

请求内容类型。此参数必须设置为`application/json`。

**Authorization** `string` **（必选）**

API Key 鉴权。不强制主 API Key，主 API Key 或临时 API Key 均可调用。

-   **主 API Key**：以 `sk-` 开头，如 `sk-xxx`。
-   **临时 API Key**：以 `st-` 开头，如 `st-xxx`。

##### 请求体（Request Body）

**encryptedTravelId** `string` **（必选）**

要结束的 Directing 加密 Travel ID。由[客户端进入房间](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-enter-travel-api-reference.md)接口返回。

**failCode** `string` **（可选）**

失败结束原因。省略时按正常结束处理。当前仅支持：

-   `TRAVEL_NO_STREAM_AUTO_END`：用于[进入房间](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-enter-travel-api-reference.md)后超过 `noStreamAutoEndTimeoutSec` 仍未收到推流的场景，该结束方式不生成回放产物

传入未支持的值返回 `400000`。

**userAgent** `string` **（可选）**

SDK 或客户端版本标识。非空字符串，优先于 HTTP `User-Agent`。

#### 响应参数

#### 正常结束

```
{
    "code": 0,
    "message": null,
    "data": {
        "encryptedTravelId": "trvl_a1b2****",
        "status": "completed",
        "endedAt": "2026-06-04T00:03:00Z",
        "durationSec": 180
    }
}
```

#### 无推流超时结束

```
{
    "code": 0,
    "message": null,
    "data": {
        "encryptedTravelId": "trvl_a1b2****",
        "status": "failed",
        "errorCode": "TRAVEL_NO_STREAM_AUTO_END",
        "errorMessage": "Something went wrong.",
        "endedAt": "2026-06-04T00:03:00Z",
        "durationSec": null
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

已结束的加密 Travel ID。

**status** `string`

结束状态：`completed`（正常结束）/ `failed`（带受支持 `failCode` 时的失败结束）。

**errorCode** `string`

失败原因代码；正常结束时为 `null`。

**errorMessage** `string`

失败说明；正常结束时为 `null`。

**endedAt** `string`

结束时间，ISO 8601 格式。

**durationSec** `integer`

有效视频时长秒数；无推流失败结束或时长尚不可解析时为 `null`。

## 前置状态与调用注意事项

-   客户端应在进房后轮询[查询Travel状态](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-query-travel-status-api-reference.md)。如果在 `noStreamAutoEndTimeoutSec` 内 `rtcStatus` 未进入推流态，使用 `TRAVEL_NO_STREAM_AUTO_END` 结束。
-   传入 `TRAVEL_NO_STREAM_AUTO_END` 后 Travel 为 `failed`，不能查询到回放产物。
-   正常结束后，`durationSec` 优先使用最终视频文件时长；最终视频尚不可用时，使用当前最新可用生成结果的 `durationMs`。两者均不可用时为 `null`。
-   正常结束进入 `completed` 后，产物合成仍可能进行中；按[查询Travel产物](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-query-travel-artifacts-api-reference.md)的返回状态决定是否继续轮询。

## 错误码

如果模型调用失败并返回报错信息，请参见[HappyOyster 错误码](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-error-code.md)进行解决。

## 下一步

Travel 进入 `completed` 后：

-   [查询Travel产物](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-query-travel-artifacts-api-reference.md)：轮询获取录制原片和合成变体。
-   [查询Travel列表](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-query-travel-list-api-reference.md)：查看历史 Travel。
