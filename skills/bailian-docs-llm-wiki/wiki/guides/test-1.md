# test 1

`test 1` 是百炼平台面向开发者提供的模型调用与成本管理核心主题，涵盖模型计费、吞吐预留、节省计划、账单管理及免费额度等关键能力。本文档整合了官方最新计费规则与实操指引，聚焦华北2（北京）地域的主流文本生成模型（如 `qwen3.8-max`、`qwen3.7-plus` 等），明确各计费模式适用场景、参数约束及开发者需主动规避的风险点。

## 支持的模型/功能

- **主流文本生成模型**：`qwen3.8-max`、`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-plus`、`qwen-plus` 及其带日期后缀的快照版本（如 `qwen3.7-plus-2026-05-26`）均被广泛支持，覆盖非思考与思考（思维链+回答）双模式 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **多地域部署**：除华北2（北京）外，美国（弗吉尼亚）、新加坡、德国（法兰克福）、日本（东京）、中国香港等地域亦提供服务，但**仅华北2（北京）地域提供新人免费额度** [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **加速与缓存能力**：`qwen3.8-max`、`qwen3.7-plus` 等模型支持[上下文缓存](raw/model-user-guide/model-experience/text-generation-model/context-cache.md)，可显著降低高频重复输入的计费成本；部分模型（如 `qwen3.8-flash`）支持高速模式（PTU），提供 1.5~2 倍 TPS 提升 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **批量与异步任务**：支持 [Batch调用](raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)，其 Token 单价为实时推理价格的 50%；生图、生视频等异步任务采用独立计费逻辑，费用结算存在延迟 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。

> **注意**：文档 1 中 `qwen3.7-max` 的能力描述为“当前能力等同于 `qwen3.7-max-2026-05-20`”，而文档 2 的训练计费表中 `qwen3.7-max-2026-05-20` 被列为独立模型代码。二者在模型能力与计费归属上存在隐含不一致，开发者应以控制台实际模型 ID 和调用返回的 `model_id` 字段为准，避免因版本映射关系变动导致预期偏差。

## 关键参数

- **Token 计费粒度**：输入/输出 Token 均按百万（M）为单位计费，阶梯计费区间中的 `K` 表示 1,000，`M` 表示 1,000,000（如 `128K` = 128,000 Token） [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **TPM 容量单位**：吞吐预留（TPU）以 `kTPM`（千 Tokens/分钟）为购买单位，输入容量起步 200 kTPM（步长 10 kTPM），输出容量起步 20 kTPM（步长 1 kTPM）；公式中输入单价按“万TPM·天”报价，需将 kTPM ÷ 10 换算 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **缓存折算系数**：不同模型缓存命中部分的折算系数不同，例如 `qwen3.8-max` 为 `0.125`，`qwen3.7-plus-2026-05-26` 为 `0.2`，直接影响预留容量的实际消耗 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **免费额度有效期**：自开通百炼/模型发布/申请通过之日起 90 天（以较晚者为准），且**仅华北2（北京）地域有效**，其他地域无此权益 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 使用方式

- **API 调用**：使用百炼通用 API Key 与 Base URL，模型 ID（如 `qwen3.8-max`）作为 `model` 参数传入；所有节省计划、资源包、免费额度均自动抵扣，无需额外配置 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **吞吐预留（TPU）**：创建后生成专属模型 Code（非原 model ID），需在 API 请求中替换 `model` 参数；标准模式与高速模式性能差异达 1.5~2 倍，需根据业务 TPS 需求选型 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **成本优化路径**：
  - 长期稳定使用 → 优先选用 [AI 通用型节省计划](https://help.aliyun.com/zh/model-studio/savings-plan-and-resource-package#ghoteqo7uv9wa)，承诺月消费换最高 5.3 折；
  - 用量小或集中单模型 → 选用对应[其他模型节省计划](raw/model-user-guide/test-1/savings-plan-and-resource-package.md)；
  - 新用户快速验证 → 启用[免费额度用完即停](raw/model-user-guide/test-1/new-free-quota.md)，避免意外扣费。
- **账单溯源**：通过账单明细中的 `资产/资源实例ID（出账粒度）` 字段（格式：`ApiKeyID;业务空间ID;模型名称;输入/输出类型;调用渠道`）精准定位费用来源 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 限制和注意事项

- **地域限制严格**：免费额度、CosyVoice 模型调优、部分模型的 `Batch调用` 半价优惠**仅限华北2（北京）地域**；跨地域调用将按对应地域单价计费，且无免费额度 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **免费额度范围窄**：仅抵扣**实时推理**费用，明确**不支持** `Batch调用`、模型训练、模型部署、知识库 RAG、PAI-DSW、OSS 等所有衍生服务 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **预算管理有盲区**：预算功能**仅覆盖 API 按调用量付费**，不包含模型训练、预置吞吐（PTU）、模型单元（DTU）等费用，设置时需单独规划 [原文标题](../../raw/model-user-guide/test-1/budget-management.md)。
- **异步任务欠费风险**：生图、生视频等异步任务费用结算存在延迟，充值补缴后仍可能因历史任务出账导致账户再次欠费，建议预留充足余额 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **模型下架影响额度**：大量模型（如 `qwen-plus`、`qwen-max`、`qwen-vl-plus` 等全系列快照版本）的免费额度已被平台下架，新用户无法获得，老用户额度到期或耗尽后即终止 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 来源文档

- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [预算管理](../../raw/model-user-guide/test-1/budget-management.md)
- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)


