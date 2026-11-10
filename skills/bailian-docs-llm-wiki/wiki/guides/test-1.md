# test 1

`test 1` 是百炼平台面向开发者提供的模型服务计费与成本管理核心主题，涵盖模型调用、训练、部署、吞吐预留及预算控制等全链路费用规则。本文档整合官方最新文档，聚焦技术实现细节，明确各计费模式的适用边界、参数含义与关键约束，帮助开发者精准预估成本、规避意外扣费，并高效配置资源。

## 支持的模型/功能

- **实时推理**：支持千问系列（如 `qwen3.8-max`、`qwen3.7-plus`）、DeepSeek、GLM、Kimi 等主流文本生成模型，覆盖华北2（北京）、美国（弗吉尼亚）、新加坡、德国（法兰克福）、日本（东京）、中国香港六大区域；部分模型（如 `qwen3.8-max`）在不同地域价格存在显著差异，需按实际部署区域查价 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **模型训练**：支持文本生成（千问、DeepSeek、GLM）、图像生成（万相、千问VL）、视频生成（万相）、语音合成（CosyVoice）等多模态模型微调，计费基于训练 [Token](../concepts/token.md) 总量，单价因模型架构与训练方式（如 `max_steps`、`n_epochs`）而异 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **模型部署与吞吐预留**：提供 PTU（预置吞吐单元）和 TPM 预留两种高性能部署方案，支持标准模式（TPS 与 API 一致）与高速模式（TPS 提升 1.5~2 倍），并支持长输入阶梯系数与缓存折算 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **成本优化工具**：提供 AI 通用型节省计划（承诺月消费换阶梯折扣）、模型专属节省计划、资源包及 [Token](../concepts/token.md) Plan 四类优惠方案，其中 AI 通用型节省计划覆盖最广，推荐作为首选 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

## 关键参数

- **[Token](../concepts/token.md) 计费粒度**：模型调用按输入/输出 Token 分别计费，单价单位为“每百万 Token”；训练按训练 Token 总量计费，单价单位为“每千 Token”；吞吐预留按输入（万 TPM/天）与输出（千 TPM/天）分别报价。
- **阶梯计费**：部分模型（如 `qwen3.7-plus`）对输入 Token 实行阶梯定价，单次请求所有 Token 均按最高所属阶梯单价结算，例如输入 100K Token 落入 `(256K, 1M]` 区间，则全部按该区间单价计费。
- **缓存折算系数**：上下文缓存命中时，输入 Token 按特定系数（如 `qwen3.8-max` 为 0.125）折算消耗的预留容量，但不影响输出容量 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **长输入阶梯系数**：针对超长输入（如 `qwen3.7-flash-2026-07-15`），Token 消耗按输入长度分段乘以不同系数（如 `(0,32K]` 为 1x，`(32K,256K]` 为 3x），再叠加缓存折算。
- **免费额度有效期**：新人免费额度有效期为 90 天，自开通百炼、模型发布或申请通过之日三者中**最晚者**起算；2025年9月8日11点前开通用户可能不足90天 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。

> **注意**：文档 1 中 `qwen3.7-plus` 在华北2（北京）的免费额度标注为“100万Token”，但文档 2 明确指出“不同模型（含同一模型的不同快照版本）的免费额度相互独立”，且文档 2 的已下架列表中包含 `qwen-plus-2025-12-01` 等大量 `qwen-plus` 系列快照，而文档 1 中 `qwen3.7-plus-2026-05-26` 等快照未被下架。这表明 `qwen3.7-plus` 主干版本与快照版本额度不互通，开发者必须严格按 `model` 参数指定的完整 ID（如 `qwen3.7-plus-2026-05-26`）使用对应额度，不可混用。

## 使用方式

- **调用接入**：统一使用百炼通用 API Key 与 Base URL，无需为节省计划、资源包或 Token Plan 单独配置凭证；费用在结算时自动按抵扣顺序抵扣 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **免费额度使用**：开通实名认证后系统自动发放，仅限华北2（北京）地域的指定模型；额度为输入/输出 Token 共用总额度，调用时自动扣减；可通过控制台“免费额度”页面开启“用完即停”功能，额度耗尽时返回 HTTP 403 错误（错误码 `AllocationQuota.FreeTierOnly`），避免意外扣费 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **吞吐预留扩容/缩容**：预付费实例扩容按剩余有效期天数向上取整计费；缩容退款按已使用小时数向上取整 × 惩罚系数（≤30天为1.2倍，>30天为1.0倍）计算；后付费实例扩容/缩容均按实际分钟数计费，无退款 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **预算设置**：在控制台“预算管理”页面，可为账号、业务空间或 API Key 设置月度预算；开启“达到预算后立即停止”后，费用达限时 API 调用将返回 HTTP 429 错误，但 PTU 溢出部分及应用调用暂不支持此限制 [原文标题](../../raw/model-user-guide/test-1/budget-management.md)。

## 限制和注意事项

- **地域限制**：新人免费额度、部分模型训练（如 CosyVoice）仅支持华北2（北京）地域；其他地域模型无免费额度，且调用价格普遍高于北京 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **额度不共享**：免费额度、节省计划额度、资源包额度均按模型 ID（含日期快照）严格隔离，`qwen3.7-plus` 与 `qwen3.7-plus-2026-05-26` 视为两个独立模型，额度不可互通。
- **不支持抵扣项**：模型训练、模型部署（PTU/DTU）、联网搜索插件、MCP 广场、通义深度搜索、案例检索、知识库规格费用（运行时长）等均**不支持**用 AI 通用型节省计划抵扣 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **欠费隔离**：账户欠费按商品 Code 隔离，例如“百炼容量预留”欠费仅影响 PTU 服务，不影响模型调用；但已欠费的商品 Code 下，即使有免费额度或节省计划，也无法抵扣 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **账单延迟**：模型推理账单通常 2~10 分钟出账，批量推理、训练等为小时级出账；账单明细仅支持查询 2026年4月1日及之后数据，历史数据需在阿里云费用与成本中心逐月导出汇总 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 来源文档

- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [预算管理](../../raw/model-user-guide/test-1/budget-management.md)


