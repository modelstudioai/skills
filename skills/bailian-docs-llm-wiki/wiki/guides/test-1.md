# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与资源管理主题，涵盖模型调用、训练、部署及成本控制的全链路规则。本文整合官方文档，明确免费额度适用范围、各计费模式的关键参数与使用约束，并指出关键注意事项，帮助开发者规避意外扣费与服务中断风险。所有计费行为均以实际出账为准，控制台显示数据存在分钟级延迟 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 支持的模型/功能

- **实时推理**：支持千问（Qwen）、DeepSeek、GLM、Kimi 等主流文本生成模型，以及万相（WanX）、Qwen-VL、CosyVoice 等多模态与语音模型。所有模型均按输入/输出 [Token](../concepts/token.md) 或等效单位计费。
- **模型训练**：支持文本生成（千问系列）、图像生成（万相、Qwen-Image）、视频生成（万相 i2v）、语音合成（CosyVoice）四类调优任务，按训练 [Token](../concepts/token.md) 总量计费 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **模型部署**：提供 PTU（预置吞吐）与 DTU（算力单元）两种部署方式，前者按 TPM 容量预付费，后者按实例时长后付费。
- **高级能力**：上下文缓存、Batch 调用、联网搜索（独立计费）等功能均被支持，但其费用归属与抵扣规则各异。

> **注意**：免费额度**仅抵扣实时推理费用**，明确不覆盖模型训练、模型部署、Batch 调用、知识库、PAI-DSW、OSS 存储及联网搜索插件等 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 关键参数

| 参数类别 | 关键字段 | 说明 |
|----------|----------|------|
| **[Token](../concepts/token.md) 计费** | `input_token`, `output_token` | 实时推理按实际消耗的输入/输出 Token 数计费；阶梯计费按单次请求总输入 Token 所属区间统一单价结算 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。 |
| **训练计费** | `training_token_total`, `max_steps`, `n_epochs`, `max_pixels` | 训练费用 = 训练 Token 总量 × 单价；不同模型计算逻辑不同（如图像模型依赖 `max_pixels` 与 `n_epochs`，视频模型依赖计费时长与 `max_pixels`）[原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。 |
| **吞吐预留（TPM）** | `input_kTPM`, `output_kTPM`, `capacity_coefficient` | 预留容量按 kTPM（千 Token/分钟）购买；长输入与缓存命中按模型专属系数折算实际消耗 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。 |
| **节省计划** | `monthly_commitment`, `commitment_period`, `discount_tier` | AI 通用型节省计划按月承诺消费额换取阶梯折扣（最高 5.3 折），额度按动态月发放，当月未用完自动清零 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。 |

## 使用方式

1. **开通与初始化**：首次开通百炼即自动获得华北2（北京）地域模型的新人免费额度（通常 100 万 Token），无需实名认证即可使用 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
2. **调用模型**：
   - 实时推理：使用通用 API Key 发起 HTTP 请求，系统自动按 `免费额度 > 资源包 > 节省计划 > 按量付费` 顺序抵扣。
   - Batch 调用：需显式指定兼容 OpenAI 的 Batch 接口，其 Token 单价为实时推理的 50%，但**不享受免费额度抵扣** [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。
3. **购买资源**：
   - 免费额度用尽后，可购买 AI 通用型节省计划（推荐）、模型专属节省计划或 Token 资源包。
   - 吞吐预留（TPM）需在控制台创建，生成专属 `model` Code 替换原调用参数。
4. **成本管控**：
   - 设置预算：在[预算管理](https://bailian.console.aliyun.com/cn-beijing/costing-balance/budget)页面为账号、业务空间或 API Key 设置月度上限，开启「达到预算后立即停止」可自动限流。
   - 开启「免费额度用完即停」：防止额度耗尽后产生意外按量费用，但会中断服务 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 限制和注意事项

- **地域限制**：免费额度、部分模型训练（如 CosyVoice）及多数部署服务**仅限华北2（北京）地域**；其他地域（如新加坡、美国）无免费额度，且价格不同 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **额度独立性**：不同模型（含同一模型的不同快照版本，如 `qwen-max` 与 `qwen-max-2026-05-17`）的免费额度相互独立，不互通、不共享；额度到期（90 天）或耗尽后自动失效，不可补发 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **抵扣优先级冲突**：若开启「免费额度用完即停」，额度耗尽后服务将返回 `403 AllocationQuota.FreeTierOnly` 错误，此时**节省计划无法生效**，必须手动关闭该开关才能恢复抵扣 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **出账延迟**：模型推理账单通常在调用结束后 2–10 分钟生成，批量任务与训练任务为小时级出账；控制台显示的剩余额度为分钟级更新，操作前务必手动刷新页面 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **账户欠费影响**：阿里云账户整体欠费（可用额度 < 0）时，**即使模型仍有免费额度或节省计划余额，所有按量调用均会失败**；需结清全部阿里云产品欠费方可恢复 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [预算管理](../../raw/model-user-guide/test-1/budget-management.md)


