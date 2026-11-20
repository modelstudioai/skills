# vector and sort

`vector and sort` 是百炼平台提供的[向量嵌入](../concepts/vector-embedding.md)（embedding）与重排序（reranking）能力集合，用于支持语义检索、相似度计算和结果精排等典型 RAG 场景。该能力由多个专用模型组成，覆盖文本单模态、多模态输入及跨文档相关性打分等需求。所有接口均通过标准 REST API 调用，需在请求中明确指定模型名称与输入格式。

## 支持的模型/功能

- **通用文本向量模型**：如 `text-embedding-v1`，适用于中英文短文本（≤512 token）的稠密向量生成，输出 1024 维 float32 向量；详情见 [向量与排序](../../raw/model-api-reference/vector-and-sort.md)。  
- **多模态向量模型**：如 `multimodal-embedding-v1`，支持图像 URL + 文本描述联合编码，输出统一向量空间表示；其输入约束与归一化方式详见 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 中的子文档说明。  
- **排序模型（Rerank）**：如 `rerank-v1`，接收 query + 多个 candidate texts，返回按相关性降序排列的分数列表；该模型不支持流式响应，且仅接受纯文本输入——[向量与排序](../../raw/model-api-reference/vector-and-sort.md) 明确指出其不兼容 Base64 图像或结构化 JSON 字段。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型标识符，例如 `"text-embedding-v1"` 或 `"rerank-v1"`；必须与 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 中公布的模型列表严格一致 |
| `input` | string / array | 是 | 文本向量模型接受单个字符串；rerank 模型接受 `{ "query": "...", "documents": ["...", "..."] }` 对象；多模态模型要求 `{"image_url": "...", "text": "..."}` |
| `encoding_format` | string | 否 | 可选 `"float"`（默认）或 `"base64"`；注意 `rerank-v1` 不支持 `"base64"`，此限制在 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 中有明确说明 |

## 使用方式

1. 构造 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/services/embeddings`（向量）或 `/api/v1/services/rerank`（排序）；  
2. 设置 `Authorization: Bearer <api_key>` 与 `Content-Type: application/json`；  
3. 在 body 中传入符合上述参数规范的 JSON；  
4. 成功响应包含 `output.embeddings`（向量）或 `output.results`（rerank），字段结构与 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 完全一致。

## 限制和注意事项

- 单次 rerank 请求最多支持 100 个 documents；超出将返回 `400 Bad Request`；  
- 所有向量模型对输入长度敏感：`text-embedding-v1` 截断超长文本至 512 token，但 `multimodal-embedding-v1` 对图像 URL 的 HTTP 响应超时阈值为 5 秒，此差异未在 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 中统一说明；  
> **注意**：原始文档中 `multimodal-embedding-v1` 子文档（`raw/model-api-reference/vector-and-sort/multimodal-vector.md`）声称支持 `image_bytes` 字段直接传入二进制，但当前 API 实际仅接受 `image_url` —— 该功能尚未上线，以线上行为为准。

## 来源文档

- [向量与排序](../../raw/model-api-reference/vector-and-sort.md)


