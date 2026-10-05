# vector and sort

`vector and sort` 是百炼平台提供的向量嵌入与排序（Rerank）能力集合，用于支持语义检索、相似度计算和结果重排序等典型 RAG 场景。该能力涵盖文本向量生成、多模态向量生成及跨模态/单模态排序模型三类服务，统一通过 `/v1/embeddings` 和 `/v1/rerank` 接口调用。所有模型均需显式指定 `model` 参数，不支持默认模型自动路由。

## 支持的模型/功能

- **文本向量模型**：支持 `text-embedding-v1`、`text-embedding-v2` 等通用文本嵌入模型，适用于中英文混合短文本（≤512 tokens）；详情见 [向量与排序](../../raw/model-api-reference/vector-and-sort.md)。
- **多模态向量模型**：支持 `multimodal-embedding-v1`，可对图像 URL + 文本描述联合编码，输出统一 1024 维向量；该能力在 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 中有完整输入格式说明。
- **排序模型（Rerank）**：提供 `rerank-v1` 和 `rerank-v2`，支持 query-document 对的细粒度相关性打分（输出 0~1 分数），最高支持 100 个文档批量重排；其请求结构与参数约束详见 [向量与排序](../../raw/model-api-reference/vector-and-sort.md)。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `"text-embedding-v1"` 或 `"rerank-v2"`；不可省略 |
| `input` | string / array | 是 | 向量模型接受单字符串或字符串数组；排序模型必须为 `{ "query": "...", "documents": [...] }` 对象 |
| `encoding_format` | string | 否 | 可选 `"float"`（默认）或 `"base64"`；仅向量模型支持 |

> **注意**：`rerank-v1` 的 `top_k` 参数最大值为 50，而 `rerank-v2` 支持 `top_k=100`；旧文档中未明确区分此限制，实际以 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 中最新版本为准。

## 使用方式

- 向量调用示例（POST `/v1/embeddings`）：
  ```json
  { "model": "text-embedding-v2", "input": ["杭州天气如何？", "北京今天下雨了吗？"] }
  ```
- 排序调用示例（POST `/v1/rerank`）：
  ```json
  {
    "model": "rerank-v2",
    "query": "量子计算原理",
    "documents": ["量子比特是基本单元", "Python 是编程语言", "薛定谔方程描述波函数演化"]
  }
  ```

## 限制和注意事项

- 所有向量模型单次请求 `input` 数组长度上限为 2048；排序模型 `documents` 数组上限为 100。
- 多模态向量模型暂不支持本地图片上传，仅接受公网可访问的 `https://` 图像 URL。
- `text-embedding-v1` 已进入维护期，新项目应优先选用 `text-embedding-v2`（参见 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 的模型状态说明）。

## 来源文档

- [向量与排序](../../raw/model-api-reference/vector-and-sort.md)


