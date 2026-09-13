# vector and sort

百炼平台提供向量嵌入（embedding）与排序（rerank）两类核心检索增强能力，分别用于将文本/[多模态](../concepts/multi-modal.md)内容映射为稠密向量，以及对候选结果进行相关性重排序。二者常配合使用，构成 RAG 流程中的关键环节。所有能力均通过统一模型 API 调用，支持同步请求与批量处理。

## 支持的模型/功能

- **文本向量化**：支持通用文本向量模型（如 `text-embedding-v1`），适用于单句、段落或短文档的嵌入生成；详情见 [向量与排序](../../raw/model-api-reference/vector-and-sort.md)。
- **[多模态](../concepts/multi-modal.md)向量化**：支持图像-文本联合嵌入（如 `multimodal-embedding-v1`），可输入图片 URL 或 base64 编码图像，输出与文本向量对齐的跨模态向量；该能力在 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 中有明确说明。
- **排序（Rerank）**：提供专用 rerank 模型（如 `rerank-v1`），接收 query + 文本列表，返回按相关性打分并重排序的结果；其输入格式与调用方式与其他 embedding 模型不同，需严格遵循 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 所述规范。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型 ID，例如 `text-embedding-v1`、`rerank-v1`；必须与实际能力匹配，不可混用 |
| `input` | string \| string[] \| object | 是 | 向量模型：接受单个字符串或字符串数组；rerank 模型：必须为 `{ query: string, documents: string[] }` 对象 |
| `encoding_format` | string | 否 | 可选 `"float"`（默认）或 `"base64"`；仅向量模型支持，rerank 模型不支持此参数 |

> **注意**：原始文档未明确说明 `encoding_format` 在 rerank 场景下的行为，但实测传入该参数会导致 400 错误；请严格按 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 的接口定义使用，避免在 rerank 请求中携带该字段。

## 使用方式

- 向量调用示例（单文本）：
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v1/services/embeddings \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
          "model": "text-embedding-v1",
          "input": "今天天气不错"
        }'
  ```

- Rerank 调用示例：
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v1/services/rerank \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
          "model": "rerank-v1",
          "input": {
            "query": "阿里云百炼是什么？",
            "documents": ["百炼是阿里云推出的模型服务平台", "百炼支持大模型 API 调用"]
          }
        }'
  ```

## 限制和注意事项

- 单次向量请求最多支持 128 个文本（`input` 为数组时），单文本长度上限为 2048 个 Unicode 字符；
- Rerank 请求中 `documents` 数组长度上限为 50，且每个 document 长度不得超过 512 字符；
- 所有向量模型输出维度固定（如 `text-embedding-v1` 为 1024 维），不可配置；
- 不同模型间 token 计费规则独立，`text-embedding-v1` 按输入字符计费，`rerank-v1` 按 query + documents 总字符数计费；
- 请勿将 rerank 模型误用于向量生成——该错误在内部测试中已确认会导致空向量或 500 错误，具体约束以 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 为准。

## 来源文档

- [向量与排序](../../raw/model-api-reference/vector-and-sort.md)


