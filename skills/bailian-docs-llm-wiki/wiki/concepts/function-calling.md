# 函数调用

函数调用（Function Calling）是百炼平台中大模型主动识别用户意图、结构化生成工具调用请求，并交由外部系统执行的关键能力。它使模型能突破纯文本生成边界，安全、可控地接入实时数据、执行计算、操作文件或调用业务 API，是构建智能体（Agent）、自动化工作流和增强型对话系统的核心机制。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台中并非单一接口能力，而是贯穿多个产品层级的统一语义机制，具体体现为：

- **Omni Realtime API**：在实时语音交互会话中，通过 `tools` 数组声明支持的工具（如天气查询、订单状态检查），模型在流式响应过程中可动态输出 `tool_calls` 事件；需注意 `tools` 与 `enable_search` 不可同时启用，二者属于正交能力路径。
- **Qwen API（OpenAI 兼容 / Responses / Anthropic Messages）**：  
  - OpenAI 兼容协议中，`tools` 字段用于声明工具列表，模型返回 `tool_calls`；  
  - **OpenAI Responses API 是唯一预置工具的入口**，内置 `web_search`、`code_interpreter` 等工具，无需开发者自行定义 schema；  
  - Anthropic Messages 协议支持自定义 `tools`，并可通过 `tool_choice` 显式控制调用策略（如 `"auto"`、`{"type": "tool", "name": "calculator"}`）。
- **插件（Plug-in）体系**：所有官方/三方/自定义插件均以函数调用形式被模型调用。工具 ID（`tool_id`）即函数名，输入参数由模型从用户 query 中抽取或由业务系统透传（通过 `biz_params`），输出结构需严格按插件定义的 `output parameters` 解析。
- **Managed Agents（托管智能体）**：内置工具（如 `bash`、`web_search`）和挂载的 MCP 服务均通过函数调用触发。模型在沙箱内自主规划多步调用序列，平台负责执行、状态管理与错误重试；`tools` 配置支持细粒度权限控制（`always_allow` / `always_ask`）。

> ✅ 统一行为：无论在哪一场景，模型均以标准 JSON Schema 描述工具能力，调用时输出 `tool_calls`（含 `id`、`function.name`、`function.arguments`），平台负责路由、执行、注入结果并继续推理。

## 关键参数和配置

| 参数 | 位置 | 类型 | 说明 | 注意事项 |
|------|------|------|------|----------|
| `tools` | 请求体顶层 | `array` | 工具定义列表，每个元素含 `type`（固定为 `"function"`）、`function.name`、`function.description`、`function.parameters`（JSON Schema） | Schema 必须合法且字段描述清晰，直接影响参数抽取准确率；避免嵌套过深（建议 ≤2 层） |
| `tool_choice` | 请求体顶层（Anthropic / OpenAI Responses） | `string` 或 `object` | 控制调用策略：`"auto"`（默认）、`"none"`（禁用）、`{"type": "function", "name": "xxx"}`（强制指定） | OpenAI Chat 协议不支持该字段，需依赖模型自身判断 |
| `tool_id` | 插件调用专用 | `string` | 插件唯一标识符（如 `"calculator"`），用于匹配 `tools` 中定义的 `function.name` | 必须与插件市场注册的 ID 完全一致，大小写敏感 |
| `biz_params` | 插件/API 调用体 | `object` | 业务系统透传的参数（如用户 ID、会话上下文），由平台注入到工具调用中 | 适用于需模型无法感知但工具执行必需的上下文信息（如鉴权 token、租户 ID） |
| `enable_search` | Omni Realtime `session.update` | `boolean` | 启用模型级联网搜索（非插件），与 `tools` 互斥 | 仅限 Omni Realtime 场景，与 `quark_search` 插件无关联 |

> ⚠️ 重要限制：  
> - `qwen-turbo` 系列模型在 Omni Realtime 中不支持覆盖 `temperature`/`top_p` 等参数，但函数调用能力本身不受影响；  
> - 所有场景下，`function.arguments` 必须为合法 JSON 字符串（非对象），模型输出后需由客户端或平台自动解析；  
> - 若工具执行失败，平台将返回结构化错误（如 `tool_call_id` + `error.message`），模型可据此重试或降级回复。

## 面向开发者，简洁实用

- **快速验证**：优先使用 **OpenAI Responses API**，它已预置常用工具，只需传入 `tools` 和 `messages`，无需定义 schema 或处理 MCP 服务注册。  
- **生产集成**：对自有 API，推荐封装为 **自定义插件**（支持 Header 鉴权、参数校验、示例填充），再通过 `tools` 声明调用；比裸写 Function Calling 更易维护、可观测。  
- **调试技巧**：开启 `stream: true`，监听 `tool_calls` 事件流；若模型未触发调用，检查 `function.description` 是否足够明确、`parameters` 是否遗漏必填字段、用户 query 是否含明确动作动词（如“查”、“算”、“生成”）。  
- **安全底线**：永远对 `function.arguments` 做白名单校验与输入消毒，禁止直接拼接执行命令；Managed Agents 的 `bash` 工具已默认沙箱隔离，但仍需避免 `rm -rf /` 类高危指令。

## 关联主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [plug in](../guides/plug-in.md)
- [managed agents](../guides/managed-agents.md)


