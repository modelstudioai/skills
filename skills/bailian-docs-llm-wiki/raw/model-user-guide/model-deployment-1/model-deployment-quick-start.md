# API 部署指南

本文档以千问模型的部署为例，使用 API（HTTP）调用方式帮助您完成阿里云百炼模型部署的全流程操作，包括部署、查询、推理、删除及权限排查。

**重要**本文档仅适用于华北2（北京）地域。

## 前提条件

-   您已经完整阅读了[模型部署](raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)，熟悉阿里云百炼平台模型部署支持的模型和基本步骤。
-   您需要已[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。请将示例代码中的 `DASHSCOPE_API_HOST` 替换为获取的 API Host。

## 1\. 部署模型

下面的命令展示如何创建专属服务。其中，按 Token 计费的示例使用已经调优好的自定义模型`qwen3-8b-ft-202511132025-0260`，创建一个专属服务`qwen3-8b-ft-202511132025-0260`；按预置吞吐和按模型单元的示例使用预置模型。

获取自定义模型 ID 的方法：前往[百炼控制台-模型调优](https://bailian.console.aliyun.com/cn-beijing/model/tuning)，点击需要部署的**任务名称** -> **产出** -> 点击蓝色字体的模型名称，进入**我的模型**页面，在模型基本信息区域可查看模型 ID。

使用**模型 ID**作为输入的`model_name`参数，即可使用 API 部署该模型。

#### 按预置吞吐（PTU）计费

**说明**执行以下部署命令后，即便您还没有调用模型，模型部署服务仍将在部署成功后开始计费。建议您先确认服务计费规则，再执行部署命令。

按预置吞吐计费模式按预置吞吐的使用时长收费，适用于追求稳定吞吐保障和高并发低延迟、且流量可预估的场景。该模式下，**吞吐/并发**和**生成速度**均为平台预置，用户不可调。

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

选择**按模型单元计费**计费方式，计费模式为按模型单元的使用时长收费，适用场景为模型调优后的大规模推理业务，资源专属，性能和成本灵活可调；吞吐/并发和生成速度均为客户自定义。

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

服务名称

自定义部署服务的名称。

选择模型

选择要部署的模型，包括平台预置模型和已调优的模型。

模型单元类型

选择部署规格，不同规格对应不同的算力和性能。

单副本模型单元

单副本所需的模型单元数量，由部署模版和模型单元类型共同决定，不可修改。例如 qwen3-32b 单副本模型单元数量为 16。总模型单元数 = 部署副本数 × 单副本模型单元，决定了部署服务使用多少资源。部署副本数扩大会使用更多模型单元，提供更好的模型性能。

部署副本数

设置初始部署副本数量，影响服务的并发处理能力。

部署模版

选择部署模版（如"单机部署"），不同模版对应不同的资源配置方案。仅在模型单元计费模式下可用。

配置模型推理模式

部分模型在以**模型单元**方式部署时，可配置推理模式、最长上下文等。

-   Instruct - 模型部署后以**非思考模式**进行推理。
    
-   Thinking - 模型部署后以思考模式进行推理。
    

最长上下文

部分模型的**模型单元**部署模式支持该设置。最长上下文长度基于模型类型。

服务限流

部分模型的**模型单元**部署模式支持该设置，可限制模型调用的 RPM、TPM。

如何在 API 设置上述内容，请参考：[使用 API 创建部署](raw/model-api-reference/model-production/deployments-api/model-deployment-text-generation-api/create-deployment-api.md)。

#### 按模型 Token 使用量计费

选择计费方式为**按Token计费**，计费模式为按Token用量收费，适用于高性价比诉求且对并发和延迟要求不高的场景。该模式价格优势最高，吞吐/并发和生成速度均由平台预置，用户不可调。

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

> capacity 参数设置无效，但必须填写。如需扩缩容，请前往专属部署[控制台](https://bailian.console.aliyun.com/cn-beijing/model/deploy)填写表单申请。

#### dashscope CLI

```
export DASHSCOPE_API_KEY="your-api-key"
# 将 {WorkspaceId} 替换为业务空间ID，cn-beijing 替换为对应地域（新加坡: ap-southeast-1, 美东: us-east-1）
export DASHSCOPE_HTTP_BASE_URL="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
# 列出已部署的专属服务
dashscope deployments list

# 创建专属服务（--plan 必填）
# plan 可选值：ptu（PTU 预留资源）/ mu（模型单元）/ lora（LoRA 部署）
dashscope deployments create -m qwen2.5-7b-instruct -s tst -c 1 --plan ptu
```

> `-m` 指定模型名称，`-s` 指定服务后缀，`-c` 指定部署容量。

**重要**SDK Expert 交互式助手可按自然语言完成同样的开发与排障，见

[DashScope SDK Expert](raw/model-api-reference/preparations/dashscope-sdk-expert.md)。

完整地域表见 [Base URL 总览](raw/model-user-guide/get-started-with-models/base-url.md)。

命令执行成功后，返回如下结果：（以 Lora 部署为例）

```
{
    "request_id": "83b173ab-2b2f-41aa-8c57-b173e8be934e",
    "output":
    {
        "deployed_model": "qwen3-8b-ft-202511132025-0260",
        "gmt_create": "2025-11-20T20:06:46.405",
        "gmt_modified": "2025-11-20T20:06:46.405",
        "status": "PENDING",
        "model_name": "qwen3-8b-ft-202511132025-0260",
        "base_model": "qwen3-8b",
        "workspace_id": "llm-8v*****",
        "charge_type": "post_paid",
        "creator": "16542*****",
        "modifier": "16542*****",
        "plan": "lora"
    }
}
```

其中`deployed_model`为专属服务的唯一ID。

## 2\. 查询服务状态

通过以下命令查询指定专属服务的详细信息：

```
curl "https://dashscope.aliyuncs.com/api/v1/deployments/qwen3-8b-ft-202511132025-0260" \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header 'Content-Type: application/json'
```

命令执行成功后，返回如下结果：

```
{
    "request_id": "ca36952d-9136-426e-ab08-68a97ad72719",
    "output":
    {
        "deployed_model": "qwen3-8b-ft-202511132025-0260",
        "gmt_create": "2025-11-20T20:32:08",
        "gmt_modified": "2025-11-20T20:42:25",
        "status": "RUNNING",
        "model_name": "qwen3-8b-ft-202511132025-0260",
        "base_model": "qwen3-8b",
        "base_capacity": 2,
        "capacity": 2,
        "ready_capacity": 2,
        "workspace_id": "llm-8v53etv3hwb8orx1",
        "charge_type": "post_paid",
        "creator": "1654290265984853",
        "modifier": "1654290265984853",
        "plan": "mu",
        "model_unit_spec": "MU1"
    }
}
```

当服务状态为`RUNNING`时，服务部署完成。

## 3\. 执行推理请求

**说明**若首次使用DashScope SDK，请参考[安装SDK](raw/model-api-reference/preparations/install-sdk.md)。

请确保 API Key 所在的业务空间与模型部署所在的业务空间相同。

调用已部署的专属服务时，`model` 参数取值应为模型部署成功后的模型 `code`，请前往[专属部署控制台（北京）](https://bailian.console.aliyun.com/cn-beijing/model/deploy)获取。

DashScope

```
import os
import dashscope

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "你是谁？"},
]
response = dashscope.Generation.call(
    # 若没有配置环境变量，请用百炼API Key将下一行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen3-14b-xxx-xxx",  # 请替换为模型部署成功后的code
    messages=messages,
    result_format="message",
    enable_thinking=False,
)
print(response)
```

OpenAI兼容接口

```
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下一行替换为：api_key="sk-xxx",
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen3-14b-xxx-xxx",  # 请替换为模型部署成功后的code
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "你是谁？"},
    ],
    extra_body={"enable_thinking": False},
)
print(completion)
```

### 推理参数对齐

百炼推理引擎的参数默认值可能与本地推理框架不同。为对齐 vLLM 默认值，建议调用时参考下表设置参数；使用 SGLang 等其他框架请参考对应文档调整。

**参数名称**

**推荐值（对应 vLLM 默认值）**

temperature

取值范围 \[0, 2)，设置为 1.0 等同于 vLLM 引擎默认值。

top\_p

取值范围 (0, 1.0\]，设置为 1.0 等同于 vLLM 引擎默认值。

top\_k

取值为 None 或大于 100 时不启用 top\_k 策略，仅 top\_p 生效；设置为 99 不支持全采样，接近 vLLM 默认值 0（全采样）。

presence\_penalty

取值范围 \[-2.0, 2.0\]，设置为 0 等同于 vLLM 引擎默认值。

repetition\_penalty（DashScope 协议）

提高可降低生成重复度，1.0 表示不惩罚；取值范围大于 0，设置为 1.0 等同于 vLLM 引擎默认值。

## 4\. 删除专属服务

**警告**执行以下删除命令后，模型部署服务将立即开始下线，且不可恢复。您将：

1.  无法调用该模型。
2.  部署服务停止计费。

不再使用的专属服务，可以通过下面的命令删除：

```
curl --request DELETE 'https://dashscope.aliyuncs.com/api/v1/deployments/qwen3-8b-ft-202511132025-0260' \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header 'Content-Type: application/json'
```

命令执行成功后，返回以下结果：

```
{
    "request_id": "8f726017-6042-420e-a465-0d366a3aba59",
    "output":
    {
        "deployed_model": "qwen3-8b-ft-202511132025-0260",
        "gmt_create": "2025-11-20T20:32:08",
        "gmt_modified": "2025-11-27T16:35:31.591",
        "status": "DELETING",
        "model_name": "qwen3-8b-ft-202511132025-0260",
        "base_model": "qwen3-8b",
        "base_capacity": 2,
        "capacity": 2,
        "ready_capacity": 2,
        "workspace_id": "llm-8v53etv3hwb8orx1",
        "charge_type": "post_paid",
        "creator": "1654290265984853",
        "modifier": "1654290265984853",
        "plan": "mu",
        "model_unit_spec": "MU1"
    }
}
```

删除成功后，再使用[2\. 查询服务状态](https://help.aliyun.com/zh/model-studio/model-deployment-quick-start#7ce6489058608)接口将无法查询到部署模型的状态。

## 权限不足排查

模型部署过程中如遇权限不足报错，根据部署方式分两种排查路径：

### 控制台部署

1.  如果显示**"缺少该模块的权限"**，请确保您的账号在该业务空间的权限管理页面中拥有**模型部署-操作**权限。
    
    如果无法正常操作，请联系您的组织或 IT 管理员添加相关权限或代为检查权限问题。
    
2.  如果部署时报错"**xx业务空间没有部署xx模型的权限**"，请前往百炼的[业务空间管理](https://bailian.console.aliyun.com/settings/workspace)页面，为对应业务空间添加对应模型的部署权限。
    
    > API 调用报错：`Workspace xxx does not have deployment privilege for model xxxx`。
    
    ![PixPin\_2025-11-27\_15-03-57](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1816324671/p1030115.png) ![PixPin\_2025-11-27\_15-06-41](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1816324671/p1030118.png)
    
    如果提示权限不足，请联系您的组织或 IT 管理员添加相关权限或代为操作。
    

### API 部署

在使用 API 进行模型部署时，需要确保：

1.  API Key 的**归属业务空间**拥有管理该模型的权限。请前往百炼的[业务空间管理](https://bailian.console.aliyun.com/settings/workspace)页面，检查对应业务空间的模型部署权限设置。
    
    > API 调用报错：`Workspace xxx does not have deployment privilege for model xxxx`。
    
    在对应业务空间的**操作**列，单击**模型权限流控设置**。
    
    在**模型列表**中找到目标模型，查看**模型部署**列的授权状态。若显示**未授权**，单击**操作**列的**编辑**进行授权。
    
    如果提示权限不足，请联系您的组织或 IT 管理员添加相关权限或代为操作。
    
2.  API Key 的**归属账号**在**归属业务空间**中拥有操作权限。请前往[百炼控制台](https://bailian.console.aliyun.com/model/market)，点击左下角的业务空间，切换到对应业务空间，再点击![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1816324671/p1030217.png)检查对应业务空间的模型部署权限设置。
    
    > API 调用报错：`Workspace access denied`。
    
    在左侧导航栏点击**权限管理**，确认用户列表中包含 API Key 的归属账号（类型为**主账号**）。
    
    如果提示权限不足，请联系您的组织或 IT 管理员添加相关权限或代为操作。
    

## API参考

详细API调用请参考[API 详情](https://help.aliyun.com/zh/model-studio/model-deployment-api)及[部署 API 全集](https://help.aliyun.com/zh/model-studio/model-deployment-new-api-reference)。
