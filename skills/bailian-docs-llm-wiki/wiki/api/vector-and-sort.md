# vector and sort

`vector and sort` 是百炼平台提供的核心语义理解能力套件，涵盖文本/多模态向量化（Embedding）与文本重排序（Rerank）两大功能。向量模型将原始内容映射到统一语义空间，支撑检索、聚类、分类等下游任务；排序模型则对召回结果进行精细化相关性重打分与重排序，显著提升 RAG、搜索等场景的准确率。两类服务均提供同步、异步及 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，适配不同规模与延迟要求的业务场景。

## 支持的模型/功能

### 文本向量模型
- **同步接口**：支持 `qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3`、`text-embedding-v2`、`text-embedding-v1` 等通用文本向量模型，适用于低延迟、小批量（≤20 行）场景 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **异步批处理接口**：支持 `text-embedding-async-v2`（单次最多 100,000 行）、`text-embedding-async-v1`，适用于大规模离线向量化任务 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **多模态向量模型**：支持 `qwen3-vl-embedding`、`qwen2.5-vl-embedding`、`tongyi-embedding-vision-plus-2026-03-06` 等，可生成文本/图像/视频的独立向量或跨模态融合向量，统一语义空间支持跨模态检索 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

### 文本排序模型（Rerank）
- **主流模型**：`qwen3.7-text-rerank`（高精度、长上下文）、`qwen3-rerank`（OpenAI 兼容、轻量高效）、`qwen3-vl-rerank`（支持图文/视频混合查询）、`gte-rerank-v2`（多语种兼容）。
- **重要迁移提示**：`gte-rerank` 模型将于 2026 年 05 月 30 日下线，官方明确推荐迁移到 `qwen3-rerank` 或 `qwen3.7-text-rerank` [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。

## 关键参数

| 参数 | 适用模型 | 说明 |
|------|----------|------|
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-03` 等 | 指定向量维度（如 `1024`, `2048`），非所有模型均支持；`text-embedding-v2/v1`、`tongyi-embedding-vision-plus` 等固定维度模型不支持该参数。 |
| `encoding_format` | 同步文本向量（`qwen3.7-text-embedding` 等） | 控制返回格式为 `float` 或 `base64`，但[同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)明确指出：老网关始终返回 `float`，新网关仅短请求支持 `base64`，长请求仍回落至 `float`。 |
| `enable_fusion` | `qwen3-vl-embedding` | 布尔值，启用后将 `contents` 中所有模态输入融合为单个向量；其他模型（如 `qwen2.5-vl-embedding`）仅支持融合，无此参数；`tongyi-embedding-vision-plus-2026-03-06` 则通过将 text/image/video 放入同一 content 对象实现融合，无需 `enable_fusion`。 |
| `instruct` | `qwen3.7-text-rerank`, `qwen3-rerank`, `qwen3-vl-rerank` | 自定义排序任务指令（如 `"Given a web search query..."`），影响模型对问答检索 vs 语义相似度等任务的策略判断，建议英文书写。 |
| `text_type` | 异步文本向量（`text-embedding-async-v2`） | 区分 `document`（底库文本）与 `query`（查询文本），对非对称检索任务效果提升显著。 |

> **注意**：文档 1 与文档 3 对 `text-embedding-async-v2` 的免费额度描述矛盾——文档 1 未列出该模型免费额度，而文档 3 明确写有“各2000万[Token](../concepts/token.md)”。以[批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)为准，该模型享有免费额度。

## 使用方式

### 接口调用路径
- **文本向量同步调用**：使用 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（`/compatible-mode/v1/embeddings`）或 DashScope 原生接口（`/api/v1/services/embeddings/text-embedding/text-embedding`），支持 `string`、`array<string>`、`file` 三种输入格式。
- **文本向量异步调用**：必须通过两步 HTTP 流程：① `POST /api/v1/services/embeddings/text-embedding/text-embedding` 创建任务（需 `X-DashScope-Async: enable` 头）；② `GET /api/v1/tasks/{task_id}` 轮询结果。
- **多模态向量调用**：统一使用 `POST /api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`，通过 `input.contents` 数组声明多模态内容，`parameters.enable_fusion` 或结构化 content 控制融合行为。
- **文本排序调用**：`qwen3-rerank` 使用 OpenAI 兼容 `/compatible-api/v1/reranks`；其余模型（`qwen3.7-text-rerank`, `qwen3-vl-rerank`, `gte-rerank-v2`）使用原生 `/api/v1/services/rerank/text-rerank/text-rerank`，注意 `input` 和 `parameters` 的嵌套层级差异。

### SDK 快速启动
- Python：安装 `dashscope` 后，直接调用 `dashscope.TextEmbedding.call()`（同步）、`dashscope.BatchTextEmbedding.call()`（异步）、`dashscope.TextReRank.call()`（排序）。
- Java：使用 `com.alibaba.dashscope.embeddings.*` 和 `com.alibaba.dashscope.rerank.*` 包，参数命名扁平化（如 `top_n` 直接传入，无需嵌套 `parameters`）。

## 限制和注意事项

- **[Token](../concepts/token.md) 与长度限制**：
  - 同步文本向量：`qwen3.7-text-embedding` 单行最长 128,000 [Token](../concepts/token.md)；`text-embedding-v4` 为 8,192 Token；`text-embedding-v1/v2` 为 2,048 Token。
  - 异步文本向量：`text-embedding-async-v2` 单行 ≤2,048 Token，单次请求 ≤100,000 行。
  - 排序模型：`qwen3.7-text-rerank` 单条文档最长 30,000 Token，总请求 Token ≤120,000；`qwen3-rerank` 单条文档限 4,000 Token。
  - 多模态向量：`qwen3-vl-embedding` 文本最长 32,000 Token，单张图片 ≤10 MB，单个视频 ≤50 MB。

- **地域与计费差异**：北京与新加坡地域的模型单价、免费额度、限流策略不同（如 `qwen3.7-text-embedding` 新加坡版无免费额度），调用前务必确认业务空间所在地域及对应文档 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。

- **向量空间一致性**：多模态向量模型（如 `qwen3-vl-embedding`）确保文本、图像、视频向量位于同一语义空间，可直接计算余弦相似度；但不同模型（如 `qwen3-vl-embedding` 与 `tongyi-embedding-vision-plus`）之间向量不可互比，禁止跨模型计算相似度。

- **错误处理**：HTTP 400 错误通常由超限（如 Token 超长、行数超限）触发，不会自动截断；401/403 多为认证失败；异步任务失败后，`output.code` 和 `output.message` 提供具体原因，需结合[错误码](../../raw/model-api-reference/preparations/error-code.md)排查。

## 来源文档

- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)


