# HappyOyster-Acting-查询World构建状态 API参考

查询 Acting World 的构建进度。接口返回加密 World ID、构建状态和首帧 URL，客户端轮询直至 World 进入 ready。

## 适用范围

查询 Acting World 的构建进度。调用前请确认以下事项：

-   **鉴权要求**：**不强制主 API Key**，主 API Key 或临时 API Key 均可调用。获取方式请参见[获取鉴权凭证](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-quick-start/happyoyster-auth-setup.md)。
-   **前置条件**：使用[创建World](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference/happyoyster-acting-create-world-api-reference.md)接口返回的 `encryptedWorldId` 查询。可从 `generating` 状态开始查询，不要求 World 已构建完成。
-   **调用方**：您的服务端或客户端均可调用。

## HTTP调用

#### 新加坡

`GET https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-acting/openapi/v1/worlds/build-status`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

#### 美国（弗吉尼亚）

`GET https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-acting/openapi/v1/worlds/build-status`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

#### 请求参数

#### 查询World构建状态

```
curl --location 'https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-acting/openapi/v1/worlds/build-status?encryptedWorldId={encryptedWorldId}' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

**Authorization** `string` **（必选）**

API Key 鉴权。不强制主 API Key，主 API Key 或临时 API Key 均可调用。

-   **主 API Key**：以 `sk-` 开头，如 `sk-xxx`。通常配置为环境变量 `$DASHSCOPE_API_KEY`。
-   **临时 API Key**：以 `st-` 开头，如 `st-xxx`。

##### Query 参数

**encryptedWorldId** `string` **（必选）**

[创建World](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference/happyoyster-acting-create-world-api-reference.md)接口返回的 Acting 加密 World ID。

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
        "firstFrame": "https://cdn.happyoyster.com/frames/acting_world_xyz789.jpg",
        "name": "深夜视频通话",
        "mode": 3
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

Acting 恒为 `3`。仅 `status=ready` 时返回。

## 前置状态与调用注意事项

-   建议每 3–5 秒轮询，直到 `status` 为 `ready` 或 `failed`。
-   只有 `ready` 的 World 才能[换取体验凭证](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference/happyoyster-acting-get-travel-credential-api-reference.md)并[进入房间](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference/happyoyster-acting-enter-travel-api-reference.md)。
-   URL 图片在异步转存后校验失败时，World 可能从 `generating` 进入 `failed`。
-   本接口不返回 `aspectRatio`；播放器方向以[进入房间](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference/happyoyster-acting-enter-travel-api-reference.md)响应中的 `aspectRatio` 为准。

## 错误码

如果模型调用失败并返回报错信息，请参见[HappyOyster 错误码](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-error-code.md)进行解决。

## 下一步

World 进入 `ready` 后可进行以下操作：

-   [获取体验凭证](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference/happyoyster-acting-get-travel-credential-api-reference.md)：换取一次性 `ticket`。
-   [查询World详情](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-acting-openapi-reference/happyoyster-acting-query-world-detail-api-reference.md)：查询完整创建元数据。
