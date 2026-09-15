# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与资源管理主题，涵盖模型调用、训练、部署的全链路成本控制机制。本文档聚焦于实时推理（即模型调用）场景下的免费额度、按量计费、节省计划及资源包等关键能力，明确各方案的适用边界、抵扣顺序与实操限制。所有计费行为均以 [Token](../concepts/token.md) 实际消耗为基准，且严格遵循地域隔离原则——华北2（北京）是唯一提供新人免费额度的地域，其他地域仅支持按量付费或预付费方案。

## 支持的模型/功能

- **支持免费额度的模型**：仅限华北2（北京）地域的指定模型，如 `qwen3.8-max`、`qwen3.7-max`、`qwen3-max`、`qwen-plus` 等主流文本生成模型（含对应快照版本），每个模型独立享有 100 万 [Token](../concepts/token.md) 免费额度 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **不支持免费额度的场景**：`Batch调用`、`模型调优`、`模型部署`、自定义模型（调优后或已部署模型）、PAI-DSW、OSS 存储及请求费用均不可用免费额度抵扣 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **支持阶梯计费的模型**：`qwen3-max`、`qwen3.6-max-preview` 等在华北2（北京）地域按输入 [Token](../concepts/token.md) 区间分档定价（如 0–32K、32K–128K），单价随用量递增 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **支持上下文缓存的模型**：`qwen3.8-max`、`qwen3.7-max` 等明确标注支持缓存，但缓存创建与命中的 Token 单价与标准输入不同，本文价格表未包含缓存单价 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。

> **注意**：文档 2 中 `qwen3.8-max-prime` 明确标注“无免费额度”，而同属华北2（北京）的 `qwen3.8-max` 有 100 万 Token 免费额度；二者模型 ID 不同、能力定位不同（优速模式 vs 通用模式），额度策略存在明确区分，非矛盾信息。

## 关键参数

- **免费额度有效期**：90 天，自开通百炼、模型发布或模型申请通过之日三者中**最晚者**起算；2025年9月8日11点前开通用户有效期可能不足90天 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **抵扣优先级顺序**：`免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费`，该顺序在所有计费场景中全局生效 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **节省计划动态月规则**：AI 通用型节省计划按“动态月”分配额度（从购买日/生效日起每满30日为一周期），**当月未用完额度自动清零，不可累积至下月** [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **Token 计费粒度**：模型训练费用按训练 Token 总数 × 训练单价计算，最小计费单位为 1 token；模型部署（PTU）按 TPM（Tokens Per Minute）与时长组合计费 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。

## 使用方式

- **启用免费额度**：首次开通阿里云百炼（华北2北京）后系统自动发放，无需实名认证即可使用；调用时自动优先抵扣，无需额外配置 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **开启“免费额度用完即停”**：在控制台[免费额度页面](https://bailian.console.aliyun.com/cn-beijing/costing-balance/free-quota)或模型详情页手动开启开关，开启后额度耗尽返回 HTTP 403 错误（错误码 `AllocationQuota.FreeTierOnly`），防止意外扣费 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **购买节省计划**：推荐首选 [AI 通用型节省计划](https://common-buy.aliyun.com/?commodityCode=sfm_GenAI_spn_cn)，覆盖绝大部分阿里直供模型（A/B/C 类），支持华北2（北京）、美国（弗吉尼亚）、新加坡等多地，购买后立即生效 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **查询剩余额度**：通过三种方式实时查看：① [免费额度页面](https://bailian.console.aliyun.com/cn-beijing/costing-balance/free-quota)；② [模型广场](https://bailian.console.aliyun.com/model/market)模型详情页“免费额度”区域；③ [模型用量页面](https://bailian.console.aliyun.com/cn-beijing/costing-balance/usage-statistics) [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 限制和注意事项

- **地域强约束**：免费额度**仅华北2（北京）有效**；其他地域（如美国、新加坡、德国、日本）模型调用无免费额度，仅支持按量付费或节省计划 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **额度不互通**：同一模型的不同快照版本（如 `qwen3.7-max` 与 `qwen3.7-max-2026-05-20`）视为独立模型，各自拥有 100 万 Token 额度，不可合并或转移 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **专属 API Key 限制**：`Token Plan/Coding Plan` 专属 API Key **不消耗免费额度**，调用直接按量付费；如需使用免费额度，必须使用通用 API Key [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **出账延迟风险**：模型推理账单通常 2–10 分钟出账，但控制台显示的免费额度为分钟级更新（需手动刷新）。若未及时刷新页面，可能显示“仍有额度”但实际已耗尽，导致产生费用 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **欠费全局阻断**：账户可用额度 < 0（即欠费）时，**即使模型仍有免费额度、节省计划或资源包剩余额度，所有模型调用均将失败**；必须结清欠费后服务才可恢复 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)


