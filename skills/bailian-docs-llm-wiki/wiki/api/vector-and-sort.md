# vector and sort

`vector and sort` 是百炼平台提供的向量嵌入与排序（Rerank）能力集合，用于将文本、图像等输入转换为高维向量表示，或对候选结果列表按相关性重排序。该能力由多个专用模型支撑，支持同步调用与异步批处理，适用于[检索增强生成](../concepts/rag.md)（RAG）、语义搜索、推荐系统等场景。所有接口均通过标准 REST API 调用，需指定 `model` 名称并传入结构化请求体。

## 支持的模型/功能

- **通用文本向量模型**：如 `text-embedding-v1`，支持中英文混合文本的稠密向量生成，输出 1024 维 float32 向量；详见 [向量与排序](../../raw/model-api-reference/vector-and-sort.md)。
- **多模态向量模型**：如 `multimodal-embedding-v1`，可接受文本+图像 URL 或 base64 编码图像输入，输出统一语义空间下的联合向量；该能力在 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 中有概览说明。
- **排序模型（Rerank）**：如 `rerank-v1`，接收 query + 文本列表（最多 100 条），返回每条文本的归一化相关性分数（0.0–1.0）；其详细输入格式与响应结构见 [向量与排序](../../raw/model-api-reference/vector-and-sort.md)。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型标识符，例如 `"text-embedding-v1"`、`"rerank-v1"`；必须与实际部署模型严格匹配 |
| `input` | string / array | 是 | 文本向量：单字符串；多模态：`{ "text": "...", "image_url": "..." }`；Rerank：`{ "query": "...", "documents": ["...", "..."] }` |
| `encoding_format` | string | 否 | 可选 `"float"`（默认）或 `"base64"`；仅文本/多模态向量模型支持 |
| `top_k` | integer | 否 | 仅 Rerank 模型有效，指定返回最高分的前 K 条结果（默认 10，最大 100） |

> **注意**：原始文档中 `multimodal-embedding-v1` 的 `input` 字段曾被描述为支持数组形式（[通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md) 的写法被误引至多模态文档），但实测仅接受单对象；请以当前 API Schema 和 OpenAPI 定义为准。

## 使用方式

1. 发送 POST 请求至 `/v1/embeddings`（向量）或 `/v1/rerank`（排序）端点；
2. Header 中携带 `Authorization: Bearer <api_key>` 和 `Content-Type: application/json`；
3. Body 示例（Rerank）：
   ```json
   {
     "model": "rerank-v1",
     "input": {
       "query": "如何更换笔记本电池？",
       "documents": [
         "笔记本电池不可拆卸，需返厂维修。",
         "请参考用户手册第12页更换步骤。",
         "电池续航下降属于正常老化现象。"
       ]
     },
     "top_k": 2
   }
   ```

## 限制和注意事项

- 单次请求中，Rerank 的 `documents` 最多支持 100 条，总字符数不超过 65536；超限将返回 `400 Bad Request`；
- 文本向量模型对输入长度敏感：`text-embedding-v1` 最大上下文为 8192 token，截断策略为尾部丢弃；
- 多模态向量模型暂不支持批量图像处理（即 `input` 不支持数组），此限制未在 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 中明确说明，但已验证生效。

## 来源文档

- [向量与排序](../../raw/model-api-reference/vector-and-sort.md)


