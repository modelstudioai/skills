# vector and sort

百炼平台提供文本向量（Embedding）、多模态向量（Multimodal Embedding）和排序（Rerank）三大核心能力，覆盖语义检索、RAG、跨模态搜索等典型AI应用链路。所有能力均支持同步与[异步调用](../concepts/asynchronous-invocation.md)，适配OpenAI兼容接口与原生DashScope SDK，并在多地（北京、新加坡等）部署以满足合规与低延迟需求。开发者可根据数据规模、模态类型、精度要求和成本预算选择对应模型与参数配置。

## 支持的模型/功能

### 文本向量化
- **通用文本向量**：支持 `qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3` 等系列模型，适用于语义搜索、聚类、分类等任务。其中 `qwen3.7-text-embedding` 和 `text-embedding-v4` 支持最高 128,000 [Token](../concepts/token.md) 单行输入，而 `text-embedding-v3` 限制为 8,192 [Token](../concepts/token.md) [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **批处理向量**：`text-embedding-async-v2` 支持单次 100,000 行、每行最多 2,048 [Token](../concepts/token.md) 的大规模异步批量处理，适合底库预计算场景 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。

### 多模态向量化
- **独立向量**：为文本、图片、视频等各模态输入分别生成独立向量（如 `tongyi-embedding-vision-plus-2026-03-06`），适用于以图搜图、以文搜图等逐项比对场景。
- **融合向量**：将多模态内容（如文本+图片+视频）编码为单一向量（如 `qwen3-vl-embedding` 启用 `enable_fusion=true`，或 `tongyi-embedding-vision-plus-2026-03-06` 将多模态字段置于同一 content 对象中），适用于商品多源信息统一表征 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

### 排序（Rerank）
- **文本排序**：`qwen3.7-text-rerank` 和 `qwen3-rerank` 支持最多 500 个文档的二次精排，`qwen3-rerank` 为当前主力推荐模型（`gte-rerank` 已于 2026 年 5 月 30 日下线）。
- **多模态排序**：`qwen3-vl-rerank` 支持文本、图片、视频混合查询与排序，例如以图查文、以文查视频等跨模态检索任务。

> **注意**：文档 2 中 `text-embedding-v2` 标注“最大行数 25”，但文档 7 中批处理模型 `text-embedding-async-v2` 明确支持“单次请求文本最大行数 100,000”。二者属不同接口（同步 vs 异步），无矛盾；但需注意 `text-embedding-v2` 仅限同步调用且已非主力推荐，新项目应优先选用 `qwen3.7-text-embedding` 或 `text-embedding-v4`。

## 关键参数

| 参数 | 适用模型 | 说明 | 示例值 |
|------|----------|------|--------|
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding`, `qwen2.5-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06` 等 | 指定向量维度，影响精度与存储开销。部分模型（如 `tongyi-embedding-vision-plus` v1）不支持该参数，固定返回 1152 维。 | `1024`, `2048`, `2560` |
| `encoding_format` | 同步文本向量（`qwen3.7-text-embedding` 等） | 控制返回格式：`float`（默认）或 `base64`。**注意**：老网关强制返回 `float`，长请求亦会降级至老网关 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。 | `"float"`, `"base64"` |
| `enable_fusion` | `qwen3-vl-embedding` | 布尔值，启用后将 `contents` 中所有模态输入融合为 1 个向量。`qwen2.5-vl-embedding` 固定融合，无需此参数。 | `true` |
| `instruct` | `qwen3.7-text-rerank`, `qwen3-rerank`, `qwen3-vl-rerank` | 自定义排序任务指令，影响相关性判断逻辑。支持英文指令如 `"Retrieve semantically similar text."`。未指定时默认按问答检索任务处理。 | `"Given a web search query, retrieve relevant passages that answer the query."` |
| `text_type` | 批处理向量（`text-embedding-async-v1/v2`） | 区分 `query`（查询文本）与 `document`（底库文本），用于优化非对称检索任务效果。聚类等对称任务可省略。 | `"query"`, `"document"` |

## 使用方式

### 调用路径
- **同步调用**：适用于实时性要求高、输入规模小的场景（如单次 ≤50 条文本、≤10 张图片）。使用 `/compatible-mode/v1/embeddings`（OpenAI 兼容）或 `/api/v1/services/embeddings/...`（原生）端点。
- **[异步调用](../concepts/asynchronous-invocation.md)**：适用于大规模批量处理（如百万级文档向量化）。需先 `POST /api/v1/services/embeddings/text-embedding/text-embedding` 创建任务，再 `GET /api/v1/tasks/{task_id}` 轮询结果。

### SDK 与 HTTP 差异
- **SDK 调用**：参数扁平化（如 `client.rerank.create(model=..., query=..., documents=...)`），自动处理认证与重试，推荐 Python/Java 开发者使用。
- **HTTP 调用**：需手动构造 `Authorization`、`Content-Type` 头，请求体严格嵌套 `input` 和 `parameters` 对象。[OpenAI 兼容接口](../concepts/openai-compatibility.md)需配置 `base_url` 为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`。

### 多模态输入格式
- **独立向量**：`contents` 数组中每个元素为单模态对象，如 `[{"text": "hello"}, {"image": "url"}]`。
- **融合向量**：
  - `qwen3-vl-embedding`：在独立向量请求基础上添加 `"parameters": {"enable_fusion": true}`；
  - `tongyi-embedding-vision-plus-2026-03-06`：将多模态字段置于同一对象内，如 `[{"text": "hello", "image": "url", "video": "url"}]`。

## 限制和注意事项

- **地域差异**：北京与新加坡地域的模型列表、免费额度、单价存在差异。例如 `qwen3.7-text-embedding` 在北京有 100 万 Token 免费额度，在新加坡则无；`text-embedding-v4` 在北京单价为 0.0005 元/千 Token，在新加坡为 0.000514 元/千 Token。调用前务必确认目标地域配置。
- **Token 计费规则**：文本向量按输入 Token 计费；多模态向量中，文本与图片/视频分开计费（如 `qwen3-vl-embedding`：文本 0.0007 元/千 Token，图片/视频 0.0018 元/千 Token）；排序模型按 `Query Tokens × Document 数量 + Document Tokens 总和` 计费。
- **输入长度硬限制**：超限将直接返回 HTTP 400 错误，**不会截断**。例如 `text-embedding-v3` 单行最多 8,192 Token，`qwen3-vl-rerank` 单条图片/视频文档分别限 40/4 个，超出即失败。
- **异步任务约束**：批处理任务有严格并发限制——单用户最多 3 个任务同时运行，排队中+运行中总数不超过 50 个；任务结果 URL 仅保留 24 小时，需及时下载。
- **模型兼容性**：`multimodal-embedding-v1` 不支持 `dimension` 参数（固定 1024 维），而 `tongyi-embedding-vision-plus` v1 也不支持该参数；但其快照版本 `tongyi-embedding-vision-plus-2026-03-06` 明确支持 `dimension` 及 `res_level`、`max_video_frames` 等新参数。

## 来源文档

- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)
- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)


