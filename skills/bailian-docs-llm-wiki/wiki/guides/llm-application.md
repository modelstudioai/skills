# llm application

百炼平台的 LLM Application 是面向业务场景的 AI 应用构建体系，提供智能体（Agent）、工作流（Workflow）和高代码应用三类范式，分别对应零代码、低代码和专业代码开发路径。其核心目标是突破大模型在私有知识访问、实时信息获取、流程控制与复杂任务规划等方面的原生局限，通过知识库检索增强（RAG）、外部工具调用（MCP/插件）、多步推理与[记忆](../concepts/memory.md)等能力，支撑真实业务落地。

## 支持的模型/功能

LLM Application 支持三大类能力载体：

- **智能体（Agent）**：以提示词驱动，具备自主意图理解、任务规划与工具调度能力。新版 Agent 2.0 将知识库、MCP 等统一为工具，支持完整“规划-执行-反思”链路回溯，推荐用于开放式对话与复杂任务场景 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。旧版 Agent 1.0 仍可用，但规划逻辑较线性，适用于意图单一的简单任务 [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)。
  
- **工作流（Workflow）**：通过可视化节点编排实现确定性流程控制，包含基础节点（开始/结束、条件判断、循环、批处理）、AI 节点（大模型、知识库、意图分类、参数提取、多模态生成）、工具节点（API、函数计算、插件、MCP、AppFlow、数据连接器）及解析节点（文档、图片、音频、视频）。各节点可组合使用，例如 `知识库节点 → 大模型节点` 实现 RAG 增强问答，或 `参数提取节点 → API节点` 构建结构化服务调用链 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。

- **高代码应用**：面向开发者，基于 Python 项目结构部署 Serverless 或 K8s 后端服务，支持 MCP 协议接入知识库、MCP 服务、应用组件与数据连接器，并提供自动化运维与可观测能力 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。

> **注意**：文档中提及的“智能模式”（AUTO/性能/均衡/经济）仅适用于 Agent 2.0 的模型选择器；Agent 1.0 和工作流中的大模型节点不支持该模式，需显式指定模型或档位。

## 关键参数

不同应用类型的关键参数配置存在差异：

- **Agent 应用**：核心参数包括 `temperature`（控制输出随机性）、`enable_thinking`（开启思考模式以提升反思效果，非所有模型支持）、`最长回复长度`；Agent 2.0 新增 `AUTO` 档位，由平台根据任务复杂度与上下文长度（≥200K tokens 时至少路由至“性能”档）自动路由 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。

- **Workflow 节点**：
  - 大模型节点：支持 `top_p`、`temperature`、`enable_thinking`、`thinking_budget` 及 `enable_search`（若模型支持）；
  - 知识库节点：关键参数为 `topK`（召回片段数，默认10）与 `知识库描述`（影响智能调用准确性）；
  - 条件判断节点：依赖 `变量`、`比较运算符`（如“包含”、“为空”）与 `比较值` 进行分支控制；
  - 循环节点：需配置 `循环类型`（数组循环/指定次数）、`中间变量`（跨轮次状态传递）与 `终止条件`（基于中间变量判断）。

- **高代码应用**：参数主要通过代码控制，环境变量（如 `DASHSCOPE_API_KEY`）由控制台注入，工具调用逻辑需在 `main.py` 中通过 `fastmcp.Client` 实现 [工具接入](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-application-mcp.md)。

## 使用方式

- **创建与配置**：
  - Agent：控制台选择“智能体应用 > Agent 2.0”，配置模型、系统提示词、知识库与内置工具（如 `bash`、`write`）；
  - Workflow：拖拽节点至画布，按需配置输入/输出变量、条件逻辑与参数，例如在 `开始节点` 定义 `query` 变量，在 `大模型节点` 的用户提示词中引用 `${开始/query}`；
  - 高代码：控制台选择“高代码应用”，上传 `.whl` 包或使用模板，通过 `requirements.txt` 固定依赖版本，并确保 `GET /health` 接口可用 [API 开发指南](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-app-develop-guide.md)。

