# 函数调用

函数调用（Function Calling）是百炼平台支持的一种结构化工具编排能力，允许模型在生成响应前主动识别用户意图、选择并填充预定义工具（如搜索、计算、数据库查询等）的参数，返回标准化的 `tool_calls` 指令而非自由文本。该机制是构建可靠 Agent、实现可控自动化任务的核心基础。

## 在百炼平台的不同场景中，这个概念如何使用

- **通用文本模型（Qwen 系列）**：通过 OpenAI 兼容 `/v1/chat/completions` 或百炼原生接口，传入 `tools` 数组与 `tool_choice` 策略（如 `"auto"`、`"required"` 或指定工具名），模型将输出 `{"tool_calls": [...]}` 结构；开发者需自行解析、执行工具，并将结果以 `tool` 角色消息回传构成完整对话链。
- **意图理解专用模型（`tongyi-intent-detect-v3`）**：专为毫秒级函数调用生成优化，适用于对话路由与轻量工具编排；推荐在 `system` 消息中声明 `Response in INTENT_MODE.` 并提供精简工具 Schema，可显著提升识别准确率与响应速度。
- **Agent 构建推荐入口（`/responses` 接口）**：内置联网搜索、代码解释器、知识库检索等工具，无需手动定义 `tools`；模型自动决策是否调用及调用哪个工具，返回结构化 `response.tool_calls` 与自动串联的 `previous_response_id`，大幅降低 Agent 工程复杂度。
- **GUI 自动化模型（`gui-plus`）**：支持 `computer_use` 类工具调用，结合界面截图理解用户操作意图（如“点击登录按钮”），生成带坐标的鼠标/键盘指令；需在 `tools` 中明确定义 `computer_use` 的 JSON Schema。
- **注意事项**：  
  - `qwen-deep-research`、`WanX`、`Tongyi Tingwu` 等非文本生成类模型**不支持函数调用**；  
  - 三方模型（如通过 OpenAI 兼容协议接入的外部模型）**不支持百炼原生 `function_call` 语义**，需自行实现解析逻辑；  
  - 非标准 JSON Schema 格式的 `tools` 定义会被静默忽略——务必校验 `type`、`properties`、`required` 字段符合 OpenAPI 3.0 子集规范。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `tools` | array of objects | 否（启用函数调用时必填） | 工具数组，每个对象需含 `type: "function"`、`function.name`、`function.description` 和符合 JSON Schema 的 `function.parameters`（仅支持 `string`/`number`/`boolean`/`object`/`array` 基础类型及 `required` 字段） |
| `tool_choice` | string or object | 否 | 控制调用策略：<br>• `"auto"`（默认）：模型自主决定是否及调用哪个工具；<br>• `"none"`：禁止调用任何工具；<br>• `"required"`：必须调用至少一个工具；<br>• `{"type": "function", "function": {"name": "xxx"}}`：强制调用指定工具 |
| `response_format` | object | 否 | 当设为 `{"type": "json_object"}` 时，可与函数调用协同使用，确保最终响应为合法 JSON（适用于需强结构化输出的场景） |

> ⚠️ 注意：`tools` 中的 `function.parameters` **不支持 `null` 类型、`anyOf`/`oneOf` 多态定义、或嵌套过深的 `additionalProperties`**；建议使用 [JSON Schema Validator](https://json-schema-validator.herokuapp.com/) 提前校验。

## 面向开发者，简洁实用

- ✅ **快速验证**：用 CLI 调用带工具的 Qwen 模型：
  ```bash
  bailian chat \
    --model qwen-turbo \
    --message "查一下今天北京的天气" \
    --tools '[{"type":"function","function":{"name":"get_weather","description":"获取指定城市天气","parameters":{"type":"object","properties":{"city":{"type":"string","description":"城市名"}},"required":["city"]}}}]' \
    --tool-choice auto
  ```
- ✅ **SDK 最佳实践（Python）**：  
  使用 DashScope SDK 时，`tools` 和 `tool_choice` 直接作为参数传入；解析响应时优先检查 `response.output.choices[0].message.tool_calls`，而非 `content`：
  ```python
  from dashscope import Generation
  response = Generation.call(
      model='qwen-max',
      messages=[{'role': 'user', 'content': '帮我订一张明天从北京到上海的高铁票'}],
      tools=TOOLS_SCHEMA,
      tool_choice='auto'
  )
  if hasattr(response.output.choices[0].message, 'tool_calls'):
      for call in response.output.choices[0].message.tool_calls:
          # 执行 call.function.name，填充 call.function.arguments
          pass
  ```
- ✅ **避坑提示**：  
  - 工具名（`function.name`）区分大小写，且不能含空格或特殊字符；  
  - `tool_choice="required"` 时若模型无法匹配任何工具，将返回 `400 Bad Request`；  
  - 流式响应（`stream=true`）下，`tool_calls` 仅在最后一个 `data:` chunk 中完整返回，中间 chunk 的 `delta` 可能为空或含部分字段——请按 `finish_reason == "tool_calls"` 判断结束。

## 关联主题页

- [getting started](../guides/getting-started.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [more models](../api/more-models.md)
- [application support](../guides/application-support.md)
- [use cases](../guides/use-cases.md)


