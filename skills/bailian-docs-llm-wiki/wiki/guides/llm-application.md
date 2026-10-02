# llm application

百炼平台的 LLM Application 提供三种核心构建模式：智能体（Agent）、工作流（Workflow）和高代码应用，分别面向零代码、低代码和专业开发者场景。它们通过集成知识库检索增强（RAG）、外部工具调用（MCP/[插件](../concepts/plugin.md)）、多模态解析等能力，突破大模型在私有知识访问、实时信息获取、流程控制和复杂任务规划等方面的原生局限，支撑真实业务落地。

## 支持的模型/功能

LLM Application 支持三类核心应用形态，各自具备差异化能力：

- **智能体（Agent）**：以提示词驱动，支持自主决策与动态工具调用。新版 Agent 2.0 将知识库、MCP 等统一为工具，实现端到端“规划-执行-反思”链路，过程可追溯；旧版 Agent 1.0 则采用分阶段调度（先检索后决策），适用于意图单一的简单任务 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
- **工作流（Workflow）**：通过可视化节点编排实现确定性流程控制，包含基础节点（开始/结束、条件判断、循环、批处理）、AI 节点（大模型、知识库、意图分类、参数提取、多模态生成）和工具节点（API、函数计算、MCP、[插件](../concepts/plugin.md)、AppFlow、数据连接器）[工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。  
- **高代码应用**：面向开发者提供完整 Python 项目部署能力，支持 Serverless Function 或 K8s 部署，内置 MCP 工具接入、可观测性及自定义前端 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。

所有应用均支持多模态文件处理（文档、图片、音视频），但处理逻辑因模式而异：智能体应用提供全文引用、切片检索（RAG）和自定义处理三种模式 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)；工作流则通过专用解析节点（文档、图片、音频、视频）将非结构化内容转为结构化变量供下游使用。

> **注意**：文档 32 中关于“智能体应用中单文件上限 10MB”的限制，与文档 26（文档解析节点单文件 ≤150MB）、文档 27（音频解析节点 ≤512MB）、文档 34（视频解析节点 ≤512MB）存在明显矛盾。实际限制以各节点具体文档为准，智能体应用的文件上传限制应以控制台实时提示或最新 API 文档为准。

## 关键参数

不同应用类型的关键配置参数如下：

- **智能体（Agent）**：  
  - 模型选择支持 `智能模式`（AUTO/性能/均衡/经济）或指定模型；AUTO 模式根据任务复杂度与上下文长度（≥200K tokens 时至少路由至“性能”档）自动选型 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
  - 全局参数包括 `最长回复长度`、`温度系数`、`enable_thinking`（是否开启思考模式）。  
  - 文件处理支持 `预解析开关`：关闭时仅传递文件 URL，由智能体自主调用工具；开启时系统预置解析器提取文本（千问-VL 系列模型即使关闭预解析也能直接解析图片/视频）。

- **工作流（Workflow）**：  
  - 大模型节点、意图分类节点、参数提取节点等均支持通用参数：`最长回复长度`、`top_p`、`temperature`、`enable_thinking`、`thinking_budget`。  
  - 条件判断节点支持“所有”或“任一”逻辑关系的条件组配置；循环节点支持数组循环/指定次数循环，并提供中间变量实现跨轮次状态传递 [循环节点](../../raw/application-user-guide/llm-application/workflow-application/loop-node.md)。  
  - 批处理节点与循环节点关键区别在于并行 vs 串行执行，且批处理不支持中间变量 [批处理节点](../../raw/application-user-guide/llm-application/workflow-application/batch-node.md)。

- **高代码应用**：  
  - 必须提供 `GET /health` 健康检查接口，入口文件固定为 `main.py`，对话默认路径为 `/process` [API 开发指南](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-app-develop-guide.md)。  
  - 工具接入需在代码中通过 `fastmcp.Client` 实现，控制台添加工具仅用于展示与环境变量配置 [工具接入](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-application-mcp.md)。

## 使用方式

- **创建与配置**：  
  - 智能体：控制台选择 `智能体应用 > Agent 2.0`（推荐）或 `Agent 1.0`，配置模型、系统提示词、知识库与[插件](../concepts/plugin.md) [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)。  
  - 工作流：从节点库拖拽或通过 `+` 按钮添加节点（如开始节点 → 条件判断 → 多个大模型节点），配置各节点输入/输出及参数 [条件判断节点](../../raw/application-user-guide/llm-application/workflow-application/conditional-node.md)。  
  - 高代码应用：控制台选择模板或上传 `.whl` 包，配置部署方式（Serverless/K8s）与资源规格 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。

- **调试与测试**：  
  - 所有应用均支持控制台内联测试；工作流节点（如循环体、批处理体）支持在测试结果面板中翻页查看每轮详细输入输出 [循环节点](../../raw/application-user-guide/llm-application/workflow-application/loop-node.md)。  
  - 知识库节点、文档/图片/音视频解析节点均提供“调试召回效果”或“解析结果预览”功能，便于优化配置。

