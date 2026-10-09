# 向量嵌入

向量嵌入（Embedding）是将原始文本、图像、视频等非结构化数据映射到低维稠密实数向量空间的数学表示方法，其核心目标是让语义相似的内容在向量空间中距离更近。该表示不依赖关键词匹配，而是通过深度模型学习隐含的语义关系，是百炼平台实现语义检索、RAG、聚类与跨模态理解的基础能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **知识库（RAG）构建**：知识库创建时，系统自动调用指定嵌入模型（如默认 `text-embedding-v4`）对文档切片进行向量化，并构建向量索引；后续检索时，用户查询也被转为同空间向量，通过余弦相似度完成语义召回。
- **API 直接调用**：开发者可通过 `/embeddings` 接口（同步）或 `/text-embedding`（异步批处理）主动获取文本/多模态内容的向量，用于自定义检索、聚类、去重或特征工程。
- **多模态应用**：使用 `qwen3-vl-embedding` 或 `tongyi-embedding-vision-plus-2026-03-06` 等模型，支持文本+图像/视频混合输入，生成**融合向量**（单向量表征整体语义）或**独立向量**（各模态各1个向量），统一支撑跨模态搜索与理解。
- **框架集成**：LlamaIndex 中通过 `DashScopeEmbedding(model_name="text-embedding-v4")` 封装调用；Spring AI Alibaba 等框架亦可直接注入百炼嵌入能力，无需本地部署模型。
- **Agent 与工作流**：当 Agent 配置了知识库作为记忆源时，其底层检索链路全程依赖向量嵌入完成语义匹配；自定义工作流中也可显式插入嵌入节点，实现动态向量化与路由。

> ⚠️ 注意：知识库创建后，所选嵌入模型不可更改；若需切换，须重建知识库。云端知识库（`DashScopeCloudIndex`）强制使用平台预设嵌入模型，不支持自定义；本地向量索引（如 `VectorStoreIndex`）才支持完全自定义模型与切分策略。

## 关键参数和配置

| 参数 | 适用模型 | 说明 | 常用取值 |
|------|----------|------|-----------|
| `model` / `model_name` | 所有嵌入模型 | 指定具体嵌入模型名称 | `text-embedding-v4`, `qwen3.7-text-embedding`, `qwen3-vl-embedding`, `tongyi-embedding-vision-plus-2026-03-06` |
| `dimensions` | 多数文本/多模态模型 | 指定向量维度（影响存储、计算开销与表达能力） | `1024`（flash）、`1536`（async）、`2048`（v4）、`2560`（qwen3.7）；部分模型固定不可调 |
| `input` | 同步接口 | 文本列表（最多20条）或单条多模态 content 对象 | `["hello", "world"]` 或 `[{"text": "...", "image": "oss://..."}]` |
| `text_type` | 异步批处理模型（`text-embedding-async-*`） | 标明输入用途，影响向量空间对齐 | `"document"`（底库索引，默认）、`"query"`（检索查询） |
| `enable_fusion` | `qwen3-vl-embedding` | 启用融合向量模式（仅该模型需显式设置） | `true` / `false`；其他多模态模型通过将多模态内容置于同一 `content` 对象自动融合，**无需此参数** |
| `res_level` / `max_video_frames` | `tongyi-embedding-vision-plus-2026-03-06` | 控制图像分辨率级别与视频抽帧数量 | `res_level`: `"low"`/`"medium"`/`"high"`；`max_video_frames`: `1–32` |

## 面向开发者，简洁实用

- ✅ **首选同步调用**：小批量（≤20条文本）、低延迟场景，用 [OpenAI 兼容接口](openai-compatible-interface.md)最简：  
  ```bash
  curl -X POST https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/embeddings \
    -H "Authorization: Bearer YOUR_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"model": "text-embedding-v4", "input": ["苹果手机电池续航如何？"]}'
  ```

- ✅ **超大批量必用异步**：10万级文本请用 `text-embedding-async-v2`，设置请求头 `X-DashScope-Async: enable`，轮询 `task_id` 获取结果（有效期24小时）。

- ✅ **多模态融合写法**：不要传多个 `content`，而应合并为一个对象：
  ```json
  {
    "input": [{
      "text": "一只橘猫在窗台晒太阳",
      "image": "oss://bucket/1.jpg",
      "video": "oss://bucket/2.mp4"
    }]
  }
  ```
  此时自动启用融合向量（`tongyi-embedding-vision-plus-2026-03-06` 等模型无需 `enable_fusion=true`）。

- ⚠️ **避坑提示**：
  - 向量维度必须与下游检索/相似度计算逻辑一致（如 FAISS 索引需提前指定维度）；
  - `text_type="query"` 与 `"document"` 的向量**不可混用比较**，否则相似度失真；
  - 多模态 URL 必须配合 `X-DashScope-OssResourceResolve: enable` 请求头；
  - 临时文件 URL 48 小时过期，生产环境请走稳定 OSS 绑定或直传流程。

## 关联主题页

- [vector and sort](../api/vector-and-sort.md)
- [knowledge base](../guides/knowledge-base.md)
- [rag api](../api/rag-api.md)
- [frameworks](../api/frameworks.md)
- [more about models](../api/more-about-models.md)


