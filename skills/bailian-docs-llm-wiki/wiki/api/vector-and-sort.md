# vector and sort

`vector and sort` 是百炼平台提供的向量嵌入与排序（Rerank）能力集合，涵盖文本向量化、多模态向量化及语义重排序三大功能。所有能力均通过统一 API 接口调用，支持同步请求与流式响应。该能力面向[检索增强生成](../concepts/rag.md)（RAG）、相似性搜索、内容推荐等典型场景，适用于需要高质量语义表征与精细化相关性打分的开发者。

## 支持的模型/功能

- **通用文本向量**：支持中英文混合文本的稠密向量生成，输出 1024 维 float32 向量，适用于文档嵌入、召回阶段向量检索。详见 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 中的子文档说明。
- **多模态向量**：支持图像 + 文本联合编码，生成跨模态对齐向量，可用于图文检索、以图搜文等任务。该能力在 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 的多模态子文档中有详细输入格式与示例。
- **排序模型（Rerank）**：对给定 query 与候选文档列表进行细粒度相关性打分（0–1 区间），支持 batch size ≤ 100。其设计目标是提升 top-k 检索结果的精度，而非替代向量召回。该功能同样归属 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 主文档体系。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `text-embedding-v3`、`multimodal-embedding-v1`、`rerank-v3`；必须与所选功能严格匹配 |
| `input` | string / array | 是 | 文本向量：单字符串或字符串数组；多模态向量：含 `text` 和 `image_url` 字段的对象数组；Rerank：含 `query`（string）与 `documents`（string 数组）的对象 |
| `encoding_format` | string | 否 | 可选 `float`（默认）或 `base64`；仅影响向量返回格式，不影响计算逻辑 |

> **注意**：`rerank-v3` 模型不支持 `encoding_format=base64`，若传入将返回 400 错误；此限制未在 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 主文档中明确说明，但已在 rerank 子文档中更新。

## 使用方式

1. **文本向量调用示例（单条）**：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/embeddings" \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "text-embedding-v3",
           "input": "人工智能正在改变世界"
         }'
   ```

2. **Rerank 批量调用（最多 100 条 documents）**：
   ```json
   {
     "model": "rerank-v3",
     "input": {
       "query": "如何训练大语言模型？",
       "documents": ["LLM 训练需大量算力", "微调是常见训练方式", "数据清洗很关键"]
     }
   }
   ```

3. 所有请求均需携带 `X-DashScope-Async` 头控制同步/异步行为（默认同步）；异步模式下需轮询 `task_id` 获取结果。

## 限制和注意事项

- 单次请求中，`input` 字符串总长度上限为 8192 token（按模型 tokenizer 计算），超长文本将被截断且**不报错**，建议预处理；
- 多模态向量接口要求 `image_url` 必须可公开访问且响应头含 `Content-Type: image/*`，否则返回 400；
- Rerank 模型对 `query` 和 `documents` 均做长度归一化处理，但过短（< 5 字符）或过长（> 512 token）输入可能导致打分稳定性下降；
- 所有向量模型输出向量**不保证正交或单位长度**，距离计算请使用余弦相似度而非欧氏距离——该要点在 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 中未强调，但实测验证为必要实践。

## 来源文档

- [向量与排序](../../raw/model-api-reference/vector-and-sort.md)


