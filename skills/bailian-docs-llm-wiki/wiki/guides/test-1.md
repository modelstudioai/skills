# test 1

`test 1` 是阿里云百炼平台面向开发者提供的模型服务计费与资源管理主题的统称，涵盖模型调用、训练、部署、吞吐预留及成本控制等核心场景。本文档整合官方技术文档，明确各能力的支持范围、关键参数、使用方式及约束条件，帮助开发者快速建立成本意识并规避常见误用风险。所有计费逻辑均以华北2（北京）地域为默认基准，跨地域调用需单独确认价格与额度适用性 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 支持的模型/功能

- **实时推理**：支持全部上架文本生成、多模态（VL）、语音（ASR/TTS）、图像/视频生成模型，是唯一可使用新人免费额度的场景 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **模型训练**：支持千问系列（Qwen3/Qwen2.5）、万相（WanX）、CosyVoice 等模型的微调，按训练 [Token](../concepts/token.md) 总量计费，不支持免费额度抵扣 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **模型部署**：支持 PTU（预置吞吐）、DTU（模型单元）等多种部署形态，按使用时长或吞吐量计费，亦不支持免费额度抵扣 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **批量调用（Batch）**：兼容 OpenAI 接口的 Batch 调用方式，其输入/输出 [Token](../concepts/token.md) 单价为实时推理价格的 50%，但**不参与免费额度抵扣** [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **上下文缓存**：部分模型（如 `qwen3.8-max`）支持显式/隐式缓存，缓存创建与命中的 [Token](../concepts/token.md) 按独立单价计费（非标准输入单价），该能力在价格表中单独说明 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。

> **注意**：文档 3 与文档 1 对 `Batch调用` 的免费额度支持存在矛盾。文档 1 明确指出“[Batch调用](raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)产生的费用不支持用免费额度抵扣”，而文档 3 在千问Max章节中仅说明其“Batch调用半价”，未提及其是否可享免费额度。依据文档 1 的权威性及明确禁止条款，应以“Batch调用不可用免费额度”为准。

## 关键参数

- **Token 计费粒度**：所有按量计费模型（推理、训练、部署）均以 Token 为最小计费单位，1 Token ≈ 1 英文单词或 1.3 个中文字符；输入/输出 Token 分开统计。
- **TPM/TPU 容量单位**：
  - `kTPM` = 1,000 Tokens/分钟（购买量单位）；
  - `万TPM` = 10,000 Tokens/分钟（输入单价报价单位，计算时需 `kTPM ÷ 10`）；
  - `千TPM` = 1,000 Tokens/分钟（输出单价报价单位，即 `kTPM`）。
- **阶梯计费区间**：部分模型（如 `qwen3-max`）按单次请求输入 Token 总量分档定价，例如 `0<Token≤32K`、`32K<Token≤128K`，**该次请求所有 Token 均按最高档单价结算** [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **免费额度有效期**：自开通百炼、模型发布或申请通过之日起 90 天（以较晚者为准）。2025年9月8日11点前开通的用户，有效期可能不足90天 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 使用方式

- **调用入口**：统一通过百炼 API（Base URL 如 `https://dashscope.aliyuncs.com/compatible-mode/v1`）发起，`model` 参数指定模型 Code（如 `qwen3.8-max`）。
- **免费额度使用**：无需额外配置，系统自动优先抵扣；必须使用通用 API Key（非 Token Plan/Coding Plan 专属 Key），且仅限华北2（北京）地域 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **节省计划抵扣**：购买 AI 通用型节省计划后，系统按 `免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费` 顺序自动抵扣，**若开启「免费额度用完即停」，额度耗尽后服务停止，节省计划无法生效** [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **预算控制**：在[预算管理](https://bailian.console.aliyun.com/cn-beijing/costing-balance/budget)页面可为账号、业务空间或 API Key 设置月度预算，并选择「达到预算后立即停止」以自动限制按量调用（生产环境慎用） [原文标题](../../raw/model-user-guide/test-1/budget-management.md)。

## 限制和注意事项

- **地域限制**：新人免费额度**仅限华北2（北京）地域**，其他地域（如新加坡、美国）无此福利；节省计划也按地域独立购买，不可跨地域抵扣 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **额度不互通**：不同模型（含快照版本，如 `qwen3.8-max` 与 `qwen3.8-max-2026-05-17`）的免费额度相互独立，不能合并或转移 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **欠费影响**：账户可用额度 < 0（欠费）时，**即使模型仍有免费额度或节省计划剩余额度，所有模型调用均将失败**。必须结清欠费才能恢复服务 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **出账延迟**：模型推理账单通常在调用结束 2–10 分钟后生成，非实时扣款；批量推理、训练等为小时级出账。监控数据（如用量统计）为分钟级更新，**不作为计费依据** [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **停止计费操作**：删除 API Key 可彻底终止 API 调用计费；下线已部署模型可停止 PTU/DTU 时长计费；退订预付费实例需在费用中心操作，已使用部分按惩罚系数结算 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [预算管理](../../raw/model-user-guide/test-1/budget-management.md)


