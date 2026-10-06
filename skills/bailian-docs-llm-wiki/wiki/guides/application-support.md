# application [support](support.md)

`application support` 是百炼平台为应用层调用提供的基础服务支持能力，涵盖模型接入、参数配置、请求调度与售后保障等环节。它面向开发者提供统一的接口抽象和标准化的服务治理机制，适用于构建对话、文本生成、多模态等各类 AI 应用。该能力依托平台底层模型服务框架实现，需配合具体模型 SDK 或 API 调用使用。

## 支持的模型/功能

- 支持调用百炼平台全部已上线的 **大语言模型（LLM）** 和 **多模态模型（如 Qwen-VL）**，包括 `qwen-max`、`qwen-plus`、`qwen-turbo` 等系列；
- 提供 **流式响应（streaming）**、**[函数调用](../concepts/function-calling.md)（function calling）**、**工具集成（tool use）** 等高级功能支持；
- 支持通过 `application_id` 绑定专属模型配置与权限策略，详见 [服务支持](../../raw/application-user-guide/application-support.md) 中的“应用绑定”说明。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `application_id` | string | 是 | 应用唯一标识，由控制台创建应用时生成，用于路由至对应模型实例与配额池 |
| `model` | string | 否 | 显式指定模型 ID（如 `qwen-plus`），若未传则使用应用默认模型；注意：当 `application_id` 已绑定固定模型时，此参数将被忽略 —— 此行为与 [售后说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 中“模型变更支持范围”的描述一致 |
| `stream` | boolean | 否 | 是否启用流式响应，默认 `false`；设为 `true` 时需按 SSE 协议解析响应 |
| `tools` | array | 否 | 工具定义列表，仅在启用[函数调用](../concepts/function-calling.md)时有效；格式需严格遵循 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 中“工具 schema 规范”章节 |

> **注意**：原始文档 [服务支持](../../raw/application-user-guide/application-support.md) 中提及“支持动态切换模型”，但实际运行中 `application_id` 绑定后模型不可运行时变更，该描述已过时；请以控制台应用配置页及 API 实际行为为准。

## 使用方式

1. 在百炼控制台创建应用，获取 `application_id`；
2. 构造 HTTP POST 请求，Endpoint 为 `https://dashscope.aliyuncs.com/api/v1/applications/{application_id}/chat`；
3. 在 Header 中携带 `Authorization: Bearer <api_key>`，Body 中传入标准消息数组（`messages`）及其他关键参数；
4. 解析响应：非流式返回完整 JSON；流式响应需按行解析 `data:` 字段，参考 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 的调试示例。

## 限制和注意事项

- 单次请求 `messages` 长度上限为 100 条，总 token 数受所选模型上下文窗口限制；
- `application_id` 仅对同地域（Region）内调用生效，跨地域需单独部署或使用全局路由开关（需工单开通）；
- 售后支持范围不包含自定义模型微调服务的故障排查，详见 [售后说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)；
- 若应用配置了敏感词过滤或内容安全策略，所有输入/输出将被强制扫描，可能引入额外延迟。

## 来源文档

- [服务支持](../../raw/application-user-guide/application-support.md)


