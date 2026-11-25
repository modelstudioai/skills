# vector and sort

百炼平台的 `vector and sort` 功能涵盖文本/多模态向量化（Embedding）与检索后重排序（Rerank）两大核心能力，支撑语义搜索、RAG、跨模态检索等关键场景。向量模型将原始内容映射到统一语义空间，排序模型则对召回结果进行精细化相关性打分与重排，二者常协同使用构成完整的检索增强链路。

## 支持的模型/功能

### 文本向量模型
- **同步接口**：支持 `qwen3.7-text-embedding`（最高128K Token）、`text-embedding-v4/v3/v2/v1` 及 `qwen3.7-text-embedding-flash`，适用于实时低延迟场景 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **批处理接口**：提供 `text-embedding-async-v1/v2`，单次请求最多支持100,000行文本，适合大规模离线向量化任务 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。

### 多模态向量模型
支持文本、图像、视频及其组合的联合向量化，包括：
- `qwen3-vl-embedding`（支持独立/融合向量，最大32K文本Token，10MB图片）
- `tongyi-embedding-vision-plus-2026-03-06` 等系列（支持多图、30+语言）
- 所有模型均在同一语义空间生成向量，可直接跨模态计算余弦相似度 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

### 排序（Rerank）模型
- **文本排序**：`qwen3.7-text-rerank`（支持120K总Token）、`qwen3-rerank`（推荐替代已下线的 `gte-rerank`）。
- **多模态排序**：`qwen3-vl-rerank` 支持文本/图片/视频混合查询与文档排序，支持 `fps` 参数控制视频抽帧密度。
> **注意**：`gte-rerank` 系列模型将于2026年05月30日下线，文档明确提示应迁移至 `qwen3-rerank` [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。

## 关键参数

| 参数 | 适用模型 | 说明 |
|------|----------|------|
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v3/v4` | 指定向量维度（如1024、2048），默认1024；`text-embedding-v1/v2` 和多模态模型不支持此参数 |
| `encoding_format` | 同步接口所有模型 | 控制返回格式为 `float` 或 `base64`；但[同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)指出：老网关及长请求强制返回 `float`，实际行为受网关路由影响 |
| `enable_fusion` | `qwen3-vl-embedding` | 设为 `true` 启用多模态融合向量（单输入生成1个融合向量）；其他模型通过输入结构隐式区分（如 `multi_images`） |
| `instruct` | `qwen3.7-text-rerank`, `qwen3-rerank`, `qwen3-vl-rerank` | 自定义排序任务指令（如 `"Retrieve semantically similar text."`），显著影响打分逻辑 |
| `top_n` | 所有Rerank模型 | 返回前N个排序结果；若大于文档总数则返回全部 |

## 使用方式

### 向量化调用
- **同步调用**：使用 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 DashScope HTTP API，`input` 可为字符串、字符串数组或文件URL。示例：
  ```python
  client.embeddings.create(model="qwen3.7-text-embedding", input=["文本A", "文本B"], dimensions=1024)
  ```
- **异步批处理**：仅支持 HTTP，需两步操作：1) `POST /api/v1/services/embeddings/text-embedding/text-embedding` 创建任务（含 `X-DashScope-Async: enable` 头）；2) `GET /api/v1/tasks/{task_id}` 查询结果 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。

### 排序调用
- **HTTP 请求体结构统一**：`input.query` + `input.documents` 数组，`parameters` 中配置 `top_n`、`instruct` 等。
- **多模态支持**：`qwen3-vl-rerank` 的 `query` 和 `documents` 元素可为 `{ "text": "..." }`、`{ "image": "url" }` 或 `{ "video": "url" }` 对象。
- **OpenAI 兼容**：`qwen3-rerank` 和 `qwen3.7-text-rerank` 支持 OpenAI 风格 `/rerank` 接口（需配置对应 `base_url`）。

## 限制和注意事项

- **Token 与数量限制**：
  - `text-embedding-v4/v3` 单行最多 8,192 Token；`qwen3.7-text-embedding` 支持 128,000 Token；`text-embedding-v1/v2` 仅 2,048 Token。
  - 批处理 `text-embedding-async-v2` 单次最多 100,000 行，但并发运行中任务数上限为 3 个。
  - Rerank 模型 `qwen3-vl-rerank` 对图片/视频文档数有限制（图片≤40，视频≤4），且 `request_max_tokens = query_tokens × doc_count + sum(doc_tokens)` 不得超过 120,000。

- **地域与计费差异**：北京与新加坡地域的模型列表、单价、免费额度存在差异（如 `qwen3.7-text-embedding` 在北京有免费额度，在新加坡无），调用前需确认地域配置 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。

- **网关兼容性风险**：`encoding_format=base64` 在长请求或老网关下会被忽略，始终返回 `float`，开发者需在客户端做好容错处理。

- **模型能力边界**：`multimodal-embedding-v1` 固定1024维且不支持 `dimensions` 参数；`qwen2.5-vl-embedding` 仅支持融合向量，不支持独立向量或多图输入。

## 来源文档

- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


