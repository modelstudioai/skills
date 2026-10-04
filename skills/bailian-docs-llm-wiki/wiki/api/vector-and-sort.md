# vector and sort

百炼平台提供两类核心向量与排序能力：**文本/多模态向量生成（Embedding）** 和 **语义相关性重排序（Rerank）**。前者将原始内容（文本、图像、视频）映射到统一语义空间的稠密向量，支撑检索、聚类等任务；后者对召回结果进行细粒度相关性打分与重排，显著提升RAG、搜索等场景的最终效果。两类能力均支持同步与异步调用模式，并覆盖多语言、多地域部署。

## 支持的模型/功能

### 文本向量模型
- **同步接口**：`qwen3.7-text-embedding`（最高2560维，128K [Token](../concepts/token.md)）、`text-embedding-v4`（Qwen3-Embedding系列，支持64–2048维）、`text-embedding-v3`、`text-embedding-v2`、`text-embedding-v1`  
- **异步批处理接口**：`text-embedding-async-v2`（单次10万行，2048 [Token](../concepts/token.md)/行）、`text-embedding-async-v1`  
- 详细参数与地域差异见 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。

### 多模态向量模型
- 支持文本、图像、视频三模态独立向量或融合向量生成：`qwen3-vl-embedding`（支持`enable_fusion=true`）、`qwen2.5-vl-embedding`（仅融合）、`tongyi-embedding-vision-plus-2026-03-06`（新版Qwen3底座，支持多分辨率与融合）、`tongyi-embedding-vision-flash-2026-03-06`、`tongyi-embedding-vision-plus`、`tongyi-embedding-vision-flash`、`multimodal-embedding-v1`  
- 融合向量需注意模型能力限制：`qwen2.5-vl-embedding` 仅支持融合，不支持独立向量；`tongyi-embedding-vision-plus` 仅支持独立向量 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

### 排序（Rerank）模型
- **文本排序**：`qwen3-rerank`（推荐替代已下线的`gte-rerank`）、`qwen3.7-text-rerank`（兼容旧版）、`gte-rerank-v2`（2026年05月30日下线）  
- **多模态排序**：`qwen3-vl-rerank`（支持text/image/video混合查询与文档）  
- 模型选型与迁移建议详见 [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。

## 关键参数

| 参数 | 适用模型 | 说明 | 是否必选 |
|--------|-----------|------|----------|
| `model` | 全部 | 模型名称，必须与[模型概览](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)中一致 | 是 |
| `input` / `query` & `documents` | Embedding: `string`/`array`/`file`；Rerank: `query`+`documents`结构 | Embedding输入支持字符串、字符串列表、文件URL；Rerank输入为查询+候选文档列表 | 是 |
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding`, `tongyi-embedding-vision-*2026-03-06*` | 指定向量维度，不同模型支持值不同（如`qwen3-vl-embedding`: 256–2560）；`tongyi-embedding-vision-plus`等旧版不支持该参数 | 否（默认值见文档） |
| `encoding_format` | Embedding同步接口 | `float`（默认）或 `base64`；但[同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)明确指出：老网关始终返回`float`，长请求亦强制降级为`float` | 否 |
| `instruct` | `qwen3.7-text-rerank`, `qwen3-rerank`, `qwen3-vl-rerank` | 自定义排序任务指令（如问答检索、语义相似度），影响打分逻辑；英文指令效果更稳定 | 否（默认按问答检索） |
| `enable_fusion` | `qwen3-vl-embedding` | `true`时启用多模态融合向量（单输入→单向量）；其他模型通过结构隐式控制（如2026-03-06版本将text/image/video放在同一content对象中） | 否（仅该模型） |

> **注意**：`text-embedding-async-v2` 的 `text_type` 参数（`document`/`query`）仅影响下游检索效果，不改变向量本身；而 `qwen3-vl-rerank` 的 `fps` 参数仅作用于视频帧采样，对文本/图片无影响。

## 使用方式

### 同步调用（Embedding/Rerank）
- **Embedding**：使用 OpenAI 兼容 SDK 或 HTTP POST 到 `/compatible-mode/v1/embeddings`（北京/新加坡地域需替换 `{WorkspaceId}` 和 base URL）。支持单文本、文本列表、文件输入。
- **Rerank**：`qwen3-rerank` 使用 `/compatible-api/v1/reranks`（扁平参数结构）；其余模型使用 `/api/v1/services/rerank/...`（嵌套 `input` 结构）。示例见 [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。

### 异步调用（Embedding）
- **HTTP**：两步操作——先 `POST /api/v1/services/embeddings/...` 创建任务（带 `X-DashScope-Async: enable`），再 `GET /api/v1/tasks/{task_id}` 查询结果（24小时有效期）。
- **SDK**：`BatchTextEmbedding.call()`（同步封装）或 `BatchTextEmbedding.async_call()` + `fetch()`/`wait()`（异步轮询）。

### 多模态输入格式
- **独立向量**：`contents` 数组中每个元素为 `{"text": "..."}`, `{"image": "url"}`, `{"video": "url"}` 或 `{"multi_images": [...]}`。
- **融合向量**：`qwen3-vl-embedding` 需设 `"enable_fusion": true`；`tongyi-embedding-vision-*2026-03-06*` 需将多模态字段置于同一字典内（如 `{"text": "...", "image": "...", "video": "..."}`）。

## 限制和注意事项

- **[Token](../concepts/token.md)与长度限制**：`qwen3.7-text-embedding` 单行支持 128,000 Token，而 `text-embedding-v4` 仅 8,192；`qwen3-vl-rerank` 图片文档上限为 40 张，视频为 4 条 [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。
- **地域与免费额度差异**：北京地域部分模型（如 `qwen3.7-text-embedding`）提供 100 万 Token 免费额度，新加坡地域无免费额度；`text-embedding-async-v2` 在北京有 2000 万 Token 免费额度，新加坡未提及 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **网关兼容性问题**：`encoding_format=base64` 在长请求或老网关下会被忽略，始终返回 `float`；开发者应以实际响应格式为准，不可依赖参数声明。
- **模型下线提醒**：`gte-rerank` 系列模型将于 2026 年 05 月 30 日下线，必须迁移到 `qwen3-rerank` [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。
- **异步任务约束**：`text-embedding-async-v2` 限流为“同时运行中任务 ≤3 个，排队中+运行中总数 ≤50 个”，超限请求将被拒绝而非排队。

## 来源文档

- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)


