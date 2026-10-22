# vector and sort

百炼平台提供文本向量（embedding）、多模态向量（multimodal embedding）和文本排序（rerank）三大核心能力，覆盖语义检索、RAG、跨模态搜索等典型场景。所有能力均支持同步与异步调用模式，并通过统一的 DashScope SDK 和 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)降低集成门槛。开发者可根据数据规模、延迟要求和模态类型选择合适模型与接口。

## 支持的模型/功能

- **文本向量化**：支持通用文本嵌入（如 `qwen3.7-text-embedding`、`text-embedding-v4`）和批处理异步嵌入（`text-embedding-async-v2`），适用于语义搜索、聚类、分类等任务 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **多模态向量化**：支持文本、图像、视频及其组合的联合向量化（如 `qwen3-vl-embedding`、`tongyi-embedding-vision-plus-2026-03-06`），所有模态向量位于同一语义空间，支持跨模态检索与相似度计算 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。
- **文本排序（Rerank）**：对召回结果进行精细化重排序，提升 Top-K 相关性。支持纯文本（`qwen3-rerank`）、多模态（`qwen3-vl-rerank`）及兼容 GTE 系列（`gte-rerank-v2`）模型；注意 `gte-rerank` 模型将于 2026 年 5 月 30 日下线，应迁移至 `qwen3-rerank` [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。

> **注意**：文档 2 中 `text-embedding-v2` 的“最大行数”为 25，而文档 3 中 `text-embedding-async-v2` 的“单次请求文本最大行数”为 100,000 —— 二者属不同接口（同步 vs 异步），无矛盾；但文档 2 表格中 `text-embedding-v2` 的“单行最大 [Token](../concepts/token.md) 数”标为 2,048，而文档 7 中 `qwen3-rerank` 的“单条最大输入 [Token](../concepts/token.md)”为 4,000，表明 `text-embedding-v2` 已属旧版低容量模型，不推荐新项目使用。

## 关键参数

| 参数 | 适用场景 | 说明 |
|--------|-----------|------|
| `model` | 所有接口 | 必选。模型名需严格匹配文档列表（如 `qwen3.7-text-embedding`, `qwen3-rerank`, `tongyi-embedding-vision-plus-2026-03-06`）。注意地域差异（北京/新加坡）可能导致可用模型与单价不同。 |
| `dimensions` / `dimension` | 文本/多模态向量 | 可选。指定输出向量维度（如 `1024`, `2048`）。`text-embedding-v1/v2` 不支持该参数；`multimodal-embedding-v1` 固定为 1024 维；`qwen3-vl-embedding` 支持 `2560`（默认）等多档可选。 |
| `input` | 所有接口 | 必选。格式依接口而异：<br>• 同步文本向量：支持 `string` / `array<string>` / `file`；<br>• 多模态向量：`contents: [{"text":"..."},{"image":"url"}]`；<br>• Rerank：`{"query": "...", "documents": [...]}`。 |
| `encoding_format` | 同步文本向量 | 可选。设为 `"float"` 或 `"base64"`，但[老网关仅返回 float](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)，长请求亦强制降级。 |
| `enable_fusion` | `qwen3-vl-embedding` | 可选布尔值。启用后将 `contents` 中所有输入融合为单个向量；未启用则返回独立向量。`qwen2.5-vl-embedding` 始终融合，不支持此参数。 |
| `instruct` | Rerank（`qwen3.7-text-rerank`/`qwen3-rerank`/`qwen3-vl-rerank`） | 可选字符串。用于指定排序任务类型（如 `"Retrieve semantically similar text."`），显著影响排序逻辑。 |

## 使用方式

- **同步调用（低延迟、小批量）**：适用于单次 ≤20 条文本（`qwen3.7-text-embedding`）或 ≤10 条（`text-embedding-v4`）的实时向量化，或 ≤500 文档的 rerank。推荐使用 OpenAI 兼容 SDK（需配置 `base_url`）或 DashScope SDK `TextEmbedding.call()` / `TextReRank.call()`。
- **异步批处理（大数据量、容忍延迟）**：适用于万级文本向量化（`text-embedding-async-v2`，单次最多 100,000 行）或超长视频/多图处理。必须通过 HTTP 创建任务 + 轮询 `GET /api/v1/tasks/{task_id}` 获取结果，或使用 DashScope SDK 的 `BatchTextEmbedding.async_call()` / `wait()` 封装。
- **多模态融合**：使用 `qwen3-vl-embedding` 时，在 `parameters` 中设置 `"enable_fusion": true`；使用 `tongyi-embedding-vision-plus-2026-03-06` 时，将 `text`、`image`、`video` 放入**同一个 content 对象**（而非数组内多个对象）即可触发融合。

## 限制和注意事项

- **[Token](../concepts/token.md) 与尺寸限制**：各模型有严格上限。例如 `text-embedding-v4` 单行最多 8,192 Token，`qwen3-vl-embedding` 图片单张 ≤10 MB，`qwen3-vl-rerank` 视频单条最多 4 个；超出将直接返回 HTTP 400 错误，**不会自动截断**。
- **地域与免费额度差异**：北京地域部分模型（如 `qwen3.7-text-embedding`）提供 100 万 Token 免费额度（90 天），而新加坡地域同模型无免费额度；异步批处理模型 `text-embedding-async-v2` 免费额度为 2000 万 Token [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **限流策略**：同步接口按 RPS 限流；异步批处理除 RPS 外，还限制“同时运行中任务数 ≤3”且“排队+运行中总数 ≤50”；多模态向量暂未明确限流规则，但大文件上传可能受网络与超时约束。
- **模型兼容性**：`tongyi-embedding-vision-plus` 和 `tongyi-embedding-vision-flash` 不支持 `dimension` 参数；`multimodal-embedding-v1` 不支持 `enable_fusion`；`gte-rerank-v2` 不支持 `instruct` 参数。务必按模型能力表选用参数。
- **响应时效性**：[异步任务](../concepts/asynchronous-task.md)结果 URL 有效期仅 **24 小时**，需及时下载保存；同步接口响应中 `relevance_score` 为本次请求内相对分数，**不可跨请求比较**。

## 来源文档

- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)
- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


