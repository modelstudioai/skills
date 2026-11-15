# vector and sort

`vector and sort` 是百炼平台提供的向量嵌入与排序（Rerank）能力集合，用于文本语义向量化、跨模态特征提取及检索结果重排序。该能力通过统一 API 接口封装，支持多种模型选型和细粒度参数控制，适用于搜索、推荐、RAG 等典型场景。所有服务均需通过 `POST /v1/embeddings` 或 `/v1/rerank` 调用，遵循标准鉴权与限流策略。

## 支持的模型/功能

- **文本向量模型**：支持 `text-embedding-v1`、`text-embedding-v2` 等通用文本嵌入模型，输出 1024 维稠密向量；详见 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 中的子文档说明。
- **多模态向量模型**：支持图像-文本联合嵌入（如 `multimodal-embedding-v1`），可对图像 URL 或 base64 编码图像生成与文本对齐的向量；该能力在 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 的 [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md) 子文档中定义。
- **排序模型（Rerank）**：提供 `rerank-v1` 和 `rerank-v2`，支持对 query-documents 对进行相关性打分并排序；其输入格式与返回结构在 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 的 [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md) 子文档中明确约定。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型 ID，如 `"text-embedding-v2"` 或 `"rerank-v2"`；必须与所调用端点匹配（`/v1/embeddings` 仅接受 embedding 类模型） |
| `input` | string \| string[] \| object[] | 是 | 文本向量：字符串或字符串数组；Rerank：`{ "query": "...", "documents": ["...", "..."] }` 结构 |
| `encoding_format` | string | 否 | 可选 `"float"`（默认）或 `"base64"`；影响向量数值的序列化方式 |
| `return_documents` | boolean | 否 | Rerank 专用，设为 `true` 时在响应中返回原始 documents 字段 |

> **注意**：原始文档中 `multimodal-vector.md` 提到图像输入支持 `image_url` 和 `image_data` 两种形式，但最新 SDK 实现仅校验 `image_url`；请以 [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md) 文档的当前版本为准，避免使用已弃用的 `image_data` 字段。

## 使用方式

- **文本向量化**：  
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v1/embeddings \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
          "model": "text-embedding-v2",
          "input": ["今天天气很好", "适合出门散步"]
        }'
  ```

- **Rerank 调用**：  
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v1/rerank \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
          "model": "rerank-v2",
          "input": {
            "query": "如何学习 Python？",
            "documents": ["Python 入门教程", "Java 编程基础", "Python 高级技巧"]
          }
        }'
  ```

## 限制和注意事项

- 单次请求最多支持 100 个文本（embedding）或 50 个 documents（rerank）；超出将返回 `400 Bad Request`。
- 多模态向量模型不支持批量图像处理，每次请求仅接受单张图像 + 可选文本描述；具体约束见 [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)。
- 所有向量模型对输入长度敏感：`text-embedding-v2` 最大 token 数为 8192，超长文本将被截断且**不触发警告**；建议预处理时主动分段。
- Rerank 模型对 `query` 和 `documents` 的语言一致性无强制校验，但混用中英文可能导致效果下降；[排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md) 明确建议同语种输入。

## 来源文档

- [向量与排序](../../raw/model-api-reference/vector-and-sort.md)


