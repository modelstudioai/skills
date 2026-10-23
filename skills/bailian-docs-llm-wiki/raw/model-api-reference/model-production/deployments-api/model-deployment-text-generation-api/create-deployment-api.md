# 文本生成-部署模型

将训练好的文本模型发布为在线 API 服务。

## 适用范围

-   **适用地域**：模型部署 API 的开放地域因部署方式而异——模型单元（MU）与 DTU 独占算力部署支持**华北2（北京）**；预置吞吐（PTU）等部署方式支持**北京与新加坡**地域。如您使用的地域未开放对应部署方式，请通过该地域的百炼控制台完成模型部署操作。
-   **开通账号权限**：若使用[阿里云子账号](raw/model-user-guide/security-and-compliance/permission-management-overview.md)（[RAM用户](https://help.aliyun.com/zh/ram/user-guide/overview-of-ram-users)），需要为子账号授予模型调用、训练和部署[权限](https://help.aliyun.com/zh/model-studio/use-workspace)。
-   **配置环境变量**：已成功[获取 API Key](raw/model-api-reference/preparations/get-api-key.md)，并[配置到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
-   **阅读部署文档**：建议先阅读[专属部署概述](raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)和[使用 API 创建模型部署任务](raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)，了解模型部署的使用方法和基本步骤。

## 部署模型

#### 华北2（北京）

`POST https://dashscope.aliyuncs.com/api/v1/deployments`

#### 新加坡

`POST https://dashscope-intl.aliyuncs.com/api/v1/deployments`

> 请求域名因地域而异：北京地域使用 `dashscope.aliyuncs.com`，新加坡地域使用 `dashscope-intl.aliyuncs.com`；业务空间专属域名（`{WorkspaceId}.{region}.maas.aliyuncs.com`）各地域均可用。各地域完整域名信息请参见[各地域接入信息](https://help.aliyun.com/zh/model-studio/regions#h2_cc92e61c)。

> Windows CMD 请将`$DASHSCOPE_API_KEY`替换为`%DASHSCOPE_API_KEY%`，PowerShell请替换为 `$env:DASHSCOPE_API_KEY`

### 请求参数

##### 请求头（Headers）

**参数**

**类型**

**必选**

**说明**

Content-Type

String

是

固定值：`application/json`。

Authorization

String

是

API Key 鉴权，格式为 `Bearer sk-xxxx`。

##### 请求体（Request Body）

请求体参数因部署方式（plan）而异，各计费方式的完整请求体参数与部署示例如下：

#### 按DTU独占算力计费

DTU 独占算力部署为预付费（按月）计费，按输入/输出 TPM 购买容量，独占 GPU 资源，是模型单元（MU）的继任方案，新购独占部署优先选择。使用前需在控制台开通 DTU 功能并申请资源额度，详见[DTU 独占算力部署](raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)。

> DTU 部署的 API 请求需使用部署所在业务空间的 `maas.aliyuncs.com` 域名（例如 `ws-vxxx.cn-beijing.maas.aliyuncs.com`）和该业务空间的 API Key；`sku_code`、`template_code` 与容量范围通过可部署模型列表接口 `plan=dtu` 查询。完整参数、扩缩容、修改限流与更新模型等接口详见[模型部署 API 参考](raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)。

**参数**

**类型**

**必选**

**说明**

model\_name

String

是

待部署的模型名称，对应[我的模型](https://bailian.console.aliyun.com/model/custom)中的模型 ID。也可通过[创建训练任务](raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)接口的输出获取。

plan

String

是

部署方案，决定计费方式：`dtu`（DTU 独占算力）、`mu`（模型单元）、`cu`（算力单元）、`ptu_v2`（预置吞吐量 V2）、`lora`（LoRA 共享部署，按 Token 用量计费）。

display\_name

String

是

服务展示名称，最多 50 个字符（其他部署方式使用 `name`）。

suffix

String

否

部署标识后缀，最多 24 个字符；生成的完整部署标识不超过 100 个字符。省略时自动生成。

sku\_code

String

是

当前模型可用的预付费 SKU，通过可部署模型列表接口 `plan=dtu` 查询。

template\_code

String

是

与模型和 SKU 匹配的部署模板，与 `sku_code` 同为查询所得。

charge\_type

String

是

付费方式，DTU 固定传 `pre_paid`（预付费）。

dtu\_capacity

Object

是

DTU 购买容量，须同时提供 `input_tpm` 与 `output_tpm`，购买范围与步长规则见[模型部署 API 参考](raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)。

dtu\_capacity.input\_tpm

Integer

是

购买的输入 TPM（tokens/min），非负整数，最大值为 2147483647，须为查询所得步长的整数倍。

dtu\_capacity.output\_tpm

Integer

是

购买的输出 TPM（tokens/min），非负整数，最大值为 2147483647，与输入 TPM 同倍数。

pre\_paid\_info

Object

是

预付费购买及自动续费设置。包含字段：`pricing_cycle`（固定传 `Month`）、`duration`（购买时长/月）、`auto_renewal`（是否自动续费）、`auto_renewal_duration`（开启自动续费时的续费时长/月）。

```
curl "https://ws-vxxx.cn-beijing.maas.aliyuncs.com/api/v1/deployments" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model_name": "your-supported-model",
    "display_name": "业务模型服务",
    "suffix": "production",
    "plan": "dtu",
    "sku_code": "your-prepaid-sku",
    "template_code": "your-template",
    "charge_type": "pre_paid",
    "pre_paid_info": {
        "pricing_cycle": "Month",
        "duration": 1,
        "auto_renewal": false
    },
    "dtu_capacity": {"input_tpm": 10000, "output_tpm": 10000}
}'
```

#### 按模型单元计费

选择按模型单元计费，计费模式为按模型单元的使用时长收费，适用于模型调优后的大规模推理业务，资源专属，性能和成本灵活可调。

> 执行以下部署命令后，即便您还没有调用模型，模型部署服务仍将在部署成功后开始计费。建议您先确认服务计费规则，再执行部署命令。

**参数**

**类型**

**必选**

**说明**

model\_name

String

是

待部署的模型名称，对应[我的模型](https://bailian.console.aliyun.com/model/custom)中的模型 ID。也可通过[创建训练任务](raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)接口的输出获取。

plan

String

是

部署方案，决定计费方式：`dtu`（DTU 独占算力）、`mu`（模型单元）、`cu`（算力单元）、`ptu_v2`（预置吞吐量 V2）、`lora`（LoRA 共享部署，按 Token 用量计费）。

name

String

否

模型的控制台显示名称。如果不传该参数，将自动使用 `model_name` 的值作为部署名称。

suffix

String

否

模型部署后将生成新的模型名称，suffix 用于指定新模型名称的后缀，最大长度为 8 个字符且需全局唯一。每个模型在首次部署时可以不指定后缀，多次部署同一模型时必须设置。

template\_id

String

条件必填

部署模板 ID，对应可部署模型列表接口返回的 `template_id`。`plan` 为 `mu` 时必须填写，推荐使用此参数指定模型单元规格（如 `MU1`）。

deploy\_spec（旧）

String

否

模型单元规格，已废弃，请改用 `template_id`。

capacity

Integer

条件必填

部署使用的资源单元数量，需为 `base_capacity` 的整数倍。不同规格的取值约束不同，例如 `MU2` 必须为 8 的倍数，`MU5` 可填 1。

charge\_type

String

否

付费方式：`post_paid`（后付费，默认）、`pre_paid`（预付费）。

enable\_thinking

Boolean

否

是否启用思考模式。部分模型支持，可设置为 `true` 或 `false`。

max\_context\_length

Number

否

最大上下文长度。部分模型支持。样例：`"max_context_length": 131072`。

rpm\_limit

Number

否

每分钟请求数（requests per minute）限流。部分模型支持。

tpm\_limit

Number

否

每分钟 Token 使用量（tokens per minute）限流。部分模型支持。

```
curl "https://dashscope.aliyuncs.com/api/v1/deployments" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "name": "my_qwen_plus",
    "model_name": "qwen-plus-2025-12-01",
    "plan": "mu",
    "template_id": "MU1",
    "enable_thinking": true,
    "capacity": 4,
    "charge_type": "post_paid",
    "max_context_length": 10000,
    "rpm_limit": 500,
    "tpm_limit": 1000
}'
```

#### 按Token用量计费

选择按 Token 用量计费，适用于高性价比诉求且对并发和延迟要求不高的场景。该模式价格优势最高，吞吐/并发和生成速度均由平台预置，用户不可调。

**参数**

**类型**

**必选**

**说明**

model\_name

String

是

待部署的模型名称，对应[我的模型](https://bailian.console.aliyun.com/model/custom)中的模型 ID。也可通过[创建训练任务](raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)接口的输出获取。

plan

String

是

部署方案，决定计费方式：`dtu`（DTU 独占算力）、`mu`（模型单元）、`cu`（算力单元）、`ptu_v2`（预置吞吐量 V2）、`lora`（LoRA 共享部署，按 Token 用量计费）。

name

String

否

模型的控制台显示名称。如果不传该参数，将自动使用 `model_name` 的值作为部署名称。

suffix

String

否

模型部署后将生成新的模型名称，suffix 用于指定新模型名称的后缀，最大长度为 8 个字符且需全局唯一。

capacity

Integer

条件必填

按 Token 用量计费时该参数设置无效但必须填写，固定传 1。

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

#### 按预置吞吐计费

按预置吞吐计费模式按预置吞吐的使用时长收费，适用于追求稳定吞吐保障和高并发低延迟、且流量可预估的场景。该模式下，吞吐/并发和生成速度均为平台预置，用户不可调。

> 执行以下部署命令后，即便您还没有调用模型，模型部署服务仍将在部署成功后开始计费。建议您先确认服务计费规则，再执行部署命令。

**参数**

**类型**

**必选**

**说明**

model\_name

String

是

待部署的模型名称，对应[我的模型](https://bailian.console.aliyun.com/model/custom)中的模型 ID。也可通过[创建训练任务](raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)接口的输出获取。

plan

String

是

部署方案，决定计费方式：`dtu`（DTU 独占算力）、`mu`（模型单元）、`cu`（算力单元）、`ptu_v2`（预置吞吐量 V2）、`lora`（LoRA 共享部署，按 Token 用量计费）。

name

String

否

模型的控制台显示名称。如果不传该参数，将自动使用 `model_name` 的值作为部署名称。

suffix

String

否

模型部署后将生成新的模型名称，suffix 用于指定新模型名称的后缀，最大长度为 8 个字符且需全局唯一。

ptu\_capacity

Object

否

预置吞吐量配置，包含 `input_tpm`（每分钟最大输入 Token 量）、`output_tpm`（每分钟最大输出 Token 量），部分模型另支持 `thinking_output_tpm`（预置思考最大输出 Token 量）。如果不填写该参数，将默认按照 `10,000 input_tpm` 和 `1,000 output_tpm` 进行设置。

```
curl "https://dashscope.aliyuncs.com/api/v1/deployments" \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "name": "my_qwen_flash",
    "model_name": "qwen-flash-2025-07-28",
    "plan": "ptu_v2",
    "ptu_capacity": {
        "input_tpm": 10000,
        "output_tpm": 1000
    }
}'
```

## 部署排障与性能调优

### max-num-seqs 参数不可配置

百炼模型部署在**按预置吞吐计费**和**按模型单元计费**两种计费方式下，吞吐、并发和生成速度均为平台预置，不支持直接调整 vLLM 内部的 `max-num-seqs` 等推理引擎参数，本接口的请求参数中也不存在该参数。

**按模型单元计费**方式下，可通过选择**模型单元类型**（对应请求参数 `template_id`）和调整**部署副本数**（对应请求参数 `capacity`）间接控制吞吐能力。

### 部署模板与资源隔离

当前部署模板仅支持单机部署（**单机部署-增强型通用推理**），不支持多卡实例隔离。如需资源隔离，请使用**按模型单元计费**方式，该方式下算力资源为业务专属。

### 限流错误处理

当并发请求超出限流阈值时，接口返回 HTTP `429`，错误码为 `Throttling.RateQuota`，错误信息为 `Requests rate limit exceeded, please try again later`。处理方式：

-   **按预置吞吐计费**：调整 `ptu_capacity` 中的 `input_tpm` 和 `output_tpm`（控制台对应 **Input kTPM** 和 **Output kTPM**），或降低请求频率。该方式下溢出策略可选**自动溢出**（切换为按量付费）或**仅使用 PTU 容量**（超出容量的请求直接返回 `429`）。
-   **按模型单元计费**：调整 `rpm_limit` 和 `tpm_limit`，或降低请求频率。

### 上下文长度调优

**按模型单元计费**方式下可通过请求参数 `max_context_length` 配置**最长上下文**，取值范围 1～262144（实际上限取决于所部署模型的能力）。该参数限制单次请求的上下文规模，从而限制单请求的内存占用，可降低 OOM 风险。

处理大量图片任务时，请结合图片尺寸和单请求图片数量设置该参数。

### 响应参数

**参数**

**类型**

**说明**

request\_id

String

请求的唯一标识符。

output

Object

任务详情。

output.deployed\_model

String

部署模型的唯一标识。用于查询模型部署状态和调用模型。

output.name

String

部署的显示名称。

output.model\_name

String

模型标识名。

output.base\_model

String

使用的基准模型。

output.status

String

部署状态：`PENDING`（正在创建）、`DEPLOYING`（部署中）、`WAIT_PRE_PAID_BILLING_TO_DEPLOYING`（创建处于预付费订单处理阶段，DTU）、`WAIT_PRE_PAID_BILLING_TO_SCALING`（扩缩容处于预付费订单处理阶段，DTU）、`UPDATING`（正在更新）、`RUNNING`（运行中，可正常处理请求）、`SCALING`（扩缩容中）、`STOPPED`（已停止，不计费）、`DELETING`（删除中）、`FAILED`（创建或更新失败）。

output.workspace\_id

String

API Key 所属业务空间 ID。请参见[获取 Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)。

output.charge\_type

String

付费模式：`post_paid`（后付费）、`pre_paid`（预付费）。

output.creator

String

创建人的阿里云账号 ID。

output.modifier

String

修改人的阿里云账号 ID。

output.plan

String

部署方式。

output.gmt\_create

String

部署任务创建时间。

output.gmt\_modified

String

部署任务更新时间。

仅模型单元（mu）部署方式返回

output.base\_capacity

Number

基础模型运行所需的最小资源单元数量。

output.ready\_capacity

Number

已就绪并可立即处理请求的资源单元数量。

output.capacity

Number

部署使用的资源单元数量。

output.model\_unit\_spec

String

模型单元规格。

output.enable\_thinking

Boolean

是否开启思考模式。

output.max\_context\_length

Number

最大上下文长度限制。

output.rpm\_limit

Number

每分钟请求数。

output.tpm\_limit

Number

每分钟 Token 使用量。

仅预置吞吐（ptu\_v2）部署方式返回

output.ptu\_capacity

Object

预置吞吐量配置，包含 `input_tpm`（每分钟最大输入 Token 量）、`output_tpm`（每分钟最大输出 Token 量），部分模型另支持 `thinking_output_tpm`（预置思考最大输出 Token 量）。

仅 DTU（dtu）部署方式返回

output.dtu\_capacity

Object

购买的输入/输出 TPM 容量，包含 `input_tpm` 与 `output_tpm`。

output.pre\_paid\_info

Object

预付费及自动续费信息。

DTU 完整响应字段说明见[模型部署 API 参考](raw/model-api-reference/model-production/deployments-api/model-deployment-api-reference.md)

调用失败时返回

code

String

错误码。调用失败时返回。

message

String

错误详情描述。调用失败时返回。

#### 成功响应示例

重点关注：`output.deployed_model`（部署模型的唯一标识）、`output.status`（部署状态）。

```
{
    "request_id": "f2ae64f7-83cc-410c-bc0b-840443f7eb86",
    "output": {
        "deployed_model": "qwen-plus-2025-12-01-mu-xxxx",
        "gmt_create": "2025-06-17T11:00:38.68",
        "gmt_modified": "2025-06-17T11:00:38.68",
        "status": "PENDING",
        "model_name": "qwen-plus-2025-12-01",
        "base_model": "qwen-plus",
        "model_unit_spec": "MU1",
        "enable_thinking": true,
        "max_context_length": 10000,
        "rpm_limit": 500,
        "tpm_limit": 1000,
        "base_capacity": 1,
        "ready_capacity": 0,
        "workspace_id": "llm-v71tlv3d***",
        "charge_type": "post_paid",
        "creator": "175805416***",
        "modifier": "175805416***",
        "plan": "mu"
    }
}
```

#### 错误响应示例

```
{
    "code": "InvalidParameter",
    "request_id": "BE213CDD-8A5C-59EE-9A67-055EAB0CB59B",
    "message": "The model xxx does not exist or is not deployable"
}
```

## 下一步

部署为异步操作，调用本接口后可通过[查询和管理部署](raw/model-api-reference/model-production/deployments-api/get-deployment-api.md)接口查询部署状态。
