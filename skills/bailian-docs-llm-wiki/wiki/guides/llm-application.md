# llm application

百炼平台的 LLM Application 是面向真实业务场景的 AI 应用构建体系，提供智能体（Agent）、工作流（Workflow）和高代码应用三种范式，分别覆盖零代码决策、低代码编排与专业级工程化部署需求。三者统一基于大模型能力底座，通过知识库、工具调用、多模态解析等扩展能力突破模型原生局限，支持从快速原型到企业级生产系统的全生命周期开发。

## 支持的模型/功能

LLM Application 支持三类核心构建模式，对应不同能力边界与适用人群：

- **智能体（Agent）**：以提示词驱动自主规划与工具调用，适用于开放式对话与动态任务求解。新版 Agent 2.0 将知识库、MCP 等统一为工具，支持完整“规划-执行-反思”链路回溯，推荐替代旧版 Agent 1.0 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)；而旧版仍保留兼容性，但规划透明度与复杂任务处理能力较弱 [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)。
- **工作流（Workflow）**：通过可视化节点编排实现确定性流程控制，内置 20+ 类节点（如条件判断、循环、批处理、API、MCP、多模态生成等），支持串行/并行/嵌套逻辑，适用于订单处理、报告生成等固定流程自动化 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)。
- **高代码应用**：面向开发者提供 Python 工程化部署能力，支持 Serverless Function 与 K8s 两种运行时，可一站式接入 MCP 工具、自定义前端及企业级可观测能力 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)。

所有模式均支持多模态文件处理（文档、图片、音视频），但解析能力因节点类型而异：文档解析节点、图片解析节点、音频解析节点、视频解析节点分别提供结构化输出，其中 Qwen-VL 系列模型专用于通用图片理解，而大模型文档解析器专用于文档类图片 [图片解析节点](../../raw/application-user-guide/llm-application/workflow-application/image-extraction-node.md)。

> **注意**：文档 34 中关于“文件问答”的支持模型列表存在大量重复占位符（如 `[选择模型](...)`），且未明确区分各处理模式对模型的实际要求；实际可用模型应以控制台实时列表为准，该文档信息已过时，不可作为选型依据。

## 关键参数

各模式共性参数与差异化配置如下：

- **模型参数**（通用）：
  - `temperature`：控制输出随机性（范围 `[0, 2)`），值越高越多样；
  - `top_p`：核采样阈值（默认 `0.80`），影响结果多样性；
  - `max_output_tokens`（最长回复长度）：模型输出 token 上限，不同模型上限不同；
  - `enable_thinking`：是否开启深度思考模式（需模型支持），输出推理过程；
  - `thinking_budget`：思考模式下思维链最大 token 数（默认 `4000`）。

- **智能体特有**：
  - `enable_search`：启用联网搜索（仅部分模型支持）；
  - `preprocess_files`：预解析开关，关闭时仅传文件 URL，由模型自主决策调用工具处理（千问-VL 系列模型除外，其可直接解析图片/视频）。

- **工作流节点特有**：
  - 循环节点支持 `中间变量` 持久化与 `终止条件` 配置，实现状态传递与条件退出；
  - 批处理节点支持 `并行运行数量` 与 `批处理次数上限`，平衡效率与资源消耗；
  - 大模型节点在批量模式下不支持记忆与失败重试，单次模式则支持。

- **高代码应用特有**：
  - 必须实现 `/health` 健康检查接口；
  - 入口文件强制为 `main.py`；
  - 对接 MCP 工具需使用 `fastmcp.Client` 并依赖环境变量（如 `DASHSCOPE_API_KEY`）[工具接入](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-application-mcp.md)。

## 使用方式

- **创建与配置**：
  - 智能体：控制台 → 应用管理 → 创建应用 → 选择“智能体应用”，配置模型、系统提示词、知识库与插件；
  - 工作流：通过画布拖拽或 `+` 按钮添加节点（如开始/结束、条件判断、大模型、MCP 等），按需配置输入/输出变量与参数；
  - 高代码应用：控制台创建后，选择“Serverless Function”或“K8s”部署方式，上传 `.whl` 包或使用模版代码 [API 开发指南](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-app-develop-guide.md)。

