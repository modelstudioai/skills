# token plan guide

[Token](../concepts/token.md) Plan 是百炼平台为模型调用提供的资源配额管理机制，用于控制 API 调用的 token 消耗额度与计费行为。开发者可通过 [Token](../concepts/token.md) Plan 明确分配、监控和限制不同应用或环境的 token 使用量，避免超额调用导致服务中断或意外计费。该机制适用于所有支持按 token 计费的模型调用场景。

## 支持的模型/功能

[Token](../concepts/token.md) Plan 当前覆盖全部百炼托管模型（含 Qwen 系列、Qwen-VL、Qwen-Audio）及部分第三方模型接入通道（如通过 Model Studio 接入的兼容 OpenAI 格式的模型）。不支持仅按请求次数计费的旧版模型（如早期 `qwen-1.8b` 无 token 计费模式版本）。具体支持列表详见 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。Coding Plan 作为独立子计划，专用于代码生成类任务，其 token 计算规则与通用 Token Plan 不同，需单独配置，参见 [Coding Plan](../../raw/model-user-guide/token-plan-guide/coding-plan-guide.md)。

## 关键参数

- `max_tokens`：单次请求允许消耗的最大 token 数（含 [prompt](prompt.md) + completion），超出将被截断并返回 `400` 错误  
- `quota`：周期性配额总量（单位：token/天），由用户在控制台设置，超限后请求将被拒绝（HTTP 429）  
- `model`：指定模型 ID，Token Plan 绑定到具体模型实例，不同模型间 quota 不共享  
- `plan_id`：Token Plan 的唯一标识符，用于 API 请求头 `X-Task-Plan-ID` 或 SDK 初始化时传入  

> **注意**：部分旧文档（如 [个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal.md) 中示例）仍将 `quota` 单位标为“千 token”，但自 v2.3.0 起已统一为“token”整数单位，实际配置时请勿除以 1000。

## 使用方式

1. 在百炼控制台「模型服务 > Token Plan」中创建计划，选择模型、设置 `quota` 和生效时间  
2. 调用模型 API 时，在请求头添加 `X-Task-Plan-ID: <plan_id>`；或使用 SDK（如 `dashscope` Python SDK v1.15.0+）初始化 client 时传入 `task_plan_id` 参数  
3. 验证是否生效：检查响应头 `X-RateLimit-Remaining` 和 `X-RateLimit-Limit` 字段，其值应与所设 `quota` 一致  
更多最佳实践可参考 [进阶接入](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md) 中的灰度发布与多环境隔离方案。

## 限制和注意事项

- 单个 Token Plan 最多绑定 10 个模型实例；如需跨模型统一配额，请使用团队版的「共享 quota 池」功能  
- Token Plan 不影响模型本身的 `max_tokens` 限制，仅控制配额消耗；二者需协同配置，否则可能出现 quota 未超但模型因 `max_tokens` 截断的情况  
- 免费额度（如新用户赠送 quota）与 Token Plan 独立计算，不计入 `quota` 值，也不受其约束  
- 所有 Token Plan 配额按 UTC 时间每日 00:00 重置，不支持自定义重置周期  
详细限制说明请查阅 [团队版](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition.md) 文档中的配额继承规则章节。

## 来源文档

- [Token Plan](../../raw/model-user-guide/token-plan-guide.md)


