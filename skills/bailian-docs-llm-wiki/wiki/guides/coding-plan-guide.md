# coding plan guide

Coding Plan 是百炼平台面向代码生成任务提供的结构化推理能力，支持将自然语言需求拆解为多步执行计划，并调用代码解释器或工具链完成实现。该能力适用于函数生成、脚本编写、数据处理等需分步验证的编程场景，区别于单次响应的纯文本补全模型。其核心价值在于提升长流程代码任务的可靠性与可调试性。

## 支持的模型/功能

- 当前仅 `qwen-coding` 系列模型（如 `qwen-coding-32b`）原生支持 Coding Plan 模式，其他模型（包括 `qwen-max` 和 `qwen-plus`）**不支持**该模式下的 plan-execution 两阶段流程。
- 功能上支持：需求解析 → 子任务分解 → 工具调用决策（如 `python_interpreter`）→ 执行结果反馈 → 计划修正。不支持自定义工具注册或外部 API 自动绑定。
- 注意：`qwen-coding` 模型在启用 Coding Plan 后**自动禁用[流式输出](../concepts/streaming.md)（stream=false）**，且不兼容 `response_format: json_object` 参数，详见 [Coding Plan概述](../../raw/token-plan-user-guide/coding-plan-guide/coding-plan.md)。

## 关键参数

- `enable_coding_plan`: 布尔值，必须设为 `true` 以激活计划模式（默认 `false`）。
- `max_plan_steps`: 整数，最大计划步数，取值范围 `[1, 10]`，默认 `5`；超出后终止并返回当前结果。
- `tool_choice`: 字符串，仅支持 `"python_interpreter"`，暂不支持 `"auto"` 或其他工具标识。
- `temperature`: 建议设为 `0.0` 以保障计划步骤的确定性；非零值可能导致子任务逻辑漂移，参见 [常见问题](../../raw/token-plan-user-guide/coding-plan-guide/coding-plan-faq.md)。

## 使用方式

1. 在请求体中显式设置 `enable_coding_plan: true`，并确保模型为 `qwen-coding-*`；
2. 构造 `messages` 时，用户输入应为完整、无歧义的编程需求（例如：“生成一个读取 CSV 并绘制柱状图的脚本，要求处理缺失值并标注均值线”），避免模糊指令；
3. 调用成功后，响应体中将包含 `plan` 字段（数组，每项含 `step`, `description`, `tool_call`）和 `execution_result` 字段（最终执行输出）；
4. 如需调试中间步骤，可结合 `max_plan_steps: 1` 与 `logprobs: true` 查看首步计划置信度，参考 [Coding Plan概述](../../raw/token-plan-user-guide/coding-plan-guide/coding-plan.md) 中的调试示例。

## 限制和注意事项

- 单次请求最大上下文长度为 32k tokens，其中 plan 阶段占用约 1/3，执行阶段占用剩余配额；超长输入将被截断且不报错。
- 不支持跨会话状态保持：每次请求的 `python_interpreter` 环境完全隔离，无法复用前序请求中的变量或导入模块。
- > **注意**：原始文档 [Coding Plan（旧版）](../../raw/token-plan-user-guide/coding-plan-guide.md) 中提及“支持 `shell` 工具”，该描述已过时；当前仅 `python_interpreter` 可用，其余工具类型将被静默忽略。
- 输出中若含不可执行代码块（如未闭合的 triple-backtick），会导致执行中断并返回错误码 `PLAN_EXECUTION_FAILED`，建议预检用户输入格式。

## 来源文档

- [Coding Plan（旧版）](../../raw/token-plan-user-guide/coding-plan-guide.md)


