# llm application

百炼平台的 LLM Application 是面向真实业务场景的 AI 应用构建体系，提供智能体（Agent）、工作流（Workflow）和高代码应用三种范式，分别对应零代码、低代码和专业代码开发路径。其核心能力包括知识库检索增强（RAG）、外部工具调用（MCP/插件）、多模态解析与生成，以及端到端的部署运维支持，旨在突破大模型在私有知识、实时信息、流程控制和复杂任务规划上的原生局限。

## 支持的模型/功能

- **智能体（Agent）**：支持 Agent 1.0 和 Agent 2.0 两代架构。Agent 2.0 将知识库、MCP 等统一为工具，支持自主规划与完整过程回溯；Agent 1.0 则采用分阶段调度（先检索后决策）。推荐新项目使用 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
- **工作流（Workflow）**：提供可视化节点编排能力，覆盖基础逻辑（开始/结束、条件判断、循环、批处理）、AI 能力（大模型、意图分类、参数提取、知识库、多模态生成）、工具集成（API、函数计算、脚本、插件、MCP、AppFlow、数据连接器）及数据处理（文档/图片/音频/视频解析、变量处理、变量赋值）。  
- **高代码应用**：基于 Python 的 Serverless Function 或 K8s 部署，支持通过 MCP 协议接入知识库、MCP 服务、应用组件和数据连接器，并提供 `main.py` 入口、`/health` 健康检查及 `/process` 对话接口标准。详细开发规范见 [API 开发指南](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-app-develop-guide.md)。  
- **多模态能力**：支持文档（PDF/DOCX等）、图片（PNG/JPG等）、音频（MP3/WAV等）、视频（MP4/MKV等）的结构化解析；支持图像、视频、音频的生成；参数提取节点在选用 Qwen-VL 系列模型时可直接从图片/视频中提取结构化参数。

> **注意**：文档 33 中声明“单个会话支持上传文件上限 10 个，且单文件不超过 10MB”，但文档 25（文档解析节点）明确限制“单文件大小不超过 150 MB”，文档 26（图片解析节点）为“20 MB”，文档 27/28（音视频解析节点）为“512 MB”。实际限制以各解析节点的独立规格为准，而非全局统一上限。

## 关键参数

- **模型通用参数**（适用于大模型节点、意图分类节点、参数提取节点等）：  
  - `temperature`：控制输出随机性（范围通常为 [0, 2)，默认 0.7）；  
  - `top_p`：控制输出多样性（默认 0.8）；  
  - `max_tokens`（或 `最长回复长度`）：模型生成内容的最大 token 数（默认 1024）；  
  - `enable_thinking`：是否启用深度思考模式（需模型支持）；  
  - `thinking_budget`：思考模式下的最大推理 token 数（默认 4000）。  
- **智能体专属参数**：  
  - `enable_search`：启用联网搜索（仅部分模型支持）；  
  - `预解析文件` 开关：控制文件是否由系统预解析为文本（千问-VL 系列模型即使关闭亦可直解图片/视频）。  
- **工作流节点特有参数**：  
  - 循环节点的 `中间变量` 和 `终止条件`；  
  - 批处理节点的 `并行运行数量`（默认 5）和 `批处理次数上限`（默认 30）；  
  - API 节点的 `超时时间`（默认 5 秒）和重试策略；  
  - 多模态生成节点的 `随机种子`、`prompt_extend`（提示词智能改写）等。

## 使用方式

- **创建与配置**：  
  - 智能体：在控制台选择“智能体应用 > Agent 2.0”，配置模型（推荐 `千问-Max` 系列）、系统提示词、知识库与内置工具（如 `bash`、`write`）。  
  - 工作流：从节点库拖拽或通过 `+` 按钮添加节点，按需连接。关键节点如 [开始和结束节点](../../raw/application-user-guide/llm-application/workflow-application/start-end-node.md) 定义输入/输出，条件判断节点实现分支路由，循环/批处理节点处理数组数据。  
  - 高代码应用：选择“高代码应用”模板，提交 `main.py` 及依赖，通过 MCP 协议在代码中调用已配置的工具。  
