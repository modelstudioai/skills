# 使用 API或命令行进行模型部署

本文档以千问模型的部署为例进行说明，使用 API（HTTP）调用方式帮助您使用阿里云百炼提供的模型部署功能。

**重要**

本文档仅适用于中国大陆版（北京地域）。

## 前提条件

-   您已经完整阅读了[模型部署简介](https://help.aliyun.com/zh/model-studio/model-deployment-introduction)，熟悉如何在阿里云百炼平台进行模型部署的支持的模型和基本步骤。
    
-   您需要已[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
    

## **1\. 部署模型**

下面的命令使用已经调优好的自定义模型`qwen3-8b-ft-202511132025-0260`，创建一个专属服务`qwen3-8b-ft-202511132025-0260`。

获取自定义模型 ID 的方法：前往[百炼控制台-模型调优](https://bailian.console.aliyun.com/cn-beijing?tab=model#/efm/model_manager)，点击需要部署的**任务名称** -> **产出** -> 点击蓝色字体的模型名称，进入**我的模型**页面。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0984437771/p1071306.png)

使用**模型 ID** 作为输入的`model_name`参数，即可使用 API 部署该模型。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0984437771/p1071307.png)

## 按预置吞吐（PTU）计费

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

### 按模型 Token 使用量计费

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
        "plan": "***"
    }
}
```

其中`deployed_model`为专属服务的唯一ID。

## **2\. 查询服务状态**

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

## **3\. 执行推理请求**

**说明**

若首次使用DashScope SDK，请参考[安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。

请确保 API Key 所在的业务空间与模型部署所在的业务空间相同。

通过SDK对专属服务发起请求：

```
from dashscope import Generation
from http import HTTPStatus
import os

response = Generation.call(
    model='qwen3-8b',
    prompt='你是谁？',
    enable_thinking=False,
    api_key=os.getenv('DASHSCOPE_API_KEY'),
)

if response.status_code == HTTPStatus.OK:
    print(response.output)
    print(response.usage)
else:
    print(response.code)
    print(response.message)
```

代码执行成功后，返回如下结果：

```
{"text": "我是Qwen，由阿里云开发的超大规模语言模型。我被设计用于生成各种类型的文本，如文章、故事、诗歌等，并能根据不同的场景和需求进行对话、解答问题、提供信息和帮助等。很高兴为您服务！如果您有任何问题或需要帮助，请随时告诉我。", "finish_reason": "stop", "choices": null}
{"input_tokens": 11, "output_tokens": 63, "total_tokens": 74}
```

## **4\. 删除专属服务**

**警告**

执行以下删除命令后，模型部署服务将立即开始下线，且不可恢复。您将：

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

删除成功后，再使用[2\. 查询服务状态](#7ce6489058608)接口将无法查询到部署模型的状态。

## API参考

详细API调用请参考[API 详情](https://help.aliyun.com/zh/model-studio/model-deployment-api)。

## **常见问题**

### **模型部署时报错权限不足怎么办？**

在使用 API 进行模型部署时，需要确保：

1.  API Key 的**归属业务空间**拥有管理该模型的权限。请前往百炼的[业务空间管理](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)页面，检查对应业务空间的模型部署权限设置。
    
    > API 调用报错：`Workspace xxx does not have deployment privilege for model xxxx`。
    
    ![PixPin\_2025-11-27\_15-03-57](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1816324671/p1030115.png)
    
    ![PixPin\_2025-11-27\_15-06-41](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1816324671/p1030118.png)
    
    如果提示权限不足，请联系您的组织或 IT 管理员添加相关权限或代为操作。
    
2.  API Key 的**归属账号**在**归属业务空间**中拥有操作权限。请前往[百炼控制台](https://bailian.console.aliyun.com/?tab=model#/model-market)，点击左下角的业务空间，切换到对应业务空间，再点击![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1816324671/p1030217.png)检查对应业务空间的模型部署权限设置。
    
    > API 调用报错：`Workspace access denied`。
    
    ![PixPin\_2025-11-27\_16-41-26](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1816324671/p1030231.png)
    
    如果提示权限不足，请联系您的组织或 IT 管理员添加相关权限或代为操作。
