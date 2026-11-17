# vector and sort

百炼平台提供文本向量化（vector）与语义排序（rerank）两类核心能力，分别用于将非结构化内容映射到统一语义空间、以及对召回结果进行精细化相关性重排。二者常协同用于RAG、搜索、推荐等场景：先用向量模型生成Embedding并构建向量库，再用排序模型对检索出的候选集进行最终打分排序。

## 支持的模型/功能

- **通用文本向量**：支持同步（`qwen3.7-text-embedding`, `text-embedding-v4`, `text-embedding-v3` 等）和异步批处理（`text-embedding-async-v2`）两种调用模式，适用于语义搜索、聚类等任务 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **多模态向量**：支持文本、图像、视频及其组合输入，提供独立向量（各模态单独编码）与融合向量（跨模态联合编码）两种模式，模型包括 `qwen3-vl-embedding`、`tongyi-embedding-vision-plus-2026-03-06` 等 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。
- **文本与多模态排序（Rerank）**：支持纯文本（`qwen3-rerank`, `qwen3.7-text-rerank`）、跨模态（`qwen3-vl-rerank`）及兼容旧版的 `gte-rerank-v2`；其中 `gte-rerank` 模型将于2026年05月30日下线，[文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md) 文档已明确提示迁移建议。

> **注意**：文档 2 中 `text-embedding-v1` 的语种支持范围（仅6种）与文档 4 中 `text-embedding-async-v1` 的语种支持范围（同为6种）一致，但文档 2 明确列出其无免费额度，而文档 4 未提及其免费额度，存在信息缺失；以文档 2 为准，`text-embedding-v1` 无免费额度。

## 关键参数

| 参数 | 适用模型 | 说明 |
|------|----------|------|
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding`, `qwen2.5-vl-embedding`, `tongyi-*` 系列多模态模型 | 指定向量维度，不同模型支持值不同（如 `qwen3-vl-embedding` 支持 2560/2048/.../256，默认2560），`multimodal-embedding-v1` 不支持该参数。 |
| `encoding_format` | 同步文本向量（`text-embedding-*`） | 控制返回格式（`float` 或 `base64`），但受网关限制：老网关始终返回 `float`；新网关仅短请求按设置返回，长请求仍回落至 `float` [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。 |
| `enable_fusion` | `qwen3-vl-embedding` | 布尔值，设为 `true` 时启用融合向量模式（将所有输入融合为1个向量）；其他模型如 `tongyi-embedding-vision-plus-2026-03-06` 则通过将 `text`/`image`/`video` 放在同一 `content` 对象中实现融合，不使用此参数。 |
| `instruct` | `qwen3.7-text-rerank`, `qwen3-rerank`, `qwen3-vl-rerank` | 自定义任务指令（如 `"Given a web search query, retrieve relevant passages..."`），影响排序策略，仅英文有效；未指定则默认按问答检索任务执行。 |
| `text_type` | 异步文本向量（`text-embedding-async-v1/v2`） | 指定文本类型：`document`（底库文本，默认）或 `query`（查询文本），对检索类非对称任务效果更优。 |

## 使用方式

- **同步向量调用**：推荐使用 OpenAI 兼容 SDK（需配置 `base_url` 为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`），支持单文本、字符串列表、文件三种 `input` 格式；注意 `qwen3.7-text-embedding` 单行最长支持 128,000 [Token](../concepts/token.md)，而 `text-embedding-v4` 仅支持 8,192 [Token](../concepts/token.md)。
- **异步批处理**：仅支持 HTTP 或 DashScope SDK 提交任务（`X-DashScope-Async: enable` 头必填），输入为远程可访问的文本文件 URL，单次最多 100,000 行；结果需轮询 `GET /api/v1/tasks/{task_id}` 获取，任务数据保留 24 小时。
- **多模态向量调用**：HTTP endpoint 为 `POST https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`，`input.contents` 数组支持混合 `text`/`image`/`video`/`multi_images` 条目；融合向量需按模型要求设置 `enable_fusion=true` 或将多模态字段置于同一对象内。
- **排序调用**：HTTP 接口统一为 `POST /api/v1/services/rerank/text-rerank/text-rerank`，`input.query` 和 `input.documents` 为必填；`qwen3-rerank` 和 `qwen3.7-text-rerank` 还支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（`POST /compatible-api/v1/reranks`），参数扁平化，无需嵌套 `input`/`parameters`。

## 限制和注意事项

- **地域差异**：北京与新加坡地域的模型价格、免费额度、[Token](../concepts/token.md) 限制可能不同（如 `qwen3.7-text-embedding` 北京有100万Token免费额度，新加坡无），调用前务必确认地域配置 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **限流策略**：同步接口遵循全局速率限制；异步批处理有严格并发控制——单用户最多 3 个作业并发运行，排队中+运行中总数不超过 50 个 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **输入长度与计费**：`qwen3-vl-rerank` 的“请求最大输入Token”计算公式为 `Query Tokens × Document 数量 + Document Tokens 总和`，超限直接返回 400 错误，**不会自动截断**；多模态模型对图片/视频大小、格式、数量均有硬性限制（如 `tongyi-embedding-vision-plus` 单张图 ≤3 MB，最多8张）。
- **模型弃用**：`gte-rerank` 系列模型已进入下线倒计时，新项目应优先选用 `qwen3-rerank`；`text-embedding-v1/v2` 无免费额度且能力较新模型弱，建议升级至 `v3/v4` 或 `qwen3.7-text-embedding`。

## 来源文档

- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)
- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)


