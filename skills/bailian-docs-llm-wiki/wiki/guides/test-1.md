# test 1

本文档汇总百炼平台关于 `test 1` 相关计费与成本管理的核心规则，面向开发者提供结构化、可操作的参考。内容覆盖模型训练/部署、吞吐预留、节省计划、免费额度、预算及账单等关键环节，所有价格与策略均以最新公开文档为准，不包含营销性描述。

## 支持的模型/功能

百炼平台支持多模态模型的训练与推理计费，涵盖文本生成（千问系列）、多模态理解与生成（千问VL、万相）、视频生成（万相-i2v/t2v）及语音合成（CosyVoice）等。其中：

- **文本生成模型**（如 `qwen3.8-max`、`qwen3.7-plus-2026-05-26`）支持标准推理、Batch调用、上下文缓存及思考模式（思维链+回答），并按输入/输出 Token 分别计费 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **图像与视频生成模型**（如 `wan2.7-i2v`、`qwen-image-2.0-pro`）采用基于像素、时长或步数的 Token 消耗模型，计费逻辑与文本模型差异显著，需特别注意 `max_pixels`、`n_epochs`、`generation_type` 等参数对费用的影响 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **语音合成模型**（如 `cosyvoice-v3-plus`）仅支持华北2（北京）地域，训练费用按 `(lm_max_epoch + fm_max_epoch) × 25 × 总时长（秒）` 估算 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。

> **注意**：部分模型（如 `kimi-k3.1-pro`）在入门型 AI 通用节省计划中明确被排除在抵扣范围之外，而其在标准 AI 通用型节省计划中属于 C 类模型，仅支持 1:1 抵扣、无折扣 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

## 关键参数

计费准确性高度依赖以下核心参数的配置：

- **训练类参数**：
  - `max_steps`（万相图生图）、`n_epochs`（千问图生图/视频）、`max_pixels`（图像/视频）、`max_token_length`（万相文生图）直接影响训练 Token 总量计算。
  - `lm_max_epoch` 与 `fm_max_epoch` 是 CosyVoice 训练的关键超参，直接线性影响 Token 消耗。
- **推理类参数**：
  - `input_token` 与 `output_token` 是所有按量计费模型的基础计量单位；`context_0-128k_input_token` 等规格字段在账单明细中用于精确归因。
  - `batch_size` 在训练中**不参与计费**，但影响 `steps` 与 `n_epochs` 的换算关系。
- **吞吐预留类参数**：
  - `输入 kTPM`（千 Tokens/分钟）与 `输出 kTPM` 是容量购买的基本单位，需注意输入单价按“万TPM·天”报价，公式中需除以 10 换算 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
  - `缓存折算系数` 与 `长输入阶梯系数` 决定实际容量消耗，例如 `qwen3.7-flash-2026-07-15` 对 50K 输入的消耗为 86 kTPM（含阶梯折算）。

## 使用方式

开发者可通过以下方式控制成本：

- **自动抵扣**：AI 通用型节省计划、资源包、Token Plan 均使用**百炼通用 API Key** 与 Base URL 接入，费用在结算时自动抵扣，无需修改调用代码 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **免费额度启用**：首次开通百炼后，华北2（北京）地域的指定模型（如 `qwen3.8-max`）自动获得 100 万 Token 免费额度，调用即自动扣除，无需额外配置 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **预算强制管控**：在控制台设置账号/业务空间/API Key 级别的月度预算，并开启“达到预算后立即停止”，可使费用达阈值时返回 HTTP 429 错误，实现硬性熔断 [原文标题](../../raw/model-user-guide/test-1/budget-management.md)。
- **异步任务监控**：生图、生视频等异步任务的费用结算存在延迟，需通过[账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)页面按 `实例ID（出账粒度）` 字段（格式为 `业务空间ID!地域!训练任务标识`）溯源，而非依赖实时用量 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 限制和注意事项

- **地域限制**：CosyVoice 模型调优仅支持华北2（北京）；新人免费额度**仅限华北2（北京）地域**，其他地域无此权益 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **免费额度限制**：额度仅抵扣**实时推理**费用，明确不支持 Batch 调用、模型训练、模型部署、PAI-DSW、OSS 存储等 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **账单延迟**：大模型推理账单为分钟级出账（通常 2–10 分钟），批量推理、训练、知识库为小时级出账；账单生成不等于实时扣款，阿里云采用“预占+月结”模式 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **欠费隔离**：欠费按商品 Code 隔离，例如 `百炼容量预留` 欠费仅导致 PTU 部署服务不可用，不影响 `百炼大模型推理` 的调用 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **模型下架**：大量模型（如 `wan2.7-i2v`、`qwen3.5-omni-flash` 等）的免费额度已被平台下架，新用户不再发放，老用户已发放额度仍可使用至到期 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 来源文档

- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [预算管理](../../raw/model-user-guide/test-1/budget-management.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)


