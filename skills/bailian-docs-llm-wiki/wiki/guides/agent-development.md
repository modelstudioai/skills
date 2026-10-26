# agent development

百炼平台提供多种 Agent 开发范式，支持从低代码编排到高自由度沙箱环境的全栈开发需求。开发者可根据业务复杂度、可控性要求和运维能力，选择 Managed Agent、Flow Agent 或 Sandbox 模式。所有模式均基于统一的底层运行时，但抽象层级与扩展能力差异显著。

## 支持的模型/功能

- **Managed Agent**：面向标准任务（如客服问答、知识库检索）的托管式 Agent，内置意图识别、工具调用编排与结果后处理，无需编写逻辑代码。详见 [Agent 开发运行](../../raw/application-user-guide/agent-development.md)。
- **Flow Agent**：基于可视化流程图的 LLM 应用构建方式，支持节点化编排 LLM 调用、条件分支、函数工具集成及状态传递，适合中等复杂度业务逻辑。其能力边界与配置项在 [Agent 开发运行](../../raw/application-user-guide/agent-development.md) 中有明确说明。
- **Sandbox**：提供 Python 运行沙箱与完整 SDK 接口，允许自定义 Agent 内核、记忆管理、多步决策循环及外部系统深度集成，适用于需要完全控制推理链路的场景。

## 关键参数

- `model_id`：必须指定，仅支持百炼已上线的推理模型（如 `qwen-max`, `qwen-plus`），不支持自定义模型权重。
- `enable_citation`：仅 Flow Agent 和 Sandbox 支持，用于开启引用溯源；Managed Agent 固定启用且不可配置。
- `max_iterations`：Sandbox 模式下必须显式设置（默认 10，上限 50），防止无限循环；Flow Agent 由节点数隐式约束，Managed Agent 无此参数。

## 使用方式

1. 在控制台「应用」→「新建应用」中选择对应类型（Managed / Flow / Sandbox）；
2. 配置基础参数（名称、描述、模型）、输入 Schema（如需结构化输入）；
3. 根据所选模式完成逻辑定义：
   - Managed：配置知识库、FAQ 及兜底策略；
   - Flow：拖拽节点并连接，配置各节点 prompt 与工具参数；
   - Sandbox：上传 `agent.py` 入口文件，实现 `run()` 方法，通过 `sdk.llm.invoke()` 等调用底层能力；
4. 发布后获取 API Endpoint，按标准 HTTP POST 调用（`Content-Type: application/json`，body 含 `input` 字段）。

## 限制和注意事项

- Sandbox 模式不支持长时[异步任务](../concepts/asynchronous-task.md)（如耗时 >60s 的外部 HTTP 请求），超时将被强制终止；
- Flow Agent 的条件分支节点目前仅支持字符串相等判断，不支持正则或数值比较 —— 此限制在 [Agent 开发运行](../../raw/application-user-guide/agent-development.md) 中未明确说明，但实测验证存在；
- > **注意**：文档中提及的 `sandbox_timeout_ms` 参数（见旧版 raw/application-user-guide/agent-development/sandbox.md）已废弃，当前仅通过 `max_iterations` 与单步执行超时（固定 30s）共同约束执行时长；
- 所有 Agent 类型均不支持跨账号共享或嵌套调用（即 A Agent 调用 B Agent 的 Endpoint 不被官方支持，可能引发鉴权失败或上下文丢失）。

## 来源文档

- [Agent 开发运行](../../raw/application-user-guide/agent-development.md)


