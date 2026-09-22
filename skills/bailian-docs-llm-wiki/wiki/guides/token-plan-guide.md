# token plan guide

[Token](../concepts/token.md) Plan 是百炼平台为模型调用提供的资源配额管理机制，用于控制 API 调用的 token 消耗总量与速率。开发者可通过 [Token](../concepts/token.md) Plan 实现细粒度的用量隔离、成本管控和稳定性保障。该机制适用于所有支持按 token 计费的模型服务，且与身份认证、项目空间和配额策略深度集成。

## 支持的模型/功能

- 所有百炼平台托管的 **大语言模型（LLM）**（如 Qwen 系列、Qwen-VL、Qwen-Audio）均支持 [Token](../concepts/token.md) Plan 控制；
- **推理 API（`/v1/chat/completions`、`/v1/completions`）** 和 **Embedding API（`/v1/embeddings`）** 均纳入 Token Plan 统计；
- 不支持 Token Plan 的场景包括：模型微调训练任务、异步批量处理（`/v1/batch`）、以及 [Coding Plan](raw/model-user-guide/token-plan-guide/coding-plan-guide.md) 独立计费通道（详见 [Coding Plan](../../raw/model-user-guide/token-plan-guide/coding-plan-guide.md)）。

## 关键参数

| 参数名 | 类型 | 说明 | 是否必需 |
|--------|------|------|----------|
| `token_plan_id` | string | Token Plan 唯一标识符，由平台分配或通过控制台创建 | 是 |
| `enable_token_limit` | boolean | 是否启用 token 总量限制（默认 `false`） | 否 |
| `max_tokens_per_day` | integer | 每日 token 上限（单位：千 token），范围 1–100000 | 当 `enable_token_limit=true` 时必需 |
| `enable_rate_limit` | boolean | 是否启用 QPS 限流（默认 `false`） | 否 |
| `max_qps` | integer | 每秒最大请求数，范围 1–100 | 当 `enable_rate_limit=true` 时必需 |

> **注意**：`max_tokens_per_day` 的实际生效单位为 **千 token**（即设置 `1000` 表示 1,000,000 tokens/天），该定义与 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md) 一致，但与旧版文档 [个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal.md) 中“按原始 token 数设置”的描述存在不一致——请以 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md) 为准。

## 使用方式

1. **创建 Plan**：在控制台「配额管理」→「Token Plan」中新建，或调用 `POST /v1/token-plans` 接口；
2. **绑定 Plan**：在调用模型 API 时，于请求 Header 中添加 `X-Token-Plan-ID: <token_plan_id>`；
3. **验证生效**：响应 Header 中若含 `X-RateLimit-Remaining-Tokens` 和 `X-RateLimit-Reset`，表示 Token Plan 已生效；
4. **调试建议**：首次使用前，建议先在沙箱环境测试，参考 [进阶配置](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md) 中的灰度发布策略。

## 限制和注意事项

- 单个 API 请求若超出当前 Plan 剩余 token 配额，将返回 `429 Too Many Requests`，错误体含 `"code": "TOKEN_EXHAUSTED"`；
- Token Plan **不跨项目空间生效**：同一 `token_plan_id` 在不同 project_id 下需分别绑定；
- 每日 token 配额按 UTC+0 时间重置，非本地时区；
- 不支持动态修改已绑定 Plan 的 `max_tokens_per_day` —— 如需调整，请新建 Plan 并重新绑定；
- 对于流式响应（`stream=true`），token 统计在响应结束时一次性扣减，**非逐 chunk 扣减**（此行为与 [玩法攻略](../../raw/model-user-guide/token-plan-guide/token-plan-playbooks.md) 中早期示例不符，应以本指南为准）。

## 来源文档

- [Token Plan](../../raw/model-user-guide/token-plan-guide.md)


