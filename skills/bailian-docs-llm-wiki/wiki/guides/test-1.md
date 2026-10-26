# test 1

阿里云百炼平台的 `test 1` 是面向开发者的核心计费与资源管理主题，涵盖模型调用、训练、部署及成本控制等关键环节。本文档整合官方技术文档，明确免费额度适用范围、各场景计费逻辑、参数配置要点及关键限制，帮助开发者快速建立成本意识并规避意外扣费风险。所有信息均基于当前平台策略，具体以控制台实时展示为准。

## 支持的模型/功能

`test 1` 覆盖百炼平台主流模型服务，包括文本生成（千问系列如 `qwen3.8-max`、`qwen-plus`）、多模态（千问VL、万相图像/视频）、语音（CosyVoice、Qwen-ASR/TTS）及第三方模型（DeepSeek、GLM、Kimi）。  
- **实时推理**：支持标准 API 调用、Batch 接口（兼容 OpenAI）、Assistant API、Responses API 等多种渠道，但 [Batch调用](raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md) 不享受新人免费额度抵扣 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。  
- **模型训练**：支持文本生成、图像生成、视频生成、语音合成四类调优任务，计费按训练 [Token](../concepts/token.md) 总量计算，公式因模型类型而异（如万相图像训练依赖 `max_steps × Lstep`，千问图像训练依赖 `n_epochs × N × (max_pixels/压缩率) × GPU系数`）[原文标题](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)。  
- **模型部署**：提供预置吞吐（PTU）、模型单元（DTU）等部署模式，其中 PTU 分标准/高速模式，支持长输入阶梯系数与缓存折算 [原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。  
- **知识库（RAG）**：向量模型（Embedding）和排序模型（Rerank）调用费用属于 `test 1` 范围，可被 AI 通用型节省计划抵扣；但知识库规格费用（如运行时长）不在此列 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。

> **注意**：文档 2 与文档 3 对 `qwen3.7-plus` 的价格描述存在矛盾。文档 2（模型训练与部署计费）中该模型未列出训练单价；文档 3（模型调用价格）则明确其在华北2（北京）地域的推理单价为输入 2 元/百万 [Token](../concepts/token.md)（≤256K）、输出 8 元/百万 [Token](../concepts/token.md)（思考模式）。此处以文档 3 的推理价格为准，训练价格需以控制台实际创建任务时的预估为准。

## 关键参数

- **Token 计量**：输入/输出 Token 统一计入免费额度总额度（如 `qwen-max` 为 100 万 Token），不区分输入或输出 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。  
- **TPM 容量**：吞吐预留（PTU）购买单位为 kTPM（千 Tokens/分钟），输入按万 TPM 报价、输出按千 TPM 报价；容量换算需考虑长输入阶梯系数（如 `qwen3.7-flash` 输入 >32K 部分系数为 3x）和缓存折算系数（如 `glm-5.2` 为 0.25）[原文标题](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)。  
- **地域绑定**：免费额度、节省计划、吞吐预留均严格按地域隔离。例如，华北2（北京）购买的节省计划仅抵扣该地域产生的推理费用，跨地域调用需单独购买 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。  
- **有效期**：新人免费额度有效期为 90 天（自开通/模型发布/申请通过日起较晚者为准），到期自动失效且不支持补发；而节省计划按“动态月”周期分配额度（如 3 个月计划每月独立获得 1000 元额度，当月未用完清零）[原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 使用方式

1. **启用免费额度**：首次开通百炼后系统自动发放，无需认证即可使用。需确保调用地域为华北2（北京），并使用通用 API Key（非 Token Plan 专属 Key）[原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。  
2. **调用模型**：通过标准 API（如 `/v1/chat/completions`）发起请求，`model` 参数指定模型 Code（如 `qwen3.8-max`），系统自动按优先级抵扣：免费额度 > 资源包 > 节省计划 > 按量付费 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。  
3. **购买节省计划**：推荐选用 [AI 通用型节省计划](https://common-buy.aliyun.com/?commodityCode=sfm_GenAI_spn_cn)，承诺月消费金额后享受阶梯折扣（最高 5.3 折），覆盖绝大部分阿里直供模型，购买后自动生效 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。  
4. **设置预算**：在控制台 **费用用量 > 预算管理** 页面，可为账号、业务空间或单个 API Key 设置月度预算，并开启「达到预算后立即停止」以自动限制调用（生产环境慎用）[原文标题](../../raw/model-user-guide/test-1/budget-management.md)。

## 限制和注意事项

- **免费额度限制**：仅抵扣实时推理费用，不支持 Batch 调用、模型训练、模型部署、PAI-DSW、OSS 存储等 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。  
- **欠费隔离**：账户欠费按商品 Code 隔离。例如，“百炼大模型部署”欠费将导致部署服务不可用，但不影响“百炼大模型推理”的调用（只要该商品 Code 未欠费）[原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。  
- **出账延迟**：模型推理账单通常在调用结束 2–10 分钟后生成，批量推理、训练等为小时级出账。因此，控制台显示“剩余额度充足”时，若实际已耗尽，仍可能因出账延迟产生费用 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。  
- **API Key 安全**：删除 API Key 是最直接的停止计费方式。若怀疑账户被盗用，应立即核查账单中的 `ApiKeyID` 字段并删除异常 Key [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。  
- **模型快照独立性**：带日期后缀的模型快照（如 `qwen3.7-max-2026-05-20`）与不带后缀的最新版（如 `qwen3.7-max`）视为两个独立模型，各自拥有 100 万 Token 免费额度，不互通、不共享 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [预算管理](../../raw/model-user-guide/test-1/budget-management.md)


