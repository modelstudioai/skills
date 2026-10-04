# llm application

百炼平台的 LLM Application 是面向业务场景的 AI 应用构建体系，提供智能体（Agent）、工作流（Workflow）和高代码应用三类范式，分别覆盖零代码决策、低代码编排与专业级工程化部署。其核心能力包括知识库检索增强（RAG）、多模态理解、外部工具调用（MCP/插件）、记忆管理及可视化节点编排，支持从简单问答到复杂任务协同的全栈落地。

## 支持的模型/功能

- **智能体（Agent）**：支持 Agent 1.0 和 Agent 2.0 两种架构。Agent 2.0 将知识库、MCP 等统一为工具，支持自主规划与完整“规划-执行-反思”链路回溯；Agent 1.0 则采用分阶段调度（先检索后决策）。推荐新项目使用 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
- **工作流（Workflow）**：提供 20+ 类节点，覆盖基础控制（开始/结束/条件/循环/批处理）、AI 能力（大模型/意图分类/参数提取/多模态生成/知识库）、工具集成（API/函数计算/脚本/MCP/插件/AppFlow）及数据解析（文档/图片/视频/音频）。所有节点均支持变量引用、失败重试与异常分支。  
- **高代码应用**：基于 Python 的 Serverless Function 或 K8s 部署，支持 MCP 协议接入知识库、MCP 服务、应用组件与数据连接器，并提供 `main.py` 入口、`/health` 健康检查及 `/process` 对话接口标准。详细开发规范见 [API 开发指南](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-app-develop-guide.md)。  
- **多模态支持**：千问-VL 系列模型（如 `qwen-vl-max`）可直接解析图片/视频，无需预解析；其他文本模型需依赖 [图片解析节点](../../raw/application-user-guide/llm-application/workflow-application/image-extraction-node.md)、[视频解析节点](../../raw/application-user-guide/llm-application/workflow-application/video-extraction-node.md) 等专用节点进行结构化提取。

> **注意**：文档 33 中“文件问答”部分列出的支持模型列表存在大量重复链接（如 `[选择模型](raw/...)`），且未明确标注具体模型名，实际可用模型应以控制台实时下拉菜单为准，该文档已过时。

## 关键参数

- **模型通用参数**（适用于大模型节点、意图分类节点、参数提取节点等）：
  - `temperature`：控制输出随机性（范围 `[0, 2)`），默认 `0.70`；
  - `top_p`：控制输出多样性，默认 `0.80`；
  - `enable_thinking`：开启深度思考模式（需模型支持），输出推理过程；
  - `thinking_budget`：思考模式下最大输出 token 数，默认 `4000`；
  - `result_format`：返回格式，默认 `message`。
- **智能体专属参数**：
  - `enable_search`：启用联网搜索（仅部分模型支持）；
  - `最长回复长度`：生成内容上限（不含提示词）；
  - `携带的上下文轮数`（Agent 1.0）或 `AUTO/性能/均衡/经济` 档位（Agent 2.0）：前者控制历史对话轮数，后者由平台自动路由至适配模型。
- **工作流节点特有参数**：
  - 循环节点：`循环次数`（1–1000）、`中间变量`（跨轮次状态传递）、`终止条件`（基于中间变量判断）；
  - 批处理节点：`并行运行数量`（1–10）、`批处理次数上限`（1–30）；
  - API 节点：`超时时间`（1–120 秒，默认 5 秒）、`最大重试次数`（1–10）；
  - 多模态生成节点：`随机种子`（控制结果一致性）、`prompt_extend`（启用后提升短提示效果但增加耗时）。

## 使用方式

- **创建与配置**：
  - 智能体：在控制台选择 [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md) 中的 Agent 2.0 模板，配置模型、系统提示词、知识库与内置工具（如 `bash`/`write`/`read`）；
  - 工作流：通过拖拽或 `+` 按钮添加节点，利用 [开始和结束节点](../../raw/application-user-guide/llm-application/workflow-application/start-end-node.md) 定义输入/输出，用条件判断、循环、批处理等节点编排逻辑；
  - 高代码应用：选择模板或上传 `.whl` 包，按 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md) 文档配置部署方式、资源规格与工具接入。
- **文件处理**：
  - 智能体中上传文件后，可选“全文引用”“切片检索（RAG）”或“自定义处理”模式；
  - 工作流中需显式使用 [文档解析节点](../../raw/application-user-guide/llm-application/workflow-application/document-extraction-node.md)、[图片解析节点](../../raw/application-user-guide/llm-application/workflow-application/image-extraction-node.md) 等提取结构化内容，再传入下游节点。
