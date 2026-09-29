# application component api reference

应用组件 API 提供了百炼平台中可复用业务能力的标准化调用接口，用于在自定义应用中集成对话、知识检索、工作流编排等核心功能。该 API 采用 RESTful 设计，支持 HTTPS 调用，并依赖 RAM 授权与 OpenAPI 签名机制进行身份验证。所有接口均需通过指定服务接入点访问，且版本兼容性遵循语义化版本规则。

## 支持的模型/功能

当前应用组件 API 支持以下核心能力：
- **对话交互**：基于 `bailian-v1` 模型系列（如 `qwen-max`, `qwen-plus`）的多轮会话管理；
- **知识增强**：绑定知识库 ID 后启用 RAG 检索，支持结构化文档与非结构化文本混合召回；
- **工作流执行**：调用预置或用户自定义的 workflow ID，支持同步返回与异步回调两种模式。  
详细能力列表请参见 [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，必须为 [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md) 中列出的有效值（如 `qwen-max`）；不支持任意字符串传入。 |
| `input.messages` | array | 是 | 对话消息数组，每项含 `role`（`user`/`assistant`/`system`）和 `content` 字段；`system` 角色仅允许首条消息使用。 |
| `parameters.knowledge_id` | string | 否 | 绑定知识库 ID，需已在控制台创建并发布；该字段生效需同时设置 `parameters.enable_knowledge` 为 `true`。 |
| `parameters.workflow_id` | string | 否 | 工作流唯一标识，须与 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md) 中定义的 workflow 兼容。 |

> **注意**：`parameters.knowledge_id` 在 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md) 文档中被错误标注为“可选但推荐”，实际为启用知识增强功能的强制依赖字段，以 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md) 的定义为准。

## 使用方式

1. **认证**：使用 RAM 子账号 AccessKey（AK/SK）按 OpenAPI v1 签名规范生成 `Authorization` 头；
2. **请求地址**：构造 `POST https://{endpoint}/api/v1/applications/{app_id}/components/chat`（其他组件路径见 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)）；
3. **请求体**：JSON 格式，包含 `model`、`input` 及可选 `parameters` 字段；
4. **响应解析**：成功时返回 `200 OK`，`output.choices[0].message.content` 为模型输出正文。

## 限制和注意事项

- 单次请求 `input.messages` 最多支持 50 条历史消息，总 token 数上限为模型 context 长度的 90%；
- 知识库检索默认返回 Top-3 片段，不可配置；若需调整，须改用独立 Knowledge API；
- 异步工作流执行最大超时时间为 300 秒，超时后返回 `504 Gateway Timeout`；
- 所有参数校验逻辑以 [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md) 中最新版为准，旧版文档中未声明的参数将被静默忽略。

## 来源文档

- [应用组件](../../raw/application-api-reference/application-component-api-reference.md)


