# vector and sort

百炼平台的 `vector and sort` 功能涵盖文本/多模态向量化（embedding）与语义重排序（rerank）两大核心能力，支撑[检索增强生成](../concepts/rag.md)（RAG）、跨模态搜索、聚类分析等典型AI应用。向量模型将非结构化内容映射至统一语义空间，排序模型则对召回结果进行精细化相关性打分与重排，二者常组合使用以构建高精度检索流水线。

## 支持的模型与功能

- **文本向量模型**：支持同步（`qwen3.7-text-embedding`, `text-embedding-v4` 等）与异步批处理（`text-embedding-async-v2`）两类接口，覆盖从实时单条到百万级批量的向量化需求 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。  
- **多模态向量模型**：支持文本、图像、视频的独立向量与融合向量生成，所有模态共享同一语义空间，可直接计算跨模态余弦相似度 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。  
- **排序（Rerank）模型**：提供纯文本（`qwen3-rerank`）、多模态（`qwen3-vl-rerank`）及兼容型（`gte-rerank-v2`）三类模型，支持 query-document 语义相关性精准打分与 top-k 返回 [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。  

> **注意**：文档中 `gte-rerank` 模型已明确标注将于 2026 年 5 月 30 日下线，且 `gte-rerank-v2` 不支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)，而 `qwen3-rerank` 和 `qwen3.7-text-rerank` 均支持 —— 开发者应优先选用 `qwen3-rerank` 作为替代方案。

## 关键参数

| 参数 | 适用场景 | 说明 |
|--------|----------|------|
| `dimensions` | 文本/多模态向量 | 指定向量维度（如 `1024`, `2048`），不同模型支持值不同；`multimodal-embedding-v1` 固定为 1024，不支持该参数。 |
| `encoding_format` | 同步文本向量 | 控制返回格式（`float` 或 `base64`），但老网关强制返回 `float`，长请求亦会降级至老网关 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。 |
| `enable_fusion` / 同一 content 对象 | 多模态向量 | `qwen3-vl-embedding` 通过 `enable_fusion=true` 开启融合；`tongyi-embedding-vision-plus-2026-03-06` 等新版模型则通过将 `text`/`image`/`video` 放入同一字典实现融合。 |
| `instruct` | 排序模型 | 指导排序策略（如 `"Given a web search query..."` 或 `"Retrieve semantically similar text."`），仅 `qwen3.7-text-rerank`/`qwen3-rerank`/`qwen3-vl-rerank` 支持。 |
| `text_type` | 异步文本向量批处理 | 区分 `query`（查询）与 `document`（底库）类型，提升检索任务效果，对称任务（如聚类）可忽略。 |

## 使用方式

- **同步向量调用**：推荐用于低延迟、小批量场景（≤20 条）。使用 OpenAI 兼容 SDK 或 DashScope HTTP 接口，需配置地域专属 `base_url`（如北京：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）。  
- **异步向量批处理**：适用于超大批量（最高 100,000 行）或大文件（≤200MB）场景，需两步操作：先 `POST /api/v1/services/embeddings/text-embedding/text-embedding` 创建任务，再 `GET /api/v1/tasks/{task_id}` 轮询结果。  
- **多模态向量调用**：统一使用 `POST https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`，`input.contents` 数组内按模态类型（`text`/`image`/`video`/`multi_images`）组织输入。  
- **排序调用**：支持 DashScope HTTP（`input.query` + `input.documents` 嵌套）与 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)（扁平结构），后者仅限 `qwen3-rerank` 和 `qwen3.7-text-rerank`。  

## 限制和注意事项

- **Token 与行数限制**：`text-embedding-v4` 单行上限 8,192 Token、最多 10 行；`qwen3.7-text-embedding` 单行可达 128,000 Token、最多 20 行；异步批处理 `text-embedding-async-v2` 单行限 2,048 Token、单次最多 100,000 行。  
- **地域差异**：免费额度、单价、部分模型可用性因地域而异（如北京有 `qwen3.7-text-embedding` 免费额度，新加坡无）；务必核对所选地域的 [模型概览](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md) 表格。  
- **融合向量兼容性**：`qwen2.5-vl-embedding` 仅支持融合向量，不支持 `enable_fusion` 参数；`tongyi-embedding-vision-plus` 系列旧版仅支持独立向量，新版（`-2026-03-06`）才同时支持两种模式。  
- **排序模型输入计算**：`qwen3-vl-rerank` 的总 Token 消耗 = `Query Tokens × Document 数量 + 所有 Document Tokens 总和`，该值不可超过 `120,000` 上限，否则报错。  
- **任务有效期**：异步批处理任务结果 URL 仅保留 24 小时，需及时下载；同步接口响应无此限制。

## 来源文档

- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)
- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


