# vector and sort

百炼平台的 `vector and sort` 功能涵盖文本/多模态向量化（embedding）与检索后重排序（rerank）两大核心能力，支撑语义搜索、RAG、聚类、跨模态检索等典型AI应用。向量模型将原始内容映射到统一语义空间，排序模型则对召回结果进行精细化相关性打分与重排，二者常组合使用以构建高精度检索系统。

## 支持的模型与功能

### 文本向量模型
- **同步接口**：支持 `qwen3.7-text-embedding`（2560维可选）、`text-embedding-v4`（2048维）、`text-embedding-v3`、`text-embedding-v2` 等，适用于低延迟、小批量场景（如单条Query实时向量化）。详情见 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **异步批处理接口**：专为大规模文本处理设计，支持 `text-embedding-async-v2`（1536维）和 `text-embedding-async-v1`，单次请求最多 100,000 行，每行最长 2,048 [Token](../concepts/token.md)。该接口仅支持异步模式，需通过任务ID轮询结果 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **OpenAI 兼容模式**：所有同步文本向量模型均提供 `/compatible-mode/v1/embeddings` 路由，支持标准 OpenAI SDK 调用，便于生态迁移。

### 多模态向量模型
支持文本、图像、视频统一表征，所有模态向量位于同一语义空间，可直接计算余弦相似度：
- `qwen3-vl-embedding`：支持独立向量与融合向量（通过 `enable_fusion=true` 开启），支持 33 种语言及多图+视频混合输入；
- `tongyi-embedding-vision-plus-2026-03-06`：新版 Qwen3 底座模型，支持 `res_level` 和 `max_video_frames` 参数，同时支持独立与融合向量（融合通过同 content 对象内混写 text/image/video 实现）；
- `qwen2.5-vl-embedding`：仅支持融合向量，不支持多图；
- `multimodal-embedding-v1`：基础版，固定 1024 维，仅支持中英文。

> **注意**：文档 5 中关于 `tongyi-embedding-vision-plus` 的图片格式限制为 JPG/PNG/BMP，而同一文档中 `tongyi-embedding-vision-plus-2026-03-06` 明确支持 WEBP/TIFF/ICNS 等更多格式；实际调用应以新快照版本（2026-03-06）的格式列表为准，旧版模型能力已逐步收敛。

### 排序（Rerank）模型
- `qwen3.7-text-rerank` 与 `qwen3-rerank`：面向纯文本检索，支持最多 500 个文档，`instruct` 参数可指定“问答检索”或“语义相似度”等任务类型；
- `qwen3-vl-rerank`：支持跨模态排序（text/image/video 混合 query 与 documents），单次请求最大文档数按模态类型动态分配（文本 100、图片 40、视频 4）；
- `gte-rerank-v2`：即将于 2026 年 5 月 30 日下线，官方明确推荐迁移到 `qwen3-rerank` [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)。

## 关键参数

| 参数 | 适用模型 | 说明 |
|--------|-----------|------|
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v4`, `qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06` 等 | 指定向量维度，不同模型支持值不同（如 `qwen3-vl-embedding` 支持 2560/2048/1536/...），未指定时取默认值。`text-embedding-v2`、`tongyi-embedding-vision-plus` 等固定维度模型不支持此参数。 |
| `text_type` | `text-embedding-async-v1/v2` | 区分 `document`（底库文本）与 `query`（查询文本），用于优化检索效果；对称任务（聚类/分类）无需设置，默认 `document`。 |
| `enable_fusion` | `qwen3-vl-embedding` | `bool` 类型，设为 `true` 时将 `contents` 中所有输入融合为单个向量；其他模型（如 `qwen2.5-vl-embedding`）无此参数，强制融合。 |
| `instruct` | `qwen3.7-text-rerank`, `qwen3-rerank`, `qwen3-vl-rerank` | 自定义排序任务指令（英文），影响模型对 Query-doc 相关性的判断逻辑，例如 `"Retrieve semantically similar text."`。 |
| `top_n` | 所有 rerank 模型 | 返回排序后前 N 个结果，默认返回全部。 |

## 使用方式

### 向量生成
- **同步调用（HTTP/OpenAI SDK）**：适用于 ≤500 条、单条 ≤128K [Token](../concepts/token.md) 的文本，直接返回向量数组。Endpoint：`POST {WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/embeddings`（OpenAI 兼容）或 `.../api/v1/services/embeddings/text-embedding/text-embedding`（DashScope 原生）。
- **异步批处理（HTTP/SDK）**：适用于超大批量（≤100,000 行），需两步：① `POST .../text-embedding` 创建任务获取 `task_id`；② `GET .../tasks/{task_id}` 查询结果 URL。文件需为公开 HTTP URL，每行一条文本。
- **多模态调用**：统一使用 `POST dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`，`input.contents` 数组中按 `{ "text": "...", "image": "...", "video": "..." }` 格式组织输入。

### 排序调用
- **HTTP**：`POST {WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank`，`input.query` 与 `input.documents` 为必填字段，`documents` 可为字符串数组（文本）或对象数组（多模态）。
- **SDK**：使用 `dashscope.TextReRank.call()` 或 `dashscope.MultiModalReRank.call()`，参数扁平化（如直接传 `query`, `documents`, `top_n`），无需手动嵌套 `input`。

## 限制和注意事项

- **限流与配额**：
  - 异步文本向量：单用户并发运行中作业 ≤3 个，排队中+运行中总数 ≤50 个；免费额度为各 2000 万 [Token](../concepts/token.md)（90 天有效）[批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
  - 同步文本向量：`qwen3.7-text-embedding` 免费额度为各 100 万 Token（90 天），`text-embedding-v2` 为各 50 万 Token。
  - 多模态向量：`qwen3-vl-embedding` 免费额度为 100 万 Token（90 天）。
- **输入限制**：
  - 同步文本向量：`text-embedding-v4` 单次最多 10 条，每条 ≤8,192 Token；`qwen3.7-text-embedding` 最多 20 条，每条 ≤128,000 Token。
  - 多模态向量：`qwen3-vl-embedding` 单次 `contents` 总数 ≤20，图片 ≤10 张，视频 ≤1 个；`tongyi-embedding-vision-plus-2026-03-06` 支持最多 64 张图片。
- **输出格式**：`encoding_format` 参数在长请求（如 >128K Token）时可能失效，内部路由至老网关后仅返回 `float` 类型向量，不支持 `base64` 编码 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **模型兼容性**：`gte-rerank-v2` 已标记为下线模型，新项目请勿选用；`qwen2.5-vl-embedding` 不支持 `multi_images`，若需多图请使用 `tongyi-embedding-vision-plus-2026-03-06` 或 `qwen3-vl-embedding`。

## 来源文档

- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