- **文件处理**：  
  - 智能体中支持三种模式：`全文引用`（适合短文档总结）、`切片检索`（RAG，适合长文档问答）、`自定义处理`（依赖插件/MCP 工具）。  
  - 工作流中使用专用解析节点（文档/图片/音频/视频解析），输出结构化变量供下游节点（如大模型、变量处理）消费。  
- **调试与观测**：  
  - 工作流可在测试面板中逐轮查看循环/批处理节点的输入输出；  
  - 高代码应用可通过 [应用观测](https://bailian.console.aliyun.com/?tab=app#/app-observe) 查看调用次数、[Token](../concepts/token.md) 消耗、延时等指标，需在部署时启用 `--telemetry enable`。

## 限制和注意事项

- **资源与配额**：  
  - 智能体单次会话文件上传上限为 10 个，但各解析节点有独立大小限制（如文档解析 ≤150 MB，图片 ≤20 MB，音视频 ≤512 MB）；  
  - 批处理节点默认并行数为 5，过高可能触发下游服务并发限流；  
  - 循环节点最大循环次数为 1000，批处理节点批处理次数上限默认 30。  
- **兼容性与依赖**：  
  - Agent 2.0 的 `AUTO` 模式按统一刊例价计费，与实际路由模型无关；手动选择性能/均衡/经济档则按对应档位计费；  
  - MCP 节点调用前需确保目标服务已开通，且百炼服务 IP（`47.93.216.17` 和 `39.105.109.77`）已加入目标服务白名单；  
  - 函数计算（FC）和 AppFlow 节点要求服务账号与百炼账号归属同一主账号。  
- **开发约束**：  
  - 高代码应用必须提供 `GET /health` 接口，入口文件必须为 `main.py`，代码包推荐 `.whl` 格式；  
  - JSON 输出模式（变量处理节点）仅支持单层键值对，不支持嵌套结构；  
  - 插件节点一次仅支持一个工具，如需多个工具需添加多个插件节点。

## 来源文档

- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [开始和结束节点](../../raw/application-user-guide/llm-application/workflow-application/start-end-node.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [条件判断节点](../../raw/application-user-guide/llm-application/workflow-application/conditional-node.md)
- [循环节点](../../raw/application-user-guide/llm-application/workflow-application/loop-node.md)
- [流程输出节点](../../raw/application-user-guide/llm-application/workflow-application/process-output-node.md)
- [批处理节点](../../raw/application-user-guide/llm-application/workflow-application/batch-node.md)
- [意图分类节点](../../raw/application-user-guide/llm-application/workflow-application/intent-node.md)
- [大模型节点](../../raw/application-user-guide/llm-application/workflow-application/llm-node.md)
- [多模态生成节点](../../raw/application-user-guide/llm-application/workflow-application/multimodal-generation-node.md)
- [智能体创建节点](../../raw/application-user-guide/llm-application/workflow-application/agent-create-node.md)
- [智能体群组节点](../../raw/application-user-guide/llm-application/workflow-application/agent-group-node.md)
- [API节点](../../raw/application-user-guide/llm-application/workflow-application/api-node.md)
- [函数计算节点](../../raw/application-user-guide/llm-application/workflow-application/fc-node.md)
- [脚本节点](../../raw/application-user-guide/llm-application/workflow-application/script-node.md)
- [插件节点](../../raw/application-user-guide/llm-application/workflow-application/plugin-node.md)
- [MCP节点](../../raw/application-user-guide/llm-application/workflow-application/mcp-node.md)
- [AppFlow节点](../../raw/application-user-guide/llm-application/workflow-application/appflow-node.md)
- [知识库节点](../../raw/application-user-guide/llm-application/workflow-application/knowledge-base-node.md)
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
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)
- [参数提取节点](../../raw/application-user-guide/llm-application/workflow-application/parameter-extraction-node.md)


