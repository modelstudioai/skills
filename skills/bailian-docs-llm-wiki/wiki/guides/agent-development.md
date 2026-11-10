# agent development

百炼平台提供多种 Agent 开发与运行模式，支持从低代码编排到高自由度沙箱环境的全栈开发路径。开发者可根据业务复杂度、可控性需求和运维能力选择合适范式，所有模式均基于统一的底层执行引擎。核心能力覆盖意图识别、[工具调用](../concepts/tool-calling.md)、多步推理与状态管理。

## 支持的模型/功能

- **Managed Agent**：平台托管的标准化 Agent，内置预置工具链（如搜索、计算、知识库检索），适合快速上线轻量级智能助手；其行为逻辑由平台配置驱动，不开放代码编辑。详见 [Agent 开发运行](../../raw/application-user-guide/agent-development.md)。
- **Flow Agent**：基于可视化流程图的 LLM 应用编排方式，支持节点化组合 LLM 调用、条件分支、变量传递与自定义函数；适用于中等复杂度的业务逻辑闭环。该模式在 [Flow Agent 文档](../../raw/application-user-guide/llm-application.md) 中有完整说明。
- **Sandbox Agent**：完全开放的 Python 沙箱环境，允许开发者编写任意逻辑（包括异步 I/O、第三方 SDK 调用、本地状态维护），通过 `@tool` 装饰器注册工具，由平台调度执行。详细约束见 [Sandbox](../../raw/application-user-guide/agent-development/sandbox.md)。

## 关键参数

- `model_id`：必须指定，仅支持百炼已发布的 Agent 专用模型（如 `qwen-max-agentic`、`qwen-plus-agentic`），通用大模型（如 `qwen-max`）不支持 Agent 模式。
- `enable_thinking`：布尔值，启用后开启多步推理规划（默认 `true`）；设为 `false` 时退化为单轮 prompt 响应，丧失[工具调用](../concepts/tool-calling.md)能力。
- `max_iterations`：最大推理步数，取值范围 `[1, 20]`，超限将强制终止并返回 `STOPPED` 状态；注意该参数在 [Sandbox](../../raw/application-user-guide/agent-development/sandbox.md) 中同样生效，但沙箱内可通过 `self.stop()` 主动退出。

## 使用方式

1. 创建应用时选择「Agent」类型；
2. 根据模式选择「Managed」「Flow」或「Sandbox」模板；
3. 配置模型、提示词（Prompt）、工具列表（Managed/Flow 可视化配置，Sandbox 需在代码中声明）；
4. 调用时传入 `input` 字符串或结构化 `input_object`（需与 Prompt 中变量名一致）；
5. 响应体含 `output`（最终结果）、`trace`（执行步骤日志）和 `status`（`SUCCESS`/`FAILED`/`STOPPED`）。

## 限制和注意事项

- Managed Agent 不支持自定义 Python 逻辑或外部依赖，所有工具必须从平台预置列表中选取；若需扩展能力，应切换至 Flow 或 Sandbox 模式。
- Flow Agent 的节点执行超时为 30 秒/节点，总流程超时为 120 秒；Sandbox 单次执行总时长上限为 60 秒，内存限制 2GB —— 这些硬性限制在 [Sandbox](../../raw/application-user-guide/agent-development/sandbox.md) 和 [Flow Agent 文档](../../raw/application-user-guide/llm-application.md) 中分别明确，但二者数值不一致，实际以调用时平台返回的 `422 Unprocessable Entity` 错误详情为准。
- > **注意**：原始文档中 [Agent 开发运行](../../raw/application-user-guide/agent-development.md) 将「应用广场」列为一种开发模式，但该入口仅提供可复用的成品 Agent 模板，**不支持二次开发或源码导出**，不应被归类为开发模式；开发者应将其视为部署参考而非开发路径。

## 来源文档

- [Agent 开发运行](../../raw/application-user-guide/agent-development.md)


