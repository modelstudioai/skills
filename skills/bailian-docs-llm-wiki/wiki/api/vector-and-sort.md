# vector and sort

百炼平台提供文本向量（Embedding）、多模态向量（Multimodal Embedding）和文本排序（Rerank）三大核心能力，覆盖语义检索、RAG、跨模态搜索、聚类与分类等典型AI应用。所有能力均通过统一API框架提供同步/异步调用支持，并兼容OpenAI生态接口，便于快速集成与迁移。

## 支持的模型/功能

### 文本向量（Embedding）
- **同步接口**：支持 `qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3`、`text-embedding-v2`、`text-embedding-v1` 等模型，适用于低延迟、小批量场景（如实时检索）。详细参数与模型能力见 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **批处理接口**：支持 `text-embedding-async-v2` 和 `text-embedding-async-v1`，专为超大批量（单次最多 100,000 行）、长尾任务设计，采用[异步任务](../concepts/asynchronous-task.md)模式，结果通过 URL 下载。参见 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **多模态向量**：支持 `qwen3-vl-embedding`、`qwen2.5-vl-embedding`、`tongyi-embedding-vision-plus-2026-03-06` 等模型，可对文本、图像、视频进行联合编码，生成统一语义空间下的向量，支持独立向量与融合向量两种模式。详见 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

### 排序（Rerank）
- **文本排序**：`qwen3.7-text-rerank`（推荐替代已下线的 `gte-rerank`）、`qwen3-rerank` 支持高精度语义重排序，最大支持 500 个文档；`gte-rerank-v2` 已进入维护期，[官方公告明确将于2026年05月30日下线](https://www.aliyun.com/notice/118217)，应尽快迁移。
- **多模态排序**：`qwen3-vl-rerank` 支持文本、图像、视频混合查询与排序，适用于跨模态检索场景。

> **注意**：`qwen2.5-vl-embedding` 仅支持融合向量（不支持独立向量），而 `tongyi-embedding-vision-plus` 和 `tongyi-embedding-vision-flash` 仅支持独立向量（不支持融合），二者能力互斥，需按业务需求严格选型 —— 此矛盾信息在 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md) 中有明确说明。

## 关键参数

| 参数 | 适用模型 | 说明 | 是否必选 |
|--------|-----------|------|----------|
| `model` | 全部 | 模型名称，如 `"qwen3.7-text-embedding"` 或 `"qwen3-vl-rerank"` | ✅ |
| `input` | 全部 | 输入内容结构体：文本向量为 `string/array/file`；多模态为 `{"contents": [...]}`；Rerank 为 `{"query": ..., "documents": [...]}` | ✅ |
| `dimensions` / `dimension` | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06` 等 | 指定向量维度（如 `1024`, `2048`），部分模型（如 `multimodal-embedding-v1`, `tongyi-embedding-vision-plus`）不支持该参数 | ❌（可选） |
| `encoding_format` | 同步文本向量 | 控制返回格式：`"float"` 或 `"base64"`；但[老网关强制返回 float，新网关长请求也降级为 float](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md) | ❌ |
| `enable_fusion` | `qwen3-vl-embedding` | 开启融合向量模式（将全部输入融合为 1 个向量）；其他模型（如 `tongyi-embedding-vision-plus-2026-03-03`）通过同 content 内多模态字段隐式实现融合 | ❌ |
| `top_n` | Rerank 全系列 | 返回前 N 个最相关结果，默认返回全部 | ❌ |
| `instruct` | `qwen3.7-text-rerank`, `qwen3-rerank`, `qwen3-vl-rerank` | 自定义排序任务指令（如 `"Retrieve semantically similar text."`），显著影响排序逻辑 | ❌ |
| `text_type` | 批处理文本向量 | 区分 `"document"`（底库）或 `"query"`（检索词），用于非对称检索优化 | ❌（默认 `"document"`） |

## 使用方式

### 同步调用（文本/多模态向量、Rerank）
- **HTTP**：使用 `POST /api/v1/services/...` 或 OpenAI 兼容 endpoint（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/embeddings`），需配置 `Authorization` 和 `Content-Type` 头。
- **SDK（Python/Java）**：推荐使用 DashScope SDK，自动处理认证、重试与地域路由。示例见 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md) 中的 Python/Java 代码块。
- **CLI**：`dashscope embeddings create -m qwen3.7-text-embedding -i "hello"` 或 `dashscope rerank create -m qwen3-rerank -q "query" -d "doc1" -d "doc2"`。

### 异步调用（批处理向量）
- **HTTP**：两步操作：① `POST /api/v1/services/embeddings/text-embedding/text-embedding` 创建任务（必须带 `X-DashScope-Async: enable` 头）；② `GET /api/v1/tasks/{task_id}` 轮询结果。
- **SDK**：`client.embeddings.jobs.create()` 提交任务，`client.embeddings.jobs.wait()` 阻塞等待完成，或 `client.embeddings.jobs.fetch()` 主动轮询。

### 多模态输入格式
- **独立向量**：`"contents": [{"text": "a"}, {"image": "url1"}, {"video": "url2"}]` → 返回 3 个向量。
- **融合向量**：
  - `qwen3-vl-embedding`：添加 `"parameters": {"enable_fusion": true}`；
  - `tongyi-embedding-vision-plus-2026-03-06`：`"contents": [{"text": "...", "image": "...", "video": "..."}]`（单个 dict 内多模态）。

## 限制和注意事项

- **[Token](../concepts/token.md) 与长度限制**：
  - `qwen3.7-text-embedding` 单行最长 128,000 [Token](../concepts/token.md)；`text-embedding-v4` 仅支持 8,192 [Token](../concepts/token.md)；`qwen3-vl-rerank` 图片输入限 40 张/请求，视频限 4 个/请求。
  - 多模态向量中，`qwen3-vl-embedding` 文本限 32,000 Token，图片单张 ≤10 MB；`tongyi-embedding-vision-plus` 图片单张 ≤3 MB。
- **并发与配额**：
  - 批处理向量：单用户并发运行中任务 ≤3 个，排队中+运行中总数 ≤50 个；免费额度为各 2000 万 Token（有效期 90 天）。
  - 同步向量：北京地域 `qwen3.7-text-embedding` 免费额度为 100 万 Token（90 天），新加坡地域无免费额度。
- **地域与 URL**：北京地域 base URL 为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/...`，新加坡为 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/...`，务必替换 `{WorkspaceId}` 并匹配地域。
- **模型兼容性**：`qwen3.7-text-rerank` 和 `qwen3-rerank` 均支持 `instruct` 参数，但 `gte-rerank-v2` 不支持；`multimodal-embedding-v1` 固定 1024 维，不支持 `dimension` 参数 —— 这些差异已在 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md) 和 [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md) 中明确标注。

## 来源文档

- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)
- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


