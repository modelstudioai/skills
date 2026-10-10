# token plan guide

[Token](../concepts/token.md) Plan 是百炼平台为开发者提供的按量计费资源配额方案，用于调用模型 API 时消耗的 token 资源管理。它支持灵活的额度分配、实时用量监控与跨模型统一结算，适用于个人开发、团队协作及生产级集成场景。具体能力与配置细节请参考 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。

## 支持的模型/功能

- 当前支持所有百炼平台公开模型（含 Qwen 系列、Qwen-VL、Qwen-Audio 等），但不包括私有化部署模型或未接入计费系统的实验性模型。
- 支持同步推理（`/v1/chat/completions`）、异步任务（`/v1/async/task`）、批量处理（`/v1/batch`）及流式响应（`stream=true`）。
- Coding Plan 作为独立子计划，专用于代码生成类模型（如 Qwen2.5-Coder），其 token 计费规则与主 [Token](../concepts/token.md) Plan 分离，详见 [Coding Plan](../../raw/model-user-guide/token-plan-guide/coding-plan-guide.md)。

## 关键参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `token_plan_id` | string | 必填，[Token](../concepts/token.md) Plan 的唯一标识，可在控制台「配额管理」中获取 |
| `model` | string | 必填，调用的具体模型 ID（如 `qwen-max`, `qwen-plus`） |
| `max_tokens` | integer | 可选，单次请求最大输出 token 数，受所选 Plan 剩余额度约束 |
| `temperature` / `top_p` 等 | float / float | 与模型行为相关，不影响 token 计费逻辑 |

> **注意**：部分旧版文档（如 [个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal.md) 中提及的 `quota_type=prepaid`）已废弃，当前所有 Plan 均采用后付费模式，实际以 [进阶接入](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md) 中的鉴权方式为准。

## 使用方式

1. 在 API 请求 Header 中添加：  
   `Authorization: Bearer <your_api_key>`  
   `X-Token-Plan-ID: <your_token_plan_id>`
2. 请求体保持标准 OpenAI 兼容格式，无需额外字段；系统自动按输入 + 输出 token 总和扣减对应 Plan 余额。
3. 可通过 `/v1/token-plan/usage` 接口实时查询剩余 token 额度（需携带 `X-Token-Plan-ID`）。

## 限制和注意事项

- 单次请求总 token（input + output）不得超过该 Plan 当前剩余额度；超限将返回 `402 Payment Required`。
- Token Plan 不支持跨区域复用（如杭州集群申请的 Plan 无法在北京集群使用），区域信息需与 API endpoint 严格匹配。
- 同一 `token_plan_id` 不可并发用于多个模型请求的额度隔离——即所有模型共享该 Plan 总额度，若需隔离，请分别创建多个 Plan。
- 团队版 Plan 的成员权限继承与额度分配策略，请参阅 [团队版](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition.md) 文档。

## 来源文档

- [Token Plan](../../raw/model-user-guide/token-plan-guide.md)


