# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与资源管理主题，涵盖模型调用、训练、部署的全链路成本结构。本文档聚焦于实时推理（模型调用）的免费额度机制、计费模型、关键参数约束及成本控制手段，不涉及模型能力、SDK 使用或业务集成逻辑。所有信息均基于华北2（北京）地域的主流文本生成模型（如 `qwen3.8-max`、`qwen3.7-plus` 等）整理，其他地域价格与额度规则存在显著差异。

## 支持的模型/功能

- **支持免费额度的模型**：仅限华北2（北京）地域的指定模型，包括 `qwen3.8-max`、`qwen3.7-plus`、`qwen3.6-plus`、`qwen3.5-plus`、`qwen-plus` 及其带日期后缀的快照版本（如 `qwen3.7-plus-2026-05-26`），以及 `qwen-max` 等。同一模型的不同快照版本视为独立模型，各自拥有 100 万 Token 的免费额度，额度不互通 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **不支持免费额度的场景**：Batch 调用、模型调优、模型部署、PAI-DSW、OSS 存储及请求费用均不可用免费额度抵扣 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **功能覆盖**：免费额度仅适用于实时推理调用；上下文缓存、Function Calling、网页抓取等原生工具调用产生的费用可被 AI 通用型节省计划抵扣，但**不参与免费额度消耗** [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

> **注意**：文档 2 中列出的 `qwen3.8-max-prime` 明确标注“无免费额度”，而文档 1 中未提及该模型。这表明 `qwen3.8-max-prime` 属于明确排除在免费额度覆盖范围外的特殊型号，开发者需特别注意其调用将直接触发按量付费。

## 关键参数

- **Token 计费粒度**：输入与输出 Token 共用总额度，不单独区分；免费额度剩余量为两者之和 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **阶梯计费阈值**：部分模型（如 `qwen3-max`、`qwen3.6-plus-preview`）按单次请求输入 Token 总量分档计价，例如 `0<Token≤32K`、`32K<Token≤128K`，且该请求所有 Token 均按对应阶梯单价结算 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **地域绑定性**：免费额度、节省计划、资源包均严格绑定地域。华北2（北京）购买的节省计划**仅抵扣该地域产生的调用费用**，跨地域调用（如从新加坡地域 API 调用北京模型）不适用 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **API Key 类型**：通用 API Key 可消耗免费额度；Token Plan/Coding Plan 专属 API Key **不消耗免费额度**，调用即按量付费 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 使用方式

- **开通即用**：首次开通百炼后，系统自动发放免费额度，无需实名认证即可使用；额度通常两小时内生效 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **抵扣优先级**：系统按固定顺序抵扣费用：**免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费**。开启“免费额度用完即停”后，额度耗尽服务立即停止，节省计划无法介入抵扣 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **查看剩余额度**：可通过三种方式实时查询：① 控制台[免费额度页面](https://bailian.console.aliyun.com/cn-beijing/costing-balance/free-quota)；② 模型广场详情页的“免费额度”区域；③ [模型用量页面](https://bailian.console.aliyun.com/cn-beijing/costing-balance/usage-statistics) [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **成本优化选型**：
  - 长期稳定使用 → 优先选择 **AI 通用型节省计划**（最高 5.3 折，覆盖绝大部分阿里直供模型）；
  - 用量小或集中单个模型 → 选用 **资源包**（按模型名称严格匹配，跨版本不通用）；
  - 团队协作共享 → 选用 **Token Plan**（额度独立于账户余额） [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

## 限制和注意事项

- **有效期硬约束**：免费额度有效期为 90 天，自开通百炼、模型发布或申请通过日起计算（以较晚者为准）。2025年9月8日11点前开通的用户，有效期可能不足 90 天；过期后额度自动作废，不补发、不延期 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **地域强限制**：仅华北2（北京）地域模型享有免费额度；美国、新加坡、德国、日本等地域模型**无免费额度**，且价格显著高于北京 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **欠费全局影响**：账户可用额度 < 0（即欠费）时，**即使模型仍有免费额度、节省计划或资源包剩余额度，所有模型调用均会失败**。必须结清欠费才能恢复服务 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **额度耗尽行为差异**：
  - 未认证用户：额度用完后**立即无法调用**，需完成实名认证并充值；
  - 已认证用户：若未开启“免费额度用完即停”，将自动转为按量付费；若已开启，则返回 HTTP 403 错误（错误码 `AllocationQuota.FreeTierOnly`） [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)


