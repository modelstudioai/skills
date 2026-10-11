# bailian [application call](../api/application-call.md)ing

百炼平台支持通过 API 方式调用已发布的智能体应用（Agent Application）和工作流应用（Workflow Application），实现与业务系统的深度集成。调用过程需使用有效的 API Key，并遵循统一的 HTTP 接口规范。所有应用调用均基于 RESTful 设计，返回结构化 JSON 响应。

## 支持的模型/功能

- **智能体应用**：支持单轮对话、多轮会话保持（需传入 `session_id`），适用于客服助手、知识问答等场景。详见 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)。
- **工作流应用**：支持串行/并行节点编排，可调用多个工具或模型组合执行复杂任务，如数据清洗+分析+报告生成。详见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
- 所有应用均支持参数透传（如 `user_id`、`tenant_id` 等上下文字段），用于权限控制或日志追踪。具体规则见 [应用的参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `application_id` | string | 是 | 应用唯一标识，可在控制台「应用管理」中获取 |
| `input` | object | 是 | 用户输入内容，结构由应用定义（通常为 `{ "query": "..." }` 或自定义 schema）|
| `session_id` | string | 否 | 用于多轮会话状态维持；智能体应用推荐传入，工作流应用忽略该字段 |
| `parameters` | object | 否 | 透传参数，将注入应用运行时上下文，格式需与 [应用的参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md) 一致 |

> **注意**：部分旧版文档示例中将 `parameters` 误写为 `extra_parameters`，实际接口仅接受 `parameters` 字段，以 [应用的参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md) 中的最新定义为准。

## 使用方式

1. 获取 API Key（需在「API 密钥管理」中创建，且对应账号具备目标应用的调用权限）；
2. 构造 POST 请求，Header 设置 `Authorization: Bearer <API_KEY>` 和 `Content-Type: application/json`；
3. Body 示例：
   ```json
   {
     "application_id": "app-abc123",
     "input": { "query": "今天北京天气如何？" },
     "session_id": "sess-xyz789",
     "parameters": { "user_id": "u_456", "locale": "zh-CN" }
   }
   ```
4. 发送至 `https://dashscope.aliyuncs.com/api/v1/applications/<application_id>/invoke`

## 限制和注意事项

- 单次请求 `input` 内容长度上限为 100,000 字符；超出将返回 `400 Bad Request`；
- 智能体应用默认超时时间为 30 秒，工作流应用为 120 秒，不可配置；
- `session_id` 为空字符串或 `null` 时，系统将自动分配新会话，不复用历史上下文；
- 调用失败时，响应体中 `code` 字段为平台错误码（如 `InvalidParameter`），而非模型内部错误；详细错误分类参考 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md) 和 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md) 的错误处理章节。

## 来源文档

- [应用调用](../../raw/application-user-guide/bailian-application-calling.md)


