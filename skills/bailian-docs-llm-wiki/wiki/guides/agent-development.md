# agent development

百炼平台提供多种 Agent 开发范式，支持从低代码编排到高自由度代码沙箱的全栈开发需求。开发者可根据任务复杂度、可控性要求和运维能力选择合适的 Agent 类型。所有类型均基于统一的执行引擎与可观测性基础设施。

## 支持的模型/功能

- **Managed Agent**：面向业务逻辑封装的托管式 Agent，支持多步骤工作流编排、内置工具调用（如知识库检索、HTTP 请求）、自动错误恢复；无需编写运行时代码，配置即生效。详见 [Agent 开发运行](../../raw/application-user-guide/agent-development.md)。
- **Flow Agent**：基于 LLM 应用构建的可视化流程 Agent，通过节点拖拽定义输入处理、LLM 调用、条件分支与输出转换；适用于快速原型验证与轻量级业务集成。其能力边界与配置方式在 [Agent 开发运行](../../raw/application-user-guide/agent-development.md) 中有明确说明。
- **Sandbox**：提供 Python 运行时沙箱环境，允许开发者完全自定义 Agent 行为（包括异步 I/O、第三方库调用、状态管理），但需自行处理超时、重试与安全隔离。详细约束见 [Agent 开发运行](../../raw/application-user-guide/agent-development.md)。

## 关键参数

| 参数名 | 类型 | 说明 | 默认值 |
|--------|------|------|--------|
| `timeout_ms` | integer | 单次执行最大耗时（毫秒） | `30000`（Managed/Flow）或 `60000`（Sandbox） |
| `max_iterations` | integer | 最大推理/循环步数 | `10`（Managed），`5`（Flow），`1`（Sandbox） |
| `enable_tracing` | boolean | 是否启用全链路追踪（影响性能） | `false` |

> **注意**：`max_iterations` 在 Sandbox 模式下固定为 `1`，不支持循环重试——这与早期文档中“Sandbox 支持迭代调用”的描述矛盾，以当前控制台实际行为及 [Agent 开发运行](../../raw/application-user-guide/agent-development.md) 的最新版本为准。

## 使用方式

1. 在控制台「应用」→「新建应用」中选择 Agent 类型；
2. 根据向导填写基础信息（名称、描述）、配置核心逻辑（工具绑定、流程图、或上传 sandbox.py）；
3. 本地调试建议使用 `qwen-agent-cli` 工具（参见 [Managed Agent](../../raw/application-user-guide/agent-development/managed-agents.md) 的调试章节）；
4. 部署后通过 `/v1/agents/{id}/invoke` 接口调用，请求体需包含 `input` 字段（string 或 object）。

## 限制和注意事项

- 所有 Agent 类型均不支持跨账号资源访问（如其他用户的知识库或 API Key）；
- Managed Agent 和 Flow Agent 的工具调用结果长度上限为 1MB；Sandbox 的 stdout/stderr 合计不超过 512KB；
- Sandbox 模式禁止执行系统命令（`os.system`, `subprocess.Popen` 等），且仅预装 `requests`, `numpy`, `pandas` 等基础库；
- 若需长期状态维护（如会话记忆），必须显式使用 `state` 参数传入/返回 JSON 序列化数据，平台不自动持久化中间状态。

## 来源文档

- [Agent 开发运行](../../raw/application-user-guide/agent-development.md)


