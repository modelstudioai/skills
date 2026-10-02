# support

`support` 是百炼平台为开发者提供的模型服务支持能力入口，涵盖模型可用性、功能覆盖范围、调用参数规范及服务边界说明。它不提供实时人工客服，而是通过结构化文档与自助工具帮助开发者快速定位问题、理解限制并完成集成。所有支持信息均以平台当前控制台和 API 行为为准，历史文档可能滞后。

## 支持的模型/功能

当前支持的模型列表详见 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md)，该文档按模型类型（基础大模型、多模态、嵌入、推理优化等）分类，并标注各模型在百炼控制台、API 及 SDK 中的可用状态。功能层面，`support` 覆盖模型调用、异步任务管理、流式响应、[Token](../concepts/token.md) 统计与错误码解析；但**不支持**模型微调过程中的实时日志透出或训练中断恢复——此类能力需通过 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 中定义的工单通道申请专项支持。

> **注意**：[模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中标注“Beta”的模型，其 API 接口稳定性与参数行为可能随版本迭代变更，不承诺向后兼容；而 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 中部分示例仍引用已下线的旧版 endpoint，实际开发请以控制台「API 调试」页生成的最新请求为准。

## 关键参数

调用 `support` 相关接口（如 `/v1/models/{model_id}/invoke`）时，必需参数包括 `model_id`（严格匹配 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中的 ID 字符串）、`input`（JSON 格式，结构依模型而异）和 `api_key`（平台颁发的密钥）。可选参数含 `stream`（布尔值，控制是否启用流式）、`max_tokens`（整数，硬性截断上限）及 `temperature`（仅对生成类模型生效）。所有参数名区分大小写，未声明的字段将被静默忽略。

## 使用方式

1. 登录百炼控制台 → 进入「模型服务」→ 选择目标模型 → 点击「API 调试」获取实时 cURL 示例；  
2. 在代码中构造 HTTP POST 请求，Header 必须包含 `Authorization: Bearer ${API_KEY}` 和 `Content-Type: application/json`；  
3. 响应体为标准 JSON，含 `output`（结果）、`usage`（token 消耗）和 `request_id`（用于问题排查）。调试过程中若遇 `400 Bad Request`，优先对照 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 中的参数校验清单自查。

## 限制和注意事项

- 单次请求 `input` 内容长度上限为 128KB（文本）或 10MB（二进制，如图像 base64）；  
- 异步任务最长保留 7 天，超期后 `request_id` 不再可查；  
- 免费额度用户无法调用部分商用模型（如 qwen-max），具体禁用列表见 [相关协议](../../raw/model-user-guide/support/related-agreements.md) 附录；  
- 所有错误响应均遵循 RFC 7807 标准，`type` 字段指向 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 中对应条目编号，便于快速检索解决方案。

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


