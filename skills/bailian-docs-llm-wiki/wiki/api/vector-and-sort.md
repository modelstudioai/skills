# vector and sort

百炼平台提供文本向量（embedding）、多模态向量（multimodal embedding）和文本排序（rerank）三大核心能力，覆盖语义检索、RAG、跨模态搜索等典型AI应用链路。所有能力均支持同步/异步调用、OpenAI兼容接口及DashScope SDK，并按实际[Token](../concepts/token.md)消耗计费。开发者可根据数据规模、模态类型、延迟敏感度和精度要求选择对应模型与接口。

## 支持的模型/功能

- **通用文本向量**：支持 `qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3` 等系列模型，适用于语义搜索、聚类、分类等任务。详细参数与地域差异见 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **批处理文本向量**：专为大规模文本设计，支持单次10万行、每行2048 [Token](../concepts/token.md)的异步批量[向量化](../concepts/embedding.md)，模型包括 `text-embedding-async-v2` 和 `text-embedding-async-v1`，详见 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **多模态向量**：支持文本、图像、视频及其组合的统一语义编码，提供独立向量（各模态单独编码）与融合向量（多模态联合编码）两种模式，覆盖 `qwen3-vl-embedding`、`tongyi-embedding-vision-plus-2026-03-06` 等模型，参见 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。
- **文本排序（Rerank）**：对召回结果进行二次精排，提升Top-K相关性。支持纯文本（`qwen3-rerank`）、多模态（`qwen3-vl-rerank`）及兼容旧版（`gte-rerank-v2`）模型，其中 `gte-rerank` 系列将于2026年05月30日下线，[文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md) 文档已明确迁移建议。

> **注意**：`qwen3-vl-embedding` 与 `qwen2.5-vl-embedding` 均支持融合向量，但前者通过 `enable_fusion=true` 参数控制，后者始终返回融合向量且不支持独立向量；而 `tongyi-embedding-vision-plus` 系列中，`-2026-03-06` 快照版本支持融合向量（需将 text/image/video 放入同一 content 对象），旧版 `tongyi-embedding-vision-plus` 则仅支持独立向量——该差异在 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md) 中有明确说明，但部分示例未严格区分，开发者需以参数行为为准。

## 关键参数

| 参数 | 适用场景 | 说明 |
|------|----------|------|
| `dimensions` | 同步文本向量、多模态向量 | 指定向量维度（如 `1024`, `2048`）。`text-embedding-v2`、`multimodal-embedding-v1` 等固定维度模型不支持此参数。 |
| `encoding_format` | 同步文本向量 | 控制输出格式：`float`（默认）或 `base64`。**注意**：老网关强制返回 `float`，长请求（如 >8192 [Token](../concepts/token.md)）也会降级至老网关，详见 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。 |
| `text_type` | 批处理文本向量 | 区分 `query`（查询文本）与 `document`（底库文本），对非对称检索任务效果显著。 |
| `enable_fusion` | `qwen3-vl-embedding` 多模态向量 | `true` 时返回融合向量（1个），`false` 或省略时返回独立向量（N个）。`qwen2.5-vl-embedding` 不支持该参数。 |
| `instruct` | 排序模型 | 自定义排序任务指令（如 `"Retrieve semantically similar text."`），影响模型对Query-Document相关性的判断逻辑，仅 `qwen3.7-text-rerank`、`qwen3-rerank`、`qwen3-vl-rerank` 支持。 |

## 使用方式

- **同步调用（低延迟、小批量）**：适用于实时场景（如用户搜索即时响应）。使用 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)（`/compatible-mode/v1/embeddings`）或 DashScope HTTP API（`/api/v1/services/embeddings/...`）。输入支持字符串、字符串列表或文件流，单次最多20条（`qwen3.7-text-embedding`）或10条（`text-embedding-v4`）。
- **异步批处理（高吞吐、大批量）**：适用于离线构建向量库。通过 `/api/v1/services/embeddings/text-embedding/text-embedding` 提交任务，支持10万行/次，文件需托管于公网可访问URL（≤200MB）。SDK 提供 `BatchTextEmbedding.call()`（同步等待）与 `async_call()` + `wait()`（异步轮询）封装。
- **多模态向量**：统一使用 `/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding` 接口，`input.contents` 数组内按需混合 `{"text":...}`、`{"image":...}`、`{"video":...}` 或 `{"multi_images":[...]}`。融合向量需确保多模态内容在同一 `content` 对象内（`2026-03-06` 版本）或显式设置 `enable_fusion=true`（`qwen3-vl-embedding`）。
- **排序模型**：`qwen3-rerank` 使用 OpenAI 兼容 `/compatible-api/v1/reranks` 接口（扁平参数）；其余模型（`qwen3.7-text-rerank`, `qwen3-vl-rerank`, `gte-rerank-v2`）使用 `/api/v1/services/rerank/text-rerank/text-rerank`（嵌套 `input` 结构）。注意 `qwen3-vl-rerank` 的 `query` 和 `documents` 均支持模态对象（如 `{"image": "url"}`）。

## 限制和注意事项

- **地域与免费额度差异**：北京地域部分模型（如 `qwen3.7-text-embedding`）提供90天内100万Token免费额度，而新加坡地域同名模型无免费额度；`text-embedding-v4` 在北京有免费额度，新加坡则无。具体请核对 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md) 中的表格。
- **限流策略**：同步接口受QPS限制（如 `text-embedding-v4` 北京地域为10 QPS），异步批处理接口限制更严格——`text-embedding-async-v2` 单用户并发运行任务数上限为3个，排队中+运行中总任务数不超过50个。超出将触发限流错误。
- **输入长度硬约束**：`text-embedding-v4` 单行最大8192 Token，超限直接报错（HTTP 400），**不会自动截断**；`qwen3-vl-embedding` 图片单张≤10 MB，视频≤50 MB；`qwen3-vl-rerank` 视频单条最多4个，图片单条最多40个。
- **模型下线提醒**：`gte-rerank` 系列模型（含 `gte-rerank-v2`）将于2026年05月30日下线，文档 [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md) 已明确推荐迁移到 `qwen3-rerank`，新项目应避免选用。
- **向量空间一致性**：多模态向量模型（如 `qwen3-vl-embedding`）保证文本、图像、视频向量位于同一语义空间，可直接计算余弦相似度；但不同模型（如 `text-embedding-v4` 与 `qwen3-vl-embedding`）的向量**不可混用比较**，因训练目标与空间分布不同。

## 来源文档

- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)
- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


