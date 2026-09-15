# 图像生成-创建调优任务

创建一个图像生成的模型微调训练任务。数据集支持通过API上传数据集或OSS挂载。

## 适用范围

-   **适用地域**：本文描述的功能**仅在华北2（北京）地域**可用，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。
-   **开通账号权限**：若使用[阿里云子账号](raw/model-user-guide/security-and-compliance/permission-management-overview.md)（[RAM用户](https://help.aliyun.com/zh/ram/user-guide/overview-of-ram-users)），需要为子账号授予模型调用、训练和部署[权限](raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
-   **配置环境变量**：已成功[获取 API Key](raw/model-api-reference/preparations/get-api-key.md)，并[配置到环境变量](raw/model-api-reference/preparations/get-api-key.md)。
-   **准备工作**：已阅读[图像生成模型调优](raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md)，了解支持微调的模型、微调步骤、数据格式以及计费说明。

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

-   `wan2.7-image-pro`：推荐用于文生图/图生图微调。
-   `wan2.7-image`
-   `qwen-image-2.0`：千问图像生成模型。支持的超参数与万相不同，请参见下方**超参数属性（qwen-image-2.0）**。

**training\_file\_ids** `array[string]` **（条件必选）**

训练集文件ID数组，可传入多个ID。与 `training_datasets` 二选一，若使用 `training_datasets` 则无需传此参数。文件ID通过[上传文件 API](https://help.aliyun.com/zh/model-studio/upload-file-api) 获取。

**validation\_file\_ids** `array[string]` （可选）

验证集文件ID数组，可传入多个ID。与 `validation_datasets` 二选一，若使用 `validation_datasets` 则无需传此参数。若两者均不提供，系统会从训练集中自动划分。文件ID通过[上传文件 API](https://help.aliyun.com/zh/model-studio/upload-file-api) 获取。

**training\_type** `string` **（必选）**

微调类型，当前仅支持`efficient_sft`（LoRA高效微调）。

**hyper\_parameters** `object` （可选）

**超参数配置**。初次训练时，推荐使用默认的超参数。若模型效果不佳或训练不收敛，可以尝试调整训练量（万相为 max\_steps，qwen-image-2.0 为 n\_epochs）或 learning\_rate 等参数。不同基准模型支持的超参数不同，请参见下方对应的超参数属性。

超参数属性（wan2.7-image-pro、wan2.7-image）

**max\_steps** `int` **（必选）**

训练总步数。控制训练时长的核心参数。推荐值：800。

max\_steps 决定训练迭代次数，max\_token\_length 决定每步处理的数据量。

建议不少于 500 步以确保模型充分收敛；大数据集可适当增加步数。

**重要**该参数影响[训练计费](raw/model-user-guide/test-1/model-training-and-deployment-billing.md)，请合理设置。

**eval\_steps** `int` **（必选）**

验证间隔。推荐值：200。取值需≥0。训练期间每隔多少个 steps 进行一次验证评估，用于阶段性评估模型训练效果。同时保存当前 step 的模型文件。

**learning\_rate** `float` **（必选）**

学习率。推荐值：3e-5。控制模型权重更新的幅度。过高可能导致模型变差，过低则变化不明显。

**generation\_type** `string` **（必选）**

生成模式。决定训练数据格式和推理方式。可选值：

-   `t2i`：文生图模式。
-   `i2i`：图生图模式。

**max\_pixels** `string` **（必选）**

训练图片的最大分辨率。设置训练集中图片分辨率的像素总数（宽×高）上限，系统仅对超过该值的图片进行缩放处理，未超限的图片保持原样。建议三个分辨率参数（max\_pixels、max\_token\_length、val\_img\_size）保持一致。

-   `1k`：即 1024×1024。
-   `2k`：即 2048×2048。

推荐值：文生图 2k，图生图 1k。

**val\_img\_size** `string` **（必选）**

验证图生成分辨率。训练过程中验证评估时生成图片的目标分辨率。可选值同 max\_pixels。推荐值：文生图 2k，图生图 1k。

**max\_token\_length** `string` **（必选）**

每步训练的最大 Token 长度，影响单步计算量与计费。与 max\_steps 共同控制训练过程：max\_steps 决定迭代次数，max\_token\_length 决定每步处理的数据量。可选值：

-   `1k`：推荐图生图场景使用。
-   `2k`：推荐文生图场景使用。

max\_token\_length 与计费 Lmax 的对应关系：

**generation\_type**

**max\_token\_length**

**L****max**

t2i（文生图）

1k

12,800

2k

23,220

i2i（图生图）

1k

23,220

2k

32,000

**gradient\_clip** `float` **（必选）**

梯度裁剪。推荐值：0.5。对所有可训练参数做全局梯度范数裁剪的阈值，防止梯度爆炸。设为 -1 表示不裁剪。

**weight\_decay** `float` **（必选）**

权重衰减。推荐值：0.02。AdamW 解耦式权重衰减系数，对所有可训练参数生效，用于正则化防止过拟合。

**lora\_rank** `int` **（必选）**

LoRA 低秩矩阵的维数。推荐值：32。该值决定了微调参数量的大小。数值越大，模型拟合能力越强，但训练速度会变慢。取值必须为2n（如 16、32、64）。

**save\_total\_limit** `int` （可选）

Checkpoint 保存数量上限。推荐值：10。限制最多保存的模型数量。系统将始终只保存训练生成的最后 N 个 Checkpoint。

**split** `float` （可选）

训练集划分比例。推荐值：0.9。取值范围为 (0, 1)。仅在未指定`validation_file_ids`或`validation_datasets`时生效。此参数用于从训练集中自动按比例拆分出验证集。例如，0.9表示90%训练集，10%验证集。

超参数属性（qwen-image-2.0）

qwen-image-2.0 按**训练轮数**（n\_epochs）控制训练过程，不支持 max\_steps、eval\_steps 和 max\_token\_length 参数。

**n\_epochs** `int` **（必选）**

训练轮数。模型在训练集上完整迭代的次数。推荐值：10。取值范围：\[1, 10000\]。轮数越多模型拟合越充分，但过多可能导致过拟合。

**重要**该参数影响[训练计费](raw/model-user-guide/test-1/model-training-and-deployment-billing.md)，请合理设置。

**eval\_epochs** `int` **（必选）**

验证间隔轮数。推荐值：10。取值范围：\[1, 1000\]。训练期间每隔多少轮进行一次验证评估，用于阶段性评估模型训练效果。同时保存当前轮次的模型文件。

**batch\_size** `int` （可选）

批次大小。每次参数更新使用的样本数。推荐值：8。取值范围：\[1, 2048\]。该参数不参与计费，不影响训练Token总量。

**learning\_rate** `float` **（必选）**

学习率。推荐值：5e-5。控制模型权重更新的幅度。过高可能导致模型变差，过低则变化不明显。

**generation\_type** `string` **（必选）**

生成模式。决定训练数据格式和推理方式。可选值：

-   `t2i`：文生图模式。
-   `i2i`：图生图模式。

推荐值：i2i。

**max\_pixels** `string` **（必选）**

训练图片的最大分辨率。取值为字符串档位，设置训练集中图片分辨率的像素总数（宽×高）上限，系统仅对超过该值的图片进行缩放处理，未超限的图片保持原样。可选值：

-   `1k`：即 1024×1024。
-   `2k`：即 2048×2048。

推荐值：2k。建议与 val\_img\_size 保持一致。

**重要**该参数影响[训练计费](raw/model-user-guide/test-1/model-training-and-deployment-billing.md)，请合理设置。

**val\_img\_size** `string` **（必选）**

验证图生成分辨率。训练过程中验证评估时生成图片的目标分辨率。可选值同 max\_pixels。推荐值：2k。

**gradient\_clip** `float` **（必选）**

梯度裁剪。推荐值：0.5。取值范围：\[0, 10.0\]。对所有可训练参数做全局梯度范数裁剪的阈值，防止梯度爆炸。

**weight\_decay** `float` **（必选）**

权重衰减。推荐值：0.02。取值范围：\[0, 1.0\]。AdamW 解耦式权重衰减系数，对所有可训练参数生效，用于正则化防止过拟合。

**lora\_rank** `int` **（必选）**

LoRA 低秩矩阵的维数。推荐值：32。取值范围：\[8, 128\]。该值决定了微调参数量的大小。数值越大，模型拟合能力越强，但训练速度会变慢。

**save\_total\_limit** `int` （可选）

Checkpoint 保存数量上限。推荐值：20。取值范围：\[1, 40\]。限制最多保存的模型数量。系统将始终只保存训练生成的最后 N 个 Checkpoint。

**split** `float` （可选）

训练集划分比例。推荐值：0.9。取值范围：\[0, 1\]。仅在未指定`validation_file_ids`或`validation_datasets`时生效。此参数用于从训练集中自动按比例拆分出验证集。例如，0.9表示90%训练集，10%验证集。

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

文生图（wan2.7-image-pro）

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "wan2.7-image-pro",
    "training_file_ids": [
        "<替换为训练数据集的文件id>"
    ],
    "training_type": "efficient_sft",
    "hyper_parameters": {
        "learning_rate": 3e-5,
        "max_steps": 800,
        "eval_steps": 200,
        "max_token_length": "2k",
        "gradient_clip": 0.5,
        "weight_decay": 0.02,
        "max_pixels": "2k",
        "val_img_size": "2k",
        "generation_type": "t2i",
        "lora_rank": 32,
        "save_total_limit": 10
    }
}'
```

图生图（wan2.7-image）

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "wan2.7-image",
    "training_file_ids": [
        "<替换为训练数据集的文件id>"
    ],
    "training_type": "efficient_sft",
    "hyper_parameters": {
        "learning_rate": 3e-5,
        "max_steps": 800,
        "eval_steps": 200,
        "max_token_length": "1k",
        "gradient_clip": 0.5,
        "weight_decay": 0.02,
        "max_pixels": "1k",
        "val_img_size": "1k",
        "generation_type": "i2i",
        "lora_rank": 32,
        "save_total_limit": 10
    }
}'
```

千问（qwen-image-2.0）

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "qwen-image-2.0",
    "training_file_ids": [
        "<替换为训练数据集的文件id>"
    ],
    "training_type": "efficient_sft",
    "hyper_parameters": {
        "learning_rate": 5e-5,
        "n_epochs": 10,
        "eval_epochs": 10,
        "batch_size": 8,
        "gradient_clip": 0.5,
        "weight_decay": 0.02,
        "max_pixels": "2k",
        "val_img_size": "2k",
        "generation_type": "t2i",
        "lora_rank": 32,
        "save_total_limit": 20
    }
}'
```

使用OSS挂载的数据集

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "wan2.7-image-pro",
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
        "learning_rate": 3e-5,
        "max_steps": 800,
        "eval_steps": 200,
        "max_token_length": "2k",
        "gradient_clip": 0.5,
        "weight_decay": 0.02,
        "max_pixels": "2k",
        "val_img_size": "2k",
        "generation_type": "t2i",
        "lora_rank": 32,
        "save_total_limit": 10
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
        "job_id": "ft-202606030110-xxxx",
        "job_name": "ft-202606030110-xxxx",
        "status": "PENDING",
        "finetuned_output": "wan2.7-image-pro-ft-202606030110-xxxx",
        "model": "wan2.7-image-pro",
        "base_model": "wan2.7-image-pro",
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
            "max_steps": 800,
            "learning_rate": 3.0E-5,
            "eval_steps": 200,
            "max_token_length": "2k",
            "max_pixels": "2k",
            "val_img_size": "2k",
            "generation_type": "t2i",
            "lora_rank": 32
        },
        "training_type": "efficient_sft",
        "create_time": "2026-06-03 01:10:47"
    }
}
```

#### 错误响应示例

```
{
    "code": "InvalidParameter",
    "request_id": "BE213CDD-8A5C-59EE-9A67-055EAB0CB59B",
    "message": "The model wan2.7-image-pro does not support training_type: full_sft"
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
