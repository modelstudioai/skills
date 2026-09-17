# 部署模型管理

部署模型管理接口， 适用于文本、图像、视频、语音等所有模型类型 。支持查询部署状态、获取可部署模型列表与部署列表、修改限流、扩缩容及删除部署。

## 适用范围

-   **适用地域**：本文描述的功能仅在**华北2（北京）地域**可用，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。
-   已成功[获取 API Key](raw/model-api-reference/preparations/get-api-key.md)并[配置到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
-   已阅读[模型部署](raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)和[使用 API 进行模型部署](raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)，了解模型部署的基本步骤。

**说明**DTU 计费模式的部署暂不支持通过本组 API 创建与管理，请在控制台操作，详见

[DTU 独占算力部署](raw/model-user-guide/model-deployment-index/dtu-model-deployment.md)。

## 查询部署模型状态

查询指定部署模型的详细信息和运行状态。可轮询此接口，当任务状态`status`变为**RUNNING**时，表示模型已部署成功。

**说明**模型部署过程预计需要 **5～10分钟**。

### 地址

```
GET https://dashscope.aliyuncs.com/api/v1/deployments/{deployed_model}
```

### 请求示例

通过以下命令可以查询指定专属服务的详细信息：

```
curl "https://dashscope.aliyuncs.com/api/v1/deployments/qwen-plus-202305099980-fac9-sample" \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
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

部署模型的唯一标识，可通过[部署模型](raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)或查询部署模型列表接口获取。

### 响应示例

关注`status`字段。当状态变为 **RUNNING** 时，表示模型已部署成功，可以开始调用。

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

### 响应参数

**字段**

**类型**

**描述**

request\_id

String

请求的唯一标识符。

output

Object

任务详情。

output.deployed\_model

String

部署模型的唯一标识。用于查询模型部署状态和调用模型。

output.model\_name

String

模型标识名。

output.base\_model

String

使用的基准模型。

output.status

String

部署状态：

-   PENDING：正在创建部署任务。
    
-   RUNNING：部署任务正在运行，模型可正常处理请求。
    
-   UPDATING：变配中。
    
-   UPDATING\_FAILED：变配失败。
    
-   DELETING：正在删除部署任务。
    
-   DELETED：已删除。
    
-   FAILED：部署任务创建或更新失败。
    
-   STOPPED：部署任务已停止，不会被计费。
    
-   ARREARS\_DOWN：欠费停服。
    
-   ARREARS\_RECOVERING：欠费停服恢复中。
    
-   OFFLINING：服务下线中。
    

output.base\_capacity

Number

基础资源单元数量。

output.capacity

Number

当前资源单元数量。

output.ready\_capacity

Number

已就绪的资源单元数量。

output.workspace\_id

String

阿里云百炼 API Key 所属的业务空间 ID。请参见[获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)。

output.charge\_type

String

付费模式。post\_paid 表示后付费。

output.gmt\_create

String

部署任务创建时间。

output.gmt\_modified

String

部署任务更新时间。

output.creator

String

创建人的阿里云账号 ID。

output.modifier

String

修改人的阿里云账号 ID。

output.plan

String

部署方式。

## 获取可部署模型列表

获取百炼平台上**有资格部署的候选模型**清单，即哪些模型可以用来创建部署。

### 地址

```
GET https://dashscope.aliyuncs.com/api/v1/deployments/models
```

### 请求示例

通过下面的命令可以查询支持部署的模型，推荐使用`version=v1.0`获取包含部署方案和模板信息的完整响应。

```
curl "https://dashscope.aliyuncs.com/api/v1/deployments/models?page_no=1&page_size=100&version=v1.0&model_source=base" \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header 'Content-Type: application/json'
```

查询用户调优模型：

```
curl "https://dashscope.aliyuncs.com/api/v1/deployments/models?page_no=1&page_size=100&version=v1.0&model_source=custom" \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header 'Content-Type: application/json'
```

### 请求参数

**参数**

**类型**

**必选**

**说明**

page\_no

Number

否

页码，默认值为1。

page\_size

Number

否

页大小，默认为50，最大值为100，最小值为1。

model\_source

String

否

模型来源。`base`表示系统模型（默认），`custom`表示用户调优模型。

version

String

否

API 版本，推荐使用`v1.0`。使用`v1.0`时，响应中将包含完整的部署方案和模板信息。

### 响应示例

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

### 响应参数

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

部署方案类型：`mu`（模型单元）、`cu`（算力单元）、`ptu`（预置吞吐量）、`lora`（LoRA共享部署）。

models\[\].plans\[\].templates

Array

部署模板列表（`plan=mu`时返回）。

models\[\].plans\[\].templates\[\].template\_id

String

模板 ID，在[创建模型部署任务](https://help.aliyun.com/zh/model-studio/model-deployment-api)时作为`deploy_spec`参数传入。

models\[\].plans\[\].templates\[\].template\_name

String

模板显示名称。

models\[\].plans\[\].templates\[\].template\_type

String

模板类型：`COUPLED`（非 PD 分离，使用`capacity`参数）、`SEPERATED`（PD 分离，使用`prefill_capacity`和`decode_capacity`参数）。

models\[\].plans\[\].templates\[\].template\_version

String

模板版本。

models\[\].plans\[\].templates\[\].template\_desc

String

模板描述。

models\[\].plans\[\].templates\[\].roles

Object

节点角色配置。COUPLED 模式包含`unified`节点，SEPERATED 模式包含`prefill`和`decode`节点。

models\[\].plans\[\].templates\[\].roles.{role}.model\_unit\_spec

String

模型单元规格。

models\[\].plans\[\].templates\[\].roles.{role}.capacity\_unit\_per\_instance

Number

单实例容量单元数，即 base\_capacity。创建部署时`capacity`必须是该值的整数倍。

page\_no

Number

查询页码。

page\_size

Number

查询页大小。

total

Long

满足查询条件的所有模型个数。

## 获取已部署模型列表

获取**已创建的部署实例**列表，即当前工作空间下实际运行或已部署的模型服务。

### 地址

```
GET https://dashscope.aliyuncs.com/api/v1/deployments
```

### 请求示例

通过以下命令可以获取专属服务列表：

```
curl "https://dashscope.aliyuncs.com/api/v1/deployments?page_no=1&page_size=100" \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
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

页大小，默认为50，最大值为200，最小值为1。

### 响应示例

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
        "modifier": "175805416***"
      }
    ]
  }
}
```

### 响应参数

**字段**

**类型**

**描述**

request\_id

String

本次请求的系统唯一码。

output.page\_no

Number

当前页码。

output.page\_size

Number

每页数量。

output.total

Number

部署总数。

output.deployments

Array

部署模型列表，每个元素的字段与[查询部署模型状态](https://help.aliyun.com/zh/model-studio/get-deployment-api#09893a6ec96xp)的 output 字段一致。

## 修改部署模型的限流

修改指定部署模型的 RPM（每分钟请求数）和 TPM（每分钟 Token 数）限流设置。

**说明**仅模型单元部署方式的[部分模型](raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)支持修改设置 rpm 和 tpm。

### 地址

```
PUT https://dashscope.aliyuncs.com/api/v1/deployments/{deployed_model}/update
```

### 请求示例

通过以下命令可以修改指定部署的限流设置：

```
curl -X PUT "https://dashscope.aliyuncs.com/api/v1/deployments/qwen-plus-2025-12-01-b6d61c71/update" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "rpm_limit": 1000,
    "tpm_limit": 200
}'
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

