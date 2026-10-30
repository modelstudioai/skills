# 向量嵌入

向量嵌入（Embedding）是将文本、图像、音频等非结构化数据映射到低维稠密实数向量空间的过程，使语义相近的内容在向量空间中距离更近。该表示形式是百炼平台实现语义检索、RAG、跨模态理解与聚类分析等高级AI能力的底层基础。

## 在百炼平台的不同场景中，这个概念如何使用

- **RAG 知识库构建**：创建知识库时通过 `embeddingModelName`（如 `text-embedding-v4`）或 `multimodalEmbeddingModelName`（如 `qwen3-vl-embedding`）指定嵌入模型，平台自动对导入文档进行切片并生成向量，存入向量数据库供后续语义检索使用。
- **独立向量服务调用**：通过 `/api/v1/services/embeddings` 或 [OpenAI 兼容接口](openai-compatible-interface.md)（如 `/compatible-mode/v1/embeddings`）直接调用文本或多模态嵌入模型，适用于自定义检索流程、数据预处理、相似度计算等场景。
- **框架集成开发**：LlamaIndex 和 Spring AI Alibaba 框架通过 `AlibabaEmbeddingClient` 或 `QwenEmbedding` 组件透明接入百炼嵌入服务，开发者只需配置 `QWEN_MODEL_NAME`（如 `"qwen3.7-text-embedding"`），无需处理协议细节。
- **多模态联合建模**：在视觉问答、图文检索等场景中，`qwen3-vl-embedding` 支持对文本+图像混合输入生成统一语义向量（启用 `enable_fusion`）或分别生成独立向量，为跨模态对齐提供基础表征。

> ⚠️ 注意：`tongyi-embedding-vision-plus` 系列仅支持独立向量（不支持融合），而 `qwen2.5-vl-embedding` 仅支持融合向量——二者能力互斥，选型需严格匹配业务需求。

## 关键参数和配置

| 参数 | 说明 | 常用值示例 | 是否必填 |
|------|------|------------|----------|
| `model` | 嵌入模型名称 | `"text-embedding-v4"`, `"qwen3-vl-embedding"` | ✅ |
| `input` | 输入内容 | 文本：`"hello world"` 或 `["doc1", "doc2"]`；多模态：`{"contents": [{"type": "text", "text": "..."}, {"type": "image_url", "image_url": {"url": "..."}}]}` | ✅ |
| `dimensions` | 输出向量维度（部分模型支持） | `1024`, `2048` | ❌（默认由模型决定） |
| `encoding_format` | 返回格式（同步接口） | `"float"`（默认）、`"base64"`（新网关长请求可能降级为 float） | ❌ |
| `enable_fusion` | 多模态模型是否融合所有输入为单向量 | `true` / `false`（仅 `qwen3-vl-embedding` 支持） | ❌（默认 `false`） |
| `text_type` | 批处理接口中区分文档/查询用途（用于非对称检索优化） | `"document"`（底库）、`"query"`（检索词） | ❌（默认 `"document"`） |

## 面向开发者，简洁实用

- ✅ **优先使用同步接口**：小批量（≤100 条）、低延迟场景（如实时问答）推荐调用 `/api/v1/services/embeddings` 或 OpenAI 兼容 endpoint。
- ✅ **大批量请用异步批处理**：超万级文本向量化（如全量知识库初始化）应选用 `text-embedding-async-v2`，提交后通过任务 ID 轮询下载结果。
- ✅ **多模态务必校验能力边界**：调用 `qwen3-vl-embedding` 前确认输入是否含图像/视频，并根据是否需要“图文联合向量”设置 `enable_fusion`；避免混用 `tongyi-embedding-vision-plus`（仅独立向量）与 `qwen2.5-vl-embedding`（仅融合向量）。
- ✅ **框架开发建议**：LlamaIndex 用户安装 `llama-index-llms-qwen` 并设置 `QWEN_API_KEY` + `QWEN_MODEL_NAME` 即可开箱即用；Spring AI 用户在 `application.yml` 中配置 `spring.ai.alibaba.embedding.model=qwen3.7-text-embedding`。
- ❌ **避免踩坑**：`gte-rerank` 已下线，请勿在 RAG Agent 配置中使用；`visual_document_qa` 场景控制台已废弃，生产环境请改用标准 RAG + `qwen3-vl-embedding` 方案。

## 关联主题页

- [rag api](../api/rag-api.md)
- [vector and sort](../api/vector-and-sort.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [model data overview](../guides/model-data-overview.md)
- [frameworks](../api/frameworks.md)


