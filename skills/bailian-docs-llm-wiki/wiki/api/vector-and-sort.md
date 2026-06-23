# vector and sort

百炼平台提供向量化（Embedding）与排序（Rerank）两大类模型 API，用于将文本、图像、视频转换为数值向量，或对召回文档进行二次精排。这些能力广泛应用于语义搜索、RAG、推荐、聚类、分类等场景。本页汇总了通用文本向量、多模态向量和排序模型的核心参数与调用方式。

## 通用文本向量模型

通用文本向量模型将文本转换为固定维度的数值向量。百炼目前提供 text-embedding-v1 到 v4 四代模型，详见[同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。

### 模型选型

| 模型 | 向量维度 | 最大行数 | 单行最大 Token | 单价（每千 Token） | 语种 |
|------|---------|---------|--------------|------------------|------|
| text-embedding-v4 | 2048/1536/1024(默认)/768/512/256/128/64 | 10 | 8,192 | 0.0005 元 | 100+ 语种 |
| text-embedding-v3 | 1024(默认)/768/512/256/128/64 | 10 | 8,192 | 0.0005 元 | 50+ 语种 |
| text-embedding-v2 | 1536 | 25 | 2,048 | 0.0007 元 | 10 语种 |
| text-embedding-v1 | 1536 | 25 | 2,048 | 0.0007 元 | 6 语种 |

- text-embedding-v4 属于 Qwen3-Embedding 系列，推荐优先使用。
- `dimensions` 参数仅 v3 和 v4 支持，可灵活指定输出维度。

### 调用方式

支持 [OpenAI 兼容接口](../concepts/openai-compatible.md)和 DashScope 原生接口两种方式：

**[OpenAI 兼容接口](../concepts/openai-compatible.md)** — endpoint: `POST https://dashscope.aliyuncs.com/compatible-mode/v1/embeddings`

```python
from openai import OpenAI
import os

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

输入支持三种形式：单个字符串、字符串列表（v3/v4 最多 10 条，v1/v2 最多 25 条）、文件对象。

### 批处理接口

对于大批量文本向量化场景，可使用异步批处理模型 `text-embedding-async-v1` / `text-embedding-async-v2`，单次最多支持 100,000 行文本。批处理需通过两步完成：先创建任务获取 task_id，再轮询查询结果。详见[批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。

> **注意**：批处理接口必须在 HTTP 请求头中设置 `X-DashScope-Async: enable`，否则将报错。批处理模型不支持 `dimensions` 参数，固定返回 1536 维向量。

## 多模态向量模型

多模态向量模型支持将文本、图像和视频转换为同一语义空间中的向量，实现跨模态检索（以文搜图、以图搜视频等）。详见[Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

### 主要模型

| 模型 | 默认维度 | 向量类型 | 特点 |
|------|---------|---------|------|
| qwen3-vl-embedding | 2560 | 独立/融合 | 33种语言，通过 `enable_fusion` 开启融合模式 |
| qwen2.5-vl-embedding | 1024 | 仅融合 | 仅返回 1 个融合向量 |
| tongyi-embedding-vision-plus-2026-03-06 | 1152 | 独立/融合 | Qwen3 底座，支持多分辨率 `res_level` |
| tongyi-embedding-vision-flash-2026-03-06 | 768 | 独立/融合 | 轻量版，价格更低（0.00015 元/千 Token） |
| multimodal-embedding-v1 | 1024 | 仅独立 | 固定维度，不支持 `dimension` 参数 |

### 向量类型

- **独立向量**：为每个输入（文本/图片/视频）分别生成独立向量，适合逐项检索。
- **融合向量**：将多模态输入融合为 1 个向量，适合需要综合理解多模态内容的场景。

调用 endpoint: `POST https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`

### 关键参数

| 参数 | 说明 | 适用模型 |
|------|------|---------|
| `dimension` | 输出向量维度 | 除 multimodal-embedding-v1 / tongyi-plus/flash 外均支持 |
| `enable_fusion` | 是否生成融合向量 | 仅 qwen3-vl-embedding |
| `res_level` | 输入分辨率档位（0-3） | 仅 2026-03-06 版本 |
| `max_video_frames` | 视频最大采样帧数（上限 64） | 仅 2026-03-06 版本 |
| `instruct` | 自定义任务说明 | qwen3-vl-embedding 等 |

## 排序模型（Rerank）

排序模型对召回阶段返回的文档进行二次精排，确保最相关结果排在最前。详见[文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。

### 模型选型

| 模型 | 最大文档数 | 单条最大 Token | 请求最大 Token | 语种 | 应用场景 |
|------|-----------|--------------|--------------|------|---------|
| qwen3-vl-rerank | 文本100/图片40/视频4 | 8,000 | 120,000 | 33种语言 | 跨模态搜索、图片检索 |
| qwen3-rerank | 500 | 4,000 | - | 100+ 语种 | 文本语义检索、RAG |
| gte-rerank-v2 | - | - | 30,000 | 50+ 语种 | 文本排序 |

> **注意**：gte-rerank 模型将于 2026 年 05 月 30 日下线，推荐迁移到 qwen3-rerank。

### 调用方式

不同模型使用不同的 API 接口：

- **qwen3-rerank**: `POST https://dashscope.aliyuncs.com/compatible-api/v1/reranks`
- **qwen3-vl-rerank / gte-rerank-v2**: `POST https://dashscope.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank`

qwen3-rerank 的请求体较为扁平（`query`、`documents`、`top_n` 等与 `model` 同级），而其他模型需将输入包装在 `input` 对象中。

### 关键参数

| 参数 | 说明 |
|------|------|
| `top_n` | 返回排序后的前 N 个文档，默认返回全部 |
| `return_documents` | 是否返回文档原文（仅 gte-rerank-v2 / qwen3-vl-rerank） |
| `instruct` | 自定义排序策略说明（仅 qwen3-rerank / qwen3-vl-rerank） |
| `fps` | 视频帧采样率，范围 [0,1]（仅 qwen3-vl-rerank） |

`instruct` 参数可切换排序策略：默认为问答检索（侧重找答案），也可设为语义相似度排序（侧重含义等价性）。建议用英文撰写。

## 前提条件

所有向量与排序模型的调用均需要：

1. [获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key) 并配置到环境变量 `DASHSCOPE_API_KEY`
2. 使用 SDK 调用时需[安装 DashScope SDK](https://help.aliyun.com/zh/model-studio/install-sdk)
3. 使用 [OpenAI 兼容接口](../concepts/openai-compatible.md)时需设置 `base_url` 为 `https://dashscope.aliyuncs.com/compatible-mode/v1`

## 限制与注意事项

- 输入超过模型最大 Token 限制时会被截断，可能影响向量质量或排序准确性。
- Rerank 模型返回的 `relevance_score` 是当前请求内的相对分数，不可跨请求比较。
- 批处理任务数据保留 24 小时，请及时下载结果。
- 各模型的并发限制不同，超出会触发限流，详见限流文档。

## 来源文档

- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)




