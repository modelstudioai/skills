# support

`support` 是百炼平台为模型调用和服务使用提供的综合性支持能力，涵盖模型兼容性、功能覆盖范围、关键配置参数及服务边界说明。开发者可通过该模块快速确认所选模型是否受支持、了解调用限制，并获取售后与合规依据。所有支持信息均以官方文档为准，建议结合具体场景查阅对应子文档。

## 支持的模型/功能

当前 `support` 模块覆盖百炼平台全部公开可调用模型，包括通义千问系列（Qwen1、Qwen2、Qwen3）、Qwen-VL、Qwen-Audio 等多模态与语言模型，以及部分第三方接入模型。模型清单以 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 为准，该文档按模型类型、版本、部署状态和推理能力维度结构化呈现，是判断模型是否可用于生产环境的核心依据。

## 关键参数

调用受支持模型时，需关注以下关键参数：
- `model`：必须与 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中公布的模型 ID 完全一致（区分大小写与连字符）；
- `max_tokens`：不同模型有独立上限，超出将触发 `400 Bad Request`，具体值请参考对应模型的规格说明；
- `stream`：仅部分模型支持流式响应，不支持时强制设为 `true` 将导致请求失败；该兼容性信息同样在 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中明确标注。

## 使用方式

通过百炼 API 调用支持的模型时，无需额外启用 `support` 功能开关，其能力内置于模型服务网关中。开发者只需确保：
- 请求 Header 中携带有效的 `Authorization` 凭据；
- 请求 Body 符合目标模型的输入 schema（如 `messages` 格式或 `input` 字段）；
- 模型 ID 和参数组合已在 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 所列的服务范围内。

> **注意**：部分旧版文档提及“需在控制台开启 Support Mode”，该描述已过时；实际无需任何手动开启操作，相关说明已被 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 明确废止。

## 限制和注意事项

- 免费试用额度仅适用于 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 中明确列出的模型与调用方式，非列表内模型不享受试用配额；
- 模型下线前至少提前 30 天公告，下线后即使 API 仍可调用，也将返回 `410 Gone`，历史调用记录不计入售后服务周期；
- 跨地域调用（如华东1区应用调用华北2区部署的模型）可能引发延迟升高或鉴权失败，此类场景需严格遵循 [相关协议](../../raw/model-user-guide/support/related-agreements.md) 中关于服务区域约束的条款。

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


