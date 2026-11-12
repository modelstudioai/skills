# test 1

`test 1` 是阿里云百炼平台面向开发者提供的模型服务计费与资源管理主题的统称，涵盖新人免费额度、按量调用、模型训练/部署、吞吐预留、节省计划及成本管控等核心计费模块。其设计目标是为不同规模和场景的模型应用提供灵活、透明、可预测的成本控制能力，所有计费行为均以 [Token](../concepts/token.md)、TPM（[Token](../concepts/token.md)s Per Minute）或时长为计量基础，并严格区分地域、模型版本与调用方式。开发者需重点关注免费额度的有效期与地域限制、按量计费的阶梯规则、以及各类预付费资源（如 PTU、节省计划）的抵扣范围与生命周期。

## 支持的模型/功能

- **支持模型**：覆盖千问系列（`qwen3.8-max`、`qwen3.7-plus` 等）、DeepSeek、GLM、Kimi、万相（Wan）、CosyVoice、Qwen-VL、Qwen-ASR/TTS 等主流模型，但具体模型是否支持免费额度、Batch 调用、上下文缓存或吞吐预留，需以各模型在控制台的实际配置为准。例如，`qwen3.8-max` 支持 Batch 调用半价与上下文缓存折扣，而 `qwen-max` 在华北2（北京）仅支持非思考模式且无免费额度 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **核心功能**：
  - 实时推理（按 [Token](../concepts/token.md) 计费）
  - Batch 批量调用（单价为实时推理的 50%）[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
  - 上下文缓存（显式/隐式，输入 Token 享独立折扣）[原文标题](../../raw/model-user-guide/model-experience/text-generation-model/context-cache.md)
  - 模型训练（按训练 Token 总数 × 循环次数计费）
  - 模型部署（PTU/DTU 按时长或吞吐量计费）
  - 吞吐预留（标准/高速模式，按天或小时预付费）
  - 节省计划（AI 通用型、模型专属型、向量排序型）

> **注意**：文档 1 明确指出“免费额度仅抵扣模型**实时推理**（调用）产生的费用”，而文档 3 和文档 4 中的模型训练、模型部署、吞吐预留均**不支持**用免费额度抵扣 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。此为关键边界，不可混淆。

## 关键参数

- **Token 计量**：输入/输出 Token 均独立计费；免费额度为输入+输出共用总额度；Batch 调用、缓存命中、思考模式（思维链）均影响单价。
- **TPM（Tokens Per Minute）**：吞吐预留的核心单位，kTPM = 1,000 Tokens/分钟；输入按万TPM（10 kTPM）报价，输出按千TPM（1 kTPM）报价。
- **阶梯计费**：部分模型（如 `qwen3.7-plus`）按单次请求输入 Token 总量分档定价，所有 Token 均按最高档单价结算。
- **容量换算系数**：长输入与缓存命中会折算实际消耗的 kTPM。例如 `qwen3.7-flash-2026-07-15` 对 50K 输入无缓存时消耗 86 kTPM，有 30K 缓存命中时仅消耗 62 kTPM [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **地域因子**：同一模型在不同地域价格差异显著（如 `qwen3.8-max` 在华北2为 ¥12/百万输入 Token，在美国弗吉尼亚为 ¥14.988），且免费额度**仅限华北2（北京）** [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 使用方式

1. **开通与认证**：必须完成阿里云实名认证，首次开通百炼后系统自动发放免费额度（仅限华北2）[原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
2. **API 调用**：使用通用 API Key 与 Base URL，通过标准 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或百炼专属接口发起请求；模型 Code（如 `qwen3.8-max`）需在请求中显式指定。
3. **免费额度管理**：在控制台[免费额度页面](https://bailian.console.aliyun.com/cn-beijing/costing-balance/free-quota)查看余量、开启/关闭“用完即停”开关；该功能默认关闭，开启后额度耗尽返回 HTTP 403 错误码 `AllocationQuota.FreeTierOnly`。
4. **节省计划抵扣**：购买 AI 通用型节省计划后，费用自动按抵扣顺序抵扣，无需手动绑定；但**不支持抵扣模型训练、模型部署、联网搜索插件等费用** [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
5. **预算控制**：在[预算管理页面](https://bailian.console.aliyun.com/cn-beijing/costing-balance/budget)为账号、业务空间或 API Key 设置月度预算，可选开启“达到预算后立即停止”（生产环境不建议启用）。

## 限制和注意事项

- **地域强约束**：免费额度、部分模型训练（如 CosyVoice）、以及多数模型的最优价格仅在华北2（北京）提供；跨地域调用将产生更高费用且无免费额度。
- **额度时效性**：免费额度有效期为 90 天（自开通/模型发布/申请通过日起较晚者计算），过期自动作废，不支持延期或补发；2025年9月8日前开通用户有效期可能不足90天 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **模型独立性**：不同模型（含快照版本，如 `qwen3.8-max` 与 `qwen3.8-max-2026-05-17`）的免费额度、训练单价、部署配置完全独立，不可互通。
- **已下架模型**：文档 1 列出大量已下架免费额度的模型（如 `wan2.7-t2v`、`qwen3-asr-flash` 等），新用户无法获得其免费额度，老用户额度仍可使用至到期 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **异步任务风险**：生图、生视频等异步任务费用结算存在延迟，充值后仍可能因历史任务出账导致二次欠费，需预留充足余额 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **退订与缩容惩罚**：预付费资源（如吞吐预留）缩容或退订时，已使用部分按 1.0–1.2 倍系数结算，剩余部分才可退款；后付费资源缩容不退费，删除即停计费。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [预算管理](../../raw/model-user-guide/test-1/budget-management.md)


