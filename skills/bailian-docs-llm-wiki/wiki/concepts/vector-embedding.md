# 向量嵌入

向量嵌入（Vector Embedding）是将原始非结构化数据（如文本、图像、视频等）映射到高维连续语义空间中的稠密数值向量的过程。每个向量在该空间中表征其语义本质，使得语义相似的内容在向量空间中距离更近，从而支持检索、聚类、排序等下游任务。

## 在百炼平台的不同场景中，这个概念如何使用

- **RAG 知识库构建**：知识库创建时默认调用 `text-embedding-v4`（或用户指定模型）对文档切片（chunk）进行批量向量化，生成的向量存入向量索引，支撑后续语义检索。向量质量直接影响召回准确率与问答效果。
- **API 层向量服务**：通过 `/compatible-mode/v1/embeddings`（同步）或 `/api/v1/services/embeddings/text-embedding/...`（异步批处理）接口，开发者可自主调用通用文本向量模型（如 `qwen3.7-text-embedding`、`text-embedding-v4`）或多模态向量模型（如 `qwen3-vl-embedding`），实现灵活的向量化逻辑。
- **多模态融合检索**：使用 `qwen3-vl-embedding` 等模型时，可通过 `enable_fusion=true` 将单条输入中的 text + image + video 融合为一个联合向量；或分别生成独立向量，用于跨模态对齐与混合检索。
- **框架集成**：LlamaIndex、Spring AI Alibaba 等框架通过 `DashScopeEmbedding` 组件封装百炼向量能力，自动适配模型选型、参数传递与错误重试，降低 RAG 工程门槛。
- **检索增强链路协同**：向量嵌入与 Rerank 模型（如 `qwen3-rerank`）构成标准 RAG 两阶段 pipeline——先用向量召回初筛结果，再用重排模型精细化打分，二者共享同一语义空间对齐前提。

## 关键参数和配置

| 参数 | 适用场景 | 说明 | 推荐值 |
|------|----------|------|--------|
| `text_type` | 文本向量（异步批处理） | 区分底库文档（`document`）与查询语句（`query`）的向量化策略，影响向量方向性。必须显式设置以保障检索一致性。 | `document`（建库）、`query`（检索） |
| `dimension` | 同步文本向量模型 | 指定输出向量维度（如 `2560`、`1024`、`128`）。维度越低，存储与计算开销越小，但可能损失语义区分度。 | `1024`（平衡精度与性能）或按业务需求选择 |
| `enable_fusion` | 多模态向量模型（如 `qwen3-vl-embedding`） | `true` 表示启用多模态融合向量（单输入 → 单向量）；`false` 或不传则生成各模态独立向量。 | `true`（需联合语义）或 `false`（需模态解耦） |
| `model` | 所有向量调用 | 必填。推荐使用最新稳定版：文本向量选 `text-embedding-v4` 或 `qwen3.7-text-embedding`；多模态选 `qwen3-vl-embedding`。旧版（如 `text-embedding-async-v1`）已过时，禁用。 | `"text-embedding-v4"` / `"qwen3-vl-embedding"` |

> ⚠️ 注意：  
> - 同步接口单次最多 20 行文本（`qwen3.7-text-embedding`），每行 [Token](token.md) 数 ≤ 8192；异步批处理支持单次 100,000 行、文件 ≤ 200MB。  
> - 所有向量模型均要求输入文本经 UTF-8 编码，避免控制字符与非法 Unicode。  
> - 地域限制：向量服务仅在北京（`cn-beijing.maas.aliyuncs.com`）和新加坡（`ap-southeast-1.maas.aliyuncs.com`）地域可用。

## 面向开发者，简洁实用

- ✅ **首选模型**：生产环境统一使用 `text-embedding-v4`（文本）或 `qwen3-vl-embedding`（多模态），二者支持最广语种、最高维度灵活性与最佳 CMTEB 检索得分。
- ✅ **必设参数**：异步批处理务必传 `text_type`；多模态融合务必确认 `enable_fusion` 值；同步调用建议显式指定 `dimension` 以规避模型默认变化风险。
- ✅ **调试技巧**：用 Playground 的「知识检索」模式对比不同 `text_type` 下的向量相似度；用 SDK 的 `BatchTextEmbedding.async_call()` 自动处理轮询，避免手动实现状态机。
- ❌ **禁止行为**：不要混用 `document`/`query` 向量做相似度计算；不要在未验证 `enable_fusion` 兼容性时切换多模态模型；不要在非北京/新加坡地域发起向量请求。
- 📦 **快速起步代码（Python SDK）**：
  ```python
  from dashscope import TextEmbedding
  
  # 同步文本向量（单条）
  resp = TextEmbedding.call(
      model='text-embedding-v4',
      input='什么是向量嵌入？',
      text_type='query',  # 关键！
      dimension=1024
  )
  vector = resp.output.embeddings[0].embedding  # list[float]
  
  # 异步批处理（文件）
  from dashscope import BatchTextEmbedding
  task = BatchTextEmbedding.async_call(
      model='text-embedding-v4',
      file_path='./docs.txt',
      text_type='document'
  )
  result = task.wait()  # 自动轮询
  ```

## 关联主题页

- [vector and sort](../api/vector-and-sort.md)
- [rag api](../api/rag-api.md)
- [knowledge base](../guides/knowledge-base.md)
- [frameworks](../api/frameworks.md)
- [qwen mt translation models](../api/qwen-mt-translation-models.md)


