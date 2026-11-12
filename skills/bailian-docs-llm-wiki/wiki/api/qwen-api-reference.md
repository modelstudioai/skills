# qwen api reference

Qwen 系列大语言模型通过百炼平台提供多种 API 接入方式，支持文本生成、多轮对话、工具调用等核心能力。开发者可根据技术栈兼容性、功能需求和运维复杂度选择合适接口。所有接口均需通过百炼平台鉴权访问，并遵循统一的配额与计费规则。

## 支持的模型/功能

当前支持的 Qwen 模型包括 `qwen-max`（旗舰版）、`qwen-plus`（均衡版）和 `qwen-turbo`（轻量版），覆盖从高精度推理到低延迟响应的全场景需求。各接口支持的功能略有差异：
- OpenAI 兼容 Chat Completions 接口支持标准 `messages` 输入与流式响应，但**不原生支持工具调用**（需自行封装）；详见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。
- Anthropic 兼容 Messages 接口支持 `tool_use` 和 `thinking` 字段，适用于需要结构化工具调用的场景；该能力在 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md) 中有明确说明。
- DashScope 接口是百炼原生方案，支持最完整的参数集（如 `enable_search`、`max_output_tokens`、`stop` 等），并提供模型专属能力（如 Qwen-VL 多模态扩展）；其详细参数定义见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。

## 关键参数

通用关键参数（跨接口适用）包括：
- `model`: 必填，取值为 `qwen-max`、`qwen-plus` 或 `qwen-turbo`；
- `messages`: 对话历史列表，格式为 `[{ "role": "user", "content": "..." }]`；
- `temperature`: 控制输出随机性（0.0–2.0），默认 1.0；
- `top_p`: 核采样阈值（0.0–1.0），默认 1.0；
- `stream`: 布尔值，启用流式响应（部分接口需额外配置 `Content-Type: text/event-stream`）。

> **注意**：`max_tokens` 在 DashScope 接口中名为 `max_output_tokens`，而 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)中仍为 `max_tokens`；二者语义一致但字段名不同，使用时需按接口规范填写。

## 使用方式

1. **认证**：所有请求需在 `Authorization` Header 中携带 Bearer [Token](../concepts/token.md)（即百炼平台 API Key）；
2. **Endpoint**：
   - OpenAI 兼容：`https://dashscope.aliyuncs.com/v1/chat/completions`
   - Anthropic 兼容：`https://dashscope.aliyuncs.com/v1/messages`
   - DashScope 原生：`https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
3. **示例请求（curl）**：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/v1/chat/completions \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "qwen-max",
           "messages": [{"role": "user", "content": "你好"}]
         }'
   ```

## 限制和注意事项

- 单次请求 `messages` 总长度（含角色标记）上限为 32768 token（Qwen-Max），具体以模型文档为准；
- 流式响应中，[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)返回 `data: {...}` 格式，DashScope 接口返回纯 JSON 数组，客户端需适配解析逻辑；
- 工具调用功能仅在 Anthropic 兼容 Messages 接口和 DashScope 接口中可用，[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)暂不支持（参见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)）；
- 所有接口均不支持跨模型 session 共享，对话状态需由客户端自行维护（除非使用 OpenAI 兼容-Responses 接口，其内置历史管理机制）。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


