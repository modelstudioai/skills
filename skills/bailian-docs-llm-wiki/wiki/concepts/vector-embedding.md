# 向量嵌入

向量嵌入（Vector Embedding）是将原始非结构化数据（如文本、图像、视频等）映射到高维连续语义空间中的稠密数值向量的过程。该向量保留了原始内容的语义特征与相对关系，使得语义相似的内容在向量空间中距离更近，从而支撑检索、聚类、去重、RAG 等下游任务。

## 在百炼平台的不同场景中，这个概念如何使用

- **RAG（知识库）场景**：向量嵌入是知识库构建的核心前置步骤。文档切片后，由指定嵌入模型（如 `text-embedding-v4` 或 `qwen3-vl-embedding`）生成向量并存入向量数据库；用户查询时，查询文本也被嵌入为向量，通过向量相似度（如余弦相似度）完成语义召回。多模态知识库（如 `image` 或 `multimedia` 类型）必须配置对应多模态嵌入模型。
  
- **向量检索服务（Vector API）**：作为独立能力提供同步/异步接口，支持开发者自主控制嵌入流程。同步接口适用于低延迟实时场景（如对话中动态嵌入用户输入），异步批处理（`text-embedding-async-v2`）适用于离线构建大规模底库向量。

- **框架集成场景**：LlamaIndex、LangChain、Spring AI 等主流框架通过 `BailianEmbeddings` 或 `AlibabaAIClient` 封装调用百炼嵌入模型，开发者无需感知底层协议，只需传入文本或 `contents` 即可获取向量，无缝接入 RAG pipeline。

- **多模态统一表征**：通过 `qwen3-vl-embedding`、`tongyi-embedding-vision-plus-2026-03-06` 等模型，支持文本、图像、视频混合输入，并可选择融合为单向量（`enable_fusion=true`）或生成各模态独立向量，服务于跨模态搜索与理解任务。

- **CLI 工具链支持**：`bl batch` 命令支持批量文本向量化（需配合 `--model text-embedding-*`），适用于数据预处理、评估集构建等工程化任务；所有文件类参数（如 `--file-url`）均自动上传并触发嵌入流程。

## 关键参数和配置

| 参数 | 适用模型/场景 | 说明 |
|------|----------------|------|
| `model` | 全部 | 必填。指定嵌入模型 ID，例如 `qwen3.7-text-embedding`、`text-embedding-v4`、`qwen3-vl-embedding`。不支持别名，未指定将报错。 |
| `input` | 同步接口、[OpenAI 兼容接口](openai-compatible-interface.md) | 支持字符串、字符串列表（最大 2048 tokens 总长）、或符合 OpenAI 兼容格式的 `contents` 数组（含 `text`/`image`/`video` 字段）。 |
| `dimensions` | 多数文本模型（如 `qwen3.7-text-embedding`） | 可选。指定输出向量维度（如 `1024`、`2048`），影响精度与存储开销；若不指定，使用模型默认维度。 |
| `text_type` | 异步模型（如 `text-embedding-async-v2`） | 必填。设为 `"document"`（用于知识库底库）或 `"query"`（用于用户检索），不同类型经模型优化，对检索效果影响显著。 |
| `enable_fusion` | `qwen3-vl-embedding` | 布尔值。设为 `true` 时，将 `contents` 中所有模态输入融合为一个联合向量；设为 `false` 则返回各模态独立向量。 |
| `base_url` | 框架/SDK 调用 | 必须显式配置为 `https://dashscope.aliyuncs.com/compatible-mode/v1`（OpenAI 兼容）或 `https://dashscope.aliyuncs.com/api/v1`（原生接口）。 |

> ⚠️ 注意：`text-embedding-async-v1` 已不推荐使用；`multimodal-embedding-v1` 不支持 `dimension` 参数；`instruct`、`fps` 等参数属于排序（Rerank）模型，**不适用于向量嵌入接口**。

## 面向开发者，简洁实用

- ✅ **首选同步调用**：实时性要求高时，直接使用 OpenAI 兼容 `/v1/embeddings` 接口或 DashScope SDK：
  ```python
  from openai import OpenAI
  client = OpenAI(api_key="sk-xxx", base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
  resp = client.embeddings.create(model="qwen3.7-text-embedding", input=["你好世界", "Hello world"])
  vectors = [item.embedding for item in resp.data]
  ```

- ✅ **批量离线处理**：千万级文档请用异步批处理，上传 CSV/JSONL 文件 URL，轮询 `task_id` 获取结果 ZIP 下载链接（支持 10 万行/任务）。

- ✅ **多模态必读**：图像/视频嵌入必须使用 `qwen3-vl-embedding` 或 `tongyi-embedding-vision-plus-2026-03-06`；输入需为 `contents=[{"image": "base64..."}, {"text": "描述"}]` 格式，融合模式按模型要求启用。

- ✅ **RAG 开发者**：在 Knowledge API 创建知识库时，通过 `embeddingModelName` 显式指定嵌入模型；避免依赖默认值，确保线上环境一致性。

- ❌ **不要混淆**：向量嵌入（embedding）≠ 排序（rerank）≠ 生成（chat/completions）。三者模型、接口、参数完全隔离，不可混用。

## 关联主题页

- [vector and sort](../api/vector-and-sort.md)
- [capabilities](../guides/capabilities.md)
- [rag api](../api/rag-api.md)
- [frameworks](../api/frameworks.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


