# 函数调用

函数调用（Function Calling）是百炼平台中模型主动识别用户意图、结构化提取参数，并按约定协议触发外部能力（如[插件](plugin.md)、API、自定义工具）的核心机制。它使大模型从“纯文本生成器”升级为可执行动作的智能代理，是构建 Agent、工作流和高代码应用的关键支撑能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）应用**：模型在 `Agent 2.0` 模式下自动规划并调用注册的函数（如搜索、计算、图像生成），全过程可追溯；函数结果被自动注入上下文，支持多轮迭代与反思。旧版 Agent 1.0 则需显式配置“工具调用阶段”，分步完成检索与决策。

- **工作流（Workflow）应用**：通过“工具节点”接入函数调用能力，支持 MCP 协议、OpenAPI 规范或百炼兼容的 Function Calling Schema。开发者可将函数作为确定性流程中的一个执行单元，与其他节点（如条件判断、循环）组合编排。

- **高代码应用**：在 Python 代码中通过 `fastmcp.Client` 显式发起函数调用，或接收模型返回的 `tool_calls` 结构并手动 dispatch；控制台仅用于工具元信息注册与环境变量配置，实际调用逻辑由开发者完全掌控。

- **Assistant API 直接调用**：开发者可向 `/v1/assistants/runs` 等端点提交含 `tools` 数组的请求，模型将根据输入自动选择函数、填充参数并返回 `tool_calls` 字段（含 `id`、`function.name`、`function.arguments`），开发者需自行解析并执行对应逻辑。

> ⚠️ 注意：所有函数调用均**不透传自定义 Header**，仅允许 `Authorization` 字段；函数 endpoint 必须可公网访问，且响应需符合 JSON Schema 格式（推荐使用 OpenAPI 3.0 定义）。

## 关键参数和配置

| 参数 | 类型 | 说明 | 是否必需 |
|------|------|------|----------|
| `tools` | array | 注册的函数列表，每个元素为 `{ "type": "function", "function": { "name", "description", "parameters" } }`，`parameters` 需为 JSON Schema Object | 是（启用函数调用时） |
| `tool_choice` | string / object | 控制调用策略：`"auto"`（默认，模型自主决定）、`"none"`（禁用）、`{"type": "function", "function": {"name": "xxx"}}`（强制指定） | 否 |
| `function_call`（已弃用） | string / object | 旧版参数，等效于 `tool_choice`，新应用请统一使用 `tool_choice` | 否（不推荐） |
| `arguments`（响应字段） | string | 模型生成的 JSON 字符串（非对象），需 `json.loads()` 解析后校验结构 | —— |
| `tool_calls`（响应字段） | array | 包含一个或多个调用请求，每个含 `id`、`function.name`、`function.arguments`；支持并发调用多个函数 | —— |

- **Schema 要求**：`parameters` 必须是有效的 JSON Schema Object（非字符串），推荐使用 `required` 字段明确必填项，避免模型传入空值。
- **错误处理**：若函数执行失败或返回格式错误，需在后续请求中通过 `tool_outputs` 提交错误信息，模型将据此重试或调整策略。

## 面向开发者，简洁实用

- ✅ **快速验证**：在控制台“智能体调试”或 Postman 中发送含 `tools` 的请求，观察响应是否含 `tool_calls`；若无，检查 `parameters` 是否为合法 Schema Object 或尝试设 `tool_choice="auto"`。
- ✅ **安全实践**：函数 endpoint 应校验 `Authorization` 头（如 Bearer [Token](token.md)），禁止依赖其他 Header 或未签名参数；敏感操作建议增加二次确认逻辑。
- ✅ **调试技巧**：开启 `stream=True` 可实时捕获 `tool_calls` 流式事件；结合 `enable_thinking=True` 查看模型内部规划过程。
- ❌ **避坑提示**：  
  - 不要将函数名设为保留字（如 `list`, `get`, `run`），易与平台内部方法冲突；  
  - `function.arguments` 是字符串，不是 JSON 对象——解析前务必 `json.loads()`；  
  - 自定义函数不支持 WebSocket、长连接或异步回调，必须同步返回 HTTP 2xx 响应。

函数调用不是黑盒能力，而是你与模型协作的契约接口：定义清晰，调用可靠，反馈及时。从第一个 `tool_calls` 出现开始，你的应用就真正“活”起来了。

## 关联主题页

- [more about models](../api/more-about-models.md)
- [application support](../guides/application-support.md)
- [llm application](../guides/llm-application.md)


