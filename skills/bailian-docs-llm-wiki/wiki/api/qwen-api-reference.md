# qwen api reference

Qwen 系列大模型通过百炼平台提供多种 API 接口，支持文本生成、多轮对话、工具调用等核心能力。开发者可根据技术栈兼容性、功能需求和运维复杂度选择合适接口。所有接口均需通过阿里云 AccessKey 进行身份认证，并遵循统一的配额与计费规则。

## 支持的模型/功能

当前 Qwen 系列支持以下主流调用方式，覆盖不同生态适配场景：

- **OpenAI 兼容 Chat Completions**：完全兼容 OpenAI `chat/completions` 接口规范，适用于已有 OpenAI 客户端（如 `openai>=1.0.0`）的快速迁移；支持 `qwen-max`、`qwen-plus`、`qwen-turbo` 等全部公开文本生成模型。详情见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。
- **OpenAI 兼容-Responses**：在标准 Chat Completions 基础上增强内置能力，自动启用联网搜索、代码解释器及网页内容提取，且隐式维护对话历史，适合无需手动管理上下文的轻量级应用。该能力说明见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。
- **Anthropic 兼容-Messages**：实现 Anthropic Messages API 规范，支持 `system` 消息、`tool_use`/`tool_result` 交互及结构化思考链输出，适用于需要可控推理路径的场景。具体参数与行为请参考 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。
- **DashScope 原生接口**：百炼专属协议，提供最细粒度控制（如 `incremental_output`、`enable_search` 显式开关）、完整流式响应字段及调试元信息（`usage`、`finish_reason`），推荐用于生产环境高可靠性要求场景。

> **注意**：`qwen-vl` 和 `qwen-audio` 等多模态模型**不支持** Anthropic Messages 接口，仅可通过 DashScope 或专用多模态 API 调用；此限制未在 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md) 中明确说明，以 DashScope 官方文档为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen-max`、`qwen-plus`；不同接口对取值范围有差异（例如 Anthropic 接口不接受 `qwen-turbo`） |
| `messages` | array | 是（除部分 DashScope 非对话模式外） | 对话消息列表，格式为 `{"role": "user/system/assistant", "content": "..."}`；Anthropic 接口支持 `tool_use` 对象嵌套 |
| `temperature` | number | 否 | 控制输出随机性（0.0–2.0），默认 `0.8`；DashScope 接口额外支持 `top_p`、`seed` 等高级采样参数 |
| `stream` | boolean | 否 | 是否启用流式响应；所有接口均支持，但 Anthropic 接口流式 chunk 结构与 OpenAI 不同 |

## 使用方式

1. **认证**：在请求 Header 中添加 `Authorization: Bearer <your_api_key>`（OpenAI/Anthropic 兼容接口）或 `Authorization: Bearer <your_dashscope_api_key>`（DashScope 接口）；
2. **Endpoint**：
   - OpenAI 兼容：`https://dashscope.aliyuncs.com/v1/chat/completions`
   - Anthropic 兼容：`https://dashscope.aliyuncs.com/v1/messages`
   - DashScope 原生：`https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
3. **示例请求（curl）**：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/v1/chat/completions" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "qwen-plus",
           "messages": [{"role": "user", "content": "你好"}]
         }'
   ```

## 限制和注意事项

- 单次请求 `messages` 总长度（含角色标记）上限为 32768 token（DashScope 接口），[OpenAI 兼容接口](../concepts/openai-compatibility.md)为 32000 token；
- 流式响应中，[OpenAI 兼容接口](../concepts/openai-compatibility.md)返回 `delta.content` 字段，Anthropic 接口返回 `delta.text` 或 `delta.partial_json`，DashScope 返回 `output.text`；
- 所有接口均**不支持**跨模型会话状态共享（如 `qwen-max` 的 history 不能复用于 `qwen-turbo` 请求），需由客户端自行维护；
- 免费额度按自然月重置，超出后按实际 token 数计费；详细配额策略参见 [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)。

## 来源文档

- [文本生成模型API参考](../../raw/model-api-reference/qwen-api-reference.md)


