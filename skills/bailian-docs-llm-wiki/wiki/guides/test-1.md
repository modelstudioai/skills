# test 1

`test 1` 是阿里云百炼平台面向开发者提供的模型服务计费与成本管理核心主题，涵盖新人免费额度、按量调用、模型训练/部署、吞吐预留、节省计划及账单监控等全链路成本控制能力。其设计目标是为不同规模和场景的用户提供灵活、透明、可预测的费用模型，支持从快速验证到规模化生产的平滑演进。

## 支持的模型/功能

- **实时推理**：支持千问（Qwen）系列（如 `qwen3.8-max`、`qwen4-max`）、DeepSeek、GLM、Kimi 等主流大模型及多模态模型（VL、ASR、TTS、图像生成、视频生成）的按 [Token](../concepts/token.md) 实时调用 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **批量推理（Batch）**：支持 `batch` 和 `batch-chat` 接口，单价为实时推理价格的 50% [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。
- **模型调优（Fine-tuning）**：支持文本生成、图像生成（万相/千问）、语音合成（CosyVoice）、视频生成等模型的微调，按训练 [Token](../concepts/token.md) 计费 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **模型部署（PTU/DTU）**：提供预置吞吐（PTU）和独占吞吐（DTU）两种部署模式，支持长输入阶梯系数与缓存折扣 [原文标题](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)。
- **吞吐预留（TPM Reservation）**：支持标准模式（等同于 API TPS）与高速模式（1.5–2 倍 TPS），按预付费（天/8 小时）或后付费（小时）计费 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。

> **注意**：文档 1 明确指出免费额度**仅抵扣模型实时推理**产生的费用，而文档 3 和文档 4 中的模型训练、模型部署、吞吐预留均**不支持使用免费额度抵扣**。该限制在所有相关文档中一致，无矛盾。

## 关键参数

- **[Token](../concepts/token.md) 计费粒度**：输入/输出 Token 均以“每百万 Token”为单位计价；训练费用以“每千 Token”为单位；吞吐预留以“kTPM”（千 Tokens/分钟）为单位购买。
- **地域差异**：华北2（北京）是唯一提供新人免费额度的地域；其他地域（如美国、新加坡、德国、日本、中国香港）模型单价普遍上浮，且无免费额度 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **阶梯计费**：部分模型（如 `qwen3.7-plus`）对输入 Token 分档定价（如 0–256K、256K–1M），单次请求所有 Token 按最高档单价结算。
- **缓存折扣**：上下文缓存（显式/隐式）命中时，输入 Token 单价大幅降低（如 `qwen4-max` 缓存命中单价为 0.5 元/百万 Token），但创建缓存本身按更高单价计费 [原文标题](../../raw/model-user-guide/model-experience/text-generation-model/context-cache.md)。
- **容量换算系数**：吞吐预留中，长输入按阶梯系数（如 `qwen3.7-flash` 输入 >32K 部分系数为 3x）、缓存命中部分按折算系数（如 `glm-5.2` 为 0.25）进行 kTPM 消耗折算 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。

## 使用方式

- **开通即用**：完成实名认证后，系统自动发放华北2（北京）地域各模型的新人免费额度（通常 100 万 Token），无需手动领取 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **API 调用**：使用通用 API Key 与 Base URL，通过标准 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)发起请求；调用自动优先消耗免费额度，再按量计费。
- **成本优化**：
  - 长期稳定使用：首选 **AI 通用型节省计划**，承诺月消费享最高 5.3 折，覆盖绝大多数模型 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
  - 用量小或集中单一模型：可选**其他模型节省计划**（如千问语音模型、向量模型专项计划）或**资源包**。
  - 高并发低延迟场景：购买**吞吐预留**（TPM Reservation）保障确定性性能。
- **预算管控**：在[预算管理](https://bailian.console.aliyun.com/cn-beijing/costing-balance/budget)页面为账号、业务空间或 API Key 设置月度预算，并可开启“达到预算后立即停止”以自动熔断 [原文标题](../../raw/model-user-guide/test-1/budget-management.md)。

## 限制和注意事项

- **免费额度限制**：仅限华北2（北京）地域；有效期 90 天（自开通/模型发布/申请通过日起算，以较晚者为准）；不同模型（含快照版本）额度独立，不互通；ASR 类模型需在业务空间内单独开通权限方可消耗额度 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **免费额度用完即停**：该功能默认关闭，开启后额度耗尽将返回 HTTP 403 错误（错误码 `AllocationQuota.FreeTierOnly`）。**生产环境不建议开启**，以免导致服务不可用 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **模型下架与额度失效**：平台已下架部分模型（如 `qwen3.8-max-0902`、`deepseek-v4-pro`）的免费额度，新用户不再获得，老用户额度仍可使用至到期或耗尽 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **账单延迟**：模型推理账单为分钟级出账（通常 2–10 分钟），非实时；批量推理、训练、部署为小时级出账。查询 2026 年 4 月 1 日前费用需前往阿里云费用中心逐月导出 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **欠费隔离**：欠费按商品 Code 隔离，例如“百炼容量预留”欠费不影响“百炼大模型推理”服务，但已欠费的商品 Code 无法使用任何额度（免费额度、节省计划、资源包） [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [预算管理](../../raw/model-user-guide/test-1/budget-management.md)


