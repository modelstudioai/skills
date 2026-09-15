# vector and sort

百炼平台提供文本向量（embedding）与排序（rerank）两类核心语义理解能力，分别用于将非结构化内容映射至统一语义空间，以及对召回结果进行精细化相关性重排序。二者常组合应用于RAG、语义搜索、推荐系统等场景：先通过向量模型生成查询与文档的嵌入向量并计算相似度完成初步召回，再用排序模型对Top-K候选结果进行二次打分排序，显著提升最终结果的相关性与准确性。所有模型均支持多语种输入，并提供同步/异步两种调用方式以适配不同吞吐与延迟需求。

## 支持的模型/功能

### 文本向量模型
- **同步接口**：支持 `qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3`、`text-embedding-v2`、`text-embedding-v1` 等通用文本向量模型，适用于低延迟、小批量（≤20行）场景 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **批处理接口**：支持 `text-embedding-async-v2`（推荐）、`text-embedding-async-v1`，适用于超大批量（最高100,000行）离线向量化任务，采用异步提交+结果轮询模式 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **多模态向量模型**：支持 `qwen3-vl-embedding`、`tongyi-embedding-vision-plus-2026-03-06` 等，可处理文本、图像、视频及其组合输入，生成独立向量或跨模态融合向量，统一语义空间 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

### 排序（Rerank）模型
- **文本排序**：`qwen3-rerank`（当前主力推荐）、`qwen3.7-text-rerank`、`gte-rerank-v2`（将于2026年5月30日下线），支持最多500个文档的单次排序，适用于纯文本检索与RAG精排。
- **多模态排序**：`qwen3-vl-rerank`，支持文本、图片、视频混合查询与文档，适用于跨模态搜索与图文匹配场景。

> **注意**：`gte-rerank` 系列模型已明确进入下线流程，新项目应优先选用 `qwen3-rerank`；其接口路径、参数结构与旧模型存在差异，迁移时需参考 [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md) 文档调整代码。

## 关键参数

| 参数 | 适用模型 | 说明 | 是否必选 |
|--------|-----------|------|----------|
| `model` | 全部 | 模型名称，如 `"qwen3-rerank"`、`"qwen3-vl-embedding"` | 是 |
| `input` / `query` + `documents` | 向量/排序 | 向量模型：`input` 可为字符串、字符串数组或文件URL；排序模型：`query`（字符串或对象）与 `documents`（字符串数组或对象数组）分离 | 是 |
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding` 等 | 指定向量维度（如 `1024`, `2048`），不同模型支持值不同；`text-embedding-v2/v1` 和 `multimodal-embedding-v1` 不支持此参数 | 否（默认值见各模型说明） |
| `text_type` | `text-embedding-async-v2` | 区分 `"document"`（底库文本）与 `"query"`（查询文本），影响向量表征策略，检索场景建议显式指定 | 否（默认 `"document"`） |
| `enable_fusion` | `qwen3-vl-embedding` | 设为 `true` 时启用多模态融合向量（单输入→单向量）；不设则为独立向量（多输入→多向量） | 否（仅融合场景需设） |
| `top_n` | 排序模型 | 返回排序后前 `n` 个结果，不设则返回全部 | 否 |
| `instruct` | `qwen3.7-text-rerank`, `qwen3-rerank`, `qwen3-vl-rerank` | 自定义排序任务指令（如 `"Retrieve semantically similar text."`），显著影响打分逻辑 | 否（但强烈建议设置以提升效果） |

## 使用方式

### 调用路径选择
- **低延迟、小批量（<20条文本）**：使用同步向量API（OpenAI兼容或DashScope原生）或 `qwen3-rerank` 的 `/compatible-api/v1/reranks` 路径。
- **高吞吐、大批量（>1000条文本）**：使用批处理向量API（`text-embedding-async-v2`）或排序模型的 `/api/v1/services/rerank/...` 路径。
- **多模态输入**：必须使用 `multimodal-embedding` 或 `qwen3-vl-rerank` 对应的专用API端点，不可混用文本模型。

### SDK 与 HTTP 差异
- 向量模型：同步调用推荐 OpenAI 兼容 SDK（`client.embeddings.create`），批处理推荐 DashScope SDK 的 `BatchTextEmbedding.call`；HTTP 需严格遵循 `X-DashScope-Async: enable` 头（批处理）或 `base_url` 地域配置。
- 排序模型：`qwen3-rerank` 使用 OpenAI 兼容路径，参数扁平（`query`, `documents`, `top_n` 同级）；其余模型使用原生路径，参数嵌套在 `input` 和 `parameters` 中。详见 [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。

### 多模态输入格式示例
- **独立向量**（每模态一个向量）：
  ```json
  "contents": [{"text":"猫"}, {"image":"https://..."}]
  ```
- **融合向量**（所有模态融合为一个向量）：
  ```json
  "contents": [{"text":"猫", "image":"https://..."}]  // 同一对象内混合
  ```

## 限制和注意事项

- **[Token](../concepts/token.md) 与尺寸限制**：
  - 同步文本向量：`qwen3.7-text-embedding` 单行最长 128,000 [Token](../concepts/token.md)；`text-embedding-v4` 为 8,192 [Token](../concepts/token.md)；`text-embedding-v2/v1` 为 2,048 Token。
  - 批处理文本向量：`text-embedding-async-v2` 单行 ≤2,048 Token，单次请求 ≤100,000 行。
  - 多模态向量：`qwen3-vl-embedding` 图片 ≤10 MB，视频 ≤50 MB；`tongyi-embedding-vision-plus` 图片 ≤3 MB，视频 ≤10 MB。
  - 排序模型：`qwen3-rerank` 单文档 ≤4,000 Token；`qwen3.7-text-rerank` 单文档 ≤30,000 Token；总请求 Token ≤120,000。

- **地域与免费额度**：
  - 北京地域部分模型（如 `qwen3.7-text-embedding`）提供90天内100万Token免费额度；新加坡地域无免费额度 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
  - 批处理模型 `text-embedding-async-v2` 提供2000万Token免费额度（90天） [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。

- **关键兼容性说明**：
  > **注意**：`encoding_format` 参数在“老网关”下始终返回 `float`，不支持 `base64` 输出；仅“新网关”的短请求才按参数生效。长请求（如大文本）会自动路由至老网关，开发者需在代码中做好格式兼容处理 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
  >
  > **注意**：`qwen2.5-vl-embedding` 仅支持融合向量，且不支持 `multi_images`；而 `tongyi-embedding-vision-plus` 仅支持独立向量，不支持 `enable_fusion`。模型能力差异显著，选型时务必核对 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md) 中的“模型能力对照”表格。

- **其他**：
  - 批处理任务结果 URL 有效期仅24小时，需及时下载。
  - `qwen3-vl-rerank` 的 `fps` 参数仅对视频生效，范围 `[0,1]`，默认 `1.0`（全帧抽取）。
  - 所有模型均要求 `Authorization: Bearer <API_KEY>` 请求头，且 `DASHSCOPE_API_KEY` 必须正确配置。

## 来源文档

- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


