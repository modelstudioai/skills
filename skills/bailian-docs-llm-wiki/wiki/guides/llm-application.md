# llm application

百炼平台的 LLM 应用提供三种核心构建范式：智能体（Agent）、工作流（Workflow）和高代码应用，分别面向零代码、低代码和专业开发者场景。它们通过集成知识库检索增强（RAG）、外部工具调用（MCP/插件）、多模态解析等能力，突破大模型在私有知识、实时信息、流程控制和复杂任务规划等方面的原生局限，支持快速构建可解决真实业务问题的 AI 应用。

## 支持的模型/功能

- **智能体应用**：支持两类版本。新版智能体（Agent 2.0）将知识库、MCP 等统一为工具，由模型自主规划调用顺序，并完整展示“规划-执行-反思”链路；旧版（Agent 1.0）则先检索知识库再决策是否调用其他工具 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。两者均支持千问系列文本与多模态模型（如 Qwen-VL-Max），但文件处理逻辑存在差异：千问-VL 系列即使关闭预解析，也能直接解析图片和视频；其余模型则严格依赖预解析开关状态。
  
- **工作流应用**：提供 20+ 类节点，覆盖全栈能力：
  - *基础控制*：开始/结束、条件判断、循环、批处理、流程输出；
  - *AI 能力*：大模型、知识库、意图分类、参数提取、多模态生成、智能体创建/群组；
  - *工具集成*：API、函数计算（FC）、插件、MCP、AppFlow、数据连接器；
  - *多模态解析*：文档、图片、音频、视频解析节点，均支持结构化输出供下游引用 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。
  
- **高代码应用**：面向 Python 开发者，支持 Serverless Function 和 K8s 两种部署方式，可通过 MCP 协议接入知识库、MCP 服务、应用组件及数据连接器，并提供 `GET /health` 健康检查接口和 `/process` 对话入口的强制规范 [API 开发指南](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-app-develop-guide.md)。

> **注意**：文档 34 中关于文件问答的支持模型列表存在大量重复链接（如多次引用 `raw/model-user-guide/get-started-with-models/models.md`）且未列出具体模型名，与文档 2、3 中明确列出的 `千问-Plus-Latest`、`千问-Max`、`Qwen-VL-Plus-Latest` 等实际可用模型不符，应以控制台实时显示为准。

## 关键参数

- **模型选择与路由**：
  - Agent 2.0 提供 `AUTO`（自动路由）、`性能`、`均衡`、`经济` 四档智能模式，其中 `AUTO` 根据任务复杂度（含上下文 Token 数）动态分配模型，当上下文 >200K 时至少路由至 `性能` 档；各档位计费独立 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
  - 工作流中各 AI 节点（大模型、意图分类、参数提取等）均支持独立配置 `temperature`（默认 0.7）、`top_p`（默认 0.8）、`最长回复长度`（默认 1024）及 `enable_thinking`（开启思考模式）等通用参数。

