# vector and sort

百炼平台提供文本向量化（vector）与文本/[多模态](../concepts/multi-modal.md)排序（sort/rerank）两类核心能力，支撑语义搜索、RAG、跨模态检索等下游任务。文本向量模型将输入转换为稠密向量，支持同步与异步批量调用；排序模型则对召回结果进行精细化相关性重排。两类能力均覆盖多语言、[多模态](../concepts/multi-modal.md)场景，并提供灵活的维度控制、输入格式与计费策略。

## 支持的模型/功能

- **文本向量模型**：包括 `qwen3.7-text-embedding`（高维、长上下文）、`text-embedding-v4`（Qwen3-Embedding 系列，100+语种及编程语言）、`text-embedding-v3/v2/v1` 及轻量版 `qwen3.7-text-embedding-flash`；还提供异步批处理专用模型 `text-embedding-async-v1/v2` [原文标题](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **[多模态](../concepts/multi-modal.md)向量模型**：支持文本、图像、视频统一语义空间表征，涵盖 `qwen3-vl-embedding`（支持独立/融合向量）、`tongyi-embedding-vision-plus-2026-03-06`（新版Qwen3底座，支持多分辨率与融合）、`multimodal-embedding-v1` 等 [原文标题](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。
- **排序（Rerank）模型**：`qwen3-rerank`（推荐主力，OpenAI兼容接口）、`qwen3.7-text-rerank`（高精度文本排序）、`qwen3-vl-rerank`（跨模态排序）、`gte-rerank-v2`（即将下线，[原文标题](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md) 中明确提示 2026年05月30日停用）。

> **注意**：`gte-rerank` 系列模型已进入下线流程，文档 6 明确要求迁移至 `qwen3-rerank`；而文档 7 仅作入口索引，未体现该关键变更，应以文档 6 为准。

## 关键参数

| 参数 | 适用模型 | 说明 |
|------|----------|------|
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06` 等 | 指定向量维度（如 `1024`, `2048`, `2560`），不同模型支持范围不同；部分模型（如 `tongyi-embedding-vision-plus`）不支持该参数，固定维度。 |
| `encoding_format` | 同步文本向量 API（`text-embedding-synchronous-api.md`） | 控制返回格式为 `float` 或 `base64`；但需注意：老网关强制返回 `float`，长请求亦路由至老网关 [原文标题](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。 |
| `enable_fusion` | `qwen3-vl-embedding` | 布尔值，启用后将 `contents` 中所有模态输入融合为单个向量；其他模型（如 `tongyi-embedding-vision-plus-2026-03-06`）通过将 `text`/`image`/`video` 放入同一 `content` 对象实现融合，不使用此参数。 |
| `instruct` | `qwen3.7-text-rerank`, `qwen3-rerank`, `qwen3-vl-rerank` | 自定义任务指令（如 `"Retrieve semantically similar text."`），影响排序策略，建议英文书写。 |
| `text_type` | 异步文本向量 API（`text-embedding-batch-api.md`） | 区分 `query`（查询文本）与 `document`（底库文本），对非对称检索任务效果提升显著。 |

## 使用方式

- **同步向量调用**：适用于小批量（≤20行）、低延迟场景。使用 OpenAI 兼容 SDK 或 HTTP POST 到 `/compatible-mode/v1/embeddings`，传入 `model`、`input`（string/array/file）及可选 `dimensions`。
- **异步向量调用**：适用于超大批量（≤100,000行）、大文件（≤200MB）场景。先调用 `/api/v1/services/embeddings/text-embedding/text-embedding` 创建任务（需 `X-DashScope-Async: enable` 头），再轮询 `/api/v1/tasks/{task_id}` 获取结果 URL。
- **多模态向量调用**：统一使用 `/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding` 接口，`input.contents` 数组中按需组合 `{"text":...}`, `{"image":...}`, `{"video":...}` 或 `{"multi_images":[...]}`。
- **排序调用**：`qwen3-rerank` 使用 OpenAI 兼容 `/compatible-api/v1/reranks` 接口（扁平参数）；其余模型使用 `/api/v1/services/rerank/text-rerank/text-rerank`（嵌套 `input` 和 `parameters`）。注意 `qwen3-rerank` 不支持 `return_documents` 参数，且响应结构无 `output` 包裹层。

## 限制和注意事项

- **[Token](../concepts/token.md) 与长度限制**：`qwen3.7-text-embedding` 单行支持 128,000 [Token](../concepts/token.md)，而 `text-embedding-v4` 仅支持 8,192 [Token](../concepts/token.md)；`qwen3-vl-rerank` 视频输入需注意 `fps` 参数控制帧数，避免超限。
- **地域与免费额度差异**：北京地域部分模型（如 `qwen3.7-text-embedding`）提供 100 万 Token 免费额度，有效期 90 天；新加坡地域同名模型可能无免费额度或单价略高，详见各模型概览表格。
- **[异步任务](../concepts/asynchronous-task.md)生命周期**：异步向量任务结果 URL 仅保留 24 小时，需及时下载；同时运行中任务上限为 3 个，排队中+运行中总数不超过 50 个。
- **模型能力边界**：`qwen2.5-vl-embedding` 仅支持融合向量，不支持 `multi_images`；`tongyi-embedding-vision-plus` 固定 1152 维，不可指定 `dimension`；`multimodal-embedding-v1` 不支持 `dimension` 参数且仅限中英文。
- **错误处理**：HTTP 调用必须携带 `Authorization` 和 `Content-Type` 头；缺失 `X-DashScope-Async: enable` 将导致异步接口报错 “current user api does not [support](../guides/support.md) synchronous calls”。

## 来源文档

- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)
- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)


