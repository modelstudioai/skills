# llm application

阿里云百炼的 LLM Application 是面向开发者构建 AI 原生应用的核心能力集合，提供零代码智能体（Agent）与低代码工作流（Workflow）两大范式。智能体应用通过提示词驱动自主规划与工具调用，适用于意图明确、需动态决策的对话场景；工作流应用则通过可视化节点编排实现确定性、可复现的多步骤任务执行，适用于流程复杂、需强控制与集成的业务场景。

## 支持的模型/功能

百炼 LLM Application 支持两类核心应用形态及其对应能力：

- **智能体应用**：分为 Agent 1.0（旧版）和 Agent 2.0（新版）。Agent 2.0 将知识库、MCP 等统一为工具，由模型自主规划调用顺序，并完整展示“规划-执行-反思”链路，推荐作为新项目首选；Agent 1.0 仅支持旧版控制台，其知识库与插件调用为分阶段触发，过程透明度较低 [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)。新版智能体还提供 `AUTO` 智能模式，根据任务复杂度（如上下文长度、问题类型）自动路由至性能/均衡/经济档位模型，兼顾效果与成本 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。

- **工作流应用**：提供 20+ 类节点，覆盖基础（大模型、知识库、多模态生成）、工具（API、函数计算、MCP、插件、AppFlow）、逻辑（条件判断、循环、批处理、脚本）及数据处理（文档/图片/音视频/视频解析、变量处理）等全栈能力。其中，[多模态生成节点](../../raw/application-user-guide/llm-application/workflow-application/multimodal-generation-node.md) 支持图像、视频、音频三类内容生成；[文档解析节点](../../raw/application-user-guide/llm-application/workflow-application/document-extraction-node.md) 和 [图片解析节点](../../raw/application-user-guide/llm-application/workflow-application/image-extraction-node.md) 分别针对不同文件类型提供结构化提取能力。

> **注意**：Agent 1.0 与 Agent 2.0 在能力边界上存在显著差异。Agent 1.0 的分享渠道（魔笔、钉钉、微信）仅对其生效，而 Agent 2.0 仅支持 API 调用 [分享智能体应用](../../raw/application-user-guide/llm-application/application-publishing-and-sharing/share-an-application.md)。开发者在选型时应以目标交付方式为首要依据。

## 关键参数

各类节点均提供标准化参数配置，核心通用参数如下：

- **模型参数**：所有大模型类节点（大模型节点、意图分类节点、参数提取节点、智能体创建节点等）均支持 `temperature`（控制随机性，范围 [0,2)，默认 0.7）、`top_p`（控制多样性，默认 0.8）、`max_tokens`（最长回复长度，默认 1024）及 `enable_thinking`（是否开启思考模式）。Agent 2.0 的 `AUTO` 模式下，`temperature` 等参数仍可全局配置，但模型选择由平台动态决定。

- **上下文管理**：`携带的上下文轮数`（Agent 1.0）或 `记忆` 配置（工作流节点）用于控制历史对话可见范围，支持“本节点缓存”（隔离）与“自定义缓存”（全局共享 `historyList`）两种模式。

- **执行控制**：`失败时重试`（最大重试次数 1–10，重试间隔 300–10000ms）和 `异常处理`（默认值或异常分支）是 API、函数计算、插件等外部调用节点的共性配置，保障流程鲁棒性。

- **批处理与循环**：`并行运行数量`（批处理节点，默认 5）和 `循环次数`（循环节点，1–1000）是批量任务的关键性能参数，需结合下游服务并发能力谨慎设置。

## 使用方式

