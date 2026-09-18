# token plan guide

Token Plan 是百炼平台为模型调用设计的资源配额与计费管理机制，用于控制 API 调用频次、并发量及总 token 消耗。开发者可通过 Token Plan 实现细粒度的用量隔离、成本管控和多环境资源分配。该机制适用于所有支持按 token 计费的模型服务，且与身份认证、API Key 权限体系深度集成。

## 支持的模型/功能

- 当前支持全部百炼托管模型（含 Qwen 系列、Qwen-VL、Qwen-Audio）及通过 [Model Studio](../../raw/model-user-guide/model-studio.md) 部署的自定义模型  
- 支持同步推理（`/v1/chat/completions`）、异步任务（`/v1/batch`）、流式响应（`stream=true`）三种调用模式  
- 仅部分模型支持 `max_tokens` 动态覆盖（详见 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)）  
- Coding Plan 作为独立子计划，专用于代码生成类模型（如 Qwen-Coder），其配额不与通用 Token Plan 互通 —— 具体规则见 [Coding Plan](../../raw/model-user-guide/token-plan-guide/coding-plan-guide.md)

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `plan_id` | string | 是 | 平台分配的唯一计划标识，需在请求 Header 中传入 `X-Plan-ID` |
| `max_tokens` | integer | 否 | 单次请求最大输出 token 数（受模型原生限制与 plan 配额双重约束） |
| `rate_limit` | integer | 否 | 每秒请求数（RPS），默认继承 plan 绑定值，不可在请求中覆盖 |
| `burst_capacity` | integer | 否 | 突发容量（单位：token），仅对异步批处理生效，参考 [进阶配置](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md) |

> **注意**：文档中提及的 `quota_type=per_call` 已于 v2.3.0 下线，当前所有 plan 均采用 `per_minute` + `per_day` 双维度配额，旧版配置将被自动迁移；详情参见 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)

## 使用方式

1. **绑定 plan 到 API Key**：在控制台「API Key 管理」页选择目标 key，点击「绑定 Token Plan」并指定 `plan_id`  
2. **发起请求**：在 HTTP Header 中添加 `X-Plan-ID: <your_plan_id>`，其余参数与标准百炼 API 一致  
3. **查看用量**：调用 `/v1/usage/plan/<plan_id>` 获取实时 token 消耗、剩余配额及触发的限流事件  

示例请求头：
```http
POST /v1/chat/completions HTTP/1.1
Authorization: Bearer sk-xxx
X-Plan-ID: plan-abc123
Content-Type: application/json
```

## 限制和注意事项

- 单个 `plan_id` 最多绑定 100 个 API Key；超出需创建新 plan  
- `X-Plan-ID` 未提供或无效时，请求将回退至账户默认 plan（若无则拒绝）  
- 流式响应中，token 计费以实际返回的 completion tokens 为准（含 `finish_reason="length"` 截断情形）  
- 团队版 plan 的成员权限继承规则与个人版不同：团队成员无法直接修改 plan 配额，须由管理员操作 —— 具体差异见 [团队版](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition.md)  
- 所有 plan 配额按 UTC 时间每日 00:00 重置，不支持自定义重置周期

## 来源文档

- [Token Plan](../../raw/model-user-guide/token-plan-guide.md)


