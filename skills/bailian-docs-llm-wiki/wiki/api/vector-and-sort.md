# vector and sort

`vector and sort` 是百炼平台提供的向量嵌入与排序（Rerank）能力集合，用于支持语义检索、相似度计算和结果重排序等典型 RAG 场景。该能力涵盖文本向量生成、多模态向量生成及跨模态/单模态排序模型三类服务，统一通过 `/v1/embeddings` 和 `/v1/rerank` 接口调用。所有模型均需显式指定 `model` 参数，且不支持动态参数 fallback。

## 支持的模型/功能

- **文本向量模型**：支持通用文本嵌入（如 `text-embedding-v1`），适用于中英文混合短文本，输出 1024 维稠密向量；详情见 [向量与排序](../../raw/model-api-reference/vector-and-sort.md)。
- **多模态向量模型**：支持图像-文本联合嵌入（如 `multimodal-embedding-v1`），可对图像 URL 或 base64 编码图像 + 文本描述生成统一向量空间表示；该能力在 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 中有完整说明。
- **排序模型（Rerank）**：提供 `rerank-v1` 等模型，接受 query + document list 输入，返回归一化相关性分数；其输入长度限制和 batch 行为与文本向量模型不同，具体参见 [向量与排序](../../raw/model-api-reference/vector-and-sort.md)。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `"text-embedding-v1"`、`"rerank-v1"`；不可省略或使用别名 |
| `input` | string / string[] / object[] | 是 | 文本向量：字符串或字符串数组；Rerank：`{ "query": "...", "documents": ["...", "..."] }` 对象数组 |
| `encoding_format` | string | 否 | 可选 `"float"`（默认）或 `"base64"`；仅对 `/v1/embeddings` 生效 |

> **注意**：原始文档中 `multimodal-embedding-v1` 的 `input` 格式描述存在歧义——[向量与排序](../../raw/model-api-reference/vector-and-sort.md) 的子页 `multimodal-vector.md` 要求必须为 `{ "image": "...", "text": "..." }` 对象，而主文档未明确此约束，实际调用时若传入字符串将返回 `400` 错误。

## 使用方式

- **文本向量调用示例**（HTTP POST `/v1/embeddings`）：
  ```json
  { "model": "text-embedding-v1", "input": ["hello", "world"] }
  ```
- **Rerank 调用示例**（HTTP POST `/v1/rerank`）：
  ```json
  {
    "model": "rerank-v1",
    "query": "人工智能开源框架",
    "documents": ["PyTorch 是一个开源机器学习库", "Linux 是一种操作系统"]
  }
  ```
- 所有请求需携带有效的 `Authorization: Bearer <api_key>` 头；响应结构遵循 OpenAI 兼容格式，但 `data` 字段中 `embedding` 或 `relevance_score` 字段命名与标准略有差异，详见各子页定义。

## 限制和注意事项

- 单次 `/v1/embeddings` 请求最多支持 2048 个 token（按模型 tokenizer 计算），超限将截断；`/v1/rerank` 的 `query` + 单个 `document` 总长度上限为 512 token。
- `text-embedding-v1` 不支持长文本分块自动合并，客户端需自行切分并聚合向量（如取平均）。
- 多模态向量模型暂不支持纯文本输入（即 `text` 字段为空），即使 `image` 有效也会报错；该限制未在 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 主文档中明确说明，仅在子页 `multimodal-vector.md` 的“错误码”章节提及。

## 来源文档

- [向量与排序](../../raw/model-api-reference/vector-and-sort.md)


