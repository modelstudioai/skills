# vector and sort

百炼平台提供文本向量（embedding）、多模态向量（multimodal embedding）和文本排序（rerank）三大核心能力，覆盖语义检索、RAG、跨模态搜索等典型场景。所有服务均支持同步与异步调用模式，可通过 DashScope SDK 或标准 HTTP API 集成，兼容 OpenAI 生态接口。

## 支持的模型/功能

- **文本向量化**：支持通用文本嵌入（如 `qwen3.7-text-embedding`、`text-embedding-v4`）和批处理异步嵌入（如 `text-embedding-async-v2`），适用于语义搜索、聚类、分类等任务。详情见 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **多模态向量化**：支持文本、图像、视频统一语义空间表征，提供独立向量（各模态单独编码）与融合向量（多模态联合编码）两种模式，模型包括 `qwen3-vl-embedding` 和 `tongyi-embedding-vision-plus-2026-03-06` 等。详见 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。
- **文本排序（Rerank）**：对召回结果进行精细化重排序，提升 Top-K 相关性。支持纯文本（`qwen3-rerank`）、多模态（`qwen3-vl-rerank`）及历史模型（`gte-rerank-v2`）。注意：`gte-rerank` 系列模型将于 2026 年 5 月 30 日下线，[排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md) 文档已明确提示迁移建议。

> **注意**：文档 2 中 `text-embedding-v2` 的免费额度为“各50万Token”，而文档 3 中 `text-embedding-async-v2` 的免费额度为“各2000万Token”；二者地域、计费模型不同，不可直接对比。实际使用时请以控制台实时配额或最新计费页为准。

## 关键参数

| 参数 | 适用场景 | 说明 |
|------|----------|------|
| `model` | 全部 | 必选。文本向量模型（如 `qwen3.7-text-embedding`）、多模态模型（如 `qwen3-vl-embedding`）或排序模型（如 `qwen3-rerank`）的精确名称。 |
| `input` | 全部 | 必选。文本向量支持 `string` / `array<string>` / `file`；多模态向量需为 `{"contents": [...]}` 结构；排序模型需为 `{"query": "...", "documents": [...]}`。 |
| `dimensions` | 文本/多模态向量 | 可选。指定输出向量维度（如 `1024`, `2048`），但部分模型（如 `tongyi-embedding-vision-plus`、`multimodal-embedding-v1`）不支持该参数，固定维度。 |
| `enable_fusion` | 仅 `qwen3-vl-embedding` | 可选布尔值。设为 `true` 时启用融合向量模式（返回单个向量）；默认为独立向量（返回多个向量）。 |
| `top_n` | 排序模型 | 可选。指定返回前 N 个最相关结果，默认返回全部。 |
| `instruct` | `qwen3.7-text-rerank` / `qwen3-rerank` / `qwen3-vl-rerank` | 可选字符串。用于指定排序任务类型（如 `"Retrieve semantically similar text."`），显著影响排序逻辑。 |

## 使用方式

- **同步调用（推荐小批量）**：适用于单次 ≤20 条文本（`qwen3.7-text-embedding`）或 ≤10 条（`text-embedding-v4`）的低延迟场景。OpenAI 兼容模式需配置 `base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"`，并使用 `client.embeddings.create()` 方法。
- **异步批处理（推荐大批量）**：适用于百万级文本向量化。需先调用 `/api/v1/services/embeddings/text-embedding/text-embedding` 创建任务，再轮询 `/api/v1/tasks/{task_id}` 获取结果。文件需通过公开 URL 提供，单文件 ≤200MB，单次最多 100,000 行。参见 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **多模态与排序调用**：统一使用 DashScope HTTP endpoint `POST https://dashscope.aliyuncs.com/api/v1/services/...`，无 OpenAI 兼容路由。SDK 调用需使用 `dashscope.TextReRank.call()` 或 `dashscope.MultimodalEmbedding.call()` 等专用方法。

## 限制和注意事项

- **输入长度限制严格**：`text-embedding-v4` 单行上限 8,192 Token，`qwen3.7-text-embedding` 单行上限 128,000 Token；超出将直接返回 HTTP 400 错误，**不会自动截断**。排序模型 `qwen3-rerank` 单条文档上限 4,000 Token，`qwen3.7-text-rerank` 请求总 Token 上限 120,000。
- **地域与计费差异**：北京与新加坡地域的模型列表、单价、免费额度均不同（如 `qwen3.7-text-embedding` 在北京有免费额度，新加坡无）。调用前务必确认 `base_url` 和 `WorkspaceId` 所属地域。
- **网关行为差异**：`encoding_format="base64"` 仅在新网关的短请求中生效；长请求会自动降级至老网关，强制返回 `float` 格式。开发时应避免依赖 `base64` 输出的稳定性。
- **模型能力边界**：`qwen2.5-vl-embedding` 仅支持融合向量，不支持 `enable_fusion` 参数；`tongyi-embedding-vision-plus` 不支持 `dimension` 参数；`multimodal-embedding-v1` 固定 1024 维且不支持融合。务必按 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md) 中的“模型能力对照”表选型。

## 来源文档

- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)
- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


