# 人物形象训练API详情

**重要**本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

## 人物形象训练

**说明**支持的领域 / 任务：aigc /facechain人物写真生成

对上传的图像压缩包进行模型训练，从而获得该图像中对应人物的resource，基于该resource可以实现人物的写真生成。

人物形象训练是人物写真生成的前置环节，只有在针对某人物进行形象训练并成功获得形象resource后，才可基于此进行生成。

## 模型概览

模型名

模型简介

facechain-finetune

对上传的图像进行模型训练，从而获得该图像中对应人物的resource，基于该resource可以实现人物的写真生成。

## HTTP调用接口

### 功能描述

本接口为模型定制类服务，需要相对较长的算法调用时间，所以在接口层面采用了异步调用的方式进行任务提交，在通过任务接口提交作业之后，系统会返回对应的作业ID，随后可以通过对模型定制类任务的查询/管理接口进行相应操作。

### 前提条件

-   已开通服务并获得API-KEY：[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。

**说明**接口限制：对单账户（含主账号与RAM子账号）任务下发接口限制QPS为2，并发任务数量限制为1。

### 准备训练数据

准备1~10张包含人脸的图片，您可以通过以下方式将这些图片提供给训练服务：

1、将这些图片存储在文件服务（例如阿里云oss）中，并生成授权的访问链接【推荐】

2、如果您没有合适的文件服务，可以将这些图片分别或打包成zip文件上传至大模型服务平台提供的模型定制文件管理服务中，并获取file\_id。

### 文件管理

您可以使用DashScope提供的文件服务来管理您的训练文件，详细的api请参考[百炼文件管理 API](https://help.aliyun.com/zh/model-studio/model-customization-file-management-service)。

### 步骤1：创建模型定制任务

```
POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/fine-tunes
```

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)。

##### 功能描述

完成训练数据的上传之后，就可以使用在上传之后得到的 file\_id 发起facechain模型定制任务。

##### 入参描述

**字段**

**类型**

**传参方式**

**必选**

**描述**

**示例值**

Content-Type

String

Header

是

请求类型：application/json

application/json

Authorization

String

Header

是

API-Key，例如：Bearer sk-xxxx

Bearer sk-xxxx

model

String

Body

是

用于定制的基础模型名

facechain-finetune

training\_file\_ids

Array

Body

是

训练集文件列表，此处使用前述准备好的训练文件，支持url、file\_id及两者混合

\[ "[](https://dashscope.oss-cn-beijing.aliyuncs.com/samples/fine-tune/facechain/sample1.jpg)[https://dashscope.oss-cn-beijing.aliyuncs.com/samples/fine-tune/facechain/sample1.jpg](https://dashscope.oss-cn-beijing.aliyuncs.com/samples/fine-tune/facechain/sample1.jpg)","[](https://dashscope.oss-cn-beijing.aliyuncs.com/samples/fine-tune/facechain/sample2.jpg)[https://dashscope.oss-cn-beijing.aliyuncs.com/samples/fine-tune/facechain/sample2.jpg](https://dashscope.oss-cn-beijing.aliyuncs.com/samples/fine-tune/facechain/sample2.jpg)","[](https://dashscope.oss-cn-beijing.aliyuncs.com/samples/fine-tune/facechain/sample3.jpg)[https://dashscope.oss-cn-beijing.aliyuncs.com/samples/fine-tune/facechain/sample3.jpg](https://dashscope.oss-cn-beijing.aliyuncs.com/samples/fine-tune/facechain/sample3.jpg)"\]

##### 出参描述

**字段**

**类型**

**描述**

**示例值**

request\_id

String

本次请求的唯一标识符，用于问题排查和日志追踪

7574ee8f-38a3-4b1e-9280-11c33ab46e51

output.status

String

任务状态。可选值包括：

-   PENDING：任务排队中
    
-   RUNNING：任务处理中
    
-   SUCCEEDED：任务执行成功
    
-   FAILED：任务执行失败
    
-   CANCELED：任务取消成功
    
-   UNKNOWN：任务不存在或状态未知
    

PENDING

output.job\_id

String

系统生成的唯一任务 ID，用于查询该定制训练任务

ft-202509020951-f8bf

output.job\_name

String

任务名称，通常与任务 ID 一致

ft-202509020951-f8bf

output.finetuned\_output

String

定制完成后生成的模型名称，后续推理调用需使用此模型

facechain-finetune-ft-202509020951-f8bf

output.model

String

定制任务使用的模型标识

facechain-finetune

output.base\_model

String

定制任务使用的基准模型，即预训练模型

facechain-finetune

output.training\_file\_ids

Array

用于模型训练的输入文件 URL 列表（支持多个）

\[ "[](https://dashscope.oss-cn-beijing.aliyuncs.com/samples/fine-tune/facechain/sample1.jpg)[https://dashscope.oss-cn-beijing.aliyuncs.com/samples/fine-tune/facechain/sample1.jpg](https://dashscope.oss-cn-beijing.aliyuncs.com/samples/fine-tune/facechain/sample1.jpg)"\]

output.validation\_file\_ids

Array

用于模型验证的文件 URL 列表，可为空表示无验证集

\[\]

output.hyper\_parameters

Object

训练过程中使用的超参数配置，默认返回为空

{}

output.training\_type

String

定制模型的训练方式，当前固定为：sft

sft

output.create\_time

String

任务创建时间，格式为

YYYY-MM-DD HH:mm:ss

2025-09-02 09:51:02

output.workspace\_id

String

调用 API 所使用的 API-Key 所属的业务空间ID

llm-dmt509ikxxxxxx

output.user\_identity

String

调用 API 的账号唯一用户标识（UID）

12402258xxxxxx

output.modifier

String

最近一次修改该任务的用户 UID

12402258xxxxxx

output.creator

String

该训练任务的创建者用户 UID

12402258xxxxxx

output.group

String

任务所属的逻辑分组标签

facechain

output.model\_name

String

任务的模型名称标识，通常与任务 ID 一致

ft-202509020951-f8bf

output.max\_output\_cnt

Int

允许同时产出的最大定制模型数量

1

#### 请求示例

**说明**需要使用您的API-KEY替换示例中的<YOUR-DASHSCOPE-API-KEY>，代码才能正常运行。

```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/fine-tunes' \
--header 'Authorization: Bearer <YOUR-DASHSCOPE-API-KEY>' \
--header 'Content-Type: application/json' \
--data '{
    "model": "facechain-finetune",
    "training_file_ids": [
        "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/fine-tune/facechain/sample1.jpg"
    ]
}'
```

#### 响应示例

```
{
    "request_id": "b6c9e77d-02a1-4a70-b127-xxxxxx",
    "output": {
        "job_id": "ft-202509020951-f8bf",
        "job_name": "ft-202509020951-f8bf",
        "status": "PENDING",
        "finetuned_output": "facechain-finetune-ft-202509020951-f8bf",
        "model": "facechain-finetune",
        "base_model": "facechain-finetune",
        "training_file_ids": [
            "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/fine-tune/facechain/sample1.jpg"
        ],
        "validation_file_ids": [],
        "hyper_parameters": {},
        "training_type": "sft",
        "create_time": "2025-09-02 09:51:02",
        "workspace_id": "llm-dmt509ikxxxxxx",
        "user_identity": "12402258xxxxxx",
        "modifier": "124022586xxxxxx",
        "creator": "1240225868xxxxxx",
        "group": "facechain",
        "model_name": "ft-202509020951-f8bf",
        "max_output_cnt": 1
    }
}
```

### 步骤2：查询定制任务的状态

**说明**需要使用真实的job\_id替换示例中的<job\_id>，代码才能正常运行。

```
GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/fine-tunes/<job_id>
```

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)。

