# agent development

百炼平台提供多种 Agent 开发范式，支持从低代码编排到全代码自定义的完整链路。开发者可根据业务复杂度和控制粒度需求，选择 Managed Agent、Flow Agent 或 Sandbox 模式进行构建与部署。所有模式均基于百炼统一的运行时与调度框架，确保一致的可观测性与扩展能力。

## 支持的模型与功能

- **Managed Agent**：面向业务逻辑封装，支持通过自然语言配置工具调用、记忆管理、多轮对话状态维护；底层自动适配 Qwen 系列大模型（如 qwen-plus、qwen-max），无需手动指定推理参数。详见 [Agent 开发运行](../../raw/application-user-guide/agent-development.md)。
- **Flow Agent**：基于可视化流程图构建 LLM 应用，支持条件分支、并行调用、自定义函数节点及外部 API 集成；适用于需要精细编排但不希望写代码的场景。其能力边界与配置项在 [Flow Agent 文档](../../raw/application-user-guide/llm-application.md) 中明确定义。
- **Sandbox**：提供 Python 运行沙箱环境，允许开发者完全自主编写 `run()` 函数，直接调用百炼 SDK（如 `dashscope.Generation.call`）、访问上下文变量、实现异步工具调用等高级能力。详细约束见 [Sandbox](../../raw/application-user-guide/agent-development/sandbox.md)。

## 关键参数

- `model`: 仅 Flow Agent 和 Sandbox 显式支持；Managed Agent 由平台自动选型，**不可覆盖**。若在 Flow Agent 中指定非百炼托管模型（如第三方 API 地址），将导致部署失败。
- `max_iterations`: 默认为 10，控制 Agent 最大自主思考步数；Sandbox 模式下该参数无效，需在代码中自行实现终止逻辑。
- `enable_memory`: 仅 Managed Agent 和 Flow Agent 支持；设为 `true` 时启用会话级[长期记忆](../concepts/long-term-memory.md)（基于向量库），默认关闭。
- > **注意**：原始文档 [Agent 开发运行](../../raw/application-user-guide/agent-development.md) 中列出的“应用广场”链接指向低代码模板市场，但该页面当前已下线，实际模板需通过控制台「新建应用 → 从模板开始」入口访问，相关说明以控制台 UI 为准。

## 使用方式

1. **Managed Agent**：在控制台选择「Agent 应用」→「新建 Managed Agent」，填写描述、配置工具集后保存即部署，无需编码。
2. **Flow Agent**：进入「LLM 应用」→「新建 Flow」，拖拽节点构建流程，双击节点配置模型、提示词或函数参数，最后发布。
3. **Sandbox**：选择「Agent 应用」→「新建 Sandbox Agent」，在编辑器中编写符合签名 `def run(inputs: dict) -> dict:` 的 Python 函数，支持导入 `dashscope`, `json`, `requests` 等白名单库。

## 限制和注意事项

- Sandbox 模式单次执行超时为 60 秒，内存上限 2GB；禁止 fork 进程、读写文件系统、监听端口或执行 shell 命令。
- 所有 Agent 类型均不支持跨账号共享会话 memory；会话 ID 必须由调用方显式传入（`session_id` 字段），否则视为新会话。
- > **注意**：[Sandbox](../../raw/application-user-guide/agent-development/sandbox.md) 文档中提及“支持 `async def run()`”，但当前运行时仅同步执行，异步函数将被静默降级为同步调用——此行为将在 v2.3 版本中修正，当前请始终使用同步 `def run()`。

## 来源文档

- [Agent 开发运行](../../raw/application-user-guide/agent-development.md)


