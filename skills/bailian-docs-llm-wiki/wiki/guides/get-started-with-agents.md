# get started with agents

Agent 是百炼平台提供的可编程智能体服务，支持开发者快速构建具备规划、工具调用和多轮推理能力的应用。本文档指导你完成 Agent 的初始化配置、核心参数设置及基础调用流程。所有操作均基于百炼 API v3 接口，需配合有效的 API Key 和模型授权。

## 支持的模型与功能

当前 Agent 服务仅支持 `qwen-plus` 和 `qwen-max` 两款模型（详见 [开始使用](../../raw/application-user-guide/get-started-with-agents.md)）。不支持 `qwen-turbo` 或历史版本如 `qwen-1.5-72b`。Agent 内置以下关键能力：  
- 自动工具选择（Tool Calling）  
- 多步任务分解与执行（Plan-and-Execute）  
- 基于用户输入动态生成[函数调用](../concepts/function-calling.md)参数  
- 支持自定义工具 Schema（OpenAPI 格式）

> **注意**：[Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 中提及的 “支持 qwen-2.5 系列” 属于过时描述，实际尚未上线，以控制台模型列表和 [开始使用](../../raw/application-user-guide/get-started-with-agents.md) 中声明为准。

## 关键参数

调用 Agent 接口时，必须传入以下参数：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 固定为 `qwen-plus` 或 `qwen-max`，不可省略 |
| `tools` | array | 否（但无工具则退化为普通 LLM 调用） | 工具定义数组，每个元素需含 `function.name`、`function.description` 和 `function.parameters`（JSON Schema） |
| `tool_choice` | string \| object | 否 | 可选 `"auto"`（默认）、`"none"` 或指定工具名；若设为对象，格式为 `{"type": "function", "function": {"name": "xxx"}}` |

注意：`temperature`、`top_p` 等采样参数在 Agent 模式下**被忽略**，由内部策略统一控制——该行为在 [开始使用](../../raw/application-user-guide/get-started-with-agents.md) 中有明确说明。

## 使用方式

1. **准备工具定义**：按 OpenAPI 3.0 规范编写 JSON Schema，确保 `parameters` 字段为合法 JSON Schema 对象（非字符串）；  
2. **构造请求体**：将工具数组传入 `tools` 字段，用户消息置于 `messages` 数组末尾；  
3. **发起 POST 请求**：目标 URL 为 `https://dashscope.aliyuncs.com/api/v1/agents`，Header 需包含 `Authorization: Bearer <api_key>`；  
4. **解析响应**：若返回 `finish_reason: "tool_calls"`，需提取 `message.tool_calls` 并同步执行对应工具，再将结果作为 `tool_message` 提交下一轮；循环直至 `finish_reason: "stop"`。

## 限制和注意事项

- 单次请求最大 token 数为 32768（含输入 + 输出），超出将触发 `400 Bad Request`；  
- 工具调用深度限制为 8 层（即最多连续 8 次 tool_call → tool_message → agent response）；  
- 不支持流式响应（`stream: true` 将被静默忽略）；  
- 所有工具函数必须为幂等设计，Agent 不保证调用顺序或重试语义；  
- 若工具返回非 JSON 或结构与 `parameters` 定义严重不符，Agent 将终止执行并返回错误码 `TOOL_EXECUTION_FAILED`。

## 来源文档

- [开始使用](../../raw/application-user-guide/get-started-with-agents.md)


