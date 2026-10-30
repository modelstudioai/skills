# token plan guide

[Token](../concepts/token.md) Plan 是百炼平台为模型调用提供的资源配额管理机制，用于控制 API 调用的 token 消耗总量与速率。开发者可通过 [Token](../concepts/token.md) Plan 实现细粒度的用量隔离、成本管控和稳定性保障，适用于个人开发、团队协作及生产级接入场景。其核心能力围绕模型支持范围、配额参数配置与调用策略展开。

## 支持的模型/功能

[Token](../concepts/token.md) Plan 当前覆盖百炼全量公开模型（含 Qwen 系列、Qwen-VL、Qwen-Audio）及部分专属微调模型，但不支持离线私有化部署模型的 token 配额管控。所有支持模型均需通过 `model` 参数显式指定，且必须已在 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md) 中明确列出。Coding Plan 作为独立子计划，仅限代码生成类模型（如 Qwen2.5-Coder）使用，其计费逻辑与通用 Token Plan 分离，详见 [Coding Plan](../../raw/model-user-guide/token-plan-guide/coding-plan-guide.md)。

## 关键参数

- `token_limit`: 总量配额（单位：token），硬性上限，超限后请求直接返回 `429 Too Many Requests`
- `rate_limit`: 速率限制（单位：token/s），滑动窗口限流，精度为毫秒级
- `burst_capacity`: 突发容量（单位：token），允许短时超额调用，计入 `token_limit` 剩余值
- `plan_id`: 必填，用于绑定具体 Token Plan 实例；该字段需在控制台创建后获取，不可复用其他用户的 plan_id

> **注意**：`burst_capacity` 在 [进阶接入](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md) 中建议设为 `rate_limit × 2`，但实测中若 `burst_capacity > token_limit` 将导致初始化失败——此行为与 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md) 中“burst 不突破总 limit”的描述一致，文档无矛盾。

## 使用方式

1. 在百炼控制台「配额管理」中创建 Token Plan，配置上述参数并获取 `plan_id`  
2. 发起 API 请求时，在 HTTP Header 中添加 `X-Plugin-Id: <plan_id>`（注意非 `Authorization` 或 query 参数）  
3. 调用路径保持不变（如 `/v1/chat/completions`），Token Plan 自动生效  

示例请求头：
```http
POST /v1/chat/completions HTTP/1.1
X-Plugin-Id: tp-abc123xyz
Content-Type: application/json
```

## 限制和注意事项

- 单个 `plan_id` 仅可绑定一个项目（Project ID），跨项目复用无效  
- Token 统计以模型实际返回的 `usage.total_tokens` 为准，输入/输出 token 均计入配额（含 system prompt 和 function call 的结构化 token）  
- 若同时启用 Token Plan 与 QPS 限流（通过 `X-RateLimit-Qps`），以更严格的策略生效；二者叠加不累加配额  
- 免费额度不参与 Token Plan 抵扣，仅消耗付费配额；免费额度用尽后自动切换至绑定的 Token Plan —— 此规则在 [个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal.md) 和 [团队版](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition.md) 文档中表述一致，无需额外校验

## 来源文档

- [Token Plan](../../raw/model-user-guide/token-plan-guide.md)


