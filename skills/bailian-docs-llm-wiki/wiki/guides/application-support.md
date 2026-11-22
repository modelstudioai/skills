# application [support](support.md)

`application support` 是百炼平台为应用层调用提供的基础服务支持能力，涵盖模型接入、功能扩展、参数配置与生命周期管理等核心环节。它面向开发者提供统一的 API 接口和 SDK 封装，用于构建生产级 AI 应用。该能力依赖平台底层模型服务与资源调度系统，需配合具体模型规格与配额策略使用。

## 支持的模型/功能

- 支持调用百炼平台全部已上线的 [通义千问系列大模型](../../raw/application-user-guide/application-support.md)（如 Qwen1.5、Qwen2、Qwen2.5），以及部分专用小模型（如 Qwen-Audio、Qwen-VL）；
- 提供标准推理（`chat/completions`）、流式响应、[函数调用](../concepts/function-calling.md)（Function Calling）、工具集成（Tools）等核心功能；
- 支持通过 `application_id` 绑定专属模型版本、提示词模板及后处理规则，实现应用级模型治理 —— 具体配置方式详见 [售后说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `application_id` | string | 是 | 应用唯一标识，由控制台创建应用时生成，用于路由至对应模型实例与配置 |
| `model` | string | 否 | 显式指定模型 ID（如 `qwen-max`）；若未传，则使用该 `application_id` 绑定的默认模型 |
| `stream` | boolean | 否 | 默认 `false`；设为 `true` 时启用 SSE 流式响应 |
| `tools` | array | 否 | [函数调用](../concepts/function-calling.md)所需工具定义列表，格式遵循 OpenAI 兼容规范 |

> **注意**：文档 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 中提及 `model` 参数“可覆盖应用绑定模型”，但实测中若应用已启用模型灰度发布策略，该覆盖行为可能被平台拦截 —— 建议优先通过控制台调整绑定模型，而非运行时覆盖。

## 使用方式

1. 在百炼控制台创建应用，获取 `application_id`；
2. 使用 SDK（如 `dashscope` Python SDK v1.20.0+）或直接调用 `/v1/applications/{application_id}/chat/completions` 接口；
3. 构造请求体，至少包含 `messages` 字段（格式同 OpenAI），并按需传入 `stream`、`tools` 等参数；
4. 处理响应：非流式返回标准 JSON；流式响应需按 SSE 协议解析 `data:` 行 —— 完整协议细节参见 [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)。

## 限制和注意事项

- 单次请求 `messages` 总 token 数上限为 32768（含 system、user、assistant 内容），超出将返回 `400 Bad Request`；
- 每个 `application_id` 默认共享所属项目配额，不单独限流；高并发场景需提前申请配额扩容；
- 不支持跨 region 调用：`application_id` 仅在其创建时指定的地域（如 `cn-beijing`）内有效；
- 若应用绑定的是私有微调模型，其输入/输出内容受企业版数据隔离策略约束，不可与公有模型混用 —— 此限制在 [售后说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 中有明确界定。

## 来源文档

- [服务支持](../../raw/application-user-guide/application-support.md)


