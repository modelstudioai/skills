# vector and sort

百炼平台提供文本向量（embedding）、多模态向量（multimodal embedding）和文本排序（rerank）三大核心能力，支撑语义搜索、RAG、跨模态检索等典型场景。所有能力均通过统一的 API 接口规范提供，支持同步/异步调用、OpenAI 兼容模式及 DashScope SDK 封装，适用于从轻量级实验到大规模批处理的全量需求。

## 支持的模型与功能

### 文本向量化
- **同步接口**：支持 `qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3` 等 6+ 模型，适用于实时低延迟场景，单次最多处理 20 条（`qwen3.7-text-embedding`）或 10 条（`text-embedding-v4`）文本 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **异步批处理**：`text-embedding-async-v2` 支持单次 100,000 行、每行 ≤2,048 [Token](../concepts/token.md) 的超大文件处理，适合离线建库任务 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。

### 多模态向量化
支持文本、图像、视频三模态统一编码，所有模型输出向量位于同一语义空间，可直接计算余弦相似度：
- `qwen3-vl-embedding`：支持独立向量（默认）与融合向量（需 `enable_fusion=true`），维度可选 2560–256；
- `tongyi-embedding-vision-plus-2026-03-06`：新版 Qwen3 底座模型，支持 `res_level` 和 `max_video_frames` 参数，同时兼容独立/融合模式；
- `multimodal-embedding-v1`：固定 1024 维，仅支持基础文本+图片+视频输入 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

### 文本排序（Rerank）
对召回结果进行二次精排，提升 Top-K 准确率：
- `qwen3-rerank`：推荐主力模型，[OpenAI 兼容接口](../concepts/openai-compatible-api.md)（`/compatible-api/v1/reranks`），最大文档数 500，单条 Query ≤4,000 [Token](../concepts/token.md)；
- `qwen3.7-text-rerank`：高容量模型（请求总 [Token](../concepts/token.md) ≤120,000），支持 `instruct` 自定义任务指令；
- `qwen3-vl-rerank`：支持文本/图片/视频混合查询与文档，适用于跨模态排序；
- > **注意**：`gte-rerank` 系列模型已进入下线倒计时，`gte-rerank-v2` 将于 2026 年 05 月 30 日正式下线，必须迁移至 `qwen3-rerank` 或 `qwen3.7-text-rerank`。

## 关键参数

| 参数 | 适用模型 | 说明 | 是否必选 |
|------|----------|------|----------|
| `model` | 全部 | 模型名称，如 `"qwen3-rerank"`、`"text-embedding-v4"` | 必选 |
| `input` / `query` + `documents` | 向量/排序 | 向量：`string`/`array<string>`/`file`；排序：`query`（string/object） + `documents`（array） | 必选 |
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding` 等 | 指定向量维度（如 `1024`, `2048`），不支持则忽略或报错 | 可选 |
| `encoding_format` | 同步向量 | `float`（默认）或 `base64`；但[老网关强制返回 float](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)，长请求亦降级为 float | 可选 |
| `instruct` | `qwen3.7-text-rerank`, `qwen3-rerank`, `qwen3-vl-rerank` | 英文任务指令，控制排序策略（如 `"Retrieve semantically similar text."`） | 可选 |
| `top_n` | 排序模型 | 返回前 N 个结果，默认返回全部 | 可选 |
| `return_documents` | `gte-rerank-v2`, `qwen3-vl-rerank` | 是否在响应中返回原文，默认 `false` | 可选 |

> **注意**：`qwen3-rerank` 的参数结构与其他排序模型不同——`query`、`documents`、`top_n`、`instruct` 均为顶层字段，**不嵌套在 `input` 或 `parameters` 中**；而 `qwen3.7-text-rerank` 必须使用 `input.query` + `input.documents` 结构。混用将导致 400 错误。

## 使用方式

### 调用路径选择
- **实时向量生成**（<1s 延迟）：使用同步 API，推荐 OpenAI 兼容模式（`/compatible-mode/v1/embeddings`）快速迁移；
- **批量建库**（万级文本）：使用异步批处理 API（`/api/v1/services/embeddings/text-embedding/text-embedding`），上传文件 URL 后轮询任务状态；
- **跨模态融合**（图文+视频）：使用 `qwen3-vl-embedding` + `enable_fusion=true`，或 `tongyi-embedding-vision-plus-2026-03-06` 将多模态内容置于同一 `content` 对象中；
- **RAG 精排**：优先选用 `qwen3-rerank`（OpenAI 兼容）或 `qwen3.7-text-rerank`（高 Token 容量），配合 `instruct` 显式声明任务类型。

### 地域与 Endpoint
- 北京地域 base URL：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/...`
- 新加坡地域 base URL：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/...`
- 多模态通用 endpoint（不区分地域）：`https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`

### SDK 快速示例（Python）
```python
# 同步向量（OpenAI 兼容）
from openai import OpenAI
client = OpenAI(base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1")
resp = client.embeddings.create(model="text-embedding-v4", input=["hello", "world"])

# 异步批处理（DashScope SDK）
from dashscope import BatchTextEmbedding
result = BatchTextEmbedding.call(
    model=BatchTextEmbedding.Models.text_embedding_async_v2,
    url="https://your-bucket.oss-cn-beijing.aliyuncs.com/data.txt"
)

# 文本排序（qwen3-rerank）
import dashscope
resp = dashscope.TextReRank.call(
    model="qwen3-rerank",
    query="如何更换手机电池",
    documents=["步骤1：关机", "电池型号：BL-5C"],
    top_n=1
)
```

## 限制和注意事项

- **Token 限制严格**：`text-embedding-v4` 单行上限 8,192 Token，超限直接返回 HTTP 400；`qwen3-vl-rerank` 视频帧数受 `fps` 参数控制，`fps=0.5` 表示抽取约一半关键帧。
- **免费额度时效性**：北京地域部分模型（如 `qwen3.7-text-embedding`）提供 100 万 Token 免费额度，**有效期仅为百炼开通后 90 天**，过期自动清零 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **异步任务生命周期**：批处理任务结果 URL 仅保留 **24 小时**，需及时下载；同时运行中任务数上限为 3 个，排队中任务总数上限为 50 个。
- **模型能力差异**：
  - `multimodal-embedding-v1` 不支持 `dimension` 参数，固定 1024 维；
  - `tongyi-embedding-vision-plus` 不支持融合向量，仅能生成独立向量；
  - `qwen2.5-vl-embedding` 仅支持融合向量，且不支持 `multi_images`。
- **地域价格差异**：新加坡地域 `qwen3.7-text-embedding` 单价为 0.000525 元/千 Token（北京为 0.0005 元），且无免费额度，生产环境部署前需核对成本。

## 来源文档

- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)
- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)


