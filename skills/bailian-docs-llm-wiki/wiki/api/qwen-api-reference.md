# qwen api reference

Qwen 系列大语言模型通过百炼平台提供多种 API 接口，支持文本生成、多轮对话、工具调用等核心能力。开发者可根据技术栈兼容性、功能需求和运维复杂度选择合适接口。所有接口均需通过阿里云 AccessKey 进行身份认证，并遵循统一的配额与计费规则。

## 支持的模型/功能

当前支持的 Qwen 模型包括 `qwen-max`（旗舰版）、`qwen-plus`（均衡版）、`qwen-turbo`（轻量版）及 `qwen2.5` 系列（如 `qwen2.5-7b-instruct`）。各模型在 [OpenAI 兼容 Chat Completions](https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-chat-completions)、[Anthropic兼容-Messages](https://help.aliyun.com/zh/model-studio/anthropic-api-messages) 和 [DashScope](https://help.aliyun.com/zh/model-studio/qwen-api-via-dashscope) 三类接口下均可调用，但功能覆盖存在差异：  
- DashScope 接口支持最全参数（如 `top_k`、`repetition_penalty`、`enable_search`），且是唯一支持流式响应（`stream=true`）与自定义 stop 字符串的原生通道；  
- [OpenAI 兼容接口](../concepts/openai-compatibility.md)默认启用对话历史自动管理，但不支持 `top_k` 或 `presence_penalty` 等非标准参数；  
- Anthropic Messages 接口支持 `tool_use` 和 `system` 消息类型，但暂不支持 `response_format` 结构化输出（该能力仅 DashScope 提供）。  
详细模型能力对比见 [原文标题](../../raw/model-api-reference/qwen-api-reference.md)。

## 关键参数

通用关键参数（以 DashScope 为例）：
- `model`: 必填，如 `"qwen-max"`；  
- `input.messages`: 消息数组，格式为 `[{ "role": "user", "content": "..." }]`；  
- `parameters.temperature`: 浮点数（0.0–2.0），控制输出随机性；  
- `parameters.max_tokens`: 输出最大 token 数，上限依模型而异（`qwen-max` 为 8192）；  
- `parameters.stream`: 布尔值，启用流式响应（仅 DashScope 支持）；  
- `parameters.tools`: 工具定义列表（仅 DashScope 和 Anthropic Messages 支持）。  
> **注意**：[OpenAI 兼容接口](../concepts/openai-compatibility.md)中 `temperature` 位于顶层而非 `parameters` 下，且 `max_tokens` 对应字段名为 `max_completion_tokens` —— 此处行为差异已在 [原文标题](../../raw/model-api-reference/qwen-api-reference.md) 中明确说明，但部分旧版 SDK 文档未同步更新，请以实际请求响应为准。

## 使用方式

1. **认证**：使用阿里云 `AccessKeyId` 和 `AccessKeySecret` 签名，或通过 `Authorization: Bearer <api_key>`（仅 DashScope 支持 API Key 方式）；  
2. **端点**：  
   - DashScope: `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`；  
   - OpenAI 兼容: `https://dashscope.aliyuncs.com/v1/chat/completions`；  
   - Anthropic Messages: `https://dashscope.aliyuncs.com/v1/messages`；  
3. **示例请求（DashScope）**：  
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "qwen-max",
           "input": {"messages": [{"role":"user","content":"你好"}]},
           "parameters": {"temperature": 0.8}
         }'
   ```  
完整调用流程与错误码说明参见 [原文标题](../../raw/model-api-reference/qwen-api-reference.md)。

## 限制和注意事项

- **配额限制**：免费额度按项目（Project）维度分配，超出后按 token 计费；`qwen-max` 的单次请求输入 + 输出总 token 不得超过 32768；  
- **超时时间**：所有接口默认超时 60 秒，DashScope 可通过 `parameters.timeout` 扩展至最长 300 秒；  
- **内容安全**：所有请求经百炼内容安全网关过滤，含敏感词或违规内容将返回 `400 Bad Request` 并附带 `error.code="content_blocked"`；  
- **工具调用**：`tools` 参数仅在 `qwen-plus` 及以上模型生效，`qwen-turbo` 调用时会静默忽略工具声明；  
- **历史管理**：[OpenAI 兼容接口](../concepts/openai-compatibility.md)的 `messages` 数组若超过 100 条，服务端将自动截断最早 20 条以保障性能 —— 此策略未在 [原文标题](../../raw/model-api-reference/qwen-api-reference.md) 中明示，属平台运行时行为，建议客户端主动维护合理长度。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


