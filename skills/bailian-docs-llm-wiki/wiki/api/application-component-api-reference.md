# application component api reference

应用组件 API 是百炼平台提供的核心能力接口，用于在自定义应用中集成大模型推理、工具调用、会话管理等能力。该 API 采用 RESTful 设计，支持同步/异步调用模式，适用于构建对话机器人、智能助手、自动化工作流等场景。所有请求需通过 RAM 授权并使用指定服务接入点，具体细节请参考 [应用组件](../../raw/application-api-reference/application-component-api-reference.md)。

## 支持的模型与功能

- **基础模型调用**：支持 `qwen-max`、`qwen-plus`、`qwen-turbo` 等 Qwen 系列模型，以及部分第三方模型（需开通白名单）  
- **增强能力**：  
  - 工具调用（Function Calling），支持动态注册和自动路由  
  - 多轮会话管理（`session_id` 驱动的状态保持）  
  - 流式响应（`stream=true`）与非流式响应双模式  
  - 输入[内容安全过滤](../concepts/security-filtering.md)（默认启用，可配置开关）  

> **注意**：[API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md) 中列出的 `/v1/chat/completions` 接口当前已统一为 `/v1/applications/{app_id}/chat`，旧路径将于 2024-Q3 下线，请以 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md) 的最新路由为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，由控制台创建应用时生成 |
| `messages` | array | 是 | 对话消息列表，格式同 OpenAI；`role` 仅支持 `user`/`assistant`/`system`，不支持 `tool`（工具结果需通过 `tool_output` 字段传入） |
| `model` | string | 否 | 显式指定模型；若未提供，则使用应用配置的默认模型（见 [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)） |
| `stream` | boolean | 否 | 默认 `false`；设为 `true` 时返回 SSE 流，首帧含 `usage` 元信息 |
| `tools` | array | 否 | 工具定义数组，结构与 OpenAI 兼容；工具执行结果必须通过后续请求的 `tool_output` 提交 |

## 使用方式

1. **认证**：使用 RAM Role 或 AccessKey 签名，Header 中携带 `Authorization: Bearer <token>`（JWT 格式，有效期 1 小时）  
2. **请求示例**（cURL）：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/applications/ak-xxx/chat" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
           "messages": [{"role": "user", "content": "你好"}],
           "stream": false
         }'
   ```
3. **响应解析**：成功响应状态码为 `200`；流式响应每帧为独立 JSON 行（NDJSON），含 `id`、`choices[].delta`、`usage` 等字段。

## 限制和注意事项

- 单次请求 `messages` 总长度上限为 32768 token（按模型 tokenizer 计算）  
- 同一 `app_id` 下并发请求数默认限流 10 QPS，可通过工单提额  
- 工具调用链深度限制为 3 层（user → tool1 → tool2 → assistant），超出将被截断并返回错误  
- **重要**：`system` 消息仅在会话首条消息中生效，后续请求中重复传入 `system` 将被忽略 —— 此行为与 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md) 文档描述一致，但与早期 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md) 示例存在差异，请以实际运行逻辑为准。

## 来源文档

- [应用组件](../../raw/application-api-reference/application-component-api-reference.md)


