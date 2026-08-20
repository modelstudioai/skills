# 使用 API 或命令行进行模型调优

## 前提条件

-   已经完整阅读了[模型调优简介](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)，了解模型调优的基本概念、流程及数据格式要求。
-   已开通服务并获得API-KEY， 请参考[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。
-   [阿里云子账号](raw/model-user-guide/security-and-compliance/permission-management-overview.md)（[RAM用户](https://help.aliyun.com/zh/ram/user-guide/overview-of-ram-users)）需被授予必要的调用、训练和部署权限。

**说明**通过 API 创建的训练任务仅支持按 Token 计费，暂不支持使用模型训练单元（预付费或后付费）。如需使用训练单元，请通过控制台创建任务。

## 上传调优文件

### 准备调优文件

SFT/DPO/CPT 各训练方式的数据格式规格、打包规则、大小与数量限制、API 上传配额详见[调优数据上传规则](https://help.aliyun.com/zh/model-studio/text-generation-tuning-data-upload-rules#sec-support-matrix)。各训练方式支持的文件格式概览：

**训练方式**

**文件格式**

SFT 文本生成

jsonl（ChatML messages 多轮结构）

SFT 多模态（图片/视频）

zip（data.jsonl + 图片/视频文件）

DPO

jsonl（chosen/rejected 偏好对比）

CPT

jsonl（纯文本 {text}）

评测集

xlsx

也可以前往[百炼控制台](https://bailian.console.aliyun.com/cn-beijing?tab=model#/efm/model_data/createDataAss)下载数据模板。

在**新增数据集**页面的上传文件区域下方，可找到**数据模板**下载链接。

### 将调优文件上传至阿里云百炼

#### DashScope API

> Windows CMD 请将`${DASHSCOPE_API_KEY}`替换为 `%DASHSCOPE_API_KEY%`，PowerShell 请替换为 `$env:DASHSCOPE_API_KEY`

```
curl --request POST \
'https://dashscope.aliyuncs.com/api/v1/files' \
--header 'Authorization: Bearer '${DASHSCOPE_API_KEY} \
--form 'files=@"/path/to/your/file.jsonl"' \
--form 'purpose="fine-tune"' \
--form 'descriptions="a sample fine-tune data file for qwen"'
```

**说明**使用限制：

-   单个文件大小最大为300MB
-   所有的有效文件（未删除）总使用空间配额为100GB
-   所有的有效文件（未删除）总数量配额为10000个
-   文件存储没有时间限制

通过 API 上传的调优文件，在百炼控制台模型调优页面与 API 调用中均可见可用。

更多详细信息请参见[上传文件](https://help.aliyun.com/zh/model-studio/upload-file-api)。

返回结果：

```
{
  "request_id":"xx",
  "data":{
    "uploaded_files":[{
      "file_id":"976bd01a-f30b-4414-86fd-50c54486e3ef",
      "name":"qwen-fine-tune-sample.jsonl"}],
  　"failed_uploads":[]}
 }
```

## 模型调优

### 创建调优任务

#### HTTP

> Windows CMD 请将`${DASHSCOPE_API_KEY}`替换为 `%DASHSCOPE_API_KEY%`，PowerShell 请替换为 `$env:DASHSCOPE_API_KEY`

```
curl --location "https://dashscope.aliyuncs.com/api/v1/fine-tunes" \
--header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
--header 'Content-Type: application/json' \
--data '{
    "model":"qwen3-8b",
    "training_datasets":[
        {"data_source_type":"file_id","file_id":"<替换为训练数据集的file_id1>"},
        {"data_source_type":"oss_mount","mount_storage":{"region":"cn-beijing","bucket":"example_bucket","file_path":"dataset/data.jsonl"}}
    ],
    "validation_datasets":[
        {"data_source_type":"file_id","file_id":"<替换为测试数据集的file_id>"},
        {"data_source_type":"oss_mount","mount_storage":{"region":"cn-beijing","bucket":"example_bucket","file_path":"dataset/val.jsonl"}}
    ],
    "hyper_parameters":
    {
        "n_epochs": 3,
        "batch_size": 16,
        "max_length": 8192,
        "learning_rate": "1.6e-5",
        "lr_scheduler_type": "linear",
        "split": 0.9,
        "warmup_ratio": 0.05,
        "eval_steps": 50,
        "data_augmentation": true,
        "augmentation_ratio": "0.1,0.05,0.15",
        "augmentation_types": "dialogue_CN,general_purpose_CN,NLP",
        "save_strategy": "epoch",
        "save_total_limit": 10
    },
    "training_type":"sft"
}'
```

**说明**使用 OSS 挂载方式加载数据集时，需将未经压缩的数据集文件夹整体上传到 OSS Bucket，不支持 zip 文件。MountStorage 的 file\_path 指定数据集的 data.jsonl 文件路径；对包含多个文件的数据集（如 data.jsonl 和图片/视频文件同目录），只需指定 data.jsonl 的路径，无需指定其他文件。挂载前需授权百炼服务访问您的 OSS 数据。OSS Bucket 所属地域支持北京（cn-beijing）和新加坡（ap-southeast-1）。

### 输入参数

**字段**

**必选**

**类型**

**传参方式**

**描述**

training\_datasets

是

Array of Dataset

Body

训练数据集列表。

validation\_datasets

否

Array of Dataset

Body

测试数据集列表。

model

是

String

Body

**用于调优的基础模型 ID，或其他调优任务产出的模型 ID。**

hyper\_parameters

否

Map

Body

用于调优模型的超参数。不同模型支持的参数及其默认值不同，请在控制台选择相同的模型和训练方式查看实际默认值。

以下参数影响训练费用，**必须填写**：`n_epochs`（循环次数）、`batch_size`（批次大小）、`max_length`（序列长度）。

training\_type

否

String

Body

调优方法，可选值为：

`cpt`

`sft`

`efficient_sft`

`dpo_full`

`dpo_lora`

job\_name

否

String

Body

调优任务名称

model\_name

否

String

Body

调优产生的模型名称（并非模型 ID，模型 ID 由系统生成）

## 返回样例

```
{
    "request_id": "635f7047-003e-4be3-b1db-6f98e239f57b",
    "output":
    {
        "job_id": "ft-202511272033-8ae7",
        "job_name": "ft-202511272033-8ae7",
        "status": "PENDING",
        "finetuned_output": "qwen3-8b-ft-202511272033-8ae7",
        "model": "qwen3-8b",
        "base_model": "qwen3-8b",
        "training_file_ids": [],
        "validation_file_ids": [],
        "training_datasets": [
            {"data_source_type": "file_id", "file_id": "9e9ffdfa-c3bf-436e-9613-6f053c66aa6e"}
        ],
        "validation_datasets": [],
        "hyper_parameters":
        {
            "n_epochs": 3,
            "batch_size": 16,
            "max_length": 8192,
            "learning_rate": "1.6e-5",
            "lr_scheduler_type": "linear",
            "split": 0.9,
            "warmup_ratio": 0.05,
            "eval_steps": 50,
            "data_augmentation": true,
            "augmentation_ratio": "0.1,0.05,0.15",
            "augmentation_types": "dialogue_CN,general_purpose_CN,NLP",
            "save_strategy": "epoch",
            "save_total_limit": 10
        },
        "training_type": "sft",
        "create_time": "2025-11-27 20:33:15",
        "workspace_id": "llm-8v53etv3hwb8orx1",
        "user_identity": "1654290265984853",
        "modifier": "1654290265984853",
        "creator": "1654290265984853",
        "group": "llm",
        "max_output_cnt": 10
    }
}
```

支持的基础模型ID（ model ）列表与训练类型（ training\_type ）支持情况：

##### 支持的模型

#### 文本生成

**说明**Qwen3.7-Plus-2026-05-26 调优后部署请联系商务经理。

**模型服务**

**模型代码**

**CPT全参训练（cpt）**

**SFT全参训练（sft）**

**SFT高效训练（efficient\_sft）**

**DPO全参训练（dpo\_full）**

**DPO高效训练（dpo\_lora）**

Qwen3.7-Plus-2026-05-26

qwen3.7-plus-2026-05-26

×

支持

×

×

×

Qwen3.6-Flash-2026-04-16

qwen3.6-flash-2026-04-16

×

支持

×

×

×

Qwen3.6-Plus-2026-04-02

qwen3.6-plus-2026-04-02

×

支持

×

×

×

Qwen3.5-27B

qwen3.5-27b

×

支持

支持

×

×

Qwen3.5-9B

qwen3.5-9b

×

支持

支持

×

×

Qwen3.5-Flash-2026-02-23

qwen3.5-flash-2026-02-23

×

支持

×

×

×

Qwen3.5-Plus-2026-02-15

qwen3.5-plus-2026-02-15

×

支持

×

×

×

Qwen3-32B

qwen3-32b

支持

支持

支持

支持

支持

Qwen3-30B-A3B-Instruct-2507

qwen3-30b-a3b-instruct-2507

支持

支持

支持

×

×

Qwen3-14B

qwen3-14b

×

支持

支持

支持

支持

Qwen3-8B

qwen3-8b

×

支持

支持

支持

支持

Qwen3-4B-Instruct-2507

qwen3-4b-instruct-2507

支持

支持

支持

支持

支持

Qwen3-1.7B

qwen3-1.7b

支持

支持

支持

支持

支持

Qwen3-0.6B

qwen3-0.6b

支持

支持

支持

支持

支持

Qwen2.5-72B-Instruct

qwen2.5-72b-instruct

支持

支持

支持

支持

支持

Qwen2.5-32B-Instruct

qwen2.5-32b-instruct

支持

支持

支持

支持

支持

Qwen2.5-14B-Instruct

qwen2.5-14b-instruct

支持

支持

支持

支持

支持

Qwen2.5-7B-Instruct

qwen2.5-7b-instruct

支持

支持

支持

支持

支持

千问-Plus-Character-2025-11-06

qwen-plus-character-2025-11-06

×

支持

支持

支持

支持

> `-Base`表示该模型只完成了预训练，虽然模型内已经存储了海量的知识，但无法正常进行对话。

#### 视觉理解（千问VL）

**模型服务**

**模型代码**

**CPT全参训练（cpt）**

**SFT全参训练（sft）**

**SFT高效训练（efficient\_sft）**

**DPO全参训练（dpo\_full）**

**DPO高效训练（dpo\_lora）**

Qwen3-VL-8B-Instruct

qwen3-vl-8b-instruct

×

支持

支持

×

×

Qwen3-VL-8B-Thinking

qwen3-vl-8b-thinking

×

支持

支持

×

×

Qwen3-VL-4B-Instruct

qwen3-vl-4b-instruct

×

支持

支持

×

×

Qwen2.5-VL-72B-Instruct

qwen2.5-vl-72b-instruct

×

支持

支持

×

×

Qwen2.5-VL-32B-Instruct

qwen2.5-vl-32b-instruct

×

支持

支持

×

×

Qwen2.5-VL-7B-Instruct

qwen2.5-vl-7b-instruct

×

支持

支持

×

×

> `-Base`表示该模型只完成了预训练，虽然模型内已经存储了海量的知识，但无法正常进行对话。

###### 调优方法对比

**特性**

**CPT（持续预训练）**

**SFT （监督微调）**

**DPO （直接偏好优化）**

一句话总结

补知识**（**注入领域知识**）**

学做事**（**学会遵循指令**）**

做得更好**（**对齐人类偏好**）**

输入数据

1000万+ Token

无标签的领域文本

1000+ 条

高质量的“问-答”对

100+ 组

同一指令下的“更好-更差”回答对

核心目标

领域适应，学习专业词汇和事实

教会模型对话格式和任务执行能力

使模型输出更符合人类价值观和偏好

学习方式

自监督学习（预测下一个词**）**

监督学习**（**模仿标准答案**）**

直接偏好学习**（**增大好答案概率，降低坏答案概率**）**

模型阶段

通常在 SFT 之前

CPT 之后，DPO 之前

通常在 SFT 之后，作为对齐的最后一步

###### 训练模式对比

**全参训练**

**高效训练 （LoRA，推荐）**

**适用场景**

• 需要模型学习新能力

• 追求全局效果最优

• 优化模型特定场景下的效果

• 对训练时间和成本敏感的场景

**训练时间**

较长，收敛速度较慢。

较短，收敛速度快。

hyper\_parameters 内 支持的设置

> 不同模型支持的参数及其默认值不同，**请前往**[**控制台**](https://bailian.console.aliyun.com/?tab=model#/efm/model_manager)**选择相同的模型和训练方式查看实际默认值**。

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

只有 freeze\_vit 设置为“true”时，模型才能进行按 [Token 用量](raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)计费。

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

各策略详情请参考[在控制台进行模型调优](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-on-console.md)。

`max_length`

（序列长度）**【必填】**

8192

Integer

指的是单条训练数据 token 支持的最大长度。如果单条数据 token 长度超过设定值，调优会直接丢弃该条数据，不进行训练。

字符与 token 之间的关系请参考Token和字符串之间怎么换算

`max_split_val_dataset_sample`

（验证集数据最大数量）

使用百炼推荐的默认值

Integer

当不设置`"validation_datasets"`时，阿里云百炼自动分割的验证集最多只有1000条。

当设置了`"validation_datasets"`时，该参数无效。

`split`

（训练集在训练文件中占比）

使用百炼推荐的默认值

Float

当不设置`"validation_datasets"`时，阿里云百炼会自动把训练文件中的80%作为训练集，20%作为验证集。

当设置了`"validation_datasets"`时，该参数无效。

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

-   格式要求：与`augmentation_types`完全对应
    
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

### 查询调优任务详情

使用创建任务时返回的`job_id`来查询任务状态。

#### HTTP

```
curl 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/<job_id>' \
--header 'Authorization: Bearer '${DASHSCOPE_API_KEY} \
--header 'Content-Type: application/json'
```

### 输入参数

**字段**

**类型**

**传参方式**

**必选**

**描述**

job\_id

String

Path Parameter

是

要查询的调优任务的ID。

### 返回成功样例

```
{
    "request_id": "d100cddb-ac85-4c82-bd5c-9b5421c5e94d",
    "output":
    {
        "job_id": "ft-202511272033-8ae7",
        "job_name": "ft-202511272033-8ae7",
        "status": "RUNNING",
        "finetuned_output": "qwen3-8b-ft-202511272033-8ae7",
        "model": "qwen3-8b",
        "base_model": "qwen3-8b",
        "training_file_ids": [],
        "validation_file_ids": [],
        "training_datasets": [
            {"data_source_type": "file_id", "file_id": "9e9ffdfa-c3bf-436e-9613-6f053c66aa6e"}
        ],
        "validation_datasets": [],
        "hyper_parameters":
        {
            "n_epochs": 3,
            "batch_size": 16,
            "max_length": 8192,
            "learning_rate": "1.6e-5",
            "lr_scheduler_type": "linear",
            "split": 0.9,
            "warmup_ratio": 0.05,
            "eval_steps": 50,
            "data_augmentation": true,
            "augmentation_ratio": "0.1,0.05,0.15",
            "augmentation_types": "dialogue_CN,general_purpose_CN,NLP",
            "save_strategy": "epoch",
            "save_total_limit": 10
        },
        "training_type": "sft",
        "create_time": "2025-11-27 20:33:15",
        "workspace_id": "llm-8v53etv3hwb8orx1",
        "user_identity": "1654290265984853",
        "modifier": "1654290265984853",
        "creator": "1654290265984853",
        "group": "llm",
        "max_output_cnt": 10
    }
}
```

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

**说明**训练成功后，`finetuned_output`指的是调优成功后的模型 ID，可用于模型部署。

### 获取调优任务日志

#### HTTP

```
curl 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/<job_id>/logs?offset=0&line=1000' \
--header 'Authorization: Bearer '${DASHSCOPE_API_KEY} \
--header 'Content-Type: application/json'
```

> 可通过 offset 和 line 两个参数获取特定行数区间的日志。 Offset 用于设置日志输出开始的位置；line 用于设置日志最多输出多少行。

返回结果样例：

```
{
    "request_id":"1100d073-4673-47df-aed8-c35b3108e968",
    "output":{
        "total":57,
        "logs":[
            "{输出调优日志1}",
            "{输出调优日志2}",
            ...
            ...
            ...
        ]
    }
}
```

### 查询与发布模型参数快照

> 仅 SFT微调训练（`efficient_sft`、`sft`）支持保存和发布其中间状态的模型参数快照（Checkpoint）。

#### 查询调优任务的参数快照列表

```
curl 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/<job_id>/checkpoints' \
--header 'Authorization: Bearer '${DASHSCOPE_API_KEY} \
--header 'Content-Type: application/json'
```
**输入参数**

**字段**

**类型**

**传参方式**

**必选**

**描述**

job\_id

String

Path Parameter

是

要查询的调优任务的ID。

**返回成功样例**

**说明**`checkpoint`指的是 Checkpoint ID，用于在[模型发布（可选）](https://help.aliyun.com/zh/model-studio/fine-tuning-api-guide#7188bc825bl6b) API 中指定要发布的快照；`model_name`指的是模型 ID，可用于模型部署。（`finetuned_output` 输出的是最后一个 checkpoint 的 `model_name`）

```
{
    "request_id": "c11939b5-efa6-4639-97ae-ed4597984647",
    "output":
    [
        {
            "create_time": "2025-11-11T16:25:42",
            "full_name": "ft-202511272033-8ae7-checkpoint-20",
            "job_id": "ft-202511272033-8ae7",
            "checkpoint": "checkpoint-20",
            "model_name": "qwen3-8b-instruct-ft-202511272033-8ae7",
            "status": "SUCCEEDED"
        }
    ]
}
```

**快照发布状态 （status）**

**含义**

PENDING

快照（Checkpoint）待发布，需要使用[模型发布](https://help.aliyun.com/zh/model-studio/fine-tuning-api-guide#7188bc825bl6b)API 发布后才可以进行[模型部署&调用](https://help.aliyun.com/zh/model-studio/fine-tuning-api-guide#a61a0681fawzl)。

PROCESSING

快照（Checkpoint）发布中。

SUCCEEDED

快照（Checkpoint）发布成功。可直接进行[模型部署&调用](https://help.aliyun.com/zh/model-studio/fine-tuning-api-guide#a61a0681fawzl)。

FAILED

快照（Checkpoint）发布失败。

#### 模型发布（可选）

**说明**在百炼平台上，模型调优完成后可以导出参数快照，导出后才能基于此版本的参数快照在百炼上进行模型部署。

导出的参数快照保存在云存储中，暂不支持访问或下载。

**说明**URL 中的 `<checkpoint_id>` 取值来自上一步查询快照列表接口返回的 `checkpoint` 字段（如 `checkpoint-20`），而非 `full_name` 或其他含 job\_id 前缀的字段值。

```
curl --request GET 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/<job_id>/export/<checkpoint_id>?model_name=<model_name>' \
--header 'Authorization: Bearer '${DASHSCOPE_API_KEY} \
--header 'Content-Type: application/json'
```
**输入参数**

**字段**

**类型**

**传参方式**

**必选**

**描述**

job\_id

String

Path Parameter

是

要查询的调优任务的 ID。

checkpoint\_id

String

Path Parameter

是

要发布的 Checkpoint ID。取值为查询快照列表接口返回的 `checkpoint` 字段值（如 `checkpoint-20`），不含 job\_id 前缀。

model\_name

String

Path Parameter

是

发布后期望的模型 ID。

**发布任务成功返回样例**
```
{
    "request_id": "ed3faa41-6be3-4271-9b83-941b23680537",
    "output": true
}
```

由于发布任务是异步执行的，请使用[查询快照列表](https://help.aliyun.com/zh/model-studio/fine-tuning-api-guide#4aaa5bd325vy7) API 观察快照发布状态。

### 模型调优的更多操作

#### 列举调优任务列表

```
curl 'https://dashscope.aliyuncs.com/api/v1/fine-tunes' \
--header 'Authorization: Bearer '${DASHSCOPE_API_KEY} \
--header 'Content-Type: application/json'
```

#### 中止调优任务

> 智能终止正在训练中的调优任务

```
curl --request POST 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/<job_id>/cancel' \
--header 'Authorization: Bearer '${DASHSCOPE_API_KEY} \
--header 'Content-Type: application/json'
```

#### 删除调优任务

> 无法删除正在训练中的调优任务

```
curl --request DELETE 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/<job_id>' \
--header 'Authorization: Bearer '${DASHSCOPE_API_KEY} \
--header 'Content-Type: application/json'
```

## API参考

DashScope命令行调用参考已包含在本篇内容中，详细API调用请参考API详情。

## 模型部署&调用

### 模型部署

更多模型部署方式的相关信息请参考：[使用 API 进行模型部署](raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。

按模型 Token 使用量

```
curl "https://dashscope.aliyuncs.com/api/v1/deployments" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model_name": "qwen3-8b-ft-202511132025-0260",
    "plan": "lora",
    "capacity": 1,
    "name": "qwen3-8b-ft"
}'
```

按模型单元的使用时长

```
curl "https://dashscope.aliyuncs.com/api/v1/deployments" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "name": "my_qwen_plus",
    "model_name": "qwen-plus-2025-12-01",
    "plan": "mu",
    "deploy_spec": "MU1",
    "enable_thinking": true,
    "capacity": 4,
    "max_context_length": 10000,
    "rpm_limit": 500,
    "tpm_limit": 1000
}'
```

### 查询模型部署的状态

当部署状态为`RUNNING`时，表示该模型当前可供调用。

```
curl 'https://dashscope.aliyuncs.com/api/v1/deployments/<替换为部署任务成功后的模型实例 ID>' \
--header 'Authorization: Bearer '${DASHSCOPE_API_KEY}  \
--header 'Content-Type: application/json'
```

更多模型部署相关的操作，如扩缩容、下线等请参见：模型部署-API详情。

### 模型调用

当模型部署状态为`RUNNING`时，可以像调用其他模型一样使用调优后的模型。

也可以前往[模型部署控制台](https://bailian.console.aliyun.com/cn-beijing?tab=model#/efm/model_deploy)界面获取**模型code**。

更多使用方法和参数设置请前往[DashScope API 参考](raw/model-api-reference/qwen-api-reference.md)。

```
curl 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation' \
--header 'Authorization: Bearer '${DASHSCOPE_API_KEY}  \
--header 'Content-Type: application/json' \
--data '{
    "model": "<替换为部署任务成功后的模型实例 ID>",
    "input":{
        "messages":[
            {
                "role": "user",
                "content": "你是谁？"
            }
        ]
    },
    "parameters": {
        "result_format": "message"
    }
}'
```

## 模型评测

阿里云百炼的模型评测功能必须使用控制台，请前往阿里云百炼的[模型评测](https://bailian.console.aliyun.com/?tab=model#/efm/model_evaluate) 页面，评估模型训练效果。

相关信息请参见模型评测。
