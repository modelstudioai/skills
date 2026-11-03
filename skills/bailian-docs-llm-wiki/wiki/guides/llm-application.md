# llm application

`llm application` 是百炼平台提供的低代码/无代码 LLM 应用构建能力，支持通过可视化编排或配置方式快速创建智能体（Agent）、工作流（Workflow）等可部署、可调用的 AI 应用。开发者无需从零训练模型，即可基于预置能力组合 Prompt、工具、知识库与业务逻辑。该能力面向生产环境设计，兼顾灵活性与工程可控性。

## 支持的模型与功能

- **核心类型**：支持两类应用形态——智能体应用（含 Agent 1.0 和 [新版智能体应用（Agent 2.0）](../../raw/raw/application-user-guide/llm-application/new-single-agent-application.md)）和 [工作流应用](../../raw/raw/application-user-guide/llm-application/workflow-application.md)；二者均支持接入百炼托管的 Qwen 系列大模型（如 qwen-max、qwen-plus），也可绑定自定义模型（需已部署至百炼模型服务）。
- **扩展能力**：支持集成 [插件](../../raw/raw/application-user-guide/plug-in.md)（如天气、数据库、HTTP 调用）、[文件问答](../../raw/raw/application-user-guide/llm-application/file-q-a.md)（PDF/Word/Excel 等格式解析与检索）、Prompt 编排及外部知识库挂载。
- > **注意**：Agent 1.0 已进入维护期，新项目应优先使用 Agent 2.0；二者在上下文管理、工具调用协议和调试体验上存在不兼容差异，详见 [智能体应用（Agent 1.0）](../../raw/raw/application-user-guide/llm-application/single-agent-application.md) 与 [新版智能体应用（Agent 2.0）](../../raw/raw/application-user-guide/llm-application/new-single-agent-application.md) 的对比说明。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model_id` | string | 是 | 模型 ID，如 `qwen-max`；必须为当前账号有调用权限的模型 |
| `input_variables` | object | 否 | 定义运行时输入变量结构（如 `{ "query": "string", "user_id": "string" }`），用于校验和前端表单生成 |
| `enable_tracing` | boolean | 否 | 是否启用全链路追踪，默认 `false`；开启后可在 [任务中心](../../raw/raw/application-user-guide/llm-application/flow-agent-task-center.md) 查看完整执行日志与 token 消耗 |

## 使用方式

1. **创建**：在控制台「应用开发」→「新建应用」中选择「智能体应用」或「工作流应用」，按向导完成基础配置；
2. **编排**：通过画布拖拽节点（LLM 调用、条件分支、插件调用等），或在 YAML 模式下直接编辑 DSL（仅工作流应用支持）；
3. **调试**：使用内置调试器提交测试输入，实时查看各节点输出与耗时；
4. **发布与调用**：发布后获取应用 ID，通过 [应用调用](../../raw/raw/application-user-guide/bailian-application-calling.md) API（`POST /v1/applications/{app_id}/chat`）或 SDK 集成到业务系统。

## 限制和注意事项

- 单次请求最大上下文长度受所选模型限制（如 qwen-max 为 32768 tokens），工作流中多节点累计 token 不单独计费但受总长约束；
- 文件问答功能依赖文档解析服务，单文件上限 100 MB，且仅支持 UTF-8 编码文本内容；
- 应用内嵌 Prompt 不支持动态模板语法（如 `{{variable}}`）以外的 Jinja2 特性，复杂逻辑请移至插件或后端处理；
- > **注意**：[应用功能动态](../../raw/raw/application-user-guide/llm-application/application-release-notes.md) 中明确标注“Agent 2.0 默认启用流式响应”，但部分旧版 SDK 尚未适配 SSE 协议，建议升级至 `@alibaba/bailian-sdk@^2.3.0` 及以上版本。

## 来源文档

- [Flow Agent](../../raw/application-user-guide/llm-application.md)


