# test 1

`test 1` 是阿里云百炼平台面向开发者提供的模型服务计费与资源管理核心主题，涵盖新人免费额度、按量调用、模型训练、部署、吞吐预留、预算控制及成本优化等全链路计费场景。本文档整合官方最新规则，明确各能力的适用范围、关键参数与使用约束，帮助开发者快速建立成本意识并规避常见误用风险。所有计费行为均以实际出账为准，控制台显示数据存在分钟级延迟，操作前请务必刷新页面 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 支持的模型/功能

- **实时推理（按量调用）**：支持千问系列（qwen-max、qwen3.8-max 等）、DeepSeek、GLM、Kimi、Qwen-VL、Qwen-Image、WanX（万相）、CosyVoice 等主流文本、多模态、语音、视频模型。仅华北2（北京）地域模型享有新人免费额度，其他地域（如美国、新加坡、德国、日本、中国香港）无免费额度 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **模型训练**：支持文本生成（千问、DeepSeek、GLM）、图像生成（万相、千问图像）、视频生成（万相图生视频）、语音合成（CosyVoice）等模型的微调，按训练 Token 总量计费，不支持免费额度抵扣 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **模型部署（PTU/DTU）**：支持预置吞吐（PTU）和模型单元（DTU）两种部署模式，按使用时长或容量计费，同样不支持免费额度抵扣 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **吞吐预留（TPM 预留）**：提供标准模式（等同 API TPS）与高速模式（1.5–2 倍 TPS），支持按天/小时/8 小时时段预付费及后付费，支持长输入阶梯系数与缓存折算 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **成本管控工具**：包括预算管理（按账号/业务空间/API Key 设置月度限额与告警）、节省计划（AI 通用型/模型专属/资源包）、账单分账（标签绑定）等。

> **注意**：文档 2 中“千问Plus”表格内 `qwen3.5-plus-2026-04-20` 行输出单价字段在“思考模式”列存在截断（显示为 `12元` 后缺失），而同表中 `qwen3.5-plus-2026-02-15` 行完整显示为 `4.8元/12元/12元`。该不一致可能为排版错误，实际应以控制台实时价格或 [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md) 文档最新完整表格为准。

## 关键参数

| 参数类型 | 说明 | 示例/取值范围 |
|----------|------|----------------|
| **Token 计费粒度** | 输入/输出 Token 均按实际消耗计费，免费额度、按量付费、节省计划均基于此；Batch 调用享 50% 折扣，但不与上下文缓存折扣叠加 | qwen3.8-max：输入 ¥12/百万Token（北京），输出 ¥36/百万Token（北京） [原文标题](../../raw/model-user-guide/test-1/model-pricing.md) |
| **TPM 容量单位** | 吞吐预留中，输入按 **万TPM**（10,000 Tokens/分钟）报价，输出按 **千TPM**（1,000 Tokens/分钟）报价；kTPM = 1,000 TPM，公式中需换算 | 购买 200 kTPM 输入 = `200 ÷ 10 = 20` 万TPM [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md) |
| **免费额度有效期** | 自开通百炼/模型发布/申请通过日起 90 天（以较晚者为准）；2025年9月8日11点前开通用户有效期可能不足90天 | 有效期不可延期、补发或重置，过期后剩余额度自动作废 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md) |
| **预算统计周期** | 严格按自然月（1日00:00至当月最后一天24:00），非动态月；仅覆盖 API 按调用量付费，不含训练、部署、知识库等费用 | 预算管理不包含模型训练费用 [原文标题](../../raw/model-user-guide/test-1/budget-management.md) |
| **节省计划周期** | AI 通用型节省计划按**动态月**分配额度（从生效日起每满30天为一周期），当月未用完额度自动清零，不累积 | 入门型节省计划“包季”套餐（如27元抵60元）总额度分3个月按月发放，每月20元 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md) |

## 使用方式

- **调用模型**：使用通用 API Key + 对应地域 Base URL（如 `https://dashscope.aliyuncs.com/compatible-mode/v1`），系统按优先级自动抵扣：**免费额度 > 资源包 > 节省计划 > 按量付费**。Token Plan/Coding Plan 专属 API Key 不消耗免费额度，需改用通用 Key [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **启用免费额度**：首次开通华北2（北京）地域百炼即自动发放，无需认证；未认证用户额度用尽后无法调用，需认证+充值；已认证用户默认转为按量付费，可开启“免费额度用完即停”避免意外扣费 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **设置预算**：在[预算管理](https://bailian.console.aliyun.com/cn-beijing/costing-balance/budget)页面，按账号/业务空间/API Key 粒度设置月度金额与告警阈值；开启“达到预算后立即停止”将返回 HTTP 429 错误，**生产环境不建议开启** [原文标题](../../raw/model-user-guide/test-1/budget-management.md)。
- **购买节省计划**：AI 通用型节省计划推荐用于长期稳定场景，承诺月消费额换取阶梯折扣（最高5.3折），覆盖绝大部分阿里直供模型；需按地域单独购买，不可跨地域抵扣 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **管理吞吐预留**：创建后获得专属模型 Code（如 `qwen3.8-max-ptu-xxxx`），调用时需替换 `model` 参数；容量换算受长输入阶梯系数与缓存折算系数影响，需按公式精确计算实际消耗 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。

## 限制和注意事项

- **免费额度限制**：仅抵扣**实时推理**费用；Batch 调用、模型训练、模型部署、PAI-DSW、OSS 存储、联网搜索插件等均**不支持**抵扣 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。同一实名主体下主账号与 RAM 子账号共享额度，但不同模型（含快照版本如 `qwen-max` 与 `qwen-max-2026-05-17`）额度完全独立，不互通。
- **账单延迟与精度**：模型推理账单为**分钟级出账**（通常2–10分钟），非实时；批量推理、训练等为小时级出账。控制台显示的剩余额度、预算使用率均为分钟级更新，存在延迟，操作前务必手动刷新页面 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **欠费隔离机制**：欠费按**商品 Code** 隔离。例如，“百炼大模型推理”欠费将导致所有模型调用不可用，但“百炼容量预留”服务仍可运行；结清对应商品 Code 欠费后服务立即恢复 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **服务停止非即时**：开启“达到预算后立即停止”或“免费额度用完即停”后，服务停止存在延迟，延迟时段内产生的费用仍将正常收取。建议在告警阈值（如80%）时及时干预 [原文标题](../../raw/model-user-guide/test-1/budget-management.md)。
- **模型部署持续计费**：模型完成部署且状态为“运行中”即开始按时长计费，**与是否被 API 调用无关**。若不再使用，必须主动下线部署，否则费用持续产生 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [预算管理](../../raw/model-user-guide/test-1/budget-management.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)