部署模型的唯一标识，可通过[部署模型](raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)或查询部署模型列表接口获取。

rpm\_limit

Number

body

至少填写一个参数

Requests per minute，每分钟请求数。

tpm\_limit

Number

body

Token per minute，每分钟 Token 使用量。

### 响应示例

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

### 响应参数

除[查询部署模型状态](https://help.aliyun.com/zh/model-studio/get-deployment-api#09893a6ec96xp)中列出的基础字段外，还可能包含以下字段：

**字段**

**类型**

**描述**

output.plan

String

部署方式。

output.model\_unit\_spec

String

模型单元部署模板，如 MU1。

output.enable\_thinking

Boolean

是否开启思考模式。

output.max\_context\_length

Number

最大上下文长度。

output.rpm\_limit

Number

每分钟请求数限制。

output.tpm\_limit

Number

每分钟 Token 数限制。

## 扩缩容部署服务

通过更新操作调整专属服务使用的资源单元数量。

### 地址

```
PUT https://dashscope.aliyuncs.com/api/v1/deployments/{deployed_model}/scale
```

### 请求示例

通过以下命令可以将指定的服务进行扩缩容：

```
curl --request PUT "https://dashscope.aliyuncs.com/api/v1/deployments/emo-35b3f106-sample01/scale" \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header 'Content-Type: application/json' \
    --data '{
                "capacity":2
            }'
```

### 请求参数

**参数**

**类型**

**必选**

**说明**

deployed\_model

String

是

部署模型的唯一标识（path 参数），可通过[部署模型](raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)或查询部署模型列表接口获取。

capacity

Integer

条件必选

仅`"plan": "mu"`时生效。具体支持情况请参考[模型单元部署的功能支持情况](raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)。

更新后模型所使用的资源单元数量，**必须**是`base_capacity`的整数倍。

ptu\_capacity

Object

条件必选

仅`"plan": "ptu"`时生效。具体支持情况请参考[PTU部署的功能支持情况](raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)。

样例：`"ptu_capacity": { "input_tpm": 10000, "output_tpm": 1000 }`。

ptu\_capacity.input\_tpm

Number

条件必选

仅`"plan": "ptu"`时生效。具体支持情况请参考[PTU部署的功能支持情况](raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)。

部署的模型每分钟支持的最大输入 Token 量（input tokens per minute）。所有模型支持。

ptu\_capacity.output\_tpm

Number

条件必选

仅`"plan": "ptu"`时生效。具体支持情况请参考[PTU部署的功能支持情况](raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)。

部署的模型每分钟支持的最大输出 Token 量（output tokens per minute）。所有模型支持。

ptu\_capacity.thinking\_output\_tpm

Number

否

仅`"plan": "ptu"`时生效。具体支持情况请参考[PTU部署的功能支持情况](raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)。

部署的模型每分钟支持的预置思考最大输出 Token 量（thinking output tokens per minute）。部分模型支持。

### 响应示例

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

### 响应参数

响应字段与[查询部署模型状态](https://help.aliyun.com/zh/model-studio/get-deployment-api#09893a6ec96xp)一致，请参考查询部署模型状态的响应参数。

## 删除部署

删除指定的部署模型，释放对应的计算资源。

**重要**执行该操作后，模型部署服务将立即下线且**不可恢复**：

1.  模型将无法调用。
2.  部署服务停止计费。

### 地址

```
DELETE https://dashscope.aliyuncs.com/api/v1/deployments/{deployed_model}
```

### 请求示例

通过以下命令可以删除指定的部署任务。

```
curl --request DELETE "https://dashscope.aliyuncs.com/api/v1/deployments/emo-35b3f106-sample01" \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
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

部署模型的唯一标识，可通过[部署模型](raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)或查询部署模型列表接口获取。

### 响应示例

关注`status`字段。当状态变为 **DELETING** 时，表示正在删除部署任务。

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

之后，再调用[查询部署模型状态](https://help.aliyun.com/zh/model-studio/get-deployment-api#09893a6ec96xp)进行验证。若返回如下内容，说明部署的服务已不存在，删除成功。

```
{
    "request_id": "eb619064-0c4f-4d29-aa49-xxxxxx",
    "message": "Not found.",
    "code": "NotFound"
}
```

### 响应参数

响应字段与[查询部署模型状态](https://help.aliyun.com/zh/model-studio/get-deployment-api#09893a6ec96xp)一致，请参考查询部署模型状态的响应参数。

## 异常响应

### 响应示例

```
{
    "request_id": "ca218d57-b91b-46b2-bd35-c41c6287bcf4",
    "message": "Model: qwen-plus-20230703-cx7f not found!",
    "code": "NotFound"
}
```

### 响应参数

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
