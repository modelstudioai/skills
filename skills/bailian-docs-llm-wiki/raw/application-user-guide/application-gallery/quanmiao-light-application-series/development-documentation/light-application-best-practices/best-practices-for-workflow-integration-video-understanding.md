# 阿里云百炼工作流集成视频理解最佳实践

本文介绍如何在阿里云百炼工作流中集成视频理解功能。

## **需求背景**

用户可能会遇到需要使用阿里云百炼工作流（workflow）搭建智能体，并希望在其中某一环节引用视频理解API的情况。阿里云百炼工作流是一种将复杂任务拆解为多个子任务，从而提高工作流程可控性的流程式AI应用。用户可以通过拖拽节点的方式来创建自定义的任务流程。

## 前提条件

-   开通阿里云百炼账号。具体操作，请参见[开通阿里云百炼](https://help.aliyun.com/zh/model-studio/first-api-call-to-qwen#67c76646c85x6)。
    
-   开通函数计算（FC）。具体操作，请参见[什么是函数计算](https://help.aliyun.com/zh/functioncompute/fc/product-overview/what-is-function-compute)。
    

## 操作步骤

本文以创建一个视频理解工作流应用为例进行说明。

### **步骤一：创建函数（FC）**

1.  在[函数计算](https://fcnext.console.aliyun.com/cn-hangzhou/functions)控制台创建事件函数。具体操作，请参见[创建事件函数](https://help.aliyun.com/zh/functioncompute/fc/user-guide/creating-an-event-function)。
    
    -   创建视频理解提交任务函数（建议函数名称：SubmitVideoAnalysisTask）。
        
        -   配置函数入口：配置->运行时->请求处理程序：FCVideoAnalysisTask.submit\_video\_analysis\_task。
            
    -   创建视频理解查询任务函数（建议函数名称：GetVideoAnalysisTask）。
        
        -   配置函数入口：配置->运行时->请求处理程序：FCVideoAnalysisTask.get\_video\_analysis\_task。
            

**说明**

-   **运行环境**：选择**Python 3.12**。
    
-   **代码上传方式：**可选择**通过ZIP包上传代码**，文件示例：[FCVideoAnalysisTask.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250530/rcuggo/FCVideoAnalysisTask.zip)。
    

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1015919471/p962779.png)

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1015919471/p962777.png)

2.  安装函数依赖。
    
    -   方案一：执行以下命令：
        
        ```
        pip3 install alibabacloud_endpoint_util alibabacloud_tea_openapi alibabacloud_quanmiaolightapp20240801 -t .
        ```
        
    -   方案二：以“层”的方式安装。相关文档，请参见[创建自定义层](https://help.aliyun.com/zh/functioncompute/fc/user-guide/create-a-custom-layer-1)。
        
    
3.  您可自行优化调整代码中的入参：比如`prompt`模板、`modelId`等。
    
    需要将代码中的[AK、SK](https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey)、[workspaceId](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)替换为实际值，以确保代码正常运行并返回正确的结果。
    
    ![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1015919471/p962781.png)
    

### **步骤二：配置阿里云百炼工作流**

1.  创建任务型工作流： 访问**[应用管理](https://bailian.console.aliyun.com/?spm=a2c4g.11186623.0.0.134172147obHXO#/app-center)**页面，单击**创建应用**，选择**工作流应用**，填写应用名称和描述信息，上传头像，点击**立即创建**即可，进入工作流配置页面。 ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2945430671/p1015539.png)
    
2.  将模板导入工作流。模板示例文件：[全妙-视频理解-工作流模板.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250530/qjfcat/%E5%85%A8%E5%A6%99-%E8%A7%86%E9%A2%91%E7%90%86%E8%A7%A3-%E5%B7%A5%E4%BD%9C%E6%B5%81%E6%A8%A1%E7%89%88.zip)。![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1015919471/p962784.png)
    
3.  修改部分节点配置：
    
    -   视频理解-提交异步任务：关联“SubmitVideoAnalysisTask”函数。
        
    -   视频理解-查询异步任务结果：关联“GetVideoAnalysisTask”函数。
        
    
    ![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1015919471/p962786.png)
    

### **可选：发布工作流为组件**

您可以将工作流应用发布为组件，以供其他智能体或工作流应用使用。具体操作，请参见[发布为组件](https://help.aliyun.com/zh/model-studio/workflow-application/#9fbf5d4dedf3k)。

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1015919471/p962778.png)

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1015919471/p962783.png)

### **可选：组件应用-串行**

可在您的工作流中导入串行的视频理解组件。示例文件：[视频理解-串行.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250603/ealumt/%E6%B5%8B%E8%AF%95-%E8%A7%86%E9%A2%91%E7%90%86%E8%A7%A3%E7%BB%84%E4%BB%B6.zip)。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1015919471/p963369.png)

### **可选：组件应用-并行**

可在您的工作流中导入并行的视频理解组件。示例文件：[视频理解-并行.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250603/nvedhp/%E8%A7%86%E9%A2%91%E7%90%86%E8%A7%A3-%E5%B9%B6%E8%A1%8C.zip)。

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1015919471/p962785.png)

## **常见问题**

#### **处理的视频支持多久时长？**

目前支持处理的视频时长不超过3分钟。后续将提升该方案中可处理的视频时长，敬请关注。