##### 功能描述

查询模型定制任务的状态，并在任务完成之后获取对应的任务结果。当训练任务成功之后，就可以使用对应的 finetuned\_output 内容做推理调用。

##### 入参描述

**字段**

**类型**

**传参方式**

**必选**

**描述**

**示例值**

Content-Type

String

Header

是

请求类型：application/json

application/json

Authorization

String

Header

是

API-Key，例如：Bearer sk-xxxx

Bearer sk-xxxx

job\_id

String

URL

是

需要查询的作业 id

ft-202509020951-f8bf

##### 出参描述

**字段**

**类型**

**描述**

**示例值**

request\_id

String

本次请求的唯一标识符，用于问题排查和日志追踪

7574ee8f-38a3-4b1e-9280-11c33ab46e51

output.status

String

任务状态。可选值包括：

-   PENDING：任务排队中
    
-   RUNNING：任务处理中
    
-   SUCCEEDED：任务执行成功
    
-   FAILED：任务执行失败
    
-   CANCELED：任务取消成功
    
-   UNKNOWN：任务不存在或状态未知
    

PENDING

output.job\_id

String

系统生成的唯一任务 ID，用于查询该定制训练任务

ft-202509020951-f8bf

output.job\_name

String

任务名称，通常与任务 ID 一致

ft-202509020951-f8bf

output.finetuned\_output

String

定制完成后生成的模型名称，后续推理调用需使用此模型

facechain-finetune-ft-202509020951-f8bf

output.model

String

定制任务使用的模型标识

facechain-finetune

output.base\_model

String

