# test 1

`test 1` 是阿里云百炼平台面向开发者提供的模型服务计费与资源管理核心主题，涵盖新人免费额度、按量调用、吞吐预留、模型训练/部署、节省计划及成本管控等全链路能力。本文档结构化梳理关键事实，聚焦可执行信息，避免营销表述，所有引用均指向原始技术文档以确保权威性。

## 支持的模型/功能

- **实时推理**：支持千问（Qwen3.8-Max、Qwen3.7-Plus 等）、DeepSeek、GLM、Kimi 等主流文本生成模型，以及万相（Wan2.7）、CosyVoice 等多模态与语音模型。具体支持列表详见[模型调用价格](raw/model-user-guide/test-1/model-pricing.md)中的地域与模型表格。
- **批量调用**：部分模型（如 `qwen3.8-max`）支持 Batch 接口，其输入/输出 [Token](../concepts/token.md) 单价为实时推理价格的 50% [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **上下文缓存**：支持显式/隐式缓存，命中时输入 [Token](../concepts/token.md) 按折扣单价计费（如 `qwen3.8-max` 输入缓存命中单价为标准输入价的 10%），但缓存创建本身按标准输入价的 125% 计费 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **[异步任务](../concepts/asynchronous-task.md)**：生图、生视频等采用异步机制，费用在任务完成并结算后产生，存在时间差 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

> **注意**：文档 1 明确指出免费额度**仅抵扣实时推理费用**，而文档 4 和文档 6 均强调模型训练、模型部署、Batch 调用、联网搜索插件等产生的费用**不支持用免费额度抵扣**。三者定义一致，无矛盾。

## 关键参数

- **[Token](../concepts/token.md) 计费粒度**：输入/输出 Token 均按实际消耗计费，精度为 1 Token；训练费用最小计费单位为 1 Token，部署/吞吐预留按 TPM（Tokens per Minute）计费。
- **阶梯计费**：部分模型（如 `qwen3.7-plus`）对输入 Token 分档定价，单次请求的所有 Token 均按最高档位单价结算 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **TPM 容量换算**：吞吐预留中，长输入和缓存命中需按模型特定系数折算（如 `qwen3.8-max` 缓存折算系数为 0.125），实际消耗 kTPM = 原始 Token × 阶梯系数 × 缓存系数 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **免费额度有效期**：自开通百炼/模型发布/申请通过之日起 90 天（以较晚者为准），但文档 1 特别注明：**2025年9月8日11点前已开通的用户，有效期可能不足90天** [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 使用方式

- **免费额度**：首次开通华北2（北京）地域百炼并完成实名认证后自动发放，无需手动领取。调用时自动抵扣，查看剩余额度请访问[免费额度页面](https://bailian.console.aliyun.com/cn-beijing/costing-balance/free-quota) [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **按量付费**：使用通用 API Key 与对应地域 Base URL 调用即可，费用实时计入账单。推荐搭配 AI 通用型节省计划使用，承诺月消费可享最高 5.3 折 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **吞吐预留（PTU）**：购买后生成专属模型 Code（需替换 API 的 `model` 参数），调用该 Code 的流量优先使用预留容量，超出部分按溢出策略处理（自动溢出或返回 429） [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **预算控制**：可在[预算管理](https://bailian.console.aliyun.com/cn-beijing/costing-balance/budget)中为账号、业务空间或 API Key 设置月度预算，并开启「达到预算后立即停止」以自动限制调用（生产环境慎用） [原文标题](../../raw/model-user-guide/test-1/budget-management.md)。

## 限制和注意事项

- **地域限制**：新人免费额度**仅华北2（北京）地域有效**，其他地域（如美国、新加坡）无免费额度 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **额度独立性**：不同模型（含快照版本，如 `qwen-max` 与 `qwen-max-2025-01-25`）的免费额度相互独立，不互通、不共享 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **免费额度用完即停**：开启此功能后，额度耗尽将返回 HTTP 403 错误（错误码 `AllocationQuota.FreeTierOnly`），但文档 1 明确警告：“**生产环境不建议开启此功能，以免额度耗尽导致服务不可用**” [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **欠费隔离**：账户欠费按商品 Code 隔离，例如“百炼容量预留”欠费不影响“百炼模型调用”，但已欠费的商品 Code 无法再使用节省计划或资源包额度 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **模型下架**：大量模型（如 `wan2.7-t2v`, `qwen3-asr-flash` 等共 200+ 个）的免费额度已被平台下架，新用户不再获得，老用户额度仍可使用至到期 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [预算管理](../../raw/model-user-guide/test-1/budget-management.md)


