# 检索增强生成（RAG）

检索增强生成（Retrieval-Augmented Generation, RAG）是一种在大模型生成回答前，先从外部知识源检索相关内容并注入 Prompt 的技术，用于为大模型补充私有数据与最新信息，提升特定领域问答的准确性、降低幻觉。

## 在百炼平台的使用场景

百炼把 RAG 能力拆成"检索"与"生成"两段，围绕这两段提供了从托管到自建、从控制台到 API 的多层方案：

- **云端知识库（托管 RAG）**：在控制台创建知识库，完成数据导入、切片、向量化、检索召回、问答生成的完整链路。适合无需自定义切分/嵌入模型、希望开箱即用的场景。知识库功能仅在中国站**华北2（北京）**地域开通使用。
- **智能体应用挂载知识库**：为百炼智能体应用绑定私有知识库（最多 15 个），让问答覆盖私域问题，并可接入网站、企业微信、微信公众号、钉钉等渠道。
- **知识检索 / 知识问答 API**：通过 DashScope 应用网关的 HTTP REST 接口调用。知识检索接口只返回排序后的切片，供你自行拼 Prompt 调用大模型；知识问答接口通过 SSE 流式返回"规划 → 检索 → 生成"三个阶段，开箱即用。
- **本地知识库 RAG**：检索环节在本地执行、生成环节调用通义千问 API，适合需要灵活控制文档切分与嵌入模型的场景。
- **框架集成**：Python 侧用 LlamaIndex 构建云端或本地 RAG 应用；Java 侧用 Spring AI Alibaba 检索百炼知识库。均以 [API Key 鉴权](api-key.md)。
- **底层能力**：向量（Embedding）模型负责语义召回，排序（Rerank）模型负责二次精排，二者是 RAG 检索质量的基础。

## 检索链路与关键参数

标准检索流程为：Query 改写 → 向量 + 关键词混合检索 → Rerank 重排 → 相似度过滤 → 返回切片。

云端知识库检索侧的核心参数：

| 参数 | 取值 | 说明 |
| --- | --- | --- |
| 初步向量检索 TopK | 1–100（默认 50） | 向量语义召回切片数 |
| 初步关键词检索 TopK | 1–100（默认 50） | 关键词匹配召回切片数 |
| 排序模型 | qwen3-rerank / qwen3-rerank(hybrid) / qwen3-vl-rerank | [多模态](multimodal.md)库只能选 vl-rerank |
| 排序模式 | 问答 / 相似 / 自定义高级 | 问答模式按 QA 匹配度，相似模式按语义相似度 |
| 相似度阈值 | 0.01–1.0 | 过滤低分切片，过高会丢弃全部结果 |
| 最大召回数量 | 1–20 | 最终返回切片数 |

框架侧（LlamaIndex）常用参数：

- `similarity_top_k`：相似度最高的检索结果数（示例 5）。
- `similarity_cutoff`：过滤检索结果的最低相似度阈值（示例 0.4）。
- `top_n`：Rerank 后返回的结果数（示例 1）。
- `node_postprocessors`：可挂 `SimilarityPostprocessor`（阈值过滤）、`DashScopeRerank`（重排）等后处理器。

本地 RAG 应用侧的 RAG 参数：召回片段数（越大参考越多但噪声可能增加）、相似度阈值（越大参考越少、为 0 不剔除）、携带上下文轮数、模型温度等。

## 向量与排序模型

- **文本向量**：推荐 `text-embedding-v4`（Qwen3-Embedding 系列，支持 100+ 语种，维度可选 2048/1536/1024 默认/768/512 等），云端知识库多用 512 维；大规模向量化可用异步批处理接口。
- **排序（Rerank）**：推荐 `qwen3-rerank`（文本）与 `qwen3-vl-rerank`（[多模态](multimodal.md)）；`gte-rerank` 系列将于 2026 年下线，建议迁移。
- **[多模态](multimodal.md)向量**：`qwen3-vl-embedding` 支持文本/图像/视频映射到同一语义空间，用于跨模态检索；图片问答类知识库使用 `multimodal-embedding-v1`（1024 维）。

## 知识库配置要点

- **类型不可改**：创建时选定文档搜索 / 数据查询 / 图片问答 / 音视频搜索类，后续不可更改。
- **一次性配置项**：Meta 信息抽取、多轮对话改写与知识库绑定，创建时未设好则后续无法开启（除非重建）。
- **切片**：推荐"智能切分"，按语义自适应选择切片点，单切片 Token 上限 6,000。
- **规格**：标准版（0.03 元/小时、1 QPS）与旗舰版（按 RCU 计费、50–10,000 QPS）；RCU 按"向上取整（峰值 QPS ÷ 50）"估算。

## 效果优化与诊断

优化建议先建立评估基线（至少 100 组覆盖事实 / 比较 / 教程 / 分析型的评测用例），再按失败类型针对性改进：

- **没有相关知识**：补充知识库内容，优化源文件排版（去水印、避免合并/跨页单元格、优先 Markdown），统一实体表述，启用多轮对话改写。
- **召回不相关**：为文件加标签做前置过滤，或配置 Meta 元数据做结构化筛选。
- **切片不完整**：改用智能切分，人工检查并修正异常切片。
- **重排不佳**：通过命中测试反复调整相似度阈值与召回片段数（K 值 1–20）。

## 鉴权与调用约定

知识检索与问答接口属于 DashScope 应用网关体系（HTTP REST），使用 API Key Bearer 鉴权，Base URL 由业务空间 ID 拼接：`https://{workspaceId}.cn-beijing.maas.aliyuncs.com`。默认用户维度限流 25 QPS。这与 `CreateIndex`、`Retrieve` 等 OpenAPI RPC 接口不同。

## 关联主题页

- [knowledge base](../guides/knowledge-base.md)
- [knowledge](../api/knowledge.md)
- [frameworks](../api/frameworks.md)
- [application use cases](../guides/application-use-cases.md)
- [vector and sort](../api/vector-and-sort.md)
- [use cases](../guides/use-cases.md)
- [data connection overview](../guides/data-connection-overview.md)


