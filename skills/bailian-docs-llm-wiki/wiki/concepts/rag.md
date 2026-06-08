# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种通过在推理时检索外部知识库中的相关文本片段，将其注入大模型上下文以补充私有数据和最新信息的技术范式。百炼平台将 RAG 作为知识库的核心机制，使大模型能够回答特定领域问题而无需微调。

## 工作原理

RAG 的基本流程为：文件解析 → 切分 → 向量化 → 存入向量库；用户提问时按语义相似度召回切片 → 经 Rerank 排序 → 注入大模型上下文生成答案。百炼平台将这一流程封装为知识库服务，开发者只需上传文档并配置参数即可使用。

## 在百炼平台的使用场景

### 智能体应用中的 RAG

- **Agent 2.0（新版）**：知识库作为工具由智能体自主规划调用，支持通过标签限定查询范围。
- **Agent 1.0（旧版）**：知识库检索先行执行，再由模型决定是否调用其他工具。
- 从知识库召回的文本切片占用模型上下文窗口并增加输入 Token 消耗。

### 工作流应用中的 RAG

在工作流中拖入"知识库"节点，将输入变量绑定到 `query`；支持固定选择或通过 `CodeList` 变量动态引入知识库；下游大模型节点的提示词中插入 `result` 变量获取召回内容。

### 框架集成

- **LlamaIndex（Python）**：通过 `DashScopeCloudIndex` 创建云端知识库，`DashScopeRerank` 做语义重排，快速构建端到端 RAG 应用。
- **Spring AI Alibaba（Java）**：通过 `DashScopeDocumentRetriever` 检索百炼知识库切片，配合 `DocumentRetrievalAdvisor` 注入大模型对话。

### 本地 RAG 应用

基于 FastAPI + Gradio + LlamaIndex 调用百炼通义千问 API 与 Embedding 模型，在本地构建完整的 RAG 问答系统。

## 关键参数与配置

| 参数 | 说明 | 推荐值 |
| --- | --- | --- |
| 向量模型 | 文档向量化模型 | `text-embedding-v4`（512 维） |
| 切片方式 | 智能切分 / 按长度 / 按页 / 按标题 / 按正则 / 按符号 | 智能切分 |
| 排序模型 | 检索后 Rerank | `qwen3-rerank（hybrid）` |
| 相似度阈值 | 低于此值的切片不召回 | 视场景调整 |
| 最大召回数量 | 排序后送入大模型的切片数 K | 上限 20 |
| similarity_top_k | LlamaIndex 检索返回最大结果数 | 5 |
| similarity_cutoff | LlamaIndex 最低相似度阈值 | 0.4 |

> 以上参数中，向量模型和切片方式在知识库创建后不可修改；相似度阈值可在应用侧覆盖知识库默认值。

## Rerank 配置优先级

不同调用方式下 Rerank 生效的优先级不同：

- **旧版智能体/工作流**：应用内配置优先级高于知识库自身配置。
- **新版智能体（Agent 2.0）**：以知识库自身配置为准。
- **OpenAPI**：API 参数（`Retrieve` 接口）优先级高于控制台配置。

## 效果优化要点

- 使用命中测试验证召回质量，对比不同排序模式（问答模式 / 相似模式 / 自定义高级）下的分数差异。
- 合理设置切片大小与重叠字符数（建议 10%-25%）。
- 开启多轮对话改写可提升多轮场景下的检索准确度。
- 对长文档优先使用切片检索模式而非全文引用。

## 关联主题页

- [knowledge base](../guides/knowledge-base.md)
- [frameworks](../api/frameworks.md)
- [application use cases](../guides/application-use-cases.md)
- [llm application](../guides/llm-application.md)
- [data connection overview](../guides/data-connection-overview.md)


