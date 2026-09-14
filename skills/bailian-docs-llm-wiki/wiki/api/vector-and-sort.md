# vector and sort

百炼平台提供[向量嵌入](../concepts/embedding.md)（Embedding）与排序（Rerank）两类核心检索增强能力，分别用于将文本/多模态内容映射到稠密向量空间，以及对候选结果进行相关性重排序。二者常配合使用，构成 RAG 流程中的关键环节。所有能力均通过统一的 `/v1/embeddings` 和 `/v1/rerank` API 接口调用。

## 支持的模型/功能

- **向量模型**：支持通用文本向量（如 `text-embedding-v1`）和多模态向量（如 `multimodal-embedding-v1`），适用于语义检索、聚类等场景。  
- **排序模型**：提供专用 rerank 模型（如 `gte-rerank`、`bge-rerank-v2`），接受 query + 多个 documents 输入，输出归一化相关性分数。  
- 详细能力列表及适用场景见 [向量与排序](../../raw/model-api-reference/vector-and-sort.md)。

## 关键参数

- **向量接口**：`model`（必需）、`input`（字符串或字符串数组）、`encoding_format`（可选，`float` 或 `base64`）。  
- **排序接口**：`model`（必需）、`query`（字符串）、`documents`（字符串数组，最多 100 条）、`return_documents`（布尔，默认 `false`）。  
- 所有参数定义与取值约束详见 [向量与排序](../../raw/model-api-reference/vector-and-sort.md)。

## 使用方式

1. 向量调用示例（Python）：
   ```python
   client.embeddings.create(model="text-embedding-v1", input=["hello", "world"])
   ```
2. 排序调用示例：
   ```python
   client.rerank.create(model="gte-rerank", query="如何部署大模型", documents=["部署指南", "API 文档", "本地运行教程"])
   ```
3. 注意：排序模型不支持流式响应；向量批量输入长度上限为 2048 tokens（单条文本），超出将被截断 —— 此限制在 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 中明确说明。

## 限制和注意事项

- 向量模型不支持微调；排序模型仅支持推理，不可作为生成模型使用。  
- 单次排序请求 `documents` 数量上限为 100，超过将返回 `400 Bad Request`。  
- > **注意**：原始文档中链接指向 help.aliyun.com 的产品页，但实际 API 行为以 `raw/model-api-reference/vector-and-sort.md` 中的参数定义和错误码为准；help 页面未覆盖全部边界情况（如 base64 编码精度损失），开发时请以该原始文档为权威依据。

## 来源文档

- [向量与排序](../../raw/model-api-reference/vector-and-sort.md)


