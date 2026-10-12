# qwen api reference

Qwen 系列大模型通过百炼平台提供多种 API 接口，支持文本生成、多轮对话、工具调用等核心能力。开发者可根据技术栈偏好和功能需求选择 OpenAI 兼容、Anthropic 兼容或百炼原生 DashScope 接口。所有接口均需通过 API Key 认证，并遵循统一的配额与计费规则。

## 支持的模型/功能

当前支持的 Qwen 模型包括 `qwen-max`、`qwen-plus` 和 `qwen-turbo`，覆盖高性能、均衡型与高性价比场景。各接口支持的功能略有差异：
- OpenAI 兼容 Chat Completions 接口支持标准 `messages` 输入与流式响应，但**不原生支持工具调用**（需自行封装）[文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)；
- Anthropic 兼容 Messages 接口原生支持 `tool_use` 与 `thinking` 模式，适用于复杂推理任务 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)；
- DashScope 接口提供最完整的功能集，包括结构化输出（JSON Schema）、自定义 stop token、以及细粒度的 logprobs 控制 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。

> **注意**：原始文档中提及的 “OpenAI兼容-Responses” 接口已下线，其功能已合并至新版 DashScope `/v1/services/aigc/text-generation` 路径，请勿再使用旧路径 `openai-compatible-responses`。

## 关键参数

通用关键参数（各接口均支持）：
- `model`: 必填，如 `"qwen-max"`；
- `messages`: 对话历史数组，格式为 `[{ "role": "user", "content": "..." }]`；
- `temperature`: 控制随机性（0.0–2.0），默认 1.0；
- `max_tokens`: 输出最大 token 数，上限依模型而异（`qwen-max` 为 8192）；
- `stream`: 布尔值，启用流式响应（仅 DashScope 与 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)支持）。

DashScope 特有参数：
- `response_format`: 支持 `"text"` 或 `{"type": "json_object"}`；
- `tools`: 定义可用工具列表，配合 `tool_choice` 使用；
- `top_p`, `repetition_penalty`, `stop` 等高级采样控制。

## 使用方式

1. 获取 API Key：在百炼控制台「API 密钥管理」中创建；
2. 设置请求头：`Authorization: Bearer <your_api_key>`，`Content-Type: application/json`；
3. 发送 POST 请求：
   - OpenAI 兼容：`POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`
   - DashScope 原生：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation`

示例（DashScope）：
```bash
curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "model": "qwen-max",
        "input": {"messages": [{"role":"user","content":"你好"}]},
        "parameters": {"max_tokens": 512}
      }'
```

## 限制和注意事项

- 单次请求 `messages` 总长度（含 system prompt）不得超过模型上下文窗口（如 `qwen-max` 为 32768 tokens）；
- 流式响应中，[OpenAI 兼容接口](../concepts/openai-compatible-api.md)返回 `data: {...}` 格式，DashScope 返回标准 JSON Lines（每行一个完整 JSON 对象）；
- 免费额度按自然月重置，超出后按用量计费；具体配额见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)；
- 不支持跨模型 session 复用；对话状态需由客户端自行维护（除 Anthropic Messages 接口内置有限历史管理外）。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


