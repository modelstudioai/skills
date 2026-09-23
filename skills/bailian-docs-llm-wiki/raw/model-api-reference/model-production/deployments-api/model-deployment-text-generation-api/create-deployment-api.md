# 文本生成-部署模型

将训练好的文本模型发布为在线 API 服务。

## 适用范围

-   **适用地域**：当前模型部署 API **仅在华北2（北京）地域**开放。如您使用其他地域，请通过该地域的百炼控制台完成模型部署操作。
-   **开通账号权限**：若使用[阿里云子账号](raw/model-user-guide/security-and-compliance/permission-management-overview.md)（[RAM用户](https://help.aliyun.com/zh/ram/user-guide/overview-of-ram-users)），需要为子账号授予模型调用、训练和部署[权限](https://help.aliyun.com/zh/model-studio/use-workspace)。
-   **配置环境变量**：已成功[获取 API Key](raw/model-api-reference/preparations/get-api-key.md)，并[配置到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
-   **阅读部署文档**：建议先阅读[专属部署概述](raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)和[使用 API 创建模型部署任务](raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)，了解模型部署的使用方法和基本步骤。

## 部署模型

#### 华北2（北京）

`POST https://dashscope.aliyuncs.com/api/v1/deployments`

> Windows CMD 请将`$DASHSCOPE_API_KEY`替换为`%DASHSCOPE_API_KEY%`，PowerShell请替换为 `$env:DASHSCOPE_API_KEY`

### 请求参数

##### 请求头（Headers）

**Content-Type** `string` **（必选）**

固定值：`application/json`

**Authorization** `string` **（必选）**

API Key鉴权，格式为`Bearer sk-xxxx`。

##### 请求体（Request Body）

**model\_name** `string` **（必选）**

待部署的模型名称，对应[我的模型](https://bailian.console.aliyun.com/model/custom)中的模型 ID。也可通过[创建训练任务](raw/_short/create-fine-tuning-job-api-ec89a5612f9a9ba9.md)接口的输出获取。

**plan** `string` **（必选）**

部署方案。可选值：

-   `mu`：按模型单元计费。
-   `lora`：LoRA 共享部署（按 Token 用量计费）。
-   `ptu`：按预置吞吐量计费。

**deploy\_spec** `string` **（条件必填）**

部署模板。当 `plan` 为 `mu` 时必须填写。样例：`"deploy_spec": "MU1"`。

可通过获取可部署模型列表接口返回的 `template_id` 字段获取。

**capacity** `integer` **（条件必填）**

部署使用的资源单元数量，需为 `base_capacity` 的整数倍。不同 `deploy_spec` 的取值约束不同，例如 `MU2` 必须为 8 的倍数，`MU5` 可填 1。

**billing\_method** `string` **（条件必填）**

计费方式。当 `plan` 为 `mu` 时必须填写。当前支持 `"POST_PAY"`（后付费）。

**enable\_thinking** `boolean` （可选）

仅 `plan` 为 `mu` 时可设置。部分模型支持，可设置为 `true` 或 `false`。

**max\_context\_length** `number` （可选）

仅 `plan` 为 `mu` 时可设置。部分模型支持。样例：`"max_context_length": 131072`。

**rpm\_limit** `number` （可选）

仅 `plan` 为 `mu` 时可设置。部分模型支持，requests per minute，每分钟请求数。

**tpm\_limit** `number` （可选）

仅 `plan` 为 `mu` 时可设置。部分模型支持，token per minute，每分钟 Token 使用量。

**ptu\_capacity** `object` （可选）

仅 `plan` 为 `ptu` 时生效。如果不填写该参数，将默认按照 `10,000 input_tpm` 和 `1,000 output_tpm` 进行设置。

ptu\_capacity 属性

**input\_tpm** `number`

部署的模型每分钟支持的最大输入 Token 量。

**output\_tpm** `number`

部署的模型每分钟支持的最大输出 Token 量。

**thinking\_output\_tpm** `number`

部分模型支持，部署的模型每分钟支持的预置思考最大输出 Token 量。

**name** `string` （可选）

模型的控制台显示名称。如果不传该参数，将自动使用 `model_name` 的值作为部署名称。

**suffix** `string` （可选）

模型部署后，将生成新的模型名称，**suffix** 用于指定新模型名称的后缀，最大长度为8个字符且需全局唯一。每个模型在首次部署时，可以不指定后缀。如果需要对同一模型进行多次部署，则必须设置后缀以便于区分。

#### 按模型单元计费

选择按模型单元计费，计费模式为按模型单元的使用时长收费，适用于模型调优后的大规模推理业务，资源专属，性能和成本灵活可调。

> 执行以下部署命令后，即便您还没有调用模型，模型部署服务仍将在部署成功后开始计费。建议您先确认服务计费规则，再执行部署命令。

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
    "billing_method": "POST_PAY",
    "max_context_length": 10000,
    "rpm_limit": 500,
    "tpm_limit": 1000
}'
```

#### 按Token用量计费

选择按 Token 用量计费，适用于高性价比诉求且对并发和延迟要求不高的场景。该模式价格优势最高，吞吐/并发和生成速度均由平台预置，用户不可调。

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

## 部署排障与性能调优

### max-num-seqs 参数不可配置

百炼模型部署在**按预置吞吐计费**和**按模型单元计费**两种计费方式下，吞吐、并发和生成速度均为平台预置，不支持直接调整 vLLM 内部的 `max-num-seqs` 等推理引擎参数，本接口的请求参数中也不存在该参数。

**按模型单元计费**方式下，可通过选择**模型单元类型**（对应请求参数 `deploy_spec`）和调整**部署副本数**（对应请求参数 `capacity`）间接控制吞吐能力。

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

**request\_id** `string`

请求的唯一标识符。

**output** `object`

任务详情。

属性

**deployed\_model** `string`

部署模型的唯一标识。用于查询模型部署状态和调用模型。

**model\_name** `string`

模型标识名。

**status** `string`

部署状态：

-   `PENDING`：正在创建部署任务。
-   `UPDATING`：正在更新部署任务。
-   `RUNNING`：部署任务正在运行，此时已部署的模型可以正常处理请求。
-   `STOPPED`：部署任务已经停止，此时的部署任务不会被计费。
-   `DELETING`：正在删除部署任务。
-   `FAILED`：部署任务创建或更新失败。

**base\_model** `string`

使用的基准模型。

**gmt\_create** `string`

部署任务创建时间。

**gmt\_modified** `string`

部署任务更新时间。

**workspace\_id** `string`

阿里云百炼API Key所属的业务空间ID。请参见[获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)。

**charge\_type** `string`

付费模式。post\_paid表示后付费。

**creator** `string`

创建人的阿里云账号ID。

**modifier** `string`

修改人的阿里云账号ID。

**plan** `string`

部署方式。

**base\_capacity** `number`

基础模型运行所需的最小资源单元数量。

**ready\_capacity** `number`

已就绪并可立即处理请求的资源单元数量。

**model\_unit\_spec** `string`

模型单元规格。仅 `plan` 为 `mu` 时返回。

**enable\_thinking** `boolean`

是否开启思考模式。仅 `plan` 为 `mu` 时返回。

**max\_context\_length** `number`

最大上下文长度限制。仅 `plan` 为 `mu` 时返回。

**rpm\_limit** `number`

每分钟请求数。仅 `plan` 为 `mu` 时返回。

**tpm\_limit** `number`

每分钟 Token 使用量。仅 `plan` 为 `mu` 时返回。

**ptu\_capacity** `object`

预置吞吐量配置。仅 `plan` 为 `ptu` 时返回。

ptu\_capacity 属性

**input\_tpm** `number`

部署的模型每分钟支持的最大输入 Token 量。

**output\_tpm** `number`

部署的模型每分钟支持的最大输出 Token 量。

**thinking\_output\_tpm** `number`

部分模型支持，部署的模型每分钟支持的预置思考最大输出 Token 量。

**code** `string`

错误码。调用失败时返回。

**message** `string`

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
