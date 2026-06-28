# vector and sort

百炼平台提供向量化（Embedding）与排序（Rerank）两类模型 API，用于把文本、图片、视频转换为数值向量并完成语义检索的召回与精排。向量模型覆盖通用文本、多模态（文本+图片+视频）以及批处理三种调用形态；排序模型则对召回结果做二次精排，支持纯文本与跨模态查询。本文汇总四类 API 的模型清单、关键参数、调用方式与限制。

## 能力概览

| 能力 | 典型模型 | 调用形态 | 接口路径 |
| --- | --- | --- | --- |
| 通用文本向量（同步） | text-embedding-v4 / v3 / v2 / v1 | OpenAI 兼容 / DashScope | `POST /compatible-mode/v1/embeddings` |
| 通用文本向量（批量） | text-embedding-async-v2 / v1 | 异步任务（创建+查询） | `POST /api/v1/services/embeddings/text-embedding/text-embedding` |
| 多模态向量 | qwen3-vl-embedding、tongyi-embedding-vision-*、multimodal-embedding-v1 | 同步 HTTP | `POST /api/v1/services/embeddings/multimodal-embedding/multimodal-embedding` |
| 文本/跨模态排序 | qwen3-rerank、qwen3-vl-rerank、gte-rerank-v2 | 同步 HTTP / SDK | `/compatible-api/v1/reranks` 或 `/api/v1/services/rerank/text-rerank/text-rerank` |

