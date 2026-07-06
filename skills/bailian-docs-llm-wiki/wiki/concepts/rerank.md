# 重排序

重排序（Rerank）是检索流程中的二次精排环节：在向量或关键词召回得到候选文档后，由排序模型结合查询与文档的相关性重新打分并排序，把最相关的切片置顶，再交由后续生成或返回流程使用。

## 在百炼平台的使用场景

重排序贯穿于平台的检索增强与排序能力两条主线：

- **知识库 RAG 流水线**：知识检索服务的流程为 Query 改写 → 向量 + 关键词混合检索 → Rerank 排序 → 加权返回。排序模型对召回阶段返回的 TopK 切片做精排，再按相似度阈值过滤与最大召回数量截断，决定最终送入生成模型的上下文。知识问答服务在多轮智能模式下会反复触发该精排环节。
- **独立文本排序 API**：作为向量与排序模型能力的一部分，开发者可直接调用 rerank 接口，对自定义的候选文档列表按查询相关性排序，用于语义搜索、推荐系统、聚类分类等下游任务，无需绑定知识库。

## 模型选型

| 模型 | 最大文档数 | 单条最大 Token | 请求最大 Token | 特点 |
| --- | --- | --- | --- | --- |
| qwen3-vl-rerank | 文本 100 / 图片 40 / 视频 4 | 8,000 | 120,000 | 多模态，支持图文视频排序 |
| qwen3-rerank | 500 | 4,000 | - | 100+ 语种，高性能文本排序 |
| gte-rerank-v2 | - | - | 30,000 | 50+ 语种（2026-05-30 下线，建议迁移到 qwen3-rerank） |

知识库内置的排序模型选项包括 `qwen3-rerank`、`qwen3-rerank(hybrid)` 与 `qwen3-vl-rerank`；多模态知识库只能选 `qwen3-vl-rerank`。

## 关键参数

独立调用 rerank API 时的核心参数：

- `model`（必选）：模型名称
- `query`（必选）：查询内容，qwen3-vl-rerank 支持文本与图片两种查询模态
- `documents`（必选）：待排序文档列表
- `top_n`（可选）：返回排序后的前 N 个文档
- `instruct`（可选）：自定义排序任务说明，可指导模型采用不同排序策略（仅 qwen3-rerank 与 qwen3-vl-rerank）

知识库检索流程中的相关配置：

- **初步向量检索 TopK / 关键词检索 TopK**：1–100，默认 50，控制进入精排的候选规模
- **排序模式**：问答模式按 QA 匹配度排序，相似模式按语义相似度排序，自定义高级模式可自行调参
- **相似度阈值**：0.01–1.0，用于过滤精排后的低分切片，过高会丢弃全部结果
- **最大召回数量**：1–20，最终返回的切片数

## API 接口

不同模型走不同的专属接口，Base URL 均为业务空间 ID 拼接的专属域名：

- qwen3-rerank：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-api/v1/reranks`
- qwen3-vl-rerank / gte-rerank-v2：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank`

请求需携带 `Authorization: Bearer <API-Key>`，API Key 在控制台 API Key 页面获取，业务空间 ID 在业务空间管理页面获取。

## 调优建议

- 召回结果不理想时，先建立至少 100 组评测基线，再按失败类型针对性调整。
- 对「列举 / 总结 / 比较」类问题适当提高最大召回数量 K（1–20），并优先选按拼装长度避免超长截断。
- 通过命中测试反复调整相似度阈值与召回片段数，找到精排质量与上下文长度的平衡点。
- 多知识库召回时，相似度相同的切片优先返回权重高的库，但权重仅在同类知识库之间生效。

## 关联主题页

- [vector and sort](../api/vector-and-sort.md)
- [knowledge base](../guides/knowledge-base.md)
- [knowledge](../api/knowledge.md)


