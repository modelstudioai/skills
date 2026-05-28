# 应用类型介绍

为突破大模型在处理私有知识、获取实时信息、遵循固定流程及规划复杂任务等方面的原生局限，阿里云百炼提供了三种核心应用构建模式：智能体（Agent）、工作流（Workflow）和高代码应用。百炼应用能够通过集成知识库检索增强、外部工具调用、记忆等核心能力，帮助快速构建能够解决真实业务问题的 AI 应用。

## 快速选型

-   **智能体（Agent）应用**：
    
    -   由提示词驱动，能够自主理解用户意图、制定决策，并调用知识库、MCP 服务等外部工具来完成任务。
        
    -   适合构建开放式对话应用，如智能客服、知识问答、任务助理、旅行规划等场景。
        
-   **工作流（Workflow）应用**：
    
    -   通过可视化节点编排，能够将多步骤复杂任务串联成稳定可控、可复现的执行链路。
        
    -   适合实现固定流程自动化，如自动化报告生成、订单处理、多步骤审批流、数据标注等场景。
        
-   **高代码应用**：
    
    -   面向专业开发者，支持基于 Python 代码构建和部署 AI 后端服务，一键部署上云并自动集成企业级运维能力。
        
    -   适合部署私有算法、集成复杂系统、构建专业级 AI 后端服务等需要深度定制的场景。
        

## 应用对比

**对比维度**

**智能体（Agent）**

**工作流（Workflow）**

**高代码应用**

开发方式

自然语言配置（零代码）

可视化节点编排（低代码）

Python 编码（专业代码）

核心特点

AI 自主决策、动态规划  
由大模型根据提示词自主规划任务步骤  

由预定义流程精确控制  
每一步都由预设的节点定义，逻辑确定  

完全由代码控制  
所有逻辑和执行路径由代码定义  

适合人群

业务人员、产品经理、运营

IT 运维、业务分析师、实施顾问

AI 工程师、开发者

开发门槛

低

中

高

## 开始使用

根据您的选型，您可以在控制台创建应用、快速上手实际案例，或通过 API 调用集成到现有系统：

-   **智能体应用**
    
    -   如何创建和配置？请参考：[新版智能体应用](https://help.aliyun.com/zh/model-studio/new-single-agent-application)（推荐）、[智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application)。
        
    -   如何快速上手实际案例？请参考：[创建智能问答 AI 电商客服助手](https://help.aliyun.com/zh/document_detail/2878136.html#0a9fbaf6a71q7)、[集成高德 MCP 的旅行规划智能体](https://help.aliyun.com/zh/document_detail/2880695.html)。
        
    -   如何通过 API 调用？请参考：[新版智能体应用 API](https://help.aliyun.com/zh/model-studio/new-agent-application-api-reference)、[调用智能体应用](https://help.aliyun.com/zh/model-studio/call-single-agent-application/)。
        
-   **工作流应用**
    
    -   如何创建和配置？请参考：[工作流应用](https://help.aliyun.com/zh/model-studio/workflow-application/)。
        
    -   如何快速上手实际案例？请参考：[创建处理复杂流程的 AI 电商客服助手](https://help.aliyun.com/zh/document_detail/2878136.html#6f801f75f371t)、[零代码搭建数据标注工作流](https://help.aliyun.com/zh/document_detail/2977204.html)。
        
    -   如何通过 API 调用？请参考：[调用工作流应用](https://help.aliyun.com/zh/model-studio/invoke-workflow-application/)。
        
-   **高代码应用**
    
    -   如何创建和部署？请参考：[高代码应用](https://help.aliyun.com/zh/model-studio/rich-code-application/)。
