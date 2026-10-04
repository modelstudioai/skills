# application component api reference

应用组件 API 是百炼平台提供的核心能力封装，用于在自定义应用中集成大模型推理、工具调用、会话管理等能力。该接口面向生产级应用开发，支持同步/异步调用模式，并与百炼统一鉴权体系深度集成。所有功能均通过标准 HTTP RESTful 接口暴露，开发者需按规范构造请求并处理响应。

## 支持的模型与功能

当前支持以下模型能力：
- 通义千问系列（`qwen-max`、`qwen-plus`、`qwen-turbo`）的文本生成与多轮对话；
- 内置工具调用（如搜索、代码解释、知识库检索），需在 `tools` 参数中显式声明；
- 流式响应（`stream=true`）和非流式响应两种模式；
- 会话状态维护（通过 `session_id` 实现上下文延续），详见 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)。

> **注意**：文档中提及的 `qwen-vl` 视觉语言模型暂未在应用组件 API 中开放，实际可用模型请以 [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md) 列表为准；该不一致已在 [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md) 中标记为“待上线”。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen-plus`，必须与 [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md) 中所列一致 |
| `input.messages` | array | 是 | 对话消息数组，格式为 `[{ "role": "user", "content": "..." }]` |
| `parameters.temperature` | number | 否 | 采样温度，默认 `0.8`；取值范围 `[0.0, 1.0]` |
| `session_id` | string | 否 | 会话唯一标识，用于上下文保持；若未提供，服务端将自动生成新会话 |
| `stream` | boolean | 否 | 是否启用流式响应，默认 `false` |

## 使用方式

1. **认证**：使用 RAM 凭据（AccessKey ID / Secret）签发签名，或通过 STS [Token](../concepts/token.md) 授权，具体流程见 [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)；  
2. **请求地址**：向服务接入点（Endpoint）发送 `POST /v1/apps/{app_id}/chat` 请求，Endpoint 地址请参考 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)；  
3. **示例请求体**：
   ```json
   {
     "model": "qwen-plus",
     "input": {
       "messages": [{"role": "user", "content": "你好"}]
     },
     "parameters": {"temperature": 0.5},
     "session_id": "sess_abc123"
   }
   ```

## 限制和注意事项

- 单次请求 `input.messages` 总长度（字符数）不得超过 32768；
- `session_id` 生命周期为 7 天，超时后上下文自动失效；
- 工具调用返回结果中 `tool_calls` 字段仅在 `stream=false` 时完整返回；流式模式下需按 chunk 解析 `delta.tool_calls`；
- 跨区域调用需确保 Endpoint 与应用所在地域一致，否则将返回 `InvalidRegion` 错误；
- 所有错误响应均遵循统一格式，含 `code` 和 `message` 字段，详细错误码见 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)。

## 来源文档

- [应用组件](../../raw/application-api-reference/application-component-api-reference.md)


