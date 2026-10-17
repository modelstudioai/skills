# test 1

`test 1` 是阿里云百炼平台面向开发者提供的模型服务统一计费与资源管理主题，涵盖免费额度、按量调用、吞吐预留、模型训练/部署、节省计划及成本管控等核心能力。其设计目标是为不同规模和场景的模型应用提供灵活、可预测、可追溯的成本控制机制，所有计费项均以 [Token](../concepts/token.md)、TPM（[Token](../concepts/token.md)s Per Minute）或训练步数为计量基础，并严格区分地域、模型版本与调用方式。开发者需重点关注免费额度的地域限制、抵扣优先级顺序及预算/限额的生效边界，避免因配置偏差导致意外扣费或服务中断。

## 支持的模型/功能

- **实时推理**：支持千问（Qwen）系列（如 `qwen3.8-max`、`qwen-plus`）、DeepSeek、GLM、Kimi 等主流大语言模型，以及千问VL、万相（WanX）、CosyVoice 等[多模态](../concepts/multimodal.md)与语音模型，覆盖文本生成、图像/视频生成、语音合成与识别等能力 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **批量调用（Batch）**：支持 OpenAI 兼容的 Batch 接口，但其输入/输出 [Token](../concepts/token.md) 单价为实时推理价格的 50%，且**不支持用新人免费额度抵扣** [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。
- **模型训练与部署**：支持文本、图像、视频、语音四类模型的微调（Fine-tuning），以及 PTU（预置吞吐）、DTU（模型单元）等多种部署模式，计费独立于推理 [原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **上下文缓存**：部分模型（如 `qwen3.8-max`）支持显式/隐式缓存，命中时输入 Token 按折扣单价计费（如 10%），创建缓存则按更高单价（如 125%）计费，该能力不影响免费额度使用 [原文标题](../../raw/model-user-guide/model-experience/text-generation-model/context-cache.md)。

> **注意**：文档 2 中 `qwen3.8-max-prime` 明确标注“无免费额度”，而文档 1 中“适用范围”强调免费额度仅限实时推理，且文档 3 明确指出模型训练、部署费用**不支持用免费额度抵扣**。三者逻辑一致，但文档 2 的表格未对 `qwen3.8-max-prime` 补充说明其是否属于实时推理范畴，易引发歧义；实际应以文档 1 的定义为准——只要调用方式为实时 API 调用，即属免费额度适用范围，`qwen3.8-max-prime` 作为实时推理模型，其额度状态应为“有”而非“无”，此处存在表述矛盾，建议以控制台实际显示为准。

## 关键参数

- **Token 计量**：输入/输出 Token 均按实际消耗计费，免费额度、按量付费、节省计划均基于此单位。长输入（如 >32K）可能触发阶梯系数（如 `qwen3.7-flash` 的 3x/6x 折算）或缓存折算（如 `glm-5.2` 缓存命中部分按 0.25 系数折算）[原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **TPM 容量**：吞吐预留（TPU）以 kTPM（1,000 Tokens/分钟）为购买单位，输入起步 200 kTPM、输出起步 20 kTPM；高速模式（PTU）提供 1.5~2 倍 TPS 提升，但单价显著高于标准模式 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **地域绑定**：免费额度、节省计划、模型价格均严格按地域隔离。例如，华北2（北京）地域的免费额度仅适用于该地域模型；在美国（弗吉尼亚）购买的 AI 通用型节省计划，**仅抵扣该地域产生的费用** [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **抵扣优先级**：系统自动按固定顺序抵扣费用：**免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费**。开启“免费额度用完即停”后，额度耗尽将直接返回 403 错误，此时节省计划无法生效，必须手动关闭该开关才能切换至后续抵扣层 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 使用方式

- **开通与初始化**：首次开通百炼即自动发放免费额度（华北2 地域），无需实名认证即可使用；额度通常两小时内生效，控制台模型广场或免费额度页面可查看余量 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **API 调用**：使用通用 API Key（非 Token Plan 专属 Key）调用标准 Base URL，系统自动按优先级抵扣额度；若需使用免费额度，**不可使用 Token Plan 专属 API Key** [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **吞吐预留**：创建后生成专属模型 Code（需替换请求中的 `model` 参数），调用该 Code 即走预留通道；容量换算受长输入阶梯系数与缓存命中率影响，需在控制台确认模型具体参数 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **成本管控**：
  - 设置**预算管理**：按账号/业务空间/API Key 粒度设置月度预算，开启“达到预算后立即停止”可自动限制按量调用（返回 429 错误）[原文标题](../../raw/model-user-guide/test-1/budget-management.md)；
  - 配置**高额消费预警**：在费用中心设置阈值，达阈值时短信/邮件提醒，防止余额快速耗尽 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)；
  - 启用**免费额度用完即停**：避免额度耗尽后自动转为按量付费产生欠费，但生产环境不建议开启，以免服务不可用 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 限制和注意事项

- **免费额度限制**：仅华北2（北京）地域有效；有效期 90 天（以开通/模型发布/申请通过之日较晚者起算）；不同模型（含快照版本如 `qwen3.8-max-2026-05-17`）额度独立不互通；ASR 类模型需在业务空间单独开通权限方可消耗额度 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **地域与模型隔离**：模型价格、节省计划、免费额度均不跨地域共享；同一模型在不同地域（如北京 vs 新加坡）价格差异显著（如 `qwen3.8-max` 输入单价北京 ¥12/百万Token，新加坡 ¥14.988/百万Token）；控制台显示“无免费额度”可能因地域不匹配或模型本身不参与活动 [原文标题](../../raw/model-user-guide/test-1/model-pricing.md)。
- **服务中断风险**：
  - 开启“免费额度用完即停”或“预算用尽即停”后，服务将返回 HTTP 403 或 429 错误，**不会自动恢复**，需手动调整配置；
  - 模型部署（PTU/DTU）按使用时长计费，即使无 API 调用，只要状态为“运行中”即持续扣费；
  - 账户欠费时，按商品 Code 隔离限制服务，某商品（如“百炼容量预留”）欠费不影响其他商品（如“百炼大模型推理”）调用，但需结清对应欠费才能恢复 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **账单延迟与排查**：模型推理账单出账延迟 2~10 分钟，批量/训练类任务延迟更长；费用归属需通过账单详情页的“实例 ID（出账粒度）”字段解析（格式为 `ApiKeyID;业务空间ID;模型名称;...`），而非仅看“计费项”名称 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [预算管理](../../raw/model-user-guide/test-1/budget-management.md)


