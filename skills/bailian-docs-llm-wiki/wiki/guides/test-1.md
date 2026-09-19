# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与资源管理主题，涵盖模型调用、训练、部署及成本优化的全链路规则。本文整合官方文档，明确免费额度适用范围、模型支持矩阵、关键参数含义及实际调用约束，帮助开发者快速建立成本意识并规避常见扣费风险。所有信息均基于华北2（北京）地域默认配置，跨地域使用需单独确认计费策略。

## 支持的模型/功能

`test 1` 覆盖百炼平台主流模型服务，包括文本生成（千问系列）、[多模态](../concepts/multimodal.md)（千问VL、万相）、语音（CosyVoice）、视频生成等，但**免费额度与部分计费模式存在严格模型绑定和地域限制**。

- **免费额度仅适用于华北2（北京）地域的实时推理调用**，且明确排除 Batch 调用、模型调优、模型部署、PAI-DSW、OSS 存储等场景 [Batch调用](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。例如，`qwen3.8-max` 在北京地域享有 100 万 [Token](../concepts/token.md) 免费额度，而同名模型在新加坡或美国地域则无此权益。
- **模型训练与部署为独立计费项**，不消耗免费额度。训练按 [Token](../concepts/token.md) 总量计费（如 `qwen3.7-plus-2026-05-26` 训练单价为 ¥0.35/千[Token](../concepts/token.md)），部署则按 PTU（预置吞吐单元）或 TPM（吞吐预留）时长计费 [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **吞吐预留（TPM 预留）支持标准与高速两种模式**，高速模式提供 1.5~2 倍 TPS 提升，但仅限部分模型（如 `qwen3.8-max`、`deepseek-v4-flash`）且需单独开通 [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。

> **注意**：文档 2 中 `qwen3.8-max-prime` 标注“无免费额度”，而文档 1 明确“每个模型均有独立的免费额度（通常为 100 万 Token）”。此处矛盾表明 `qwen3.8-max-prime` 属于特殊定价模型，其免费额度政策与常规模型不同，开发者应以控制台实际显示为准，不可默认套用通用规则。

## 关键参数

理解以下参数是准确预估成本和配置服务的基础：

- **Token 计费粒度**：输入/输出 Token 分开计费，单价按百万 Token 报价（如 `qwen3.6-plus` 输入单价 ¥2/百万Token）。阶梯计费中，单次请求的所有 Token 均按最高档位单价结算 [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)。
- **TPM（Tokens Per Minute）容量单位**：吞吐预留中，输入容量单位为 kTPM（千 Tokens/分钟），但报价按“万TPM·天”；输出容量单位为 kTPM，报价按“千TPM·天”。计算费用时需注意单位换算（kTPM ÷ 10 → 万TPM）[吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **缓存折算系数与长输入阶梯系数**：影响 TPM 预留的实际消耗。例如 `qwen3.7-flash` 对超出 32K 的输入部分按 3x 系数折算，而缓存命中部分再乘以 0.2 折算系数，显著降低有效消耗 [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **节省计划承诺周期**：AI 通用型节省计划以“动态月”为单位发放额度（非自然月），当月未用完额度自动清零，不累积至下月 [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

## 使用方式

开发者需按以下流程完成服务接入与成本管理：

1. **开通与额度获取**：首次开通百炼后，系统自动发放北京地域模型的免费额度，无需实名认证即可使用。额度在两小时内生效，可通过控制台 [免费额度](https://bailian.console.aliyun.com/cn-beijing/costing-balance/free-quota) 页面查看 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
2. **API 调用**：使用通用 API Key（非 Token Plan 专属 Key）发起实时推理请求，系统自动按 `免费额度 > 资源包 > 节省计划 > 按量付费` 顺序抵扣。若开启“免费额度用完即停”，额度耗尽将返回 HTTP 403 错误 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
3. **成本优化选型**：
   - 长期稳定调用：优先购买 [AI 通用型节省计划](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)，覆盖绝大部分阿里直供模型。
   - 单一模型高频调用：可选模型专属节省计划或资源包。
   - 团队协作：使用 Token Plan 团队版，额度独立于账户余额。
4. **账单与用量监控**：调用结束后 2~10 分钟生成推理账单，可在 [账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail) 页面通过 `实例 ID（出账粒度）` 字段（格式：`ApiKeyID;业务空间ID;模型名称;...`）精准溯源费用 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 限制和注意事项

- **地域强约束**：免费额度、部分模型部署、吞吐预留均仅在北京地域生效。跨地域调用（如从新加坡 ECS 调用北京模型）虽可被 AI 通用型节省计划抵扣，但网络延迟与合规性需自行评估 [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **额度不互通**：同一模型的不同快照版本（如 `qwen3.7-max` 与 `qwen3.7-max-2026-05-20`）视为独立模型，各自拥有 100 万 Token 免费额度，不可共享 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **欠费即停服**：账户可用额度 < 0 时，所有按量付费服务（含免费额度、节省计划、资源包）立即暂停，即使剩余额度充足也无法调用 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **模型部署持续计费**：已部署模型处于“运行中”状态即开始计费，与是否被 API 调用无关。停止计费需主动下线模型或退订预付费实例 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **出账延迟风险**：模型推理账单存在分钟级延迟，可能导致“控制台显示有额度但实际已耗尽”而产生意外扣费。操作前务必手动刷新控制台页面，并设置高额消费预警 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)


