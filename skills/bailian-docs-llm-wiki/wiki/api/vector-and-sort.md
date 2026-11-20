# vector and sort

百炼平台提供文本向量（Embedding）、多模态向量（Multimodal Embedding）和文本排序（Rerank）三大核心能力，分别用于语义表征、跨模态理解与检索结果精排。所有能力均支持同步/异步调用、[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)及 DashScope SDK 封装，适用于 RAG、搜索、推荐、聚类等典型场景。详细模型选型与参数配置请参考 [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md) 等原始文档。

## 支持的模型与功能

### 文本向量化
- **同步接口**：支持 `qwen3.7-text-embedding`、`text-embedding-v4/v3/v2/v1` 等模型，适用于低延迟、小批量（≤20 行）场景。其中 `qwen3.7-text-embedding` 单行最大支持 128,000 Token，`text-embedding-v4` 为 Qwen3-Embedding 系列，支持 64–2048 维可选 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **异步批处理**：`text-embedding-async-v2` 支持单次 100,000 行、每行 ≤2,048 Token 的大规模文件处理，适合离线向量化任务 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。

### 多模态向量化
- 支持文本、图像、视频三模态统一表征，所有模态向量位于同一语义空间，可直接计算余弦相似度。
- 提供两种模式：
  - **独立向量**：每个输入（如 1 文本 + 2 图片）生成独立向量，适用于以文搜图等逐项匹配；
  - **融合向量**：将多模态输入（如文本+图片+视频）编码为单一向量，适用于商品多源信息融合表征。
- 模型包括 `qwen3-vl-embedding`（支持 `enable_fusion` 开关）、`tongyi-embedding-vision-plus-2026-03-06`（融合向量通过同 content 对象实现）等 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

### 排序（Rerank）
- `qwen3.7-text-rerank` 和 `qwen3-rerank` 支持纯文本重排，最大文档数 500，推荐替代即将下线的 `gte-rerank` 系列。
- `qwen3-vl-rerank` 支持跨模态重排（文本/图片/视频混合查询与文档），支持 `fps` 参数控制视频抽帧密度。
- 所有 rerank 模型均支持 `instruct` 参数指定任务类型（如问答检索 vs 语义相似度），显著影响排序逻辑。

> **注意**：`gte-rerank` 系列模型（含 `gte-rerank-v2`）将于 2026 年 05 月 30 日下线，官方明确推荐迁移至 `qwen3-rerank` 或 `qwen3.7-text-rerank` [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)。

## 关键参数

| 参数 | 适用场景 | 说明 |
|------|----------|------|
| `dimensions` | 同步文本向量、多模态向量 | 指定向量维度（如 `1024`, `2048`）。`text-embedding-v1/v2` 不支持；`multimodal-embedding-v1` 固定为 1024 维，不支持该参数。 |
| `encoding_format` | 同步文本向量 | 取值 `float` 或 `base64`，但老网关强制返回 `float`，长请求自动降级至老网关 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。 |
| `enable_fusion` | `qwen3-vl-embedding` | `true` 时启用融合向量；其他模型（如 `tongyi-embedding-vision-plus-2026-03-06`）通过将 text/image/video 放入同一 content 对象实现融合，无需此参数。 |
| `text_type` | 异步文本向量 | `document`（默认，用于底库）或 `query`（用于检索查询），影响向量表征策略。 |
| `instruct` | Rerank | 控制排序意图，如 `"Given a web search query, retrieve relevant passages..."`（问答）或 `"Retrieve semantically similar text."`（语义等价）。仅 `qwen3.7-text-rerank`/`qwen3-rerank`/`qwen3-vl-rerank` 支持。 |
| `top_n` | Rerank | 返回前 N 个结果，默认返回全部。 |

## 使用方式

### 调用路径
- **同步文本向量**：HTTP POST 到 `/compatible-mode/v1/embeddings`（OpenAI 兼容）或 `/api/v1/services/embeddings/text-embedding/text-embedding`（DashScope 原生）。
- **异步文本向量**：两步调用 —— 先 POST 创建任务（`X-DashScope-Async: enable`），再 GET `/api/v1/tasks/{task_id}` 查询结果。
- **多模态向量**：统一 HTTP POST 到 `/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`，`input.contents` 数组描述多模态输入。
- **Rerank**：HTTP POST 到 `/api/v1/services/rerank/text-rerank/text-rerank`，`input.query` 与 `input.documents` 结构化传入；`qwen3-rerank` 还支持 OpenAI 兼容 `/compatible-api/v1/reranks`。

### SDK 快速示例（Python）
```python
# 同步文本向量（OpenAI 兼容）
from openai import OpenAI
client = OpenAI(base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1", api_key=os.getenv("DASHSCOPE_API_KEY"))
res = client.embeddings.create(model="qwen3.7-text-embedding", input="hello world", dimensions=1024)

# 异步文本向量（DashScope SDK）
import dashscope
client = dashscope.Client(api_key=os.getenv("DASHSCOPE_API_KEY"), workspace="{WorkspaceId}", region="cn-beijing")
job = client.embeddings.jobs.create(model="text-embedding-async-v2", file_url="https://xxx.txt")
result = client.embeddings.jobs.wait(job)  # 自动轮询

# Rerank（DashScope 原生）
res = client.rerank.create(
    model="qwen3-rerank",
    query="什么是向量检索",
    documents=["向量检索是基于向量相似度的搜索技术", "RAG 是一种应用架构"]
)
```

## 限制与注意事项

- **地域差异**：北京与新加坡地域的模型免费额度、单价、限流策略不同。例如 `qwen3.7-text-embedding` 在北京有 100 万 Token 免费额度，在新加坡则无 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **Token 计费规则**：文本向量按输入 Token 计费；多模态向量中图片/视频单独计费（如 `qwen3-vl-embedding` 图片/视频 0.0018 元/千 Token，文本 0.0007 元/千 Token）；Rerank 按 `Query Tokens × Document 数量 + Document Tokens 总和` 计费。
- **异步任务生命周期**：批处理任务结果 URL 有效期仅 **24 小时**，需及时下载保存 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **模型兼容性**：`gte-rerank-v2` 和 `qwen3-vl-rerank` **不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**，调用会返回 `model_not_supported` 错误；仅 `qwen3.7-text-rerank` 和 `qwen3-rerank` 支持。
- **输入格式陷阱**：多模态向量中 `multi_images` 仅被 `tongyi-embedding-vision-plus` 等特定模型支持；`qwen2.5-vl-embedding` 仅支持融合向量且不支持多图，强行传入 `multi_images` 将报错。

## 来源文档

- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)
- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


