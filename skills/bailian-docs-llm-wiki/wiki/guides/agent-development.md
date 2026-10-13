# agent development

百炼平台提供多种 Agent 开发范式，支持从低代码编排到高自由度代码沙箱的全链路开发。开发者可根据任务复杂度、可控性需求和运维能力选择合适模式，所有 Agent 均可部署为 API 服务并集成至业务系统。核心能力围绕 LLM 编排、工具调用、状态管理与异步执行展开。

## 支持的模型与功能

- **Managed Agent**：基于预置模板与可视化节点（如 LLM 调用、条件分支、HTTP 请求）构建，无需编写代码，适合快速验证业务逻辑。支持多轮对话上下文维护与内置工具（如知识库检索、数据库查询）。详见 [Agent 开发运行](../../raw/application-user-guide/agent-development.md)。
- **Flow Agent**：面向开发者设计的声明式流程引擎，通过 YAML 或 JSON 定义节点拓扑与数据流转，支持自定义 Python 函数节点、外部 API 集成及错误重试策略。其能力边界在 [Flow Agent](../../raw/application-user-guide/agent-development/llm-application.md) 中有明确定义。
- **Sandbox**：提供隔离的 Python 执行环境，允许上传依赖、编写任意逻辑（含异步 I/O、第三方 SDK 调用），适用于需深度控制执行流或集成私有服务的场景。[Sandbox](../../raw/application-user-guide/agent-development/sandbox.md) 文档说明了资源限制与安全约束。

## 关键参数

- `timeout`: 全局超时（秒），Flow Agent 默认 30s，Sandbox 默认 120s；超过将强制终止执行。
- `max_iterations`: 仅 Managed Agent 和 Flow Agent 支持，限制循环/递归最大步数，默认 50，防止无限推理。
- `enable_tracing`: 布尔值，启用后返回完整执行轨迹（含各节点输入/输出、耗时、LLM token 统计），调试必备。
- `stream`: 布尔值，仅 Flow Agent 和 Sandbox 支持流式响应（`text/event-stream`），Managed Agent 不支持[流式输出](../concepts/streaming.md)。

## 使用方式

1. 在控制台「Agent 开发」页创建新 Agent，选择类型（Managed / Flow / Sandbox）；
2. 按向导配置基础信息（名称、描述、默认模型）；
3. 根据所选类型完成编辑：
   - Managed Agent：拖拽节点 + 设置参数；
   - Flow Agent：编写 YAML 流程定义，或使用可视化编辑器同步生成；
   - Sandbox：上传 `main.py` 及 `requirements.txt`，编写 `run()` 入口函数；
4. 点击「调试」测试输入/输出，确认无误后「发布」获取 API endpoint；
5. 调用时通过 HTTP POST 向 `/v1/agents/{agent_id}/invoke` 提交 JSON payload，结构统一为 `{ "input": { ... }, "parameters": { ... } }`。

## 限制和注意事项

- 所有 Agent 的单次请求 `input` 字段总大小上限为 2MB；超出将返回 `413 Payload Too Large`。
- Managed Agent 不支持自定义模型权重加载或 LoRA 微调，如需该能力请改用 Flow Agent 或 Sandbox。
- > **注意**：原始文档 [Agent 开发运行](../../raw/application-user-guide/agent-development.md) 中列出的“Managed Agent 支持 Python 脚本节点”已过时——该功能已于 v2.3.0 移除，实际仅 Flow Agent 和 Sandbox 支持代码执行。
- Sandbox 的网络访问默认仅允许白名单域名（如 `api.qwen.com`, `dashscope.aliyuncs.com`），如需新增需提交工单审批；而 Flow Agent 的 HTTP 节点无此限制。
- Flow Agent 的 YAML 定义中，`type: llm` 节点若未显式指定 `model` 参数，将回退至 Agent 创建时设定的默认模型；但 [Flow Agent](../../raw/application-user-guide/agent-development/llm-application.md) 文档中示例未强调此回退行为，易引发配置遗漏。

## 来源文档

- [Agent 开发运行](../../raw/application-user-guide/agent-development.md)


