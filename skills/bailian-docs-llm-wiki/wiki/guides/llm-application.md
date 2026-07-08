# llm application

阿里云百炼提供三种核心应用构建模式——智能体（Agent）、工作流（Workflow）和高代码应用，用于突破大模型在处理私有知识、获取实时信息、遵循固定流程及规划复杂任务等方面的原生局限。开发者可根据场景复杂度和技术栈选择合适的模式，通过集成知识库、MCP 工具、插件等能力快速构建 AI 应用。

## 应用类型选型

百炼平台的三种应用类型在开发方式、适用人群和核心特点上有明显差异，详见[应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)。

| 维度 | 智能体（Agent） | 工作流（Workflow） | 高代码应用 |
|------|-----------------|---------------------|------------|
| 开发方式 | 自然语言配置（零代码） | 可视化节点编排（低代码） | Python 编码 |
| 核心特点 | AI 自主决策、动态规划 | 预定义流程精确控制 | 完全由代码控制 |
| 适合人群 | 业务人员、产品经理 | IT 运维、业务分析师 | AI 工程师、开发者 |
| 典型场景 | 智能客服、知识问答、任务助理 | 报告生成、订单处理、审批流 | 私有算法部署、复杂系统集成 |

## 智能体应用（Agent）

智能体由提示词驱动，通过自主理解用户意图、制定决策并调用外部工具完成任务。百炼目前提供两个版本：

### Agent 2.0（推荐）

新版智能体将知识库、MCP 等多种能力统一为工具，由模型自主规划调用顺序，支持完整的"规划-执行-反思"链路展示。详见[新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。

核心能力：

- **模型选择**：推荐选用具备强工具调用能力的模型（如千问-Max 系列）。支持配置 temperature、最长回复长度、enable_thinking（思考模式）等参数。
- **内置工具**：提供沙箱环境中的 bash、read、write、edit、glob、grep、download_file 等工具，默认关闭，按需开启。
- **知识库**：作为工具由智能体自主规划调用，支持通过标签限定检索范围。
- **MCP 服务**：外部工具均以 MCP 协议接入，支持动态非固定顺序调用。
- **预解析文件**：支持开启/关闭文件预解析，千问-VL 系列可直接解析图片和视频。
- **应用组件**：可将已发布的智能体或工作流作为工具接入。
- **技能（Skill）**：可添加能力包，智能体在对话中自动识别并调用。
- **短期记忆**：支持 0-30 轮上下文记忆。

> **注意**：旧版智能体和新版智能体基于不同的技术架构，不支持直接升级或版本切换。如需使用 Agent 2.0，需重新创建应用。

**ReAct 最大轮次**：取值 1-50，限制单次会话中工具调用的最大次数，超出后自动生成最终回复。

### Agent 1.0（旧版）

旧版智能体在检索知识库后再决策是否调用其他工具，适用于意图单一、流程固定的简单任务。核心能力包括知识库（RAG）和插件调用，详见[智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)。

> **注意**：旧版智能体的自定义插件有 5 秒超时限制。

## 工作流应用（Workflow）

工作流通过可视化节点编排将多步骤复杂任务串联成稳定可控的执行链路。适合固定流程自动化场景，如诈骗信息识别、智能导购、日程管理等。详见[工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。

主要节点类型：

- **开始/结束节点**：定义输入输出参数，预置 query、historyList、imageList 变量。
- **大模型节点**：配置模型、提示词和用户提示词，支持记忆功能。
- **意图分类节点**：根据用户意图分流到不同处理分支。
- **智能体群组节点**：编排多个子智能体协作完成任务。
- **变量处理节点**：处理和转换流程中的变量。

工作流支持**会话变量**作为全局变量，在整个工作流生命周期内记录参数信息并在各节点间共享。

## 高代码应用

面向专业开发者，支持基于 Python 项目结构部署 AI 后端服务。详见[高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。

关键特性：

- **部署方式**：Serverless Function（低负载、无状态、快速拉起）和 K8s（高性能、有状态、长程任务）两种模式。
- **代码提交**：支持使用模板代码（基础对话 Agent、工具调用 Agent、深度研究 Agent）或上传 .whl 格式代码包。
- **MCP 工具接入**：控制台直接关联知识库、工作流、插件等 MCP 服务。
- **自定义前端**：支持直接体验、自定义交互卡片和基于 Spark Design 框架的自定义 WebUI。
- **企业级能力**：自动化运维、可观测、日志服务、API 网关。
- **网关配置**：通过云原生 API 网关实现自定义域名和生产环境访问，支持 [Token](../concepts/token.md) 鉴权。

## 文件问答

智能体应用支持上传文件后进行智能问答，提供三种处理模式，详见[文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)：

| 模式 | 适用场景 | 特点 |
|------|----------|------|
| 全文引用 | 文档总结、全文翻译、风格润色 | 简单直接，受上下文长度限制 |
| 切片检索（RAG） | 长文档问答、知识库检索 | 能处理超长文件，依赖切片和检索策略 |
| 自定义处理 | 图片转换、视频分析等需要外部工具的任务 | 功能灵活，依赖所配置的工具 |

文件格式支持：文档（doc/docx/ppt/pdf/md 等）、图片（png/jpg/gif 等）、视频（mp4/mkv 等）、音频（mp3/wav 等）。单会话最多 10 个文件，单文件不超过 10MB。超过 10MB 的文件需使用文件上传 API。

## 发布与调用

三种应用类型均需先在控制台**发布**后才能通过 API/SDK 调用：

- **智能体应用**：支持 API/SDK 调用，也可发布到钉钉、微信公众号等第三方平台，或发布为可复用组件。
- **工作流应用**：发布后通过工作流应用 API 调用。
- **高代码应用**：通过触发器 URL 或云原生 API 网关访问。

## 计费说明

- **模型调用**：按模型类型和 [Token](../concepts/token.md) 用量计费，创建应用本身不收费。
- **知识库**：按量付费，召回的文本切片会增加模型输入 [Token](../concepts/token.md)。
- **MCP/插件**：部分官方 MCP 按模型调用计费（如文生图），部分涉及第三方 API 费用。
- **高代码应用**：部署后函数计算、API 网关、存储均会产生费用。
- **文件问答**：文件上传不收费，问答按模型 Token 计费，全文引用模式消耗最大，切片检索模式通常更经济。

## 来源文档

- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)


