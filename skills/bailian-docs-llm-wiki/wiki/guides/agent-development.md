# agent development

百炼平台提供多种 Agent 开发范式，支持从低代码编排到高自由度代码沙箱的全链路开发。开发者可根据任务复杂度、可控性要求和运维能力选择合适模式，所有 Agent 均统一接入百炼推理网关与可观测体系。核心能力围绕模型调用、工具集成、状态管理与执行控制展开。

## 支持的模型与功能

- **Managed Agent**：基于预置模板与可视化配置构建，内置对 Qwen 系列（如 `qwen-max`、`qwen-plus`）及部分第三方模型（如 `llama-3-70b`）的支持，自动处理工具调用、记忆管理和错误重试逻辑。详见 [Agent 开发运行](../../raw/application-user-guide/agent-development.md)。
- **Flow Agent**：通过节点化流程图定义 LLM 与工具/条件分支的编排逻辑，支持 HTTP 请求、数据库查询、Python 脚本等标准组件，适用于结构化业务流程。其设计规范与节点能力在 [Flow Agent](../../raw/application-user-guide/llm-application.md) 中详细说明。
- **Sandbox Agent**：提供隔离 Python 执行环境，允许编写任意逻辑（含自定义工具、异步 I/O、外部 SDK 调用），模型仅作为“智能中枢”参与决策，其余完全由开发者控制。沙箱安全边界与资源限制见 [Sandbox](../../raw/application-user-guide/agent-development/sandbox.md)。

## 关键参数

- `model_id`：必需，指定底层大模型 ID（如 `qwen-max`），需与所选 Agent 类型兼容；
- `tools`：数组，声明可用工具列表（格式为 `{ "name": "...", "description": "...", "parameters": {...} }`），仅 Managed 和 Flow Agent 支持自动注入；
- `max_iterations`：默认 15，控制 Agent 最大自主调用循环次数，Sandbox Agent 不受此限；
- `enable_memory`：布尔值，启用会话级上下文缓存（Managed/Flow 默认开启，Sandbox 需手动实现）；
- `timeout_ms`：全局超时，默认 30000 ms，Sandbox 中单次 `exec()` 调用另有独立超时（见 [Sandbox](../../raw/application-user-guide/agent-development/sandbox.md)）。

## 使用方式

1. 在控制台「应用」→「新建应用」中选择对应 Agent 类型（Managed / Flow / Sandbox）；
2. 配置基础参数（`model_id`、`tools` 等）并保存；
3. 通过 `/v1/agents/{agent_id}/chat` 接口发起调用，请求体需包含 `input` 字符串及可选 `session_id`；
4. 流式响应遵循 Server-Sent Events (SSE) 协议，每帧含 `event: message` 或 `event: tool_call`；非流式则返回完整 JSON 响应体。

> **注意**：Flow Agent 的 `/v1/agents/{id}/chat` 接口在 v2.3.0 后已废弃，必须使用 `/v1/flows/{flow_id}/run` 替代——该变更未在 [Flow Agent](../../raw/application-user-guide/llm-application.md) 中同步更新，请以 OpenAPI 文档为准。

## 限制和注意事项

- Managed Agent 不支持自定义模型加载或 CUDA 内核级优化，仅限平台白名单模型；
- Flow Agent 节点间最大数据传输量为 2MB，超限将触发 `DATA_SIZE_EXCEEDED` 错误；
- Sandbox Agent 的 `exec()` 函数禁止执行系统命令（如 `os.system`）、读写宿主文件系统、创建子进程或监听网络端口；
- 所有 Agent 类型均不支持跨 session 共享内存或持久化状态，[长期记忆](../concepts/long-term-memory.md)需对接外部向量库或数据库；
- 当前版本中，Managed Agent 的 `tools` 参数若包含未注册工具名，将静默忽略而非报错——该行为与 [Agent 开发运行](../../raw/application-user-guide/agent-development.md) 中“严格校验工具合法性”的描述存在矛盾，实际以运行时行为为准。

## 来源文档

- [Agent 开发运行](../../raw/application-user-guide/agent-development.md)


