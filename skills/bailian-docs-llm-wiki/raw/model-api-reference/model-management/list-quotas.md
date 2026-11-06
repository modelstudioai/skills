# 查询模型限额

查询模型的账号级和业务空间级限流配额，包括请求频率、用量及异步任务排队和并发限制，支持按模型名称或模型 ID 筛选及分页查询。

## 请求说明

调用时请将 `{WorkspaceId}` 替换为业务空间 ID，并在请求 Header 中设置 `Authorization: Bearer YOUR_API_KEY`，其中 `YOUR_API_KEY` 需替换为在[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key)获取的 API Key。

#### 华北2（北京）

GET`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/models/limits`

#### 新加坡

GET`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/models/limits`

#### 中国香港

GET`https://{WorkspaceId}.cn-hongkong.maas.aliyuncs.com/api/v1/models/limits`

#### 日本（东京）

GET`https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/api/v1/models/limits`

#### 德国（法兰克福）

GET`https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1/models/limits`

#### 美国（弗吉尼亚）

GET`https://dashscope-us.aliyuncs.com/api/v1/models/limits`

所有参数均通过 Query String 传递。

`name`String可选

按模型名称进行模糊搜索。示例：`qwen`

`model`String可选

按模型 ID 进行精确查询。示例：`qwen3.8-max`

`page_no`Integer可选

页码，从 1 开始。默认值：`1`。

`page_size`Integer可选

每页返回的模型数量。默认值：`20`。

#### 所有模型

```
curl "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/models/limits?page_no=1&page_size=100" \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header "Content-Type: application/json"
```

#### 指定模型

```
curl "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/models/limits?model=qwen3.8-max" \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header "Content-Type: application/json"
```

## 返回说明

`request_id`String

请求 ID，用于问题排查。

`output.total`Number

符合条件的模型总数。

`output.page_no`Number

当前页码。

`output.page_size`Number

每页条数。

`output.quotas[]`Array\[Object\]

模型限流配额列表，每个元素为一个模型的限流配额。

`model`String

模型 ID。

`workspace_id`String

业务空间 ID。

`model_limit`Object | null

账号级别限流，即该模型在当前账号下的总限流上限。可能为 `null`；非 `null` 时包含以下字段。

`request_limit`Number

请求频率限制值。

`request_limit_period`Number

请求限流的时间周期，单位秒。值为 `60` 表示每分钟（RPM），值为 `1` 表示每秒（QPS）。

`usage_limit`Number

用量限制数。值为 `null` 表示无用量限制。

`usage_limit_field`String

用量限制类型，如 `total_tokens`。

`usage_limit_period`Number

用量限制的时间周期，单位秒。

`async_user_queue_limit`Number

异步任务排队数上限。

`async_user_concurrency_limit`Number

异步任务最大并发数。

`workspace_limit`Object

业务空间级别限流。您可以为每个业务空间单独设置限流，但所有业务空间的总限流不能超过 `model_limit`。值为 `null` 表示未设置业务空间级别限制。包含的字段与 `model_limit` 相同。

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
                "model": "qwen3.8-max",
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
                "model": "qwen-image-3.0-pro",
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

-   `qwen3.8-max`：每秒最多 500 次请求，每 6 秒最多使用 500,000 Token，未设置业务空间级别限制。
-   `wan2.6-i2v-flash`：每秒最多 5 次请求，无用量限制，异步任务最大排队数 500、最大并发数 5。
-   `qwen-image-3.0-pro`：每分钟最多 2 次请求，每分钟最多使用 1,000,000 Token，未设置业务空间级别限制。

## 错误码

如果调用失败，会返回错误信息。更多错误码及解决方法，请参见[错误信息](raw/model-api-reference/preparations/error-code.md)。
