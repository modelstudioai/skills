# llm application

`llm application` 是百炼平台提供的低代码/无代码 LLM 应用构建能力，支持通过可视化编排或配置化方式快速创建智能体（Agent）、工作流（Workflow）等可部署、可调用的 AI 应用。其核心目标是降低 LLM 工程化门槛，同时保留对模型、工具、Prompt 等关键环节的精细控制。所有应用均基于 [Flow Agent](../../raw/application-user-guide/llm-application.md) 统一架构实现。

## 支持的模型与功能

- **模型支持**：默认集成平台托管的 Qwen 系列大模型（如 `qwen-max`、`qwen-plus`），也支持用户自有模型（需已接入百炼模型中心）；部分高级功能（如多跳推理、长上下文处理）依赖模型原生能力，具体以 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md) 文档说明为准。
- **核心功能类型**：
  - 单智能体应用（Single Agent）：面向对话式任务，支持插件调用、记忆管理、多轮状态跟踪；
  - 工作流应用（Workflow）：支持 DAG 图形化编排，节点可为 LLM 调用、条件判断、HTTP 请求、知识库检索等；
  - 文件问答（File QA）：基于上传文档构建私有知识库，支持 PDF/Word/Excel/TXT 等格式解析与语义检索；
  - 任务中心（Task Center）：用于异步长周期任务调度与状态监控，适用于批量处理、定时触发等场景。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model_id` | string | 是 | 指定基础大模型 ID，例如 `"qwen-max"`；必须已在当前项目中授权使用 |
| `prompt_template` | string | 否 | 自定义 Prompt 模板，支持 Jinja2 语法；若未指定，则使用 [Prompt](../../raw/application-user-guide/prompt.md) 中配置的默认模板 |
| `tools` | array | 否 | 插件列表，每个元素为 `{ "tool_name": "xxx", "tool_parameters": { ... } }`；工具需已在应用中启用并授权 |
| `retrieval_config` | object | 否 | 仅文件问答类应用有效，含 `top_k`、`score_threshold` 等向量检索参数 |

> **注意**：`model_id` 在 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md) 中支持按节点单独指定，但在单智能体应用中全局生效；若混用不兼容模型（如在同一个 workflow 中混用 qwen-turbo 和非 Qwen 模型），可能导致运行时错误。

## 使用方式

1. **创建应用**：在控制台「应用开发」→「新建应用」中选择类型（智能体/工作流/文件问答），完成基础配置；
2. **配置逻辑**：  
   - 智能体应用：在「编排」页添加工具、设置记忆策略、调整 Prompt；  
   - 工作流应用：拖拽节点、连线、双击节点配置参数；  
   - 文件问答：上传文件 → 构建索引 → 配置检索参数；
3. **调试与发布**：使用内置调试器验证输入输出；发布后获取 `app_id`，通过 [应用调用](../../raw/application-user-guide/bailian-application-calling.md) API 或 SDK 集成到业务系统。

## 限制和注意事项

- 单次请求最大上下文长度受所选模型限制（如 `qwen-max` 当前上限为 32768 tokens），超长输入将被截断；
- 文件问答应用单次上传文件总数 ≤ 50 个，总大小 ≤ 500 MB；知识库索引构建耗时随文件数量线性增长；
- 所有应用默认启用流式响应（`stream=true`），若需完整响应请显式设置 `stream=false`；
- 权限隔离严格：应用仅能访问其所属项目下已授权的模型、插件、知识库；跨项目资源需通过 [权限管理](../../raw/application-user-guide/application-permission-management.md) 显式授予。

## 来源文档

- [Flow Agent](../../raw/application-user-guide/llm-application.md)


