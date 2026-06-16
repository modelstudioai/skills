# 检索增强生成

检索增强生成（Retrieval-Augmented Generation, RAG）是一种将信息检索与大语言模型生成相结合的技术范式：先从外部知识库中按语义相似度召回与用户问题最相关的文档切片，再将这些切片作为上下文注入大模型，由模型基于检索到的事实生成回答。RAG 使大模型能够回答训练数据之外的特定领域问题，同时降低幻觉风险。

## 在百炼平台中的应用场景

RAG 在百炼平台中被广泛用于以下场景：

- **知识库问答**：将企业私有文档（PDF、Word、Markdown 等）上传至百炼知识库，经解析、切分、向量化后存入向量库。用户提问时，系统按语义检索召回相关切片并交由大模型生成答案。
- **智能客服接入**：通过 AppFlow 将百炼智能体应用接入网站、微信公众号、企业微信、钉钉等渠道，结合知识库实现私域问答。
- **框架集成开发**：通过 LlamaIndex（Python）或 Spring AI Alibaba（Java）等框架快速构建 RAG 应用，将文档解析、云端索引构建、检索和生成串联为完整流水线。
- **本地 RAG 应用**：使用 Python + 百炼 Embedding API + Gradio 搭建本地检索 + 云端生成的 RAG 服务，支持临时文件上传和持久化知识库两种模式。

## RAG 流水线核心步骤

1. **文档解析与切分**：将非结构化文件解析为文本，按智能切分、定长、按页、按标题等策略拆分为切片（单切片上限 6000 Token）。
2. **向量化与索引**：使用向量模型（推荐 `text-embedding-v4`，512 维）将切片转为向量并写入向量库。
3. **语义检索**：用户查询同样向量化后，按相似度从向量库中召回 Top-K 切片，仅高于相似度阈值的切片被返回。
4. **排序（Rerank）**：可选地使用排序模型（推荐 `qwen3-rerank(hybrid)`）对召回结果进行二次排序，综合语义与 BM25 信号提升精度。
5. **生成回答**：将召回并排序后的切片注入大模型 Prompt，由模型生成最终回答。

## 关键参数与配置

| 参数 | 说明 | 推荐值 |
| --- | --- | --- |
| 向量模型 | 文档向量化模型 | `text-embedding-v4`（512 维） |
| 切片方式 | 文档拆分策略 | 智能切分（语义自适应） |
| 排序模型 | 检索结果重排序 | `qwen3-rerank(hybrid)` |
| 相似度阈值 | 低于此值的切片不召回 | 视场景调整（视觉理解默认 0.20） |
| 最大召回数量 | 排序后送入大模型的切片数 K | 上限 20 |
| similarity_top_k | LlamaIndex 检索返回最大结果数 | 5 |
| similarity_cutoff | LlamaIndex 最低相似度阈值 | 0.4 |

> **注意**：向量模型、切片方式等索引参数仅在知识库创建时可配置，创建后无法修改。相似度阈值可在应用侧覆盖知识库默认值。

## 效果优化建议

- **切片粒度**：过大导致噪声过多，过小丢失上下文。建议从智能切分开始，根据命中测试结果调整。
- **排序模式选择**：问答模式（默认）适合开放式问答；相似模式适合查找最接近的文档段落；自定义高级模式可用自然语言指令控制排序逻辑。
- **多轮对话改写**：开启后会用轻量模型基于历史对话补全当前查询，提升多轮场景的检索准确性。
- **命中测试**：在不调用大模型的前提下模拟提问，验证召回质量并对比不同排序模式的分数差异，用于调优阈值。
- **Meta 信息抽取**：为切片附加文件名、分类等元数据，提高特定场景下的检索精度。

## 来源文档

- 知识库（knowledge-base.md）
- 通过 LlamaIndex API 构建 RAG 应用（[frameworks](../api/frameworks.md).md）
- 典型应用场景接入方案（application-use-cases.md）
- 平台使用场景与最佳实践（use-cases.md）
- 文件管理 API（file-management-api.md）
- 数据连接概述（data-connection-overview.md）

## 关联主题页

- [knowledge base](../guides/knowledge-base.md)
- [frameworks](../api/frameworks.md)
- [application use cases](../guides/application-use-cases.md)
- [use cases](../guides/use-cases.md)
- [file management api](../api/file-management-api.md)
- [data connection overview](../guides/data-connection-overview.md)