- **调试与发布**：
  - 所有应用均支持在线测试对话或工作流运行；
  - 发布前需确认权限（如 RAM 角色）、完成必要配置（如 Agent 的发布操作、高代码应用的健康检查接口）；
  - 发布后可通过 API/SDK 调用，或集成至钉钉、微信公众号等渠道。

## 限制和注意事项

- **资源限制**：
  - 文件大小：智能体单文件 ≤ 10MB；工作流中文档解析 ≤ 150MB、图片 ≤ 20MB、视频/音频 ≤ 512MB；
  - 循环/批处理：循环次数上限 1000，批处理数组长度上限 30；
  - 上下文：Agent 2.0 的 AUTO 档位在上下文 [Token](../concepts/token.md) > 200K 时强制路由至“性能”档。
- **兼容性与行为差异**：
  - Agent 1.0 与 Agent 2.0 的工具调用逻辑不同：前者分步执行（先 RAG 后调插件），后者统一规划；迁移时需重构配置；
  - 工作流中 `大模型节点` 的批量处理模式不支持记忆、失败重试与异常处理，而单次处理模式支持；
  - `变量赋值节点` 是唯一支持写入会话变量、内置变量及循环中间变量的节点，用于实现状态持久化。
- **安全与计费**：
  - API 节点调用外部服务时，需将百炼服务 IP（`47.93.216.17` 和 `39.105.109.77`）加入目标服务器白名单；
  - 文档/图片/音频/视频解析节点中，“大模型文档解析”等部分解析器暂不计费，但 Qwen-VL 解析、MCP 调用等会产生对应模型或服务费用；
  - 高代码应用若使用 K8s 部署，需提前开通 ACK 并完成授权。

## 来源文档

- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [开始和结束节点](../../raw/application-user-guide/llm-application/workflow-application/start-end-node.md)
- [条件判断节点](../../raw/application-user-guide/llm-application/workflow-application/conditional-node.md)
- [循环节点](../../raw/application-user-guide/llm-application/workflow-application/loop-node.md)
- [批处理节点](../../raw/application-user-guide/llm-application/workflow-application/batch-node.md)
- [流程输出节点](../../raw/application-user-guide/llm-application/workflow-application/process-output-node.md)
- [大模型节点](../../raw/application-user-guide/llm-application/workflow-application/llm-node.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [意图分类节点](../../raw/application-user-guide/llm-application/workflow-application/intent-node.md)
- [参数提取节点](../../raw/application-user-guide/llm-application/workflow-application/parameter-extraction-node.md)
- [多模态生成节点](../../raw/application-user-guide/llm-application/workflow-application/multimodal-generation-node.md)
- [知识库节点](../../raw/application-user-guide/llm-application/workflow-application/knowledge-base-node.md)
- [智能体群组节点](../../raw/application-user-guide/llm-application/workflow-application/agent-group-node.md)
- [API节点](../../raw/application-user-guide/llm-application/workflow-application/api-node.md)
- [函数计算节点](../../raw/application-user-guide/llm-application/workflow-application/fc-node.md)
- [脚本节点](../../raw/application-user-guide/llm-application/workflow-application/script-node.md)
- [插件节点](../../raw/application-user-guide/llm-application/workflow-application/plugin-node.md)
- [MCP节点](../../raw/application-user-guide/llm-application/workflow-application/mcp-node.md)
- [AppFlow节点](../../raw/application-user-guide/llm-application/workflow-application/appflow-node.md)
- [应用组件节点](../../raw/application-user-guide/llm-application/workflow-application/component-node.md)
- [变量处理节点](../../raw/application-user-guide/llm-application/workflow-application/variable-processing-node.md)
- [智能体创建节点](../../raw/application-user-guide/llm-application/workflow-application/agent-create-node.md)
- [文档解析节点](../../raw/application-user-guide/llm-application/workflow-application/document-extraction-node.md)
- [变量赋值节点](../../raw/application-user-guide/llm-application/workflow-application/variable-assignment-node.md)
- [图片解析节点](../../raw/application-user-guide/llm-application/workflow-application/image-extraction-node.md)
- [视频解析节点](../../raw/application-user-guide/llm-application/workflow-application/video-extraction-node.md)
- [数据连接器节点](../../raw/application-user-guide/llm-application/workflow-application/data-connector-node.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [工具接入](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-application-mcp.md)
- [API 开发指南](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-app-develop-guide.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)
- [音频解析节点](../../raw/application-user-guide/llm-application/workflow-application/audio-extraction-node.md)


