# 函数调用

函数调用（Function Calling）是百炼平台中实现模型与外部系统能力协同的核心机制：模型在推理过程中，可自主识别用户意图、生成结构化工具调用请求（含函数名与参数），由平台或 SDK 负责安全执行、结果注入并继续推理，从而完成搜索、计算、OCR、GUI操作等超出纯语言生成范畴的任务。

## 在百炼平台的不同场景中，这个概念如何使用

- **[OpenAI 兼容接口](openai-compatible-interface.md)（`/chat/completions`）**：通过 `tools` 数组注册函数定义，设置 `tool_choice` 控制调用策略（如 `"auto"` 或指定函数名）。模型返回 `{"tool_calls": [...]}`，SDK 自动解析、执行并拼接 `tool_message` 后续调用。适用于通用文本+工具混合任务（如查天气、调用数据库）。

- **意图理解模型（`tongyi-intent-detect-v3`）**：不直接执行函数，而是作为“函数调用前置决策器”——输入用户消息后，输出标准化意图标签（如 `SEARCH_PRODUCT`）及结构化参数（如 `{"keyword": "无线耳机"}`），供业务层路由至对应工具或服务。需严格配置 System Message 以启用 `INTENT_MODE`。

- **Agent 框架（Managed / Flow / Sandbox）**：  
  - *Managed Agent*：工具由控制台预绑定，模型自动触发，开发者无需透传 `tools`；  
  - *Flow Agent*：工具调用作为独立节点嵌入工作流，支持条件分支与多工具串行/并行；  
  - *Sandbox Agent*：在 Python `run()` 函数内，通过 `self.call_tool(name, **kwargs)` 显式发起调用，完全掌控执行逻辑与错误处理。

- **GUI 自动化模型（`gui-plus` 系列）**：必须配合 `computer_use` 工具函数使用。模型接收截图后，输出 `tool_calls` 调用 `computer_use` 并传入操作指令（如 `{"action": "click", "x": 120, "y": 340}`），平台执行真实鼠标键盘操作并返回屏幕变化结果。

> ⚠️ 注意：`qwen-deep-research` 等专用模型**不支持标准 `function_call` 协议**，其“研究路径规划”和“网络搜索”为内置能力，不可自定义工具；OCR/GUI 类模型虽支持 `tool_calls`，但仅限平台预置的专用工具（如 `ocr_extract`, `computer_use`），不接受任意第三方函数注册。

## 关键参数和配置

| 参数 | 作用 | 适用场景 | 示例值 |
|------|------|----------|--------|
| `tools` | 定义可用函数列表，含 `name`、`description`、`parameters`（JSON Schema） | [OpenAI 兼容接口](openai-compatible-interface.md)、Flow Agent、Sandbox Agent | `[{"name": "get_weather", "description": "查询城市天气", "parameters": {"type": "object", "properties": {"city": {"type": "string"}}}}]` |
| `tool_choice` | 控制模型是否及如何调用函数 | [OpenAI 兼容接口](openai-compatible-interface.md) | `"auto"`（默认）、`"none"`、`{"type": "function", "function": {"name": "get_weather"}}` |
| `enable_thinking` | 是否启用带推理链的工具调用（返回 `reasoning_content` 字段） | `gui-plus`、Batch 接口 | `true`（开启后响应含思考过程，计费更高） |
| `system` message 中的指令 | 触发特定函数调用模式的关键开关 | 意图理解模型、OpenAI 兼容接口 | `"Response in INTENT_MODE."`（意图模型）、`"You are a helpful assistant that can call functions."`（通用模型） |

- **必填约束**：所有工具调用均要求 `parameters` 符合 JSON Schema 校验；若传入非法参数，平台将返回 `400 Bad Request` 并提示具体字段错误。
- **安全限制**：工具执行环境严格隔离（Sandbox 沙箱、Connector 白名单域名、MCP 权限管控），禁止直接访问内网、本地文件系统或未授权 API。

## 面向开发者，简洁实用

- ✅ **快速验证**：用 Playground 测试 `qwen3.8-max` + `tools`，观察 `tool_calls` 输出格式；再换 `tongyi-intent-detect-v3` 对比意图标签输出差异。  
- ✅ **生产建议**：  
  - 优先使用 Managed Agent 封装高频工具（如订单查询），降低维护成本；  
  - 复杂逻辑（如多步骤表单填写）用 Sandbox Agent 自行 `call_tool` 并处理异常；  
  - GUI 自动化务必搭配 `vl_high_resolution_images: true` 提升截图定位精度。  
- ❌ **避坑提示**：  
  - 不要对 `qwen-deep-research` 传 `tools` 参数——会被忽略且可能引发兼容性警告；  
  - `tools` 数组长度无硬性上限，但超过 20 个函数会显著增加模型推理延迟，建议按场景分组注册；  
  - 所有工具调用结果均以 `tool_message` 形式注入下一轮 `messages`，勿遗漏该消息体否则上下文断裂。

## 关联主题页

- [more models](../api/more-models.md)
- [get started with agents](../guides/get-started-with-agents.md)
- [agent development](../guides/agent-development.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


