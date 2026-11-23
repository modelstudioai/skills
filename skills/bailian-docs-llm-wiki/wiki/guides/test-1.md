# test 1

`test 1` 是阿里云百炼平台面向开发者提供的模型服务计费与资源管理核心主题，涵盖新人免费额度、模型调用、训练部署、吞吐预留、节省计划及成本管控等全链路能力。本文档整合官方最新规则，聚焦可执行的技术细节，不包含营销性描述，所有信息均基于当前生效的平台策略。

## 支持的模型/功能

- **实时推理**：支持千问（Qwen）系列（如 `qwen4-max`、`qwen3.8-max`）、DeepSeek、GLM、Kimi 等主流大模型，覆盖文本生成、多模态、语音、图像、视频等场景。  
- **批量调用**：支持 [Batch调用](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)，输入/输出 Token 单价为实时推理价格的 50%（部分模型适用）。  
- **上下文缓存**：支持显式/隐式缓存，命中时输入 Token 按折扣单价计费（如 `qwen4-max` 缓存命中单价为 ¥0.5/百万 Token），详见 [上下文缓存](../../raw/model-user-guide/model-experience/text-generation-model/context-cache.md)。  
- **模型训练与部署**：支持千问、万相、CosyVoice 等模型的微调训练（按 Token 计费）及高速/标准模式部署（按 TPM 或时长计费）。  
- **异步任务**：生图、生视频等任务采用异步机制，费用在任务完成并结算后计入账单，存在延迟出账特性（见 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)）。

> **注意**：文档 1 明确指出免费额度**仅抵扣模型实时推理**产生的费用，而 [Batch调用](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)、[模型调优](https://help.aliyun.com/zh/model-studio/model-training-overview)、[模型部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md) 均**不支持**用免费额度抵扣。该规则与文档 2 中 Batch 调用享半价优惠、文档 3 中训练/部署单独计费的描述完全一致，无矛盾。

## 关键参数

- **免费额度**：新人开通后自动发放，通常为 100 万 Token/模型，**仅限华北2（北京）地域**，有效期 90 天（以开通/发布/申请通过之日较晚者起算）；不同模型（含快照版本）额度独立，不互通。  
- **Token 计费粒度**：模型调用按输入/输出 Token 总数计费；训练按训练 Token 总量计费（单位：千 Token）；部署按 kTPM（千 Tokens/分钟）购买容量。  
- **阶梯计费**：部分模型（如 `qwen3.7-plus`）对输入 Token 分档定价（如 0–256K、256K–1M），单次请求所有 Token 均按所属最高档单价结算。  
- **缓存折算系数**：吞吐预留中，缓存命中部分按系数折算（如 `qwen3.8-max` 系数为 0.125），直接影响 kTPM 消耗量（见 [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)）。  
- **地域价格差异**：同一模型在不同地域价格不同（如 `qwen3.8-max` 在北京输入单价 ¥12/百万 Token，在弗吉尼亚为 ¥14.988/百万 Token），且免费额度仅北京有效。

## 使用方式

- **开通与认证**：需先完成[实名认证](https://myaccount.console.aliyun.com/cert-info)，再使用主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 账号登录控制台，系统自动开通服务并发放免费额度。  
- **调用模型**：使用通用 API Key 与 Base URL，通过标准 REST API 调用；Batch 调用需使用专用接口（如 `/v1/batches`）。  
- **启用节省计划**：推荐选用 [AI 通用型节省计划](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)，购买后自动抵扣支持范围内的模型调用费用，无需修改代码或配置。  
- **设置预算**：在 [预算管理](../../raw/model-user-guide/test-1/budget-management.md) 页面按账号/业务空间/API Key 设置月度预算，可选开启“达到预算后立即停止”以自动限制调用（生产环境慎用）。  
- **查看用量与额度**：通过控制台 [免费额度](https://bailian.console.aliyun.com/cn-beijing/costing-balance/free-quota)、[模型用量](https://bailian.console.aliyun.com/cn-beijing/costing-balance/usage-statistics)、[费用概览](https://bailian.console.aliyun.com/cn-beijing/costing-balance/overview) 页面实时监控。

## 限制和注意事项

- **免费额度限制**：ASR 类模型需在业务空间**逐一开通权限**后方可调用并消耗额度；主账号与 RAM 子账号**共享额度**；已下架模型（如 `qwen3.8-max-0902`）新用户不再获得额度，老用户额度仍可使用至到期（见 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)）。  
- **吞吐预留限制**：8 小时时段预留**不支持扩缩容、续订与退订**，仅限每日 22:00–00:00 下单；高速模式预付费实例到期后停机 2 小时释放资源，后付费实例无到期概念。  
- **账单与欠费**：模型推理账单**分钟级出账（2–10 分钟延迟）**，异步任务（生图/生视频）费用结算更晚；账户欠费按**商品 Code 隔离**，某商品欠费不影响其他服务（如百炼推理欠费不影响 PTU 部署）；代金券不计入账户可用额度，充值后仍可能因延迟结算再次欠费（见 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)）。  
- **预算管理限制**：仅统计**阿里直供模型**的 API 按量付费费用，三方直供模型、训练、部署、知识库规格费等**均不计入**；开启“达预算即停”后，API 直接调用三方直供模型也会被限制（见 [预算管理](../../raw/model-user-guide/test-1/budget-management.md)）。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [预算管理](../../raw/model-user-guide/test-1/budget-management.md)


