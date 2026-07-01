# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种结合信息检索与大模型生成的技术范式，通过在生成回答前从外部知识源中检索相关内容，使大模型能够利用私有数据和最新信息，从而提升回答的准确性和可靠性。

## 在百炼平台中的应用场景

### 知识库问答

百炼知识库基于 RAG 技术构建，支持将非结构化文档（PDF、Word、Markdown 等）导入后自动切片、向量化，在用户提问时检索相关片段并交由大模型生成回答。适用于企业内部知识问答、智能客服、产品文档助手等场景。

### 智能体应用集成

智能体应用（Agent）可将知识库作为工具接入，由 Agent 自主规划何时调用检索。新版 Agent 2.0 将知识库与 MCP 工具统一管理，支持多轮规划搜索（Agentic RAG），能自动进行意图识别和 Query 改写。

### 工作流应用

在工作流编排中，可将知识库节点拖入画布，配置输入变量和 TopK 参数，实现固定流程中的检索增强环节。

### 外部应用集成

通过百炼 SDK 或 LlamaIndex、Spring AI Alibaba 等开源框架调用知识库检索能力，构建自定义 RAG 应用。LlamaIndex 支持云端知识库构建与本地知识库两种方案；Spring AI Alibaba 支持 Java 生态下的知识库检索集成。

### 多渠道接入

RAG 应用可通过 AppFlow 无代码连接流接入网站、企业微信、微信公众号、钉钉等渠道，快速实现基于私域知识的对话服务。

## RAG 检索流水线

百炼知识检索服务提供完整的检索流水线：

1. **Query 改写**（可选）：根据历史对话自动补全用户查询
2. **混合检索**：向量检索 + 关键词检索并行召回
3. **排序精排**（Rerank）：使用排序模型（如 qwen3-rerank）对召回结果二次排序
4. **加权返回**：输出最终相关片段供大模型生成回答

支持两种检索模式：
- **极速模式**：单轮检索后直接生成，低延时
- **多轮智能模式**：基于 Agent 的多轮规划搜索，自动进行意图识别和多次检索

## 关键参数与配置

### 索引阶段

| 参数 | 说明 |
|------|------|
| 切片方式 | 推荐"智能切分"（基于语义相关性自适应切分） |
| 向量模型 | text-embedding-v4（支持 64-2048 维可选）或 multimodal-embedding-v1（1024 维） |
| Meta 信息抽取 | 为切片附加元数据，提升检索精度 |
| 多轮对话改写 | 自动补全多轮对话中的指代（创建后不可开启） |

### 检索阶段

| 参数 | 说明 |
|------|------|
| 相似度阈值 | 仅高于此值的切片被召回，需反复调试 |
| 初步向量检索 TopK | 向量检索初步召回数量（1-100，默认 50） |
| 初步关键词检索 TopK | 关键词检索初步召回数量（1-100，默认 50） |
| 最大召回数量 | 最终返回的切片数（1-20） |
| 排序模型 | qwen3-rerank（文本）/ qwen3-vl-rerank（[多模态](multimodal.md)） |

### LlamaIndex 集成参数

| 参数 | 说明 |
|------|------|
| similarity_top_k | 相似度最高的检索结果数 |
| similarity_cutoff | 最低相似度阈值（过滤低相关结果） |
| top_n | Rerank 后返回的结果数 |
| response_mode | 响应聚合方式（如 tree_summarize） |

## RAG 效果优化方向

1. **检索无效**：补充知识库内容、优化源文件排版、消除实体歧义、启用多轮对话改写
2. **召回不相关**：添加文档标签过滤、定义 Meta 元数据实现结构化搜索
3. **切片不完整**：采用智能切分策略、人工检查修正切片内容
4. **重排不佳**：调低相似度阈值、增加召回片段数
5. **模型理解有误**：更换参数更多或专业能力更强的大模型

建议优化前先通过自动评测功能建立量化基线（至少 100 组测试用例），以客观衡量改进效果。

## 关联主题页

- [knowledge base](../guides/knowledge-base.md)
- [application use cases](../guides/application-use-cases.md)
- [use cases](../guides/use-cases.md)
- [frameworks](../api/frameworks.md)
- [llm application](../guides/llm-application.md)
- [data connection overview](../guides/data-connection-overview.md)
- [vector and sort](../api/vector-and-sort.md)


