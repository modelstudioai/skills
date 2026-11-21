# application component api reference

应用组件 API 提供了百炼平台中可复用业务能力的标准化调用接口，用于在自定义应用中集成对话、知识检索、工作流编排等核心功能。该 API 采用 RESTful 设计，支持 HTTPS 调用与 RAM 凭据鉴权。所有接口均需通过指定服务接入点访问，并遵循统一的请求/响应结构。

## 支持的模型与功能

当前应用组件 API 支持以下核心能力：
- **对话交互**：调用 `chat` 接口发起多轮会话，支持流式响应（`stream=true`）；
- **知识检索增强（RAG）**：通过 `retrieve` 接口对接已配置的知识库，返回相关文档片段；
- **工作流执行**：使用 `run_workflow` 触发预设的可视化工作流，支持传入动态输入参数。

> **注意**：[API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md) 中列出的 `generate_image` 接口已在 v2.1.0 版本中移除，实际调用将返回 `404 Not Found`；请参考 [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md) 确认废弃项。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，由控制台创建应用时生成，见 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md) 文档中的示例 |
| `model` | string | 否 | 指定底层模型（如 `qwen-max`, `qwen-plus`），未指定时使用应用默认模型 |
| `stream` | boolean | 否 | 默认 `false`；设为 `true` 时启用 SSE 流式响应 |
| `input` | object | 是 | 用户输入内容，结构依接口类型而异（如 `chat` 接口要求 `messages` 数组） |

## 使用方式

1. 获取 `app_id` 和 `access_token`（通过 RAM 角色临时凭证或 API Key，详见 [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)）；  
2. 构造请求 URL：`POST https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/chat`（以 chat 为例）；  
3. 设置 Header：`Authorization: Bearer ${access_token}`，`Content-Type: application/json`；  
4. 发送 JSON Body，例如：
   ```json
   { "input": { "messages": [{ "role": "user", "content": "你好" }] } }
   ```

## 限制和注意事项

- 单次请求 `input.messages` 最多支持 50 条历史消息，总 token 数上限为 32768（含 system prompt）；  
- 流式响应（`stream=true`）下，客户端必须正确处理 `text/event-stream` MIME 类型及 `data:` 前缀格式；  
- 所有接口均受百炼平台配额限制，超出后返回 `429 Too Many Requests`，建议实现指数退避重试；  
- 应用组件 API 不支持跨地域调用：`app_id` 所属地域必须与请求接入点地域一致（参见 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)）。

## 来源文档

- [应用组件](../../raw/application-api-reference/application-component-api-reference.md)


