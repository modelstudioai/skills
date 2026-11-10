# qwen api reference

Qwen 系列大语言模型通过百炼平台提供多种 API 接口，支持文本生成、多轮对话、[工具调用](../concepts/tool-calling.md)等核心能力。开发者可根据技术栈偏好和功能需求选择 OpenAI 兼容、Anthropic 兼容或百炼原生 DashScope 接口。所有接口均需通过 API Key 认证，并遵循统一的配额与计费规则。

## 支持的模型/功能

当前支持的 Qwen 模型包括 `qwen-max`（旗舰版）、`qwen-plus`（均衡版）和 `qwen-turbo`（轻量版），覆盖高精度推理、中长上下文处理及低延迟响应场景。各接口支持的功能略有差异：
- OpenAI 兼容 Chat Completions 接口支持标准 `messages` 输入与流式响应，但**不原生支持[工具调用](../concepts/tool-calling.md)**，需自行封装；详见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。
- Anthropic 兼容 Messages 接口支持 `tool_use` 和 `thinking` 模式，适用于需要结构化[工具调用](../concepts/tool-calling.md)的场景；该能力在 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md) 中有明确说明。
- DashScope 接口是百炼原生方案，提供最完整的参数控制（如 `enable_search`、`enable_code_interpreter`）和最高优先级的模型更新支持；其详细能力清单见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。

## 关键参数

通用关键参数（跨接口一致）：
- `model`: 必填，取值为 `qwen-max` / `qwen-plus` / `qwen-turbo`
- `messages`: 对话历史数组，格式为 `[{ "role": "user" | "assistant" | "system", "content": string }]`
- `temperature`: 控制输出随机性（0.0–1.0，默认 0.8）
- `max_tokens`: 输出最大 token 数（注意：不同接口对超限行为处理不同，DashScope 会严格截断，[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)可能返回 error）

接口特有参数：
- [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)支持 `stream`、`response_format`（仅 JSON Schema）、`tools`（需配合 `tool_choice`）
- Anthropic 兼容接口支持 `system` 字段（独立于 messages）、`tool_choice`（`auto`/`any`/`none`）和 `max_tokens`（必填）
- DashScope 接口支持 `top_p`、`seed`、`incremental_output` 及扩展工具开关（如 `enable_web_search`）

> **注意**：`max_tokens` 在 Anthropic 兼容接口中为必填项，而在 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)中为可选项——此差异已在 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md) 的子文档中确认，但部分旧版 SDK 示例未体现该约束，建议以最新文档为准。

## 使用方式

1. 获取 API Key：登录百炼控制台 →「API 密钥管理」→ 创建密钥  
2. 设置请求头：`Authorization: Bearer <your_api_key>`，`Content-Type: application/json`  
3. 发送 POST 请求至对应 endpoint：
   - OpenAI 兼容：`https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`
   - Anthropic 兼容：`https://dashscope.aliyuncs.com/compatible-mode/v1/messages`
   - DashScope 原生：`https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`

示例请求体（DashScope）：
```json
{
  "model": "qwen-max",
  "input": {
    "messages": [{"role": "user", "content": "你好"}]
  },
  "parameters": {"temperature": 0.5, "max_tokens": 512}
}
```

## 限制和注意事项

- 单次请求 `messages` 总长度（含 system prompt）不得超过模型上下文窗口（`qwen-max`: 32768 tokens；`qwen-plus`: 131072 tokens；`qwen-turbo`: 8192 tokens）  
- 流式响应中，OpenAI 兼容接口返回 `delta` 字段，DashScope 返回 `output.text` 增量，二者字段语义不完全对齐，需按接口规范解析  
- 工具调用功能在 OpenAI 兼容接口中依赖 `tools` + `tool_choice` 参数组合，但**不支持自动触发联网搜索**（该能力仅 DashScope 和 Anthropic 兼容接口提供）  
- 所有接口均不支持跨请求的 server-side 对话状态维护；若需持久化 history，须由客户端自行管理或使用百炼提供的 [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md) 封装服务（该服务内置对话管理逻辑）

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


