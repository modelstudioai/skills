# vector and sort

本页汇总百炼平台"向量化与排序"类模型的 API 参考，覆盖通用文本向量（同步/批处理）、[多模态](../concepts/multimodal.md)向量以及文本排序（rerank）四组接口。所有接口均通过 [API Key](../concepts/api-key.md)（环境变量 `DASHSCOPE_API_KEY`）鉴权，HTTP 端点中的 `{WorkspaceId}` 需替换为真实的[业务空间](../concepts/workspace.md) ID。

## 通用文本向量（Text Embedding）

### 模型与规格

同步接口支持以下模型（详见[同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)）：

| 模型 | 向量维度 | 单行最大 [Token](../concepts/token.md) | 最大行数 | 单价（千 [Token](../concepts/token.md)） |
| --- | --- | --- | --- | --- |
| qwen3.7-text-embedding | 2560/2048/1536/1024（默认）/768/512/256 | 128,000 | 20 | 0.0005 元 |
| text-embedding-v4 | 2048/1536/1024（默认）/768/512/256/128/64 | 8,192 | 10 | 0.0005 元 |
| text-embedding-v3 | 1024（默认）/768/512/256/128/64 | 8,192 | 10 | 0.0005 元 |
| text-embedding-v2 | 1,536 固定 | 2,048 | 25 | 0.0007 元 |
| text-embedding-v1 | 1,536 固定 | 2,048 | 25 | 0.0007 元 |

### 调用方式

- **OpenAI 兼容**：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/embeddings`，请求体包含 `model`、`input`（字符串/字符串列表/文件）、`dimensions`（仅 v3/v4 及 qwen3.7 支持）、`encoding_format`（仅 `float`）。
- 输入既支持单条字符串，也支持字符串列表；Python SDK 还支持直接传入文件对象。

### 批处理接口

大规模离线向量化使用异步批处理（详见[批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)）：

- 模型：`text-embedding-async-v1` / `text-embedding-async-v2`，单次请求最多 100,000 行、单行最长 2,048 [Token](../concepts/token.md)、文件不超过 200 MB。
- HTTP 仅支持异步：创建任务时必须携带请求头 `X-DashScope-Async: enable`（缺失会报 "current user api does not [support](../guides/support.md) synchronous calls"），随后用 `GET .../api/v1/tasks/{task_id}` 轮询结果。
- 任务数据仅保留 24 小时，需及时下载结果 URL；[限流](../concepts/rate-limit.md)：任务下发 RPS 为 1，并发运行作业最多 3 个，排队+运行总数不超过 50。
- 参数 `text_type` 区分 `query` / `document`（默认 `document`），非对称检索场景建议显式区分。

> **注意**：批处理接口文档中"查询结果"部分将 `url` 字段描述为"模型生成图片的URL地址"，系从图像类文档复制而来的笔误，实际为向量结果文件的下载地址。

## [多模态](../concepts/multimodal.md)向量（Multimodal Embedding）

将文本、图片、视频映射到同一语义空间，支持跨模态检索、相似度计算与聚类（详见[Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)）。

- 端点：`POST https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`。
- 输入：`input.contents` 数组，元素支持 `text`、`image`（URL 或 Base64 Data URI）、`video`（仅 URL）、`multi_images`（仅 tongyi 系列支持）。
- 向量类型：
  - **独立向量**：每个输入各生成一个向量；
  - **融合向量**：`qwen3-vl-embedding` 通过 `parameters.enable_fusion=true` 开启；`tongyi-embedding-vision-*-2026-03-06` 通过将 text/image/video 放入**同一个 content 对象**实现，不使用 `enable_fusion`；`qwen2.5-vl-embedding` 仅支持融合向量。
- 关键参数：`dimension`（各模型可选值不同，`multimodal-embedding-v1` 与旧版 tongyi 系列固定维度）、`fps`（视频抽帧比例）、`instruct`（英文任务说明，约 1%–5% 效果提升）、`res_level` 与 `max_video_frames`（仅 2026-03-06 快照版本）。
- 请求条数限制因模型而异，例如 `qwen3-vl-embedding` 单次内容元素不超过 20、图片不超过 10 张、视频不超过 1 个。

## 文本排序（Rerank）

对召回结果做二次精排，提升 RAG 与搜索的相关性（详见[文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)）。

### 模型与接口

| 模型 | 端点 | 特点 |
| --- | --- | --- |
| qwen3-rerank | `POST .../compatible-api/v1/reranks` | 最多 500 文档，单条 4,000 [Token](../concepts/token.md)，请求上限 120,000 [Token](../concepts/token.md)，100+ 语种 |
| qwen3-vl-rerank | `POST .../api/v1/services/rerank/text-rerank/text-rerank` | [多模态](../concepts/multimodal.md)（文本 100 / 图片 40 / 视频 4），query 支持 text 或 image |
| gte-rerank-v2 | 同上 | 50+ 语种 |

> **注意**：gte-rerank 模型将于 **2026 年 5 月 30 日下线**，请迁移到 qwen3-rerank。

### 请求结构差异

- **qwen3-rerank** 使用扁平结构：`query`、`documents`、`top_n`、`instruct` 与 `model` 同级，响应中 `results` 位于顶层。
- **qwen3-vl-rerank / gte-rerank-v2** 使用嵌套结构：`input.query` / `input.documents` + `parameters.top_n` / `return_documents` / `fps`，响应位于 `output.results`。
- `instruct` 用于声明排序任务类型（如问答检索或语义相似度），建议英文撰写，仅 qwen3 系列生效。
- `relevance_score` 取值 0–1，是**当前请求内的相对分数**，不可跨请求比较。
- [DashScope SDK](../concepts/dashscope-sdk.md) 将参数扁平化封装（如 `dashscope.TextReRank.call(model=..., query=..., documents=..., top_n=...)`），与 HTTP 嵌套结构不同，开发时注意区分。

## 通用注意事项

- 调用前需获取并配置 [API Key](../concepts/api-key.md)；SDK 调用需安装 [DashScope SDK](../concepts/dashscope-sdk.md)。
- 不同地域 URL 不同（北京为 `cn-beijing`，新加坡为 `ap-southeast-1`），调用时替换 `{WorkspaceId}`。
- 输入超长会被截断，可能影响向量/排序质量，请按模型的 [Token](../concepts/token.md) 上限切分文本。
- 各模型[限流](../concepts/rate-limit.md)规则参见百炼[限流](../concepts/rate-limit.md)文档；错误码对照参见百炼错误码文档。

## 来源文档

- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)





