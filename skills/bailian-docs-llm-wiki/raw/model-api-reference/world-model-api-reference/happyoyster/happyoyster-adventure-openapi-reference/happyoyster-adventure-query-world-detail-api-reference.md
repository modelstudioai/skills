# HappyOyster-Adventure-查询World详情 API参考

查询单个 Adventure World 的完整元数据和可回显创建参数。构建进度轮询请使用查询World构建状态接口。

## 适用范围

查询单个 Adventure World 的完整元数据和可回显创建参数。调用前请确认以下事项：

-   **鉴权要求**：仅支持**主 API Key**调用，临时 API Key 不可用（错误码 `403003`）。
    
    -   获取主 API Key：[获取与配置 API Key](https://help.aliyun.com/zh/model-studio/get-api-key#c38fb45bc6sje)。
-   **前置条件**：使用[创建World](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference/happyoyster-adventure-create-world-api-reference.md)接口返回的 `encryptedWorldId` 查询。构建进度轮询应使用[查询World构建状态](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference/happyoyster-adventure-query-world-build-status-api-reference.md)。
    
-   **调用方**：您的服务端调用。
    

## HTTP调用

#### 华北2（北京）

`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-adventure/openapi/v1/worlds/detail`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

#### 新加坡

`GET https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-adventure/openapi/v1/worlds/detail`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

#### 美国（弗吉尼亚）

`GET https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-adventure/openapi/v1/worlds/detail`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

#### 请求参数

查询World详情

```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-adventure/openapi/v1/worlds/detail?encryptedWorldId={encryptedWorldId}' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

**Authorization** `string` **（必选）**

API Key 鉴权。仅支持**主 API Key**，以 `sk-` 开头，如 `sk-xxx`。通常配置为环境变量 `$DASHSCOPE_API_KEY`。临时 API Key（`st-` 开头）调用返回 `403003`。

##### Query 参数

**encryptedWorldId** `string` **（必选）**

当前主账号名下的 Adventure 加密 World ID。由[创建World](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference/happyoyster-adventure-create-world-api-reference.md)接口返回。

#### 响应参数

查询成功

```
{
    "code": 0,
    "message": null,
    "data": {
        "encryptedWorldId": "enc_a1b2****",
        "name": "江南雨夜奇遇",
        "status": "ready",
        "mode": 1,
        "creationModel": "simple",
        "prompt": "黄昏的江南水乡，石桥与乌篷船",
        "eventStyle": "normal",
        "perspective": "third_person",
        "uploadMode": "first_frame",
        "resolution": null,
        "aspectRatio": null,
        "layout": null,
        "narrative": null,
        "refWorldId": null,
        "firstFrameImage": {
            "url": "https://cdn.happyoyster.com/frames/jiangnan.jpg",
            "referenceType": "default"
        },
        "inputImages": null,
        "sceneImage": null,
        "roleImage": null,
        "scenePrompt": null,
        "rolePrompt": null,
        "scriptList": null,
        "previewUrl": null,
        "createdAt": "2026-06-03T10:00:00Z",
        "updatedAt": "2026-06-03T10:05:00Z"
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

Adventure 恒为 `1`。

**creationModel** `string`

Adventure 恒为 `simple`。

**prompt** `string`

创建时提交的顶层 Prompt。

**eventStyle** `string`

创建时的事件风格：`normal` / `dramatic` / `regular`。

**perspective** `string`

视角：`first_person` / `third_person`。

**uploadMode** `string`

固定为 `first_frame`。

**resolution** `null`

Adventure 不使用该字段，通常为 `null`。

**aspectRatio** `null`

Adventure 不使用该字段，固定为 `null`。

**layout** `null`

Adventure 不使用该字段，通常为 `null`。

**narrative** `null`

Adventure 不使用该字段，通常为 `null`。

**refWorldId** `string`

衍生创建时使用的加密参考 World ID；无则为 `null`。

**firstFrameImage** `object`

创建时的必填首帧图片；只返回 URL 形式。含 `url` 和 `referenceType`。

**inputImages** `null`

Adventure 当前不使用该字段。

**scriptList** `null`

Adventure 不支持 ScriptList，固定为 `null`。

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
-   查询其它模型、其它主账号或已删除的 World 均返回 `403001`，不会泄漏资源是否存在。

## 错误码

如果模型调用失败并返回报错信息，请参见[HappyOyster 错误码](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-error-code.md)进行解决。

## 下一步

-   [查询World列表](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference/happyoyster-adventure-query-world-list-api-reference.md)：分页查询所有 Adventure World。
-   [删除World](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference/happyoyster-adventure-delete-world-api-reference.md)：删除不再使用的 World。
-   World 为 `ready` 时可[获取体验凭证](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference/happyoyster-adventure-get-travel-credential-api-reference.md)。
