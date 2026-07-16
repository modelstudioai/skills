# vector and sort

百炼平台围绕"向量化"与"排序"提供了一整套模型 API，覆盖通用文本向量、多模态向量与文本/多模态重排序三大能力。它们共同服务于语义搜索、推荐、聚类、分类与 RAG 检索：向量模型负责把文本、图片、视频编码为同一语义空间中的数值向量，排序（rerank）模型则在召回阶段之后对候选结果做二次精排，提升最终相关性。

## 能力与模型总览

按用途可分为三类接口，分别对应不同的 endpoint 与调用方式：

- **通用文本向量（同步）**：将字符串 / 字符串列表 / 文件转为向量，实时返回。支持 `qwen3.7-text-embedding`、`text-embedding-v4/v3/v2/v1`。详见 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **通用文本向量（批处理）**：面向大规模离线向量化，仅支持异步模式，通过文件 URL 输入。支持 `text-embedding-async-v2/v1`。详见 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **多模态向量**：将文本、图片、视频编码到同一语义空间，支持跨模态检索与融合表征。支持 `qwen3-vl-embedding`、`qwen2.5-vl-embedding`、`tongyi-embedding-vision-plus/flash`（含 `2026-03-06` 快照版）、`multimodal-embedding-v1`。详见 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。
- **文本 / 多模态排序**：对召回文档做精排，支持 `qwen3-rerank`、`qwen3-vl-rerank`（多模态）、`gte-rerank-v2`。详见 [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。

> **注意**：`gte-rerank` 模型将于 2026-05-30 下线，官方推荐迁移到 `qwen3-rerank`。新项目请直接选用 `qwen3-rerank` / `qwen3-vl-rerank`。

## 通用文本向量

### 同步接口

- **兼容方式**：提供 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，可用 OpenAI SDK 直连。
  - base_url：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
  - endpoint：`POST .../compatible-mode/v1/embeddings`
  - 调用前需将 `{WorkspaceId}` 替换为真实业务空间 ID。
- **关键参数**：
  - `model`（必选）：模型名称。
  - `input`（必选）：`string` / `array<string>` / `file` 三种形态。
  - `dimensions`（可选）：仅 `text-embedding-v3/v4`（及 `qwen3.7-text-embedding` 的 2560 维）支持自定义维度，取值 2560/2048/1536/1024/768/512/256/128/64，默认 1024。
  - `encoding_format`（可选）：当前仅支持 `float`。
- **输入上限（按模型区分）**：
  - `qwen3.7-text-embedding`：单条字符串最长 128,000 Token；列表/文件最多 20 条。
  - `text-embedding-v3/v4`：单条 8,192 Token；列表/文件最多 10 条。
  - `text-embedding-v1/v2`：单条 2,048 Token；列表/文件最多 25 条。

> **注意**：`dimensions` 只对部分模型生效——`text-embedding-v1/v2` 为固定维度（分别 1536 / 1536），传入该参数无意义；`v4` 才支持 2048/1536 等高维度。选维度前请对照模型概览表。

### 批处理接口

批处理专用于大批量离线场景，特点是**仅支持异步**：

- endpoint：`POST https://dashscope.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding`。
- HTTP 请求**必须**带请求头 `X-DashScope-Async: enable`，否则报错 `current user api does not support synchronous calls`。
- 输入通过 `input.url` 传入文件 HTTP URL（一行一条），单行最长 2,048 Token、最多 100,000 行、文件不超过 200MB。
- `parameters.text_type` 可选 `document`（默认）或 `query`；检索类非对称任务建议区分 query / document。
- 调用两步走：创建任务拿到 `task_id` → `GET .../api/v1/tasks/{task_id}` 轮询结果。任务状态含 PENDING / RUNNING / SUCCEEDED / FAILED / CANCELED / UNKNOWN。
- **数据时效**：任务结果 URL 仅保留 24 小时，务必及时下载，详见 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **限流**：`text-embedding-async-v2` 任务下发 RPS 为 1，排队+运行作业不超过 50 个，同时并发运行不超过 3 个。

## 多模态向量

多模态向量把 text / image / video 编码进**同一语义空间**，可直接用余弦相似度做跨模态匹配（以文搜图、以图搜视频等）。

- endpoint：`POST https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`。
- 输入通过 `input.contents` 数组传入，每个元素为 `{"模态类型": "值"}`，支持 `text` / `image` / `video` / `multi_images` 四种类型。图片可用 URL 或 Base64 Data URI，视频仅支持公开 URL。
- **独立向量 vs 融合向量**：
  - 独立向量：为每个输入分别生成一个向量，适合逐项对比（以图搜图）。
  - 融合向量：将所有输入融合为 1 个向量，适合整体语义表征（如商品图+描述文本）。
  - `qwen3-vl-embedding` 通过 `enable_fusion=true` 开启融合；`tongyi-embedding-vision-*-2026-03-06` 则通过把 text/image/video 放进同一个 content 对象来生成融合向量（不使用 `enable_fusion`）。
- **关键参数（在 `parameters` 内）**：`dimension`（不同模型取值不同）、`output_type`（仅 `dense`）、`fps`（视频帧率比例 [0,1]）、`instruct`（任务说明，建议英文）、`res_level`（分辨率档位 0/1/2/3，仅 2026-03-06 版）、`max_video_frames`（最大采样帧，≤64，仅 2026-03-06 版）。

> **注意**：各模型的向量类型能力差异明显——`qwen2.5-vl-embedding` **仅**支持融合向量、不支持独立向量与多图；`tongyi-embedding-vision-plus/flash`（非快照版）**仅**支持独立向量；`multimodal-embedding-v1` 与 `tongyi-embedding-vision-plus/flash` 不支持 `dimension` 参数（维度固定）。选型前务必核对 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md) 中的"模型能力对照"表。

