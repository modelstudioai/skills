# llm application

百炼平台的 LLM Application 是面向真实业务场景的 AI 应用构建体系，提供智能体（Agent）、工作流（Workflow）和高代码应用三种范式，分别覆盖零代码决策、低代码编排与专业级代码开发需求。其核心能力包括知识库检索增强（RAG）、多模态理解、外部工具调用（MCP/插件）及长上下文处理，支持从简单问答到复杂任务规划的全栈落地。

## 支持的模型与功能

- **模型支持**：  
  - 智能体与工作流节点支持千问系列（Qwen-Max、Qwen-Plus、Qwen-VL 等）、QwQ、Coder-Plus 及第三方模型（如 DeepSeek）。其中 `千问-VL` 系列具备原生多模态能力，即使关闭预解析文件也能直接解析图片/视频 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)；而文本模型需依赖预解析或显式配置知识库节点才能处理非文本文件。  
  - 高代码应用通过 MCP 协议接入模型，支持 Serverless Function 或 K8s 部署，可灵活对接自定义模型服务 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。  

- **核心功能**：  
  - **智能体（Agent）**：支持 Agent 1.0（意图驱动、分步调用）与 Agent 2.0（统一工具规划、完整链路回溯），后者推荐用于复杂任务 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
  - **工作流（Workflow）**：提供 20+ 节点类型，涵盖基础逻辑（条件判断、循环、批处理）、AI 处理（大模型、意图分类、参数提取）、多模态生成（图像/视频/音频）、外部集成（API、函数计算、MCP、AppFlow）及数据解析（文档、图片、音视频、表格）等能力。  
  - **高代码应用**：基于 Python 全栈开发，支持 MCP 工具接入、可观测性埋点与企业级运维，适用于深度定制场景 [API 开发指南](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-app-develop-guide.md)。  

> **注意**：文档中关于“智能体创建节点”与“智能体群组节点”的能力边界存在表述差异。前者在工作流内动态创建临时智能体，后者调度已发布的独立智能体应用；但两者的模型参数配置项（如 `enable_thinking`）均被描述为“启用深度思考模式”，而实际 Agent 2.0 的 `enable_thinking` 参数仅对支持思考模式的模型生效，且与工作流节点中的同名参数无功能耦合——开发者需按节点类型独立配置，不可跨节点复用参数语义。

## 关键参数

- **通用参数**（适用于大模型、意图分类、参数提取等节点）：  
  - `temperature`（默认 0.7）：控制输出随机性，范围 [0, 2)，值越高越多样。  
  - `top_p`（默认 0.8）：控制输出多样性，值越大结果越分散。  
  - `最长回复长度`（默认 1024）：模型生成 token 上限，不含提示词。  
  - `enable_thinking`（默认开启）：启用思维链推理，需配合 `thinking_budget`（默认 4000）限制推理 token。  

- **智能体专属参数**：  
  - `enable_search`：开启联网搜索（仅部分模型支持），若参数未显示则代表当前模型不支持 [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)。  
  - `携带的上下文轮数`（Agent 1.0）：控制输入模型的历史对话轮数，影响多轮一致性。  
  - `AUTO/性能/均衡/经济` 模式（Agent 2.0）：平台自动路由模型，`AUTO` 档位根据任务复杂度（含上下文长度）动态选择，超 200K token 时至少路由至“性能”档。  

- **工作流特有参数**：  
  - 批处理节点：`并行运行数量`（默认 5）与 `批处理次数上限`（默认 30），直接影响并发资源消耗。  
  - 循环节点：`中间变量` 用于跨轮次状态传递，`终止条件` 仅支持基于中间变量判断。  
  - 知识库节点：`topK`（默认 10）控制每个知识库召回片段数，`知识库描述` 影响智能调用模式下的触发准确性。  

## 使用方式

