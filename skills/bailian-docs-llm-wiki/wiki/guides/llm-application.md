# llm application

`llm application` 是阿里云百炼平台提供的面向大语言模型（LLM）的三类核心应用构建模式：智能体（Agent）、工作流（Workflow）和高代码应用（Rich Code Application）。它们分别对应零代码、低代码和专业代码开发范式，支持通过集成知识库、外部工具（MCP/插件）、多模态解析等能力，突破大模型在私有知识访问、实时信息获取、流程控制与复杂任务规划等方面的原生局限，快速构建生产级 AI 应用。

## 支持的模型/功能

平台提供统一模型底座支持，但不同应用类型对模型能力的要求存在差异：

- **智能体应用**：推荐选用具备强工具调用与多步规划能力的模型，如 `千问-Max` 系列；新版 Agent 2.0 明确要求模型支持 `enable_thinking` 参数以启用深度反思链路 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。对于文件问答场景，视觉理解模型（如 `千问-VL-Max`、`千问-VL-Plus`）可直接解析图片/视频，而文本模型需依赖预解析开关控制文件处理方式 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。
- **工作流应用**：各节点（如大模型节点、意图分类节点、参数提取节点）均支持独立配置模型，可混合使用不同模型。例如，意图分类节点可选用专用小模型提升响应速度，而主生成节点选用 `千问-Plus-Latest` 保证质量 [意图分类节点](../../raw/application-user-guide/llm-application/workflow-application/intent-node.md)。
- **高代码应用**：开发者完全掌控模型调用逻辑，可通过 `fastmcp.Client` 接入任意支持 MCP 协议的模型服务，包括自定义部署模型 [工具接入](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-application-mcp.md)。

> **注意**：文档 33 中列出的“支持的模型”表格存在大量重复链接（如多个 `[选择模型](...)`），且未明确区分各模型在智能体、工作流或高代码场景下的实际兼容性，该列表应以控制台实时显示为准，不可作为权威依据。

## 关键参数

各类应用共享部分通用参数，但配置入口与语义略有不同：

- **最长回复长度**：所有模型调用节点（智能体配置、大模型节点、意图分类节点等）均支持此参数，单位为 token，用于限制模型输出长度。默认值通常为 `1024`，但智能体应用中部分模型上限更高 [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)。
- **temperature（温度系数）**：控制生成随机性，范围 `[0, 2)`，值越高越多样。该参数在智能体、工作流各 AI 节点及高代码应用代码中均需显式设置。
- **enable_thinking**：启用模型深度思考模式，输出推理过程。此参数仅对支持思考能力的模型有效，且在 Agent 2.0 的模型设置中为关键开关；在工作流的大模型节点、意图分类节点等处也作为可选配置出现 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
- **上下文管理**：智能体应用通过“携带的上下文轮数”控制历史对话长度；工作流则通过“记忆”功能（本节点缓存/自定义缓存）实现，需配合 `historyList` 等内置变量使用 [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)。

## 使用方式

根据业务复杂度与开发能力选择对应范式：

- **智能体（Agent）**：适用于开放式对话与自主决策场景（如客服、旅行规划）。创建后通过自然语言配置系统提示词、绑定知识库与插件即可运行。Agent 2.0 提供完整“规划-执行-反思”链路可视化 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
- **工作流（Workflow）**：适用于固定流程自动化（如报告生成、订单审批）。通过拖拽节点（开始/结束、条件判断、批处理、大模型、知识库、MCP、API 等）编排执行链路，支持并行、循环、分支等复杂控制流 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。
- **高代码应用**：面向专业开发者，基于 Python 项目结构（含 `main.py` 入口、`requirements.txt`）一键部署为 Serverless 或 K8s 服务，支持 MCP 工具接入与自定义前端 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。

## 限制和注意事项

- **文件处理限制**：智能体应用单会话最多上传 10 个文件，单文件不超过 10MB；工作流中各解析节点有独立限制（如文档解析节点单文件 ≤150MB，图片解析节点 ≤20MB）[文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。
- **模型上下文窗口**：RAG 检索结果与用户输入共同占用模型上下文。当上下文 Token 数超过 200K 时，Agent 2.0 的 AUTO 模式将强制路由至“性能”档位以保障处理效果 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
- **节点嵌套限制**：工作流中，批处理节点与循环节点互斥，批处理体内禁止嵌套循环节点，循环体内禁止嵌套批处理节点 [批处理节点](../../raw/application-user-guide/llm-application/workflow-application/batch-node.md)。
- **权限与网络**：调用外部 API 时，需将百炼服务 IP（`47.93.216.17` 和 `39.105.109.77`）加入目标服务白名单；高代码应用部署需提前授权函数计算（FC）与 API 网关角色 [API节点](../../raw/application-user-guide/llm-application/workflow-application/api-node.md)。

## 来源文档

- [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [开始和结束节点](../../raw/application-user-guide/llm-application/workflow-application/start-end-node.md)
- [条件判断节点](../../raw/application-user-guide/llm-application/workflow-application/conditional-node.md)
- [批处理节点](../../raw/application-user-guide/llm-application/workflow-application/batch-node.md)
- [流程输出节点](../../raw/application-user-guide/llm-application/workflow-application/process-output-node.md)
- [循环节点](../../raw/application-user-guide/llm-application/workflow-application/loop-node.md)
- [知识库节点](../../raw/application-user-guide/llm-application/workflow-application/knowledge-base-node.md)
- [大模型节点](../../raw/application-user-guide/llm-application/workflow-application/llm-node.md)
- [意图分类节点](../../raw/application-user-guide/llm-application/workflow-application/intent-node.md)
- [参数提取节点](../../raw/application-user-guide/llm-application/workflow-application/parameter-extraction-node.md)
- [多模态生成节点](../../raw/application-user-guide/llm-application/workflow-application/multimodal-generation-node.md)
- [智能体创建节点](../../raw/application-user-guide/llm-application/workflow-application/agent-create-node.md)
- [API节点](../../raw/application-user-guide/llm-application/workflow-application/api-node.md)
- [智能体群组节点](../../raw/application-user-guide/llm-application/workflow-application/agent-group-node.md)
- [函数计算节点](../../raw/application-user-guide/llm-application/workflow-application/fc-node.md)
- [脚本节点](../../raw/application-user-guide/llm-application/workflow-application/script-node.md)
- [插件节点](../../raw/application-user-guide/llm-application/workflow-application/plugin-node.md)
- [MCP节点](../../raw/application-user-guide/llm-application/workflow-application/mcp-node.md)
- [应用组件节点](../../raw/application-user-guide/llm-application/workflow-application/component-node.md)
- [变量处理节点](../../raw/application-user-guide/llm-application/workflow-application/variable-processing-node.md)
- [AppFlow节点](../../raw/application-user-guide/llm-application/workflow-application/appflow-node.md)
- [文档解析节点](../../raw/application-user-guide/llm-application/workflow-application/document-extraction-node.md)
- [变量赋值节点](../../raw/application-user-guide/llm-application/workflow-application/variable-assignment-node.md)
- [图片解析节点](../../raw/application-user-guide/llm-application/workflow-application/image-extraction-node.md)
- [音频解析节点](../../raw/application-user-guide/llm-application/workflow-application/audio-extraction-node.md)
- [视频解析节点](../../raw/application-user-guide/llm-application/workflow-application/video-extraction-node.md)
- [数据连接器节点](../../raw/application-user-guide/llm-application/workflow-application/data-connector-node.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [工具接入](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-application-mcp.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)
- [API 开发指南](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-app-develop-guide.md)


