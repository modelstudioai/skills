# 检索增强生成（RAG）

检索增强生成（Retrieval-Augmented Generation，RAG）是一种将外部知识检索与大模型生成相结合的技术范式，通过在推理时动态检索相关文档片段并注入上下文，使大模型能够基于私有数据和最新信息生成更准确的回答。百炼平台以 RAG 为核心技术构建了知识库服务体系，覆盖从数据导入、向量化、检索召回到问答生成的完整链路。

## 核心流程

百炼 RAG 的标准流水线分为四个阶段：

1. **文档解析与切片**：将非结构化文档（PDF、Word、Markdown 等）解析为文本，按语义切分为片段（推荐智能切分，单切片上限 6,000 Token）。
2. **向量化**：使用 Embedding 模型将切片转换为数值向量并存入向量索引。推荐 text-embedding-v4（Qwen3-Embedding 系列，支持 100+ 语种，维度可选 64–2048）。
3. **检索与排序**：接收用户 Query 后，经 Query 改写 → 向量 + 关键词混合检索 → Rerank 排序 → 加权返回相关切片。
4. **生成回答**：将检索到的切片与用户问题拼接为 Prompt，送入大模型生成最终回答。

## 在百炼平台的使用方式

### 知识库服务（托管式）

在百炼控制台创建知识库，平台托管全部 RAG 流程。支持四种知识库类型：

- **文档搜索类**：企业文档、产品手册等非结构化数据问答
- **数据查询类**：结构化 Excel/CSV，支持 NL2SQL
- **图片问答类**：基于 multimodal-embedding-v1 的视觉检索
- **音视频搜索类**：语音识别 + 视频帧提取，按时间轴结构化

平台提供两条独立服务线：
- **知识检索**（`POST /api/v1/indices/knowledge/search`）：仅返回排序后的切片，适合自定义生成流程
- **知识问答**（`POST /api/v2/apps/knowledge/chat`）：端到端问答，支持极速模式和 Agentic 多轮规划搜索，通过 SSE [流式输出](streaming.md)

### 框架集成（自建式）

通过开源框架在应用侧构建 RAG：

- **LlamaIndex**（Python）：使用 `DashScopeCloudIndex` 创建云端知识库，`DashScopeCloudRetriever` 执行检索，支持 `SimilarityPostprocessor` 和 `DashScopeRerank` 后处理
- **Spring AI Alibaba**（Java）：在 Spring Boot 3.x 中集成百炼知识库检索能力
- **本地 RAG**：检索在本地执行，生成调用通义千问 API，适合需要灵活切分和自定义嵌入模型的场景

### 渠道接入

RAG 应用可通过 AppFlow 无代码连接流接入网站、企业微信、微信公众号、钉钉等渠道。

## 关键参数与配置

### 检索参数

| 参数 | 取值范围 | 说明 |
| --- | --- | --- |
| 向量检索 TopK | 1–100（默认 50） | 向量语义召回切片数 |
| 关键词检索 TopK | 1–100（默认 50） | 关键词匹配召回切片数 |
| 排序模型 | qwen3-rerank / qwen3-rerank(hybrid) / qwen3-vl-rerank | [多模态](multimodal.md)库须选 vl-rerank |
| 相似度阈值 | 0.01–1.0 | 过滤低分切片，过高会丢弃全部结果 |
| 最大召回数量 | 1–20 | 最终返回切片数 |

### 向量模型选择

| 模型 | 向量维度 | 单行最大 Token | 适用场景 |
| --- | --- | --- | --- |
| text-embedding-v4 | 64–2048（默认 1024） | 8,192 | 推荐，100+ 语种 |
| text-embedding-v3 | 64–1024（默认 1024） | 8,192 | 50+ 语种 |
| multimodal-embedding-v1 | 1024 | - | 图片问答类知识库专用 |
| qwen3-vl-embedding | 2560 | - | 视觉理解（富文本文档） |

### 索引配置注意事项

- **Meta 信息抽取**和**多轮对话改写**在知识库创建后无法更改，必须在创建时配置
- 切片方式推荐智能切分，基于语义相关性自适应选择切片点
- 多知识库权重仅在同类型知识库之间生效

## 效果优化

当召回不完整或回答不准确时，建议按以下方向排查：

1. **补充知识**：优化源文件排版，统一实体表述，启用多轮对话改写
2. **改善召回**：为文件添加标签或 Meta 元数据做前置过滤
3. **优化切片**：改用智能切分，人工修正异常切片
4. **调整排序**：通过命中测试反复调整相似度阈值与 K 值；对列举/总结/比较类问题适当提高 K
5. **升级模型**：生成模型可选 qwen-max（效果优先）、qwen-plus（均衡）、qwen-turbo（速度优先）

## 关联主题页

- [knowledge base](../guides/knowledge-base.md)
- [application use cases](../guides/application-use-cases.md)
- [use cases](../guides/use-cases.md)
- [frameworks](../api/frameworks.md)
- [vector and sort](../api/vector-and-sort.md)
- [knowledge](../api/knowledge.md)


