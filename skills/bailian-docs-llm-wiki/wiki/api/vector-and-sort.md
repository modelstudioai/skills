# vector and sort

百炼平台提供文本向量（Embedding）、多模态向量（Multimodal Embedding）和文本排序（Rerank）三大核心能力，覆盖语义检索、RAG、跨模态搜索等典型AI应用链路。所有能力均支持同步/异步调用、OpenAI兼容接口及DashScope SDK，并按实际[Token](../concepts/token.md)消耗计费。开发者可根据数据规模、延迟敏感度与模态需求选择对应模型与调用方式。

## 支持的模型/功能

### 文本向量化
- **同步模型**：`qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3`、`text-embedding-v2`、`qwen3.7-text-embedding-flash`，支持单次最多20–128,000 [Token](../concepts/token.md)输入，维度可配置（如1024、1536、2048等），详见[同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **异步批处理模型**：`text-embedding-async-v1` 和 `text-embedding-async-v2`，专为超大批量文本（单次最多100,000行，每行≤2,048 [Token](../concepts/token.md)）设计，适用于离线向量化任务。

### 多模态向量化
- **统一语义空间模型**：`qwen3-vl-embedding`（支持独立/融合向量）、`qwen2.5-vl-embedding`（仅融合）、`tongyi-embedding-vision-plus-2026-03-06`（新版Qwen3底座，支持多分辨率与融合）、`multimodal-embedding-v1` 等，支持文本、图像、视频任意组合输入，所有模态向量可直接计算余弦相似度。详细能力对比见[Multi-modal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

### 排序（Rerank）
- **文本排序**：`qwen3.7-text-rerank`（推荐替代已下线的`gte-rerank`）、`qwen3-rerank`，支持最多500个文档排序，单文档最大4,000 Token。
- **多模态排序**：`qwen3-vl-rerank`，支持文本、图片、视频混合查询与排序，单次最多100文本/40图片/4视频，适用于跨模态检索场景，其使用说明见[文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。

> **注意**：`gte-rerank`系列模型（含`gte-rerank-v2`）虽仍可用，但官方明确标注“将于2026年05月30日下线”，且[文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)文档中已强烈建议迁移至`qwen3-rerank`或`qwen3.7-text-rerank`。

## 关键参数

| 参数 | 适用模型 | 说明 |
|--------|-----------|------|
| `text_type` | `text-embedding-async-*` | 取值 `document`（默认，用于底库）或 `query`（用于检索查询），影响向量表征方向，对非对称检索任务效果显著。 |
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v4`, `qwen3-vl-embedding` 等 | 指定向量维度（如1024、1536、2048），不同模型支持范围不同；`multimodal-embedding-v1` 固定为1024维，不支持该参数。 |
| `enable_fusion` | `qwen3-vl-embedding` | `bool`，设为 `true` 时将 `contents` 中所有输入融合为1个向量；其他模型（如 `tongyi-embedding-vision-plus-2026-03-06`）通过将 text/image/video 放入同一 content 对象实现融合，无需此参数。 |
| `instruct` | `qwen3.7-text-rerank`, `qwen3-rerank`, `qwen3-vl-rerank` | 自定义排序任务指令（如 `"Retrieve semantically similar text."`），直接影响相关性判断逻辑，必须用英文。 |
| `top_n` | 所有 Rerank 模型 | 返回排序后前 N 个结果，默认返回全部；若 N > 文档总数，则返回全部。 |

## 使用方式

### 调用路径
- **HTTP 直接调用**：需构造完整 endpoint（含 `{WorkspaceId}` 和地域域名），设置 `Authorization` 和 `Content-Type` 请求头。异步批处理必须携带 `X-DashScope-Async: enable` 头。
- **[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**：适用于熟悉 OpenAI 生态的用户，base_url 为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`（Embedding）或 `/compatible-api/v1/reranks`（Rerank），请求体结构更扁平。
- **DashScope SDK（Python/Java）**：封装了同步/异步调用逻辑，推荐使用 `client.embeddings.jobs.create()` + `.wait()` 或 `client.rerank.create()`，自动处理重试与轮询。

### 典型流程示例
- **批量文本向量化**：先调用 `POST /api/v1/services/embeddings/text-embedding/text-embedding` 创建异步任务 → 获取 `task_id` → 定期 `GET /api/v1/tasks/{task_id}` 查询状态 → 状态为 `SUCCEEDED` 后下载结果URL中的向量文件。
- **跨模态排序**：对 `qwen3-vl-rerank` 发送请求，`input.query` 传入 `{"image": "url"}`，`input.documents` 传入混合数组（如 `{"text": "..."}, {"video": "url"}`），启用 `return_documents: true` 获取原文。

## 限制和注意事项

- **并发与配额**：`text-embedding-async-v2` 用户级并发运行任务数上限为3个，排队中+运行中总数不超过50个；同步模型受通用限流策略约束，详见[限流](https://help.aliyun.com/zh/model-studio/rate-limit)。
- **文件与Token限制**：
  - 异步批处理：输入文件 ≤ 200 MB，单行 ≤ 2,048 Token，总行数 ≤ 100,000；
  - `text-embedding-v4` 同步调用：单条文本 ≤ 8,192 Token，列表最多10条；
  - `qwen3-vl-rerank`：单次请求总输入Token ≤ 120,000（计算公式：`Query Tokens × Document 数量 + Document Tokens 总和`）。
- **地域差异**：北京、新加坡等地域的 endpoint 域名、免费额度、单价均不同，调用前务必确认业务空间ID与对应地域URL（如 `cn-beijing` 或 `ap-southeast-1`）。
- **向量格式兼容性**：`encoding_format` 参数在老网关中被忽略，始终返回 `float`；新网关对短请求生效，长请求仍路由至老网关。生产环境建议显式指定并验证响应格式。
- **模型弃用风险**：`text-embedding-v1`、`text-embedding-v2`、`gte-rerank` 系列无免费额度且部分已标记下线计划，新项目应优先选用 `qwen3.7-text-embedding`、`text-embedding-v4` 或 `qwen3-rerank`。

## 来源文档

- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


