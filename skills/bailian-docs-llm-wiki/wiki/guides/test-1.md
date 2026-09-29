# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与资源管理主题，涵盖模型调用、训练、部署及成本控制的全链路规则。本文档整合了免费额度发放、按量计费、吞吐预留、节省计划、预算管理及账单溯源等关键机制，帮助开发者准确预估成本、规避意外扣费，并实现精细化用量管控。所有计费行为均以实际出账为准，且受地域、模型版本、调用方式（如 Batch/实时）等多维度影响。

## 支持的模型/功能

- **支持模型**：覆盖千问（Qwen3.x 系列 Max/Plus/Flash）、DeepSeek、GLM、Kimi、万相（Wan2.x 图像/视频）、CosyVoice 语音等主流模型，以及 Qwen-VL、Qwen-OCR 等多模态模型。具体支持列表请参考 [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md) 文档中各地域的模型 ID 表格。
- **核心功能**：
  - 实时推理（含上下文缓存、Function Calling、网页抓取等原生工具）
  - Batch 批量调用（兼容 OpenAI 接口）
  - 模型调优（Fine-tuning）与模型部署（PTU/DTU）
  - 吞吐预留（TPM 预留，含标准/高速模式）
  - 知识库（RAG）向量与排序模型调用（Embedding/Rerank）

> **注意**：文档 1 明确指出，[Batch调用](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)、[模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md) 和 [模型部署](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md) 均**不支持抵扣新人免费额度**；而文档 6 则说明 AI 通用型节省计划**支持抵扣 Batch 调用费用**，但**不支持抵扣模型调优与部署费用**。二者在“Batch 调用是否可被免费额度覆盖”上无矛盾（均不可），但在“是否可被节省计划覆盖”上存在隐含差异——文档 6 的抵扣范围描述更全面，应以此为准。

## 关键参数

- **Token 计量**：输入/输出 Token 分开统计，缓存命中部分按独立单价计费（如显式缓存创建为标准输入价的 125%，命中为 10%）；长输入按阶梯系数折算（如 `qwen3.7-flash-2026-07-15` 在 (32K,256K] 区间系数为 3x）[吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **地域约束**：免费额度**仅华北2（北京）地域有效**；节省计划、模型部署、吞吐预留均按地域独立购买与抵扣，跨地域调用不共享额度。
- **模型版本标识**：带日期后缀的快照版本（如 `qwen3.8-max-2026-05-17`）与无后缀最新版（如 `qwen3.8-max`）视为**完全独立模型**，各自拥有独立免费额度、独立计费项与独立部署实例。
- **调用渠道标识**：账单中 `实例 ID（出账粒度）` 字段以分号 `;` 分隔，格式为 `ApiKeyID;业务空间ID;模型名称;输入/输出类型;调用渠道;免费额度用完即停标识`，其中 `调用渠道` 可为 `app`（代码调用）、`bmp`（控制台体验中心）或 `assistant-api`（Assistant API）[账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 使用方式

- **免费额度**：首次开通百炼后自动发放，无需实名认证即可使用；调用时系统自动优先抵扣，无需修改 API Key 或请求参数。需确保使用**通用 API Key**（非 Token Plan/Coding Plan 专属 Key），否则不生效 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **按量付费**：默认模式，直接调用模型 API 即可，费用从账户余额扣除。需注意：若开启「免费额度用完即停」，额度耗尽后将返回 HTTP 403 错误（错误码 `AllocationQuota.FreeTierOnly`），而非自动转为按量付费。
- **吞吐预留（TPM）**：创建后生成专属 `model` 参数（如 `qwen3.8-max-tpu-xxxx`），调用时需显式替换请求中的 `model` 字段；预留容量内调用不额外计费，溢出部分按「自动溢出」策略切换为按量付费，并在响应 Header 中返回 `x-dashscope-ptu-overflow:true`。
- **节省计划**：购买后自动生效，抵扣顺序为 `免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费`；若已开启「免费额度用完即停」，则节省计划无法触发抵扣，需手动关闭该开关 [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **预算管理**：在控制台设置账号/业务空间/API Key 粒度的月度预算，开启「达到预算后立即停止」可使超支调用返回 HTTP 429 错误；但该功能**不适用于美国（弗吉尼亚）地域，且 PTU 溢出部分与应用调用暂不支持自动停止** [预算管理](../../raw/model-user-guide/test-1/budget-management.md)。

## 限制和注意事项

- **免费额度限制**：有效期严格为 90 天（以开通/模型发布/申请通过三者中最晚时间起算），到期自动作废，不延期、不补发；主账号与 RAM 子账号**共享额度**，但不同模型间额度**完全隔离**。
- **计费延迟与出账**：模型推理账单为**分钟级出账（通常 2~10 分钟）**，非实时扣款；批量推理、训练、知识库为小时级出账。因此，调用后立即查不到账单属正常现象，需等待出账延迟 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **欠费影响**：账户可用额度 < 0 时，**即使仍有免费额度、节省计划或资源包剩余额度，所有按量付费类服务（包括实时推理）将全部暂停**；仅 Coding Plan/Token Plan 等独立订阅套餐不受影响。
- **模型部署持续计费**：模型一旦部署成功并处于「运行中」状态，即开始按使用时长计费，**与是否发生 API 调用无关**。若不再使用，必须主动下线部署实例，否则费用将持续产生 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **API Key 安全**：删除 API Key 是最直接的「停止计费」手段，可立即阻断所有通过该 Key 的调用；但删除后无法恢复，需谨慎操作。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [预算管理](../../raw/model-user-guide/test-1/budget-management.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)


