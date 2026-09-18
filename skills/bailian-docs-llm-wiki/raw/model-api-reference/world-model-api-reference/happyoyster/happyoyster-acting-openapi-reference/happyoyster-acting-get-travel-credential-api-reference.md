# HappyOyster-Acting-获取体验凭证 API参考

三方服务端使用主 API Key 换取短时效、一次性的 ticket，再将其安全下发给客户端。此接口只校验 World 归属、状态与规格，不创建 Travel。

## 适用范围

三方服务端使用主 API Key 换取短时效、一次性的 `ticket`，再将其安全下发给客户端。调用前请确认以下事项：

-   **鉴权要求**：仅支持**主 API Key**调用，临时 API Key 不可用（错误码 `403003`）。
    
    -   获取主 API Key：[获取与配置 API Key](https://help.aliyun.com/zh/model-studio/get-api-key#c38fb45bc6sje)。
-   **前置条件**：World 必须属于当前主账号和 Acting 模型，且状态为 `ready`。可通过[查询World构建状态](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference/happyoyster-acting-query-world-build-status-api-reference.md)接口确认。
    
-   **调用方**：您的**服务端**调用，换得的 `ticket` 应只下发给准备立即进房的客户端。
    

## HTTP调用

#### 新加坡

`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-acting/openapi/v1/worlds/get-travel-credential`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

#### 美国（弗吉尼亚）

`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-acting/openapi/v1/worlds/get-travel-credential`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

#### 请求参数

获取体验凭证

```
curl --location 'https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-acting/openapi/v1/worlds/get-travel-credential' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "encryptedWorldId": "{encryptedWorldId}"
}'
```

**Content-Type**`string`**（必选）**

请求内容类型。此参数必须设置为`application/json`。

**Authorization** `string` **（必选）**

API Key 鉴权。仅支持**主 API Key**，以 `sk-` 开头，如 `sk-xxx`。通常配置为环境变量 `$DASHSCOPE_API_KEY`。临时 API Key（`st-` 开头）调用返回 `403003`。

##### 请求体（Request Body）

**encryptedWorldId** `string` **（必选）**

当前主账号名下、状态为 `ready` 的 Acting World ID。由[创建World](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference/happyoyster-acting-create-world-api-reference.md)接口返回。

#### 响应参数

换取成功

```
{
    "code": 0,
    "message": null,
    "data": {
        "ticket": "tk_a1b2****",
        "expiresIn": 1800,
        "encryptedWorldId": "enc_a1b2****"
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

**ticket** `string`

前缀为 `tk_` 的一次性 Travel 凭证。有效期 1800 秒（30 分钟），且只能成功使用一次。

**expiresIn** `integer`

有效期秒数，固定为 `1800`，即 30 分钟。

**encryptedWorldId** `string`

凭证对应的加密 World ID。

## 前置状态与调用注意事项

-   World 必须属于当前主账号和 Acting 模型，且状态为 `ready`。
-   `ticket` 有效期为 1800 秒且只能成功使用一次；过期或已使用后须重新换取。
-   `ticket` 应只下发给准备立即进房的客户端，不应持久化为长期访问凭证。
-   调用本接口不会创建 Travel；Travel 在[进入房间](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference/happyoyster-acting-enter-travel-api-reference.md)成功时创建。
-   Acting 功能闸主要在创建和进房时生效；换凭证仍会校验 World 对应规格，规格未开通时返回 `403007`。

## 错误码

如果模型调用失败并返回报错信息，请参见[HappyOyster 错误码](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-error-code.md)进行解决。

## 下一步

换取 `ticket` 后：

-   [客户端进入房间](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference/happyoyster-acting-enter-travel-api-reference.md)：客户端使用 `ticket` 创建 Travel 并获取 RTC 配置。
