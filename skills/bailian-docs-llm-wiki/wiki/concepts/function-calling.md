# 函数调用

函数调用（Function Calling）是百炼平台核心的工具集成能力，指大语言模型在推理过程中主动识别用户意图、生成结构化工具调用请求（`tool_calls`），并由平台自动执行外部 API（如企业微信消息发送、数据库查询、RAG 检索等），再将结果注入后续推理链路的闭环机制。该能力无需开发者手动解析指令或拼接 HTTP 请求，实现“语义到动作”的端到端自动化。

## 在百炼平台的不同场景中如何使用

- **应用级集成（Application Use Cases）**：用于对接企业微信、钉钉等办公平台开放接口。例如，在客服助手场景中，当用户说“把订单号 12345 的物流信息发给张经理”，模型可自动生成 `work_wechat_send_message` 工具调用，平台自动完成身份鉴权、消息组装与投递。需在请求中显式传入 `tools` 参数声明可用工具列表。

- **Managed Agents API**：作为托管智能体的核心执行单元，函数调用与 Skill（技能）深度绑定。每个 Skill 封装一个或多个工具逻辑（如 `fetch_customer_data`），Agent 在运行时根据 `session_id` 和 `memory_store_id` 上下文动态选择并调用 Skill，调用结果自动写入 Memory Store 并参与后续决策。

- **Qwen API（OpenAI 兼容 / Anthropic 兼容）**：通过标准协议字段启用。  
  - [OpenAI 兼容接口](openai-compatible-interface.md)：在 `tools` 数组中定义函数 schema，响应中返回 `tool_calls` 字段；  
  - Anthropic Messages 接口：使用 `tool_use` 块和 `tool_result` 交互，支持多工具并行调用与嵌套思考。  
  所有协议均要求模型具备函数调用能力（如 `qwen4-max`、`qwen3.8-omni-flash`），不支持的模型（如部分轻量版 `flash` 模型）将忽略 `tools` 参数。

- **Flow Agent 编排**：在可视化流程中，“工具调用”节点直接映射为函数调用能力。开发者可配置输入参数映射、失败重试策略及结果分支路由，无需编码即可组合多个工具形成业务工作流（如“先查库存 → 再调支付 → 最后发通知”）。

- **Sandbox 自定义 Agent**：在 Python 沙箱中，可通过 `bailian.tool_call()` 辅助函数触发平台托管的工具调用，或直接调用 `requests` 调用自有服务——但后者不享受平台的统一鉴权、限流、重试与可观测性保障，推荐优先使用平台原生函数调用。

## 关键参数和配置

- `tools`: **必填数组**，定义可用工具的 JSON Schema 列表。每个元素包含 `type: "function"`、`function.name`（唯一标识）、`function.description`（供模型理解用途）及 `function.parameters`（JSON Schema 格式）。示例：
  ```json
  {
    "type": "function",
    "function": {
      "name": "work_wechat_send_message",
      "description": "向企业微信指定成员发送文本消息",
      "parameters": {
        "type": "object",
        "properties": {
          "user_id": {"type": "string", "description": "接收人UserID"},
          "content": {"type": "string", "description": "消息文本"}
        },
        "required": ["user_id", "content"]
      }
    }
  }
  ```

- `tool_choice`: **可选字符串或对象**，控制调用策略：  
  - `"auto"`（默认）：由模型自主决定是否调用及调用哪个工具；  
  - `"none"`：禁用函数调用，强制模型仅生成文本回复；  
  - `{"type": "function", "function": {"name": "xxx"}}`：强制指定调用某工具（适用于确定性流程）。

- `parallel_tool_calls`: **布尔值，默认 `true`**（仅 Anthropic Messages 协议支持）。设为 `true` 时允许模型一次性生成多个 `tool_use` 块，并行执行；设为 `false` 则串行调用。

- 注意事项：  
  - 工具名（`function.name`）必须与平台注册的 Skill 或预置工具 ID 完全一致，大小写敏感；  
  - `tools` 中定义的参数 schema 必须与实际工具接口签名严格匹配，否则调用失败；  
  - 函数调用不计入 `max_tokens` 限制，但 `tool_calls` 响应内容会占用输出 token 预算。

## 面向开发者：简洁实用提示

- ✅ **快速验证**：用 `qwen4-max` + 最简 `tools` 定义发起一次 `/v1/chat/completions` 请求，检查响应中是否含 `tool_calls` 字段及正确 `name`/`arguments`。  
- ✅ **调试必开**：在 Managed Agents 或 Flow Agent 中启用 `X-Bailian-Debug: true` 或 `enable_tracing: true`，查看完整调用链日志（含工具输入/输出、耗时、错误堆栈）。  
- ⚠️ **避免常见错误**：  
  - 不要将工具逻辑写在 `system` prompt 中——模型无法执行 prompt 里的伪代码；  
  - 不要省略 `tools` 中的 `required` 字段——缺失必填参数会导致调用被拒绝；  
  - 不要在 Sandbox 中重复实现已由平台托管的工具（如 `work_wechat_send_message`）——直接调用更安全、可监控。  
- 🚀 **进阶建议**：对高并发场景，将高频工具封装为 Skill 并绑定独立 `Environment`，实现资源隔离与独立扩缩容。

## 关联主题页

- [application use cases](../guides/application-use-cases.md)
- [managed agents api](../api/managed-agents-api.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [agent development](../guides/agent-development.md)


