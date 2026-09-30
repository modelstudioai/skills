# test 1

`test 1` 是阿里云百炼平台面向开发者提供的模型服务计费与资源管理核心主题，涵盖免费额度发放规则、按量调用、吞吐预留、模型训练/部署、成本管控等全链路计费场景。本文整合官方文档，明确各能力的适用范围、关键参数及使用约束，帮助开发者快速建立成本认知并规避常见误用风险。

## 支持的模型/功能

`test 1` 覆盖百炼平台主流模型服务，包括文本生成（千问系列）、多模态（千问VL、万相）、语音（CosyVoice）、视频生成等。所有模型均支持标准实时推理调用，并可叠加 Batch 接口、上下文缓存、Function Calling 等高级功能。但需注意：**免费额度仅抵扣实时推理费用**，不覆盖 [Batch调用](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)、[模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)、[模型部署](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md) 及 PAI-DSW、OSS 等关联服务 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。

> **注意**：文档 2 中列出的 `qwen3.8-max-prime` 明确标注“无免费额度”，而文档 1 强调“每个模型（含快照版本）额度独立”。但文档 2 表格中同一模型 `qwen3.8-max` 在华北2（北京）有 100 万 Token 免费额度，而 `qwen3.8-max-prime` 却无——这并非矛盾，而是因 `prime` 模式属于独立模型 Code，其额度需单独开通且当前未纳入新人赠送范围。开发者须以控制台实际显示为准，不可假设同名主模型有额度即代表其变体也有。

## 关键参数

- **Token 计费粒度**：输入/输出 Token 分开计费，单价按模型、地域、阶梯区间（如 0–32K、32K–128K）浮动，详见 [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md) 文档。
- **TPM 预留单位**：吞吐预留以 kTPM（千 Tokens/分钟）为购买单位，输入起步 200 kTPM，输出起步 20 kTPM；计费时需换算为万TPM（输入）和千TPM（输出） [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **训练 Token 计算**：模型训练费用基于 `训练数据 Token 总数 × 循环次数 × 单价`，其中图像/视频训练还涉及 `max_pixels`、`n_epochs`、GPU 系数等动态因子 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **预算维度**：支持账号、业务空间、API Key 三级独立设置，但**仅统计 API 按调用量付费费用**，不包含模型训练、PTU、DTU 等 [原文标题](../../raw/model-user-guide/test-1/budget-management.md)。

## 使用方式

1. **免费额度启用**：首次开通百炼后自动发放，无需认证即可使用。调用时系统自动优先抵扣，无需修改 API Key 或请求头 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
2. **按量调用**：直接使用通用 API Key 调用，费用从账户余额扣除；若开启「免费额度用完即停」，额度耗尽将返回 `403 AllocationQuota.FreeTierOnly` 错误。
3. **吞吐预留**：在控制台购买后获得专属 `model` Code（如 `qwen3.8-max-ptu-xxxx`），调用时需显式替换 `model` 参数，否则不生效。
4. **节省计划**：购买后自动按 `免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费` 顺序抵扣，无需代码变更。
5. **预算管理**：在控制台设置月度预算并开启「达到预算后立即停止」，超限调用将返回 HTTP 429 错误。

## 限制和注意事项

- **地域限制**：新人免费额度**仅华北2（北京）地域有效**，其他地域（如美国、新加坡）模型无此福利 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **额度时效性**：免费额度有效期为 90 天（以开通/模型发布/申请通过三者最晚时间起算），过期自动作废，不延期、不补发。
- **OAuth 独立体系**：OAuth 认证享有每日 2000 次独立免费调用，其额度与控制台 API Key 免费额度完全隔离，控制台不显示 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **Token Plan 专属 Key 限制**：使用 Token Plan 团队版专属 API Key 调用时，**不消耗免费额度**，且图像/视频生成模型会报 400 错误，必须改用通用 API Key 或通过 Skill 接入 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **账单延迟**：模型推理账单通常在调用结束 2–10 分钟后生成，非实时出账；批量推理、训练等为小时级出账，高峰期可能进一步延迟 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **生产环境警告**：「免费额度用完即停」和「预算达限即停」功能在生产环境**不建议开启**，因服务中断不可控，且存在生效延迟导致超额扣费风险。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [预算管理](../../raw/model-user-guide/test-1/budget-management.md)


