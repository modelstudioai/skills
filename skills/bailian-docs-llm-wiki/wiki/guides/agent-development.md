# agent development

百炼平台提供多种 Agent 开发范式，支持从低代码编排到高自由度沙箱开发的全链路能力。开发者可根据业务复杂度、可控性需求和运维成本，在 Managed Agent、Flow Agent 和 Sandbox 三种模式中选择合适路径。所有模式均基于百炼统一的推理与调度底座，共享模型调用、工具集成与可观测性能力。

## 支持的模型/功能

- **Managed Agent**：面向标准化场景（如客服问答、知识库检索），预置意图识别、多轮对话管理、RAG 增强等能力，无需编写逻辑代码；模型层默认使用 Qwen-Max 或 Qwen-Plus，支持在 [Managed Agent](../../raw/application-user-guide/agent-development/managed-agents.md) 文档中查看可选模型列表及切换方式。  
- **Flow Agent**：通过可视化节点流编排 LLM 调用、条件分支、工具调用（如数据库查询、API 调用）和状态传递，适用于中等复杂度业务逻辑；其底层执行引擎与 [Flow Agent](../../raw/application-user-guide/agent-development/llm-application.md) 所述一致，支持自定义 Prompt 模板与上下文长度配置。  
- **Sandbox**：提供 Python 运行时环境，允许开发者完全自主实现 Agent 行为（如自定义记忆模块、异步工具聚合、外部服务编排），适用于算法实验或深度定制场景；详细接口规范见 [Sandbox](../../raw/application-user-guide/agent-development/sandbox.md)。

## 关键参数

| 参数 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `model` | string | 指定主推理模型 ID（如 `qwen-max`, `qwen-plus`） | `qwen-max` |
| `temperature` | float | 控制输出随机性 | `0.5` |
| `max_iterations` | int | Flow Agent/Sandbox 中最大循环/重试次数 | `15` |
| `enable_tracing` | bool | 是否启用全链路追踪（含 LLM 输入/输出、工具调用日志） | `false` |

> **注意**：`max_iterations` 在 Managed Agent 中不可配置，其内部迭代由平台策略控制；该限制与 [Managed Agent](../../raw/application-user-guide/agent-development/managed-agents.md) 文档描述一致，但与旧版文档中“可设为 30”的说法冲突，请以当前文档为准。

## 使用方式

1. 在控制台「应用开发」→「新建 Agent」中选择模式（Managed / Flow / Sandbox）；  
2. 配置基础参数（名称、描述、模型等），按向导完成初始化；  
3. 对于 Flow Agent，拖拽节点并连接逻辑流；对于 Sandbox，上传 `main.py` 入口文件及依赖 `requirements.txt`；  
4. 点击「调试」启动本地模拟运行，或「发布」生成 API Endpoint。调试过程需参考 [Sandbox](../../raw/application-user-guide/agent-development/sandbox.md) 中的本地运行协议。

## 限制和注意事项

- Managed Agent 不支持自定义 Python 逻辑或外部 HTTP 工具调用；  
- Flow Agent 单次请求总 Token 上限为 32k（输入+输出），超限将触发截断并返回错误；  
- Sandbox 模式下，单次执行时长上限为 60 秒，内存限制为 2GB，且不支持持久化存储（如写入本地文件）；  
- 所有 Agent 模式均不支持跨账号共享运行时上下文，会话隔离由 `session_id` 强制保证；  
- 若在 Flow Agent 中嵌入非百炼托管的第三方 LLM API，其调用延迟与稳定性不在平台 SLA 保障范围内。

## 来源文档

- [Agent 开发运行](../../raw/application-user-guide/agent-development.md)


