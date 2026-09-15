# application component api reference

应用组件 API 提供了百炼平台中可复用业务能力的标准化调用接口，用于在自定义应用中集成对话、知识检索、工作流编排等核心功能。该 API 采用 RESTful 设计，支持 HTTPS 调用与 RAM 凭据鉴权。所有接口均需通过指定服务接入点访问，并遵循统一的请求/响应结构。

## 支持的模型与功能

当前应用组件 API 支持以下核心能力：
- **对话交互**：调用 `chat` 接口发起多轮会话，支持流式响应（`stream=true`）；
- **知识检索增强（RAG）**：通过 `retrieve` 接口对接已配置的知识库，返回相关文档片段；
- **工作流执行**：使用 `run_workflow` 触发预设的可视化工作流，支持传入动态输入参数。

> **注意**：`retrieve` 接口在 [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md) 中列为 Beta 功能，但 [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md) 明确标注其已于 v2.1.0 正式 GA，建议以 [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md) 为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，由控制台创建应用时生成 |
| `model_id` | string | 否 | 指定后端模型（如 `qwen-max`），若不填则使用应用默认模型 |
| `stream` | boolean | 否 | 默认 `false`；设为 `true` 时启用 SSE 流式响应 |
| `input` | object | 是（除 `retrieve` 外） | 用户输入内容，结构依接口而异（如 `chat` 中为 `{ "messages": [...] }`） |

## 使用方式

1. 获取 `app_id` 和 `access_token`（通过 [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md) 中描述的 RAM 角色凭证或短期 [Token](../concepts/token.md)）；  
2. 构造请求 URL：`POST https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/[chat|retrieve|run_workflow]`；  
3. 设置 Header：`Authorization: Bearer {access_token}`，`Content-Type: application/json`；  
4. 发送 JSON Body（参考 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md) 中各接口示例）。

## 限制和注意事项

- 单次 `chat` 请求最大 `messages` 数量为 50 条，总 token 上限取决于所选模型（详见对应模型文档）；  
- `retrieve` 接口单次最多返回 10 个文档片段，且仅支持已发布状态的知识库；  
- 所有接口均受百炼平台配额管控，超限将返回 `429 Too Many Requests`；  
- 若未显式指定 `model_id`，系统将回退至应用创建时绑定的默认模型，该行为在 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md) 文档中有明确说明。

## 来源文档

- [应用组件](../../raw/application-api-reference/application-component-api-reference.md)


