# 函数调用

函数调用（Function Calling）是百炼平台中大模型主动识别用户意图、自主选择并执行外部工具能力的核心机制。它通过结构化描述工具接口（名称、参数、语义），使模型能在推理过程中动态生成工具调用请求，而非仅输出文本，从而实现对实时信息、精确计算、多模态生成等模型原生能力之外任务的可靠闭环。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台中并非单一 API 特性，而是贯穿多个能力层级的统一交互范式，具体体现为：

- **Omni Realtime API（实时语音交互）**：模型在流式语音对话中可自主触发 `function` 类型工具（如查天气、订机票），调用结果需由客户端通过 `conversation.item.create` 回传，并显式发送 `response.create` 以驱动后续响应。适用于低延迟语音助手、智能座舱等强交互场景。

- **Application Component API（基础模型 API）**：通过 `tools` 数组声明工具集，配合 `tool_choice` 控制策略（`"auto"`/`"none"`/指定工具），模型在单次 `/v1/chat/completions` 请求中返回 `tool_calls`，开发者需解析 `function.name` 和 `function.arguments` 并同步执行，再将结果以 `role: "tool"` 消息形式拼入下一轮 `messages` 继续调用。

- **Application Call（智能体/工作流调用）**：插件（Plug-in）和 MCP 服务均以函数调用语义集成。智能体应用中，模型自动规划是否调用及调用哪个插件；工作流应用中，MCP 节点作为显式工具节点被编排执行。`biz_params.user_defined_params` 可透传插件所需业务参数。

- **Plug-in（插件系统）**：所有插件本质是封装后的函数——每个工具（Tool）对应一个标准化的 HTTP 接口，其 `tool_name`、`tool_description` 和 `in_params` 共同构成模型可理解的“函数签名”。模型依据自然语言描述匹配工具，生成符合 `in_params` 结构的 JSON 参数。

- **Model Context Protocol（MCP）**：MCP 是函数调用的协议层抽象。官方或自定义 MCP 服务提供符合 Streamable HTTP 规范的工具端点，百炼平台将其统一注册为可调用函数。模型无需感知底层是 REST 还是 SSE，仅按 `name` 和 `parameters` 发起调用，平台负责协议转换与安全代理。

> ✅ 关键共识：无论在哪一层，函数调用都遵循“声明 → 触发 → 执行 → 注入”四步闭环，且模型始终只负责 *决策* 和 *参数生成*，不执行实际逻辑。

## 关键参数和配置

| 参数 | 位置 | 类型 | 说明 |
|------|------|------|------|
| `tools` | Omni Realtime、Application Component、Application Call（DashScope）、Plug-in、MCP 配置页 | array | 工具定义列表，每项含 `name`（必填，英文标识符）、`description`（必填，自然语言功能说明）、`parameters`（JSON Schema 格式，含 `properties` 和 `required`） |
| `tool_choice` | Application Component API、Application Call（DashScope） | string / object | 控制调用策略：`"auto"`（默认，模型自主决定）、`"none"`（禁用）、`{"type": "function", "function": {"name": "xxx"}}`（强制指定） |
| `function.name` | 所有调用响应中 | string | 模型生成的工具名称，必须与 `tools` 中某项 `name` 完全一致（区分大小写） |
| `function.arguments` | 所有调用响应中 | string (JSON) | 模型生成的参数字符串，需 `JSON.parse()` 后校验是否符合对应工具的 `parameters` Schema |
| `tool_id` | Plug-in 系统 | string | 插件内工具的唯一 ID，用于调试和日志追踪（控制台悬停复制），不参与模型推理 |
| `env` / `KMS 加密凭证` | MCP 自定义服务配置 | object / secret | 工具执行所需的敏感参数（如 API Key），必须通过 KMS 加密注入，禁止明文 |

> ⚠️ 注意事项：
> - `parameters` 中 Object 类型的子属性 **不能为空**，否则工具发布失败；
> - GET 方法的插件 **不支持 Object 类型输入参数**，复杂结构请改用 POST + `application/json`；
> - 所有工具调用返回结果将作为上下文注入模型输入，显著增加 Token 消耗，请评估响应长度；
> - 单次请求最多触发 **10 个工具调用**（跨插件/跨 MCP 均计入）。

## 面向开发者，简洁实用

- **快速验证**：从控制台「插件市场」添加一个 `calculator` 插件到智能体，发送“37 × 89 等于多少？”，观察日志中 `tool_calls` 和 `tool` 消息即可确认函数调用通路。
- **调试要点**：优先检查 `function.name` 是否拼写一致、`function.arguments` 是否为合法 JSON、参数值是否满足 `parameters` 中 `type` 和 `required` 约束。
- **错误处理**：若模型未触发调用，检查 `description` 是否足够清晰（建议含示例）；若调用失败，先验证工具 URL 和鉴权配置，再检查 `in_params` 的 `passing_method`（`model_recognition` 表示由模型填充，`biz_pass_through` 表示由业务代码透传）。
- **生产建议**：对高并发场景，MCP 服务请启用「极速模式」避免冷启动延迟；涉及敏感操作的工具，务必在 `out_params` 中明确定义返回字段，防止模型误读冗余信息。

## 关联主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [application component api reference](../api/application-component-api-reference.md)
- [application call](../api/application-call.md)
- [plug in](../guides/plug-in.md)
- [model context protocol](../guides/model-context-protocol.md)


