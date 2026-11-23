# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与成本管理主题，涵盖模型调用、训练、部署全链路的费用规则、额度机制与管控工具。本文整合免费额度、按量计费、吞吐预留、节省计划、预算及账单等关键能力，帮助开发者在保障服务稳定性的同时实现精细化成本治理。所有策略均以华北2（北京）地域为默认基准，跨地域使用需注意价格与额度差异。

## 支持的模型/功能

- **实时推理**：支持千问（Qwen）、DeepSeek、GLM、Kimi 等主流文本生成模型，以及千问VL、万相、CosyVoice 等多模态与语音模型。仅实时推理调用可抵扣新人免费额度，详见[新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **批量调用（Batch）**：部分模型（如 `qwen3.8-max`）支持 Batch 接口，其输入/输出 Token 单价为实时推理价格的 50%，但**不与上下文缓存折扣同时生效** [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **上下文缓存**：支持显式/隐式缓存，命中 Token 按折扣单价计费（如 10%），创建缓存 Token 按标准输入单价的 125% 计费；该能力与 Batch 调用互斥 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **模型训练与部署**：覆盖文本、图像、语音、视频四类模型调优，训练按 Token 总量计费；部署支持吞吐预留（PTU）与模型单元（DTU）两种模式，其中 PTU 分标准/高速模式，且支持长输入阶梯系数与缓存折算 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。

> **注意**：文档 1 明确指出免费额度**不支持 Batch 调用、模型调优、模型部署**；而文档 2 在“影响计费的因素”中说明 Batch 调用可享半价——二者无矛盾，因 Batch 属于独立计费路径，其半价优惠与免费额度抵扣属正交机制，但 Batch 请求本身无法消耗免费额度。

## 关键参数

- **Token 计量**：输入/输出 Token 统一计入免费额度总额度（如 `qwen3.8-max` 为 100 万 Token），不区分类型；调用时按实际 token 数实时扣减。
- **TPM（Tokens Per Minute）**：吞吐预留容量单位，1 kTPM = 1,000 Tokens/分钟；输入/输出容量起步值分别为 200 kTPM / 20 kTPM，步长为 10 kTPM / 1 kTPM。
- **容量换算系数**：
  - *缓存折算系数*：缓存命中部分 Token 按系数折算（如 `qwen3.8-max` 为 0.125），直接影响 kTPM 消耗；
  - *长输入阶梯系数*：对超长输入（如 >32K）分段应用不同系数（如 `qwen3.7-flash` 的 (32K,256K] 区间为 3x） [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **地域与部署范围**：同一模型在不同地域（如华北2、新加坡、弗吉尼亚）价格不同，且免费额度**仅华北2（北京）有效**；部分模型（如 CosyVoice 调优）仅限华北2 地域使用 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。

## 使用方式

- **免费额度启用**：完成实名认证后，系统自动发放，无需手动领取；额度在控制台[免费额度页面](https://bailian.console.aliyun.com/cn-beijing/costing-balance/free-quota)或[模型广场](https://bailian.console.aliyun.com/model/market)查看，分钟级更新。
- **按量付费调用**：使用通用 API Key 与 Base URL，费用自动从账户余额扣除；支持通过 AI 通用型节省计划（最高 5.3 折）、资源包或 Token Plan 抵扣，三者均使用同一套接入凭证 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **吞吐预留（PTU）**：创建后生成专属 `model` code，需在 API 请求中替换原模型 ID；支持预付费（按天/8小时）与后付费（按小时），扩容/缩容按剩余有效期或实际使用时长结算。
- **预算管理**：在[预算管理页面](https://bailian.console.aliyun.com/cn-beijing/costing-balance/budget)设置账号/业务空间/API Key 级月度预算，开启“达到预算后立即停止”可自动返回 HTTP 429 错误，但**生产环境不建议开启**，以防服务中断。

## 限制和注意事项

- **免费额度限制**：有效期 90 天（以开通/模型发布/申请通过三者最晚时间起算）；额度到期或耗尽后自动失效，不补发、不延期；主账号与 RAM 子账号共享额度，但不同模型（含快照版本）额度完全独立 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **地域与模型兼容性**：免费额度、部分训练能力（如 CosyVoice）、特定部署选项（如某些 PTU 模式）均受地域约束；跨地域调用需单独确认价格与功能可用性。
- **账单延迟与出账逻辑**：大模型推理账单通常延迟 2–10 分钟出账，异步任务（如生视频）费用可能在任务完成数小时后才结算；**节省计划额度扣减基于实际出账时间，非任务提交时间**，需设置消费预警避免意外欠费 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **三方直供模型隔离**：预算管理、免费额度、节省计划均**不覆盖三方直供模型**（模型卡片标有“三方直供”）；但开启“达预算即停”后，阿里直供模型费用耗尽时，API 直接调用三方模型也会被限制。
- **欠费影响范围**：按商品 Code 隔离，百炼容量预留欠费不影响模型调用，反之亦然；代金券不计入账户可用额度，后付费场景下需确保现金余额 > 当月冻结金额才能正常调用。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [预算管理](../../raw/model-user-guide/test-1/budget-management.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)


