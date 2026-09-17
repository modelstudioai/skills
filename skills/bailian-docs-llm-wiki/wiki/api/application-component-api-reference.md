# application component api reference

应用组件 API 提供了在百炼平台中集成和调用预置能力（如对话、知识检索、工具调用等）的标准接口，适用于构建企业级 AI 应用。该 API 以 RESTful 形式提供，支持同步响应与[流式输出](../concepts/streaming-output.md)，并与百炼统一身份认证体系深度集成。开发者需通过 RAM 授权获取访问凭证，方可调用相关接口。

## 支持的模型/功能

当前应用组件 API 支持以下核心能力：  
- 基于百炼托管模型的对话推理（如 `qwen-max`、`qwen-plus`、`qwen-turbo`）；  
- 结合知识库的增强问答（需提前配置 KnowledgeBase ID）；  
- 工具调用（Tool Calling），支持自定义函数描述与自动参数提取；  
- 多轮会话状态管理（通过 `session_id` 维持上下文）。  
详细能力列表及对应模型版本请参见 [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen-max`；必须与 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md) 中公布的可用模型一致 |
| `input.messages` | array | 是 | 消息数组，格式为 `[{ "role": "user", "content": "..." }]`；支持 `user`/`assistant`/`system` 角色 |
| `parameters.temperature` | number | 否 | 采样温度，默认 `0.8`；范围 `[0.0, 2.0]` |
| `parameters.top_p` | number | 否 | 核采样阈值，默认 `0.95`；范围 `[0.0, 1.0]` |
| `parameters.max_tokens` | integer | 否 | 最大生成 token 数，默认 `2048`，上限 `8192` |

> **注意**：`parameters.stop` 当前仅支持字符串数组（如 `["\n"]`），不支持正则或复杂表达式——该限制在 [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md) 中未明确提及，但实测 v2023-12-29 及后续版本均不生效，建议避免使用。

## 使用方式

1. 获取服务接入点：从 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md) 获取对应 Region 的 endpoint URL（如 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`）；  
2. 构造请求头：包含 `Authorization: Bearer <api_key>` 和 `Content-Type: application/json`；  
3. 发送 POST 请求，body 示例：
```json
{
  "model": "qwen-max",
  "input": {
    "messages": [{"role": "user", "content": "你好"}]
  },
  "parameters": {"temperature": 0.5}
}
```

## 限制和注意事项

- 单次请求 `input.messages` 总长度不得超过 32768 tokens（含 system [prompt](../guides/prompt.md)）；  
- 流式响应需设置 `stream: true`，此时响应体为 SSE 格式，字段名与非流式保持一致（如 `output.text`）；  
- 调用失败时，HTTP 状态码非 `2xx`，错误结构遵循百炼统一规范，详见 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)；  
- RAM 授权策略需显式授予 `dashscope:InvokeApplication` 权限，具体配置参考 [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)。

## 来源文档

- [应用组件](../../raw/application-api-reference/application-component-api-reference.md)


