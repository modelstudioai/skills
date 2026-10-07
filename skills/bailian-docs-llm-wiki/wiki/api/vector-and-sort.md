# vector and sort

百炼平台提供文本向量（embedding）与排序（rerank）两类核心语义计算能力，分别用于将非结构化内容映射到统一语义空间，以及对召回结果进行精细化相关性重排序。二者常组合使用构建高质量检索、RAG 和推荐系统：先用向量模型生成底库文档向量并建立索引，再用排序模型对查询-文档对进行打分排序。

## 支持的模型/功能

### 文本向量模型
支持同步与异步两种调用模式：
- **同步接口**：适用于小批量（≤20 行）、低延迟场景，支持 `qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3` 等模型，[详见同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)。
- **批处理接口**：适用于超大批量（最高 100,000 行）、高吞吐场景，仅支持 `text-embedding-async-v2` 和 `text-embedding-async-v1`，采用异步任务模式，[详见批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)。

### 多模态向量模型
支持文本、图像、视频跨模态统一表征，所有模态向量位于同一语义空间，可直接计算余弦相似度。支持独立向量（每输入生成一向量）与融合向量（多模态输入融合为一向量）两种模式，主流模型包括 `qwen3-vl-embedding`、`tongyi-embedding-vision-plus-2026-03-06` 等，[详见 Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

### 排序（Rerank）模型
专用于对召回文档进行二次精排，提升 Top-K 结果准确率。支持纯文本（`qwen3-rerank`）、多模态（`qwen3-vl-rerank`）及兼容旧版（`gte-rerank-v2`）模型。注意：`gte-rerank` 系列模型将于 2026 年 5 月 30 日下线，应迁移至 `qwen3-rerank` 或 `qwen3.7-text-rerank`，[详见文本排序文档](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)。

> **注意**：`qwen3-rerank` 使用 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)（`/compatible-api/v1/reranks`），而 `qwen3.7-text-rerank`、`qwen3-vl-rerank` 和 `gte-rerank-v2` 使用标准百炼接口（`/api/v1/services/rerank/...`），二者请求体结构、参数层级和响应格式均不兼容，不可混用。

## 关键参数

| 参数 | 适用模型 | 说明 |
|------|----------|------|
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v3/v4`, `qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06` 等 | 指定向量维度，不同模型支持值不同（如 `qwen3-vl-embedding`: 2560/2048/...；`tongyi-embedding-vision-plus`: **不支持**，固定 1152 维）。 |
| `encoding_format` | 同步文本向量（`text-embedding-*`） | 控制返回格式为 `float` 或 `base64`，但受网关限制：老网关强制返回 `float`，新网关对长请求也降级为 `float`。 |
| `enable_fusion` | `qwen3-vl-embedding` | `true` 时启用融合向量模式；其他模型（如 `qwen2.5-vl-embedding`）仅支持融合，`tongyi-embedding-vision-plus-2026-03-06` 则通过将 text/image/video 放入同一 content 对象实现融合。 |
| `text_type` | 异步文本向量（`text-embedding-async-*`） | 区分 `query`（查询文本）与 `document`（底库文本），对检索类非对称任务效果更佳。 |
| `instruct` | `qwen3.7-text-rerank`, `qwen3-rerank`, `qwen3-vl-rerank` | 自定义排序任务指令（如 `"Retrieve semantically similar text."`），显著影响排序逻辑，建议英文书写。 |

## 使用方式

### 同步向量调用（推荐小批量）
使用 OpenAI 兼容 SDK 或 HTTP，指定 `model`、`input`（字符串/列表/文件）及可选 `dimensions`：
```python
from openai import OpenAI
client = OpenAI(base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1")
resp = client.embeddings.create(
    model="qwen3.7-text-embedding",
    input=["文本1", "文本2"],
    dimensions=1024
)
```

### 批处理向量调用（推荐大批量）
必须使用异步任务流：先 `POST /api/v1/services/embeddings/text-embedding/text-embedding` 创建任务（传入含文本 URL 的 `input`），再轮询 `GET /api/v1/tasks/{task_id}` 获取结果。

### 排序调用
- **纯文本排序**：`qwen3-rerank` 使用扁平参数（`query`, `documents`, `top_n` 直接同级）；其余模型需嵌套在 `input` 和 `parameters` 中。
- **多模态排序**：`qwen3-vl-rerank` 的 `query` 和 `documents` 均支持 `{"text": "..."}`
或 `{"image": "url"}` 格式，实现以图搜文等跨模态排序。

## 限制和注意事项

- **[Token](../concepts/token.md) 与行数限制**：同步文本向量中，`qwen3.7-text-embedding` 单行最多 128,000 [Token](../concepts/token.md)、最多 20 行；`text-embedding-v4` 降为单行 8,192 [Token](../concepts/token.md)、最多 10 行；异步模型 `text-embedding-async-v2` 支持单次 100,000 行但单行仅限 2,048 Token。超出将返回 HTTP 400 错误，**不会自动截断**。
- **地域与免费额度差异**：北京地域部分模型（如 `qwen3.7-text-embedding`）提供 100 万 Token 免费额度，而新加坡地域同名模型**无免费额度**，且单价略高（如 0.000525 元 vs 0.0005 元）。
- **模型弃用风险**：`gte-rerank` 系列模型已明确进入下线倒计时，新项目应避免选用；`text-embedding-v1/v2` 在文档中未标注下线，但已被 `v3/v4` 及 `qwen3.7-text-embedding` 明确替代，建议优先选用新版。
- **多模态输入约束**：`qwen3-vl-embedding` 单次请求内容元素总数 ≤ 20（图片+视频+文本条目之和），而 `tongyi-embedding-vision-plus-2026-03-06` 支持最多 64 张图片，需按实际需求选型。

## 来源文档

- [同步接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)
- [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)
- [批处理接口API详情](../../raw/model-api-reference/vector-and-sort/general-text-vector/text-embedding-batch-api.md)
- [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)
- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)
- [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)
- [文本排序](../../raw/model-api-reference/vector-and-sort/rerank-model/text-rerank-api.md)


