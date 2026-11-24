# agent development

百炼平台提供多种 Agent 开发范式，支持从低代码编排到高自由度代码沙箱的全栈开发路径。开发者可根据业务复杂度、可控性需求和运维能力选择合适模式，所有类型均统一接入百炼推理网关与可观测性体系。核心能力围绕 LLM 编排、工具调用、状态管理与调试诊断展开。

## 支持的模型与功能

- **Managed Agent**：平台托管的声明式 Agent，通过 YAML 配置定义工具链、记忆策略与终止条件，适合标准化任务（如客服问答、数据查询）；底层默认使用 Qwen-Max 或 Qwen-Plus，支持按需切换 [原文标题](../../raw/application-user-guide/agent-development.md)。
- **Flow Agent**：可视化流程编排 Agent，支持节点拖拽、条件分支、循环与自定义 Python 脚本节点；完整兼容百炼内置工具（如 WebSearch、数据库连接器）及用户上传的 API 工具 [原文标题](../../raw/application-user-guide/agent-development.md)。
- **Sandbox Agent**：完全开放的 Python 沙箱环境，允许 `pip install` 第三方包、读写临时文件、调用 `requests` 等标准库，适用于需要深度定制逻辑或集成私有 SDK 的场景 [原文标题](../../raw/application-user-guide/agent-development.md)。

## 关键参数

| 参数名 | 类型 | 说明 | 默认值 |
|--------|------|------|--------|
| `timeout_ms` | int | 单次执行最大耗时（毫秒），超时强制中断 | 30000 |
| `max_iterations` | int | 最大推理步数（仅 Managed/Flow Agent 有效） | 15 |
| `enable_tracing` | bool | 是否启用全链路追踪（含 LLM 输入/输出、工具调用日志） | `false` |
| `sandbox_runtime` | string | Sandbox Agent 的 Python 运行时版本 | `3.11` |

> **注意**：`max_iterations` 在 Sandbox Agent 中不生效，其迭代控制需由用户代码显式实现（如 `while` 循环 + `break` 条件），该行为与 [原文标题](../../raw/application-user-guide/agent-development/managed-agents.md) 中描述的“统一迭代上限”存在不一致，以实际运行时行为为准。

## 使用方式

1. **创建 Agent**：在控制台「应用开发」→「新建 Agent」中选择类型（Managed / Flow / Sandbox）；
2. **配置与调试**：填写基础参数，上传工具定义（OpenAPI Spec 或 JSON Schema），使用内置 Playground 实时测试输入输出；
3. **部署与调用**：发布后获取 HTTP Endpoint，按标准 REST 接口调用（`POST /v1/agents/{id}/invoke`），请求体需包含 `input` 字段（字符串或对象）。

## 限制和注意事项

- 所有 Agent 类型均禁止访问内网地址（`10.0.0.0/8`、`172.16.0.0/12`、`192.168.0.0/16`）、本地文件系统（Sandbox 除外）及执行系统命令（如 `os.system`）；
- Managed Agent 不支持动态加载未预注册的工具，若需新增工具，必须先在「工具中心」完成注册并重新发布 Agent；
- Flow Agent 的自定义 Python 节点受内存限制（2GB）和 CPU 时间片约束（单节点 ≤ 5s），超限将触发 `RuntimeError`；
- Sandbox Agent 的 `pip install` 仅支持 PyPI 公共包，不支持 `--find-links` 或私有 index，且安装包体积总和不得超过 100MB。

## 来源文档

- [Agent 开发运行](../../raw/application-user-guide/agent-development.md)


