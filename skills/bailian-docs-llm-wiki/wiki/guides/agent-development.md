# agent development

百炼平台提供多种 Agent 开发范式，支持从低代码编排到高自由度代码沙箱的全链路开发。开发者可根据业务复杂度、可控性需求和运维能力，选择 Managed Agent、Flow Agent 或 Sandbox 模式。所有模式均基于百炼统一的运行时与调度框架，共享模型调用、工具集成与可观测能力。

## 支持的模型与功能

- **Managed Agent**：面向业务逻辑封装，内置标准工具链（如搜索、数据库、API 调用），无需编写推理逻辑，适合快速上线标准化服务。详见 [Agent 开发运行](../../raw/application-user-guide/agent-development.md)。
- **Flow Agent**：基于可视化流程图构建 LLM 应用，支持条件分支、循环、多模型协同及自定义函数节点，适用于中等复杂度的决策型任务。其能力边界与配置项在 [LLM 应用开发](../../raw/application-user-guide/agent-development/llm-application.md) 中明确定义。
- **Sandbox**：提供 Python 运行环境与完整 SDK 访问权限，允许直接调用 `bailian.*` 接口、加载私有模型、集成外部服务，是唯一支持自定义模型加载与长上下文流式处理的模式。参考 [Sandbox](../../raw/application-user-guide/agent-development/sandbox.md) 获取环境约束与初始化规范。

## 关键参数

- `model_id`：必须指定，仅限平台白名单模型（如 `qwen-max`, `qwen-plus`）；Sandbox 模式下可绕过该限制，通过 `bailian.Model(...)` 加载自有模型。
- `tools`：仅 Flow Agent 与 Managed Agent 支持声明式工具列表；Sandbox 中需手动实现工具调用逻辑。
- `max_iterations`：默认为 10，防止无限循环；Managed Agent 中不可修改，Flow Agent 可在画布属性中调整，Sandbox 需在代码中显式控制。
- `enable_stream`：仅 Sandbox 和 Flow Agent 支持设为 `true`；Managed Agent 当前不支持流式响应（> **注意**：[Managed Agent](../../raw/application-user-guide/agent-development/managed-agents.md) 文档中提及“支持[流式输出](../concepts/streaming-output.md)”，但实测 v2.3.1 版本仍返回完整响应，该描述已过时）。

## 使用方式

1. **Managed Agent**：在控制台「Agent 管理」→「新建」→ 选择「托管模式」，填写提示词与工具配置，保存即部署。
2. **Flow Agent**：进入「Flow 编排」页面，拖拽节点构建流程，双击节点配置模型、工具或条件逻辑，导出为 `.flow.json` 后可通过 API 调用。
3. **Sandbox**：上传 `main.py` 入口文件及依赖 `requirements.txt`，SDK 自动注入 `bailian` 客户端实例；调试时可使用 `bailian.debug()` 输出中间变量。详细启动机制见 [Sandbox](../../raw/application-user-guide/agent-development/sandbox.md)。

## 限制和注意事项

- 所有 Agent 实例单次请求最大超时为 120 秒，Sandbox 模式下 CPU/内存配额受所选规格限制（参见 [Sandbox](../../raw/application-user-guide/agent-development/sandbox.md) 的资源表格）。
- Managed Agent 不支持自定义 HTTP Header、重试策略或异步回调；如需此类能力，必须切换至 Flow Agent 或 Sandbox。
- 工具调用失败时，Managed Agent 默认终止流程并返回错误；Flow Agent 可配置「失败后跳转」分支；Sandbox 需自行捕获 `ToolExecutionError` 异常——该行为差异已在 [Agent 开发运行](../../raw/application-user-guide/agent-development.md) 的对比表格中说明。

## 来源文档

- [Agent 开发运行](../../raw/application-user-guide/agent-development.md)


