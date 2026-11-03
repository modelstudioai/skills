# agent development

百炼平台提供多种 Agent 开发范式，支持从低代码编排到全代码自定义的渐进式开发路径。开发者可根据业务复杂度、可控性需求和团队技术栈，选择 Managed Agent、Flow Agent 或 Sandbox 模式。所有模式均基于统一的运行时调度与可观测能力，但底层执行机制与配置粒度存在显著差异。

## 支持的模型/功能

- **Managed Agent**：平台托管的轻量级 Agent，内置意图识别、工具调用编排与错误恢复逻辑，适用于标准客服、FAQ 问答等场景；仅支持 `qwen-max`、`qwen-plus` 等指定模型，不支持自定义 LLM 或工具链 [Agent 开发运行](../../raw/application-user-guide/agent-development.md)。  
- **Flow Agent**：基于可视化流程图的 LLM 应用构建方式，支持多节点条件分支、变量传递与外部 API 集成；其核心能力在 [Flow Agent](../../raw/application-user-guide/llm-application.md) 中定义，但注意该文档未明确说明是否支持异步工具调用（最新 SDK 已支持，而文档未更新）。  
- **Sandbox**：完全开放的 Python 运行环境，允许开发者编写任意逻辑（包括自定义 Agent 框架、状态管理、长周期任务），需自行实现 `run()` 接口并遵守资源约束；详细规范见 [Sandbox](../../raw/application-user-guide/agent-development/sandbox.md)。

## 关键参数

- `model_id`：仅 Managed Agent 和 Flow Agent 需显式指定；Sandbox 中由用户代码控制模型调用，平台不透出该参数。  
- `tools`：Managed Agent 仅支持平台预注册的工具集（如 `web_search`, `calculator`）；Flow Agent 允许绑定自定义 OpenAPI 工具；Sandbox 完全自主实现工具调用逻辑。  
- `timeout_ms`：全局超时，默认 30000 ms；Sandbox 中若未在 `run()` 内主动处理超时，将被强制终止 —— 此行为与 [Sandbox](../../raw/application-user-guide/agent-development/sandbox.md) 所述“支持无限期运行”存在矛盾。  
> **注意**：[Sandbox](../../raw/application-user-guide/agent-development/sandbox.md) 声称支持无限期运行，但实际运行时强制应用 300s 硬性超时限制，以保障集群稳定性，请务必在代码中实现心跳或分段执行。

## 使用方式

1. **Managed Agent**：通过控制台「创建 Agent」→ 选择「Managed」模板 → 配置 [prompt](prompt.md) + 选择工具 → 部署；无需写代码。  
2. **Flow Agent**：在 Flow 编辑器中拖拽节点，配置 LLM 节点的 `model_id` 和 `tools`，连接条件分支后发布；配置项最终序列化为 JSON Schema，详见 [Flow Agent](../../raw/application-user-guide/llm-application.md)。  
3. **Sandbox**：上传 `main.py`（含 `def run(inputs: dict) -> dict:`），通过 `/v1/agents/{id}/invoke` 调用；必须确保依赖包在 `requirements.txt` 中声明，且总包体积 ≤ 50MB。

## 限制和注意事项

- 所有 Agent 类型均不支持跨请求状态保持（如 session storage），状态需由调用方维护或存入外部存储。  
- Managed Agent 不支持流式响应（streaming），仅返回最终结果；Flow Agent 和 Sandbox 支持，但需在调用时显式设置 `stream=true`。  
- Sandbox 的 CPU/内存配额固定（2C/4G），不可调整；若需更高资源，请改用函数计算（FC）+ 百炼 API 组合方案。  
> **注意**：[Agent 开发运行](../../raw/application-user-guide/agent-development.md) 列出的三类链接未说明版本兼容性，实际开发中请确认所用控制台版本 ≥ v2.8.0，否则 Flow Agent 的 `parallel` 节点可能不可用。

## 来源文档

- [Agent 开发运行](../../raw/application-user-guide/agent-development.md)


