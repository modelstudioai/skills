# llm application

`llm application` 是阿里云百炼平台面向开发者提供的核心能力抽象，涵盖智能体（Agent）与工作流（Workflow）两类应用范式。智能体应用以自然语言驱动、零代码方式实现意图识别、工具调用与自主规划；工作流应用则通过可视化节点编排，将大模型、API、函数计算等能力串联为可复现、可调试、可监控的确定性执行链路。二者共同构成构建生产级 AI 应用的基础设施。

## 支持的模型/功能

百炼 `llm application` 支持两类主流应用形态及其对应能力：

- **智能体应用**：分为 Agent 1.0（旧版）和 Agent 2.0（新版）。Agent 1.0 采用“先检索后决策”模式，知识库与插件调用逻辑分离；Agent 2.0 将知识库、MCP 服务等统一建模为工具，由模型自主规划调用顺序与时机，并完整暴露“规划-执行-反思”链路 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。Agent 2.0 推荐用于复杂任务，而 Agent 1.0 仍适用于流程固定、意图单一的场景。
  
- **工作流应用**：提供 20+ 类型节点，覆盖全栈能力：
  - **基础节点**：大模型节点、多模态生成节点、知识库节点；
  - **工具节点**：API 节点、函数计算（FC）节点、MCP 节点、插件节点、AppFlow 节点、应用组件节点；
  - **逻辑节点**：条件判断节点、循环节点、批处理节点、脚本节点；
  - **数据解析节点**：文档/图片/音频/视频解析节点，支持结构化提取；
  - **辅助节点**：流程输出节点、变量处理节点、变量赋值节点、记忆库节点等。

> **注意**：Agent 1.0 仅支持在旧版控制台创建，且其分享渠道（魔笔、钉钉、微信等）不兼容 Agent 2.0；Agent 2.0 仅支持 API 调用 [分享智能体应用](../../raw/application-user-guide/llm-application/application-publishing-and-sharing/share-an-application.md)。

## 关键参数

各类节点均提供标准化参数配置，核心通用参数包括：

- **模型参数**（大模型节点、意图分类节点、参数提取节点等）：
  - `temperature`：控制输出随机性（范围 `[0, 2)`），默认 `0.7`；
  - `top_p`：控制输出多样性（范围 `(0, 1]`），默认 `0.8`；
  - `max_tokens`（最长回复长度）：模型输出 token 上限，不同模型上限不同；
  - `enable_thinking`：是否启用深度思考模式，影响推理过程输出。

- **执行控制参数**（API 节点、插件节点、脚本节点等）：
  - `timeout`：超时时间（秒），如 API 节点默认 `5` 秒，FC 节点固定 `60` 秒；
  - `max_retries` 与 `retry_interval`：失败重试策略，默认关闭，开启后需配置重试次数（1–10）与间隔（300–10000 ms）。

- **上下文与记忆参数**（大模型节点、意图分类节点、应用组件节点等）：
  - `memory_type`：支持 `node_cache`（本节点内缓存）或 `custom_cache`（引用全局 `historyList` 变量）；
  - `memory_rounds`：缓存轮次（1–50），默认 `3`。

- **批量处理参数**（批处理节点、大模型节点批量模式）：
  - `batch_size`（并行运行数量）：默认 `5`，影响并发资源消耗；
  - `batch_limit`（批处理次数上限）：默认 `30`（批处理节点）或 `50`（大模型节点），防止单次处理过载。

## 使用方式

### 创建与部署
- **智能体应用**：通过控制台「应用管理」→「创建智能体」入口，选择 Agent 2.0（默认）或点击「旧版 Agent 创建入口」跳转至旧版控制台 [开始使用](../../raw/application-user-guide/llm-application/llm-application-start-using.md)。
- **工作流应用**：在控制台「应用管理」→「创建工作流应用」，通过拖拽节点、连线配置完成编排。
- **CLI 调用**：使用 `bl app call --app-id <ID> --prompt "..."` 命令调用已发布应用 [使用 CLI](../../raw/application-user-guide/llm-application/llm-application-start-using/flow-agent-cli.md)。

### 节点集成关键实践
- **输入/输出绑定**：所有节点均支持通过 `/` 触发变量选择器，引用上游节点输出（如 `${开始/query}`）、系统变量（如 `historyList`）或自定义变量。
- **分支控制**：条件判断节点、意图分类节点输出 IF/ELSE 分支，支持多分支并行；循环节点与批处理节点分别实现串行/并行迭代。
- **状态传递**：循环节点依赖「中间变量」跨轮次传递状态；变量赋值节点支持写入会话变量、内置变量及循环中间变量 [变量赋值节点](../../raw/application-user-guide/llm-application/workflow-application/variable-assignment-node.md)。
- **异步任务管理**：MA 异步任务节点提交长耗时任务后返回 Task ID，结果需通过「任务中心」查询 [任务中心](../../raw/application-user-guide/llm-application/flow-agent-task-center.md)。

## 限制和注意事项