调用前需[获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key) 并配置到环境变量 `DASHSCOPE_API_KEY`；通过 SDK 调用还需[安装 DashScope SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。详见[同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。

## 通用文本向量

### 模型清单

| 模型 | 向量维度 | 最大行数 | 单行最大 [Token](../concepts/token.md) | 单价（每千输入 [Token](../concepts/token.md)） | 支持语种 |
| --- | --- | --- | --- | --- | --- |
| text-embedding-v4 | 2048、1536、1024（默认）、768、512、256、128、64 | 10 | 8,192 | 0.0005 元（Batch 0.00025 元） | 100+ 主流语种 |
| text-embedding-v3 | 1024（默认）、768、512、256、128、64 | 10 | 8,192 | 0.0005 元（Batch 0.00025 元） | 50+ 主流语种 |
| text-embedding-v2 | 1,536 | 25 | 2,048 | 0.0007 元（Batch 0.00035 元） | 9 种主流语种 |
| text-embedding-v1 | 1,536 | 25 | 2,048 | 0.0007 元（Batch 0.00035 元） | 6 种主流语种 |

text-embedding-v4 属于 Qwen3-Embedding 系列，支持最多语种与最灵活的维度选择；v3/v4 支持自定义 `dimensions`，v1/v2 固定 1536 维。各模型提供百炼开通后 90 天内的免费额度（v4/v3 各 100 万 [Token](../concepts/token.md)，v2/v1 各 50 万 Token）。模型限流规则参见[限流](https://help.aliyun.com/zh/model-studio/rate-limit)。

### 同步调用

OpenAI 兼容 base_url：`https://dashscope.aliyuncs.com/compatible-mode/v1`，endpoint：`POST /compatible-mode/v1/embeddings`。

关键请求参数：

- `model`（string，必选）：模型名称。
- `input`（string / array / file，必选）：待处理文本。v3/v4 字符串最长 8,192 Token，列表或文件最多 10 条，每条 8,192 Token；v1/v2 字符串最长 2,048 Token，列表或文件最多 25 条，每条 2,048 Token。
- `dimensions`（integer，可选）：向量维度，仅 v3/v4 支持，默认 1024。
- `encoding_format`（string，可选）：当前仅支持 `float`。

curl 示例：

```bash
curl --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/embeddings' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "text-embedding-v4",
    "input": "衣服的质量杠杠的，很漂亮，超喜欢",
    "dimensions": 1024,
    "encoding_format": "float"
}'
```

Python（OpenAI SDK）示例：

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

completion = client.embeddings.create(
    model="text-embedding-v4",
    input="衣服的质量杠杠的，很漂亮，超喜欢",
    dimensions=1024,
    encoding_format="float"
)
print(completion.model_dump_json())
```

`input` 也支持字符串列表（一次性向量化多条文本）和文件（`f` 对象或读取文件内容后传入）。成功响应在 `data[].embedding` 中返回向量数组，并附带 `usage.prompt_tokens` / `total_tokens`。

### 批处理接口

批量向量化仅支持异步模式，需两步完成：创建任务获取 `task_id`，再轮询查询结果。模型与限制见下表（详见[批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)）。

| 模型 | 向量维度 | 单次请求最大行数 | 单行最大 Token | 单价 | 同时处理任务数 |
| --- | --- | --- | --- | --- | --- |
| text-embedding-async-v2 | 1,536 | 100,000 | 2,048 | 0.0007 元 | 排队+运行≤50，并发≤3 |
| text-embedding-async-v1 | 1,536 | 100,000 | 2,048 | 0.0007 元 | 同上 |

创建任务必须携带请求头 `X-DashScope-Async: enable`，否则报错 "current user api does not [support](../guides/support.md) synchronous calls"。`input.url` 指向待向量化的文件（一行一条，单行≤2,048 Token，文件≤200MB）。`parameters.text_type` 可选 `document`（默认，适合聚类/分类）或 `query`（适合检索场景）。

```bash
curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -H 'X-DashScope-Async: enable' \
    -d '{
    "model": "text-embedding-async-v2",
    "input": {
        "url": "https://modelscope.oss-cn-beijing.aliyuncs.com/resource/text_embedding_file.txt"
    },
    "parameters": {
        "text_type": "query"
    }
}'
```

创建成功返回 `task_id` 与 `task_status: PENDING`。随后通过 `GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}` 查询，状态枚举：PENDING / RUNNING / SUCCEEDED / FAILED / CANCELED / UNKNOWN。任务数据（结果 URL 等）仅保留 24 小时，需及时保存。SDK（`BatchTextEmbedding`）封装了 `call`（同步等待）、`async_call` + `fetch`/`wait`/`cancel` 等方法，`cancel` 仅对 PENDING 状态任务有效。

## 多模态向量

多模态向量模型把文本、图片、视频编码到同一语义空间，支持以文搜图、以图搜视频、跨模态相似度计算与内容聚类。详见[Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

### 向量类型

- **独立向量**：为 `contents` 中每个输入分别生成一个向量（如 1 段文本+1 张图片返回 2 个向量），适合逐项对比。
- **融合向量**：将所有输入融合为 1 个向量，适合整体理解多模态内容。`qwen3-vl-embedding` 通过 `enable_fusion=true` 开启；`tongyi-embedding-vision-plus-2026-03-06` / `tongyi-embedding-vision-flash-2026-03-06` 通过把 text、image、video 放进同一个 content 对象实现融合。

模型兼容性：`qwen2.5-vl-embedding` 仅支持融合向量；`tongyi-embedding-vision-plus` / `flash` 仅支持独立向量；`multimodal-embedding-v1` 固定 1024 维且不支持 `dimension` 参数。

### 模型清单（北京）

| 模型 | 默认维度 | 文本长度 | 图片限制 | 视频限制 | 单价（每千 Token） |
| --- | --- | --- | --- | --- | --- |
| qwen3-vl-embedding | 2560 | 32,000 Token | 单张≤10 MB | ≤50 MB | 图片/视频 0.0018 元，文本 0.0007 元 |
| qwen2.5-vl-embedding | 1024 | — | 单张≤5 MB | — | — |
| tongyi-embedding-vision-plus-2026-03-06 | 1152 | 1,024 Token | 建议≤5 MB，最大 10 MB，最多 64 张 | ≤50 MB，H.264/H.265 | 0.0005 元 |
| tongyi-embedding-vision-flash-2026-03-06 | 768 | 1,024 Token | 同上 | 同上 | 0.00015 元 |
| tongyi-embedding-vision-plus | 1152 | 1,024 Token | 单张≤3 MB，最多 8 张 | ≤10 MB | 0.0005 元 |
| tongyi-embedding-vision-flash | 768 | 1,024 Token | 单张≤3 MB | ≤10 MB | 0.00015 元 |
| multimodal-embedding-v1 | 1024 | 512 Token | 单张≤3 MB | ≤10 MB | 图片/视频 0.0009 元，文本 0.0007 元 |

新加坡地域仅提供 `tongyi-embedding-vision-plus` 与 `tongyi-embedding-vision-flash`。

### 调用方式

endpoint：`POST https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`。

`input.contents` 是一个数组，每个元素用 key 指定模态：`text`（字符串）、`image`（URL 或 Base64 Data URI）、`video`（URL）、`multi_images`（多图序列，仅 tongyi-embedding-vision-plus/flash 及 2026-03-06 快照支持）。

独立向量示例（每个输入各自生成向量）：

```bash
curl --silent --location --request POST 'https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding' \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header 'Content-Type: application/json' \
    --data '{
        "model": "tongyi-embedding-vision-plus",
        "input": {
            "contents": [
                {"text": "多模态向量模型"},
                {"image": "https://img.alicdn.com/...jpg"},
                {"video": "https://help-static-aliyun-doc.aliyuncs.com/.../new+video.mp4"}
            ]
        }
    }'
