# vector and sort

`vector and sort` 是百炼平台提供的向量嵌入与排序（Rerank）能力集合，用于支持语义检索、相似度计算和结果重排序等典型 RAG 场景。该能力涵盖文本向量、多模态向量及专用排序模型三类服务，统一通过 `/v1/embeddings` 和 `/v1/rerank` 接口调用。所有模型均需显式指定 `model` 参数，且不支持跨类型混用。

## 支持的模型/功能

- **通用文本向量**：支持中英文混合文本的稠密向量生成，适用于文档嵌入、聚类等任务；模型如 `text-embedding-v3`（推荐）、`text-embedding-v2`（已逐步下线）。详见 [向量与排序](../../raw/model-api-reference/vector-and-sort.md)。
- **多模态向量**：支持图像+文本联合嵌入（如 `multimodal-embedding-v1`），输出统一维度向量，适用于图文跨模态检索。该能力在 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 中有独立子章节说明。
- **排序模型（Rerank）**：专用于对候选文档列表按相关性重打分排序，输入为 query + 文本列表，输出为带 score 的排序结果；当前仅支持 `rerank-v3`，不支持自定义阈值或 top-k 截断逻辑。参考 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 中的 rerank 模型说明。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 必须为具体模型名（如 `text-embedding-v3`、`rerank-v3`），不可省略或使用别名 |
| `input` | string / string[] | 是 | 向量接口接受单字符串或字符串数组；rerank 接口必须为 `{ "query": "...", "documents": ["...", "..."] }` 对象 |
| `encoding_format` | string | 否 | 仅向量接口支持，可选 `"float"`（默认）或 `"base64"`；rerank 接口不支持此参数 |
| `return_documents` | boolean | 否 | 仅 rerank 接口支持，设为 `true` 时返回原始 documents 字段（默认 `false`） |

> **注意**：`text-embedding-v2` 在部分旧版 SDK 示例中仍被引用，但其已停止维护且输出维度与 v3 不兼容；请务必使用 `text-embedding-v3`，详见 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 中的版本说明。

## 使用方式

- 向量生成（POST `/v1/embeddings`）：
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v1/embeddings \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
          "model": "text-embedding-v3",
          "input": ["hello", "world"]
        }'
  ```

- 排序调用（POST `/v1/rerank`）：
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v1/rerank \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
          "model": "rerank-v3",
          "query": "人工智能开源框架",
          "documents": ["PyTorch 是一个开源机器学习库", "Linux 是一种操作系统"]
        }'
  ```

## 限制和注意事项

- 单次请求最大 `input` 数量：文本向量 ≤ 100 条，rerank ≤ 50 条文档；
- 输入文本总 token 数（含 query）不得超过 8192（rerank）或 2048（向量）；
- 所有向量模型输出为 float32 数组，未归一化；如需余弦相似度，请自行 L2 归一化后点积；
- `multimodal-embedding-v1` 当前仅支持 base64 编码图像 URL 或本地文件二进制上传，不支持纯文本输入——此行为与文本向量模型存在本质差异，需严格区分调用路径。

## 来源文档

- [向量与排序](../../raw/model-api-reference/vector-and-sort.md)


