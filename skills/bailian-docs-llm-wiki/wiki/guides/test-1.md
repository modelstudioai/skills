# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与成本管理主题，涵盖模型调用、训练、部署及资源预留等全链路费用规则。本文整合官方文档，明确免费额度适用范围、各类计费模式的优先级与抵扣逻辑，并指出关键限制（如地域约束、功能互斥性），帮助开发者精准预估成本、规避意外扣费。所有价格与策略均以华北2（北京）地域为基准，其他地域需参考对应文档确认差异。

## 支持的模型/功能

- **实时推理**：支持千问（Qwen）、DeepSeek、GLM、Kimi 等主流文本生成模型，以及万相（WanX）、Qwen-VL、CosyVoice 等多模态与语音模型。所有模型均按输入/输出 [Token](../concepts/token.md) 或特定单位（如图片张数、语音秒数）计费 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **模型训练**：覆盖文本生成（千问）、图像生成（万相、千问图像）、视频生成（万相图生视频）、语音合成（CosyVoice）四类任务，计费基于训练 [Token](../concepts/token.md) 总量或等效计算量 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **模型部署**：提供 PTU（预置吞吐）和 DTU（模型单元）两种方式，前者按 TPM 容量预付费，后者按算力单元后付费 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **批量调用（Batch）**：支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，其输入/输出 [Token](../concepts/token.md) 单价为实时推理价格的 50%，但**不支持用免费额度抵扣** [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。

> **注意**：文档 1 明确指出免费额度**仅抵扣实时推理费用**，而文档 2 和文档 3 均将 Batch 调用列为独立计费项且不支持免费额度。两者一致，但需特别注意该限制在代码集成时易被忽略。

## 关键参数

- **免费额度**：新人默认获赠各模型 100 万 Token，有效期 90 天（自开通/模型发布/申请通过日起算，以较晚者为准），仅限华北2（北京）地域 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **Token 计费粒度**：输入/输出 Token 均按实际消耗计费，不分是否产生幻觉或错误；缓存命中部分按独立单价（如 10%）结算，不计入标准输入单价 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **TPM 容量换算**：吞吐预留（PTU）中，长输入 Token 按阶梯系数折算（如 `qwen3.7-flash` 输入 >32K 部分系数为 3x），缓存命中部分再乘缓存折算系数（如 0.2） [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **抵扣优先级**：系统严格按 `免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费` 顺序抵扣费用，不可跳过或调整 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

## 使用方式

1. **开通即用**：首次开通百炼后，系统自动发放免费额度，无需实名认证即可使用；额度耗尽后，已认证用户自动转为按量付费，未认证用户需完成认证并充值 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
2. **调用配置**：
   - 实时推理：直接使用通用 API Key 调用，系统自动优先抵扣免费额度；
   - Batch 调用：需显式指定 `/v1/batch` 接口路径，单价自动半价，但**不走免费额度通道**；
   - PTU 部署：创建后获得专属 `model` Code，调用时需替换原模型 ID，容量内调用不额外计费。
3. **成本控制**：
   - 开启「免费额度用完即停」：额度耗尽时返回 HTTP 403 错误（`AllocationQuota.FreeTierOnly`），防止意外扣费；
   - 设置预算管理：可为账号、业务空间或 API Key 设置月度预算，开启「达到预算后立即停止」则超限返回 429 错误；
   - 购买节省计划：承诺月消费金额换取阶梯折扣，AI 通用型节省计划覆盖绝大部分模型，是长期使用的推荐方案 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

## 限制和注意事项

- **地域限制**：免费额度、部分模型训练（如 CosyVoice）及 PTU 部署仅支持华北2（北京）地域；其他地域（如新加坡、美国弗吉尼亚）需单独购买对应地域的节省计划或按原价计费 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **功能互斥**：
  - 「免费额度用完即停」开启后，服务停止，**AI 通用型节省计划无法抵扣**；需手动关闭该开关才能恢复节省计划抵扣 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
  - Token Plan/Coding Plan 的专属 API Key **不消耗免费额度**，必须改用通用 API Key 才能享受免费额度 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **出账延迟**：模型推理账单通常延迟 2–10 分钟生成，批量推理、训练等为小时级出账；账单详情中的「实例 ID」字段是溯源关键，格式为 `ApiKeyID;业务空间ID;模型名称;...` [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **欠费影响**：账户可用额度 < 0 时，**即使免费额度或节省计划仍有余额，所有按量付费服务均暂停**；Coding Plan/Token Plan 因额度独立，欠费期间仍可使用 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [预算管理](../../raw/model-user-guide/test-1/budget-management.md)


