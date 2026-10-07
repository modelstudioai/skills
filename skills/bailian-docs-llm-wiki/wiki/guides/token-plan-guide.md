# token plan guide

[Token](../concepts/token.md) Plan 是百炼平台为模型调用设计的资源配额与计费管理机制，用于控制 API 调用的 token 消耗量、设置用量上限并实现精细化成本管控。开发者可通过 [Token](../concepts/token.md) Plan 绑定模型实例、配置额度策略，并在服务级或请求级生效。该机制适用于所有支持按 token 计费的模型调用场景。

## 支持的模型/功能

- 所有百炼托管模型（含 Qwen 系列、Qwen-VL、Qwen-Audio）均支持 [Token](../concepts/token.md) Plan 控制，但部分旧版推理引擎模型（如 legacy-v1 接口）暂不支持 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)  
- 支持的功能包括：按日/月配额限制、突发流量弹性扩容（需开通团队版）、请求级 token 截断（`max_tokens` 优先于 Plan 配额生效）、异步任务 token 预占  
- Coding Plan 作为子集，专用于代码生成类模型（如 Qwen-Coder），其 token 计算规则与通用 Plan 不同，详见 [Coding Plan](../../raw/model-user-guide/token-plan-guide/coding-plan-guide.md)

## 关键参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `plan_id` | string | Token Plan 唯一标识，创建后不可修改 |
| `quota` | integer | 月度总配额（单位：token），最小值 1000 |
| `grace_period` | integer | 宽限期（秒），超限后允许继续调用的缓冲时间，默认 300 |
| `enforce_mode` | string | 取值 `"hard"`（立即拒绝）或 `"soft"`（记录告警但放行），默认 `"soft"` |

> **注意**：文档 [个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal.md) 中描述 `grace_period` 默认为 0，但最新平台行为已统一为 300 秒；请以实际 API 响应和 [进阶接入](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md) 中的实测逻辑为准。

## 使用方式

1. **创建 Plan**：调用 `POST /v1/token-plans`，传入 `quota` 和 `enforce_mode`  
2. **绑定模型实例**：在模型部署配置中指定 `token_plan_id`，或通过 `PUT /v1/models/{model_id}` 更新  
3. **请求级覆盖**：在单次 API 请求 header 中添加 `X-Token-Plan-ID: <id>`，可临时覆盖实例级绑定  
4. **查询用量**：调用 `GET /v1/token-plans/{plan_id}/usage?date=2024-06` 获取按日统计  

## 限制和注意事项

- 单个 Plan 最多绑定 50 个模型实例；超出需拆分或升级至团队版  
- Token 计费以模型实际返回的 `usage.total_tokens` 为准（含 [prompt](prompt.md) + completion），不包含重试或流式 chunk 的重复计数  
- 若同时配置了 `max_tokens` 和 Plan 配额，模型将在任一条件触发时截断输出（以先达到者为准）  
- 团队版支持跨成员共享 Plan，但个人版 Plan 无法被其他账号访问或继承 [团队版](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition.md)

## 来源文档

- [Token Plan](../../raw/model-user-guide/token-plan-guide.md)