```

融合向量示例（qwen3-vl-embedding 通过 `enable_fusion=true` 开启）：

```bash
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding' \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header 'Content-Type: application/json' \
    --data '{
        "model": "qwen3-vl-embedding",
        "input": {
            "contents": [
                {"text": "商品描述文本"},
                {"image": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/256_1.png"},
                {"video": "https://help-static-aliyun-doc.aliyuncs.com/.../new+video.mp4"}
            ]
        },
        "parameters": {"enable_fusion": true}
    }'
```

关键参数：`dimension`（指定维度，按模型支持范围）、`fps`（视频帧数比例，0–1，默认 1.0）、`instruct`（自定义任务说明，建议英文）、`res_level`（仅 2026-03-06 快照支持，0/1/2/3 档，默认 1）、`max_video_frames`（仅 2026-03-06 快照支持，最大 64，默认 8）。

### 单次请求条数限制

- `qwen3-vl-embedding`：内容元素总数≤20，图片≤5，视频≤1。
- `qwen2.5-vl-embedding`：图片、文本、视频、融合对象每种类型最多 1 次。
- `tongyi-embedding-vision-plus-2026-03-06` / `flash-2026-03-06`：内容元素总数≤20，图片≤64，视频≤8。
- `multimodal-embedding-v1`：内容元素总数≤20，图片/视频各最多 1 条，文本最多 20 条。

## 文本与跨模态排序

排序模型对召回阶段返回的候选文档进行二次精排，把与查询最相关的结果排在前面，提升检索与 RAG 应用的准确率。详见[文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。

> **注意**：`gte-rerank` 模型将于 2026 年 05 月 30 日下线，推荐使用 `qwen3-rerank` 替代。

### 模型清单

| 模型 | 最大文档数 | 单条最大输入 Token | 请求最大输入 Token | 语种 | 应用场景 |
| --- | --- | --- | --- | --- | --- |
| qwen3-vl-rerank | 文本 100 / 图片 40 / 视频 4 | 8,000 | 120,000 | 33 种主流语言 | 图像聚类、跨模态搜索、图片检索 |
| qwen3-rerank | 500 | 4,000 | — | 100+ 主流语种 | 文本语义检索、RAG |
| gte-rerank-v2 | 30,000 | — | — | 50 余语种 | 文本语义检索 |

请求最大输入 Token 的计算公式为 `Query Tokens × Document 数量 + Document Tokens 总和`，不得超过上限。超长输入将被截断，可能导致排序结果不准确。

### 接口差异

不同模型使用不同接口，请求体结构也不同：

- **qwen3-rerank**：`POST https://dashscope.aliyuncs.com/compatible-api/v1/reranks`，`query` 与 `documents` 直接与 `model` 同级，`top_n`、`instruct` 也为顶级参数。
- **qwen3-vl-rerank / gte-rerank-v2**：`POST https://dashscope.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank`，使用嵌套的 `input.query` / `input.documents` 与 `parameters` 结构。

qwen3-rerank 示例：

```bash
curl --request POST \
  --url https://dashscope.aliyuncs.com/compatible-api/v1/reranks \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "qwen3-rerank",
    "documents": [
        "文本排序模型广泛用于搜索引擎和推荐系统...",
        "量子计算是计算科学的一个前沿领域",
        "预训练语言模型的发展给文本排序模型带来了新的进展"
    ],
    "query": "什么是文本排序模型",
    "top_n": 2,
    "instruct": "Given a web search query, retrieve relevant passages that answer the query."
}'
```

### 关键参数

- `model`（必选）：qwen3-rerank / qwen3-vl-rerank / gte-rerank-v2。
- `query`（必选）：查询内容，最大 4,000 Token。qwen3-vl-rerank 支持字符串或 `{"text": ...}` / `{"image": ...}` 对象格式。
- `documents`（必选）：候选文档列表。qwen3-vl-rerank 每个元素用 `{"text"|"image"|"video": ...}` 指定模态，图片支持 URL 或 Base64，视频仅支持 URL。
- `top_n`（可选）：返回前 N 个文档，默认返回全部。
- `return_documents`（可选）：是否返回文档原文，默认 `false`，仅 gte-rerank-v2 / qwen3-vl-rerank 支持。
- `instruct`（可选，仅 qwen3-rerank / qwen3-vl-rerank）：自定义排序任务说明，建议英文。默认按问答检索任务排序；可设为 `"Retrieve semantically similar text."` 切换为语义相似度排序。
- `fps`（可选，仅 qwen3-vl-rerank）：视频帧数比例 0–1，默认 1.0。

### 响应结构

qwen3-rerank 响应中 `results` 直接位于顶层；qwen3-vl-rerank / gte-rerank-v2 响应包裹在 `output` 对象中。每个结果包含 `index`（对应输入文档索引）、`relevance_score`（0.0–1.0，按降序排列）。`relevance_score` 是本次请求内的相对分数，不可跨请求比较。SDK（`dashscope.TextReRank.call`）使用扁平参数，成功时固定返回空 `code` / `message`。

## 限制与注意事项

- **Token 与行数限制**：各模型对单行 Token、最大行数/文档数、文件大小有不同上限，超出将被截断或拒收。批处理文件单行≤2,048 Token、最大 100,000 行、文件≤200MB。
- **任务保留时长**：批处理任务数据仅保留 24 小时，超时自动清除，需及时拉取结果。
- **并发与限流**：批处理单个用户排队+运行任务≤50，并发运行≤3；任务下发接口 RPS 限制为 1。所有模型均受[限流](https://help.aliyun.com/zh/model-studio/rate-limit)约束。
- **接口不兼容**：qwen3-rerank 与 qwen3-vl-rerank / gte-rerank-v2 走不同 endpoint 且请求体结构不同，混用会报错。SDK 与 HTTP 参数命名相近但结构不同（HTTP 嵌套 `input`/`parameters`，SDK 扁平），开发时需区分。
- **下线计划**：gte-rerank 模型 2026 年 05 月 30 日下线，建议迁移到 qwen3-rerank。
- **地域差异**：多模态向量模型在新加坡地域仅提供 tongyi-embedding-vision-plus/flash，且新加坡查询结果 base_url 需替换为 `https://dashscope-intl.aliyuncs.com/api/v1/tasks/{task_id}`。
- **融合向量兼容性**：`qwen2.5-vl-embedding` 仅支持融合向量、不支持多图；`tongyi-embedding-vision-plus` / `flash` 仅支持独立向量；`multimodal-embedding-v1` 固定 1024 维、不支持 `dimension`。选型时务必核对模型能力对照表。

## 来源文档

- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)


