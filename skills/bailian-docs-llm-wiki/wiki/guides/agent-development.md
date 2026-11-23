# agent development

百炼平台提供多种 Agent 开发范式，支持从低代码编排到高自由度沙箱开发的全链路能力。开发者可根据业务复杂度、可控性需求和运维成本，在 Managed Agent、Flow Agent 和 Sandbox 三种模式中选择合适路径。所有模式均基于百炼统一的推理与调度底座，共享模型调用、工具集成与会话管理能力。

## 支持的模型与功能

- **Managed Agent**：面向标准化场景（如客服问答、知识库检索），预置意图识别、多轮对话状态管理、RAG 增强等能力，无需编写逻辑代码；底层默认使用 Qwen-Max 或 Qwen-Plus，支持通过参数切换 [原文标题](../../raw/application-user-guide/agent-development.md)。
- **Flow Agent**：基于可视化流程图构建 LLM 应用，支持节点化编排 LLM 调用、条件分支、工具调用（如 HTTP 请求、数据库查询）、变量传递；可接入自定义函数，适用于中等复杂度业务逻辑 [原文标题](../../raw/application-user-guide/agent-development.md)。
- **Sandbox**：提供 Python 运行时环境与 SDK（`bailian-sdk`），允许完全自主实现 `Agent.run()` 接口，支持异步流式响应、自定义记忆模块、外部服务深度集成；需自行处理 token 限长、错误重试与超时控制 [原文标题](../../raw/application-user-guide/agent-development.md)。

## 关键参数

| 参数名 | 类型 | 说明 | 默认值 |
|--------|------|------|--------|
| `model_id` | string | 指定基础大模型 ID（如 `qwen-max`, `qwen-plus`） | `qwen-max` |
| `max_iterations` | int | Flow Agent 或 Sandbox 中最大循环/递归调用次数 | `10` |
| `enable_rag` | bool | 是否启用 RAG 检索（仅 Managed/Flow Agent 生效） | `false` |
| `stream` | bool | 是否开启流式响应（Sandbox 必须显式设置） | `false` |

> **注意**：`max_iterations` 在 Managed Agent 中实际受后台策略硬限制为 `5`，与文档中声明的 `10` 不一致，请以运行时实际报错为准（参见 [原文标题](../../raw/application-user-guide/agent-development/managed-agents.md)）。

## 使用方式

1. **创建 Agent**：在控制台「应用开发」→「新建 Agent」中选择模式（Managed / Flow / Sandbox）；
2. **配置核心组件**：
   - Managed：绑定知识库、设置欢迎语、配置兜底回复；
   - Flow：拖拽节点、连接边、在 LLM 节点中填写 `system_prompt` 与 `user_prompt` 模板；
   - Sandbox：上传 `agent.py`，确保包含 `class MyAgent(Agent)` 及 `def run(self, messages: List[Dict]) -> Iterator[str]` 方法；
3. **调试与部署**：使用内置 Chat UI 测试，通过 API Key 调用 `/v1/agents/{agent_id}/chat` 接口；生产环境建议配置独立 endpoint 并启用鉴权。

## 限制和注意事项

- 所有 Agent 的单次请求 `messages` 总长度（含历史）不得超过 32768 tokens，超长将被截断且不告警；
- Flow Agent 中 HTTP 工具节点不支持重定向跳转与客户端证书认证；
- Sandbox 模式下禁止执行系统命令（如 `os.system`, `subprocess.Popen`）、写入本地文件或监听端口，违反将触发沙箱终止；
- Managed Agent 不支持自定义 tool call 解析逻辑，若需精细控制 function calling 行为，必须降级至 Flow 或 Sandbox 模式。

## 来源文档

- [Agent 开发运行](../../raw/application-user-guide/agent-development.md)


