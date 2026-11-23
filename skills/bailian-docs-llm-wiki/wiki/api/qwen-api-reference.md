# qwen api reference

Qwen 系列大语言模型通过百炼平台提供多种 API 接入方式，支持 OpenAI、Anthropic 兼容协议及百炼原生 DashScope 接口。开发者可根据现有技术栈、功能需求（如工具调用、联网搜索）和运维习惯选择最适配的调用路径。所有接口均需通过百炼平台鉴权访问，且模型能力与参数支持因接入方式而异。

## 支持的模型/功能

当前 Qwen 系列支持的主流模型包括 `qwen-max`、`qwen-plus`、`qwen-turbo` 和 `qwen2.5` 等，具体可用模型列表以 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md) 中实时更新为准。不同接入方式支持的功能存在差异：  
- OpenAI 兼容 Chat Completions 接口支持基础对话与流式响应，但**不原生支持工具调用或联网搜索**；  
- OpenAI 兼容-Responses 接口内置联网搜索、代码解释器和网页内容提取能力，并自动维护对话历史；  
- Anthropic 兼容-Messages 接口支持 `tool_use` 和 `thinking` 模式，适用于需要结构化工具调用的场景；  
- DashScope 接口提供最完整的参数控制（如 `top_k`、`repetition_penalty`）和高级功能（如自定义 stop token、logprobs），详见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。

> **注意**：原始文档中提及的 `qwen2.5` 模型在部分旧版 DashScope SDK 中尚未默认启用，实际调用前请确认 SDK 版本 ≥ 4.12.0，或直接查阅 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md) 获取最新模型兼容性说明。

## 关键参数

通用关键参数（各接口均支持，但命名或行为略有差异）包括：  
- `model`：必需，指定模型 ID（如 `"qwen-max"`）；  
- `messages`：必需，对话消息数组，格式为 `[{ "role": "user", "content": "..." }]`；  
- `temperature`：控制输出随机性（0.0–2.0，默认 1.0）；  
- `max_tokens`：最大生成 token 数（含输入与输出，部分接口上限为 32768）；  
- `stream`：布尔值，启用流式响应（`true`/`false`）。  

DashScope 接口额外支持 `top_k`、`repetition_penalty`、`stop`（字符串或字符串数组）等精细化控制参数，详细说明见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。

## 使用方式

1. **认证**：使用百炼平台颁发的 `API Key`，通过 `Authorization: Bearer <api_key>` 请求头传递；  
2. **Endpoint**：根据所选协议构造 URL：  
   - OpenAI 兼容：`https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`；  
   - Anthropic 兼容：`https://dashscope.aliyuncs.com/compatible-mode/v1/messages`；  
   - DashScope 原生：`https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`；  
3. **请求示例**（cURL，DashScope 原生）：  
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "qwen-max",
           "input": {"messages": [{"role":"user","content":"你好"}]},
           "parameters": {"temperature": 0.8}
         }'
   ```

## 限制和注意事项

- 单次请求 `messages` 总长度（token 数）不得超过模型上下文窗口（如 `qwen-max` 为 32768 tokens），超长输入将被截断且**不返回警告**；  
- [OpenAI 兼容接口](../concepts/openai-compatible-api.md)的 `tools` 字段仅在 `/compatible-mode/v1/chat/completions` 路径下有效，且需配合 `tool_choice="auto"` 或显式指定，该行为与标准 OpenAI v1 不完全一致；  
- 所有接口均不支持跨会话状态共享，若需长期对话管理，必须自行维护 `messages` 历史或使用 OpenAI 兼容-Responses 接口（其内置对话状态管理）；  
- 错误码统一遵循 HTTP 状态码 + 百炼自定义 `code` 字段（如 `InvalidParameter`、`Throttling`），完整错误列表参见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


