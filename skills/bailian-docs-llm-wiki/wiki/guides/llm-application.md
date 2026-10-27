# llm application

百炼平台的 LLM 应用提供三种核心构建范式：智能体（Agent）、工作流（Workflow）和高代码应用，分别面向开放式自主决策、固定流程自动化和深度定制化开发场景。所有类型均支持模型调用、知识库集成、外部工具扩展及多轮对话能力，开发者可根据任务复杂度、可控性要求与团队技术栈选择最适配方案。

## 支持的模型/功能

百炼 LLM 应用支持统一的模型底座能力，覆盖文本生成、多模态理解与生成、结构化参数提取等全栈功能：

- **文本大模型**：千问系列（Qwen-Max、Qwen-Plus、Qwen2.5、Qwen3 等）为默认主力模型，支持 `enable_thinking` 深度推理模式；第三方模型（如 DeepSeek）亦可接入，但需以控制台实际可用列表为准 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
- **多模态模型**：Qwen-VL 系列（如 `Qwen-VL-Plus-Latest`）用于图片/视频解析与生成；多模态生成节点支持图像、视频、音频三类独立模型调用 [多模态生成节点](../../raw/application-user-guide/llm-application/workflow-application/multimodal-generation-node.md)。
- **专用模型节点**：
  - 意图分类节点、参数提取节点、文档/图片/视频/音频解析节点均内置专用模型或可选模型，例如参数提取节点明确支持 VL 系列模型处理视觉输入 [参数提取节点](../../raw/application-user-guide/llm-application/workflow-application/parameter-extraction-node.md)；
  - 知识库节点不依赖特定模型，其检索结果由下游大模型节点消费，但检索质量受所选模型的语义理解能力间接影响。

> **注意**：文档 40（文件问答）中列出的“千问-QwQ”“千问3-Coder-Plus”等模型名称与当前控制台实际模型列表存在不一致，且未说明其在 Agent/Workflow 中的具体支持状态；实际开发请以控制台模型选择器下拉菜单及 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md) 中推荐的 `千问-Max` 系列为准。

## 关键参数

各节点共用一套基础参数体系，但配置入口与生效范围不同：

- **通用生成参数**（适用于大模型节点、意图分类节点、参数提取节点、智能体创建节点等）：
  - `temperature`：控制输出随机性，取值 `[0, 2)`，默认 `0.70`；
  - `top_p`：控制输出多样性，取值 `(0, 1]`，默认 `0.80`；
  - `max_output_tokens`（最长回复长度）：模型输出 token 上限，不同节点默认值不同（如大模型节点默认 `1024`，智能体应用默认值依模型而异），上限受模型本身限制 [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)。
- **推理增强参数**：
  - `enable_thinking`：开启后触发思维链（CoT）推理，`thinking_budget` 控制其最大 token 数（默认 `4000`），该参数在大模型节点、意图分类节点、参数提取节点中均存在且行为一致；
  - `result_format`：指定返回格式（如 `message`），影响结构化解析。
- **Agent 特有参数**：
  - `携带的上下文轮数`（仅 Agent 1.0）：控制输入模型的历史对话轮数，影响多轮连贯性；
  - `智能模式`（仅 Agent 2.0）：提供 AUTO/性能/均衡/经济四档自动路由策略，按任务复杂度动态匹配模型与上下文能力，计费规则与单档位不同 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。

## 使用方式

LLM 应用的使用分为三类路径，对应不同抽象层级：

- **零代码智能体（Agent）**：通过自然语言配置系统提示词、绑定知识库（RAG）与插件（MCP），由模型自主规划工具调用顺序。适合快速构建客服、问答等开放式对话应用。创建入口在控制台「应用管理」→「智能体应用」页签 [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)。
- **低代码工作流（Workflow）**：通过可视化画布编排节点（如开始/结束、条件判断、批处理、大模型、知识库、API、MCP、多模态生成等），显式定义执行逻辑。适合需要精确控制流程、处理批量数据或混合多模态任务的场景。节点类型详见 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md) 及其子文档。
- **高代码应用（Rich Code）**：基于 Python 项目结构，使用 `agentscope-runtime` SDK 编写后端服务，通过 MCP 协议接入知识库、MCP 服务、应用组件等工具，并一键部署为 Serverless 或 K8s 服务。适合需要完全掌控逻辑、集成企业系统或构建专业级 AI 后端的开发者 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。

## 限制和注意事项

