# 函数调用

函数调用（Function Calling）是百炼平台支持的核心能力之一，指大模型在推理过程中主动识别用户意图、生成结构化工具调用请求（含工具名称与参数），并由平台自动执行外部函数或插件，最终将结果注入上下文继续推理的闭环机制。该能力使模型突破静态知识边界，实现动态计算、实时检索、多模态生成等复杂任务。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台并非单一接口功能，而是贯穿多个服务层级的统一语义能力，具体体现为以下三种协同形态：

- **基础模型 API 层（Assistant API）**：通过 `tools` 字段声明可用函数列表（如 `calculator`, `code_interpreter`），设置 `tool_choice` 控制调用策略（`auto`/`required`/指定工具名）。模型自主决定是否调用、调用哪个工具及传入参数，返回 `tool_calls` 结构；开发者需按 `tool_call_id` 同步执行并回填 `tool_responses`，再发起下一轮请求完成完整链路。

- **托管智能体（Managed Agents）层**：函数调用被深度集成进 Agent 执行引擎。开发者通过 `tools` 参数注册 HTTP、知识库检索、自定义 Skill 等工具，Agent 自动规划多步调用序列（支持嵌套、并行）、管理会话状态与上下文隔离，并内置错误重试与超时熔断。无需手动处理 `tool_calls`/`tool_responses`，平台自动完成“规划→调用→注入→再推理”全流程。

- **插件（Plug-in）与 [OpenAI 兼容接口](openai-compatible-api.md)层**：官方插件（如 `quark_search`, `generate_qrcode`）和 OpenAI 兼容的 `chat.completions` 接口均复用同一函数调用协议。插件市场发布的工具可直接绑定至智能体或工作流；OpenAI SDK 用户只需传入 `tools` 和 `tool_choice`，即可获得与原生 OpenAI 一致的函数调用体验，底层由百炼统一调度。

> ✅ 统一性提示：无论使用哪一层，函数调用的输入描述格式（JSON Schema）、参数提取逻辑、安全校验规则（如 Object 子属性非空、GET 方法禁用 Object 参数）均由平台统一实施，确保行为一致性。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 | 典型值 |
|------|------|------|------|--------|
| `tools` | array | 是（启用函数调用时） | 工具定义列表，每个元素含 `type`（`function`/`http`/`retrieval`）、`function.name`、`function.description`、`function.parameters`（JSON Schema 格式） | `[{"type": "function", "function": {"name": "calculator", "description": "执行数学运算", "parameters": {"type": "object", "properties": {"expression": {"type": "string"}}, "required": ["expression"]}}}]` |
| `tool_choice` | string / object | 否 | 控制调用策略：<br>- `"auto"`（默认）：模型自主决策<br>- `"none"`：禁止调用<br>- `"required"`：必须调用一个工具<br>- `{"type": "function", "function": {"name": "xxx"}}`：强制调用指定工具 | `"auto"`, `"required"`, `{"type":"function","function":{"name":"code_interpreter"}}` |
| `tool_input` | object | 否（仅部分 SDK/API 支持） | 显式指定工具输入参数（绕过模型提取），适用于确定性调用场景 | `{"expression": "sqrt(144) + 2*3"}` |
| `biz_params` | object | 否（鉴权/透传场景） | 业务级参数透传字段，用于携带用户 [Token](token.md)、API Key、自定义元数据等，不参与模型推理 | `{"user_token": "xxx", "session_id": "abc123"}` |

> ⚠️ 注意事项：
> - `tools` 中 `function.parameters` 的 JSON Schema 必须严格校验：Object 类型的子属性不可为空，否则发布失败（错误码 `130022`）；
> - 模型仅支持 `qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max`、`qwen-vl-plus` 及部分 OpenAI 兼容模型（如 `qwen3.8-max`），其他模型调用将静默忽略 `tools`；
> - 托管智能体中，单次请求最多触发 5 次工具调用，单个 Agent 最多绑定 10 个工具（插件场景）或 100 个 Skill（Managed Agents API 场景）。

## 面向开发者，简洁实用

- **快速验证**：控制台「调试」页 → 选择支持函数调用的模型 → 在 `tools` 输入框粘贴工具定义 → 发送测试请求，观察响应中的 `tool_calls` 字段。
- **SDK 推荐**：Python 使用 `dashscope` v1.20.0+ 或 `openai` v1.0+（配置 `base_url`）；Node.js 使用 `@alibabacloud/dashscope` v1.15.0+。避免自行解析 `tool_calls`，优先使用 SDK 封装的 `call_with_tools()` 或 `chat.completions.create()` 方法。
- **调试技巧**：开启 `stream=true` 时，函数调用请求出现在 `event: tool_calls` SSE 事件中；若模型未触发调用，检查 `function.description` 是否清晰、`parameters` 是否覆盖用户可能输入的关键字段。
- **生产建议**：对关键工具调用，务必在业务侧实现幂等处理与超时兜底；敏感操作（如支付、删除）禁止依赖模型自动调用，应改为工作流节点人工确认。

## 关联主题页

- [start using](../guides/start-using.md)
- [managed agents](../guides/managed-agents.md)
- [managed agents api](../api/managed-agents-api.md)
- [plug in](../guides/plug-in.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


