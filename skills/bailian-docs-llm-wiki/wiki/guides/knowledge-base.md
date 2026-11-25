# knowledge base

百炼 Knowledge（原 RAG）是面向企业级场景的知识库与检索服务，支持私有文档的自动解析、切片、向量化与索引构建，并通过 API 或控制台提供多路召回检索与基于大模型的流式问答能力。它作为连接私有知识与大模型推理的关键中间层，适用于客服知识库、内部文档助手、合规问答等场景。该能力已深度集成至百炼应用开发工作流中，开发者可快速接入自有数据源并生成可部署的知识服务。

## 支持的模型与功能

- **默认模型**：知识问答（`/v1/rag/qa`）默认调用 `qwen-max` 或 `qwen-plus`（具体取决于知识库创建时的模型配置），支持流式响应；检索阶段不依赖大模型，由向量引擎与关键词引擎协同完成多路召回。
- **核心功能**：
  - 多源数据接入：支持本地文件上传、OSS、MySQL、Excel/CSV 表格等 [数据集](../../raw/application-user-guide/knowledge-base.md)；
  - 智能切片与解析：自动识别 PDF/Word/Excel/PPT/TXT 等格式结构，保留标题层级与表格语义；
  - Agentic 多轮检索：支持基于用户历史交互动态优化召回策略，详见 [知识检索](../../raw/application-user-guide/knowledge-base.md)；
  - 流式问答服务：结合检索结果与 [prompt](prompt.md) 工程，输出带引用溯源的流式回答，见 [知识问答](../../raw/application-user-guide/knowledge-base.md)。

## 关键参数

| 参数 | 说明 | 示例值 | 是否必需 |
|------|------|--------|----------|
| `knowledge_id` | 知识库唯一标识符，创建后由平台分配 | `kb-xxxxxx` | 是（问答/检索接口均需） |
| `top_k` | 单次检索返回的最相关切片数 | `3`（默认）、`5`、`10` | 否（默认 3） |
| `enable_rerank` | 是否启用重排序（基于交叉编码器） | `true` / `false` | 否（默认 false，开启后延迟略增） |
| `stream` | 问答接口是否启用流式响应 | `true`（仅 `/v1/rag/qa` 支持） | 否（默认 false） |
| `retrieval_strategy` | 检索策略类型 | `hybrid`（默认，向量+关键词）、`vector_only`、`keyword_only` | 否 |

> **注意**：`retrieval_strategy=hybrid` 在部分旧版 SDK 中可能被误记为 `multi`，请以 [Knowledge API（原RAG API） 参考](../../raw/application-user-guide/knowledge-base.md) 中的最新字段名为准。

## 使用方式

1. **控制台快速验证**：通过 [Playground](../../raw/application-user-guide/knowledge-base.md) 直接上传文档、发起检索与问答，观察效果；
2. **API 集成**：
   - 创建知识库 → 获取 `knowledge_id`；
   - 调用 `/v1/rag/retrieve` 进行纯检索（返回切片 ID 与文本片段）；
   - 调用 `/v1/rag/qa` 发起问答（自动完成检索 + LLM 生成，支持 `stream=true`）；
3. **高级集成**：通过 MCP 协议对接 Agent 框架，或使用 CLI 批量管理文档生命周期（参见 [应用集成](../../raw/application-user-guide/knowledge-base.md)）。

## 限制和注意事项

- 单个知识库最大支持 100 万切片（超出后写入失败，需拆分知识库或调整切片策略）；
- PDF 文件单页最大尺寸限制为 10MB，超限将跳过解析；
- 表格类文档（Excel/CSV）中，列名将作为元数据注入切片，但不参与向量化（仅内容文本向量化）；
- 向量索引更新非实时：文档上传/删除后，索引重建通常在 30–120 秒内完成，期间检索可能命中旧结果；
- 免费试用额度仅覆盖基础解析与检索，高频问答调用需确认配额与计费项（详见控制台「用量中心」）。

## 来源文档

- [Knowledge 简介（原RAG 简介）](../../raw/application-user-guide/knowledge-base.md)


