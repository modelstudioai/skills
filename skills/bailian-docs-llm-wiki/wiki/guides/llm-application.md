# llm application

阿里云百炼平台提供三种核心应用构建模式：智能体（Agent）、工作流（Workflow）和高代码应用，用于突破大模型在私有知识访问、实时信息获取和复杂任务规划方面的原生局限。开发者可根据开发门槛、控制粒度和业务场景选择合适的应用类型，并通过集成知识库、MCP 工具、插件等能力构建完整的 AI 应用。

## 应用类型与选型

| 对比维度 | 智能体（Agent） | 工作流（Workflow） | 高代码应用 |
|---------|---------------|-------------------|-----------|
| 开发方式 | 自然语言配置（零代码） | 可视化节点编排（低代码） | Python 编码 |
| 核心特点 | AI 自主决策、动态规划 | 预定义流程精确控制 | 完全由代码控制 |
| 适合人群 | 业务人员、产品经理 | IT 运维、业务分析师 | AI 工程师、开发者 |
| 开发门槛 | 低 | 中 | 高 |

详细的类型介绍参见 [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)。

## [智能体应用](../concepts/agent-application.md)

### 新版智能体（Agent 2.0）

新版智能体将知识库、MCP 等能力统一为工具，由智能体自主规划调用顺序，支持完整的"规划-执行-反思"链路展示。推荐在无旧版依赖时使用新版。

核心能力配置：

- **模型选择**：推荐具备强工具调用能力的模型（如千问-Max 系列）。支持配置最长回复长度、temperature、enable_thinking（思考模式）等参数。
- **提示词**：定义角色、行为指令与能力边界，支持自定义变量嵌入。
- **内置工具**：沙箱环境中的 bash、write、read、edit、glob、grep、download_file 等工具，默认关闭需按需开启。
- **知识库**：作为工具由智能体自主调用，支持标签过滤限定查询范围。
- **MCP**：外部工具以 MCP 协议接入，支持动态非固定顺序调用。
- **记忆**：短期记忆支持 0-30 轮上下文；长期记忆暂未支持。
- **ReAct 最大轮次**：取值 1-50，限制单次会话中工具调用最大次数。

详细配置方法参见 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。

### 旧版智能体（Agent 1.0）

旧版智能体通过知识库（RAG）和插件扩展能力，适合意图单一、流程固定的简单任务。知识库检索后再决策是否调用其他工具。

> **注意**：新版智能体与旧版智能体基于不同技术架构，不支持直接升级或版本切换。需要迁移时必须重新创建新版应用。

旧版智能体的自定义插件有 5 秒超时限制。详情参见 [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)。

## 工作流应用

工作流通过可视化节点编排将多步骤任务串联为稳定可控的执行链路，适合固定流程自动化场景。

主要节点类型：

- **开始/结束节点**：定义输入输出参数结构，预置 query、historyList、imageList 变量
- **大模型节点**：配置模型、提示词和用户提示词
- **意图分类节点**：根据用户输入分发到不同处理分支
- **智能体群组节点**：将子智能体作为工具组合调用
- **变量处理节点**：文本输出或变量转换

工作流支持会话变量作为全局参数在节点间传递，支持记忆功能（本节点缓存或自定义缓存）。

创建和配置详情参见 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。

## 高代码应用

面向专业开发者，支持基于 Python 项目部署 AI 后端服务。

关键特性：

- **部署方式**：Serverless Function（无状态快速拉起）和 K8s（高性能有状态长程任务）
- **MCP 工具接入**：控制台直接关联知识库、工作流、插件等 MCP 服务
- **前端体验**：支持直接体验、自定义交互卡片、基于 Spark Design 的自定义 WebUI
- **企业级能力**：自动化运维、可观测、日志服务、API 网关
- **代码提交**：支持控制台模板创建或命令行上传 .whl 代码包

生产环境建议开启网关功能，通过自定义域名访问。时延敏感业务建议最小实例数大于等于 1。

详细开发和部署流程参见 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。

## 文件问答

[智能体应用](../concepts/agent-application.md)支持上传文件进行智能问答，提供三种处理模式：

| 模式 | 适用场景 | 特点 |
|------|---------|------|
| 全文引用 | 文档总结、全文翻译 | 简单直接，受上下文长度限制 |
| 切片检索（RAG） | 长文档问答、知识库检索 | 能处理超长文件，效果依赖检索策略 |
| 自定义处理 | 图片转换、视频分析等需工具介入的任务 | 功能灵活，依赖配置的工具 |

文件限制：单会话最多 10 个文件，单文件不超过 10MB。超过 10MB 需使用文件上传 API。

支持格式：文档（doc/docx/pdf/md/txt 等）、图片（png/jpg/bmp/gif）、视频（mp4/mkv/avi 等）、音频（mp3/wav/flac 等）。

详细使用方式参见 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。

## 发布与调用

所有应用类型均需先发布才能通过 API 集成：

1. 在应用配置页点击"发布"，确认变更后完成发布
2. 在"发布渠道"页签查看 API 调用方式
3. [智能体应用](../concepts/agent-application.md)还支持发布到钉钉、微信公众号等第三方平台

RAM 账号发布前需确认拥有 `ram:CreateServiceLinkedRole` 权限。

## 计费说明

- **模型调用**：按模型类型和 [Token](../concepts/token.md) 用量计费
- **知识库**：按量付费，召回的文本切片会增加输入 [Token](../concepts/token.md)
- **MCP/插件**：部分官方 MCP 按调用计费，第三方 MCP 费用由第三方收取
- **高代码应用**：部署后函数计算、API 网关、存储均按量计费
- **文件上传**：上传本身不收费，问答消耗按所选模型标准计费

## 来源文档

- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)









