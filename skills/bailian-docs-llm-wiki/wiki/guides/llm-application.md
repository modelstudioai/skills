# llm application

`llm application` 是阿里云百炼平台提供的核心 AI 应用构建能力集合，支持通过智能体（Agent）、工作流（Workflow）和高代码（Rich Code）三种范式，将大语言模型与知识库、外部工具、多模态能力及业务系统深度集成，快速构建可解决真实业务问题的生产级 AI 应用。其设计目标是突破 LLM 在私有知识访问、实时信息获取、确定性流程控制和复杂任务规划等方面的原生局限。

## 支持的模型/功能

百炼 `llm application` 支持三类应用形态，对应不同能力边界与开发范式：

- **智能体（Agent）**：以提示词驱动，由模型自主理解意图、规划步骤并调用工具（如知识库、MCP、内置沙箱工具）。新版 Agent 2.0 将知识库与 MCP 统一为“工具”，支持完整“规划-执行-反思”链路回溯，显著优于旧版 Agent 1.0 的固定调度逻辑 [原文标题](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
- **工作流（Workflow）**：通过可视化节点编排实现确定性、可复现的多步执行链路，包含基础节点（开始/结束/条件/循环/批处理）、AI 节点（大模型/知识库/意图分类/参数提取/多模态生成）、工具节点（API/函数计算/脚本/MCP/插件/AppFlow/数据连接器）及解析节点（文档/图片/视频/音频）等丰富组件 [原文标题](../../raw/application-user-guide/llm-application/workflow-application.md)。
- **高代码（Rich Code）**：面向专业开发者，支持基于 Python 项目结构部署 Serverless 或 K8s 后端服务，完全由代码控制逻辑，并通过 MCP 协议接入知识库、MCP 服务、应用组件和数据连接器等能力 [原文标题](../../raw/application-user-guide/llm-application/rich-code-application.md)。

> **注意**：文档 34 中关于“文件问答”的模型支持列表存在大量重复链接（如多个 `[选择模型](...)`）且未列出具体模型名，与文档 1 和文档 3 中明确列出的 `千问-Max`、`千问-VL` 系列等实际可用模型不符，该列表应以控制台实时显示为准，不可直接引用。

## 关键参数

各类应用共用部分核心参数，但配置位置与语义略有差异：

- **模型选择**：智能体应用支持“智能模式”（AUTO/性能/均衡/经济）或“指定模型”；工作流中各 AI 节点（大模型/意图分类/参数提取等）均需独立选择模型；高代码应用则在代码中通过 `fastmcp.Client` 显式调用。所有场景均推荐选用具备强工具调用能力的模型（如 `千问-Max` 系列）[原文标题](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
- **温度系数（temperature）**：控制输出随机性，范围通常为 `[0, 2)`，值越高越多样。智能体与工作流节点均支持此参数，但高代码应用需在代码中设置。
- **最长回复长度**：模型生成内容的 token 上限，不包含提示词。各节点默认值可能不同（如大模型节点默认 1024），需根据任务需求调整。
- **enable_thinking**：是否开启模型深度思考模式，用于提升规划与反思效果。仅对支持该能力的模型生效，且在 Agent 2.0 配置中明确提及 [原文标题](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。

## 使用方式

- **智能体应用**：在控制台“应用管理”页创建，选择“智能体应用 > Agent 2.0”，配置模型、系统提示词、预解析文件开关及内置工具（如 `bash`、`write`、`read`）后即可测试 [原文标题](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
- **工作流应用**：通过拖拽节点（如开始、大模型、知识库、条件判断、循环、批处理等）至画布，配置各节点输入/输出/参数后连线编排。例如，用“开始节点 → 知识库节点 → 大模型节点”实现 RAG 增强问答 [原文标题](../../raw/application-user-guide/llm-application/workflow-application.md)。
- **高代码应用**：本地开发 Python 项目（含 `main.py` 入口、`requirements.txt` 及工具模块），通过 `agentscope-runtime` 命令行工具上传部署，或在控制台选择模板一键创建 [原文标题](../../raw/application-user-guide/llm-application/rich-code-application.md)。

## 限制和注意事项

- **文件处理限制**：智能体应用单会话最多上传 10 个文件，单文件不超过 10MB；工作流中各解析节点有独立限制（如文档解析单文件 ≤150MB，图片 ≤20MB，视频/音频 ≤512MB）；所有上传文件仅在当前会话有效，刷新页面即丢失。
- **上下文与 Token**：RAG 检索结果占用模型上下文窗口，需合理设置切片大小与 topK；当上下文 Token 数超过 200K 时，Agent 2.0 的 AUTO 模式将强制路由至“性能”档以保障效果 [原文标题](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
- **工具调用隔离**：智能体内置工具（`bash`/`write`/`read`）运行于隔离沙箱，无法访问外部网络或持久化存储；工作流中的 API/MCP/函数计算等节点则需确保百炼服务 IP（`47.93.216.17` 和 `39.105.109.77`）已加入目标服务白名单 [原文标题](../../raw/application-user-guide/llm-application/workflow-application/api-node.md)。
- **节点能力约束**：循环节点内禁止嵌套循环或批处理；批处理节点不支持流程输出节点；MCP 节点不支持[流式输出](../concepts/streaming.md)；视频/音频解析节点仅支持单文件。

## 来源文档

- [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [开始和结束节点](../../raw/application-user-guide/llm-application/workflow-application/start-end-node.md)
- [条件判断节点](../../raw/application-user-guide/llm-application/workflow-application/conditional-node.md)
- [循环节点](../../raw/application-user-guide/llm-application/workflow-application/loop-node.md)
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
- [函数计算节点](../../raw/application-user-guide/llm-application/workflow-application/fc-node.md)
- [脚本节点](../../raw/application-user-guide/llm-application/workflow-application/script-node.md)
- [插件节点](../../raw/application-user-guide/llm-application/workflow-application/plugin-node.md)
- [AppFlow节点](../../raw/application-user-guide/llm-application/workflow-application/appflow-node.md)
- [MCP节点](../../raw/application-user-guide/llm-application/workflow-application/mcp-node.md)
- [应用组件节点](../../raw/application-user-guide/llm-application/workflow-application/component-node.md)
- [变量赋值节点](../../raw/application-user-guide/llm-application/workflow-application/variable-assignment-node.md)
- [变量处理节点](../../raw/application-user-guide/llm-application/workflow-application/variable-processing-node.md)
- [文档解析节点](../../raw/application-user-guide/llm-application/workflow-application/document-extraction-node.md)
- [图片解析节点](../../raw/application-user-guide/llm-application/workflow-application/image-extraction-node.md)
- [视频解析节点](../../raw/application-user-guide/llm-application/workflow-application/video-extraction-node.md)
- [音频解析节点](../../raw/application-user-guide/llm-application/workflow-application/audio-extraction-node.md)
- [数据连接器节点](../../raw/application-user-guide/llm-application/workflow-application/data-connector-node.md)
- [工具接入](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-application-mcp.md)
- [API 开发指南](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-app-develop-guide.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)


