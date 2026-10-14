# test 1

`test 1` 是阿里云百炼平台面向开发者的核心计费与资源管理主题，涵盖模型调用、训练、部署、吞吐预留等全链路费用模型。其核心逻辑是：**免费额度优先抵扣 → 节省计划/资源包次之 → 最终按量付费**，且不同计费场景（推理、训练、部署）适用完全独立的规则体系。开发者需根据业务稳定性、调用量规模和地域分布，组合使用免费额度、节省计划、吞吐预留等工具实现成本可控。

## 支持的模型/功能

- **实时推理**：支持千问（Qwen3.x 系列）、DeepSeek、GLM、Kimi、CosyVoice、万相（WanX）、Qwen-VL 等主流文本、多模态、语音、视频模型，覆盖华北2（北京）、新加坡、美国（弗吉尼亚）、德国（法兰克福）、日本（东京）、中国香港等多地域 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **模型训练**：支持文本生成（千问、DeepSeek）、图像生成（万相、千问图像）、视频生成（万相图生视频）、语音合成（CosyVoice）四类调优任务，按训练 [Token](../concepts/token.md) 总量计费 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **模型部署**：提供 PTU（预置吞吐）、DTU（模型单元）等多种部署形态，支持长输入、上下文缓存等高级特性 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **吞吐预留（TPM 预留）**：支持标准模式（等同于普通 API TPS）与高速模式（1.5~2 倍 TPS），可按天、8 小时时段或小时（仅高速）购买 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。

> **注意**：文档 3 和文档 4 对 `qwen3.7-flash-2026-07-15` 的最长输入 [Token](../concepts/token.md) 描述存在矛盾——文档 3 标注为 `128K`，而文档 4 明确标注为 `1M`。实际以控制台模型广场详情页或 [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md) 中“最长输入 [Token](../concepts/token.md)”字段为准，建议调用前通过 `GET /v1/models/{model}` 接口确认。

## 关键参数

- **Token 计量**：所有按量计费场景（推理、训练、部署）均以 Token 为基本单位。输入/输出 Token 分开计费，缓存命中部分按特定折算系数（如 0.1–0.25）计算 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **TPM（Tokens Per Minute）**：吞吐预留的核心容量单位，kTPM = 1,000 Tokens/分钟；输入单价按“万TPM·天”报价，输出单价按“千TPM·天”报价 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **阶梯计费**：部分模型（如 `qwen3.7-plus`）对输入 Token 实行阶梯定价（如 0–256K、256K–1M），单次请求所有 Token 均按最高档位单价结算 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **免费额度有效期**：自开通百炼、模型发布或申请通过之日起 90 天（以较晚者为准），但 2025年9月8日11点前已开通的用户可能不足 90 天 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 使用方式

- **调用推理**：使用通用 API Key + 百炼 Base URL（如 `https://dashscope.aliyuncs.com/compatible-mode/v1`），系统自动按 `免费额度 > 资源包 > 节省计划 > 按量付费` 顺序抵扣 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **启用免费额度**：首次开通华北2（北京）地域百炼服务后自动发放，无需实名认证即可使用；未认证用户额度用尽后自动停服，已认证用户则转为按量付费 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **购买节省计划**：推荐选用 [AI 通用型节省计划](https://common-buy.aliyun.com/?commodityCode=sfm_GenAI_spn_cn)，承诺月消费金额换取阶梯折扣（最高 5.3 折），覆盖绝大部分阿里直供模型，一次购买跨模型通用 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **设置预算**：在[预算管理](https://bailian.console.aliyun.com/cn-beijing/costing-balance/budget)页面，可为账号、业务空间或单个 API Key 设置月度预算，并开启「达到预算后立即停止」以自动熔断调用（生产环境慎用） [原文标题](../../raw/model-user-guide/test-1/budget-management.md)。

## 限制和注意事项

- **地域隔离**：免费额度、节省计划、吞吐预留均严格限定地域。例如，在华北2（北京）购买的节省计划，仅能抵扣该地域产生的费用，无法跨地域使用 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **免费额度不覆盖范围**：Batch 调用、模型调优、模型部署、PAI-DSW、OSS 存储、联网搜索插件等费用**均不可用免费额度抵扣** [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **专属 API Key 例外**：Token Plan/Coding Plan 的专属 API Key 不消耗免费额度，调用直接按量付费；如需使用免费额度，必须改用通用 API Key [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **出账延迟风险**：模型推理账单通常在调用结束后 2–10 分钟生成，但“预占+月结”模式下实际扣款在次月初。若依赖“免费额度用完即停”，需注意控制台显示的剩余额度存在分钟级延迟，可能导致额度耗尽后仍产生少量费用 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **欠费全局影响**：阿里云账户可用额度 < 0（即欠费）时，**即使模型仍有免费额度或节省计划剩余额度，所有按量付费调用也将被拒绝**。务必确保主账号余额充足 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [预算管理](../../raw/model-user-guide/test-1/budget-management.md)


