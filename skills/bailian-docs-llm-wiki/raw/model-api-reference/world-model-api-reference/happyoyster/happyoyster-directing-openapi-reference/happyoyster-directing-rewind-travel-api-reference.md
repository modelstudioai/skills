# HappyOyster-Directing-回溯Travel API参考

将 Travel 回溯到指定视频时间点，并从实际落点恢复运行。Travel 必须先进入 paused 状态。

## 适用范围

将 Travel 回溯到指定视频时间点，并从实际落点恢复运行。调用前请确认以下事项：

-   **鉴权要求**：**不强制主 API Key**，主 API Key 或临时 API Key 均可调用。获取方式请参见[获取鉴权凭证](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-quick-start/happyoyster-auth-setup.md)。
-   **前置条件**：Travel 必须先进入 `paused` 状态，不能在 `running` 时直接回溯。可通过[查询Travel状态](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-query-travel-status-api-reference.md)接口确认。
-   **调用方**：您的服务端或客户端均可调用。

## HTTP调用

#### 新加坡

`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/rewind`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

#### 美国（弗吉尼亚）

`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/rewind`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

#### 请求参数

#### 回溯Travel

```
curl --location 'https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/rewind' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "encryptedTravelId": "{encryptedTravelId}",
    "rewindToSec": 84.0,
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

要回溯的 Directing 加密 Travel ID。由[客户端进入房间](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-enter-travel-api-reference.md)接口返回。

**rewindToSec** `number` **（必选）**

目标视频时间，单位秒。大于或等于 `0`，建议为 4 的倍数（如 4、8、12）。服务端按 `Math.round(rewindToSec / 4) × 4` 四舍五入到最近的 4 秒边界。实际落点以响应中的 `resumedAtSec` / `actualRewindToSec` 为准。

**userAgent** `string` **（可选）**

SDK 或客户端版本标识。非空字符串，优先于 HTTP `User-Agent`。

#### 响应参数

#### 回溯成功

```
{
    "code": 0,
    "message": null,
    "data": {
        "encryptedTravelId": "trvl_a1b2****",
        "status": "running",
        "resumedAtSec": 84.0,
        "actualRewindToSec": 84.0
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

加密的 Travel ID。

**status** `string`

回溯完成后的状态，返回 `running`。

**resumedAtSec** `number`

实际恢复播放的秒数，可能与请求值略有偏差。

**actualRewindToSec** `number`

实际回溯落点，与 `resumedAtSec` 相同。

## 前置状态与调用注意事项

-   Travel 必须先进入 `paused`；不能在 `running` 时直接回溯。
-   [暂停Travel](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-pause-travel-api-reference.md)存在约 3 秒的异步确认屏障。收到 pause 响应后，仍应轮询[查询Travel状态](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-query-travel-status-api-reference.md)，确认对外状态已经是 `paused` 再调用本接口。
-   剧本按 4 秒 Block 组织，`rewindToSec` 建议使用 4、8、12 等 4 的倍数（如 `6 → 8`）。
-   实际落点以 `resumedAtSec` / `actualRewindToSec` 为准。

## 错误码

如果模型调用失败并返回报错信息，请参见[HappyOyster 错误码](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-error-code.md)进行解决。

## 下一步

回溯后 Travel 回到 `running`：

-   [查询Travel状态](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-query-travel-status-api-reference.md)：确认运行状态。
-   普通模式：[发送过程指令](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-instruct-travel-api-reference.md)。
-   [暂停Travel](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-pause-travel-api-reference.md)：再次暂停以进行下一次回溯。
-   [结束Travel](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-end-travel-api-reference.md)：结束会话并处理产物。
