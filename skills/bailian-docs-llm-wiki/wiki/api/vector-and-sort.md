# vector and sort

百炼平台提供文本向量化（vector）、多模态向量化及文本/跨模态排序（sort / rerank）三大核心能力，支撑语义搜索、RAG、聚类、跨模态检索等下游任务。所有能力均通过同步/异步 HTTP API 与 [OpenAI 兼容接口](../concepts/openai-compatibility.md)提供，支持灵活的维度控制、输入格式与语种适配。

## 支持的模型与功能

### 文本向量模型
- **通用文本向量**：支持 `qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3` 等多版本，覆盖 201 种语种，向量维度可选（如 256–2560），详见 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **批处理异步向量**：`text-embedding-async-v1/v2` 专为大规模文本设计，单次支持最多 100,000 行，文件上限 200MB，适用于离线建库场景 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。

### 多模态向量模型
- 支持文本、图像、视频统一语义空间表征，提供**独立向量**（每模态各生成 1 向量）与**融合向量**（多模态输入合成 1 向量）两种模式。
- 主流模型包括 `qwen3-vl-embedding`（支持 `enable_fusion`）、`tongyi-embedding-vision-plus-2026-03-06`（支持同 content 融合）等，详见 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

### 排序（Rerank）模型
- **文本排序**：`qwen3.7-text-rerank`（推荐替代已下线的 `gte-rerank`）、`qwen3-rerank`，支持最多 500 文档/请求，语种覆盖超 100 种。
- **多模态排序**：`qwen3-vl-rerank` 支持 text/image/video 混合查询与文档，最大文档数按模态类型差异化限制（文本 100、图片 40、视频 4）。

> **注意**：文档 7 明确指出 `gte-rerank` 模型将于 2026 年 05 月 30 日下线，且 `qwen3-rerank` 已成为主力文本排序模型；但文档 2 中仍列出 `text-embedding-v2/v1` 等旧版向量模型，其免费额度与限流策略已不适用于新用户，实际应优先选用 `qwen3.7-text-embedding` 或 `text-embedding-v4`。

## 关键参数

| 参数 | 适用模型 | 说明 |
|--------|-----------|------|
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06` 等 | 指定向量维度（如 `1024`, `2048`），非所有模型均支持；`multimodal-embedding-v1` 和 `tongyi-embedding-vision-plus` 固定维度，不可配置。 |
| `encoding_format` | 同步文本向量（`text-embedding-*`） | 控制返回格式为 `float` 或 `base64`；但[同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)明确说明：老网关强制返回 `float`，长请求亦自动降级至老网关。 |
| `enable_fusion` | `qwen3-vl-embedding` | 布尔值，启用后将 `contents` 中所有输入融合为单一向量；`qwen2.5-vl-embedding` 无此参数（仅融合），`tongyi-2026-03-06` 系列通过同 content 结构隐式融合。 |
| `instruct` | `qwen3.7-text-rerank`, `qwen3-rerank`, `qwen3-vl-rerank` | 自定义排序任务指令（如 `"Retrieve semantically similar text."`），显著影响相关性判断逻辑。 |
| `text_type` | `text-embedding-async-v1/v2` | 区分 `query`（查询）与 `document`（底库），对检索类任务效果提升明显。 |

## 使用方式

### 同步调用（文本向量）
- **OpenAI 兼容**：使用 `base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"`，调用 `client.embeddings.create()`，支持 `input` 为字符串、字符串列表或文件对象。
- **DashScope HTTP**：`POST /api/v1/services/embeddings/text-embedding/text-embedding`，需在请求头中设置 `X-DashScope-Async: disable`（默认）。

### 异步调用（批量向量）
- **HTTP 两步法**：先 `POST /api/v1/services/embeddings/text-embedding/text-embedding` 创建任务（必须带 `X-DashScope-Async: enable`），再 `GET /api/v1/tasks/{task_id}` 轮询结果。
- **SDK 封装**：`dashscope.Client().embeddings.jobs.create()` 支持同步等待（`.wait()`）或异步轮询（`.fetch()`），简化状态管理。

### 多模态与排序
- **多模态向量**：统一 endpoint `POST /api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`，`input.contents` 数组支持混合 `{"text":...}`, `{"image":...}`, `{"video":...}` 及 `{"multi_images":[...]}`。
- **排序模型**：`POST /api/v1/services/rerank/text-rerank/text-rerank`，`input.query` 与 `input.documents` 为必填对象；`qwen3-rerank` 和 `qwen3.7-text-rerank` 额外支持 OpenAI 兼容 rerank 接口（`/compatible-api/v1/reranks`）。

## 限制和注意事项

- **Token 与行数限制**：
  - `qwen3.7-text-embedding`：单行最长 128,000 Token，最多 20 行；`text-embedding-v4`：单行 8,192 Token，最多 10 行。
  - `text-embedding-async-v2`：单次请求最多 100,000 行，单行 ≤ 2,048 Token。
  - `qwen3-vl-rerank`：单次请求总 Token 上限 120,000，计算公式为 `Query Tokens × Document 数 + Document Tokens 总和`。

- **地域与计费差异**：
  - 北京地域部分模型（如 `qwen3.7-text-embedding`）提供 100 万 Token 免费额度，有效期 90 天；新加坡地域同名模型通常无免费额度，单价略高（如 `0.000525元/千Token` vs `0.0005元`）。

- **兼容性与网关行为**：
  > **注意**：`encoding_format` 参数在[同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)中被明确标注为“老网关不支持 `base64` 输出”，且长请求会自动路由至老网关——这意味着生产环境中若需 `base64` 格式，必须确保输入极短并确认网关版本，否则将静默降级为 `float`。

- **模型弃用**：`gte-rerank` 系列已进入下线倒计时，新项目务必迁移至 `qwen3-rerank`；`text-embedding-v1/v2` 缺少免费额度且性能落后，应避免选用。

## 来源文档

- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)
- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


