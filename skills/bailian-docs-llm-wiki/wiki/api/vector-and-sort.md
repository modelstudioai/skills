# vector and sort

百炼平台提供两类核心语义处理能力：**向量（Vector）** 与 **排序（Sort/Rerank）**。向量模型将文本、图像、视频等多模态内容映射到统一语义空间，生成稠密向量，支撑检索、聚类、分类等任务；排序模型则对召回的候选结果进行精细化相关性重排，显著提升最终结果的准确率。二者常组合使用，构成 RAG、智能搜索等应用的底层语义理解双引擎。

## 支持的模型/功能

### 文本向量模型
- **同步接口**：支持 `qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3`、`text-embedding-v2`、`text-embedding-v1` 等通用文本向量模型，适用于低延迟、小批量场景（如实时查询向量化）。详细参数与模型能力见 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **批处理接口**：支持 `text-embedding-async-v2` 和 `text-embedding-async-v1`，专为大规模离线向量化设计，单次请求最多处理 100,000 行文本，文件大小上限 200MB，适合构建向量数据库底库。参见 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **多模态向量模型**：支持 `qwen3-vl-embedding`、`tongyi-embedding-vision-plus-2026-03-06` 等，可将文本、图像、视频统一编码至同一语义空间，支持独立向量（每模态各一向量）与融合向量（多模态输入合成单一向量）两种模式。详见 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

### 排序（Rerank）模型
- **文本排序**：`qwen3-rerank`（推荐主力）、`qwen3.7-text-rerank`、`gte-rerank-v2`（将于2026年05月30日下线），支持最大500文档/请求，适用于纯文本语义重排。
- **多模态排序**：`qwen3-vl-rerank`，支持文本、图片、视频混合查询与文档，最大文档数按类型区分（文本100、图片40、视频4），是跨模态搜索的关键组件。

> **注意**：`gte-rerank` 系列模型已进入下线流程，[文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md) 文档明确提示“gte-rerank模型将于2026年05月30日下线，推荐使用qwen3-rerank模型替代”，开发者应尽快迁移。

## 关键参数

| 参数 | 适用模型 | 说明 | 是否必选 |
|------|----------|------|----------|
| `model` | 全部 | 模型名称，必须与[模型概览](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)中列出的名称严格一致 | 是 |
| `input` / `query` & `documents` | 向量模型用 `input`；排序模型中 `qwen3-rerank` 直接用 `query`/`documents`，其余用嵌套 `input` | 向量：字符串、字符串列表或文件URL；排序：`query`为字符串或模态对象，`documents`为字符串或模态对象数组 | 是 |
| `dimensions` / `dimension` | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06` 等 | 指定向量维度，不同模型支持值不同（如 `qwen3-vl-embedding` 支持 2560/2048/.../256，默认2560）；`tongyi-embedding-vision-plus` 等旧版不支持此参数 | 否（有默认值） |
| `encoding_format` | 同步向量接口 | 控制返回格式：`float`（默认）或 `base64`；但[同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)指出：“老网关……均只返回`float`类型数据，不支持输出`base64`数据”，新网关长请求也降级为 `float` | 否 |
| `instruct` | `qwen3.7-text-rerank`, `qwen3-rerank`, `qwen3-vl-rerank` | 自定义排序任务指令（如 `"Retrieve semantically similar text."`），影响模型对相关性的判断逻辑 | 否（默认为问答检索） |
| `enable_fusion` | `qwen3-vl-embedding` | `true` 时启用多模态融合向量；`false` 或未设置时为独立向量 | 否（仅融合模式需设） |

## 使用方式

- **同步调用（低延迟）**：适用于单次少量文本（≤20行）或单条长文本（≤128K Token）。使用 OpenAI 兼容 SDK 或 HTTP POST 到 `/compatible-mode/v1/embeddings`（向量）或 `/compatible-api/v1/reranks`（`qwen3-rerank`）。
- **异步批处理（高吞吐）**：适用于海量文本（≤100,000行）。通过 HTTP POST 到 `/api/v1/services/embeddings/text-embedding/text-embedding` 创建任务，再用 `GET /api/v1/tasks/{task_id}` 轮询结果。SDK 提供 `BatchTextEmbedding.async_call()` 封装。
- **多模态调用**：统一使用 `/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding` 接口，`input.contents` 数组内按需组合 `{"text":...}`, `{"image":...}`, `{"video":...}` 等对象。融合向量需将多模态字段置于同一字典内（如 `{"text":..., "image":...}`）或设置 `enable_fusion=true`（`qwen3-vl-embedding`）。

## 限制和注意事项

- **Token 与尺寸限制**：各模型有严格上限。例如 `text-embedding-v4` 单行限 8,192 Token，而 `qwen3.7-text-embedding` 达 128,000 Token；`qwen3-vl-embedding` 图片单张限 10 MB，视频限 50 MB。超限将直接返回 HTTP 400 错误，**不会自动截断**。
- **地域与计费差异**：北京与新加坡地域的模型单价、免费额度不同（如 `qwen3.7-text-embedding` 北京有免费额度，新加坡无），且 `text-embedding-v3` 在新加坡有额外 50万Token 免费额度。务必根据部署地域核对 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md) 中的表格。
- **异步任务生命周期**：批处理任务结果 URL 仅保留 **24 小时**，需及时下载保存；同时运行中任务数上限为 3 个，排队中+运行中总数不超过 50 个。
- **向量空间一致性**：多模态向量模型（如 `qwen3-vl-embedding`）保证文本、图像、视频向量位于**同一语义空间**，可直接用余弦相似度计算跨模态距离；但不同模型（如 `text-embedding-v4` 与 `qwen3-vl-embedding`）的向量**不可混用**，因空间不兼容。
- **SDK 与 HTTP 参数结构差异**：HTTP 接口普遍采用嵌套结构（如 `input.query`, `parameters.top_n`），而 DashScope SDK 采用扁平参数（如 `query=...`, `top_n=...`）。开发时需严格参照对应文档示例，避免因结构错误导致 400 错误。

## 来源文档

- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)
- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)


