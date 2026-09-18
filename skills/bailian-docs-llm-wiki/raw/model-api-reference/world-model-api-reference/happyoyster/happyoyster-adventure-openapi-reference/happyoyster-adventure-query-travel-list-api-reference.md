# HappyOyster-Adventure-查询Travel列表 API参考

分页查询当前主账号名下的 Adventure Travel，可按状态或关联 World 筛选。

## 适用范围

分页查询当前主账号名下的 Adventure Travel，可按状态或关联 World 筛选。调用前请确认以下事项：

-   **鉴权要求**：仅支持**主 API Key**调用，临时 API Key 不可用（错误码 `403003`）。
    
    -   获取主 API Key：[获取与配置 API Key](https://help.aliyun.com/zh/model-studio/get-api-key#c38fb45bc6sje)。
-   **调用方**：您的服务端调用。
    

## HTTP调用

#### 华北2（北京）

`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-adventure/openapi/v1/travels`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

#### 新加坡

`GET https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-adventure/openapi/v1/travels`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

#### 美国（弗吉尼亚）

`GET https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-adventure/openapi/v1/travels`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

#### 请求参数

查询Travel列表

```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v2/apps/happyoyster-1.0-adventure/openapi/v1/travels?page=1&pageSize=20&status=completed&encryptedWorldId={encryptedWorldId}' \
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

按 Travel 状态筛选。未知值不筛选。可选值：

-   `init`：正在初始化会话资源
-   `pending`：排队或等待服务资源
-   `running`：正在运行
-   `failed`：Travel 失败
-   `completed`：Travel 已结束，可查询产物

**encryptedWorldId** `string` **（可选）**

当前主账号名下的 Adventure World ID。传入时仅返回该 World 的 Travel。本接口不支持 `mode` Query 参数，模型专属入口会自动限定为 Adventure。

#### 响应参数

查询成功

```
{
    "code": 0,
    "message": null,
    "data": {
        "items": [
            {
                "encryptedTravelId": "trvl_a1b2****",
                "status": "completed",
                "mode": 1,
                "encryptedWorldId": "enc_a1b2****",
                "durationSec": 90,
                "createdAt": "2026-06-03T10:00:00Z",
                "endedAt": "2026-06-03T10:01:30Z"
            },
            {
                "encryptedTravelId": "trvl_g7h8****",
                "status": "running",
                "mode": 1,
                "encryptedWorldId": "enc_a1b2****",
                "durationSec": null,
                "createdAt": "2026-06-03T11:00:00Z",
                "endedAt": null
            }
        ],
        "pagination": {
            "page": 1,
            "pageSize": 20,
            "total": 2,
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

当前页 Travel 列表；无结果时为空数组。每项含 `encryptedTravelId`、`status`、`mode`（恒为 `1`）、`encryptedWorldId`、`durationSec`（进行中、失败或时长尚不可用时为 `null`）、`createdAt`、`endedAt`（进行中时为 `null`）。

**pagination** `object`

分页信息。含 `page`、`pageSize`、`total`、`hasMore`。

## 前置状态与调用注意事项

-   接口自动只返回 Adventure Travel，`items[].mode` 恒为 `1`。
-   使用 `encryptedWorldId` 筛选时，该 World 必须属于当前主账号和 Adventure 模型；其它模型的 World 返回 `403001`。
-   进行中 Travel 的 `durationSec` 和 `endedAt` 通常为 `null`。
-   未知 `status` 不会报错，而是按不筛选状态处理。
-   空结果不是错误，返回 `items=[]` 和对应分页信息。

## 错误码

如果模型调用失败并返回报错信息，请参见[HappyOyster 错误码](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-error-code.md)进行解决。

## 下一步

-   [查询Travel状态](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference/happyoyster-adventure-query-travel-status-api-reference.md)：查询单个 Travel 的实时状态。
-   [查询Travel产物](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-adventure-openapi-reference/happyoyster-adventure-query-travel-artifacts-api-reference.md)：查询已完成 Travel 的视频产物。
