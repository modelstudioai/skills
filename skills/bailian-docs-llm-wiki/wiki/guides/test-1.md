# test 1

`test 1` 是阿里云百炼平台面向开发者的核心计费与成本管理主题，涵盖模型调用、训练、部署及资源预留等全链路费用规则。本文整合官方文档，明确免费额度适用范围、关键参数定义、主流使用方式，并指出各计费模式间的边界与限制，帮助开发者精准预估成本、规避意外扣费。

## 支持的模型/功能

- **实时推理（按量调用）**：支持千问（Qwen）、DeepSeek、GLM、Kimi 等主流文本生成模型，以及千问VL、万相（Wan）、CosyVoice 等多模态与语音模型。所有模型均按输入/输出 [Token](../concepts/token.md) 计费，部分支持 Batch 调用半价与上下文缓存折扣 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **模型训练**：覆盖文本生成（千问系列）、图像生成（万相、千问Image）、视频生成（万相i2v/r2v）、语音合成（CosyVoice）等场景，按训练 [Token](../concepts/token.md) 总量计费，计算逻辑因模型类型而异 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **模型部署（PTU/DTU）**：提供预置吞吐（PTU）与独占吞吐（DTU）两种部署模式，支持标准/高速性能档位，按容量（kTPM）与时长（天/小时）计费 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **成本优化工具**：支持 AI 通用型节省计划（跨模型抵扣）、模型专属节省计划（单模型）、[Token](../concepts/token.md) Plan（订阅制）及资源包等多种优惠方案 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

> **注意**：文档 1 明确指出免费额度**仅抵扣模型实时推理费用**，不支持 Batch 调用、模型调优、模型部署、PAI-DSW、OSS 存储等 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)；而文档 3 和文档 4 均强调 Batch 调用虽享半价，但其费用仍属“模型调用”范畴，**不享受免费额度抵扣**——二者在“是否可被免费额度覆盖”上存在隐含矛盾，实际以文档 1 的排除性说明为准。

## 关键参数

- **Token 计费单位**：输入/输出 Token 均以“百万 Token”为单价基准（如 ¥12/百万 Token），账单中用量按实际 Token 数折算。
- **TPM（Tokens Per Minute）**：吞吐预留核心单位，1 kTPM = 1,000 Tokens/分钟；输入容量按“万TPM”报价（即 10 kTPM = 1 万TPM），输出按“千TPM”报价 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **阶梯计费区间**：部分模型（如 qwen3.8-max）对输入 Token 分档定价（如 0–1M），单次请求所有 Token 均按最高档单价结算 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **长输入系数与缓存系数**：吞吐预留中，长输入 Token 按模型配置的阶梯系数折算（如 qwen3.7-flash 输入 >32K 部分系数为 3x），缓存命中 Token 按缓存折算系数（如 0.2）额外折减 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。

## 使用方式

- **开通即用免费额度**：完成实名认证后，在华北2（北京）地域开通百炼，系统自动发放各模型独立免费额度（通常 100 万 Token），有效期 90 天 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **按量调用**：直接使用 API Key 调用模型，费用实时计入账单，支持通过节省计划或资源包自动抵扣 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **吞吐预留（PTU）**：在控制台创建预留实例，获取专属 `model` Code 替换原 API 参数，预留容量内调用不额外计费，溢出按策略处理（自动切换按量或返回 429） [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **预算管控**：在[预算管理](https://bailian.console.aliyun.com/cn-beijing/costing-balance/budget)页面为账号、业务空间或 API Key 设置月度预算，开启“达到预算后立即停止”可自动限流 [原文标题](../../raw/model-user-guide/test-1/budget-management.md)。

## 限制和注意事项

- **地域限制**：新人免费额度、ASR 模型权限开通、CosyVoice 调优等能力**仅限华北2（北京）地域**；其他地域模型无免费额度，且部分功能不可用 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **额度隔离**：免费额度、节省计划、资源包均按**商品 Code** 隔离。某商品（如“百炼容量预留”）欠费时，仅该服务不可用，不影响其他商品（如“百炼大模型推理”） [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **生效延迟**：免费额度开通后通常两小时内生效；账单出账有延迟（推理类 2–10 分钟，训练类小时级）；预算停用、PTU 扩容等操作亦存在生效延迟，期间费用仍会正常产生 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **生产环境警示**：免费额度“用完即停”功能默认关闭，**生产环境不建议开启**，以免额度耗尽导致服务中断；同样，“达到预算后立即停止”也需谨慎启用，因其可能引发业务不可用 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [预算管理](../../raw/model-user-guide/test-1/budget-management.md)


