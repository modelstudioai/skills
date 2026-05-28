# 模型导入API参考

本文介绍模型导入相关 API，使用 API（HTTP）调用方式帮助您将自定义模型从 OSS 导入到阿里云百炼平台。模型导入的核心流程为：提交导入任务、轮询任务状态、任务完成。

## 前提条件

-   已配置百炼的 API-KEY，请参考[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。
    
-   已创建 OSS Bucket，并完成百炼平台的 OSS 授权。详见[模型导入](https://help.aliyun.com/zh/model-studio/model-import)中的使用前提。
    
-   模型文件已上传至 OSS Bucket，并符合[导入要求与限制](https://help.aliyun.com/zh/model-studio/model-import#h2-file-format-constraints)。
    

## 公共请求头

所有接口均需在 HTTP Header 中携带以下字段：

**Header**

**说明**

Authorization

`Bearer ${DASHSCOPE_API_KEY}`，API-KEY 的获取请参考[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。

Content-Type

`application/json`

## 创建导入任务

提交一个模型导入任务。系统将对模型文件进行结构和安全校验，确保文件能够正常部署。

### **地址**

```
POST https://dashscope.aliyuncs.com/api/v1/custom_models/import
```

### **请求示例**

```
curl -X POST "https://dashscope.aliyuncs.com/api/v1/custom_models/import" \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header "Content-Type: application/json" \
    --data '{
        "model_name": "qwen3-32b",
        "display_name": "我的 LoRA 微调模型",
        "source": "oss",
        "weight_type": "lora",
        "storage_info": {
            "bucket_name": "my-model-bucket",
            "object_key": "models/qwen3-32b-lora/"
        }
    }'
```

### **请求参数**

**参数**

**类型**

**传参方式**

**必选**

**说明**

model\_name

String

body

是

基础模型的名称。对应控制台**基础模型**字段。当前支持的模型请参见[支持导入的基础模型](https://help.aliyun.com/zh/model-studio/model-import#h2-supported-models)。示例：`qwen3-32b`。

display\_name

String

body

否

导入模型的显示名称，对应控制台**模型名称**字段。最多50个字符。不传时默认使用基础模型名称。

source

String

body

是

导入来源。对应控制台**导入来源**字段。当前仅支持 `oss`（从 OSS 导入）。响应中返回大写 `OSS`。

weight\_type

String

body

是

训练类型。`full` 表示全参微调模型，`lora` 表示 LoRA 微调模型。

storage\_info

Object

body

是

导入来源的存储信息。

storage\_info.bucket\_name

String

body

是

OSS Bucket 名称。对应控制台**Bucket**字段。

storage\_info.object\_key

String

body

是

模型文件所在 OSS 路径前缀，需以 `/` 结尾。示例：`models/qwen3-32b-lora/`。

### **响应示例**

```
{
    "request_id": "6c6b****-3fea-****-bc26-c9e2********",
    "output": {
        "job_id": "937b****-2a4f-****-8abe-c2fa********",
        "model_name": "qwen3-32b-offline-20240101-abc1",
        "display_name": "我的 LoRA 微调模型",
        "source": "OSS",
        "weight_type": "lora",
        "storage_info": {
            "bucket_name": "my-model-bucket",
            "object_key": "models/qwen3-32b-lora/"
        },
        "status": "PENDING",
        "gmt_create": "2024-01-01T12:00:00.000+00:00"
    }
}
```

### **响应参数**

**参数**

**类型**

**说明**

request\_id

String

请求 ID。

output.job\_id

String

导入任务 ID，用于查询任务状态或删除任务。

output.model\_name

String

系统生成的模型标识，格式为基础模型名称加时间戳后缀。

output.display\_name

String

导入模型的显示名称。

output.source

String

导入来源，返回值为大写 `OSS`。

output.weight\_type

String

训练类型。

output.storage\_info

Object

导入来源的存储信息，包含 `bucket_name` 和 `object_key`。

output.status

String

任务状态。参见[任务状态说明](#mi04sec01)。

output.gmt\_create

String

任务创建时间，ISO 8601 格式。示例：`2024-01-01T12:00:00.000+00:00`。

## 查询导入任务详情

查询指定导入任务的当前状态及详情。

### **地址**

```
GET https://dashscope.aliyuncs.com/api/v1/custom_models/import/{job_id}
```

### **请求示例**

```
curl "https://dashscope.aliyuncs.com/api/v1/custom_models/import/937b****-2a4f-****-8abe-c2fa********" \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header "Content-Type: application/json"
```

### **请求参数**

**参数**

**类型**

**传参方式**

**必选**

**说明**

job\_id

String

path

是

导入任务 ID，创建导入任务时返回。

### **响应示例**

```
{
    "request_id": "ca21****-b91b-****-bd35-c41c********",
    "output": {
        "job_id": "937b****-2a4f-****-8abe-c2fa********",
        "model_name": "qwen3-32b-offline-20240101-abc1",
        "display_name": "我的 LoRA 微调模型",
        "source": "OSS",
        "storage_info": {
            "bucket_name": "my-model-bucket",
            "object_key": "models/qwen3-32b-lora/"
        },
        "status": "RUNNING",
        "gmt_create": "2024-01-01T12:00:00.000+00:00"
    }
}
```

### **响应参数**

响应参数与[创建导入任务](#mi01sec01)的响应参数基本一致，但不包含 `weight_type` 字段。当任务失败时，响应中将额外包含 `error_code` 字段，表示失败原因。

## 查询导入任务列表

分页查询当前工作空间下的导入任务列表。

### **地址**

```
GET https://dashscope.aliyuncs.com/api/v1/custom_models/import
```

### **请求示例**

```
curl "https://dashscope.aliyuncs.com/api/v1/custom_models/import?page_no=1&page_size=10" \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header "Content-Type: application/json"
```

按状态过滤：

```
curl "https://dashscope.aliyuncs.com/api/v1/custom_models/import?page_no=1&page_size=10&status=SUCCESSED" \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header "Content-Type: application/json"
```

### **请求参数**

**参数**

**类型**

**传参方式**

**必选**

**说明**

page\_no

Integer

query

否

页码，默认值为1。

page\_size

Integer

query

否

每页条数，默认值为10，最大值为100。

status

String

query

否

按任务状态过滤，参见[任务状态说明](#mi04sec01)。

model\_name

String

query

否

按模型名称过滤，需传入响应中返回的系统生成名称（精确匹配）。

### **响应示例**

```
{
    "request_id": "ca21****-b91b-****-bd35-c41c********",
    "output": {
        "total": 2,
        "page_no": 1,
        "page_size": 10,
        "list": [
            {
                "job_id": "937b****-2a4f-****-8abe-c2fa********",
                "model_name": "qwen3-32b-offline-20240101-abc1",
                "display_name": "我的 LoRA 微调模型",
                "status": "SUCCESSED",
                "source": "OSS",
                "storage_info": {
                    "bucket_name": "my-model-bucket",
                    "object_key": "models/qwen3-32b-lora/"
                },
                "gmt_create": "2024-01-01T12:00:00.000+00:00"
            },
            {
                "job_id": "edb0****-39ac-****-9859-8b1e********",
                "model_name": "qwen3-32b-offline-20240102-xyz4",
                "display_name": "我的全参微调模型",
                "status": "FAILED",
                "source": "OSS",
                "storage_info": {
                    "bucket_name": "my-model-bucket",
                    "object_key": "models/qwen3-32b-full/"
                },
                "error_code": "OSS获取文件失败，请检查OSS内文件",
                "gmt_create": "2024-01-02T09:00:00.000+00:00"
            }
        ]
    }
}
```

### **响应参数**

**参数**

**类型**

**说明**

request\_id

String

请求 ID。

output.total

Integer

满足查询条件的任务总数。

output.page\_no

Integer

当前页码。

output.page\_size

Integer

每页条数。

output.list

Array

导入任务列表。每个元素的字段与[创建导入任务](#mi01sec01)的响应参数基本一致，但不包含 `weight_type` 字段。任务失败时额外包含 `error_code` 字段。

## 删除导入的模型

删除指定的导入任务及其关联的模型文件。只有状态为 `SUCCESSED` 或 `FAILED` 的任务可以删除。删除成功后返回被删除任务的详情。

### **地址**

```
DELETE https://dashscope.aliyuncs.com/api/v1/custom_models/import/{job_id}
```

### **请求示例**

```
curl -X DELETE "https://dashscope.aliyuncs.com/api/v1/custom_models/import/937b****-2a4f-****-8abe-c2fa********" \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header "Content-Type: application/json"
```

### **请求参数**

**参数**

**类型**

**传参方式**

**必选**

**说明**

job\_id

String

path

是

导入任务 ID。

### **响应示例**

```
{
    "request_id": "e22b****-b20a-****-bf23-9b53********",
    "output": {
        "job_id": "937b****-2a4f-****-8abe-c2fa********",
        "model_name": "qwen3-32b-offline-20240101-abc1",
        "display_name": "我的 LoRA 微调模型",
        "source": "OSS",
        "storage_info": {
            "bucket_name": "my-model-bucket",
            "object_key": "models/qwen3-32b-lora/"
        },
        "status": "SUCCESSED",
        "gmt_create": "2024-01-01T12:00:00.000+00:00"
    }
}
```

### **响应参数**

**参数**

**类型**

**说明**

request\_id

String

请求 ID。

output

Object

被删除的任务详情，字段与[创建导入任务](#mi01sec01)的响应参数基本一致，但不包含 `weight_type` 字段。

## 任务状态说明

导入任务在生命周期中可能处于以下状态：

**状态**

**说明**

PENDING

任务已提交，等待处理。

RUNNING

任务正在执行中，系统正在校验和导入模型文件。

SUCCESSED

任务执行成功，模型已导入完成，可以进行部署。

FAILED

任务执行失败。可通过查询任务详情获取 `error_code` 了解失败原因。

## 异常响应

当请求发生错误时，接口将返回如下格式的错误响应：

```
{
    "request_id": "ca21****-b91b-****-bd35-c41c********",
    "code": "OperationDenied",
    "message": "The import job is currently running and cannot be deleted."
}
```

### **错误码**

**错误码**

**说明**

InvalidParameter

请求参数无效。例如必填参数缺失、参数格式错误或参数值不合法。

NotFound

指定的资源不存在。例如 job\_id 不存在、无权访问或基础模型不支持导入。

OperationDenied

操作被拒绝。例如对 RUNNING 状态的任务执行删除操作。

InvalidApiKey

API-KEY 无效或未提供。

InternalError

系统内部错误，请稍后重试。
