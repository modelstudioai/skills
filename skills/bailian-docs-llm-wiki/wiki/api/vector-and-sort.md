# vector and sort

百炼平台提供文本向量化（Embedding）和文本排序（Rerank）两类模型服务，覆盖通用文本向量、多模态向量和语义排序场景。这些模型可用于语义搜索、RAG 应用、推荐系统、聚类分类等下游任务，支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)和 DashScope 原生接口两种调用方式。

## 通用文本向量模型

通用文本向量模型将文本转换为数值向量，当前提供 4 个版本，详见[同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。

| 模型 | 向量维度 | 最大行数 | 单行最大 Token | 支持语种 |
|------|---------|---------|--------------|---------|
| text-embedding-v4（Qwen3-Embedding） | 2048/1536/1024(默认)/768/512/256/128/64 | 10 | 8,192 | 100+ 语种及编程语言 |
| text-embedding-v3 | 1024(默认)/768/512/256/128/64 | 10 | 8,192 | 50+ 语种 |
| text-embedding-v2 | 1536 | 25 | 2,048 | 中英等10语种 |
| text-embedding-v1 | 1536 | 25 | 2,048 | 中英等6语种 |

### 调用方式（[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)）

**base_url**: `https://dashscope.aliyuncs.com/compatible-mode/v1`

**请求体关键参数**：

- **model**（必选）：模型名称，如 `text-embedding-v4`
- **input**（必选）：输入文本，支持字符串、字符串列表或文件
- **dimensions**（可选）：向量维度，仅 v3/v4 支持，默认 1024
- **encoding_format**（可选）：返回格式，当前仅支持 `float`

调用示例（Python）：

```python
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)
completion = client.embeddings.create(
    model="text-embedding-v4",
    input="待向量化的文本",
    dimensions=1024,
    encoding_format="float"
)
```

> **注意**：`dimensions` 参数仅 text-embedding-v3 和 text-embedding-v4 支持。v1/v2 模型固定返回 1536 维向量。

### 批处理接口

对于大规模文本向量化场景，可使用异步批处理接口，单次最多处理 10 万行文本，详见[批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。批处理模型为 `text-embedding-async-v1` 和 `text-embedding-async-v2`。

批处理调用流程：
1. 创建异步任务，提交包含待向量化文本的文件 URL
2. 使用返回的 `task_id` 轮询任务状态
3. 任务完成后从返回的 URL 获取结果

HTTP 调用时必须设置请求头 `X-DashScope-Async: enable`，否则会报错。批处理接口支持 `text_type` 参数区分 `query`（查询文本）和 `document`（底库文本），检索场景下建议区分使用以获得更好效果。

## 多模态向量模型

多模态向量模型将文本、图像和视频转换为同一语义空间中的向量，支持跨模态检索（以文搜图、以图搜视频等），详见[Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

### 主要模型

| 模型 | 默认维度 | 向量类型 | 特点 |
|------|---------|---------|------|
| qwen3-vl-embedding | 2560 | 独立/融合 | 通过 `enable_fusion` 开启融合模式，33种语言 |
| qwen2.5-vl-embedding | 1024 | 仅融合 | 始终返回1个融合向量 |
| tongyi-embedding-vision-plus-2026-03-06 | 1152 | 独立/融合 | Qwen3底座，30+语言，支持 `res_level` |
| tongyi-embedding-vision-flash-2026-03-06 | 768 | 独立/融合 | 轻量版，价格更低 |
| tongyi-embedding-vision-plus | 1152 | 仅独立 | 支持多图序列（最多8张） |
| multimodal-embedding-v1 | 1024 | 仅独立 | 固定维度，不支持 `dimension` 参数 |

### 向量类型

- **独立向量**：为每个输入分别生成独立向量，适用于以图搜图、以文搜图等逐项对比场景
- **融合向量**：将所有输入融合为 1 个向量，适用于需要整体理解多模态内容的场景（如商品图+描述融合检索）

> **注意**：不同模型开启融合向量的方式不同。`qwen3-vl-embedding` 通过 `enable_fusion=true` 参数开启；`tongyi-embedding-vision-plus-2026-03-06` 等 2026-03-06 版本通过将 text/image/video 放在同一个 content 对象中实现，不使用 `enable_fusion` 参数。

### 多模态向量特有参数

- **dimension**：指定向量维度，不同模型支持范围不同
- **fps**：控制视频抽帧比例，范围 [0,1]，默认 1.0
- **enable_fusion**：是否生成融合向量（仅 qwen3-vl-embedding）
- **instruct**：自定义任务说明，建议英文撰写
- **res_level**：输入分辨率档位 0-3（仅 2026-03-06 版本），高分辨率可提升图像敏感场景效果 5%-10%
- **max_video_frames**：视频最大采样帧数上限，最大 64（仅 2026-03-06 版本）

## 文本排序模型（Rerank）

排序模型对召回的文档进行二次精排，确保最相关结果排在最前，详见[文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。

### 可用模型

| 模型 | 最大文档数 | 单条最大 Token | 请求最大 Token | 场景 |
|------|----------|--------------|--------------|------|
| qwen3-vl-rerank | 文本100/图片40/视频4 | 8,000 | 120,000 | 跨模态搜索、图片检索 |
| qwen3-rerank | 500 | 4,000 | 120,000 | 文本语义检索、RAG |
| gte-rerank-v2 | 500 | 4,000 | 30,000 | 多语种文本排序 |

> **注意**：gte-rerank 模型将于 2026 年 5 月 30 日下线，推荐使用 qwen3-rerank 替代。

### 调用差异

不同模型使用不同的 API 接口和请求格式：

- **qwen3-rerank**：`POST /compatible-api/v1/reranks`，`query`/`documents`/`top_n` 等参数与 `model` 同级
- **qwen3-vl-rerank / gte-rerank-v2**：`POST /api/v1/services/rerank/text-rerank/text-rerank`，参数嵌套在 `input` 和 `parameters` 中

### 关键参数

- **query**（必选）：查询内容。qwen3-vl-rerank 支持文本或图片查询
- **documents**（必选）：待排序文档列表。qwen3-vl-rerank 支持 text/image/video 多模态文档
- **top_n**（可选）：返回排序后的前 N 个文档
- **instruct**（可选）：自定义排序任务说明，默认按问答检索排序，也可设置为语义相似度排序
- **return_documents**（可选）：是否返回文档原文，默认 false

## 前提条件

所有向量和排序模型的调用都需要：

1. [获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)
2. [配置 API Key 到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)
3. 如使用 SDK，需要[安装 DashScope SDK](https://help.aliyun.com/zh/model-studio/install-sdk)

## 限制与注意事项

- 输入内容超过模型 Token 上限时会被截断，可能影响结果准确性
- Rerank 的 `relevance_score` 是当前请求内的相对分数，不可跨请求比较
- 批处理任务数据（状态、结果 URL 等）仅保留 24 小时，需及时下载结果
- 各模型均有限流策略，详见限流文档
- 多模态模型的图片支持 URL 和 Base64 两种方式，视频仅支持 URL

## 来源文档

- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


