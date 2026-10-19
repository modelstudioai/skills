# support

`support` 是百炼平台为模型调用和管理提供的基础服务支持能力，涵盖模型可用性、功能边界、参数配置及售后保障等维度。开发者可通过该服务确认所选模型是否受支持、了解调用限制，并获取故障响应与服务范围说明。所有支持信息均以官方文档为准，建议结合具体模型文档交叉验证。

## 支持的模型/功能

当前支持的模型列表详见 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md)，该文档按模型类型（如大语言模型、多模态模型）、部署形态（API/SDK/控制台）及商用状态分类维护。功能支持范围包括同步推理、流式响应、批量调用及部分模型的微调后服务接入。注意：[常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 中提及的“历史对话上下文自动截断”功能，仅适用于 `qwen-max` 和 `qwen-plus`，其他模型需自行实现 truncation 逻辑。

## 关键参数

调用支持服务相关接口时，关键参数包括 `model`（必填，值须来自 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中的正式模型标识）、`timeout`（单位秒，默认 60，最大 300）和 `enable_tracing`（布尔值，启用后返回 trace_id 用于问题定位）。参数校验严格，传入未列明的 `model` 值将直接返回 `400 Bad Request`。

## 使用方式

通过百炼 SDK 或 REST API 调用 `/v1/support` 端点可查询服务健康状态与模型就绪情况；实际模型调用则使用 `/v1/chat/completions` 等标准路径，其可用性依赖 `support` 层返回的模型状态。初始化 SDK 时需指定 `region` 和 `access_key`，区域信息应与 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 中约定的服务覆盖范围一致。

## 限制和注意事项

- 单账户默认并发调用上限为 100 QPS，超出需提工单申请扩容；
- 免费试用模型不享受 SLA 保障，具体承诺见 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md)；
- > **注意**：[相关协议](../../raw/model-user-guide/support/related-agreements.md) 中关于“不可抗力导致的服务中断免责”条款，与 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 第 3.2 条“99.9% 月度可用性承诺”存在表述冲突，以最新版 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 为准；
- 模型下线前至少提前 30 天公告，下线模型无法再发起新调用，存量请求仍可完成。

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


