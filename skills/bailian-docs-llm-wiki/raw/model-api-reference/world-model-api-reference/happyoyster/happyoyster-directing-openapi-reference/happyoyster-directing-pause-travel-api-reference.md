# HappyOyster-Directing-暂停Travel API参考

请求暂停正在运行的 Directing Travel。暂停完成后可调用恢复或回溯。

## 适用范围

请求暂停正在运行的 Directing Travel。暂停完成后可调用[恢复](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-resume-travel-api-reference.md)或[回溯](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-rewind-travel-api-reference.md)。调用前请确认以下事项：

-   **鉴权要求**：**不强制主 API Key**，主 API Key 或临时 API Key 均可调用。获取方式请参见[获取鉴权凭证](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-quick-start/happyoyster-auth-setup.md)。
-   **前置条件**：Travel 状态需为 `running`。可通过[查询Travel状态](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-query-travel-status-api-reference.md)接口确认。
-   **调用方**：您的服务端或客户端均可调用。

## HTTP调用

#### 新加坡

`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/pause`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

#### 美国（弗吉尼亚）

`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/pause`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

#### 请求参数

暂停Travel

```
curl --location 'https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/pause' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "encryptedTravelId": "{encryptedTravelId}",
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

要暂停的 Directing 加密 Travel ID。由[客户端进入房间](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-enter-travel-api-reference.md)接口返回。

**userAgent** `string` **（可选）**

SDK 或客户端版本标识。非空字符串，优先于 HTTP `User-Agent`。

#### 响应参数

暂停成功

```
{
    "code": 0,
    "message": null,
    "data": {
        "encryptedTravelId": "trvl_a1b2****",
        "status": "paused"
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

暂停目标状态，返回 `paused`。

## 前置状态与调用注意事项

-   Travel 当前状态必须为 `running`。
-   进房响应中的 `version` 必须为 `storyV2`；本模型进房固定返回该值。
-   pause 的服务端状态确认是异步过程。需要紧接着调用[回溯](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-rewind-travel-api-reference.md)或[恢复](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-resume-travel-api-reference.md)时，应轮询[查询Travel状态](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-query-travel-status-api-reference.md)直到状态为 `paused`。

## 错误码

如果模型调用失败并返回报错信息，请参见[HappyOyster 错误码](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-error-code.md)进行解决。

## 下一步

暂停后可进行以下操作：

-   [恢复Travel](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-resume-travel-api-reference.md)：恢复已暂停的 Travel 继续运行。
-   [回溯Travel](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-rewind-travel-api-reference.md)：回到指定视频时间点。
-   [结束Travel](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-end-travel-api-reference.md)：直接结束 Travel。
