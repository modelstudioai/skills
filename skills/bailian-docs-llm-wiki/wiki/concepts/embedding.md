# 向量嵌入

向量嵌入（Embedding）是将文本、图像、音频、视频等非结构化数据映射到高维稠密实数向量空间的数学表示方法，使语义相近的内容在向量空间中距离更近（如余弦相似度更高），从而支撑语义检索、聚类、去重与跨模态对齐等任务。

## 在百炼平台的不同场景中，这个概念如何使用

- **知识库（RAG）核心底座**：知识库构建时，所有文档切片（PDF/Word/Markdown）、表格行、图片描述、音视频转写文本均通过嵌入模型统一向量化，并存入向量索引。检索阶段，用户查询也被实时嵌入，系统通过向量相似度召回最相关的片段。
- **独立向量服务**：开发者可直接调用 `/api/v1/services/embeddings/...` 接口，对任意文本或图文混合输入生成向量，用于自定义检索系统、语义去重、内容推荐或冷启动特征工程。
- **多模态统一表征**：`qwen3-vl-embedding` 等模型支持文本、图像、视频输入融合为同一语义空间的单一向量（启用 `enable_fusion=true`），实现“以图搜文”“以文搜图”“视频片段语义定位”等跨模态能力。
- **框架集成基础能力**：LlamaIndex、Spring AI Alibaba 等框架通过 `BaiLianEmbedding` 组件复用百炼嵌入服务，无需自行部署模型，即可快速构建 RAG 应用。
- **智能体（Agent）上下文理解**：新版 Agent 2.0 在工具选择、记忆检索、长期状态管理中，依赖嵌入向量对历史对话、工具描述、知识片段进行语义匹配与动态关联。

## 关键参数和配置

| 参数 | 适用模型 | 说明 | 开发建议 |
|------|----------|------|----------|
| `dimensions` | `qwen3.7-text-embedding`, `text-embedding-v4`, `qwen3-vl-embedding` 等 | 指定向量维度（如 1024、2048、2560）。不同模型支持值不同；`tongyi-embedding-vision-plus` 固定为 1152 维，不支持该参数。 | 优先使用默认维度（如 `text-embedding-v4` 默认 1024），除非业务明确需降维压缩（注意精度损失）。 |
| `encoding_format` | 同步文本向量（`text-embedding-*`） | 取值 `float`（默认）或 `base64`；`base64` 可节省约 30% 带宽，但需客户端解码。 | 小批量调试用 `float`；生产大批量调用且网络受限时，可显式设为 `base64` 并做好解码容错。 |
| `text_type` | 异步文本向量（`text-embedding-async-*`） | 必填，取值 `query` 或 `document`；模型据此优化非对称语义建模（如 query 更关注关键词，document 更关注上下文完整性）。 | **必须区分**：查询文本传 `"text_type": "query"`，知识库文档传 `"text_type": "document"`，否则影响检索精度。 |
| `enable_fusion` | `qwen3-vl-embedding` | `true` 启用多模态融合向量（单输入含 text+image/video → 单向量）；`false` 则各模态独立生成向量。 | 跨模态检索场景（如图文问答）务必设为 `true`；纯文本或单模态场景无需设置。 |

> ⚠️ 注意：嵌入模型一旦在知识库创建时选定（如 `text-embedding-v4`），即不可更改；若需升级，须重建知识库。

## 面向开发者，简洁实用

- **选型建议**：  
  - 中英文混合文本 → 用 `text-embedding-v4`（默认、平衡）或 `qwen3.7-text-embedding`（最新、稍高精度）；  
  - 图文/视频混合 → 用 `qwen3-vl-embedding`（推荐）或 `tongyi-embedding-vision-plus-2026-03-06`（固定维度、轻量）；  
  - 超大批量（>10k 条）→ 用异步批处理接口（`text-embedding-async-v2`），避免超时。

- **调用示例（同步小批量）**：
  ```python
  from openai import OpenAI
  client = OpenAI(base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1")
  
  # 文本嵌入（query 场景）
  resp = client.embeddings.create(
      model="qwen3.7-text-embedding",
      input=["用户想买一台轻薄笔记本"],
      dimensions=1024
  )
  query_vector = resp.data[0].embedding  # list[float]
  
  # 多模态融合嵌入（图文）
  resp = client.embeddings.create(
      model="qwen3-vl-embedding",
      input=[{
          "text": "一只橘猫坐在窗台上晒太阳",
          "image_url": "https://example.com/cat.jpg"
      }],
      enable_fusion=True
  )
  ```

- **避坑提示**：  
  - 不要混用 `text_type`：`query` 和 `document` 向量不可直接计算相似度；  
  - 向量维度必须一致才能计算余弦相似度（如 `query` 用 1024 维，则 `document` 向量也必须是 1024 维）；  
  - 多模态嵌入中，`image_url` 必须可公开访问（或使用百炼托管的 OSS URL），私有内网地址会失败。

## 关联主题页

- [knowledge base](../guides/knowledge-base.md)
- [vector and sort](../api/vector-and-sort.md)
- [llm application](../guides/llm-application.md)
- [frameworks](../api/frameworks.md)
- [use cases](../guides/use-cases.md)


