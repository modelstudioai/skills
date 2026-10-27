# vector and sort

百炼平台提供文本向量（embedding）、多模态向量（multimodal embedding）和文本排序（rerank）三大核心能力，覆盖语义检索、RAG、跨模态搜索等典型AI应用链路。所有能力均支持同步与异步调用方式，并通过统一的 API 设计与 SDK 封装降低集成门槛。开发者可根据数据规模、模态类型、延迟敏感度及成本要求选择合适模型与接口。

## 支持的模型/功能

### 文本向量化
- **同步接口**：适用于单次 ≤20 条（`qwen3.7-text-embedding`）、≤10 条（`text-embedding-v4`）或 ≤25 条（`text-embedding-v2`）的低延迟场景，支持 `qwen3.7-text-embedding`、`text-embedding-v4/v3/v2/v1` 等系列模型 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **批处理接口**：适用于大规模离线任务（单次最多 100,000 行），仅支持异步模式，模型为 `text-embedding-async-v2/v1` [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。

### 多模态向量化
支持文本、图像、视频及其组合的统一语义空间表征，分为：
- **独立向量**：每个输入（text/image/video/multi_images）生成独立向量，适用于以图搜图、以文搜图等逐项比对场景；
- **融合向量**：将多种模态输入融合为单一向量，适用于商品图文联合表征等整体理解场景。`qwen3-vl-embedding` 通过 `enable_fusion=true` 开启；`tongyi-embedding-vision-plus-2026-03-06` 等新版模型则通过将 text/image/video 放入同一 content 对象实现 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

### 排序（Rerank）
对召回结果进行二次精排，提升 Top-K 相关性。支持：
- **纯文本排序**：`qwen3.7-text-rerank`（推荐替代已下线的 `gte-rerank`）、`qwen3-rerank`；
- **多模态排序**：`qwen3-vl-rerank`，支持 text/image/video 混合查询与文档；
- **通用排序**：`gte-rerank-v2`（即将下线，不建议新接入）。

> **注意**：`gte-rerank` 系列模型（含 `gte-rerank-v2`）已明确标注将于 2026 年 05 月 30 日下线，[排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md) 文档强烈推荐迁移至 `qwen3-rerank` 或 `qwen3.7-text-rerank`。

## 关键参数

| 参数 | 适用模型 | 说明 |
|------|----------|------|
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding`, `qwen2.5-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06`, `tongyi-embedding-vision-flash-2026-03-06` | 指定向量维度。不同模型支持值不同（如 `qwen3-vl-embedding` 支持 2560/2048/.../256），未指定时取默认值。`tongyi-embedding-vision-plus` 等旧版模型不支持该参数。 |
| `encoding_format` | 同步文本向量接口 | 控制返回格式为 `float` 或 `base64`，但受网关限制：老网关强制返回 `float`，新网关仅短请求生效 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。 |
| `enable_fusion` | `qwen3-vl-embedding` | 布尔值，启用后将 `contents` 中所有输入融合为 1 个向量；其他模型（如 `qwen2.5-vl-embedding`）仅支持融合，`tongyi-embedding-vision-plus-2026-03-06` 则通过结构化 content 实现融合，无需此参数。 |
| `instruct` | `qwen3.7-text-rerank`, `qwen3-rerank`, `qwen3-vl-rerank` | 自定义排序任务指令（如 `"Retrieve semantically similar text."`），影响相关性打分逻辑，建议使用英文。 |
| `text_type` | 批处理文本向量接口 | 区分 `query`（查询文本）与 `document`（底库文本），对非对称检索任务可提升效果。 |

## 使用方式

### 接口调用路径
- **文本向量同步**：`POST /compatible-mode/v1/embeddings`（OpenAI 兼容）或 `POST /api/v1/services/embeddings/text-embedding/text-embedding`（DashScope 原生）；
- **文本向量批处理**：`POST /api/v1/services/embeddings/text-embedding/text-embedding` + `X-DashScope-Async: enable` 头，再 `GET /api/v1/tasks/{task_id}` 查询；
- **多模态向量**：`POST /api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`；
- **排序模型**：`POST /api/v1/services/rerank/text-rerank/text-rerank`。

### SDK 调用要点
- 所有 SDK 调用需提前配置 `DASHSCOPE_API_KEY` 环境变量及业务空间 ID（`workspace`）与地域（`region`）；
- DashScope SDK 对批处理和排序接口封装了 `jobs.create()` / `rerank.create()` 等高层方法，自动处理异步轮询（如 `client.embeddings.jobs.wait()`）；
- OpenAI 兼容 SDK 需显式设置 `base_url`（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），并确保 `{WorkspaceId}` 替换为真实值。

## 限制和注意事项

- **Token 与行数限制**：  
  - 同步文本向量：`qwen3.7-text-embedding` 单行上限 128,000 Token，最多 20 行；`text-embedding-v4` 单行上限 8,192 Token，最多 10 行；`text-embedding-v2` 单行上限 2,048 Token，最多 25 行。  
  - 批处理文本向量：单次请求最多 100,000 行，单行上限 2,048 Token，文件大小 ≤200MB。  
  - 多模态向量：`qwen3-vl-embedding` 文本上限 32,000 Token，图片单张 ≤10 MB；`tongyi-embedding-vision-plus-2026-03-06` 图片最多 64 张，视频 ≤50 MB。  
  - 排序模型：`qwen3.7-text-rerank` 单次请求最大输入 Token 为 120,000（建议值），`qwen3-vl-rerank` 文本 Query 上限 8,000 Token，图片/视频文档分别限 40/4 条。

- **地域与免费额度差异**：  
  > **注意**：北京与新加坡地域的模型免费额度不一致。例如 `qwen3.7-text-embedding` 在北京享 100 万 Token 免费额度（90 天），在新加坡则无免费额度；`text-embedding-v3` 在北京无免费额度，在新加坡提供 50 万 Token 免费额度 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。

- **异步任务生命周期**：  
  批处理任务结果 URL 有效期仅 **24 小时**，需及时下载保存；任务 ID 查询有效期同样为 24 小时。

- **模型兼容性警告**：  
  `multimodal-embedding-v1` 不支持 `dimension` 参数，固定输出 1024 维；`tongyi-embedding-vision-plus` 和 `tongyi-embedding-vision-flash` 也不支持该参数，而其 2026-03-06 快照版本已全面支持 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

## 来源文档

- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)
- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


