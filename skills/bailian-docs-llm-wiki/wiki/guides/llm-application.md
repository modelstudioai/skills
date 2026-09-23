# llm application

百炼平台的 LLM Application 是面向真实业务场景的 AI 应用构建体系，提供智能体（Agent）、工作流（Workflow）和高代码应用三类核心范式，分别覆盖零代码决策、低代码编排与专业级工程化部署需求。所有类型均深度集成知识库检索增强（RAG）、MCP 工具调用、多模态解析等能力，支持从私有数据接入到复杂任务规划的端到端闭环。

## 支持的模型/功能

- **智能体（Agent）**：支持 Agent 1.0 和 Agent 2.0 两代架构。Agent 2.0 将知识库、MCP 等统一为工具，支持自主规划与完整过程回溯；Agent 1.0 采用分阶段调度（先检索后决策），适合意图单一的轻量场景。推荐优先使用 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
- **工作流（Workflow）**：提供 20+ 类节点，覆盖逻辑控制（条件判断、循环、批处理）、AI 处理（大模型、意图分类、参数提取）、多模态解析（文档、图片、音频、视频）、外部集成（API、函数计算、MCP、AppFlow、数据连接器）及组件复用（应用组件、智能体群组）。其中 [智能体群组节点](../../raw/application-user-guide/llm-application/workflow-application/agent-group-node.md) 支持多智能体协同调度，[参数提取节点](../../raw/application-user-guide/llm-application/workflow-application/parameter-extraction-node.md) 支持 VL 模型对图片/视频的结构化信息抽取。
- **高代码应用**：基于 Python 的 Serverless Function 或 K8s 部署模式，支持 MCP 协议接入知识库、MCP 服务、应用组件和数据连接器，并提供 `AgentScope-AI` CLI 工具链实现本地开发→打包→一键部署全流程。

> **注意**：文档 33 中关于“文件问答”支持模型的列表存在大量重复占位符（如 `[选择模型](...)`），且未明确标注是否适用于所有智能体版本；实际可用模型请以控制台实时下拉菜单为准，该文档已过时，不可作为选型依据。

## 关键参数

| 参数类别 | 适用范围 | 关键说明 |
|----------|----------|----------|
| **模型参数** | 所有含模型选择的节点（大模型、意图分类、参数提取、智能体创建、智能体群组等） | `temperature`（默认 0.7）、`top_p`（默认 0.8）、`enable_thinking`（开启思考链）、`thinking_budget`（思考 token 上限，默认 4000）；`result_format` 默认为 `message`；`enable_search` 仅部分模型支持。 |
| **上下文控制** | 智能体（Agent 1.0）、大模型节点（单次模式） | Agent 1.0 支持配置“携带的上下文轮数”（1–50）；大模型节点支持“本节点缓存”或“自定义缓存”（如 `historyList`）；工作流中需显式传递 `historyList` 变量以维持多轮对话状态。 |
| **文件处理** | 智能体、文档/图片/音频/视频解析节点 | 智能体支持“全文引用”“切片检索（RAG）”“自定义处理”三种模式；解析节点有严格格式与大小限制（如文档 ≤150 MB、图片 ≤20 MB、音频 ≤512 MB、视频 ≤512 MB）。 |
| **执行控制** | 循环、批处理、API、脚本、插件、MCP 等节点 | 循环节点支持“数组循环”与“指定次数”，并提供中间变量实现跨轮次状态传递；批处理节点支持并行数量（默认 5）与批处理上限（默认 30）；API 节点超时默认 5 秒，可重试；所有支持失败重试的节点默认最大重试 3–5 次。 |

## 使用方式

