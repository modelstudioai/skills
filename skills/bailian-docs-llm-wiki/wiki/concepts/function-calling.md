# 函数调用

函数调用（Function Calling）是百炼平台支持的一种结构化工具交互能力，允许大模型在推理过程中主动识别用户意图、生成符合预定义 Schema 的函数调用请求（而非自由文本），由系统或开发者执行对应工具后，将结果注入上下文继续推理。该机制是构建可靠智能体（Agent）的核心基础设施。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台中并非单一接口功能，而是贯穿多个协议与模型的能力范式，具体体现为：

- **OpenAI 兼容 Chat API**：通过 `tools` 数组声明可用函数（JSON Schema 格式），设置 `tool_choice` 控制调用策略（`auto`/`required`/指定函数名）。模型返回 `tool_calls` 字段，含 `function.name` 和 `function.arguments`（字符串，需 `json.loads` 解析）。适用于 `qwen4-max`、`qwen3.8-max` 等主流文本模型。
  
- **OpenAI 兼容 Responses API**：作为专为 Agent 设计的增强协议，原生集成联网搜索、网页抽取、代码解释器等内置工具链。无需手动定义 `tools`，只需启用对应能力（如 `enable_web_search=true`），系统自动调度并注入结果；同时支持传入自定义 `tools`，行为与 Chat API 一致，但上下文管理更鲁棒（通过 `previous_response_id` 自动续写）。

- **Anthropic 兼容 Messages API**：使用 `tool_use` 内容块（`type: "tool_use"`）表达调用意图，配合 `tool_result` 块注入执行结果。需在 `system` 或首条 `user` 消息中提供 `<tools>` XML 定义，适用于 `qwen4-max`、`qwen3.8-max` 等支持 Anthropic 协议的模型。

- **DashScope 原生 API**：通过 `functions` 参数（非 OpenAI 风格的 `tools`）声明函数列表，模型返回 `function_call` 字段（含 `name` 和 `arguments` 字符串）。这是最底层、兼容性最广的方式，**唯一支持 `qwen-audio` 等多模态模型的函数调用路径**。

- **意图理解专用模型（`tongyi-intent-detect-v3`）**：以轻量级、确定性方式实现“伪函数调用”——通过系统提示 `Response in INTENT_MODE.` 触发，模型直接输出标准 JSON 格式的 `intent` 和 `parameters`，无需解析 `arguments` 字符串，毫秒级响应，适合高并发路由场景。

> ✅ 提示：所有协议下，函数调用均依赖模型对 Schema 的理解能力，建议使用 `qwen4-max` 或 `qwen3.8-max` 等高阶模型以获得最佳准确率；低阶模型（如 `qwen-plus`）可能忽略 `tool_choice` 或返回格式错误。

## 关键参数和配置

| 参数 | 所属协议 | 说明 | 注意事项 |
|------|----------|------|----------|
| `tools` / `functions` | OpenAI Chat / DashScope | 必填数组，每个元素为 JSON Schema 描述的函数（含 `name`, `description`, `parameters`） | `parameters` 必须是合法 JSON Schema（支持 `string`/`number`/`boolean`/`object`/`array`），不支持 `null` 类型；`required` 字段必须显式声明 |
| `tool_choice` | OpenAI Chat | 控制调用策略：`"auto"`（默认，由模型决定）、`"none"`（禁用）、`{"type": "function", "function": {"name": "xxx"}}`（强制调用指定函数） | 若设为 `required` 但模型无法匹配任何工具，将返回 `400 Bad Request` |
| `enable_web_search`, `enable_code_interpreter` 等 | Responses API | 布尔型开关，启用内置工具链 | 启用后无需定义 `tools`，系统自动注入工具描述与结果；计费按实际调用次数叠加 |
| `functions`（DashScope 原生） | DashScope | 同 `tools`，但字段名与解析逻辑为 DashScope 专属 | 仅 DashScope SDK 支持；Python 中通过 `Generation.call(..., functions=[...])` 传入 |
| `system` 消息内容 | Anthropic / DashScope / Chat | 在 Anthropic 中为顶层字段；在 Chat/DashScope 中为 `messages[0]` 的 `role: system` | Anthropic 协议下，`<tools>` 必须放在 `system` 中且格式严格（XML 标签闭合、无换行）；Chat 协议下，`system` 仅作提示，不参与工具定义 |

- **安全配置**：函数调用本身不涉及认证，但**执行阶段的工具（如 HTTP 请求、数据库查询）必须由开发者自行鉴权与沙箱隔离**。百炼平台仅负责生成调用请求，不执行任何外部操作。
- **流式响应**：函数调用请求（`tool_calls` / `tool_use`）总在首次响应中完整返回，**不支持流式生成 `arguments`**；后续 `tool_result` 或 `function_call` 结果需通过二次请求注入。

## 面向开发者，简洁实用

- ✅ **快速上手（OpenAI Chat）**：
  ```python
  from openai import OpenAI
  client = OpenAI(base_url="https://YOUR-WORKSPACE.cn-beijing.maas.aliyuncs.com/compatible-mode/v1", api_key="YOUR_KEY")
  
  tools = [{
      "type": "function",
      "function": {
          "name": "get_weather",
          "description": "获取指定城市的实时天气",
          "parameters": {
              "type": "object",
              "properties": {"city": {"type": "string", "description": "城市名称"}},
              "required": ["city"]
          }
      }
  }]
  
  response = client.chat.completions.create(
      model="qwen4-max",
      messages=[{"role": "user", "content": "北京今天热吗？"}],
      tools=tools,
      tool_choice="auto"  # 或 "required"
  )
  
  # 解析调用
  if response.choices[0].message.tool_calls:
      call = response.choices[0].message.tool_calls[0]
      city = json.loads(call.function.arguments)["city"]  # 执行你的 get_weather(city)
  ```

- ⚠️ **避坑指南**：
  - 不要将敏感参数（如 API Key、数据库密码）写在 `tools` 的 `parameters` Schema 中——Schema 是明文透出给模型的；
  - `arguments` 是字符串，务必 `json.loads()` 解析，切勿用 `eval()`；
  - 使用 Responses API 时，若需自定义工具，仍需传 `tools`，但 `tool_choice` 行为与 Chat API 一致；
  - DashScope 原生调用 `qwen-audio` 时，`functions` 是唯一支持函数调用的方式，OpenAI 兼容协议不适用。

- 📌 **调试建议**：
  - 开启 `stream=True` 可观察模型是否进入工具调用分支（首个 `delta` 中含 `tool_calls`）；
  - 检查响应中的 `finish_reason`：`"tool_calls"` 表示成功触发，`"stop"` 表示未调用；
  - 对于意图识别模型，直接检查返回 JSON 的 `intent` 字段，无需解析 `arguments`。

## 关联主题页

- [preparations](../api/preparations.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [more about models](../api/more-about-models.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [more models](../api/more-models.md)


