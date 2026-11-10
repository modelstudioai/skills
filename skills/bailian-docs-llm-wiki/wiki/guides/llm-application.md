# llm application

`llm application` 是阿里云百炼平台面向开发者提供的核心 AI 应用构建能力，涵盖零代码智能体（Agent）与低代码工作流（Workflow）两大范式。智能体应用通过提示词驱动、自主规划与[工具调用](../concepts/tool-calling.md)解决开放式任务；工作流应用则通过可视化节点编排实现确定性、可复现的多步骤任务执行。二者共同支撑从简单问答到复杂业务流程的全场景 AI 应用落地。

## 支持的模型/功能

平台提供两类主流应用形态，其底层模型与扩展能力高度统一：

- **智能体应用**：支持 Agent 1.0（旧版控制台）与 Agent 2.0（新版控制台默认）。Agent 2.0 将知识库、MCP、插件等统一为工具，由模型自主规划调用顺序，过程透明可追溯；Agent 1.0 则采用分阶段策略（先 RAG 后[工具调用](../concepts/tool-calling.md)），适用于流程固定场景 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。  
- **工作流应用**：提供 20+ 类节点，覆盖基础（大模型、多模态生成、知识库）、工具（API、MCP、函数计算、插件、AppFlow）、逻辑（条件判断、循环、批处理、意图分类）及数据处理（文档/图片/音视频/视频解析、变量处理、变量赋值）等全链路能力。所有节点均支持参数化配置与变量引用，形成端到端的数据流闭环。

关键能力模块包括：
- **RAG 增强**：知识库节点支持文档、表格、图片三类知识源检索，可配置 `topK`、智能调用、二次过滤等策略 [知识库节点](../../raw/application-user-guide/llm-application/workflow-application/knowledge-base-node.md)；
- **多模态处理**：多模态生成节点支持图像/视频/音频生成；文档/图片/音视频/视频解析节点分别提取结构化内容，适配不同输入格式；
- **外部集成**：API 节点（HTTP）、MCP 节点（标准化工具协议）、函数计算节点（FC）、AppFlow 节点（跨系统数据流）、插件节点（官方/自定义）提供灵活的系统对接能力；
- **智能调度**：智能体群组节点基于决策模型自动选择子智能体协同；MA 同步/异步节点支持托管智能体的长时任务管理。

> **注意**：文档 40 明确指出“分享渠道（魔笔分享渠道、钉钉、微信、组件、音视频实时互动）均为 **Agent 1.0** 智能体应用的功能。**Agent 2.0** 智能体应用仅支持通过 API 调用，不支持上述分享渠道”，而文档 33 的快速开始流程已默认引导至新版控制台创建 Agent 2.0。开发者需根据发布需求明确版本选型，避免因版本不兼容导致分享功能失效。

## 关键参数

各节点共性参数设计一致，便于统一管理：

- **模型通用参数**（大模型、意图分类、参数提取、智能体创建、智能体群组等节点）：
  - `temperature`：控制输出随机性（范围 `[0, 2)`），值越高越多样；
  - `top_p`：控制输出多样性（默认 `0.80`），值越大结果越发散；
  - `max_tokens`（最长回复长度）：模型输出 token 上限（默认 `1024`），不含提示词；
  - `enable_thinking`：是否开启深度思考模式（默认开启），影响推理过程输出；
  - `thinking_budget`：思考模式下思维链最大 token 数（默认 `4000`）。

- **工作流特有参数**：
  - **循环节点**：`循环次数`（1–1000）、`中间变量`（用于跨轮次状态传递）、`终止条件`（基于中间变量判断）；
  - **批处理节点**：`并行运行数量`（默认 `5`，影响并发资源消耗）、`批处理次数上限`（默认 `30`，防止单次处理过载）；
  - **条件判断节点**：支持 `所有`（AND）与 `任一`（OR）条件关系，分支命名自动映射为 `IF`/`ELSE`；
  - **开始/结束节点**：`query`（用户输入）、`historyList`（对话历史）、`imageList`（图片列表）为预置变量；结束节点支持 `文本输出`、`JSON输出`、`流式输出` 三种模式。

