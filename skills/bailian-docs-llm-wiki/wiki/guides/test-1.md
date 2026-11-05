# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与资源管理主题，涵盖模型调用、训练、部署及成本控制的全链路规则。本文档整合了免费额度、按量计费、吞吐预留、节省计划、账单管理与预算控制六大模块，旨在为开发者提供清晰、可执行的成本治理依据。所有计费行为均以实际出账为准，且受地域、模型版本、调用方式等多维因素影响。

## 支持的模型/功能

- **实时推理**：支持 `qwen3.8-max`、`qwen3.7-plus`、`deepseek-v4-flash` 等主流文本生成模型，以及 `qwen3-vl-8b-instruct`、`wan2.7-i2v` 等多模态与生成类模型。所有模型均需在华北2（北京）地域开通方可享受新人免费额度 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **批量调用**：支持 [OpenAI 兼容接口](../concepts/openai-compatibility.md)的 Batch 调用，其输入/输出 [Token](../concepts/token.md) 单价为实时推理价格的 50% [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。
- **上下文缓存**：部分模型（如 `qwen3.8-max`、`qwen3.7-plus`）支持显式/隐式缓存，命中时输入 [Token](../concepts/token.md) 按折扣单价计费（如 10%），创建缓存则按标准单价的 125% 计费 [原文标题](../../raw/model-user-guide/model-experience/text-generation-model/context-cache.md)。
- **异步任务**：生图、生视频等模型采用异步机制，费用在任务完成并结算后生成，存在延迟出账风险 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

> **注意**：文档 1 明确指出免费额度**不抵扣** Batch 调用、模型调优、模型部署、PAI-DSW、OSS 存储等费用；而文档 2 在“千问Max”计费说明中却将 Batch 调用列为“影响计费的因素”，二者对 Batch 是否属于“实时推理”的界定存在逻辑冲突。实际计费以文档 1 的适用范围为准：Batch 属于独立计费项，不参与免费额度抵扣，也不享受免费额度专属价格。

## 关键参数

- **[Token](../concepts/token.md) 计量**：输入/输出 Token 统一计入免费额度总额度（如 `qwen-max` 为 100 万 Token），不区分类型 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **TPM 容量单位**：吞吐预留中，输入容量以 **万TPM**（10,000 Tokens/分钟）报价，输出以 **千TPM**（1,000 Tokens/分钟）报价，计算时需换算 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **长输入阶梯系数**：对超长输入（如 `qwen3.7-flash-2026-07-15` 输入 >32K Token），按 `(0,32K]`、`(32K,256K]`、`(256K,1M]` 分段应用 1x/3x/6x 折算系数 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **缓存折算系数**：缓存命中部分 Token 按模型专属系数折减（如 `qwen3.8-max` 为 0.125），直接影响 TPM 容量消耗 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。

## 使用方式

- **免费额度启用**：开通阿里云百炼并完成实名认证后，系统自动发放，无需手动领取；仅华北2（北京）地域有效 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **节省计划接入**：购买 AI 通用型节省计划后，使用百炼通用 API Key 与 Base URL 调用即可自动抵扣，**仅抵扣生效后产生的费用**，购买前费用不可追溯 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **吞吐预留调用**：创建成功后生成专属模型 Code（非原模型 ID），需在 API 请求中显式替换 `model` 参数，否则无法享受预留容量 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **预算控制**：在[预算管理](https://bailian.console.aliyun.com/cn-beijing/costing-balance/budget)页面设置账号/业务空间/API Key 级别月度预算，开启「达到预算后立即停止」可自动返回 HTTP 429 错误 [原文标题](../../raw/model-user-guide/test-1/budget-management.md)。

## 限制和注意事项

- **地域隔离**：免费额度、节省计划、吞吐预留均严格按地域隔离。华北2（北京）购买的节省计划**无法抵扣**美国（弗吉尼亚）地域的调用费用 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **额度时效性**：新人免费额度有效期为 90 天（以开通/模型发布/申请通过三者最晚时间起算），到期后剩余额度自动作废，不延期、不补发 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **模型快照独立性**：带日期后缀的模型快照（如 `qwen3.8-max-2026-05-17`）与无后缀最新版（如 `qwen3.8-max`）视为两个独立模型，各自拥有独立免费额度，额度不互通 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **欠费影响范围**：账户欠费按商品 Code 隔离。例如 `百炼容量预留` 欠费仅导致 PTU 服务不可用，不影响 `百炼大模型推理` 的正常使用 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **生产环境禁用建议**：`免费额度用完即停` 和 `预算达限即停` 功能在生产环境可能导致服务中断，官方明确提示“不建议开启” [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [预算管理](../../raw/model-user-guide/test-1/budget-management.md)


