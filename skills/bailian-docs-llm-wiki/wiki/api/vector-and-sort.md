# vector and sort

百炼平台提供文本向量（embedding）、多模态向量（multimodal embedding）和排序（rerank）三大核心能力，覆盖语义检索、RAG、跨模态搜索等典型AI应用链路。所有能力均支持同步与异步调用方式，适配OpenAI兼容接口与DashScope原生SDK，开发者可按场景需求灵活选型。

## 支持的模型/功能

### 文本向量模型
- **同步接口**：支持 `qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3`、`text-embedding-v2`、`text-embedding-v1` 等多版本模型，适用于低延迟、小批量（≤20行）实时向量化场景 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **批处理接口**：`text-embedding-async-v2`（推荐）与 `text-embedding-async-v1`，专为超大批量（单次最多100,000行）离线任务设计，需通过异步任务ID轮询结果 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。

### 多模态向量模型
支持文本、图像、视频三模态统一表征，分为两类：
- **独立向量**：为每个输入项（如1段文本+1张图）生成独立向量，适用于以文搜图、以图搜图等逐项匹配场景；
- **融合向量**：将多模态输入（如文本+图片+视频）编码为单一向量，适用于商品多模态统一表征等整体理解任务。  
  具体模型包括 `qwen3-vl-embedding`（支持独立/融合双模式）、`tongyi-embedding-vision-plus-2026-03-06`（新版Qwen3底座，支持多分辨率与融合）等 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

### 排序（Rerank）模型
用于对召回结果进行二次精排，提升Top-K相关性：
- `qwen3-rerank`：新主力模型，OpenAI兼容接口，轻量高效；
- `qwen3.7-text-rerank` 与 `qwen3-vl-rerank`：支持文本/多模态混合排序，含丰富参数控制；
- `gte-rerank-v2`：已进入维护期，**将于2026年05月30日下线**，请尽快迁移至 `qwen3-rerank` [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)。

> **注意**：`qwen3-rerank` 使用 `/compatible-api/v1/reranks` 路径且参数扁平化（`query`、`documents` 与 `model` 同级），而 `qwen3.7-text-rerank` 和 `qwen3-vl-rerank` 使用 `/api/v1/services/rerank/...` 路径且要求嵌套在 `input` 对象中——二者请求结构不兼容，不可混用。

## 关键参数

| 参数 | 适用模型 | 说明 |
|--------|-----------|------|
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06` 等 | 指定向量维度（如 `1024`, `2048`）。部分旧模型（如 `text-embedding-v2`, `tongyi-embedding-vision-plus`）不支持该参数，返回固定维度。 |
| `encoding_format` | 同步文本向量接口 | 控制输出格式：`float`（默认）或 `base64`。**注意**：老网关强制返回 `float`，长请求（Token > 8192）也会降级至老网关，此时 `base64` 设置无效 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。 |
| `enable_fusion` | `qwen3-vl-embedding` | `true` 时启用融合向量；其他模型（如 `tongyi-embedding-vision-plus-2026-03-06`）通过将 text/image/video 放入同一 content 对象实现融合，**无需此参数**。 |
| `instruct` | `qwen3.7-text-rerank`, `qwen3-rerank`, `qwen3-vl-rerank` | 自定义排序任务指令（如 `"Retrieve semantically similar text."`），显著影响排序逻辑，建议使用英文。 |
| `text_type` | 批处理文本向量（`text-embedding-async-v2`） | 区分 `query`（查询）与 `document`（底库），对非对称检索任务效果提升明显。 |

## 使用方式

### 同步调用（文本/多模态）
- **HTTP**：直接 POST 到对应 endpoint（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/embeddings`），传入 `model`、`input`（字符串/数组/文件）及可选参数。
- **OpenAI SDK**：配置 `base_url` 为兼容地址，调用 `client.embeddings.create()`。
- **DashScope SDK**：使用 `dashscope.TextEmbedding.call()` 或 `dashscope.MultimodalEmbedding.call()`，参数更简洁。

### 异步调用（大批量文本）
- **HTTP**：两步操作 —— 1) POST 创建任务（带 `X-DashScope-Async: enable`），获取 `task_id`；2) GET `https://.../api/v1/tasks/{task_id}` 查询结果。
- **DashScope SDK**：`BatchTextEmbedding.call()`（同步封装）或 `BatchTextEmbedding.async_call()` + `fetch()`/`wait()`（显式异步控制）。

### 排序调用
- `qwen3-rerank`：使用 OpenAI 兼容路径 `/compatible-api/v1/reranks`，参数扁平化。
- 其他 rerank 模型：使用 `/api/v1/services/rerank/...` 路径，`query` 与 `documents` 必须嵌套在 `input` 对象内。

## 限制和注意事项

- **Token 限制严格**：各模型对单行/单次请求 Token 数有硬性上限（如 `text-embedding-v4` 单行 ≤8192，`qwen3.7-text-embedding` 单行 ≤128,000），超限直接返回 HTTP 400 错误，**不会自动截断**。
- **地域差异**：北京与新加坡地域的模型列表、单价、免费额度不同（如新加坡 `qwen3.7-text-embedding` 无免费额度），调用前务必确认地域配置 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **异步任务生命周期**：批处理任务结果 URL 仅保留 **24 小时**，需及时下载；同时运行中任务数上限为 3 个，排队中任务上限为 50 个 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **多模态输入约束**：`qwen3-vl-embedding` 单次请求内容元素总数 ≤20（图片≤10，视频≤1）；`tongyi-embedding-vision-plus-2026-03-06` 支持最多 64 张图片，但总元素数仍 ≤20。
- **模型弃用风险**：`gte-rerank` 系列已明确下线计划，`text-embedding-v1/v2` 功能较旧，建议优先选用 `qwen3.7-text-embedding` 和 `qwen3-rerank` 等新一代模型。

## 来源文档

- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)
- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)


