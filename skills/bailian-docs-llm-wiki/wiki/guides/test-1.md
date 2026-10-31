# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与成本管理主题，涵盖模型训练、模型部署、吞吐预留、节省计划、账单查询及预算控制等全链路费用场景。本文档整合官方最新规则，聚焦可执行的技术细节，不包含营销性描述，所有价格与参数均以原始文档为准，并明确标注矛盾或过时信息。

## 支持的模型/功能

`test 1` 覆盖百炼平台主流模型类型的计费能力，包括文本生成（千问系列）、多模态（千问VL、万相）、语音（CosyVoice、Qwen-TTS/ASR）及视频生成模型。其中：

- **文本生成模型**（如 `qwen3.8-max`、`qwen3.7-plus-2026-05-26`）支持按 Token 调用计费、吞吐预留（PTU/DTU）、AI 通用型节省计划等多种模式，是当前最成熟、覆盖最广的计费类型 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **图像与视频生成模型**（如 `wan2.7-i2v`、`qwen-image-2.0-pro`）采用基于 `max_pixels`、`n_epochs` 或 `计费时长` 的 Token 估算公式，计费逻辑与文本模型差异显著，且部分模型（如 `wan2.7-i2v`）已下架免费额度 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **语音合成模型**（如 `cosyvoice-v3-plus`）仅支持华北2（北京）地域，训练计费公式为 `(lm_max_epoch + fm_max_epoch) × 25 × 总时长（秒）`，不参与通用节省计划抵扣 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。

> **注意**：文档 2 明确列出 `wan2.7-i2v` 已于 2026-10-29 下架免费额度；而文档 1 中仍将其列为有效训练模型并给出价格（2元/千Token）。实际使用中，该模型**不再享有新人免费额度**，但训练服务本身仍可用，需按量付费。

## 关键参数

不同计费模式依赖特定参数组合，开发者必须准确配置以避免误计费：

- **模型训练**：关键参数包括 `max_steps`（t2i/i2i）、`n_epochs`（图像/视频）、`max_pixels`（图像/视频）、`generation_type`（t2i/i2i）、`计费时长`（视频，取 `min(10, 四舍五入后时长)`），以及 `GPU系数`（动态值，实际用量以 API 返回 `usage` 字段为准）[原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **吞吐预留（PTU）**：关键参数为 `输入kTPM`（起步200，步长10）、`输出kTPM`（起步20，步长1）、`购买时长`（1–365天）、`性能模式`（标准/高速）及 `容量换算系数`（长输入阶梯系数、缓存折算系数）。例如 `qwen3.7-flash-2026-07-15` 输入阶梯系数为 `(0,32K] 1x, (32K,256K] 3x, (256K,1M] 6x` [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **节省计划**：关键参数为 `月承诺消费金额`（1000元起）、`购买时长`（3/6/12/24个月）、`付款方式`（全预付/零预付）及 `地域`（华北2（北京）等6地，**不跨地域抵扣**）[原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

## 使用方式

开发者应根据业务稳定性与成本敏感度选择合适模式：

- **按量调用**：适用于低频、不可预测流量。调用时使用通用 API Key 和 Base URL，费用实时计入账单。**必须注意**：免费额度仅限华北2（北京）地域，且仅抵扣实时推理（非 Batch、非训练、非部署）[原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **吞吐预留（PTU）**：适用于高并发、确定性 SLA 场景。创建后获得专属模型 Code（需替换 API `model` 参数），预留容量内调用不额外收费，溢出按策略处理（自动切换按量或返回 429）[原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **AI 通用型节省计划**：**推荐作为绝大多数场景首选**。承诺月消费金额换取阶梯折扣（最高5.3折），覆盖绝大部分阿里直供模型（A/B/C类），购买后自动生效，无需修改代码 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **资源包/Token Plan**：适用于用量小或高度集中于单一模型的场景（如仅用 `qwen3.5-plus`），或 AI 编程工具集成（Token Plan 需配置专属 API Key）[原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

## 限制和注意事项

- **地域隔离严格**：免费额度、节省计划、吞吐预留均按地域独立生效。在华北2（北京）购买的节省计划，**无法抵扣**美国（弗吉尼亚）产生的调用费用 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **免费额度非全局共享**：主账号与 RAM 子账号共享额度，但不同模型（含带日期后缀的快照版本）额度完全独立。`qwen3.7-plus-2026-05-26` 与 `qwen3.7-plus` 视为两个模型，各自拥有 100 万 Token 免费额度 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **账单延迟与出账逻辑**：模型推理账单通常延迟 2–10 分钟出账，批量/训练/知识库为小时级出账。**费用概览页面数据存在延迟，权威数据源为 [阿里云费用与成本](https://billing-cost.console.aliyun.com/home)** [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **预算管理范围有限**：仅管控 API 按调用量付费费用，**明确不包含**模型训练、模型部署（PTU/DTU）、知识库规格费等 [原文标题](../../raw/model-user-guide/test-1/budget-management.md)。
- **“达到预算后立即停止”风险提示**：生产环境**不建议开启**。该功能触发后返回 HTTP 429，且 PTU 溢出调用、应用调用暂不支持自动停止，服务停止亦有延迟，延迟期内费用仍正常收取 [原文标题](../../raw/model-user-guide/test-1/budget-management.md)。

## 来源文档

- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [预算管理](../../raw/model-user-guide/test-1/budget-management.md)


