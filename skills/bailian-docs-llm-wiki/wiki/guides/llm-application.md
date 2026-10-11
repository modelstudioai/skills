# llm application

百炼平台的 LLM Application 是面向业务场景构建 AI 应用的核心能力层，提供智能体（Agent）、工作流（Workflow）和高代码应用三类范式，分别覆盖零代码决策、低代码编排与专业级工程化部署。三者统一基于 MCP 协议集成知识库、插件、外部服务等能力，支持从简单问答到复杂多模态任务的端到端实现。

## 支持的模型/功能

LLM Application 支持三类核心范式，对应不同抽象层级的能力：

- **智能体（Agent）**：以提示词驱动自主规划与工具调用，适用于开放式对话与动态任务求解。新版 Agent 2.0 将知识库、MCP 等统一为工具，支持完整“规划-执行-反思”链路回溯 [原文标题](../../raw/application-user-guide/llm-application/new-single-agent-application.md)；旧版 Agent 1.0 则采用分阶段调度（先检索后决策），适合意图单一、流程固定的场景 [原文标题](../../raw/application-user-guide/llm-application/single-agent-application.md)。
  
- **工作流（Workflow）**：通过可视化节点编排确定性执行链路，包含基础节点（开始/结束/条件/循环/批处理）、AI 节点（大模型/知识库/意图分类/参数提取/智能体创建/智能体群组）及工具节点（API/MCP/插件/函数计算/多模态生成等）。例如，`知识库节点`支持文档、表格、图片三类知识源混合召回，并可启用二次智能过滤提升精度 [原文标题](../../raw/application-user-guide/llm-application/workflow-application/knowledge-base-node.md)。

- **高代码应用**：面向开发者提供 Python 工程化部署能力，支持 Serverless Function 与 K8s 两种运行时，内置 MCP 工具接入框架与可观测性埋点规范 [原文标题](../../raw/application-user-guide/llm-application/rich-code-application.md)。

> **注意**：文档 32 中列出的“支持的模型”列表存在大量重复占位符（如 `[选择模型](...)`），且未明确区分各范式对模型的实际要求。实际开发中应以控制台实时可选模型为准，尤其需注意：Agent 2.0 推荐选用 `千问-Max` 系列等强工具调用模型；而工作流中的 `大模型节点`、`意图分类节点` 等均支持独立配置 `enable_thinking` 参数，但该参数在部分旧模型上不可用。

## 关键参数

各范式共性参数与关键差异如下：

| 参数 | 智能体（Agent） | 工作流（Workflow） | 高代码应用 |
|------|----------------|---------------------|-------------|
| **模型选择** | 支持 `智能模式`（AUTO/性能/均衡/经济）自动路由，或指定模型；AUTO 模式按上下文长度与任务复杂度动态降级 [原文标题](../../raw/application-user-guide/llm-application/new-single-agent-application.md) | 各 AI 节点（如大模型节点、意图分类节点）独立配置模型及参数（`temperature`/`top_p`/`enable_thinking` 等） | 由代码逻辑控制，控制台仅用于展示已接入的 MCP 工具，不直接配置模型参数 |
| **温度系数（temperature）** | 全局配置，影响生成随机性 | 按节点粒度配置，例如 `大模型节点` 默认 `0.70`，`意图分类节点` 默认 `0.70` | 无全局配置，需在代码中显式传入 |
| **最长回复长度** | 模型生成内容上限（不含提示词） | 各节点独立配置，默认 `1024` tokens | 由开发者在 LLM 调用代码中控制 |
| **思考模式（enable_thinking）** | 可开启，提升反思效果；不支持的模型无法配置 | 多数 AI 节点支持，`thinking_budget` 默认 `4000` tokens | 需在代码中通过 MCP Client 调用时显式启用 |

此外，文件处理相关参数需特别注意：
- 智能体支持 `全文引用`、`切片检索（RAG）`、`自定义处理` 三种模式，其中 `切片检索` 的召回质量依赖于切片策略与 `topK` 设置 [原文标题](../../raw/application-user-guide/llm-application/file-q-a.md)；
- 工作流中 `文档解析节点`、`图片解析节点` 等支持多种解析器（如 `大模型文档解析`、`Qwen VL解析`），计费与效果差异显著，例如 `Qwen VL解析` 产生 Qwen-VL 模型调用费用，而 `大模型文档解析` 暂不计费 [原文标题](../../raw/application-user-guide/llm-application/workflow-application/image-extraction-node.md)。

## 使用方式

