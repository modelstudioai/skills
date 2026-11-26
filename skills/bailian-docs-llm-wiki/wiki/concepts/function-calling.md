# 函数调用

函数调用（Function Calling）是百炼平台中实现大模型与外部系统协同执行的关键机制：模型在推理过程中，可主动识别用户意图、生成结构化的工具调用请求（含函数名与参数），由平台运行时解析并安全执行对应函数，再将结果注入后续对话上下文，从而完成复杂任务闭环。

## 在百炼平台的不同场景中，这个概念如何使用

- **基础模型调用**：在 `qwen-max`、`qwen-plus` 等支持 `function_calling` capability 的模型上，通过 `tools` 参数声明可用函数列表，模型会在 `messages` 中返回 `tool_calls` 字段（非文本内容），开发者需自行解析、执行并拼回 `tool_message` 继续对话。  
- **Agent 自动化工作流**：Managed Agent 和 Flow Agent 原生集成函数调用能力，无需手动处理 `tool_calls` —— 平台自动路由、鉴权、执行、超时重试，并将结果以标准格式注入记忆上下文，支撑多步决策（如“查天气→订机票→发邮件”）。  
- **意图理解专用模型**：`tongyi-intent-detect-v3` 在 `INTENT_MODE` 下直接输出符合函数签名的 JSON 结构（含 `function_name` 与 `arguments`），可作为轻量级工具编排入口，适用于规则明确、低延迟要求的场景。  
- **CLI 工具链驱动**：百炼 CLI 的 Skills（如 `bl image generate`、`bl rag search`）本质是预注册的函数，当用户输入自然语言指令（如“生成产品图”），CLI 内置 Agent 自动触发对应函数调用，屏蔽底层 API 细节。  
- **Responses API 高级模式**：OpenAI 兼容的 Responses 接口内置联网搜索、代码解释器等系统函数，启用后模型可自主触发，无需显式传入 `tools`，适合快速构建免开发智能体。  
- **深度研究与 GUI 自动化**：`qwen-deep-research` 在规划阶段会生成带参数的子任务调用；`gui-plus` 则将鼠标点击、键盘输入等操作抽象为可调用函数，实现端到端界面交互闭环。

## 关键参数和配置

- `tools`: 必填（当启用函数调用时），为函数定义数组，每个元素包含 `type: "function"`、`function.name`（字符串，需与后端注册名一致）、`function.description`（功能说明）、`function.parameters`（JSON Schema 格式，用于模型参数生成约束）。  
- `tool_choice`: 控制调用策略，可选 `"auto"`（默认，模型自主决定是否调用）、`"none"`（禁用）、或 `{"type": "function", "function": {"name": "xxx"}}`（强制指定函数）。  
- `response_format`: 若需模型返回严格 JSON 结构（如函数参数），建议配合 `{"type": "json_object"}` 使用，但需确保所选模型 capability 支持该格式。  
- `enable_thinking`: 在 Batch 或 GUI 场景中，设为 `false` 可跳过推理过程，直接输出函数调用，降低 token 开销与延迟。  
- **能力校验前置**：调用前必须确认目标模型的 `capabilities` 包含 `"function_calling"`（通过 `GET /v2/models/{model}` 查询），否则请求将被拒绝（HTTP 400）。

## 面向开发者，简洁实用

- ✅ **推荐实践**：优先使用 Responses API 或 Managed Agent，让平台托管函数调度逻辑；仅在需精细控制执行顺序/错误处理时，才手动处理 `tool_calls`。  
- ✅ **调试技巧**：开启 `stream: true` 可实时观察模型是否进入函数调用分支（响应中出现 `delta.tool_calls`）；若始终无 `tool_calls`，检查 `tools` 描述是否清晰、`messages` 是否提供足够触发线索。  
- ⚠️ **避坑提示**：  
  - 不要将敏感凭证（如数据库密码）硬编码在 `tools` 的 `function.parameters` 中，应通过 Connector 或环境变量注入；  
  - `tool_calls` 中的 `arguments` 是字符串（非 JSON 对象），需 `JSON.parse()` 后再传入函数；  
  - 多函数并发调用需自行实现并发控制与结果聚合，平台不保证执行顺序。  
- 📦 **快速起步**：用 CLI 初始化一个带函数能力的 Agent：`bl agent init --with-skills image,rag`，然后发送 `帮我用RAG查最新AI政策，再生成摘要图`，即可体验端到端函数链路。

## 关联主题页

- [getting started](../guides/getting-started.md)
- [capabilities](../guides/capabilities.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [more models](../api/more-models.md)
- [agent context](../guides/agent-context.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