- **文件处理**：
  - 智能体应用支持三种文件问答模式：`全文引用`（受限于上下文长度）、`切片检索`（RAG，需配置切片策略）、`自定义处理`（模型自主调用工具）[文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。
  - 工作流中解析类节点有明确限制：文档解析单文件 ≤150 MB/1.5 万页；图片 ≤20 MB；音频/视频 ≤512 MB；所有解析节点均不计费。

- **流程控制**：
  - 循环节点支持 `数组循环`（按元素遍历）和 `指定次数循环`，并提供 `中间变量` 实现跨轮次状态传递；终止条件仅能基于中间变量判断。
  - 批处理节点默认并行数为 5，支持设置 `批处理次数上限`（默认 30）以防止资源耗尽；其与循环节点的核心区别在于并行 vs 串行执行 [批处理节点](../../raw/application-user-guide/llm-application/workflow-application/batch-node.md)。

## 使用方式

- **创建与配置**：
  - 智能体：控制台选择 `Agent 2.0` 或 `Agent 1.0`，配置模型、系统提示词、知识库/RAG、内置工具（如 `bash`、`write`）。
  - 工作流：通过拖拽或 `+` 按钮添加节点，在画布上编排逻辑；关键节点如 `条件判断`、`循环`、`批处理` 需配置条件组、循环类型、批处理数组等核心参数。
  - 高代码应用：控制台创建后，选择 `Serverless Function` 或 `K8s` 部署方式，上传 `.whl` 包或使用模板；代码中必须包含 `main.py` 入口和 `/health` 接口。

- **调试与测试**：
  - 工作流支持在测试面板中逐轮查看循环/批处理节点的输入输出；知识库节点提供 `调试召回效果` 功能，可验证 RAG 检索质量。
  - 智能体应用支持在对话界面直接上传文件并提问，实时验证文件问答效果。

- **集成与调用**：
  - 所有应用发布后均可通过 API 调用：智能体应用参考 [新版智能体应用 API](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)，工作流应用参考 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
  - 高代码应用部署后自动生成公网 API 地址，遵循 AgentScope API 协议规范。

## 限制和注意事项

- **资源与配额**：
  - 智能体应用单会话文件上限 10 个，单文件 ≤10 MB，且文件仅在当前会话有效 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。
  - 工作流中循环节点最大循环次数为 1000，批处理节点最大批处理次数为 100；函数计算节点超时固定为 60 秒，不可修改。

- **功能约束**：
  - 循环体内禁止嵌套循环或批处理节点；批处理体内禁止添加流程输出节点；条件判断节点不输出数据变量，仅控制流程走向。
  - 变量处理节点的 `JSON输出` 模式仅支持单层键值对，无法生成嵌套 JSON 结构；若需嵌套，须在下游节点二次处理。

- **权限与依赖**：
  - 高代码应用部署需提前授权函数计算（FC）和 API 网关服务角色；调用外部 API 时，需将百炼服务 IP（`47.93.216.17` 和 `39.105.109.77`）加入目标服务白名单 [API节点](../../raw/application-user-guide/llm-application/workflow-application/api-node.md)。
  - 智能体群组节点要求子智能体必须已发布；应用组件节点要求组件已创建并发布至组件管理页面。

## 来源文档

- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [条件判断节点](../../raw/application-user-guide/llm-application/workflow-application/conditional-node.md)
- [开始和结束节点](../../raw/application-user-guide/llm-application/workflow-application/start-end-node.md)
- [流程输出节点](../../raw/application-user-guide/llm-application/workflow-application/process-output-node.md)
- [循环节点](../../raw/application-user-guide/llm-application/workflow-application/loop-node.md)
- [批处理节点](../../raw/application-user-guide/llm-application/workflow-application/batch-node.md)
- [意图分类节点](../../raw/application-user-guide/llm-application/workflow-application/intent-node.md)
- [知识库节点](../../raw/application-user-guide/llm-application/workflow-application/knowledge-base-node.md)
- [大模型节点](../../raw/application-user-guide/llm-application/workflow-application/llm-node.md)
- [参数提取节点](../../raw/application-user-guide/llm-application/workflow-application/parameter-extraction-node.md)
- [多模态生成节点](../../raw/application-user-guide/llm-application/workflow-application/multimodal-generation-node.md)
- [智能体创建节点](../../raw/application-user-guide/llm-application/workflow-application/agent-create-node.md)
- [智能体群组节点](../../raw/application-user-guide/llm-application/workflow-application/agent-group-node.md)
- [API节点](../../raw/application-user-guide/llm-application/workflow-application/api-node.md)
- [函数计算节点](../../raw/application-user-guide/llm-application/workflow-application/fc-node.md)
- [插件节点](../../raw/application-user-guide/llm-application/workflow-application/plugin-node.md)
- [脚本节点](../../raw/application-user-guide/llm-application/workflow-application/script-node.md)
- [MCP节点](../../raw/application-user-guide/llm-application/workflow-application/mcp-node.md)
- [应用组件节点](../../raw/application-user-guide/llm-application/workflow-application/component-node.md)
- [AppFlow节点](../../raw/application-user-guide/llm-application/workflow-application/appflow-node.md)
- [变量处理节点](../../raw/application-user-guide/llm-application/workflow-application/variable-processing-node.md)
- [变量赋值节点](../../raw/application-user-guide/llm-application/workflow-application/variable-assignment-node.md)
- [文档解析节点](../../raw/application-user-guide/llm-application/workflow-application/document-extraction-node.md)
- [图片解析节点](../../raw/application-user-guide/llm-application/workflow-application/image-extraction-node.md)
- [音频解析节点](../../raw/application-user-guide/llm-application/workflow-application/audio-extraction-node.md)
- [视频解析节点](../../raw/application-user-guide/llm-application/workflow-application/video-extraction-node.md)
- [数据连接器节点](../../raw/application-user-guide/llm-application/workflow-application/data-connector-node.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [工具接入](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-application-mcp.md)
- [API 开发指南](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-app-develop-guide.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)


