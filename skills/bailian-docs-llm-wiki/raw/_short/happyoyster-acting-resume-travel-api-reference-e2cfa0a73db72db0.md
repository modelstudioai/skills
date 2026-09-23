# HappyOyster-Acting-恢复Travel API参考

恢复已暂停的 Acting Travel，使其重新进入运行状态。

## 适用范围

恢复已暂停的 Acting Travel，使其重新进入运行状态。调用前请确认以下事项：

-   **鉴权要求**：**不强制主 API Key**，主 API Key 或临时 API Key 均可调用。获取方式请参见[获取鉴权凭证](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-quick-start/happyoyster-auth-setup.md)。
-   **前置条件**：Travel 必须已通过[查询Travel状态](raw/_short/happyoyster-acting-query-travel-status-api-refer-bb36f15c26e6c92c.md)确认为 `paused`。
-   **调用方**：您的服务端或客户端均可调用。

## HTTP调用

#### 新加坡

`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-acting/openapi/v1/travels/resume`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

#### 美国（弗吉尼亚）

`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-acting/openapi/v1/travels/resume`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

#### 请求参数

#### 恢复Travel

```
curl --location 'https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-acting/openapi/v1/travels/resume' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "encryptedTravelId": "{encryptedTravelId}",
    "userAgent": "HappyOyster-Web/1.2.0"
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

要恢复的 Acting 加密 Travel ID。由[客户端进入房间](raw/_short/happyoyster-acting-enter-travel-api-reference-56ea4df0a872fdb7.md)接口返回。

**userAgent** `string` **（可选）**

SDK 或客户端版本标识。非空字符串，优先于 HTTP `User-Agent`，用于 SDK 版本和平台统计。

#### 响应参数

#### 恢复成功

```
{
    "code": 0,
    "message": null,
    "data": {
        "encryptedTravelId": "trvl_a1b2****",
        "status": "running"
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

恢复后的状态，返回 `running`。

## 前置状态与调用注意事项

-   Travel 必须已通过[查询Travel状态](raw/_short/happyoyster-acting-query-travel-status-api-refer-bb36f15c26e6c92c.md)确认为 `paused`。
-   进房响应中的 `version` 必须为 `actingV2`。
-   已结束或失败的 Travel 不能恢复。
-   恢复后可继续发送[文本过程指令](raw/_short/happyoyster-acting-instruct-travel-api-reference-5c29e8efed3870dd.md)；客户端应以状态查询结果收敛本地运行状态。
-   恢复不改变进房时返回的 `aspectRatio`。

## 错误码

如果模型调用失败并返回报错信息，请参见[HappyOyster 错误码](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-error-code.md)进行解决。

## 下一步

恢复后可进行以下操作：

-   [查询Travel状态](raw/_short/happyoyster-acting-query-travel-status-api-refer-bb36f15c26e6c92c.md)：确认 Travel 回到 `running`。
-   [发送文本过程指令](raw/_short/happyoyster-acting-instruct-travel-api-reference-5c29e8efed3870dd.md)：继续驱动角色表演。
-   [结束Travel](raw/_short/happyoyster-acting-end-travel-api-reference-07665d664cc3dbc3.md)：结束会话并处理产物。
