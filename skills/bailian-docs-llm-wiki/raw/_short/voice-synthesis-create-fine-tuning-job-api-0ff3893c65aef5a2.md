# 语音合成（CosyVoice）-创建调优任务

创建一个语音合成的模型调优训练任务。数据集支持通过API上传数据集或OSS挂载。

## 适用范围

-   **适用地域**：本文描述的功能**仅在华北2（北京）地域**可用，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。
-   **开通账号权限**：若使用[阿里云子账号](raw/model-user-guide/security-and-compliance/permission-management-overview.md)（[RAM用户](https://help.aliyun.com/zh/ram/user-guide/overview-of-ram-users)），需要为子账号授予模型调用、训练和部署[权限](raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
-   **配置环境变量**：已成功[获取 API Key](raw/model-api-reference/preparations/get-api-key.md)，并[配置到环境变量](raw/model-api-reference/preparations/get-api-key.md)。
-   **准备工作**：已阅读[CosyVoice模型调优](raw/model-user-guide/fine-tuning/fine-tune-speech-synthesis-model/fine-tune-speech-synthesis-model-by-api.md)，了解支持调优的模型、调优步骤、数据格式以及计费说明。

## 创建调优任务

#### 华北2（北京）

`POST https://dashscope.aliyuncs.com/api/v1/fine-tunes`

> Windows CMD 请将`$DASHSCOPE_API_KEY`替换为`%DASHSCOPE_API_KEY%`，PowerShell请替换为 `$env:DASHSCOPE_API_KEY`

### 请求参数

##### 请求头（Headers）

**Content-Type** `string` **（必选）**

固定值：`application/json`

**Authorization** `string` **（必选）**

API Key鉴权，格式为`Bearer sk-xxxx`。

##### 请求体（Request Body）

**model** `string` **（必选）**

指定调优所用的基准模型。当前仅支持：

-   `cosyvoice-v3-flash`

**training\_type** `string` **（必选）**

微调类型，当前仅支持`efficient_sft`（高效微调）。

**hyper\_parameters** `object` **（必选）**

**超参数配置**。CosyVoice 调优涉及两个子网络，两者已解耦、可独立调整：

-   LM（Language Model）：将文本转为离散语音 token 的自回归语言模型，对韵律影响较大。超参以 `lm_*` 前缀区分。
-   FM（Flow Matching）：将语音 token 还原为 Mel 谱的流匹配模型，对音色还原度影响较大。超参以 `fm_*` 前缀区分。

超参数属性

**lm\_max\_epoch** `int` **（必选）**

LM 调优轮次（epoch 数）。推荐值：60。取值范围：\[1, 2147483647\]。

**lm\_step** `int` **（必选）**

LM 保存 checkpoint 的步长（每多少个 epoch 保存一次）。推荐值：5。取值范围：\[1, 2147483647\]。

**lm\_num** `int` **（必选）**

LM 保留的 checkpoint 数量上限。推荐值：3。取值范围：\[1, 2147483647\]。

**lm\_batch\_size** `int` **（必选）**

LM 批次大小（batch size）。推荐值：1000。取值范围：\[1, 2147483647\]。

**fm\_max\_epoch** `int` **（必选）**

FM 调优轮次（epoch 数）。推荐值：100。取值范围：\[1, 2147483647\]。

**fm\_step** `int` **（必选）**

FM 保存 checkpoint 的步长（每多少个 epoch 保存一次）。推荐值：10。取值范围：\[1, 2147483647\]。

**fm\_num** `int` **（必选）**

FM 保留的 checkpoint 数量上限。推荐值：3。取值范围：\[1, 2147483647\]。

**fm\_batch\_size** `int` **（必选）**

FM 批次大小（batch size）。推荐值：2000。取值范围：\[1, 2147483647\]。

**training\_datasets** `Array of Dataset` **（条件必选）**

训练集文件列表。与 `training_file_ids` 二选一，若使用 `training_file_ids` 则无需传此参数。仅支持挂载一个训练文件。

Dataset 结构

**data\_source\_type** `string` **（必选）**

数据源类型，可选值：

-   `oss_mount`（挂载 OSS 文件）
-   `file_id`（由文件管理服务 API 上传的文件）

**mount\_storage** `object` （条件必选）

数据源类型为 `oss_mount` 时必填。OSS 挂载信息。

属性

**region** `string` **（必选）**

要挂载的 OSS Bucket 所属地域。支持北京（cn-beijing）和新加坡（ap-southeast-1）。

**bucket** `string` **（必选）**

要挂载的 OSS Bucket 名称。

**file\_path** `string` **（必选）**

要挂载的 OSS 文件路径（object key）。对包含多个文件的数据集，使用其 data.jsonl 的文件路径。与使用 file\_id 的方式不同，需要将未经压缩的数据集文件夹整体上传到 OSS，不支持 zip 文件。

**file\_id** `string` （条件必选）

数据源类型为 `file_id` 时必填。文件 ID，由[上传文件 API](https://help.aliyun.com/zh/model-studio/upload-file-api) 产生。

**validation\_datasets** `Array of Dataset` （可选）

验证集文件列表。结构同`training_datasets`。

与 `validation_file_ids` 二选一。若两者均不提供，系统会从训练集中自动划分。

**training\_file\_ids** `array[string]` **（条件必选）**

训练集文件ID数组，可传入多个ID。与 `training_datasets` 二选一，若使用 `training_datasets` 则无需传此参数。文件ID通过[上传文件 API](https://help.aliyun.com/zh/model-studio/upload-file-api) 获取。

**validation\_file\_ids** `array[string]` （可选）

验证集文件ID数组，可传入多个ID。与 `validation_datasets` 二选一，若使用 `validation_datasets` 则无需传此参数。若两者均不提供，系统会从训练集中自动划分。文件ID通过[上传文件 API](https://help.aliyun.com/zh/model-studio/upload-file-api) 获取。

**job\_name** `string` （可选）

调优任务名称。

**model\_name** `string` （可选）

调优完成后的模型名称。

使用file\_id的数据集

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "cosyvoice-v3-flash",
    "training_datasets": [
        {
            "data_source_type": "file_id",
            "file_id": "<替换为训练数据集的file_id>"
        }
    ],
    "hyper_parameters": {
        "lm_max_epoch": 60,
        "lm_step": 5,
        "lm_num": 3,
        "lm_batch_size": 1000,
        "fm_max_epoch": 100,
        "fm_step": 10,
        "fm_num": 3,
        "fm_batch_size": 2000
    },
    "training_type": "efficient_sft"
}'
```

使用OSS挂载的数据集

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "cosyvoice-v3-flash",
    "training_datasets": [
        {
            "data_source_type": "oss_mount",
            "mount_storage": {
                "region": "cn-beijing",
                "bucket": "example_bucket",
                "file_path": "dataset/data.jsonl"
            }
        }
    ],
    "hyper_parameters": {
        "lm_max_epoch": 60,
        "lm_step": 5,
        "lm_num": 3,
        "lm_batch_size": 1000,
        "fm_max_epoch": 100,
        "fm_step": 10,
        "fm_num": 3,
        "fm_batch_size": 2000
    },
    "training_type": "efficient_sft"
}'
```

### 响应参数

**request\_id** `string`

请求的唯一标识符。

**output** `object`

任务详情。

属性

**job\_id** `string`

模型调优任务唯一标识，用于查询任务详情、日志、取消或删除任务。生成规则：`ft-{yyyyMMddHHmm}-{4位uuid}`。

**job\_name** `string`

模型调优任务名称。

**model\_name** `string`

调优完成后的模型名称。

**status** `string`

调优训练任务的状态：

-   `PENDING`：训练待开始。
-   `QUEUING`：训练正在排队（同一时间只能运行一个调优任务）。
-   `RUNNING`：训练正在进行中。
-   `SUCCEEDED`：训练成功。
-   `FAILED`：训练失败。
-   `CANCELED`：训练已取消。
-   `CANCELING`：训练正在取消中。

**finetuned\_output** `string`

调优后产出的新模型ID，部署和调用时需要用到。任务状态为 SUCCEEDED 时返回。

**model** `string`

使用的基准模型。

**base\_model** `string`

使用的基准模型。

**training\_file\_ids** `array`

兼容旧版字段，新任务始终返回空数组，请使用 `training_datasets`。

**training\_datasets** `Array of Dataset`

训练数据集列表。

**validation\_file\_ids** `array`

兼容旧版字段，新任务始终返回空数组，请使用 `validation_datasets`。

**validation\_datasets** `Array of Dataset`

验证数据集列表。若未指定验证集，为空数组。

**hyper\_parameters** `object`

实际使用的超参数。

**training\_type** `string`

模型调优的训练方式。

**output\_cnt** `integer`

当前任务已产出的 Checkpoint 数量。Checkpoint 详细列表可通过[Checkpoint 管理](raw/model-api-reference/model-production/fine-tuning-jobs-api/list-checkpoints-api.md)接口获取。

**max\_output\_cnt** `integer`

单次任务可产出的 Checkpoint 数量上限。`output_cnt` 超出上限的部分会按调优充分度截断。

**charge\_type** `string`

计费类型。CosyVoice 模型为 token。

**create\_time** `string`

任务创建时间。

**end\_time** `string`

任务结束时间。任务状态为 SUCCEEDED、FAILED 或 CANCELED 时返回。

**usage** `integer`

调优任务消耗的 Token 数。任务状态为 SUCCEEDED 或 CANCELED 时返回。

**workspace\_id** `string`

阿里云百炼API Key所属的业务空间ID。请参见[获取Workspace ID](raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

**user\_identity** `string`

用户标识，阿里云账号ID。

**creator** `string`

创建人的阿里云账号ID。

**modifier** `string`

修改人的阿里云账号ID。

**group** `string`

模型调优任务分组。

**code** `string`

错误码。调用失败时返回。请参见下方错误码表。

**message** `string`

错误详情描述。调用失败时返回。

#### 成功响应示例

重点关注：`output.job_id`（任务ID）、`output.finetuned_output`（调优后产出的新模型名称）。

```
{
    "request_id": "0eb05b0c-02ba-414a-9d0c-xxxxxxxxx",
    "output": {
        "job_id": "ft-202511111122-xxxx",
        "job_name": "ft-202511111122-xxxx",
        "status": "PENDING",
        "finetuned_output": "cosyvoice-v3-flash-ft-202511111122-xxxx",
        "model": "cosyvoice-v3-flash",
        "base_model": "cosyvoice-v3-flash",
        "training_file_ids": [],
        "training_datasets": [
            {
                "data_source_type": "file_id",
                "file_id": "xxxxxxxxxxxx"
            }
        ],
        "validation_file_ids": [],
        "validation_datasets": [],
        "hyper_parameters": {
            "lm_max_epoch": 60,
            "lm_step": 5,
            "lm_num": 3,
            "lm_batch_size": 1000,
            "fm_max_epoch": 100,
            "fm_step": 10,
            "fm_num": 3,
            "fm_batch_size": 2000
        },
        "training_type": "efficient_sft",
        "model_name": "ft-202511111122-xxxx",
        "output_cnt": 0,
        "max_output_cnt": 10,
        "charge_type": "token",
        "create_time": "2025-11-11 11:22:22"
    }
}
```

#### 错误响应示例

```
{
    "code": "InvalidParameter",
    "request_id": "BE213CDD-8A5C-59EE-9A67-055EAB0CB59B",
    "message": "The model cosyvoice-v3-flash does not support training_type: full_sft"
}
```

## 错误码

如果调用失败并返回报错信息，请参见下表进行排查。

**HTTP 状态码**

**错误码**

**解决方案**

400

InvalidParameter

参数错误，缺少参数或者参数格式问题等。根据错误信息修正您的参数。

400

UnsupportedOperation

当资源处于特定状态时，无法对其进行操作。待要操作的资源到达可操作状态时再进行操作。

404

NotFound

要查询/操作的资源不存在。检查资源ID是否错误。

409

Conflict

已存在同名部署实例，需要指定后缀进行区分。

429

Throttling

资源的创建触发平台限制。删除不再使用的模型。如您确实需要提高调优任务的并发量或保留更多调优成功的模型，请联系商务经理。

500

InternalError

内部错误。记录 request\_id，通过工单联系阿里云工程师进行排查。

## 下一步

调优为异步操作，调用本接口后可通过[查询和管理调优任务](raw/model-api-reference/model-production/fine-tuning-jobs-api/get-fine-tuning-job-api.md)接口查询调优任务状态。
