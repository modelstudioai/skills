# 函数调用

函数调用（Function Calling）是百炼平台中模型主动识别用户意图、生成结构化工具请求，并交由系统或外部服务执行的关键能力。它不是简单的 API 请求转发，而是模型在推理过程中自主完成“规划—参数提取—调用触发”闭环的智能行为，是构建可行动 Agent 的核心机制。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台中并非单一接口能力，而是贯穿多个层级的统一语义抽象，具体体现为：

- **Qwen API（OpenAI 兼容 Responses / Anthropic Messages 协议）**：通过 `tools` 数组声明可用函数（含内置工具如 `web_search`、`code_interpreter` 及自定义 function），模型在 `tool_use` 消息中返回 JSON 格式的调用请求（含 `name` 和 `input`）。开发者需解析响应、执行实际逻辑、再将结果以 `tool_result` 形式回传继续对话。

- **Managed Agents API（托管智能体）**：函数调用被封装为 `tool_call` 和 `tool_result` 事件类型，通过 `/v1/sessions/{session_id}/events` SSE 流实时推送。Agent 运行时自动调度已绑定的 Skill（即注册的函数），无需开发者手动解析或拼接消息——平台完成从模型输出到 Skill 执行、结果注入的全链路托管。

- **LLM 应用（智能体应用 Agent 2.0）**：函数调用与知识库、MCP [插件](plugin.md)等统一抽象为“工具”，由模型自主决策调用顺序与时机。控制台配置中启用[插件](plugin.md)即等效于向模型暴露对应函数；运行时所有工具调用均展示在“规划-执行-反思”链路中，支持调试与审计。

- **[插件](plugin.md)（Plug-in）**：每个插件本质上是一个可注册、可发现、可调用的函数。无论是官方 `calculator` 还是自定义 MCP 服务，其输入/输出参数、鉴权方式、错误处理均由插件元数据严格定义，确保模型生成的调用请求可被安全、确定性地执行。

- **Omni Realtime API（实时[多模态](multi-modal.md)）**：通过 `session.update` 设置 `tools` 后，模型可在语音或文本交互中动态触发函数（如搜索、计算），并以 `tool_call` 事件形式实时下发。该场景强调低延迟响应，调用与结果反馈均通过 WebSocket 事件流完成，不依赖传统 HTTP 轮询。

> ✅ 统一原则：无论在哪一场景，**函数调用的发起方始终是模型（而非开发者代码）**；开发者职责是提供清晰的工具定义、可靠的服务实现、以及合规的结果回传机制。

## 关键参数和配置

函数调用行为由以下关键参数协同控制，需在对应 API 或配置界面中显式设置：

- `tools`（必填数组）：定义可用函数列表，每项包含：
  - `type`: 当前仅支持 `"function"`；
  - `function.name`: 工具唯一标识符（如 `"web_search"`、`"text_to_image"`），必须与插件 ID 或 Skill ID 严格一致；
  - `function.description`: 供模型理解用途的自然语言描述（影响调用准确性）；
  - `function.parameters`: JSON Schema 格式，明确定义输入字段名、类型、是否必需、示例值等（**Schema 必须有效且无空 Object**）。

- `tool_choice`（可选）：控制模型调用策略：
  - `"auto"`（默认）：模型按需自主决定是否及何时调用；
  - `"none"`：禁用所有函数调用；
  - `{"type": "function", "name": "xxx"}`：强制指定调用某函数（适用于确定性流程）。

- `enable_search`（Omni Realtime 特有）：布尔开关，启用后模型可自动触发联网搜索（底层复用夸克搜索能力），**与 `tools` 互斥，不可同时启用**。

- 鉴权与透传（自定义插件/MCP）：
  - `biz_params`：用于传递业务级参数（如用户 ID、会话上下文），在 API 调用时透传至插件后端；
  - Header/Query 鉴权：在插件配置中预设 `Authorization`、`X-Api-Key` 等，由平台自动注入请求头或查询参数。

## 面向开发者，简洁实用

- ✅ **定义优先**：写好 `function.description` 和精准的 `parameters` Schema，比调整 temperature 更能提升调用准确率。
- ✅ **验证必做**：自定义插件发布前务必完成在线调试；Qwen API 中首次使用新工具，建议先用 `stream=false` 测试非流式响应。
- ✅ **错误要捕获**：模型可能生成非法参数（如类型错误、缺失必填字段）。你的工具实现必须校验输入，并返回符合 `tool_result` 格式的结构化错误（如 `{"error": "Invalid URL format"}`）。
- ✅ **结果需精简**：`tool_result` 内容将计入模型上下文。避免返回原始 HTML、长日志或二进制数据；提取关键字段（如搜索摘要、计算结果）即可。
- ⚠️ **注意兼容性**：`qwen-turbo` 等轻量模型函数调用稳定性低于 `qwen-max`；`qwen-vl` 系列图像理解模型暂不支持工具调用；`QwQ`/`QVQ` 模型不支持 `system` 消息，影响工具描述可见性——请以[各模型文档](raw/model-api-reference/qwen-api-reference.md)为准。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [managed agents api](../api/managed-agents-api.md)
- [llm application](../guides/llm-application.md)
- [plug in](../guides/plug-in.md)
- [omni realtime api](../api/omni-realtime-api.md)


