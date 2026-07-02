# vector and sort

百炼平台提供文本向量（Embedding）和文本排序（Rerank）两大类模型能力，支持将文本、图像、视频转换为数值向量或对候选文档进行相关性排序。这些能力广泛应用于语义搜索、RAG 检索增强、推荐系统、聚类分类等下游任务。

## 文本向量模型

### 通用文本向量（同步接口）

通用文本向量模型将文本转换为数值向量，支持多种维度和语种。当前推荐使用 text-embedding-v4（属于 Qwen3-Embedding 系列），支持 100+ 主流语种及多种编程语言。详细参数和调用方式参见 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。

| 模型 | 向量维度 | 最大行数 | 单行最大 [Token](../concepts/token.md) | 语种 |
|------|---------|---------|---------------|------|
| text-embedding-v4 | 2048/1536/1024(默认)/768/512/256/128/64 | 10 | 8,192 | 100+ 语种 |
| text-embedding-v3 | 1024(默认)/768/512/256/128/64 | 10 | 8,192 | 50+ 语种 |
| text-embedding-v2 | 1,536 | 25 | 2,048 | 10 语种 |
| text-embedding-v1 | 1,536 | 25 | 2,048 | 6 语种 |

**关键参数：**

- `model`（必选）：模型名称
- `input`（必选）：字符串、字符串列表或文件
- `dimensions`（可选）：指定向量维度，仅 v3/v4 支持
- `encoding_format`（可选）：当前仅支持 `float`

**调用方式：** 支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（base_url: `https://dashscope.aliyuncs.com/compatible-mode/v1`）和 [DashScope SDK](../concepts/dashscope-sdk.md)。

### 批处理接口

对于大规模文本向量化场景，可使用异步批处理接口（text-embedding-async-v1/v2），单次支持最多 10 万行文本。需通过 HTTP 的 `X-DashScope-Async: enable` 请求头启用异步模式，提交任务后通过 task_id 轮询结果。详细说明参见 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。

> **注意**：批处理接口同时处理中的任务数量不超过 50 个，并发运行上限为 3 个，超出部分需在队列中等待。

## 文本排序模型（Rerank）

排序模型对召回阶段的文档进行二次精准排序，将与查询最相关的结果排在前面。当前推荐使用 qwen3-rerank（文本）和 qwen3-vl-rerank（[多模态](../concepts/multimodal.md)），详见 [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。

| 模型 | 最大文档数 | 单条最大 [Token](../concepts/token.md) | 请求最大 [Token](../concepts/token.md) | 特点 |
|------|-----------|---------------|---------------|------|
| qwen3-vl-rerank | 文本100/图片40/视频4 | 8,000 | 120,000 | [多模态](../concepts/multimodal.md)，支持图文视频排序 |
| qwen3-rerank | 500 | 4,000 | - | 100+ 语种，高性能文本排序 |
| gte-rerank-v2 | - | - | 30,000 | 50+ 语种（即将下线） |

> **注意**：gte-rerank 模型将于 2026 年 05 月 30 日下线，推荐迁移到 qwen3-rerank。

**关键参数：**

- `model`（必选）：模型名称
- `query`（必选）：查询内容，qwen3-vl-rerank 支持文本和图片两种查询模态
- `documents`（必选）：待排序文档列表
- `top_n`（可选）：返回排序后的前 N 个文档
- `instruct`（可选）：自定义排序任务说明，可指导模型采用不同排序策略（仅 qwen3-rerank 和 qwen3-vl-rerank）

**不同模型使用不同 API 接口：**

- qwen3-rerank：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-api/v1/reranks`
- qwen3-vl-rerank / gte-rerank-v2：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank`

## [多模态](../concepts/multimodal.md)向量模型

[多模态](../concepts/multimodal.md)向量模型将文本、图像和视频转换为同一语义空间中的向量，支持跨模态检索（以文搜图、以图搜视频等）。详细 API 参见 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

**向量类型：**

- **独立向量**：为每个输入分别生成向量，适用于逐项对比
- **融合向量**：将所有输入融合为 1 个向量，适用于综合理解[多模态](../concepts/multimodal.md)内容

| 模型 | 默认维度 | 向量类型 | 说明 |
|------|---------|---------|------|
| qwen3-vl-embedding | 2560 | 独立/融合 | 通过 `enable_fusion` 开启融合，33 语种 |
| qwen2.5-vl-embedding | 1024 | 仅融合 | 不支持独立向量和多图 |
| tongyi-embedding-vision-plus-2026-03-06 | 1152 | 独立/融合 | Qwen3 底座，支持多分辨率 |
| tongyi-embedding-vision-flash-2026-03-06 | 768 | 独立/融合 | 轻量版 |
| multimodal-embedding-v1 | 1024 | 独立 | 固定维度，不支持 dimension 参数 |

**统一调用接口：** `POST https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`

## 使用限制与注意事项

- 所有模型调用前需获取 [API Key](../concepts/api-key.md) 并配置到环境变量 `DASHSCOPE_API_KEY`
- 向量模型的 `relevance_score` 为当前请求内的相对分数，不可跨请求比较
- 输入超长时会被截断，可能影响结果准确性
- 模型限流触发条件因模型而异，详见各模型限流说明
- 批处理任务数据保留 24 小时，需及时下载结果

## 来源文档

- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)



