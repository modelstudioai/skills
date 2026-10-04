# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与资源管理主题，涵盖模型调用、训练、部署及成本控制的全链路规则。本文整合官方文档，明确免费额度适用范围、各计费模式（按量、预留、节省计划）的边界与优先级，并指出关键限制（如地域依赖、功能互斥、出账延迟等），帮助开发者精准预估成本、规避意外扣费。所有信息均基于华北2（北京）地域最新实践，其他地域需单独验证。

## 支持的模型/功能

- **实时推理**：支持千问系列（`qwen3.8-max`、`qwen3.7-plus` 等）、DeepSeek、GLM、Kimi 等主流文本生成模型，以及万相（图像）、Qwen-VL（多模态）、CosyVoice（语音）等生成类模型。具体模型列表及能力详见 [模型调用价格](raw/model-user-guide/test-1/model-pricing.md)。
- **批量推理（Batch）**：支持 OpenAI 兼容 Batch 接口，但其费用不享受免费额度抵扣，且单价为实时推理的 50% [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。
- **模型训练与调优**：支持文本生成、图像生成、视频生成、语音合成四类模型的微调，计费按训练 [Token](../concepts/token.md) 总量计算，与推理费用完全分离 [原文标题](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)。
- **模型部署**：提供 PTU（预置吞吐）、DTU（模型单元）等部署形态，按使用时长或吞吐量计费，部署状态为“运行中”即开始计费，与是否被调用无关 [原文标题](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)。

> **注意**：`test 1` 主题下，**上下文缓存**（显式/隐式）仅影响输入 [Token](../concepts/token.md) 计费单价，不改变输出单价；而 **Batch 调用**与**上下文缓存**不能同时生效，二者折扣互斥 [原文标题](../../raw/model-user-guide/model-experience/text-generation-model/context-cache.md)。

## 关键参数

- **[Token](../concepts/token.md) 计量**：输入/输出 Token 均计入总消耗，免费额度为输入+输出共用总额度，不区分类型。
- **阶梯计费**：部分模型（如 `qwen3-max`）对输入 Token 分档定价（如 0–32K、32K–128K），单次请求所有 Token 按最高档单价结算。
- **TPM 容量**：吞吐预留（TPM）以 kTPM（千 Tokens/分钟）为单位购买，输入按万TPM报价、输出按千TPM报价，需在公式中换算 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **缓存折算系数**：在吞吐预留场景下，缓存命中的输入 Token 按特定系数（如 `qwen3.8-max` 为 0.125）折算容量消耗，直接影响实际占用额度。
- **地域绑定**：免费额度、节省计划、模型部署均严格绑定地域（如华北2），跨地域调用不共享额度或折扣。

## 使用方式

1. **开通与初始化**：首次开通百炼后，系统自动发放华北2（北京）地域模型的新人免费额度（通常 100 万 Token），无需实名认证即可使用 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
2. **调用模型**：使用通用 API Key 发起 HTTP 请求，系统自动按优先级抵扣：免费额度 → 资源包 → AI 通用型节省计划 → 按量付费。专属 API Key（如 Token Plan）不消耗免费额度。
3. **成本管控**：
   - 设置预算：在[预算管理](https://bailian.console.aliyun.com/cn-beijing/costing-balance/budget)页面为账号、业务空间或 API Key 设置月度上限，开启“达到预算后立即停止”可自动限流。
   - 开启“免费额度用完即停”：在免费额度页面为单个模型开启此开关，额度耗尽时返回 `AllocationQuota.FreeTierOnly` 错误，避免意外扣费。
4. **查询与分析**：
   - 查看剩余额度：通过控制台[免费额度](https://bailian.console.aliyun.com/cn-beijing/costing-balance/free-quota)页面或模型广场详情页。
   - 解析账单：账单详情页的“实例 ID（出账粒度）”字段以分号 `;` 分隔，格式为 `ApiKeyID;业务空间ID;模型名称;输入/输出类型;调用渠道;免费额度用完即停标识`，用于精准归因。

## 限制和注意事项

- **地域限制**：免费额度、模型部署、吞吐预留均仅在华北2（北京）地域有效，其他地域（如美国、新加坡）无免费额度，且价格不同 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **功能互斥**：
  - 开启“免费额度用完即停”后，服务将直接停止，此时节省计划无法抵扣，必须手动关闭该开关才能恢复抵扣 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
  - Batch 调用与上下文缓存不可同时生效，二者折扣策略冲突。
- **出账与扣款延迟**：模型推理账单分钟级出账（2–10 分钟），但按量付费采用“预占+月结”模式，最终扣款在次月初完成，非实时扣款。
- **欠费影响**：账户可用额度 < 0 时，即使模型仍有免费额度或节省计划，所有按量付费服务（含推理、部署）均会暂停，需结清欠费后恢复。
- **监控非计费依据**：模型监控数据（如调用量、TPM）为分钟级更新，仅供参考，不作为计费依据，计费以最终账单为准 [原文标题](../../raw/model-user-guide/model-monitoring/model-telemetry.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [预算管理](../../raw/model-user-guide/test-1/budget-management.md)


