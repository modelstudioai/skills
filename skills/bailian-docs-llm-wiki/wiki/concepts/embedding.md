# 向量化

向量化（Embedding）是将文本、图片、视频等非结构化数据通过模型映射为高维数值向量的过程。在百炼平台中，向量化是语义检索、推荐、聚类、分类与 RAG 检索的核心基础——向量模型将不同模态的数据编码到同一语义空间，使机器能够基于向量距离衡量语义相似度。

## 在百炼平台中的使用场景

### 向量与排序 API

百炼提供通用文本向量和[多模态](multimodal.md)向量两类接口，用于将原始数据转为向量：

- **通用文本向量（同步）**：支持 `qwen3.7-text-embedding`、`text-embedding-v4/v3/v2/v1`，将字符串或文件实时转为向量。提供 [OpenAI 兼容接口](openai-compatible-interface.md)，可用 OpenAI SDK 直连。
- **通用文本向量（批处理）**：面向大规模离线场景，仅支持异步模式，通过文件 URL 输入，支持 `text-embedding-async-v2/v1`。单文件最多 100,000 行、200MB。
- **[多模态](multimodal.md)向量**：将文本、图片、视频编码到同一语义空间，支持跨模态检索。模型包括 `qwen3-vl-embedding`、`qwen2.5-vl-embedding`、`multimodal-embedding-v1` 等。

### 知识库索引与检索

知识库在导入文档时自动调用向量模型对文本切片进行向量化，构建语义索引。检索阶段，用户查询同样经过向量化后与索引向量做相似度匹配，完成语义召回。

- **文档搜索**：支持 `text-embedding-v4` 和 `text-embedding-v3`（512 维）。
- **视觉理解（富文本文档）**：自动切换为 `qwen3-vl-embedding`，对 PDF、图片等进行视觉级理解和索引，保留版面信息。
- **图片问答**：使用 `multimodal-embedding-v1`（1024 维）。

### 知识检索与问答 API

知识检索接口（`POST /api/v1/indices/knowledge/search`）跨多个知识库执行联合语义检索，底层依赖向量化的索引与查询。知识问答接口则在此基础上自动完成规划、检索、生成全流程。

## 关键参数与配置

### 维度（dimensions）

仅部分模型支持自定义输出维度：

| 模型 | 支持维度 | 默认 |
| --- | --- | --- |
| `qwen3.7-text-embedding` | 2560/2048/1536/1024/768/512/256/128/64 | — |
| `text-embedding-v4` | 2048/1536/1024/768/512/256/128/64 | 1024 |
| `text-embedding-v3` | 1024/768/512/256/128/64 | 1024 |
| `text-embedding-v1/v2` | 固定 1536（不可调） | 1536 |

> 知识库场景下 `text-embedding-v3/v4` 统一使用 512 维。

### 输入上限

| 模型 | 单条最大 Token | 列表/文件最大条数 |
| --- | --- | --- |
| `qwen3.7-text-embedding` | 128,000 | 20 |
| `text-embedding-v3/v4` | 8,192 | 10 |
| `text-embedding-v1/v2` | 2,048 | 25 |

### text_type（批处理）

批处理接口的 `parameters.text_type` 可选 `document`（默认）或 `query`。检索类非对称任务建议区分 query 与 document，以提升检索效果。

### encoding_format

同步接口可选 `encoding_format`，当前仅支持 `float`。

## 使用建议

- **检索场景**优先选 `text-embedding-v4` 或 `qwen3.7-text-embedding`，维度更高、效果更好。
- **跨模态场景**（图文检索）使用 `qwen3-vl-embedding` 或 `multimodal-embedding-v1`。
- **大规模离线**用批处理接口，注意请求头须带 `X-DashScope-Async: enable`，否则会报错。
- **知识库**中向量模型由知识库类型决定，创建时选定后不可更改，务必提前规划。
- 向量检索召回后通常配合 rerank 模型（如 `qwen3-rerank`）做二次精排，进一步提升相关性。

## 关联主题页

- [vector and sort](../api/vector-and-sort.md)
- [knowledge base](../guides/knowledge-base.md)
- [knowledge](../api/knowledge.md)