## 文本 / 多模态排序（Rerank）

排序模型对召回文档二次精排，返回相关性分数。不同模型使用不同接口：

- `qwen3-rerank`：`POST .../compatible-api/v1/reranks`，且 `query` / `documents` / `top_n` / `instruct` 与 `model` **同层级**（不使用 `input` / `parameters` 包装）。
- `qwen3-vl-rerank`（多模态）/ `gte-rerank-v2`：`POST .../api/v1/services/rerank/text-rerank/text-rerank`，参数需包装进 `input` 与 `parameters` 对象。

关键参数与返回：

- `query`（必选）：最大 4,000 Token；`qwen3-vl-rerank` 支持 `{"text": ...}` 或 `{"image": ...}` 对象形式。
- `documents`（必选）：候选文档数组；`qwen3-vl-rerank` 每项可为 `text` / `image` / `video`。
- `top_n`（可选）：返回前 N 条，默认全部。
- `return_documents`（可选，默认 `false`）：是否回带原文，仅 `gte-rerank-v2` / `qwen3-vl-rerank` 支持。
- `instruct`（可选）：仅 `qwen3-rerank` / `qwen3-vl-rerank` 生效，用于切换问答检索 / 语义相似度等排序策略，建议英文。
- `fps`（可选）：仅 `qwen3-vl-rerank` 支持，控制视频抽帧比例。
- 返回 `results` 按 `relevance_score`（0.0–1.0）降序排列，`index` 对应输入原始位置。

> **注意**：`relevance_score` 是**单次请求内的相对分数**，仅用于本次请求内排序，不可作为跨请求比较的绝对阈值。此外两类接口响应结构不同——`qwen3-rerank` 的 `results` 位于响应顶层且无 `output` 对象，其余模型结果在 `output.results` 内，详见 [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。

## 通用限制与注意事项

- **前提条件**：所有接口都需先[获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并配置到环境变量 `DASHSCOPE_API_KEY`；SDK 调用还需安装 DashScope SDK。
- **地域**：同步向量与 rerank 走 `maas.aliyuncs.com`（需替换 `{WorkspaceId}`），多模态与批处理走 `dashscope.aliyuncs.com`；新加坡地域需将 base_url 换为 `dashscope-intl.aliyuncs.com`。
- **SDK 与 HTTP 差异**：HTTP 使用嵌套的 `input` / `parameters` 结构，DashScope SDK 多为扁平参数，开发时注意区分。
- **超长截断**：rerank 中单条超过"单条最大输入 Token"会被截断，API 仅基于截断后内容计算，可能影响排序准确性。
- **限流与错误码**：触发条件参见平台[限流](https://help.aliyun.com/zh/model-studio/rate-limit)文档，失败响应通过 `code` / `message` 指明原因，对照[错误码](https://help.aliyun.com/zh/model-studio/error-code)排查。

## 来源文档

- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)


