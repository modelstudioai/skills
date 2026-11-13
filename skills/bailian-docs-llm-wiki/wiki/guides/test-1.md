# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与资源管理主题，涵盖模型调用、训练、部署及成本控制的全链路规则。本文档整合了免费额度发放逻辑、多维度计费模型（按量、预留、节省计划）、账单溯源方法及主动控费手段，适用于需要精确预估成本、规避意外扣费、并进行精细化资源治理的技术团队。

## 支持的模型/功能

- **实时推理**：支持 `qwen3.8-max`、`qwen3.7-plus`、`qwen3.6-flash` 等主流千问系列模型，以及 DeepSeek、GLM、Kimi 等第三方模型（详见[模型调用价格](raw/model-user-guide/test-1/model-pricing.md)）。
- **[异步任务](../concepts/asynchronous-task.md)**：生图、生视频等异步模型调用（如 `wan2.7-i2v`）支持按任务结算，但费用延迟出账 [账单查询与成本管理](raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **模型训练与部署**：支持文本生成（Qwen、DeepSeek）、图像生成（万相、Qwen-VL）、语音合成（CosyVoice）等模型的微调与 PTU 部署 [模型训练与部署计费](raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **吞吐预留（TPU/PTU）**：提供标准模式（TPU）与高速模式（PTU），支持长输入阶梯折算与缓存命中系数优化 [吞吐预留计费](raw/model-user-guide/test-1/tpm-reservation-billing.md)。

> **注意**：文档 1 明确指出免费额度**仅抵扣实时推理费用**，而文档 3 和文档 4 中的模型训练、模型部署、吞吐预留均**不支持免费额度抵扣**。该矛盾点需严格区分使用场景，避免误判成本。

## 关键参数

- **Token 计费粒度**：输入/输出 Token 均以“每百万 Token”为单位计价；训练费用以“每千 Token”为单位（如 `qwen3-vl-8b-instruct` 为 ¥0.012/千Token）[模型训练与部署计费](raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **TPM 容量单位**：吞吐预留中，输入按“万TPM/天”报价，输出按“千TPM/天”报价；kTPM（1,000 Tokens/分钟）为购买基本单位 [吞吐预留计费](raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **免费额度有效期**：自开通/模型发布/申请通过日起 90 天（以较晚者为准），但 2025年9月8日11点前开通用户可能不足 90 天 [新人免费额度](raw/model-user-guide/test-1/new-free-quota.md)。
- **地域价格差异**：同一模型在华北2（北京）、美国（弗吉尼亚）、新加坡等地域单价不同（如 `qwen3.8-max` 在北京输入单价 ¥12/百万Token，在弗吉尼亚为 ¥14.988/百万Token）[模型调用价格](raw/model-user-guide/test-1/model-pricing.md)。

## 使用方式

- **免费额度自动生效**：完成实名认证后开通百炼即自动发放，无需手动领取；额度在华北2（北京）地域有效，其他地域无 [新人免费额度](raw/model-user-guide/test-1/new-free-quota.md)。
- **节省计划自动抵扣**：购买 AI 通用型节省计划后，使用百炼通用 API Key 与 Base URL 调用模型，费用在结算时自动按抵扣顺序抵扣，**仅抵扣生效后产生的费用** [节省计划与资源包](raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **预算控费**：在[预算管理](raw/model-user-guide/test-1/budget-management.md)中为账号、业务空间或 API Key 设置月度预算，并可开启“达到预算后立即停止”，触发时返回 HTTP 429 错误。
- **账单溯源**：通过账单详情页的 `资产/资源实例ID（出账粒度）` 字段（格式为 `ApiKeyID;业务空间ID;模型名称;输入/输出类型;调用渠道;免费额度用完即停标识`）精准定位费用来源 [账单查询与成本管理](raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 限制和注意事项

- **免费额度不可跨模型共享**：`qwen3.8-max` 与 `qwen3.8-max-2026-05-17` 视为两个独立模型，各自拥有 100 万 Token 免费额度，额度不互通 [新人免费额度](raw/model-user-guide/test-1/new-free-quota.md)。
- **[异步任务](../concepts/asynchronous-task.md)欠费风险**：生图、生视频等[异步任务](../concepts/asynchronous-task.md)提交后，即使账户后续欠费，任务仍可能执行并产生费用；充值后因结算延迟，可能再次触发欠费 [账单查询与成本管理](raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **“免费额度用完即停”功能限制**：开启后，额度耗尽时返回 `AllocationQuota.FreeTierOnly` 错误（HTTP 403），但**生产环境不建议开启**，以免服务不可用；且关闭后状态同步存在约半小时延迟 [新人免费额度](raw/model-user-guide/test-1/new-free-quota.md)。
- **节省计划不覆盖全部费用**：模型调优、模型部署、联网搜索插件、知识库规格费用等**明确不支持节省计划抵扣** [节省计划与资源包](raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [预算管理](../../raw/model-user-guide/test-1/budget-management.md)


