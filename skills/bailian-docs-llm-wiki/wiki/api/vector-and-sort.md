# vector and sort

`vector and sort` 是百炼平台提供的向量嵌入与排序（Rerank）能力集合，用于文本语义向量化、跨模态向量化及检索后重排序。该能力通过统一 API 接口封装，支持多种模型选型和细粒度参数控制，适用于搜索、推荐、RAG 等场景。所有服务均按调用次数计费，需通过 `POST /v1/embeddings` 或 `/v1/rerank` 调用。

## 支持的模型/功能

- **文本向量化**：支持 `text-embedding-v1`、`text-embedding-v2` 等通用文本嵌入模型，输出 1024 维稠密向量；详情见 [向量与排序](../../raw/model-api-reference/vector-and-sort.md)。  
- **多模态向量化**：支持图像-文本联合嵌入（如 `multimodal-embedding-v1`），可对图片 URL 或 base64 编码图像生成向量；该能力在 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 的子文档中有完整说明。  
- **排序（Rerank）**：提供 `rerank-v1`、`rerank-v2` 等专用重排序模型，接受 query + 文档列表输入，返回带 score 的排序结果；其接口定义与行为规范详见 [向量与排序](../../raw/model-api-reference/vector-and-sort.md)。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型 ID，如 `"text-embedding-v1"`、`"rerank-v2"`；必须与请求路径匹配（`/v1/embeddings` 仅支持 embedding 模型） |
| `input` | string \| string[] \| object[] | 是 | 向量化时为文本或图像对象数组；Rerank 时为 `{query: string, documents: string[]}` 对象 |
| `encoding_format` | string | 否 | 可选 `"float"`（默认）或 `"base64"`；影响向量返回格式 |
| `top_k` | integer | 否（Rerank 必填） | Rerank 模型返回的最高分文档数，范围 1–100 |

> **注意**：`text-embedding-v2` 默认返回 2048 维向量，而 `text-embedding-v1` 为 1024 维；若业务依赖固定维度，请显式指定模型版本，避免因平台默认值变更导致下游解析失败。

## 使用方式

1. **文本向量化请求示例**：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/embeddings \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "text-embedding-v1",
           "input": ["今天天气很好", "适合出门散步"]
         }'
   ```

2. **Rerank 请求示例**：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/rerank \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "rerank-v2",
           "input": {
             "query": "人工智能开源框架",
             "documents": ["PyTorch 官方教程", "TensorFlow 模型部署指南", "LangChain 快速入门"]
           },
           "top_k": 3
         }'
   ```

## 限制和注意事项

- 单次 `input` 最多支持 128 个文本项（向量化）或 100 个文档（Rerank）；超出将返回 `400 Bad Request`。
- 多模态向量化暂不支持批量图像输入，每次请求仅接受单张图像；具体约束参见 [向量与排序](../../raw/model-api-reference/vector-and-sort.md)。
- 所有向量服务响应中 `data[i].embedding` 字段为浮点数组（`encoding_format="float"` 时），长度由模型决定，不可硬编码假设为 1024。
- Rerank 模型对 `query` 长度敏感：超过 512 token 将被截断，且不返回警告；建议客户端预处理。

## 来源文档

- [向量与排序](../../raw/model-api-reference/vector-and-sort.md)


