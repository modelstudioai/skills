# HappyOyster-Adventure-查询World列表 API参考

分页查询当前主账号名下的 Adventure World。接口自动按模型隔离，不会返回 Directing 或 Acting World。

## 适用范围

分页查询当前主账号名下的 Adventure World。调用前请确认以下事项：

-   **鉴权要求**：仅支持**主 API Key**调用，临时 API Key 不可用（错误码 `403003`）。
    
    -   获取主 API Key：[获取与配置 API Key](https://help.aliyun.com/zh/model-studio/get-api-key#c38fb45bc6sje)。
-   **调用方**：您的服务端调用。
    

## HTTP调用

#### 华北2（北京）

`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-adventure/openapi/v1/worlds`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

#### 新加坡

`GET https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-adventure/openapi/v1/worlds`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

#### 美国（弗吉尼亚）

`GET https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-adventure/openapi/v1/worlds`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

#### 请求参数

#### 查询World列表

```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-adventure/openapi/v1/worlds?page=1&pageSize=20&status=ready' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

**Authorization** `string` **（必选）**

API Key 鉴权。仅支持**主 API Key**，以 `sk-` 开头，如 `sk-xxx`。通常配置为环境变量 `$DASHSCOPE_API_KEY`。临时 API Key（`st-` 开头）调用返回 `403003`。

##### Query 参数

**page** `integer` **（可选）**

页码，默认 `1`。`page <= 0` 时按 `1` 处理。

**pageSize** `integer` **（可选）**

每页条数，默认 `20`。`pageSize <= 0` 时按 `20`，大于 `100` 时按 `100` 处理。

**status** `string` **（可选）**

按构建状态筛选。未知值不筛选。可选值：

-   `generating`：构建中
-   `ready`：就绪
-   `failed`：构建失败

**mode** `integer` **（可选）**

无需传入。列表已按 Adventure 模型过滤，`items[].mode` 恒为 `1`。若仍传入且非 `1` 返回 `400000`。

#### 响应参数

#### 查询成功

```
{
    "code": 0,
    "message": null,
    "data": {
        "items": [
            {
                "encryptedWorldId": "enc_a1b2****",
                "name": "赛博朋克侦探世界",
                "status": "ready",
                "mode": 1,
                "previewUrl": null,
                "createdAt": "2026-06-03T10:00:00Z",
                "perspective": "first_person",
                "creationModel": "simple",
                "uploadMode": "first_frame"
            }
        ],
        "pagination": {
            "page": 1,
            "pageSize": 20,
            "total": 1,
            "hasMore": false
        }
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

**items** `array`

当前页 World 列表；无结果时为空数组。每项含 `encryptedWorldId`、`name`、`status`（`generating` / `ready` / `failed`）、`mode`（恒为 `1`）、`previewUrl`（通常为 `null`）、`createdAt`、`perspective`（`first_person` / `third_person`）、`creationModel`（恒为 `simple`）、`uploadMode`（固定为 `first_frame`）。

**pagination** `object`

分页信息。含 `page`、`pageSize`、`total`、`hasMore`（`page × pageSize < total` 时为 `true`）。

## 前置状态与调用注意事项

-   列表项是轻量快照，不返回图片、Prompt、`refWorldId` 或其它完整创建参数；需要完整配置时调用[查询World详情](raw/_short/happyoyster-adventure-query-world-detail-api-ref-f8cbdb13a8e701d5.md)。
-   未知 `status` 不会报错，而是按不筛选状态处理。
-   翻页时应使用响应中的 `pagination.pageSize` 和 `hasMore`，不要假设请求值一定原样采用。
-   空结果不是错误，返回 `items=[]` 和对应分页信息。

## 错误码

如果模型调用失败并返回报错信息，请参见[HappyOyster 错误码](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-error-code.md)进行解决。

## 下一步

-   [查询World详情](raw/_short/happyoyster-adventure-query-world-detail-api-ref-f8cbdb13a8e701d5.md)：查看单个 World 完整元数据。
-   [删除World](raw/_short/happyoyster-adventure-delete-world-api-reference-55040f62da8f233e.md)：删除不再使用的 World。
