# HappyOyster-Directing-删除World API参考

删除当前主账号名下的 Directing World。同账号下 World 已不存在时幂等返回 deleted=false。

## 适用范围

删除当前主账号名下的 Directing World。调用前请确认以下事项：

-   **鉴权要求**：仅支持**主 API Key**调用，临时 API Key 不可用（错误码 `403003`）。
    
    -   获取主 API Key：[获取与配置 API Key](https://help.aliyun.com/zh/model-studio/get-api-key#c38fb45bc6sje)。
-   **前置条件**：使用[创建World](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-create-world-api-reference.md)接口返回的 `encryptedWorldId` 删除。
    
-   **调用方**：您的服务端调用。本接口不接受请求体字段 `userAgent`。
    

## HTTP调用

#### 新加坡

`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/worlds/delete`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

#### 美国（弗吉尼亚）

`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/worlds/delete`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

#### 请求参数

删除World

```
curl --location 'https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/worlds/delete' \
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

要删除的 Directing 加密 World ID。由[创建World](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-create-world-api-reference.md)接口返回。

#### 响应参数

删除成功

```
{
    "code": 0,
    "message": null,
    "data": {
        "encryptedWorldId": "enc_a1b2****",
        "deleted": true
    }
}
```

World 已不存在

```
{
    "code": 0,
    "message": null,
    "data": {
        "encryptedWorldId": "enc_a1b2****",
        "deleted": false
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

**encryptedWorldId** `string`

请求中的加密 World ID。

**deleted** `boolean`

`true` 表示已删除；`false` 表示本次未删除到 World。

## 前置状态与调用注意事项

-   同账号下 World 已不存在时返回 `code=0` 且 `deleted=false`，不返回 `403001`。
-   ID 可解析但跨账号、workspace 不匹配或资源不是 Directing World 时，返回 `403001`。
-   删除后继续查询该 World 时，按不存在或已删除资源处理。

## 错误码

如果模型调用失败并返回报错信息，请参见[HappyOyster 错误码](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-error-code.md)进行解决。

## 下一步

-   [查询World列表](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-query-world-list-api-reference.md)：查看剩余 Directing World。
-   [创建World](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-create-world-api-reference.md)：创建新的 Directing World。
