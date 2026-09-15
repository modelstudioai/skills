# 图像生成-部署模型

将训练好的图像生成模型发布为在线 API 服务。

## 适用范围

-   **适用地域**：当前模型部署 API **仅在华北2（北京）地域**开放。如您使用其他地域，请通过该地域的百炼控制台完成模型部署操作。
-   **开通账号权限**：若使用[阿里云子账号](raw/model-user-guide/security-and-compliance/permission-management-overview.md)（[RAM用户](https://help.aliyun.com/zh/ram/user-guide/overview-of-ram-users)），需要为子账号授予模型调用、训练和部署[权限](raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
-   **配置环境变量**：已成功[获取 API Key](raw/model-api-reference/preparations/get-api-key.md)，并[配置到环境变量](raw/model-api-reference/preparations/get-api-key.md)。
-   **前提条件**：已完成模型微调训练。请先调用[查询调优任务](raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/create-fine-tuning-job-api.md)接口，确认任务状态 `status` 为 **SUCCEEDED** 后再进行部署。

## 部署模型

#### 华北2（北京）

`POST https://dashscope.aliyuncs.com/api/v1/deployments`

> Windows CMD 请将`$DASHSCOPE_API_KEY`替换为`%DASHSCOPE_API_KEY%`，PowerShell请替换为 `$env:DASHSCOPE_API_KEY`

### 请求参数

##### 请求头（Headers）

**Content-Type** `string` **（必选）**

固定值：`application/json`

**Authorization** `string` **（必选）**

API Key鉴权，格式为`Bearer sk-xxxx`。

##### 请求体（Request Body）

**model\_name** `string` **（必选）**

待部署的模型ID（非基础模型名称，而是微调或导出后生成的模型标识）。获取方式：

-   微调产出的模型：使用[创建调优任务](raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/create-fine-tuning-job-api.md)响应中 `output.finetuned_output` 的值。
-   导出的模型：使用[查询导出的模型详情](raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/create-fine-tuning-job-api.md)响应中 `output[].model_name` 的值。

**capacity** `integer` **（必选）**

部署的模型实例数量。推荐设置为1。

**plan** `string` **（必选）**

部署方式。LoRA高效微调推荐为`lora`。

#### 部署模型

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/deployments' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model_name": "<替换为模型名称model_name>",
    "capacity": 1,
    "plan": "lora"
}'
```

### 响应参数

**request\_id** `string`

请求的唯一标识符。

**output** `object`

任务详情。

属性

**deployed\_model** `string`

部署模型的唯一标识。用于查询模型部署状态和调用模型。

**model\_name** `string`

模型标识名。

**status** `string`

部署状态：

-   `PENDING`：部署中。
-   `RUNNING`：运行中。
-   `FAILED`：部署失败。

**base\_model** `string`

使用的基准模型。

**gmt\_create** `string`

部署任务创建时间。

**gmt\_modified** `string`

部署任务更新时间。

**workspace\_id** `string`

阿里云百炼API Key所属的业务空间ID。请参见[获取Workspace ID](raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

**charge\_type** `string`

付费模式。post\_paid表示后付费。

**creator** `string`

创建人的阿里云账号ID。

**modifier** `string`

修改人的阿里云账号ID。

**plan** `string`

部署方式。

**code** `string`

错误码。调用失败时返回。

**message** `string`

错误详情描述。调用失败时返回。

#### 成功响应示例

重点关注：`output.deployed_model`（部署模型的唯一标识）、`output.status`（部署状态）。

```
{
    "request_id": "96020b2e-9072-4c8a-9981-xxxxxxxxx",
    "output": {
        "deployed_model": "wan2.7-image-pro-ft-202507011122-xxxx",
        "gmt_create": "2025-07-01T10:30:00.000",
        "gmt_modified": "2025-07-01T10:30:00.000",
        "status": "PENDING",
        "model_name": "wan2.7-image-pro-ft-202507011122-xxxx",
        "base_model": "wan2.7-image-pro",
        "workspace_id": "llm-xxxxxxxxx",
        "charge_type": "post_paid",
        "creator": "12xxxxxxx",
        "modifier": "12xxxxxxx",
        "plan": "lora"
    }
}
```

#### 错误响应示例

```
{
    "code": "InvalidParameter",
    "request_id": "BE213CDD-8A5C-59EE-9A67-055EAB0CB59B",
    "message": "The model xxx does not exist or is not deployable"
}
```

## 下一步

部署为异步操作，调用本接口后可通过[查询和管理部署](raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)接口查询部署状态。
