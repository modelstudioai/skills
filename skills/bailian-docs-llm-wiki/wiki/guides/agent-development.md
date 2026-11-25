# agent development

百炼平台提供多种 Agent 开发范式，支持从低代码编排到高自由度代码沙箱的全栈开发路径。开发者可根据任务复杂度、可控性需求和运维能力选择合适模式。所有 Agent 类型均统一接入百炼推理网关与可观测体系。

## 支持的模型/功能

- **Managed Agent**：基于预置模板与可视化配置构建的托管式 Agent，适用于标准客服、知识问答等场景，无需编写代码；详情见 [Agent 开发运行](../../raw/application-user-guide/agent-development.md)。  
- **Flow Agent**：通过拖拽节点（LLM 调用、条件分支、工具调用等）定义执行流，支持自定义 Prompt 与上下文管理；其能力边界与调试机制在 [Agent 开发运行](../../raw/application-user-guide/agent-development.md) 中有明确说明。  
- **Sandbox Agent**：提供 Python 运行时沙箱，允许开发者编写完整 `run()` 函数，直接调用百炼 SDK、外部 API 或本地逻辑，灵活性最高；相关约束详见 [Agent 开发运行](../../raw/application-user-guide/agent-development.md)。

## 关键参数

- `model_id`：必须指定，仅支持百炼平台已发布的 LLM 模型 ID（如 `qwen-max`、`qwen-plus`），不支持第三方模型别名。  
- `timeout`：最大执行时长，默认 30s，Sandbox Agent 可设为 60s，超过将强制终止。  
- `enable_tracing`：启用后可查看完整执行链路（含 LLM 输入/输出、工具调用耗时），对 Flow Agent 和 Sandbox Agent 均有效。

## 使用方式

1. 在控制台「应用开发」→「新建 Agent」中选择类型（Managed / Flow / Sandbox）；  
2. 完成配置后，点击「部署」获取唯一 `agent_id`；  
3. 通过 OpenAPI `/v1/agents/{agent_id}/chat` 发起调用，请求体需包含 `messages` 数组（格式同标准 Chat API）；  
4. Flow Agent 与 Sandbox Agent 支持传入 `session_id` 实现多轮状态保持（需自行维护 session 生命周期）。

## 限制和注意事项

- Managed Agent 不支持自定义工具集成，若需调用数据库或企业内部系统，必须切换至 Flow 或 Sandbox 模式。  
- Sandbox Agent 的 Python 环境禁止执行系统命令（`os.system`、`subprocess` 等）、文件写入及网络外连（仅允许通过 `requests` 调用白名单域名）；该限制在 [Agent 开发运行](../../raw/application-user-guide/agent-development.md) 中有明确定义。  
- > **注意**：原始文档中提及的「应用广场」为只读模板库，不可直接部署为可编辑 Agent；实际开发应基于 Flow 或 Sandbox 新建实例，避免误用过期模板——此点与早期文档描述存在偏差，以当前控制台行为为准。

## 来源文档

- [Agent 开发运行](../../raw/application-user-guide/agent-development.md)


