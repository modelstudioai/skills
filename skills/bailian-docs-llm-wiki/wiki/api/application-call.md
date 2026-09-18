# application call

`application call` 是百炼平台提供的核心 API 接口，用于以编程方式触发已部署应用的执行流程，将用户输入传递给应用并获取结构化响应。该接口支持多种调用协议（如 DashScope 兼容格式、OpenAI 兼容格式），适用于集成到业务系统、Agent 编排或自动化工作流中。详细行为和兼容性请参考 [应用调用](../../raw/application-api-reference/application-call.md)。

## 支持的模型/功能

- 所有在百炼控制台「应用」模块中成功发布（Published）的应用均可被调用；
- 支持调用基于大语言模型（LLM）、RAG 增强、工具调用（Tool Calling）或多步骤工作流构建的应用；
- 同时提供两种协议风格：  
  - DashScope 兼容协议（推荐用于百炼原生生态，支持流式响应、[函数调用](../concepts/function-calling.md)等高级能力）；  
  - OpenAI 兼容 Responses API（适配已有 OpenAI 客户端，但部分百炼特有能力受限）。  
  协议差异详见 [DashScope API](../../raw/application-api-reference/application-call/application-dashscope-api-reference.md) 和 [Responses API](../../raw/application-api-reference/application-call/openai-responses-api.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，需通过 [获取APP ID 和 Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 获取 |
| `workspace_id` | string | 是 | 工作空间 ID，与 `app_id` 成对使用，确保权限上下文正确 |
| `input` | object | 是 | 用户输入内容，格式为 `{ "text": "..." }` 或带多模态字段（如 `image_url`）的扩展对象 |
| `stream` | boolean | 否 | 默认 `false`；设为 `true` 时启用 SSE 流式响应（仅 DashScope 协议支持） |
| `parameters` | object | 否 | 覆盖应用配置中的运行时参数（如 `temperature`, `max_tokens`） |

> **注意**：`input` 字段在 OpenAI 兼容 API 中需映射为 `messages` 数组（如 `[{"role":"user","content":"..."}]`），该差异已在 [Responses API](../../raw/application-api-reference/application-call/openai-responses-api.md) 中明确定义，但与 [DashScope API](../../raw/application-api-reference/application-call/application-dashscope-api-reference.md) 的 `input` 结构不兼容，请勿混用。

## 使用方式

1. 确保应用状态为 **Published**，且调用方具备对应 `workspace_id` 的 `AppCaller` 权限；
2. 构造 HTTP POST 请求，目标 URL 为 `https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/call`（DashScope 协议）或 `https://dashscope.aliyuncs.com/v1/chat/completions`（OpenAI 协议）；
3. 设置请求头：`Authorization: Bearer <api_key>`，`Content-Type: application/json`；
4. 发送 JSON body（以 DashScope 协议为例）：
   ```json
   {
     "input": {"text": "总结这篇文档的核心要点"},
     "parameters": {"temperature": 0.3},
     "stream": false
   }
   ```
   更多示例见 [应用调用](../../raw/application-api-reference/application-call.md)。

## 限制和注意事项

- 单次调用最大 `input.text` 长度为 100,000 字符（含上下文）；超出将返回 `400 Bad Request`；
- 流式响应（`stream=true`）仅在 DashScope 协议下可用，OpenAI 协议不支持 SSE；
- 调用失败时，错误码与语义遵循 [DashScope API](../../raw/application-api-reference/application-call/application-dashscope-api-reference.md) 定义，而非 OpenAI 标准；
- Workspace ID 必须与 App ID 所属工作空间一致，跨 workspace 调用将被拒绝（即使 API Key 有效）；
- 应用若启用了敏感信息过滤或合规拦截，响应中可能包含 `filtered` 字段，需在客户端主动处理。

## 来源文档

- [应用调用](../../raw/application-api-reference/application-call.md)


