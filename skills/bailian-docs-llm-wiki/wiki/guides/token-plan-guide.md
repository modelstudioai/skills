# token plan guide

[Token](../concepts/token.md) Plan 是百炼平台为模型调用提供的资源配额管理机制，用于控制 API 调用的 token 消耗总量与速率。它适用于不同规模的应用场景，支持按模型、调用路径和用户身份进行精细化配额分配。开发者需结合业务负载合理配置，避免因超限导致请求被拒绝。

## 支持的模型/功能

[Token](../concepts/token.md) Plan 当前覆盖全部百炼托管模型（含 Qwen 系列、Qwen-VL、Qwen-Audio）及部分第三方模型接入通道。基础能力包括：按请求计费（input + output tokens）、并发数限制、突发流量缓冲（burst allowance），以及跨模型共享配额池（仅限团队版）。[Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md) 中明确指出，Coding Plan 作为独立子计划，仅对 `/v1/coding/*` 接口生效，不参与通用 token 配额统计。

## 关键参数

- `max_tokens_per_request`：单次请求最大输出 token 数（默认 2048，不可超过模型原生上限）  
- `tokens_per_minute`：每分钟总 token 配额（含 input + output）  
- `requests_per_minute`：每分钟最大请求数（硬性限流阈值）  
- `burst_capacity`：突发令牌桶容量（单位：tokens），默认为 `tokens_per_minute / 60 * 5`  
- `model_whitelist`：显式指定生效模型列表（如 `qwen-max`, `qwen-plus`），空值表示全部支持模型  

> **注意**：[个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal.md) 文档中列出的 `burst_capacity` 默认值为固定 100，但 [进阶配置](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md) 明确说明该值动态计算且可覆盖，以后者为准。

## 使用方式

1. 在控制台「模型服务 → [Token](../concepts/token.md) Plan」创建新计划，或通过 OpenAPI `POST /v1/token-plans` 提交 JSON 配置；  
2. 将计划绑定至具体模型服务（Service ID）或 API Key；  
3. 发起调用时，HTTP Header 中需携带 `x-bailian-token-plan-id: <plan_id>`（服务端绑定模式下可省略）；  
4. 实时用量可通过 `GET /v1/token-plans/{id}/usage` 查询，响应包含 `used_tokens_this_minute` 和 `remaining_burst` 字段。[玩法攻略](../../raw/model-user-guide/token-plan-guide/token-plan-playbooks.md) 提供了灰度发布、AB 测试等典型绑定策略示例。

## 限制和注意事项

- 单个 Token Plan 最多绑定 50 个 Service 或 API Key；  
- 修改 `tokens_per_minute` 后，新配额在下一个整分钟生效（非实时）；  
- 输出 token 统计以模型实际返回的 `usage.output_tokens` 为准，若模型未返回该字段（如部分旧版兼容接口），将按响应长度粗略估算；  
- 免费额度不叠加 Token Plan 配额，优先消耗免费 quota，超出后才触发 Plan 限流；  
- [团队版](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition.md) 支持配额继承与子账户隔离，但子账户无法单独创建 Plan，必须由管理员分配。

## 来源文档

- [Token Plan](../../raw/model-user-guide/token-plan-guide.md)


