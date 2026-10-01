# llm application

`llm application` 是阿里云百炼平台提供的核心 AI 应用构建能力集合，支持通过零代码、低代码和高代码三种范式，将大语言模型与知识库、外部工具、多模态能力及业务系统深度集成，快速构建可解决真实业务问题的生产级 AI 应用。其核心价值在于突破大模型原生能力边界，实现私有知识问答、实时信息获取、复杂任务规划与自动化执行。

## 支持的模型/功能

百炼 `llm application` 提供三类应用模式，面向不同技术背景与业务复杂度需求：

- **智能体（Agent）应用**：由提示词驱动，具备自主意图理解、动态规划与工具调用能力。新版 Agent 2.0 将知识库、MCP 等统一为工具，支持完整的“规划-执行-反思”链路回溯，适用于开放式对话、任务助理等场景 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
- **工作流（Workflow）应用**：通过可视化节点编排，将多步骤任务串联为确定性执行链路。支持大模型、知识库、意图分类、参数提取、多模态生成、API/MCP/函数计算等多种节点类型，适用于报告生成、客服流程、数据标注等固定流程自动化场景 [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)。
- **高代码应用**：面向专业开发者，支持基于 Python 项目结构部署 Serverless 或 K8s 后端服务，提供完整 MCP 工具接入、可观测性与企业级运维能力，适用于需要深度定制、私有算法集成或高性能长程任务的场景 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。

> **注意**：文档中提及的“智能体应用（Agent 1.0）”已明确被新版 Agent 2.0 取代，其规划逻辑（先检索后决策）和过程透明度均弱于新版，[应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md) 文档亦明确推荐优先使用 Agent 2.0。

## 关键参数

各类应用的核心参数配置高度一致，主要围绕模型、提示词与上下文控制：

- **模型选择与参数**：所有应用均支持在模型选择器中指定具体模型（如 `千问-Max`）或启用 `智能模式`（AUTO/性能/均衡/经济），后者根据任务复杂度自动路由并统一计费。通用参数包括：
  - `最长回复长度`：模型生成内容的 Token 上限（不含提示词）。
  - `temperature`：控制输出随机性（范围通常为 `[0, 2)`），值越高越多样。
  - `enable_thinking`：是否开启模型深度思考模式，提升规划与反思效果（部分模型不支持）。
- **系统提示词（System Prompt）**：定义智能体角色、行为规范与能力边界，是控制输出一致性与任务合规性的核心手段。支持嵌入自定义变量（如 `/` 触发变量选择），用于动态注入上下文 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
- **文件处理模式**：智能体应用支持三种文件问答模式——`全文引用`（直接注入解析后全文）、`切片检索`（RAG，按需召回相关片段）和`自定义处理`（模型自主调用插件/MCP 处理）[文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。

## 使用方式

- **创建与配置**：在百炼控制台 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) 页面，根据选型点击“创建应用”，选择对应类型（Agent 2.0 / Workflow / 高代码应用），完成模型、提示词、工具（知识库、MCP、插件等）的配置。
- **交互与调试**：智能体应用支持文本对话与文件上传；工作流应用通过画布拖拽节点（如大模型节点、知识库节点、条件判断节点、循环节点等）进行编排，并可在测试面板中查看每轮迭代的详细输入输出 [循环节点](../../raw/application-user-guide/llm-application/workflow-application/loop-node.md)。
- **发布与调用**：应用发布后，可通过 API/SDK 调用，或集成至钉钉、微信公众号等第三方平台。高代码应用还支持命令行一键部署 `.whl` 包 [API 开发指南](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-app-develop-guide.md)。

## 限制和注意事项

- **上下文与文件限制**：智能体应用单会话最多上传 10 个文件，单文件上限 10MB；工作流中图片解析单文件 ≤20MB，音频/视频 ≤512MB，文档 ≤150MB [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)；当上下文 Token 数超过 200K 时，Agent 2.0 的 AUTO 模式将强制路由至“性能”档位以保障效果 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
- **工具与节点约束**：工作流中，循环体子画布内禁止嵌套循环或批处理节点；批处理节点不支持添加流程输出节点；API 节点调用外部服务前，需将百炼服务 IP（`47.93.216.17` 和 `39.105.109.77`）加入目标服务器白名单 [API节点](../../raw/application-user-guide/llm-application/workflow-application/api-node.md)。
- **高代码开发规范**：Python 后端必须提供 `GET /health` 健康检查接口，入口文件必须为 `main.py`，对话默认路径为 `/process`；依赖版本建议在 `requirements.txt` 中使用 `==` 固定，避免构建失败 [API 开发指南](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-app-develop-guide.md)。

## 来源文档

- [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [开始和结束节点](../../raw/application-user-guide/llm-application/workflow-application/start-end-node.md)
- [循环节点](../../raw/application-user-guide/llm-application/workflow-application/loop-node.md)
- [条件判断节点](../../raw/application-user-guide/llm-application/workflow-application/conditional-node.md)
- [批处理节点](../../raw/application-user-guide/llm-application/workflow-application/batch-node.md)
- [流程输出节点](../../raw/application-user-guide/llm-application/workflow-application/process-output-node.md)
- [大模型节点](../../raw/application-user-guide/llm-application/workflow-application/llm-node.md)
- [知识库节点](../../raw/application-user-guide/llm-application/workflow-application/knowledge-base-node.md)
- [意图分类节点](../../raw/application-user-guide/llm-application/workflow-application/intent-node.md)
- [参数提取节点](../../raw/application-user-guide/llm-application/workflow-application/parameter-extraction-node.md)
- [多模态生成节点](../../raw/application-user-guide/llm-application/workflow-application/multimodal-generation-node.md)
- [智能体群组节点](../../raw/application-user-guide/llm-application/workflow-application/agent-group-node.md)
- [智能体创建节点](../../raw/application-user-guide/llm-application/workflow-application/agent-create-node.md)
- [API节点](../../raw/application-user-guide/llm-application/workflow-application/api-node.md)
- [插件节点](../../raw/application-user-guide/llm-application/workflow-application/plugin-node.md)
- [脚本节点](../../raw/application-user-guide/llm-application/workflow-application/script-node.md)
- [函数计算节点](../../raw/application-user-guide/llm-application/workflow-application/fc-node.md)
- [应用组件节点](../../raw/application-user-guide/llm-application/workflow-application/component-node.md)
- [MCP节点](../../raw/application-user-guide/llm-application/workflow-application/mcp-node.md)
- [AppFlow节点](../../raw/application-user-guide/llm-application/workflow-application/appflow-node.md)
- [变量赋值节点](../../raw/application-user-guide/llm-application/workflow-application/variable-assignment-node.md)
- [变量处理节点](../../raw/application-user-guide/llm-application/workflow-application/variable-processing-node.md)
- [图片解析节点](../../raw/application-user-guide/llm-application/workflow-application/image-extraction-node.md)
- [音频解析节点](../../raw/application-user-guide/llm-application/workflow-application/audio-extraction-node.md)
- [文档解析节点](../../raw/application-user-guide/llm-application/workflow-application/document-extraction-node.md)
- [数据连接器节点](../../raw/application-user-guide/llm-application/workflow-application/data-connector-node.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [视频解析节点](../../raw/application-user-guide/llm-application/workflow-application/video-extraction-node.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)
- [工具接入](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-application-mcp.md)
- [API 开发指南](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-app-develop-guide.md)


