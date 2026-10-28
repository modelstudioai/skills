# token plan guide

[Token](../concepts/token.md) Plan 是百炼平台为模型调用设计的资源配额与计费管理机制，用于控制 API 调用频次、并发量及总 token 消耗量。开发者需根据业务场景选择对应计划，并在请求中显式声明 `plan` 参数以生效配额策略。该机制与模型选型、请求参数强耦合，配置错误将导致 403 或 429 错误。

## 支持的模型/功能

[Token](../concepts/token.md) Plan 当前覆盖全部百炼托管模型（含 Qwen 系列、Qwen-VL、Qwen-Audio）及部分第三方模型接入通道。**不支持**自定义训练模型（Fine-tuning Job）或私有部署实例的 token 配额管理。具体兼容性请参考 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md) 中的“适用模型列表”章节。Coding Plan 作为独立子类，仅适用于 `/v1/coding/completions` 接口，详见 [Coding Plan](../../raw/model-user-guide/token-plan-guide/coding-plan-guide.md)。

## 关键参数

- `plan`: 必填字符串，取值为 `personal`、`team` 或 `coding`（大小写敏感）  
- `model`: 必填，需与所选 plan 兼容（例如 `qwen-max` 不支持 `personal` plan）  
- `max_tokens`: 受 plan 总配额限制，超出时请求被截断并返回 `truncated` 标志  
- `temperature` / `top_p` 等采样参数不影响配额计算，但影响实际 token 消耗量  

> **注意**：原始文档 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md) 中提到 `plan` 可省略默认使用 `personal`，但实测 v3.2+ 版本 API 已强制要求显式传入，否则返回 `400 Missing plan parameter` —— 请以 [进阶接入](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md) 的最新示例为准。

## 使用方式

1. 在 API 请求 Header 中添加 `Authorization: Bearer <api_key>`  
2. 在 JSON Body 中指定 `plan` 和 `model`（例如 `"plan": "team", "model": "qwen-plus"`）  
3. 调用 `/v1/chat/completions` 或 `/v1/coding/completions` 等受控接口  
4. 通过 `/v1/usage/token-plan` 查询当前 plan 的剩余配额（需额外权限）  

## 限制和注意事项

- 同一 API Key 下，不同 plan 的配额**不共享**；切换 plan 后历史消耗不累计  
- `personal` plan 仅限个人开发者账号，企业主体调用将被拒绝（即使 API Key 有效）  
- 所有 plan 均按自然日重置配额，UTC+0 时间 00:00 开始，非北京时间  
- 流式响应（`stream: true`）的 token 计费以实际返回的 token 数为准，非预估量  
- 若请求中 `model` 与 `plan` 不匹配（如用 `personal` 调用 `qwen-turbo`），API 将直接拒绝，而非降级处理  

> **注意**：[个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal.md) 文档中列出的免费额度为 2023 年旧版政策，当前已统一调整为 1000 tokens/日（新注册账号首月加倍），请以控制台实时显示为准。

## 来源文档

- [Token Plan](../../raw/model-user-guide/token-plan-guide.md)


