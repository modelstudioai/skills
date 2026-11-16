# test 1

`test 1` 是百炼平台面向开发者提供的模型调用与计费管理能力模块，主要用于统一管控模型服务的资源消耗、成本核算及预算控制。其核心覆盖模型推理、训练部署、吞吐预留等场景的计费逻辑，并支持细粒度账单查询与预算告警。该模块的设计与实现详见 [模型计费](../../raw/model-user-guide/test-1.md)。

## 支持的模型/功能

- 支持所有已接入百炼平台的公有云模型（含 Qwen 系列、通义万相、通义听悟等）的按量调用计费  
- 支持模型微调、全参数训练及在线服务部署的独立计费项  
- 提供吞吐预留（TPM Reservation）能力，适用于高稳定性、低延迟要求的生产场景  
- 支持节省计划（Savings Plan）和资源包（Resource Package）两种预付费模式，需结合 [模型计费](../../raw/model-user-guide/test-1.md) 中的定价策略使用  

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `model_id` | 模型唯一标识，必须与 [模型计费](../../raw/model-user-guide/test-1.md) 中公示的模型列表一致 | `qwen-max`, `qwen-plus` |
| `tpm_reservation_id` | 吞吐预留实例 ID，仅在启用 TPM 预留时必填 | `trp-abc123` |
| `billing_cycle` | 计费周期，支持 `hourly` / `daily` / `monthly`（默认 `monthly`） | `monthly` |

> **注意**：`billing_cycle` 在 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md) 中定义为只读字段，实际生效周期由账户级设置决定，API 请求中显式传入将被忽略。

## 使用方式

1. 调用模型前，确保账户已开通对应模型的访问权限并完成实名认证  
2. 若使用吞吐预留，需先通过控制台或 OpenAPI 创建 `tpm_reservation_id`，参考 [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)  
3. 发起模型请求时，在请求头或 payload 中携带计费上下文（如 `X-Billing-Mode: on-demand` 或 `X-Billing-Mode: savings-plan`）  
4. 成本数据可通过 `/v1/billing/bills` 接口实时查询，详细字段含义见 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)

## 限制和注意事项

- 新用户默认享有 500 元新人免费额度，有效期 30 天，具体规则参见 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)  
- 同一 `tpm_reservation_id` 仅支持绑定单一模型版本；跨版本升级需重新申请预留  
- 节省计划不支持退款，且不可转让；资源包仅限购买账号内使用  
- 模型训练任务若超时未完成，仍按整小时计费（不足 1 小时按 1 小时计），详见 [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)

## 来源文档

- [模型计费](../../raw/model-user-guide/test-1.md)


