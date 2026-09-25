# 函数调用

函数调用（Function Calling）是百炼平台支持的一种结构化工具编排能力，指模型在生成响应时，主动识别用户意图并按预定义 Schema 生成标准 JSON 格式的函数调用请求（而非自由文本），交由开发者后端执行真实动作（如查数据库、调第三方 API、控制设备等），再将结果注入上下文继续推理。该机制是构建可靠 AI Agent 的核心基础设施。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用能力在百炼平台中并非所有模型默认启用，而是**按模型类型和调用方式差异化支持**，主要应用于以下三类场景：

- **意图理解专用模型（`tongyi-intent-detect-v3`）**：这是百炼最轻量、最高效的函数调用入口。它不生成自然语言回复，而是专精于毫秒级意图识别与函数名+参数的精准提取。需在 `system` 消息中明确声明 `Response in INTENT_MODE.`，并在 `messages` 中提供工具定义（JSON Schema）或意图字典。适用于对话路由、客服工单分派、智能硬件指令解析等低延迟决策场景。

- **Qwen3 系列大模型（如 `qwen3.8-max`, `qwen3.7-plus`）通过 Responses API**：在 OpenAI 兼容的 `responses.create()` 接口中启用。模型可自主判断是否需要调用函数，并返回符合 OpenAI Function Calling 规范的 `tool_calls` 字段（含 `function.name` 和 `function.arguments`）。开发者需自行解析、执行、构造 `tool_result` 并再次提交给模型完成闭环。支持多轮工具调用与上下文自动关联（通过 `previous_response_id` 维持会话状态）。

- **GUI 自动化模型（`gui-plus` 系列）**：结合 `computer_use` 工具函数，实现“截图→理解→生成鼠标/键盘操作指令”的端到端自动化。调用时需在 `extra_body` 中传入非标参数（如 `enable_thinking=true`），并确保 `messages[0].content` 包含有效截图 URL。该场景下函数调用结果直接驱动操作系统行为，属于高权限、强领域耦合的专用能力。

> ⚠️ 注意：  
> - `qwen-deep-research`、OCR、嵌入等模型**不支持函数调用**；  
> - Java SDK 当前**不支持 OpenAI 兼容的 function calling 流程**，仅 Python DashScope SDK 和 OpenAI SDK（配合 `base_url`）可用；  
> - 所有函数调用均依赖 `model` 参数严格匹配已开通服务的模型名，且必须使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）。

## 关键参数和配置

| 参数 | 作用 | 说明 | 是否必需 |
|------|------|------|----------|
| `tools` | 定义可用函数列表 | OpenAI 兼容格式数组，每个元素为 `{ "type": "function", "function": { "name": "...", "description": "...", "parameters": { ... } } }`。Schema 必须合法，否则模型无法解析。 | 是（启用函数调用时） |
| `tool_choice` | 控制调用策略 | 可选 `"auto"`（默认，模型自主决定）、`"none"`（禁用）、或 `{"type": "function", "function": {"name": "xxx"}}`（强制指定）。 | 否（默认 `auto`） |
| `system` message 内容 | 触发意图识别模式 | 对 `tongyi-intent-detect-v3`，必须包含 `Response in INTENT_MODE.`；可附加工具描述或意图枚举（如 `"intent_options": ["search_order", "cancel_subscription"]`）。 | 是（对该模型） |
| `previous_response_id` | 维持多轮工具交互上下文 | 传入上一轮 `responses.create()` 返回的顶层 `id`（非 `output` 中消息 ID），用于自动注入历史工具调用结果。 | 是（多轮调用时） |
| `enable_thinking` | 启用混合推理模式（部分模型） | 如 `gui-plus-2026-02-26` 需通过 `extra_body` 传入 `{"enable_thinking": true}` 才激活 `reasoning_content` 输出，辅助调试函数选择逻辑。 | 否（按需） |

## 面向开发者：快速上手建议

- ✅ **首选 `tongyi-intent-detect-v3` 做轻量路由**：延迟 <50ms，无需流式处理，适合高频、确定性意图场景；  
- ✅ **用 Responses API + `qwen3.8-max` 构建通用 Agent**：兼容 OpenAI 生态，支持 `tool_result` 注入与上下文延续，推荐搭配 LangChain 或自研 Orchestrator；  
- ✅ **始终校验 `function.arguments` JSON 合法性**：模型可能输出语法错误的 JSON，务必用 `json.loads()` 包裹并捕获异常；  
- ❌ **避免在异步任务（如图像生成）中混用函数调用**：异步接口不支持 `tools` 参数，函数调用仅适用于同步文本/多模态推理；  
- 🔐 **生产环境禁用前端直调函数调用**：因涉及后端敏感操作，必须通过可信服务层做参数校验、权限控制与审计日志。

## 关联主题页

- [more about models](../api/more-about-models.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [more models](../api/more-models.md)


