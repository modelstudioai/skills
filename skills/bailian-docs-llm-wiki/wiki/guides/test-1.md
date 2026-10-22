# test 1

阿里云百炼平台的 `test 1` 是面向开发者的核心计费与资源管理能力集合，涵盖模型调用、吞吐预留、训练部署、账单控制及成本优化等全链路场景。其设计目标是提供细粒度、可预测、可管控的模型服务使用体验，支持从免费试用到大规模生产部署的平滑演进。所有能力均基于统一的 Token/TPM 计量体系，并严格遵循地域隔离、模型独立、额度不互通等基本原则。

## 支持的模型/功能

`test 1` 覆盖百炼平台主流模型服务，包括文本生成（千问 Max/Plus/Flash 系列）、多模态（千问 VL、万相图像/视频）、语音（CosyVoice、Qwen-TTS/ASR）及向量/排序模型等。核心功能分为三类：

- **实时推理**：支持标准 API 调用、Batch 批量接口（[Batch调用](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)）、Function Calling 等，是免费额度唯一适用的场景。
- **吞吐预留（PTU）**：提供标准模式（TPS 与标准 API 一致）和高速模式（TPS 提升 1.5~2 倍），适用于高并发、低延迟确定性要求的生产环境 [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **模型训练与部署**：支持文本、图像、视频、语音四类模型的微调训练（[模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)），以及训练后模型的专属部署（PTU 或 DTU 模式）。

> **注意**：文档 3 和文档 4 中对 `qwen3.7-max` 的能力描述存在矛盾。文档 3 称其“当前能力等同于 `qwen3.7-max-2026-05-20`”，而文档 4 在训练价格表中将其列为独立模型且未注明等效关系。实际使用时请以控制台模型广场最新快照版本为准，避免因版本别名导致计费或功能偏差。

## 关键参数

- **Token 计量**：所有按量计费模型（推理、训练）均以输入/输出 Token 为基本单位。长输入（如 >32K）按阶梯系数折算（[模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)），缓存命中部分按独立折扣单价计费。
- **TPM 容量**：吞吐预留以 kTPM（1,000 Tokens/分钟）为购买单位，输入/输出容量独立配置，起步分别为 200kTPM 和 20kTPM [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。
- **地域绑定**：免费额度、节省计划、PTU 预留均严格绑定地域（如华北2北京），跨地域调用不共享额度或折扣 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **模型独立性**：同一模型的不同快照（如 `qwen3.8-max` 与 `qwen3.8-max-2026-05-17`）拥有完全独立的免费额度、PTU 实例和训练费用，不可互通 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 使用方式

1. **开通与初始化**：首次开通百炼即自动获得华北2（北京）地域各模型的新人免费额度（100万 Token/模型），无需实名认证即可使用 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
2. **调用接入**：使用通用 API Key 和对应地域 Base URL 发起请求，系统自动按优先级抵扣：免费额度 → 节省计划 → 资源包 → 按量付费 [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
3. **成本管控**：
   - 设置月度预算（仅限 API 推理费用），开启「达到预算后立即停止」可自动返回 429 错误 [预算管理](../../raw/model-user-guide/test-1/budget-management.md)。
   - 开启「免费额度用完即停」开关，额度耗尽时返回 `AllocationQuota.FreeTierOnly` 错误，防止意外扣费 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
4. **账单溯源**：通过账单详情页的 `资产/资源实例ID（出账粒度）` 字段（格式为 `ApiKeyID;业务空间ID;模型名称;...`）精确定位每笔费用的来源 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。

## 限制和注意事项

- **免费额度限制**：仅抵扣实时推理费用；Batch 调用、模型训练、部署、知识库 RAG、联网搜索等均不支持 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **额度时效性**：免费额度有效期为 90 天（自开通/模型发布/申请通过日起算，以较晚者为准），过期自动作废，不延期、不补发 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **欠费隔离**：账户欠费按商品 Code 隔离。例如，“百炼容量预留”欠费会导致 PTU 服务不可用，但不影响“百炼大模型推理”的免费额度使用 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **PTU 溢出行为**：当 PTU 容量不足时，若选择「自动溢出」策略，调用将切换至按量付费，Header 中会返回 `x-dashscope-ptu-overflow:true`；若选择「仅使用 PTU 容量」，则直接返回 HTTP 429 错误 [模型部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。
- **预算管理范围**：预算功能仅覆盖 API 按调用量付费，明确不包含模型训练、PTU、DTU、知识库规格等费用 [预算管理](../../raw/model-user-guide/test-1/budget-management.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [预算管理](../../raw/model-user-guide/test-1/budget-management.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)


