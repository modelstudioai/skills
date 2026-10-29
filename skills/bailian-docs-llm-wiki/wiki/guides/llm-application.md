# llm application

`llm application` 是百炼平台提供的低代码/无代码 LLM 应用构建能力，支持通过可视化编排（Flow Agent）或 [Prompt 工程](../concepts/prompt-engineering.md)快速创建智能体（Agent）、工作流（Workflow）等可部署、可调用的应用。开发者无需从零训练模型，即可基于平台预置能力集成知识库、插件、多步骤逻辑与外部系统。该能力面向生产环境设计，适用于客服助手、文档分析、自动化任务等场景。

## 支持的模型与功能

- **核心类型**：支持两类应用形态——单智能体（Agent 1.0 和 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)）和 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)，后者支持多节点条件分支、并行执行与状态传递。
- **扩展能力**：可绑定 [插件](../../raw/application-user-guide/plug-in.md) 实现 API 调用（如天气、数据库），接入 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md) 模块实现私有文档理解，也可复用平台级 [Prompt](../../raw/application-user-guide/prompt.md) 管理能力进行提示词版本控制。
- **运行时依赖**：底层默认调用百炼托管的 Qwen 系列大模型（如 qwen-max、qwen-plus），部分高级节点（如代码解释器）需显式指定模型。

## 关键参数

- `app_id`：应用唯一标识，发布后生成，用于 [应用调用](../../raw/application-user-guide/bailian-application-calling.md) 接口。
- `inputs`：JSON 对象，字段名需与应用内定义的输入变量严格一致（区分大小写），不支持嵌套过深（建议 ≤3 层）。
- `stream`：布尔值，仅对支持流式响应的节点生效；若设为 `true`，需按 SSE 协议解析响应。
- `trace_id`：可选，用于全链路追踪，需符合 UUID v4 格式。

## 使用方式

1. **构建**：在控制台「应用开发」页选择「新建应用」→「智能体应用」或「工作流应用」，拖拽节点配置逻辑（如 LLM 节点、条件判断、HTTP 请求）；
2. **调试**：使用右上角「测试」面板输入样例 `inputs`，实时查看节点输出与 token 消耗；
3. **发布**：点击「发布」生成 `app_id`，随后可通过 HTTP POST 调用 `/v1/applications/{app_id}/invoke`（参考 [应用调用](../../raw/application-user-guide/bailian-application-calling.md) 文档）；
4. **集成**：支持 SDK（Python/Java）调用，亦可配置 Webhook 或通过 [任务中心](../../raw/application-user-guide/llm-application/flow-agent-task-center.md) 批量触发[异步任务](../concepts/asynchronous-task.md)。

## 限制和注意事项

- 单次请求最大 `inputs` 大小为 2 MB；工作流总节点数上限为 50，循环节点最多嵌套 3 层；
- Agent 2.0 默认启用记忆机制（Conversation History），但历史上下文长度受模型 context window 限制，超出部分将被截断；
- > **注意**：[智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md) 已进入维护模式，新项目应优先使用 Agent 2.0；二者在记忆管理、错误重试策略上存在不兼容变更，迁移前请仔细比对 [应用功能动态](../../raw/application-user-guide/llm-application/application-release-notes.md)；
- 文件问答模块仅支持 PDF/DOCX/TXT/MD 格式，单文件 ≤100 MB，且 OCR 能力需额外开通权限；
- 权限隔离以应用粒度生效，[权限管理](../../raw/application-user-guide/application-permission-management.md) 中未显式授予的成员无法查看或调试应用。

## 来源文档

- [Flow Agent](../../raw/application-user-guide/llm-application.md)


