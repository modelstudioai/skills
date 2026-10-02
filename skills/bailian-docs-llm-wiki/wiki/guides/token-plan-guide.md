# token plan guide

[Token](../concepts/token.md) Plan 是百炼平台为模型调用设计的资源配额与计费管理机制，用于控制 API 调用的 token 消耗量、设定使用上限并支持按需扩容。它适用于所有通过百炼 API 接入的模型服务，是开发者进行成本管控和稳定性保障的基础配置。具体策略因账户类型（个人/团队）和模型能力而异，详见 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。

## 支持的模型/功能

- 所有百炼托管模型（含 Qwen 系列、Qwen-VL、Qwen-Audio 等）均支持 [Token](../concepts/token.md) Plan 配置  
- 支持同步推理（`/v1/chat/completions`）、异步任务（`/v1/async-tasks`）、批量处理（`/v1/batch`）等调用方式  
- Coding Plan 作为独立子计划，专用于代码生成类模型（如 Qwen2.5-Coder），其 token 计量规则与通用 [Token](../concepts/token.md) Plan 分离，详见 [Coding Plan](../../raw/model-user-guide/token-plan-guide/coding-plan-guide.md)  

## 关键参数

| 参数名 | 类型 | 说明 | 默认值 |
|--------|------|------|--------|
| `max_tokens` | integer | 单次请求允许消耗的最大 token 数（含 [prompt](prompt.md) + completion） | 由所选 plan 决定，非固定值 |
| `rate_limit` | string | 每秒最大 token 消耗速率（如 `"10000/tokens-per-second"`） | 因账号类型和模型而异，参见 [个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal.md) 与 [团队版](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition.md) 文档 |
| `burst_capacity` | integer | 突发流量可透支的 token 上限（单位：token） | 通常为 `rate_limit` 值的 2–5 倍 |

> **注意**：`max_tokens` 在部分旧版 SDK 中被误用为“响应长度限制”，实际应以 `max_completion_tokens`（若支持）或 `max_tokens` 的语义上下文为准；最新行为请以 [进阶接入](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md) 中的参数说明为准。

## 使用方式

1. **控制台配置**：登录百炼控制台 →「模型服务」→「Token Plan」页，选择对应模型与环境（开发/生产），设置 `rate_limit` 和 `burst_capacity`  
2. **API 调用时显式声明**（可选）：在请求 header 中添加 `X-Request-Token-Limit: <int>`，该值不可超过当前 plan 的 `burst_capacity`  
3. **监控与告警**：通过 `/v1/usage/token-usage` 接口实时查询已用 token 量，结合云监控配置超阈值告警  

## 限制和注意事项

- Token Plan 不支持跨模型共享配额（例如 Qwen-VL 的 token 消耗不计入 Qwen2 的 quota）  
- 异步任务与批量任务的 token 消耗按实际执行结果计量，非按请求预估；失败任务仍会计入已用 token  
- 免费额度仅适用于首次开通的个人账号，且不可叠加；团队版需管理员统一配置，成员无权修改 plan 设置  
- 若同时启用 Token Plan 与 Rate Limiting 中间件（如自建网关），需确保两者策略一致，否则可能触发双重限流 —— 具体兼容性细节见 [玩法攻略](../../raw/model-user-guide/token-plan-guide/token-plan-playbooks.md)

## 来源文档

- [Token Plan](../../raw/model-user-guide/token-plan-guide.md)


