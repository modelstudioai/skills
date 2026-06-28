# 检索增强生成

检索增强生成（Retrieval-Augmented Generation，RAG）是一种在生成回答前，先从外部[知识库](knowledge-base.md)或私有数据中检索相关内容，再将检索结果与用户问题一起交给大模型生成答案的技术范式。它用于为大模型补充私有数据与最新信息，使应用能够准确回答特定领域问题，并降低幻觉。

## 在百炼平台中的使用

百炼平台的 RAG 能力以[知识库](knowledge-base.md)为核心载体，覆盖云端托管与本地部署两条路径，并可挂载到智能体、工作流或通过 SDK 集成到外部应用。

### 云端[知识库](knowledge-base.md) RAG

百炼知识库基于 RAG 技术提供文档搜索、数据查询、图片问答、音视频搜索四类能力。检索环节在云端执行，使用平台默认的智能文档切分与官方向量模型，不支持自定义切分与嵌入模型。开发者只需创建知识库、导入数据、配置检索参数，即可在应用中调用。知识库仅能在中国站华北2（北京）地域开通和使用，分为标准版与旗舰版两种规格。

集成方式：

- [智能体应用](agent-application.md)：在应用配置页添加知识库，可设置相似度阈值与权重；新版智能体（Agent 2.0）将知识库统一为工具，由智能体自主规划调用顺序。
- 工作流应用：将知识库节点拖入画布，配置 query 输入变量、选择固定或动态引入知识库、设置 TopK。
- 外部应用：通过阿里云百炼 SDK 调用检索能力，需为子账号授予 AliyunBailianDataFullAccess 策略并加入[业务空间](workspace.md)。

### 本地知识库 RAG

检索环节在本地执行，生成环节调用通义千问 API，适合需要灵活切分与自定义嵌入模型的场景。可改用本地部署的 GTE 文本向量模型（如 `iic/nlp_gte_sentence-embedding_chinese-large`），并自行控制召回片段数与相似度阈值。受 embedding API 限流影响，不建议传入超过 100 MB 的文件。

### 框架集成

百炼支持通过主流开源框架构建 RAG 应用：

- LlamaIndex（Python 3.9+）：读取本地文件上传到百炼应用数据、构建云端知识库与检索引擎。检索引擎可配置 `similarity_top_k`、`similarity_cutoff`、`top_n` 等参数，并通过 `SimilarityPostprocessor`、`DashScopeRerank` 等后处理器过滤与重排。
- Spring AI Alibaba（Java，Spring Boot 3.x，JDK 17+）：调用百炼智能体/工作流应用并检索百炼知识库，支持流式与非流式调用。

## 关键参数与配置

### 检索参数

- 相似度阈值：仅语义相似度高于此阈值的文本切片才会被召回。阈值过高（如 0.60）可能导致无召回结果，需结合数据分布调整。
- 召回片段数（K 值）：取值范围 1–20，调大可提升完整性但增加 [Token](token.md) 消耗与噪声；拼装后总长度超出大模型输入限制会被截断。
- 初步向量检索 TopK / 初步关键词检索 TopK：默认 50，取值范围 10–100，影响送入排序模型的切片数量与成本。
- 权重：仅在同类知识库之间生效，用于干预多知识库召回顺序。

### 向量与切片

- 向量模型：文档搜索、数据查询、音视频搜索类支持 text-embedding-v4、text-embedding-v3（均为 512 维）；图片问答类仅支持 multimodal-embedding-v1（1024 维），维度不可更改。
- 文本切片长度上限：单个切片 6,000 [Token](token.md)；编辑切片长度限制为 10–6,000 字符；单次查询最多召回 20 个切片。

### 规格与并发

- 标准版：1 QPS（固定），存储 ≤ 100 GB，0.03 元/知识库/小时。
- 旗舰版：50–10,000 QPS（对应 1–200 RCU），存储 ≤ 9,999 GB，0.2 元/RCU/小时。所需 RCU = 向上取整（检索峰值 QPS ÷ 50）。

## 生成阶段优化

生成答案阶段可更换为能力更强的商业模型（如千问-Max/Plus/QwQ），并优化提示词模板：限定输出范围、采用少样本提示、使用内容分隔标记，且 `${documents}` 占位符只出现一次。[智能体应用](agent-application.md)中可开启"展示回答来源"，以角标形式展示知识来源与源文件地址。

## 效果优化思路

当召回不完整或回答不准确时，建议先建立评测基线（至少 100 组问题，覆盖事实型/比较型/教程型/分析型），再按 RAG 三阶段诊断改进：

1. 建立索引：优化源文件排版（优先 Markdown、移除水印、避免复杂表格）、统一实体表述、启用多轮对话改写（仅创建时开启，后续无法补开）。
2. 检索召回：为文件添加标签过滤、配置元数据做结构化搜索、采用智能切分保留语义完整性、调整相似度阈值与召回片段数。
3. 生成答案：更换更强模型、优化提示词模板。

> **注意**：知识库一旦创建，无法再配置 metadata 抽取，也无法更改文档切分 chunk，请在创建时一次性规划好元数据与切片策略。相似度阈值与召回片段数需平衡召回率与噪声，并非越大越好。

## 关联主题页

- [knowledge base](../guides/knowledge-base.md)
- [frameworks](../api/frameworks.md)
- [application use cases](../guides/application-use-cases.md)
- [use cases](../guides/use-cases.md)
- [llm application](../guides/llm-application.md)
- [memory library overview](../guides/memory-library-overview.md)
- [data connection overview](../guides/data-connection-overview.md)


