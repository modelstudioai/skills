# test 1

`test 1` 是阿里云百炼平台面向开发者提供的模型服务计费与资源管理核心主题，涵盖模型调用、训练、部署及成本控制的全链路规则。本文整合官方文档，明确免费额度适用范围、各类计费模式（按量、预留、节省计划等）的关键参数与使用约束，并指出常见矛盾点与实操注意事项，帮助开发者快速建立准确的成本认知和调用策略。

## 支持的模型/功能

- **实时推理**：所有在华北2（北京）地域上架的文本生成、多模态（VL）、语音（ASR/TTS）、图像/视频生成模型均支持基础调用，其中 `qwen3.8-max`、`qwen3.7-plus` 等主流千问系列模型提供阶梯计费、Batch半价、上下文缓存等高级功能 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **模型训练**：支持文本生成（千问系列）、图像生成（万相、千问图像）、视频生成（万相i2v）、语音合成（CosyVoice）四类调优任务，计费基于训练Token总量，公式因模型类型而异（如万相i2v按计费时长×像素系数计算）[原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **模型部署**：支持PTU（预置吞吐）部署，按输入/输出TPM容量预付费或后付费，不同模型（如 `qwen3.8-max` 与 `deepseek-v4-pro`）的单价、最长输入Token及性能模式（标准/高速）存在显著差异 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **吞吐预留（TPM Reservation）**：提供标准模式（等同API TPS）与高速模式（1.5~2倍TPS），支持按天、按8小时时段购买，容量换算需考虑长输入阶梯系数与缓存折算系数 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。

## 关键参数

| 类别 | 参数 | 说明 | 示例值 |
|--------|------|------|--------|
| **免费额度** | 总量/有效期 | 每模型独立100万Token，有效期90天（以开通/模型发布/申请通过三者最晚时间起算） | `qwen3.8-max`: 1,000,000 Token, 90天 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md) |
| **调用计费** | 输入/输出单价 | 按百万Token计价，受地域、阶梯区间（如0–128K）、模式（思考/非思考）影响 | 华北2 `qwen3.8-max`: 输入¥12/百万Token，输出¥36/百万Token [原文标题](../../raw/model-user-guide/test-1/model-pricing.md) |
| **训练计费** | 训练Token总量 | 公式复杂，依赖超参（`max_steps`, `n_epochs`, `max_pixels`）与模型特性（如万相i2v按`min(10, 四舍五入时长)`计费） | `wan2.7-i2v`训练10秒视频：`10 × (36864/1024) × 800 = 288,000` Token [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md) |
| **部署/预留** | TPM容量单位 | 输入按万TPM、输出按千TPM报价；实际购买量单位为kTPM（1kTPM=1000 Tokens/分钟） | 购买200输入kTPM → 公式中按`200 ÷ 10 = 20`万TPM计算 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md) |

> **注意**：文档2与文档4对 `qwen3.7-plus` 的输入单价存在矛盾。文档2称其训练单价为¥0.35/千Token（即¥350/百万Token），而文档4显示其推理输入单价为¥2/百万Token（限时8折）。二者分属训练与推理场景，不可直接比较，但需明确：**训练费用远高于推理费用**，且训练不享受免费额度抵扣 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。

## 使用方式

- **启用免费额度**：首次开通百炼（仅华北2地域）后自动发放，无需认证即可使用；调用时系统自动优先抵扣，无需修改API Key或请求头 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **调用模型**：使用通用API Key（非Token Plan专属Key），通过标准OpenAI兼容接口发起请求；若需Batch半价，须在请求中指定支持Batch的模型Code（如 `qwen3.8-max`）[原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **购买节省计划**：在[AI通用型节省计划购买页](https://common-buy.aliyun.com/?commodityCode=sfm_GenAI_spn_cn)选择地域（如华北2）、承诺周期（3/6/12/24个月）与月消费额，折扣力度随承诺金额递增，最高5.3折 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **设置预算**：在控制台**费用用量 > 预算管理**页面，按账号/业务空间/API Key粒度配置月度预算金额，并可选开启「达到预算后立即停止」以自动限流 [原文标题](../../raw/model-user-guide/test-1/budget-management.md)。

## 限制和注意事项

- **免费额度限制**：仅抵扣**实时推理**费用；Batch调用、模型训练、模型部署、PAI-DSW、OSS存储等均**不支持抵扣** [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。未认证用户额度用尽后服务完全中断，已认证用户则自动转按量付费（除非开启“用完即停”）。
- **地域隔离**：免费额度、节省计划、吞吐预留均**严格按地域隔离**。华北2购买的节省计划无法抵扣新加坡地域调用费用；同一模型在不同地域（如北京vs新加坡）价格不同，且免费额度仅北京有效 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **计费延迟风险**：模型推理账单通常2–10分钟出账，但监控数据、控制台额度显示均为分钟级更新。若未及时刷新页面，可能因显示“有余额”而误判，导致意外扣费 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **部署即计费**：模型完成部署进入“运行中”状态即开始计费，**与是否发生API调用无关**。长期不用应主动下线，否则持续产生费用 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **抵扣顺序刚性**：系统按固定优先级抵扣：`免费额度 > 资源包 > 其他模型节省计划 > AI通用型节省计划 > 按量付费`。若开启“免费额度用完即停”，服务将停止，后续节省计划**无法生效**，必须手动关闭该开关才能恢复抵扣 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [预算管理](../../raw/model-user-guide/test-1/budget-management.md)


