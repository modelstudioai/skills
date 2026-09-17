# llm application

`llm application` 是阿里云百炼平台提供的核心 AI 应用构建能力，支持通过零代码、低代码或高代码方式，将大语言模型与知识库、外部工具（MCP/[插件](../concepts/plugin.md)）、[多模态](../concepts/multi-modal.md)解析等能力深度集成，构建可解决真实业务问题的智能应用。其核心形态包括智能体（Agent）、工作流（Workflow）和高代码应用三类，分别面向不同开发能力和场景复杂度需求。

## 支持的模型/功能

- **智能体（Agent）**：分为 Agent 1.0 和 Agent 2.0 两个版本。Agent 2.0 将知识库、MCP 等统一为工具，由模型自主规划调用顺序，并完整展示“规划-执行-反思”链路；而 Agent 1.0 则采用先检索后决策的串行模式 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
- **工作流（Workflow）**：提供可视化节点编排能力，包含开始/结束节点、条件判断、循环、批处理、大模型、知识库、参数提取、意图分类、[多模态](../concepts/multi-modal.md)生成、MCP、API、函数计算、脚本、[插件](../concepts/plugin.md)、AppFlow、数据连接器、文档/图片/音频/视频解析、变量处理、变量赋值等数十种节点类型，支持复杂任务的确定性编排 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。  
- **高代码应用**：面向专业开发者，支持基于 Python 项目结构一键部署 Serverless 或 K8s 后端服务，内置 MCP 工具接入、可观测性、API 网关等企业级能力 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。  
- **[多模态](../concepts/multi-modal.md)与文件处理**：支持文档、图片、音视频的解析与问答，提供全文引用、切片检索（RAG）和自定义处理三种模式，适配不同长度与交互需求 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。

> **注意**：文档 33 中关于“单文件不超过 10MB”的限制与文档 25（文档解析节点，单文件 ≤150 MB）、文档 27（图片解析节点，≤20 MB）、文档 28/29（音视频解析节点，≤512 MB）存在明显矛盾。实际能力以各节点独立配置为准，文件问答功能的上传限制仅适用于智能体应用的会话级临时文件，不约束工作流中专用解析节点的处理能力。

## 关键参数

- **模型通用参数**：所有支持模型的节点（大模型、参数提取、意图分类、智能体创建/群组等）均支持 `temperature`（控制随机性）、`top_p`（控制多样性）、`最长回复长度`（输出 token 上限）及 `enable_thinking`（开启思考模式）等基础参数。思考模式下需额外配置 `thinking_budget`（思维链最大 token 数）[大模型节点](../../raw/application-user-guide/llm-application/workflow-application/llm-node.md)。  
- **Agent 特有参数**：Agent 2.0 提供 `智能模式`（AUTO/性能/均衡/经济），其中 AUTO 档位根据任务复杂度与上下文长度（如超 200K tokens 强制路由至性能档）动态选择模型，计费按统一刊例价 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
- **工作流节点特有参数**：  
  - 批处理节点：`并行运行数量`（默认 5）、`批处理次数上限`（默认 30）；  
  - 循环节点：支持 `中间变量` 跨轮次传递及 `终止条件`（基于中间变量判断）；  
  - 知识库节点：`topK`（召回片段数，默认 10）、`知识库描述`（用于智能调用模式）；  
  - 多模态生成节点：`随机种子`（控制结果可复现性）、`prompt_extend`（提示词智能改写）等。

## 使用方式

- **智能体应用**：在控制台「应用管理」→「创建应用」→ 选择「智能体应用 > Agent 2.0」，配置模型、系统提示词、预解析文件开关及内置工具（`bash`/`write`/`read`）即可快速启动 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
- **工作流应用**：通过拖拽或 + 按钮添加节点，在画布上编排逻辑。例如，典型 RAG 流程为：`开始节点` → `知识库节点` → `大模型节点` → `结束节点`；复杂任务可结合 `条件判断节点` 分支路由或 `循环节点` 批量处理 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。  
- **高代码应用**：使用 `agentscope-runtime` CLI 工具上传 `.whl` 包，入口文件必须为 `main.py`，且需实现 `/health` 健康检查接口；工具接入需在代码中通过 `fastmcp.Client` 调用，控制台添加仅作元信息管理 [API 开发指南](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-app-develop-guide.md)。

## 限制和注意事项

- **上下文与 [Token](../concepts/token.md) 限制**：Agent 2.0 的 AUTO 模式在上下文 [Token](../concepts/token.md) 超过 200K 时强制路由至性能档；工作流中知识库召回内容占用模型上下文，需合理设置 `topK` 避免超限 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
- **文件处理范围**：智能体应用中上传的文件仅在当前会话有效，刷新即丢失；而工作流中的解析节点（如文档/图片/音视频解析）支持更大文件（最高 512 MB）且结果持久化为变量供下游复用 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。  
- **节点能力边界**：  
  - `大模型节点` 不支持直接调用[插件](../concepts/plugin.md)，需使用 `智能体创建节点` 实现知识库与工具集成；  
  - `批处理节点` 内部禁止嵌套批处理或循环；  
  - `循环节点` 的 `终止条件` 仅支持基于中间变量判断，不可引用数组元素或全局变量 [循环节点](../../raw/application-user-guide/llm-application/workflow-application/loop-node.md)。  
- **权限与网络**：调用 API 节点时，需将百炼服务 IP（47.93.216.17 / 39.105.109.77）加入目标服务白名单；高代码应用部署需提前授权函数计算（FC）与 API 网关角色 [API节点](../../raw/application-user-guide/llm-application/workflow-application/api-node.md)。

## 来源文档

- [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [开始和结束节点](../../raw/application-user-guide/llm-application/workflow-application/start-end-node.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [条件判断节点](../../raw/application-user-guide/llm-application/workflow-application/conditional-node.md)
- [批处理节点](../../raw/application-user-guide/llm-application/workflow-application/batch-node.md)
- [循环节点](../../raw/application-user-guide/llm-application/workflow-application/loop-node.md)
- [大模型节点](../../raw/application-user-guide/llm-application/workflow-application/llm-node.md)
- [流程输出节点](../../raw/application-user-guide/llm-application/workflow-application/process-output-node.md)
- [知识库节点](../../raw/application-user-guide/llm-application/workflow-application/knowledge-base-node.md)
- [参数提取节点](../../raw/application-user-guide/llm-application/workflow-application/parameter-extraction-node.md)
- [意图分类节点](../../raw/application-user-guide/llm-application/workflow-application/intent-node.md)
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
- [变量处理节点](../../raw/application-user-guide/llm-application/workflow-application/variable-processing-node.md)
- [文档解析节点](../../raw/application-user-guide/llm-application/workflow-application/document-extraction-node.md)
- [变量赋值节点](../../raw/application-user-guide/llm-application/workflow-application/variable-assignment-node.md)
- [图片解析节点](../../raw/application-user-guide/llm-application/workflow-application/image-extraction-node.md)
- [音频解析节点](../../raw/application-user-guide/llm-application/workflow-application/audio-extraction-node.md)
- [视频解析节点](../../raw/application-user-guide/llm-application/workflow-application/video-extraction-node.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [数据连接器节点](../../raw/application-user-guide/llm-application/workflow-application/data-connector-node.md)
- [API 开发指南](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-app-develop-guide.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)
- [工具接入](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-application-mcp.md)


