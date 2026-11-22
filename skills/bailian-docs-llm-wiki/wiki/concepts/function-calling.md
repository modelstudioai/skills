# 函数调用

函数调用（Function Calling）是百炼平台中实现大模型与外部能力深度协同的核心机制，指模型在推理过程中自主识别用户意图、生成结构化工具调用请求（`tool_calls`），并由平台或开发者运行时解析、执行对应函数后将结果注入后续上下文，从而完成复杂任务闭环。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台并非单一接口能力，而是贯穿多个层级的横切能力，其使用方式因场景而异：

- **意图理解模型（`tongyi-intent-detect-v3`）**：专为轻量级函数调用编排设计。模型在毫秒级响应中直接输出标准化 `tool_calls`（如 `{"name": "route_to_faq", "arguments": {"intent": "refund_policy"}}`），无需额外提示工程，适用于对话路由、智能助手快速分发等低延迟场景。

- **Agent 开发（Managed / Flow / Sandbox Agent）**：函数调用是 Agent 的默认交互范式。模型根据 `tools` 定义自动生成调用请求；Managed 和 Flow Agent 由平台自动调度已注册工具（MCP 或 Skill），Sandbox Agent 则需在 `app.py` 中显式实现 `tool_calls` 解析逻辑，并返回 `tool_call_id` 对应的执行结果。

- **Agent 上下文（Context）集成**：当启用 RAG、Connector 或 ParseX 时，函数调用常作为隐式触发环节——例如用户上传 PDF 后，系统自动调用 `parsex` 技能提取内容，再将结果以 `tool_message` 形式注入上下文，整个过程对开发者透明但依赖函数调用协议。

- **Agent Store（MCP & Skill）**：MCP 是函数调用的标准化协议载体，每个 MCP 服务（如 `web_search`, `amap-maps`）均暴露为一个可被模型识别和调用的函数；Skill 则通过语义匹配自动触发，其内部执行也遵循 `tool_call → execute → tool_message` 流程，但封装更轻量、无网络依赖。

> ✅ 统一行为：所有场景下，模型输出的 `tool_calls` 均为标准 OpenAI 格式（含 `id`, `function.name`, `function.arguments`），平台 SDK 自动处理序列化、调度、超时与错误注入，开发者只需关注函数定义与结果处理。

## 关键参数和配置

函数调用能力本身不依赖独立参数，但其生效需配合以下关键配置：

| 配置项 | 所属场景 | 说明 |
|---------|-----------|------|
| `tools` | Agent / Chat API 调用 | 必填数组，声明可用函数列表（OpenAI 兼容格式）。每个元素含 `type: "function"`、`function.name`、`function.description` 及 `parameters` JSON Schema。平台据此约束模型输出范围。 |
| `tool_choice` | Agent / Chat API 调用 | 控制调用策略：<br>• `"auto"`（默认）：模型自主决定是否及调用哪个函数；<br>• `"none"`：禁用函数调用；<br>• `{"type": "function", "function": {"name": "xxx"}}`：强制调用指定函数（适合确定性流程）。 |
| `enable_thinking` | GUI-Plus 等专用模型 | 若启用，模型会在 `tool_calls` 前输出 `reasoning_content` 字段，便于调试调用逻辑（如“用户要求点击‘提交’按钮，需先定位该按钮坐标”）。 |
| `max_iterations` | Managed / Flow Agent | 限制单次会话中函数调用的最大轮次（默认 15），防止无限循环；Sandbox Agent 由代码控制，不受此限。 |
| `context.tools` | Agent Context 配置 | 当通过 `context` 注入工具时（如 Connector 绑定的数据库查询函数），需在此处声明，确保模型在上下文感知状态下可调用。 |

> ⚠️ 注意：  
> - 工具函数的 `parameters` Schema 必须严格符合 JSON Schema 规范（如 `string`, `number`, `array`, `required` 字段），否则模型可能生成非法 `arguments`；建议使用 `jsonschema` 库校验。  
> - `tool_calls` 中的 `arguments` 始终为字符串（JSON 序列化后），需在运行时 `json.loads()` 解析——Sandbox Agent 必须自行完成此步。  
> - 函数执行失败时，平台将自动注入 `tool_message`（含 `tool_call_id` 和 `content: "error: xxx"`），模型可据此重试或降级回答。

## 面向开发者，简洁实用

- ✅ **快速启用**：在 Agent 配置或 Chat API 请求中传入 `tools` 数组，即可开启函数调用；无需修改模型或部署额外服务。  
- ✅ **调试技巧**：设置 `tool_choice="none"` 发送相同输入，对比纯文本输出与 `tool_calls` 输出，快速验证提示词与工具描述是否引导准确。  
- ✅ **错误处理**：始终检查响应中是否存在 `tool_calls`；若存在，必须执行对应函数并按 `tool_call_id` 返回结果，否则会中断 Agent 流程。  
- ✅ **性能提示**：单次请求中 `tools` 数量建议 ≤20；过多函数会增加模型推理开销并降低调用准确率；高频调用场景优先复用 MCP 服务而非重复注册相似工具。  
- ✅ **安全边界**：函数执行环境默认隔离（Sandbox Agent 可配 `allow_internet`），但 `tools` 的 `description` 不应暴露敏感实现细节（如“调用内部风控 API”），应聚焦用户可见能力（如“验证订单风险等级”）。

## 关联主题页

- [more models](../api/more-models.md)
- [agent development](../guides/agent-development.md)
- [agent context](../guides/agent-context.md)
- [agent store](../guides/agent-store.md)


