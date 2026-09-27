# Token

Token 是百炼平台中用于度量模型计算资源消耗的最小计量单位，代表模型在处理文本、图像、音频等输入输出时所消耗的语义单元（如子词、字节对、视觉 patch 等）。它既是计费与配额控制的核心依据，也是性能监控、用量分析和成本优化的基础指标。

## 在百炼平台的不同场景中，这个概念如何使用

- **计费与配额控制（Token Plan）**：所有支持 Token Plan 的模型（如 `qwen-turbo`、`text-embedding-v3`、`bge-reranker-v2-m3`）均按实际消耗的 Token 数计费。调用时需显式指定 `plan` 参数（如 `"personal"`），其配额上限（如日总 Token 限额、单次 `max_tokens`）直接约束模型响应长度与调用频次。多模态模型（如 `qwen-vl-plus`）暂不纳入 Token Plan，仍按请求次数计费。

- **模型监控与用量统计**：监控系统中的 `TotalToken 数` 指标即为该模型在选定时间范围内所有成功请求的输入 Token 与输出 Token 之和。该数据延迟约 1 小时，用于成本归因、API-Key 级用量审计及告警（如“单日 TotalToken 超阈值”），但**不作为最终计费凭证**——费用中心账单为准。

- **向量与排序服务（Embedding / Rerank）**：文本[向量化](embedding.md)（如 `text-embedding-v4`）按输入文本的 Token 数计费；Rerank 服务（如 `qwen3-rerank`）则按 Query + 所有 Document 的总 Token 数计费。批处理接口（如异步 Embedding）同样以原始文本 Token 总量为计费基准，与是否压缩、编码格式（`float`/`base64`）无关。

- **生成类模型（LLM / Multimodal）**：`input.tokens` 和 `output.tokens` 分别记录 Prompt 与响应的 Token 消耗，可在审计日志中查看（不含内容本身）。流式响应中，`output.tokens` 为最终累计值。`max_tokens` 参数限制的是模型最多生成的 Token 数，受当前 Token Plan 配额硬性约束。

- **RAG 与缓存场景**：显式缓存（`cache_control`）可显著降低重复 Prompt 的 Token 消耗（降幅达 90%），因其跳过模型推理，直接返回缓存向量或响应——此时仅产生极小的元数据 Token 开销，不计入主计费流水。

## 关键参数和配置

| 参数名 | 所属场景 | 说明 | 是否影响 Token 计费 |
|--------|----------|------|---------------------|
| `max_tokens` | 所有生成类 API | 单次响应最大生成 Token 数，受 Token Plan 配额限制；设为 0 或省略时由模型自动决定上限 | ✅ 是（上限约束） |
| `plan` | Token Plan | Plan 标识符（如 `"team"`），决定本次调用的 Token 配额池与计费规则 | ✅ 是（绑定计费主体） |
| `input.tokens` / `output.tokens` | 审计日志、监控指标 | 响应头或日志中返回的实际消耗 Token 数，用于调试与用量分析 | ——（只读，非配置项） |
| `dimensions` | Embedding API | 向量维度（如 `1024`），**不影响 Token 消耗**，仅改变向量大小与存储开销 | ❌ 否 |
| `encoding_format: base64` | Embedding API | 输出编码方式，**不改变 Token 计费逻辑**，仅影响传输体积 | ❌ 否 |

> ⚠️ 注意：Token 计费基于原始输入文本（含 system [prompt](../guides/prompt.md)、messages、[prompt](../guides/prompt.md) 字段等）与模型实际输出的完整 tokenization 结果，与 `stream`、`temperature`、`top_p` 等采样参数无关；也与是否启用缓存、日志投递、监控告警等平台功能无关。

## 面向开发者，简洁实用

- **查用量**：登录控制台 → **费用与成本 > 模型用量**，按模型、API-Key、时间粒度（天/小时/分钟）查看 `TotalToken` 统计。
- **控成本**：
  - 对高频固定 Prompt，务必启用 [显式缓存](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)；
  - Embedding 场景优先选用 `text-embedding-lite` 等轻量模型；
  - Rerank 任务避免传入超长 Document，预截断至关键段落。
- **排问题**：
  - 若收到 `429 Too Many Requests`，检查 Token Plan 配额是否耗尽（而非单纯 RPM 限流）；
  - 若 `max_tokens` 设置未生效，确认 `plan` 与 `model` 兼容性（如 `coding` Plan 不支持 `qwen-max`）；
  - 审计日志中 `input.tokens` 异常偏高？检查是否误将 Base64 图片、大段 JSON Schema 等非文本内容直传至文本模型。
- **写代码**：始终在 SDK 调用中显式传入 `plan`（推荐全局客户端配置 + 单次覆盖），避免依赖旧版默认 fallback 行为。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [token plan api](../api/token-plan-api.md)
- [model monitoring](../guides/model-monitoring.md)
- [vector and sort](../api/vector-and-sort.md)
- [use cases](../guides/use-cases.md)


