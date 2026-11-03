# vector and sort

百炼平台提供文本向量化（vector）与文本/[多模态](../concepts/multi-modal.md)排序（sort / rerank）两类核心能力，支撑语义搜索、RAG、聚类、跨模态检索等下游任务。向量模型将原始内容映射到统一语义空间，排序模型则对召回结果进行精细化相关性重排。两类能力既可独立使用，也可组合构建端到端检索系统。

## 支持的模型与功能

### 文本向量模型
- **同步接口**：支持 `qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3`、`text-embedding-v2`、`text-embedding-v1` 等多版本模型，适用于低延迟、小批量场景（如单条Query实时向量化）。详细参数见 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **异步批处理接口**：专为大规模文本向量化设计，支持 `text-embedding-async-v2` 和 `text-embedding-async-v1` 两个模型，适用于百万级文档预处理。该能力在 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md) 中有完整说明。
- **[多模态](../concepts/multi-modal.md)向量模型**：支持文本、图像、视频统一表征，包括 `qwen3-vl-embedding`（支持独立/融合向量）、`qwen2.5-vl-embedding`（仅融合）、`tongyi-embedding-vision-plus-2026-03-06` 等。详见 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

### 排序（Rerank）模型
- **文本排序**：`qwen3.7-text-rerank`（推荐主力）、`qwen3-rerank`（轻量替代）、`gte-rerank-v2`（即将下线，[官方公告](https://www.aliyun.com/notice/118217) 明确其将于2026年05月30日停用）。
- **[多模态](../concepts/multi-modal.md)排序**：`qwen3-vl-rerank` 支持文本、图片、视频混合查询与排序，是跨模态检索的关键组件，文档见 [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。

> **注意**：`gte-rerank` 系列模型已进入下线倒计时，新项目应优先选用 `qwen3-rerank` 或 `qwen3.7-text-rerank`，避免未来兼容性风险。

## 关键参数

| 参数 | 适用模型 | 说明 |
|------|----------|------|
| `text_type` | 异步文本向量 (`text-embedding-async-*`) | 取值 `document`（默认，用于底库）或 `query`（用于检索Query），影响向量表示优化方向。 |
| `dimensions` | 同步文本向量 (`qwen3.7-text-embedding`, `text-embedding-v4/v3`)、多模态向量 (`qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06`) | 指定向量维度，不同模型支持范围不同（如 `qwen3.7-text-embedding` 支持 2560/2048/1536/1024/768/512/256）。`text-embedding-v2/v1` 和 `tongyi-embedding-vision-plus` 等不支持此参数。 |
| `enable_fusion` | `qwen3-vl-embedding` | `true` 时启用多模态融合向量（单输入生成1个融合向量）；`false`（默认）或省略时生成独立向量（每个输入各1个向量）。 |
| `instruct` | `qwen3.7-text-rerank`, `qwen3-rerank`, `qwen3-vl-rerank` | 自定义排序任务指令，如 `"Given a web search query, retrieve relevant passages that answer the query."`（问答检索）或 `"Retrieve semantically similar text."`（语义相似度），直接影响排序逻辑。 |
| `top_n` | 所有 rerank 模型 | 返回排序后前 N 个结果，默认返回全部。 |

## 使用方式

### 调用路径
- **HTTP 直接调用**：所有能力均提供标准 RESTful API，需配置 `Authorization`（Bearer [Token](../concepts/token.md)）和 `Content-Type: application/json`。地域 Base URL 需替换 `{WorkspaceId}` 并匹配实际 region（如 `cn-beijing`）。
- **OpenAI 兼容模式**：同步文本向量支持 OpenAI `/embeddings` 接口，Base URL 为 `https://{WorkspaceId}.<region>.maas.aliyuncs.com/compatible-mode/v1`，便于快速迁移现有代码。
- **DashScope SDK**：Python/Java SDK 提供更高层封装，如 `client.embeddings.jobs.create()`（异步批处理）、`client.rerank.create()`（排序），自动处理认证、重试与轮询，推荐生产环境使用。

### 典型流程示例
1. **向量构建**：使用 `text-embedding-async-v2` 对千万级商品描述文件（URL）进行异步批处理，指定 `text_type="document"`。
2. **Query 向量化**：使用 `qwen3.7-text-embedding` 同步接口，对用户实时输入的 Query 字符串生成向量，指定 `text_type="query"` 和 `dimensions=1536`。
3. **粗排+精排**：先基于向量余弦相似度召回 Top-K 候选，再用 `qwen3.7-text-rerank` 对候选集进行重排，传入 `instruct` 明确任务类型，并设置 `top_n=5` 获取最终结果。

## 限制和注意事项

- **限流策略**：
  - 异步批处理：单用户并发运行中任务数上限为 **3**，排队中+运行中总任务数上限为 **50**（见 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)）。
  - 同步向量：各模型有独立 RPS 与 [Token](../concepts/token.md) 限流，具体数值需参考控制台配额或 [限流文档](https://help.aliyun.com/zh/model-studio/rate-limit#953ddcd76495l)。
- **输入约束**：
  - 同步文本向量：`qwen3.7-text-embedding` 单次最多 20 行，每行最长 128,000 [Token](../concepts/token.md)；`text-embedding-v4` 最多 10 行，每行最长 8,192 Token；`text-embedding-v2` 最多 25 行，每行最长 2,048 Token。
  - 多模态向量：`qwen3-vl-embedding` 单次请求 `contents` 总数 ≤ 20，其中图片 ≤ 10，视频 ≤ 1；`tongyi-embedding-vision-plus-2026-03-06` 图片 ≤ 64，视频 ≤ 8。
  - 排序模型：`qwen3-vl-rerank` 单次最多 500 文档，但图片/视频文档会按等效 Token 折算，实际数量受 `request_max_tokens`（120,000）限制。
- **输出格式**：
  - `encoding_format` 在同步向量中仅对“短请求”生效（新网关），长请求仍强制返回 `float`；`base64` 编码暂未全量支持。
  - 排序结果中的 `relevance_score` 是本次请求内的**相对分数**，不可跨请求比较绝对值。
- **地域与模型可用性**：部分模型（如 `qwen3.7-text-embedding`）在新加坡地域无免费额度；`qwen2.5-vl-embedding` 仅支持 11 种语言，而 `qwen3-vl-embedding` 支持 33 种，选型时需核对 [模型概览](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md) 表格。

## 来源文档

- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


