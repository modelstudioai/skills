# test 1

`test 1` 是阿里云百炼平台面向开发者提供的模型服务计费与资源管理主题的统称，涵盖新人免费额度、模型调用、训练、部署、吞吐预留、节省计划及成本管控等核心计费场景。所有计费行为均基于地域（如华北2）、模型 Code、调用方式（实时/批量/Batch）和资源类型（按量/预置/订阅）进行精确计量与隔离。开发者需特别注意免费额度的地域限制、模型快照版本的额度独立性，以及不同计费模式（如按量 vs 预留）在容量、溢出策略和生命周期上的关键差异。

## 支持的模型/功能

- **支持模型**：覆盖千问（Qwen）、万相（Wan）、CosyVoice、DeepSeek、GLM、Kimi 等系列，包括文本生成、多模态（VL）、语音（ASR/TTS）、图像/视频生成等类型。具体模型列表以[模型广场](https://bailian.console.aliyun.com/model/market)实时展示为准。
- **核心功能**：
  - 实时推理（含思考链、Batch 调用、上下文缓存）；
  - 模型训练（微调），支持文本、图像、视频、语音等多模态任务；
  - 模型部署（PTU/DTU），提供标准与高速（1.5–2×TPS）两种性能模式；
  - 吞吐预留（TPM 预留），支持标准/高速模式及 8 小时时段包；
  - 成本优化工具：AI 通用型节省计划、模型专属节省计划、资源包、[Token](../concepts/token.md) Plan。

> **注意**：文档 1 明确指出“ASR 类模型需在百炼控制台业务空间逐一开通权限后方可调用并消耗免费额度”，而文档 3 和文档 5 中未提及该强制开通要求，存在操作流程不一致风险。实际使用前请务必在控制台完成 ASR 模型的业务空间授权。

## 关键参数

| 参数类别 | 关键参数 | 说明 |
|----------|----------|------|
| **计费维度** | 地域、模型 Code、API Key、业务空间、调用渠道（如 `app`/`batch`/`managed agent`） | 所有账单按此粒度拆分；地域决定免费额度可用性与价格（如华北2有免费额度，其他地域无）[原文标题](../../raw/model-user-guide/test-1/new-free-quota.md) |
| **[Token](../concepts/token.md) 计量** | 输入 [Token](../concepts/token.md)、输出 Token、缓存命中 Token | 免费额度为输入+输出共用总额度，不区分类型；缓存命中 Token 按折算系数（如 0.125）计入预留容量消耗 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md) |
| **吞吐单位** | kTPM（1,000 Tokens/分钟）、万TPM（10,000 Tokens/分钟）、千TPM（1,000 Tokens/分钟） | 输入单价按万TPM 报价，输出单价按千TPM 报价；公式中需换算 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md) |
| **阶梯计费** | 输入 Token 区间（如 `(0,128K]`, `(128K,1M]`） | 单次请求所有 Token 均按最高区间单价结算；长输入按阶梯系数折算（如 Qwen3.7-flash 的 `(32K,256K]` 区间系数为 3x） |

## 使用方式

- **免费额度**：首次开通华北2（北京）地域百炼即自动发放（无需实名认证），有效期 90 天，仅抵扣实时推理费用。查看路径：[免费额度页面](https://bailian.console.aliyun.com/cn-beijing/costing-balance/free-quota) 或 [模型广场详情页](https://bailian.console.aliyun.com/model/market)。
- **按量调用**：使用通用 API Key + Base URL（如 `https://dashscope.aliyuncs.com/compatible-mode/v1`），费用实时计入账单，支持节省计划自动抵扣。
- **吞吐预留（TPM）**：创建后生成专属模型 Code（需替换 API 请求中的 `model` 参数），调用该 Code 即走预留通道；标准模式 TPS 与普通 API 相同，高速模式提升 1.5–2×TPS。
- **节省计划**：购买 AI 通用型节省计划后，**自动生效**，无需修改 API Key 或 Base URL，费用在结算时按抵扣顺序自动抵扣 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **预算管理**：在[预算管理页面](https://bailian.console.aliyun.com/cn-beijing/costing-balance/budget)设置账号/业务空间/API Key 级别月度预算，开启「达到预算后立即停止」可自动返回 HTTP 429。

## 限制和注意事项

- **免费额度限制**：
  - 仅华北2（北京）地域有效，其他地域无；
  - 不抵扣 Batch 调用、模型训练、模型部署、PAI-DSW、OSS 存储等费用；
  - 不同模型（含带日期后缀的快照版，如 `qwen-max-2025-01-25`）额度完全独立，不互通；
  - RAM 子账号与主账号共享额度，但模型用量统计按账号隔离。

- **模型训练与部署限制**：
  - CosyVoice 模型调优**仅支持华北2（北京）**地域；
  - 模型部署（PTU）溢出时，若选择「仅使用 PTU 容量」策略，超限调用将返回 429；若选「自动溢出」，则切换为按量付费，并在响应 Header 中添加 `x-dashscope-ptu-overflow:true`。

- **成本管控限制**：
  - 预算管理**不包含**模型训练、预置吞吐（PTU）、模型单元（DTU）费用，仅限 API 按量调用；
  - 「达到预算后立即停止」功能**不适用于 PTU 溢出部分及应用（app）渠道调用**；
  - 节省计划额度按**动态月**发放（非自然月），当月未用完自动清零，不可累积；
  - 账单存在 2–10 分钟出账延迟，控制台数据刷新亦有延迟，**不可依赖实时余额判断服务状态**。

- **关键注意事项**：
  > **注意**：文档 4 中“扩容”章节明确说明“预付费购买粒度为天，计费精度为小时”，而文档 6 的“欠费处理”部分指出“按量付费采用‘预占+月结’模式”，二者计费精度（小时 vs 月）存在表述冲突。实际计费以账单明细中按分钟/小时出账的记录为准，建议以[账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)为最终依据。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [预算管理](../../raw/model-user-guide/test-1/budget-management.md)


