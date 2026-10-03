# test 1

`test 1` 是阿里云百炼平台面向开发者提供的模型服务计费与资源管理主题的统称，涵盖模型调用、训练、部署、吞吐预留、成本优化及预算控制等核心计费场景。本文档聚焦于开发者实际使用中高频接触的模型推理（实时调用）相关能力、参数、接入方式及关键约束，不包含模型开发、评估等非生产环境操作。所有计费逻辑均以华北2（北京）地域为默认基准，跨地域调用需注意价格与额度隔离规则。

## 支持的模型/功能

- **支持模型**：覆盖千问系列（如 `qwen3.8-max`、`qwen3.7-plus`）、DeepSeek、GLM、Kimi 等主流大语言模型，以及万相（图像/视频）、CosyVoice（语音）等多模态模型。具体支持列表以[模型广场](https://bailian.console.aliyun.com/model/market)为准。
- **核心功能**：
  - 实时推理（标准 API 调用）
  - Batch 批量调用（兼容 OpenAI 接口）[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
  - 上下文缓存（显式/隐式）[原文标题](../../raw/model-user-guide/model-experience/text-generation-model/context-cache.md)
  - 模型调优（Fine-tuning）与模型部署（PTU/DTU）[原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)

> **注意**：免费额度**仅抵扣实时推理**产生的费用，明确不支持抵扣 Batch 调用、模型调优、模型部署、PAI-DSW、OSS 存储等费用 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 关键参数

- **Token 计费粒度**：输入 Token 与输出 Token 分开计费，单价按模型、地域、输入长度区间（阶梯计费）浮动。例如 `qwen3.8-max`（北京）输入单价为 ¥12/百万 Token（0–1M 区间），输出为 ¥36/百万 Token [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **TPM（Tokens Per Minute）容量单位**：吞吐预留（PTU）以 kTPM（千 Tokens/分钟）为购买单位，输入起步 200 kTPM，输出起步 20 kTPM [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **免费额度有效期**：自开通百炼、模型发布或申请通过之日起 90 天（以较晚者为准），到期自动失效且不可延期或补发 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 使用方式

1. **开通与认证**：首次开通阿里云百炼即自动发放新人免费额度（无需实名认证），但额度用完后若需按量付费，必须完成[实名认证](https://myaccount.console.aliyun.com/cert-info)并充值。
2. **调用入口**：
   - API 调用：使用通用 API Key（非 Token Plan 专属 Key），指定 `model` 参数（如 `"qwen3.8-max"`）和 Base URL（如 `https://dashscope.aliyuncs.com/compatible-mode/v1`）。
   - 控制台体验：通过[体验中心](https://bailian.console.aliyun.com/model/experience/text)直接测试。
3. **成本优化路径**：
   - 小规模试用 → 依赖免费额度；
   - 长期稳定调用 → 优先选用[AI 通用型节省计划](https://help.aliyun.com/zh/model-studio/savings-plan-and-resource-package#ghoteqo7uv9wa)，承诺月消费换取最高 5.3 折；
   - 高并发低延迟场景 → 购买吞吐预留（PTU）保障确定性性能 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。

## 限制和注意事项

- **地域隔离**：免费额度、节省计划、吞吐预留均严格按地域隔离。华北2（北京）购买的节省计划**无法抵扣**美国（弗吉尼亚）或新加坡地域的调用费用 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **额度共享规则**：主账号与其 RAM 子账号**共享同一免费额度**；不同模型（含快照版本如 `qwen3.8-max` 与 `qwen3.8-max-2026-05-17`）额度相互独立，不互通 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **预算管理范围**：仅管控 API 按调用量付费费用，**不包含**模型训练、PTU 预留、DTU 部署等费用 [原文标题](../../raw/model-user-guide/test-1/budget-management.md)。
- **生产环境警示**：开启「免费额度用完即停」或「达到预算后立即停止」将导致服务中断，生产环境**不建议启用**，应结合高额消费预警与余额监控主动管理 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [预算管理](../../raw/model-user-guide/test-1/budget-management.md)


