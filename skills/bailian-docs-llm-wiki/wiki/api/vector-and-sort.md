# vector and sort

百炼平台提供文本向量（vector）与排序（rerank）两类核心语义理解能力，分别用于将非结构化内容映射到统一语义空间，以及对召回结果进行精细化相关性重排。二者常协同用于RAG、搜索、推荐等场景：先通过向量模型生成嵌入实现高效召回，再用排序模型对Top-K结果进行精准打分排序。所有模型均支持多语种输入，并提供同步/异步两种调用方式。

## 支持的模型/功能

### 文本向量模型
- **同步接口**：支持 `qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3`、`text-embedding-v2`、`text-embedding-v1` 等通用文本向量模型，适用于低延迟、小批量（≤20行）场景 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **异步批处理**：支持 `text-embedding-async-v2`（最大10万行/次）和 `text-embedding-async-v1`，适用于大规模离线向量化任务 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **[多模态](../concepts/multimodal.md)向量**：支持 `qwen3-vl-embedding`、`tongyi-embedding-vision-plus-2026-03-06` 等模型，可对文本、图像、视频生成统一语义空间的向量，支持独立向量与融合向量两种模式 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

### 排序（Rerank）模型
- **文本排序**：`qwen3-rerank`（推荐替代已下线的 `gte-rerank`）、`qwen3.7-text-rerank`，适用于纯文本检索重排。
- **[多模态](../concepts/multimodal.md)排序**：`qwen3-vl-rerank`，支持文本/图片/视频混合查询与文档的跨模态重排。
- **注意**：`gte-rerank` 系列模型（如 `gte-rerank-v2`）将于2026年05月30日下线，新项目请直接使用 `qwen3-rerank` [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。

## 关键参数

| 参数 | 适用模型 | 说明 |
|--------|-----------|------|
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06` 等 | 指定向量维度（如 `1024`, `2048`），不同模型支持值不同；`text-embedding-v2/v1` 和 `multimodal-embedding-v1` 不支持此参数，固定维度。 |
| `encoding_format` | 同步文本向量（`qwen3.7-text-embedding` 等） | 控制返回格式为 `float` 或 `base64`；但[同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)明确指出：老网关始终返回 `float`，长请求也强制路由至老网关，实际 `base64` 不可用。 |
| `enable_fusion` | `qwen3-vl-embedding` | 开启后将[多模态](../concepts/multimodal.md)输入融合为单个向量；`qwen2.5-vl-embedding` 无此参数（仅支持融合），而 `tongyi-embedding-vision-plus-2026-03-06` 通过将 text/image/video 放在同一 content 对象中实现融合，不依赖该参数。 |
| `instruct` | `qwen3.7-text-rerank`, `qwen3-rerank`, `qwen3-vl-rerank` | 自定义排序任务指令（如 `"Retrieve semantically similar text."`），显著影响排序逻辑，建议显式指定。 |
| `text_type` | 异步文本向量（`text-embedding-async-v2`） | 区分 `query`（查询）与 `document`（底库），对检索类任务效果提升明显。 |

## 使用方式

- **同步调用（文本向量）**：使用 OpenAI 兼容 SDK 或 HTTP POST 到 `compatible-mode/v1/embeddings`，支持字符串、字符串列表或文件输入。示例：
  ```python
  client.embeddings.create(model="qwen3.7-text-embedding", input="你好世界", dimensions=1024)
  ```
- **异步调用（文本向量）**：通过 `X-DashScope-Async: enable` 头发起任务，再轮询 `GET /api/v1/tasks/{task_id}` 获取结果；SDK 提供 `BatchTextEmbedding.async_call()` 封装 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **多模态向量**：HTTP 请求体 `input.contents` 数组中按需组合 `{"text":...}`, `{"image":...}`, `{"video":...}` 等对象；融合向量需确保多模态内容在同一 `content` 对象内（如 `tongyi-embedding-vision-plus-2026-03-06`）或设置 `enable_fusion=true`（如 `qwen3-vl-embedding`）。
- **排序模型**：注意接口路径差异——`qwen3-rerank` 使用 `/compatible-api/v1/reranks`（扁平参数），其余模型使用 `/api/v1/services/rerank/...`（嵌套 `input` 结构）。`qwen3-vl-rerank` 的 `query` 和 `documents` 均支持模态对象（如 `{"image": "url"}`）。

## 限制和注意事项

- **[Token](../concepts/token.md) 与行数限制**：同步文本向量中，`qwen3.7-text-embedding` 单行最长 128,000 [Token](../concepts/token.md)，最多 20 行；而 `text-embedding-v4` 单行仅限 8,192 [Token](../concepts/token.md)，最多 10 行。异步批处理 `text-embedding-async-v2` 支持单次 10 万行，但单行上限仅 2,048 Token。务必根据数据长度选择合适模型。
- **地域与免费额度差异**：北京地域部分模型（如 `qwen3.7-text-embedding`）提供 100 万 Token 免费额度，而新加坡地域同名模型无免费额度 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。部署前需确认地域策略。
- **模型兼容性陷阱**：`text-embedding-v2` 在文档1中列为北京地域支持，但在文档3的异步模型列表中未出现，且其同步版最大行数（25）高于 `v4`（10）但低于 `qwen3.7-text-embedding`（20），属中等容量模型；而 `text-embedding-async-v2` 是专为异步设计的高吞吐模型，二者不可混用。开发时应严格按调用方式（同步/异步）匹配模型系列。
- **多模态输入约束**：`qwen2.5-vl-embedding` 仅支持单文本+单图+单视频组合（各1次），不支持多图或多视频；而 `tongyi-embedding-vision-plus-2026-03-06` 支持最多 64 张图片和 8 个视频 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

## 来源文档

- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


