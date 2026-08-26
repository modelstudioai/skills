# 更新模型限流

调用 POST /api/v1/models/limits 接口更新指定业务空间下模型的限流配额（QPM / TPM），支持"合并覆盖"与"删除限流"两种操作。

## 前提条件

已创建 API Key 并配置为环境变量 `DASHSCOPE_API_KEY`。配置方法请参见[配置API Key到环境变量](raw/model-api-reference/preparations/get-api-key.md)。

## 请求说明

-   **HTTP 方法**：POST
    
-   **请求地址**
    
    > 调用时请将 `{WorkspaceId}` 替换为您的业务空间 ID。
    
    **地域**
    
    **Endpoint**
    
    华北2（北京）
    
    `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/models/limits`
    
-   **认证方式**
    
    在请求 Header 中设置 `Authorization: Bearer {API_KEY}`。
    

## 请求参数

所有参数均通过请求 Body 传递。

**参数**

**类型**

**必选**

**描述**

models

Array\[Object\]

是

逐模型限流项列表。必填，数量需为 1~200。示例：`[{"model":"qwen-plus","request_limit":60}]`

models\[\].model

String

是

模型 ID，不能为空。如 `qwen-plus`、`qwen3-max`。

models\[\].operation\_type

String

否

操作类型。可选值：

-   `OVERLAY`：合并覆盖（只覆盖传入字段，未传字段回填当前值）。
    
-   `DELETE`：删除限流（此时限流值字段需全部为空）。
    

默认值：`OVERLAY`。

models\[\].request\_limit

Number

否

请求次数上限（QPM），非负。每分钟最大请求数，单位次/分钟。`operation_type=DELETE` 时必须为空。默认值：null（不变更）。示例：`60`

models\[\].request\_limit\_period

Number

否

请求限流时间周期，正整数，单位秒，如 `60`\=1 分钟。默认值：null（不变更）。

models\[\].usage\_limit

Number

否

用量上限（TPM），非负。每分钟最大 Token 用量。`operation_type=DELETE` 时必须为空。默认值：null（不变更）。示例：`100000`

models\[\].usage\_limit\_period

Number

否

用量限流时间周期，正整数，单位秒，如 `60`\=1 分钟。默认值：null（不变更）。

## 返回参数

**参数**

**类型**

**描述**

request\_id

String

请求 ID。示例：`d5f5201f-ee7a-9e3d-8569-bc0eedec21f9`

code

String

错误码，成功为 `null`。

message

String

错误信息，成功为 `null`。

success

Boolean

是否成功。示例：`true`

output

Object

业务数据，本接口为 `null`。

## TPM 豁免场景

若需"只限制 RPM、豁免 TPM"，推荐两步法——先调用本接口对目标模型传 `{"model":"X","operation_type":"DELETE"}` 删除全部限流，再传 `{"model":"X","operation_type":"OVERLAY","request_limit":60,"request_limit_period":60}` 只设置 QPM。两步非原子，中间有短暂无限制窗口。

## 请求示例

**示例一：设置 QPM=60、TPM=100000**
```
curl -X POST "https://dashscope.aliyuncs.com/api/v1/models/limits" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json' \
    --data '{
        "models": [
            {
                "model": "qwen-plus",
                "operation_type": "OVERLAY",
                "request_limit": 60,
                "request_limit_period": 60,
                "usage_limit": 100000,
                "usage_limit_period": 60
            }
        ]
    }'
```
**示例二：删除限流**
```
curl -X POST "https://dashscope.aliyuncs.com/api/v1/models/limits" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json' \
    --data '{
        "models": [
            {"model": "qwen-plus", "operation_type": "DELETE"}
        ]
    }'
```

## 返回示例

**成功示例**
```
{
    "code": null,
    "message": null,
    "success": true,
    "output": null,
    "request_id": "d5f5201f-ee7a-9e3d-8569-bc0eedec21f9"
}
```
**失败示例**
```
{
    "code": "InvalidParameter",
    "message": "Cannot set TPM without QPM for model qwen-plus: no existing QPM limit, please set QPM first",
    "success": false,
    "output": null,
    "request_id": "d5f5201f-ee7a-9e3d-8569-bc0eedec21f9"
}
```

## 错误码

如果调用失败，会返回错误信息。更多错误码及解决方法，请参见[错误信息](raw/model-api-reference/preparations/error-code.md)。
