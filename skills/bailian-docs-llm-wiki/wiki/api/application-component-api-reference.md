# application component api reference

应用组件 API 提供了在百炼平台中集成和调用预置能力（如对话、知识检索、工具调用等）的标准接口，适用于构建端到端 AI 应用。该 API 以 RESTful 形式提供，支持同步响应与[流式输出](../concepts/streaming-output.md)，并与百炼的权限体系（RAM）、模型路由及服务治理机制深度集成。开发者需通过 [API概览](raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md) 理解整体设计原则后，再配置具体调用。

## 支持的模型/功能

当前支持以下核心能力：
- **对话模型**：`qwen-max`、`qwen-plus`、`qwen-turbo`（默认路由至最新稳定版本）；
- **知识增强**：通过 `retrieval` 参数启用向量检索，支持接入百炼知识库（需提前绑定）；
- **工具调用**：支持 `tools` 字段声明函数列表，由模型自主选择并生成 `tool_calls`；  
- **多模态输入**：仅 `qwen-vl-plus` 支持图像 base64 或 OSS URL 输入（详见 [API目录](raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md) 中 `/v1/chat/completions` 的 `messages[].content` 定义）。

> **注意**：原始文档中 [版本说明](raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md) 提及 `qwen-2.5` 为已上线模型，但实际调用时该标识不可用，应使用 `qwen-max` 获取同代最优能力——此为已知过时信息。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型 ID，必须为平台支持的合法值（见上节），不支持自定义别名 |
| `messages` | array | 是 | 对话历史，格式同 OpenAI，但 `role: "system"` 仅首条生效 |
| `stream` | boolean | 否 | `true` 时返回 SSE 流；`false`（默认）返回 JSON 响应体 |
| `retrieval` | object | 否 | 启用知识检索，结构为 `{ "knowledge_id": "xxx", "top_k": 3 }` |
| `tools` | array | 否 | 工具定义数组，每项含 `function.name`、`description`、`parameters`（JSON Schema） |

## 使用方式

1. **认证**：使用阿里云 AccessKey（推荐 RAM 子账号）+ 签名，或 STS [Token](../concepts/token.md)（参见 [授权信息](raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)）；  
2. **请求地址**：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`（生产环境 endpoint 见 [服务接入点](raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)）；  
3. **示例请求体**：
```json
{
  "model": "qwen-plus",
  "messages": [{"role": "user", "content": "今天北京天气如何？"}],
  "retrieval": {"knowledge_id": "kg-abc123", "top_k": 2}
}
```

## 限制和注意事项

- 单次请求 `messages` 总长度上限为 32768 token（按模型 tokenizer 计算），超限将返回 `400 Bad Request`；
- `stream: true` 时，响应头 `Content-Type` 固定为 `text/event-stream`，客户端须按 SSE 协议解析；
- 工具调用返回的 `tool_calls` 不包含执行结果，需开发者自行调用对应服务并拼接 `tool_message` 后续提交；
- 所有 API 调用受百炼配额系统管控，超出额度将返回 `429 Too Many Requests`，配额详情请查阅控制台或 [API概览](raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)。

## 来源文档

- [应用组件](../../raw/application-api-reference/application-component-api-reference.md)


