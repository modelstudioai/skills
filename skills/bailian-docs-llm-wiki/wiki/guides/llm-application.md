# llm application

百炼平台的 LLM 应用提供三种核心构建模式：智能体（Agent）、工作流（Workflow）和高代码应用，分别面向零代码、低代码与专业开发场景。它们通过集成知识库检索增强（RAG）、外部工具调用（MCP/插件）、多模态解析等能力，突破大模型在私有知识访问、实时信息获取、流程控制与复杂任务规划等方面的原生局限，支持快速构建可解决真实业务问题的 AI 应用 [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)。

## 支持的模型与功能

### 智能体（Agent）
- **模型支持**：千问系列主流文本模型（如 `千问-Plus-Latest`、`千问-Max`），以及具备多模态能力的 `千问-VL` 系列模型；新版 Agent 2.0 推荐使用强工具调用能力模型 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
- **核心能力**：
  - 自主规划与工具调用（知识库、MCP、内置沙箱工具如 `bash`/`read`/`write`）；
  - 预解析文件（开启时自动提取文本；关闭时传递文件 URL，由模型自主决策调用）；
  - 多模态文件处理：`千问-VL` 系列模型即使关闭预解析，也能直接解析图片/视频 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
- **版本差异**：Agent 2.0 将知识库与 MCP 统一为工具，支持完整“规划-执行-反思”链路回溯；Agent 1.0 则按固定顺序依次调用知识库与插件 [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)。

### 工作流（Workflow）
- **节点类型丰富**：涵盖基础逻辑（开始/结束、条件判断、循环、批处理）、AI 节点（大模型、知识库、意图分类、参数提取、多模态生成）、工具节点（API、函数计算、MCP、插件、AppFlow）及数据解析节点（文档、图片、视频、音频）。
- **多模态解析支持**：
  - 文档解析：支持 PDF/DOCX/XLSX/MD/TXT 等，输出结构化 `layout` 或 `cells`；
  - 图片解析：提供“大模型文档解析”（专用于含文字文档类图片）与“Qwen VL 解析”（通用图片，需自定义提示词）两种模式 [图片解析节点](../../raw/application-user-guide/llm-application/workflow-application/image-extraction-node.md)；
  - 视频/音频解析：同步提取 ASR 文本与关键帧描述，输出带时间戳的 `segments` 结构 [视频解析节点](../../raw/application-user-guide/llm-application/workflow-application/video-extraction-node.md)、[音频解析节点](../../raw/application-user-guide/llm-application/workflow-application/audio-extraction-node.md)。

### 高代码应用
- **部署方式**：支持 Serverless Function（无状态、低成本）与 K8s（高性能、有状态长程任务）两种模式 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。
- **工具接入**：通过 MCP 协议接入知识库、MCP 服务、应用组件与数据连接器，需在代码中实现 `fastmcp.Client` 调用逻辑 [工具接入](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-application-mcp.md)。

> **注意**：文档 31（文件问答）中声明“单个会话支持上传文件上限 10 个，且单文件不超过 10MB”，但文档 24（文档解析节点）、25（图片解析节点）、27（视频解析节点）、33（音频解析节点）分别规定单文件上限为 150 MB、20 MB、512 MB、512 MB。实际限制以各节点具体配置为准，会话级限制不适用于工作流内通过节点上传的文件。

## 关键参数

| 参数类别 | 适用场景 | 关键参数 | 说明 |
|----------|----------|----------|------|
| **模型通用参数** | 所有模型节点（智能体、工作流大模型节点、意图分类节点等） | `temperature`、`top_p`、`max_output_tokens` | 控制生成随机性、多样性与长度；取值范围与默认值因节点而异，如大模型节点默认 `temperature=0.70` [大模型节点](../../raw/application-user-guide/llm-application/workflow-application/llm-node.md) |
| **智能体特有参数** | Agent 2.0 配置 | `enable_thinking`、`thinking_budget` | 开启深度思考模式，`thinking_budget` 控制思维链最大 token 数；不支持该模式的模型无法配置 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md) |
| **工作流节点参数** | 循环节点 | `循环次数`、`中间变量`、`终止条件` | `中间变量` 实现跨轮次状态传递；`终止条件` 仅支持基于中间变量判断 [循环节点](../../raw/application-user-guide/llm-application/workflow-application/loop-node.md) |
| **高代码应用参数** | 部署配置 | `规格方案`（vCPU/内存）、`最小实例数`、`单实例并发度` | 影响性能与成本；时延敏感业务建议 `最小实例数 ≥ 1` [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md) |

## 使用方式

