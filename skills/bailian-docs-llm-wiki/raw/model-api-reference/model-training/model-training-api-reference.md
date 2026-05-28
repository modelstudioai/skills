# 模型调优 API 参考

本文为您提供模型调优（模型训练、模型微调）的HTTP调用API参考。

**重要**

本文档仅适用于中国大陆版（北京地域）。

使用这些API，您可以：

-   创建一个模型调优任务。
    
-   查看或列举调优任务及其状态。
    
-   查看特定调优任务的过程日志。
    
-   取消或删除一个调优任务。
    

## **前提条件**

-   您已经阅读了[模型调优简介](https://help.aliyun.com/zh/model-studio/model-training-overview)和[使用 API 进行模型调优](https://help.aliyun.com/zh/model-studio/fine-tuning-api-guide)，了解了如何使用模型调优API并熟悉如何在阿里云百炼平台进行模型调优的基本步骤。
    
-   已配置了百炼的 API-KEY， 请参考[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。
    

### **文件管理**

请查看[模型定制文件管理服务 API 参考](https://help.aliyun.com/zh/model-studio/model-customization-file-management-service)。

## 创建调优任务

> Windows CMD 请将`${DASHSCOPE_API_KEY}`替换为`%DASHSCOPE_API_KEY%`，PowerShell请替换为 `$env:DASHSCOPE_API_KEY`

```
curl --location --request POST "https://dashscope.aliyuncs.com/api/v1/fine-tunes" \
--header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
--header 'Content-Type: application/json' \
--data '{
    "model":"qwen3-14b",
    "training_file_ids":[
        "86a9fe7f-dd77-43b0-9834-2170e12339ec",
        "03ead352-6190-4328-8016-61821c23d4fc"
    ],
    "hyper_parameters":{
        "n_epochs":3,
        "batch_size":32,
        "max_length":8192,
        "learning_rate":"1.6e-5",
        "lr_scheduler_type":"linear",
        "split":0.9
    },
    "training_type":"sft",
    "finetuned_output_suffix":"suffix"
}'
```

### **输入参数**

**字段**

**必选**

**类型**

**传参方式**

**参数说明**

training\_file\_ids

是

Array

Body

训练集文件ID列表，文件ID由[模型定制文件管理服务 API](https://help.aliyun.com/zh/model-studio/model-customization-file-management-service) 产生。

validation\_file\_ids

否

Array

Body

测试集文件ID列表，文件ID由[模型定制文件管理服务 API](https://help.aliyun.com/zh/model-studio/model-customization-file-management-service) 产生。

model

是

String

Body

用于调优的[基础模型ID](https://help.aliyun.com/zh/model-studio/fine-tuning-api-guide#4825f2a597fjq)基础模型 ID；或其他调优任务产出的模型ID（对已经调优了的模型进行再次调优）。

hyper\_parameters

否

Map

Body

调优时的超参列表。不同模型支持的参数及其默认值不同，**请在控制台选择相同的模型和训练方式查看实际默认值**。以下参数影响训练费用，**必须填写**：`n_epochs`（循环次数）、`batch_size`（批次大小）、`max_length`（序列长度）。各参数详情请参见[hyper\_parameters 参数说明](https://help.aliyun.com/zh/model-studio/fine-tuning-api-guide#647c159c9dn6e)。

training\_type

否

String

Body

训练方法，可选值为：`cpt`、`sft`、`efficient_sft`、`dpo_full`、`dpo_lora`。

job\_name

否

String

Body

调优任务名称

model\_name

否

String

Body

调优完成后的模型名称

#### `hyper_parameters`内**支持的设置**

> 不同模型支持的参数及其默认值不同，**请前往[控制台](https://bailian.console.aliyun.com/?tab=model#/efm/model_manager)选择相同的模型和训练方式查看实际默认值**。

**参数名称**

**推荐设置**

类型

**超参作用**

`n_epochs`

（循环次数）**【必填】**

**数据量 < 10,000, 3~5次**

**数据量 > 10,000, 1~2次**

Integer

模型遍历训练的次数，请根据模型调优实际使用经验进行调整。

模型训练循环次数越多，训练时间越长，训练费用越高。

`learning_rate`

（学习率）

使用百炼推荐的默认值

Float

控制模型修正权重的强度。

-   学习率设置得太高，模型参数会剧烈变化，导致调优后的模型表现不一定更好，甚至变差；
    
-   学习率太低，调优后的模型表现不会有太大变化。
    

`freeze_vit`

（是否冻结视觉主干网络）

根据需求调整

Boolean

用于冻结视觉主干网络的参数，使其在训练过程中不更新权重。仅适用于 千问-VL（视觉理解）模型。

**说明**

只有 freeze\_vit 设置为“true”时，模型才能进行按 [Token 用量](https://help.aliyun.com/zh/model-studio/model-deployment-introduction#9ea9924cd8138)计费。

`batch_size`

（批次大小）**【必填】**

使用百炼推荐的默认值

Integer

一次性送入模型进行训练的数据条数，参数过小会显著延长训练时间。不同模型的默认值不同，请前往控制台查看。

`eval_steps`

（验证步数）

根据需求调整

Integer

训练阶段针对模型的验证间隔步长，用于阶段性评估模型训练准确率、训练损失。

该参数影响模型调优进行时的 Validation Loss 和 Validation Token Accuracy 的显示频率。

`logging_steps`

（日志显示步数）

根据需求调整

Integer

调优日志打印的步数。

`lr_scheduler_type`

（学习率调整策略）

推荐`linear`/`Inverse_sqrt`

String

在模型训练中动态调整学习率的策略。

各策略详情请参考[在控制台进行模型调优](https://help.aliyun.com/zh/model-studio/model-training-on-console#7864d6a606ztg)。

`max_length`

（序列长度）**【必填】**

8192

Integer

指的是单条训练数据 token 支持的最大长度。如果单条数据 token 长度超过设定值，调优会直接丢弃该条数据，不进行训练。

字符与 token 之间的关系请参考[Token和字符串之间怎么换算](https://help.aliyun.com/zh/model-studio/billing-for-model-studio#35d3b2ad2386c)

`max_split_val_dataset_sample`

（验证集数据最大数量）

使用百炼推荐的默认值

Integer

当不设置`"validation_file_ids"`时，阿里云百炼自动分割的验证集最多只有1000条。

当设置了`"validation_file_ids"`时，该参数无效。

`split`

（训练集在训练文件中占比）

使用百炼推荐的默认值

Float

当不设置`"validation_file_ids"`时，阿里云百炼会自动把训练文件中的80%作为训练集，20%作为验证集。

当设置了`"validation_file_ids"`时，该参数无效。

`warmup_ratio`

（学习率预热比例）

使用百炼推荐的默认值

Float

学习率预热占用总的训练过程的比例。学习率预热是指学习率在训练开始后由一个较小值线性递增至学习率设定值。

该参数主要是限制模型参数在训练初始阶段的变化幅度，从而帮助模型更稳定地进行训练。

比例过大效果与过低的学习率相同，会导致调优后的模型表现不会有太大变化。

比例过小效果与过高的学习率相同，可能导致调优后的模型表现不一定更好，甚至变差。

> 该参数仅对学习率调整策略“Constant”无效。

`weight_decay`

（权重衰减）

使用百炼推荐的默认值

Float

L2正则化强度。L2正则化能在一定程度上保持模型的通用能力。数值过大会导致模型调优效果不明显。

**高效微调（支持**`efficient_sft`、`dpo_lora`**）参数**

**说明**

当对一个已经高效微调后的模型进行二次高效微调时，`lora_rank`、`lora_alpha`、`lora_dropout`三个参数必须保持一致。

`lora_rank`

（LoRA秩值）

64

Integer

LoRA训练中的低秩矩阵的秩大小。秩越大调优效果越好，但训练会略慢。

`lora_alpha`

（LoRA阿尔法）

使用百炼推荐的默认值

Integer

用于控制原模型权重与LoRA的低秩修正项之间的结合缩放系数。

较大的Alpha值会给予LoRA修正项更多权重，使得模型更加依赖于微调任务的特定信息；

而较小的Alpha值则会让模型更倾向于保留原始预训练模型的知识。

`lora_dropout`

（LoRA丢弃率）

使用百炼推荐的默认值

Float

LoRA训练中的低秩矩阵值的丢弃率。

使用推荐数值能增强模型通用化能力。

数值过大会导致模型微调效果不明显。

**混合训练（支持**`efficient_sft`、`sft`**）参数**

`data_augmentation`

（是否开启混合训练）

根据模型的使用场景混合

Boolean

开启后，训练数据将与百炼提供的通用数据集（多领域/多行业/多场景）混合：

\- 效果：提升训练效果，避免模型能力退化。

\- 计费：混合数据计入总训练Token，按标准计费。

`augmentation_types`

（选择预置数据的类型）

根据模型的使用场景混合

例：`"augmentation_types": "dialogue_CN,general_purpose_CN,NLP"`

> 需与`augmentation_ratio`配合使用

String

**数据集 code**

**数据集名称**

**支持的模型**

`dialogue_cn`

中文-对话

千问 2 系列

`math_cn`

中文-数学

`general_coding_cn`

中文-代码

`general_purpose_cn`

中文-通用

`nlp`

NLP 理解

`dialogue_en`

英文-对话

`math_en`

英文-数学

`general_coding_en`

英文-代码

`general_purpose_en`

英文-通用

`mix_v2`

通用-V2

千问 3 系列

`vl_mix`

通用

千问 3 VL 系列

`augmentation_ratio`

（设置混合倍率）

根据模型的使用场景混合

String

-   格式要求：与`augmentation_types`一一对应
    
-   示例：`"0.1,0.05,0.15"`（分别对应`augmentation_types`列出的三种数据集）
    
-   含义：按训练数据量的`10%/5%/15%`随机抽取混合
    
-   范围：`0.0 ~ 2.0`
    

**模型参数快照发布（仅支持**`efficient_sft`、`sft`**）参数**

`save_strategy`

（快照存储策略）

可以设置为 `epoch`或`steps`。

-   设置为`steps`时，可以通过设置`save_steps`参数，调整保存间隔。
    

String

设置调优过程中，保存模型参数快照（Checkpoint）的保存间隔和保存数量上限。

`save_steps`

（存储步数）

如果需要手动修改，建议设置为`eval_steps`参数的整数倍。

Integer

设置每训练多少步保存一次模型参数快照（Checkpoint）。

`save_total_limit`

（快照存储数量上限）

10

Integer

限制最多保存多少个模型参数快照（Checkpoint）用于发布。

### **返回样例**

```
{
    "request_id": "9654e55a-d74b-4113-aee1-fa19c9384fcc",
    "output": {
        "job_id": "ft-202410291653-1c7f",
        "job_name": "ft-202410291653-1c7f",
        "status": "PENDING",
        "model": "qwen3-14b",
        "base_model": "qwen3-14b",
        "training_file_ids": [
            "976bd01a-f30b-4414-86fd-50c54486e3ef"
        ],
        "validation_file_ids": [

        ],
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
        "workspace_id":"llm-v71tlv***",
        "user_identity": "1396993924585947",
        "modifier": "1396993924585947",
        "creator": "1396993924585947",
        "group": "llm"
    }
}
```

### **返回参数**

**参数名称**

**类型**

**参数说明**

request\_id

String

本次请求的ID。

output

Object

本次调优任务的详细信息。

output.job\_id

String

本次调优的任务ID，用于后续查询状态。

生成规则：`ft-{yyyyMMddHHmm}-{4位uuid}`。

output.jobs\_name

String

同`output.job_id`。

output.status

String

本次调优[任务的状态](#2287fa490f9ga)。

output.model

String

调优任务使用的模型ID。

output.base\_model

String

调优任务使用的模型对应的基础模型ID。

比如：调优任务`ft-202410291653-1c7f`使用的基础模型是`qwen3-14b`。

output.training\_file\_ids

Array

训练文件ID列表。

output.validation\_file\_ids

Array

验证文件ID列表。

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

对该调优任务进行最后一次操作的账号UID。

比如：某个子账号取消了该任务，该子账号UID会显示在这里。

output.creator

String

该调优任务创建人UID。

output.group

String

模型调优的任务类型。

**任务状态**

**含义**

PENDING

训练待开始。

QUEUING

训练正在排队（同时只有一个训练任务可以进行）

RUNNING

训练正在进行中。

CANCELING

训练正在取消中。

SUCCEEDED

训练成功。

FAILED

训练失败。

CANCELED

训练已经取消。

## 查询调优任务详情

> Windows CMD 请将`${DASHSCOPE_API_KEY}`替换为 `%DASHSCOPE_API_KEY%`，PowerShell 请替换为 `$env:DASHSCOPE_API_KEY`

```
curl --location --request GET "https://dashscope.aliyuncs.com/api/v1/fine-tunes/<替换为您的调优任务id>" \
--header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
--header 'Content-Type: application/json'
```

### **输入参数**

**字段**

**类型**

**传参方式**

**必选**

**描述**

job\_id

String

Url Path

是

要查询的调优任务的ID。即[创建调优任务返回参数](#5029d0724bzmm)中的job\_id。

### **返回样例**

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
        "training_file_ids": [
            "976bd01a-f30b-4414-86fd-50c54486e3ef"
        ],
        "validation_file_ids": [

        ],
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
        "workspace_id":"llm-v71tlv***",
        "user_identity": "1396993924585947",
        "modifier": "1396993924585947",
        "creator": "1396993924585947",
        "end_time": "2024-10-29 17:11:26",
        "group": "llm",
        "usage": 279808
    }
}
```

### **返回参数**

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

本次调优[任务的状态](#2287fa490f9ga)。

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

训练文件ID列表。

output.validation\_file\_ids

Array

验证文件ID列表。

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

调优任务消耗的Token（count）数，扣费计算公式请参考：[计费项](https://help.aliyun.com/zh/model-studio/billing-for-model-studio#cd67c8d10ekx2)。当任务状态为“SUCCEED”、“CANCELED”时出现。

## 列举调优任务

> Windows CMD 请将`${DASHSCOPE_API_KEY}`替换为 `%DASHSCOPE_API_KEY%`，PowerShell 请替换为 `$env:DASHSCOPE_API_KEY`

```
curl --location --request GET "https://dashscope.aliyuncs.com/api/v1/fine-tunes?model=qwen3-14b&page_no=2" \
--header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
--header 'Content-Type: application/json'
```

### **输入参数**

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

默认10，最大值100，最小值1

model

String

Query

否

模型ID，指定该参数表示只列举基于该模型的调优任务

### **返回样例**

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
                "training_file_ids": [
                    "976bd01a-f30b-4414-86fd-50c54486e3ef"
                ],
                "validation_file_ids": [

                ],
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
                "workspace_id":"llm-v71tlv***",
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
                "training_file_ids": [
                    "86a9fe7f-dd77-43b0-9834-2170e12339ec",
                    "03ead352-6190-4328-8016-61821c23d4fc"
                ],
                "validation_file_ids": [

                ],
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
                "workspace_id":"llm-v71tlv***",
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

### **返回参数**

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

多个调优任务详情，详细参数请参考[调优任务详情返回参数](#tb2)。

## **获取调优任务日志**

> Windows CMD 请将`${DASHSCOPE_API_KEY}`替换为 `%DASHSCOPE_API_KEY%`，PowerShell 请替换为 `$env:DASHSCOPE_API_KEY`

```
curl --location --request GET "https://dashscope.aliyuncs.com/api/v1/fine-tunes/<替换为您的调优任务id>/logs?offset=10&line=10" \
--header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
--header 'Content-Type: application/json'
```

### **输入参数**

**字段**

**类型**

**传参方式**

**必选**

**描述**

job\_id

String

Url Path

是

要打印日志的调优任务ID。

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

### **返回样例**

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

### **返回参数**

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

Integer

输出的日志。

## **取消调优任务**

> Windows CMD 请将`${DASHSCOPE_API_KEY}`替换为 `%DASHSCOPE_API_KEY%`，PowerShell 请替换为 `$env:DASHSCOPE_API_KEY`

```
curl --location --request POST "https://dashscope.aliyuncs.com/api/v1/fine-tunes/<替换为您的调优任务id>/cancel" \
--header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
--header 'Content-Type: application/json'
```

### **输入参数**

**字段**

**类型**

**传参方式**

**必选**

**描述**

job\_id

String

Url Path

是

要取消的调优任务ID。

### **返回样例**

```
{
    "request_id": "670fca9d-48dd-4c5a-83e7-33bcc20420f8",
    "output": {
        "status": "success"
    }
}
```

### **返回参数**

**参数名称**

**类型**

**参数说明**

request\_id

String

本次请求的ID。

output

Object

取消操作返回的详细信息。

## **取消调优任务**

> Windows CMD 请将`${DASHSCOPE_API_KEY}`替换为 `%DASHSCOPE_API_KEY%`，PowerShell 请替换为 `$env:DASHSCOPE_API_KEY`

```
curl --location --request POST "https://dashscope.aliyuncs.com/api/v1/fine-tunes/<替换为您的调优任务id>/cancel" \
--header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
--header 'Content-Type: application/json'
```

### **输入参数**

**字段**

**类型**

**传参方式**

**必选**

**描述**

job\_id

String

Url Path

是

要取消的调优任务ID。

### **返回样例**

```
{
    "request_id": "670fca9d-48dd-4c5a-83e7-33bcc20420f8",
    "output": {
        "status": "success"
    }
}
```

### **返回参数**

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

> Windows CMD 请将`${DASHSCOPE_API_KEY}`替换为 `%DASHSCOPE_API_KEY%`，PowerShell 请替换为 `$env:DASHSCOPE_API_KEY`

```
curl --location --request DELETE "https://dashscope.aliyuncs.com/api/v1/fine-tunes/<替换为您的调优任务id>" \
--header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
--header 'Content-Type: application/json'
```

### **输入参数**

**字段**

**类型**

**传参方式**

**必选**

**描述**

job\_id

String

Url Path

是

要删除的调优任务ID。

### **返回样例**

```
{
    "request_id": "7d7e1469-df77-4163-83ce-54425df744ed",
    "output": {
        "status": "success"
    }
}
```

### **返回参数**

**参数名称**

**类型**

**参数说明**

request\_id

String

本次请求的ID。

output

Object

删除操作返回的详细信息。

## **调优任务状态**

**任务状态**

**含义**

PENDING

训练待开始。

QUEUING

训练正在排队（同时只有一个训练任务可以进行）

RUNNING

训练正在进行中。

CANCELING

训练正在取消中。

SUCCEEDED

训练成功。

FAILED

训练失败。

CANCELED

训练已经取消。

## **请求错误码说明**

请求异常时返回

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

请求异常示例

```
{
  "code": "NotFound",
  "request_id": "BE213CDD-8A5C-59EE-9A67-055EAB0CB59B",
  "message": "Not Found!"
}
```

错误码列表

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
    
-   如您确实需要提高训练任务的并发量或保留更多训练成功的模型，请联系商务经理。
    

500

InternalError

Internal server error!

内部错误。

记录 request\_id，通过工单联系阿里云工程师进行排查。

UID