- **创建与配置**：  
  - 智能体：控制台选择 `智能体应用 > Agent 2.0`，配置模型、系统提示词、知识库及内置工具（如 `bash`、`write`）[新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
  - 工作流：通过可视化画布拖拽节点，配置输入（开始节点）、逻辑（条件/循环/批处理）、AI 处理（大模型/意图分类）、工具调用（MCP/API）及输出（结束节点/流程输出节点）[工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。  
  - 高代码应用：控制台选择“高代码应用”，上传 `.whl` 包或使用模板，通过 `fastmcp.Client` 在代码中接入 MCP 工具 [工具接入](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-application-mcp.md)。  

- **文件处理**：  
  - 智能体支持三种模式：`全文引用`（受限于上下文长度）、`切片检索`（RAG，适合长文档）、`自定义处理`（依赖插件/MCP 工具）[文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。  
  - 工作流需搭配专用解析节点：`文档解析`（PDF/Word）、`图片解析`（Qwen-VL 或大模型文档解析）、`视频解析`（语音转录+关键帧描述）、`音频解析`（ASR 文本+时间戳）。  

- **调试与发布**：  
  - 所有应用需先“发布”方可通过 API 调用；工作流支持实时测试并查看各节点输入/输出详情（如循环/批处理的轮次级日志）。  
  - 高代码应用需实现 `/health` 健康检查接口，并通过 `AgentScope-AI` CLI 工具部署 [API 开发指南](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-app-develop-guide.md)。  

## 限制与注意事项

- **资源限制**：  
  - 文件大小：智能体单文件 ≤ 10MB；工作流中文档 ≤ 150MB、视频/音频 ≤ 512MB、图片 ≤ 20MB [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)；图片解析支持列表，其余解析节点仅支持单文件。  
  - 循环/批处理：循环次数上限 1000，批处理数组长度受 `批处理次数上限` 限制（默认 30）；批处理并行数过高可能触发下游服务限流。  

- **功能约束**：  
  - `变量处理节点` 的 JSON 输出模式仅支持单层键值对，无法生成嵌套结构；需下游节点二次处理 [变量处理节点](../../raw/application-user-guide/llm-application/workflow-application/variable-processing-node.md)。  
  - `AppFlow节点` 不支持[流式输出](../concepts/streaming.md)，如需渐进式响应，须将输出传给支持流式的大模型节点 [AppFlow节点](../../raw/application-user-guide/llm-application/workflow-application/appflow-node.md)。  
  - `知识库节点` 的“旧版调用”模式已逐步淘汰，推荐使用“必定调用”或“智能调用”，后者需准确配置 `知识库描述` 以提升触发精度。  

- **权限与依赖**：  
  - 调用函数计算（FC）、AppFlow 或 MCP 服务前，需确保百炼账号与对应云服务账号归属同一主账号，并完成角色授权（如 `ram:CreateServiceLinkedRole`）[函数计算节点](../../raw/application-user-guide/llm-application/workflow-application/fc-node.md)。  
  - 高代码应用部署需提前开通 FC/API 网关权限，K8s 方式还需 ACK 授权 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。

## 来源文档

- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
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
- [多模态生成节点](../../raw/application-user-guide/llm-application/workflow-application/multimodal-generation-node.md)
- [智能体创建节点](../../raw/application-user-guide/llm-application/workflow-application/agent-create-node.md)
- [参数提取节点](../../raw/application-user-guide/llm-application/workflow-application/parameter-extraction-node.md)
- [函数计算节点](../../raw/application-user-guide/llm-application/workflow-application/fc-node.md)
- [智能体群组节点](../../raw/application-user-guide/llm-application/workflow-application/agent-group-node.md)
- [API节点](../../raw/application-user-guide/llm-application/workflow-application/api-node.md)
- [脚本节点](../../raw/application-user-guide/llm-application/workflow-application/script-node.md)
- [MCP节点](../../raw/application-user-guide/llm-application/workflow-application/mcp-node.md)
- [插件节点](../../raw/application-user-guide/llm-application/workflow-application/plugin-node.md)
- [应用组件节点](../../raw/application-user-guide/llm-application/workflow-application/component-node.md)
- [AppFlow节点](../../raw/application-user-guide/llm-application/workflow-application/appflow-node.md)
- [变量处理节点](../../raw/application-user-guide/llm-application/workflow-application/variable-processing-node.md)
- [变量赋值节点](../../raw/application-user-guide/llm-application/workflow-application/variable-assignment-node.md)
- [文档解析节点](../../raw/application-user-guide/llm-application/workflow-application/document-extraction-node.md)
- [视频解析节点](../../raw/application-user-guide/llm-application/workflow-application/video-extraction-node.md)
- [数据连接器节点](../../raw/application-user-guide/llm-application/workflow-application/data-connector-node.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [工具接入](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-application-mcp.md)
- [API 开发指南](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-app-develop-guide.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)
- [音频解析节点](../../raw/application-user-guide/llm-application/workflow-application/audio-extraction-node.md)
- [图片解析节点](../../raw/application-user-guide/llm-application/workflow-application/image-extraction-node.md)


