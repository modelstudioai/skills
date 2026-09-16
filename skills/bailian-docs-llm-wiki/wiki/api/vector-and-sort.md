# vector and sort

百炼平台提供文本向量（vector）与排序（rerank）两类核心语义理解能力，分别用于将非结构化内容映射到统一语义空间，以及对召回结果进行精细化相关性重排序。二者常组合使用构建端到端检索系统（如 RAG），支持同步/异步调用、多模态输入及细粒度参数控制。

## 支持的模型/功能

### 文本向量化
- **同步接口**：支持 `qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3` 等通用文本模型，适用于低延迟场景（如实时搜索）。详细参数见 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **批处理接口**：支持 `text-embedding-async-v2`（100,000 行/请求）等异步模型，适用于大规模离线向量化任务 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **多模态向量化**：`qwen3-vl-embedding`、`tongyi-embedding-vision-plus-2026-03-06` 等模型支持文本、图像、视频混合输入，可生成独立向量或融合向量 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

### 排序（Rerank）
- **文本排序**：`qwen3-rerank`（推荐替代已下线的 `gte-rerank`）、`qwen3.7-text-rerank` 支持高精度语义相关性打分。
- **多模态排序**：`qwen3-vl-rerank` 支持文本/图像/视频混合查询与文档排序，适用于跨模态检索场景。

> **注意**：`gte-rerank` 系列模型将于 2026 年 05 月 30 日下线，新项目请直接使用 `qwen3-rerank` [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。

## 关键参数

| 参数 | 适用模型 | 说明 |
|--------|-----------|------|
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding` 等 | 指定向量维度（如 `1024`, `2048`），部分旧模型（如 `text-embedding-v2`）不支持。 |
| `encoding_format` | 同步文本向量模型 | 控制返回格式为 `float` 或 `base64`；但[同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)明确指出：老网关强制返回 `float`，长请求亦回退至老网关。 |
| `enable_fusion` | `qwen3-vl-embedding` | 设为 `true` 时将多模态输入融合为单个向量；`qwen2.5-vl-embedding` 仅支持融合模式且无此参数。 |
| `instruct` | `qwen3.7-text-rerank`, `qwen3-rerank`, `qwen3-vl-rerank` | 自定义排序任务指令（如 `"Retrieve semantically similar text."`），显著影响排序策略。 |
| `text_type` | 异步文本向量模型（`text-embedding-async-v2`） | 区分 `query`（查询）与 `document`（底库），提升检索效果。 |

## 使用方式

- **同步调用（文本向量）**：使用 OpenAI 兼容 SDK 或 HTTP POST 到 `/compatible-mode/v1/embeddings`，支持字符串、字符串列表、文件输入。示例：
  ```python
  client.embeddings.create(model="qwen3.7-text-embedding", input=["hello", "world"], dimensions=1024)
  ```
- **异步调用（文本向量）**：通过 `/api/v1/services/embeddings/text-embedding/text-embedding` 提交任务，再轮询 `/api/v1/tasks/{task_id}` 获取结果。需设置 `X-DashScope-Async: enable` 头 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **多模态向量**：HTTP POST 到 `/services/embeddings/multimodal-embedding/multimodal-embedding`，`input.contents` 中按模态类型组织数据（如 `{"text": "...", "image": "url"}`）。
- **排序模型**：`qwen3-rerank` 使用 OpenAI 兼容 `/compatible-api/v1/reranks` 接口；其余模型使用 `/api/v1/services/rerank/text-rerank/text-rerank`，`query` 和 `documents` 均嵌套在 `input` 对象中。

## 限制和注意事项

- **输入长度限制差异大**：`qwen3.7-text-embedding` 单行支持 128,000 Token，而 `text-embedding-v4` 仅支持 8,192 Token；`qwen3-rerank` 单条文档限 4,000 Token，`qwen3.7-text-rerank` 则达 30,000 Token。务必按模型文档校验输入。
- **地域与免费额度差异**：北京地域部分模型（如 `qwen3.7-text-embedding`）提供 100 万 Token 免费额度，新加坡地域同名模型无免费额度 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **异步任务生命周期**：批处理任务结果 URL 仅保留 24 小时，需及时下载；同时运行中任务数上限为 3 个，排队中+运行中总数不超过 50 个 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **多模态融合约束**：`tongyi-embedding-vision-plus-2026-03-06` 的融合向量要求 `text`/`image`/`video` 在同一 `content` 对象内，而非 `enable_fusion=true` —— 此参数仅 `qwen3-vl-embedding` 支持 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

## 来源文档

- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


