# vector and sort

`vector and sort` 是百炼平台提供的[向量嵌入](../concepts/vector-embedding.md)（embedding）与重排序（reranking）能力集合，用于支持语义检索、相似度计算和结果精排等典型 RAG 场景。该能力由多个专用模型组成，覆盖文本单模态、多模态输入及跨文档相关性打分等需求。所有接口均通过标准 REST API 调用，需在请求中明确指定模型名称与输入格式。

## 支持的模型/功能

- **通用文本向量模型**：如 `text-embedding-v1`，适用于长文本、短句、关键词的稠密向量生成，输出 1024 维 float32 向量；详见 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 中的子文档说明。
- **多模态向量模型**：如 `multimodal-embedding-v1`，支持文本+图像联合嵌入，要求输入为 base64 编码图像与描述文本组合；该能力在 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 的多模态子页中有详细 schema 定义。
- **排序模型（Rerank）**：如 `rerank-v1`，接收 query + 多个 candidate texts，返回归一化相关性分数（0.0–1.0），不支持流式响应；其输入长度限制与评分逻辑参见 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 的 rerank 子文档。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `"text-embedding-v1"`、`"rerank-v1"`；必须与实际部署模型严格匹配 |
| `input` | string / array | 是 | 文本向量模型接受 string 或 string[]；rerank 模型接受 `{ "query": "...", "documents": ["...", "..."] }` 对象 |
| `encoding_format` | string | 否 | 可选 `"float"`（默认）或 `"base64"`；仅文本向量模型支持 `"base64"` 输出 |
| `top_k` | integer | 否 | 仅 rerank 模型有效，指定返回最高分的前 K 个结果（默认 5，最大 100） |

> **注意**：`text-embedding-v1` 的 `input` 字段在部分旧版 SDK 示例中被误标为支持 object 类型，但根据最新 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 规范，仅接受 string 或 string[]，传入 object 将返回 400 错误。

## 使用方式

1. **文本向量调用示例（同步）**：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/embeddings \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "text-embedding-v1",
           "input": ["今天天气很好", "人工智能正在快速发展"]
         }'
   ```

2. **Rerank 调用示例**：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/rerank \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "rerank-v1",
           "input": {
             "query": "量子计算的应用场景有哪些？",
             "documents": [
               "量子计算可用于密码破解。",
               "它在材料模拟中具有优势。",
               "与经典计算机相比功耗更低。"
             ]
           }
         }'
   ```

## 限制和注意事项

- 所有向量模型单次请求 `input` 元素数上限为 128（文本向量）或 100（rerank）；超出将触发 `429 Too Many Requests`。
- rerank 模型对 `query` 和每个 `document` 的总 token 数限制为 2048（按模型 tokenizer 计算），超长内容将被截断，**不会报错但影响精度**。
- 多模态向量模型暂不支持批量图像处理（即 `input` 中不能包含多个图像对象），此限制在 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 的 multimodal-vector 子页中已明确标注。

## 来源文档

- [向量与排序](../../raw/model-api-reference/vector-and-sort.md)


