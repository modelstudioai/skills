# test 1

`test 1` 是百炼平台面向开发者提供的模型调用与成本管理核心主题，涵盖模型计费、免费额度、吞吐预留、节省计划、账单查询及预算控制等关键能力。本文档整合多源技术文档，聚焦实际开发与运维场景，明确各计费模式的适用边界、参数逻辑与操作约束，避免因信息分散导致的误配或意外扣费。

## 支持的模型/功能

`test 1` 主要覆盖文本生成类大模型（如千问 Max/Plus 系列）、部分多模态模型（如千问VL）及语音合成模型（CosyVoice）的调用与训练能力。其中，**实时推理**（即 API 调用）是核心支持功能，适用于华北2（北京）、美国（弗吉尼亚）、新加坡、德国（法兰克福）、日本（东京）等多地部署；而**模型训练**与**模型部署**为独立计费模块，需单独开通并配置资源。值得注意的是，[新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)仅限华北2（北京）地域的指定模型生效，其他地域及所有训练/部署服务均不参与该福利。此外，[Batch调用](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)虽被多个文档提及，但其免费额度抵扣资格已被明确排除——根据[新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)说明，Batch调用产生的费用**不支持用免费额度抵扣**。

> **注意**：文档 1 中 `qwen3.8-max-prime` 模型标注“无免费额度”，而同属华北2（北京）的 `qwen3.8-max` 等模型则享有 100 万 Token 免费额度；但文档 2 明确指出“仅华北2（北京）地域模型享有免费额度”，未对 `prime` 模式做例外说明。此处存在隐含矛盾：若 `qwen3.8-max-prime` 部署于华北2（北京），其应默认享有额度，但文档 1 单独声明“无”，需以文档 1 的具体模型条目为准。开发者在选型时应以控制台实时展示的额度为准，而非依赖通用规则。

## 关键参数

关键参数围绕计费粒度与容量单位展开：
- **Token 计费**：输入/输出 Token 是按量付费的核心计量单位，单价按模型、地域、阶梯区间（如 0–32K、32K–128K）动态浮动，详见[模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)。
- **TPM（Tokens Per Minute）**：吞吐预留（PTU）的容量单位，购买量以 `kTPM`（千 Tokens/分钟）为步长，输入起步 200 kTPM，输出起步 20 kTPM；计费时需按公式换算为“万TPM·天”或“千TPM·天”。
- **缓存折算系数与长输入阶梯系数**：影响 PTU 容量实际消耗，例如 `qwen3.7-flash-2026-07-15` 的缓存折算系数为 0.2，长输入（>32K）阶梯系数为 3x，命中缓存可显著降低 kTPM 消耗 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **免费额度有效期**：统一为 90 天，自开通百炼、模型发布或申请通过之日三者中**最晚者**起算，且到期后剩余额度自动作废，不可延期或补发 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 使用方式

开发者可通过三种主要路径接入：
1. **按量调用（推荐入门）**：使用通用 API Key 直接调用模型，系统自动按优先级抵扣：免费额度 → 资源包 → 节省计划 → 按量付费。此方式无需预购，适合用量波动场景。
2. **吞吐预留（PTU）**：预购固定 TPM 容量，适用于有确定性 QPS 要求的生产环境。创建后获得专属 `model` 参数（如 `ptu-qwen3.8-max-xxxx`），调用时需显式指定。标准模式与高速模式（PTU）性能不同，后者提供 1.5–2 倍 TPS 提升 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
3. **节省计划**：承诺月消费金额换取折扣，AI 通用型节省计划覆盖绝大多数阿里直供模型，是长期稳定使用的首选方案。其抵扣逻辑独立于地域，只要调用请求路由至对应地域的 Base URL 即可生效 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

## 限制和注意事项

- **地域隔离严格**：免费额度、节省计划、吞吐预留均**不可跨地域共享**。例如，在华北2（北京）购买的节省计划，仅能抵扣该地域产生的调用费用；同理，新加坡地域的模型无免费额度。
- **免费额度用完即停的风险**：该功能（又称“安心模式”）开启后，额度耗尽将返回 HTTP 403 错误（错误码 `AllocationQuota.FreeTierOnly`），服务立即中断。**生产环境不建议开启**，因其可能导致业务不可用，且开启后节省计划无法生效 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **出账延迟与扣费逻辑**：模型推理账单通常延迟 2–10 分钟出账，而按量付费采用“预占+月结”模式，非实时扣款。这意味着服务停止后仍可能产生延迟账单，账户欠费将导致**所有模型调用（含仍有剩余额度者）全部中断**。
- **模型训练与部署不享受免费额度**：[新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)明确排除模型调优、模型部署、PAI-DSW 等服务，其费用需单独结算。
- **预算管理范围有限**：仅管控 API 按调用量付费，**不包含模型训练、PTU、DTU 等费用**，设置预算时需额外规划此类支出。

## 来源文档

- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [预算管理](../../raw/model-user-guide/test-1/budget-management.md)


