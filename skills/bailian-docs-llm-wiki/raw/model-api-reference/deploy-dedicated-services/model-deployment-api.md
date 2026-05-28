# 模型部署API参考

本文档以通义千问模型的部署为例进行说明，使用 API（HTTP）调用方式帮助您使用阿里云百炼提供的模型部署功能。

## 前提条件

-   您已经阅读了[模型部署简介](https://help.aliyun.com/zh/model-studio/model-deployment-introduction)和[使用 API 进行模型部署](https://help.aliyun.com/zh/model-studio/model-deployment-quick-start)的相关内容，掌握了模型部署 API 的使用方法，并熟悉了在阿里云百炼平台上进行模型部署的基本步骤。
    
-   已配置百炼的 API-KEY， 请参考[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。
    

## 获取可以部署的模型列表

### **地址**

```
GET https://dashscope.aliyuncs.com/api/v1/deployments/models
```

### **请求示例**

通过下面的命令可以查询支持部署的模型。

```
curl "https://dashscope.aliyuncs.com/api/v1/deployments/models?page_no=1&page_size=100" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json'
```

### **请求参数**

**参数**

**类型**

**传参方式**

**必选**

**说明**

page\_no

Number

query

否

页码，默认值为1。

page\_size

Number

query

否

页大小，默认为50，最大值为200，最小值为1。

### **响应示例**

命令执行完成后，获得以下结果：

```
{
    "request_id":"f7da015c-ea90-4d96-af89-2f8d7604026a",
    "output":{
        "models":[
            {
                "model_name":"emo",
                "base_capacity":1
            },
            {
                "model_name":"qwen-plus-ft-20230703-cx7f",
                "base_capacity":8
            }
            ...
        ],
        "page_no":1,
        "page_size":50,
        "total":2
    }
}
```

### **响应参数**

**参数**

**类型**

**说明**

model\_name

String

支持部署的模型名称。

base\_capacity

String

该字段定义了模型部署所需的最小资源单元数量。

page\_no

Number

查询页码。

page\_size

Number

查询页大小。

total

Long

满足查询条件的所有模型个数。

## 创建模型部署任务

### **地址**

```
POST https://dashscope.aliyuncs.com/api/v1/deployments
```

### **请求示例**

#### 按预置吞吐（PTU）计费

**说明**

执行以下部署命令后，即便您还没有调用模型，模型部署服务仍将在部署成功后开始计费。建议您先确认服务计费规则，再执行部署命令。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5681566771/p1069175.png)

```
curl "https://dashscope.aliyuncs.com/api/v1/deployments" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "name": "my_qwen_flash",
    "model_name": "qwen-flash-2025-07-28",
    "plan": "ptu",
    "ptu_capacity": {
        "input_tpm": 10000,
	"output_tpm": 1000
    }
}'
```

#### 按模型单元的使用时长计费

**说明**

-   执行以下部署命令后，即便您还没有调用模型，模型部署服务仍将在部署成功后开始计费。建议您先确认服务计费规则，再执行部署命令。
    
-   模型单元-后付费方式的算力资源先买到先得。如购买不成功会全额退款。
    

#### ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1816324671/p1028065.png)

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

模型单元部署模式还支持以下更多设置：

**配置内容**

**配置详情**

配置模型推理模式

部分模型在以**模型单元**方式部署时，可配置推理模式、最长上下文等。

-   Instruct - 模型部署后以**非思考模式**进行推理。
    
-   Thinking - 模型部署后以思考模式进行推理。
    

最长上下文

部分模型的**模型单元**部署模式支持该设置。最长上下文长度基于模型类型。

服务限流

部分模型的**模型单元**部署模式支持该设置，可限制模型调用的 RPM、TPM。

如何在 API 设置上述内容，请参考：[使用 API 创建模型部署任务](https://help.aliyun.com/zh/model-studio/model-deployment-api#0dda8fc0587ho)。

#### 按模型 Token 使用量计费

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1816324671/p1028063.png)

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

> capacity 参数设置无效，但必须填写。如需希望扩缩容，请前往百炼模型部署[控制台](https://bailian.console.aliyun.com/tab=model?tab=model#/efm/model_deploy)填写表单申请。

#### **按算力单元的使用时长收费（仅适用于图片生成、视频生成）**

**说明**

执行以下部署命令后，即便您还没有调用模型，模型部署服务仍将在部署成功后开始计费。建议您先确认服务计费规则，再执行部署命令。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1816324671/p1028070.png)

```
curl "https://dashscope.aliyuncs.com/api/v1/deployments" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{        
    "model_name": "animate-anyone-detect",
    "capacity": 2,
    "plan": "cu",
    "name": "my_animate"
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

待部署的模型名称，对应[我的模型](https://bailian.console.aliyun.com/?tab=model#/efm/model_center)中的模型 ID。

capacity

Number

body

是

表示实际分配给模型的资源单元数量。**必须**是`[base_capacity](#4d68826158yix)`的整数倍。

> 按 Token 用量计费的部署方式，capacity 参数设置无效，但必须填写。如需希望扩缩容，请前往百炼模型部署[控制台](https://bailian.console.aliyun.com/tab=model?tab=model#/efm/model_deploy)填写表单申请。

plan

String

body

否

支持三种部署后的计费模式：

**计费方式**

**plan 设置**

按算力计费

不设置该参数

按 Token 用量计费

`"plan": "lora"`

按模型单元计费

`"plan": "mu"`

调优后的模型支持的部署方式可以在[我的模型](https://bailian.console.aliyun.com/?tab=model#/efm/model_center)中快速查询到。

diasplay\_name

String

body

否

模型的控制台显示名称

deploy\_spec

String

body

否

仅`"plan": "mu"`时，可填写该设置。

具体支持情况请参考：[模型单元部署的功能支持情况](#2fc096b2fdw9z)。

当设置`"plan": "mu"`时，该参数**必须填写**。样例：`"deploy_spec": "MU1"`。

enable\_thinking

Boolean

body

否

部分模型支持，可设置为`true`或`false`。

max\_context\_length

Number

body

否

部分模型支持。样例：`"max_context_length": 131072`。

rpm\_limit

Number

body

否

部分模型支持， requests per minute，每分钟请求数。

tpm\_limit

Number

body

否

部分模型支持， token per minute，每分钟 Token 使用量。

suffix

String

body

否

模型部署后，将生成新的模型名称，**suffix** 用于指定新模型名称的后缀，最大长度为8个字符且需全局唯一。每个模型在首次部署时，可以不指定后缀。如果需要对同一模型进行多次部署，则必须设置后缀以便于区分。

参考输出参数 **deployed\_model**。

### **支持的模型**

**模型单元**部署模式下，限流、推理加速等功能的**支持情况**。

#### 文本生成

##### 千问

**模型名称**

**模型代码**

**模型单元规格**

**小时单价（元）**

**月单价（元）**

千问3.6-35B-A3B

qwen3.6-35b-a3b

MU8

¥47

¥22,400

MU9

¥51

¥24,600

千问3.6-27B

qwen3.6-27b

MU9

¥51

¥24,600

千问3.6-Flash-2026-04-16

qwen3.6-flash-2026-04-16

MU1

¥54

¥26,118

千问3.6-Plus-2026-04-02

qwen3.6-plus-2026-04-02

MU1

¥54

PD分离模式：¥864

¥26,118

PD分离模式：¥417,888

千问3.5-397B-A17B

qwen3.5-397b-a17b

MU3

¥137

PD分离模式：¥2,192

¥65,969

PD分离模式：¥1,055,504

MU6

¥25

¥12,089

千问3.5-122B-A10B

qwen3.5-122b-a10b

MU1

¥54

¥26,118

MU2

¥63

¥30,036

MU6

¥25

¥12,089

MU9

¥51

¥24,600

千问3.5-35B-A3B

qwen3.5-35b-a3b

MU1

¥54

¥26,118

MU2

¥63

¥30,036

MU8

¥47

¥22,400

MU9

¥51

¥24,600

千问3.5-27B

qwen3.5-27b

MU1

¥54

¥26,118

MU9

¥51

¥24,600

千问3.5-9B

qwen3.5-9b

MU1

¥54

¥26,118

MU8

¥47

¥22,400

MU9

¥51

¥24,600

千问3.5-Flash-2026-02-23

qwen3.5-flash-2026-02-23

MU1

¥54

¥26,118

MU2

¥63

¥30,036

千问3.5-Plus-2026-02-15

qwen3.5-plus-2026-02-15

MU1

¥54

PD分离模式：¥864

¥26,118

PD分离模式：¥417,888

MU3

¥137

PD分离模式：¥2,192

¥65,969

PD分离模式：¥1,055,504

千问3-235B-A22B-Instruct-2507

qwen3-235b-a22b-instruct-2507

MU1

¥54

¥26,118

MU2

¥63

¥30,036

千问3-Next-80B-A3B-Instruct

qwen3-next-80b-a3b-instruct

MU1

¥54

¥26,118

千问3-32B

qwen3-32b

MU1

¥54

¥26,118

MU6

¥25

¥12,089

千问3-30B-A3B

qwen3-30b-a3b

MU9

¥51

¥24,600

千问3-30B-A3B-Instruct-2507

qwen3-30b-a3b-instruct-2507

MU1

¥54

¥26,118

MU2

¥63

¥30,036

千问3-8B

qwen3-8b

MU1

¥54

¥26,118

MU2

¥63

¥30,036

MU5

¥21

¥10,139

千问3-4B

qwen3-4b

MU1

¥54

¥26,118

MU5

¥21

¥10,139

千问3-1.7B

qwen3-1.7b

MU1

¥54

¥26,118

MU5

¥21

¥10,139

千问3-Embedding-0.6B

qwen3-embedding-0.6b

MU5

¥21

¥10,139

MU6

¥25

¥12,089

千问3-MoE-Rerank-0.6B

qwen3-moe-rerank-0.6b

MU5

¥21

¥10,139

千问3-Rerank-0.6B

qwen3-rerank-0.6b

MU5

¥21

¥10,139

MU6

¥25

¥12,089

千问3-Max-2025-09-23

qwen3-max-2025-09-23

MU2

¥63

¥30,036

MU3

¥137

¥65,969

千问3-Rerank

qwen3-rerank

MU5

¥21

¥10,139

千问2.5-开源版-72B

qwen2.5-72b-instruct

MU1

¥54

¥26,118

千问2.5-开源版-32B

qwen2.5-32b-instruct

MU1

¥54

¥26,118

千问2.5-开源版-14B

qwen2.5-14b-instruct

MU1

¥54

¥26,118

千问2.5-开源版-7B

qwen2.5-7b-instruct

MU1

¥54

¥26,118

MU5

¥21

¥10,139

千问2.5-开源版-3B

qwen2.5-3b-instruct

MU5

¥21

¥10,139

千问-Flash-2025-07-28

qwen-flash-2025-07-28

MU1

¥54

¥26,118

千问-Plus-2025-07-28

qwen-plus-2025-07-28

MU1

¥54

PD分离模式：¥864

¥26,118

PD分离模式：¥417,888

千问-Plus-2025-12-01

qwen-plus-2025-12-01

MU1

¥54

¥26,118

##### GLM

**模型名称**

**模型代码**

**模型单元规格**

**小时单价（元）**

**月单价（元）**

GLM-5

glm-5

MU3

¥137

PD分离模式：¥2,192

¥65,969

PD分离模式：¥1,055,504

GLM-4.7

glm-4.7

MU6

¥25

PD分离模式：¥800

¥12,089

PD分离模式：¥386,848

##### DeepSeek

**模型名称**

**模型代码**

**模型单元规格**

**小时单价（元）**

**月单价（元）**

DeepSeek-v4-Flash

deepseek-v4-flash

MU1

¥54

¥26,118

DeepSeek-v3.2

deepseek-v3.2

MU2

¥63

PD分离模式：¥1,008

¥30,036

PD分离模式：¥480,576

##### 更多模型

**模型名称**

**模型代码**

**模型单元规格**

**小时单价（元）**

**月单价（元）**

MiniMax-M2.5

MiniMax-M2.5

MU1

¥54

PD分离模式：¥864

¥26,118

PD分离模式：¥417,888

Kimi-K2.5

kimi-k2.5

MU2

¥63

¥30,036

模型类型：

-   Instruct - 模型部署后以**非思考模式**进行推理。
    
-   Thinking - 模型部署后以思考模式进行推理。
    

模型部署类型：

-   PD 分离模式 - **降低首 Token 延迟、提高吞吐。**
    
    该部署模式部署的模型在进行模型推理时，将首 Token 计算（Prefill）和后续 Token 计算（Decode）两个计算阶段，拆到不同的计算节点执行。
    

#### 多模态

##### 千问VL

**模型名称**

**模型代码**

**模型单元规格**

**小时单价（元）**

**月单价（元）**

千问3.5-Omni-Flash

qwen3.5-omni-flash

MU8

¥47

¥22,400

MU9

¥51

¥24,600

千问3.5-Omni-Plus

qwen3.5-omni-plus

MU9

¥51

¥24,600

千问3-VL-235B-A22B-Instruct

qwen3-vl-235b-a22b-instruct

MU1

¥54

¥26,118

千问3-VL-235B-A22B-Thinking

qwen3-vl-235b-a22b-thinking

MU1

¥54

¥26,118

千问3-VL-32B-Instruct

qwen3-vl-32b-instruct

MU2

¥63

¥30,036

千问3-VL-8B-Instruct

qwen3-vl-8b-instruct

MU1

¥54

¥26,118

千问3-VL-4B-Instruct

qwen3-vl-4b-instruct

MU1

¥54

¥26,118

千问3-VL-2B-Instruct

qwen3-vl-2b-instruct

MU5

¥21

¥10,139

千问3-VL-Embedding-2B

qwen3-vl-embedding-2b

MU5

¥21

¥10,139

千问3-VL-Flash-2025-10-15

qwen3-vl-flash-2025-10-15

MU1

¥54

¥26,118

千问3-VL-Plus-2025-09-23

qwen3-vl-plus-2025-09-23

MU1

¥54

¥26,118

千问VL-Max-2025-08-13

qwen-vl-max-2025-08-13

MU6

¥25

¥12,089

千问VL-OCR-2025-11-20

qwen-vl-ocr-2025-11-20

MU6

¥25

¥12,089

模型类型：

-   Instruct - 模型部署后以**非思考模式**进行推理。
    
-   Thinking - 模型部署后以思考模式进行推理。
    
-   Instruct/Thinking - 可在模型部署时**选择是否开启思考模式**。
    

### **响应示例**

命令执行完成后，返回如下结果：

```
{
  "request_id": "f2ae64f7-83cc-410c-bc0b-840443f7eb86",
  "output": {
    "deployed_model": "emo-35b3f106-sample01",
    "gmt_create": "2025-06-17T11:00:38.68",
    "gmt_modified": "2025-06-17T11:00:38.68",
    "status": "PENDING",
    "model_name": "emo",
    "base_model": "emo",
    "base_capacity": 1,
    "capacity": 1,
    "ready_capacity": 0,
    "workspace_id": "llm-v71tlv3d***",
    "charge_type": "post_paid",
    "creator": "175805416***",
    "modifier": "175805416***"
  }
}
```

### **响应参数**

**参数**

**类型**

**说明**

request\_id

String

本次请求的ID。

output

Object

本次部署任务的详细信息。

deployed\_model

String

新模型的唯一标识。在发起模型调用请求时需要在SDK参数传入。

gmt\_create

String

创建部署任务的时间。

gmt\_modified

String

修改部署任务的时间。

status

String

部署任务的状态。

-   PENDING：正在创建部署任务。
    
-   UPDATING：正在更新部署任务。
    
-   RUNNING：部署任务正在运行，此时已部署的模型可以正常处理请求。
    
-   STOPPED：部署任务已经停止，此时的部署任务不会被计费。
    
-   DELETING：正在删除部署任务。
    
-   FAILED：部署任务创建或更新失败。
    

model\_name

String

部署任务使用的模型名称。

base\_model

String

部署任务使用的模型对应的基础模型ID。

base\_capacity

Number

基础模型运行所需的最小资源单元数量。

capacity

Number

部署任务使用的资源单元数量。

ready\_capacity

Number

已就绪并可立即处理请求的资源单元数量。受限于资源初始化速度或硬件状态。

workspace\_id

String

部署任务所属的业务空间ID。

charge\_type

String

部署任务的扣费方法。

> `post_paid`：后付费。

creator

String

该部署任务创建人UID。

modifier

String

对该部署任务进行最后一次操作的账号UID。

plan

String

部署任务的计费模式。（部分模式不显示该参数）

仅**模型单元**部署方式响应

model\_unit\_spec

String

模型单元规格。

enable\_thinking

Boolean

是否开启思考模式，部分模型支持。

max\_context\_length

Number

最大上下文长度限制。

rpm\_limit

String

Requests per minute，每分钟请求数。

tpm\_limit

Number

Token per minute，每分钟 Token 使用量。

## 修改部署的模型设置

**说明**

仅模型单元部署方式的[部分模型](#2fc096b2fdw9z)支持修改设置 rpm 和 tpm。

### **地址**

```
PUT https://dashscope.aliyuncs.com/api/v1/deployments/{deployed_model}/update
```

### **请求示例**

通过以下命令可以查询指定专属服务的详细信息：

```
curl -X PUT "https://dashscope.aliyuncs.com/api/v1/deployments/{deployed_model}/update" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "rpm_limit": 1000,
    "tpm_limit": 200
}'
```

### **请求参数**

**参数**

**类型**

**传参方式**

**必选**

**说明**

deployed\_model

String

path

是

新模型的唯一标识。

rpm\_limit

Number

body

至少填写一个参数

Requests per minute，每分钟请求数。

tpm\_limit

Number

body

Token per minute，每分钟 Token 使用量。

### **响应示例**

命令执行完成后，返回如下结果：

```
{
    "request_id": "1d121fd9-876c-40ad-bc40-a9e68ef3b986",
    "output":
    {
        "deployed_model": "qwen-plus-2025-12-01-b6d61c71",
        "gmt_create": "2026-01-07T13:52:44",
        "gmt_modified": "2026-01-07T14:01:41",
        "status": "PENDING",
        "model_name": "qwen-plus-2025-12-01",
        "base_model": "qwen-plus-2025-12-01",
        "base_capacity": 4,
        "capacity": 4,
        "ready_capacity": 0,
        "workspace_id": "llm-8v53e*******",
        "charge_type": "post_paid",
        "creator": "16542902******",
        "modifier": "16542902********",
        "plan": "mu",
        "model_unit_spec": "MU1",
        "enable_thinking": true,
        "max_context_length": 1,
        "rpm_limit": 1000,
        "tpm_limit": 200
    }
}
```

### **响应参数**

请参考[创建模型部署任务](#13f7a7d05829h)的响应参数。

## 查询模型部署任务

### **地址**

```
GET https://dashscope.aliyuncs.com/api/v1/deployments/{deployed_model}
```

### **请求示例**

通过以下命令可以查询指定专属服务的详细信息：

```
curl "https://dashscope.aliyuncs.com/api/v1/deployments/qwen-plus-202305099980-fac9-sample" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json'
```

### **请求参数**

**参数**

**类型**

**传参方式**

**必选**

**说明**

deployed\_model

String

path

是

新模型的唯一标识。

### **响应示例**

命令执行完成后，返回如下结果：

```
{
  "request_id": "66a855f0-a6fe-4b05-9786-fb30c7c6782d",
  "output": {
    "deployed_model": "emo-35b3f106-sample01",
    "gmt_create": "2025-06-17T11:00:38",
    "gmt_modified": "2025-06-17T11:06:13",
    "status": "RUNNING",
    "model_name": "emo",
    "base_model": "emo",
    "base_capacity": 1,
    "capacity": 1,
    "ready_capacity": 1,
    "workspace_id": "llm-v71tlv3***",
    "charge_type": "post_paid",
    "creator": "175805416***",
    "modifier": "175805416***"
  }
}
```

### **响应参数**

请参考[创建模型部署任务](#13f7a7d05829h)的响应参数。

## 列举模型部署任务

### **地址**

```
GET https://dashscope.aliyuncs.com/api/v1/deployments
```

### **请求示例**

通过以下命令可以获取专属服务列表：

```
curl "https://dashscope.aliyuncs.com/api/v1/deployments?page_no=1&page_size=100" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json'
```

### **请求参数**

**参数**

**类型**

**传参方式**

**必选**

**说明**

page\_no

Number

query

否

页码，默认值为1。

page\_size

Number

query

否

页大小，默认为50，最大值为200，最小值为1。

### **响应示例**

命令执行完成后，返回以下结果：

```
{
  "request_id": "7efdd3a7-a90d-96c6-b477-70055d59edf7",
  "output": {
    "page_no": 1,
    "page_size": 10,
    "total": 1,
    "deployments": [
      {
        "deployed_model": "emo-35b3f106-sample01",
        "gmt_create": "2025-06-17T11:00:38",
        "gmt_modified": "2025-06-17T11:06:13",
        "status": "RUNNING",
        "model_name": "emo",
        "base_model": "emo",
        "base_capacity": 1,
        "capacity": 1,
        "ready_capacity": 1,
        "workspace_id": "llm-v71tlv3d***",
        "charge_type": "post_paid",
        "creator": "175805416***",
        "modifier": "175805416***",
        "plan": "cu"
      }
    ]
  }
}
```

### **响应参数**

请参考[创建模型部署任务](#13f7a7d05829h)的响应参数。

## 更新模型部署任务

通过更新操作调整专属服务使用的资源单元数量。

### **地址**

```
PUT https://dashscope.aliyuncs.com/api/v1/deployments/{deployed_model}/scale
```

### **请求示例**

通过以下命令可以将指定的服务进行扩缩容：

```
curl --request PUT "https://dashscope.aliyuncs.com/api/v1/deployments/emo-35b3f106-sample01/scale" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json' \
    --data '{    
                "capacity":2
            }'
```

### **请求参数**

**参数**

**类型**

**传参方式**

**必选**

**说明**

deployed\_model

String

path

是

新模型的唯一标识。

capacity

Number

body

是

更新之后，模型所使用的资源单元。**必须**是`[base_capacity](#4d68826158yix)`的整数倍。

### **响应示例**

命令执行完成后，返回以下结果：

```
{
  "request_id": "6c6b7676-3fea-423b-bc26-c9e2337e1142",
  "output": {
    "deployed_model": "emo-35b3f106-sample01",
    "gmt_create": "2025-06-17T11:00:38",
    "gmt_modified": "2025-06-17T11:42:02.311",
    "status": "UPDATING",
    "model_name": "emo",
    "base_model": "emo",
    "base_capacity": 1,
    "capacity": 2,
    "ready_capacity": 1,
    "workspace_id": "llm-v71tlv3dezezp2en",
    "charge_type": "post_paid",
    "creator": "17580541***",
    "modifier": "17580541***"
  }
}
```

### **响应参数**

请参考[创建模型部署任务](#13f7a7d05829h)的响应参数。

## 删除模型部署任务

### **地址**

```
DELETE https://dashscope.aliyuncs.com/api/v1/deployments/{deployed_model}
```

### **请求示例**

通过以下命令可以删除指定的部署任务。

```
curl --request DELETE "https://dashscope.aliyuncs.com/api/v1/deployments/emo-35b3f106-sample01" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json'
```

### **请求参数**

**参数**

**类型**

**传参方式**

**必选**

**说明**

deployed\_model

String

path

是

新模型的唯一标识。

### **响应示例**

命令执行完成后，返回以下结果：

```
{
  "request_id": "5378b78b-8564-481f-a3e0-580e551df22c",
  "output": {
    "deployed_model": "emo-35b3f106-sample01",
    "gmt_create": "2025-06-17T11:00:38",
    "gmt_modified": "2025-06-17T11:42:02",
    "status": "DELETING",
    "model_name": "emo",
    "base_model": "emo",
    "base_capacity": 1,
    "capacity": 2,
    "ready_capacity": 1,
    "workspace_id": "llm-v71tlv3***",
    "charge_type": "post_paid",
    "creator": "175805416***",
    "modifier": "175805416***"
  }
}
```

### **响应参数**

请参考[创建模型部署任务](#13f7a7d05829h)的响应参数。

## 异常响应

### **响应示例**

```
{
    "request_id": "ca218d57-b91b-46b2-bd35-c41c6287bcf4",
    "message": "Model: qwen-plus-20230703-cx7f not found!",
    "code": "NotFound"
}
```

### **响应参数**

**字段**

**类型**

**描述**

request\_id

String

本次请求的系统唯一码。

code

String

错误码。

message

String

错误信息。

当请求出错时，可能返回以下错误：

**错误码**

**错误信息**

**错误原因**

**NotFound**

Model: xxx not found!

-   创建部署任务时指定了不存在的模型。
    
-   查询/更新/删除部署任务时指定了不存在的模型。
    

**Conflict**

Deployed model xxx already exists, please specify a suffix.

创建部署任务时使用了已使用过的suffix。

**InvalidParameter**

Invalid capacity (xx), capacity must be larger than or equal to 0 and multiples of 1 and less than 1000!

创建/更新部署任务时指定了无效的算力单元数量。
