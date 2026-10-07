# test 1

`test 1` 是阿里云百炼平台面向开发者提供的模型服务计费与资源管理核心主题，涵盖模型调用、训练、部署、吞吐预留、成本优化及预算控制等全链路能力。本文档整合官方最新技术文档，明确各能力的适用范围、关键参数与使用约束，帮助开发者快速建立清晰的成本认知与技术选型依据。所有信息均基于华北2（北京）地域主推能力，跨地域部署需单独评估。

## 支持的模型/功能

`test 1` 覆盖百炼平台主流模型服务类型，包括文本生成（千问系列）、多模态（千问VL、万相）、语音（CosyVoice、Qwen-ASR/TTS）及视频生成模型。其中，**文本生成模型**是核心载体，支持标准推理、Batch调用、上下文缓存、思考模式（Chain-of-Thought）等多种功能形态。需注意，[Batch调用](raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)和[模型调优](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)虽属同一模型ID，但其计费规则、免费额度适用性与实时推理完全独立。例如，`qwen3.8-max` 的 Batch 调用单价为实时推理的 50%，但其产生的费用**不享受新人免费额度抵扣** [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。

> **注意**：文档 2 中“千问Max”表格列出 `qwen3.8-max-prime` 模型，标注“无免费额度”，而文档 1 明确说明“仅华北2（北京）地域模型享有免费额度”。但文档 2 同一表格中 `qwen3.8-max` 在华北2（北京）列明确标注“100万[Token](../concepts/token.md)”，且文档 1 的“适用范围”章节强调“带日期后缀的快照版本（如 `qwen-max-2026-05-17`）与不带日期的最新版本（如 `qwen-max`）视为两个独立模型”。因此，`qwen3.8-max-prime` 作为独立模型 Code，其“无免费额度”的标注与文档 1 规则一致，并非矛盾，而是模型粒度隔离的体现。

## 关键参数

核心计费参数围绕 [Token](../concepts/token.md) 和吞吐量（TPM/TPU）展开：
- **[Token](../concepts/token.md) 计费**：输入/输出 Token 分开计价，单价按模型、地域、阶梯区间（如 0–32K、32K–128K）动态变化。例如 `qwen3-max` 在华北2（北京）的输入单价为 2.5 元/百万Token（0–32K 区间），超出则升至 4 元/百万Token [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **TPM 预留**：吞吐预留（原 TPM 预留）以 kTPM（千 Tokens/分钟）为单位购买，分标准模式（与普通 API TPS 相同）和高速模式（1.5–2 倍 TPS）。容量换算需考虑长输入阶梯系数与缓存折算系数，例如 `qwen3.7-flash-2026-07-15` 对 50K 输入 Token，前 32K 按 1x、超出部分按 3x 折算 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **训练 Token**：模型训练费用 = 训练数据 Token 总数 × 循环次数 × 训练单价。不同模型单价差异巨大，如 `qwen3.8-27b` 为 0.05 元/千Token，而 `qwen3.7-plus-2026-05-26` 高达 0.35 元/千Token [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。

## 使用方式

开发者可通过多种方式接入并管理 `test 1` 相关资源：
- **API 调用**：使用通用 API Key（非 Token Plan 专属 Key）发起 HTTP 请求，系统自动按 `免费额度 > 资源包 > 节省计划 > 按量付费` 顺序抵扣费用。调用时需指定 `model` 参数（如 `qwen3.8-max`）及 `base_url`（华北2（北京）为 `https://dashscope.aliyuncs.com/compatible-mode/v1`）。
- **成本优化**：推荐优先采用 [AI 通用型节省计划](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)，承诺月消费金额可享最高 5.3 折，覆盖绝大部分阿里直供模型；小规模或特定模型场景可选用资源包。所有方案均需在控制台或费用中心购买，现金支付。
- **预算管控**：通过 [预算管理](../../raw/model-user-guide/test-1/budget-management.md) 功能，可为账号、业务空间或单个 API Key 设置月度费用上限，并选择“达到预算后立即停止”以自动熔断调用，防止意外超支。

## 限制和注意事项

- **地域限制**：新人免费额度、部分模型训练（如 CosyVoice）及默认 Base URL 仅支持华北2（北京）地域。其他地域（如新加坡、美国）虽可调用，但无免费额度且价格更高，需单独购买节省计划 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **额度与服务状态强耦合**：开启“免费额度用完即停”后，额度耗尽将返回 `HTTP 403` 错误（错误码 `AllocationQuota.FreeTierOnly`），此时即使账户余额充足，节省计划也无法生效，必须手动关闭该开关才能恢复 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **账单延迟与费用归属**：模型推理账单存在 2–10 分钟出账延迟，而模型训练、知识库等为小时级出账。账单中的“实例 ID（出账粒度）”字段（格式为 `ApiKeyID;业务空间ID;模型名称;...`）是精准溯源费用归属的唯一依据，而非“商品名称” [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **服务停止非瞬时**：无论是预算用尽、免费额度耗尽还是欠费，服务停止均存在延迟，延迟期内产生的费用仍会正常计收。生产环境应避免依赖“立即停止”机制，而应结合预警与主动关停（如删除 API Key）进行风控。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [预算管理](../../raw/model-user-guide/test-1/budget-management.md)


