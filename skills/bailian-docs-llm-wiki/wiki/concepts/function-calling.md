# 函数调用

函数调用（Function Calling）是大模型与外部工具交互的核心机制，允许模型在对话过程中识别用户意图并主动调用预定义的函数或工具，从而获取实时数据、执行计算或触发外部操作。

## 工作原理

函数调用的基本流程为：

1. 开发者在请求中定义可用工具（函数名称、描述、参数 schema）
2. 模型根据用户输入判断是否需要调用工具
3. 若需调用，模型输出结构化的函数名和参数
4. 应用执行函数并将结果返回模型
5. 模型结合函数返回结果生成最终回复

## 在百炼平台的使用场景

### OpenAI 兼容 Chat Completions 接口

通过标准的 `tools` 参数定义可用函数，模型会在 `tool_calls` 字段中返回调用请求。支持 Qwen 系列全部商业版和开源版模型。开发者需在请求体中声明函数的 JSON Schema，并在收到 `tool_calls` 后自行执行函数、将结果以 `tool` 角色消息回传。

### Anthropic 兼容 Messages 接口

百炼的 Anthropic 兼容接口同样支持工具调用，协议与 Anthropic 官方一致，适合从 Anthropic 生态迁移的开发者。

### 实时[多模态](multimodal.md)交互（Omni Realtime API）

在 WebSocket 长连接的实时对话中，函数调用以事件驱动方式运行。模型通过服务端事件返回工具调用请求，客户端执行后通过 `conversation.item.create`（role 为 tool）回传结果，再发送 `response.create` 触发模型继续生成。适用于语音对话中需要查询外部数据的场景。

### 智能体应用

智能体（Agent 2.0）将函数调用能力封装为自动化的工具调度。开发者只需在控制台配置插件或 MCP 服务，智能体会自主规划调用顺序，以 ReAct 模式循环执行"规划-调用-反思"直至完成任务。单次会话最多支持 50 轮工具调用。

### 工作流应用

在工作流中，函数调用以节点形式出现。每个工具节点需手动指定输入参数，输出结果传递到下一个节点，适合固定流程的自动化场景。

## 关键参数与配置

| 参数 | 说明 | 适用接口 |
| --- | --- | --- |
| `tools` | 工具定义数组，每个元素包含 `type`、`function`（含 `name`、`description`、`parameters`） | Chat Completions、DashScope |
| `tool_choice` | 控制模型是否调用工具：`auto`（模型自行判断）、`none`（禁止调用）、指定函数名（强制调用） | Chat Completions |
| `parallel_tool_calls` | 是否允许模型一次返回多个工具调用 | Chat Completions |

### 函数定义示例结构

```json
{
  "type": "function",
  "function": {
    "name": "get_weather",
    "description": "查询指定城市的天气信息",
    "parameters": {
      "type": "object",
      "properties": {
        "city": { "type": "string", "description": "城市名称" }
      },
      "required": ["city"]
    }
  }
}
```

## 与插件和 MCP 的关系

- **插件**：百炼插件本质上是对函数调用的封装。官方插件和自定义插件通过平台预定义好工具 schema，开发者无需手动编写函数定义。
- **MCP 服务**：Model Context Protocol 在协议层标准化了工具的发现与调用流程，使模型能通过统一接口访问海量第三方工具，底层仍依赖函数调用机制驱动。

## 限制和注意事项

- 函数调用会增加 [Token](token.md) 消耗：工具定义和返回结果均计入上下文长度
- 模型对工具的选择准确性依赖函数描述的清晰度，建议用自然语言准确描述函数用途和参数含义
- 不同模型对函数调用的支持程度不同，推荐使用 qwen-plus、qwen-max 等具备强工具调用能力的模型
- 实时交互场景中，工具调用的响应延迟会直接影响对话流畅度，建议优化外部函数的执行速度

## 关联主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [plug in](../guides/plug-in.md)
- [model context protocol](../guides/model-context-protocol.md)
- [llm application](../guides/llm-application.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


