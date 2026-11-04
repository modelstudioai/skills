# agent development

百炼平台提供多种 Agent 开发范式，支持从低代码编排到高自由度沙箱开发的全链路能力。开发者可根据业务复杂度、可控性需求和运维成本，在 Managed Agent、Flow Agent 和 Sandbox 三种模式中选择合适路径。所有模式均基于百炼统一的推理与调度底座，共享模型调用、工具集成和会话管理能力。

## 支持的模型与功能

- **Managed Agent**：面向标准化场景（如客服问答、知识库检索），预置意图识别、多轮对话状态管理、RAG 增强等能力，无需编写逻辑代码；底层默认使用 Qwen-Max 或 Qwen-Plus，支持通过 [原文标题](../../raw/application-user-guide/agent-development/managed-agents.md) 查看具体模型绑定规则与扩展方式。  
- **Flow Agent**：基于可视化流程图构建 LLM 应用，支持条件分支、并行调用、自定义函数节点及外部 API 集成；其执行引擎兼容全部百炼托管模型（含 Qwen 系列、GLM 系列及第三方模型 API），详见 [原文标题](../../raw/application-user-guide/agent-development/llm-application.md)。  
- **Sandbox**：提供 Python 运行时沙箱，允许完全自定义 Agent 行为（如重写 `run()` 方法、接入私有工具链、实现异步流式响应）；但仅支持同步调用 Qwen-Max/Qwen-Plus，不支持 GLM 等非 Qwen 模型——该限制在 [原文标题](../../raw/application-user-guide/agent-development/sandbox.md) 中明确说明，与 Flow Agent 的模型兼容性存在差异。

> **注意**：Flow Agent 文档中提及“可配置任意百炼支持模型”，而 Sandbox 文档明确限定仅支持 Qwen 系列。二者存在模型覆盖范围不一致问题，请以 Sandbox 文档为准，避免在沙箱中尝试调用 GLM 模型导致运行时失败。

## 关键参数

- `model`: 指定主推理模型（如 `"qwen-max"`），对 Managed Agent 和 Flow Agent 为可选（有默认值），对 Sandbox 为必填且仅限白名单模型。  
- `tools`: 工具列表，格式为 `[{ "name": "...", "description": "...", "parameters": {...} }]`；Sandbox 中需额外实现 `tool_call` 回调逻辑。  
- `stream`: 布尔值，控制是否启用流式响应；Flow Agent 和 Sandbox 均支持，但 Managed Agent 当前不支持[流式输出](../concepts/streaming-output.md)（参见 [原文标题](../../raw/application-user-guide/agent-development/managed-agents.md)）。  
- `max_iterations`: 最大循环/重试次数（默认 10），适用于需自主规划的 Agent 场景。

## 使用方式

1. **创建 Agent**：在控制台「应用开发」→「Agent」页选择模式（Managed / Flow / Sandbox）；  
2. **配置核心组件**：填写 prompt、绑定知识库、添加 tools（Flow/Sandbox 可拖拽或编码）、设置参数；  
3. **调试与发布**：使用内置 Playground 测试多轮交互，通过 API Key 或 SDK 调用已发布 endpoint；Flow Agent 支持导出 JSON 流程定义，Sandbox 支持上传 `.py` 文件。

## 限制和注意事项

- Managed Agent 不支持自定义 Python 逻辑，且无法修改底层对话状态机；若需深度定制，应选用 Flow Agent 或 Sandbox。  
- Sandbox 沙箱环境禁止访问外网（除显式授权的 Webhook 外），且单次执行超时为 60 秒；超时行为在 [原文标题](../../raw/application-user-guide/agent-development/sandbox.md) 中有明确定义。  
- 所有 Agent 模式均不支持跨账号共享调试会话上下文，生产环境需自行维护 `session_id` 并传入请求 header。

## 来源文档

- [Agent 开发运行](../../raw/application-user-guide/agent-development.md)


