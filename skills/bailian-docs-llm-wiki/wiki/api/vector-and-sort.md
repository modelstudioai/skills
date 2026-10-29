# vector and sort

百炼平台提供文本向量（Embedding）、多模态向量（Multimodal Embedding）和文本排序（Rerank）三大核心能力，覆盖语义检索、RAG、跨模态搜索等典型场景。所有服务均支持同步与异步调用方式，适配 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)及 DashScope 原生 SDK，开发者可按数据规模、延迟敏感度与模态需求灵活选型。

## 支持的模型/功能

- **通用文本向量**：支持 `qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3` 等系列模型，适用于语义搜索、聚类、分类等任务；[同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md) 和 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md) 分别面向实时低延迟与海量离线场景。
- **多模态向量**：支持 `qwen3-vl-embedding`、`tongyi-embedding-vision-plus-2026-03-06` 等模型，统一文本、图像、视频的语义空间，支持独立向量（逐项编码）与融合向量（多模态联合编码）两种模式；详见 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。
- **文本排序（Rerank）**：提供 `qwen3.7-text-rerank`、`qwen3-rerank`、`qwen3-vl-rerank` 等模型，对召回结果进行精细化重排序，显著提升 RAG 与搜索相关性；[排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md) 文档涵盖多模态查询、自定义指令（`instruct`）等高级能力。

> **注意**：`gte-rerank` 系列模型（含 `gte-rerank-v2`）已进入下线过渡期，官方明确提示“`gte-rerank` 模型将于2026年05月30日下线，推荐使用 `qwen3-rerank` 替代”，该信息在 [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md) 中有权威声明，应作为迁移依据。

## 关键参数

| 参数 | 适用模型 | 说明 |
|------|----------|------|
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-03` 等 | 指定向量维度，不同模型支持值不同（如 `qwen3-vl-embedding` 支持 256–2560），默认值需查模型概览表；`text-embedding-v2`、`multimodal-embedding-v1` 等不支持此参数。 |
| `encoding_format` | 同步文本向量（OpenAI 兼容） | 取值 `float` 或 `base64`，但受网关限制：老网关强制返回 `float`，新网关仅短请求生效；详见 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。 |
| `enable_fusion` | `qwen3-vl-embedding` | `bool` 类型，设为 `true` 时将 `contents` 中所有输入融合为单个向量；`qwen2.5-vl-embedding` 不支持该参数（始终融合），而 `tongyi-embedding-vision-plus-2026-03-06` 通过同 content 对象内多模态字段实现融合，无需此参数。 |
| `instruct` | `qwen3.7-text-rerank`, `qwen3-rerank`, `qwen3-vl-rerank` | 自定义排序任务指令（如 `"Retrieve semantically similar text."`），影响模型对 Query-Document 相关性的判断逻辑；`gte-rerank-v2` 不支持。 |
| `text_type` | 异步文本向量（`text-embedding-async-v1/v2`） | 取值 `document`（默认）或 `query`，用于非对称检索任务优化；聚类等对称任务无需设置。 |

## 使用方式

- **同步调用（低延迟）**：适用于单次 ≤20 条文本（`qwen3.7-text-embedding`）或 ≤10 条（`text-embedding-v4`）的实时向量化。使用 OpenAI 兼容 SDK 或 HTTP POST 到 `compatible-mode/v1/embeddings`，需配置 `base_url` 并替换 `{WorkspaceId}`。示例：
  ```python
  client.embeddings.create(model="qwen3.7-text-embedding", input=["文本1", "文本2"], dimensions=1024)
  ```
- **异步批处理（高吞吐）**：适用于百万级文本批量向量化。通过 `text-embedding-async-v2` 模型提交文件 URL，单次最多 100,000 行、每行 ≤2,048 [Token](../concepts/token.md)；调用流程为“创建任务 → 轮询 `GET /api/v1/tasks/{task_id}` 获取结果”。详见 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **Rerank 调用**：必须传入 `query` 和 `documents` 数组，`documents` 支持纯文本或 `{"text": "...", "image": "...", "video": "..."}` 结构化输入（`qwen3-vl-rerank`）。SDK 调用更简洁（扁平参数），HTTP 需嵌套于 `input` 对象中。
- **多模态向量**：`contents` 字段接受混合数组（如 `[{"text":"..."}, {"image":"..."}, {"video":"..."}]`），融合模式需按模型要求设置 `enable_fusion=true` 或将多模态字段置于同一字典内。

## 限制和注意事项

- **[Token](../concepts/token.md) 与尺寸限制**：  
  - 同步文本向量：`qwen3.7-text-embedding` 单行最长 128,000 [Token](../concepts/token.md)，`text-embedding-v4` 仅 8,192 Token；  
  - 多模态向量：`qwen3-vl-embedding` 图片单张 ≤10 MB，视频 ≤50 MB；`tongyi-embedding-vision-plus` 图片单张 ≤3 MB；  
  - Rerank：`qwen3.7-text-rerank` 单次请求最大输入 Token 为 120,000（计算公式：`Query Tokens × Document 数量 + Document Tokens 总和`）。
- **地域与免费额度差异**：北京地域部分模型（如 `qwen3.7-text-embedding`）提供 100 万 Token 免费额度，而新加坡地域同名模型无免费额度；异步模型 `text-embedding-async-v2` 提供 2000 万 Token 免费额度（有效期 90 天）。
- **限流策略**：异步向量任务存在双重限流——单用户并发运行中任务数 ≤3，排队+运行中总数 ≤50；同步接口遵循通用 [限流](https://help.aliyun.com/zh/model-studio/rate-limit#953ddcd76495l) 规则。
- **向量空间一致性**：多模态模型（如 `qwen3-vl-embedding`）确保文本、图像、视频向量位于同一语义空间，可直接用余弦相似度跨模态比对；但 `tongyi-embedding-vision-plus` 与 `tongyi-embedding-vision-flash` 的向量空间彼此独立，不可混用。

## 来源文档

- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)
- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)


