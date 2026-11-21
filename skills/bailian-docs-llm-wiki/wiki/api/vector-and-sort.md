# vector and sort

百炼平台提供两类核心向量与排序能力：**文本/多模态向量生成（Embedding）** 用于将原始内容映射到语义向量空间，支撑检索、聚类等任务；**重排序（Rerank）** 用于对召回结果进行精细化相关性打分与排序，显著提升最终结果质量。两类能力均支持同步与[异步调用](../concepts/asynchronous-invocation.md)模式，并覆盖文本、图像、视频等多模态输入。

## 支持的模型/功能

### 文本向量模型
- **同步接口**：`qwen3.7-text-embedding`（2560/2048/1536/1024/768/512/256维）、`text-embedding-v4`（2048/1536/1024/768/512/256/128/64维）、`qwen3.7-text-embedding-flash`（1024/768/512/256维）等，详见[同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **批处理接口**：`text-embedding-async-v2`（1536维，单次10万行）、`text-embedding-async-v1`，适用于超大批量文本向量化任务，详见[批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。

### 多模态向量模型
- `qwen3-vl-embedding`（2560/2048/1536/1024/768/512/256维）：支持**独立向量**（每个输入生成一个向量）和**融合向量**（通过 `enable_fusion=true` 将多模态输入融合为1个向量）。
- `tongyi-embedding-vision-plus-2026-03-06`（1152/1024/512/256/128/64维）：支持独立/融合双模式，且融合时可将 `text`、`image`、`video` 放在同一 content 对象中，无需 `enable_fusion` 参数。
- `qwen2.5-vl-embedding`（2048/1024/768/512维）：**仅支持融合向量**，不支持独立向量，详见[Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

### 排序（Rerank）模型
- `qwen3.7-text-rerank` 和 `qwen3-rerank`：纯文本重排序，支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)；`qwen3.7-text-rerank` 已明确替代即将下线的 `gte-rerank` 系列。
- `qwen3-vl-rerank`：支持跨模态重排序（文本/图片/视频混合查询与文档），支持 `fps` 参数控制视频抽帧密度。
- > **注意**：文档 4 中仅列出“[排序模型（Rerank）](raw/model-api-reference/vector-and-sort/rerank-model.md)”作为入口页，实际完整能力与参数说明均在文档 5 [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md) 中，开发者应以文档 5 为准。

## 关键参数

| 参数 | 适用模型 | 说明 |
|------|----------|------|
| `dimensions` / `dimension` | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding`, `tongyi-embedding-vision-plus*` 等 | 指定向量维度。不同模型支持值不同，如 `qwen3-vl-embedding` 支持 2560/2048/.../256，默认 2560；`multimodal-embedding-v1` 不支持该参数，固定 1024 维。 |
| `encoding_format` | 同步文本向量（`qwen3.7-text-embedding` 等） | 控制返回格式为 `float` 或 `base64`，但受网关限制：老网关强制返回 `float`，新网关短请求才按需返回。 |
| `enable_fusion` | `qwen3-vl-embedding` | `bool` 类型，设为 `true` 时启用融合向量模式；其他模型（如 `tongyi-embedding-vision-plus-2026-03-06`）通过结构化 input 实现融合，不使用此参数。 |
| `text_type` | 批处理 `text-embedding-async-*` | 取值 `document`（默认）或 `query`，用于非对称检索任务优化。 |
| `instruct` | `qwen3.7-text-rerank`, `qwen3-rerank`, `qwen3-vl-rerank` | 自定义排序指令，如 `"Given a web search query, retrieve relevant passages..."`，影响模型对 Query-Document 相关性的判断逻辑。 |
| `fps` | `qwen3-vl-rerank` | 视频抽帧频率（单位：帧/秒），范围 (0, 5]，默认 1.0。 |

## 使用方式

- **同步调用（低延迟、小批量）**：适用于实时场景（如用户搜索即时向量化）。使用 `/compatible-mode/v1/embeddings`（OpenAI 兼容）或 `/api/v1/services/rerank/...`（DashScope 原生）端点。支持 Python/Java SDK、curl、dashscope CLI。示例见[同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **异步批处理（高吞吐、大批量）**：适用于离线构建向量库。需两步：1) 调用 `/api/v1/services/embeddings/text-embedding/text-embedding` 提交任务并获取 `task_id`；2) 用 `GET /api/v1/tasks/{task_id}` 轮询结果。文件需托管于公网可访问 URL，单文件 ≤200MB，单次最多 10 万行。详见[批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **多模态融合**：对 `qwen3-vl-embedding`，在 request body 的 `parameters` 中设置 `"enable_fusion": true`；对 `tongyi-embedding-vision-plus-2026-03-06`，直接将 `text`、`image`、`video` 放入同一个 `content` 对象（如 `{"text": "...", "image": "...", "video": "..."}`）即可触发融合编码。

## 限制和注意事项

- **Token 与尺寸限制**：
  - `qwen3.7-text-embedding` 单行最长 128,000 Token；`text-embedding-v4` 仅支持 8,192 Token；`multimodal-embedding-v1` 文本限 512 Token。
  - `qwen3-vl-embedding` 图片单张 ≤10 MB，视频 ≤50 MB；`tongyi-embedding-vision-plus` 图片单张 ≤3 MB，视频 ≤10 MB。
- **并发与配额**：
  - 异步批处理：单用户同时运行中任务数上限为 3 个，排队中+运行中总数 ≤50 个；`text-embedding-async-v2` 免费额度为 2000 万 Token（90 天）。
  - 同步接口：各模型有独立 RPS 限流，具体见[限流文档](https://help.aliyun.com/zh/model-studio/rate-limit#953ddcd76495l)。
- > **注意**：文档 1 中 `text-embedding-v2` 标注单价为 0.0007 元/千 Token，而文档 2 中 `text-embedding-async-v2` 单价为 0.0007 元/千 Token —— 二者虽名称相似，但属于**不同接口类型（同步 vs 异步）和不同模型系列**，不可混用参数或计费规则。开发者须严格按接口文档选择对应模型。
- **模型生命周期**：`gte-rerank` 系列模型将于 2026 年 5 月 30 日下线，必须迁移至 `qwen3-rerank` 或 `qwen3.7-text-rerank`，详见[文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。

## 来源文档

- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)
- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)


