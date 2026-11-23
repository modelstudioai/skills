# vector and sort

百炼平台提供文本向量（embedding）、多模态向量（multimodal embedding）和文本排序（rerank）三大核心能力，覆盖语义检索、RAG、跨模态搜索等典型场景。所有服务均支持同步与异步调用模式，具备细粒度参数控制、多地域部署及 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)，适用于从单次调试到大规模批处理的全量开发需求。详细模型能力与限制请参见各子模块文档。

## 支持的模型/功能

### 文本向量化
- **同步接口**：支持 `qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3` 等通用文本模型，适用于低延迟、小批量场景（如实时检索）。[同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)  
- **异步批处理**：支持 `text-embedding-async-v2`（100,000 行/请求），适用于超大批量离线向量化任务（如知识库预处理）。[批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)  
- **免费额度**：北京地域 `qwen3.7-text-embedding`、`text-embedding-v4` 等模型提供 100 万 Token 免费额度（开通后 90 天内有效）；新加坡地域无免费额度。

### 多模态向量化
- 支持文本、图像、视频三模态统一向量空间表征，提供**独立向量**（每模态生成一个向量）与**融合向量**（多模态输入编码为单一向量）两种模式。
- 主流模型包括 `qwen3-vl-embedding`（支持 `enable_fusion=true`）、`tongyi-embedding-vision-plus-2026-03-06`（融合向量通过同 content 对象实现）等。[Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)

### 排序（Rerank）
- 提供纯文本与多模态排序能力：
  - `qwen3-rerank` 和 `qwen3.7-text-rerank`：支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)，适用于 RAG 场景的高精度重排；
  - `qwen3-vl-rerank`：支持图文/图视/文视混合查询与文档排序；
  - `gte-rerank-v2`：仅支持文本，最大文档数达 30,000 条，但已于 2026 年 5 月 30 日下线，[文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md) 文档明确提示迁移至 `qwen3-rerank`。

> **注意**：文档 7 中 `gte-rerank-v2` 的“最大文档数”标注为 `30,000`，但同一文档表格中又注明其“单次请求最大文档数”未明确限制，仅说明“单条最大输入Token”为 30,000。该数值实际指单个 document 或 query 的 token 上限，而非总文档数。此处以表格中“最大文档数”列为准，即 `gte-rerank-v2` 不设总文档数硬限制，但受 `请求最大输入Token=Query Tokens × Document 数量 + Document Tokens 总和 ≤ 120,000` 约束。

## 关键参数

| 参数 | 适用模型 | 说明 | 是否必选 |
|------|----------|------|----------|
| `model` | 全部 | 模型名称，如 `qwen3.7-text-embedding`、`qwen3-rerank` | 必选 |
| `input` | 全部 | 向量化或排序的原始数据。文本向量支持 `string`/`array<string>`/`file`；多模态向量需为 `{"contents": [...]}`；rerank 需嵌套 `query` 与 `documents` | 必选 |
| `dimensions` / `dimension` | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding` 等 | 指定向量维度（如 `1024`, `2048`），不同模型支持值不同 | 可选（默认值见各模型概览） |
| `encoding_format` | 同步文本向量 | 控制返回格式：`float`（默认）或 `base64`；但老网关强制返回 `float` | 可选 |
| `enable_fusion` | `qwen3-vl-embedding` | `true` 时启用融合向量模式；其他模型（如 `tongyi-embedding-vision-plus-2026-03-06`）通过将 text/image/video 放入同一 content 对象实现融合 | 可选（仅 `qwen3-vl-embedding`） |
| `instruct` | `qwen3.7-text-rerank`, `qwen3-rerank`, `qwen3-vl-rerank` | 自定义排序任务指令（如 `"Retrieve semantically similar text."`），影响相关性判断逻辑 | 可选 |
| `top_n` | rerank 模型 | 返回 top-N 排序结果，默认返回全部 | 可选 |
| `return_documents` | `gte-rerank-v2`, `qwen3-vl-rerank`, `qwen3-rerank` | 是否在响应中返回原文，默认 `false` | 可选 |

## 使用方式

### 调用路径
- **同步文本向量**：HTTP POST 到 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1/embeddings`（OpenAI 兼容）或 `.../api/v1/services/embeddings/text-embedding/text-embedding`（DashScope 原生）。
- **异步文本向量**：两步调用 —— 先 `POST .../api/v1/services/embeddings/text-embedding/text-embedding` 创建任务（带 `X-DashScope-Async: enable`），再 `GET .../api/v1/tasks/{task_id}` 查询结果。
- **多模态向量**：统一 HTTP POST 到 `https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`，`input.contents` 指定模态组合。
- **排序模型**：HTTP POST 到 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank`（原生）或 `.../compatible-api/v1/reranks`（OpenAI 兼容，仅限 `qwen3-rerank`/`qwen3.7-text-rerank`）。

### SDK 与 CLI
- DashScope SDK（Python/Java）封装了异步轮询、任务等待等逻辑，推荐用于生产环境。例如 `client.embeddings.jobs.wait(job)` 自动阻塞直至完成。
- dashscope CLI 支持快速验证：`dashscope embeddings create -m text-embedding-v3 -i "hello"` 或 `dashscope rerank create -m qwen3-rerank -q "query" -d "doc1" -d "doc2"`。

## 限制和注意事项

- **Token 与长度限制**：
  - `qwen3.7-text-embedding` 单行最长 128,000 Token，`text-embedding-v4` 为 8,192 Token，`text-embedding-v1/v2` 为 2,048 Token；
  - `qwen3-vl-rerank` 图片文档上限 40 张、视频上限 4 个，且 `fps` 参数仅对该模型生效；
  - 所有 rerank 模型的 `请求最大输入Token` = `Query Tokens × Document 数量 + Document Tokens 总和`，不得超过文档标明的上限（如 `qwen3.7-text-rerank` 为 120,000）。

- **地域与计费差异**：
  - 北京与新加坡地域模型列表、单价、免费额度不同（如新加坡 `qwen3.7-text-embedding` 无免费额度），调用前需确认 `base_url` 和模型可用性。

- **网关兼容性**：
  > **注意**：文档 1 中 `encoding_format` 参数说明指出，“老网关”不支持 `base64` 输出，无论请求如何设置均返回 `float`；而“新网关”对短请求按设置返回，长请求仍路由至老网关。开发者应通过实际响应体验证格式，不可仅依赖参数声明。

- **模型弃用**：
  - `gte-rerank` 系列模型已明确下线计划，必须迁移至 `qwen3-rerank`；`text-embedding-v1/v2` 无免费额度且能力较新模型弱，建议优先选用 `text-embedding-v4` 或 `qwen3.7-text-embedding`。

- **文件与 URL 输入**：
  - 异步文本向量要求输入文件为公开可访问 URL（如 OSS），且单文件 ≤ 200MB、单行 ≤ 2,048 Token；
  - 多模态向量中图片/视频 URL 必须可公开访问，Base64 编码仅支持图片（`data:image/...;base64,...`），不支持视频。

## 来源文档

- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


