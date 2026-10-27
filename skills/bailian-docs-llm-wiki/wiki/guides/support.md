# support

`support` 是百炼平台为模型调用和管理提供的基础服务支持能力，涵盖模型可用性、功能边界、调用参数约束及售后响应机制。开发者可通过该服务确认所选模型是否受支持、了解关键配置项限制，并获取故障排查与服务保障依据。所有支持范围均以最新发布的官方文档为准。

## 支持的模型/功能

当前支持的模型列表详见 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md)，该文档按模型类型（如大语言模型、多模态模型、Embedding 模型）和上线状态（公测/正式/下线）分类维护。功能支持包括同步推理、流式响应、批量调用及部分模型的自定义 stop token 配置。不支持的功能（如[模型微调](../concepts/model-fine-tuning.md)触发、私有部署实例直连）在 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 中明确排除。

## 关键参数

- `model`: 必填，值必须来自 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中的 `model_id` 字段，大小写敏感；
- `temperature`: 范围 0.0–2.0，超出将被截断并返回警告（非报错），详见 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)；
- `max_tokens`: 默认值因模型而异，最大允许值由模型自身能力决定，不可超过 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中标注的 `max_output_tokens` 上限。

## 使用方式

通过 `/v1/chat/completions` 或 `/v1/embeddings` 等标准 API 端点发起 HTTP POST 请求，需携带有效 API Key 及符合要求的 JSON payload。请求头必须包含 `Content-Type: application/json`；未认证或签名失效时返回 `401 Unauthorized`。完整调用示例与错误码说明见 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)。

## 限制和注意事项

- 单次请求最大上下文长度（input + output tokens）受模型硬性限制，超限将直接拒绝，不进行自动截断；
- 免费试用额度仅适用于指定模型（见 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中 `free_tier_eligible` 标记），且不覆盖 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 中定义的付费服务场景；
> **注意**：原始文档中 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 提到“`top_p` 参数默认为 1.0”，但 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中多个新上线模型实际默认值为 0.95 —— 请以模型列表中标注的默认值为准。

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


