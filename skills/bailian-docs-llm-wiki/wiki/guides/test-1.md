# test 1

`test 1` 是百炼平台面向开发者提供的模型调用与成本管理核心主题，涵盖模型计费、免费额度、吞吐预留、节省计划、账单查询及预算控制等关键能力。本文档整合官方最新文档，聚焦实际开发场景中的可操作信息，明确各计费模式的适用边界、抵扣优先级与配置要点，帮助开发者快速建立成本可控的模型服务架构。

## 支持的模型/功能

`test 1` 覆盖百炼平台主流文本生成模型（千问 Max/Plus/Flash 系列）、多模态模型（千问VL、万相）、语音模型（CosyVoice、Qwen-TTS）及第三方模型（DeepSeek、GLM、Kimi），支持实时推理、Batch 调用、上下文缓存、模型训练、模型部署（PTU/DTU）、知识库（RAG）等全链路功能。其中，**新人免费额度仅适用于华北2（北京）地域的实时推理调用**，不覆盖 Batch 调用、模型训练、模型部署、PAI-DSW、OSS 存储等 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。> **注意**：文档 1 中列出的 `qwen3.8-max-prime` 模型在“华北2（北京）”价格表中标注“无免费额度”，但文档 2 明确指出“仅华北2（北京）地域模型享有免费额度”，且该模型 ID 在文档 2 的适用范围中未被排除；此矛盾表明 `qwen3.8-max-prime` 当前不参与新人免费额度发放，其免费额度状态以 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md) 的通用规则为准，即“不同模型（含快照版本）额度相互独立”，该模型需单独确认额度状态。

## 关键参数

- **Token 计费粒度**：输入/输出 Token 均按实际消耗计费，单价单位为“每百万 Token”。阶梯计费按单次请求总输入 Token 所属区间统一结算（如输入 100K Token 落入第二档，则全部 100K 按第二档单价计费）[原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **TPM 容量单位**：吞吐预留（TPU）以 kTPM（1,000 Tokens/分钟）为购买单位，输入按万TPM、输出按千TPM 报价；长输入与缓存命中按模型特定系数折算容量消耗 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **抵扣优先级**：费用结算时严格遵循 `免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费` 的顺序，此规则是成本规划的基础 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 使用方式

1. **开通与调用**：首次开通百炼后，系统自动发放华北2（北京）地域各模型的免费额度（通常 100 万 Token），无需手动领取或实名认证即可使用 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。调用时使用通用 API Key 与对应地域 Base URL（如 `https://dashscope.aliyuncs.com/compatible-mode/v1`），系统自动优先抵扣免费额度。
2. **成本优化选型**：
   - 长期稳定使用：首选 **AI 通用型节省计划**（承诺月消费换阶梯折扣，最高 5.3 折），覆盖绝大部分阿里直供模型 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
   - 用量小或集中单模型：选用**其他模型节省计划**或**资源包**。
   - 编程/智能体工具场景：选用 **Token Plan**（需专属 API Key）。
3. **预算与告警**：通过 [预算管理](https://bailian.console.aliyun.com/cn-beijing/costing-balance/budget) 设置账号/业务空间/API Key 级别月度预算，开启“达到预算后立即停止”可自动限制按量调用（返回 HTTP 429），但生产环境不建议开启 [原文标题](../../raw/model-user-guide/test-1/budget-management.md)。

## 限制和注意事项

- **地域限制**：免费额度、部分模型训练（如 CosyVoice）仅限华北2（北京）；节省计划、吞吐预留等需按地域分别购买，不可跨地域抵扣或使用。
- **额度时效性**：免费额度有效期为 90 天（以开通/模型发布/申请通过之日较晚者为准），到期或耗尽后自动失效，不补发、不延期；AI 通用型节省计划按“动态月”分配额度，当月未用完部分自动清零 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **服务中断风险**：账户欠费时，即使模型仍有免费额度或节省计划剩余额度，所有按量付费服务（包括推理、部署）均会暂停；模型部署（PTU/DTU）按使用时长计费，部署状态为“运行中”即开始收费，与是否被调用无关 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **出账延迟**：模型推理账单通常在调用结束后 2~10 分钟出账，批量推理、训练等为小时级出账；账单显示的“大模型文本消耗量”需结合“实例 ID（出账粒度）”字段（格式为 `ApiKeyID;业务空间ID;模型名称;...`）才能准确定位具体模型 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 来源文档

- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [预算管理](../../raw/model-user-guide/test-1/budget-management.md)


