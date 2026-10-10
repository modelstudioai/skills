# test 1

`test 1` 是百炼平台面向开发者提供的统一计费与成本管控主题，涵盖模型调用、训练、部署、吞吐预留等核心场景的定价规则、使用约束及管理工具。本文整合官方文档，聚焦可执行的技术要点，明确各计费模式的适用边界、关键参数含义及常见冲突点，帮助开发者快速选型并规避意外扣费风险。

## 支持的模型/功能

`test 1` 主要覆盖以下模型与能力的计费体系：

- **文本生成模型**：千问系列（如 `qwen3.8-max`、`qwen3.7-plus`）、GLM、DeepSeek、Kimi 等，支持非思考/思考双模式，部分模型提供优速模式（Prime）[原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **多模态模型**：千问VL、万相（图像/视频生成）、Qwen-Image 等，其训练与推理计费规则独立于纯文本模型 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **语音模型**：CosyVoice、Qwen-TTS、Paraformer 等，仅华北2（北京）地域支持调优，且训练费用按 [Token](../concepts/token.md) 消耗量单独计价 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **向量与排序模型**：Embedding 和 Rerank 模型，其调用费用可被 AI 通用型节省计划抵扣，但规格费用（如知识库运行时长）不在此列 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

> **注意**：文档中 `qwen3.7-max` 多次声明“当前能力等同于 `qwen3.7-max-2026-05-20`”，但同一表格中又将二者列为独立模型并分别列出价格与免费额度。该表述与[新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)中“带日期后缀的快照版本与不带日期的最新版本视为两个独立模型”的原则矛盾。实际计费以模型 ID 为准，二者为不同实体，不可互换或共享额度。

## 关键参数

- **[Token](../concepts/token.md) 计费粒度**：所有按量计费均以 **1 [Token](../concepts/token.md)** 为最小单位，输入/输出 Token 分开结算；缓存命中 Token 按折扣单价计费（如 10%），但显式缓存创建 Token 按 125% 计费 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **TPM（Tokens Per Minute）容量单位**：吞吐预留中，`kTPM = 1,000 Tokens/分钟`；输入单价按 `万TPM`（即 10 kTPM）报价，输出单价按 `千TPM`（即 1 kTPM）报价，公式中需做单位换算 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **阶梯计费区间**：部分模型（如 `qwen3.7-plus`）对输入 Token 数分档定价（如 `0<Token≤256K`、`256K<Token≤1M`），**单次请求的所有 Token 均按最高档单价结算**，非分段计费 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **长输入与缓存折算系数**：吞吐预留中，长输入 Token 按阶梯系数折算（如 `qwen3.7-flash` 在 `(32K,256K]` 区间系数为 3x），缓存命中部分再乘缓存折算系数（如 0.2），最终从购买额度中扣减 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。

## 使用方式

- **默认计费模式**：开通即启用**按量后付费**，无需预购，费用按实际 Token 消耗实时冻结、月结扣款 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **成本优化方案**：
  - **AI 通用型节省计划**：承诺月消费金额换取阶梯折扣（最高 5.3 折），覆盖绝大多数阿里直供模型，**是长期稳定使用的首选** [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
  - **资源包**：一次性购买固定 Token 量，仅适用于单个特定模型（如 `qwen-plus`），灵活性低于节省计划 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
  - **吞吐预留（TPM 预留）**：预付费购买专属推理吞吐，保障低延迟与高并发，支持标准/高速两种性能模式，超出部分按溢出策略处理 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **免费额度使用**：仅华北2（北京）地域模型享有，自动优先抵扣，无需额外配置；但使用 `Token Plan` 专属 API Key 将**跳过免费额度**，直接按量付费 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 限制和注意事项

- **地域限制**：免费额度、部分模型调优（如 CosyVoice）仅限华北2（北京）；其他地域（如美国、新加坡）模型无免费额度，且单价普遍更高 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **抵扣顺序刚性**：费用抵扣严格遵循 `免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费` 顺序，**开启「免费额度用完即停」后，服务将直接返回 403 错误，节省计划无法生效** [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **预算管理范围有限**：仅管控 API 按调用量付费产生的费用，**不包含模型训练、PTU 部署、DTU 单元、知识库规格等费用** [原文标题](../../raw/model-user-guide/test-1/budget-management.md)。
- **账户欠费影响全局**：一旦阿里云主账号欠费（可用额度 < 0），即使模型仍有免费额度或节省计划剩余额度，**所有模型调用均会失败**，必须结清欠费方可恢复 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 来源文档

- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [预算管理](../../raw/model-user-guide/test-1/budget-management.md)


