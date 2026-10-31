# qwen api reference

Qwen 系列大模型通过百炼平台提供多种 API 接入方式，支持文本生成、工具调用、多轮对话等核心能力。开发者可根据技术栈兼容性、功能需求和运维复杂度选择合适接口。所有接口均需通过百炼平台申请 API Key 并完成鉴权。

## 支持的模型与功能

当前 Qwen 系列支持以下主流接入协议：

- **OpenAI 兼容 Chat Completions**：完全遵循 OpenAI `/v1/chat/completions` 规范，适用于已有 OpenAI SDK 的项目快速迁移。详见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。
- **OpenAI 兼容-Responses**：在标准 Chat Completions 基础上增强，内置联网搜索、代码解释器和网页内容提取能力，并自动维护对话上下文，无需客户端手动管理 history。该能力描述见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。
- **Anthropic 兼容 Messages**：适配 Anthropic Messages API（`/messages`），支持 `tool_use`、`thinking` 等结构化输出，适用于需要显式推理链或工具编排的场景。具体参数与行为请参考 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。
- **DashScope 原生接口**：百炼专属协议，提供最全参数控制（如 `top_k`、`repetition_penalty`、`enable_search` 细粒度开关）及模型专属能力（如 Qwen2-VL 多模态输入支持），推荐新项目优先选用。

> **注意**：`OpenAI 兼容-Responses` 接口的 `max_tokens` 行为与标准 OpenAI 不一致——其实际限制包含系统提示词与工具调用返回内容总长度，而标准 OpenAI 仅限制模型输出。此差异已在 [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md) 文档中明确说明，但未在主入口文档同步更新，使用时请以子文档为准。

## 关键参数

通用关键参数（各接口均支持，语义一致）：

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `model` | string | 必填。模型标识符，如 `qwen-max`、`qwen-plus`、`qwen-turbo`；部分接口（如 DashScope）还支持 `qwen-vl-plus` 等多模态型号。 |
| `messages` | array | 必填。对话消息数组，格式为 `[{ "role": "user", "content": "..." }]`；`system` 角色在 Anthropic 和 DashScope 接口中受支持，在 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)中可能被忽略或转为 `user`。 |
| `temperature` | number | 控制随机性，默认 `0.8`；范围 `0.0–2.0`。 |
| `top_p` | number | 核采样阈值，默认 `0.8`；范围 `0.0–1.0`。 |

接口特有参数示例：
- DashScope：`top_k`（默认 `40`）、`repetition_penalty`（默认 `1.05`）、`enable_search`（布尔值，启用实时搜索）；
- Anthropic：`tools`（工具定义数组）、`tool_choice`（工具调用策略）；
- OpenAI 兼容-Responses：`enable_code_interpreter`、`enable_web_search`（均为布尔值，独立开关）。

## 使用方式

1. **认证**：所有请求需在 `Authorization` Header 中携带 `Bearer <your_api_key>`；
2. **Endpoint**（以 `qwen-plus` 为例）：
   - OpenAI 兼容：`https://dashscope.aliyuncs.com/v1/chat/completions`
   - Anthropic 兼容：`https://dashscope.aliyuncs.com/v1/messages`
   - DashScope 原生：`https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
3. **示例请求（cURL）**：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/v1/chat/completions" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "qwen-plus",
           "messages": [{"role": "user", "content": "你好"}],
           "temperature": 0.5
         }'
   ```

## 限制和注意事项

- **速率限制**：免费版默认 5 QPS，企业版按配额配置；超出将返回 `429 Too Many Requests`；
- **输入长度**：`qwen-turbo` 最大上下文为 8K tokens，`qwen-plus` 为 32K，`qwen-max` 为 64K；超长输入将被截断且不报错；
- **输出长度**：`max_tokens` 限制的是模型生成 token 数，不包含输入；但 `OpenAI 兼容-Responses` 接口的实际响应长度可能因工具调用结果膨胀，需预留缓冲；
- **工具调用**：仅 DashScope 和 Anthropic 接口支持自定义工具函数；[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)的工具能力为平台预置，不可扩展；
- **错误码**：统一使用 HTTP 状态码 + JSON 错误体，常见如 `400 Bad Request`（参数错误）、`401 Unauthorized`（密钥无效）、`404 Not Found`（模型不存在）。详细映射见 [DashScope 错误码文档](../../raw/error-codes/dashscope-error-codes.md)。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


