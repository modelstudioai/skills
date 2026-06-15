# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将外部知识检索与大模型生成相结合的技术范式。它在用户提问时，先从知识库中按语义相似度召回相关文档切片，再将这些切片作为上下文交由大模型生成答案，从而使模型能够回答训练数据之外的领域问题。

## 在百炼平台中的定位

百炼平台将 RAG 作为知识库的核心技术架构。整个流程包括：文件解析 → 文档切分 → 向量化（Embedding） → 存入向量库 → 语义检索召回 → 大模型生成回答。开发者可以通过控制台零代码搭建，也可以通过 SDK 和框架进行全代码集成。

## 典型使用场景

### 智能体应用 + 知识库

最常见的 RAG 场景。在百炼控制台创建智能体应用后，关联一个或多个知识库，应用在对话时自动检索知识库并生成回答。支持的知识库类型包括：

- **文档搜索**：面向 PDF、Word、Markdown 等非结构化文档，支持基础问答、图文并茂回复、视觉理解（富文本）、极速问答等子场景。
- **数据查询（NL2SQL）**：面向结构化 Excel / RDS 表格数据。
- **图片问答**：数据表中包含 `image_url` 字段，支持图搜场景。
- **音视频搜索**：按时间轴对齐语音识别、视频帧提取与剧情解析。

### 工作流应用中的知识库节点

在工作流中拖入「知识库」节点，将输入变量绑定到 `query`，支持固定选择或通过 `CodeList` 变量动态引入知识库，下游接大模型节点生成答案。

### 多渠道接入

RAG 应用可通过 AppFlow 连接流快速接入网站、微信公众号、企业微信、钉钉等渠道，实现私域知识问答的即时部署。

### 本地 RAG 应用

通过 Python + LlamaIndex + 百炼 Embedding API + Gradio 搭建本地检索 + 云端生成的 RAG 应用，适合需要本地化部署检索层的场景。

## 关键参数与配置

### 向量模型（Embedding）

| 模型 | 维度 | 适用场景 |
| --- | --- | --- |
| `text-embedding-v4`（推荐） | 512 | 文档/数据/音视频类知识库 |
| `text-embedding-v3` | 512 | 文档/数据/音视频类知识库 |
| `multimodal-embedding-v1` | 1024 | 图片问答类知识库 |
| `qwen3-vl-embedding` | — | 视觉理解场景（自动使用） |

### 文档切分

支持智能切分（推荐）、按长度（含重叠字符数，建议 10-25%）、按页、按标题、按正则、按符号等方式，单切片上限 6000 Token。

### 排序模型（Rerank）

- `qwen3-rerank（hybrid）`（推荐）：综合语义 + BM25
- `qwen3-rerank`：仅语义排序

排序模式分为问答模式（默认）、相似模式、自定义高级（支持自然语言指令，最长 200 字）。

### 检索参数

| 参数 | 说明 |
| --- | --- |
| 相似度阈值 | 仅高于此值的切片被召回；应用侧设置会覆盖知识库默认值 |
| 最大召回数量 | 排序后送入大模型的切片数 K，上限 20 |
| 多轮对话改写 | 用轻量模型基于历史对话补全当前查询，提升多轮场景检索准确度 |

## 框架集成

### LlamaIndex（Python）

通过 `DashScopeParse`（文档解析）、`DashScopeCloudIndex`（知识库管理）、`DashScopeRerank`（语义重排）三个核心组件构建 RAG 应用。关键参数：

```python
Settings.llm = DashScope(model_name="qwen-max")
similarity_top_k = 5        # 检索返回的最大结果数
similarity_cutoff = 0.4      # 最低相似度阈值
top_n = 1                    # 重排后返回的结果数
```

### Spring AI Alibaba（Java）

通过 `DashScopeDocumentRetriever` 检索百炼知识库，结合 `DocumentRetrievalAdvisor` 将检索结果注入大模型 Prompt。知识库需提前在控制台创建，`INDEX_NAME` 设置为知识库名称。

## RAG 效果优化

当召回不全或回答不准时，可从以下维度调优：

- **数据质量**：确保文档内容完整、格式规范，必要时做预处理清洗
- **切分策略**：根据文档结构选择合适的切分方式和切片大小
- **检索参数**：调整相似度阈值和召回数量 K
- **排序模型**：启用 Rerank 并选择合适的排序模式
- **Prompt 设计**：优化应用的 System Prompt，明确回答边界和格式要求
- **命中测试**：在不调用大模型的前提下模拟提问，验证召回质量并调优阈值

## 注意事项

- 知识库创建后，向量模型和知识库类型不可更改
- 排序模型不支持图片问答类知识库；视觉理解和极速问答场景不支持排序模式配置
- 应用侧的 Rerank 配置优先级高于知识库本身配置；API 参数优先级高于控制台配置
- 向量存储支持内置（免费）和 ADB-PG（自购计费）两种方案

## 关联主题页

- [knowledge base](../guides/knowledge-base.md)
- [frameworks](../api/frameworks.md)
- [use cases](../guides/use-cases.md)
- [application use cases](../guides/application-use-cases.md)
- [start using](../guides/start-using.md)
- [data connection overview](../guides/data-connection-overview.md)


