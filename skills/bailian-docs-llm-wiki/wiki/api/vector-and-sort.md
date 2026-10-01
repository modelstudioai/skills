# vector and sort

`vector and sort` 是百炼平台提供的向量嵌入与重排序（Rerank）能力集合，用于支持语义检索、相似度计算和结果精排等典型 RAG 场景。该能力涵盖文本向量生成、多模态向量生成及跨文档相关性重排序三类核心模型。所有接口均通过统一的 `/v1/embeddings` 和 `/v1/rerank` 路径调用，需配合对应模型名称使用。

## 支持的模型/功能

- **文本向量模型**：支持通用文本嵌入（如 `text-embedding-v1`），适用于单语言（中文为主）短文本编码；详情见 [向量与排序](../../raw/model-api-reference/vector-and-sort.md)。
- **多模态向量模型**：支持图文联合嵌入（如 `multimodal-embedding-v1`），输入可为文本+图像 base64 或纯文本，输出统一 1024 维向量；该能力在 [向量与排序](../../raw/model-api-reference/vector-and-sort.md) 中有完整说明。
- **排序模型（Rerank）**：支持查询-文档对的相关性打分（如 `rerank-v1`），仅接受 query + 文档列表（最多 100 篇），不支持流式响应；具体输入格式参见 [向量与排序](../../raw/model-api-reference/vector-and-sort.md)。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型 ID，如 `text-embedding-v1`、`rerank-v1`；必须与接口路径匹配（`/v1/embeddings` 仅支持 embedding 类模型） |
| `input` | string \| string[] \| object[] | 是 | embedding 接口：字符串或字符串数组；rerank 接口：`{ "query": "...", "documents": ["...", "..."] }` 对象 |
| `encoding_format` | string | 否 | 可选 `"float"`（默认）或 `"base64"`；仅 embedding 接口支持 |

> **注意**：原始文档中 `multimodal-embedding-v1` 的 `input` 示例显示支持 `{"text": "...", "image_url": "..."}` 格式，但当前 API 实际仅接受 `{"text": "...", "image": "base64..."}` —— 请以 [通用文本向量](../../raw/model-api-reference/vector-and-sort/general-text-vector.md) 中的最新请求体结构为准。

## 使用方式

1. **获取向量**（文本）：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/embeddings \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "text-embedding-v1",
           "input": ["今天天气如何？", "北京明天会下雨吗？"]
         }'
   ```

2. **多模态向量**（需 base64 图像）：
   ```json
   {
     "model": "multimodal-embedding-v1",
     "input": {
       "text": "一只橘猫坐在窗台上",
       "image": "/9j/4AAQSkZJRgABAQAAA..."
     }
   }
   ```

3. **重排序**：
   ```json
   {
     "model": "rerank-v1",
     "input": {
       "query": "杭州最好的龙井茶产地是哪里？",
       "documents": [
         "西湖区是龙井茶的核心产区。",
         "安徽黄山也产优质绿茶。",
         "龙井茶原产于浙江杭州西湖一带。"
       ]
     }
   }
   ```

## 限制和注意事项

- 单次 embedding 请求最多支持 100 个文本（`input` 为数组时），总 token 数不超过 8192；
- rerank 接口 `documents` 最多 100 篇，每篇长度建议 ≤ 512 tokens，超长将被截断；
- 所有向量模型返回的 `embedding` 字段为 float 数组（非 base64），除非显式指定 `encoding_format: "base64"`；
- 多模态向量模型暂不支持批量图像输入，每次仅处理单张图像 + 文本组合；
- 模型版本升级可能导致向量空间不兼容，请在生产环境固定 `model` 版本（如 `text-embedding-v1` 而非 `text-embedding` 别名）。

## 来源文档

- [向量与排序](../../raw/model-api-reference/vector-and-sort.md)


