# test 1

`test 1` 是百炼平台面向开发者提供的模型调用与计费管理能力模块，主要用于统一管控模型服务的资源消耗、成本核算及预算控制。其核心覆盖模型推理、训练部署、吞吐预留等场景的计费逻辑，并支持细粒度账单查询与预算告警。该模块的设计目标是保障资源使用的可预测性与成本透明性，适用于需要精细化成本治理的生产环境。

## 支持的模型/功能

- 支持所有百炼平台托管的 SaaS 模型（如 Qwen 系列、Qwen-VL 等）的按量调用计费  
- 支持自定义模型的训练与在线部署计费（含 GPU 实例时长、存储、镜像构建等）  
- 提供吞吐预留（TPM Reservation）能力，允许预购固定并发能力以降低单位请求成本  
- 集成节省计划（Savings Plan）与资源包（Resource Package），支持跨模型、跨地域的额度共享与抵扣  
- 支持多维度账单导出、成本分摊标签（Tag-based cost allocation）及预算阈值告警  

> **注意**：文档中提及的“跨模型额度共享”仅适用于同一代计费体系（v2.0+），旧版资源包不兼容新计费模型，详见 [模型计费](../../raw/model-user-guide/test-1.md) 的说明。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `billing_scope` | string | 是 | 计费作用域，取值 `project`（项目级）或 `user`（用户级）；默认 `project` |
| `reservation_period` | int | 否 | 吞吐预留周期（月），支持 1/3/6/12；仅当启用 TPM 预留时生效 |
| `budget_alert_threshold` | float | 否 | 预算告警阈值（百分比），范围 50–100，默认 80 |
| `cost_tag_keys` | string[] | 否 | 成本分摊标签键列表，如 `["env", "team"]`；需提前在控制台配置 |

## 使用方式

1. 在控制台「费用中心 → 计费设置」中为项目开启 `test 1` 功能  
2. 调用 `/v1/billing/configure` 接口提交配置（需 `BillingAdmin` 权限）  
3. 通过 `/v1/billing/usage` 查询实时用量，或 `/v1/billing/bills` 获取历史账单（支持按 `start_time`/`end_time` 分页）  
4. 预算告警事件将通过云消息服务（CMS）推送至已绑定的 Webhook 或钉钉群，格式遵循 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md) 定义  

## 限制和注意事项

- 单个项目最多配置 5 个独立预算规则；超出需申请配额提升  
- TPM 预留一旦生效不可退订，但支持降配（仅限同周期内下调预留值）  
- 资源包余额仅在购买当月生效，不滚动累积；过期未用完部分自动作废  
- 所有计费数据延迟 ≤ 15 分钟，实时用量接口返回的是近似值，最终结算以 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md) 中的正式账单为准  
- 新人免费额度有效期为注册后 30 天，且仅适用于首次调用的模型服务，详情见 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)

## 来源文档

- [模型计费](../../raw/model-user-guide/test-1.md)


