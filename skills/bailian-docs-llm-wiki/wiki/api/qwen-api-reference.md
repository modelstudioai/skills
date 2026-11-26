# qwen api reference

Qwen 系列大模型通过百炼平台提供多种标准化 API 接口，支持文本生成、多轮对话、工具调用等核心能力。开发者可根据技术栈偏好和功能需求选择 OpenAI 兼容、Anthropic 兼容或百炼原生 DashScope 接口。所有接口均需通过 API Key 认证，并遵循统一的请求/响应格式规范。

## 支持的模型与功能

当前 Qwen 系列支持以下主流模型（以 `qwen-` 开头）：`qwen-max`（旗舰版）、`qwen-plus`（均衡版）、`qwen-turbo`（轻量版），以及专用于代码生成的 `qwen-coder`。各模型均支持基础文本生成、多轮对话、[函数调用](../concepts/function-calling.md)（function calling）及结构化输出（JSON mode）。工具调用能力在 [OpenAI兼容-Responses](../../raw/qwen-api-reference/qwen-api-reference.md) 和 [Anthropic兼容-Messages](../../raw/qwen-api-reference/qwen-api-reference.md) 中均有实现，但具体参数名和响应字段存在差异；建议优先参考 [DashScope](../../raw/qwen-api-reference/qwen-api-reference.md) 文档以获取最完整的能力映射。

## 关键参数

通用关键参数包括：
- `model`: 必填，如 `"qwen-max"`；
- `messages`: 对话历史数组，格式为 `[{ "role": "user", "content": "..." }]`；
- `temperature`: 控制随机性（0.0–2.0，默认 1.0）；
- `top_p`: 核采样阈值（0.0–1.0，默认 0.8）；
- `max_tokens`: 输出最大 token 数（默认 2048，上限依模型而异）；
- `tools` / `tool_choice`: 用于启用[函数调用](../concepts/function-calling.md)（仅 DashScope 和 Anthropic Messages 接口完全支持）。

> **注意**：`response_format` 参数在 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)中仅支持 `"json_object"`（需配合 `response_schema`），而 DashScope 接口支持更灵活的 schema 定义；该不一致已在 [DashScope](../../raw/qwen-api-reference/qwen-api-reference.md) 文档中明确说明。

## 使用方式

推荐按以下顺序接入：
1. 获取 API Key（控制台 → API 密钥管理）；
2. 选择接口类型：若已使用 OpenAI SDK，可直接复用 `openai.ChatCompletion.create()` 调用 [OpenAI 兼容 Chat Completions](../../raw/qwen-api-reference/qwen-api-reference.md)；若需联网搜索或自动历史管理，选用 [OpenAI兼容-Responses](../../raw/qwen-api-reference/qwen-api-reference.md)；
3. 构造请求体并发送 POST 请求至对应 endpoint（如 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`）；
4. 解析 JSON 响应中的 `output.text` 或 `output.choices[0].message.content` 字段。

## 限制和注意事项

- 单次请求 `messages` 总长度（输入+输出）不得超过模型上下文窗口（`qwen-max` 为 32768 tokens）；
- 免费试用额度按 token 计费，超出后需绑定支付方式；
- [函数调用](../concepts/function-calling.md)返回的 `tool_calls` 在 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)中为数组，在 Anthropic 接口中为嵌套对象，需适配解析逻辑；
- 流式响应（`stream: true`）在所有接口中均支持，但事件格式略有不同：DashScope 使用 `data: {...}` 行分隔，[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)遵循 SSE 标准。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


