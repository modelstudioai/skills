# vector and sort

百炼平台的 `vector and sort` 功能涵盖文本/多模态向量生成（embedding）与检索后重排序（rerank）两大核心能力，支撑语义搜索、RAG、跨模态检索等关键场景。向量模型将原始内容映射到统一语义空间，排序模型则对召回结果进行精细化相关性打分与重排，二者常组合使用以构建高精度检索系统。

## 支持的模型/功能

### 文本向量模型
- **同步接口**：支持 `qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3`、`text-embedding-v2`、`text-embedding-v1` 等，适用于低延迟、小批量（≤20 行）场景 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **异步批处理接口**：支持 `text-embedding-async-v2`（推荐）、`text-embedding-async-v1`，适用于超大批量（最高 100,000 行）文本向量化任务 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。

### 多模态向量模型
- 支持文本、图像、视频及其组合的联合向量化，所有模态共享同一语义空间，可直接计算跨模态余弦相似度。
- 模型包括 `qwen3-vl-embedding`（支持独立/融合向量）、`qwen2.5-vl-embedding`（仅融合）、`tongyi-embedding-vision-plus-2026-03-06`（新版，支持多分辨率与融合）、`multimodal-embedding-v1` 等 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

### 排序（Rerank）模型
- **文本排序**：`qwen3.7-text-rerank`（主力）、`qwen3-rerank`（轻量替代）、`gte-rerank-v2`（即将下线，[官方公告](https://www.aliyun.com/notice/118217) 明确建议迁移）。
- **多模态排序**：`qwen3-vl-rerank`，支持 text/image/video 混合查询与文档排序。

> **注意**：`gte-rerank` 系列模型（含 `gte-rerank-v2`）已进入下线周期，`gte-rerank` 将于 2026 年 05 月 30 日正式下线，新项目应优先选用 `qwen3-rerank` 或 `qwen3.7-text-rerank`。

## 关键参数

| 参数 | 适用模型 | 说明 |
|------|----------|------|
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06`, `tongyi-embedding-vision-flash-2026-03-06` | 指定向量维度（如 `1024`, `2048`），非所有模型均支持；`text-embedding-v2/v1` 和 `tongyi-embedding-vision-plus/flash`（非2026快照版）不支持此参数。 |
| `encoding_format` | 同步文本向量（OpenAI 兼容模式） | 控制返回格式为 `float` 或 `base64`，但受网关限制：老网关强制返回 `float`，新网关对长请求也降级为 `float` [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。 |
| `enable_fusion` | `qwen3-vl-embedding` | 启用后将 `contents` 中所有输入融合为单个向量；`qwen2.5-vl-embedding` 始终融合，无需该参数。 |
| `text_type` | 异步文本向量（`text-embedding-async-v1/v2`） | 指定为 `"query"` 或 `"document"`，用于优化检索类非对称任务效果。 |
| `instruct` | `qwen3.7-text-rerank`, `qwen3-rerank`, `qwen3-vl-rerank` | 自定义排序任务指令（如 `"Retrieve semantically similar text."`），显著影响排序逻辑，建议使用英文。 |

## 使用方式

### 向量生成
- **同步调用（小批量）**：使用 OpenAI 兼容 SDK 或 DashScope SDK，通过 `/embeddings` endpoint 发送请求。支持 `string`、`array<string>` 或文件流输入。示例：
  ```python
  client.embeddings.create(model="qwen3.7-text-embedding", input=["文本A", "文本B"], dimensions=1024)
  ```
- **异步批处理（大批量）**：需先提交任务（指定 `input.url` 指向文本文件），再轮询或等待 `task_id` 获取结果 URL。文件需满足：单行 ≤2048 [Token](../concepts/token.md)，总行数 ≤100,000，文件大小 ≤200MB [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **多模态向量**：HTTP 请求体中 `input.contents` 为对象数组，每个对象指定 `text`/`image`/`video`/`multi_images` 字段；融合向量需将多模态字段置于同一对象内（如 `{"text": "...", "image": "..."}`）或设置 `enable_fusion=true`。

### 排序（Rerank）
- 统一使用 `/services/rerank/text-rerank/text-rerank` endpoint。
- `input.query` 可为字符串（文本）或对象（`{"text": "..."}` 或 `{"image": "..."}`）；`input.documents` 为字符串或对象数组。
- 通过 `parameters.top_n` 控制返回数量，`parameters.return_documents=true` 可返回原文。

## 限制和注意事项

- **[Token](../concepts/token.md) 限制严格**：各模型对单条输入、单次请求总 [Token](../concepts/token.md) 有硬性上限（如 `text-embedding-v4` 单行 ≤8192 Token，`qwen3-vl-rerank` 请求总 Token ≤120,000），超限直接返回 HTTP 400 错误，**不会自动截断**。
- **地域与免费额度差异**：北京地域部分模型（如 `qwen3.7-text-embedding`）提供 100 万 Token 免费额度，而新加坡地域同名模型无免费额度；`text-embedding-async-v2` 在北京有 2000 万 Token 免费额度，新加坡未提及 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **[异步任务](../concepts/asynchronous-task.md)生命周期**：批处理任务结果 URL 有效期仅 **24 小时**，需及时下载；同时运行中任务数上限为 3 个，排队中+运行中总数不超过 50 个。
- **模型兼容性陷阱**：`tongyi-embedding-vision-plus`（非2026快照版）不支持 `dimension` 参数且固定 1152 维，而其快照版 `tongyi-embedding-vision-plus-2026-03-06` 支持灵活维度配置，混用易导致参数错误。
- **SDK 与 HTTP 参数结构差异**：DashScope SDK 对参数进行了扁平化封装（如 `TextReRank.call(query=..., documents=...)`），而 HTTP 接口要求嵌套在 `input` 和 `parameters` 对象中，开发时需严格对照文档。

## 来源文档

- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)
- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


