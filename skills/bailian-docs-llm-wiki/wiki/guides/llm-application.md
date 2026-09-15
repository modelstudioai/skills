# llm application

百炼平台的 LLM Application 是面向真实业务场景的 AI 应用构建体系，提供智能体（Agent）、工作流（Workflow）和高代码应用三种范式，分别覆盖零代码决策、低代码编排与专业级工程化部署需求。三者统一基于大模型能力底座，通过知识库、工具调用、多模态解析等扩展机制突破模型原生限制，支持私有知识融合、实时信息获取与复杂任务规划。

## 支持的模型/功能

LLM Application 的核心能力由底层模型驱动，并通过标准化组件扩展：

- **智能体（Agent）**：支持两类版本。Agent 1.0 以提示词驱动，独立配置知识库（RAG）与插件；Agent 2.0 将知识库、MCP 等统一为“工具”，由模型自主规划调用顺序，过程可追溯 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。推荐新项目优先使用 Agent 2.0。
- **工作流（Workflow）**：提供 20+ 类节点，覆盖基础逻辑（开始/结束、条件判断、循环、批处理）、AI 处理（大模型、意图分类、参数提取、知识库、多模态生成）、外部集成（API、函数计算、MCP、插件、AppFlow、数据连接器）及数据解析（文档、图片、音频、视频）等全链路能力。其中，[知识库节点](../../raw/application-user-guide/llm-application/workflow-application/knowledge-base-node.md) 支持文档/表格/图片三类知识源混合召回与智能过滤；[多模态生成节点](../../raw/application-user-guide/llm-application/workflow-application/multimodal-generation-node.md) 支持图像、视频、音频三类内容生成。
- **高代码应用**：面向开发者，基于 Python 项目结构部署 Serverless 或 K8s 服务，支持 MCP 协议接入知识库、MCP 服务、应用组件与数据连接器四类工具 [工具接入](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-application-mcp.md)。必须包含 `main.py` 入口与 `/health` 健康检查接口 [API 开发指南](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-app-develop-guide.md)。

> **注意**：文档 34 中列出的“千问3-Coder-Plus”“千问-QwQ-Preview”等模型名称在其他文档（如文档 2、3、11）的模型选择界面描述中未被提及，且其实际可用性与兼容性（如是否支持 `enable_thinking` 或 `enable_search`）未明确说明。建议以控制台实时下拉菜单为准，避免依赖该列表。

## 关键参数

各类型应用共用部分核心参数，但配置位置与语义略有差异：

- **最长回复长度**：控制模型输出 token 上限，不包含提示词。智能体中该参数位于模型设置内；工作流的大模型/意图分类/参数提取等节点均提供此参数，默认值为 1024；Agent 2.0 还额外支持 `thinking_budget`（思考链最大 tokens）。
- **温度系数（temperature）**：控制输出随机性，范围通常为 [0, 2)，默认值多为 0.7。Agent 1.0 和 Agent 2.0 均支持，工作流节点亦普遍支持。
- **enable_thinking**：启用深度思考模式，输出推理过程。Agent 2.0、工作流的大模型节点、意图分类节点、参数提取节点均支持此参数；Agent 1.0 文档中未提及该参数，仅提及其旧版“推理模式”，二者功能定位相似但配置项名称不一致，存在术语不统一问题。
- **上下文管理**：智能体通过“携带的上下文轮数”控制历史对话长度；工作流则通过“记忆”功能（本节点缓存/自定义缓存）实现，依赖 `historyList` 等内置变量 [开始和结束节点](../../raw/application-user-guide/llm-application/workflow-application/start-end-node.md)。

## 使用方式

- **创建与配置**：
  - 智能体：在控制台选择“智能体应用 > Agent 2.0”创建，配置模型（推荐 `千问-Max` 系列或 `智能模式`）、系统提示词、预解析文件开关及内置工具（如 `bash`、`write`）。
  - 工作流：通过可视化画布拖拽节点，关键节点如 [开始和结束节点](../../raw/application-user-guide/llm-application/workflow-application/start-end-node.md) 定义 I/O，[条件判断节点](../../raw/application-user-guide/llm-application/workflow-application/conditional-node.md) 实现分支路由，[循环节点](../../raw/application-user-guide/llm-application/workflow-application/loop-node.md) 与 [批处理节点](../../raw/application-user-guide/llm-application/workflow-application/batch-node.md) 分别支持串行与并行迭代。
  - 高代码应用：支持控制台模板创建或命令行上传 `.whl` 包，需严格遵循项目结构（`main.py` 入口、`requirements.txt` 固定版本）与 API 协议（`/process` 对话接口）。

