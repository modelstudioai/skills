# application call

`application call` 是百炼平台提供的核心 API 接口，用于以编程方式调用已部署的 AI 应用（App），将用户输入传递给应用工作流并获取结构化响应。该接口支持同步调用模式，适用于集成到后端服务、自动化脚本或低延迟交互场景。调用需通过 HTTP POST 请求发起，并依赖有效的认证凭证与正确的参数配置。

## 支持的模型/功能

`application call` 本身不直接绑定特定基础模型，而是执行已配置在应用中的完整工作流——该工作流可包含 LLM 调用、工具调用、条件分支、数据预处理等节点。因此，实际使用的模型取决于应用创建时所选的 [DashScope API](../../raw/application-api-reference/application-call/application-dashscope-api-reference.md) 后端（如 qwen-max、qwen-plus）或 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)。注意：若应用启用了 RAG [插件](../concepts/plugin.md)或自定义函数，这些能力也将随调用自动生效。

> **注意**：部分旧版文档提及“仅支持 qwen 系列模型”，但根据最新 [Responses API](../../raw/application-api-reference/application-call/openai-responses-api.md) 规范，OpenAI 兼容模式下亦支持 `gpt-4o` 等第三方模型标识（需平台白名单配置），该能力已在 v2.3+ 版本中正式启用。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，需通过 [获取APP ID 和 Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 获取 |
| `input` | object | 是 | 用户输入内容，结构由应用 Schema 定义，常见字段如 `query`、`files`、`user_id` |
| `workspace_id` | string | 否 | 工作区 ID；若未提供，则使用 `app_id` 所属默认工作区（见 [获取APP ID 和 Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)） |
| `stream` | boolean | 否 | 是否启用流式响应，默认 `false`；设为 `true` 时需按 SSE 格式解析 |
| `parameters` | object | 否 | 覆盖应用级默认参数，如 `temperature`、`max_tokens` 等，具体字段依底层模型而定 |

## 使用方式

1. 获取 `app_id` 和（可选）`workspace_id`（参见 [获取APP ID 和 Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)）  
2. 构造 JSON 请求体，确保 `input` 符合应用定义的输入 Schema  
3. 发送 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/call`，携带 `Authorization: Bearer <api_key>`  
4. 解析响应：成功时返回 `output` 对象；错误时检查 `code` 与 `message` 字段（详见 [DashScope API](../../raw/application-api-reference/application-call/application-dashscope-api-reference.md) 错误码表）

## 限制和注意事项

- 单次请求 `input` 总大小上限为 10 MB（含文本与 Base64 编码文件）  
- 同步调用超时时间为 120 秒；流式调用建议客户端设置 300 秒连接保活  
- `app_id` 必须属于调用方有权限访问的工作区，跨工作区调用需显式传入 `workspace_id`  
- 若应用启用了敏感信息过滤或合规审查，响应可能被截断或替换，此行为不可绕过  

> **注意**：文档中曾存在关于 `stream=true` 时 `output` 字段结构的不一致描述——[DashScope API](../../raw/application-api-reference/application-call/application-dashscope-api-reference.md) 明确要求流式响应为 chunked SSE，而 [Responses API](../../raw/application-api-reference/application-call/openai-responses-api.md) 示例中混用了非标准 JSON 数组格式。请以 DashScope API 文档为准，忽略 Responses API 中的数组示例。

## 来源文档

- [应用调用](../../raw/application-api-reference/application-call.md)