定制任务使用的基准模型，即预训练模型

facechain-finetune

output.training\_file\_ids

Array

用于模型训练的输入文件 URL 列表（支持多个）

\[ "[](https://dashscope.oss-cn-beijing.aliyuncs.com/samples/fine-tune/facechain/sample1.jpg)[https://dashscope.oss-cn-beijing.aliyuncs.com/samples/fine-tune/facechain/sample1.jpg](https://dashscope.oss-cn-beijing.aliyuncs.com/samples/fine-tune/facechain/sample1.jpg)"\]

output.validation\_file\_ids

Array

用于模型验证的文件 URL 列表，可为空表示无验证集

\[\]

output.hyper\_parameters

Object

训练过程中使用的超参数配置，默认返回为空

{}

output.training\_type

String

定制模型的训练方式，当前固定为：sft

sft

output.create\_time

String

任务创建时间，格式为

YYYY-MM-DD HH:mm:ss

2025-09-02 09:51:02

output.workspace\_id

String

调用 API 所使用的 API-Key 所属的业务空间ID

llm-dmt509ikxxxxxx

output.user\_identity

String

调用 API 的账号唯一用户标识（UID）

12402258xxxxxx

output.modifier

String

最近一次修改该任务的用户 UID

12402258xxxxxx

output.creator

String

该训练任务的创建者用户 UID

12402258xxxxxx

output.group

String

任务所属的逻辑分组标签

facechain

output.usage

Int

训练次数，用于计量计费

1

output.end\_time

String

任务结束时间，格式为

YYYY-MM-DD HH:mm:ss

仅在任务完成（SUCCEEDED/FAILED）后返回

2025-09-02 09:56:04

output.model\_name

String

任务的模型名称标识，通常与任务 ID 一致

ft-202509020951-f8bf

output.max\_output\_cnt

Int

允许同时产出的最大定制模型数量

1

output.output\_cnt

Int

当前已产出的定制模型数量

仅在任务完成后返回

1

#### 请求示例

**说明**需要使用您的API-KEY替换示例中的<YOUR-DASHSCOPE-API-KEY>，代码才能正常运行。

```
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/fine-tunes/ft-202509020951-xxxx' \
--header 'Authorization: Bearer <YOUR-DASHSCOPE-API-KEY>' \
--header 'Content-Type: application/json'
```

#### 响应示例

```
{
    "request_id": "fcfb99e6-7ae5-48b2-acca-xxxxxx",
    "output": {
        "job_id": "ft-202509020951-f8bf",
        "job_name": "ft-202509020951-f8bf",
        "status": "SUCCEEDED",
        "finetuned_output": "facechain-finetune-ft-202509020951-f8bf",
        "model": "facechain-finetune",
        "base_model": "facechain-finetune",
        "training_file_ids": [
            "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/fine-tune/facechain/sample1.jpg"
        ],
        "validation_file_ids": [],
        "hyper_parameters": {},
        "training_type": "sft",
        "create_time": "2025-09-02 09:51:02",
        "workspace_id": "llm-dmt509ikfxxxxxxx",
        "user_identity": "1240225868xxxxxx",
        "modifier": "1240225868xxxxxx",
        "creator": "1240225868xxxxxx",
        "end_time": "2025-09-02 09:56:04",
        "group": "facechain",
        "usage": 1,
        "model_name": "ft-202509020951-f8bf",
        "max_output_cnt": 1,
        "output_cnt": 1
    }
}
```

其他更多定制任务的列举、删除等能力，请参考[模型定制API详情](https://help.aliyun.com/zh/model-studio/model-training-api-reference)

## 状态码说明

大模型服务平台通用状态码请查阅：[错误码](raw/model-api-reference/preparations/error-code.md)

同时本模型还有如下特定错误码：

**http状态码**

**错误码（code）**

**错误信息（message）**

**含义说明**

**处理方式**

400

InvalidParameter

Missing training files.

参数错误，缺少参数或者参数格式问题等

根据错误信息，修正您的参数

400

UnsupportedOperation

The fine-tune job can not be deleted because it is succeeded,failed or canceled

当资源处于特定状态时，无法对其进行操作

待要操作的资源到达可操作状态时再进行操作

404

NotFound

job {job\_id} not found.

要查询/操作的资源不存在

检查要查询/操作的资源id是否错误

409

Conflict

Model instance xxxxx already exists, please specify a suffix

已存在deployed\_model名为xxxxx的部署实例，需要指定后缀进行区分

为部署指定唯一的后缀

429

Throttling

Too many fine-tune job in running, please retry later

资源的创建触发平台限制

稍后再试

500

InternalError

Internal server error!

内部错误

记录reqeust\_id，通过工单联系阿里云
