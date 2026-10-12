# 模型部署新 API 参考

本文档以千问模型的部署为例进行说明，使用 API（HTTP）调用方式帮助您使用阿里云百炼提供的模型部署功能。

**重要**本文档仅适用于华北2（北京）地域。

## 前提条件

-   您已经阅读了[模型部署](raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)和[使用 API 进行模型部署](raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)的相关内容，掌握了模型部署 API 的使用方法，并熟悉了在阿里云百炼平台上进行模型部署的基本步骤。
-   已配置百炼的 API-KEY， 请参考[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。

## 获取可以部署的模型列表

```
GET https://dashscope.aliyuncs.com/api/v1/deployments/models
```

### 请求示例

通过下面的命令可以查询支持部署的模型，推荐使用`version=v1.0`获取包含部署方案和模板信息的完整响应。

```
curl "https://dashscope.aliyuncs.com/api/v1/deployments/models?page_no=1&page_size=100&version=v1.0&model_source=base" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json'
```

查询用户微调模型：

```
curl "https://dashscope.aliyuncs.com/api/v1/deployments/models?page_no=1&page_size=100&version=v1.0&model_source=custom" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json'
```

### 请求参数

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

页大小，默认为50，最大值为100，最小值为1。

model\_source

String

query

否

模型来源。`base`表示系统模型（默认），`custom`表示用户微调模型。

version

String

query

否

API 版本，推荐使用`v1.0`。使用`v1.0`时，响应中将包含完整的部署方案和模板信息。

### 响应示例&参数

点击此处查看

命令执行完成后，获得以下结果：

```
{
    "request_id": "f7da015c-ea90-4d96-af89-2f8d7604026a",
    "output": {
        "page_no": 1,
        "page_size": 100,
        "total": 5,
        "models": [
            {
                "model_name": "qwen3-8b",
                "plans": [
                    {
                        "plan": "mu",
                        "templates": [
                            {
                                "template_id": "MU1",
                                "template_name": "单机部署-标准推理型",
                                "template_type": "COUPLED",
                                "template_version": "v1",
                                "template_desc": "适用于标准推理场景",
                                "roles": {
                                    "unified": {
                                        "model_unit_spec": "MU1",
                                        "capacity_unit_per_instance": 4
                                    }
                                }
                            },
                            {
                                "template_id": "MU1-PD",
                                "template_name": "PD分离部署-标准推理型",
                                "template_type": "SEPERATED",
                                "template_version": "v1",
                                "template_desc": "适用于PD分离推理场景",
                                "roles": {
                                    "prefill": {
                                        "model_unit_spec": "MU1",
                                        "capacity_unit_per_instance": 4
                                    },
                                    "decode": {
                                        "model_unit_spec": "MU1",
                                        "capacity_unit_per_instance": 4
                                    }
                                }
                            }
                        ]
                    },
                    {
                        "plan": "lora"
                    }
                ]
            }
        ]
    }
}
```

#### 响应参数

**参数**

**类型**

**说明**

models

Array

可部署模型列表。

models\[\].model\_name

String

模型名称。

models\[\].plans

Array

该模型支持的部署方案列表。使用`version=v1.0`时返回。

models\[\].plans\[\].plan

String

部署方案类型：`mu`（模型单元）、`cu`（算力单元）、`ptu_v2`（预置吞吐量V2）、`lora`（LoRA共享部署）。

models\[\].plans\[\].templates

Array

部署模板列表（`plan=mu`时返回）。

page\_no

Number

查询页码。

page\_size

Number

查询页大小。

total

Long

满足查询条件的所有模型个数。

#### 模板字段说明（templates）

**参数**

**类型**

**说明**

template\_id

String

模板 ID，在创建模型部署任务时作为`template_id`参数传入。

template\_name

String

模板显示名称。

template\_type

String

模板类型：`COUPLED`（非 PD 分离，使用`capacity`参数）、`SEPERATED`（PD 分离，使用`prefill_capacity`和`decode_capacity`参数）。

template\_version

String

模板版本。

template\_desc

String

模板描述。

roles

Object

节点角色配置。COUPLED 模式包含`unified`节点，SEPERATED 模式包含`prefill`和`decode`节点。

#### roles 节点字段说明

**参数**

**类型**

**说明**

model\_unit\_spec

String

模型单元规格。

capacity\_unit\_per\_instance

Number

单实例容量单元数，即 base\_capacity。创建部署时`capacity`必须是该值的整数倍。

## 创建模型部署任务

```
POST https://dashscope.aliyuncs.com/api/v1/deployments
```

### 请求示例

#### 示例1：模型单元部署（COUPLED 模式）

使用 `template_id` 指定 MU1 规格，`capacity` 为资源单元数量：

```
curl "https://dashscope.aliyuncs.com/api/v1/deployments" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model_name": "qwen3-8b",
    "plan": "mu",
    "template_id": "MU1",
    "capacity": 4
}'
```

#### 示例2：模型单元部署（PD 分离模式）

使用 `MU1-PD` 模板，分别指定 `prefill_capacity` 和 `decode_capacity`：

```
curl "https://dashscope.aliyuncs.com/api/v1/deployments" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model_name": "qwen3-8b",
    "plan": "mu",
    "template_id": "MU1-PD",
    "prefill_capacity": 4,
    "decode_capacity": 8
}'
```

#### 示例3：PTU v2 部署

按 Token 用量计费：

```
curl "https://dashscope.aliyuncs.com/api/v1/deployments" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model_name": "qwen3-8b",
    "plan": "ptu_v2"
}'
```

#### 示例4：LoRA 共享部署

按 Token 用量计费：

```
curl "https://dashscope.aliyuncs.com/api/v1/deployments" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model_name": "qwen3-8b-ft-202511132025-0260",
    "plan": "lora"
}'
```

### 请求参数

**参数**

**类型**

**传参方式**

**必选**

**说明**

model\_name

String

body

是

待部署的模型名称。

plan

String

body

是

部署方案：`mu`（模型单元）、`cu`（算力单元）、`ptu_v2`（预置吞吐量V2）、`lora`（LoRA共享部署）。

template\_id

String

body

条件必填

部署模板 ID，对应获取可以部署的模型列表接口返回的 `template_id`。设置 `plan` 为 `mu` 时必须填写。推荐使用此参数指定模型单元规格。

deploy\_spec（旧）

String

body

否

模型单元规格，已废弃。

capacity

Number

body

条件必填

资源单元数量。COUPLED 模式（非 PD 分离）必填，必须是 `capacity_unit_per_instance` 的整数倍。按 Token 用量计费（`plan` 为 `lora`）时该参数设置无效但必须填写。

prefill\_capacity

Number

body

条件必填

Prefill 容量。PD 分离模式（`template_type` 为 `SEPERATED`）时必填。

decode\_capacity

Number

body

条件必填

Decode 容量。PD 分离模式（`template_type` 为 `SEPERATED`）时必填。

name

String

body

否

服务显示名称。

suffix

String

body

否

模型部署后将生成新的模型名称，suffix 用于指定新模型名称的后缀，最大长度为8个字符且需全局唯一。每个模型在首次部署时可以不指定后缀，多次部署同一模型时必须设置。

charge\_type

String

body

否

付费方式：`post_paid`（后付费，默认）、`pre_paid`（预付费）。

pre\_paid\_info

Object

body

条件必填

预付费信息，`charge_type` 为 `pre_paid` 时必填。包含字段：`auto_renewal`（Boolean，是否自动续费）、`duration`（Number，购买时长/月）、`auto_renewal_duration`（Number，自动续费时长）。

pre\_paid\_info.auto\_renewal

Boolean

body

是

是否自动续费

pre\_paid\_info.duration

Integer

body

是

购买时长（月）

pre\_paid\_info.auto\_renewal\_duration

Integer

body

条件必填

自动续费时长（autoRenewal=true时必填）

enable\_thinking

Boolean

body

否

是否启用思考模式，部分模型支持。

max\_context\_length

Number

body

否

最大上下文长度，部分模型支持。

quantization\_precision

String

body

否

量化精度。

qpm\_limit

Number

body

否

QPM 限流，每分钟请求数限制。仅 `plan` 为 `mu` 的部分模型支持。

tpm\_limit

Number

body

否

TPM 限流，每分钟 Token 使用量限制。仅 `plan` 为 `mu` 的部分模型支持。

### 支持的模型

模型单元 部署模式下，限流、推理加速等功能的 支持情况 。

#### 文本生成

#### 千问

**模型名称**

**模型代码**

**模型单元规格**

**小时单价（元）**

**最小计费：分钟**

**包月单价（元）**

**最小计费：天**

千问3.6-35B-A3B

qwen3.6-35b-a3b

MU1 x 8

¥432

¥208,944

MU2 x 8

¥504

¥240,288

MU3 x 8

¥1,096

¥527,752

MU9 x 1

¥51

¥24,600

千问3.6-27B

qwen3.6-27b

MU9 x 1

¥51

¥24,600

千问3.6-Flash-2026-04-16

qwen3.6-flash-2026-04-16

MU1 x 2

¥108

¥52,236

MU3 x 8

¥1,096

¥527,752

千问3.6-Plus-2026-04-02

qwen3.6-plus-2026-04-02

MU1 x 8

MU1 x 16（PD分离模式）

¥432

PD分离模式：¥864

¥208,944

PD分离模式：¥417,888

千问3.5-397B-A17B

qwen3.5-397b-a17b

MU3 x 8

MU3 x 16（PD分离模式）

¥1,096

PD分离模式：¥2,192

¥527,752

PD分离模式：¥1,055,504

MU6 x 16

¥400

¥193,424

千问3.5-122B-A10B

qwen3.5-122b-a10b

MU1 x 4

¥216

¥104,472

MU6 x 16

¥400

¥193,424

千问3.5-35B-A3B

qwen3.5-35b-a3b

MU1 x 2

¥108

¥52,236

MU2 x 8

¥504

¥240,288

MU3 x 8

¥1,096

¥527,752

MU9 x 1

¥51

¥24,600

千问3.5-27B

qwen3.5-27b

MU2 x 8

¥504

¥240,288

MU3 x 8

¥1,096

¥527,752

MU8 x 1

¥47

¥22,400

MU9 x 1

¥51

¥24,600

千问3.5-9B

qwen3.5-9b

MU2 x 2

¥126

¥60,072

千问3.5-Flash-2026-02-23

qwen3.5-flash-2026-02-23

MU1 x 2

¥108

¥52,236

千问3.5-Plus-2026-02-15

qwen3.5-plus-2026-02-15

MU1 x 8

MU1 x 16（PD分离模式）

¥432

PD分离模式：¥864

¥208,944

PD分离模式：¥417,888

MU2 x 8

¥504

¥240,288

MU3 x 8

MU3 x 16（PD分离模式）

¥1,096

PD分离模式：¥2,192

¥527,752

PD分离模式：¥1,055,504

千问3-235B-A22B-Instruct-2507

qwen3-235b-a22b-instruct-2507

MU1 x 4

¥216

¥104,472

MU2 x 8

¥504

¥240,288

MU3 x 8

¥1,096

¥527,752

千问3-32B

qwen3-32b

MU6 x 16

¥400

¥193,424

千问3-30B-A3B-Thinking-2507

qwen3-30b-a3b-thinking-2507

MU1 x 2

¥108

¥52,236

千问3-8B

qwen3-8b

MU1 x 2

¥108

¥52,236

MU2 x 2

¥126

¥60,072

千问3-4B

qwen3-4b

MU1 x 2

¥108

¥52,236

MU5 x 1

¥21

¥10,139

千问3-Embedding-0.6B

qwen3-embedding-0.6b

MU5 x 1

¥21

¥10,139

MU6 x 1

¥25

¥12,089

千问3-MoE-Rerank-0.6B

qwen3-moe-rerank-0.6b

MU5 x 1

¥21

¥10,139

千问3-Rerank-0.6B

qwen3-rerank-0.6b

MU5 x 1

¥21

¥10,139

MU6 x 1

¥25

¥12,089

千问3-Max-2025-09-23

qwen3-max-2025-09-23

MU2 x 8

¥504

¥240,288

MU3 x 8

¥1,096

¥527,752

千问3-Rerank

qwen3-rerank

MU5 x 1

¥21

¥10,139

千问2.5-开源版-72B

qwen2.5-72b-instruct

MU1 x 8

¥432

¥208,944

千问2.5-开源版-14B

qwen2.5-14b-instruct

MU1 x 2

¥108

¥52,236

千问2.5-开源版-7B

qwen2.5-7b-instruct

MU1 x 2

¥108

¥52,236

MU5 x 1

¥21

¥10,139

千问-Plus-2025-07-28

qwen-plus-2025-07-28

MU1 x 4

MU1 x 16（PD分离模式）

¥216

PD分离模式：¥864

¥104,472

PD分离模式：¥417,888

千问-Plus-2025-12-01

qwen-plus-2025-12-01

MU1 x 4

¥216

¥104,472

Qwen-Plus-Character-2025-11-06

qwen-plus-character-2025-11-06

MU1 x 4

¥216

¥104,472

#### GLM

**模型名称**

**模型代码**

**模型单元规格**

**小时单价（元）**

**最小计费：分钟**

**包月单价（元）**

**最小计费：天**

GLM-5.1

glm-5.1

MU2 x 8

¥504

¥240,288

MU3 x 16（PD分离模式）

PD分离模式：¥2,192

PD分离模式：¥1,055,504

MU6 x 16

¥400

¥193,424

GLM-5

glm-5

MU3 x 16（PD分离模式）

PD分离模式：¥2,192

PD分离模式：¥1,055,504

GLM-4.7

glm-4.7

MU6 x 32（PD分离模式）

PD分离模式：¥800

PD分离模式：¥386,848

#### DeepSeek

**模型名称**

**模型代码**

**模型单元规格**

**小时单价（元）**

**最小计费：分钟**

**包月单价（元）**

**最小计费：天**

DeepSeek-v4-Flash

deepseek-v4-flash

MU1 x 8

¥432

¥208,944

MU3 x 8

¥1,096

¥527,752

DeepSeek-v3.2

deepseek-v3.2

MU2 x 16（PD分离模式）

PD分离模式：¥1,008

PD分离模式：¥480,576

#### 更多模型

**模型名称**

**模型代码**

**模型单元规格**

**小时单价（元）**

**最小计费：分钟**

**包月单价（元）**

**最小计费：天**

Kimi-K2.5

kimi-k2.5

MU2 x 8

¥504

¥240,288

模型类型：

-   Instruct - 模型部署后以**非思考模式**进行推理。
-   Thinking - 模型部署后以思考模式进行推理。

模型部署类型：

-   PD 分离模式 - **降低首 Token 延迟、提高吞吐。** 该部署模式部署的模型在进行模型推理时，将首 Token 计算（Prefill）和后续 Token 计算（Decode）两个计算阶段，拆到不同的计算节点执行。

#### 多模态

#### 千问VL

**模型名称**

**模型代码**

**模型单元规格**

**小时单价（元）**

**最小计费：分钟**

**包月单价（元）**

**最小计费：天**

千问3-VL-235B-A22B-Thinking

qwen3-vl-235b-a22b-thinking

MU1 x 8

¥432

¥208,944

MU2 x 8

¥504

¥240,288

MU3 x 8

¥1,096

¥527,752

千问3-VL-32B-Instruct

qwen3-vl-32b-instruct

MU2 x 8

¥504

¥240,288

MU3 x 8

¥1,096

¥527,752

千问3-VL-8B-Instruct

qwen3-vl-8b-instruct

MU1 x 2

¥108

¥52,236

MU5 x 1

¥21

¥10,139

千问3-VL-4B-Instruct

qwen3-vl-4b-instruct

MU1 x 2

¥108

¥52,236

千问3-VL-2B-Instruct

qwen3-vl-2b-instruct

MU5 x 1

¥21

¥10,139

千问3-VL-Embedding-2B

qwen3-vl-embedding-2b

MU5 x 1

¥21

¥10,139

千问3-VL-Flash-2025-10-15

qwen3-vl-flash-2025-10-15

MU1 x 4

¥216

¥104,472

千问3-VL-Plus-2025-09-23

qwen3-vl-plus-2025-09-23

MU1 x 4

¥216

¥104,472

千问VL-Max-2025-08-13

qwen-vl-max-2025-08-13

MU6 x 4

¥100

¥48,356

#### 千问 Omni

**模型名称**

**模型代码**

**模型单元规格**

**小时单价（元）**

**最小计费：分钟**

**包月单价（元）**

**最小计费：天**

千问3.5-Omni-Flash

qwen3.5-omni-flash

MU9 x 1

¥51

¥24,600

模型类型：

-   Instruct - 模型部署后以**非思考模式**进行推理。
-   Thinking - 模型部署后以思考模式进行推理。
-   Instruct/Thinking - 可在模型部署时**选择是否开启思考模式**。

#### 语音合成

**CosyVoice**

**模型名称**

**模型代码**

**模型单元规格**

**小时单价（元）**

**包月单价（元）**

cosyvoice-v3-flash

cosyvoice-v3-flash

MU5

¥21

¥10,139

### 响应示例&参数

点击此处查看

命令执行完成后，获得以下结果：

```
{
    "request_id": "f2ae64f7-83cc-410c-bc0b-840443f7eb86",
    "output": {
        "deployed_model": "qwen3-8b-20260115-abcd",
        "name": "我的模型服务",
        "model_name": "qwen3-8b",
        "base_model": "qwen3-8b",
        "status": "PENDING",
        "capacity": 4,
        "ready_capacity": 0,
        "base_capacity": 4,
        "workspace_id": "llm-8v53e*******",
        "charge_type": "post_paid",
        "plan": "mu",
        "model_unit_spec": "MU1",
        "creator": "16542902******",
        "modifier": "16542902******",
        "qpm_limit": 100000000,
        "tpm_limit": 3600000,
        "mu_capacity": {
            "unified": {
                "base_capacity": 4,
                "model_unit_spec": "MU1",
                "ready_capacity": 0,
                "capacity": 4
            }
        },
        "gmt_create": "2026-01-15T10:00:00",
        "gmt_modified": "2026-01-15T10:00:00"
    }
}
```

**参数**

**类型**

**说明**

request\_id

String

本次请求的 ID。

output

Object

本次部署任务的详细信息。

deployed\_model

String

新模型的唯一标识，在发起模型调用请求时需要在 SDK 参数传入。

name

String

服务显示名称。

model\_name

String

部署任务使用的模型名称。

base\_model

String

部署任务使用的模型对应的基础模型 ID。

status

String

部署任务的状态。

-   PENDING：正在创建部署任务。
    
-   DEPLOYING：部署中。
    
-   RUNNING：部署任务正在运行，可正常处理请求。
    
-   SCALING：扩缩容中。
    
-   UPDATING：正在更新部署任务。
    
-   UPDATING\_PAUSED：更新已暂停。
    
-   SUSPENDING：暂停中（欠费）。
    
-   SUSPENDED：已暂停（欠费）。
    
-   STOPPING：停止中。
    
-   STOPPED：已停止，不再计费。
    
-   STARTING：启动中（从 STOPPED/FAILED 状态重新启动）。
    
-   FAILED：部署任务创建或更新失败。
    
-   DELETING：正在删除部署任务。
    

capacity

Number

部署任务的目标资源单元数量。

ready\_capacity

Number

已就绪并可立即处理请求的资源单元数量。

base\_capacity

Number

单实例基础容量。

workspace\_id

String

部署任务所属的业务空间 ID。

charge\_type

String

`post_paid`：后付费；`pre_paid`：预付费。

plan

String

部署任务的计费模式。

model\_unit\_spec

String

模型单元规格。

gmt\_create

String

创建部署任务的时间。

gmt\_modified

String

修改部署任务的时间。

creator

String

该部署任务创建人 UID。

modifier

String

对该部署任务进行最后一次操作的账号 UID。

fail\_reason

String

失败原因（仅 FAILED 状态返回）。

enable\_thinking

Boolean

是否开启思考模式，部分模型支持。

max\_context\_length

Number

最大上下文长度限制。

qpm\_limit

Number

QPM 限流，每分钟请求数。

tpm\_limit

Number

TPM 限流，每分钟 Token 使用量。

quantization\_precision

String

量化精度。

仅模型单元（mu）部署方式响应

mu\_capacity

Object

MU 容量详情。COUPLED 模式包含 `unified` 节点，SEPERATED 模式包含 `prefill` 和 `decode` 节点。每个节点包含：base\_capacity、model\_unit\_spec、ready\_capacity、capacity。

pre\_paid\_info

Object

预付费信息。

pre\_paid\_info.auto\_renewal

Boolean

是否自动续费

pre\_paid\_info.duration

Integer

购买时长（月）

pre\_paid\_info.auto\_renewal\_duration

Integer

自动续费时长

pre\_paid\_instance\_id

String

预付费实例 ID。

pre\_paid\_gmt\_expired

String

预付费过期时间。

仅预置吞吐量V2（ptu\_v2）部署方式响应

ptu\_capacity

Object

PTU V2 容量信息。包含字段：

-   `input_tpm_quota`（Number，输入 TPM 配额）
    
-   `output_tpm_quota`（Number，输出 TPM 配额）
    

pre\_paid\_info

Object

预付费信息。

pre\_paid\_info.auto\_renewal

Boolean

是否自动续费

pre\_paid\_info.duration

Integer

购买时长（月）

pre\_paid\_info.auto\_renewal\_duration

Integer

自动续费时长

pre\_paid\_instance\_id

String

预付费实例 ID。

pre\_paid\_gmt\_expired

String

预付费过期时间。

## 查询模型部署任务

```
GET https://dashscope.aliyuncs.com/api/v1/deployments/{deployed_model}
```

### 请求示例

```
curl "https://dashscope.aliyuncs.com/api/v1/deployments/qwen3-8b-20260115-abcd" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json'
```

### 请求参数

**参数**

**类型**

**传参方式**

**必选**

**说明**

deployed\_model

String

path

是

部署模型的唯一标识，可通过创建模型部署任务或列举模型部署任务获取。

### 响应示例&参数

点击此处查看

命令执行完成后，获得以下结果：

```
{
    "request_id": "d8b8c47b-ae32-4c41-b9f4-9a1e2b3c4d5e",
    "output": {
        "deployed_model": "qwen3-8b-20260115-abcd",
        "name": "我的模型服务",
        "model_name": "qwen3-8b",
        "base_model": "qwen3-8b",
        "status": "RUNNING",
        "capacity": 4,
        "ready_capacity": 4,
        "base_capacity": 4,
        "workspace_id": "llm-8v53e*******",
        "charge_type": "post_paid",
        "plan": "mu",
        "model_unit_spec": "MU1",
        "creator": "16542902******",
        "modifier": "16542902******",
        "qpm_limit": 100000000,
        "tpm_limit": 3600000,
        "mu_capacity": {
            "unified": {
                "base_capacity": 4,
                "model_unit_spec": "MU1",
                "ready_capacity": 4,
                "capacity": 4
            }
        },
        "gmt_create": "2026-01-15T10:00:00",
        "gmt_modified": "2026-01-15T10:30:00"
    }
}
```

#### 响应参数

响应参数与创建模型部署任务的响应参数一致，请参考创建模型部署任务的响应参数说明。

## 列举模型部署任务

```
GET https://dashscope.aliyuncs.com/api/v1/deployments
```

### 请求示例

```
curl "https://dashscope.aliyuncs.com/api/v1/deployments?page_no=1&page_size=10" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json'
```

### 请求参数

**参数**

**类型**

**传参方式**

**必选**

**说明**

age\_no

Number

query

否

页码，默认值为1。

page\_size

Number

query

否

页大小，默认为10，最大值为100。

### 响应示例&参数

点击此处查看

命令执行完成后，获得以下结果：

```
{
    "request_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "output": {
        "page_no": 1,
        "page_size": 10,
        "total": 2,
        "deployments": [
            {
                "deployed_model": "qwen3-8b-20260115-abcd",
                "name": "我的模型服务",
                "model_name": "qwen3-8b",
                "base_model": "qwen3-8b",
                "status": "RUNNING",
                "capacity": 4,
                "ready_capacity": 4,
                "base_capacity": 4,
                "workspace_id": "llm-8v53e*******",
                "charge_type": "post_paid",
                "plan": "mu",
                "model_unit_spec": "MU1",
                "creator": "16542902******",
                "modifier": "16542902******",
                "qpm_limit": 100000000,
                "tpm_limit": 3600000,
                "mu_capacity": {
                    "unified": {
                        "base_capacity": 4,
                        "model_unit_spec": "MU1",
                        "ready_capacity": 4,
                        "capacity": 4
                    }
                },
                "gmt_create": "2026-01-15T10:00:00",
                "gmt_modified": "2026-01-15T10:30:00"
            }
        ]
    }
}
```

#### 响应参数

参数

类型

说明

page\_no

Number

查询页码。

page\_size

Number

查询页大小。

total

Long

满足查询条件的所有部署任务总数。

deployments

Array

部署任务列表。每个元素的字段与创建模型部署任务的响应参数一致，请参考创建模型部署任务的响应参数说明。

## 更新模型部署任务

**说明**更新模型部署任务即对部署服务进行扩缩容操作。仅当服务状态为 RUNNING 或 SCALING 时可调用，其他状态调用将返回 OperationDenied 错误。

```
PUT https://dashscope.aliyuncs.com/api/v1/deployments/{deployed_model}/scale
```

### 请求示例

COUPLED 模式扩缩容：

```
curl -X PUT "https://dashscope.aliyuncs.com/api/v1/deployments/qwen3-8b-20260115-abcd/scale" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json' \
    --data '{
    "capacity": 8
}'
```

PD 分离模式扩缩容：

```
curl -X PUT "https://dashscope.aliyuncs.com/api/v1/deployments/qwen3-8b-20260115-abcd/scale" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json' \
    --data '{
    "prefill_capacity": 4,
    "decode_capacity": 8
}'
```

### 请求参数

参数

类型

传参方式

必选

说明

deployed\_model

String

path

是

部署模型的唯一标识。

capacity

Number

body

条件必填

扩缩容的目标资源单元数量。COUPLED 模式（非 PD 分离）时必填，必须是 `base_capacity` 的整数倍。

prefill\_capacity

Number

body

条件必填

Prefill 目标容量。PD 分离模式时必填。

decode\_capacity

Number

body

条件必填

Decode 目标容量。PD 分离模式时必填。

ptu\_capacity

Object

body

条件必填

PTU V2 容量信息。包含字段：

-   `input_tpm_quota`（Number，输入 TPM 配额）
    
-   `output_tpm_quota`（Number，输出 TPM 配额）
    

### 响应示例&参数

点击此处查看

命令执行完成后，获得以下结果：

```
{
    "request_id": "e5f6a7b8-c9d0-1234-5678-abcdef012345",
    "output": {
        "deployed_model": "qwen3-8b-20260115-abcd",
        "name": "我的模型服务",
        "model_name": "qwen3-8b",
        "base_model": "qwen3-8b",
        "status": "SCALING",
        "capacity": 8,
        "ready_capacity": 4,
        "base_capacity": 4,
        "workspace_id": "llm-8v53e*******",
        "charge_type": "post_paid",
        "plan": "mu",
        "model_unit_spec": "MU1",
        "creator": "16542902******",
        "modifier": "16542902******",
        "qpm_limit": 100000000,
        "tpm_limit": 3600000,
        "mu_capacity": {
            "unified": {
                "base_capacity": 4,
                "model_unit_spec": "MU1",
                "ready_capacity": 4,
                "capacity": 8
            }
        },
        "gmt_create": "2026-01-15T10:00:00",
        "gmt_modified": "2026-01-15T11:00:00"
    }
}
```

#### 响应参数

响应参数与创建模型部署任务的响应参数一致，请参考创建模型部署任务的响应参数说明。

## 停止部署的模型

**说明**仅模型单元（mu）部署方式支持停止服务。仅当服务状态为 RUNNING 或 SCALING 时可调用。cu、ptu\_v2、lora 方式调用此接口将返回 UnsupportedOperation 错误。停止后服务不再计费，可通过API 详情 API 重新启动。

```
POST https://dashscope.aliyuncs.com/api/v1/deployments/{deployed_model}/stop
```

### 请求示例

```
curl -X POST "https://dashscope.aliyuncs.com/api/v1/deployments/qwen3-8b-20260115-abcd/stop" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json'
```

### 请求参数

**参数**

**类型**

**传参方式**

**必选**

**说明**

deployed\_model

String

path

是

部署模型的唯一标识。

### 响应示例&参数

点击此处查看

命令执行完成后，获得以下结果：

```
{
    "request_id": "f1a2b3c4-d5e6-7890-abcd-ef1234567890",
    "output": {
        "deployed_model": "qwen3-8b-20260115-abcd",
        "name": "我的模型服务",
        "model_name": "qwen3-8b",
        "base_model": "qwen3-8b",
        "status": "STOPPING",
        "capacity": 4,
        "ready_capacity": 4,
        "base_capacity": 4,
        "workspace_id": "llm-8v53e*******",
        "charge_type": "post_paid",
        "plan": "mu",
        "model_unit_spec": "MU1",
        "creator": "16542902******",
        "modifier": "16542902******",
        "qpm_limit": 100000000,
        "tpm_limit": 3600000,
        "mu_capacity": {
            "unified": {
                "base_capacity": 4,
                "model_unit_spec": "MU1",
                "ready_capacity": 4,
                "capacity": 4
            }
        },
        "gmt_create": "2026-01-15T10:00:00",
        "gmt_modified": "2026-01-15T12:00:00"
    }
}
```

#### 响应参数

响应参数与创建模型部署任务的响应参数一致，请参考创建模型部署任务的响应参数说明。

## 重新启动部署的模型

```
POST https://dashscope.aliyuncs.com/api/v1/deployments/{deployed_model}/start
```

### 请求示例

```
curl -X POST "https://dashscope.aliyuncs.com/api/v1/deployments/qwen3-8b-20260115-abcd/start" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json'
```

### 请求参数

**参数**

**类型**

**传参方式**

**必选**

**说明**

deployed\_model

String

path

是

部署模型的唯一标识，可通过创建模型部署任务或列举模型部署任务获取。

### 响应示例&参数

点击此处查看

命令执行完成后，获得以下结果：

> 启动后状态为 `STARTING`，模型可调用后变为 `RUNNING`

```
{
  "request_id": "xxx-xxx-xxx",
  "output": {
    "deployed_model": "qwen-7b-chat-ft-20240101-abcd",
    "model_name": "qwen-7b-chat-ft",
    "base_model": "qwen-7b-chat",
    "status": "STARTING",
    "capacity": 1,
    "ready_capacity": 0,
    "base_capacity": 1,
    "plan": "mu",
    "model_unit_spec": "MU5",
    "workspace_id": "workspace-xxx",
    "charge_type": "post_paid",
    "creator": "user123",
    "modifier": "user123",
    "qpm_limit": 100000000,
    "tpm_limit": 3600000,
    "mu_capacity": {
      "unified": {
        "base_capacity": 1,
        "model_unit_spec": "",
        "ready_capacity": 0,
        "capacity": 1
      }
    },
    "gmt_create": "2024-01-01T10:00:00",
    "gmt_modified": "2024-01-01T13:00:00"
  }
}
```

#### 响应参数

响应参数与创建模型部署任务的响应参数一致，请参考创建模型部署任务的响应参数说明。

## 删除模型部署任务

**说明**仅当服务状态为 STOPPED 或 FAILED 时可调用删除。RUNNING 状态的服务需先调用API 详情接口。

```
DELETE https://dashscope.aliyuncs.com/api/v1/deployments/{deployed_model}
```

### 请求示例

```
curl -X DELETE "https://dashscope.aliyuncs.com/api/v1/deployments/qwen3-8b-20260115-abcd" \
    --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    --header 'Content-Type: application/json'
```

### 请求参数

**参数**

**类型**

**传参方式**

**必选**

**说明**

deployed\_model

String

path

是

部署模型的唯一标识。

### 响应示例&参数

点击此处查看

命令执行完成后，获得以下结果：

```
{
    "request_id": "g1h2i3j4-k5l6-7890-mnop-qr1234567890",
    "output": {
        "deployed_model": "qwen3-8b-20260115-abcd",
        "name": "我的模型服务",
        "model_name": "qwen3-8b",
        "base_model": "qwen3-8b",
        "status": "DELETING",
        "capacity": 4,
        "ready_capacity": 0,
        "base_capacity": 4,
        "workspace_id": "llm-8v53e*******",
        "charge_type": "post_paid",
        "plan": "mu",
        "model_unit_spec": "MU1",
        "creator": "16542902******",
        "modifier": "16542902******",
        "gmt_create": "2026-01-15T10:00:00",
        "gmt_modified": "2026-01-15T14:00:00"
    }
}
```

#### 响应参数

响应参数与创建模型部署任务的响应参数一致，请参考创建模型部署任务的响应参数说明。

## 异常响应

```
{
    "request_id": "6fec0a3f-a1df-4f89-8c8f-33cb0db9f5b0",
    "code": "InvalidParameter",
    "message": "capacity is required when template_type is COUPLED"
}
```

### 响应参数

**参数**

**类型**

**说明**

request\_id

String

本次请求的系统生成 ID。

code

String

错误码，标识错误类型。

message

String

错误详情，用于问题排查。

### 常见错误

**错误原因**

**说明**

`InvalidParameter`

参数错误，如缺少必填参数、参数值不合法、template\_id 和 deploy\_spec 同时传入等。

`AccessDenied`

权限不足或资源不存在。

`OperationDenied`

当前状态不允许执行该操作，如在非 RUNNING 状态下执行扩缩容，或在非 STOPPED/FAILED 状态下删除。

`UnsupportedOperation`

当前部署方案不支持该操作，如 cu 方式不支持停止服务。

`StockLimit`

资源库存不足，无法完成扩容或部署。

`InternalError`

内部错误。

`NotFound`

指定的部署任务不存在。

`Conflict`

操作冲突，如服务正在进行其他操作。
