# test 1

`test 1` 是阿里云百炼平台面向开发者提供的核心计费与资源管理主题，涵盖模型调用、训练、部署及成本优化的全链路规则。本文档整合免费额度发放逻辑、按量/预留/预置吞吐等多维计费模式、节省计划抵扣策略及账单溯源方法，帮助开发者准确预估成本、规避意外扣费，并实现精细化用量管控。所有规则均以华北2（北京）地域为默认基准，跨地域部署需单独配置。

## 支持的模型/功能

- **实时推理**：支持千问（Qwen3.8-Max、Qwen3.7-Plus 等）、DeepSeek、GLM、Kimi 等主流文本生成模型，以及 Qwen-VL、WanX（万相）、CosyVoice 等多模态与语音模型。[新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)明确说明，免费额度仅覆盖**华北2（北京）地域的实时推理调用**，Batch 调用、模型调优、模型部署等均不适用。
- **模型训练**：支持文本生成（千问系列）、图像生成（万相、千问图像）、视频生成（万相图生视频）、语音合成（CosyVoice）四类训练任务，计费基于训练 Token 总量或等效计算量（如视频时长×像素系数）。[模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)详细列出了各模型的训练单价与公式。
- **模型部署**：提供两种计费模式：  
  - **按使用时长计费（PTU）**：以预置吞吐（PTU）为单位，分“标准”与“独占”规格，支持输入/输出 TPM 分离计价；  
  - **吞吐预留（TPM Reservation）**：预付费购买专属推理吞吐量，支持标准/高速模式，容量内调用不额外收费，超出部分按溢出策略处理。[吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)文档定义了其容量换算规则（含长输入阶梯系数与缓存折算）及生命周期管理。

> **注意**：文档 2 与文档 3 对“模型部署”的定义存在差异。文档 2 将 PTU 部署归类为“模型部署计费”，而文档 3 的“吞吐预留”虽功能相似（均为预留资源），但被单独列为一类计费项。实际使用中，二者属并列选项，非包含关系，开发者需根据 SLA（如是否需要独占资源、是否要求高速 TPS）选择。

## 关键参数

- **Token 计费粒度**：所有按量计费（推理、训练）均以 Token 为最小单位。输入/输出 Token 分开统计，且部分模型（如 qwen3.6-max-preview）实行阶梯计费——单次请求的全部 Token 均按最高输入 Token 区间单价结算。[模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)文档提供了各模型在不同地域的详细单价表。
- **TPM/TPU 容量单位**：  
  - `kTPM = 1,000 Tokens/分钟`，为吞吐预留的购买单位；  
  - `TPU`（预置吞吐单元）是 PTU 部署的计量单位，其输入/输出 TPM 容量需在创建时指定，超出部分触发溢出策略。  
- **免费额度参数**：每个模型独立享有 100 万 Token 免费额度（如 `qwen3.8-max` 与 `qwen3.8-max-2026-05-17` 视为不同模型），有效期 90 天（自开通/模型发布/申请通过日起算，以较晚者为准）。额度为输入+输出 Token 共用总额度，不区分类型 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 使用方式

1. **开通与初始化**：首次开通百炼后，系统自动发放华北2（北京）地域各模型的免费额度，无需实名认证即可使用。API Key 通用，无需为免费额度单独创建 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
2. **调用与计费**：  
   - 实时推理调用自动按优先级抵扣：`免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费`；  
   - 若开启“免费额度用完即停”，额度耗尽将返回 `403 AllocationQuota.FreeTierOnly` 错误，服务中断；关闭该开关后，自动切换至后续抵扣项或按量付费 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。  
3. **成本优化选型**：  
   - **长期稳定使用**：首选 [AI 通用型节省计划](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)，承诺月消费换取阶梯折扣（最高 5.3 折），覆盖绝大部分阿里直供模型；  
   - **小规模/单模型集中使用**：可选资源包（一次性购买固定 Token 量）或其他模型节省计划；  
   - **高并发/低延迟场景**：选用吞吐预留（TPM Reservation）或 PTU 部署，确保确定性性能。

## 限制和注意事项

- **地域限制**：免费额度、大部分模型训练及部署服务仅在华北2（北京）地域可用；美国、新加坡等地域模型无免费额度，且调用单价更高 [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)。
- **额度与服务状态强耦合**：账户欠费时，即使模型仍有免费额度或节省计划剩余额度，**所有按量付费相关服务（包括推理、训练、部署）均会暂停**。必须结清欠费才能恢复 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **账单延迟与溯源**：模型推理账单为分钟级出账（通常 2~10 分钟），训练/批量推理为小时级。费用归属需通过账单中 `实例 ID（出账粒度）` 字段解析，其格式为 `ApiKeyID;业务空间ID;模型名称;输入/输出类型;调用渠道;免费额度用完即停标识`，是定位费用来源的唯一可靠依据 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **模型版本隔离**：带日期后缀的快照版本（如 `qwen3.7-plus-2026-05-26`）与不带后缀的最新版（如 `qwen3.7-plus`）视为独立模型，免费额度、资源包、节省计划均不互通 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)


