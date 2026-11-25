# 函数调用

函数调用（Function Calling）是百炼平台中大模型主动识别用户意图、生成结构化[工具调用](tool-calling.md)请求，并协同外部系统执行具体操作的核心能力。它使模型不再仅输出文本，而是可按需触发计算器、搜索、代码执行、图像生成等真实服务，实现“思考→决策→行动”的闭环。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台中并非通用能力，而是**严格绑定于特定模型与调用路径**，主要应用于以下三类场景：

- **标准聊天接口（`/v1/chat/completions`）**：  
  仅 `qwen-max` 和 `qwen-plus` 支持。开发者需在请求中传入 `tools` 数组（定义可用函数），并设置 `tool_choice`（如 `"auto"` 或指定 `{"type": "function", "function": {"name": "calculator"}}`）。模型将返回 `tool_calls` 字段（含 `function.name` 和 `function.arguments`），而非纯文本响应。客户端需解析该结构、调用对应工具、再将结果以 `role: "tool"` 消息回传，完成多轮协作。

- **插件（Plug-in）集成场景**：  
  插件本质即标准化的函数封装。官方插件（如 `calculator`、`code_interpreter`）、三方插件及自定义 MCP 插件，均通过 `tools` 参数注入到 `qwen-plus`/`qwen-max` 请求中。智能体应用中由模型自主决策调用；工作流应用中则作为显式编排节点，不依赖模型推理触发。

- **专用意图理解模型（`tongyi-intent-detect-v3`）**：  
  该模型专为低延迟、高精度意图识别与函数路由设计。它不直接执行工具，但可快速解析用户输入，输出标准化的 `<intent>` 标签结构（含 `tool_name`、`parameters` 等），供业务系统直接调度后端服务，适用于对话路由、客服工单分发等强确定性场景。

> ⚠️ 注意：`qwen-turbo`、`qwen-vl-plus`、`qwen-mt-plus`、`gui-plus` 等所有其他模型**均不支持函数调用能力**。OCR、ASR、TTS、文生图等专用模型需通过独立 API 调用，不可嵌入 `tools` 流程。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `tools` | array | 是（启用函数调用时） | 工具定义列表，每个元素为 OpenAI 兼容格式对象，含 `function.name`（字符串，≤20字符）、`function.description`、`function.parameters`（JSON Schema） | `[{"function": {"name": "calculator", "description": "执行数学计算", "parameters": {"type": "object", "properties": {"expression": {"type": "string"}}}}}]` |
| `tool_choice` | string / object | 否 | 控制调用策略：<br>• `"none"`：禁用函数调用（默认）<br>• `"auto"`：由模型自主决定是否调用<br>• `{"type": "function", "function": {"name": "xxx"}}`：强制调用指定函数 | `"auto"` |
| `tool_choice`（意图模型） | string | 是（调用 `tongyi-intent-detect-v3` 时） | 固定为 `"required"`，且需在 `system` 消息中声明 `Response in INTENT_MODE.` | `"required"` |
| `messages.role` | string | 是 | 函数调用流程中必须包含 `role: "tool"` 的消息，用于回传工具执行结果；`content` 为 JSON 字符串或 `null`（失败时） | `{"role": "tool", "tool_call_id": "call_abc123", "content": "{\"result\": 42}"}"` |

- **工具 ID 与鉴权**：自定义插件需配置 `tool_id` 及 Header/Query 鉴权（如 `Authorization: Bearer xxx`），该信息不参与模型推理，仅由客户端在调用工具时透传。
- **参数校验**：`function.parameters` 必须为合法 JSON Schema；`Object` 类型参数的子属性不可为空，否则发布失败。
- **安全要求**：函数调用本身不改变鉴权方式，仍依赖 API Key 或临时 [Token](token.md)；但工具后端服务需自行实现鉴权与风控。

## 面向开发者，简洁实用

- ✅ **快速验证**：用 CLI 一行命令测试函数调用是否生效：  
  ```bash
  bailian chat --model qwen-plus \
    --message "计算 123*456" \
    --tools '[{"function":{"name":"calculator","description":"执行数学计算","parameters":{"type":"object","properties":{"expression":{"type":"string"}}}}}]' \
    --tool-choice auto
  ```

- ✅ **必做检查项**：  
  - 确认模型为 `qwen-plus` 或 `qwen-max`；  
  - `tools` 中每个 `function.name` 唯一且符合命名规范（小写字母+下划线，≤20字符）；  
  - `function.parameters` 使用标准 JSON Schema，避免 `required: []` 等无效写法；  
  - 工具执行结果必须原样、无修改地以 `role: "tool"` 消息回传，`tool_call_id` 必须与模型返回值完全一致。

- ❌ **常见错误**：  
  - 对 `qwen-turbo` 传 `tools` → 返回 `400 Bad Request`（模型不支持）；  
  - `function.parameters` 缺少 `type` 字段 → 模型无法解析参数，可能静默忽略工具；  
  - 工具返回非 JSON 字符串（如带中文引号）→ 解析失败，导致后续对话中断。

函数调用是构建生产级智能体的关键跃迁点。从定义清晰的工具 Schema 开始，逐步接入真实服务，即可让大模型真正“动起来”。

## 关联主题页

- [getting started](../guides/getting-started.md)
- [more about models](../api/more-about-models.md)
- [plug in](../guides/plug-in.md)
- [more models](../api/more-models.md)


