# token plan guide

[Token](../concepts/token.md) Plan 是百炼平台为开发者提供的按量计费资源配额方案，用于调用模型 API 时消耗的 token 资源管理。它支持灵活的额度分配、实时用量监控与跨模型统一结算，适用于个人开发、团队协作及生产级集成场景。具体能力与配置细节请参考 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。

## 支持的模型/功能

- 当前支持所有百炼平台已上线的通用大模型（如 Qwen 系列、Qwen2、Qwen3）、多模态模型（Qwen-VL、Qwen-Audio）及部分推理优化模型（如 Qwen2.5-7B-Instruct-Int4）。
- 支持同步推理（`/v1/chat/completions`）、[异步任务](../concepts/asynchronous-task.md)（`/v1/async-tasks`）、批量处理（`/v1/batch`）及流式响应（`stream=true`）。
- Coding Plan 作为独立子计划，专用于代码生成类模型（如 Qwen2.5-Coder），其 token 计费规则与通用 [Token](../concepts/token.md) Plan 分离，详见 [Coding Plan](../../raw/model-user-guide/token-plan-guide/coding-plan-guide.md)。

## 关键参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `model` | string | 必填，指定模型 ID（如 `qwen-max`, `qwen-plus`），需与所购 [Token](../concepts/token.md) Plan 的授权模型范围一致 |
| `input_tokens` / `output_tokens` | integer | 只读，由平台自动统计返回，用于用量分析与账单核对 |
| `max_tokens` | integer | 可选，限制生成长度；超出该值将被截断，不额外计费 |
| `top_p`, `temperature` 等采样参数 | float / number | 不影响 token 计费，仅控制生成质量 |

> **注意**：部分旧版文档中提及 `token_limit` 作为请求级硬限参，该参数已于 v2024.06 接口版本废弃，实际生效的是账户级 Token Plan 配额，以 [进阶接入](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md) 中的配额继承逻辑为准。

## 使用方式

1. **开通与绑定**：在控制台「计费中心 → Token Plan」页面完成购买，并为对应项目（Project）或 API Key 绑定 Plan；
2. **发起调用**：使用已绑定 Plan 的 API Key 发起标准 OpenAI 兼容请求，无需额外 header 或 query 参数；
3. **用量查询**：通过 `/v1/usage` 接口或控制台「用量明细」页实时查看 `input_tokens` 与 `output_tokens` 消耗；
4. **额度预警**：当剩余配额 ≤ 5% 时，系统自动触发邮件+站内信通知，阈值不可自定义。

## 限制和注意事项

- 单次请求最大 `input_tokens + output_tokens` 总和不得超过模型上下文窗口的 90%（例如 qwen-max 上下文 32k，则单次上限为 28.8k）；
- Token Plan 不支持跨地域（Region）复用，华东 1 购买的 Plan 无法在华北 2 调用；
- 免费试用额度（如新用户赠送 100 万 tokens）优先于付费 Plan 扣减，且不参与退款或转移；
- 团队版 Plan 的成员权限继承规则与个人版不同，成员仅能使用其所属子账号绑定的额度，主账号不可代扣，详情见 [团队版](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition.md)。

## 来源文档

- [Token Plan](../../raw/model-user-guide/token-plan-guide.md)


