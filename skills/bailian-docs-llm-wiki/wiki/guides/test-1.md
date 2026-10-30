# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与资源管理能力集合，涵盖新人免费额度、吞吐预留（TPM）、模型调用、训练与部署、节省计划、账单成本管控及预算管理等全链路能力。本文档结构化梳理其关键机制，聚焦可操作性信息，帮助开发者快速选型、配置并规避常见陷阱。

## 支持的模型/功能

- **免费额度适用模型**：仅华北2（北京）地域的指定模型享有新人免费额度（通常为 100 万 [Token](../concepts/token.md)），且不同模型（含快照版本如 `qwen-max-2025-01-25` 与 `qwen-max`）额度完全独立、不互通 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **吞吐预留（TPM）支持模型**：包括 `qwen3.8-max`、`qwen3.7-flash-2026-07-15`、`glm-5.2`、`deepseek-v4-pro` 等，分标准模式（同TPS）与高速模式（1.5~2倍TPS），支持华北2（北京）和新加坡地域 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **模型调用覆盖范围**：按量计费支持全部公开模型，但免费额度**仅抵扣实时推理**，明确排除 Batch 调用、模型调优、模型部署、PAI-DSW、OSS 存储等费用 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **节省计划覆盖模型**：AI 通用型节省计划可抵扣 A 类（千问、向量、排序等）、B 类（图像、语音、视频）、C 类（DeepSeek、Kimi、GLM 等阿里直供版）模型的调用费用；但**三方直供模型不支持抵扣**，需以控制台实际展示为准 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

## 关键参数

- **免费额度有效期**：90 天，自开通百炼、模型发布或申请通过之日三者中**最晚者**起算；2025年9月8日前开通用户有效期可能不足90天 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **TPM 容量单位**：输入按 **万TPM/天** 报价，输出按 **千TPM/天** 报价；购买时输入起步 200 kTPM，输出起步 20 kTPM [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **长输入折算系数**：不同模型阶梯规则差异大，例如 `qwen3.7-flash-2026-07-15` 对 (32K,256K] 输入段采用 3x 系数，而 `glm-5.1` 对同一区间输入采用 1.33x，输出采用 1.17x [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **模型调用阶梯计费**：以 `qwen3.7-plus-2026-05-26` 为例，输入 [Token](../concepts/token.md) ≤256K 时输入单价 ¥2/百万，>256K 时升至 ¥6/百万，**整次请求所有 [Token](../concepts/token.md) 均按高阶单价结算** [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **预算管理范围**：**仅限 API 按调用量付费产生的费用**，明确排除模型训练、预置吞吐（PTU）、模型单元（DTU）等费用 [原文标题](../../raw/model-user-guide/test-1/budget-management.md)。

> **注意**：文档 4 中 `qwen3.7-plus` 的价格表标注“当前能力等同于 `qwen3.7-plus-2026-05-26`”，但文档 3 的模型部署计费表中 `qwen3.7-plus-2026-05-26` 的最长输入 Token 为 256K，而文档 4 中 `qwen3.7-plus` 的输入单价描述未体现该限制，存在潜在歧义。开发者应以模型部署页或控制台实际参数为准。

## 使用方式

- **免费额度启用**：开通百炼并完成实名认证后自动发放，无需手动领取；额度在华北2（北京）地域模型列表中以蓝色额度条标识，两小时内生效 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **吞吐预留调用**：创建成功后生成专属模型 Code（如 `qwen3.8-max-ptu-xxxx`），需在 API 请求中将 `model` 参数替换为此 Code 才能命中预留容量 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **节省计划生效**：购买后使用**百炼通用 API Key 与 Base URL** 接入，费用在结算时自动抵扣，**仅抵扣生效后产生的费用**，购买前已产生费用无法追溯 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **预算自动停用**：开启「达到预算后立即停止」后，费用达阈值时 API 调用返回 HTTP 429 错误；但 PTU 溢出部分及应用产生的调用暂不支持此自动停止机制 [原文标题](../../raw/model-user-guide/test-1/budget-management.md)。

## 限制和注意事项

- **免费额度地域强约束**：仅华北2（北京）地域模型可用，其他地域（如美国、新加坡）无任何免费额度 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **TPM 预留“生效即计费”**：创建成功即开始计费，与是否调用无关；容量费用按购买量全额计收，不因实际用量减免 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **模型部署溢出行为差异**：当输入超最长 Token 或 TPM 超额时，若选择「自动溢出」策略，调用将切换为按量付费并返回 Header `x-dashscope-ptu-overflow:true`；若选择「仅使用 PTU 容量」则直接返回 429 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **账单出账延迟**：大模型推理账单为分钟级出账（通常 2–10 分钟），批量推理、模型训练等为小时级出账；查询账单时需等待系统出账完成，刚调用后查不到属正常现象 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **入门型节省计划退订限制**：一经支付，**不支持退订**，购买前需确认档位和需求 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [预算管理](../../raw/model-user-guide/test-1/budget-management.md)


