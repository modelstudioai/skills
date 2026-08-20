# 查询模型限额

调用 GET /api/v1/models/limits 接口查询当前 API Key 下各模型的限流配额，包括请求频率限制和用量限制，用于了解和规划 API 调用量。

## 前提条件

已创建 API Key 并配置为环境变量 `DASHSCOPE_API_KEY`。配置方法请参见[配置API Key到环境变量](raw/model-api-reference/preparations/get-api-key.md)。

## 请求说明

-   **HTTP 方法**：GET
    
-   **请求地址**
    
    > 调用时请将 `{WorkspaceId}` 替换为您的业务空间 ID。
    
    **地域**
    
    **Endpoint**
    
    华北2（北京）
    
    `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/models/limits`
    
-   **认证方式**
    
    在请求 Header 中设置 `Authorization: Bearer {API_KEY}`。
    

## 请求参数

所有参数均通过 Query String 传递。

**参数**

**类型**

**必选**

**描述**

name

String

否

按模型名称进行模糊搜索。示例：`qwen`

model

String

否

按模型 ID 进行精确查询。示例：`qwen3-max`

page\_no

Integer

否

页码，从 1 开始。默认值：`1`。

page\_size

Integer

否

每页返回的模型数量。默认值：`20`。

## 返回参数

**参数**

**类型**

**描述**

request\_id

String

请求 ID，用于问题排查。

output.total

Number

符合条件的模型总数。

output.page\_no

Number

当前页码。

output.page\_size

Number

每页条数。

output.quotas\[\].model

String

模型 ID。

output.quotas\[\].workspace\_id

String

业务空间 ID。

output.quotas\[\].model\_limit

Object

账号级别限流，即该模型在当前账号下的总限流上限。包含以下字段：

-   `request_limit`（Number）：请求频率限制值。
    
-   `request_limit_period`（Number）：请求限流的时间周期，单位秒。值为 `60` 表示每分钟（RPM），值为 `1` 表示每秒（QPS）。
    
-   `usage_limit`（Number）：用量限制数。值为 `null` 表示无用量限制。
    
-   `usage_limit_field`（String）：用量限制类型，如 `total_tokens`。
    
-   `usage_limit_period`（Number）：用量限制的时间周期，单位秒。
    
-   `async_user_queue_limit`（Number）：异步任务排队数上限。
    
-   `async_user_concurrency_limit`（Number）：异步任务最大并发数。
    

output.quotas\[\].workspace\_limit

Object

业务空间级别限流。您可以为每个业务空间单独设置限流，但所有业务空间的总限流不能超过 `model_limit`。值为 `null` 表示未设置业务空间级别限制。包含的字段与 `model_limit` 相同。

## 请求示例

**示例一：查询所有模型的限额**
```
curl "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/models/limits?page_no=1&page_size=100" \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header "Content-Type: application/json"
```
**示例二：查询特定模型的限额**
```
curl "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/models/limits?model=qwen3-max" \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header "Content-Type: application/json"
```

## 返回示例

```
{
    "code": null,
    "message": null,
    "success": true,
    "output": {
        "total": 453,
        "page_no": 1,
        "page_size": 10,
        "quotas": [
            {
                "model": "qwen3-max",
                "workspace_id": "llm-8l75168qayuhsr3o",
                "model_limit": {
                    "request_limit": 500,
                    "request_limit_period": 1,
                    "usage_limit": 500000,
                    "usage_limit_field": "total_tokens",
                    "usage_limit_period": 6,
                    "async_user_queue_limit": null,
                    "async_user_concurrency_limit": null
                },
                "workspace_limit": null
            },
            {
                "model": "wan2.6-i2v-flash",
                "workspace_id": "llm-8l75168qayuhsr3o",
                "model_limit": {
                    "request_limit": 5,
                    "request_limit_period": 1,
                    "usage_limit": null,
                    "usage_limit_field": null,
                    "usage_limit_period": null,
                    "async_user_queue_limit": 500,
                    "async_user_concurrency_limit": 5
                },
                "workspace_limit": null
            },
            {
                "model": "qwen-image-max",
                "workspace_id": "llm-8l75168qayuhsr3o",
                "model_limit": {
                    "request_limit": 2,
                    "request_limit_period": 60,
                    "usage_limit": 1000000,
                    "usage_limit_field": "total_tokens",
                    "usage_limit_period": 60,
                    "async_user_queue_limit": null,
                    "async_user_concurrency_limit": null
                },
                "workspace_limit": null
            }
        ]
    },
    "request_id": "2043b55f-f0d2-95ee-a449-234e1ee57042"
}
```

以上示例中：

-   `qwen3-max`：每秒最多 500 次请求，每 6 秒最多使用 500,000 Token，未设置业务空间级别限制。
-   `wan2.6-i2v-flash`：每秒最多 5 次请求，无用量限制，异步任务最大排队数 500、最大并发数 5。
-   `qwen-image-max`：每分钟最多 2 次请求，每分钟最多使用 1,000,000 Token，未设置业务空间级别限制。

## 错误码

如果调用失败，会返回错误信息。更多错误码及解决方法，请参见[错误信息](raw/model-api-reference/preparations/error-code.md)。
