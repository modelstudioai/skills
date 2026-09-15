# 调优任务管理

查询、取消、删除调优任务，以及查询调优任务日志。

## 适用范围

-   **适用地域**：本文描述的功能仅在华北2（北京）地域可用，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。
-   已成功[获取 API Key](raw/model-api-reference/preparations/get-api-key.md)并[配置到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
-   已通过[创建调优任务](raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/create-fine-tuning-job-api.md)接口创建了调优任务。

## 查询调优任务状态

查询指定调优任务的详细信息和运行状态。

### 地址

```
GET https://dashscope.aliyuncs.com/api/v1/fine-tunes/{job_id}
```

### 请求示例

```
curl --location --request GET "https://dashscope.aliyuncs.com/api/v1/fine-tunes/<替换为您的调优任务id>" \
      --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
      --header 'Content-Type: application/json'
```

### 请求参数

**字段**

**类型**

**传参方式**

**必选**

**描述**

job\_id

String

Url Path

是

要查询的调优任务的ID。即[创建调优任务返回参数](raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/create-fine-tuning-job-api.md)中的job\_id。

### 响应示例

#### 文本生成模型

```
{
    "request_id": "c59b2145-a93c-4e00-b610-4d7cc5c521a2",
    "output": {
        "job_id": "ft-202410291653-1c7f",
        "job_name": "ft-202410291653-1c7f",
        "status": "SUCCEEDED",
        "finetuned_output": "qwen3-14b-suffix-ft-202410291653-1c7f",
        "model": "qwen3-14b",
        "base_model": "qwen3-14b",
        "training_file_ids": [],
        "validation_file_ids": [],
        "training_datasets": [
            {
                "data_source_type": "file_id",
                "file_id": "976bd01a-f30b-4414-86fd-50c54486e3ef"
            }
        ],
        "validation_datasets": [],
        "hyper_parameters": {
            "n_epochs": 3,
            "batch_size": 32,
            "max_length": 8192,
            "learning_rate": "1.6e-5",
            "lr_scheduler_type": "linear",
            "split": 0.9
        },
        "training_type": "sft",
        "create_time": "2024-10-29 16:53:53",
        "workspace_id": "llm-v71tlv***",
        "user_identity": "1396993924585947",
        "modifier": "1396993924585947",
        "creator": "1396993924585947",
        "end_time": "2024-10-29 17:11:26",
        "group": "llm",
        "usage": 279808
    }
}
```

#### 视频生成模型

关注 `output.status`（SUCCEEDED 表示训练完成）和 `output.usage`（训练消耗的总 Token 数量）。

```
{
    "request_id": "9bbb953c-bef2-4b59-9fc5-xxxxxxxxx",
    "output": {
        "job_id": "ft-202511111122-xxxx",
        "status": "SUCCEEDED",
        "finetuned_output": "wan2.5-i2v-preview-ft-202511111122-xxxx",
        "model": "wan2.5-i2v-preview",
        "base_model": "wan2.5-i2v-preview",
        "training_file_ids": [],
        "validation_file_ids": [],
        "training_datasets": [
            {
                "data_source_type": "file_id",
                "file_id": "xxxxxxxxxxxx"
            }
        ],
        "validation_datasets": [],
        "hyper_parameters": {
            "n_epochs": 400,
            "learning_rate": 2e-05,
            "split": 0.9,
            "eval_epochs": 50
        },
        "training_type": "efficient_sft",
        "create_time": "2025-11-11 11:22:22",
        "end_time": "2025-11-11 16:49:01",
        "usage": 432000,
        "output_cnt": 8
    }
}
```

#### 图像生成模型

```
{
    "request_id": "03d738f5-3720-90b0-9c7b-xxxxxxxxx",
    "output": {
        "job_id": "ft-202606030110-xxxx",
        "status": "SUCCEEDED",
        "finetuned_output": "wan2.7-image-pro-ft-202606030110-xxxx",
        "model": "wan2.7-image-pro",
        "base_model": "wan2.7-image-pro",
        "training_file_ids": [],
        "validation_file_ids": [],
        "training_datasets": [
            {
                "data_source_type": "file_id",
                "file_id": "xxxxxxxxxxxx"
            }
        ],
        "validation_datasets": [],
        "hyper_parameters": {
            "max_steps": 800,
            "learning_rate": 3e-05,
            "eval_steps": 200,
            "max_token_length": "2k",
            "max_pixels": "2k",
            "val_img_size": "2k",
            "generation_type": "t2i",
            "lora_rank": 32
        },
        "training_type": "efficient_sft",
        "create_time": "2026-06-03 01:10:47",
        "end_time": "2026-06-03 01:38:53",
        "usage": 10273216,
        "output_cnt": 1
    }
}
```

### 响应参数

**参数名称**

**类型**

**参数说明**

request\_id

String

本次请求的ID。

output

Object

调优任务的详细信息。

output.job\_id

String

本次调优的任务ID，用于后续查询状态。

生成规则：`ft-{yyyyMMddHHmm}-{4位uuid}`。

output.jobs\_name

String

同`output.job_id`。

output.status

String

本次调优[任务的状态](raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/create-fine-tuning-job-api.md)。

output.finetuned\_output

String

仅调优任务状态为“SUCCEED”时出现，返回的是调优完成的模型ID。

output.model

String

调优任务使用的模型ID。

output.base\_model

String

调优任务使用的模型对应的基础模型ID。

比如：调优任务`ft-202410291653-1c7f`使用的基础模型是`qwen3-14b`。

output.training\_file\_ids

Array

兼容字段，新任务始终返回空数组，请使用 training\_datasets。

output.validation\_file\_ids

Array

兼容字段，新任务始终返回空数组，请使用 validation\_datasets。

output.training\_datasets

Array of Dataset

训练数据集列表。

output.validation\_datasets

Array of Dataset

测试数据集列表。

output.hyper\_parameters

Object

显性声明过的超参表。

output.training\_type

String

调优方法。

output.create\_time

String

调优任务创建时间。

output.workspace\_id

String

调优任务所属的业务空间ID。

output.user\_identity

String

该调优任务隶属的主账号UID。

output.modifier

String

对该调优任务进行最后一次操作的账号UID。（比如：某个子账号取消了该任务，该子账号UID会显示在这里）

output.creator

String

该调优任务创建人UID。

output.end\_time

String

调优任务结束时间，当任务状态为“SUCCEED”、“FAILED”、“CANCELED”时出现。

output.group

String

模型调优的任务类型。

output.usage

Integer

调优任务消耗的Token（count）数，扣费计算公式请参考：计费说明。当任务状态为“SUCCEED”、“CANCELED”时出现。

output.output\_cnt

Integer

当前任务已产出的 Checkpoint 数量。仅对支持多 Checkpoint 输出的模型（如 `cosyvoice-v3-flash`）返回。Checkpoint 详细列表可通过查询 Checkpoint 接口获取。

output.max\_output\_cnt

Integer

单次任务可产出的 Checkpoint 数量上限。`output_cnt` 超出上限的部分会按调优充分度截断。仅对支持多 Checkpoint 输出的模型返回。

## 取消调优任务

取消正在运行的调优任务。仅处于运行中状态的任务可被取消。

### 地址

```
POST https://dashscope.aliyuncs.com/api/v1/fine-tunes/{job_id}/cancel
```

### 请求示例

```
curl --location --request POST "https://dashscope.aliyuncs.com/api/v1/fine-tunes/<替换为您的调优任务id>/cancel" \
      --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
      --header 'Content-Type: application/json'
```

### 请求参数

**字段**

**类型**

**传参方式**

**必选**

**描述**

job\_id

String

Url Path

是

要取消的调优任务ID，可通过[创建训练任务](raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/create-fine-tuning-job-api.md)或列举训练任务接口获取。

### 响应示例

```
{
    "request_id": "670fca9d-48dd-4c5a-83e7-33bcc20420f8",
    "output": {
        "status": "success"
    }
}
```

### 响应参数

**参数名称**

**类型**

**参数说明**

request\_id

String

本次请求的ID。

output

Object

取消操作返回的详细信息。

## 删除调优任务

删除指定的调优任务记录。

### 地址

```
DELETE https://dashscope.aliyuncs.com/api/v1/fine-tunes/{job_id}
```

### 请求示例

```
curl --location --request DELETE "https://dashscope.aliyuncs.com/api/v1/fine-tunes/<替换为您的调优任务id>" \
      --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
      --header 'Content-Type: application/json'
```

### 请求参数

**字段**

**类型**

**传参方式**

**必选**

**描述**

job\_id

String

Url Path

是

要删除的调优任务ID，可通过[创建训练任务](raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/create-fine-tuning-job-api.md)或列举训练任务接口获取。

### 响应示例

```
{
    "request_id": "7d7e1469-df77-4163-83ce-54425df744ed",
    "output": {
        "status": "success"
    }
}
```

### 响应参数

**参数名称**

**类型**

**参数说明**

request\_id

String

本次请求的ID。

output

Object

删除操作返回的详细信息。

## 查询调优任务列表

分页查询当前账号下的调优任务列表。

### 地址

```
GET https://dashscope.aliyuncs.com/api/v1/fine-tunes
```

### 请求示例

```
curl --location --request GET "https://dashscope.aliyuncs.com/api/v1/fine-tunes?model=qwen3-14b&page_no=2" \
      --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
      --header 'Content-Type: application/json'
```

### 请求参数

**参数名称**

**类型**

**传参方式**

**是否必填**

**参数说明**

page\_no

Integer

Query

否

默认1

page\_size

Integer

Query

否

默认10，最大值1000，最小值1

model

String

Query

否

模型ID，指定该参数表示只列举基于该模型的调优任务

### 响应示例

```
{
    "request_id": "2182ef64-6398-457b-b3f6-5fde5fd6b388",
    "output": {
        "page_no": 2,
        "page_size": 10,
        "total": 12,
        "jobs": [
            {
                "job_id": "ft-202410291653-1c7f",
                "job_name": "ft-202410291653-1c7f",
                "status": "SUCCEEDED",
                "finetuned_output": "qwen3-14b-suffix-ft-202410291653-1c7f",
                "model": "qwen3-14b",
                "base_model": "qwen3-14b",
                "training_file_ids": [],
                "validation_file_ids": [],
                "training_datasets": [
                    {
                        "data_source_type": "file_id",
                        "file_id": "976bd01a-f30b-4414-86fd-50c54486e3ef"
                    }
                ],
                "validation_datasets": [],
                "hyper_parameters": {
                    "n_epochs": 3,
                    "batch_size": 32,
                    "max_length": 8192,
                    "learning_rate": "1.6e-5",
                    "lr_scheduler_type": "linear",
                    "split": 0.9
                },
                "training_type": "sft",
                "create_time": "2024-10-29 16:53:53",
                "workspace_id": "llm-v71tlv***",
                "user_identity": "1396993924585947",
                "modifier": "1396993924585947",
                "creator": "1396993924585947",
                "end_time": "2024-10-29 17:11:26",
                "group": "llm",
                "usage": 279808
            },
            {
                "job_id": "ft-202410291512-1851",
                "job_name": "ft-202410291512-1851",
                "status": "CANCELED",
                "model": "qwen3-14b",
                "base_model": "qwen3-14b",
                "training_file_ids": [],
                "validation_file_ids": [],
                "training_datasets": [
                    {
                        "data_source_type": "file_id",
                        "file_id": "86a9fe7f-dd77-43b0-9834-2170e12339ec"
                    },
                    {
                        "data_source_type": "file_id",
                        "file_id": "03ead352-6190-4328-8016-61821c23d4fc"
                    }
                ],
                "validation_datasets": [],
                "hyper_parameters": {
                    "n_epochs": 3,
                    "batch_size": 32,
                    "max_length": 8192,
                    "learning_rate": "1.6e-5",
                    "lr_scheduler_type": "linear",
                    "split": 0.9
                },
                "code": "1",
                "training_type": "sft",
                "create_time": "2024-10-29 15:12:00",
                "workspace_id": "llm-v71tlv***",
                "user_identity": "1396993924585947",
                "modifier": "1396993924585947",
                "creator": "1396993924585947",
                "end_time": "2024-10-29 15:16:00",
                "group": "llm",
                "usage": 0
            }
        ]
    }
}
```

### 响应参数

**参数名称**

**类型**

**参数说明**

request\_id

String

本次请求的ID。

output

Object

查询返回的详细信息。

output.page\_no

Integer

页码。

output.page\_size

Integer

每页显示的数据量。

output.total

Integer

调优任务总计数量。

output.jobs

Array

多个调优任务详情。

点击此处查看调优任务详情对象

**参数名称**

**类型**

**参数说明**

request\_id

String

本次请求的ID。

output

Object

调优任务的详细信息。

output.job\_id

String

本次调优的任务ID，用于后续查询状态。

生成规则：`ft-{yyyyMMddHHmm}-{4位uuid}`。

output.jobs\_name

String

同`output.job_id`。

output.status

String

本次调优[任务的状态](raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/create-fine-tuning-job-api.md)。

output.finetuned\_output

String

仅调优任务状态为“SUCCEED”时出现，返回的是调优完成的模型ID。

output.model

String

调优任务使用的模型ID。

output.base\_model

String

调优任务使用的模型对应的基础模型ID。

比如：调优任务`ft-202410291653-1c7f`使用的基础模型是`qwen3-14b`。

output.training\_file\_ids

Array

兼容字段，新任务始终返回空数组，请使用 training\_datasets。

output.validation\_file\_ids

Array

兼容字段，新任务始终返回空数组，请使用 validation\_datasets。

output.training\_datasets

Array of Dataset

训练数据集列表。

output.validation\_datasets

Array of Dataset

测试数据集列表。

output.hyper\_parameters

Object

显性声明过的超参表。

output.training\_type

String

调优方法。

output.create\_time

String

调优任务创建时间。

output.workspace\_id

String

调优任务所属的业务空间ID。

output.user\_identity

String

该调优任务隶属的主账号UID。

output.modifier

String

对该调优任务进行最后一次操作的账号UID。（比如：某个子账号取消了该任务，该子账号UID会显示在这里）

output.creator

String

该调优任务创建人UID。

output.end\_time

String

调优任务结束时间，当任务状态为“SUCCEED”、“FAILED”、“CANCELED”时出现。

output.group

String

模型调优的任务类型。

output.usage

Integer

调优任务消耗的Token（count）数，扣费计算公式请参考：计费说明。当任务状态为“SUCCEED”、“CANCELED”时出现。

output.output\_cnt

Integer

当前任务已产出的 Checkpoint 数量。仅对支持多 Checkpoint 输出的模型（如 `cosyvoice-v3-flash`）返回。Checkpoint 详细列表可通过查询 Checkpoint 接口获取。

output.max\_output\_cnt

Integer

单次任务可产出的 Checkpoint 数量上限。`output_cnt` 超出上限的部分会按调优充分度截断。仅对支持多 Checkpoint 输出的模型返回

## 查询调优任务日志

查询指定调优任务的训练日志。

### 地址

```
GET https://dashscope.aliyuncs.com/api/v1/fine-tunes/{job_id}/logs
```

### 请求示例

```
curl --location --request GET "https://dashscope.aliyuncs.com/api/v1/fine-tunes/<替换为您的调优任务id>/logs?offset=10&line=10" \
      --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
      --header 'Content-Type: application/json'
```

### 请求参数

**字段**

**类型**

**传参方式**

**必选**

**描述**

job\_id

String

Url Path

是

要打印日志的调优任务ID，可通过创建训练任务或列举训练任务接口获取。

offset

Number

Query

否

忽略前`offset`行输出，从第`offset+1`行开始读取。不能超过当前已有输出的总行数，超过则不会有输出信息返回。默认值为0。

line

Number

Query

否

从`offset+1`行（包含）起，读取`line`行输出信息，如果本次请求的输出不足`line`行，则以实际输出为准。默认值为100，上限为1000。

### 响应示例

```
{
    "request_id": "ce49b45d-fe46-474e-9e1b-3e7427ffdf5a",
    "output": {
        "total": 20,
        "logs": [
            "{'train_runtime': 216.3999, 'train_samples_per_second': 2.066, 'train_steps_per_second': 0.014, 'train_loss': 0.9122632344563802, 'epoch': 0.8571428571428571}",
            " Actual number of consumed tokens is 279808!",
            " Uploaded checkpoint!",
            " Fine-tune succeeded!",
            " use checkpoint-3 as final checkpoint",
            "2024-10-29 17:03:47,719 - INFO - transfer for inference succeeded, start to deliver it for inference",
            "2024-10-29 17:09:43,322 - INFO - start to save checkpoint",
            "2024-10-29 17:11:24,689 - INFO - finetune-job succeeded",
            "2024-10-29 17:11:25,130 - INFO - training usage 279808",
            "2024-10-29 17:11:25,175 - INFO - ##FT_COMPLETE##"
        ]
    }
}
```

### 响应参数

**参数名称**

**类型**

**参数说明**

request\_id

String

本次请求的ID。

output

Object

查询返回的详细信息。

output.total

Integer

日志总计行数。

output.logs

Array

输出的日志。

## 异常响应

### 响应示例

```
{
    "code": "NotFound",
    "request_id": "BE213CDD-8A5C-59EE-9A67-055EAB0CB59B",
    "message": "Not Found!"
}
```

### 响应参数

**字段**

**类型**

**描述**

**示例值**

code

String

错误码。

NotFound

request\_id

String

本次请求的系统唯一码。

6332fb02-3111-43f0-bf79-f9e8c5ffa7f9

message

String

错误信息。

Not Found!

当请求出错时，可能返回以下错误：

**HTTP状态码**

**错误码**

**错误信息举例**

**含义**

**处理方式**

400

InvalidParameter

Missing training files

参数错误，缺少参数或者参数格式问题等。

根据错误信息，修正您的参数。

400

UnsupportedOperation

The fine-tune job can not be canceled because it is succeeded or failed

当资源处于特定状态时，无法对其进行操作。

待要操作的资源到达可操作状态时再进行操作。

400

UnsupportedOperation

The fine-tune job can not be deleted because it is succeeded,failed or canceled

当资源处于特定状态时，无法对其进行操作。

待要操作的资源到达可操作状态时再进行操作。

404

NotFound

Not found!

要查询/操作的资源不存在。

检查要查询/操作的资源ID是否错误。

409

Conflict

Model instance xxxxx already exists, please specify a suffix

已存在deployed\_model名为xxxxx的部署实例，需要指定后缀进行区分。

为部署指定唯一的后缀。

429

Throttling

-   Too many fine-tune job in running, please retry later.
    
-   Only 20 fine-tune job in running or succeeded allowed per user.
    

资源的创建触发平台限制。

-   删除不再使用的模型。
    
-   如您确实需要提高调优任务的并发量或保留更多调优成功的模型，请联系商务经理。
    

500

InternalError

Internal server error!

内部错误。

记录 request\_id，通过工单联系阿里云工程师进行排查。
