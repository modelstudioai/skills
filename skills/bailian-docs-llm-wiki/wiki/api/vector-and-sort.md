# vector and sort

百炼平台提供文本向量（embedding）、多模态向量（multimodal embedding）和排序（rerank）三大核心能力，覆盖语义检索、RAG、跨模态搜索等典型AI应用链路。所有能力均支持同步与异步调用，适配OpenAI兼容接口与DashScope原生SDK，开发者可根据数据规模、延迟敏感度和模态需求灵活选型。详细模型能力与参数约束请参考下文结构化说明。

## 支持的模型/功能

- **通用文本向量**：支持同步与批处理两种模式。同步接口适用于小批量、低延迟场景（如单次≤20条文本），批处理接口适用于大规模文件向量化（如10万行文本）。主流模型包括 `qwen3.7-text-embedding`（最高128K Token/行）、`text-embedding-v4`（支持64–2560维可调）及历史版本 `text-embedding-v2/v3`。详见 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md) 和 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
  
- **多模态向量**：支持文本、图像、视频统一语义空间表征，提供**独立向量**（每模态各1个向量）与**融合向量**（多模态输入融合为1个向量）两种模式。主力模型包括 `qwen3-vl-embedding`（支持`enable_fusion=true`）、`tongyi-embedding-vision-plus-2026-03-06`（支持多图+视频+文本混合融合）及轻量版 `tongyi-embedding-vision-flash-2026-03-06`。[Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md) 提供完整输入格式与维度配置说明。

- **排序模型（Rerank）**：对召回结果进行二次精排，提升相关性。支持纯文本（`qwen3-rerank`, `qwen3.7-text-rerank`）、多模态（`qwen3-vl-rerank`）及兼容旧版（`gte-rerank-v2`）三类模型。其中 `gte-rerank` 系列将于2026年5月30日下线，[排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md) 文档已明确迁移建议。

> **注意**：`qwen2.5-vl-embedding` 仅支持融合向量且不支持多图输入；而 `tongyi-embedding-vision-plus`（无后缀）仅支持独立向量，不支持 `enable_fusion` 参数——该矛盾在 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md) 中已通过模型能力对照表澄清，以该文档为准。

## 关键参数

| 参数 | 适用场景 | 说明 |
|--------|-----------|------|
| `text_type` | 批处理文本向量（`text-embedding-async-v1/v2`） | 取值 `document`（默认，用于底库）或 `query`（用于检索查询），影响向量表征方向，对检索效果至关重要。 |
| `enable_fusion` | `qwen3-vl-embedding` 多模态向量 | `true` 时将 `contents` 中所有输入融合为1个向量；`false` 或未设置时返回独立向量。其他模型（如 `tongyi-embedding-vision-plus-2026-03-06`）通过**同个 content 对象内混写 text/image/video** 实现融合，不依赖此参数。 |
| `instruct` | 所有 rerank 模型（除 `qwen3-rerank` 外） | 控制排序策略，如 `"Given a web search query, retrieve relevant passages..."`（问答检索）或 `"Retrieve semantically similar text."`（语义相似度）。`qwen3-rerank` 不支持该参数。 |
| `dimensions` / `dimension` | 同步文本向量 / 多模态向量 | 同步接口用 `dimensions`（OpenAI兼容），多模态接口用 `dimension`（DashScope原生）。注意 `tongyi-embedding-vision-plus` 等旧模型不支持该参数，固定维度。 |
| `top_n` | rerank 模型 | 返回前 N 个结果，默认返回全部。`qwen3-rerank` 的 `top_n` 与 `model` 同级，而其他模型需置于 `parameters` 内。 |

## 使用方式

- **同步调用（推荐小批量）**：使用 `/compatible-mode/v1/embeddings`（OpenAI兼容）或 `/api/v1/services/embeddings/text-embedding/text-embedding`（DashScope原生，需 `X-DashScope-Async: disable`）。支持字符串、字符串数组、本地文件三种 `input` 格式，`qwen3.7-text-embedding` 单行最高支持128K Token。示例见 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。

- **异步批处理（推荐大批量）**：仅 DashScope 原生接口支持，必须设置请求头 `X-DashScope-Async: enable`。输入为公开可访问的文本文件 URL（一行一条），单文件最大200MB、10万行、单行2048 Token。创建任务后需轮询 `GET /api/v1/tasks/{task_id}` 获取结果URL。详见 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。

- **多模态与rerank调用**：统一使用 `POST /api/v1/services/embeddings/multimodal-embedding/multimodal-embedding` 或 `POST /api/v1/services/rerank/text-rerank/text-rerank`（部分rerank模型用 `/compatible-api/v1/reranks`）。输入 `contents` 或 `documents` 为数组，每个元素为 `{ "text": "...", "image": "...", "video": "..." }` 结构。SDK 调用时参数扁平化（如 `text_rerank(..., query="...", documents=[...])`），无需嵌套 `input`。

## 限制和注意事项

- **地域与Endpoint差异**：北京地域使用 `cn-beijing.maas.aliyuncs.com`，新加坡用 `ap-southeast-1.maas.aliyuncs.com`；多模态向量统一使用 `dashscope.aliyuncs.com` 公共域名，而文本向量与rerank需替换 `{WorkspaceId}`。Base URL 配置错误是常见失败原因。
  
- **Token计费与限流**：
  - 文本向量批处理：单用户并发运行中任务 ≤3 个，排队中+运行中总数 ≤50 个；`text-embedding-async-v2` 免费额度为2000万Token/90天。
  - 多模态向量：`qwen3-vl-embedding` 视频输入上限50MB，图片单张10MB；`tongyi-embedding-vision-plus-2026-03-06` 单次请求内容元素总数 ≤20（图片≤64张，视频≤8个）。
  - Rerank：`qwen3-vl-rerank` 单次最多500个文档，但图片/视频类型有单独限制（图片≤40，视频≤4）；`qwen3.7-text-rerank` 请求总Token = `Query Tokens × Document 数量 + Document Tokens 总和`，上限120K。

- **关键兼容性警告**：
  - `encoding_format="base64"` 在长请求（如大文件）中可能被降级为 `float`，因路由至老网关——此行为在 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md) 中已明确说明。
  - `qwen3-rerank` 接口路径、参数层级（`query`/`documents` 与 `model` 同级）、响应结构（无 `output` 包裹）与其他rerank模型完全不兼容，不可混用。
  - 所有模型均要求 `Authorization: Bearer <API_KEY>`，缺失或格式错误（如漏掉 `Bearer`）将返回 `InvalidApiKey` 错误。

## 来源文档

- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)
- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)


