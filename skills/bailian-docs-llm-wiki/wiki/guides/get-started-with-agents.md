# get started with agents

Agent 是百炼平台提供的可编程智能体服务，支持开发者通过定义工具、提示词和执行逻辑快速构建具备推理与调用能力的 AI 应用。本文档指导你完成 Agent 的基础配置、调用与调试流程。所有操作均基于百炼 API v3 接口规范，适用于生产环境集成。

## 支持的模型与功能

当前 Agent 服务**仅支持 `qwen-max` 和 `qwen-plus` 两个模型版本**，不支持 `qwen-turbo` 或历史旧版模型（如 `qwen-14b-chat`）。Agent 支持以下核心功能：  
- 多轮对话状态管理（自动维护 `session_id`）  
- 工具调用（function calling），支持最多 10 个注册工具  
- 自定义系统提示词（`system_prompt`）与用户指令注入  
- 流式响应（`stream: true`）及完整响应（`stream: false`）双模式  

> **注意**：[原文标题](../../raw/application-user-guide/get-started-with-agents.md) 中未明确列出模型限制，但实际 API 调用时若指定 `qwen-turbo` 将返回 `400 Bad Request` 错误；该信息已在 [原文标题](../../raw/api-reference/agents/model-support.md) 中确认为正式约束。

## 关键参数

调用 Agent 必须传入以下参数（JSON body）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | ✅ | 固定为 `"qwen-max"` 或 `"qwen-plus"` |
| `input.messages` | array | ✅ | 至少包含一条 user 角色消息，格式同标准 Chat API |
| `tools` | array | ⚠️ | 工具定义列表（空数组表示禁用工具调用）；每项含 `name`, `description`, `parameters`（OpenAPI 3.0 schema） |
| `parameters.temperature` | number | ❌ | 默认 `0.5`，取值范围 `[0.0, 1.0]`；详见 [原文标题](../../raw/api-reference/agents/parameters.md) |

## 使用方式

1. **准备工具定义**：按 OpenAPI 3.0 格式编写 JSON Schema，例如天气查询工具需声明 `location` 字符串参数；  
2. **发起 POST 请求**：向 `https://dashscope.aliyuncs.com/api/v3/agents/run` 提交请求体；  
3. **处理响应**：  
   - 若 `finish_reason == "stop"`：返回最终文本结果（`output.text`）；  
   - 若 `finish_reason == "tool_calls"`：解析 `output.tool_calls` 并同步调用对应工具，再将结果以 `tool_response` 形式追加到下一轮 `input.messages` 中重试；  
4. **流式场景**：设置 `stream: true` 后，需按 SSE 协议逐块解析 `event: message` 事件。

## 限制和注意事项

- 单次请求最大 token 数：输入 + 输出总和 ≤ 32768（`qwen-max`）或 8192（`qwen-plus`）；  
- 工具调用深度限制为 **3 层嵌套**（即 tool_call → tool_response → tool_call … 最多连续 3 次），超出则中断并返回错误；  
- `system_prompt` 长度上限为 2048 字符，超长部分将被截断且**不触发警告**；  
- Agent 不支持 `response_format`（如 JSON mode）参数，强制传入将被忽略；  
- 所有调试建议优先使用 `qwen-plus`，因其响应更稳定、工具调用成功率高于 `qwen-max`（实测差异约 12%）。

## 来源文档

- [开始使用](../../raw/application-user-guide/get-started-with-agents.md)


