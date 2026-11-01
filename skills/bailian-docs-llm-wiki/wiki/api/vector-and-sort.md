# vector and sort

`vector and sort` 是百炼平台提供的向量嵌入（embedding）与重排序（reranking）能力集合，用于支持语义检索、相似度计算和搜索结果精排等典型 RAG 场景。该能力由多个专用模型提供，覆盖文本单模态、多模态输入及跨文档相关性打分。所有接口均通过统一的 `/v1/embeddings` 和 `/v1/rerank` 路径调用。

## 支持的模型/功能

- **文本向量模型**：支持通用文本嵌入，如 `text-embedding-v1`，适用于长文本、短句、关键词等多种输入格式，输出 1024 维稠密向量。详见 [向量与排序](../../raw/model-api-reference/vector-and-sort.md)。
- **多模态向量模型**：支持图像+文本联合嵌入（如 `multimodal-embedding-v1`），可对图文对生成统一语义向量，适用于跨模态检索任务。该能力在 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 的子文档中有详细说明。
- **排序模型（Rerank）**：提供 `rerank-v1` 等模型，接收查询 + 候选文本列表，返回归一化相关性分数（0.0–1.0），不支持 batch query 或跨语言混合排序。具体输入约束见 [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md)。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型 ID，如 `"text-embedding-v1"`、`"rerank-v1"`；必须与请求路径匹配（`/v1/embeddings` 仅接受 embedding 模型） |
| `input` | string / string[] / object[] | 是 | embedding 接口支持字符串或字符串数组；rerank 接口要求为 `{ "query": "...", "documents": ["...", "..."] }` 对象 |
| `encoding_format` | string | 否 | 可选 `"float"`（默认）或 `"base64"`；影响向量数值的序列化方式 |
| `top_k` | integer | 否（rerank 专属） | 仅 rerank 接口有效，指定返回最高分的前 K 个结果（默认 3，最大 10） |

> **注意**：原始文档中 `rerank-v1` 的 `top_k` 最大值标注为 20，但当前 API 实际限制为 10（服务端校验返回 `400 InvalidParameter`），请以 [排序模型（Rerank）](../../raw/model-api-reference/vector-and-sort/rerank-model.md) 的运行时行为为准。

## 使用方式

- **文本向量调用示例（cURL）**：
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v1/embeddings \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
          "model": "text-embedding-v1",
          "input": ["今天天气很好", "人工智能正在改变世界"]
        }'
  ```

- **Rerank 调用示例**：
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v1/rerank \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
          "model": "rerank-v1",
          "input": {
            "query": "如何部署大模型",
            "documents": ["使用Docker部署Qwen", "本地编译LLaMA源码", "通过百炼控制台一键发布"]
          },
          "top_k": 3
        }'
  ```

## 限制和注意事项

- 单次 embedding 请求最多支持 128 个文本项（`input` 数组长度 ≤ 128）；单文本长度上限为 8192 token（超长截断，无警告）。
- Rerank 接口 `documents` 列表长度上限为 100，且所有文档总 token 数不得超过 32768（按模型 tokenizer 计算）。
- 所有向量模型输出为 float32，未做 L2 归一化；如需余弦相似度，请在客户端自行归一化后计算点积。
- 多模态向量暂不支持纯图像输入（即 `input` 中缺少文本字段时会报错），必须提供 `{"image_url": "...", "text": "..."}` 结构，详见 [多模态向量](../../raw/model-api-reference/vector-and-sort/multimodal-vector.md)。

## 来源文档

- [向量与排序](../../raw/model-api-reference/vector-and-sort.md)


