# test 1

阿里云百炼平台的 `test 1` 主题聚焦于模型服务的核心计费与资源管理机制，涵盖实时推理、模型训练、部署、吞吐预留等多维度成本构成。本文档面向开发者，系统梳理其支持能力、关键参数、调用方式及约束条件，帮助快速建立成本控制与资源规划认知。所有信息均基于当前平台公开文档整合，不包含营销性描述。

## 支持的模型/功能

`test 1` 并非单一模型，而是指代百炼平台中围绕大模型服务的一整套计费与资源管理体系，覆盖以下核心功能模块：

- **实时推理（按量调用）**：支持千问（Qwen）、DeepSeek、GLM、Kimi 等主流文本生成模型，以及千问VL、万相（WanX）、CosyVoice 等多模态与语音模型。具体模型列表及地域支持详见[模型调用价格](raw/model-user-guide/test-1/model-pricing.md)。
- **模型训练（Fine-tuning）**：支持文本生成（千问系列）、图像生成（万相、千问图像）、视频生成（万相图生视频）、语音合成（CosyVoice）等多类型模型微调，计费按训练 [Token](../concepts/token.md) 总量计算 [模型训练与部署计费](raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **模型部署（PTU/DTU）**：提供预置吞吐（PTU）和模型单元（DTU）两种部署模式，适用于高并发、低延迟场景，支持华北2（北京）与新加坡等多地部署 [模型训练与部署计费](raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **吞吐预留（TPM Reservation）**：提供标准模式（与按量API相同TPS）与高速模式（1.5~2倍TPS）的专属推理吞吐量购买，支持8小时时段预留等灵活形态 [吞吐预留计费](raw/model-user-guide/test-1/tpm-reservation-billing.md)。

> **注意**：文档 3（模型调用价格）与文档 2（模型训练与部署计费）在部分模型价格上存在表述差异。例如，文档 3 中 `qwen3.7-plus-2026-05-26` 在华北2（北京）的输入单价为 2 元/百万[Token](../concepts/token.md)，而文档 2 中同模型训练单价为 ¥0.35/千[Token](../concepts/token.md)（即 350 元/百万Token）。此差异源于二者计费对象不同——前者为**推理调用**，后者为**模型训练**，属正常设计，非矛盾。

## 关键参数

- **Token 计量单位**：所有按量计费（推理、训练、部署）均以 Token 为基本单位。输入/输出 Token 分开计量，长上下文、缓存命中等场景有特定折算系数 [吞吐预留计费](raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **TPM（Tokens Per Minute）**：用于吞吐预留与部署计费，表示每分钟可处理的 Token 数量。购买时以 kTPM（千TPM）为单位，输入按万TPM报价、输出按千TPM报价 [吞吐预留计费](raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **免费额度**：新人开通后自动获得，通常为 100 万 Token/模型，仅限华北2（北京）地域的实时推理调用，有效期 90 天 [新人免费额度](raw/model-user-guide/test-1/new-free-quota.md)。
- **地域（Region）**：计费与功能强绑定地域。例如，免费额度、部分模型训练服务（如 CosyVoice）仅支持华北2（北京）；节省计划需按地域单独购买，不可跨地域抵扣 [节省计划与资源包](raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

## 使用方式

1. **开通与初始化**：首次开通百炼服务后，系统自动发放新人免费额度，无需手动领取或实名认证即可使用 [新人免费额度](raw/model-user-guide/test-1/new-free-quota.md)。
2. **调用模型**：
   - 实时推理：使用通用 API Key 和对应地域 Base URL（如 `https://dashscope.aliyuncs.com/compatible-mode/v1`），系统自动优先抵扣免费额度 > 资源包 > 节省计划 > 按量付费 [新人免费额度](raw/model-user-guide/test-1/new-free-quota.md)。
   - 模型训练/部署：通过控制台或 API 提交任务，费用在任务完成或资源创建后开始计算 [模型训练与部署计费](raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
3. **成本优化**：
   - 长期稳定使用：推荐购买 [AI 通用型节省计划](raw/model-user-guide/test-1/savings-plan-and-resource-package.md)，承诺月消费换取最高 5.3 折折扣。
   - 用量集中或小规模：可选特定模型节省计划或资源包 [节省计划与资源包](raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
   - 精确控费：设置 [预算管理](raw/model-user-guide/test-1/budget-management.md)，达预算后可自动停止按量调用（生产环境慎用）。

## 限制和注意事项

- **免费额度限制**：仅抵扣实时推理费用，**不支持**抵扣 Batch 调用、模型训练、模型部署、PAI-DSW、OSS 存储等任何其他费用 [新人免费额度](raw/model-user-guide/test-1/new-free-quota.md)。
- **地域隔离**：免费额度、节省计划、模型部署、吞吐预留均严格按地域隔离。在华北2（北京）购买的服务，无法用于新加坡或美国（弗吉尼亚）的调用 [节省计划与资源包](raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **欠费影响**：账户欠费按商品 Code 隔离。若“百炼大模型推理”商品 Code 欠费，即使模型仍有免费额度也无法调用；但“百炼容量预留”等其他商品 Code 的服务仍可正常使用 [账单查询与成本管理](raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **出账延迟**：模型推理账单为分钟级出账（通常 2~10 分钟），并非实时扣款。因此，预算预警、免费额度耗尽通知与实际账单生成之间存在时间差，可能导致“显示有余额但已欠费”的情况 [账单查询与成本管理](raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [预算管理](../../raw/model-user-guide/test-1/budget-management.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)


