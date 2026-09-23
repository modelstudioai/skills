# HappyOyster-Acting-查询World详情 API参考

查询单个 Acting World 的完整元数据和可回显创建参数。构建进度轮询请使用查询World构建状态接口。

## 适用范围

查询单个 Acting World 的完整元数据和可回显创建参数。调用前请确认以下事项：

-   **鉴权要求**：仅支持**主 API Key**调用，临时 API Key 不可用（错误码 `403003`）。
    
    -   获取主 API Key：[获取与配置 API Key](https://help.aliyun.com/zh/model-studio/get-api-key#c38fb45bc6sje)。
-   **前置条件**：使用[创建World](raw/_short/happyoyster-acting-create-world-api-reference-47f1f4ec26522c7d.md)接口返回的 `encryptedWorldId` 查询。构建进度轮询应使用[查询World构建状态](raw/_short/happyoyster-acting-query-world-build-status-api--5436f98af63bbe85.md)。
    
-   **调用方**：您的服务端调用。
    

## HTTP调用

#### 新加坡

`GET https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-acting/openapi/v1/worlds/detail`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

#### 美国（弗吉尼亚）

`GET https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-acting/openapi/v1/worlds/detail`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

#### 请求参数

#### 查询World详情

```
curl --location 'https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-acting/openapi/v1/worlds/detail?encryptedWorldId={encryptedWorldId}' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

**Authorization** `string` **（必选）**

API Key 鉴权。仅支持**主 API Key**，以 `sk-` 开头，如 `sk-xxx`。通常配置为环境变量 `$DASHSCOPE_API_KEY`。临时 API Key（`st-` 开头）调用返回 `403003`。

##### Query 参数

**encryptedWorldId** `string` **（必选）**

当前主账号名下的 Acting 加密 World ID。由[创建World](raw/_short/happyoyster-acting-create-world-api-reference-47f1f4ec26522c7d.md)接口返回。

#### 响应参数

```
{
    "code": 0,
    "message": null,
    "data": {
        "encryptedWorldId": "enc_a1b2****",
        "name": "深夜视频通话",
        "status": "ready",
        "mode": 3,
        "creationModel": "simple",
        "prompt": "深夜视频通话中，一位安静的女孩微笑着回应镜头",
        "eventStyle": "first_frame",
        "perspective": null,
        "uploadMode": "first_frame",
        "resolution": "480p",
        "aspectRatio": "9:16",
        "layout": null,
        "narrative": null,
        "refWorldId": null,
        "firstFrameImage": {
            "url": "https://cdn.happyoyster.com/frames/portrait-call.jpg",
            "referenceType": "default"
        },
        "inputImages": null,
        "sceneImage": null,
        "roleImage": null,
        "scenePrompt": null,
        "rolePrompt": null,
        "scriptList": null,
        "previewUrl": null,
        "createdAt": "2026-09-09T08:00:00Z",
        "updatedAt": "2026-09-09T08:05:00Z"
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

**name** `string`

World 名称。

**status** `string`

构建状态：`generating` / `ready` / `failed`。

**mode** `integer`

Acting 恒为 `3`。

**creationModel** `string`

Acting 恒为 `simple`。

**prompt** `string`

创建时提交的顶层 Prompt。

**eventStyle** `string`

兼容返回字段；合规创建省略该字段时，服务端通常按 `uploadMode` 映射并回显 `first_frame`。它不是 Acting 的创建参数，客户端不应主动回传。

**perspective** `null`

Acting 不接受视角创建参数，固定为 `null`。

**uploadMode** `string`

固定为 `first_frame`。

**resolution** `string`

`480p` / `720p`；创建时未传则为 `480p`。

**aspectRatio** `string`

`9:16` / `16:9`；创建时未传则为 `9:16`。

**layout** `null`

Acting 不接受该创建参数，固定为 `null`。

**narrative** `null`

Acting 不接受该创建参数，固定为 `null`。

**refWorldId** `string`

衍生创建时使用的 Acting 加密参考 World ID；无则为 `null`。

**firstFrameImage** `object`

创建时的必填首帧图；只返回 URL 形式，不回传 base64。含 `url` 和 `referenceType`。

**inputImages** `null`

Acting 当前不使用该字段。

**sceneImage** `null`

Acting 不使用场景角色图片槽位，固定为 `null`。

**roleImage** `null`

Acting 不使用场景角色图片槽位，固定为 `null`。

**scenePrompt** `null`

Acting 不使用场景角色文案，固定为 `null`。

**rolePrompt** `null`

Acting 不使用场景角色文案，固定为 `null`。

**scriptList** `null`

Acting 不支持 ScriptList，固定为 `null`。

**previewUrl** `null`

当前固定为 `null`。

**createdAt** `string`

创建时间，ISO 8601 格式。

**updatedAt** `string`

最近更新时间，ISO 8601 格式。

## 前置状态与调用注意事项

-   本接口可查询 `generating`、`ready` 或 `failed` World；部分构建产物在未就绪时可能为 `null`。
-   详情接口不回显 `async`，因为它是调用行为开关，不是 World 属性。
-   图片只返回 URL 和 `referenceType`，不会回传创建请求中的 base64 内容。
-   `eventStyle` 通常与 `uploadMode` 同值；客户端应以 `uploadMode` 作为 Acting 创建模式的权威字段。
-   播放器可预先读取 `aspectRatio`，但实际进房时仍应以[进入房间](raw/_short/happyoyster-acting-enter-travel-api-reference-56ea4df0a872fdb7.md)响应值设置方向。
-   查询其它模型、其它主账号或已删除的 World 均返回 `403001`，不会泄漏资源是否存在。

## 错误码

如果模型调用失败并返回报错信息，请参见[HappyOyster 错误码](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-error-code.md)进行解决。

## 下一步

-   [查询World列表](raw/_short/happyoyster-acting-query-world-list-api-referenc-3550b0de031bc3dc.md)：分页查询所有 Acting World。
-   [删除World](raw/_short/happyoyster-acting-delete-world-api-reference-e7a48c5a6f87668c.md)：删除不再使用的 World。
-   World 为 `ready` 时可[获取体验凭证](raw/_short/happyoyster-acting-get-travel-credential-api-ref-dfc7dc5832959ca8.md)。
