# 查询模型授权

调用 GET /api/v1/models/permissions 接口查询当前业务空间下可授权或已授权的模型列表及其权限明细。

## 前提条件

已创建 API Key 并配置为环境变量 `DASHSCOPE_API_KEY`。配置方法请参见[配置API Key到环境变量](raw/model-api-reference/preparations/get-api-key.md)。

## 请求说明

-   **HTTP 方法**：GET
    
-   **请求地址**
    
    > 调用时请将 `{WorkspaceId}` 替换为您的业务空间 ID。
    
    **地域**
    
    **Endpoint**
    
    华北2（北京）
    
    `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/models/permissions`
    
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

模型名称模糊搜索，对 `name` 与 `model_id` 做模糊匹配。示例：`qwen`

model

String

否

模型 ID 精确查询，对 `model_id` 做精确匹配。示例：`qwen-plus`

page\_no

Integer

否

页码，正整数，从 1 开始。默认值：`1`。

page\_size

Integer

否

每页数量，取值范围 1~200，最大 200。默认值：`20`。

authorization\_scope

String

否

授权范围筛选。可选值：

-   `AUTHORIZABLE`：可授权的模型（默认）。
    
-   `AUTHORIZED`：已授权的模型。
    

默认值：`AUTHORIZABLE`。示例：`AUTHORIZED`

action

String

否

权限动作维度。可选值：`INFERENCE`\-推理（当前仅支持此值）。仅在 `authorization_scope=AUTHORIZED` 时驱动过滤维度。默认值：`INFERENCE`。

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

output.total

Number

总数。示例：`5`

output.page\_no

Number

页码。示例：`1`

output.page\_size

Number

每页数量。示例：`20`

output.permissions

Array\[Object\]

权限列表，见返回示例。

output.model

String

模型 ID。示例：`qwen-plus`

output.name

String

模型展示名。示例：`通义千问-Plus`

output.permissions\[\].permissions

Object

权限明细。示例：`{"inference":true,"fine_tune":false,"deploy":false}`。包含以下字段：

-   `inference`（Boolean）：是否具备模型调用权限。示例：`true`
    
-   `fine_tune`（Boolean）：是否具备模型训练权限。示例：`false`
    
-   `deploy`（Boolean）：是否具备模型部署权限。示例：`false`
    

## 请求示例

```
curl "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/models/permissions?authorization_scope=AUTHORIZED&action=INFERENCE&page_no=1&page_size=20" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json'
```

## 返回示例

```
{
    "code": null,
    "message": null,
    "success": true,
    "output": {
        "total": 3,
        "page_no": 1,
        "page_size": 20,
        "permissions": [
            {
                "model": "qwen-plus",
                "name": "通义千问-Plus",
                "permissions": {
                    "inference": true,
                    "fine_tune": false,
                    "deploy": false
                }
            },
            {
                "model": "qwen3-max",
                "name": "通义千问3-Max",
                "permissions": {
                    "inference": true,
                    "fine_tune": true,
                    "deploy": false
                }
            },
            {
                "model": "qwen-turbo",
                "name": "通义千问-Turbo",
                "permissions": {
                    "inference": true,
                    "fine_tune": false,
                    "deploy": false
                }
            }
        ]
    },
    "request_id": "d5f5201f-ee7a-9e3d-8569-bc0eedec21f9"
}
```

## 错误码

如果调用失败，会返回错误信息。更多错误码及解决方法，请参见[错误信息](raw/model-api-reference/preparations/error-code.md)。
