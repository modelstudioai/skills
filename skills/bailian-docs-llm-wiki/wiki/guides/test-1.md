# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与成本管理主题，涵盖模型训练、部署、调用及预算控制等全链路费用规则。本文整合官方文档，明确各计费模式适用场景、关键参数逻辑与实操限制，帮助开发者精准预估成本、规避意外扣费，并高效选择抵扣方案。所有价格与规则均以华北2（北京）地域为准，其他地域需单独确认。

## 支持的模型/功能

`test 1` 覆盖百炼平台主流模型类型及其对应计费能力：

- **文本生成模型**：千问系列（Qwen3.x、Qwen2.5）、DeepSeek、GLM 等，支持按 [Token](../concepts/token.md) 调用计费、吞吐预留（PTU/DTU）及模型部署计费 [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **多模态模型**：千问VL、万相（图像生成）、Qwen-Image（图像生成）、万相-i2v（视频生成），其训练计费基于 [Token](../concepts/token.md) 总量或等效时长/像素计算 [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **语音模型**：CosyVoice、Qwen-TTS、Paraformer 等，训练按音频总秒数与轮次计费，推理按字符或秒计费 [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **工具与扩展服务**：Function Calling、网页抓取、联网搜索等原生工具调用费用可被 AI 通用型节省计划抵扣，但联网搜索插件本身独立计费 [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

> **注意**：文档中 `qwen3.7-max` 与 `qwen3.7-max-2026-05-20` 在多个价格表中被标注为“当前能力等同”，但其输入单价在[模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)中均为 ¥12/百万[Token](../concepts/token.md)，而[吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)中标准模式输入单价为 ¥121/万TPM·天（即 ¥12.1/百万Token），存在约 0.8% 的微小差异，属四舍五入导致，不影响实际计费精度。

## 关键参数

计费行为由以下核心参数驱动，开发者需在 API 请求或控制台配置中显式指定：

- **`model`**：模型唯一标识符（如 `qwen3.8-max`、`wan2.7-i2v`），决定基础单价、免费额度归属及支持的计费模式。不同快照版本（如 `qwen3.5-plus-2026-02-15`）视为独立模型，额度不共享 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **`input_tokens` / `output_tokens`**：实际消耗的输入与输出 Token 数，是按量计费的直接依据；阶梯计费按单次请求总输入 Token 所属区间统一结算 [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)。
- **`max_steps` / `n_epochs` / `max_pixels` / `generation_type`**：训练类任务的关键超参，直接影响训练 Token 总量计算。例如万相图像训练中 `generation_type=t2i` 且 `max_token_length="1k"` 时，`Lmax=12,800` [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **`tpm_capacity`**：吞吐预留（PTU）购买的容量单位（kTPM），结合模型的`长输入阶梯系数`和`缓存折算系数`动态换算实际消耗 [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **`free_quota_stop`**：免费额度用完即停开关状态（`0` 或 `1`），影响额度耗尽后的行为（返回 403 或转按量付费） [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 使用方式

### 1. 成本规划与抵扣选型
- **试用期**：开通即获华北2（北京）地域各模型 100 万 Token 免费额度，有效期 90 天，自动优先抵扣 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **长期稳定使用**：首选 [AI 通用型节省计划](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)，承诺月消费换取最高 5.3 折，覆盖绝大多数阿里直供模型。
- **用量集中或团队协作**：按需选用资源包（单模型固定 Token 量）或 Token Plan（团队席位制） [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

### 2. 调用与监控
- **API 调用**：使用通用 API Key（非 Token Plan 专属 Key）以消耗免费额度；实时调用自动按 `免费额度 > 资源包 > 节省计划 > 按量付费` 顺序抵扣 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **用量监控**：通过 [模型用量](https://bailian.console.aliyun.com/cn-beijing/costing-balance/usage-statistics) 页面分钟级查看 Token 消耗，通过 [账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail) 查看 T+1 日明细，字段 `实例 ID（出账粒度）` 可溯源至 `ApiKeyID;业务空间ID;模型名称` [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

### 3. 预算与风控
- **主动控费**：在 [预算管理](https://bailian.console.aliyun.com/cn-beijing/costing-balance/budget) 设置账号/业务空间/API Key 级别月度预算，开启「达到预算后立即停止」可自动返回 429 错误 [预算管理](../../raw/model-user-guide/test-1/budget-management.md)。
- **防欠费**：设置 [高额消费预警](https://usercenter2.aliyun.com/home/alarm-threshold)；账户欠费时，即使有剩余额度也无法调用 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 限制和注意事项

- **地域限制**：免费额度、部分模型训练（如 CosyVoice）仅支持华北2（北京）地域；其他地域（新加坡、美国等）需单独购买对应地域的节省计划或按量付费 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)、[节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **额度隔离**：免费额度、资源包、节省计划相互独立，不互通；同一模型的不同快照版本额度不共享，系统不会自动切换 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **计费延迟**：模型推理账单通常 2–10 分钟出账，批量/训练类任务小时级出账；“预占+月结”模式下，实际扣款在次月初完成 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **服务依赖**：模型部署状态为“运行中”即开始按时长计费，与是否被 API 调用无关；未主动调用也可能产生费用 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **缓存与阶梯**：上下文缓存命中部分按特殊折算系数计费，长输入按阶梯系数放大 TPM 消耗，需在吞吐预留配置中预先评估 [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)、[模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)。

## 来源文档

- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [预算管理](../../raw/model-user-guide/test-1/budget-management.md)


