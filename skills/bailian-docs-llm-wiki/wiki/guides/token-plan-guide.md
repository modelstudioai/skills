# token plan guide

[Token](../concepts/token.md) Plan 是百炼平台为模型调用提供的配额管理机制，用于控制 API 请求的 token 消耗额度、速率及生命周期。开发者可通过 [Token](../concepts/token.md) Plan 实现细粒度的资源隔离、成本管控与服务分级。该机制适用于所有支持按 token 计费的模型调用场景。

## 支持的模型/功能

[Token](../concepts/token.md) Plan 当前支持以下模型类型和功能：
- 所有百炼托管的 `qwen-*` 系列大模型（如 `qwen-max`, `qwen-plus`, `qwen-turbo`）
- `lingji-*` 系列[多模态](../concepts/multimodal.md)模型（需开启 `enable_multimodal=true`）
- 流式响应（`stream=true`）与非流式响应均受同一 Token Plan 约束
- 不支持[函数调用](../concepts/function-calling.md)（Function Calling）独立配额，其 token 消耗计入主 Plan；详见 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)

## 关键参数

创建或更新 Token Plan 时需配置以下必选参数：

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `quota` | integer | 总配额（单位：token），最小值为 1000，最大值为 100_000_000 |
| `rate_limit` | integer | 每秒最大 token 消耗量（TPS），范围 1–10000 |
| `valid_until` | string (ISO 8601) | 过期时间，最长支持 365 天后，不支持永久有效 |

> **注意**：`rate_limit` 单位为 *token per second*，而非 request per second；部分旧文档误标为 QPS，应以 [进阶配置](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md) 中定义为准。

## 使用方式

1. **创建 Plan**：调用 `POST /v1/token-plans`，传入上述参数；
2. **绑定到 API Key**：在创建 API Key 时通过 `token_plan_id` 字段指定，或后续通过 `PATCH /v1/api-keys/{id}` 更新；
3. **验证生效**：发起模型请求时，若请求头含 `Authorization: Bearer <api_key>`，且该 key 已绑定有效 Plan，则自动启用配额校验；
4. **查询用量**：调用 `GET /v1/token-plans/{id}/usage` 获取实时消耗统计（延迟 ≤ 3s）。

所有操作均需具备 `token_plan:manage` 权限；详细流程见 [个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal.md) 和 [团队版](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition.md) 文档。

## 限制和注意事项

- 单个 API Key 仅可绑定一个 Token Plan；解绑后需重新绑定才生效；
- Token Plan 不支持跨项目（project）复用，每个 project 需独立创建；
- 配额按自然日重置（UTC+0），非按创建时间滚动周期；
- 当 `quota` 耗尽时，请求将返回 `429 Too Many Requests`，响应头含 `X-RateLimit-Remaining: 0`；
- 图像输入（base64 或 URL）的 token 计算方式与文本不同，具体规则参见 [Coding Plan](../../raw/model-user-guide/token-plan-guide/coding-plan-guide.md) 中的 multimodal tokenization 表格。

## 来源文档

- [Token Plan](../../raw/model-user-guide/token-plan-guide.md)


