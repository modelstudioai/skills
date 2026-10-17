# 函数调用

函数调用（Function Calling）是百炼平台中由大语言模型主动触发外部工具或服务执行特定任务的能力，其核心是模型根据用户意图，结构化地生成工具名称与参数，交由平台运行时解析、安全调用并注入结果回对话上下文，从而实现超越纯文本生成的闭环操作。

在百炼平台的不同场景中，这个概念如何使用：

- **Qwen API（模型直调）**：通过 `tools` 参数声明可用工具（如 `web_search`、`code_interpreter`、`file_search`），模型在推理过程中自动决定是否调用及调用哪个工具，并输出符合 OpenAI 或 Anthropic 兼容协议的 `tool_calls` 结构；平台自动执行调用、处理超时/错误，并将结果以 `tool_message` 形式注入后续上下文。适用于需要轻量级工具集成的单次请求场景。
  
- **Managed Agents**：不直接暴露函数调用接口，但通过注册 Skill（Webhook 类型）实现等效能力——Agent 在执行流程中按需触发 Skill，Skill 本质即远程函数调用；开发者需自行实现 Webhook 端点，平台负责身份校验、重试、超时（默认 30s）和结果注入。适用于有状态、多步骤、需环境隔离的生产级 Agent。

- **Flow Agent**：在可视化画布中添加「Tool Call」节点，配置工具 ID（对应已注册 Skill）及输入映射规则；模型输出被解析为结构化参数后传入，支持同步返回或异步轮询；节点可接条件分支与后续 LLM 节点，实现可控的工具编排逻辑。适合需调试工具链路、快速验证交互逻辑的场景。

- **Sandbox**：无内置函数调用机制，但开发者可在 `main.py` 中自由发起 HTTP 请求、调用 SDK 或本地函数；需手动解析模型输出（如 JSON 格式指令）、构造参数、处理异常并返回结构化响应。适用于私有协议、高定制化或需复杂状态管理的函数集成。

关键参数和配置：

- `tools`（Qwen API）：JSON 数组，每个元素为 `{ "type": "web_search" | "code_interpreter" | "file_search", "description": "...", "parameters": { ... } }`；参数 schema 需严格遵循 JSON Schema Draft-07，平台据此校验模型输出。
- `tool_choice`（Qwen API，可选）：控制调用策略，支持 `"auto"`（默认）、`"none"`（禁用）或 `{"type": "function", "function": {"name": "xxx"}}`（强制指定）。
- Skill 配置（Managed Agents / Flow Agent）：注册时需提供 `webhook_url`、`method`（仅 `POST`）、`timeout_ms`（1000–30000，默认 5000）、`retry_policy`（最多 2 次）；请求体为标准 JSON，含 `input` 字段（模型生成的参数）与 `session_id` 等上下文元数据。
- [Token](token.md) Plan 关联：所有函数调用产生的输入 token（工具描述 + 参数）与输出 token（工具返回内容）均计入绑定的 [Token](token.md) Plan 配额，流式调用亦按实际消耗计费。

面向开发者，简洁实用：

- ✅ 优先使用 Qwen API 的 `tools` 实现简单工具链；无需部署额外服务，开箱即用。
- ✅ 需多步协同、记忆共享或错误恢复？选 Managed Agent + Skill，专注业务逻辑而非基础设施。
- ✅ 要可视化调试或混合人工审核？用 Flow Agent 的 Tool Call 节点，拖拽即配。
- ✅ 私有协议、长连接、或需调用内部 gRPC/数据库？必须用 Sandbox，自己掌控全部调用生命周期。
- ⚠️ 所有函数调用均受 `timeout_ms` 限制（Qwen API 默认 30s，Managed Agents Skill 默认 5s），超时即失败，务必在端点侧做好幂等与快速响应。
- ⚠️ 模型生成的参数可能非法，务必在 Skill/Webhook/Sandbox 中做二次校验与白名单过滤，不可直接透传执行。

## 关联主题页

- [managed agents api](../api/managed-agents-api.md)
- [agent development](../guides/agent-development.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [token plan guide](../guides/token-plan-guide.md)