- **智能体应用**：通过新版控制台 [应用管理](https://bailian.console.aliyun.com/flow-agent/app-center) → **创建智能体** 即可启动。配置核心项为模型（推荐 `千问-Max-Latest`）、系统提示词（定义角色与约束）、以及工具（知识库、MCP 服务）。测试时直接在对话框输入即可验证 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。

- **工作流应用**：在控制台画布中拖拽节点并连线。典型模式为：`开始节点`（接收 `query`/`imageList` 等输入）→ `条件判断节点` 或 `意图分类节点`（路由）→ `大模型节点`/`知识库节点`/`MCP节点`（核心处理）→ `结束节点`（输出）。对于批量任务，使用 `批处理节点`（并行）或 `循环节点`（串行+中间变量）；对于异步长耗时任务，使用 `MA 异步任务节点` 并在 [任务中心](../../raw/application-user-guide/llm-application/flow-agent-task-center.md) 查看结果。

- **CLI 调用**：已发布应用可通过 `bl app call --app-id <ID> --prompt "..."` 命令快速集成到开发环境，适合自动化测试与轻量级集成 [使用 CLI](../../raw/application-user-guide/llm-application/llm-application-start-using/flow-agent-cli.md)。

## 限制和注意事项

- **版本与功能隔离**：Agent 1.0 与 Agent 2.0 不互通。Agent 1.0 应用无法升级为 2.0，且其分享能力（UI、钉钉等）对 2.0 不可用；反之，2.0 的高级规划能力也无法在 1.0 中复现。

- **资源与配额**：文件解析有严格大小限制（文档 150MB、图片 20MB、音视频 512MB）；工作流中 `批处理节点` 的 `批处理次数上限` 默认 30，`循环节点` 最大循环次数为 1000，超限将被截断。异步任务与同步调用共享单应用 QPS 配额 [应用限流](../../raw/application-user-guide/bailian-application-calling/flow-agent-rate-limiting.md)。

- **安全与网络**：`脚本节点` 运行于沙箱环境，**禁止访问公网**，需调用外部服务时必须使用 `API节点`、`MCP节点` 或 `插件节点` [脚本节点](../../raw/application-user-guide/llm-application/workflow-application/script-node.md)。

- **调试与可观测性**：工作流执行中可使用 `流程输出节点` 实时反馈状态；`智能体群组节点` 的 `agProcess` 字段以 Markdown 格式输出完整调度过程，便于审计；所有异步任务均可在 [任务中心](../../raw/application-user-guide/llm-application/flow-agent-task-center.md) 追踪全生命周期日志。

## 来源文档

- [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [开始和结束节点](../../raw/application-user-guide/llm-application/workflow-application/start-end-node.md)
- [概述](../../raw/application-user-guide/llm-application/workflow-application/introduction.md)
- [条件判断节点](../../raw/application-user-guide/llm-application/workflow-application/conditional-node.md)
- [批处理节点](../../raw/application-user-guide/llm-application/workflow-application/batch-node.md)
- [循环节点](../../raw/application-user-guide/llm-application/workflow-application/loop-node.md)
- [流程输出节点](../../raw/application-user-guide/llm-application/workflow-application/process-output-node.md)
- [大模型节点](../../raw/application-user-guide/llm-application/workflow-application/llm-node.md)
- [知识库节点](../../raw/application-user-guide/llm-application/workflow-application/knowledge-base-node.md)
- [意图分类节点](../../raw/application-user-guide/llm-application/workflow-application/intent-node.md)
- [参数提取节点](../../raw/application-user-guide/llm-application/workflow-application/parameter-extraction-node.md)
- [多模态生成节点](../../raw/application-user-guide/llm-application/workflow-application/multimodal-generation-node.md)
- [智能体创建节点](../../raw/application-user-guide/llm-application/workflow-application/agent-create-node.md)
- [智能体群组节点](../../raw/application-user-guide/llm-application/workflow-application/agent-group-node.md)
- [API节点](../../raw/application-user-guide/llm-application/workflow-application/api-node.md)
- [函数计算节点](../../raw/application-user-guide/llm-application/workflow-application/fc-node.md)
- [插件节点](../../raw/application-user-guide/llm-application/workflow-application/plugin-node.md)
- [脚本节点](../../raw/application-user-guide/llm-application/workflow-application/script-node.md)
- [MCP节点](../../raw/application-user-guide/llm-application/workflow-application/mcp-node.md)
- [应用组件节点](../../raw/application-user-guide/llm-application/workflow-application/component-node.md)
- [AppFlow节点](../../raw/application-user-guide/llm-application/workflow-application/appflow-node.md)
- [变量处理节点](../../raw/application-user-guide/llm-application/workflow-application/variable-processing-node.md)
- [文档解析节点](../../raw/application-user-guide/llm-application/workflow-application/document-extraction-node.md)
- [变量赋值节点](../../raw/application-user-guide/llm-application/workflow-application/variable-assignment-node.md)
- [图片解析节点](../../raw/application-user-guide/llm-application/workflow-application/image-extraction-node.md)
- [音频解析节点](../../raw/application-user-guide/llm-application/workflow-application/audio-extraction-node.md)
- [视频解析节点](../../raw/application-user-guide/llm-application/workflow-application/video-extraction-node.md)
- [数据连接器节点](../../raw/application-user-guide/llm-application/workflow-application/data-connector-node.md)
- [MA 同步执行节点](../../raw/application-user-guide/llm-application/workflow-application/ma-sync-node.md)
- [记忆库节点](../../raw/application-user-guide/llm-application/workflow-application/memory-node.md)
- [MA 异步任务节点](../../raw/application-user-guide/llm-application/workflow-application/ma-async-node.md)
- [开始使用](../../raw/application-user-guide/llm-application/llm-application-start-using.md)
- [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [概述](../../raw/application-user-guide/llm-application/llm-application-start-using/flow-agent-introduction.md)
- [应用发布与分享](../../raw/application-user-guide/llm-application/application-publishing-and-sharing.md)
- [分享智能体应用](../../raw/application-user-guide/llm-application/application-publishing-and-sharing/share-an-application.md)
- [使用 CLI](../../raw/application-user-guide/llm-application/llm-application-start-using/flow-agent-cli.md)
- [使用智能体或工作流作为组件](../../raw/application-user-guide/llm-application/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)
- [应用功能动态](../../raw/application-user-guide/llm-application/application-release-notes.md)
- [UI设计器](../../raw/application-user-guide/llm-application/application-publishing-and-sharing/ui-designer.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)
- [任务中心](../../raw/application-user-guide/llm-application/flow-agent-task-center.md)


