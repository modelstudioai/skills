# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与成本管理主题，涵盖模型训练、部署、调用及资源预留等全链路费用规则。本文整合了模型支持范围、关键参数配置、标准化使用方式，并明确各项限制与实操注意事项，帮助开发者快速建立成本意识并规避常见误用风险。所有价格与策略均以最新控制台为准，实际费用请以账单明细为最终依据。

## 支持的模型/功能

`test 1` 主要覆盖百炼平台主流模型的计费能力，包括文本生成（千问系列、DeepSeek、GLM）、多模态（千问VL、万相）、图像/视频生成（wan2.7-i2v、qwen-image-2.0）及语音合成（CosyVoice）等。其中，文本生成模型是计费体系最完备的类别，支持按 Token 调用、吞吐预留（PTU/TPM）、节省计划等多种模式；而图像与视频生成模型则采用基于 `max_pixels`、`max_steps` 或 `计费时长` 的专用 Token 计算公式 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。语音合成模型（CosyVoice）当前仅限华北2（北京）地域使用，其训练消耗按 `(lm_max_epoch + fm_max_epoch) × 25 × 总时长(秒)` 估算 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。

> **注意**：文档 1 中列出的 `Qwen3.7-Plus-2026-05-26` 等带日期后缀的模型快照，在文档 2 的调用价格表中被标注为“当前能力等同于 `qwen3.7-plus-2026-05-20`”，表明部分快照版本已实质合并或降级为通用别名，开发者应以控制台实际可用 Model ID 为准，避免依赖过时快照代码。

## 关键参数

计费逻辑高度依赖以下核心参数：
- **Token 相关**：输入/输出 Token 数、`max_token_length`（影响 Lmax）、`max_pixels`（图像/视频训练）、`n_epochs` / `max_steps`（训练轮次/步数）；
- **吞吐相关**：输入 kTPM、输出 kTPM、性能模式（标准/高速）、缓存折算系数、长输入阶梯系数；
- **时间相关**：训练 `n_epochs`、视频 `计费时长`（四舍五入后取 min(10, x)）、预留购买时长（天/小时）；
- **地域与部署**：模型服务地域（如华北2（北京）、新加坡）、部署类型（PTU/DTU/按量）。

例如，万相图生视频（`wan2.7-i2v`）的训练 Token 总量 = `∑视频计费时长 × (max_pixels / 1024) × n_epochs`，其中单条视频计费时长上限为 10 秒 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)；而吞吐预留中 `qwen3.7-flash-2026-07-15` 的长输入阶梯系数为 `(0,32K] 1x, (32K,256K] 3x, (256K,1M] 6x`，直接影响容量扣减 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。

## 使用方式

开发者需按场景选择计费模式：
- **模型调用**：默认按量计费，通过 API Key 发起请求，系统自动按 `免费额度 > 资源包 > 节省计划 > 按量付费` 顺序抵扣 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)；
- **模型训练**：在控制台创建微调任务，配置 `n_epochs`、`max_pixels` 等超参，费用按预估公式实时显示，最终以 `usage` 字段为准 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)；
- **模型部署**：选择 PTU（预置吞吐）或 DTU（算力单元），PTU 需指定输入/输出 kTPM 及性能模式，支持扩容/缩容；DTU 则按实例规格计费；
- **成本管控**：启用预算管理（按账号/业务空间/API Key 设置月度限额与告警）、开启「免费额度用完即停」防止意外扣费、配置高额消费预警 [原文标题](../../raw/model-user-guide/test-1/budget-management.md)。

所有操作均需通过百炼控制台或 OpenAI 兼容 API 完成，API 调用需指定正确 `model` 参数（如 `qwen3.8-max`）及对应 Base URL 地域。

## 限制和注意事项

- **地域限制**：新人免费额度、CosyVoice 训练、部分模型部署仅支持华北2（北京）；其他地域（如新加坡、美国弗吉尼亚）需单独购买对应地域的节省计划或预留资源 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)；
- **额度隔离**：免费额度、资源包、节省计划均按模型 Code 独立计算，`qwen3.8-max` 与 `qwen3.8-max-0902` 视为不同模型，额度不互通；
- **出账延迟**：模型推理账单通常延迟 2–10 分钟出账，批量推理、训练、知识库为小时级出账，不可作为实时计费依据 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)；
- **欠费影响**：账户欠费时，即使存在免费额度或节省计划，所有按量付费服务（含模型调用、部署）将暂停，必须结清欠费后恢复；
- **停止计费**：删除 API Key 可立即终止 API 调用计费；下线模型部署可终止 PTU/DTU 计费；退订预付费实例需在费用中心操作，已使用部分按 1.2 倍系数结算（≤30 天）或 1.0 倍（>30 天）。

> **注意**：文档 5 中吞吐预留的「8 小时时段预留」明确要求下单时段为每日 22:00–次日 00:00，且当日 00:00–22:00 不可下单；而文档 1 中模型部署的预付费订单“若在 22:00 后下单，到期日将自动顺延1天”——二者虽同涉 22:00 时间点，但适用场景（时段预留 vs 普通 PTU）与规则逻辑（顺延 vs 限时下单）完全不同，开发者须严格区分。

## 来源文档

- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [预算管理](../../raw/model-user-guide/test-1/budget-management.md)


