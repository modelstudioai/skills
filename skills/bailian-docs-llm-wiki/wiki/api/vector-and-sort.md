# vector and sort

百炼平台的 `vector and sort` 功能涵盖文本/[多模态](../concepts/multi-modal.md)向量化（embedding）与语义重排序（rerank）两大核心能力，支撑[检索增强生成](../concepts/rag.md)（RAG）、跨模态搜索、聚类分类等典型AI应用。向量模型将原始内容映射至统一语义空间，排序模型则对召回结果进行精细化相关性打分与重排，二者常协同使用以构建高精度语义检索链路。

## 支持的模型/功能

### 文本向量化
- **同步接口**：支持 `qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3`、`text-embedding-v2`、`text-embedding-v1` 等通用文本模型，适用于低延迟、小批量场景（如实时查询向量化）。详情见 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **批处理接口**：支持 `text-embedding-async-v2`（推荐）和 `text-embedding-async-v1`，专为大规模离线向量化设计，单次最多处理 100,000 行文本，文件上限 200MB。详情见 [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。
- **[多模态](../concepts/multi-modal.md)向量化**：支持 `qwen3-vl-embedding`、`tongyi-embedding-vision-plus-2026-03-06` 等模型，可对文本、图像、视频及多图序列生成独立向量或融合向量，实现跨模态语义对齐。详情见 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

### 排序（Rerank）
- **文本排序**：`qwen3.7-text-rerank`（主力推荐）、`qwen3-rerank`（轻量替代）、`gte-rerank-v2`（即将下线，[官方公告](https://www.aliyun.com/notice/118217)明确2026年05月30日停用）。
- **[多模态](../concepts/multi-modal.md)排序**：`qwen3-vl-rerank` 支持文本、图片、视频混合查询与文档排序，适用于跨模态检索场景。

> **注意**：`gte-rerank-v2` 模型虽在文档中仍被列出，但其已进入下线倒计时，新项目应优先选用 `qwen3-rerank` 或 `qwen3.7-text-rerank`，避免未来兼容性风险。

## 关键参数

| 参数 | 适用模型 | 说明 | 是否必选 |
|------|----------|------|----------|
| `model` | 全部 | 模型名称，必须与[模型概览](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)中一致 | 是 |
| `input` / `query` & `documents` | 向量/排序 | 向量：字符串、字符串列表或文件URL；排序：`query`（字符串或对象）+ `documents`（字符串数组或对象数组） | 是 |
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding` 等 | 指定向量维度，不同模型支持值不同（如 `qwen3-vl-embedding` 支持 2560/2048/.../256，默认2560） | 否（默认值因模型而异） |
| `encoding_format` | 同步向量接口 | `float`（默认）或 `base64`；**注意**：老网关强制返回 `float`，长请求亦会降级至老网关 [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md) | 否 |
| `enable_fusion` | `qwen3-vl-embedding` | `true` 时生成融合向量（所有输入合并为1个向量），`false` 或未设置时生成独立向量 | 否（仅该模型） |
| `instruct` | `qwen3.7-text-rerank`, `qwen3-rerank`, `qwen3-vl-rerank` | 自定义排序任务指令，如 `"Retrieve semantically similar text."`，显著影响排序逻辑 | 否（默认按问答检索） |
| `top_n` | 排序模型 | 返回前 N 个结果，超出文档总数时返回全部 | 否 |

## 使用方式

### 调用路径选择
- **实时、小批量（≤20条）**：优先使用同步向量接口（OpenAI 兼容或 DashScope HTTP）。
- **离线、大批量（>20条或超大文件）**：必须使用批处理接口（异步模式，通过 `task_id` 轮询结果）。
- **跨模态任务**：使用 `multimodal-embedding` 接口（HTTP 或 SDK），注意 `contents` 数组结构与 `enable_fusion` 参数控制。

### 基础调用示例（Python + OpenAI 兼容）
```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"  # 替换 WorkspaceId
)

# 同步向量
resp = client.embeddings.create(
    model="qwen3.7-text-embedding",
    input=["苹果手机", "华为手机"],
    dimensions=1024
)

# 文本排序（OpenAI 兼容）
resp = client.reranks.create(
    model="qwen3-rerank",
    query="如何选购智能手机？",
    documents=["苹果手机性能强劲", "华为手机拍照效果好", "小米手机性价比高"],
    top_n=2
)
```

### 批处理关键步骤（HTTP）
1. **创建任务**：`POST /api/v1/services/embeddings/text-embedding/text-embedding`，Header 必须含 `X-DashScope-Async: enable`。
2. **轮询结果**：用返回的 `task_id` 调用 `GET /api/v1/tasks/{task_id}`，直至 `task_status` 为 `SUCCEEDED`。
3. **下载结果**：从响应 `output.url` 获取 JSONL 格式向量结果（每行一个 `[text, embedding]` 对）。

## 限制和注意事项

- **[Token](../concepts/token.md) 与长度限制**：
  - `qwen3.7-text-embedding` 单行最长 128,000 [Token](../concepts/token.md)；`text-embedding-v4` 仅支持 8,192 [Token](../concepts/token.md)；`text-embedding-v1/v2` 限 2,048 Token。超限将返回 HTTP 400 错误，**不会自动截断**。
  - `qwen3-vl-rerank` 的 `query` 和 `documents` Token 总和（计算公式：`Query Tokens × Document 数量 + Document Tokens 总和`）不得超过 120,000，否则报错。

- **地域与计费差异**：
  - 北京地域部分模型（如 `qwen3.7-text-embedding`）提供 100 万 Token 免费额度，有效期 90 天；新加坡地域同名模型**无免费额度**，且单价略高（如 `qwen3.7-text-embedding` 北京 0.0005元/千Token，新加坡 0.000525元/千Token）[同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。

- **SDK 与网关行为**：
  - `encoding_format=base64` 在长请求或老网关下会被忽略，始终返回 `float`，开发者需在代码中兼容此降级行为。
  - 批处理接口 `text-embedding-async-v2` 有严格并发限制：单用户**同时运行中任务 ≤3 个**，排队中+运行中任务总数 ≤50 个，超出将触发限流。

- **模型能力边界**：
  - `qwen2.5-vl-embedding` **仅支持融合向量**，不支持 `enable_fusion=false` 的独立向量模式；`tongyi-embedding-vision-plus` 系列旧版**仅支持独立向量**，不支持融合。混用参数将导致错误或静默忽略。

## 来源文档

- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)
- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)


