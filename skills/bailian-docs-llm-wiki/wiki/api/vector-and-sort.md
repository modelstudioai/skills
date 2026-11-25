# vector and sort

百炼平台提供[向量嵌入](../concepts/vector-embedding.md)（embedding）与排序（rerank）两类核心检索增强能力，支持文本、多模态内容的语义表征与相关性重排序。所有能力均通过统一 API 接口调用，适用于 RAG、语义搜索、推荐等场景。具体功能划分与模型支持详见 [向量与排序](../../raw/model-api-reference/vector-and-sort.md)。

## 支持的模型/功能

- **文本向量模型**：支持 `text-embedding-v1`（默认）、`text-embedding-v2`（更高精度，需显式指定），适用于中英文混合短文本嵌入；  
- **多模态向量模型**：`multimodal-embedding-v1` 支持图像+文本联合嵌入，输入为 base64 图像 + 可选描述文本；  
- **排序模型（Rerank）**：`rerank-v1` 和 `rerank-v2`，接受 query + 文档列表，输出重排序后的相关性分数；`rerank-v2` 支持长文档（max 512 tokens per doc），但 batch size 限制为 1；详情见 [向量与排序](../../raw/model-api-reference/vector-and-sort.md)。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `"text-embedding-v1"`、`"rerank-v2"`；必须与 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 中列出的模型名完全一致 |
| `input` | string / array | 是 | 向量模型：单字符串或字符串数组；排序模型：`{ "query": "...", "documents": [...] }` 对象 |
| `encoding_format` | string | 否 | 仅向量模型支持，可选 `"float"`（默认）或 `"base64"`；注意 `multimodal-embedding-v1` 不支持 `"base64"` 输出 |

> **注意**：原始文档中 `multimodal-embedding-v1` 的 `encoding_format` 描述存在矛盾——[向量与排序](../../raw/model-api-reference/vector-and-sort.md) 的子页 `multimodal-vector.md` 声明其仅支持 `"float"`，但 `general-text-vector.md` 错误地将该参数列为通用可选项。请以 multimodal-vector.md 实际行为为准。

## 使用方式

1. **向量调用示例（文本）**：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/services/embeddings \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "text-embedding-v1",
           "input": ["今天天气如何？", "北京明天会下雨吗？"]
         }'
   ```

2. **排序调用示例**：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/services/rerank \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "rerank-v2",
           "input": {
             "query": "量子计算原理",
             "documents": ["薛定谔方程是基础...", "Shor算法用于整数分解..."]
           }
         }'
   ```

## 限制和注意事项

- 单次请求最大 `input` 长度：文本向量模型为 2048 tokens，多模态向量模型图像尺寸上限为 1024×1024；  
- 排序模型 `rerank-v1` 最大 `documents` 数量为 10，`rerank-v2` 为 5（因长文本处理开销）；  
- 所有向量模型返回维度固定（`text-embedding-v1`: 1024, `multimodal-embedding-v1`: 512），不可配置；  
- 注意：`rerank-v2` 的 `top_k` 参数在 API 中实际未生效，当前始终返回全部输入文档的排序结果——该行为与 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 中“支持 top_k 截断”的描述不符，属文档过时，请以实际响应为准。

## 来源文档

- [向量与排序](../../raw/model-api-reference/vector-and-sort.md)


