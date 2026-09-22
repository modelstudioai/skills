# vector and sort

百炼平台提供两类核心向量与排序能力：**通用文本向量（Text Embedding）**用于将文本映射到语义向量空间，支撑检索、聚类等任务；**排序模型（Rerank）**则对召回结果进行精细化重排序，提升相关性精度。此外，多模态向量支持文本、图像、视频的统一语义表征。所有能力均通过同步/异步API及SDK提供，适配OpenAI兼容接口与原生DashScope协议。

## 支持的模型/功能

- **通用文本向量**：支持同步与异步两种调用模式。同步模型包括 `qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3` 等，适用于低延迟、小批量场景；异步模型 `text-embedding-async-v2` 支持单次10万行、每行2048 [Token](../concepts/token.md)的大规模批处理，详见[同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)和[批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。  
- **多模态向量**：支持文本、图像、视频跨模态统一编码，提供**独立向量**（各模态单独生成向量）与**融合向量**（多模态输入联合编码为单向量）两种模式。主流模型包括 `qwen3-vl-embedding`（支持 `enable_fusion`）、`tongyi-embedding-vision-plus-2026-03-06`（融合向量通过同 content 对象实现）等，详见[Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。  
- **排序模型（Rerank）**：分为纯文本（如 `qwen3-rerank`、`qwen3.7-text-rerank`）与多模态（`qwen3-vl-rerank`）两类。`qwen3-rerank` 使用 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)，而 `qwen3.7-text-rerank` 和 `qwen3-vl-rerank` 使用原生接口；注意 `gte-rerank` 系列将于2026年05月30日下线，应迁移至 `qwen3-rerank`。

> **注意**：文档1中 `text-embedding-v2` 的“最大行数”为25，而文档2中 `text-embedding-async-v2` 的“单次请求文本最大行数”为100,000——二者属不同调用路径（同步 vs 异步），无矛盾；但文档6明确指出 `gte-rerank` 模型即将下线，而文档5仅列出入口链接，未提示生命周期状态，开发时应以文档6为准。

## 关键参数

- **`dimensions`**：指定输出向量维度，仅部分模型支持（如 `qwen3.7-text-embedding`、`text-embedding-v4`、`qwen3-vl-embedding`），取值需严格匹配模型支持列表（如 `qwen3-vl-embedding` 支持 2560/2048/.../256，默认2560）；`tongyi-embedding-vision-plus` 等旧模型不支持该参数，固定维度。  
- **`encoding_format`**（同步文本向量）：控制返回格式为 `float` 或 `base64`，但受网关限制：老网关强制返回 `float`，新网关仅对短请求生效，长请求仍回落至 `float`。  
- **`enable_fusion`**（多模态向量）：仅 `qwen3-vl-embedding` 支持，设为 `true` 时将 `contents` 中所有输入融合为单向量；`tongyi-embedding-vision-plus-2026-03-06` 等新版模型改用“同 content 对象内混合模态”方式实现融合，无需此参数。  
- **`instruct`**（排序模型）：指导排序策略，如 `"Given a web search query, retrieve relevant passages that answer the query."`（问答检索）或 `"Retrieve semantically similar text."`（语义相似度），仅对 `qwen3.7-text-rerank`、`qwen3-rerank`、`qwen3-vl-rerank` 生效。  
- **`text_type`**（异步文本向量）：区分 `document`（底库文本）与 `query`（查询文本），影响向量表征优化，推荐在检索类非对称任务中显式设置。

## 使用方式

- **同步调用（文本向量）**：使用 OpenAI SDK 或 HTTP POST 到 `compatible-mode/v1/embeddings`，支持 `string`、`array<string>`、`file` 三种输入格式。示例中 Python SDK 需配置 `base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"`。  
- **异步调用（文本向量）**：HTTP 调用需设置请求头 `X-DashScope-Async: enable`，并传入文件 URL；SDK 提供 `BatchTextEmbedding.call()`（同步等待）与 `BatchTextEmbedding.async_call()`（返回 task_id）两种封装。  
- **多模态向量**：统一使用 `POST https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`，`input.contents` 数组内按模态类型（`text`/`image`/`video`/`multi_images`）组织数据；融合向量需确保多模态字段位于同一字典内（如 `{"text": "...", "image": "..."}`）。  
- **排序模型**：`qwen3-rerank` 使用 [OpenAI 兼容接口](../concepts/openai-compatible-api.md) `POST /compatible-api/v1/reranks`，参数扁平化（`query`、`documents` 与 `model` 同级）；其余模型使用原生接口 `POST /api/v1/services/rerank/text-rerank/text-rerank`，参数嵌套于 `input` 和 `parameters` 对象中。

## 限制和注意事项

- **[Token](../concepts/token.md) 与尺寸限制**：同步文本向量中，`qwen3.7-text-embedding` 单行上限 128,000 [Token](../concepts/token.md)，而 `text-embedding-v4` 仅 8,192 Token；多模态向量中，`qwen3-vl-embedding` 图片单张≤10 MB，视频≤50 MB；`qwen3-vl-rerank` 视频帧数由 `fps` 参数控制（范围 [0,1]）。  
- **地域与免费额度差异**：北京地域部分模型（如 `qwen3.7-text-embedding`）提供90天内100万Token免费额度，而新加坡地域同名模型无免费额度；异步模型 `text-embedding-async-v2` 免费额度为2000万Token。  
- **接口兼容性**：[OpenAI 兼容接口](../concepts/openai-compatible-api.md)仅支持同步文本向量与 `qwen3-rerank`，不支持多模态向量、异步文本向量及 `qwen3.7-text-rerank` 等原生模型。  
- **任务有效期**：异步批处理任务结果 URL 仅保留24小时，需及时下载；同步请求无此限制，但需自行处理超时与重试。  
- **模型选型建议**：高精度场景优先选用 `text-embedding-v4`（2048维）或 `qwen3-vl-embedding`（2560维）；成本敏感场景可选 `qwen3.7-text-embedding-flash` 或 `tongyi-embedding-vision-flash-2026-03-06`；排序任务务必迁移到 `qwen3-rerank` 以规避 `gte-rerank` 下线风险。

## 来源文档

- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)
- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)