- **文件处理**：
  - 智能体中上传文件后，自动触发解析，支持全文引用、切片检索（RAG）或自定义处理三种模式；
  - 工作流中需显式添加文档/图片/音频/视频解析节点，并配置文件类型与解析器（如大模型文档解析器或 Qwen-VL 解析器）。

- **调试与发布**：
  - 所有应用均支持在线文本对话测试；
  - 工作流提供分步调试能力，可查看循环/批处理各轮次输入输出；
  - 发布是 API 调用前提，智能体与工作流发布后获取 endpoint，高代码应用部署即生效。

## 限制和注意事项

- **资源限制**：
  - 单次会话文件上传上限 10 个，单文件 ≤10MB（智能体）；文档解析节点单文件 ≤150MB；图片 ≤20MB；音视频 ≤512MB；
  - 循环节点最大循环次数 1000，批处理节点默认并行数 5、上限 30；
  - 函数计算节点超时固定为 60 秒，不可修改。

- **能力边界**：
  - 智能体 1.0 与 2.0 不兼容：Agent 2.0 的统一工具调度机制无法降级使用 Agent 1.0 的独立知识库/MCP 配置；
  - 工作流中循环体内**不支持嵌套循环或批处理节点**，批处理体内**不支持嵌套批处理或循环节点**；
  - 变量处理节点的 JSON 输出模式**仅支持单层键值对**，无法生成嵌套 JSON 或数组对象；
  - AppFlow 节点与 MCP 节点**不支持[流式输出](../concepts/streaming-output.md)**，如需流式响应，需经大模型节点二次处理。

- **权限与网络**：
  - 调用外部 API 时，需将百炼服务 IP（`47.93.216.17` 和 `39.105.109.77`）加入目标服务白名单；
  - 高代码应用部署需提前授权函数计算（FC）与 API 网关角色权限；
  - 使用 MCP 服务前，必须已在 MCP 广场开通或自建服务。

- **计费与运维**：
  - Agent 2.0 的 `AUTO` 模式按统一刊例价计费，与实际路由模型无关；手动选择性能/均衡/经济档则按对应档位计费；
  - 文档/图片/音频/视频解析节点当前暂不计费，但调用 Qwen-VL 解析器会产生对应模型费用；
  - 高代码应用观测数据（调用次数、Token 总量、延时等）需通过 `--telemetry enable` 显式开启上报。

## 来源文档

- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [条件判断节点](../../raw/application-user-guide/llm-application/workflow-application/conditional-node.md)
- [开始和结束节点](../../raw/application-user-guide/llm-application/workflow-application/start-end-node.md)
- [循环节点](../../raw/application-user-guide/llm-application/workflow-application/loop-node.md)
- [批处理节点](../../raw/application-user-guide/llm-application/workflow-application/batch-node.md)
- [流程输出节点](../../raw/application-user-guide/llm-application/workflow-application/process-output-node.md)
- [大模型节点](../../raw/application-user-guide/llm-application/workflow-application/llm-node.md)
- [知识库节点](../../raw/application-user-guide/llm-application/workflow-application/knowledge-base-node.md)
- [意图分类节点](../../raw/application-user-guide/llm-application/workflow-application/intent-node.md)
- [参数提取节点](../../raw/application-user-guide/llm-application/workflow-application/parameter-extraction-node.md)
- [多模态生成节点](../../raw/application-user-guide/llm-application/workflow-application/multimodal-generation-node.md)
- [智能体创建节点](../../raw/application-user-guide/llm-application/workflow-application/agent-create-node.md)
- [智能体群组节点](../../raw/application-user-guide/llm-application/workflow-application/agent-group-node.md)
- [API节点](../../raw/application-user-guide/llm-application/workflow-application/api-node.md)
- [脚本节点](../../raw/application-user-guide/llm-application/workflow-application/script-node.md)
- [函数计算节点](../../raw/application-user-guide/llm-application/workflow-application/fc-node.md)
- [AppFlow节点](../../raw/application-user-guide/llm-application/workflow-application/appflow-node.md)
- [MCP节点](../../raw/application-user-guide/llm-application/workflow-application/mcp-node.md)
- [插件节点](../../raw/application-user-guide/llm-application/workflow-application/plugin-node.md)
- [变量处理节点](../../raw/application-user-guide/llm-application/workflow-application/variable-processing-node.md)
- [应用组件节点](../../raw/application-user-guide/llm-application/workflow-application/component-node.md)
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


