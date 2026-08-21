# 更新模型授权

调用 POST /api/v1/models/permissions 接口更新指定业务空间下模型的授权（推理 / 微调 / 部署），支持逐模型授权与"一键授权"两种模式。

## 前提条件

已创建 API Key 并配置为环境变量 `DASHSCOPE_API_KEY`。配置方法请参见[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

## 请求说明

-   **HTTP 方法**：POST
    
-   **请求地址**
    
    > 调用时请将 `{WorkspaceId}` 替换为您的业务空间 ID。
    
    **地域**
    
    **Endpoint**
    
    华北2（北京）
    
    `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/models/permissions`
    
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

条件必填

逐模型授权项列表。当 `access_all_entities` 为 `OPEN`/`CLOSE` 时可空；为 `KEEP` 或不传时必填，且数量需为 1~20。示例：`[{"model":"qwen-plus","inference":true}]`

models\[\].model

String

是

模型 ID，不能为空。如 `qwen-plus`、`qwen3-max`。

models\[\].inference

Boolean

否

模型调用权限。`true`\=授权推理，`false`\=取消授权，不传=保持现状。默认值：null（不变更）。

models\[\].finetune

Boolean

否

模型训练权限。`true`\=授权微调，`false`\=取消，不传=保持现状。默认值：null（不变更）。

models\[\].deploy

Boolean

否

模型部署权限。`true`\=授权部署，`false`\=取消，不传=保持现状。默认值：null（不变更）。

access\_all\_entities

String

否

一键授权开关。可选值：

-   `OPEN`：一键授权当前空间全部推理模型（含后续新增）。
    
-   `CLOSE`：取消一键授权并清空历史推理授权。
    
-   `KEEP`：保持原逐模型授权行为（缺省）。
    

传 `OPEN`/`CLOSE` 时 `models` 可不填。默认值：`KEEP`。示例：`OPEN`

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

## 请求示例

**示例一：逐模型授权**

```
curl -X POST "https://dashscope.aliyuncs.com/api/v1/models/permissions" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json' \
    --data '{
        "models": [
            {"model": "qwen-plus", "inference": true, "fine_tune": true, "deploy": false},
            {"model": "qwen3-max", "inference": true}
        ]
    }'
```

**示例二：一键授权**

```
curl -X POST "https://dashscope.aliyuncs.com/api/v1/models/permissions" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json' \
    --data '{"access_all_entities": "OPEN"}'
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
    "message": "Model qwen-xxx is not authorized for Inference",
    "success": false,
    "output": null,
    "request_id": "d5f5201f-ee7a-9e3d-8569-bc0eedec21f9"
}
```

## 错误码

如果调用失败，会返回错误信息。更多错误码及解决方法，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。
