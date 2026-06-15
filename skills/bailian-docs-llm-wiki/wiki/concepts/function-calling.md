# 函数调用与工具集成

函数调用（Function Calling）是大模型与外部工具交互的核心机制，允许模型在推理过程中识别用户意图并主动调用预定义的函数或工具，从而突破纯文本生成的局限，实现实时数据获取、精确计算、外部系统操作等能力。在百炼平台中，函数调用贯穿于插件、MCP 服务、智能体应用等多个场景，是构建 AI 应用的关键基础设施。

## 基本原理

函数调用的核心流程为：

1. 开发者在请求中通过 `tools` 参数声明可用工具的名称、描述和参数 schema
2. 模型根据用户输入和工具描述，判断是否需要调用工具，并生成结构化的调用参数
3. 应用侧执行实际的函数调用，将结果返回给模型
4. 模型结合函数返回结果生成最终回复

百炼平台支持单次调用多个工具（最多 10 个），模型会根据输入自动选择调用一个或多个。

## 在百炼平台的使用场景

### 通过 Chat Completions API 直接调用

所有通义千问通用模型均支持 Function Calling。开发者在 `tools` 参数中定义工具的 JSON Schema，模型返回 `tool_calls` 字段指示需要调用的函数及参数。推荐使用 `qwen3.7-plus` 起步，它在能力与成本之间取得平衡。

### 通过插件系统调用

百炼的插件本质上是对 Function Calling 的封装。插件包含一个或多个工具，每个工具对应一个 API 端点。支持三种调用方式：

- **智能体应用**：模型根据用户输入自动判断是否调用插件工具
- **工作流应用**：将插件作为工作流节点按编排顺序执行
- **Assistant API**：通过 `tools` 参数指定工具 ID 进行调用

官方插件（如代码解释器 `code_interpreter`、夸克搜索 `quark_search`、计算器 `calculator` 等）开箱即用；自定义插件可接入任意 API。

### 通过 MCP 协议调用

MCP（模型上下文协议）是函数调用的标准化扩展。通过 MCP，开发者无需为每个工具单独编写接口，即可在智能体和工作流中接入大量第三方工具。MCP 服务可在智能体应用中由模型自主判断调用（最多同时添加 5 个），也可在工作流中作为节点手动指定。

### 通过 Responses API 调用

Responses API 是 Chat Completions API 的演进版本，提供了内置工具（联网搜索、代码解释器等），无需开发者自行实现 Function Calling 的完整流程，简化了工具集成的开发体验。

## 关键参数与配置

### tools 参数

在 API 调用中声明可用工具：

```json
{
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "获取指定城市的天气信息",
        "parameters": {
          "type": "object",
          "properties": {
            "city": { "type": "string", "description": "城市名称" }
          },
          "required": ["city"]
        }
      }
    }
  ]
}
```

### 自定义插件配置要点

- **插件 URL**：API 的访问域名（同一插件下的工具共享）
- **工具路径**：相对于插件 URL 的 API 路径
- **鉴权配置**：支持服务级和用户级鉴权，Token 可放在 Header 或 Query 中
- **输入参数**：支持"大模型识别"（从用户输入提取）和"业务透传"（外部主动传入）两种传参方式
- **输出参数**：定义 API 返回的数据结构，模型据此筛选和组合结果

### 相关模型参数

| 参数 | 说明 |
|------|------|
| `enable_thinking` | 开启思考模式，提升复杂工具调用场景的规划能力 |
| `temperature` | 控制输出随机性，工具调用场景建议使用较低值 |
| ReAct 最大轮次 | 智能体应用中限制单次会话的工具调用次数（1-50） |

## 支持的模型

| 模型 | Function Calling | 内置工具 | 结构化输出 |
|------|-----------------|----------|-----------|
| `qwen3.7-max` | 支持 | 支持 | 不支持 |
| `qwen3.7-plus` | 支持 | 支持 | 支持 |
| `qwen3.6-flash` | 支持 | 支持 | 支持 |
| `qwen-max` | 支持 | - | - |
| `qwen-plus` | 支持 | - | - |
| `qwen-turbo` | 支持 | - | - |

## 注意事项

- 工具调用会增加 Token 消耗：工具描述和返回结果均计入上下文
- 智能体调用工具依赖提示词质量，需在提示词中明确工具名称和能力描述
- 自定义插件的超时限制为 5 秒
- 工具创建后需在线调试通过并发布，只有"已发布"状态的工具才能被调用
- Function Calling 不等同于联网搜索；夸克搜索插件是模型直接调用插件执行搜索，而 `enable_search` 参数是模型尝试利用互联网信息丰富生成内容

## 关联主题页

- [plug in](../guides/plug-in.md)
- [model context protocol](../guides/model-context-protocol.md)
- [llm application](../guides/llm-application.md)
- [model inference](../guides/model-inference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


