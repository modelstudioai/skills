# vector and sort

百炼平台提供文本向量化（vector）与语义排序（sort / rerank）两类核心能力，分别用于将非结构化内容映射到统一语义空间、以及对召回结果进行精细化相关性重排。二者常协同用于RAG、搜索、推荐等场景：先通过向量检索快速召回候选集，再用排序模型提升Top-K结果的精准度。

## 支持的模型/功能

### 文本向量模型
- **同步接口**：支持 `qwen3.7-text-embedding`（2560维/128K token）、`text-embedding-v4`（2048维/8K token）、`qwen3.7-text-embedding-flash`（1024维/128K token）等多版本模型，适用于实时低延迟场景 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **异步批处理**：`text-embedding-async-v2`（1536维/2K token/10万行）专为大规模离线向量化设计，需通过任务ID轮询结果 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **多模态向量**：`qwen3-vl-embedding`、`tongyi-embedding-vision-plus-2026-03-06` 等支持文本、图像、视频跨模态统一编码，可生成独立向量或融合向量 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

### 排序（Rerank）模型
- **文本排序**：`qwen3.7-text-rerank`（500文档/120K总token）、`qwen3-rerank`（4K单文档token）支持中英等201种语种；`gte-rerank-v2` 已进入下线倒计时（2026-05-30），请尽快迁移 [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。
- **多模态排序**：`qwen3-vl-rerank` 支持文本、图片、视频混合查询与排序，支持 `fps` 参数控制视频帧采样率。

> **注意**：`text-embedding-async-v1` 在文档2中未列出免费额度，而文档5中 `text-embedding-v1` 明确标注“无免费额度”，但二者命名逻辑不一致；实际使用应以控制台配额页或最新计费文档为准，避免依赖旧版异步v1模型。

## 关键参数

| 参数 | 适用模型 | 说明 |
|------|----------|------|
| `text_type` | `text-embedding-async-*` | 指定 `document`（底库文本）或 `query`（查询文本），影响向量表征方向，对检索效果至关重要 |
| `enable_fusion` | `qwen3-vl-embedding` | 设为 `true` 时将 contents 中所有模态输入融合为单个向量；其他模型如 `tongyi-embedding-vision-plus-2026-03-06` 通过同 content 对象内多模态字段隐式启用融合 |
| `instruct` | `qwen3.7-text-rerank`, `qwen3-rerank`, `qwen3-vl-rerank` | 控制排序策略，如 `"Given a web search query..."`（问答检索）或 `"Retrieve semantically similar text."`（语义相似度） |
| `dimension` | 多数向量模型 | 指定向量维度（如 `qwen3.7-text-embedding` 支持 2560/2048/1536...），影响精度与存储开销；`multimodal-embedding-v1` 不支持该参数 |
| `fps` | `qwen3-vl-rerank` | 视频帧率控制，取值 (0, 5]，默认 1.0，降低值可减少计算量 |

## 使用方式

### 向量生成
- **同步调用（推荐实时场景）**：使用 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 DashScope SDK，直接传入字符串、字符串数组或文件流。例如：
  ```python
  client.embeddings.create(model="qwen3.7-text-embedding", input=["文本A", "文本B"], dimensions=1024)
  ```
- **异步批处理（推荐离线场景）**：上传文本文件 URL，创建任务后轮询 `task_id` 获取结果 URL。HTTP 调用必须携带 `X-DashScope-Async: enable` 请求头 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **多模态向量**：通过 `contents` 数组传入 `{"text": "..."}, {"image": "..."}, {"video": "..."}` 等对象，融合模式需按模型要求组织（如 `qwen3-vl-embedding` 需设 `enable_fusion=true`，而 `tongyi-embedding-vision-plus-2026-03-06` 需将多模态字段置于同一字典内）。

### 排序调用
- **HTTP 接口**：`input` 内嵌 `query` 与 `documents`，`parameters` 包含 `top_n`、`instruct` 等。`qwen3-vl-rerank` 的 `query` 和 `documents` 元素均支持模态字典（如 `{"image": "url"}`）。
- **[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**：仅 `qwen3-rerank` 和 `qwen3.7-text-rerank` 支持，请求体扁平化（`query`、`documents` 与 `model` 同级），endpoint 为 `/compatible-api/v1/reranks`。

## 限制和注意事项

- **限流与配额**：
  - 异步向量任务：单用户并发运行中任务 ≤ 3 个，排队中+运行中总数 ≤ 50 个 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
  - 免费额度：多数新模型（如 `qwen3.7-text-embedding`）提供 100 万 [Token](../concepts/token.md) 90 天免费额度，但 `text-embedding-v2`、`text-embedding-v3` 等旧版无免费额度，需注意成本规划。
- **输入约束**：
  - 同步文本向量：`qwen3.7-text-embedding` 单行最长 128,000 [Token](../concepts/token.md)，而 `text-embedding-v2` 仅支持 2,048 [Token](../concepts/token.md)，模型选型需严格匹配业务长度需求。
  - 多模态向量：`qwen2.5-vl-embedding` 仅支持融合向量且不支持 `multi_images`，而 `tongyi-embedding-vision-plus` 仅支持独立向量——二者能力互斥，不可混用 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。
- **兼容性**：
  - `gte-rerank-v2` 不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，调用时会返回 `model_not_supported` 错误；`qwen3-vl-rerank` 的 `instruct` 参数在 OpenAI 兼容接口中同样生效。
  - `encoding_format` 在 OpenAI 兼容接口中存在网关差异：长请求强制返回 `float`，无法保证 `base64` 输出，生产环境应做降级处理。

## 来源文档

- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)


