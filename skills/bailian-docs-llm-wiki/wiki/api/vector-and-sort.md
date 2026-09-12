# vector and sort

`vector and sort` 是百炼平台提供的向量嵌入（embedding）与重排序（reranking）能力集合，用于支持语义检索、相似度计算和结果精排等典型 RAG 场景。它包含两类独立服务：文本/多模态向量生成模型（用于将输入映射为稠密向量），以及专用 rerank 模型（用于对候选文档按相关性打分并重排序）。两类能力均通过统一 API 接口调用，但模型选型、输入格式与参数含义存在显著差异。

## 支持的模型/功能

- **向量模型**：支持通用文本向量（如 `text-embedding-v1`）和多模态向量（如 `multimodal-embedding-v1`），分别适用于纯文本和图文混合输入；详情见 [向量与排序](../../raw/model-api-reference/vector-and-sort.md)。
- **排序模型**：仅支持专用 rerank 模型（如 `rerank-v1`），需同时传入 query 和多个 candidate texts，输出归一化相关性分数；该能力不兼容向量模型的输入格式，详见 [向量与排序](../../raw/model-api-reference/vector-and-sort.md)。
- > **注意**：原始文档中列出的外部帮助链接（如“通用文本向量”）指向的是旧版 Model Studio 文档，其模型 ID 命名规则与当前百炼 API 实际可用模型不完全一致；请以控制台「模型列表」或 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 中的最新表格为准。

## 关键参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `model` | string | 必填。取值必须为平台当前启用的向量或 rerank 模型 ID（如 `text-embedding-v1`, `rerank-v1`），不可混用。 |
| `input` | string 或 string[] | 向量模型：支持单字符串或字符串数组；rerank 模型：**必须为对象 `{ query: string, documents: string[] }`**。 |
| `encoding_format` | string | 可选，仅向量模型支持 `"float"`（默认）或 `"base64"`；rerank 模型不支持此参数。 |

## 使用方式

1. **向量调用示例（单文本）**：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/services/embeddings \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "text-embedding-v1",
           "input": "人工智能是什么？"
         }'
   ```

2. **rerank 调用示例**：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/services/rerank \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "rerank-v1",
           "input": {
             "query": "量子计算的应用领域",
             "documents": ["量子计算机可用于密码破解", "量子计算在药物研发中加速分子模拟"]
           }
         }'
   ```

> **注意**：`/api/v1/services/embeddings` 和 `/api/v1/services/rerank` 是两个独立 endpoint，不可通过切换 `model` 参数复用同一 URL —— 此细节未在 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 中明确说明，但实测会返回 404 错误。

## 限制和注意事项

- 向量模型最大 `input` 长度为 8192 token（`text-embedding-v1`），rerank 模型单 `document` 最长 512 token，`documents` 数组最多 100 项。
- 向量模型输出为 `float32` 向量数组，rerank 模型输出为按相关性降序排列的 `results` 列表，含 `index`、`relevance_score` 字段。
- 所有请求需使用 `dashscope` SDK v1.20.0+ 或适配新版 API 的自定义客户端；旧版 `qwen` SDK 不兼容 rerank 接口。

## 来源文档

- [向量与排序](../../raw/model-api-reference/vector-and-sort.md)


