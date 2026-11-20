# test 1

`test 1` 是阿里云百炼平台面向开发者提供的模型服务计费与成本管理核心主题，涵盖模型调用、吞吐预留、训练部署、节省计划及账单监控等全链路计费规则。本文档整合最新政策与技术细节，聚焦华北2（北京）地域的主流模型（如 `qwen3.8-max`、`qwen3.7-plus-2026-05-26`），明确免费额度适用范围、关键参数配置逻辑及生产环境避坑要点，为开发者提供可直接落地的成本控制方案。

## 支持的模型/功能

- **支持模型**：`qwen3.8-max`、`qwen3.7-plus-2026-05-26`、`qwen3.7-flash-2026-07-15`、`deepseek-v4-flash`、`glm-5.2` 等主流文本生成模型；万相（`wan2.7-i2v`）、千问VL（`qwen3-vl-8b-instruct`）、CosyVoice 等多模态与语音模型亦纳入计费体系 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **核心功能**：
  - 实时推理（含思考/非思考模式、上下文缓存、Batch 调用）
  - 吞吐预留（标准/高速模式、8 小时时段、按天/小时计费）
  - 模型训练（Token 级粒度，支持千问、万相、CosyVoice 等）
  - 模型部署（预置吞吐单元 PTU、模型单元 DTU）
  - 成本优化工具（AI 通用型节省计划、资源包、预算管理）

> **注意**：文档 1 明确指出 `qwen3.8-max-0902` 已下架免费额度，但文档 2 的价格表仍将其列为有价模型。实际使用中该模型**无免费额度**，需按量付费或通过节省计划抵扣，以 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md) 的下架列表为准。

## 关键参数

- **Token 计费粒度**：输入/输出 Token 分开计费，免费额度为输入+输出共用总额度（如 `qwen3.8-max` 为 100 万 Token）[原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **TPM 容量单位**：吞吐预留以 `kTPM`（1,000 Tokens/分钟）为单位，输入起步 200 kTPM，输出起步 20 kTPM [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **阶梯计费阈值**：部分模型（如 `qwen3.7-plus`）按输入 Token 分档（0–256K、256K–1M），单价随档位升高；长输入（>32K）按阶梯系数折算容量消耗 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **缓存折算系数**：显式/隐式缓存命中部分按特定系数（如 `qwen3.8-max` 为 0.125）折算输入 kTPM，显著降低容量消耗 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。

## 使用方式

- **免费额度激活**：完成阿里云实名认证后，主账号或拥有 `AliyunBailianFullAccess` 权限的 RAM 子账号登录百炼控制台，系统自动发放额度，无需手动领取 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **API 调用**：使用通用 API Key 与 Base URL，通过标准 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)发起请求；吞吐预留需替换 `model` 参数为专属模型 code [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **节省计划抵扣**：购买 AI 通用型节省计划后，费用在结算时自动抵扣，覆盖 A/B/C 类模型（C 类无折扣，1:1 抵扣），且**全地域通用** [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **预算管控**：在控制台「预算管理」页面设置账号/业务空间/API Key 级月度预算，开启「达到预算后立即停止」可自动限制按量调用（生产环境慎用）[原文标题](../../raw/model-user-guide/test-1/budget-management.md)。

## 限制和注意事项

- **地域限制**：新人免费额度**仅华北2（北京）地域有效**，其他地域（如美国、新加坡）模型调用无免费额度，且价格上浮 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **额度独立性**：不同模型（含快照版本，如 `qwen3.8-max` 与 `qwen3.8-max-0902`）的免费额度相互独立，不互通、不转移；额度耗尽后系统**不会自动切换至其他有额度的模型** [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **免费额度用完即停**：开启此功能后，额度耗尽将返回 HTTP 403 错误（错误码 `AllocationQuota.FreeTierOnly`），避免意外扣费；但**生产环境不建议开启**，以免服务中断 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **三方直供模型限制**：预算管理、节省计划（入门型）均**不支持三方直供模型**（如 `kimi-k3`、`deepseek-v4-pro` 的三方版本），仅阿里直供模型可参与成本优化 [原文标题](../../raw/model-user-guide/test-1/budget-management.md)。
- **异步任务欠费风险**：生图、生视频等异步任务费用结算存在延迟，充值补缴后仍可能因已提交任务产生新账单，导致再次欠费，需预留充足余额 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [预算管理](../../raw/model-user-guide/test-1/budget-management.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)


