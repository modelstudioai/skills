# application component api reference

应用组件 API 是百炼平台提供的核心能力接口，用于在自定义应用中集成大模型推理、工具调用、会话管理等能力。该 API 以 RESTful 形式提供，支持同步/[异步调用](../concepts/asynchronous-invocation.md)模式，适用于构建对话型、任务型及工作流类 AI 应用。所有接口均需通过 RAM 授权并使用指定服务接入点访问。

## 支持的模型与功能

当前支持调用百炼平台托管的全部公开模型（如 qwen-max、qwen-plus、qwen-turbo），以及用户已部署的私有模型。功能覆盖文本生成、多轮对话（含 history 管理）、[函数调用](../concepts/function-calling.md)（function calling）、流式响应（stream=true）和输出格式约束（response_format）。部分高级功能（如 long-context 模式或结构化输出校验）仅对特定模型版本开放，详见 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md) 中的功能矩阵表。

> **注意**：[API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md) 中列出的 `/v1/chat/completions` 接口当前实际支持 `tools` 字段，但文档中未明确标注其兼容性；请以 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md) 所附最新 OpenAPI 3.0 Schema 为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型 ID，必须为已授权且可用的模型（如 `qwen-max`） |
| `messages` | array | 是 | 对话消息列表，每项含 `role`（system/user/assistant/tool）和 `content` |
| `stream` | boolean | 否 | true 时返回 SSE 流式响应；默认 false |
| `tools` | array | 否 | 工具定义列表，格式遵循 OpenAI tool schema |
| `tool_choice` | string/object | 否 | 控制工具调用策略，可选 `"auto"`、`"none"` 或指定 tool |
| `max_tokens` | integer | 否 | 输出最大 token 数，范围 1–4096 |

## 使用方式

1. **鉴权**：使用阿里云 STS Token 或长期 AK/SK，通过 `Authorization: Bearer <token>` 或 `X-Aliyun-ACS-AccessKey-ID` + `X-Aliyun-ACS-AccessKey-Secret` 头传递凭证；具体授权流程见 [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)。  
2. **请求示例**（cURL）：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "qwen-max",
           "messages": [{"role": "user", "content": "你好"}]
         }'
   ```
3. **响应解析**：成功响应包含 `output.text`（非流式）或 `output.choices[0].delta.content`（流式），错误码遵循标准 HTTP 状态码及 `code` 字段（如 `InvalidParameter.ModelNotAuthorized`）。

## 限制和注意事项

- 单次请求 `messages` 总长度上限为 32768 tokens（含 system [prompt](../guides/prompt.md)）；超出将返回 `400 Bad Request`。
- 异步任务（`/v1/async_tasks`）最长保留结果 7 天，超期后不可查询。
- `tools` 调用返回的 `tool_calls` 中 `id` 字段在部分旧版 SDK 中可能为空，建议始终校验 `function.name` 和 `function.arguments`；此行为差异已在 [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md) 的 v20240315 更新中明确修复。

## 来源文档

- [应用组件](../../raw/application-api-reference/application-component-api-reference.md)


