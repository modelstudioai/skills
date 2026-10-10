# knowledge base

百炼平台的知识库（Knowledge Base）是面向企业级 RAG 应用的核心基础设施，支持私有文档的自动解析、切片、向量化与索引构建，并提供多路召回检索与大模型驱动的流式问答能力。其设计目标是将结构化/非结构化数据无缝接入大模型应用流水线，开发者可通过控制台或 API 快速集成。该能力在 [RAG 简介](../../raw/application-user-guide/knowledge-base.md) 中被定义为“企业级知识库与检索服务”。

## 支持的模型与功能

- **内置模型支持**：知识库默认使用百炼托管的 embedding 模型（如 `text-embedding-v1`）完成向量化；问答阶段可自由指定任意已授权的大模型（如 `qwen-max`、`qwen-plus`），需在请求时通过 `model_id` 显式传入。
- **核心功能**：
  - 多源数据接入：支持本地文件上传、OSS、MySQL、Excel/CSV 表格等，详见 [数据集](../../raw/application-user-guide/knowledge-base/data-connection-overview/data-connection.md)；
  - 智能切片与策略配置：支持按段落、标题、固定 token 长度或语义边界切分，可在 [创建知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md) 中设置；
  - 多路召回检索：融合关键词、向量、BM25 等策略，支持重排序（rerank）；
  - 流式问答（RAG-QA）：基于检索结果生成答案，支持 `stream=true` 返回增量响应。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `knowledge_id` | string | 是 | 知识库唯一标识，创建后由平台分配 |
| `query` | string | 是 | 用户原始查询文本（用于检索与问答） |
| `top_k` | int | 否 | 检索返回的最相关切片数，默认 3，最大 50 |
| `model_id` | string | 否（问答必填） | 问答所用大模型 ID，如 `qwen-max`；若未指定，使用知识库默认模型（如有） |
| `enable_rerank` | bool | 否 | 是否启用重排序，默认 `false`；启用后延迟略增但精度提升 |

> **注意**：`model_id` 在检索接口（`/v1/knowledge/retrieve`）中不生效，仅用于问答接口（`/v1/knowledge/qa`）；此行为与 [RAG API 参考](../../raw/application-api-reference/rag-api/rag-api-overview.md) 的接口定义一致，但部分旧版控制台文档误标为“检索也支持模型切换”，请以 API 文档为准。

## 使用方式

1. **控制台快速验证**：通过 [Playground](../../raw/application-user-guide/knowledge-base/playground.md) 实时调试检索与问答效果，无需编码；
2. **API 集成**：
   - 创建知识库 → 上传文档 → 等待状态变为 `active`；
   - 调用 `/v1/knowledge/retrieve` 获取上下文切片；
   - 或直接调用 `/v1/knowledge/qa` 进行端到端问答（自动完成检索+生成）；
3. **高级集成**：支持 MCP 协议对接 Agent 框架、CLI 批量管理、以及 Skill 封装为低代码组件。

## 限制和注意事项

- 单个知识库最大文档数：10,000 份；单文档最大体积：100 MB（PDF/Word）或 50 MB（纯文本）；
- 切片后单条 chunk 最大长度：2048 tokens（超出将被截断），该限制硬编码于解析引擎，不可配置；
- 向量索引更新非实时：文档上传/更新后，通常需 1–3 分钟完成索引构建，期间检索可能命中旧数据；
- 免费试用额度仅覆盖基础解析与检索，高并发问答或 rerank 调用计入额外计费项；
- 所有知识库数据默认加密存储于用户专属租户空间，不跨租户共享——该安全模型在 [RAG 简介](../../raw/application-user-guide/knowledge-base.md) 中明确声明。

## 来源文档

- [RAG 简介](../../raw/application-user-guide/knowledge-base.md)


