# vector and sort

`vector and sort` 是百炼平台提供的向量嵌入（embedding）与重排序（reranking）能力集合，用于支持语义检索、相似度计算和结果精排等典型 RAG 场景。该能力由多个专用模型组成，覆盖文本单模态、多模态输入及跨文档相关性打分等需求。所有接口均通过标准 REST API 调用，需指定模型名称并遵循统一的请求体结构。

## 支持的模型/功能

- **文本向量模型**：如 `text-embedding-v1`，适用于通用中文/英文文本嵌入，输出 1024 维稠密向量；详细能力见 [向量与排序](../../raw/model-api-reference/vector-and-sort.md)  
- **多模态向量模型**：如 `multimodal-embedding-v1`，支持图像 URL + 文本描述联合编码，适用于图文混合检索场景，其输入格式与限制详见 [向量与排序](../../raw/model-api-reference/vector-and-sort.md)  
- **排序模型（Rerank）**：如 `rerank-v1`，接收 query + 多个 candidate texts，返回归一化相关性分数（0.0–1.0），不支持流式响应；该模型的调用方式与评估指标说明参见 [向量与排序](../../raw/model-api-reference/vector-and-sort.md)

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型标识符，例如 `"text-embedding-v1"` 或 `"rerank-v1"` |
| `input` | string / array | 是 | 文本向量模型接受单个字符串或字符串数组；rerank 模型要求为 `{ "query": "...", "documents": ["...", "..."] }` 对象 |
| `encoding_format` | string | 否 | 可选 `"float"`（默认）或 `"base64"`，仅对 embedding 接口生效 |

> **注意**：`multimodal-embedding-v1` 的 `input` 字段结构与文本向量模型不兼容——它必须是包含 `image_url` 和 `text` 字段的对象，而非字符串。此差异在 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 中未明确强调，但实际 API 校验会拒绝错误格式。

## 使用方式

1. 发送 `POST` 请求至 `/v1/embeddings`（向量）或 `/v1/rerank`（排序）端点  
2. 在请求头中携带 `Authorization: Bearer <api_key>`  
3. 请求体示例（rerank）：
   ```json
   {
     "model": "rerank-v1",
     "input": {
       "query": "量子计算原理",
       "documents": ["薛定谔方程是基础", "Shor算法用于质因数分解"]
     }
   }
   ```

## 限制和注意事项

- 单次请求最大 `documents` 数量为 50（rerank），文本向量批量上限为 2048 条（`input` 为数组时）  
- 所有向量模型输出维度固定，不可配置；rerank 模型不支持自定义 top-k 截断，需客户端自行处理  
- 图像 URL 必须可公开访问且响应头含 `Content-Type: image/*`，否则 `multimodal-embedding-v1` 将返回 `400` 错误 —— 此约束在 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 中未列出，但实测必现

## 来源文档

- [向量与排序](../../raw/model-api-reference/vector-and-sort.md)


