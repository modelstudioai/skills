# token plan guide

[Token](../concepts/token.md) Plan 是百炼平台为模型调用设计的资源配额与计费管理机制，用于控制 API 调用的 token 消耗量、设定用量上限并支持按需升级。它适用于所有通过百炼 API 接入的模型服务，是开发者进行成本管控和稳定性保障的核心配置项。具体策略因账号类型（个人/团队）和模型能力而异，详见 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。

## 支持的模型/功能

- 所有百炼托管模型（含 Qwen 系列、Qwen-VL、Qwen-Audio 等）均支持 [Token](../concepts/token.md) Plan 配置；
- 支持同步推理（`/v1/chat/completions`）、[异步任务](../concepts/asynchronous-task.md)（`/v1/batches`）、流式响应（`stream=true`）等调用方式；
- Coding Plan 作为独立子计划，专用于代码生成类模型（如 Qwen2.5-Coder），其 token 计算规则与通用 Plan 不同，详见 [Coding Plan](../../raw/model-user-guide/token-plan-guide/coding-plan-guide.md)；
- 多模态模型（如 Qwen-VL）的图像 token 单独计费，不计入文本 token 配额，该规则在 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md) 中明确说明。

## 关键参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `max_tokens` | int | 单次请求允许生成的最大 token 数（不含输入 token），默认值由所选 Plan 决定 |
| `input_token_quota` | int | 每日/每月输入 token 总配额（取决于 Plan 类型），超出后请求将被拒绝 |
| `output_token_quota` | int | 每日/每月输出 token 总配额，独立于输入配额统计 |
| `plan_id` | string | Plan 唯一标识符（如 `personal-basic`, `team-pro`），需在请求 header 中显式传入 `X-Plan-ID` |

> **注意**：部分旧版文档中提及 `total_token_quota` 为输入+输出合并配额，该描述已过时；当前所有 Plan 均采用输入/输出分离计量，以 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md) 为准。

## 使用方式

1. **启用 Plan**：在百炼控制台「API 密钥管理」页为对应 API Key 绑定 Plan（支持切换）；
2. **调用时指定**：在 HTTP 请求 header 中添加 `X-Plan-ID: <plan_id>`，否则使用 API Key 默认绑定的 Plan；
3. **查询用量**：调用 `GET /v1/usage/token-plan` 获取当前周期内输入/输出 token 消耗明细；
4. **动态降级**：当配额不足时，系统自动返回 `429 Too Many Requests`，错误体中包含 `retry-after` 和剩余配额信息，建议客户端实现指数退避重试。

## 限制和注意事项

- 个人版 Plan 仅支持单 API Key 绑定，不可共享；团队版支持多成员共用同一 Plan 配额（按组织维度汇总）；
- Plan 配额按自然日（UTC+8）或自然月滚动重置，不支持自定义周期；
- 流式响应中，`usage` 字段仅在 `finish_reason == "stop"` 的最后一个 chunk 中返回完整 token 统计；
- 若同时启用 Rate Limit 和 [Token](../concepts/token.md) Plan，二者独立生效：Rate Limit 控制 QPS，Token Plan 控制总 token 量；
- 模型微调（Fine-tuning）任务不走 Token Plan 流程，其消耗单独计费，相关说明见 [进阶接入](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md)。

## 来源文档

- [Token Plan](../../raw/model-user-guide/token-plan-guide.md)


