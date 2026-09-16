# application component api reference

应用组件 API 是百炼平台提供的核心能力接口，用于在自定义应用中集成大模型推理、工具调用、会话管理等能力。该 API 以 RESTful 形式提供，支持同步/异步调用模式，适用于构建对话机器人、智能助手、自动化工作流等场景。所有请求需通过 RAM 授权并使用指定服务接入点，具体细节请参考 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)。

## 支持的模型与功能

当前支持的模型包括 `qwen-max`、`qwen-plus`、`qwen-turbo` 及部分专属微调模型（需开通白名单）。功能覆盖：
- 单轮/多轮对话（含历史上下文维护）
- [函数调用](../concepts/function-calling.md)（Function Calling）与工具编排
- 流式响应（`stream=true`）
- 输入内容校验与结构化输出（通过 `response_format` 指定 JSON Schema）

> **注意**：文档中提及的 `qwen-vl` 和 `qwen-audio` 模型在 [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md) 中已标记为“暂不开放公测”，与早期 [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md) 中的描述存在不一致，请以最新 API 目录为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型 ID，如 `qwen-plus`；必须与授权范围匹配 |
| `messages` | array | 是 | 对话消息列表，每项含 `role`（`user`/`assistant`/`system`/`tool`）和 `content` |
| `tools` | array | 否 | 工具定义数组，格式遵循 OpenAI Tool Specification |
| `tool_choice` | string / object | 否 | 控制工具调用策略，可选 `"auto"`、`"none"` 或指定工具 |
| `stream` | boolean | 否 | 默认 `false`；设为 `true` 时返回 SSE 流式响应 |
| `max_tokens` | integer | 否 | 输出最大 token 数，范围 1–4096 |

## 使用方式

1. **认证**：使用 RAM 用户 AccessKey（需授予 `bailian:InvokeApplicationComponent` 权限），通过 `Authorization: Bearer <access_token>` 或 `X-Acs-AccessKeyId` + `X-Acs-Signature` 方式鉴权  
2. **请求地址**：`POST https://<region-id>.bailian.aliyuncs.com/api/v1/chat/completions`（区域 ID 见 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)）  
3. **示例请求体**：
```json
{
  "model": "qwen-plus",
  "messages": [{"role": "user", "content": "你好"}],
  "stream": false
}
```

## 限制和注意事项

- 单次请求 `messages` 总长度不得超过 32768 tokens（含系统提示与工具描述）  
- 异步任务（`/v1/jobs`）最长保留 7 天，超时自动清理  
- 工具调用返回的 `tool_calls` 字段中，`function.arguments` 始终为字符串，需自行 JSON.parse  
- 所有时间戳字段（如 `created`）均采用 Unix 时间戳（秒级）  
- 跨区域调用不支持，务必确保 SDK 配置的 `region_id` 与接入点一致  

请严格依据 [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md) 配置权限，避免因策略缺失导致 `403 Forbidden` 错误。

## 来源文档

- [应用组件](../../raw/application-api-reference/application-component-api-reference.md)


