# vector and sort

百炼平台提供文本向量（embedding）、多模态向量（multimodal embedding）和文本排序（rerank）三类核心语义理解能力，覆盖从原始内容表征、跨模态对齐到检索结果精排的完整 pipeline。所有能力均支持同步与异步调用，适配 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)与 DashScope 原生 SDK，并在多地（北京、新加坡等）部署以满足低延迟与合规需求。

## 支持的模型/功能

- **文本向量化**：支持通用文本嵌入（`qwen3.7-text-embedding`、`text-embedding-v4` 等）与批处理异步嵌入（`text-embedding-async-v2`），适用于语义搜索、聚类、RAG 底库构建等场景。详情见 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **多模态向量化**：支持文本、图像、视频统一语义空间表征（`qwen3-vl-embedding`、`tongyi-embedding-vision-plus-2026-03-06` 等），提供独立向量（每模态各一）与融合向量（多模态合一）两种模式，适用于跨模态检索与多源内容理解。详见 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。
- **文本排序（Rerank）**：对召回结果进行二次重排序，提升 Top-K 相关性。支持纯文本（`qwen3-rerank`）、多模态（`qwen3-vl-rerank`）及兼容旧版（`gte-rerank-v2`）模型；其中 `gte-rerank` 系列将于 2026 年 5 月 30 日下线，[请迁移至 `qwen3-rerank`](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。

> **注意**：文档中 `qwen3.7-text-rerank` 的 HTTP 接口路径为 `/api/v1/services/rerank/text-rerank/text-rerank`，而 `qwen3-rerank` 使用 `/compatible-api/v1/reranks` —— 二者请求体结构、参数层级（如 `input` 是否包裹 `query`/`documents`）及响应格式均不兼容，不可混用。

## 关键参数

| 参数 | 适用模型 | 说明 |
|------|----------|------|
| `model` | 全部 | 必选。模型名称需严格匹配文档中列出的合法值（如 `qwen3-vl-embedding`、`qwen3-rerank`），大小写敏感。 |
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-03` 等 | 可选。指定输出向量维度。不同模型支持的取值范围不同（如 `text-embedding-v4` 支持 `2048/1536/1024/.../64`），未指定时取默认值。`text-embedding-v1/v2` 和 `tongyi-embedding-vision-plus` 等不支持该参数。 |
| `encoding_format` | 同步文本向量（`text-embedding-*`） | 可选。设为 `"float"` 或 `"base64"`，但实际返回格式受网关限制：老网关强制返回 `float`；新网关仅短请求按设置返回，长请求仍降级为 `float`。 |
| `enable_fusion` | `qwen3-vl-embedding` | 可选布尔值。设为 `true` 时将 `contents` 中所有输入融合为单个向量；设为 `false`（默认）或不传时生成独立向量。`tongyi-embedding-vision-plus-2026-03-06` 等新版模型通过将多模态字段置于同一 `content` 对象内实现融合，**不使用此参数**。 |
| `instruct` | `qwen3.7-text-rerank`, `qwen3-rerank`, `qwen3-vl-rerank` | 可选字符串。用于指定排序任务类型（如 `"Given a web search query, retrieve relevant passages..."`），显著影响相关性打分逻辑。未指定则默认按问答检索任务处理。 |
| `text_type` | 异步文本向量（`text-embedding-async-v*`） | 可选。设为 `"query"` 或 `"document"`，用于非对称检索任务优化（如 Query-Document 匹配）。 |

## 使用方式

- **同步调用（推荐小批量、低延迟场景）**：
  - 文本向量：使用 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（`/compatible-mode/v1/embeddings`）或 DashScope SDK `dashscope.TextEmbedding.call()`。
  - 多模态向量：使用 DashScope 原生 HTTP 接口（`/services/embeddings/multimodal-embedding/multimodal-embedding`）或 SDK `dashscope.MultimodalEmbedding.call()`。
  - 排序：`qwen3-rerank` 使用 `/compatible-api/v1/reranks`；其余 rerank 模型使用 `/services/rerank/text-rerank/text-rerank`。

- **异步调用（推荐大批量、高吞吐场景）**：
  - 文本向量：使用 `text-embedding-async-v2` 模型，通过两步完成：① 创建任务（`POST /services/embeddings/text-embedding/text-embedding` + `X-DashScope-Async: enable`）；② 轮询 `GET /tasks/{task_id}` 获取结果。SDK 提供 `BatchTextEmbedding.async_call()` 封装。
  - 多模态与排序暂不提供官方异步接口，需自行封装重试逻辑。

- **地域与 WorkspaceId**：所有接口 URL 均含 `{WorkspaceId}` 占位符，需替换为真实业务空间 ID；地域后缀（如 `cn-beijing`、`ap-southeast-1`）需与所选模型部署地一致。完整配置参考 [Base URL 总览](../../raw/model-user-guide/get-started-with-models/base-url.md)。

## 限制和注意事项

- **输入长度与批量限制**：
  - 同步文本向量：`qwen3.7-text-embedding` 单行最长 128,000 [Token](../concepts/token.md)，最多 20 行；`text-embedding-v4` 单行最长 8,192 [Token](../concepts/token.md)，最多 10 行；`text-embedding-v1/v2` 单行最长 2,048 [Token](../concepts/token.md)，最多 25 行。
  - 异步文本向量：`text-embedding-async-v2` 单次请求最多 100,000 行，单行最长 2,048 Token。
  - 排序模型：`qwen3-rerank` 单条文档最大 4,000 Token；`qwen3.7-text-rerank` 单条最大 30,000 Token；总请求 Token 数 = `Query Tokens × Document 数量 + Document Tokens 总和`，不得超过模型规定的请求最大输入 Token（如 `qwen3.7-text-rerank` 为 120,000）。
  - 多模态向量：`qwen3-vl-embedding` 文本最长 32,000 Token，图片单张 ≤10 MB，视频 ≤50 MB；`tongyi-embedding-vision-plus-2026-03-06` 单次请求内容元素总数 ≤20，图片最多 64 张。

- **免费额度与计费**：北京地域部分模型（如 `qwen3.7-text-embedding`）提供开通后 90 天内 100 万 Token 免费额度；新加坡地域模型通常无免费额度。计费按实际输入 Token 数（非字符数）计算，详见各模型表格中的“单价”列。

- **限流策略**：同步接口遵循全局速率限制（[限流文档](https://help.aliyun.com/zh/model-studio/rate-limit#953ddcd76495l)）；异步批处理接口有严格并发控制：单用户同时运行中任务 ≤3 个，排队中+运行中任务总数 ≤50 个。

- **模型兼容性**：`qwen2.5-vl-embedding` 仅支持融合向量，不支持 `enable_fusion` 参数；`multimodal-embedding-v1` 不支持 `dimension` 参数，固定 1024 维；`tongyi-embedding-vision-plus` 等旧版模型不支持 `res_level`、`max_video_frames` 等新参数。请严格依据 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md) 中的“模型能力对照”表选用参数。

> **注意**：文档 2 中 `text-embedding-v3` 在北京地域表格中标注支持语种为“50+主流语种”，而文档 7 中 `qwen3-rerank` 标注为“100+主流语种”，二者语种覆盖存在差异。实际使用时应以具体模型文档为准，避免假设跨模型语种能力一致。

## 来源文档

- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)
- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


