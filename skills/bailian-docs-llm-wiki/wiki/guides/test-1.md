# test 1

test 1 是百炼平台面向模型调用与资源管理的统一计费模块，覆盖模型推理、训练部署、吞吐预留及成本控制等核心场景。其设计目标是为开发者提供细粒度、可预测、可管控的资源使用计量与计费能力。所有计费行为均基于实际资源消耗（如 token 数、GPU 小时、TPM 预留量等）并按分钟级精度结算，详见 [模型计费](../../raw/model-user-guide/test-1.md)。

## 支持的模型/功能

- 支持所有百炼平台托管的 SaaS 模型（如 Qwen 系列、Qwen-VL、Qwen-Audio）及用户自定义微调模型的调用计费；
- 支持模型训练任务（全参数微调、LoRA）、模型部署（Serverless 推理、专属实例）的独立计费项；
- 提供吞吐预留（TPM Reservation）能力，允许预购固定推理吞吐量以降低单位成本；
- 集成节省计划（Savings Plan）与资源包（Resource Package），支持跨模型、跨地域的额度共享与抵扣；
- 支持账单明细导出、多维度成本分摊（按项目/标签/用户）、预算告警等成本治理功能。  
  更完整的功能列表请参考 [模型计费](../../raw/model-user-guide/test-1.md)。

## 关键参数

- `model_id`：必填，指定计费关联的模型唯一标识（如 `qwen-max-20240806`），影响单价与计费策略；
- `input_tokens` / `output_tokens`：用于推理类请求的精确计费依据，按实际解析后的 token 数计量；
- `instance_type` + `duration_seconds`：训练/部署任务的核心计费参数，单位为 GPU 秒（如 `gpu-a10-24g` × 3600s）；
- `reserved_tpm`：吞吐预留配置值，最小单位为 100 TPM，生效后按小时计费，不可退订；
- `billing_cycle`：支持 `hourly`（默认）与 `monthly` 两种结算周期，影响账单生成频率与折扣适用性。  
  参数语义与约束详见 [模型调用计费](../../raw/test-1/model-pricing.md) 和 [模型训练与部署计费](../../raw/test-1/model-training-and-deployment-billing.md)。

## 使用方式

1. 开通百炼服务后，默认启用按量计费，无需额外开通；
2. 调用 `/v1/chat/completions` 或 `/v1/models/{model_id}/train` 等 API 时，系统自动采集资源消耗并计入账单；
3. 吞吐预留与节省计划需通过控制台「费用中心 → 资源包管理」或 OpenAPI `POST /billing/reservations` 主动购买；
4. 成本分析与预算设置可通过 `GET /billing/costs` 和 `PUT /billing/budgets` 接口编程管理；  
   完整 API 列表与示例见 [账单查询与成本管理](../../raw/test-1/bill-query-and-cost-management.md)。

## 限制和注意事项

- 新人免费额度仅限首次注册账号，有效期 30 天，额度不可叠加或转让，过期自动清零；
- 吞吐预留不支持跨地域抵扣（例如华东1预留的 TPM 无法用于华北2的请求），且不兼容 Serverless 实例的弹性扩缩容；
- > **注意**：文档中提及的「资源包可抵扣训练费用」与 [模型训练与部署计费](../../raw/test-1/model-training-and-deployment-billing.md) 当前版本存在矛盾——后者明确说明资源包**仅支持抵扣推理调用费用**，训练费用须单独购买训练包或按量支付。请以该文档最新版为准；
- 所有计费数据延迟不超过 5 分钟，但账单最终生成与发票开具存在 T+1 日延迟；
- 预算告警阈值最低设为 1 元，且仅支持邮件通知，Webhook 支持计划中。

## 来源文档

- [模型计费](../../raw/model-user-guide/test-1.md)