### 创建与配置
- **智能体**：控制台 → 应用管理 → 创建应用 → 选择 `智能体应用 > Agent 2.0`，配置模型、系统提示词、预解析开关及内置工具（如 `bash`/`write`/`read`）[原文标题](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
- **工作流**：通过拖拽节点构建画布，关键节点如 `条件判断节点` 支持“所有/任一”条件逻辑，`循环节点` 提供数组循环与指定次数循环两种模式，并支持中间变量跨轮次传递 [原文标题](../../raw/application-user-guide/llm-application/workflow-application/loop-node.md)。
- **高代码应用**：控制台创建后，通过 `AgentScope-AI` CLI 上传 `.whl` 包，入口文件必须为 `main.py`，且需提供 `/health` 健康检查接口 [原文标题](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-app-develop-guide.md)。

### 集成与调用
- 所有应用发布后均可通过 API/SDK 调用；
- 工作流支持 `流程输出节点` 实现中间结果流式返回，而 `结束节点` 控制最终输出格式（文本/JSON/流式）；
- 高代码应用通过 `fastmcp.Client` 接入 MCP 工具，示例代码见 [原文标题](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-application-mcp.md)。

## 限制和注意事项

- **文件限制**：智能体单会话最多上传 10 个文件，单文件 ≤10MB；工作流中 `文档解析节点` 单文件 ≤150MB、`音频/视频解析节点` 单文件 ≤512MB [原文标题](../../raw/application-user-guide/llm-application/workflow-application/document-extraction-node.md)。
- **上下文长度**：Agent 2.0 在上下文 Token 数超过 200K 时强制路由至 `性能` 档位，以保障长上下文处理效果；工作流节点无全局上下文限制，但各节点输入受其自身参数约束。
- **节点嵌套限制**：工作流中 `循环节点` 内部禁止嵌套另一个循环节点或批处理节点；`批处理节点` 内部禁止嵌套任何其他批处理或循环节点 [原文标题](../../raw/application-user-guide/llm-application/workflow-application/batch-node.md)。
- **权限与网络**：调用 `API节点` 或 `函数计算节点` 时，需将百炼服务 IP（`47.93.216.17` 和 `39.105.109.77`）加入目标服务白名单；使用 `AppFlow节点` 时，创建连接流的账号须与百炼登录账号一致或隶属同一主账号 [原文标题](../../raw/application-user-guide/llm-application/workflow-application/api-node.md)。
- **计费差异**：`智能模式` 下按统一刊例价计费，与实际路由模型无关；而手动选择 `性能/均衡/经济` 档位则按对应档位计费；工作流中 `Qwen VL解析` 等节点按实际调用模型计费，非解析器本身计费。

## 来源文档

- [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [开始和结束节点](../../raw/application-user-guide/llm-application/workflow-application/start-end-node.md)
- [条件判断节点](../../raw/application-user-guide/llm-application/workflow-application/conditional-node.md)
- [循环节点](../../raw/application-user-guide/llm-application/workflow-application/loop-node.md)
- [批处理节点](../../raw/application-user-guide/llm-application/workflow-application/batch-node.md)
- [流程输出节点](../../raw/application-user-guide/llm-application/workflow-application/process-output-node.md)
- [知识库节点](../../raw/application-user-guide/llm-application/workflow-application/knowledge-base-node.md)
- [参数提取节点](../../raw/application-user-guide/llm-application/workflow-application/parameter-extraction-node.md)
- [大模型节点](../../raw/application-user-guide/llm-application/workflow-application/llm-node.md)
- [意图分类节点](../../raw/application-user-guide/llm-application/workflow-application/intent-node.md)
- [智能体创建节点](../../raw/application-user-guide/llm-application/workflow-application/agent-create-node.md)
- [智能体群组节点](../../raw/application-user-guide/llm-application/workflow-application/agent-group-node.md)
- [API节点](../../raw/application-user-guide/llm-application/workflow-application/api-node.md)
- [多模态生成节点](../../raw/application-user-guide/llm-application/workflow-application/multimodal-generation-node.md)
- [脚本节点](../../raw/application-user-guide/llm-application/workflow-application/script-node.md)
- [MCP节点](../../raw/application-user-guide/llm-application/workflow-application/mcp-node.md)
- [插件节点](../../raw/application-user-guide/llm-application/workflow-application/plugin-node.md)
- [AppFlow节点](../../raw/application-user-guide/llm-application/workflow-application/appflow-node.md)
- [应用组件节点](../../raw/application-user-guide/llm-application/workflow-application/component-node.md)
- [变量处理节点](../../raw/application-user-guide/llm-application/workflow-application/variable-processing-node.md)
- [变量赋值节点](../../raw/application-user-guide/llm-application/workflow-application/variable-assignment-node.md)
- [文档解析节点](../../raw/application-user-guide/llm-application/workflow-application/document-extraction-node.md)
- [图片解析节点](../../raw/application-user-guide/llm-application/workflow-application/image-extraction-node.md)
- [音频解析节点](../../raw/application-user-guide/llm-application/workflow-application/audio-extraction-node.md)
- [数据连接器节点](../../raw/application-user-guide/llm-application/workflow-application/data-connector-node.md)
- [视频解析节点](../../raw/application-user-guide/llm-application/workflow-application/video-extraction-node.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)
- [工具接入](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-application-mcp.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)
- [API 开发指南](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-app-develop-guide.md)
- [函数计算节点](../../raw/application-user-guide/llm-application/workflow-application/fc-node.md)