- **资源与配额**：
  - 批处理节点数组长度上限为 `30`（默认），循环节点最大循环次数为 `1000`；
  - 文档解析单文件 ≤ 150 MB / 1.5 万页；图片 ≤ 20 MB；音视频 ≤ 512 MB；
  - 异步任务与同步调用共享单应用 QPS 配额 [应用限流](../../raw/application-user-guide/bailian-application-calling/flow-agent-rate-limiting.md)。

- **功能约束**：
  - 脚本节点运行于沙箱环境，**禁止直接访问公网**（HTTP/HTTPS/DNS），需调用外部服务时必须使用 API 节点、插件节点或 MCP 节点 [脚本节点](../../raw/application-user-guide/llm-application/workflow-application/script-node.md)；
  - 批处理体内**不支持嵌套批处理或循环节点**，也不支持添加流程输出节点；
  - Agent 2.0 不支持魔笔、钉钉等 UI 分享渠道，仅支持 API 调用。

- **版本与兼容性**：
  - Agent 1.0 与 Agent 2.0 的配置项、能力边界、调试体验存在显著差异，迁移需重新设计提示词与工具集成逻辑；
  - 工作流中的「应用组件节点」可复用已发布的智能体或工作流组件，但组件本身必须已发布且与当前应用同属一个业务空间 [使用智能体或工作流作为组件](../../raw/application-user-guide/llm-application/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。

## 来源文档

- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [开始和结束节点](../../raw/application-user-guide/llm-application/workflow-application/start-end-node.md)
- [概述](../../raw/application-user-guide/llm-application/workflow-application/introduction.md)
- [循环节点](../../raw/application-user-guide/llm-application/workflow-application/loop-node.md)
- [条件判断节点](../../raw/application-user-guide/llm-application/workflow-application/conditional-node.md)
- [批处理节点](../../raw/application-user-guide/llm-application/workflow-application/batch-node.md)
- [流程输出节点](../../raw/application-user-guide/llm-application/workflow-application/process-output-node.md)
- [大模型节点](../../raw/application-user-guide/llm-application/workflow-application/llm-node.md)
- [知识库节点](../../raw/application-user-guide/llm-application/workflow-application/knowledge-base-node.md)
- [意图分类节点](../../raw/application-user-guide/llm-application/workflow-application/intent-node.md)
- [参数提取节点](../../raw/application-user-guide/llm-application/workflow-application/parameter-extraction-node.md)
- [多模态生成节点](../../raw/application-user-guide/llm-application/workflow-application/multimodal-generation-node.md)
- [智能体群组节点](../../raw/application-user-guide/llm-application/workflow-application/agent-group-node.md)
- [智能体创建节点](../../raw/application-user-guide/llm-application/workflow-application/agent-create-node.md)
- [函数计算节点](../../raw/application-user-guide/llm-application/workflow-application/fc-node.md)
- [API节点](../../raw/application-user-guide/llm-application/workflow-application/api-node.md)
- [插件节点](../../raw/application-user-guide/llm-application/workflow-application/plugin-node.md)
- [脚本节点](../../raw/application-user-guide/llm-application/workflow-application/script-node.md)
- [AppFlow节点](../../raw/application-user-guide/llm-application/workflow-application/appflow-node.md)
- [MCP节点](../../raw/application-user-guide/llm-application/workflow-application/mcp-node.md)
- [变量处理节点](../../raw/application-user-guide/llm-application/workflow-application/variable-processing-node.md)
- [变量赋值节点](../../raw/application-user-guide/llm-application/workflow-application/variable-assignment-node.md)
- [文档解析节点](../../raw/application-user-guide/llm-application/workflow-application/document-extraction-node.md)
- [图片解析节点](../../raw/application-user-guide/llm-application/workflow-application/image-extraction-node.md)
- [音频解析节点](../../raw/application-user-guide/llm-application/workflow-application/audio-extraction-node.md)
- [视频解析节点](../../raw/application-user-guide/llm-application/workflow-application/video-extraction-node.md)
- [数据连接器节点](../../raw/application-user-guide/llm-application/workflow-application/data-connector-node.md)
- [记忆库节点](../../raw/application-user-guide/llm-application/workflow-application/memory-node.md)
- [MA 同步执行节点](../../raw/application-user-guide/llm-application/workflow-application/ma-sync-node.md)
- [MA 异步任务节点](../../raw/application-user-guide/llm-application/workflow-application/ma-async-node.md)
- [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [开始使用](../../raw/application-user-guide/llm-application/llm-application-start-using.md)
- [概述](../../raw/application-user-guide/llm-application/llm-application-start-using/flow-agent-introduction.md)
- [使用 CLI](../../raw/application-user-guide/llm-application/llm-application-start-using/flow-agent-cli.md)
- [应用发布与分享](../../raw/application-user-guide/llm-application/application-publishing-and-sharing.md)
- [分享智能体应用](../../raw/application-user-guide/llm-application/application-publishing-and-sharing/share-an-application.md)
- [使用智能体或工作流作为组件](../../raw/application-user-guide/llm-application/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [UI设计器](../../raw/application-user-guide/llm-application/application-publishing-and-sharing/ui-designer.md)
- [任务中心](../../raw/application-user-guide/llm-application/flow-agent-task-center.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)
- [应用组件节点](../../raw/application-user-guide/llm-application/workflow-application/component-node.md)


