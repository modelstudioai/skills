# vector and sort

百炼平台提供向量嵌入（Vector Embedding）与排序（Rerank）两类核心检索增强能力，分别用于将文本/多模态内容映射至语义向量空间，以及对候选结果进行精细化相关性重排序。二者常配合使用，构成 RAG 流程中“召回→重排”关键环节。所有能力均通过统一模型 API 调用，支持同步请求与流式响应。

## 支持的模型/功能

- **文本向量模型**：支持通用文本嵌入（如 `text-embedding-v1`），适用于关键词、段落、文档级语义表征；详情见 [向量与排序](../../raw/model-api-reference/vector-and-sort.md)。
- **多模态向量模型**：支持图文联合嵌入（如 `multimodal-embedding-v1`），输入可为文本+图像 URL 或 base64 编码图像；该能力在 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 中有明确说明。
- **排序模型（Rerank）**：专用于对已召回的 Top-K 候选文本列表按查询相关性打分并重排序，仅接受 query + texts 列表输入，不支持单文本嵌入；参见 [向量与排序](../../raw/model-api-reference/vector-and-sort.md)。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型 ID，如 `text-embedding-v1`、`rerank-v1` |
| `input` | string \| string[] \| object | 是 | 向量模型：单字符串或字符串数组；排序模型：必须为 `{ query: string, documents: string[] }` 对象 |
| `encoding_format` | string | 否 | 可选 `float`（默认）或 `base64`，影响 `embedding` 字段编码方式 |

> **注意**：排序模型的 `input` 格式与向量模型严格不同，且不支持 `batch_size` 参数——该字段仅在部分旧版 SDK 示例中出现，实际 API 不识别，应以 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 官方定义为准。

## 使用方式

- 向量调用示例（批量文本嵌入）：
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v1/services/embeddings \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
          "model": "text-embedding-v1",
          "input": ["今天天气如何", "明天会下雨吗"]
        }'
  ```

- 排序调用示例：
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v1/services/rerank \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
          "model": "rerank-v1",
          "input": {
            "query": "阿里云百炼平台怎么调用向量API？",
            "documents": ["参考文档A：快速入门", "参考文档B：参数说明", "参考文档C：错误码列表"]
          }
        }'
  ```

## 限制和注意事项

- 单次向量请求最多支持 100 个文本（`input` 数组长度 ≤ 100）；排序请求最多支持 100 个 `documents`。
- 所有向量模型输出维度固定（如 `text-embedding-v1` 为 1536 维），不可配置；多模态向量模型暂不支持自定义图像预处理逻辑。
- 排序模型返回结果中 `results` 字段为按 score 降序排列的索引数组，**不返回原始文本内容**，需客户端自行映射；此行为与部分第三方文档描述不符，应以 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 实际响应结构为准。

## 来源文档

- [向量与排序](../../raw/model-api-reference/vector-and-sort.md)


