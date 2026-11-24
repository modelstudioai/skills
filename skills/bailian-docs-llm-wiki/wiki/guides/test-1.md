# test 1

`test 1` 是阿里云百炼平台面向开发者提供的模型服务计费与成本管理核心主题，涵盖模型调用、训练、部署、预留容量及预算控制等全链路费用场景。其核心逻辑是：**按量调用默认计费，免费额度仅限华北2（北京）地域特定模型且有效期90天；模型训练与部署为独立计费项；吞吐预留、节省计划和预算管理是三大主动成本管控手段**。所有计费行为均以 [Token](../concepts/token.md)、TPM、时长或任务为计量单位，并严格区分阿里直供与三方直供模型的抵扣范围。

## 支持的模型/功能

- **支持模型类型**：覆盖文本生成（如 `qwen3.8-max`、`qwen3.7-plus`）、多模态（`qwen3-vl-8b-instruct`）、语音（`cosyvoice-v3-plus`）、图像（`wan2.7-image-pro`）及视频（`wan2.7-i2v`）等全模态模型。
- **核心功能计费范畴**：
  - **实时推理**：支持免费额度抵扣（仅华北2（北京）地域），详见[新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)；
  - **Batch 调用**：输入/输出 [Token](../concepts/token.md) 单价按实时推理价格的 50% 计费（若模型支持）；
  - **上下文缓存**：显式缓存创建与命中 [Token](../concepts/token.md) 采用独立折扣单价，不包含在标准输入单价中；
  - **模型训练**：按训练 Token 总数计费，不同模型（如 `qwen3.8-27b`、`wan2.7-image-pro`）单价差异显著；
  - **模型部署（吞吐预留）**：按输入/输出 kTPM × 时长计费，支持标准/高速模式及预付费/后付费；
  - **异步任务**（生图、生视频）：费用结算存在延迟，任务提交与出账非实时同步。

> **注意**：文档 1 明确指出“免费额度仅抵扣模型**实时推理**产生的费用”，而文档 2 和文档 3 分别强调 Batch 调用、模型训练、模型部署均**不支持**免费额度抵扣。三者定义一致，无矛盾。

## 关键参数

- **Token 计量**：输入/输出 Token 均单独计费；缓存命中部分按折算系数（如 `qwen3.8-max` 为 0.125）折减输入 kTPM；长输入按阶梯系数（如 `qwen3.7-flash-2026-07-15` 在 (32K,256K] 区间系数为 3x）折算。
- **TPM 容量单位**：1 kTPM = 1,000 Tokens/分钟；吞吐预留输入起步 200 kTPM（步长 10 kTPM），输出起步 20 kTPM（步长 1 kTPM）。
- **训练计费因子**：图像生成模型依赖 `max_steps × Lstep`，视频生成模型依赖 `∑(视频计费时长) × max_pixels/1024 × n_epochs`，语音模型依赖 `(lm_max_epoch + fm_max_epoch) × 25 × 总时长`。
- **地域影响**：同一模型（如 `qwen3.8-max`）在华北2（北京）、美国（弗吉尼亚）、新加坡等地域的单价不同，且仅华北2（北京）提供免费额度。

## 使用方式

- **免费额度启用**：完成实名认证后自动发放，无需手动领取；通过[免费额度页面](https://bailian.console.aliyun.com/cn-beijing/costing-balance/free-quota)或[模型广场](https://bailian.console.aliyun.com/model/market)查看余量；开启“免费额度用完即停”可避免意外扣费（返回 HTTP 403 错误码 `AllocationQuota.FreeTierOnly`）。
- **吞吐预留配置**：在控制台创建专属模型 code，选择标准/高速模式、预付费（按天/8h）或后付费（按小时），设置输入/输出 kTPM 及购买时长；容量换算自动应用阶梯与缓存系数。
- **节省计划接入**：购买 [AI 通用型节省计划](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md) 后，使用百炼通用 API Key 与 Base URL 调用，费用自动按抵扣顺序（免费额度 → 节省计划 → 按量付费）结算。
- **预算管理**：在[预算管理页面](https://bailian.console.aliyun.com/cn-beijing/costing-balance/budget)按账号/业务空间/API Key 设置月度预算，开启“达到预算后立即停止”可限制按量调用（返回 HTTP 429）。

> **注意**：文档 6 强调“生产环境不建议开启‘达到预算后立即停止’”，而文档 1 中“免费额度用完即停”功能也注明“生产环境不建议开启”。二者风险一致（服务中断），但适用场景不同：前者针对预算总额，后者针对免费额度耗尽。此为设计一致性，非矛盾。

## 限制和注意事项

- **免费额度限制**：仅华北2（北京）地域有效；ASR 类模型需在业务空间逐一开通权限；主账号与 RAM 子账号共享额度；快照版本（如 `qwen3.8-max-0902`）与最新版（`qwen3.8-max`）额度独立；已下架模型（如 `deepseek-v4.1-flash-1017`）新用户不再获得额度 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **模型训练与部署隔离**：训练费用与部署费用完全分离；部署的模型（如 PTU 实例）调用产生的 Token 费用，不计入模型训练账单，而是归入“百炼大模型推理”商品；部署实例到期后 2 小时释放资源。
- **抵扣范围限制**：AI 通用型节省计划**不支持抵扣**模型训练、模型部署、联网搜索插件、MCP 广场、通义深度搜索等费用；预算管理**仅统计阿里直供模型的按调用量付费**，三方直供模型费用不计入也不触发停机，但达预算后其 API 调用也会被限制。
- **账单延迟与溯源**：模型推理账单分钟级出账（2–10 分钟延迟），批量/训练/知识库账单小时级出账；账单明细中“资产/资源实例ID”字段以 `;` 分隔，格式为 `ApiKeyID;业务空间ID;模型名称;输入/输出类型;调用渠道;免费额度用完即停标识`，是定位费用来源的关键依据 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **欠费处理**：账户欠费按商品 Code 隔离，仅影响对应服务（如“百炼容量预留”欠费不影响模型调用）；异步任务（生图/生视频）在欠费期间完成仍会正常计费，充值后可能因延迟结算再次触发欠费。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [预算管理](../../raw/model-user-guide/test-1/budget-management.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)


