# llm application

百炼平台的 LLM Application 提供三种核心构建模式：智能体（Agent）、工作流（Workflow）和高代码应用，分别面向零代码、低代码和专业开发者场景。它们通过集成知识库检索增强（RAG）、外部工具调用（MCP/插件）、多模态解析等能力，突破大模型在私有知识、实时信息、流程控制和复杂任务规划等方面的原生局限，支持快速构建生产级 AI 应用。

## 支持的模型/功能

- **智能体（Agent）**：支持 Agent 1.0 和 Agent 2.0 两个版本。Agent 2.0 将知识库、MCP 等统一为工具，支持自主规划与完整“规划-执行-反思”链路回溯；Agent 1.0 则采用分阶段调度（先检索后决策），适合意图单一的简单任务 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
- **工作流（Workflow）**：提供可视化节点编排能力，涵盖基础逻辑（开始/结束、条件判断、循环、批处理）、AI 节点（大模型、知识库、意图分类、参数提取、智能体创建/群组）、多模态节点（文档/图片/视频/音频解析、多模态生成）及工具节点（API、函数计算、脚本、插件、MCP、AppFlow、数据连接器）[工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。  
- **高代码应用**：面向 Python 开发者，支持 Serverless Function 和 K8s 两种部署方式，提供一站式 MCP 工具接入、自定义前端 WebUI 及企业级可观测能力 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。  
- **多模态与文件处理**：支持文档、图片、音视频的结构化解析（如 `文档解析节点`、`图片解析节点`、`视频解析节点`、`音频解析节点`），并可与大模型节点组合实现端到端内容理解与生成。

> **注意**：文档 32（文件问答）中关于“单文件不超过 10MB”的限制与文档 24（文档解析节点）、文档 25（图片解析节点）、文档 31（视频解析节点）、文档 34（音频解析节点）中明确列出的更大文件限制（如视频 512 MB、图片 20 MB）存在矛盾。实际能力以各节点独立文档的规格说明为准，文件问答模块的描述已过时。

## 关键参数

- **模型参数通用项**：所有 AI 类节点（大模型、意图分类、参数提取、智能体创建/群组等）均支持配置 `temperature`（控制随机性）、`top_p`（控制多样性）、`最长回复长度`（token 数上限）及 `enable_thinking`（是否启用思考模式）。  
- **Agent 2.0 特有参数**：`enable_thinking` 在 Agent 2.0 中直接影响反思效果；其模型选择器还提供 `AUTO` 档位，根据任务复杂度（结合用户消息与上下文长度）自动路由至 `性能`/`均衡`/`经济` 模型，并按统一刊例价计费 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
- **工作流节点特有参数**：
  - `循环节点`：支持 `数组循环` 与 `指定次数循环`，通过 `中间变量` 实现跨轮次状态传递，并支持基于该变量的 `终止条件`。
  - `批处理节点`：配置 `并行运行数量`（默认 5）与 `批处理次数上限`（默认 30），用于控制并发资源消耗。
  - `大模型节点`：`记忆` 配置支持 `本节点缓存`（限定轮次）或 `自定义缓存`（引用全局 `historyList`）。
- **高代码应用参数**：部署时需配置 `规格方案`（vCPU/内存）、`最小实例数`（推荐 ≥1 保障热启动）、`单实例并发度` 及 `部署地域`，详见 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。

## 使用方式

- **创建与配置**：
  - 智能体：在控制台选择 `智能体应用 > Agent 2.0`（推荐）或 `Agent 1.0`，配置模型、系统提示词、知识库及内置工具（如 `bash`、`write`）[新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
  - 工作流：通过拖拽或 `+` 按钮添加节点，在画布上连线编排。关键节点如 `开始节点` 定义输入（`query`、`historyList`）、`结束节点` 定义输出（文本/JSON/流式），`条件判断节点` 控制分支逻辑 [开始和结束节点](../../raw/application-user-guide/llm-application/workflow-application/start-end-node.md)。  
  - 高代码应用：通过控制台模板创建或命令行上传 `.whl` 包，项目需包含 `main.py` 入口、`requirements.txt`（建议固定依赖版本）及规范的 `tools/`、`prompts/` 目录结构 [工具接入](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-application-mcp.md)。  
- **调用与集成**：
  - 所有应用发布后，均可通过 API/SDK 调用；智能体与工作流还支持发布至钉钉、微信公众号等第三方平台。  
  - 高代码应用需实现 `GET /health` 健康检查接口，并默认提供 `/process` 对话接口；可通过 `@trace` 装饰器植入观测日志 [API 开发指南](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-app-develop-guide.md)。  
- **文件处理**：智能体支持 `全文引用`、`切片检索`（RAG）和 `自定义处理` 三种模式；工作流则通过专用解析节点（如 `文档解析节点`）将非结构化文件转为结构化变量供下游使用。

## 限制和注意事项

- **文件限制**：各解析节点有独立规格——文档解析单文件 ≤150 MB/1.5 万页，图片 ≤20 MB，视频 ≤512 MB，音频 ≤512 MB；智能体会话内文件上限为 10 个且单文件 ≤10 MB，但此限制不适用于工作流节点 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。  
- **节点能力边界**：
  - `循环节点` 内部禁止嵌套循环或批处理节点；`批处理节点` 内部禁止嵌套批处理或循环节点，且不支持 `流程输出节点`。  
  - `变量处理节点` 的 `JSON输出` 模式仅支持单层键值对，无法生成嵌套 JSON 结构。  
- **权限与依赖**：高代码应用部署需提前授权函数计算（FC）和 API 网关服务角色；使用 `函数计算节点` 或 `AppFlow节点` 时，目标服务账号须与百炼账号同属一个主账号 [函数计算节点](../../raw/application-user-guide/llm-application/workflow-application/fc-node.md)。  
- **计费与调试**：`AUTO` 档位按统一刊例价计费，与实际路由模型无关；`大模型文档解析`、`大模型音视频解析` 等节点暂不计费，但 `Qwen VL解析` 等调用视觉模型的节点会产生对应模型调用费用。

## 来源文档

- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [开始和结束节点](../../raw/application-user-guide/llm-application/workflow-application/start-end-node.md)
- [循环节点](../../raw/application-user-guide/llm-application/workflow-application/loop-node.md)
- [条件判断节点](../../raw/application-user-guide/llm-application/workflow-application/conditional-node.md)
- [流程输出节点](../../raw/application-user-guide/llm-application/workflow-application/process-output-node.md)
- [大模型节点](../../raw/application-user-guide/llm-application/workflow-application/llm-node.md)
- [批处理节点](../../raw/application-user-guide/llm-application/workflow-application/batch-node.md)
- [意图分类节点](../../raw/application-user-guide/llm-application/workflow-application/intent-node.md)
- [知识库节点](../../raw/application-user-guide/llm-application/workflow-application/knowledge-base-node.md)
- [参数提取节点](../../raw/application-user-guide/llm-application/workflow-application/parameter-extraction-node.md)
- [智能体群组节点](../../raw/application-user-guide/llm-application/workflow-application/agent-group-node.md)
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
- [智能体创建节点](../../raw/application-user-guide/llm-application/workflow-application/agent-create-node.md)
- [多模态生成节点](../../raw/application-user-guide/llm-application/workflow-application/multimodal-generation-node.md)
- [数据连接器节点](../../raw/application-user-guide/llm-application/workflow-application/data-connector-node.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [工具接入](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-application-mcp.md)
- [视频解析节点](../../raw/application-user-guide/llm-application/workflow-application/video-extraction-node.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)
- [API 开发指南](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-app-develop-guide.md)
- [音频解析节点](../../raw/application-user-guide/llm-application/workflow-application/audio-extraction-node.md)


