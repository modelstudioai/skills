# application component api reference

应用组件 API 提供了在百炼平台中集成和调用预置能力（如对话、知识检索、工具调用等）的标准接口，适用于构建企业级 AI 应用。该 API 以 RESTful 形式提供，支持同步响应与[流式输出](../concepts/streaming.md)，并与百炼统一身份认证体系深度集成。开发者需通过 RAM 授权获取访问凭证，方可调用相关接口。

## 支持的模型/功能

当前应用组件 API 支持以下核心能力：  
- 基于百炼托管模型的对话推理（如 `qwen-max`、`qwen-plus`、`qwen-turbo`）；  
- 结合知识库的增强问答（需提前配置 KnowledgeBase ID）；  
- 工具调用（Tool Calling），支持自定义函数描述与自动参数提取；  
- 多轮会话状态管理（通过 `session_id` 维持上下文）。  
详细能力列表及对应模型兼容性请参见 [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen-max`；必须与 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md) 中声明的可用模型一致 |
| `input.messages` | array | 是 | 对话消息数组，格式为 `[{ "role": "user", "content": "..." }]`；`role` 仅支持 `"user"` 和 `"assistant"` |
| `parameters.temperature` | number | 否 | 采样温度，默认 `0.85`；取值范围 `[0.0, 2.0]` |
| `parameters.top_p` | number | 否 | 核采样阈值，默认 `0.8`；取值范围 `[0.0, 1.0]` |
| `knowledge_config.knowledge_base_ids` | array | 否 | 知识库 ID 列表，启用知识增强时必填；ID 需已在控制台创建并发布 |

> **注意**：`input.messages` 中若包含 `role: "system"`，将被静默忽略——该行为与 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md) 描述一致，但与旧版文档 `api-bailian-2023-09-15-overview.md`（已归档）中“支持 system 角色”的说明冲突，后者已过时。

## 使用方式

1. 获取服务接入点：调用前需从 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md) 获取最新 Region 对应的 endpoint URL；  
2. 构造请求头：`Authorization: Bearer <access_token>`，其中 token 由 RAM 授权流程颁发；  
3. 发送 POST 请求至 `/v1/applications/{app_id}/chat`，body 为 JSON 格式，结构符合上述关键参数定义；  
4. 流式响应需设置 `Accept: text/event-stream`，并按 SSE 协议解析 `data:` 字段。

## 限制和注意事项

- 单次请求 `input.messages` 最多支持 50 条消息，总 tokens 不得超过模型最大上下文长度（例如 `qwen-max` 为 32768）；  
- `session_id` 若未显式传入，服务端将自动生成，但不保证跨请求一致性；建议业务层主动维护；  
- 知识库检索结果默认最多返回 5 个 chunk，不可通过参数调整；如需更多上下文，请自行调用知识库检索 API；  
- 所有调用均受配额限制，具体额度取决于应用绑定的 RAM 角色策略，详见 [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)。

## 来源文档

- [应用组件](../../raw/application-api-reference/application-component-api-reference.md)


