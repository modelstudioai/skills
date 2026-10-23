# vector and sort

`vector and sort` 是百炼平台提供的[向量嵌入](../concepts/embedding.md)与排序（Rerank）能力集合，用于将文本、图像等输入转换为高维向量表示，或对候选结果列表按相关性重排序。该能力由多个专用模型支撑，支持同步调用与异步批处理，适用于[检索增强生成](../concepts/rag.md)（RAG）、语义搜索、推荐系统等场景。所有接口均通过统一 `/v1/embeddings` 和 `/v1/rerank` 路径接入。

## 支持的模型/功能

- **通用文本向量**：支持中英文混合文本的稠密向量生成，适用于通用语义检索；模型版本 `text-embedding-v3` 为当前默认推荐，兼容 `text-embedding-v2`（已标记为[原文标题](../../raw/model-api-reference/vector-and-sort/general-text-vector.md)）。  
- **多模态向量**：支持文本+图像联合嵌入，可用于跨模态检索；需传入 base64 编码图像及描述文本，详细格式见 [原文标题](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)。  
- **排序模型（Rerank）**：对给定 query 与一组 candidate texts 进行细粒度相关性打分并重排序；仅支持文本输入，不支持图像；最新模型 `rerank-v3` 已替代旧版 `rerank-v2`，后者在 [原文标题](../../raw/model-api-reference/vector-and-sort/rerank-model.md) 中仍有说明但已不建议使用。

> **注意**：`rerank-v2` 文档中声明支持 `top_k=100`，但实际 API 限制为 `top_k ≤ 50`（以 `/v1/rerank` 接口返回的 `422 Unprocessable Entity` 错误为准），请以当前 SDK 示例和 OpenAPI Schema 为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 取值为 `text-embedding-v3`、`multimodal-embedding-v1` 或 `rerank-v3`；不可混用 |
| `input` | string / array | 是 | 文本向量：单字符串或字符串数组；多模态：`{ "text": "...", "image": "base64..." }` 对象或对象数组；Rerank：`{ "query": "...", "documents": ["...", "..."] }` 对象 |
| `encoding_format` | string | 否 | 仅文本/多模态向量支持，可选 `"float"`（默认）或 `"base64"` |
| `return_documents` | boolean | 否 | 仅 Rerank 模型支持，设为 `true` 时在响应中返回原始 documents 字段 |

## 使用方式

- **文本向量调用示例（同步）**：
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v1/embeddings \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
          "model": "text-embedding-v3",
          "input": ["今天天气如何？", "What is the weather like today?"]
        }'
  ```

- **Rerank 调用示例（同步）**：
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v1/rerank \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
          "model": "rerank-v3",
          "query": "量子计算原理",
          "documents": ["量子比特介绍", "Shor算法详解", "经典计算机架构"],
          "top_k": 2
        }'
  ```

- 所有向量类请求最大 `input` 长度为 8192 token（按模型 tokenizer 计算）；Rerank 的 `documents` 总长度上限为 4096 token（含 query）。

## 限制和注意事项

- 单次请求最多支持 100 个文本向量生成（`input` 数组长度 ≤ 100），但多模态向量仅支持单条输入（数组长度必须为 1）。
- Rerank 模型不支持流式响应（`stream: true` 将被忽略），且 `top_k` 实际有效范围为 `1–50`（超出将报错）。
- 多模态向量模型对图像分辨率无硬性限制，但建议 ≤ 1024×1024，超大图像可能导致 OOM 或超时；具体约束详见 [原文标题](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)。
- 所有向量输出均为归一化后的 float32 向量（L2 norm = 1.0），无需额外归一化即可用于余弦相似度计算。

## 来源文档

- [向量与排序](../../raw/model-api-reference/vector-and-sort.md)


