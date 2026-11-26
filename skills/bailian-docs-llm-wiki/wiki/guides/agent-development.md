# agent development

百炼平台提供多种 Agent 开发范式，支持从低代码编排到高自由度代码沙箱的全栈开发路径。开发者可根据任务复杂度、可控性需求和运维能力选择合适模式。所有 Agent 类型均统一接入百炼推理网关与可观测性体系。

## 支持的模型/功能

- **Managed Agent**：基于预置模板与可视化配置构建的托管式 Agent，适合标准客服、知识问答等场景，无需编写逻辑代码；详见 [Agent 开发运行](../../raw/application-user-guide/agent-development.md)。  
- **Flow Agent**：通过 LLM Application（即 Flow 编排）定义多步骤调用链，支持条件分支、工具调用、状态传递；其能力边界与 [Agent 开发运行](../../raw/application-user-guide/agent-development.md) 中描述的 LLM Application 一致。  
- **Sandbox Agent**：提供 Python 运行时沙箱，允许用户提交自定义 `main.py` 及依赖文件，完全掌控执行逻辑与外部服务集成；该模式能力详见 [Agent 开发运行](../../raw/application-user-guide/agent-development.md)。

## 关键参数

- `model_id`：仅 Flow Agent 和 Sandbox Agent 需显式指定后端模型（如 `qwen-max`），Managed Agent 由平台自动绑定最优模型，不可覆盖。  
- `timeout_ms`：默认 30000（30 秒），Sandbox Agent 建议不超过 60000，超时将强制终止进程并返回 `504 Gateway Timeout`。  
- `enable_tracing`：布尔值，启用后在百炼控制台可观测完整执行链路（含 LLM 调用、工具响应、沙箱 stdout），对调试至关重要。

## 使用方式

1. 在控制台「应用开发」→「新建应用」中选择 Agent 类型；  
2. 根据所选类型填写必要配置（如 Flow Agent 的节点图、Sandbox Agent 的代码包 ZIP）；  
3. 调用时通过 `/v1/agents/{agent_id}/invoke` 接口发送 JSON 请求体，需包含 `input` 字段（字符串或对象）；  
4. 响应结构统一为 `{ "output": ..., "status": "success" | "failed", "trace_id": "..." }`。

## 限制和注意事项

- Managed Agent 不支持自定义模型或代码注入，其行为完全由平台配置驱动；若需模型微调或私有工具集成，必须选用 Flow 或 Sandbox 模式。  
- Sandbox Agent 的 ZIP 包大小上限为 50 MB，且禁止访问 `/proc`、`/sys` 等系统路径，网络请求仅允许白名单域名（默认含 `api.bailian.com`、`alipay.com` 等）。  
> **注意**：原始文档中 [Agent 开发运行](../../raw/application-user-guide/agent-development.md) 将“应用广场”列为一种 Agent 类型，但实际其仅为预置应用分发渠道，不构成独立开发模式——此为表述歧义，开发者不应将其与 Managed/Flow/Sandbox 并列理解。

## 来源文档

- [Agent 开发运行](../../raw/application-user-guide/agent-development.md)


