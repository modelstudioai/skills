# 检索增强生成（RAG）

检索增强生成（Retrieval-Augmented Generation，RAG）是一种在大模型生成回答前，先从知识库中检索相关内容切片并注入上下文的技术，用于把企业私有数据、业务文档和最新信息接入大模型应用，提升回答的准确性与可追溯性。在百炼平台上，RAG 以知识库为核心载体，贯穿智能体、工作流、知识检索/知识问答服务以及开源框架集成等多种使用形态。

## 工作原理

一次典型的 RAG 调用包含以下环节：

1. **数据接入**：将 PDF、DOCX、Markdown、Excel、图片、音视频等数据解析、切片、向量化后存入知识库（向量模型如 `text-embedding-v4`、`multimodal-embedding-v1`）。
2. **检索**：用户 query 经向量检索 + 关键词检索召回候选切片，再由排序模型（如 `qwen3-rerank`、`qwen3-vl-rerank`）重排。
3. **过滤与拼装**：按相似度阈值、标签/元数据过滤、召回片段数筛选切片，拼入提示词。
4. **生成**：大模型（千问 Max/Plus/Turbo、千问 VL、DeepSeek 等）基于检索内容生成回答。

## 在百炼平台的使用场景

### 挂载到智能体应用

在智能体应用中添加文档知识库，配置调用方式（如"必定调用"）、相似度阈值、权重、标签/元数据过滤和召回片段数。新版智能体（Agent 2.0）将知识库统一视为工具，由模型自主规划调用时机，并支持通过文件标签 + 提示词规则限定检索范围。注意检索文本会占用上下文窗口并增加输入 Token 消耗。

### 挂载到工作流应用

在工作流中添加"知识库"节点，把输入变量（通常是 `${sys.query}`）传给检索节点，再将检索结果交给大模型节点生成。适合需要组合检索、工具调用、条件分支的固定流程。

### 知识检索 / 知识问答服务

- **知识检索**（`POST /api/v1/indices/knowledge/search`）：只返回排序后的切片，由开发者自行拼接 [prompt](../guides/prompt.md) 并调用大模型，适合需要自定义生成流程的场景。
- **知识问答**（`POST /api/v2/apps/knowledge/chat`）：服务端自动完成规划、检索、生成，通过 SSE 流式返回，适合开箱即用的端到端问答。

两类服务均支持最多绑定 15 个知识库，可配置权重、路由、TopK、排序模型、阈值和过滤条件；API 使用[业务空间](workspace.md)专属域名 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com`，Bearer [API Key 鉴权](api-key.md)，默认[限流](rate-limit.md) 25 QPS。

### 通过开源框架构建

- **LlamaIndex（Python）**：读取本地文件上传构建云端知识库，用 `as_retriever()` / `as_query_engine()` 构建检索与问答链路；云端方案使用官方智能切分与向量模型，不支持自定义切分或嵌入模型。
- **Spring AI Alibaba（Java）**：集成百炼智能体/工作流应用并检索百炼知识库，通过 `DASHSCOPE_API_KEY` / `AI_DASHSCOPE_API_KEY` 等环境变量配置鉴权。
- **本地知识库方案**：检索在本地执行、生成调用通义千问 API，适合需要自定义切分与嵌入模型（如本地 GTE 模型）的场景。

### 接入业务渠道

基于 RAG 的智能体应用可通过 AppFlow 快速接入网站、企业微信、微信公众号、钉钉等渠道，为应用添加私有知识库后即可覆盖私域问题。

## 关键参数与配置

| 参数 | 说明 |
| --- | --- |
| 相似度阈值 | 仅召回分数高于阈值的切片；过高漏召回，过低引入噪声 |
| 召回片段数 / TopK | 复杂问题可增大，但会增加上下文长度与 Token 成本 |
| 权重 | 多知识库联合检索时，相似度接近的切片优先返回高权重库 |
| 标签过滤 / 元数据过滤 | 限定检索范围，减少无关切片召回 |
| 排序（rerank）模型 | 对召回结果重排，如 `qwen3-rerank`、`gte-rerank` |
| 向量模型 | `text-embedding-v4`/`v3`（512 维）、`multimodal-embedding-v1`（1024 维），创建后不可修改 |
| Meta 信息抽取 / 多轮对话改写 | 需在创建知识库时配置，后补通常需重建知识库 |

LlamaIndex 侧对应参数为 `similarity_top_k`、`similarity_cutoff`、`top_n`（重排返回数），并可通过 `node_postprocessors` 做相似度过滤与重排后处理。

## 效果优化与注意事项

- **调优闭环**：通过评测集、命中测试、标签/元数据过滤、切片修正、阈值与召回片段数调整来定位并优化 RAG 效果。
- **监控**：检索调用可投递到 SLS，按知识库、[业务空间](workspace.md)、API 路径、错误码、耗时等维度分析告警。
- **地域限制**：知识库相关功能仅在中国站华北2（北京）地域开通和使用。
- **成本**：检索切片计入模型输入 Token；合理设置阈值和召回片段数可在效果与成本间取得平衡。

## 关联主题页

- [knowledge base](../guides/knowledge-base.md)
- [application use cases](../guides/application-use-cases.md)
- [llm application](../guides/llm-application.md)
- [frameworks](../api/frameworks.md)
- [use cases](../guides/use-cases.md)
- [knowledge](../api/knowledge.md)