- **文件处理**：
  - 智能体支持三种模式：全文引用（适合短文档总结）、切片检索（RAG，适合长文档问答）、自定义处理（依赖插件/MCP）[文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。
  - 工作流提供专用解析节点：[文档解析节点](../../raw/application-user-guide/llm-application/workflow-application/document-extraction-node.md)（PDF/DOCX 等）、[图片解析节点](../../raw/application-user-guide/llm-application/workflow-application/image-extraction-node.md)（支持 Qwen-VL 模型定制解析）、[音频/视频解析节点](../../raw/application-user-guide/llm-application/workflow-application/audio-extraction-node.md)（ASR 与关键帧提取）。

- **发布与调用**：
  - 智能体与工作流需先“发布”才能通过 API/SDK 调用，或集成至钉钉、微信等渠道。
  - 高代码应用部署即服务，API 地址在控制台直接获取，支持流式响应。

## 限制和注意事项

- **资源与配额**：
  - 文件上传：智能体单会话上限 10 个文件，单文件 ≤10MB；工作流文档解析单文件 ≤150MB/1.5万页，图片 ≤20MB，音视频 ≤512MB。
  - 循环与批处理：循环次数上限 1000，批处理默认并行数 5、上限 30；超限需手动调整。
  - 模型上下文：Agent 2.0 的 `AUTO` 模式在上下文 [Token](../concepts/token.md) >200K 时强制路由至“性能”档，以保障长文本处理效果。

- **功能边界**：
  - 工作流节点存在嵌套限制：循环体内禁止嵌套循环或批处理；批处理体内禁止嵌套批处理或循环。
  - JSON 输出：[变量处理节点](../../raw/application-user-guide/llm-application/workflow-application/variable-processing-node.md) 的 JSON 模式仅支持单层键值对，无法生成嵌套结构。
  - [流式输出](../concepts/streaming-output.md)：仅文本输出模式支持流式，JSON 输出模式不支持；AppFlow 节点本身不支持[流式输出](../concepts/streaming-output.md)。

- **开发与调试**：
  - 高代码应用的 MCP 工具调用需在代码中实现，控制台添加仅为配置展示，实际逻辑需依赖 `fastmcp.Client` [工具接入](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-application-mcp.md)。
  - 工作流调试：可通过测试面板翻页查看循环/批处理各轮次的详细输入输出，或使用 [流程输出节点](../../raw/application-user-guide/llm-application/workflow-application/process-output-node.md) 插入中间状态日志。

## 来源文档

- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [开始和结束节点](../../raw/application-user-guide/llm-application/workflow-application/start-end-node.md)
- [条件判断节点](../../raw/application-user-guide/llm-application/workflow-application/conditional-node.md)
- [循环节点](../../raw/application-user-guide/llm-application/workflow-application/loop-node.md)
- [批处理节点](../../raw/application-user-guide/llm-application/workflow-application/batch-node.md)
- [流程输出节点](../../raw/application-user-guide/llm-application/workflow-application/process-output-node.md)
- [知识库节点](../../raw/application-user-guide/llm-application/workflow-application/knowledge-base-node.md)
- [大模型节点](../../raw/application-user-guide/llm-application/workflow-application/llm-node.md)
- [意图分类节点](../../raw/application-user-guide/llm-application/workflow-application/intent-node.md)
- [多模态生成节点](../../raw/application-user-guide/llm-application/workflow-application/multimodal-generation-node.md)
- [参数提取节点](../../raw/application-user-guide/llm-application/workflow-application/parameter-extraction-node.md)
- [智能体创建节点](../../raw/application-user-guide/llm-application/workflow-application/agent-create-node.md)
- [智能体群组节点](../../raw/application-user-guide/llm-application/workflow-application/agent-group-node.md)
- [API节点](../../raw/application-user-guide/llm-application/workflow-application/api-node.md)
- [函数计算节点](../../raw/application-user-guide/llm-application/workflow-application/fc-node.md)
- [插件节点](../../raw/application-user-guide/llm-application/workflow-application/plugin-node.md)
- [脚本节点](../../raw/application-user-guide/llm-application/workflow-application/script-node.md)
- [AppFlow节点](../../raw/application-user-guide/llm-application/workflow-application/appflow-node.md)
- [MCP节点](../../raw/application-user-guide/llm-application/workflow-application/mcp-node.md)
- [应用组件节点](../../raw/application-user-guide/llm-application/workflow-application/component-node.md)
- [变量处理节点](../../raw/application-user-guide/llm-application/workflow-application/variable-processing-node.md)
- [变量赋值节点](../../raw/application-user-guide/llm-application/workflow-application/variable-assignment-node.md)
- [文档解析节点](../../raw/application-user-guide/llm-application/workflow-application/document-extraction-node.md)
- [图片解析节点](../../raw/application-user-guide/llm-application/workflow-application/image-extraction-node.md)
- [音频解析节点](../../raw/application-user-guide/llm-application/workflow-application/audio-extraction-node.md)
- [视频解析节点](../../raw/application-user-guide/llm-application/workflow-application/video-extraction-node.md)
- [工具接入](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-application-mcp.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [数据连接器节点](../../raw/application-user-guide/llm-application/workflow-application/data-connector-node.md)
- [API 开发指南](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-app-develop-guide.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)


