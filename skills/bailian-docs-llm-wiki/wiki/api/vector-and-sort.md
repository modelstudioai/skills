# vector and sort

百炼平台的 `vector and sort` 功能涵盖文本/多模态向量化（embedding）与文本/跨模态排序（rerank）两大核心能力，用于构建语义搜索、RAG、推荐系统等AI应用的基础检索链路。向量模型将原始内容映射到统一语义空间，排序模型则对召回结果进行精细化相关性重排，二者常协同使用以提升端到端检索质量。

## 支持的模型与功能

### 文本向量模型
- **同步接口**：支持 `qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3`、`text-embedding-v2`、`text-embedding-v1` 等多版本模型，适用于低延迟、小批量场景 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **批处理接口**：提供 `text-embedding-async-v2` 和 `text-embedding-async-v1`，专为超大批量（单次最多 100,000 行）、长文本（单行最多 2,048 [Token](../concepts/token.md)）场景设计，采用异步任务模式 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。

### 多模态向量模型
- 支持文本、图像、视频三类模态的独立向量与融合向量生成，模型包括 `qwen3-vl-embedding`（支持 `enable_fusion`）、`qwen2.5-vl-embedding`（仅融合）、`tongyi-embedding-vision-plus-2026-03-06`（支持多分辨率与融合）等 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

### 排序（Rerank）模型
- **文本排序**：`qwen3.7-text-rerank`（推荐替代已下线的 `gte-rerank`）、`qwen3-rerank`；支持最多 500 个文档、单条 Query 最高 4,000 [Token](../concepts/token.md)。
- **多模态排序**：`qwen3-vl-rerank`，支持文本/图片/视频混合查询与文档，最大文档数按模态类型动态限制（如文本 100 条、图片 40 张）。
- 所有排序模型均支持 `instruct` 参数定制任务意图（如问答检索 vs 语义相似度），并可通过 `top_n` 控制返回数量。

> **注意**：文档 6 明确指出 `gte-rerank` 模型将于 2026 年 05 月 30 日下线，而文档 7 的目录页未体现该弃用信息，应以文档 6 为准。

## 关键参数

| 参数 | 适用模型 | 说明 |
|------|----------|------|
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding`, `qwen2.5-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06`, `tongyi-embedding-vision-flash-2026-03-06` | 指定向量维度，不同模型支持值不同（如 `qwen3.7-text-embedding` 支持 2560/2048/.../256，默认 1024）；`tongyi-embedding-vision-plus` 等旧版模型不支持此参数。 |
| `encoding_format` | 同步文本向量接口 | 控制输出格式（`float` 或 `base64`），但受网关限制：老网关强制返回 `float`，新网关仅短请求支持按需返回。 |
| `enable_fusion` | `qwen3-vl-embedding` | 布尔值，启用后将 `contents` 中所有输入融合为单个向量；其他模型（如 `qwen2.5-vl-embedding`）无此参数，其行为固定为融合。 |
| `text_type` | 批处理文本向量接口 | 可选 `document`（默认）或 `query`，用于非对称检索任务优化。 |
| `instruct` | 所有 `qwen3.*-rerank` 及 `gte-rerank-v2` | 自定义排序指令（英文），影响相关性判断逻辑，例如 `"Retrieve semantically similar text."`。 |

## 使用方式

### 向量生成
- **同步调用**（适合 ≤20 条）：使用 OpenAI 兼容 SDK 或 DashScope SDK，通过 `POST /compatible-mode/v1/embeddings` 发送请求，支持字符串、字符串列表或文件输入 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **异步批处理**（适合海量数据）：调用 `POST /api/v1/services/embeddings/text-embedding/text-embedding` 提交任务，输入为公开可访问的文本文件 URL；结果通过 `GET /api/v1/tasks/{task_id}` 查询，任务状态保留 24 小时 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **多模态向量**：统一使用 `POST /api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`，`contents` 数组中按需组合 `text`/`image`/`video`/`multi_images` 对象；融合向量需将多模态内容置于同一字典内（如 `{"text": "...", "image": "..."}`）。

### 排序调用
- 统一使用 `POST /api/v1/services/rerank/text-rerank/text-rerank`，`input.query` 与 `input.documents` 为必填字段。
- `qwen3-vl-rerank` 支持混合模态输入：`query` 可为字符串（文本）或 `{"image": "url"}`，`documents` 数组中每个元素可为字符串（文本）、`{"image": "url"}` 或 `{"video": "url"}`。
- SDK 调用更简洁：`client.rerank.create(model=..., query=..., documents=[...], top_n=10)`。

## 限制和注意事项

- **[Token](../concepts/token.md) 限制严格**：同步文本向量中，`qwen3.7-text-embedding` 单行最高 128,000 Token，而 `text-embedding-v4` 仅 8,192 Token；超出即返回 HTTP 400 错误，**不会自动截断**。
- **地域与免费额度差异**：北京地域部分模型（如 `qwen3.7-text-embedding`）提供 100 万 Token 免费额度，有效期 90 天；新加坡地域同名模型无免费额度 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **异步任务并发控制**：`text-embedding-async-v2` 限制单用户同时运行中任务 ≤3 个，排队中 + 运行中总数 ≤50 个 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **多模态输入格式敏感**：`tongyi-embedding-vision-plus` 等模型要求 `multi_images` 必须为数组，而 `qwen3-vl-embedding` 的融合模式要求所有模态在同一个对象内；格式错误将导致解析失败。
- **排序模型计费逻辑**：`qwen3.7-text-rerank` 的 `usage.prompt_tokens` 返回输入总 Token 数，而其他模型仅返回 `total_tokens`；计费依据均为 `total_tokens`。

## 来源文档

- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)
- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)


