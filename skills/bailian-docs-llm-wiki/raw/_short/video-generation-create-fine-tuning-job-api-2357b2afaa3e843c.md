# 视频生成-创建调优任务

创建一个视频生成的模型微调训练任务。数据集支持通过API上传数据集或OSS挂载。

## 适用范围

-   **适用地域**：本文描述的功能**仅在华北2（北京）地域**可用，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。
-   **开通账号权限**：若使用[阿里云子账号](raw/model-user-guide/security-and-compliance/permission-management-overview.md)（[RAM用户](https://help.aliyun.com/zh/ram/user-guide/overview-of-ram-users)），需要为子账号授予模型调用、训练和部署[权限](raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
-   **配置环境变量**：已成功[获取 API Key](raw/model-api-reference/preparations/get-api-key.md)，并[配置到环境变量](raw/model-api-reference/preparations/get-api-key.md)。
-   **准备工作**：已阅读[视频生成模型调优](raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)，了解支持微调的模型、微调步骤、数据格式以及计费说明。

## 创建微调任务

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

指定微调所用的基准模型。

图生视频-基于首帧：

-   `wan2.7-i2v`：支持首帧和首尾帧微调，通过超参数`task_type`切换，默认为首帧（`i2v`）。
-   `wan2.5-i2v-preview`
-   `wan2.2-i2v-flash`

图生视频-基于首尾帧：

-   `wan2.7-i2v`：需设置超参数`task_type`为`kf2v`。
-   `wan2.2-kf2v-flash`

**training\_file\_ids** `array[string]` **（条件必选）**

训练集文件ID数组，可传入多个ID。与 `training_datasets` 二选一，若使用 `training_datasets` 则无需传此参数。文件ID通过[上传文件 API](https://help.aliyun.com/zh/model-studio/upload-file-api) 获取。

**validation\_file\_ids** `array[string]` （可选）

验证集文件ID数组，可传入多个ID。与 `validation_datasets` 二选一，若使用 `validation_datasets` 则无需传此参数。若两者均不提供，系统会从训练集中自动划分。文件ID通过[上传文件 API](https://help.aliyun.com/zh/model-studio/upload-file-api) 获取。

**training\_type** `string` **（必选）**

微调类型，当前仅支持`efficient_sft`（LoRA高效微调）。

**hyper\_parameters** `object` （可选）

**超参数配置**。初次训练时，推荐使用默认的超参数。若模型效果不佳或训练不收敛，可以尝试调整 n\_epochs 或 learning\_rate 等参数。

超参数属性

**batch\_size** `int` **（必选）**

批次大小。一次性送入模型进行训练的数据条数。

-   wan2.7-i2v：推荐为1。
-   wan2.5-i2v-preview：推荐为2。
-   wan2.2-i2v-flash：推荐为4。
-   wan2.2-kf2v-flash：推荐为4。

**n\_epochs** `int` **（必选）**

训练循环次数。推荐值：50。

`steps = n_epochs × ⌈数据集大小 / batch_size⌉`。建议总步数 ≥ 800。

例如：数据集 5 条，batch\_size=2，每轮步数=⌈5/2⌉=3，最小 n\_epochs = 800/3 ≈ 267。

-   推荐训练轮数会根据数据量自动调整。数据越少，需要更多轮数来充分学习；数据越多，每轮包含的样本越多，因此所需轮数会减少。
-   50 epochs 主要适用于 2 条左右的小数据集；当数据量达到 50-60 条视频时，通常建议训练约 3000-5000 steps 即可。

**重要**该参数影响[训练计费](raw/model-user-guide/test-1/model-training-and-deployment-billing.md)，请合理设置。

**learning\_rate** `float` **（必选）**

学习率。推荐值：2e-5。控制模型权重更新的幅度。过高可能导致模型变差，过低则变化不明显。

**eval\_epochs** `int` **（必选）**

验证间隔。推荐值：20。取值需≥`n_epochs/10`。训练期间每隔多少个epoch进行一次验证评估。

**max\_pixels** `int` **（必选）**

训练视频的最大分辨率。设置训练视频分辨率的像素总数（宽×高）限制。系统仅对超过该值的视频进行缩放处理。

-   wan2.7-i2v：推荐 102400。取值范围：36864 (192×192) ～ 123904 (352×352)。
-   wan2.5-i2v-preview：推荐 36864。取值范围：16384 (128×128) ～ 36864 (192×192)。
-   wan2.2-i2v-flash：推荐 262144。取值范围：65536 (256×256) ～ 262144 (512×512)。
-   wan2.2-kf2v-flash：推荐 262144。取值范围：65536 (256×256) ～ 262144 (512×512)。

**split** `float` （可选）

训练集划分比例。推荐值：0.9。取值范围为 (0, 1)。

仅在未指定`validation_file_ids`时生效。此参数用于从训练集中自动按比例拆分出验证集。例如，0.9表示90%训练集，10%验证集。

**max\_split\_val\_dataset\_sample** `int` （可选）

从训练集中自动划分验证集的最大样本数。推荐值：5。取值需≥1。

仅在未指定`validation_file_ids`时生效。该参数为验证集数量设置上限：`验证集数量 = min(数据集总数 × (1 − split), max_split_val_dataset_sample)`

**save\_total\_limit** `int` （可选）

Checkpoint 保存数量上限。推荐值：10。限制最多保存的模型数量，系统将只保存最后 N 个 Checkpoint。

**lora\_rank** `int` （可选）

LoRA 低秩矩阵的维数。推荐值：32。该值决定了微调参数量的大小，数值越大拟合能力越强，但训练速度会变慢。取值必须为2n（如 16、32、64）。

**lora\_alpha** `int` （可选）

LoRA 权重的缩放系数。推荐值：32。用于调节微调后的参数对原模型权重的影响程度。取值必须为2n（如 16、32、64）。

**task\_type** `string` （可选）

微调任务类型。仅对`wan2.7-i2v`模型有效，其他模型无需设置此参数。

-   `i2v`（默认值）：首帧生视频微调。
-   `kf2v`：首尾帧生视频微调。

**training\_datasets** `Array of Dataset` **（条件必选）**

训练集文件列表。与 `training_file_ids` 二选一，若使用 `training_file_ids` 则无需传此参数。

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

**job\_name** `string` （可选）

调优任务名称。

**model\_name** `string` （可选）

调优完成后的模型名称。

图生视频-基于首帧（Wan2.7）

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "wan2.7-i2v",
    "training_file_ids": [
        "<替换为训练数据集的文件id>"
    ],
    "training_type": "efficient_sft",
    "hyper_parameters": {
        "task_type": "i2v",
        "n_epochs": 50,
        "batch_size": 1,
        "learning_rate": 2e-5,
        "split": 0.9,
        "max_split_val_dataset_sample": 5,
        "eval_epochs": 20,
        "max_pixels": 102400,
        "save_total_limit": 10,
        "lora_rank": 32,
        "lora_alpha": 32
    }
}'
```

图生视频-基于首尾帧（Wan2.7）

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "wan2.7-i2v",
    "training_file_ids": [
        "<替换为训练数据集的文件id>"
    ],
    "training_type": "efficient_sft",
    "hyper_parameters": {
        "task_type": "kf2v",
        "n_epochs": 50,
        "batch_size": 1,
        "learning_rate": 2e-5,
        "split": 0.9,
        "max_split_val_dataset_sample": 5,
        "eval_epochs": 20,
        "max_pixels": 102400,
        "save_total_limit": 10,
        "lora_rank": 32,
        "lora_alpha": 32
    }
}'
```

图生视频-基于首尾帧（Wan2.2）

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "wan2.2-kf2v-flash",
    "training_file_ids": [
        "<替换为训练数据集的文件id>"
    ],
    "training_type": "efficient_sft",
    "hyper_parameters": {
        "n_epochs": 50,
        "batch_size": 4,
        "learning_rate": 2e-5,
        "split": 0.9,
        "max_split_val_dataset_sample": 5,
        "eval_epochs": 20,
        "max_pixels": 262144,
        "save_total_limit": 10,
        "lora_rank": 32,
        "lora_alpha": 32
    }
}'
```

使用OSS挂载的数据集

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "wan2.7-i2v",
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
    "training_type": "efficient_sft",
    "hyper_parameters": {
        "n_epochs": 50,
        "batch_size": 1,
        "learning_rate": 2e-5,
        "split": 0.9,
        "max_split_val_dataset_sample": 5,
        "eval_epochs": 20,
        "max_pixels": 102400,
        "save_total_limit": 10,
        "lora_rank": 32,
        "lora_alpha": 32
    }
}'
```

### 响应参数

**request\_id** `string`

请求的唯一标识符。

**output** `object`

任务详情。

属性

**job\_id** `string`

模型微调任务唯一标识，用于查询任务详情、日志、取消或删除任务。生成规则：`ft-{yyyyMMddHHmm}-{4位uuid}`。

**job\_name** `string`

模型微调任务名称。

**status** `string`

微调训练任务的状态：

-   `PENDING`：训练待开始。
-   `QUEUING`：训练正在排队（同一时间只能运行一个微调任务）。
-   `RUNNING`：训练正在进行中。
-   `SUCCEEDED`：训练成功。
-   `FAILED`：训练失败。
-   `CANCELED`：训练已取消。
-   `CANCELING`：训练正在取消中。

**finetuned\_output** `string`

微调后产出的新模型ID，部署和调用时需要用到。任务状态为 SUCCEEDED 时返回。

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

模型微调的训练方式。

**create\_time** `string`

任务创建时间。

**end\_time** `string`

任务结束时间。任务状态为 SUCCEEDED、FAILED 或 CANCELED 时返回。

**usage** `integer`

微调任务消耗的 Token 数。任务状态为 SUCCEEDED 或 CANCELED 时返回。

**workspace\_id** `string`

阿里云百炼API Key所属的业务空间ID。请参见[获取Workspace ID](raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

**user\_identity** `string`

用户标识，阿里云账号ID。

**creator** `string`

创建人的阿里云账号ID。

**modifier** `string`

修改人的阿里云账号ID。

**group** `string`

模型微调任务分组。

**max\_output\_cnt** `integer`

训练期间最多保存的 checkpoint 数量。等同于超参数 save\_total\_limit 的值。

**code** `string`

错误码。调用失败时返回。请参见下方错误码表。

**message** `string`

错误详情描述。调用失败时返回。

#### 成功响应示例

重点关注：`output.job_id`（任务ID）、`output.finetuned_output`（微调后产出的新模型名称）。

```
{
    "request_id": "0eb05b0c-02ba-414a-9d0c-xxxxxxxxx",
    "output": {
        "job_id": "ft-202511111122-xxxx",
        "job_name": "ft-202511111122-xxxx",
        "status": "PENDING",
        "finetuned_output": "wan2.5-i2v-preview-ft-202511111122-xxxx",
        "model": "wan2.5-i2v-preview",
        "base_model": "wan2.5-i2v-preview",
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
            "n_epochs": 50,
            "batch_size": 2,
            "learning_rate": 2.0E-5,
            "split": 0.9,
            "eval_epochs": 20
        },
        "training_type": "efficient_sft",
        "create_time": "2025-11-11 11:22:22"
    }
}
```

#### 错误响应示例

```
{
    "code": "InvalidParameter",
    "request_id": "BE213CDD-8A5C-59EE-9A67-055EAB0CB59B",
    "message": "The model wan2.7-i2v does not support training_type: full_sft"
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
