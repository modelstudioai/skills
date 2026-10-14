# 函数调用

函数调用（Function Calling）是百炼平台中模型主动识别用户意图、生成结构化工具调用请求的能力，而非仅输出自然语言文本。它使大模型能与外部系统（如数据库、API、业务服务）安全、可控地协同执行任务，是构建智能体（Agent）、自动化工作流和生产级 AI 应用的核心机制。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台中并非单一 API 能力，而是贯穿多个层级的**语义能力+协议支持+运行时调度**组合：

- **专用意图理解模型**（`tongyi-intent-detect-v3`）：专为函数调用设计，以毫秒级延迟输出标准 OpenAI 格式的 `tool_calls` 数组（含 `function.name` 和 `function.arguments`），适用于对话路由、客服工单分派等低延迟编排场景。必须在 system message 中明确声明 `Response in INTENT_MODE.` 才触发该模式。

- **Omni 实时 API 模型**（如 `qwen3.8-omni-flash-realtime`）：在语音/文本实时交互中动态启用函数调用。通过 `tools` 参数注册工具列表后，模型可在流式响应中插入 `function_call` 事件；支持 `type=function`（传统 JSON Schema 工具）与 `type=mcp`（Model Context Protocol）双范式，且与联网搜索互斥。

- **Agent 开发框架**：
  - **Managed Agent**：自动解析模型返回的 `tool_calls` 并调用预置工具（如知识库检索、计算器），开发者无需编写调用逻辑；
  - **Flow Agent**：将“工具调用”作为可视化节点，可配置参数映射、错误重试与结果分支；
  - **Sandbox**：完全开放控制权，开发者需自行解析 `tool_calls` 字段、构造 HTTP 请求、处理响应并决定是否继续调用模型（即实现自定义 ReAct 循环）。

- **[OpenAI 兼容接口](openai-compatible-api.md)**（`chat/completions`）：所有支持函数调用的模型（如 `qwen3.8-max`、`qwen3-vl-plus`）均遵循 OpenAI 协议。需传入 `tools`（工具描述数组）和 `tool_choice`（指定 `auto`/`required`/`{"type": "function", "function": {"name": "xxx"}}`），模型返回 `finish_reason: "tool_calls"` 时即表示需执行工具。

> ⚠️ 注意：`qwen-deep-research`、`Qwen-Audio` 等模型**不支持函数调用**；OCR、GUI-Plus 等专用模型也未开放该能力——函数调用仅限明确标注支持的模型（详见各模型文档的「支持的功能」章节）。

## 关键参数和配置

| 参数 | 作用 | 必填 | 示例值 | 说明 |
|------|------|------|--------|------|
| `tools` | 声明可用工具列表，格式为 OpenAI `tools` schema | 是（启用调用时） | `[{"type": "function", "function": {"name": "get_weather", "parameters": {...}}}]` | 工具名（`name`）需全局唯一；`parameters` 必须为 JSON Schema object 类型；MCP 工具需设 `"type": "mcp"` |
| `tool_choice` | 控制模型是否及如何调用工具 | 否（默认 `auto`） | `"auto"` / `"none"` / `{"type": "function", "function": {"name": "get_weather"}}` | `required` 已弃用，推荐用 `{"type": "function", ...}` 显式指定 |
| `enable_thinking` | （部分模型）开启后返回 `reasoning_content` 字段，便于调试工具选择逻辑 | 否 | `true` | 仅 `gui-plus-2026-02-26`（混合思考版）等特定模型支持，需通过 `extra_body` 传入 |
| `max_tokens` | 限制模型生成 token 总数（含工具调用内容） | 否 | `4096` | 工具调用本身不消耗额外 token，但 `arguments` 字符串计入总长度 |

- **工具注册要求**：  
  - 工具名（`function.name`）必须为合法 Python 标识符（字母/数字/下划线，不以数字开头）；  
  - `arguments` 必须是合法 JSON 对象字符串（非原始 dict），模型返回的是已序列化的字符串，需 `json.loads()` 解析；  
  - 百炼不校验工具实际存在性，调用失败由开发者在 Sandbox 或 Flow Agent 中捕获并处理。

- **安全约束**：  
  - 所有工具调用均在百炼沙箱内执行（Managed/Flow Agent）或由开发者在 Sandbox 中显式发起；  
  - 工具 URL 必须为公网可访问 HTTPS 地址，禁止内网地址（如 `10.0.0.0/8`）；  
  - Sandbox 中调用外部 API 需通过百炼代理网关，不可直连。

## 面向开发者，简洁实用

- ✅ **快速验证**：用 `tongyi-intent-detect-v3` + `INTENT_MODE` 最快验证函数调用效果（<100ms 延迟）；  
- ✅ **生产首选**：对实时交互场景，优先选用 `qwen3.8-omni-flash-realtime`，它原生支持流式工具调用事件，避免阻塞等待；  
- ✅ **兼容迁移**：使用 OpenAI SDK 时，只需确保 `base_url` 指向业务空间专属域名，并传入标准 `tools` 参数，其余代码零修改；  
- ❌ **避免踩坑**：  
  - 不要对不支持模型（如 `qwen3.5-ocr`）传 `tools` 参数，将导致 `400 Bad Request`；  
  - 不要手动拼接 `tool_calls` 到 `messages` 中——模型只负责生成，调用由运行时完成；  
  - Sandbox 中务必对 `tool_calls` 做异常捕获，否则一次失败将中断整个 Agent 执行流。  

函数调用不是魔法，而是百炼将「意图识别 → 结构化生成 → 安全执行 → 结果注入」闭环封装后的工程能力。善用它，让模型真正成为你系统的协作者。

## 关联主题页

- [more about models](../api/more-about-models.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [agent development](../guides/agent-development.md)
- [more models](../api/more-models.md)
- [omni realtime api](../api/omni-realtime-api.md)


