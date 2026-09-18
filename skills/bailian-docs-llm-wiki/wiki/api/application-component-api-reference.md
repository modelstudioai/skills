# application component api reference

应用组件 API 提供了在百炼平台中集成和调用预置能力（如对话、知识检索、工具调用等）的标准接口，适用于构建企业级 AI 应用。该 API 以 RESTful 形式提供，支持同步响应与[流式输出](../concepts/streaming-output.md)，需通过 RAM 授权访问。所有接口均基于统一的服务接入点，版本演进遵循语义化规范。

## 支持的模型/功能

当前应用组件 API 支持以下核心能力：  
- 基于 `bailian-v1` 模型的多轮对话（含上下文管理）；  
- 知识库增强问答（RAG），支持向量检索与重排；  
- 工具调用（Tool Calling），可对接自定义 HTTP 工具或平台内置函数；  
- 输出结构化 JSON（需显式设置 `response_format: "json_object"`）。  
详细能力列表见 [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md)。

## 关键参数

必填参数包括：  
- `model`: 必须为 `bailian-v1`（暂不支持其他模型别名）；  
- `input.messages`: 非空消息数组，格式同 OpenAI ChatML；  
- `parameters.temperature`: 范围 `[0.0, 2.0]`，默认 `0.8`；  
- `parameters.top_p`: 范围 `[0.0, 1.0]`，默认 `0.95`；  
- `parameters.max_tokens`: 最大输出 token 数，上限 `4096`（超出将被截断）。  
授权与端点配置详见 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md) 和 [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)。

## 使用方式

1. 通过 RAM 角色获取 `bailian:InvokeApplicationComponent` 权限；  
2. 构造 POST 请求至 `/v1/applications/{app_id}/chat/completions`（`app_id` 为控制台创建的应用唯一标识）；  
3. 设置 `Content-Type: application/json` 与 `Authorization: Bearer <access_token>`；  
4. 示例请求体参考 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md) 中的 `curl` 片段。

## 限制和注意事项

- 单次请求最大 `input.messages` 长度为 32768 tokens（含 system + user + assistant 消息）；  
- 流式响应（`stream: true`）仅支持 SSE 格式，不兼容 WebSocket；  
- `tool_choice` 参数若设为 `"auto"`，系统可能忽略部分工具描述字段 —— 此行为与 [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md) 中 v2024.03 的变更描述存在偏差；  
> **注意**：文档 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md) 中示例使用的 `model: qwen-max` 已过时，实际仅接受 `bailian-v1`，请以 [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md) 为准；  
> **注意**：[授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md) 中列出的 `bailian:ListApplications` 权限非调用必需，仅用于控制台管理。

## 来源文档

- [应用组件](../../raw/application-api-reference/application-component-api-reference.md)


