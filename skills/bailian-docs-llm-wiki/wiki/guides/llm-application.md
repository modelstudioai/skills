# llm application

阿里云百炼平台提供三种核心应用构建模式——智能体（Agent）、工作流（Workflow）和高代码应用，帮助开发者突破大模型在私有知识、实时信息、固定流程和复杂任务规划等方面的原生局限。通过集成知识库检索增强（RAG）、外部工具调用（MCP/插件）、记忆等核心能力，可快速构建解决真实业务问题的 AI 应用。

## 应用类型与选型

根据 [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)，三种应用类型的核心区别如下：

| 对比维度 | 智能体（Agent） | 工作流（Workflow） | 高代码应用 |
|---------|---------------|-------------------|-----------|
| 开发方式 | 自然语言配置（零代码） | 可视化节点编排（低代码） | Python 编码 |
| 核心特点 | AI 自主决策、动态规划 | 预定义流程精确控制 | 完全由代码控制 |
| 适合人群 | 业务人员、产品经理 | IT 运维、业务分析师 | AI 工程师、开发者 |
| 典型场景 | 智能客服、知识问答、旅行规划 | 报告生成、订单处理、数据标注 | 私有算法部署、复杂系统集成 |

### 智能体应用（Agent）

智能体由提示词驱动，通过协调外部能力完成复杂任务。当前存在两个版本：

- **Agent 2.0（新版，推荐）**：将知识库、MCP 统一为工具，由智能体自主规划调用顺序，支持完整的"规划-执行-反思"链路展示。
- **Agent 1.0（旧版）**：知识库检索先行，再决策是否调用其他工具，适用于意图单一、流程固定的简单任务。

> **注意**：根据 [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md) 文档，旧版和新版智能体基于不同技术架构，不支持直接升级或版本切换，需重新创建应用。

### 工作流应用

工作流通过可视化节点编排将多步骤任务串联为可控的执行链路。支持的节点类型包括：开始/结束节点、大模型节点、意图分类节点、智能体群组节点、变量处理节点等。适用于诈骗信息识别、智能导购、日程管理等固定流程场景。

### 高代码应用

面向专业开发者，支持基于完整 Python 项目结构部署 AI 后端服务。根据 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md) 文档，主要特性包括：

- 支持 **Serverless Function** 和 **K8s** 两种部署方式
- 一站式 MCP 工具接入
- 自定义前端体验（基于 Spark Design 框架）
- 自动集成企业级运维能力（可观测、日志、API 网关）

## 支持的模型

智能体应用支持千问系列模型和自定义部署模型，主要包括：

**文本生成模型**：千问-Max、千问-Plus、千问-Turbo、千问-Long、千问3-Coder-Plus、千问3/2.5/2 开源模型、千问-QwQ、DeepSeek

**视觉理解模型**：千问VL-Max、千问VL-Plus、千问VL-OCR

为确保多步规划效果，新版智能体推荐选用具备强工具调用能力的模型（如 `千问-Max` 系列）。

## 核心能力与关键参数

### 模型参数

| 参数 | 说明 |
|------|------|
| 最长回复长度 | 模型生成的长度限制，不包含提示词 |
| temperature | 控制生成随机性和多样性，数值越高随机性越强 |
| enable_thinking | 是否开启思考模式，有助于提升智能体反思效果（仅部分模型支持） |

### 知识库（RAG）

连接外部知识库，基于私有数据回答问题。新版智能体中知识库作为工具由智能体自主规划调用，支持通过标签限定查询范围。从知识库召回的文本切片会占用模型上下文窗口并增加输入 Token。

### 文件问答

根据 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md) 文档，支持三种处理模式：

- **全文引用**：文件内容整体传递给模型，适合文档总结、全文翻译。参数：单文件最大解析长度、最大拼装长度。
- **切片检索**：文件切分后检索最相关片段，适合长文档问答。参数：召回片段数、最大拼装长度。
- **自定义处理**：模型自主调用外部工具处理文件，适合图片转换、视频分析等。

文件限制：单会话最多 10 个文件，单文件不超过 10MB。支持格式涵盖文档（doc/pdf/md 等）、图片（png/jpg 等）、视频（mp4/mkv 等）、音频（mp3/wav 等）。

### MCP 与插件

- 新版智能体通过 MCP 协议统一接入外部工具
- 旧版智能体通过插件机制调用工具，自定义插件超时限制为 **5 秒**
- 插件支持一键转换为 MCP 服务

### 记忆

- **短期记忆**：多轮会话上下文，支持 0-30 轮
- **长期记忆**：新版智能体暂不支持（计划中），旧版智能体支持且数据存储不收费

> **注意**：旧版智能体文档提到支持长期记忆且记忆体 Token 暂不计费，但新版智能体文档明确表示长期记忆"计划在未来迭代中支持"。两个版本的记忆能力存在差异。

### ReAct 最大轮次

新版智能体支持配置 ReAct 最大轮次（1-50），限制单次会话中工具调用的最大次数，超出后自动退出工具调用链路并生成最终回复。

## 使用方式

### 创建与配置

1. 访问百炼控制台 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)
2. 创建应用时选择对应类型（智能体 Agent 2.0/1.0、工作流、高代码）
3. 配置模型、系统提示词、知识库、工具等
4. 在右侧对话窗口调试验证

### 发布与调用

- **发布**是所有后续调用和集成的前提条件
- 支持 API 调用集成到现有系统
- 智能体应用 API 默认限流：**100 次/分钟**（所有请求共享配额）

### 高代码应用部署

```bash
# 通过 AgentScope-AI 命令行工具部署
# 支持 .whl 格式代码包上传
```

部署后通过网关访问：
```bash
curl -i -X POST "http://{your-domain}/{your-agentCode}/process" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {token}" \
  -d '{"input": [{"role": "user", "content": [{"type": "text", "text": "你好"}]}], "session_id": "xxx", "user_id": "xxx"}'
```

## 计费说明

| 计费项 | 说明 |
|--------|------|
| 模型调用 | 按模型类型和 Token 用量计费 |
| 知识库 | 按量付费，召回文本增加模型输入 Token |
| MCP/插件 | 部分官方 MCP 按模型调用计费，第三方 API 费用由第三方收取 |
| 文件上传 | 不收费 |
| 高代码应用 | 函数计算、网关、存储均产生费用 |

仅创建应用不收费，调用时按实际使用计费。

## 限制与注意事项

- 上传文件仅在当前会话有效，刷新或关闭页面将丢失
- 通过文件上传 API 的文件有效期为 24 小时
- API 调用时无法动态切换文件处理模式，按应用保存的配置执行
- RAM 账号发布应用需确认拥有 `ram:CreateServiceLinkedRole` 权限
- 应用对外提供服务需完成合规备案
- 千问-VL 系列模型即使关闭预解析文件也能直接解析图片和视频
- 高代码应用部署地域应与网关所在地域相同
- Assistant API 创建的应用不支持控制台管理

## 来源文档

- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [新版智能体应用](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [智能体应用](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)




