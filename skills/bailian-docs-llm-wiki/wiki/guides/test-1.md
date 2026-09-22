# test 1

`test 1` 是阿里云百炼平台面向开发者提供的模型服务统一标识，涵盖模型调用、训练、部署及配套计费与成本管理能力。其核心能力围绕实时推理（支持多种模型与参数配置）、模型调优、专属部署三大场景展开，并通过免费额度、节省计划、吞吐预留等多种计费模式满足不同规模与稳定性的使用需求。所有服务均以 API 为统一接入方式，地域隔离明确，计费逻辑严格区分输入/输出 [Token](../concepts/token.md)、TPM 容量、训练步数等维度。

## 支持的模型/功能

`test 1` 所指代的服务体系支持以下主流模型系列及其关键能力：

- **文本生成模型**：千问系列（`qwen3.8-max`、`qwen3.7-plus` 等）、DeepSeek、GLM、Kimi 等，覆盖非思考/思考双模式，支持长上下文（最高 1M [Token](../concepts/token.md)）与思维链推理。
- **多模态模型**：千问VL（`qwen3-vl-8b-instruct`）、万相（`wan2.7-image-pro`）、Qwen-Image 等，支持图文理解、文生图、图生图等任务。
- **语音模型**：CosyVoice（`cosyvoice-v3-plus`）、Qwen-TTS、Paraformer、Fun-ASR 等，覆盖语音合成与识别全链路。
- **视频模型**：万相图生视频（`wan2.7-i2v`）等。
- **核心功能**：实时推理、Batch 调用（[Batch调用](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)）、上下文缓存、Function Calling、网页抓取等原生工具调用，以及模型调优（[模型调优](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)）与[模型部署](../concepts/model-deployment.md)（[模型部署](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)）。

> **注意**：文档中 `qwen3.6-max-preview` 在“模型调用价格”文档中被列为 A 类模型（支持 AI 通用型节省计划抵扣），但在“节省计划与资源包”文档中明确说明 C 类模型包含 `qwen3.6-max-preview` 且仅阿里直供版本支持抵扣。该矛盾需以控制台实际模型广场展示为准，建议调用前在控制台确认模型所属类别。

## 关键参数

调用与计费依赖以下关键参数，需在请求或配置中显式指定：

- **`model`**：模型唯一标识（如 `qwen3.8-max`），决定计费单价、免费额度归属及功能支持。带日期后缀的快照版本（如 `qwen3.8-max-2026-05-17`）与不带后缀的最新版视为独立模型，额度与计费规则互不共享 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。
- **`input_tokens` / `output_tokens`**：计费基础单位，按实际消耗 [Token](../concepts/token.md) 数结算。输入 Token 包含提示词与历史上下文；输出 Token 为模型生成内容长度。
- **`max_tokens`**：控制输出长度上限，影响输出 Token 实际消耗。
- **`temperature` / `top_p`**：影响输出随机性与多样性，不直接影响计费。
- **`enable_search`**：启用联网搜索插件时，将产生独立于模型推理的额外计费，需单独关注 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **`cache_enabled`**：开启上下文缓存后，命中部分 Token 按折扣单价计费（如 10%），创建缓存按更高单价（如 125%）计费，详见 [上下文缓存](../../raw/model-user-guide/model-experience/text-generation-model/context-cache.md) 文档。

## 使用方式

### 1. 基础调用
通过标准 REST API 发起请求，需提供：
- 正确的 Base URL（地域相关，如华北2为 `https://dashscope.aliyuncs.com/compatible-mode/v1`）；
- 有效的 API Key（通用 Key 才能消耗免费额度，[Token Plan 专属 Key 不适用](../../raw/model-user-guide/test-1/new-free-quota.md)）；
- `model` 参数与符合要求的 `messages` 或 `prompt`。

### 2. 免费额度使用
首次开通百炼即自动发放，仅限华北2（北京）地域模型。系统按优先级自动抵扣：免费额度 > 资源包 > 节省计划 > 按量付费。未认证用户额度用尽后服务中断；已认证用户可选择开启“免费额度用完即停”防止意外扣费 [原文标题](../../raw/model-user-guide/test-1/new-free-quota.md)。

### 3. 成本优化方案
- **节省计划**：承诺月消费金额换取阶梯折扣（最高 5.3 折），覆盖绝大部分阿里直供模型，推荐长期稳定使用场景 [原文标题](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)。
- **吞吐预留（TPM）**：预购确定性推理容量，分标准/高速模式，支持按天、按小时或 8 小时时段购买，适用于高并发、低延迟场景。
- **预算管理**：为账号、业务空间或 API Key 设置月度费用上限，可选达预算后自动停止调用（生产环境慎用）。

## 限制和注意事项

- **地域限制**：新人免费额度、部分模型训练（如 CosyVoice）仅支持华北2（北京）地域；其他地域（如美国、新加坡）模型无免费额度，且价格与计费规则独立。
- **免费额度限制**：仅抵扣实时推理费用，[Batch调用](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)、模型调优、[模型部署](../concepts/model-deployment.md)、知识库向量计算等均不支持抵扣。
- **账户状态影响**：账户欠费时，即使模型仍有免费额度或节省计划剩余额度，所有按量付费服务（包括推理）将暂停，必须结清欠费后恢复。
- **出账延迟**：模型推理账单通常延迟 2~10 分钟生成，批量推理、训练等为小时级出账，账单查询需等待对应延迟 [原文标题](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)。
- **API Key 管理**：删除 API Key 是立即停止计费的最有效手段，适用于紧急止血场景；但需同步更新所有调用方配置，否则将导致服务中断。

## 来源文档

- [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)
- [模型调用价格](../../raw/model-user-guide/test-1/model-pricing.md)
- [模型训练与部署计费](../../raw/model-user-guide/test-1/model-training-and-deployment-billing.md)
- [节省计划与资源包](../../raw/model-user-guide/test-1/savings-plan-and-resource-package.md)
- [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)
- [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md)
- [预算管理](../../raw/model-user-guide/test-1/budget-management.md)


