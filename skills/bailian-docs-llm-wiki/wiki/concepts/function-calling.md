# 函数调用

函数调用（Function Calling）是百炼平台中模型主动识别用户意图、生成结构化工具调用请求，并与外部系统（如数据库、API、数据连接等）协同完成复杂任务的核心能力。它使大模型不仅能生成文本，还能安全、可控地执行真实世界操作，是构建智能体（Agent）、自动化工作流和增强型应用的关键机制。

## 在百炼平台的不同场景中，这个概念如何使用

- **基础 API 调用**：在 `/v1/chat/completions` 等标准推理接口中，通过传入 `tools` 参数声明可用函数，模型返回 `tool_calls` 字段，开发者需解析并同步执行对应逻辑，再将结果以 `role: "tool"` 消息回传，实现多轮交互。
- **插件（Plug-in）场景**：仅 `qwen-max`、`qwen-plus` 和新版 `qwen-turbo` 支持；插件本质是预注册的标准化函数，其 schema 需严格遵循 OpenAPI 3.0.3 子集，调用流程与通用函数调用一致，但 endpoint 必须 HTTPS 且域名需在控制台白名单备案。
- **Skill 技能编排**：Skill 可内嵌函数调用节点，作为多 step 流程中的一个执行单元，与其他 RAG 检索、HTTP 请求等节点组合使用，实现端到端业务逻辑封装。
- **数据连接（Data Connection）集成**：在函数定义的 `parameters.schema` 中可直接引用已配置的 `connection_id`，模型自动将自然语言请求（如“查上月销售额”）转化为带参数的 SQL 或数据源查询，凭证全程不透出。
- **计费与资源管理**：函数调用产生的 token 消耗（含输入 messages、tools 定义、tool_calls 输出及 tool response）可全额使用 [Token](token.md) Plan 抵扣，但不支持私有化部署或自定义微调模型的专属 endpoint。

## 关键参数和配置

- `tools`: 必填，JSON Schema 数组，每个元素必须包含：
  - `type`: 固定为 `"function"`
  - `function.name`: 字符串，唯一标识函数名（仅字母、数字、下划线，长度 ≤64）
  - `function.description`: 简明功能说明（≤512 字符），影响模型调用决策
  - `function.parameters`: OpenAPI 兼容的 JSON Schema（不支持 `nullable`、`oneOf`、`anyOf` 等联合类型）
- `tool_choice`: 控制调用策略，可选值：
  - `"auto"`（默认）：由模型自主判断是否及调用哪个函数
  - `"none"`：强制禁用函数调用，模型仅作文本回复
  - `{ "type": "function", "function": { "name": "xxx" } }`：指定唯一可调用函数
- `enable_thinking`: 非必填布尔值，启用后模型可能在 `thinking` 字段中输出调用理由（不计费，但输出不可靠，**严禁用于业务逻辑判断**）

> ⚠️ 注意：单次请求最多声明 20 个 `tools`，单次响应最多触发 5 次 `tool_calls`；所有函数调用超时固定为 10 秒，超时后返回 `{"error": "tool_timeout"}`，平台不重试，需客户端自行实现重试逻辑。

## 面向开发者，简洁实用

- ✅ **推荐实践**：始终显式指定 `tool_choice`（避免意外跳过调用）；为每个 `function.parameters` 提供最小必要字段，并标注 `required`；使用 `X-DashScope-Token-Plan-ID` 头或 SDK 的 `token_plan_id` 参数确保计费走 [Token](token.md) Plan。
- ❌ **避坑提示**：不要依赖 `thinking` 字段做业务分支；不要在 `tools` 中使用复杂 schema；自定义函数 endpoint 必须支持 HTTPS 且域名已备案；`tool_calls` 返回后，必须构造符合格式的 `role: "tool"` 消息并完整拼入后续请求的 `messages`，否则模型无法继续推理。
- 🔧 **调试建议**：开启 `enable_tracing`（Skill 场景）或使用控制台调试器，查看每轮 `tool_calls` 的原始输出、实际调用参数与耗时；[Token](token.md) Plan 余额可通过 `/v1/plan/balance` 实时查询。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [data connection overview](../guides/data-connection-overview.md)
- [skill](../guides/skill.md)
- [plug in](../guides/plug-in.md)
- [application support](../guides/application-support.md)


