# 向量嵌入

向量嵌入（Vector Embedding）是将原始非结构化数据（如文本、图像、音频等）映射到高维连续语义空间中的稠密实数向量的过程。该向量保留了原始数据的语义特征，使得语义相似的内容在向量空间中距离更近，从而支持相似性计算、检索与聚类等下游任务。

## 在百炼平台的不同场景中，这个概念如何使用

向量嵌入是百炼平台多项核心能力的底层基础，在以下场景中被统一抽象并深度集成：

- **语义搜索与 RAG**：知识库（Knowledge Base）自动对上传文档进行分块与向量化，构建可检索的向量索引；用户查询经同一嵌入模型编码后，通过余弦相似度完成初步召回。
- **[长期记忆](long-term-memory.md)管理**：记忆库（Memory Library）默认使用 `text-embedding-v1` 对 `content` 字段生成向量，支持按语义+元数据混合检索，实现多轮对话中上下文信息的持久化复用。
- **框架集成开发**：LlamaIndex 和 Spring AI Alibaba 等框架通过 `DashScopeEmbedding` 组件调用百炼向量 API，开发者可自由选择 `text-embedding-v3`、`qwen3.7-text-embedding` 等模型，用于本地构建索引或增强云端检索流程。
- **多模态理解**：`qwen3-vl-embedding` 和 `tongyi-embedding-vision-plus-2026-03-06` 支持文本、图像、视频及其组合输入，可输出独立模态向量或启用 `enable_fusion=true` 生成跨模态融合向量，统一表征异构语义。
- **智能体与工作流**：LLM Application 中的知识库节点、文档解析节点及多模态生成节点均隐式依赖向量嵌入能力——无论是底库预处理还是实时查询编码，均由平台托管的嵌入服务完成，开发者无需自行部署向量模型。

> ⚠️ 注意：知识库和记忆库虽都使用向量嵌入，但策略不同——知识库支持自定义嵌入模型（通过 API 或 SDK 显式指定），而记忆库当前**强制绑定 `text-embedding-v1`，不可更换**，如需其他模型需联系技术支持。

## 关键参数和配置

| 参数 | 适用场景 | 说明 | 是否必选 |
|--------|-----------|------|----------|
| `model` | 所有向量 API 调用 | 指定嵌入模型名称，例如 `"text-embedding-v4"`、`"qwen3-vl-embedding"`；不同模型支持的输入类型与维度不同 | 是 |
| `input` | 同步向量 API | 接受字符串、字符串数组或文件 URL（如 PDF/IMG 的公网可访问链接）；单次最多 20 条文本 | 是 |
| `dimensions` | `text-embedding-v3/v4`、`qwen3.7-text-embedding`、`qwen3-vl-embedding` 等 | 指定向量输出维度（如 `1024`, `2048`），影响存储开销与检索精度；不传则使用模型默认维度 | 否 |
| `text_type` | 批处理 API（`text-embedding-async-v2`） | 设为 `"query"`（查询文本）或 `"document"`（底库文本），影响归一化与表征策略；RAG 场景建议显式区分 | 否（默认 `"document"`） |
| `enable_fusion` | 多模态嵌入（`qwen3-vl-embedding`） | 设为 `true` 时，对多模态输入（如图文对）生成**单一融合向量**；设为 `false`（默认）则返回多个独立向量 | 否（仅融合场景需设） |

- **批量处理推荐**：超大批量（>1000 条）向量化请优先使用 `text-embedding-async-v2` 批处理接口，支持最高 100,000 行/任务，采用异步提交 + 轮询结果模式。
- **OpenAI 兼容调用**：同步向量 API 支持 OpenAI 格式 SDK（如 `client.embeddings.create(input=..., model=...)`），降低迁移成本。

## 面向开发者，简洁实用

- ✅ **选型建议**：
  - 通用文本：优先用 `text-embedding-v4`（最新版，CMTEB 检索得分高）或 `qwen3.7-text-embedding`（Qwen 3.7 生态对齐）；
  - 多模态：用 `qwen3-vl-embedding`（支持图文视频，推荐开启 `enable_fusion` 做跨模态匹配）；
  - 高吞吐离线：用 `text-embedding-async-v2` + `text_type` 区分 query/document；
  - 旧项目兼容：`text-embedding-v2` 仍可用，但不支持 `dimensions`，且性能弱于 v3/v4。

- ✅ **调试技巧**：
  - 若检索效果差，先检查 `score_threshold`（知识库默认 `0.3`）是否过严，或尝试调低；
  - 多模态输入务必确认文件 URL 可公开访问且格式受支持（如 JPG/PNG/MP4）；
  - 使用 `dimensions` 时，确保向量数据库（如 Milvus、PGVector）已按对应维度建索引。

- ✅ **避坑提醒**：
  - 记忆库不支持自定义嵌入模型 —— 不要尝试在 `upsert` 请求中传 `model` 参数，无效；
  - `gte-rerank` 系列已下线，新项目勿再使用；排序阶段请用 `qwen3-rerank` 替代；
  - 控制台创建的知识库默认走百炼托管向量化流程，如需自定义切分或嵌入，请用 LlamaIndex + `DashScopeEmbedding` 本地构建。

如需快速验证，可直接调用同步 API：
```bash
curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/embeddings/text-embedding-v4" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "model": "text-embedding-v4",
        "input": ["今天天气真好", "阳光明媚适合出游"]
      }'
```

## 关联主题页

- [vector and sort](../api/vector-and-sort.md)
- [knowledge base](../guides/knowledge-base.md)
- [memory library overview](../guides/memory-library-overview.md)
- [frameworks](../api/frameworks.md)
- [llm application](../guides/llm-application.md)