## 使用方式

### 创建与调试
- **智能体应用**：在新版控制台 [应用管理](https://bailian.console.aliyun.com/flow-agent/app-center) 点击 **创建智能体**，选择模型、配置系统提示词、添加知识库或 MCP 工具即可快速启动；测试阶段直接在对话框输入问题验证效果。
- **工作流应用**：通过画布拖拽或节点 + 按钮添加节点，按逻辑连线（如 `开始 → 条件判断 → 多个大模型节点`）。所有节点均支持实时调试：运行后点击节点可查看该节点的详细输入/输出、token 消耗及错误信息 [概述](../../raw/application-user-guide/llm-application/workflow-application/introduction.md)。

### 变量与数据流
- **变量引用统一语法**：`${节点名/变量名}`（如 `${开始/query}`、`${大模型/result}`），在提示词、参数配置、输出模板中均可使用；
- **数据流向控制**：
  - `流程输出节点` 用于中间状态反馈（如“正在处理…”），支持[流式输出](../concepts/streaming-output.md)；
  - `变量赋值节点` 实现“写回”能力，可更新会话变量、内置变量或循环中间变量；
  - `变量处理节点` 提供 `文本输出`（模板拼接）、`JSON输出`（结构化封装）、`聚合分组`（多分支取首个非空值）三种模式，解决下游节点空值报错问题。

### 部署与调用
- **API 调用**：应用发布后获取 `app_id`，通过 `POST /v1/apps/{app_id}/chat`（同步）或 `/v1/apps/{app_id}/chat/async`（异步）调用；[异步任务](../concepts/asynchronous-task.md) ID 可在 [任务中心](../../raw/application-user-guide/llm-application/flow-agent-task-center.md) 查询状态与结果；
- **CLI 调用**：使用 `bl app call --app-id <id> --prompt "..."` 命令快速测试已发布应用；
- **UI 集成**：通过 UI 设计器将智能体或工作流发布为网页应用，支持钉钉、微信等渠道嵌入。

## 限制和注意事项

- **上下文与 [Token](../concepts/token.md) 限制**：所有节点均受模型上下文窗口约束。知识库检索结果、文档解析内容、循环/批处理的数组元素均计入上下文；超限时需调整 `topK`、切片长度或启用[流式输出](../concepts/streaming-output.md)缓解压力。
- **文件处理限制**：
  - 文档解析：单文件 ≤ 150 MB，页数 ≤ 1.5 万页；
  - 图片解析：单文件 ≤ 20 MB；
  - 音频/视频解析：单文件 ≤ 512 MB；
  - 所有解析节点均**仅支持单文件**，不支持列表批量解析（批处理节点需配合脚本节点预处理）。
- **网络与安全**：
  - 脚本节点运行于沙箱环境，**禁止直接访问公网**（HTTP/HTTPS/DNS），需调用外部服务时必须使用 API/MCP/插件节点；
  - API 节点调用第三方服务时，需将百炼服务 IP（`47.93.216.17`, `39.105.109.77`）加入目标服务器白名单。
- **版本与兼容性**：
  - Agent 1.0 与 Agent 2.0 不互通，Agent 2.0 的 `AUTO` 模式按统一刊例价计费，与实际路由模型无关；
  - 工作流中的 `智能体创建节点` 生成的智能体为临时实例，不产生独立应用；而 `应用组件节点` 必须引用已发布的智能体或工作流组件。
- **调试建议**：工作流执行异常时，优先检查节点间变量引用是否正确（如 `${开始/query}` 是否存在）、上游节点是否成功输出、API/MCP 节点的输入参数格式是否符合要求（参考对应节点的 [MCP节点](../../raw/application-user-guide/llm-application/workflow-application/mcp-node.md) 或 [API节点](../../raw/application-user-guide/llm-application/workflow-application/api-node.md) 文档）。

## 来源文档

- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [概述](../../raw/application-user-guide/llm-application/workflow-application/introduction.md)
- [条件判断节点](../../raw/application-user-guide/llm-application/workflow-application/conditional-node.md)
- [开始和结束节点](../../raw/application-user-guide/llm-application/workflow-application/start-end-node.md)
- [循环节点](../../raw/application-user-guide/llm-application/workflow-application/loop-node.md)
- [批处理节点](../../raw/application-user-guide/llm-application/workflow-application/batch-node.md)
- [流程输出节点](../../raw/application-user-guide/llm-application/workflow-application/process-output-node.md)
- [大模型节点](../../raw/application-user-guide/llm-application/workflow-application/llm-node.md)
- [意图分类节点](../../raw/application-user-guide/llm-application/workflow-application/intent-node.md)
- [知识库节点](../../raw/application-user-guide/llm-application/workflow-application/knowledge-base-node.md)
- [参数提取节点](../../raw/application-user-guide/llm-application/workflow-application/parameter-extraction-node.md)
- [智能体创建节点](../../raw/application-user-guide/llm-application/workflow-application/agent-create-node.md)
- [多模态生成节点](../../raw/application-user-guide/llm-application/workflow-application/multimodal-generation-node.md)
- [API节点](../../raw/application-user-guide/llm-application/workflow-application/api-node.md)
- [智能体群组节点](../../raw/application-user-guide/llm-application/workflow-application/agent-group-node.md)
- [函数计算节点](../../raw/application-user-guide/llm-application/workflow-application/fc-node.md)
- [脚本节点](../../raw/application-user-guide/llm-application/workflow-application/script-node.md)
- [MCP节点](../../raw/application-user-guide/llm-application/workflow-application/mcp-node.md)
- [插件节点](../../raw/application-user-guide/llm-application/workflow-application/plugin-node.md)
- [AppFlow节点](../../raw/application-user-guide/llm-application/workflow-application/appflow-node.md)
- [变量处理节点](../../raw/application-user-guide/llm-application/workflow-application/variable-processing-node.md)
- [应用组件节点](../../raw/application-user-guide/llm-application/workflow-application/component-node.md)
- [变量赋值节点](../../raw/application-user-guide/llm-application/workflow-application/variable-assignment-node.md)
- [文档解析节点](../../raw/application-user-guide/llm-application/workflow-application/document-extraction-node.md)
- [图片解析节点](../../raw/application-user-guide/llm-application/workflow-application/image-extraction-node.md)
- [音频解析节点](../../raw/application-user-guide/llm-application/workflow-application/audio-extraction-node.md)
- [数据连接器节点](../../raw/application-user-guide/llm-application/workflow-application/data-connector-node.md)
- [视频解析节点](../../raw/application-user-guide/llm-application/workflow-application/video-extraction-node.md)
- [记忆库节点](../../raw/application-user-guide/llm-application/workflow-application/memory-node.md)
- [MA 同步执行节点](../../raw/application-user-guide/llm-application/workflow-application/ma-sync-node.md)
- [MA 异步任务节点](../../raw/application-user-guide/llm-application/workflow-application/ma-async-node.md)
- [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [开始使用](../../raw/application-user-guide/llm-application/llm-application-start-using.md)
- [使用 CLI](../../raw/application-user-guide/llm-application/llm-application-start-using/flow-agent-cli.md)
- [概述](../../raw/application-user-guide/llm-application/llm-application-start-using/flow-agent-introduction.md)
- [应用发布与分享](../../raw/application-user-guide/llm-application/application-publishing-and-sharing.md)
- [使用智能体或工作流作为组件](../../raw/application-user-guide/llm-application/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [UI设计器](../../raw/application-user-guide/llm-application/application-publishing-and-sharing/ui-designer.md)
- [分享智能体应用](../../raw/application-user-guide/llm-application/application-publishing-and-sharing/share-an-application.md)
- [任务中心](../../raw/application-user-guide/llm-application/flow-agent-task-center.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)


