# vector and sort

百炼平台提供文本向量（Embedding）、多模态向量（Multimodal Embedding）和文本排序（Rerank）三大核心能力，覆盖语义检索、RAG、跨模态搜索等典型场景。所有能力均支持同步/[异步调用](../concepts/asynchronous-invocation.md)、[OpenAI 兼容接口](../concepts/openai-compatibility.md)及 DashScope SDK，并按 Token 或任务计费。开发者可根据数据规模、延迟要求与模态类型选择合适模型与接口。

## 支持的模型/功能

- **文本向量化**：支持通用文本向量模型（如 `qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3`）及批处理异步模型（`text-embedding-async-v2`），适用于语义搜索、聚类、分类等任务 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **多模态向量化**：支持文本、图像、视频统一语义空间建模，提供独立向量（每模态各一）与融合向量（多模态合一）两种模式，模型包括 `qwen3-vl-embedding`、`tongyi-embedding-vision-plus-2026-03-06` 等 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。
- **文本排序（Rerank）**：对召回结果进行二次精排，支持纯文本（`qwen3-rerank`）、多模态（`qwen3-vl-rerank`）及兼容模型（`gte-rerank-v2`），其中 `gte-rerank` 系列将于 2026 年 05 月 30 日下线，建议迁移至 `qwen3-rerank` [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。

> **注意**：文档中 `text-embedding-v2` 标注“最大行数 25”，但同页其他模型（如 `qwen3.7-text-embedding`）明确标注“最大行数 20”；而批处理接口 `text-embedding-async-v2` 明确支持“单次请求文本最大行数 100,000”。该不一致表明“最大行数”需结合接口类型（同步 vs 批处理）理解，同步接口的行数限制指单次请求输入数组长度，非全局上限。

## 关键参数

| 参数 | 适用场景 | 说明 |
|--------|-----------|------|
| `dimensions` | 同步文本向量、多模态向量 | 指定向量维度（如 `1024`、`2048`），部分模型（如 `text-embedding-v1`、`tongyi-embedding-vision-plus`）不支持该参数，返回固定维度。 |
| `encoding_format` | 同步文本向量 | 控制输出格式为 `float`（默认）或 `base64`；但老网关强制返回 `float`，长请求亦自动降级为老网关 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。 |
| `enable_fusion` / 同一 content 对象内多模态字段 | 多模态向量 | `qwen3-vl-embedding` 通过 `enable_fusion=true` 开启融合；`tongyi-embedding-vision-plus-2026-03-06` 等则通过将 `text`、`image`、`video` 写入同一字典实现融合。 |
| `instruct` | Rerank | 自定义排序任务指令（如 `"Given a web search query..."`），仅 `qwen3.7-text-rerank`、`qwen3-rerank`、`qwen3-vl-rerank` 支持，影响语义匹配策略。 |
| `top_n` | Rerank | 返回排序后前 N 个结果，默认返回全部；若 `N > 文档总数`，则返回全部。 |
| `text_type` | 批处理文本向量 | 区分 `query`（查询文本）与 `document`（底库文本），用于优化检索效果，对称任务（如聚类）可忽略。 |

## 使用方式

- **同步文本向量**：推荐使用 OpenAI 兼容 SDK（需配置 `base_url` 为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`），支持 `input` 为字符串、字符串列表或文件句柄；HTTP 直接调用需设置 `model` 和 `input`，`dimensions` 和 `encoding_format` 为可选 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **批处理文本向量**：仅支持异步，需两步操作：① 调用 `/api/v1/services/embeddings/text-embedding/text-embedding` 创建任务（`X-DashScope-Async: enable` 必须）；② 用 `task_id` 轮询 `/api/v1/tasks/{task_id}` 获取结果；文件需通过公网可访问 URL 提交。
- **多模态向量**：HTTP 接口统一为 `POST https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`，`input.contents` 数组支持混合 `text`/`image`/`video`/`multi_images`；融合向量需按模型要求使用 `enable_fusion` 或同对象嵌套。
- **Rerank**：HTTP 接口为 `POST https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank`，`input.query` 与 `input.documents` 为必填；SDK 调用更简洁，直接传入 `query`、`documents`、`top_n` 等扁平参数。

## 限制和注意事项

- **Token 与尺寸限制**：
  - 同步文本向量：`qwen3.7-text-embedding` 单行最长 128,000 Token，`text-embedding-v4` 为 8,192 Token，`text-embedding-v1/v2` 为 2,048 Token；
  - 批处理文本向量：单行 ≤ 2,048 Token，单次最多 100,000 行；
  - 多模态向量：`qwen3-vl-embedding` 文本 ≤ 32,000 Token，图片 ≤ 10 MB，视频 ≤ 50 MB；
  - Rerank：`qwen3.7-text-rerank` 单次请求最大输入 Token 为 120,000（建议值），`qwen3-vl-rerank` 文本单条 ≤ 4,000 Token，图片/视频有独立数量限制。

- **地域与免费额度差异**：
  - 北京地域部分模型（如 `qwen3.7-text-embedding`）提供 100 万 Token 免费额度，有效期 90 天；新加坡地域同名模型无免费额度 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
  - `text-embedding-async-v2` 免费额度为各 2000 万 Token，远高于同步接口。

- **模型生命周期**：
  - `gte-rerank` 系列（含 `gte-rerank-v2`）将于 2026-05-30 下线，必须迁移至 `qwen3-rerank` 或 `qwen3.7-text-rerank`；
  - `multimodal-embedding-v1` 不支持 `dimension` 参数，固定 1024 维，新项目应优先选用 `tongyi-embedding-vision-plus-2026-03-03` 等新版模型。

- **其他重要约束**：
  - 批处理异步任务：单用户并发运行中任务数上限为 3，排队中+运行中总数 ≤ 50；
  - Rerank 响应中的 `relevance_score` 是本次请求内的相对分数，不可跨请求比较；
  - 多模态融合向量要求所有输入模态在语义上强关联，混搭无关内容（如随机图文）会降低向量质量。

## 来源文档

- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)
- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)


