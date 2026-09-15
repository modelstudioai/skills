# 我的模型

在我的模型中，可以统一管理您在阿里云百炼调优后的模型以及本地微调后导入的模型（限LoRA微调和全参微调），支持云端部署，提供高并发、低延迟的推理服务。

## 支持的模型

在[我的模型](https://bailian.console.aliyun.com/model/custom)页面，您可以管理以下两类模型：

-   **调优模型：**指在阿里云百炼调优后的模型，详见[模型调优支持的模型](https://help.aliyun.com/zh/model-studio/model-training-overview#adf01c4f4dqxd)。
    
-   **导入模型：**指从阿里云对象存储OSS导入的模型**。**支持导入部分经过 LoRA 微调或全参微调的模型。
    
    > 导入全参微调后的模型属于白名单功能，如需开通请联系客户经理。
    
    模型列表：
    
    **支持的模型**
    
    **模型名称**
    
    千问 3
    
    千问3-32B
    
    千问3-14B
    
    千问3-8B
    
    千问 2.5
    
    千问2.5-72B
    
    千问2.5-32B
    
    千问2.5-14B
    
    千问2.5-7B
    
    千问 2.5-VL
    
    千问2.5-VL-72B
    
    千问2.5-VL-32B
    
    千问2.5-VL-7B
    
    > 数据更新可能存在延迟，请以导入模型时界面实际显示为准。
    

## 导入模型

接下来为您介绍如何通过阿里云百炼控制台从OSS导入模型。

> 导入模型不支持通过API或命令行操作。

1.  在[我的模型](https://bailian.console.aliyun.com/model/custom)页面，单击**导入模型**，进入导入模型界面。
    
2.  输入**模型名称**，并选择导入模型的**基础模型**（即被微调的模型）。
    
3.  **导入方式**选择**从OSS导入**，暂不支持其它方式。您需要自行将已完成LoRA微调或全参微调的模型的相关文件[上传](https://help.aliyun.com/zh/oss/user-guide/upload-objects-to-oss/)至阿里云对象存储OSS。[查看模型文件示例](https://help.aliyun.com/zh/model-studio/my-model-center#8200512f30r63)
    
    **重要**
    
    -   首次导入请先按照界面提示完成授权，并为目标Bucket添加标签。详见[首次从 OSS 向阿里云百炼导入文件，应该如何操作](raw/model-user-guide/model-deployment-1/my-model-center.md)。
    -   支持的OSS Bucket存储类型不包括归档、冷归档或深度冷归档。支持内容加密的Bucket。支持私有的Bucket。
    -   不支持访问OSS Bucket根目录下的文件，请您在OSS Bucket下选择已有的子目录或新建一个子目录供阿里云百炼访问。
    -   支持导入任意大小的模型文件，导入后将使用阿里云百炼提供的免费存储空间。
    
4.  单击**确定**后，系统将开始导入模型。在请求高峰时段，该过程可能需要较长时间，请耐心等待。
    

## 后续操作

### 管理我的模型

在[我的模型](https://bailian.console.aliyun.com/model/custom)页面可查看当前业务空间内所有已调优和导入的模型，并执行部署、删除等操作。

> **删除：**已部署的模型须先下线再删除；若模型来自[模型调优](https://bailian.console.aliyun.com/model/tuning)，本操作不会删除模型调优界面中的记录。

### 调用我的模型

模型需成功部署后才能提供推理服务（只能通过API调用）。关于具体操作和计费方式，请参见[部署后调用](raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。

-   **关键限制：**在阿里云百炼[调优](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)后的模型部署成功后，只能使用其所在业务空间的 API-KEY 调用，且目前仅支持通过[DashScope](raw/model-api-reference/more-about-models/model-calling-in-sub-workspace.md)方式调用，不支持通过OpenAI兼容方式调用。
-   **优化推理效果：**请在调用时显式配置推理超参（如`presence_penalty`、`frequency_penalty`和`repetition_penalty`等），并确保与您线下微调后的推理超参设置保持一致。

## 模型文件示例

-   LoRA微调后一般会生成两个checkpoint文件，分别是best\_model\_checkpoint（在验证集上表现最优的检查点）与last\_model\_checkpoint（最后一次保存的检查点）。您可以根据需求选择其中一个导入。
    
    请确保导入的模型文件中包含adapter\_model.safetensors和adapter\_config.json。如需了解LoRA微调方法，您可以参考[阿里云大模型ACP课程](https://edu.aliyun.com/course/3130200/)中的模型微调章节。
    
    checkpoint 文件目录中通常包含以下文件：`global_step100/`（子目录）、`README.md`、`adapter_config.json`、`adapter_model.safetensors`、`additional_config.json`、`configuration.json`、`generation_config.json`、`latest`、`rng_state_0.pth` 和 `rng_state_1.pth`。
    
-   全参微调需要导入的文件和开源模型保持一致。
    

## 常见问题

首次从 OSS 向阿里云百炼导入文件，应该如何操作？

如果您是首次从 OSS 向阿里云百炼导入文件，请先按照界面提示完成授权，并为目标 OSS Bucket 添加`bailian-datahub-access`标签，然后再进行导入。

> 如果您尚不清楚主账号和子账号的概念和区别，请先阅读[权限管理](raw/model-user-guide/security-and-compliance/permission-management-overview.md)。

#### 使用主账号

1.  单击**前往授权**。
    
    在 **导入方式** 中选择 **从OSS导入** 后，页面会显示"您还未授权OSS"的提示信息，在提示栏右侧找到 **前往授权** 链接。
    
2.  在弹出的对话框中，单击**确认授权**，系统将为您自动开通[OSS服务关联角色](raw/application-api-reference/more/bailian-service-linked-role.md)（必要条件）。
    
    > 通常秒级生效，服务高峰期可能会稍有延迟。
    
    > [遇到“本次请求失败，尝试重新提交试试或联系管理员，错误码：10041495”怎么办](raw/model-user-guide/model-deployment-1/my-model-center.md)
    
3.  为目标 OSS Bucket 添加`bailian-datahub-access`标签。
    
    > 该标签用于标记阿里云百炼可访问的 Bucket，未标记的 Bucket 阿里云百炼无法访问。
    
    1.  访问[OSS管理控制台](https://oss.console.aliyun.com/)，单击左侧导航栏中的****Bucket 列表****，即可查看您已创建的Bucket。
    2.  在待添加标签的Bucket**标签**列，悬停鼠标于![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1134056371/p903505.png)图标上，然后单击**前往编辑**。
    3.  单击**创建标签**。
    4.  单击**标签**，添加标签名为`bailian-datahub-access`，标签值为`read`的标签，然后单击**保存**。
4.  返回**导入模型**界面，重新选择目标 Bucket 再尝试导入。
    
    > **请注意，阿里云百炼不支持访问保存在 Bucket 根目录下的文件。**请您选择 Bucket 下的现有文件夹或新建一个文件夹供阿里云百炼访问。
    

#### 使用 子账号

1.  单击**前往授权**。
    
2.  在弹出的对话框中，单击**确认授权**。界面会提示**授权失败**、**当前用户没有创建服务关联角色的权限**（因为当前子账号没有创建服务关联角色的权限。接下来需要先授予子账号创建服务关联角色的权限，再授予子账号通过阿里云百炼访问OSS的权限）。
    
    对话框中显示 Service Name 为 `datahub.sfm.aliyuncs.com`，服务关联角色名称为 `AliyunServiceRoleForSFMDataHubOSSImport`，执行该操作所需的用户权限为 `ram:CreateServiceLinkedRole`。
    
3.  授予子账号创建服务关联角色的权限。
    
    1.  **需主账号登录**[RAM控制台](https://ram.console.aliyun.com/)，在左侧导航栏，选择**权限管理权限策略**，然后单击界面上的**创建权限策略**。
    2.  在**脚本编辑**的`Effect`、`Action`、`Resource`、`Condition`中分别输入以下脚本中的对应内容后，单击**确定**。

```
{
    "Action": [
        "ram:CreateServiceLinkedRole"
    ],
    "Resource": "*",
    "Effect": "Allow",
    "Condition": {
        "StringEquals": {
            "ram:ServiceName": "datahub.sfm.aliyuncs.com"
        }
    }
}
```

3.  输入权限策略名称后，单击**确定**。
    
    本示例中，权限策略名称为`服务关联角色`。
    
4.  在左侧导航栏，选择**身份管理用户**。在页面列表中找到待授权的子账号，然后单击子账号**操作**列的**添加权限**。
    
5.  在权限策略中选择刚才创建的权限策略（自定义策略），单击**确认新增授权**。至此，子账号拥有了创建服务关联角色的权限。
    
6.  授权子账号通过阿里云百炼访问OSS。
    
    1.  返回**导入模型**界面，单击**前往授权**。
        
        **导入方式**选择**OSS**后，界面提示**您还未授权OSS**。
        
    2.  在弹出的对话框中，单击**确认授权**，系统将为您自动开通[OSS服务关联角色](raw/application-api-reference/more/bailian-service-linked-role.md)（必要条件）。
        
        > 通常秒级生效，服务高峰期可能会稍有延迟。
        
        > [遇到“本次请求失败，尝试重新提交试试或联系管理员，错误码：10041495”怎么办](raw/model-user-guide/model-deployment-1/my-model-center.md)
        
7.  为目标 OSS Bucket 添加`bailian-datahub-access`标签。
    
    > 该标签用于标记阿里云百炼可访问的 Bucket，未标记的 Bucket 阿里云百炼无法访问。
    
    1.  访问[OSS管理控制台](https://oss.console.aliyun.com/)，单击左侧导航栏中的****Bucket 列表****，即可查看您已创建的Bucket。
    2.  在待添加标签的Bucket**标签**列，悬停鼠标于![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1134056371/p903505.png)图标上，然后单击**前往编辑**。
    3.  单击**创建标签**。
    4.  单击**标签**，添加标签名为`bailian-datahub-access`，标签值为`read`的标签，然后单击**保存**。
8.  返回**导入模型**界面，重新选择目标 Bucket 再尝试导入。
    
    > **请注意，阿里云百炼不支持访问保存在 Bucket 根目录下的文件。**请您选择 Bucket 下的现有文件夹或新建一个文件夹供阿里云百炼访问。
    

遇到“10041495”报错怎么办？

一般是由于主账号尚未开通对象存储服务 OSS，处理步骤：

1.  需主账号前往[OSS管理控制台](https://oss.console.aliyun.com/)，按界面指引开通 OSS。
2.  返回阿里云百炼**导入模型**界面，再尝试授权。
