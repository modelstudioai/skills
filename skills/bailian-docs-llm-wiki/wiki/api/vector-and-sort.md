# vector and sort

百炼平台提供文本向量（embedding）、多模态向量（multimodal embedding）和文本排序（rerank）三大核心能力，覆盖语义检索、RAG、跨模态搜索、聚类等典型AI应用。所有能力均通过标准化API提供，支持同步/[异步调用](../concepts/asynchronous-invocation.md)、OpenAI兼容模式及SDK封装，适用于从单条实时推理到百万级批量处理的全场景需求。详细模型能力与参数请参考[通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)等原始文档。

## 支持的模型/功能

### 文本向量化
- **同步接口**：支持 `qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3`、`text-embedding-v2`、`text-embedding-v1` 等模型，适用于低延迟、小批量场景（如实时搜索Query编码）。详见 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **异步批处理**：支持 `text-embedding-async-v2`（推荐）和 `text-embedding-async-v1`，适用于超大批量（最高10万行/请求）、长耗时任务，输入为公开可访问的文本文件URL。详见 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。

### 多模态向量化
- 支持文本、图像、视频三模态统一向量空间建模，提供**独立向量**（每模态各1个向量）与**融合向量**（多模态输入融合为1个向量）两种模式。
- 主流模型包括 `qwen3-vl-embedding`（支持 fusion）、`tongyi-embedding-vision-plus-2026-03-06`（Qwen3底座，支持多分辨率与融合）、`multimodal-embedding-v1`（基础版）等。具体能力对照见 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

### 排序（Rerank）
- 提供纯文本与多模态排序能力：
  - 文本排序：`qwen3-rerank`（OpenAI兼容新接口）、`qwen3.7-text-rerank`（旧接口）、`gte-rerank-v2`（即将下线，[官方公告](https://www.aliyun.com/notice/118217)明确建议迁移）；
  - 多模态排序：`qwen3-vl-rerank`，支持 text/image/video 混合查询与文档排序。
- > **注意**：`gte-rerank` 系列模型（含 `gte-rerank-v2`）将于2026年05月30日下线，新项目应优先选用 `qwen3-rerank` 或 `qwen3.7-text-rerank`。

## 关键参数

| 参数 | 适用模型 | 说明 | 是否必选 |
|------|----------|------|----------|
| `model` | 全部 | 模型名称，如 `"qwen3-rerank"`、`"tongyi-embedding-vision-plus-2026-03-06"` | 必选 |
| `input` / `query` + `documents` | 向量：`input`；Rerank：`query`+`documents` | 向量：字符串/字符串列表/文件；Rerank：`query`为字符串或模态对象，`documents`为字符串或模态对象数组 | 必选 |
| `dimensions` / `dimension` | `qwen3.7-text-embedding`, `text-embedding-v{3,4}`, `qwen3-vl-embedding`, `tongyi-embedding-vision-*` | 指定向量维度（如 `1024`, `2048`），不同模型支持值不同 | 可选（默认值见各模型概览） |
| `enable_fusion` | `qwen3-vl-embedding` | `true` 时启用多模态融合向量（返回1个向量） | 仅融合场景需设为 `true` |
| `top_n` | Rerank 模型 | 返回前 N 个最相关结果 | 可选（默认返回全部） |
| `instruct` | `qwen3.7-text-rerank`, `qwen3-rerank`, `qwen3-vl-rerank` | 自定义排序任务指令（如 `"Retrieve semantically similar text."`），影响排序策略 | 可选（默认为问答检索） |

> **注意**：`qwen3-rerank` 的请求体结构与其他 rerank 模型不同——它**不使用嵌套 `input` 对象**，`query` 和 `documents` 与 `model` 同级；而 `qwen3.7-text-rerank`、`qwen3-vl-rerank`、`gte-rerank-v2` 必须将 `query` 和 `documents` 包裹在 `input` 对象内。此差异在 [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md) 文档中有明确示例对比。

## 使用方式

### 调用路径
- **同步向量/排序**：使用 OpenAI 兼容 endpoint（如 `.../compatible-mode/v1/embeddings`）或 DashScope 原生 endpoint（如 `.../api/v1/services/rerank/...`），适合 <1s 延迟要求场景。
- **异步批处理**：仅支持 HTTP 两步调用（创建任务 → 轮询结果），适用于大文件（≤200MB）、高吞吐场景，详见 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **SDK 封装**：Python/Java SDK 提供 `dashscope.TextEmbedding`、`dashscope.BatchTextEmbedding`、`dashscope.TextReRank` 等高层接口，自动处理认证、重试与格式转换。

### 典型代码片段（Python）
```python
# 同步文本向量（OpenAI兼容）
from openai import OpenAI
client = OpenAI(base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1")
resp = client.embeddings.create(model="qwen3.7-text-embedding", input="hello world")

# 异步多模态向量（原生HTTP）
import requests
resp = requests.post(
    "https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding",
    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    json={"model": "qwen3-vl-embedding", "input": {"contents": [{"text": "a cat"}, {"image": "url"}]}, "parameters": {"enable_fusion": True}}
)

# 文本排序（qwen3-rerank，OpenAI兼容风格）
resp = client.reranks.create(model="qwen3-rerank", query="what is LLM?", documents=["LLM is large language model", "RAG is retrieval augmented generation"])
```

## 限制和注意事项

- **Token 与长度限制**：
  - `qwen3.7-text-embedding` 单行最长 128,000 Token；`text-embedding-v4` 仅支持 8,192 Token；`qwen3-vl-rerank` 图片文档上限 40 张，视频上限 4 个。
  - 所有模型对输入总 Token 数均有硬性上限（如 `qwen3.7-text-rerank` 请求最大 120,000 Token），超限直接返回 HTTP 400，**不会自动截断**。
- **地域与免费额度**：
  - 北京地域部分模型（如 `qwen3.7-text-embedding`）提供 100 万 Token 免费额度（开通后90天有效），新加坡地域同名模型**无免费额度**（见 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md) 表格）。
- **网关兼容性**：
  - `encoding_format="base64"` 仅在新网关的短请求中生效；长请求会路由至老网关，强制返回 `float` 格式（见 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md) 中“encoding_format”说明）。
- **异步任务管理**：
  - 批处理任务 ID 有效期仅 **24 小时**，结果 URL 过期后无法访问，需及时下载。
  - 单用户并发运行中异步作业数上限为 **3 个**，排队中任务总数上限为 **50 个**（见 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)）。

## 来源文档

- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)
- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


