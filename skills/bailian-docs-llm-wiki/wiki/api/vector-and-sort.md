# vector and sort

百炼平台提供文本向量（embedding）、多模态向量（multimodal embedding）和文本排序（rerank）三类核心语义理解能力，覆盖从原始内容表征、跨模态对齐到检索结果精排的完整 pipeline。所有能力均支持同步与异步调用，适配 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)与 DashScope 原生 SDK，并在多地（北京、新加坡等）部署以满足低延迟与合规需求。

## 支持的模型/功能

- **文本向量化**：支持通用文本嵌入（如 `qwen3.7-text-embedding`、`text-embedding-v4`）与批处理异步模型（如 `text-embedding-async-v2`），适用于语义搜索、聚类、RAG 等场景。详情见 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **多模态向量化**：支持文本、图像、视频统一语义空间建模（如 `qwen3-vl-embedding`、`tongyi-embedding-vision-plus-2026-03-06`），提供独立向量（per-modality）与融合向量（fused）两种模式，支撑跨模态检索与相似度计算。详见 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。
- **文本排序（Rerank）**：对召回结果进行二次重排序，提升相关性精度。支持纯文本（`qwen3-rerank`）、多模态（`qwen3-vl-rerank`）及兼容型（`gte-rerank-v2`）模型。注意：`gte-rerank` 系列将于 2026 年 5 月 30 日下线，[排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md) 文档已明确推荐迁移至 `qwen3-rerank`。

> **注意**：`qwen3-vl-embedding` 的 `enable_fusion` 参数仅在独立向量模式下生效；而 `tongyi-embedding-vision-plus-2026-03-06` 等新版模型通过将 text/image/video 放入同一 content 对象实现融合，**不使用 `enable_fusion` 字段**——两套机制并存但互不兼容，开发者需按模型文档严格匹配参数用法。

## 关键参数

| 参数 | 适用模型 | 说明 | 示例值 |
|------|----------|------|--------|
| `model` | 全部 | 必选，指定模型名称，不同地域可用模型不同（如北京有免费额度，新加坡无） | `"qwen3.7-text-embedding"`, `"qwen3-vl-embedding"` |
| `input` / `query` / `documents` | 按模型区分 | 向量模型：`input` 支持 string/array/file；rerank 模型：`query` + `documents` 结构化输入 | `"衣服的质量杠杠的..."`, `["doc1", "doc2"]` |
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding` 等 | 可选，指定输出向量维度；部分旧模型（如 `text-embedding-v2`, `multimodal-embedding-v1`）不支持 | `1024`, `2560` |
| `encoding_format` | 向量同步接口 | 可选，控制返回格式（`float` 或 `base64`），但[老网关强制返回 `float`](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md) | `"float"` |
| `text_type` | `text-embedding-async-v2` | 批处理专用，区分 `document`（底库）与 `query`（检索）类型，影响向量表征策略 | `"query"` |
| `instruct` | `qwen3.7-text-rerank`, `qwen3-rerank`, `qwen3-vl-rerank` | 可选，指定排序任务类型（如问答检索/语义相似度），显著影响排序逻辑 | `"Retrieve semantically similar text."` |
| `enable_fusion` | 仅 `qwen3-vl-embedding` | 布尔值，开启后将 `contents` 中所有模态融合为单个向量；其他模型（如 `tongyi-embedding-vision-plus-2026-03-06`）**不支持此参数** | `true` |

## 使用方式

- **同步调用（推荐小批量）**：  
  - 文本向量：使用 OpenAI 兼容 `/embeddings` 接口（需配置 `base_url` 为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）或 DashScope SDK `dashscope.TextEmbedding.call()`。  
  - 多模态向量：HTTP POST 到 `https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`，`input.contents` 按模态构造字典。  
  - Rerank：`qwen3-rerank` 使用 `/compatible-api/v1/reranks`（扁平参数），其余模型使用 `/api/v1/services/rerank/text-rerank/text-rerank`（嵌套 `input`）。

- **异步调用（推荐大批量）**：  
  - 文本批处理：调用 `text-embedding-async-v2`，上传文本文件 URL，通过 `task_id` 轮询结果。参考 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。  
  - 多模态与 rerank 暂不提供原生异步接口，需自行封装重试逻辑。

- **CLI 与 SDK**：  
  `dashscope` CLI 支持快速调试（如 `dashscope embeddings create -m text-embedding-v3 -i "hello"`）；Python/Java SDK 提供更高层封装（如 `BatchTextEmbedding.call()`、`TextReRank.call()`），降低集成复杂度。

## 限制和注意事项

- **Token 与尺寸限制**：  
  - `qwen3.7-text-embedding` 单行最长 **128,000 Token**，`text-embedding-v4` 仅 **8,192 Token**；`qwen3-vl-embedding` 图片限 **10 MB**，视频限 **50 MB**；`qwen3-vl-rerank` 单条文本最大 **8,000 Token**。超限将直接返回 HTTP 400 错误，**不会自动截断**。  
  - 批处理 `text-embedding-async-v2` 单次最多 **100,000 行**，文件大小 ≤ **200 MB**。

- **地域与额度差异**：  
  - 北京地域多数模型提供 **90 天免费额度**（如 `qwen3.7-text-embedding` 各 100 万 Token），新加坡地域**无免费额度**且单价略高（如 `qwen3.7-text-embedding` 北京 0.0005 元/千 Token，新加坡 0.000525 元）。  
  - `text-embedding-v3` 在北京有免费额度，在新加坡仅部分版本（如 `text-embedding-v3`）提供 50 万 Token 免费额度。

- **模型兼容性陷阱**：  
  > **注意**：`text-embedding-v2` 最大行数为 **25**，而 `qwen3.7-text-embedding` 为 **20**，`text-embedding-v4` 仅为 **10** —— 迁移时若未调整批量大小，将触发 `422 Unprocessable Entity` 错误。同理，`multimodal-embedding-v1` 固定 1024 维，**不支持 `dimension` 参数**，传入将被忽略或报错。

- **异步任务管理**：  
  `text-embedding-async-v2` 任务状态仅保留 **24 小时**，且单用户并发运行中任务上限为 **3 个**（排队中+运行中总数 ≤ 50）。务必及时保存 `url` 返回的结果，超时后无法再次获取。

## 来源文档

- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)
- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


