# llm application

百炼平台的 LLM 应用提供三种核心构建模式：智能体（Agent）、工作流（Workflow）和高代码应用，分别面向零代码、低代码和专业开发者场景。它们通过集成知识库检索（RAG）、外部工具调用（MCP/插件）、多模态解析等能力，突破大模型在私有知识访问、实时信息获取和复杂任务规划上的原生局限，支持从简单问答到多角色协同的全栈 AI 应用开发。

## 支持的模型与功能

- **智能体应用**：支持新版 Agent 2.0（推荐）与旧版 Agent 1.0。Agent 2.0 将知识库、MCP 等统一为可自主规划调用的工具，并完整展示“规划-执行-反思”链路；Agent 1.0 则采用先检索后决策的串行流程 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
- **工作流应用**：提供可视化节点编排能力，涵盖基础逻辑（条件判断、循环、批处理）、AI 节点（大模型、意图分类、参数提取、知识库）、多模态节点（图像/视频/音频生成）及工具节点（API、函数计算、MCP、AppFlow）。其中，[条件判断节点](../../raw/application-user-guide/llm-application/workflow-application/conditional-node.md) 支持“所有/任一”条件组逻辑，适用于意图路由等动态分支场景。
- **高代码应用**：面向 Python 开发者，支持 Serverless Function 或 K8s 部署，通过 MCP 协议接入知识库、MCP 服务、应用组件和数据连接器，实现深度定制 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。

> **注意**：文档 32（文件问答）中列出的“千问3-Coder-Plus”“千问-QwQ-Preview”等模型名称未在其他文档（如文档 1 的模型选择器说明或文档 29 的高代码模板说明）中被明确列为正式支持型号，且其命名方式与主流千问系列（如 `qwen-plus`、`qwen-max`）不一致。建议以控制台实际可选模型为准，该列表可能存在过时或占位符内容。

## 关键参数

- **模型参数**：通用参数包括 `temperature`（控制随机性，范围通常为 [0, 2)，默认 0.7）、`top_p`（控制多样性，默认 0.8）、`max_output_tokens`（最长回复长度，默认 1024）。Agent 2.0 特有 `enable_thinking` 参数，开启后增强反思能力；工作流各 AI 节点（如大模型、意图分类、参数提取）均支持此参数及 `thinking_budget`（默认 4000 tokens）。
- **智能体专属参数**：
  - Agent 2.0 提供 `AUTO` 智能模式（自动路由至性能/均衡/经济档），其路由逻辑依赖任务复杂度与上下文 Token 数（>200K 时至少启用性能档）；
  - Agent 1.0 支持 `携带的上下文轮数` 参数，用于控制历史对话记忆长度。
- **工作流节点特有参数**：
  - 循环节点：`循环次数`（1–1000）、`中间变量`（用于跨轮次状态传递）、`终止条件`（仅基于中间变量判断）；
  - 批处理节点：`并行运行数量`（默认 5）、`批处理次数上限`（默认 30）；
  - 多模态生成节点：`随机种子`（控制结果可复现性）、`prompt_extend`（启用后由大模型智能改写提示词）。

## 使用方式

- **创建入口**：统一通过百炼控制台 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) → **创建应用** 启动，按类型选择“智能体应用”“工作流应用”或“高代码应用”。
- **智能体配置**：
  - Agent 2.0：在模型选择器中启用 `AUTO` 模式或指定 `千问-Max` 等强工具调用模型；通过“预解析文件”开关控制文件是否由系统主动解析（关闭时需智能体自行调用工具处理 URL）；内置 `bash`/`write`/`read` 工具需手动开启 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
- **工作流编排**：
  - 从开始节点定义输入（`query`、`imageList` 等），通过拖拽或 `+` 按钮添加节点；
  - 条件判断、循环、批处理等逻辑节点支持多分支连接；大模型节点可配置单次/批量处理模式；
  - 文件/图片/音视频/视频解析节点均支持 URL 或 File 变量输入，并输出结构化字段（如 `layout`、`images`、`segments`）供下游引用。
- **高代码开发**：
  - 入口文件必须为 `main.py`，需提供 `/health` 健康检查接口；
  - 工具接入需在代码中通过 `fastmcp.Client` 调用 MCP 服务，控制台添加仅为元数据管理 [工具接入](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-application-mcp.md)。

## 限制和注意事项

- **文件处理限制**：
  - 智能体会话级上传：单文件 ≤10MB，单次会话最多 10 个文件，且文件仅在当前会话有效 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)；
  - 工作流节点：文档解析单文件 ≤150MB/1.5万页；图片解析 ≤20MB；音视频解析 ≤512MB；均仅支持单文件。
- **模型与能力兼容性**：
  - 千问-VL 系列模型具备原生多模态能力，即使关闭“预解析文件”，也能直接解析图片/视频；其他文本模型则严格依赖预解析开关 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)；
  - `enable_search`（联网搜索）参数并非所有模型都支持，若控制台未显示该选项，则当前模型不支持。
- **工作流执行约束**：
  - 循环体内禁止嵌套循环或批处理节点；
  - 批处理体与循环体均不支持添加流程输出节点；
  - API 节点调用外部服务前，需将百炼服务 IP（`47.93.216.17` 和 `39.105.109.77`）加入目标服务器白名单 [API节点](../../raw/application-user-guide/llm-application/workflow-application/api-node.md)。
- **高代码部署要求**：使用命令行部署 `.whl` 包时，需添加 `--telemetry enable` 参数才能启用应用观测功能 [API 开发指南](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-app-develop-guide.md)。

## 来源文档

- [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [条件判断节点](../../raw/application-user-guide/llm-application/workflow-application/conditional-node.md)
- [开始和结束节点](../../raw/application-user-guide/llm-application/workflow-application/start-end-node.md)
- [循环节点](../../raw/application-user-guide/llm-application/workflow-application/loop-node.md)
- [批处理节点](../../raw/application-user-guide/llm-application/workflow-application/batch-node.md)
- [流程输出节点](../../raw/application-user-guide/llm-application/workflow-application/process-output-node.md)
- [大模型节点](../../raw/application-user-guide/llm-application/workflow-application/llm-node.md)
- [知识库节点](../../raw/application-user-guide/llm-application/workflow-application/knowledge-base-node.md)
- [意图分类节点](../../raw/application-user-guide/llm-application/workflow-application/intent-node.md)
- [参数提取节点](../../raw/application-user-guide/llm-application/workflow-application/parameter-extraction-node.md)
- [多模态生成节点](../../raw/application-user-guide/llm-application/workflow-application/multimodal-generation-node.md)
- [智能体创建节点](../../raw/application-user-guide/llm-application/workflow-application/agent-create-node.md)
- [智能体群组节点](../../raw/application-user-guide/llm-application/workflow-application/agent-group-node.md)
- [API节点](../../raw/application-user-guide/llm-application/workflow-application/api-node.md)
- [脚本节点](../../raw/application-user-guide/llm-application/workflow-application/script-node.md)
- [函数计算节点](../../raw/application-user-guide/llm-application/workflow-application/fc-node.md)
- [插件节点](../../raw/application-user-guide/llm-application/workflow-application/plugin-node.md)
- [AppFlow节点](../../raw/application-user-guide/llm-application/workflow-application/appflow-node.md)
- [应用组件节点](../../raw/application-user-guide/llm-application/workflow-application/component-node.md)
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
- [MCP节点](../../raw/application-user-guide/llm-application/workflow-application/mcp-node.md)
- [变量处理节点](../../raw/application-user-guide/llm-application/workflow-application/variable-processing-node.md)