- **文件处理**：
  - Agent 支持三种模式：`全文引用`（适合短文档总结）、`切片检索`（RAG，适合长文档精准问答）、`自定义处理`（依赖配置的插件/MCP 工具） [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)；
  - Workflow 提供专用解析节点：`文档解析节点`（支持 PDF/DOCX/Excel）、`图片解析节点`（区分文档类与通用图片）、`音频/视频解析节点`（输出 ASR 文本与关键帧描述），解析结果可直接被下游节点引用。

- **调用与集成**：
  - 所有应用发布后均可通过 API 调用，Agent 应用参考 [新版智能体应用 API](../../raw/application-user-guide/llm-application/new-single-agent-application.md)，Workflow 应用参考 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)；
  - 高代码应用默认暴露 `/process` 对话接口，支持流式响应，需在代码中实现 `@trace` 装饰器以启用观测 [API 开发指南](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-app-develop-guide.md)。

## 限制和注意事项

- **资源与配额**：
  - 文件上传：Agent 单会话最多 10 个文件，单文件 ≤10MB；Workflow 解析节点有独立限制（如文档 ≤150MB/1.5万页，图片 ≤20MB，音视频 ≤512MB）；
  - 循环与批处理：循环次数上限 1000，批处理默认并行数 5，需根据下游节点并发能力调整；
  - API 节点：需将百炼服务 IP（47.93.216.17、39.105.109.77）加入目标服务白名单。

- **功能边界**：
  - Agent 1.0 与 Agent 2.0 不兼容：Agent 1.0 的知识库与插件调用逻辑独立，而 Agent 2.0 统一为工具，迁移需重构；
  - Workflow 的 JSON 输出模式仅支持单层键值对，无法生成嵌套 JSON，需下游节点二次处理 [变量处理节点](../../raw/application-user-guide/llm-application/workflow-application/variable-processing-node.md)；
  - 高代码应用的 MCP 工具需在代码中显式调用，控制台添加仅用于展示与环境变量注入。

- **调试与可观测性**：
  - Workflow 支持在测试面板中翻页查看循环/批处理各轮次的详细输入输出；
  - 高代码应用可通过 [应用观测](https://bailian.console.aliyun.com/?tab=app#/app-observe) 查看调用次数、[Token](../concepts/token.md) 总量与延时，需部署时启用 `--telemetry enable`。

## 来源文档

- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [开始和结束节点](../../raw/application-user-guide/llm-application/workflow-application/start-end-node.md)
- [条件判断节点](../../raw/application-user-guide/llm-application/workflow-application/conditional-node.md)
- [循环节点](../../raw/application-user-guide/llm-application/workflow-application/loop-node.md)
- [批处理节点](../../raw/application-user-guide/llm-application/workflow-application/batch-node.md)
- [大模型节点](../../raw/application-user-guide/llm-application/workflow-application/llm-node.md)
- [流程输出节点](../../raw/application-user-guide/llm-application/workflow-application/process-output-node.md)
- [知识库节点](../../raw/application-user-guide/llm-application/workflow-application/knowledge-base-node.md)
- [意图分类节点](../../raw/application-user-guide/llm-application/workflow-application/intent-node.md)
- [参数提取节点](../../raw/application-user-guide/llm-application/workflow-application/parameter-extraction-node.md)
- [多模态生成节点](../../raw/application-user-guide/llm-application/workflow-application/multimodal-generation-node.md)
- [智能体创建节点](../../raw/application-user-guide/llm-application/workflow-application/agent-create-node.md)
- [API节点](../../raw/application-user-guide/llm-application/workflow-application/api-node.md)
- [智能体群组节点](../../raw/application-user-guide/llm-application/workflow-application/agent-group-node.md)
- [脚本节点](../../raw/application-user-guide/llm-application/workflow-application/script-node.md)
- [函数计算节点](../../raw/application-user-guide/llm-application/workflow-application/fc-node.md)
- [插件节点](../../raw/application-user-guide/llm-application/workflow-application/plugin-node.md)
- [应用组件节点](../../raw/application-user-guide/llm-application/workflow-application/component-node.md)
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
- [AppFlow节点](../../raw/application-user-guide/llm-application/workflow-application/appflow-node.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)
- [MCP节点](../../raw/application-user-guide/llm-application/workflow-application/mcp-node.md)


