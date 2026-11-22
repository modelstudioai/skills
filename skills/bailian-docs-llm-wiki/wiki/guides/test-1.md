# test 1

`test 1` 是阿里云百炼平台面向开发者提供的模型服务计费与成本管理核心主题，涵盖新人免费额度、按量调用、模型训练/部署、吞吐预留、节省计划及预算管控等全链路成本要素。本文档结构化梳理关键能力边界、参数规则与实操要点，帮助开发者快速建立成本认知并规避常见误用风险。

## 支持的模型/功能

- **实时推理**：支持千问（Qwen）、DeepSeek、GLM、Kimi 等主流大模型及[多模态](../concepts/multi-modal.md)模型（如 Qwen-VL、万相）的 API 调用，覆盖文本生成、图像生成、语音合成与识别、视频生成等场景。
- **批量调用**：支持 [Batch 接口](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)，输入/输出 [Token](../concepts/token.md) 单价为实时推理价格的 50%（部分模型适用），但不与上下文缓存折扣叠加。
- **上下文缓存**：支持显式/隐式缓存，命中 [Token](../concepts/token.md) 按极低单价计费（如 qwen4-max 缓存命中仅 ¥0.5/百万 [Token](../concepts/token.md)），但创建缓存按更高单价计费（如 qwen4-max 创建缓存（5m）为 ¥12.5/百万 Token）[原文标题](../../raw/model-user-guide/model-experience/text-generation-model/context-cache.md)。
- **模型调优与部署**：支持文本、图像、语音、视频模型的微调训练（按训练 Token 计费），以及模型高速部署（吞吐预留/PTU）或按量部署（DTU）。
- **不支持免费额度抵扣的功能**：[Batch调用](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)、[模型调优](https://help.aliyun.com/zh/model-studio/model-training-overview)、[模型部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)、PAI-DSW、OSS 存储及联网搜索插件费用均不可用免费额度抵扣。

> **注意**：文档 1 明确指出免费额度“仅抵扣模型**实时推理**（调用）产生的费用”，而文档 2 和文档 3 中 Batch 调用、模型训练、模型部署均被单独列为独立计费项，三者逻辑一致，无矛盾。

## 关键参数

- **Token 计费粒度**：所有按量调用以输入 Token 和输出 Token 分别计量，1 Token ≈ 1 个中文字符或 3/4 个英文单词；长文本输入按阶梯系数折算（如 qwen3.7-flash 输入 >32K 部分系数为 3x）。
- **地域与价格绑定**：同一模型在不同地域价格不同（如 qwen3.8-max 华北2输入单价 ¥12/百万，美国弗吉尼亚为 ¥14.988/百万），且**仅华北2（北京）地域模型享有免费额度**。
- **吞吐预留（PTU）单位**：kTPM（千 Tokens/分钟），输入起步 200 kTPM，输出起步 20 kTPM；高速模式 TPS 提升 1.5–2 倍，但单价显著高于标准模式（如 qwen3.8-max 华北2高速预付费输入单价 ¥34.56/kTPM·天 vs 标准模式 ¥12.1/kTPM·天）。
- **节省计划承诺周期**：AI 通用型节省计划以“动态月”为周期（非自然月），每月额度独立发放、当月清零，不累积；入门型计划亦遵循此规则 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

## 使用方式

- **免费额度自动生效**：完成[实名认证](https://myaccount.console.aliyun.com/cert-info)后，主账号或拥有 `AliyunBailianFullAccess` 权限的 RAM 账号登录控制台即自动发放，无需手动领取 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **API 调用**：使用通用 API Key 与 Base URL，费用自动按抵扣顺序结算（免费额度 → 节省计划 → 资源包 → 按量付费）；专属吞吐预留需替换 `model` 参数为生成的专属 model code。
- **节省计划接入**：购买后自动生效，无需配置；抵扣范围覆盖模型调用、工具调用（Function Calling、网页抓取）、上下文缓存、批量推理等，但**不支持模型训练、部署、知识库规格费及联网搜索插件费用**。
- **预算管理**：在[预算管理](https://bailian.console.aliyun.com/cn-beijing/costing-balance/budget)页面按账号/业务空间/API Key 设置月度预算，开启“达到预算后立即停止”可自动返回 HTTP 429 错误。

## 限制和注意事项

- **免费额度限制**：有效期 90 天（以开通/模型发布/申请通过之日较晚者起算）；额度用尽或过期后自动失效，不补发、不延期；RAM 子账号与主账号共享额度；不同模型（含快照版本）额度完全独立，不互通。
- **吞吐预留生命周期**：预付费实例到期后立即停机，2 小时后释放资源；8 小时时段预留不支持扩缩容、续订与退订，时段结束即失效。
- **账单延迟**：模型推理账单分钟级出账（通常 2–10 分钟），批量/训练/部署账单小时级出账；**出账不等于扣款**，按量付费采用“预占+月结”模式。
- **欠费隔离**：欠费按商品 Code 隔离（如“百炼容量预留”欠费不影响“百炼大模型推理”服务），但已欠费的商品 Code 下，节省计划、资源包等额度均无法抵扣。
- **预算管理局限性**：仅统计阿里直供模型的 API 按量调用费用，**不包含三方直供模型、模型训练、PTU、DTU、知识库规格费**；开启“达预算即停”后，即使后续发放免费额度，服务也不会自动恢复，需手动调整预算。

> **注意**：文档 7 明确说明“三方直供模型的费用不计入预算金额”，而文档 5 在“AI 通用型节省计划”中指出“C 类模型（如 DeepSeek、Kimi）可抵扣但无折扣”，二者存在关键差异——预算管理完全排除三方直供模型，而节省计划虽无折扣但仍可抵扣其费用。开发者需严格区分“预算管控范围”与“费用抵扣范围”。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [预算管理](../../raw/model-user-guide/test-1/budget-management.md)


