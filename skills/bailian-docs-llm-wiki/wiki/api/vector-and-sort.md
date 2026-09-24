# vector and sort

百炼平台提供文本向量化（vector）与语义排序（sort / rerank）两类核心能力，分别用于将非结构化内容映射到统一语义空间、以及对召回结果进行精细化相关性重排序。二者常协同用于RAG、检索增强、跨模态搜索等场景，支持纯文本、多模态（图文/视频）等多种输入形式。

## 支持的模型与功能

- **通用文本向量**：支持同步与异步两种调用模式。同步接口（如 `qwen3.7-text-embedding`、`text-embedding-v4`）适用于小批量、低延迟场景；异步批处理接口（如 `text-embedding-async-v2`）适用于大规模文件（单次最多100,000行，文件≤200MB）[批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。  
- **多模态向量**：支持文本、图像、视频的独立向量与融合向量生成。`qwen3-vl-embedding` 和 `tongyi-embedding-vision-plus-2026-03-06` 同时支持两种模式；`qwen2.5-vl-embedding` 仅支持融合向量；`tongyi-embedding-vision-plus` 等旧版仅支持独立向量 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。  
- **文本排序（Rerank）**：提供 `qwen3-rerank`（推荐主力模型）、`qwen3.7-text-rerank`、`qwen3-vl-rerank`（支持图文/视频混合排序）及已进入下线过渡期的 `gte-rerank-v2`（将于2026年05月30日下线）[文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。

> **注意**：文档中 `text-embedding-async-v1` 的语种支持范围（仅6种）明显窄于 `text-embedding-async-v2`（10种），且未在任何新版文档中被提及或推荐，应视为已过时模型，生产环境请优先选用 `v2` 或同步系列新模型。

## 关键参数

| 参数 | 适用模型 | 说明 |
|------|----------|------|
| `text_type` | `text-embedding-async-*` | 取值 `document`（默认，用于底库）或 `query`（用于检索查询），影响向量表征方向，对检索效果有显著影响。 |
| `enable_fusion` | `qwen3-vl-embedding` | `true` 时启用融合向量（单输入多模态融合为1个向量）；其他模型通过输入结构隐式控制（如将 text/image/video 放入同一 content 对象）。 |
| `dimension` | 多数向量模型 | 指定输出向量维度（如 `qwen3.7-text-embedding` 支持 2560/2048/1536/1024/768/512/256；`text-embedding-v4` 额外支持 128/64）。`tongyi-embedding-vision-plus` 等旧模型不支持该参数。 |
| `instruct` | `qwen3.7-text-rerank` / `qwen3-rerank` / `qwen3-vl-rerank` | 自定义任务指令，如 `"Given a web search query, retrieve relevant passages that answer the query."`（问答检索）或 `"Retrieve semantically similar text."`（语义相似度），直接影响排序策略。 |
| `top_n` | 所有 rerank 模型 | 返回排序后前 N 个结果，默认返回全部。 |

## 使用方式

- **同步向量调用**：使用 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)（`/compatible-mode/v1/embeddings`）或 DashScope SDK `TextEmbedding.call()`，支持字符串、字符串数组、本地文件输入。注意各模型对单行 [Token](../concepts/token.md) 数（如 `text-embedding-v4` 限 8,192）和最大行数（如 `qwen3.7-text-embedding` 限 20 行）的硬性约束 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。  
- **异步向量批处理**：必须通过两步完成——先 `POST /api/v1/services/embeddings/text-embedding/text-embedding` 创建任务（需设 `X-DashScope-Async: enable`），再 `GET /api/v1/tasks/{task_id}` 轮询结果。SDK 提供 `BatchTextEmbedding.async_call()` 封装轮询逻辑。  
- **多模态向量**：统一使用 `POST /api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`，通过 `input.contents` 数组传入 `{text: "..."}, {image: "..."}, {video: "..."}` 等对象。融合向量需按模型要求设置 `enable_fusion=true` 或将多模态字段置于同一字典内。  
- **排序调用**：`qwen3-rerank` 使用独立 endpoint `/compatible-api/v1/reranks` 且参数扁平（`query`, `documents` 与 `model` 同级）；其余 rerank 模型使用 `/api/v1/services/rerank/text-rerank/text-rerank`，参数需嵌套在 `input` 对象中。SDK 中统一使用 `TextReRank.call()`。

## 限制和注意事项

- **地域与Endpoint差异**：北京地域使用 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，新加坡地域需替换为 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`；多模态向量 HTTP 接口固定使用 `dashscope.aliyuncs.com` 域名，不依赖 WorkspaceId。  
- **[Token](../concepts/token.md) 计费规则**：向量模型按“输入 [Token](../concepts/token.md) 数”计费（文本/图片/视频分开计）；rerank 模型按 `Query Tokens × Document 数量 + Document Tokens 总和` 计算总 Token。免费额度有效期均为开通后90天（部分模型如 `multimodal-embedding-v1` 为自开通/发布日起90天）。  
- **异步任务生命周期**：异步任务 ID 有效期仅 24 小时，结果 URL 也仅保留 24 小时，务必及时下载。同时运行中任务上限为 3 个，并发排队任务上限为 50 个。  
- **模型兼容性**：`gte-rerank` 系列已明确进入下线流程，新项目禁止接入；`text-embedding-v1/v2` 为旧版模型，新需求应优先选用 `qwen3.7-text-embedding` 或 `text-embedding-v4`。  
- **输入格式安全**：所有 URL 必须公开可访问；Base64 图片需符合 `data:image/{format};base64,{data}` 格式；视频仅支持 URL 且需为 H.264/H.265 编码（`tongyi-embedding-vision-plus` 等旧版仅支持 MP4/MOV/AVI）。

## 来源文档

- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)
- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)


