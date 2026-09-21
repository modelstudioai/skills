# HappyOyster-Directing-发送过程指令 API参考

向普通模式 Travel 发送一条文本指令，驱动后续画面生成。仅 creationModel=simple 支持；scriptlist Travel 应使用剧本全量更新。

## 适用范围

向普通模式（`creationModel=simple`）Travel 发送一条文本指令，驱动后续画面生成。调用前请确认以下事项：

-   **鉴权要求**：**不强制主 API Key**，主 API Key 或临时 API Key 均可调用。获取方式请参见[获取鉴权凭证](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-quick-start/happyoyster-auth-setup.md)。
-   **前置条件**：Travel 的 `creationModel` 必须为 `simple`，状态需可接收指令。可通过[查询Travel状态](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-query-travel-status-api-reference.md)接口确认。
-   **调用方**：您的服务端或客户端均可调用。

## HTTP调用

#### 新加坡

`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/instruct`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

#### 美国（弗吉尼亚）

`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/instruct`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

#### 请求参数

#### 发送过程指令

```
curl --location 'https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-directing/openapi/v1/travels/instruct' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "encryptedTravelId": "{encryptedTravelId}",
    "content": "突然出现一只巨大的机器恐龙",
    "clientRequestId": "instruction_20260909_001",
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

要控制的 Directing 加密 Travel ID，`creationModel` 必须为 `simple`。由[客户端进入房间](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-enter-travel-api-reference.md)接口返回。

**content** `string` **（必选）**

文本过程指令。非空，最长 2000 字；为空或超过 2000 字返回 `400000`。

**clientRequestId** `string` **（可选）**

指令重试幂等键。同一条指令重试时复用同值，以避免重复计费。推荐格式 `[A-Za-z0-9_-]{1,32}`。

-   缺省或格式不合法不会返回参数错误：服务端会回退使用网关 `request_id`，仍不可用时使用随机幂等键
-   该字段只用于计费去重，不保证指令处理本身只执行一次

**userAgent** `string` **（可选）**

SDK 或客户端版本标识。非空字符串，优先于 HTTP `User-Agent`。

#### 响应参数

#### 指令已接受

```
{
    "code": 0,
    "message": null,
    "data": {
        "encryptedTravelId": "trvl_a1b2****",
        "content": "突然出现一只巨大的机器恐龙",
        "accepted": true
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

**content** `string`

已接受的指令文本。

**accepted** `boolean`

是否已接受指令并进入处理流程。

## 前置状态与调用注意事项

-   仅 `creationModel=simple` 支持本接口；`scriptlist` Travel 应使用[剧本全量更新](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-update-script-api-reference.md)，误调用 `instruct` 返回 `403006`。
-   Travel 当前状态必须可接收指令；已结束或失败的 Travel 不可写。
-   `content` 为空或超过 2000 字时返回 `400000`。
-   建议每次逻辑指令生成稳定的 `clientRequestId`，重试时复用。
-   指令未通过内容安全策略时返回 `403004`。

## 错误码

如果模型调用失败并返回报错信息，请参见[HappyOyster 错误码](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-error-code.md)进行解决。

## 下一步

发送指令后：

-   [查询Travel状态](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-query-travel-status-api-reference.md)：查看指令执行状态和章节信息。
-   [暂停Travel](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-pause-travel-api-reference.md) / [恢复Travel](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-resume-travel-api-reference.md) / [回溯Travel](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-rewind-travel-api-reference.md)。
-   [结束Travel](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-directing-openapi-reference/happyoyster-directing-end-travel-api-reference.md)：结束会话并处理产物。
