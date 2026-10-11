# test 1

`test 1` 是阿里云百炼平台面向开发者提供的模型服务计费与资源管理核心主题，涵盖免费额度发放规则、模型调用与训练部署的计费逻辑、吞吐预留机制、成本优化方案（节省计划/资源包）及预算管控能力。本文档聚焦于技术实现细节与开发者可操作项，不包含营销性描述，所有价格与策略均以华北2（北京）地域为默认基准，其他地域需单独确认适用性。

## 支持的模型/功能

`test 1` 覆盖百炼平台主流模型类型及其配套能力，包括：

- **文本生成模型**：千问系列（如 `qwen3.8-max`、`qwen3.7-plus`）、GLM 系列（如 `glm-5.2`）、DeepSeek 等，支持实时推理、Batch 调用、上下文缓存、Function Calling 等 [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md) 所列功能；
- **多模态模型**：千问 VL（`qwen2.5-vl-72b-instruct`）、万相图像/视频生成（`wan2.7-image-pro`、`wan2.7-i2v`），支持对应微调与部署；
- **语音模型**：CosyVoice（`cosyvoice-v3-plus`）、Qwen-ASR/TTS 系列，仅限华北2（北京）地域调优；
- **向量与排序模型**：Embedding 与 Rerank 模型，其调用费用可被 AI 通用型节省计划抵扣，详见 [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

> **注意**：文档 3 中“千问Max”表格列出 `qwen3.8-max-prime` 模型标注“无免费额度”，而文档 1 明确说明“仅华北2（北京）地域模型享有免费额度”。但文档 3 同一表格中 `qwen3.8-max` 在华北2（北京）列明确标注“100万Token”，且文档 1 的“适用范围”强调免费额度仅抵扣**实时推理**。因此 `qwen3.8-max-prime` 的“无免费额度”标注与其所在地域无关，而是该模型本身不参与新人免费额度发放——这与文档 1 “部分模型不参与新人免费额度发放”的结论一致，不存在矛盾。

## 关键参数

- **免费额度**：默认 100 万 Token/模型，有效期 90 天（自开通/模型发布/申请通过日起较晚者计算），仅抵扣实时推理费用，不支持 Batch、调优、部署等 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)；
- **Token 计费粒度**：最小计费单位为 1 Token，输入/输出 Token 分开计价，阶梯计费按单次请求总输入 Token 数确定单价区间；
- **TPM 预留容量**：吞吐预留以 kTPM（千 Tokens/分钟）为购买单位，输入起步 200 kTPM，输出起步 20 kTPM，长输入与缓存命中按模型特定系数折算消耗 [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)；
- **节省计划承诺周期**：AI 通用型节省计划支持 3/6/12/24 个月档位，月承诺金额 1000 元起，折扣力度随周期与金额递增，额度按动态月发放，当月未用完自动清零 [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)；
- **预算统计范围**：仅覆盖 API 按调用量付费产生的费用，明确排除模型训练、PTU、DTU 等费用 [预算管理](../../raw/model-user-guide/test-1/budget-management.md)。

## 使用方式

1. **开通与初始化**：首次开通百炼即自动发放免费额度，无需实名认证；额度在两小时内生效，可通过[免费额度页面](https://bailian.console.aliyun.com/cn-beijing/costing-balance/free-quota)查看；
2. **调用模型**：使用通用 API Key（非 Token Plan 专属 Key）发起 HTTP 请求，系统自动按 `免费额度 > 资源包 > 节省计划 > 按量付费` 顺序抵扣；
3. **购买预留吞吐**：在控制台选择模型、地域、性能模式（标准/高速）、输入/输出 kTPM 及购买时长，生成专属 `model` Code 用于调用；
4. **配置节省计划**：在[AI 通用型节省计划购买页](https://common-buy.aliyun.com/?commodityCode=sfm_GenAI_spn_cn)选择地域、周期、月承诺金额与付款方式（全预付/零预付），购买后立即生效并自动抵扣；
5. **设置预算**：在[预算管理页面](https://bailian.console.aliyun.com/cn-beijing/costing-balance/budget)按账号/业务空间/API Key 维度设置月度预算金额，并可选开启“达到预算后立即停止”；
6. **查询账单**：调用结束后 2~10 分钟生成推理账单，通过[账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)筛选“大模型服务平台百炼”，解析 `实例 ID（出账粒度）` 字段（格式：`ApiKeyID;业务空间ID;模型名称;...`）定位具体消费项 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 限制和注意事项

- **地域限制**：免费额度、语音模型调优、部分模型部署仅支持华北2（北京）地域；节省计划、吞吐预留需按地域单独购买，不可跨地域抵扣或复用；
- **额度互斥**：免费额度用完即停（安心模式）开启后，服务将返回 `AllocationQuota.FreeTierOnly` 错误，此时节省计划无法抵扣，必须手动关闭该开关才能恢复抵扣 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)；
- **缓存与 Batch 不叠加优惠**：同一请求若同时启用 Batch 调用与上下文缓存，二者优惠不可同时生效，系统优先应用 Batch 半价 [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)；
- **预算停服延迟**：开启“达到预算后立即停止”后，服务停止存在延迟，延迟期内产生的费用仍会正常收取，生产环境不建议开启 [预算管理](../../raw/model-user-guide/test-1/budget-management.md)；
- **退订惩罚**：预付费吞吐预留、模型部署等退订时，已使用部分按 1.2 倍系数结算（≤30 天）或 1.0 倍（>30 天），退款需在[费用中心](https://usercenter2.aliyun.com/refund/refund)操作 [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)；
- **账户欠费影响**：账户可用额度 < 0 时，即使免费额度、节省计划、资源包仍有余额，所有按量付费模型调用均将暂停，必须结清欠费方可恢复 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [预算管理](../../raw/model-user-guide/test-1/budget-management.md)


