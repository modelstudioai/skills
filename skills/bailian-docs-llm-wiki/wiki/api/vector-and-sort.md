# vector and sort

百炼平台提供文本向量（Embedding）、多模态向量（Multimodal Embedding）和文本排序（Rerank）三大核心能力，覆盖语义检索、RAG、跨模态搜索、聚类与分类等典型AI应用链路。所有能力均支持同步/异步调用、OpenAI兼容接口及SDK封装，适用于从单条实时推理到百万级批量处理的全场景需求。

## 支持的模型/功能

- **通用文本向量**：支持 `qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3` 等多代模型，适用于中英文及201种语言的语义表征；[同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md) 提供低延迟实时向量化能力。
- **多模态向量**：支持 `qwen3-vl-embedding`、`tongyi-embedding-vision-plus-2026-03-06` 等模型，统一文本、图像、视频的语义空间，支持独立向量与融合向量两种模式；详见 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。
- **文本排序（Rerank）**：提供 `qwen3-rerank`（推荐替代已下线的 `gte-rerank`）、`qwen3.7-text-rerank` 和 `qwen3-vl-rerank`，支持纯文本、图文混合、图/视频查询等多种排序任务；[文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md) 文档明确标注了 `gte-rerank` 模型将于2026年05月30日下线。

> **注意**：`text-embedding-v2` 在北京地域有免费额度（50万Token），而新加坡地域无免费额度；`text-embedding-v4` 在两地均无免费额度，但支持更多语种和编程语言。该差异未在文档中统一说明，开发者需按地域核对计费策略。

## 关键参数

| 参数 | 适用场景 | 说明 |
|--------|-----------|------|
| `model` | 所有接口 | 必选。模型名需严格匹配文档列表，如 `qwen3.7-text-embedding`、`tongyi-embedding-vision-plus-2026-03-06`、`qwen3-rerank`。注意 `qwen3-rerank` 使用独立的 `/compatible-api/v1/reranks` 接口，与其他 rerank 模型不同。 |
| `dimensions` | 向量类模型 | 可选。仅 `qwen3.7-text-embedding`、`text-embedding-v3/v4`、`qwen3-vl-embedding` 等新模型支持；`multimodal-embedding-v1`、`tongyi-embedding-vision-plus` 等旧模型不支持，强制返回固定维度。 |
| `input` | 同步向量/排序 | 格式灵活：字符串、字符串数组或文件对象（向量）；或含 `query`/`documents` 的对象（排序）。多模态输入必须为 `{"contents": [...]}` 结构。 |
| `enable_fusion` | 多模态向量 | 仅 `qwen3-vl-embedding` 支持。设为 `true` 时将全部输入融合为单个向量；其他模型（如 `tongyi-embedding-vision-plus-2026-03-06`）通过将 `text`/`image`/`video` 放入同一 content 对象实现融合，**不使用此参数**。 |
| `instruct` | Rerank | 可选。指导排序策略，如 `"Given a web search query, retrieve relevant passages that answer the query."`（问答检索）或 `"Retrieve semantically similar text."`（语义相似度）。仅 `qwen3.7-text-rerank`、`qwen3-rerank`、`qwen3-vl-rerank` 生效。 |

## 使用方式

- **同步向量**：使用 [OpenAI 兼容接口](../concepts/openai-compatibility.md)（`/compatible-mode/v1/embeddings`）或 DashScope 原生接口，适合单次 ≤20 条（`qwen3.7-text-embedding`）或 ≤10 条（`text-embedding-v4`）的低延迟场景。示例见 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **批处理向量**：使用异步 HTTP 接口（`X-DashScope-Async: enable`）或 `BatchTextEmbedding` SDK，支持单次 100,000 行、200MB 文件，适用于大规模底库构建；详见 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **多模态向量**：必须使用原生 HTTP 接口 `POST /api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`，不支持 OpenAI 兼容模式；支持 `text`/`image`/`video`/`multi_images` 组合输入。
- **排序（Rerank）**：`qwen3-rerank` 使用 `/compatible-api/v1/reranks`（扁平参数结构），其余模型使用 `/api/v1/services/rerank/text-rerank/text-rerank`（嵌套 `input` 结构），务必区分接口路径与参数层级。

## 限制和注意事项

- **Token 限制**：`qwen3.7-text-embedding` 单行支持 128,000 Token，而 `text-embedding-v4` 仅支持 8,192 Token；`qwen3-rerank` 单条文档上限为 4,000 Token，`qwen3.7-text-rerank` 为 30,000 Token。超限将直接返回 HTTP 400 错误，**不会自动截断**。
- **地域与计费差异**：北京地域部分模型（如 `qwen3.7-text-embedding`）提供 90 天内 100 万 Token 免费额度，新加坡地域多数模型无免费额度；单价也存在微小差异（如 `qwen3.7-text-embedding` 北京 0.0005 元/千 Token，新加坡 0.000525 元/千 Token）。
- **模型能力边界**：
  - `qwen2.5-vl-embedding` 仅支持融合向量，不支持 `enable_fusion=false` 的独立向量模式；
  - `tongyi-embedding-vision-plus` 和 `tongyi-embedding-vision-flash` 不支持 `dimension` 参数，固定返回 1152/768 维；
  - `multimodal-embedding-v1` 不支持 `dimension` 参数且仅支持中文/英文。
- **异步任务管理**：批处理任务 ID 有效期仅 24 小时，结果 URL 需及时保存；并发运行中任务数上限为 3 个，排队中任务总数上限为 50 个。

## 来源文档

- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)
- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


