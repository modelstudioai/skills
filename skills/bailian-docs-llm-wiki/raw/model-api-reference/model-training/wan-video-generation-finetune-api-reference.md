# 视频生成模型微调API参考

本文档提供万相 **图生视频模型** 微调的完整 API 参考。

## **适用范围**

-   **适用地域**：本文档仅适用于[中国内地部署模式](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)下的北京地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)。
    
-   **开通账号权限**：若使用[阿里云子账号](https://help.aliyun.com/zh/model-studio/permission-management-overview#24ca2dad7djzs)（[RAM用户](https://help.aliyun.com/zh/ram/user-guide/overview-of-ram-users)），需要为子账号授予模型调用、训练和部署[权限](https://help.aliyun.com/zh/model-studio/use-workspace#895b613347th4)。
    
-   **配置环境变量**：已成功[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)，并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
    
-   **准备工作**：
    
    -   已阅读[模型微调指南](https://help.aliyun.com/zh/model-studio/wan-video-generation-finetune-guide)，了解**支持微调的模型、微调步骤、数据格式以及计费说明**。
        
    -   下载数据集样例：
        
        -   图生视频-基于首帧**：**[训练集](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251107/ujfrui/wan-i2v-training-dataset.zip)、[验证集](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251113/iumzue/wan-i2v-valid-dataset.zip)。
            
        -   图生视频-基于首尾帧：[训练集](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260119/wapfil/wan-kf2v-training-dataset.zip)、[验证集](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260119/gjlxnm/wan-kf2v-valid-dataset.zip)。
            

## **上传数据集**

**API描述**：将本地的数据集（.zip 格式）上传到阿里云百炼平台，获取唯一的文件ID（`**file_id**`）。

**说明**

-   通过 API 上传时，zip 压缩包大小 **≤ 1GB**。
    
-   批量上传请参见[上传文件API](https://help.aliyun.com/zh/model-studio/model-customization-file-management-service#d031ae7005zbz)。
    

#### **请求接口**

```
POST https://dashscope.aliyuncs.com/api/v1/files
Content-type: multipart/form-data
```

### **入参描述**

**字段**

**传参方式**

**类型**

**必选**

**描述**

**示例值**

files

Body (form-data)

file

是

本地数据集文件（.zip格式）。

传参时需使用格式 `files=@"<文件路径>"`，路径可以是相对路径或绝对路径。

@"./wan-i2v-training-dataset.zip"

purpose

Body (form-data)

string

是

微调任务固定为 fine-tune。

fine-tune

descriptions

Body (form-data)

string

否

数据集的描述信息。

a fine-tune training data file for wan

### **出参描述**

**字段**

**类型**

**描述**

**示例值**

request\_id

string

请求的唯一标识符。

1f3f1c5b-7418-4976-aaea-xxxxxx

data

object

返回的数据对象。

\-

data.uploaded\_files

array

上传成功的文件列表。

\-

data.uploaded\_files\[\].file\_id

string

文件在平台内的唯一标识符，用于创建微调任务。

3bff1ef7-f72d-4285-bb75-xxxxxx

data.uploaded\_files\[\].name

string

文件名。

wan-i2v-training-dataset.zip

data.failed\_uploads

array

上传失败的文件列表。

\[\]

### **请求示例**

```
curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/files' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--form 'files=@"./wan-i2v-training-dataset.zip"' \
--form 'purpose="fine-tune"' \
--form 'descriptions="a fine-tune training data file for wan"'
```

### **响应示例**

请复制并保存 `**file_id**`，这是上传数据集的唯一标识。

```
{
    "data": {
        "uploaded_files": [
            {
                "name": "wan-i2v-training-dataset.zip",
                "file_id": "3bff1ef7-f72d-4285-bb75-xxxxxx"
            }
        ],
        "failed_uploads": []
    },
    "request_id": "1f3f1c5b-7418-4976-aaea-xxxxxx"
}
```

## **创建微调任务**

**API描述**：基于指定的基准模型和上传的数据集，启动模型微调训练任务。

#### **请求接口**

```
POST https://dashscope.aliyuncs.com/api/v1/fine-tunes
Content-type: application/json
```

### **入参描述**

**字段**

**传参方式**

**类型**

**必选**

**描述**

**示例值**

model

Body

string

是

指定微调所用的基准模型。

-   图生视频-基于首帧：wan2.5-i2v-preview、wan2.2-i2v-flash
    
-   图生视频-基于首尾帧：wan2.2-kf2v-flash
    

wan2.5-i2v-preview

training\_file\_ids

Body

array\[string\]

是

训练集文件ID数组，可传入多个ID。

\["3bff1ef7-f72d-4285-bb75-xxxxxx"\]

validation\_file\_ids

Body

array\[string\]

否

验证集文件ID数组，可传入多个ID。

若不提供，系统会从训练集中自动划分。

\-

training\_type

Body

string

是

微调类型，当前仅支持`efficient_sft`（LoRA高效微调）。

efficient\_sft

hyper\_parameters

Body

object

否

超参数配置。

见下表

#### **超参数（hyper\_parameters）**

初次训练时，推荐使用默认的超参数。若模型效果不佳或训练不收敛，可以尝试调整 n\_epochs或learning\_rate等参数。

**字段**

**类型**

**必选**

**描述**

**默认值**

batch\_size

int

是

**批次大小**。

一次性送入模型进行训练的数据条数。

-   wan2.5-i2v-preview：推荐使用默认值，固定为2。
    
-   wan2.2-i2v-flash：推荐使用默认值，固定为4。
    
-   wan2.2-kf2v-flash：推荐使用默认值，固定为4。
    

wan2.5: 2

wan2.2: 4

n\_epochs

int

是

**训练循环次数。**

训练总步数（steps）由训练轮数（n\_epochs）、数据集大小和批大小（batch\_size）共同决定，计算公式为：steps = n\_epochs × 向上取整（数据集大小 / batch\_size）。

为确保模型充分训练，建议总训练步数不少于 **800** 步。推荐的最小训练轮数可按此公式估算：`n_epochs = 800 / 向上取整（数据集大小 / batch_size）`。

> 例如：数据集有5条数据，batch\_size为2，则每轮训练步数=向上取整（5/2）= 3，所需最小训练轮数n\_epochs = 800 / 3 ≈ 267。此值为推荐最小值，可适当调高。

400

learning\_rate

float

是

**学习率。**控制模型权重更新的幅度。

过高可能导致模型变差，过低则变化不明显。推荐使用默认值。

2e-5

eval\_epochs

int

是

**验证间隔**。取值需≥`n_epochs/10`。

训练期间每隔多少个epoch进行一次验证评估，用于阶段性评估模型训练效果。

50

max\_pixels

int

是

**训练视频的最大分辨率**。

设置训练集中输入视频分辨率的像素总数（宽×高）限制。系统仅对**超过该值**的视频进行缩放处理，未超限的视频将保持原样。

-   wan2.5-i2v-preview：默认 36864。取值范围：16384 (128×128) ～ 36864 (192×192)。
    
-   wan2.2-i2v-flash：默认 262144。取值范围：65536 (256×256) ～ 262144 (512×512)。
    
-   wan2.2-kf2v-flash：默认 262144。取值范围：65536 (256×256) ～ 262144 (512×512)。
    

wan2.5：36864

wan2.2：262144

split

float

否

**训练集划分比例**。取值范围为 (0, 1)。

仅在未指定`validation_file_ids`时生效。

此参数用于从训练集中自动按比例拆分出验证集。例如，0.9表示90%训练集，10%验证集。最终验证集的数量还会受到`max_split_val_dataset_sample`的限制。

0.9

max\_split\_val\_dataset\_sample

int

否

**从训练集中自动划分验证集的最大样本数**。取值需≥1。

仅在未指定`validation_file_ids`时生效。

该参数为验证集数量设置了一个上限，具体为：

`验证集数量 = min(数据集总数 × (1 − split), max_split_val_dataset_sample)`

> 例如：数据集共100条，split为0.9 （即取10%作验证集），max\_split\_val\_dataset\_sample为5。计算出的验证集为10条（100×0.1），但由于上限为5，最终只会使用5条数据作为验证集。

5

save\_total\_limit

int

否

**Checkpoint 保存数量上限。**

限制最多保存的模型数量。系统将始终只保存训练生成的最后 N 个 Checkpoint（N 为该参数值）。

20

lora\_rank

int

否

**LoRA 低秩矩阵的维数**。推荐使用默认值。

该值决定了微调参数量的大小。数值越大，模型拟合能力越强，但训练速度会变慢。

取值必须为2n（如 16、32、64）。

32

lora\_alpha

int

否

**LoRA 权重的缩放系数**。推荐使用默认值。

用于调节微调后的参数对原模型权重的影响程度（通常与 lora\_rank 配合使用）。

取值必须为2n（如 16、32、64）。

32

### **出参描述**

**字段**

**类型**

**描述**

**示例值**

request\_id

string

请求的唯一标识符。

0eb05b0c-02ba-414a-9d0c-xxxxxxxxx

output

object

任务详情。

\-

output.job\_id

string

模型微调任务唯一标识，用于后续查询任务状态。

ft-202511111122-xxxx

output.job\_name

string

模型微调任务名称。

ft-202511111122-xxxx

output.status

string

微调训练任务的状态：

-   PENDING：训练待开始。
    
-   QUEUING：训练正在排队（同时只有一个训练任务可以进行）。
    
-   RUNNING：训练正在进行中。
    
-   CANCELING：训练正在取消中。
    
-   SUCCEEDED：训练成功。
    
-   FAILED：训练失败。
    
-   CANCELED：训练已经取消。
    

PENDING

output.finetuned\_output

string

微调后产出的新模型名称。部署和调用时需要用到。

wan2.5-i2v-preview-ft-202511111122-xxxx

output.model

string

使用的基准模型。

wan2.5-i2v-preview

output.base\_model

string

使用的基准模型。

wan2.5-i2v-preview

output.training\_file\_ids

array

使用的训练集文件ID列表。

\["3bff1ef7-f72d-4285-bb75-xxxxxx"\]

output.validation\_file\_ids

array

使用的验证集文件ID列表。若未上传验证集，为空列表。

\[\]

output.hyper\_parameters

object

实际使用的超参数。

{...}

output.training\_type

string

模型微调的训练方式。固定为efficient\_sft。

efficient\_sft

output.create\_time

string

任务创建时间。

2025-11-11 11:22:22

output.workspace\_id

string

阿里云百炼API Key所属的业务空间ID。

请参见[获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)。

llm-xxxxxxxxx

output.user\_identity

string

用户标识，阿里云账号ID。

12xxxxxxx

output.modifier

string

修改人的阿里云账号ID。

12xxxxxxx

output.creator

string

创建人的阿里云账号ID。

12xxxxxxx

output.group

string

模型微调任务分组。

llm

output.max\_output\_cnt

integer

训练期间最多保存的 checkpoint 数量。

等同于[超参数](#5f391e4b3cezf)save\_total\_limit参数的值。

8

### **请求示例**

请将`<替换为训练数据集的文件id>`完整替换为[上传数据集](#977caa6c1for9)获取的文件ID。

## 图生视频-基于首帧

## Wan2.5模型

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model":"wan2.5-i2v-preview",
    "training_file_ids":[
        "<替换为训练数据集的文件id>"
    ],
    "training_type":"efficient_sft",
    "hyper_parameters":{
        "n_epochs":400,
        "batch_size":2,
        "learning_rate":2e-5,
        "split":0.9,
        "eval_epochs": 50,
        "max_pixels": 36864
    }
}'
```

## Wan2.2模型

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model":"wan2.2-i2v-flash",
    "training_file_ids":[
        "<替换为训练数据集的文件id>"
    ],
    "training_type":"efficient_sft",
    "hyper_parameters":{
        "n_epochs":400,
        "batch_size":4,
        "learning_rate":2e-5,
        "split":0.9,
        "eval_epochs": 50,
        "max_pixels": 262144
    }
}'
```

## 图生视频-基于首尾帧

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model":"wan2.2-kf2v-flash",
    "training_file_ids":[
        "<替换为训练数据集的文件id>"
    ],
    "training_type":"efficient_sft",
    "hyper_parameters":{
        "n_epochs":400,
        "batch_size":4,
        "learning_rate":2e-5,
        "split":0.9,
        "eval_epochs": 50,
        "max_pixels": 262144
    }
}'
```

## 上传多个训练集和验证集

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model":"wan2.5-i2v-preview",
    "training_file_ids":[
        "<替换为训练集的文件id_1>",
        "<替换为训练集的文件id_2>"
    ],
    "validation_file_ids":[
         "<替换为验证集的文件id_1>",
         "<替换为验证集的文件id_2>"
    ],
    "training_type":"efficient_sft",
    "hyper_parameters":{
        "n_epochs":400,
        "batch_size":2,
        "learning_rate":2e-5,
        "split":0.9,
        "eval_epochs": 50,
        "max_pixels": 36864
    }
}'
```

### **响应示例**

重点关注这两个参数：`**output.job_id**`（任务ID）**、**`**output.finetuned_output**`（微调后产出的新模型名称）。

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
        "training_file_ids": [
            "xxxxxxxxxxxx"
        ],
        "validation_file_ids": [],
        "hyper_parameters": {
            "n_epochs": 400,
            "batch_size": 2,
            "learning_rate": 2.0E-5,
            "split": 0.9,
            "eval_epochs": 50
        },
        "training_type": "efficient_sft",
        "create_time": "2025-11-11 11:22:22",
        "workspace_id": "llm-xxxxxxxxx",
        "user_identity": "12xxxxxxx",
        "modifier": "12xxxxxxx",
        "creator": "12xxxxxxx",
        "group": "llm",
        "max_output_cnt": 20
    }
}
```

## **查询微调任务状态**

**API描述**：通过 `job_id` 查询微调任务进度。轮询此接口，当任务状态`status` 变为 **SUCCEEDED**，表示模型训练成功完成。

**说明**

本文示例的微调任务训练需要**数小时**，具体耗时根据基础模型而定，请耐心等待。

#### **请求接口**

```
GET https://dashscope.aliyuncs.com/api/v1/fine-tunes/{job_id}
```

### **入参描述**

**字段**

**传参方式**

**类型**

**必选**

**描述**

**示例值**

job\_id

Path parameter

string

是

微调任务ID。

ft-202511111122-xxxx

### **出参描述**

**字段**

**类型**

**描述**

**示例值**

request\_id

string

请求的唯一标识符。

0eb05b0c-02ba-414a-9d0c-xxxxxxxxx

output

object

任务详情。

\-

output.job\_id

string

模型微调任务唯一标识，用于后续查询任务状态。

ft-202511111122-xxxx

output.job\_name

string

模型微调任务名称。

ft-202511111122-xxxx

output.status

string

微调训练任务的状态。

-   PENDING：训练待开始。
    
-   QUEUING：训练正在排队（同时只有一个训练任务可以进行）。
    
-   RUNNING：训练正在进行中。
    
-   CANCELING：训练正在取消中。
    
-   SUCCEEDED：训练成功。
    
-   FAILED：训练失败。
    
-   CANCELED：训练已经取消。
    

PENDING

output.finetuned\_output

string

微调后产出的新模型名称。

wan2.5-i2v-preview-ft-202511111122-xxxx

output.model

string

使用的基准模型。

wan2.5-i2v-preview

output.base\_model

string

使用的基准模型。

wan2.5-i2v-preview

output.training\_file\_ids

array

使用的训练集文件ID列表。

\["3bff1ef7-f72d-4285-bb75-xxxxxx"\]

output.validation\_file\_ids

array

使用的验证集文件ID列表。若未上传验证集，为空列表。

\[\]

output.hyper\_parameters

object

实际使用的超参数。

{...}

output.training\_type

string

模型微调的训练方式。固定为efficient\_sft。

efficient\_sft

output.create\_time

string

微调任务创建时间。

2025-11-11 11:22:22

output.end\_time

string

微调任务完成时间。

2025-11-11 16:49:01

output.workspace\_id

string

阿里云百炼API Key所属的业务空间ID。

请参见[获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)。

llm-xxxxxxxxx

output.user\_identity

string

用户标识，阿里云账号ID。

12xxxxxxx

output.modifier

string

修改人的阿里云账号ID。

12xxxxxxx

output.creator

string

创建人的阿里云账号ID。

12xxxxxxx

output.group

string

模型微调任务分组。

llm

output.max\_output\_cnt

integer

最多保存的 checkpoint 数量。

等同于[超参数](#5f391e4b3cezf)`save_total_limit`的值。

8

output.output\_cnt

integer

实际保存的 checkpoint 数量。

该值小于或等于`output.max_output_cnt`。

8

output.usage

integer

训练消耗的总Token数量，用于模型训练计费。

432000

### **请求示例**

请将 URL 中的 `<替换为微调任务job_id>` 完整替换为[创建微调任务](#03af17bea7l1w)输出参数`job_id`的值。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/<替换为微调任务job_id>' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json'
```

### **响应示例**

关注两个参数：`**output.status**`（状态为SUCCEEDED，表示训练完成）**、**`**output.usage**`（训练消耗的总Token数量）**。**

```
{
    "request_id": "9bbb953c-bef2-4b59-9fc5-xxxxxxxxx",
    "output": {
        "job_id": "ft-202511111122-xxxx",
        "job_name": "ft-202511111122-xxxx",
        "status": "SUCCEEDED",
        "finetuned_output": "wan2.5-i2v-preview-ft-202511111122-xxxx",
        "model": "wan2.5-i2v-preview",
        "base_model": "wan2.5-i2v-preview",
        "training_file_ids": [
            "xxxxxxxxxxxx"
        ],
        "validation_file_ids": [],
        "hyper_parameters": {
            "n_epochs": 400,
            "batch_size": 2,
            "learning_rate": 2.0E-5,
            "split": 0.9,
            "eval_epochs": 50
        },
        "training_type": "efficient_sft",
        "create_time": "2025-11-11 11:22:22",
        "workspace_id": "llm-xxxxxxxxx",
        "user_identity": "xxxxxxxxx",
        "modifier": "xxxxxxxxx",
        "creator": "xxxxxxxxx",
        "end_time": "2025-11-11 16:49:01",
        "group": "llm",
        "usage": 432000,
        "max_output_cnt": 8,
        "output_cnt": 8
    }
}
```

## **部署模型**

**API描述**：将训练好的模型发布为在线 API 服务。请先[查询微调任务状态](#a242dac535nqt)，确保模型训练任务的状态`status` 为 **SUCCEEDED**。

#### **请求接口**

```
POST https://dashscope.aliyuncs.com/api/v1/deployments
Content-Type: application/json
```

### **入参描述**

**字段**

**传参方式**

**类型**

**必选**

**描述**

**示例值**

model\_name

Body

string

是

待部署的模型名称。

-   部署微调接口产出的模型：填写[创建微调任务](#03af17bea7l1w)输出参数 `output.finetuned_output` 的值。
    
-   部署导出的模型：填写[查询导出的模型详情](#18e0fbf9cadde)输出参数`output[].model_name`的值。
    

wan2.5-i2v-preview-ft-202511111122-xxxx

capacity

Body

integer

是

部署的模型实例数量。推荐设置为1。

1

plan

Body

string

是

部署方式。LoRA高效微调固定为`lora`。

lora

aigc\_config

Body

object

是

提示词配置。

\-

aigc\_config.use\_input\_prompt

Body

boolean

是

用于控制 API 调用时的提示词生成逻辑。

-   `false`（默认值）：自动生成模式。系统忽略在 API 接口传入的 prompt，强制使用下方两个参数配置的模板，自动生成提示词。
    
-   `true`：手动传入模式。系统直接使用在 API 接口传入的 prompt。下方配置的模板参数将全部失效。
    

false

aigc\_config.prompt

Body

string

是

预设的Prompt模板。

仅在`use_input_prompt=false`时生效。

在模型调用时，系统会分析输入图像，将画面内容填入该模板，自动生成带特效指令的完整描述。

注意：此参数会自动**覆盖**模型调用接口中传入的 prompt 参数。

根据图像内容提供视频描述...

> 请参见[请求示例](#87d0238adaw58)

aigc\_config.lora\_prompt\_default

Body

string

是

备用Prompt模板。

仅在`use_input_prompt=false`时生效。

当使用`aigc_config.prompt`生成失败时，将使用此参数来生成视频。

然后开始展示s86b5p金钱雨特效...

> 请参见[请求示例](#87d0238adaw58)

**关于aigc\_config.prompt参数说明**

-   **为什么要设置这个参数**？
    
    如果不设置此参数，每次调用模型都需要手动编写完整 Prompt；设置后，调用微调模型时，只需上传图片，系统会根据此参数自动补全特效指令，无需手动输入 Prompt。
    
-   **如何设置？**
    
    **Prompt = 任务指令（告诉模型要做什么）+ 输出模板（规范输出格式）+ 示例（让模型学习示例结构）。**
    
    ```
    根据图像内容提供视频描述，描述必须包含“然后开始展示s86b5p金钱雨特效，无数巨大尺寸的美元钞票（米黄底/深绿图案）如暴雨般倾泻而下，密集地砸向并环绕她（他）。钞票持续落下，同时镜头缓缓拉进，她（他）双臂舒展上扬，脖颈微仰，表情惊喜，完全沉浸在这场狂野的金钱雨中”。
    输出模版:
    视频开头展示了[主体描述]。[环境描述]。然后开始展示s86b5p金钱雨特效，无数巨大尺寸的美元钞票（米黄底/深绿图案）如暴雨般倾泻而下，密集地砸向并环绕她（他）。钞票持续落下，同时镜头缓缓拉进，她（他）双臂舒展上扬，脖颈微仰，表情惊喜，完全沉浸在这场狂野的金钱雨中。
    示例:
    视频开头展示了一位年轻女性在海滩上的场景。她的头发湿漉漉的，呈现出深棕色，卷曲且略显凌乱。她的脸上带着灿烂的笑容。背景是波涛汹涌的海浪和远处的山脉。然后开始展示s86b5p金钱雨特效，无数巨大尺寸的美元钞票（米黄底/深绿图案）如暴雨般倾泻而下，密集地砸向并环绕她。钞票持续落下，同时镜头缓缓拉进，她双臂舒展上扬，脖颈微仰，表情惊喜，完全沉浸在这场狂野的金钱雨中。
    ```
    
    > 关于“输出模板”描述，请参见[视频标注：为视频编写Prompt](https://help.aliyun.com/zh/model-studio/wan-video-generation-finetune-guide#102ebee9f3dtq)。
    

### **出参描述**

**字段**

**类型**

**描述**

**示例值**

request\_id

string

请求的唯一标识符。

0eb05b0c-02ba-414a-9d0c-xxxxxxxxx

output

object

任务详情。

\-

output.deployed\_model

string

部署模型的唯一标识。

用于查询模型部署状态和调用模型。

wan2.5-i2v-preview-ft-202511111122-xxxx

output.model\_name

string

模型标识名。

wan2.5-i2v-preview-ft-202511111122-xxxx

output.status

string

部署状态：

-   PENDING：部署中
    
-   RUNNING：运行中
    
-   FAILED：部署失败
    

PENDING

output.base\_model

string

使用的基准模型。

wan2.5-i2v-preview

output.gmt\_create

string

部署任务创建时间。

2025-11-11T17:46:53.294

output.gmt\_modified

string

部署任务更新时间。

2025-11-11T17:46:53.294

output.workspace\_id

string

阿里云百炼API Key所属的业务空间ID。

请参见[获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)。

llm-xxxxxxxxx

output.charge\_type

string

付费模式。post\_paid表示后付费。

post\_paid

output.creator

string

创建人的阿里云账号ID。

12xxxxxxx

output.modifier

string

修改人的阿里云账号ID。

12xxxxxxx

output.plan

string

部署方式。

lora

### **请求示例**

请将 `<替换为模型名称model_name>` 完整替换为[创建微调任务](#03af17bea7l1w)输出参数`finetuned_output`的值。

## 图生视频-基于首帧

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/deployments' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model_name": "<替换为模型名称model_name>",
    "aigc_config": {
        "use_input_prompt": false,
        "prompt": "根据图像内容提供视频描述，描述必须包含“然后开始展示s86b5p金钱雨特效，无数巨大尺寸的美元钞票（米黄底/深绿图案）如暴雨般倾泻而下，密集地砸向并环绕她（他）。钞票持续落下，同时镜头缓缓拉进，她（他）双臂舒展上扬，脖颈微仰，表情惊喜，完全沉浸在这场狂野的金钱雨中”。\n输出模板:\n视频开头展示了[主体描述模板[环境描述]。然后开始展示s86b5p金钱雨特效，无数巨大尺寸的美元钞票（米黄底/深绿图案）如暴雨般倾泻而下，密集地砸向并环绕她（他）。钞票持续落下，同时镜头缓缓拉进，她（他）双臂舒展上扬，脖颈微仰，表情惊喜，完全沉浸在这场狂野的金钱雨中。\n示例:\n视频开头展示了一位年轻女性在海滩上的场景。她的头发湿漉漉的，呈现出深棕色，卷曲且略显凌乱。她的脸上带着灿烂的笑容。背景是波涛汹涌的海浪和远处的山脉。然后开始展示s86b5p金钱雨特效，无数巨大尺寸的美元钞票（米黄底/深绿图案）如暴雨般倾泻而下，密集地砸向并环绕她。钞票持续落下，同时镜头缓缓拉进，她双臂舒展上扬，脖颈微仰，表情惊喜，完全沉浸在这场狂野的金钱雨中。",
        "lora_prompt_default": "然后开始展示s86b5p金钱雨特效，无数巨大尺寸的美元钞票（米黄底/深绿图案）如暴雨般倾泻而下，密集地砸向并环绕主角。钞票持续落下，同时镜头缓缓拉进，主角双臂舒展上扬，脖颈微仰，表情惊喜，完全沉浸在这场狂野的金钱雨中。"
    },
    "capacity": 1,
    "plan": "lora"
}'
```

## 图生视频-基于首尾帧

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/deployments' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model_name": "<替换为模型名称model_name>",
    "aigc_config": {
        "use_input_prompt": false,
        "prompt": "根据图像内容提供视频描述，描述必须包含“然后她开始了s86b5p变身。”\n输出模板:\n视模板头展示了[主体描述]。[环境描述]。然后她开始了s86b5p变身。\n示例:\n视频开头展示了一位年轻女性在户外的场景。她有着短而卷曲的深棕色头发，面带微笑，显得非常亲切。她穿着一件黑色的Polo衫，上面有彩色的花卉刺绣图案，背景是绿色的植被和远处的山脉。然后她开始了s86b5p变身。",
        "lora_prompt_default": "然后她开始了s86b5p变身。"
    },
    "capacity": 1,
    "plan": "lora"
}'
```

### **响应示例**

关注两个参数：`output.deployed_model`（部署模型的唯一标识）、`output.status`（状态为PENDING，表示部署中）。

```
{
    "request_id": "96020b2e-9072-4c8a-9981-xxxxxxxxx",
    "output": {
        "deployed_model": "wan2.5-i2v-preview-ft-202511111122-xxxx",
        "gmt_create": "2025-11-11T17:46:53.294",
        "gmt_modified": "2025-11-11T17:46:53.294",
        "status": "PENDING",
        "model_name": "wan2.5-i2v-preview-ft-202511111122-xxxx",
        "base_model": "wan2.5-i2v-preview",
        "workspace_id": "llm-xxxxxxxxx",
        "charge_type": "post_paid",
        "creator": "12xxxxxxx",
        "modifier": "12xxxxxxx",
        "plan": "lora"
    }
}
```

## 查询模型部署状态

**API描述**：轮询此接口，当任务状态`status` 变为 **RUNNING**，表示模型已部署成功。

**说明**

本文示例的微调模型，部署过程预计需要 **5～10分钟**。

#### **请求接口**

```
GET https://dashscope.aliyuncs.com/api/v1/deployments/{deployed_model}
```

### **入参描述**

**字段**

**传参方式**

**类型**

**必选**

**描述**

**示例值**

deployed\_model

Path parameter

string

是

部署模型的唯一标识。

填写[部署模型](#836890b48brgk)输出参数 `output.deployed_model` 的值。

wan2.5-i2v-preview-ft-202511111122-xxxx

### **出参描述**

**字段**

**类型**

**描述**

**示例值**

request\_id

string

请求的唯一标识符。

0eb05b0c-02ba-414a-9d0c-xxxxxxxxx

output

object

任务详情。

\-

output.deployed\_model

string

部署模型的唯一标识。用于后续调用模型。

wan2.5-i2v-preview-ft-202511111122-xxxx

output.model\_name

string

模型标识名。

wan2.5-i2v-preview-ft-202511111122-xxxx

output.status

string

部署状态：

-   PENDING：部署中
    
-   RUNNING：运行中
    
-   ARREARS\_DOWN：欠费停服
    
-   ARREARS\_RECOVERING：欠费停服恢复中
    
-   FAILED：部署失败
    
-   OFFLINING：服务下线中
    
-   UPDATING：变配中
    
-   UPDATING\_FAILED：变配失败
    

RUNNING

output.base\_model

string

使用的基准模型。

wan2.5-i2v-preview

output.gmt\_create

string

部署任务创建时间。

2025-11-11T17:46:53.294

output.gmt\_modified

string

部署任务更新时间。

2025-11-11T18:02:2

output.workspace\_id

string

阿里云百炼API Key所属的业务空间ID。

请参见[获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#d3eb3cd37b7fu)。

llm-xxxxxxxxx

output.charge\_type

string

付费模式。post\_paid表示后付费。

post\_paid

output.creator

string

创建人的阿里云账号ID。

12xxxxxxx

output.modifier

string

修改人的阿里云账号ID。

12xxxxxxx

output.plan

string

部署方式。

lora

### **请求示例**

请将 `<替换为deployed_model>` 完整替换为[部署模型](#836890b48brgk)输出参数 `output.deployed_model` 的值。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/deployments/<替换为deployed_model>' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json'
```

### **响应示例**

关注`status`字段。当状态变为 **RUNNING** 时，表示模型已部署成功，可以开始调用。

```
{
    "request_id": "66d15f35-0772-409f-bc70-xxxxxxxxx",
    "output": {
        "deployed_model": "wan2.5-i2v-preview-ft-202511111122-xxxx",
        "gmt_create": "2025-11-11T17:46:53",
        "gmt_modified": "2025-11-11T18:02:24",
        "status": "RUNNING",
        "model_name": "wan2.5-i2v-preview-ft-202511111122-xxxx",
        "base_model": "wan2.5-i2v-preview",
        "workspace_id": "llm-xxxxxxxxx",
        "charge_type": "post_paid",
        "creator": "12xxxxxxx",
        "modifier": "12xxxxxxxx",
        "plan": "lora"
    }
}
```

## **调用模型生成视频**

调用微调后的LoRA模型，请参见[调用模型生成视频](https://help.aliyun.com/zh/model-studio/wan-video-generation-finetune-guide#543cc07530gl2)。

## **Checkpoint 管理**

### **1\. 查询Checkpoint列表**

**API描述**：获取通过验证集成功生成预览视频的 Checkpoint列表，验证失败的不会列出。

**使用限制**：该接口需在模型微调训练完成后调用，否则将返回空列表。

#### **请求接口**

```
GET https://dashscope.aliyuncs.com/api/v1/fine-tunes/{job_id}/validation-results
```

#### **入参描述**

**字段**

**传参方式**

**类型**

**必选**

**描述**

**示例值**

job\_id

Path parameter

string

是

微调任务ID。

ft-202511111122-xxxx

#### **出参描述**

**字段**

**类型**

**描述**

**示例值**

request\_id

string

请求的唯一标识符。

0eb05b0c-02ba-414a-9d0c-xxxxxxxxx

output

array\[string\]

Checkpoint列表。

\-

output\[\].checkpoint

string

Checkpoint名称。

checkpoint-160

#### **请求示例**

请将 URL 中的 `<替换为微调任务job_id>` 完整替换为[创建微调任务](#03af17bea7l1w)输出参数`job_id`的值。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/<替换为微调任务job_id>/validation-results' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json'
```

#### **响应示例**

```
{
    "request_id": "da1310f5-5a21-4e29-99d4-xxxxxx",
    "output": [
        {
            "checkpoint": "checkpoint-160"
        },
        {
            "checkpoint": "checkpoint-20"
        },
        {
            "checkpoint": "checkpoint-40"
        },
        {
            "checkpoint": "checkpoint-60"
        }
    ]
}
```

### **2\. 查询Checkpoint验证结果**

**API描述**： 根据`checkpoint`（例如“checkpoint-160”），查看其生成的视频效果。

#### **请求接口**

```
GET https://dashscope.aliyuncs.com/api/v1/fine-tunes/{job_id}/validation-details/{checkpoint}?page_no=1&page_size=10
```

#### **入参描述**

**字段**

**传参方式**

**类型**

**必选**

**描述**

**示例值**

job\_id

Path parameter

string

是

微调任务ID。

ft-202511111122-xxxx

checkpoint

Path parameter

string

是

Checkpoint名称。

checkpoint-160

page\_no

Query parameter

integer

否

页码。默认为1。

1

page\_size

Query parameter

integer

否

每页数量。默认为10。

10

#### **出参描述**

**字段**

**类型**

**描述**

**示例值**

request\_id

string

请求的唯一标识符。

375b3ad0-d3fa-451f-b629-xxxxxxx

output

object

输出结果。

\-

output.page\_no

integer

页码。

1

output.page\_size

integer

每页数量。

10

output.total

integer

验证集列表总数量。

1

output.list

array\[object\]

验证集列表。

\-

output.list\[\].video\_path

string

通过Checkpoint生成的视频。

video\_path有效期为24小时，请及时下载视频。

https://finetune-swap-wulanchabu.oss-cn-wulanchabu.aliyuncs.com/xxx.mp4?Expires=xxxx

output.list\[\].prompt

string

验证数据的prompt。从数据集的标注文件data.jsonl获得。

视频开头展示了一位年轻男性坐在咖啡馆的场景...

output.list\[\].first\_frame\_path

string

验证的图像地址。系统会读取数据集中的图像，并生成一个公网URL地址。

https://finetune-swap-wulanchabu.oss-cn-wulanchabu.aliyuncs.com/xxx.jpeg

#### **请求示例**

-   `<替换为微调任务job_id>`： 完整替换为[创建微调任务](#03af17bea7l1w)输出参数`job_id`的值。
    
-   `<替换为选择的checkpoint>`：完整替换为选定的Checkpoint名称，例如“checkpoint-160”。
    

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/<替换为微调任务job_id>/validation-details/<替换为选择的checkpoint>?page_no=1&page_size=10' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

#### **响应示例**

> video\_path有效期为24小时，请及时下载视频。

```
{
    "request_id": "375b3ad0-d3fa-451f-b629-xxxxxxx",
    "output": {
        "page_no": 1,
        "page_size": 10,
        "total": 1,
        "list": [
            {
                "video_path": "https://finetune-swap-wulanchabu.oss-cn-wulanchabu.aliyuncs.com/xxx.mp4?Expires=xxxx",
                "prompt": "视频开头展示了一位年轻男性坐在咖啡馆的场景。他穿着一件米色的Polo衫，神情专注且略显沉思，手指轻轻托着下巴。他的面前摆放着一杯热气腾腾的咖啡，背景是木质条纹的墙壁和一个装饰牌。然后开始展示s86b5p金钱雨特效，无数巨大尺寸的美元钞票（米黄底/深绿图案）如暴雨般倾泻而下，密集地砸向并环绕他。钞票持续落下，他双臂舒展上扬，脖颈微仰，表情惊喜，完全沉浸在这场狂野的金钱雨中。",
                "first_frame_path": "https://finetune-swap-wulanchabu.oss-cn-wulanchabu.aliyuncs.com/xxx.jpeg"
            }
        ]
    }
}
```

### **3\. 导出Checkpoint**

**API描述**：将Checkpoint导出为可部署模型。

#### **请求接口**

```
GET https://dashscope.aliyuncs.com/api/v1/fine-tunes/{job_id}/export/{checkpoint}?model_name={model_name}
```

#### **入参描述**

**字段**

**传参方式**

**类型**

**必选**

**描述**

**示例值**

job\_id

Path parameter

string

是

微调任务ID。

ft-202511111122-xxxx

checkpoint

Path parameter

string

是

Checkpoint名称。

checkpoint-160

model\_name

Query parameter

string

是

用于在控制台中展示的导出模型名称。

该名称需全局唯一，建议使用中英文、数字、下划线（\_）和短横线（-）字符。

请注意：此参数仅用于控制台显示，实际导出的模型名称以[查询导出的模型详情](#18e0fbf9cadde)输出参数`output[].model_name`为准。

wan2.5-i2v-preview-ft-202511111122-xxxx

#### **出参描述**

**字段**

**类型**

**描述**

**示例值**

request\_id

string

请求的唯一标识符。

0eb05b0c-02ba-414a-9d0c-xxxxxxxxx

output

boolean

导出请求是否提交成功。

-   true：表示导出请求提交成功。
    
-   false：表示导出请求提交失败，建议重试。
    

true

#### **请求示例**

-   `<替换为微调任务job_id>`：完整替换为[创建微调任务](#03af17bea7l1w)输出参数`job_id`的值。
    
-   `<替换为待导出的checkpoint>`：完整替换为checkpoint的值，例如“checkpoint-160”。
    
-   `<替换为控制台展示的导出模型名称>`：完整替换为自定义的模型名称，仅用于控制台展示。
    

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/<替换为微调任务job_id>/export/<替换为待导出的checkpoint>?model_name=<替换为控制台展示的导出模型名称>' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

#### **响应示例**

```
{
    "request_id": "0817d1ed-b6b6-4383-9650-xxxxx",
    "output": true
}
```

### **4\. 查询导出模型详情**

**API描述**：查询所有Checkpoint的状态，确认导出已完成，并获取它专属的、用于部署的新模型名称（`**model_name**`）。

#### **请求接口**

```
GET https://dashscope.aliyuncs.com/api/v1/fine-tunes/{job_id}/checkpoints
```

#### **入参描述**

**字段**

**传参方式**

**类型**

**必选**

**描述**

**示例值**

job\_id

Path parameter

string

是

微调任务ID。

ft-202511111122-xxxx

#### **出参描述**

**字段**

**类型**

**描述**

**示例值**

request\_id

string

请求的唯一标识符。

0eb05b0c-02ba-414a-9d0c-xxxxxxxxx

output

array\[object\]

Checkpoint列表详情。

\-

output\[\].create\_time

string

创建时间。

2025-11-11T13:27:29

output\[\].job\_id

string

微调任务ID。

ft-202511111122-xxxx

output\[\].checkpoint

string

Checkpoint名称。

checkpoint-160

output\[\].full\_name

string

Checkpoint完整名称标识。

ft-202511111122-496e-checkpoint-160

output\[\].model\_name

string

导出后的模型名称。用于模型部署和调用。

当`status`为SUCCEEDED时返回。

wan2.5-i2v-preview-ft-202511111122-xxxx-c160

output\[\].model\_display\_name

string

模型展示名称。

wan2.5-i2v-preview-ft-202511111122-xxxx

output\[\].status

string

模型导出状态：

-   PENDING：排队中
    
-   PROCESSING：导出中
    
-   SUCCEEDED：导出成功
    
-   FAILED：导出失败
    
-   UNSUPPORTED：不支持导出
    

SUCCEEDED

#### **请求示例**

请将 `<替换为微调任务job_id>` 完整替换为[创建微调任务](#03af17bea7l1w)输出参数`job_id`的值。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/<替换为微调任务job_id>/checkpoints' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

#### **响应示例**

请在返回列表中定位目标 Checkpoint（如 checkpoint-160）。当其状态变为 **SUCCEEDED** 时，表示导出成功，请务必获取并保存 `**model_name**`，它是后续模型部署与调用的唯一标识。

```
{
    "request_id": "b0e33c6e-404b-4524-87ac-xxxxxx",
    "output": [
         ......,
        {
            "create_time": "2025-11-11T13:42:31",
            "full_name": "ft-202511111122-496e-checkpoint-180",
            "job_id": "ft-202511111122-496e",
            "checkpoint": "checkpoint-180",
            "status": "PENDING" // 未导出的checkpoint，没有model_name字段
        },
        {
            "create_time": "2025-11-11T13:27:29",
            "full_name": "ft-202511111122-496e-checkpoint-160",
            "job_id": "ft-202511111122-496e",
            "checkpoint": "checkpoint-160",                             
            "model_name": "wan2.5-i2v-preview-ft-202511111122-xxxx-c160", // 重要字段，用于模型部署和调用
            "model_display_name": "wan2.5-i2v-preview-ft-202511111122-xxxx", 
            "status": "SUCCEEDED" // 成功导出的checkpoint
        },
        ......
        
    ]
}
```

### **5\. 部署和调用模型**

在成功导出 Checkpoint 并获取 `**model_name**` 后，请按照以下步骤执行后续操作：

-   [部署模型](#836890b48brgk)：在输入参数 `model_name`，填入导出后获取到的具体值。
    
-   [查询模型部署状态](#04b2baf08b1e9)
    
-   [调用模型生成视频](#848bf20229erb)
    

## **微调任务管理**

> 输入参数和输出参数请参见[模型调优 API参考](https://help.aliyun.com/zh/model-studio/model-training-api-reference)。

### **查询微调任务日志**

**请求示例**

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/<替换为微调任务job_id>/logs' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

**响应示例**

```
{
    "request_id": "b7ecb456-6dd1-4f35-a581-xxxxxx",
    "output": {
        "total": 25,
        "logs": [
            "2025-11-11 11:23:37,315 - INFO - data process succeeded, start to fine-tune",
            " Actual number of consumed tokens is 215040 !",
            " Actual number of consumed tokens is 419840 !",
            " Actual number of consumed tokens is 624640 !",
            " Actual number of consumed tokens is 829440 !",
            " Actual number of consumed tokens is 1034240 !",
            " Actual number of consumed tokens is 1239040 !",
            " Actual number of consumed tokens is 1443840 !",
            " Actual number of consumed tokens is 1648640 !",
            " Actual number of consumed tokens is 1853440 !",
            " Actual number of consumed tokens is 2058240 !",
            " Actual number of consumed tokens is 2263040 !",
            " Actual number of consumed tokens is 2467840 !",
            " Actual number of consumed tokens is 2672640 !",
            " Actual number of consumed tokens is 2877440 !",
            " Actual number of consumed tokens is 3082240 !",
            " Actual number of consumed tokens is 3287040 !",
            " Actual number of consumed tokens is 3491840 !",
            " Actual number of consumed tokens is 3696640 !",
            " Actual number of consumed tokens is 3901440 !",
            "2025-11-11 16:31:40,760 - INFO - fine-tuned output got, start to transfer it for inference",
            "2025-11-11 16:32:29,162 - INFO - transfer for inference succeeded, start to deliver it for inference",
            "2025-11-11 16:40:28,784 - INFO - start to save checkpoint",
            "2025-11-11 16:49:01,738 - INFO - finetune-job succeeded",
            "2025-11-11 16:49:02,234 - INFO - ##FT_COMPLETE##"
        ]
    }
}
```

### **查询微调任务列表**

**请求示例**

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/fine-tunes' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

**响应示例**

```
{
    "request_id": "bf4d3475-f50c-42e2-a263-xxxxxxxxx",
    "output": {
        "page_no": 1,
        "page_size": 10,
        "total": 1,
        "jobs": [
            {
                "job_id": "ft-202511111122-xxxx",
                "job_name": "ft-202511111122-xxxx",
                "status": "SUCCEEDED",
                "finetuned_output": "wan2.5-i2v-preview-ft-202511111122-xxxx",
                "model": "wan2.5-i2v-preview",
                "base_model": "wan2.5-i2v-preview",
                "training_file_ids": [
                    "xxxxxxxxx"
                ],
                "validation_file_ids": [],
                "hyper_parameters": {
                    "n_epochs": 400,
                    "batch_size": 2,
                    "learning_rate": 2.0E-5,
                    "split": 0.9,
                    "eval_epochs": 50
                },
                "training_type": "efficient_sft",
                "create_time": "2025-11-11 11:22:22",
                "workspace_id": "llm-xxxxxxxxx",
                "user_identity": "xxxxxxxxx",
                "modifier": "xxxxxxxxx",
                "creator": "xxxxxxxxx",
                "end_time": "2025-11-11 16:49:01",
                "group": "llm",
                "usage": 432000,
                "max_output_cnt": 8,
                "output_cnt": 8
            }
        ]
    }
}
```

### **取消微调任务**

**请求示例**

```
curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/<替换为微调任务job_id>/cancel' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json'
```

**响应示例**

```
{
    "request_id": "d8dab938-e32e-40bf-83ab-xxxxxx",
    "output": {
        "status": "success"
    }
}
```

### **删除微调任务**

**请求示例**

```
curl --location --request DELETE 'https://dashscope.aliyuncs.com/api/v1/fine-tunes/<替换为微调任务job_id>' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json'
```

**响应示例**

```
{
    "request_id": "1301136c-12f2-4504-880a-xxxxxx",
    "output": {
        "status": "success"
    }
}
```

## **部署模型管理**

### **删除部署的模型服务**

**重要**

执行该操作后，模型部署服务将立即下线且**不可恢复**：

1.  模型将无法调用。
    
2.  部署服务停止计费。
    

**请求示例**

```
curl --request DELETE 'https://dashscope.aliyuncs.com/api/v1/deployments/<替换为deployed_model>' \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header 'Content-Type: application/json'
```

**响应示例**

关注`output.status`参数：若值为 DELETING，表示删除请求已成功提交，正在删除模型服务。

```
{
    "request_id": "c2ed2aa2-39b8-4a86-b79e-xxxxxx",
    "output": {
        "deployed_model": "wan2.5-i2v-preview-ft-202511111122-xxxx",
        "gmt_create": "2025-11-11T17:46:53",
        "gmt_modified": "2025-12-22T11:18:27.532",
        "status": "DELETING",
        "model_name": "wan2.5-i2v-preview-ft-202511111122-xxxx",
        "base_model": "wan2.5-i2v-preview",
        "workspace_id": "llm-xxxxxx",
        "charge_type": "post_paid",
        "creator": "xxxxxx",
        "modifier": "xxxxxx",
        "plan": "lora"
    }
}
```

之后，再调用[查询模型部署状态](#04b2baf08b1e9)进行验证。若返回如下内容，说明部署的服务已不存在，删除成功。

```
{
    "request_id": "eb619064-0c4£-4d29-aa49-xxxxxx",
    "message": "Not found.",
    "code": "NotFound"
}
```