- **发布与调用**：  
  - 应用必须发布后方可通过 API/SDK 调用，或集成至钉钉、微信公众号等渠道 [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)。  
  - 高代码应用部署后自动暴露公网 API，支持流式响应（需在代码中实现）与可观测性数据上报 [API 开发指南](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-app-develop-guide.md)。

## 限制和注意事项

- **资源与配额**：  
  - 智能体应用单会话最多上传 10 个文件，但各文件大小限制不一（文档类 ≤150MB，音视频 ≤512MB）；工作流中各类解析节点有独立文件大小上限，需按节点文档确认。  
  - 循环节点最大循环次数为 1000，批处理节点默认并行数为 5、上限为 30，超限需手动调整 [批处理节点](../../raw/application-user-guide/llm-application/workflow-application/batch-node.md)。  
  - 高代码应用 Serverless 部署模式下，实例并发度、内存规格受所选资源方案约束。

- **功能边界**：  
  - 工作流中 `JSON 输出模式` 仅支持单层键值对，无法生成嵌套 JSON；如需复杂结构，需在下游节点二次处理 [变量处理节点](../../raw/application-user-guide/llm-application/workflow-application/variable-processing-node.md)。  
  - AppFlow 节点、MCP 节点不支持[流式输出](../concepts/streaming-output.md)，若需流式返回，需将其结果传入支持流式的大模型节点进行二次处理 [AppFlow节点](../../raw/application-user-guide/llm-application/workflow-application/appflow-node.md)。  
  - 大模型节点批量处理模式不支持记忆、失败重试与异常处理，仅单次处理模式支持 [大模型节点](../../raw/application-user-guide/llm-application/workflow-application/llm-node.md)。

- **安全与权限**：  
  - 调用外部 API 时，需将百炼服务 IP（`47.93.216.17` 和 `39.105.109.77`）加入目标服务白名单 [API节点](../../raw/application-user-guide/llm-application/workflow-application/api-node.md)。  
  - 高代码应用部署需授权函数计算（FC）与 API 网关角色，权限不足时需联系管理员 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。

## 来源文档

- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [条件判断节点](../../raw/application-user-guide/llm-application/workflow-application/conditional-node.md)
- [开始和结束节点](../../raw/application-user-guide/llm-application/workflow-application/start-end-node.md)
- [循环节点](../../raw/application-user-guide/llm-application/workflow-application/loop-node.md)
- [批处理节点](../../raw/application-user-guide/llm-application/workflow-application/batch-node.md)
- [流程输出节点](../../raw/application-user-guide/llm-application/workflow-application/process-output-node.md)
- [知识库节点](../../raw/application-user-guide/llm-application/workflow-application/knowledge-base-node.md)
- [大模型节点](../../raw/application-user-guide/llm-application/workflow-application/llm-node.md)
- [多模态生成节点](../../raw/application-user-guide/llm-application/workflow-application/multimodal-generation-node.md)
- [意图分类节点](../../raw/application-user-guide/llm-application/workflow-application/intent-node.md)
- [智能体创建节点](../../raw/application-user-guide/llm-application/workflow-application/agent-create-node.md)
- [参数提取节点](../../raw/application-user-guide/llm-application/workflow-application/parameter-extraction-node.md)
- [智能体群组节点](../../raw/application-user-guide/llm-application/workflow-application/agent-group-node.md)
- [脚本节点](../../raw/application-user-guide/llm-application/workflow-application/script-node.md)
- [API节点](../../raw/application-user-guide/llm-application/workflow-application/api-node.md)
- [函数计算节点](../../raw/application-user-guide/llm-application/workflow-application/fc-node.md)
- [插件节点](../../raw/application-user-guide/llm-application/workflow-application/plugin-node.md)
- [AppFlow节点](../../raw/application-user-guide/llm-application/workflow-application/appflow-node.md)
- [MCP节点](../../raw/application-user-guide/llm-application/workflow-application/mcp-node.md)
- [变量赋值节点](../../raw/application-user-guide/llm-application/workflow-application/variable-assignment-node.md)
- [变量处理节点](../../raw/application-user-guide/llm-application/workflow-application/variable-processing-node.md)
- [应用组件节点](../../raw/application-user-guide/llm-application/workflow-application/component-node.md)
- [文档解析节点](../../raw/application-user-guide/llm-application/workflow-application/document-extraction-node.md)
- [音频解析节点](../../raw/application-user-guide/llm-application/workflow-application/audio-extraction-node.md)
- [图片解析节点](../../raw/application-user-guide/llm-application/workflow-application/image-extraction-node.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [工具接入](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-application-mcp.md)
- [API 开发指南](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-app-develop-guide.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)
- [数据连接器节点](../../raw/application-user-guide/llm-application/workflow-application/data-connector-node.md)
- [视频解析节点](../../raw/application-user-guide/llm-application/workflow-application/video-extraction-node.md)


