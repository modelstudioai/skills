# agent development

百炼平台提供多种 Agent 开发范式，支持从低代码编排到高自由度代码沙箱的全栈开发流程。开发者可根据任务复杂度、可控性需求和运维能力选择合适模式。所有 Agent 均基于统一运行时调度，共享平台级可观测性与生命周期管理能力。

## 支持的模型与功能

- **Managed Agent**：面向业务逻辑封装的托管式 Agent，内置工具调用、记忆管理、多轮对话状态跟踪能力，适合快速交付标准场景（如客服问答、工单分派）；详情见 [Agent 开发运行](../../raw/application-user-guide/agent-development.md)。  
- **Flow Agent**：基于可视化流程图的 LLM 应用编排，支持条件分支、并行调用、自定义函数节点，适用于需要灵活控制执行路径的中等复杂度任务；其设计规范详见 [Agent 开发运行](../../raw/application-user-guide/agent-development.md)。  
- **Sandbox**：提供 Python 运行时沙箱，允许直接编写 `run()` 函数，完全掌控输入/输出、外部依赖（需白名单）、异步 I/O 与错误处理，适用于算法密集型或需集成私有 SDK 的场景；参考 [Agent 开发运行](../../raw/application-user-guide/agent-development.md) 中的沙箱说明。

## 关键参数

- `timeout`: 最大执行时长（秒），Managed Agent 默认 30s，Flow Agent 默认 60s，Sandbox 默认 120s；超时将强制终止并返回 `ExecutionTimeoutError`。  
- `max_iterations`: Flow Agent 与 Sandbox 中用于防止循环调用的迭代上限，默认为 50，不可设为 0 或负值。  
- `enable_tracing`: 布尔值，启用后记录完整执行链路（含 LLM 调用、工具输入/输出、异常堆栈），仅 Sandbox 支持细粒度 trace 控制。

## 使用方式

1. 在控制台「Agent 开发」页新建项目，选择类型（Managed / Flow / Sandbox）；  
2. 按向导填写基础配置（名称、描述、默认模型），其中 Sandbox 需额外声明 `requirements.txt`；  
3. 编写核心逻辑：Managed Agent 通过表单配置工具与提示词；Flow Agent 拖拽节点并配置参数；Sandbox 直接编辑 `main.py` 中的 `run(input: dict) -> dict` 函数；  
4. 本地调试（推荐使用 CLI 工具 `bailian-cli agent test --type=sandbox --file=main.py`）；  
5. 发布后获取 endpoint，按标准 REST API 调用（POST `/v1/agents/{id}/invoke`，Body 为 JSON 格式 input）。

## 限制和注意事项

- Managed Agent 不支持自定义 Python 代码或动态加载外部模块；若需该能力，必须切换至 Sandbox 模式。  
- Flow Agent 的「自定义函数节点」底层仍受限于 Managed Agent 运行时，无法突破其内存（2GB）与网络策略（仅允许访问百炼内置工具及白名单域名）；> **注意**：此限制与 [Managed Agent](../../raw/application-user-guide/agent-development/managed-agents.md) 文档中“支持任意 HTTP 请求”的旧描述存在冲突，以当前平台实际行为为准（2024Q3 版本已收紧网络策略）。  
- Sandbox 的 `pip install` 仅在构建阶段生效，运行时不可修改依赖；且不支持 `torch`、`tensorflow` 等 GPU 加速库（CPU-only 环境）。  
- 所有 Agent 类型均不支持跨账号共享 secret 或访问其他用户的工作空间资源，权限隔离严格遵循百炼 IAM 模型。

## 来源文档

- [Agent 开发运行](../../raw/application-user-guide/agent-development.md)


