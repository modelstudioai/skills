# 函数调用

函数调用（Function Calling）是百炼平台中大模型主动识别用户意图、规划执行步骤，并按标准协议触发外部工具或服务的关键能力。它使模型从“纯文本生成器”升级为可操作现实世界的智能代理，支撑联网搜索、代码执行、图像生成、数据库查询等超出模型原生能力的复杂任务。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台中并非单一接口特性，而是贯穿多个技术栈的统一语义能力，具体体现为：

- **API 层（Qwen API）**：在 `Responses` 和 `Anthropic Messages` 协议中，通过 `tools` 字段声明可用函数列表；模型返回结构化 `tool_calls`，平台自动解析并同步/异步调用对应工具，再将结果注入上下文继续推理。`Responses API` 还支持内置工具（如 `web_search`, `code_interpreter`）开箱即用，无需额外部署。

- **Agent 开发层**：Managed Agent 和 Flow Agent 原生集成函数调用逻辑——开发者只需配置 `tools` 参数，Agent 运行时自动完成工具选择、参数提取、调用执行与结果整合；Sandbox Agent 则由开发者在 Python 沙箱中手动调用 `agent_tools.*` 或自定义 HTTP 客户端，实现完全可控的函数调度。

- **插件（Plug-in）层**：所有插件（官方/三方/自定义）均以函数为最小可调用单元。自定义插件需明确定义 `tool_name`、`tool_description` 和 `input_parameters`，其本质就是注册一个可通过自然语言触发的 HTTP 函数端点；调用时平台自动完成参数映射、鉴权透传（`biz_params`）和响应解析。

- **Application Call 层**：当调用已发布的智能体或工作流应用时，若该应用启用了插件或工具，`biz_params` 可携带运行时参数（如用户 token、业务 ID），驱动函数调用动态适配上下文；RAG 检索、知识库查询等高级功能也常以内置函数形式参与调用链。

- **Omni Realtime 层**：在实时音视频交互中，函数调用支持 `type=function`（传统工具）与 `type=mcp`（MCP 协议插件）双模式共存（仅 `qwen3.8-omni-flash-realtime` 支持），允许模型在语音对话流中即时触发搜索、计算或图像生成，并将结果以文本+音频混合方式实时返回。

> ✅ 关键共识：无论在哪一层，函数调用都遵循「声明 → 规划 → 执行 → 注入」四步闭环，且调用结果始终作为新消息（`tool_result`）加入 `messages` 上下文，供后续推理使用。

## 关键参数和配置

| 参数 | 作用 | 必填 | 常见值/说明 |
|------|------|------|-------------|
| `tools` | 声明可用函数列表 | 是（启用调用时） | 数组，每个元素含 `name`（字符串）、`description`（自然语言描述）、`parameters`（JSON Schema 定义）。`Responses API` 支持内置工具名（如 `"web_search"`）；`Anthropic` 需带日期后缀（如 `"web_search_20250305"`）；`Omni Realtime` 支持 `{"type": "function"}` 或 `{"type": "mcp"}`。 |
| `tool_choice` | 控制调用策略 | 否 | `"auto"`（默认，模型自主决定）、`"none"`（禁用）、`{"type": "function", "function": {"name": "xxx"}}`（强制指定）。`Responses API` 使用 `tool_choice`；`Anthropic` 使用 `tool_choice`；`Omni Realtime` 使用 `tool_choice`。 |
| `biz_params` | 传递运行时上下文参数 | 否（按需） | 对象，用于向工具注入用户级信息（如 `"user_id": "u123"`）、鉴权凭证（`"user_defined_tokens"`）或业务透传字段（`"biz_data"`）。在 Application Call 和 Plug-in 场景中关键。 |
| `enable_search` | 启用内置联网搜索（替代自定义工具） | 否 | `true`/`false`。注意：与 `tools` **互斥**，不可同时启用（尤其在 Omni Realtime 中）。 |
| `previous_response_id`（仅 Responses） | 复用历史调用上下文 | 否 | 字符串，用于多轮函数调用链的上下文继承（如搜索→摘要→翻译），避免重复传参。 |

> ⚠️ 注意事项：
> - 工具描述（`description`）质量直接影响模型调用准确率，建议包含典型输入示例；
> - `parameters` 的 JSON Schema 必须严格定义类型与必填项，`Object` 类型子属性不能为空（否则插件发布失败）；
> - 所有协议中，函数调用返回的 `tool_call_id` 必须与后续 `tool_result` 的 `tool_call_id` 精确匹配，否则上下文注入失败；
> - 流式响应中，`tool_calls` 事件需在 `message` 事件前到达，客户端应按事件顺序组装完整上下文。

## 面向开发者，简洁实用

- **快速验证**：用 `qwen3.8-max` + `Responses API`，`tools` 设为 `[{"name": "calculator", "description": "执行数学运算，如 '2+3*4'" }]`，输入 `"计算 123 的平方根"`，观察是否返回 `tool_calls`。
- **生产推荐**：优先使用 `Responses API`（非 `Chat API`），因其支持 `previous_response_id`、`store`、内置工具及更稳定的多模态函数调用语义。
- **调试技巧**：开启 `stream=true`，监听 `event: tool_call` 和 `event: tool_result` 事件，确认调用链完整性；检查响应中的 `response.tool_calls` 字段是否存在及格式是否合法。
- **避坑提示**：`enable_search=true` 与自定义 `tools` 不兼容；`Anthropic` 工具名必须带日期后缀；`Omni Realtime` 中 `mcp` 工具仅 `qwen3.8` 支持；所有函数调用结果都需显式注入上下文，平台不会自动重试失败调用。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [agent development](../guides/agent-development.md)
- [plug in](../guides/plug-in.md)
- [application call](../api/application-call.md)
- [omni realtime api](../api/omni-realtime-api.md)