- **创建入口**：统一通过百炼控制台 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) → “创建应用” 进入，按类型选择模板。
- **智能体配置重点**：在 Agent 2.0 中，模型选择器支持 `AUTO`（自动路由）、`性能`、`均衡`、`经济` 四档，`AUTO` 按任务复杂度动态匹配模型，计费统一；系统提示词支持嵌入 `/` 自定义变量；预解析文件开关决定是否由系统主动解析上传文件。
- **工作流编排要点**：
  - 开始节点定义 `query`（必填）、`historyList`（多轮必需）、`imageList`（多模态必需）等内置变量；
  - 条件判断节点分支间为“或”关系，每个条件组内可设“所有/任一”逻辑；
  - 循环体与批处理体均禁止嵌套同类节点，且不支持添加流程输出节点；
  - 流程输出节点用于中间结果流式返回，结束节点用于最终结果输出（仅一个）。
- **高代码部署流程**：控制台创建 → 选择 Serverless/K8s → 提交模版代码或 `.whl` 包 → 授权 FC/API 网关 → 启动；入口文件必须为 `main.py`，需暴露 `/health` 健康检查接口；工具接入需在代码中通过 `fastmcp.Client` 实现，控制台配置仅作展示。

## 限制和注意事项

- **资源与配额**：单个会话文件上传上限 10 个且单文件 ≤10 MB（智能体）；文档解析单文件 ≤150 MB；图片 ≤20 MB；音视频 ≤512 MB；循环次数上限 1000；批处理数组长度受“批处理次数上限”约束（默认 30）。
- **模型兼容性**：非多模态模型（如纯文本千问系列）无法直接解析图片/视频，必须开启“预解析文件”；千问-VL 系列模型即使关闭预解析，也能直接解析图片/视频，但对非图像/视频文件仍依赖预解析开关。
- **节点行为差异**：
  - 大模型节点（批量模式）不支持记忆、失败重试与异常处理；
  - 智能体创建节点生成的智能体仅运行时存在，不创建独立应用；
  - 智能体群组节点的决策模型不生成最终答案，仅调度子智能体，`result.agResult` 才是最终输出；
  - AppFlow 节点不支持[流式输出](../concepts/streaming-output.md)，如需流式效果需接大模型节点二次处理。
- **安全与网络**：调用外部 API 时，需将百炼服务 IP（`47.93.216.17` 和 `39.105.109.77`）加入目标服务白名单；函数计算、AppFlow、MCP 等云资源节点要求账号归属同一主账号或已授权。

## 来源文档

- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
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
- [智能体创建节点](../../raw/application-user-guide/llm-application/workflow-application/agent-create-node.md)
- [API节点](../../raw/application-user-guide/llm-application/workflow-application/api-node.md)
- [函数计算节点](../../raw/application-user-guide/llm-application/workflow-application/fc-node.md)
- [脚本节点](../../raw/application-user-guide/llm-application/workflow-application/script-node.md)
- [插件节点](../../raw/application-user-guide/llm-application/workflow-application/plugin-node.md)
- [MCP节点](../../raw/application-user-guide/llm-application/workflow-application/mcp-node.md)
- [AppFlow节点](../../raw/application-user-guide/llm-application/workflow-application/appflow-node.md)
- [应用组件节点](../../raw/application-user-guide/llm-application/workflow-application/component-node.md)
- [变量处理节点](../../raw/application-user-guide/llm-application/workflow-application/variable-processing-node.md)
- [变量赋值节点](../../raw/application-user-guide/llm-application/workflow-application/variable-assignment-node.md)
- [文档解析节点](../../raw/application-user-guide/llm-application/workflow-application/document-extraction-node.md)
- [图片解析节点](../../raw/application-user-guide/llm-application/workflow-application/image-extraction-node.md)
- [多模态生成节点](../../raw/application-user-guide/llm-application/workflow-application/multimodal-generation-node.md)
- [音频解析节点](../../raw/application-user-guide/llm-application/workflow-application/audio-extraction-node.md)
- [视频解析节点](../../raw/application-user-guide/llm-application/workflow-application/video-extraction-node.md)
- [数据连接器节点](../../raw/application-user-guide/llm-application/workflow-application/data-connector-node.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [工具接入](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-application-mcp.md)
- [API 开发指南](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-app-develop-guide.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)
- [智能体群组节点](../../raw/application-user-guide/llm-application/workflow-application/agent-group-node.md)


