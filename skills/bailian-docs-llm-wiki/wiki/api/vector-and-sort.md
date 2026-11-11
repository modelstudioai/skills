# vector and sort

百炼平台提供文本向量化（vector）与文本重排序（sort/rerank）两类核心语义理解能力，分别用于将非结构化文本映射到稠密向量空间，以及对召回结果进行精细化相关性打分与重排。二者常组合使用构建端到端检索系统（如 RAG），支持同步/异步调用、[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)及多模态扩展。

## 支持的模型/功能

### 文本向量模型
- **同步接口**：支持 `qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3` 等通用文本向量模型，适用于低延迟、小批量场景（单次最多 20 行，最长 128,000 Token）。详情见 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **异步批处理**：`text-embedding-async-v2` 支持单次 100,000 行、每行最多 2,048 Token 的大规模批量处理，适合离线向量化任务 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **多模态向量**：`qwen3-vl-embedding`、`tongyi-embedding-vision-plus-2026-03-06` 等模型支持文本、图像、视频统一语义空间嵌入，可生成独立向量或跨模态融合向量 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

### 排序（Rerank）模型
- **文本排序**：`qwen3.7-text-rerank` 和 `qwen3-rerank` 支持最大 500 文档/请求、Query 最长 30,000 Token，适用于高精度语义检索；`gte-rerank-v2` 已逐步被替代，不推荐新项目使用。
- **多模态排序**：`qwen3-vl-rerank` 支持文本、图像、视频混合输入的跨模态重排序，文档数限制依模态类型动态调整（如文本最多 100 条，图片最多 40 条）。

> **注意**：`gte-rerank` 模型已于 2026 年 05 月 30 日下线，[文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md) 文档明确要求迁移至 `qwen3-rerank` 或 `qwen3.7-text-rerank`。

## 关键参数

| 参数 | 适用模型 | 说明 |
|------|----------|------|
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v4`, `text-embedding-v3`, `qwen3-vl-embedding`, `tongyi-embedding-vision-plus-*` | 指定向量维度（如 `1024`, `2048`），不同模型支持值不同；`multimodal-embedding-v1` 不支持该参数。 |
| `encoding_format` | 同步文本向量（`qwen3.7-text-embedding` 等） | 控制返回格式为 `float` 或 `base64`，但[同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)指出老网关仅返回 `float`，长请求亦强制降级。 |
| `enable_fusion` | `qwen3-vl-embedding` | `true` 时将 `contents` 中所有模态融合为单个向量；`false`（默认）或未设置时生成独立向量。 |
| `instruct` | `qwen3.7-text-rerank`, `qwen3-rerank`, `qwen3-vl-rerank` | 自定义排序任务指令（如 `"Given a web search query..."`），影响语义匹配策略，英文效果更稳定。 |
| `text_type` | 异步文本向量（`text-embedding-async-v2`） | 区分 `query`（查询）与 `document`（底库），提升非对称检索任务效果。 |

## 使用方式

### 调用路径
- **同步向量**：HTTP POST 到 `/compatible-mode/v1/embeddings`（OpenAI 兼容）或 `/api/v1/services/embeddings/text-embedding/text-embedding`（DashScope 原生）。
- **异步向量**：先调用任务创建接口（`X-DashScope-Async: enable`），再轮询 `/api/v1/tasks/{task_id}` 获取结果。
- **排序**：HTTP POST 到 `/api/v1/services/rerank/text-rerank/text-rerank`（原生）或 `/compatible-api/v1/reranks`（OpenAI 兼容，仅限 `qwen3-rerank`/`qwen3.7-text-rerank`）。

### 输入格式示例
- **文本向量（同步）**：`input` 可为字符串、字符串数组或文件句柄。
- **多模态向量**：`input.contents` 为对象数组，每个元素含 `text`/`image`/`video`/`multi_images` 键。
- **排序**：`input.query` 与 `input.documents` 必须同级嵌套于 `input` 对象内；`qwen3-vl-rerank` 支持 `{"text": "..."}` 或 `{"image": "..."}` 形式。

## 限制和注意事项

- **Token 限制严格**：超限直接返回 HTTP 400 错误，**不会截断**。例如 `text-embedding-v4` 单行上限 8,192 Token，`qwen3-vl-rerank` Query 上限 4,000 Token。
- **地域差异**：北京与新加坡地域的模型免费额度、单价、部分参数支持度不同（如 `qwen3.7-text-embedding` 在新加坡无免费额度），需按实际部署地域查表。
- **异步任务生命周期**：批处理任务结果 URL 有效期仅 **24 小时**，需及时下载；并发运行中任务上限为 3 个，排队中总数上限为 50 个。
- **模型兼容性**：`gte-rerank-v2` 和 `qwen3-vl-rerank` **不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**，调用会返回 `model_not_supported` 错误；`qwen2.5-vl-embedding` 仅支持融合向量，不支持 `enable_fusion` 参数（因其恒为融合模式）。
- **多模态融合约束**：`qwen3-vl-embedding` 启用 `enable_fusion=true` 时，`contents` 中所有元素将被融合；而 `tongyi-embedding-vision-plus-2026-03-06` 的融合需将多模态字段置于**同一 content 对象内**（如 `{"text": "...", "image": "..."}`），二者机制不同。

## 来源文档

- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)


