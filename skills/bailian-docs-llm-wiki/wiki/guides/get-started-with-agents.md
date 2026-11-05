# get started with agents

Agent 是百炼平台提供的可编程智能体服务，支持开发者快速构建具备规划、工具调用和多轮推理能力的应用。本文档指导你完成 Agent 的初始化配置、核心参数设置及基础调用流程。所有操作均基于百炼 API v3 接口，需配合有效的 API Key 和模型授权。

## 支持的模型与功能

当前 Agent 服务仅支持 `qwen-plus` 和 `qwen-max` 两款模型（详见 [开始使用](../../raw/application-user-guide/get-started-with-agents.md)）。不支持 `qwen-turbo` 或历史版本如 `qwen-1.5-72b`。Agent 内置以下关键能力：  
- 自动工具选择（Tool Calling）  
- 多步任务分解与执行（Plan-and-Execute）  
- 基于用户输入动态生成[函数调用](../concepts/function-calling.md)参数  
- 支持自定义工具 Schema（OpenAPI 格式）

> **注意**：原始文档中提及的 “支持所有 Qwen 系列模型” 已过时；实际可用模型以控制台「Agent 配置页」实时列表为准，该限制在 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 中有明确说明。

## 关键参数

调用 Agent 必须传入以下参数（JSON body）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 仅限 `qwen-plus` 或 `qwen-max`，大小写敏感 |
| `input` | object | 是 | 包含 `messages`（对话历史数组）和可选 `tools`（工具列表） |
| `tools` | array | 否 | 工具定义数组，每个元素需含 `function.name`、`function.description` 和 `function.parameters`（JSON Schema） |
| `stream` | boolean | 否 | 设为 `true` 可启用流式响应（仅支持 SSE） |

注意：`input.messages` 中首条消息必须为 `role: "user"`，且 `content` 字段不可为空字符串——该约束在 [开始使用](../../raw/application-user-guide/get-started-with-agents.md) 中未明确强调，但实测会返回 `400 Bad Request`。

## 使用方式

1. **准备工具定义**：按 OpenAPI 3.0 规范编写工具 Schema，确保 `parameters` 为合法 JSON Schema（非 Swagger 2.0）；  
2. **构造请求体**：将工具列表嵌入 `input.tools`，对话历史放入 `input.messages`；  
3. **发起 POST 请求**：目标 URL 为 `https://dashscope.aliyuncs.com/api/v3/agents`，Header 中携带 `Authorization: Bearer <api_key>`；  
4. **处理响应**：成功时返回 `output.choices[0].message`，其中可能包含 `tool_calls` 数组或最终文本回复。

完整示例见 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 中的「快速调用示例」章节。

## 限制和注意事项

- 单次请求最大 token 数为 32768（含 [prompt](prompt.md) + tools + response），超出将触发截断并返回警告字段 `truncated: true`；  
- 工具调用深度限制为 8 层（即最多连续 8 次 tool_call → observation → LLM 回应循环）；  
- 不支持上传文件或图像作为输入；所有 `input.messages` 中的 `content` 必须为纯文本或结构化 JSON（无 base64 编码）；  
- 流式响应（`stream: true`）下，`tool_calls` 事件仅在 final message 中完整返回，中间 chunk 不含 `delta.tool_calls` 字段——此行为与常规 chat 接口不同，已在 [开始使用](../../raw/application-user-guide/get-started-with-agents.md) 的附注中确认。

## 来源文档

- [开始使用](../../raw/application-user-guide/get-started-with-agents.md)


