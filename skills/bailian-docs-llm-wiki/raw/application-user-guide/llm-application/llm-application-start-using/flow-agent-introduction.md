# 概述

了解 Flow Agent 的应用类型、扩展能力和使用方法。

## 什么是 Flow Agent

Flow Agent 是阿里云百炼提供的可视化应用开发平台，支持构建、调试和发布智能体应用和工作流应用。

## 应用类型

大模型原生能力在处理私有知识、获取实时信息、遵循固定流程和规划复杂任务方面存在局限。阿里云百炼通过知识库检索增强、外部工具调用和记忆等核心能力，帮助您快速构建解决真实业务问题的 AI 应用。

按任务选择：需要开放式对话或基于私有资料回答问题，选择**智能体应用**；已经知道处理步骤、需要按固定流程生成报告，选择**工作流应用**。

应用类型

说明

适用场景

[智能体应用](raw/application-user-guide/llm-application/new-single-agent-application.md)

自然语言配置（零代码），可调用知识库、MCP 服务等工具完成任务

智能客服、知识问答、任务助理

[工作流应用](raw/application-user-guide/llm-application/workflow-application.md)

可视化节点编排（低代码），将多步骤任务串联为稳定可控、可复现的执行链路

报告生成、订单处理、多步骤审批

## 扩展能力

能力

说明

适用场景

[文件问答](raw/application-user-guide/llm-application/file-q-a.md)

对文档、图片、音视频等文件进行内容理解和问答，提供全文引用、切片检索和自定义处理三种模式

长文档问答、资料检索、图片和音视频内容理解

[Prompt](raw/application-user-guide/prompt.md)

管理可复用的 Prompt 模板，支持样例库、自动优化和反馈优化

沉淀常用提示词、持续优化回答效果

[插件](raw/application-user-guide/plug-in.md)

通过官方插件和自定义插件扩展应用能力

联网搜索、代码执行、业务系统调用

[任务中心](raw/application-user-guide/llm-application/flow-agent-task-center.md)

查看异步调用产生的后台任务，包括执行状态、输入输出和时间信息

长耗时任务的进度跟踪与结果查询

## 开始使用

按所选路线先创建和配置，再通过对应 API 调用。工作流没有结果或变量不符，先在[测试应用](https://help.aliyun.com/zh/model-studio/workflow/introduction#test-app)中检查节点输入输出；调用超时时，查看[API 调用说明](https://help.aliyun.com/zh/model-studio/workflow/introduction#d6ec5f242b81v)。API 返回错误码时，查看[错误码](raw/model-api-reference/preparations/error-code.md)。

如需托管会话、独立沙箱和长时任务运行，参见独立的[托管 Agent 概述](raw/application-user-guide/agent-development/managed-agents/managed-agents-start-using/managed-agents-introduction.md)。

[

**快速开始**

5 分钟创建第一个智能体应用。

](https://help.aliyun.com/zh/model-studio/build-knowledge-base-qa-assistant-without-coding)[

**创建智能体应用**

选择模型、编写提示词，创建智能体应用。

](raw/application-user-guide/llm-application/new-single-agent-application.md)[

**创建工作流应用**

通过可视化节点编排，创建工作流应用。

](raw/application-user-guide/llm-application/workflow-application.md)[

**使用 CLI**

在终端用 bl app 列出并调用已发布的应用与工作流。

](raw/application-user-guide/llm-application/llm-application-start-using/flow-agent-cli.md)

### 实践案例

-   **智能体应用**：[创建智能问答 AI 电商客服助手](https://www.aliyun.com/solution/tech-solution/build-ai-applications-based-on-alibaba-cloud-model-studio#0a9fbaf6a71q7)。
-   **工作流应用**：[创建处理复杂流程的 AI 电商客服助手](https://www.aliyun.com/solution/tech-solution/build-ai-applications-based-on-alibaba-cloud-model-studio#6f801f75f371t)、[零代码搭建数据标注工作流](https://www.aliyun.com/solution/tech-solution-deploy/2977204)。

### API 接入

-   **新版智能体应用（Agent 2.0，推荐）**：[新版智能体应用 API](raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)。
-   **工作流应用**：[调用工作流应用](raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。

### 旧版兼容

已有 Agent 1.0 应用可继续参考[智能体应用（Agent 1.0）](raw/application-user-guide/llm-application/single-agent-application.md)进行创建和配置，并通过[调用智能体应用](raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)接入 API；新建应用优先使用上面的 Agent 2.0 入口。
