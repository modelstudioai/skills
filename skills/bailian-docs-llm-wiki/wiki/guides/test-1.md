# test 1

test 1 是百炼平台面向开发者提供的基础模型服务入口，支持按需调用、训练部署及资源预留等多种使用模式。其计费体系覆盖模型推理、训练、吞吐保障等核心场景，所有费用均基于实际资源消耗与预购承诺综合计算。详细计费规则请参考 [产品计费](../../raw/model-user-guide/test-1.md) 文档。

## 支持的模型/功能

- 支持标准 API 调用（同步/流式）、微调训练、私有化部署及吞吐量（TPM）预留；
- 提供多种精度与规模的模型变体（如 `test-1-base`、`test-1-pro`），具体能力差异见 [模型调用计费](../../raw/model-user-guide/test-1/model-pricing.md)；
- 支持通过节省计划（Savings Plan）和资源包抵扣账单，适用于长期稳定调用量场景，详情参见 [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

## 关键参数

- `model`: 必填，指定模型 ID（如 `test-1-base`）；
- `max_tokens`: 最大生成长度，上限受模型版本限制（`test-1-base` ≤ 4096，`test-1-pro` ≤ 8192）；
- `tpm_reservation`: 可选，用于启用吞吐预留，需提前购买并绑定至项目，详见 [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)；
- `stream`: 布尔值，启用流式响应时设为 `true`，注意流式调用不参与部分资源包抵扣。

## 使用方式

1. 在控制台开通 test 1 服务并完成项目授权；
2. 调用 `/v1/chat/completions` 或 `/v1/completions` 接口，携带认证 `Authorization: Bearer <api_key>`；
3. 若需训练或部署，通过 `POST /v1/models/train` 提交数据集与配置，训练任务状态可通过 `/v1/jobs/{job_id}` 查询；
4. 所有计费项实时同步至账单系统，支持按日粒度查看明细，操作路径见 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 限制和注意事项

- 免费额度仅限新注册用户首次开通 test 1 服务时自动发放，有效期 30 天，过期未用完不续期，具体规则见 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)；
- 预留 TPM 不可跨项目共享，且未使用的预留额度不累计、不退款；
> **注意**：[模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md) 中标注的“训练任务按小时计费”与最新控制台显示的“按 GPU 秒级计费”存在不一致，以控制台实时计费页为准；
- 预算告警阈值设置后仅对后续消费生效，无法追溯已发生费用，预算管理功能说明见 [预算管理](../../raw/model-user-guide/test-1/budget-management.md)。

## 来源文档

- [产品计费](../../raw/model-user-guide/test-1.md)


