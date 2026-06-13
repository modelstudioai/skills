# llm application

阿里云百炼提供三种核心应用构建模式——智能体（Agent）、工作流（Workflow）和高代码应用，用于突破大模型在私有知识访问、实时信息获取和复杂任务规划等方面的原生局限。开发者可根据业务场景的复杂度和定制需求，选择零代码、低代码或专业代码的方式构建 AI 应用。

## 应用类型与选型

百炼平台的三种应用类型覆盖从零代码到专业开发的完整场景，详见[应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)。

| 维度 | 智能体（Agent） | 工作流（Workflow） | 高代码应用 |
|------|-----------------|-------------------|-----------|
| 开发方式 | 自然语言配置（零代码） | 可视化节点编排（低代码） | Python 编码 |
| 核心特点 | AI 自主决策、动态规划 | 预定义流程精确控制 | 完全由代码控制 |
| 适合人群 | 业务人员、产品经理 | IT 运维、业务分析师 | AI 工程师、开发者 |
| 开发门槛 | 低 | 中 | 高 |

**选型建议**：
- 需要模型自主决策、调用工具完成开放式任务 --> 智能体
- 需要固定流程、可复现的自动化链路 --> 工作流
- 需要深度定制、部署私有算法或集成复杂系统 --> 高代码应用

## 智能体应用

### 新版智能体（Agent 2.0）

新版智能体将知识库、MCP 等能力统一为工具，由模型自主规划调用顺序，支持完整的"规划-执行-反思"链路展示。推荐在无旧版依赖时使用新版，详见[新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。

**核心能力配置**：

- **模型选择**：推荐使用 `千问-Max` 系列模型以确保多步规划效果。支持配置 `temperature`、`最长回复长度`、`enable_thinking`（思考模式）等参数。
- **系统提示词**：定义智能体角色和行为边界，支持嵌入自定义变量。
- **知识库**：作为工具由智能体自主调用，支持通过标签限定检索范围。
- **MCP**：外部工具以 MCP 协议接入，支持官方和自定义 MCP 服务，插件可一键转换为 MCP。
- **记忆**：短期记忆支持 0-30 轮上下文；长期记忆暂未开放。
- **ReAct 最大轮次**：取值 1-50，限制单次会话工具调用次数。

> **注意**：旧版智能体（Agent 1.0）与新版基于不同技术架构，不支持直接升级或降级，需重新创建应用。

### 旧版智能体（Agent 1.0）

旧版智能体采用"先检索知识库、再决策是否调用其他工具"的固定流程，适用于意图单一的简单任务。详见[智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)。核心能力包括知识库（RAG）和插件调用。

### 文件问答

智能体应用支持上传文件进行智能问答，提供三种处理模式：

- **全文引用**：将文件内容整体输入模型，适合文档总结、全文翻译。受上下文长度限制。
- **切片检索（RAG）**：将文件切分为片段按相关性检索，适合长文档精确问答。
- **自定义处理**：将文件信息传给模型，由模型调用 MCP/插件处理，适合图片转换、视频分析等。

**文件限制**：单个会话最多 10 个文件，单文件不超过 10MB。支持文档（doc/pdf/md 等）、图片（png/jpg 等）、视频（mp4 等）、音频（mp3/wav 等）格式。详见[文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。

## 工作流应用

工作流通过可视化节点编排，将复杂任务拆分为有序执行步骤。支持大模型节点、意图分类节点、智能体群组节点、变量处理节点等多种节点类型。详见[工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。

**典型场景**：自动化报告生成、诈骗信息识别、智能导购、日程管理等。

**关键特性**：
- **会话变量**：全局变量，可在工作流全生命周期内跨节点引用
- **记忆功能**：大模型和意图分类节点支持"本节点缓存"和"自定义缓存"两种模式
- **智能体群组**：可将多个已发布的智能体作为子节点组合使用

## 高代码应用

面向专业开发者，支持基于 Python 项目部署 AI 后端服务。详见[高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。

**部署方式**：
- **Serverless Function**（默认）：适合低负载、无状态场景，花销低
- **K8s**：适合高性能、有状态长程任务，需开通 ACK 容器服务

**关键能力**：
- 一站式 MCP 工具接入（知识库、工作流、插件）
- 自定义前端 WebUI（基于 Spark Design 框架）
- API 网关（自定义域名 + Token 鉴权）
- 应用观测与日志

平台提供基础对话 Agent、工具调用 Agent、深度研究 Agent 等应用模板。

## 发布与 API 调用

所有类型的应用都需要先在控制台**发布**后才能进行 API 调用或集成。

- 智能体应用 API 调用频率默认限制为 **100 次/分钟**（所有请求共享配额）
- 文件上传 API 获取的 `session_file_id` 有效期通常为 24 小时
- 通过 RAM 账号创建的应用，发布前需确认已拥有 `ram:CreateServiceLinkedRole` 权限

## 计费说明

- **创建应用不收费**，仅在调用时按模型类型和 Token 用量计费
- **知识库**按量付费，召回的文本切片会增加模型输入 Token 消耗
- **MCP**：部分官方 MCP 按模型调用计费（如文生图、语音合成），第三方 MCP 费用由第三方收取
- **高代码应用**：部署后函数计算、API 网关、存储均会产生费用
- **自定义插件超时限制**为 5 秒

## 来源文档

- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)



