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
| `parameters.top_p` | number | 否 | 核采样阈值，默认 `0.95`；范围 `(0.0, 1.0]` |
| `parameters.max_tokens` | integer | 否 | 最大生成 token 数，默认 `2048`，上限 `8192` |

> **注意**：`parameters.stop` 当前仅支持字符串数组（如 `["\n"]`），不支持正则或复杂模式——该限制在 [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md) 中未明确提及，但实测 v2023-12-29 及后续版本均不生效，建议避免使用。

## 使用方式

1. 获取服务接入点：调用前需确认 Region 对应的 Endpoint，参考 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)；  
2. 配置授权：使用阿里云 RAM 的 `BaiLianFullAccess` 或最小权限策略（含 `bailian:InvokeApplicationComponent` 动作），详见 [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)；  
3. 发起 POST 请求：`POST https://{endpoint}/api/v1/applications/{app_id}/components/invoke`，Header 中携带 `Authorization: Bearer <access_token>`；  
4. 解析响应：成功时返回 `200 OK`，流式响应需按 SSE 格式解析 `data:` 行。

## 限制和注意事项

- 单次请求最大 `input.messages` 长度为 100 条，总 token 数（输入+输出）不得超过模型上下文窗口（如 `qwen-max` 为 32768）；  
- 流式响应中 `delta.content` 字段可能为空（例如工具调用阶段），需兼容空内容处理逻辑；  
- `session_id` 若未显式传入，服务端将自动生成，但不保证跨请求一致性，生产环境务必自行维护；  
- 所有参数校验失败均返回 `400 Bad Request`，错误码与具体字段在 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md) 的“错误响应”章节定义。

## 来源文档

- [应用组件](../../raw/application-api-reference/application-component-api-reference.md)


