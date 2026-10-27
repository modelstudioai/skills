# test 1

`test 1` 是阿里云百炼平台面向开发者提供的模型服务计费与资源管理核心主题，涵盖新人免费额度、按量调用、吞吐预留（PTU）、模型训练/部署、预算控制及成本优化方案等全链路能力。本文档整合官方最新规则，聚焦华北2（北京）地域主流文本生成模型（如 `qwen3.8-max`、`qwen3.7-plus`），明确各计费模式的适用边界、关键参数与实操约束，帮助开发者快速建立成本意识并规避常见扣费风险。

## 支持的模型/功能

- **支持模型**：以千问系列为主，包括 `qwen3.8-max`、`qwen3.7-plus`、`qwen3.6-flash` 等文本生成模型；部分图像（万相）、语音（CosyVoice）、视频（万相i2v）及多模态（Qwen-VL）模型也纳入支持范围，但其免费额度、训练与部署规则独立 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **核心功能覆盖**：
  - 实时推理（含思考/非思考模式、Batch调用、上下文缓存）
  - 模型训练（微调）与部署（PTU/DTU）
  - 吞吐预留（标准/高速模式）
  - 成本管控（预算管理、节省计划、资源包）
- **地域限制**：新人免费额度**仅限华北2（北京）地域**，其他地域（如美国、新加坡、德国）无免费额度，且价格普遍上浮 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。模型训练服务亦存在地域限制，例如 CosyVoice 仅支持华北2（北京）[原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。

## 关键参数

- **Token 计费粒度**：输入/输出 Token 均按实际消耗计费，免费额度、按量付费、节省计划均基于此单位。注意：免费额度为输入+输出共用总额度，不区分类型 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **TPM（Tokens Per Minute）容量单位**：吞吐预留（PTU）以 kTPM（千 Tokens/分钟）为购买单位，输入按万TPM报价、输出按千TPM报价，计算时需换算 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **阶梯计费阈值**：部分模型（如 `qwen3.7-plus`）对输入 Token 分档定价（如 0–256K、256K–1M），单次请求所有 Token 均按最高档单价结算 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **缓存折算系数**：启用上下文缓存时，命中部分 Token 按系数（如 `qwen3.8-max` 为 0.125）折算 TPM 消耗，显著降低预留成本 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。

## 使用方式

- **免费额度使用**：开通百炼后自动发放，无需认证即可使用；调用时系统自动优先抵扣，无需额外配置。必须使用**通用 API Key**（非 Token Plan 专属 Key）才能消耗免费额度 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **按量调用**：直接通过百炼 API 调用，费用实时计入账单（分钟级出账）。推荐搭配 AI 通用型节省计划，承诺月消费可享最高 5.3 折，覆盖绝大多数模型 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **吞吐预留（PTU）**：创建后生成专属 `model` Code，需在 API 请求中显式指定该 Code 才能走预留通道。高速模式提供 1.5–2 倍 TPS，但价格高于标准模式 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **预算管理**：在控制台设置账号/业务空间/API Key 级别月度预算，开启「达到预算后立即停止」可自动限制按量调用（返回 429 错误），但**生产环境不建议开启**，以防业务中断 [原文标题](../../raw/model-user-guide/test-1/budget-management.md)。

## 限制和注意事项

> **注意**：文档 1 与文档 2 对 `qwen3.8-max` 的免费额度有效期描述存在矛盾。文档 1 明确指出“2025年9月8日11点前已开通用户，免费额度有效期可能不足90天”，而文档 2 表格中仅标注“有效期：自开通百炼/模型发布/申请通过之日起90天内（以较晚者为准）”，未体现该例外条款。开发者应以文档 1 的时效性说明为准。

- **免费额度限制**：
  - 仅抵扣**实时推理**费用，Batch调用、模型训练、模型部署、PAI-DSW、OSS 存储等均不支持 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
  - 不同模型（含快照版本如 `qwen3.8-max` 与 `qwen3.8-max-2026-05-17`）额度完全独立，不可互通 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
  - 免费额度用完即停（`AllocationQuota.FreeTierOnly` 错误）功能，未认证用户强制开启且无法关闭；已认证用户默认关闭，需手动开启 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。

- **计费与出账延迟**：
  - 模型推理账单通常**2–10 分钟**出账，但“预占+月结”模式下实际扣款在次月初完成，期间账户余额可能被冻结 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
  - 吞吐预留（PTU）创建成功即开始计费，**不因实际用量减免**；模型部署（DTU）则从部署状态变为“运行中”起计费，与是否调用无关 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。

- **成本失控高发场景**：
  - IDE 插件（如 Cline、CodeBuddy）自动补全会携带完整上下文，单次对话消耗数千 Token，极易快速耗尽免费额度或预算 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
  - 长上下文对话中，输入 Token 随历史累积增长，47 次调用累计超 2500 万 Token 导致 20 分钟内余额耗尽的案例已被证实 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
  - 联网搜索（`enable_search`）等插件功能按调用次数单独计费，即使未主动调用模型，只要应用配置开启，每次触发即产生费用 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [预算管理](../../raw/model-user-guide/test-1/budget-management.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)


