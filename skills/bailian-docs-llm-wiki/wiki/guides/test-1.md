# test 1

`test 1` 是阿里云百炼平台面向开发者提供的模型服务计费与成本管理核心主题，涵盖新人免费额度、按量调用、模型训练/部署、节省计划及账单溯源等全链路规则。本文档整合官方最新策略，聚焦华北2（北京）地域主流通用模型（如 `qwen3.8-max`、`qwen3.7-plus` 等），明确各计费场景的适用范围、抵扣优先级与实操约束，避免因规则误读导致意外扣费或服务中断。

## 支持的模型/功能

- **实时推理（支持免费额度）**：`qwen3.8-max`、`qwen3.7-plus`、`qwen-max` 等文本生成模型在华北2（北京）地域享有独立免费额度（通常为 100 万 Token），详见[新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。  
- **不支持免费额度的场景**：[Batch调用](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)、模型调优、[模型部署](../concepts/model-deployment.md)、PAI-DSW、OSS 存储及请求费用均**不可抵扣**免费额度 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。  
- **模型训练与部署**：支持千问系列（Qwen3/VL）、万相（WanX）、CosyVoice 等多模态模型的微调与专属部署，但其费用独立于推理计费，需单独购买 [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。  
- **上下文缓存与 Batch 调用**：部分模型（如 `qwen3.8-max`）支持缓存折扣和 Batch 半价，但二者**不能同时生效**，且缓存单价未包含在基础价格表中 [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)。

> **注意**：文档 3 中 `qwen3.8-max` 在华北2（北京）的输入单价标为 12 元/百万 Token，而文档 2 中同模型 PTU 部署的“后付费输入”单价为 ¥28.8 / Per 10K TPM/小时。二者计费维度不同（Token vs TPM），但若用户误将部署单价理解为推理单价，可能导致成本预估偏差。务必区分「实时推理」与「PTU 部署」两类服务。

## 关键参数

- **免费额度有效期**：90 天，自开通百炼、模型发布或申请通过日起计算（以较晚者为准）；2025年9月8日11点前开通的用户有效期可能不足90天 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。  
- **Token 计费粒度**：按实际消耗的输入/输出 Token 总数计费，免费额度剩余量为二者共用总额度，不单独区分 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。  
- **阶梯计费阈值**：部分模型（如 `qwen3-max`）按单次请求输入 Token 数分档（如 0–32K、32K–128K），该请求所有 Token 均按对应档位单价结算 [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)。  
- **抵扣优先级顺序**：`免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费`，此顺序直接影响费用归属，例如开启「免费额度用完即停」后，节省计划无法触发抵扣 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 使用方式

- **免费额度启用**：首次开通百炼后自动发放，无需实名认证；调用时系统自动优先抵扣，无需额外配置 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。  
- **节省计划选购**：推荐优先选用 [AI 通用型节省计划](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)，覆盖绝大部分阿里直供模型（A 类），承诺周期越长、月消费额越高，折扣越大（最高 5.3 折）。  
- **资源包匹配规则**：严格按模型 ID 匹配（如 `qwen-plus` 资源包不可用于 `qwen-max`），跨版本不通用；购买后立即生效，有效期依档位而定（如 1,000 元档为 6 个月） [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。  
- **账单溯源操作**：通过账单详情页的 `实例 ID（出账粒度）` 字段（格式：`ApiKeyID;业务空间ID;模型名称;输入/输出类型;调用渠道`）可精准定位费用来源 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 限制和注意事项

- **地域限制**：免费额度仅限华北2（北京）地域；其他地域（如美国、新加坡）模型无免费额度，且价格存在差异（如 `qwen3.8-max` 在新加坡输入单价为 14.988 元/百万 Token） [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)。  
- **免费额度用完即停（安心模式）**：未认证用户强制开启，额度耗尽返回 `AllocationQuota.FreeTierOnly` 错误；已认证用户可手动开关，但开启后节省计划无法抵扣，需关闭该功能才能恢复付费调用 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。  
- **账户欠费影响**：即使模型仍有免费额度或节省计划剩余额度，只要阿里云账户整体可用额度 < 0，所有模型调用将被拒绝 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。  
- **出账延迟风险**：模型推理账单通常 2–10 分钟出账，但“预占+月结”模式下实际扣款在次月初完成；配置变更（如关闭用完即停）存在生效延迟，可能导致额度耗尽后仍产生费用 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)


