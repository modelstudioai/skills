# HappyOyster-Adventure-查询World构建状态 API参考

查询 Adventure World 的构建进度。接口返回加密 World ID、构建状态和首帧 URL，客户端轮询直至 World 进入 ready。

## 适用范围

查询 Adventure World 的构建进度。调用前请确认以下事项：

-   **鉴权要求**：**不强制主 API Key**，主 API Key 或临时 API Key 均可调用。获取方式请参见[获取鉴权凭证](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-quick-start/happyoyster-auth-setup.md)。
-   **前置条件**：使用[创建World](raw/_short/happyoyster-adventure-create-world-api-reference-b764ec539142394b.md)接口返回的 `encryptedWorldId` 查询。可从 `generating` 状态开始查询。
-   **调用方**：您的服务端或客户端均可调用。

## HTTP调用

#### 华北2（北京）

`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-adventure/openapi/v1/worlds/build-status`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

#### 新加坡

`GET https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-adventure/openapi/v1/worlds/build-status`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

#### 美国（弗吉尼亚）

`GET https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-adventure/openapi/v1/worlds/build-status`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

#### 请求参数

#### 查询World构建状态

```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-adventure/openapi/v1/worlds/build-status?encryptedWorldId={encryptedWorldId}' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

**Authorization** `string` **（必选）**

API Key 鉴权。不强制主 API Key，主 API Key 或临时 API Key 均可调用。

-   **主 API Key**：以 `sk-` 开头，如 `sk-xxx`。
-   **临时 API Key**：以 `st-` 开头，如 `st-xxx`。

##### Query 参数

**encryptedWorldId** `string` **（必选）**

[创建World](raw/_short/happyoyster-adventure-create-world-api-reference-b764ec539142394b.md)接口返回的加密 World ID，由服务端加密生成，无需自行解密。

#### 响应参数

#### 构建中

```
{
    "code": 0,
    "message": null,
    "data": {
        "encryptedWorldId": "enc_a1b2****",
        "status": "generating",
        "firstFrame": null
    }
}
```

#### 构建完成

```
{
    "code": 0,
    "message": null,
    "data": {
        "encryptedWorldId": "enc_a1b2****",
        "status": "ready",
        "firstFrame": "https://cdn.happyoyster.com/frames/world_xyz789.jpg",
        "name": "赛博朋克侦探世界",
        "mode": 1
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

加密 World ID。

**status** `string`

构建状态：

-   `generating`：构建中
-   `ready`：就绪，可换取体验凭证并进房
-   `failed`：构建失败

**firstFrame** `string`

World 首帧 URL；尚未生成或构建失败时为 `null`。

**name** `string`

World 名称。仅 `status=ready` 时返回。

**mode** `integer`

Adventure 恒为 `1`。仅 `status=ready` 时返回。

## 前置状态与调用注意事项

-   建议每 3–5 秒轮询，直到 `status` 为 `ready` 或 `failed`。
-   只有 `ready` 的 World 才能[换取体验凭证](raw/_short/happyoyster-adventure-get-travel-credential-api--d269f4908c7288f2.md)并[进入房间](raw/_short/happyoyster-adventure-enter-travel-api-reference-3eb107188008bbaf.md)。
-   URL 图片在异步转存后校验失败时，World 可能从 `generating` 进入 `failed`。
-   本接口不返回 `aspectRatio`；需要 `perspective`、`uploadMode` 等创建元数据时，请调用[查询World详情](raw/_short/happyoyster-adventure-query-world-detail-api-ref-f8cbdb13a8e701d5.md)。

## 错误码

如果模型调用失败并返回报错信息，请参见[HappyOyster 错误码](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-error-code.md)进行解决。

## 下一步

World 进入 `ready` 后：

-   [获取体验凭证](raw/_short/happyoyster-adventure-get-travel-credential-api--d269f4908c7288f2.md)：换取一次性 `ticket`。
-   [查询World详情](raw/_short/happyoyster-adventure-query-world-detail-api-ref-f8cbdb13a8e701d5.md)：查询完整创建元数据。
