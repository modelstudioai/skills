# vector and sort

`vector and sort` 是百炼平台提供的向量嵌入与排序（Rerank）能力集合，用于将文本、图像等输入转换为高维向量表示，或对候选结果列表按相关性重排序。该能力由多个专用模型支撑，支持同步调用与异步批处理，适用于[检索增强生成](../concepts/rag.md)（RAG）、语义搜索、推荐系统等场景。所有接口均通过统一 `/v1/embeddings` 和 `/v1/rerank` 路径接入。

## 支持的模型/功能

- **通用文本向量**：支持中英文混合文本的稠密向量生成，适用于通用语义检索；模型版本 `text-embedding-v3` 为当前默认且推荐版本，详见 [向量与排序](../../raw/model-api-reference/vector-and-sort.md)。  
- **多模态向量**：支持图像+文本联合嵌入（如图文匹配），需传入 base64 编码图像及可选描述文本；该能力仅限 `multimodal-embedding-v1` 模型，其输入格式与文本向量不兼容，详见 [向量与排序](../../raw/model-api-reference/vector-and-sort.md)。  
- **排序模型（Rerank）**：对给定 query 与一组 candidate texts 进行细粒度相关性打分并重排序，支持最大 100 个候选文本；模型 `rerank-v3` 为最新稳定版，[向量与排序](../../raw/model-api-reference/vector-and-sort.md) 中明确要求 query 字段不可为空且长度 ≤ 512 Unicode 字符。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 取值必须为 `text-embedding-v3`、`multimodal-embedding-v1` 或 `rerank-v3`，不支持别名或旧版模型（如 `text-embedding-v1` 已下线） |
| `input` | string / array | 是 | 文本向量：string 或 string[]；多模态向量：object 数组，含 `image` 和 `text` 字段；Rerank：object，含 `query` 和 `documents` 字段 |
| `encoding_format` | string | 否 | 可选 `float`（默认）或 `base64`；`base64` 仅适用于文本向量，多模态与 rerank 不支持 |
| `return_documents` | boolean | 否 | 仅 rerank 模型有效，设为 `true` 时在响应中返回原始 documents 字段 |

> **注意**：原始文档中 `multimodal-embedding-v1` 的示例请求体曾包含 `type: "image"` 字段，但该字段已于 v2.3.0 版本移除，实际调用时若传入将被忽略——请以 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 中最新 JSON Schema 为准。

## 使用方式

- **文本向量调用示例（单条）**：
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v1/embeddings \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
          "model": "text-embedding-v3",
          "input": "今天天气真好"
        }'
  ```

- **Rerank 调用示例（批量）**：
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v1/rerank \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
          "model": "rerank-v3",
          "query": "如何学习Python",
          "documents": ["Python入门教程", "Java编程基础", "Python数据分析实战"],
          "return_documents": true
        }'
  ```

- 多模态向量需使用 `input` 数组，每个元素为 `{ "image": "base64...", "text": "可选描述" }`，具体结构参见 [向量与排序](../../raw/model-api-reference/vector-and-sort.md)。

## 限制和注意事项

- 单次请求 `input` 元素总数上限：文本向量 ≤ 128 条，多模态向量 ≤ 32 条，Rerank ≤ 100 条（`documents` 长度）。
- 所有文本类输入（含 `query`、`documents`、`text` 字段）均按 Unicode 字符计长，超限将返回 `400 Bad Request`。
- `text-embedding-v3` 输出向量维度为 1024，`rerank-v3` 输出为 `[{"index": 0, "relevance_score": 0.92}]` 格式，无原始向量；二者不可混用作距离计算。
- 异步任务（`/v1/embeddings/async`）仅支持文本向量，不支持多模态与 rerank。

## 来源文档

- [向量与排序](../../raw/model-api-reference/vector-and-sort.md)


