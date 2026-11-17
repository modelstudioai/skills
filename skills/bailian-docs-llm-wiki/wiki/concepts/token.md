# Token

Token 是百炼平台中用于计量模型计算资源消耗与计费的核心单位，表示模型在处理文本（输入/输出）、训练、缓存、吞吐等场景中所消耗的最小语义单元。它既反映模型实际计算负载，也是用量统计、成本核算、性能监控与配额控制的统一粒度。

## 在百炼平台的不同场景中，这个概念如何使用

- **实时推理调用**：每次 API 请求的 `prompt`（输入）和 `response`（输出）均被切分为 Token，按实际数量计费。例如调用 `qwen-max` 时，1000 字中文约消耗 1300–1500 Token（取决于分词器），输出长度由 `max_tokens` 参数显式限制。
- **批量推理（Batch）**：按总输入 + 总输出 Token 数计费，单价为实时推理的 50%，适用于离线批量生成任务。
- **模型训练（Fine-tuning）**：以“每千 Token”为单位计费，费用基于训练数据集的全部输入 Token 总量（含 [prompt](../guides/prompt.md) + label）计算。
- **上下文缓存（Context Cache）**：首次缓存长 Prompt 按标准单价计费；后续命中时，仅对缓存部分按折扣单价（如 0.5 元/百万 Token）计费，显著降低高频复用场景成本。
- **吞吐预留（TPM Reservation）**：以“kTPM”（千 Tokens/分钟）为单位购买预置吞吐能力，实际消耗按请求 Token 数 × 阶梯系数（如长输入 >32K 部分×3）动态折算。
- **用量监控与告警**：`TotalToken 数` 是核心监控指标，支持按模型/API Key/地域等维度聚合，可用于配置成本突增告警（如“单模型日 Token 消耗超 500 万”）。
- **模型评测**：评测任务中每条样本的单次推理消耗 Token 计入费用；若启用 `Pass@K`（K>1），则 Token 消耗与 K 值成正比。

## 关键参数和配置

- `max_tokens`（API 参数）：**强烈建议生产环境必设**。限制模型最大输出长度，直接控制 Token 消耗上限与响应成本，避免意外长输出导致费用激增。
- `top_p` / `temperature`（采样参数）：虽不直接影响 Token 数量，但影响输出确定性；高随机性可能增加重试概率，间接推高 Token 总用量。
- 缓存相关参数（如 `cache_prompt`）：显式启用缓存可复用已编码的输入 Token，降低重复请求的 Token 成本，但首次缓存仍按全量计费。
- 计费单位统一：  
  - 实时/批量推理、监控用量 → **每百万 Token（1,000,000 tokens）**  
  - 模型训练 → **每千 Token（1,000 tokens）**  
  - 吞吐预留 → **kTPM（1,000 tokens/minute）**

## 面向开发者，简洁实用

- ✅ **务必设置 `max_tokens`**：防止模型无约束生成，是成本可控的第一道防线。  
- ✅ **善用缓存**：对固定系统提示词（system [prompt](../guides/prompt.md)）或高频模板启用 `cache_prompt`，长期可降本 30%+。  
- ✅ **监控 `TotalToken 数`**：在[模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)中配置告警，及时发现异常调用或 Prompt 泄露风险。  
- ✅ **免费额度优先消耗**：华北2（北京）地域新人自动获得 100 万 Token 免费额度，仅限实时推理，调用即自动抵扣。  
- ❌ **避免硬编码敏感参数**：`api_key` 等凭证不得写死在代码中，应通过环境变量或密钥管理服务注入。  
- ⚠️ **注意地域差异**：免费额度、阶梯定价、基线评测等功能仅限北京地域；其他地域（如新加坡、美国）无免费额度且单价上浮。  

Token 不是抽象概念，而是你每一次 `Generation.call()`、每一次 `EvaluationTask.run()`、每一笔账单背后真实流动的计算价值——精确认知并主动管理它，是高效、稳定、低成本使用百炼平台的关键。

## 关联主题页

- [preparations](../api/preparations.md)
- [test 1](../guides/test-1.md)
- [model monitoring](../guides/model-monitoring.md)
- [model evaluation introduction](../guides/model-evaluation-introduction.md)
- [billing api](../api/billing-api.md)