### 创建与配置
- **智能体**：控制台 → 应用管理 → 创建应用 → 选择“智能体应用 > Agent 2.0” → 配置模型、系统提示词、知识库/MCP 工具 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
- **工作流**：控制台 → 应用管理 → 创建应用 → 选择“工作流应用” → 在画布中拖拽/连线节点（如开始 → 知识库 → 大模型 → 结束）→ 配置各节点输入/输出/参数 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。
- **高代码应用**：控制台 → 应用管理 → 创建应用 → 选择“高代码应用” → 选择模板或上传 `.whl` 包 → 配置部署方式与资源 → 提交部署 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。

### API 调用
- **智能体/工作流**：发布应用后，通过 DashScope SDK 或 HTTP API 调用；新版智能体应用推荐使用 [新版智能体应用 API](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)。
- **高代码应用**：部署后获得公网 API 地址，遵循 `/process` 对话接口协议；必须实现 `/health` 健康检查接口 [API 开发指南](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-app-develop-guide.md)。

### 文件处理模式（智能体）
- **全文引用**：将解析后全文作为上下文输入，适合短文档总结；
- **切片检索（RAG）**：将文件切片并检索最相关片段，适合长文档精确定位；
- **自定义处理**：传递文件 URL 或内容，由模型自主调用插件/MCP 处理 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。

## 限制和注意事项

- **文件限制**：智能体会话内单文件 ≤ 10MB；工作流节点独立限制（如文档解析 ≤ 150MB，视频/音频 ≤ 512MB）；所有节点均**仅支持单文件解析**，不支持列表批量上传 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)、[文档解析节点](../../raw/application-user-guide/llm-application/workflow-application/document-extraction-node.md)。
- **节点嵌套限制**：循环体内禁止嵌套另一循环节点或批处理节点；批处理体内禁止嵌套批处理或循环节点 [循环节点](../../raw/application-user-guide/llm-application/workflow-application/loop-node.md)、[批处理节点](../../raw/application-user-guide/llm-application/workflow-application/batch-node.md)。
- **权限要求**：发布智能体应用需 RAM 账号具备 `ram:CreateServiceLinkedRole` 权限；高代码应用部署需授权函数计算（FC）与 API 网关服务角色 [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)、[高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。
- **计费差异**：Agent 2.0 的 `AUTO` 模式按统一刊例价计费，与实际路由模型无关；手动选择性能/均衡/经济档则按对应档位计费 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。

## 来源文档

- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [开始和结束节点](../../raw/application-user-guide/llm-application/workflow-application/start-end-node.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [循环节点](../../raw/application-user-guide/llm-application/workflow-application/loop-node.md)
- [条件判断节点](../../raw/application-user-guide/llm-application/workflow-application/conditional-node.md)
- [批处理节点](../../raw/application-user-guide/llm-application/workflow-application/batch-node.md)
- [流程输出节点](../../raw/application-user-guide/llm-application/workflow-application/process-output-node.md)
- [知识库节点](../../raw/application-user-guide/llm-application/workflow-application/knowledge-base-node.md)
- [大模型节点](../../raw/application-user-guide/llm-application/workflow-application/llm-node.md)
- [意图分类节点](../../raw/application-user-guide/llm-application/workflow-application/intent-node.md)
- [参数提取节点](../../raw/application-user-guide/llm-application/workflow-application/parameter-extraction-node.md)
- [多模态生成节点](../../raw/application-user-guide/llm-application/workflow-application/multimodal-generation-node.md)
- [智能体群组节点](../../raw/application-user-guide/llm-application/workflow-application/agent-group-node.md)
- [智能体创建节点](../../raw/application-user-guide/llm-application/workflow-application/agent-create-node.md)
- [函数计算节点](../../raw/application-user-guide/llm-application/workflow-application/fc-node.md)
- [API节点](../../raw/application-user-guide/llm-application/workflow-application/api-node.md)
- [脚本节点](../../raw/application-user-guide/llm-application/workflow-application/script-node.md)
- [MCP节点](../../raw/application-user-guide/llm-application/workflow-application/mcp-node.md)
- [应用组件节点](../../raw/application-user-guide/llm-application/workflow-application/component-node.md)
- [插件节点](../../raw/application-user-guide/llm-application/workflow-application/plugin-node.md)
- [AppFlow节点](../../raw/application-user-guide/llm-application/workflow-application/appflow-node.md)
- [文档解析节点](../../raw/application-user-guide/llm-application/workflow-application/document-extraction-node.md)
- [图片解析节点](../../raw/application-user-guide/llm-application/workflow-application/image-extraction-node.md)
- [变量赋值节点](../../raw/application-user-guide/llm-application/workflow-application/variable-assignment-node.md)
- [视频解析节点](../../raw/application-user-guide/llm-application/workflow-application/video-extraction-node.md)
- [数据连接器节点](../../raw/application-user-guide/llm-application/workflow-application/data-connector-node.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [工具接入](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-application-mcp.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)
- [API 开发指南](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-app-develop-guide.md)
- [音频解析节点](../../raw/application-user-guide/llm-application/workflow-application/audio-extraction-node.md)


