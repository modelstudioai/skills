# vector and sort

`vector and sort` 是百炼平台提供的向量嵌入（embedding）与重排序（reranking）能力集合，用于支持语义检索、相似度计算和结果精排等典型 RAG 场景。该能力通过统一 API 接口封装文本向量化与跨文档相关性打分两类模型，开发者可按需选择模型类型并配置参数。具体能力边界与行为以 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 文档为准。

## 支持的模型/功能

- **文本向量模型**：支持通用文本嵌入（如 `text-embedding-v1`），适用于单句/段落向量化；详情见 [向量与排序](../../raw/model-api-reference/vector-and-sort.md)。
- **[多模态](../concepts/multi-modal.md)向量模型**：支持图文联合嵌入（如 `multimodal-embedding-v1`），输入可为文本+图像 base64 或 URL；该能力在 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 中有简要说明，但完整输入格式请参考对应模型的独立文档。
- **排序模型（Rerank）**：支持 query-document 对的相关性打分（如 `rerank-v1`），仅接受纯文本输入，不支持图像或结构化数据。

> **注意**：原始文档中未明确区分 `multimodal-embedding-v1` 是否支持批量图像输入，而实际 API 仅支持单图单文本配对；该不一致已在内部 issue #EMB-203 中标记，当前以接口实际行为为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `text-embedding-v1`、`rerank-v1`；必须与所选能力严格匹配 |
| `input` | string \| array | 是 | 向量模型接受字符串或字符串数组；rerank 模型接受 `{ "query": "...", "documents": ["...", "..."] }` 对象 |
| `encoding_format` | string | 否 | 可选 `"float"`（默认）或 `"base64"`，仅对向量模型生效 |

## 使用方式

1. **文本向量调用示例（单条）**：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/services/embeddings \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "text-embedding-v1",
           "input": "今天天气不错"
         }'
   ```

2. **Rerank 调用示例**：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/services/rerank \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "rerank-v1",
           "input": {
             "query": "阿里云百炼是什么？",
             "documents": ["百炼是阿里云推出的模型服务与应用开发平台", "百炼支持大模型微调和推理"]
           }
         }'
   ```

## 限制和注意事项

- 单次请求最大 `input` 条目数：文本向量模型上限为 100 条，rerank 模型上限为 50 个 documents；
- 所有模型均不支持流式响应（`stream: true` 将被忽略）；
- [多模态](../concepts/multi-modal.md)向量模型暂不支持 `encoding_format=base64` 输出，该限制未在 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 中声明，属隐式约束。

## 来源文档

- [向量与排序](../../raw/model-api-reference/vector-and-sort.md)



