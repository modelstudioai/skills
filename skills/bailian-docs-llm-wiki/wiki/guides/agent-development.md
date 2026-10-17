# agent development

百炼平台提供多种 Agent 开发范式，支持从低代码编排到高自由度代码沙箱的全栈开发需求。开发者可根据任务复杂度、可控性要求和运维能力选择合适的 Agent 类型。所有类型均基于统一的执行引擎与可观测性基础设施。

## 支持的模型/功能

- **Managed Agent**：面向业务逻辑封装的托管式 Agent，支持多步骤工作流编排、内置工具调用（如知识库检索、HTTP 请求）、自动错误恢复；无需编写运行时代码，配置即生效。详见 [Agent 开发运行](../../raw/application-user-guide/agent-development.md)。
- **Flow Agent**：基于 LLM 应用构建的可视化流程 Agent，通过节点拖拽定义输入处理、LLM 调用、条件分支与输出格式化；适用于快速原型验证与轻量级自动化。其能力边界与配置项在 [Agent 开发运行](../../raw/application-user-guide/agent-development.md) 中有明确说明。
- **Sandbox**：提供 Python 运行时沙箱环境，允许开发者完全控制执行逻辑，支持自定义依赖安装、异步 I/O、外部服务集成及状态持久化；适合需要精细控制或集成私有 SDK 的场景。详细约束与生命周期管理见 [Agent 开发运行](../../raw/application-user-guide/agent-development.md)。

## 关键参数

- `timeout_ms`：全局超时，默认 30000（30 秒），Sandbox 可设为最高 60000，Flow Agent 不可超过 45000；
- `max_steps`：仅 Flow Agent 和 Managed Agent 有效，限制 LLM 决策步数，范围 1–20；
- `enable_tracing`：启用后返回完整执行链路（含 tool call 输入/输出、LLM prompt），默认关闭；
- Sandbox 额外支持 `requirements.txt` 指定依赖，但禁止使用 `os.system`、`subprocess` 等系统调用。

## 使用方式

1. 在控制台「应用」→「新建应用」中选择对应 Agent 类型；
2. Managed Agent：填写描述、配置工具集、设置 fallback 行为；
3. Flow Agent：在画布中连接 Input → LLM Node → Condition → Output 节点，双击节点编辑参数；
4. Sandbox：上传 `main.py` 入口文件及可选 `requirements.txt`，确保 `main()` 函数接收 `input: dict` 并返回 `dict`；
5. 所有类型均支持通过 `/v1/chat/completions` API 调用，需在请求头携带 `x-bailian-agent-id`。

## 限制和注意事项

- Managed Agent 和 Flow Agent 均不支持长时后台任务（如轮询、WebSocket）；如需此类能力，必须使用 Sandbox 并自行实现重试与心跳。
- Sandbox 的冷启动延迟较高（平均 2–5 秒），不适合对首字节延迟敏感的实时交互场景。
- > **注意**：原始文档中 [Managed Agent](raw/application-user-guide/agent-development/managed-agents.md) 提到“支持自定义 Python 工具”，但该能力已在 v2.3 版本中移除，当前仅可通过 Flow Agent 或 Sandbox 实现同等效果；请以 [Agent 开发运行](../../raw/application-user-guide/agent-development.md) 的最新描述为准。

## 来源文档

- [Agent 开发运行](../../raw/application-user-guide/agent-development.md)


