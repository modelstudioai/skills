# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与成本管理主题，涵盖模型调用、训练、部署及资源预留等全链路费用机制。本文整合官方文档，明确免费额度适用范围、各计费模式的关键参数与使用约束，并指出关键注意事项与潜在矛盾点，帮助开发者快速建立成本控制认知。所有价格与规则均以华北2（北京）地域为默认基准，跨地域调用需单独评估。

## 支持的模型/功能

- **实时推理（按量调用）**：支持千问系列（如 `qwen3.8-max`、`qwen-plus`）、DeepSeek、GLM、Kimi 等主流文本生成模型，以及部分 VL、ASR、TTS 模型。**注意**：免费额度仅覆盖实时推理，[Batch调用](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)、模型调优、模型部署、PAI-DSW、OSS 存储等均不抵扣 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **模型训练**：支持千问（文本/多模态）、万相（图像/视频）、CosyVoice（语音）等模型微调，按训练 Token 总量计费，单价因模型类型与超参配置差异显著 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **模型部署（PTU/DTU）**：提供预置吞吐（PTU）和独占吞吐（DTU）两种部署模式，支持标准与高速（1.5–2×TPS）性能档位，按输入/输出 TPM 容量与使用时长计费 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **吞吐预留（TPM 预留）**：支持标准模式（与 API 同 TPS）与高速模式（PTU），可按天、8 小时时段或小时（仅高速）购买，容量单位为 kTPM（1,000 Tokens/分钟） [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。

## 关键参数

| 参数类别 | 名称 | 说明 | 示例值/范围 |
|----------|------|------|-------------|
| **通用** | 免费额度有效期 | 自开通/模型发布/申请通过日起 90 天（以较晚者为准）；2025年9月8日前开通用户可能不足90天 | 90 天 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md) |
| **调用计费** | 输入/输出单价 | 按百万 Token 计价，分阶梯（如 `0<Token≤1M`）；Batch 调用享 50% 折扣；思考模式（思维链）输出单价通常高于非思考模式 | `qwen3.8-max`：输入 ¥12/MTok，输出 ¥36/MTok（华北2） [原文标题](../../raw/model-user-guide/test-1/model-pricing.md) |
| **训练计费** | 训练 Token 总量 | 因模型类型而异：文本模型 = (数据 Token + 混合数据 Token) × 循环次数；图像模型 ≈ `max_steps × Lmax`；视频模型 = `∑(视频计费时长) × max_pixels/1024 × n_epochs` | `wan2.7-i2v`：`Lmax=12,800`（t2i, 1k） [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md) |
| **部署/预留** | 容量单位 | 输入按 **万TPM**（10,000 Tokens/分钟）报价，输出按 **千TPM**（1,000 Tokens/分钟）报价；购买量单位为 kTPM（1,000 Tokens/分钟） | 输入起步 200 kTPM，输出起步 20 kTPM [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md) |
| **节省计划** | 承诺周期 | 动态月制：从生效日起每满 30 天为一个周期，额度当月未用完自动清零，不累积 | 3/6/12/24 个月 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md) |

> **注意**：文档 4（`model-pricing.md`）中 `qwen3.7-plus` 在“华北2（北京）”表格标注“当前能力等同于 `qwen3.7-plus-2026-05-26`”，但同一文档美国地域表格中又将 `qwen3.7-plus` 与 `qwen3.7-plus-2026-05-26` 并列列出且价格一致。这暗示二者在功能与计价上已无实质区别，但命名冗余易引发混淆，建议统一使用带日期后缀的 Code 以确保精确性。

## 使用方式

- **启用免费额度**：完成阿里云实名认证后，开通华北2（北京）地域百炼服务即自动发放（100 万 Token/模型），无需手动领取；额度仅限该地域实时推理使用 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **调用模型**：使用通用 API Key 与对应地域 Base URL 发起 HTTP 请求；若开启「免费额度用完即停」，额度耗尽将返回 `HTTP 403` 错误（错误码 `AllocationQuota.FreeTierOnly`） [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **购买节省计划**：推荐首选 [AI 通用型节省计划](https://common-buy.aliyun.com/?commodityCode=sfm_GenAI_spn_cn)，承诺月消费额换取阶梯折扣（最高 5.3 折），覆盖绝大部分阿里直供模型；购买后自动生效，费用按[抵扣顺序](https://help.aliyun.com/zh/model-studio/savings-plan-and-resource-package#h3-deduction-order)自动抵扣 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **设置预算**：在[预算管理](https://bailian.console.aliyun.com/cn-beijing/costing-balance/budget)页面，按账号/业务空间/API Key 维度设置月度预算；开启「达到预算后立即停止」可自动限制按量调用（返回 429），但**生产环境不建议开启** [原文标题](../../raw/model-user-guide/test-1/budget-management.md)。
- **查询账单**：实时推理账单分钟级出账（2–10 分钟），批量/训练类账单小时级出账；关键字段 `资产/资源实例ID（出账粒度）` 以 `;` 分隔，格式为 `ApiKeyID;业务空间ID;模型名称;输入/输出类型;调用渠道;免费额度用完即停标识`，用于精准溯源 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 限制和注意事项

- **地域强绑定**：免费额度、节省计划、吞吐预留均严格按地域隔离。华北2（北京）购买的节省计划**无法抵扣**新加坡地域调用费用；不同地域需分别购买 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **额度不互通**：各模型（含不同快照版本，如 `qwen-max` 与 `qwen-max-2025-01-25`）的免费额度相互独立，不可合并或转移；系统不会自动切换至有额度的其他模型 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **缓存计费特殊性**：上下文缓存的创建与命中 Token 采用独立单价（如创建按标准输入价 125%，命中按 10%），本文价格表中的输入单价**不含**缓存单价，需另行查阅 [上下文缓存](../../raw/model-user-guide/model-experience/text-generation-model/context-cache.md) 文档 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **欠费隔离**：欠费按商品 Code 隔离。例如 `百炼容量预留` 欠费仅导致 PTU 服务不可用，不影响 `百炼大模型推理` 的正常使用 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **停止计费操作**：下线部署模型仅停止其调用费用；对于预付费（按天）的吞吐预留，**必须在[退订管理](https://billing-cost.console.aliyun.com/refund/refund)页面主动退订**，否则到期后仍会按规则延后2小时停机并保留14小时资源，产生额外费用 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [预算管理](../../raw/model-user-guide/test-1/budget-management.md)