- **Agent 版本兼容性**：Agent 1.0 支持 UI 分享、钉钉/微信发布等渠道；Agent 2.0 **仅支持 API 调用**，不支持上述分享渠道，选型时需严格区分 [分享智能体应用](../../raw/application-user-guide/llm-application/application-publishing-and-sharing/share-an-application.md)。
- **上下文与资源限制**：
  - 文件上传：单文件 ≤ 10MB（Agent）、≤ 150MB（文档解析节点）、≤ 512MB（音视频解析节点）；单次会话最多 10 个文件 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)；
  - 批处理节点并行数上限为 `10`，循环节点最大次数为 `1000`，均需根据下游服务并发承受力合理设置 [批处理节点](../../raw/application-user-guide/llm-application/workflow-application/batch-node.md)；
  - 知识库检索结果占用模型上下文，需协同调整 `topK` 与 `max_output_tokens` 避免超限 [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)。
- **节点能力边界**：
  - 流程输出节点用于中间状态反馈，**不可替代结束节点**作为最终输出；结束节点每个工作流仅允许一个 [流程输出节点](../../raw/application-user-guide/llm-application/workflow-application/process-output-node.md)；
  - 批处理节点**不支持嵌套批处理或循环节点**，且批处理体内禁止添加流程输出节点 [批处理节点](../../raw/application-user-guide/llm-application/workflow-application/batch-node.md)；
  - API 节点调用外部服务前，必须将百炼服务 IP（`47.93.216.17` 和 `39.105.109.77`）加入目标服务器白名单 [API节点](../../raw/application-user-guide/llm-application/workflow-application/api-node.md)。

## 来源文档

- [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [开始和结束节点](../../raw/application-user-guide/llm-application/workflow-application/start-end-node.md)
- [条件判断节点](../../raw/application-user-guide/llm-application/workflow-application/conditional-node.md)
- [批处理节点](../../raw/application-user-guide/llm-application/workflow-application/batch-node.md)
- [流程输出节点](../../raw/application-user-guide/llm-application/workflow-application/process-output-node.md)
- [循环节点](../../raw/application-user-guide/llm-application/workflow-application/loop-node.md)
- [意图分类节点](../../raw/application-user-guide/llm-application/workflow-application/intent-node.md)
- [大模型节点](../../raw/application-user-guide/llm-application/workflow-application/llm-node.md)
- [知识库节点](../../raw/application-user-guide/llm-application/workflow-application/knowledge-base-node.md)
- [参数提取节点](../../raw/application-user-guide/llm-application/workflow-application/parameter-extraction-node.md)
- [多模态生成节点](../../raw/application-user-guide/llm-application/workflow-application/multimodal-generation-node.md)
- [智能体创建节点](../../raw/application-user-guide/llm-application/workflow-application/agent-create-node.md)
- [API节点](../../raw/application-user-guide/llm-application/workflow-application/api-node.md)
- [智能体群组节点](../../raw/application-user-guide/llm-application/workflow-application/agent-group-node.md)
- [函数计算节点](../../raw/application-user-guide/llm-application/workflow-application/fc-node.md)
- [脚本节点](../../raw/application-user-guide/llm-application/workflow-application/script-node.md)
- [MCP节点](../../raw/application-user-guide/llm-application/workflow-application/mcp-node.md)
- [插件节点](../../raw/application-user-guide/llm-application/workflow-application/plugin-node.md)
- [应用组件节点](../../raw/application-user-guide/llm-application/workflow-application/component-node.md)
- [AppFlow节点](../../raw/application-user-guide/llm-application/workflow-application/appflow-node.md)
- [变量处理节点](../../raw/application-user-guide/llm-application/workflow-application/variable-processing-node.md)
- [文档解析节点](../../raw/application-user-guide/llm-application/workflow-application/document-extraction-node.md)
- [图片解析节点](../../raw/application-user-guide/llm-application/workflow-application/image-extraction-node.md)
- [变量赋值节点](../../raw/application-user-guide/llm-application/workflow-application/variable-assignment-node.md)
- [视频解析节点](../../raw/application-user-guide/llm-application/workflow-application/video-extraction-node.md)
- [音频解析节点](../../raw/application-user-guide/llm-application/workflow-application/audio-extraction-node.md)
- [数据连接器节点](../../raw/application-user-guide/llm-application/workflow-application/data-connector-node.md)
- [开始使用](../../raw/application-user-guide/llm-application/llm-application-start-using.md)
- [应用发布与分享](../../raw/application-user-guide/llm-application/application-publishing-and-sharing.md)
- [使用智能体或工作流作为组件](../../raw/application-user-guide/llm-application/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [分享智能体应用](../../raw/application-user-guide/llm-application/application-publishing-and-sharing/share-an-application.md)
- [UI设计器](../../raw/application-user-guide/llm-application/application-publishing-and-sharing/ui-designer.md)
- [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [应用功能动态](../../raw/application-user-guide/llm-application/application-release-notes.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [工具接入](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-application-mcp.md)
- [API 开发指南](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-app-develop-guide.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)


